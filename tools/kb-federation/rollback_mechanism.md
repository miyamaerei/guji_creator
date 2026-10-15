# 合并回退机制设计

> 版本：v1.0  
> 日期：2026-10-14

---

## 1. 回退的核心挑战

合并操作涉及多个表的修改：
1. **merged_nodes 表**：创建合并后的 node
2. **nodes 表**：标记原 node 为 `merged_into`
3. **edges 表**：转移关系边到 merged node
4. **record_refs 表**：转移引用到 merged node
5. **canonical/members 表**：更新 canonical 组

回退需要**逆向操作**所有这些修改。

---

## 2. 回退策略

### 策略 1：软删除 + 回退日志（推荐）

**原理**：不物理删除任何数据，只标记状态，记录回退日志

**实现**：

```sql
-- 1. nodes 表增加 merged_into 字段
ALTER TABLE nodes ADD COLUMN merged_into TEXT;
ALTER TABLE nodes ADD COLUMN merged_at TEXT;
ALTER TABLE nodes ADD COLUMN merge_id TEXT;  -- 关联到 merge_log

-- 2. 创建 merge_log 表（记录所有合并操作）
CREATE TABLE merge_log (
  merge_id       TEXT PRIMARY KEY,      -- 合并操作 ID
  merged_uid     TEXT NOT NULL,         -- 合并后的 node uid
  source_uids    TEXT NOT NULL,         -- JSON: 来源 node uid 列表
  action         TEXT NOT NULL,         -- merge | rollback
  method         TEXT,                  -- 合并方法
  confidence     REAL,                  -- 合并置信度
  reason         TEXT,                  -- 合并/回退理由
  decided_by     TEXT,                  -- 决策者（auto | user_id）
  created_at     TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (merged_uid) REFERENCES merged_nodes(merged_uid)
);

-- 3. merged_nodes 表增加 status 字段
ALTER TABLE merged_nodes ADD COLUMN status TEXT DEFAULT 'active';  -- active | rolled_back
ALTER TABLE merged_nodes ADD COLUMN rolled_back_at TEXT;
ALTER TABLE merged_nodes ADD COLUMN rollback_merge_id TEXT;  -- 关联到回退日志
```

### 策略 2：版本快照

**原理**：每次合并前保存快照，回退时恢复快照

**实现**：

```sql
CREATE TABLE merge_snapshots (
  snapshot_id    TEXT PRIMARY KEY,
  merge_id       TEXT NOT NULL,         -- 关联到 merge_log
  snapshot_type  TEXT NOT NULL,         -- nodes | edges | refs
  snapshot_data  TEXT NOT NULL,         -- JSON: 快照数据
  created_at     TEXT DEFAULT (datetime('now'))
);
```

---

## 3. 回退算法

### 3.1 回退合并

```python
def rollback_merge(merge_id, reason, decided_by='auto'):
    """
    回退指定的合并操作
    """
    # 1. 查找合并日志
    log = con.execute('''
        SELECT merged_uid, source_uids, method, confidence
        FROM merge_log
        WHERE merge_id=? AND action='merge'
    ''', (merge_id,)).fetchone()
    
    if not log:
        raise ValueError(f"Merge {merge_id} not found")
    
    merged_uid, source_uids_json, method, confidence = log
    source_uids = json.loads(source_uids_json)
    
    # 2. 生成回退日志 ID
    rollback_id = f"rollback-{generate_id()}"
    
    # 3. 恢复 nodes 表（取消 merged_into 标记）
    for uid in source_uids:
        con.execute('''
            UPDATE nodes 
            SET merged_into=NULL, merged_at=NULL, merge_id=NULL
            WHERE uid=?
        ''', (uid,))
    
    # 4. 恢复 edges 表（转移回原 node）
    # 需要根据 merge_snapshot 或规则决定哪些边属于哪个原 node
    restore_edges(merged_uid, source_uids)
    
    # 5. 恢复 record_refs 表
    restore_refs(merged_uid, source_uids)
    
    # 6. 标记 merged_nodes 为已回退
    con.execute('''
        UPDATE merged_nodes
        SET status='rolled_back', rolled_back_at=datetime('now'), rollback_merge_id=?
        WHERE merged_uid=?
    ''', (rollback_id, merged_uid))
    
    # 7. 记录回退日志
    con.execute('''
        INSERT INTO merge_log (merge_id, merged_uid, source_uids, action, reason, decided_by)
        VALUES (?, ?, ?, 'rollback', ?, ?)
    ''', (rollback_id, merged_uid, source_uids_json, reason, decided_by))
    
    # 8. 更新 canonical/members（如果使用 canonical 组）
    rollback_canonical(merged_uid, source_uids)
    
    con.commit()
    
    return rollback_id
```

### 3.2 恢复关系边

```python
def restore_edges(merged_uid, source_uids):
    """
    将 merged node 的边恢复给原 nodes
    """
    # 方案 1：根据 merge_snapshot 恢复
    snapshot = get_snapshot(merged_uid, 'edges')
    if snapshot:
        for edge in snapshot:
            original_uid = edge['original_subject'] if edge['original_subject'] in source_uids else edge['original_object']
            con.execute('''
                UPDATE edges
                SET subject_uid=?, object_uid=?
                WHERE uid=?
            ''', (edge['original_subject'], edge['original_object'], edge['uid']))
        return
    
    # 方案 2：根据规则启发式恢复
    # 例如：如果边的 payload 中有 book_id，可以按 book_id 分配
    for edge in con.execute('SELECT * FROM edges WHERE subject_uid=? OR object_uid=?', (merged_uid, merged_uid)):
        # 启发式：根据边的 book_id 判断应该属于哪个原 node
        edge_book = edge['book_id']
        for uid in source_uids:
            if uid.startswith(edge_book):
                # 这条边应该属于这个原 node
                if edge['subject_uid'] == merged_uid:
                    con.execute('UPDATE edges SET subject_uid=? WHERE uid=?', (uid, edge['uid']))
                if edge['object_uid'] == merged_uid:
                    con.execute('UPDATE edges SET object_uid=? WHERE uid=?', (uid, edge['uid']))
                break
```

### 3.3 恢复引用

```python
def restore_refs(merged_uid, source_uids):
    """
    将 merged node 的引用恢复给原 nodes
    """
    # 类似 restore_edges，根据 snapshot 或启发式规则恢复
    snapshot = get_snapshot(merged_uid, 'refs')
    if snapshot:
        for ref in snapshot:
            con.execute('''
                UPDATE record_refs
                SET target_uid=?
                WHERE ref_id=?
            ''', (ref['original_target'], ref['ref_id']))
```

### 3.4 恢复 canonical 组

```python
def rollback_canonical(merged_uid, source_uids):
    """
    恢复 canonical 组
    """
    # 查找 merged_uid 对应的 canonical
    row = con.execute('''
        SELECT canonical_id FROM members WHERE uid=?
    ''', (merged_uid,)).fetchone()
    
    if not row:
        return
    
    canonical_id = row[0]
    
    # 删除 merged_uid 的 member 记录
    con.execute('DELETE FROM members WHERE uid=?', (merged_uid,))
    
    # 重新添加原 nodes 为 members
    for uid in source_uids:
        con.execute('''
            INSERT OR IGNORE INTO members (canonical_id, uid, method, confidence, status, evidence_count)
            VALUES (?, ?, 'rollback', 1.0, 'auto', 0)
        ''', (canonical_id, uid))
```

---

## 4. 快照机制

### 4.1 合并前保存快照

```python
def save_snapshot(merge_id, merged_uid, source_uids):
    """
    合并前保存快照
    """
    # 1. 保存 nodes 快照
    nodes_snapshot = []
    for uid in source_uids:
        row = con.execute('SELECT * FROM nodes WHERE uid=?', (uid,)).fetchone()
        nodes_snapshot.append(dict(row))
    
    con.execute('''
        INSERT INTO merge_snapshots (snapshot_id, merge_id, snapshot_type, snapshot_data)
        VALUES (?, ?, 'nodes', ?)
    ''', (f"snap-{generate_id()}", merge_id, json.dumps(nodes_snapshot, ensure_ascii=False)))
    
    # 2. 保存 edges 快照
    edges_snapshot = []
    for uid in source_uids:
        for edge in con.execute('SELECT * FROM edges WHERE subject_uid=? OR object_uid=?', (uid, uid)):
            edges_snapshot.append({
                'uid': edge['uid'],
                'original_subject': edge['subject_uid'],
                'original_object': edge['object_uid']
            })
    
    con.execute('''
        INSERT INTO merge_snapshots (snapshot_id, merge_id, snapshot_type, snapshot_data)
        VALUES (?, ?, 'edges', ?)
    ''', (f"snap-{generate_id()}", merge_id, json.dumps(edges_snapshot, ensure_ascii=False)))
    
    # 3. 保存 refs 快照
    refs_snapshot = []
    for uid in source_uids:
        for ref in con.execute('SELECT * FROM record_refs WHERE target_uid=?', (uid,)):
            refs_snapshot.append({
                'ref_id': ref['ref_id'],
                'original_target': ref['target_uid']
            })
    
    con.execute('''
        INSERT INTO merge_snapshots (snapshot_id, merge_id, snapshot_type, snapshot_data)
        VALUES (?, ?, 'refs', ?)
    ''', (f"snap-{generate_id()}", merge_id, json.dumps(refs_snapshot, ensure_ascii=False)))
```

### 4.2 获取快照

```python
def get_snapshot(merged_uid, snapshot_type):
    """
    获取指定类型的快照
    """
    row = con.execute('''
        SELECT ms.snapshot_data
        FROM merge_snapshots ms
        JOIN merge_log ml ON ms.merge_id = ml.merge_id
        WHERE ml.merged_uid=? AND ms.snapshot_type=?
        ORDER BY ms.created_at DESC
        LIMIT 1
    ''', (merged_uid, snapshot_type)).fetchone()
    
    if row:
        return json.loads(row[0])
    return None
```

---

## 5. 合并操作（带快照）

```python
def merge_nodes_with_snapshot(uid_a, uid_b, method, confidence):
    """
    合并两个 node，并保存快照
    """
    # 1. 生成 merge_id
    merge_id = f"merge-{generate_id()}"
    
    # 2. 保存快照（合并前）
    save_snapshot(merge_id, None, [uid_a, uid_b])
    
    # 3. 执行合并
    merged_uid = merge_nodes(uid_a, uid_b, method, confidence)
    
    # 4. 记录合并日志
    con.execute('''
        INSERT INTO merge_log (merge_id, merged_uid, source_uids, action, method, confidence, decided_by)
        VALUES (?, ?, ?, 'merge', ?, ?, 'auto')
    ''', (merge_id, merged_uid, json.dumps([uid_a, uid_b]), method, confidence))
    
    con.commit()
    
    return merge_id, merged_uid
```

---

## 6. 回退查询接口

### 6.1 查询合并历史

```python
def get_merge_history(uid):
    """
    查询某 node 的合并历史
    """
    rows = con.execute('''
        SELECT merge_id, action, method, confidence, reason, decided_by, created_at
        FROM merge_log
        WHERE merged_uid=? OR source_uids LIKE ?
        ORDER BY created_at DESC
    ''', (uid, f'%{uid}%')).fetchall()
    
    history = []
    for row in rows:
        history.append({
            'merge_id': row[0],
            'action': row[1],
            'method': row[2],
            'confidence': row[3],
            'reason': row[4],
            'decided_by': row[5],
            'created_at': row[6]
        })
    
    return history
```

### 6.2 查询可回退的合并

```python
def get_rollbackable_merges():
    """
    查询可以回退的合并（status='active'）
    """
    rows = con.execute('''
        SELECT ml.merge_id, ml.merged_uid, ml.source_uids, ml.method, ml.confidence, ml.created_at
        FROM merge_log ml
        JOIN merged_nodes mn ON ml.merged_uid = mn.merged_uid
        WHERE ml.action='merge' AND mn.status='active'
        ORDER BY ml.created_at DESC
    ''').fetchall()
    
    merges = []
    for row in rows:
        merges.append({
            'merge_id': row[0],
            'merged_uid': row[1],
            'source_uids': json.loads(row[2]),
            'method': row[3],
            'confidence': row[4],
            'created_at': row[5]
        })
    
    return merges
```

---

## 7. 人工审核队列

```python
def add_to_review_queue(merge_id, reason):
    """
    将合并加入人工审核队列
    """
    con.execute('''
        INSERT INTO review_queue (merge_id, reason, status, created_at)
        VALUES (?, ?, 'pending', datetime('now'))
    ''', (merge_id, reason))
    con.commit()

def review_merge(merge_id, decision, reviewer, reason):
    """
    人工审核合并
    decision: approve | reject | rollback
    """
    if decision == 'approve':
        con.execute('''
            UPDATE review_queue SET status='approved', reviewed_by=?, review_reason=?, reviewed_at=datetime('now')
            WHERE merge_id=?
        ''', (reviewer, reason, merge_id))
    elif decision == 'reject' or decision == 'rollback':
        rollback_merge(merge_id, reason=reason, decided_by=reviewer)
        con.execute('''
            UPDATE review_queue SET status='rejected', reviewed_by=?, review_reason=?, reviewed_at=datetime('now')
            WHERE merge_id=?
        ''', (reviewer, reason, merge_id))
    
    con.commit()
```

---

## 8. 实施计划

### Phase 1: 基础回退

1. 添加 `merged_into` 字段到 nodes 表
2. 创建 `merge_log` 表
3. 实现 `rollback_merge` 基础逻辑

### Phase 2: 快照机制

1. 创建 `merge_snapshots` 表
2. 实现 `save_snapshot` 和 `get_snapshot`
3. 合并前自动保存快照

### Phase 3: 审核队列

1. 创建 `review_queue` 表
2. 实现审核接口
3. 低置信度合并自动进入审核队列

### Phase 4: 查询接口

1. 实现 `get_merge_history`
2. 实现 `get_rollbackable_merges`
3. 提供 Web UI 查看/回退合并

---

## 9. 预期效果

- **可追溯**：每次合并都有日志，知道谁合并了谁
- **可回退**：任何合并都可以回退，数据不丢失
- **可审核**：低置信度合并进入人工审核
- **可查询**：提供完整的合并历史查询

---

## 10. 风险与缓解

| 风险 | 缓解措施 |
|------|---------|
| 快照数据量大 | 定期清理旧快照（保留 30 天） |
| 回退后数据不一致 | 回退后运行一致性检查 |
| 多次合并/回退混乱 | 用 merge_id 串联，严格追踪 |
| 性能影响 | 快照异步保存，不阻塞主流程 |
