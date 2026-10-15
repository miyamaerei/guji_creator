# 属性冲突检测与解决机制

> 版本：v1.0  
> 日期：2026-10-14

---

## 1. 问题定义

**场景**：两个 node 正确判定为同一实体，但属性合并时出现冲突

**例子**：
- Node A: birth_place = "濠州"
- Node B: birth_place = "钟离"
- 实际：两者都对（濠州钟离是完整地名），但合并算法可能标记为冲突

**例子**：
- Node A: reign = "洪武"
- Node B: reign = "永乐"
- 实际：这是真正的冲突，需要人工判定

**需求**：
1. 检测属性冲突
2. 区分"假冲突"（互补信息）和"真冲突"（矛盾信息）
3. 提供属性级别的修正机制（不需要回退整个合并）

---

## 2. 属性冲突分类

### 2.1 冲突类型

| 类型 | 含义 | 例子 | 处理方式 |
|------|------|------|---------|
| **互补** | 两边信息互补，不矛盾 | "濠州" + "钟离" → "濠州钟离" | 自动合并 |
| **同义** | 两边信息等价，表述不同 | "朱元璋" = "朱重八" | 保留两者为别名 |
| **矛盾** | 两边信息矛盾 | "洪武" vs "永乐" | 人工判定 |
| **缺失** | 一边有，一边无 | A 有 birth_place，B 无 | 直接采用 |
| **多值** | 允许多个值 | 多个官职、多个字号 | 保留所有值 |

### 2.2 属性类型与冲突规则

```python
ATTRIBUTE_CONFLICT_RULES = {
    # 单值属性（冲突时需要解决）
    'single_value': {
        'birth_place': 'complement_or_conflict',  # 可互补或冲突
        'death_place': 'complement_or_conflict',
        'reign': 'conflict',  # 只能有一个
        'era': 'conflict',
    },
    
    # 多值属性（允许多个值）
    'multi_value': {
        'aliases': 'merge_all',  # 合并所有别名
        'roles': 'merge_all',  # 合并所有角色
        'offices': 'merge_all',  # 合并所有官职
    },
    
    # 层级属性（可合并为层级结构）
    'hierarchical': {
        'place': 'merge_hierarchy',  # 省-府-县
        'office': 'merge_hierarchy',  # 机构-职名
    }
}
```

---

## 3. 属性冲突检测

### 3.1 检测算法

```python
def detect_attribute_conflicts(node_a, node_b):
    """
    检测两个 node 的属性冲突
    返回：{
        'complementary': [...],  # 互补属性
        'synonymous': [...],     # 同义属性
        'conflicting': [...],    # 矛盾属性
        'missing': [...],        # 缺失属性
        'multi_value': [...]     # 多值属性
    }
    """
    attrs_a = node_a.get('attributes', {})
    attrs_b = node_b.get('attributes', {})
    
    conflicts = {
        'complementary': [],
        'synonymous': [],
        'conflicting': [],
        'missing': [],
        'multi_value': []
    }
    
    all_keys = set(attrs_a.keys()) | set(attrs_b.keys())
    
    for key in all_keys:
        val_a = attrs_a.get(key)
        val_b = attrs_b.get(key)
        
        # 缺失：一边有，一边无
        if val_a and not val_b:
            conflicts['missing'].append({
                'key': key,
                'value': val_a,
                'source': 'a'
            })
            continue
        if val_b and not val_a:
            conflicts['missing'].append({
                'key': key,
                'value': val_b,
                'source': 'b'
            })
            continue
        
        # 两边都有
        if val_a and val_b:
            # 多值属性
            if is_multi_value(key):
                conflicts['multi_value'].append({
                    'key': key,
                    'values': [val_a, val_b]
                })
                continue
            
            # 同义
            if is_synonymous(key, val_a, val_b):
                conflicts['synonymous'].append({
                    'key': key,
                    'values': [val_a, val_b]
                })
                continue
            
            # 互补
            if is_complementary(key, val_a, val_b):
                conflicts['complementary'].append({
                    'key': key,
                    'values': [val_a, val_b],
                    'merged': merge_complementary(key, val_a, val_b)
                })
                continue
            
            # 矛盾
            conflicts['conflicting'].append({
                'key': key,
                'value_a': val_a,
                'value_b': val_b
            })
    
    return conflicts
```

### 3.2 互补检测

```python
def is_complementary(key, val_a, val_b):
    """
    判断两个值是否互补
    """
    # 地名互补：如 "濠州" + "钟离" → "濠州钟离"
    if key in ['birth_place', 'death_place', 'place']:
        # 如果一个值是另一个的子串，可能是互补
        if val_a in val_b or val_b in val_a:
            return True
        # 如果是相邻地区，也可能是互补
        if are_adjacent_places(val_a, val_b):
            return True
    
    return False

def merge_complementary(key, val_a, val_b):
    """
    合并互补值
    """
    if key in ['birth_place', 'death_place', 'place']:
        # 地名：拼接
        if val_a in val_b:
            return val_b
        if val_b in val_a:
            return val_a
        # 尝试按层级拼接
        return f"{val_a}{val_b}"
    
    return f"{val_a}, {val_b}"
```

### 3.3 同义检测

```python
def is_synonymous(key, val_a, val_b):
    """
    判断两个值是否同义
    """
    # 人名同义
    if key in ['name', 'label']:
        return val_a in get_aliases(val_b) or val_b in get_aliases(val_a)
    
    # 地名同义（古今地名）
    if key in ['place', 'birth_place']:
        return are_synonymous_places(val_a, val_b)
    
    # 官职同义
    if key in ['office', 'role']:
        return are_synonymous_offices(val_a, val_b)
    
    return val_a == val_b
```

---

## 4. 属性冲突解决

### 4.1 自动解决

```python
def resolve_attribute_conflicts(conflicts):
    """
    自动解决可解决的冲突
    返回：{
        'resolved': {...},  # 已解决的属性
        'unresolved': [...]  # 需要人工判定的冲突
    }
    """
    resolved = {}
    unresolved = []
    
    # 1. 缺失属性：直接采用
    for item in conflicts['missing']:
        resolved[item['key']] = item['value']
    
    # 2. 互补属性：合并
    for item in conflicts['complementary']:
        resolved[item['key']] = item['merged']
    
    # 3. 同义属性：保留主值，其他加入别名
    for item in conflicts['synonymous']:
        resolved[item['key']] = item['values'][0]  # 保留第一个
    
    # 4. 多值属性：合并所有值
    for item in conflicts['multi_value']:
        resolved[item['key']] = merge_multi_value(item['key'], item['values'])
    
    # 5. 矛盾属性：需要人工判定
    for item in conflicts['conflicting']:
        unresolved.append(item)
    
    return {
        'resolved': resolved,
        'unresolved': unresolved
    }
```

### 4.2 人工判定队列

```python
def add_to_attribute_review(merged_uid, unresolved_conflicts):
    """
    将未解决的属性冲突加入人工审核队列
    """
    for conflict in unresolved_conflicts:
        con.execute('''
            INSERT INTO attribute_review_queue 
            (merged_uid, attr_key, value_a, value_b, status, created_at)
            VALUES (?, ?, ?, ?, 'pending', datetime('now'))
        ''', (
            merged_uid,
            conflict['key'],
            json.dumps(conflict['value_a'], ensure_ascii=False),
            json.dumps(conflict['value_b'], ensure_ascii=False)
        ))
    con.commit()
```

### 4.3 人工判定接口

```python
def resolve_attribute_conflict(review_id, decision, value, reviewer, reason):
    """
    人工判定属性冲突
    decision: use_a | use_b | use_both | use_custom
    value: 自定义值（decision=use_custom 时）
    """
    # 获取冲突信息
    row = con.execute('''
        SELECT merged_uid, attr_key, value_a, value_b
        FROM attribute_review_queue
        WHERE review_id=?
    ''', (review_id,)).fetchone()
    
    if not row:
        raise ValueError(f"Review {review_id} not found")
    
    merged_uid, attr_key, value_a_json, value_b_json = row
    value_a = json.loads(value_a_json)
    value_b = json.loads(value_b_json)
    
    # 根据决策确定最终值
    if decision == 'use_a':
        final_value = value_a
    elif decision == 'use_b':
        final_value = value_b
    elif decision == 'use_both':
        final_value = [value_a, value_b]
    elif decision == 'use_custom':
        final_value = value
    else:
        raise ValueError(f"Invalid decision: {decision}")
    
    # 更新 merged_nodes 的属性
    merged = get_merged_node(merged_uid)
    merged['attributes'][attr_key] = {
        'value': final_value,
        'source': f'resolved_by_{reviewer}',
        'resolved_at': datetime.now().isoformat(),
        'reason': reason
    }
    
    # 保存更新
    con.execute('''
        UPDATE merged_nodes
        SET attributes=?
        WHERE merged_uid=?
    ''', (json.dumps(merged['attributes'], ensure_ascii=False), merged_uid))
    
    # 标记为已解决
    con.execute('''
        UPDATE attribute_review_queue
        SET status='resolved', resolved_by=?, resolved_value=?, resolved_at=datetime('now'), reason=?
        WHERE review_id=?
    ''', (reviewer, json.dumps(final_value, ensure_ascii=False), reason, review_id))
    
    con.commit()
```

---

## 5. 属性修正（不回退合并）

### 5.1 属性修正日志

```sql
CREATE TABLE attribute_corrections (
  correction_id  TEXT PRIMARY KEY,
  merged_uid     TEXT NOT NULL,
  attr_key       TEXT NOT NULL,
  old_value      TEXT,
  new_value      TEXT NOT NULL,
  reason         TEXT,
  corrected_by   TEXT,
  created_at     TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (merged_uid) REFERENCES merged_nodes(merged_uid)
);
```

### 5.2 修正接口

```python
def correct_attribute(merged_uid, attr_key, new_value, reason, corrected_by):
    """
    修正 merged node 的属性（不回退整个合并）
    """
    # 获取当前值
    merged = get_merged_node(merged_uid)
    old_value = merged['attributes'].get(attr_key)
    
    # 记录修正日志
    correction_id = f"corr-{generate_id()}"
    con.execute('''
        INSERT INTO attribute_corrections 
        (correction_id, merged_uid, attr_key, old_value, new_value, reason, corrected_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        correction_id,
        merged_uid,
        attr_key,
        json.dumps(old_value, ensure_ascii=False) if old_value else None,
        json.dumps(new_value, ensure_ascii=False),
        reason,
        corrected_by
    ))
    
    # 更新属性
    merged['attributes'][attr_key] = {
        'value': new_value,
        'source': f'corrected_by_{corrected_by}',
        'corrected_at': datetime.now().isoformat(),
        'reason': reason,
        'correction_id': correction_id
    }
    
    con.execute('''
        UPDATE merged_nodes
        SET attributes=?
        WHERE merged_uid=?
    ''', (json.dumps(merged['attributes'], ensure_ascii=False), merged_uid))
    
    con.commit()
    
    return correction_id
```

### 5.3 查询修正历史

```python
def get_attribute_history(merged_uid, attr_key=None):
    """
    查询属性的修正历史
    """
    if attr_key:
        rows = con.execute('''
            SELECT correction_id, old_value, new_value, reason, corrected_by, created_at
            FROM attribute_corrections
            WHERE merged_uid=? AND attr_key=?
            ORDER BY created_at DESC
        ''', (merged_uid, attr_key)).fetchall()
    else:
        rows = con.execute('''
            SELECT correction_id, attr_key, old_value, new_value, reason, corrected_by, created_at
            FROM attribute_corrections
            WHERE merged_uid=?
            ORDER BY created_at DESC
        ''', (merged_uid,)).fetchall()
    
    history = []
    for row in rows:
        history.append({
            'correction_id': row[0],
            'attr_key': row[1] if len(row) > 6 else attr_key,
            'old_value': json.loads(row[2]) if row[2] else None,
            'new_value': json.loads(row[3]),
            'reason': row[4],
            'corrected_by': row[5],
            'created_at': row[6]
        })
    
    return history
```

---

## 6. 合并时的属性处理流程

```python
def merge_nodes_with_attributes(uid_a, uid_b, method, confidence):
    """
    合并两个 node，处理属性冲突
    """
    # 1. 读取两个 node
    node_a = read_node(uid_a)
    node_b = read_node(uid_b)
    
    # 2. 检测属性冲突
    conflicts = detect_attribute_conflicts(node_a, node_b)
    
    # 3. 自动解决可解决的冲突
    resolution = resolve_attribute_conflicts(conflicts)
    merged_attributes = resolution['resolved']
    unresolved = resolution['unresolved']
    
    # 4. 执行合并
    merged_uid = merge_nodes(uid_a, uid_b, method, confidence)
    
    # 5. 设置已解决的属性
    update_merged_attributes(merged_uid, merged_attributes)
    
    # 6. 未解决的冲突加入人工审核队列
    if unresolved:
        add_to_attribute_review(merged_uid, unresolved)
        # 标记为需要人工审核
        con.execute('''
            UPDATE merged_nodes SET status='needs_attribute_review' WHERE merged_uid=?
        ''', (merged_uid,))
    
    con.commit()
    
    return merged_uid, {
        'resolved': len(merged_attributes),
        'unresolved': len(unresolved)
    }
```

---

## 7. 实施计划

### Phase 1: 冲突检测

1. 实现 `detect_attribute_conflicts`
2. 定义属性类型与冲突规则
3. 实现互补/同义检测

### Phase 2: 自动解决

1. 实现 `resolve_attribute_conflicts`
2. 实现互补值合并逻辑
3. 实现多值属性合并

### Phase 3: 人工审核

1. 创建 `attribute_review_queue` 表
2. 实现审核接口
3. 实现 `resolve_attribute_conflict`

### Phase 4: 属性修正

1. 创建 `attribute_corrections` 表
2. 实现 `correct_attribute` 接口
3. 实现修正历史查询

---

## 8. 预期效果

- **自动解决率**：> 70% 的属性冲突可自动解决（互补/同义/多值）
- **人工审核率**：< 30% 需要人工判定（矛盾属性）
- **可追溯**：每个属性都有修正历史
- **可修正**：属性级别修正，不需要回退整个合并

---

## 9. 示例

### 示例 1：互补属性

```
Node A: birth_place = "濠州"
Node B: birth_place = "钟离"

检测：互补（钟离是濠州下属县）
合并：birth_place = "濠州钟离"
状态：自动解决
```

### 示例 2：矛盾属性

```
Node A: reign = "洪武"
Node B: reign = "永乐"

检测：矛盾（两个不同的年号）
合并：标记为冲突
状态：加入人工审核队列
人工判定：use_a（洪武）
理由：根据其他证据（关联人物、事件），A 更可靠
```

### 示例 3：属性修正

```
合并后：birth_place = "濠州钟离"
发现错误：应该是 "濠州"（钟离是误加）

修正：correct_attribute(merged_uid, 'birth_place', '濠州', '误加', 'reviewer')
结果：birth_place = "濠州"
历史：记录修正日志
```
