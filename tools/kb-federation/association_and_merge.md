# 关联性与节点合并设计

> 版本：v1.0  
> 日期：2026-10-14

---

## 1. 问题定义

### 1.1 关联性（Association）

两个 node **不是同一个实体**，但有关系：
- **引用关系**：A 书中提到 B 书的人物
- **变体关系**：同一事件的不同叙述（轶闻）
- **层级关系**：上下级、父子、师徒
- **共现关系**：经常一起出现的人物

### 1.2 合并结构（Merge Structure）

两个 node **是同一个实体**，需要合并：
- 如何保留两边的名字变体？
- 如何保留两边的属性？
- 如何保留两边的关系？
- 如何保留两边的引用？

---

## 2. 关联性处理

### 2.1 关联类型分类

| 关联类型 | 含义 | 例子 | 表示方式 |
|---------|------|------|---------|
| **same_as** | 同一实体 | 朱元璋 = 明太祖 | canonical 合并 |
| **variant_of** | 变体/异文 | 同一事件的不同叙述 | assoc_edges |
| **cites** | 引用 | A 书引用 B 书 | assoc_edges |
| **about** | 关于 | 轶闻关于某人物 | assoc_edges |
| **related_to** | 一般关联 | 同时代、同地域 | assoc_edges |
| **part_of** | 部分-整体 | 县属于府 | edges (hierarchy) |
| **preceded_by** | 时间序列 | 前任/后任 | edges (temporal) |

### 2.2 关联表设计：assoc_edges

```sql
CREATE TABLE assoc_edges (
  from_uid       TEXT NOT NULL,      -- 起点 node uid
  to_uid         TEXT NOT NULL,      -- 终点 node uid
  assoc_type     TEXT NOT NULL,      -- 关联类型
  evidence_ref   TEXT,               -- 证据来源（record_refs.ref_id）
  confidence     REAL DEFAULT 1.0,   -- 置信度
  note           TEXT,               -- 备注
  created_at     TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (from_uid, to_uid, assoc_type),
  FOREIGN KEY (from_uid) REFERENCES nodes(uid),
  FOREIGN KEY (to_uid) REFERENCES nodes(uid)
);

CREATE INDEX idx_assoc_from ON assoc_edges(from_uid);
CREATE INDEX idx_assoc_to ON assoc_edges(to_uid);
CREATE INDEX idx_assoc_type ON assoc_edges(assoc_type);
```

### 2.3 关联生成规则

```python
def generate_assoc_edges(new_entity, existing_entities):
    """
    为新实体生成关联边
    """
    assocs = []
    
    # 1. variant_of: 同一事件/轶闻的不同叙述
    if new_entity['type'] in ('event', 'anecdote'):
        variants = find_variants(new_entity, existing_entities)
        for v in variants:
            assocs.append((new_entity['uid'], v['uid'], 'variant_of', 0.80))
    
    # 2. cites: 引用关系
    if has_citation(new_entity):
        cited = extract_citations(new_entity)
        for c in cited:
            assocs.append((new_entity['uid'], c['uid'], 'cites', 0.90))
    
    # 3. about: 轶闻关于某人物
    if new_entity['type'] == 'anecdote':
        subjects = extract_subjects(new_entity)
        for s in subjects:
            assocs.append((new_entity['uid'], s['uid'], 'about', 0.85))
    
    # 4. related_to: 共现关系
    cooccurring = find_cooccurrence(new_entity, existing_entities)
    for c in cooccurring:
        assocs.append((new_entity['uid'], c['uid'], 'related_to', 0.60))
    
    return assocs
```

### 2.4 关联查询

```python
def get_associations(uid, assoc_type=None):
    """
    查询某实体的所有关联
    """
    if assoc_type:
        rows = con.execute('''
            SELECT to_uid, assoc_type, confidence, note
            FROM assoc_edges
            WHERE from_uid=? AND assoc_type=?
        ''', (uid, assoc_type)).fetchall()
    else:
        rows = con.execute('''
            SELECT to_uid, assoc_type, confidence, note
            FROM assoc_edges
            WHERE from_uid=?
        ''', (uid,)).fetchall()
    
    return rows
```

---

## 3. 节点合并结构

### 3.1 合并的目标

当判定 node A 和 node B 是同一实体时，合并后的 node 应该：
- ✅ 保留 A 和 B 的所有名字变体（surfaces）
- ✅ 保留 A 和 B 的所有属性（attributes）
- ✅ 保留 A 和 B 的所有关系（edges）
- ✅ 保留 A 和 B 的所有引用（record_refs）
- ✅ 标记来源（哪些信息来自 A，哪些来自 B）

### 3.2 合并策略

#### 策略 1：Canonical 组（当前方案）

**原理**：不物理合并 node，而是通过 canonical 组逻辑关联

```
canonical: canon-00001
  repr_label: 朱元璋
  repr_type: person
  members:
    - kzz:01:ENT-0465 (明太祖)
    - kzz:01:ENT-0570 (朱元璋)
    - kzz:05:ENT-1011 (太祖高皇帝)
```

**优点**：
- 不丢失信息（每个 node 保持原样）
- 可追溯（知道每个名字来自哪本书）
- 可回滚（可以拆分 canonical）

**缺点**：
- 查询复杂（需要先查 canonical，再查 members）
- 关系分散（A 的关系在 A 上，B 的关系在 B 上）

#### 策略 2：物理合并（新方案）

**原理**：创建一个新的 merged node，包含所有信息

```sql
CREATE TABLE merged_nodes (
  merged_uid     TEXT PRIMARY KEY,      -- 合并后的 uid（如 merge-00001）
  canonical_id   TEXT,                  -- 关联的 canonical（可选）
  repr_label     TEXT,                  -- 代表名
  repr_type      TEXT,                  -- 类型
  surfaces       TEXT,                  -- JSON: 所有名字变体
  attributes     TEXT,                  -- JSON: 合并后的属性
  source_uids    TEXT,                  -- JSON: 来源 node uid 列表
  merged_at      TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (canonical_id) REFERENCES canonical(canonical_id)
);
```

**合并后的 payload 结构**：

```json
{
  "repr_label": "朱元璋",
  "type": "person",
  "surfaces": {
    "本名": ["朱元璋"],
    "庙号": ["明太祖", "太祖"],
    "谥号": ["太祖高皇帝"],
    "字": ["国瑞"]
  },
  "attributes": {
    "era": {"value": "明", "source": "kzz:01:ENT-0465"},
    "reign": {"value": "洪武", "source": "kzz:01:ENT-0570"},
    "birth_place": {"value": "濠州钟离", "source": "kzz:05:ENT-1011"},
    "role": {"value": "皇帝", "source": "kzz:01:ENT-0465"}
  },
  "source_uids": [
    "kzz:01:ENT-0465",
    "kzz:01:ENT-0570",
    "kzz:05:ENT-1011"
  ],
  "merge_history": [
    {
      "timestamp": "2026-10-14T10:00:00",
      "action": "merge",
      "from_uids": ["kzz:01:ENT-0465", "kzz:01:ENT-0570"],
      "method": "designator_miaohao",
      "confidence": 0.95
    }
  ]
}
```

### 3.3 合并算法

```python
def merge_nodes(uid_a, uid_b, method, confidence):
    """
    物理合并两个 node
    """
    # 1. 读取两个 node
    node_a = read_node(uid_a)
    node_b = read_node(uid_b)
    
    # 2. 生成 merged_uid
    merged_uid = f"merge-{generate_id()}"
    
    # 3. 合并 surfaces
    merged_surfaces = merge_surfaces(node_a, node_b)
    
    # 4. 合并 attributes
    merged_attributes = merge_attributes(node_a, node_b)
    
    # 5. 创建 merged node
    merged_payload = {
        'repr_label': choose_repr_label(node_a, node_b),
        'type': node_a['type'],
        'surfaces': merged_surfaces,
        'attributes': merged_attributes,
        'source_uids': [uid_a, uid_b],
        'merge_history': [{
            'timestamp': datetime.now().isoformat(),
            'action': 'merge',
            'from_uids': [uid_a, uid_b],
            'method': method,
            'confidence': confidence
        }]
    }
    
    con.execute('''
        INSERT INTO merged_nodes (merged_uid, repr_label, repr_type, surfaces, attributes, source_uids)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        merged_uid,
        merged_payload['repr_label'],
        merged_payload['type'],
        json.dumps(merged_surfaces, ensure_ascii=False),
        json.dumps(merged_attributes, ensure_ascii=False),
        json.dumps([uid_a, uid_b], ensure_ascii=False)
    ))
    
    # 6. 转移关系边
    transfer_edges(uid_a, merged_uid)
    transfer_edges(uid_b, merged_uid)
    
    # 7. 转移引用
    transfer_refs(uid_a, merged_uid)
    transfer_refs(uid_b, merged_uid)
    
    # 8. 标记原 node 为已合并
    con.execute('UPDATE nodes SET merged_into=? WHERE uid=?', (merged_uid, uid_a))
    con.execute('UPDATE nodes SET merged_into=? WHERE uid=?', (merged_uid, uid_b))
    
    con.commit()
    
    return merged_uid
```

### 3.4 合并细节

#### 3.4.1 合并 surfaces

```python
def merge_surfaces(node_a, node_b):
    """
    合并名字变体，按类型分组
    """
    surfaces = defaultdict(list)
    
    # 从 node_a 提取
    for kind, values in node_a.get('surfaces', {}).items():
        surfaces[kind].extend(values)
    
    # 从 node_b 提取
    for kind, values in node_b.get('surfaces', {}).items():
        for v in values:
            if v not in surfaces[kind]:  # 去重
                surfaces[kind].append(v)
    
    return dict(surfaces)
```

#### 3.4.2 合并 attributes

```python
def merge_attributes(node_a, node_b):
    """
    合并属性，冲突时保留两者
    """
    attributes = {}
    
    # 从 node_a 提取
    for key, val in node_a.get('attributes', {}).items():
        attributes[key] = val
    
    # 从 node_b 提取
    for key, val in node_b.get('attributes', {}).items():
        if key in attributes:
            # 冲突：保留两者
            if attributes[key]['value'] != val['value']:
                attributes[key] = {
                    'value': [attributes[key]['value'], val['value']],
                    'source': [attributes[key].get('source'), val.get('source')],
                    'conflict': True
                }
        else:
            attributes[key] = val
    
    return attributes
```

#### 3.4.3 转移关系边

```python
def transfer_edges(from_uid, to_uid):
    """
    将所有指向 from_uid 的边转移到 to_uid
    """
    # 出边
    con.execute('''
        UPDATE edges SET subject_uid=? WHERE subject_uid=?
    ''', (to_uid, from_uid))
    
    # 入边
    con.execute('''
        UPDATE edges SET object_uid=? WHERE object_uid=?
    ''', (to_uid, from_uid))
```

#### 3.4.4 转移引用

```python
def transfer_refs(from_uid, to_uid):
    """
    将所有指向 from_uid 的引用转移到 to_uid
    """
    con.execute('''
        UPDATE record_refs SET target_uid=? WHERE target_uid=?
    ''', (to_uid, from_uid))
```

---

## 4. 查询接口

### 4.1 查询合并后的 node

```python
def get_merged_node(merged_uid):
    """
    查询合并后的 node
    """
    row = con.execute('''
        SELECT merged_uid, repr_label, repr_type, surfaces, attributes, source_uids
        FROM merged_nodes
        WHERE merged_uid=?
    ''', (merged_uid,)).fetchone()
    
    if not row:
        return None
    
    merged_uid, repr_label, repr_type, surfaces, attributes, source_uids = row
    
    return {
        'uid': merged_uid,
        'label': repr_label,
        'type': repr_type,
        'surfaces': json.loads(surfaces),
        'attributes': json.loads(attributes),
        'source_uids': json.loads(source_uids)
    }
```

### 4.2 查询关联

```python
def get_all_associations(uid):
    """
    查询某实体的所有关联（包括 merged node）
    """
    # 如果是 merged node，查询所有 source_uids 的关联
    merged = get_merged_node(uid)
    if merged:
        uids = merged['source_uids']
    else:
        uids = [uid]
    
    assocs = []
    for u in uids:
        rows = con.execute('''
            SELECT to_uid, assoc_type, confidence, note
            FROM assoc_edges
            WHERE from_uid=?
        ''', (u,)).fetchall()
        assocs.extend(rows)
    
    return assocs
```

---

## 5. 混合方案（推荐）

**结合 canonical 组和物理合并的优点**：

1. **逻辑层**：用 canonical 组管理身份（可追溯、可回滚）
2. **物理层**：用 merged_nodes 提供统一查询接口（高性能）
3. **关联层**：用 assoc_edges 管理非同一性关联

```
canonical (逻辑身份)
  ↓
merged_nodes (物理合并，查询用)
  ↓
source nodes (原始数据，保留)
```

**查询流程**：
1. 用户查询 "朱元璋"
2. 找到 canonical: canon-00001
3. 找到 merged_node: merge-00001
4. 返回合并后的完整信息

---

## 6. 实施计划

### Phase 1: 关联表

1. 创建 assoc_edges 表
2. 实现关联生成逻辑
3. 实现关联查询接口

### Phase 2: 合并表

1. 创建 merged_nodes 表
2. 实现合并算法
3. 实现合并查询接口

### Phase 3: 混合方案

1. 实现 canonical → merged_nodes 的映射
2. 实现统一查询接口
3. 实现合并历史追踪

### Phase 4: 增量合并

1. 新书加入时，自动合并
2. 低置信度案例，进入人工审核
3. 人工审核后，触发合并

---

## 7. 预期效果

- **关联性**：支持 7 种关联类型，覆盖大部分古籍关联场景
- **合并结构**：保留所有信息，支持追溯和回滚
- **查询性能**：merged_nodes 提供统一接口，查询速度快
- **可维护性**：canonical 组管理身份，逻辑清晰
