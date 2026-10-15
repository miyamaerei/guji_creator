# 全流程验证与冲突检测

> 版本：v1.0  
> 日期：2026-10-14

---

## 1. 还存在的问题

### 1.1 传递性合并冲突

**场景**：
- A 与 B 合并（置信度 0.80）
- B 与 C 合并（置信度 0.80）
- 但 A 与 C 的属性矛盾（如 birth_place 不同）

**问题**：传递闭包会放大错误

**解决**：
- 合并前检查传递链上的属性一致性
- 如果 A→B→C 链上有属性矛盾，标记为需要人工审核
- 不使用纯并查集，使用带约束的聚类

### 1.2 合并顺序依赖

**场景**：
- 先合并 A+B，再合并 (A+B)+C
- vs 先合并 B+C，再合并 A+(B+C)
- 可能得到不同的结果

**解决**：
- 按置信度降序合并（高置信度优先）
- 记录合并顺序，支持回退到任意状态

### 1.3 关系一致性

**场景**：
- A 有关系 A→X
- B 有关系 B→Y
- A 与 B 合并后，X 与 Y 是否应该合并？

**解决**：
- 合并后检查关系邻居
- 如果 X 与 Y 也高度相似，提示可能也需要合并
- 但不自动合并，只提示

### 1.4 性能问题

**场景**：
- 100 万节点，新来 1 个节点
- 如何快速找到可能冲突的节点？

**解决**：
- 分块索引（blocking）
- 近似匹配（LSH, MinHash）
- 分层过滤（先粗筛，再精筛）

---

## 2. 现有数据库唯一性验证

### 2.1 问题定义

给定现有数据库，找出所有**可能是同一实体**的节点对。

### 2.2 验证方法

#### 方法 1：名字重复检测

```python
def find_duplicate_names(con):
    """
    找出同类型、同名的节点对
    """
    rows = con.execute('''
        SELECT n1.uid, n1.label, n1.type, n1.book_id,
               n2.uid, n2.label, n2.type, n2.book_id
        FROM nodes n1
        JOIN nodes n2 ON n1.label = n2.label 
            AND n1.type = n2.type 
            AND n1.uid < n2.uid
        WHERE n1.label IS NOT NULL
        ORDER BY n1.type, n1.label
    ''').fetchall()
    
    duplicates = []
    for row in rows:
        duplicates.append({
            'uid_a': row[0],
            'uid_b': row[3],
            'label': row[1],
            'type': row[2],
            'book_a': row[3],
            'book_b': row[6],
            'method': 'exact_name',
            'confidence': 0.90
        })
    
    return duplicates
```

#### 方法 2：属性重复检测

```python
def find_duplicate_attributes(con, attr_keys=['birth_place', 'reign']):
    """
    找出关键属性相同的节点对
    """
    duplicates = []
    
    for key in attr_keys:
        # 提取所有有这个属性的节点
        nodes_with_attr = []
        for uid, label, typ, payload in con.execute('SELECT uid, label, type, payload FROM nodes'):
            if not payload:
                continue
            try:
                attrs = json.loads(payload).get('attributes', {})
                if key in attrs:
                    nodes_with_attr.append((uid, label, typ, attrs[key]))
            except:
                continue
        
        # 按属性值分组
        by_value = defaultdict(list)
        for uid, label, typ, val in nodes_with_attr:
            by_value[val].append((uid, label, typ))
        
        # 找出同值的节点对
        for val, nodes in by_value.items():
            if len(nodes) > 1:
                for i in range(len(nodes)):
                    for j in range(i+1, len(nodes)):
                        uid_a, label_a, typ_a = nodes[i]
                        uid_b, label_b, typ_b = nodes[j]
                        if typ_a == typ_b:  # 同类型
                            duplicates.append({
                                'uid_a': uid_a,
                                'uid_b': uid_b,
                                'label_a': label_a,
                                'label_b': label_b,
                                'type': typ_a,
                                'attr_key': key,
                                'attr_value': val,
                                'method': 'attribute_match',
                                'confidence': 0.75
                            })
    
    return duplicates
```

#### 方法 3：关系网络重叠检测

```python
def find_duplicate_relations(con):
    """
    找出关系网络高度重叠的节点对
    """
    # 构建关系邻接表
    adj = defaultdict(set)
    for subj, obj, pred in con.execute('SELECT subject_uid, object_uid, predicate FROM edges'):
        if subj and obj:
            adj[subj].add((obj, pred))
            adj[obj].add((subj, pred))
    
    duplicates = []
    
    # 对每对节点，计算关系网络重叠度
    uids = list(adj.keys())
    for i in range(len(uids)):
        for j in range(i+1, len(uids)):
            uid_a = uids[i]
            uid_b = uids[j]
            
            # 获取类型（过滤：只比较同类型）
            type_a = get_type(uid_a)
            type_b = get_type(uid_b)
            if type_a != type_b:
                continue
            
            # 计算 Jaccard 相似度
            neighbors_a = adj[uid_a]
            neighbors_b = adj[uid_b]
            
            if not neighbors_a or not neighbors_b:
                continue
            
            # 只看 object_uid，忽略 predicate
            objs_a = {obj for obj, pred in neighbors_a}
            objs_b = {obj for obj, pred in neighbors_b}
            
            overlap = len(objs_a & objs_b)
            total = len(objs_a | objs_b)
            
            if total > 0:
                similarity = overlap / total
                if similarity >= 0.7:  # 阈值
                    duplicates.append({
                        'uid_a': uid_a,
                        'uid_b': uid_b,
                        'type': type_a,
                        'similarity': similarity,
                        'shared_neighbors': list(objs_a & objs_b),
                        'method': 'relation_overlap',
                        'confidence': 0.70
                    })
    
    return duplicates
```

### 2.3 综合验证流程

```python
def validate_uniqueness(con):
    """
    全面验证数据库的唯一性
    """
    print("=== 唯一性验证 ===\n")
    
    # 1. 名字重复
    print("1. 检测名字重复...")
    name_dups = find_duplicate_names(con)
    print(f"   发现 {len(name_dups)} 对同名节点")
    
    # 2. 属性重复
    print("2. 检测属性重复...")
    attr_dups = find_duplicate_attributes(con)
    print(f"   发现 {len(attr_dups)} 对属性重复节点")
    
    # 3. 关系重复
    print("3. 检测关系重复...")
    rel_dups = find_duplicate_relations(con)
    print(f"   发现 {len(rel_dups)} 对关系重叠节点")
    
    # 4. 合并结果
    all_dups = name_dups + attr_dups + rel_dups
    print(f"\n总计: {len(all_dups)} 对可能的重复")
    
    # 5. 按置信度排序
    all_dups.sort(key=lambda x: -x['confidence'])
    
    # 6. 输出报告
    with open('uniqueness_validation_report.txt', 'w', encoding='utf-8') as f:
        f.write("=== 唯一性验证报告 ===\n\n")
        f.write(f"总重复对数: {len(all_dups)}\n")
        f.write(f"  - 名字重复: {len(name_dups)}\n")
        f.write(f"  - 属性重复: {len(attr_dups)}\n")
        f.write(f"  - 关系重复: {len(rel_dups)}\n\n")
        
        f.write("=== 高置信度重复（需要合并） ===\n")
        for dup in all_dups[:50]:
            f.write(f"{dup['uid_a']} <-> {dup['uid_b']}\n")
            f.write(f"  方法: {dup['method']}, 置信度: {dup['confidence']}\n")
            if 'label' in dup:
                f.write(f"  名字: {dup['label']}\n")
            if 'attr_key' in dup:
                f.write(f"  属性: {dup['attr_key']}={dup['attr_value']}\n")
            f.write("\n")
    
    return all_dups
```

---

## 3. 新节点冲突检测

### 3.1 问题定义

给定新节点 N，快速找出数据库中**可能与 N 冲突**的节点。

### 3.2 分块索引（Blocking）

**原理**：将节点分成若干块，只比较同块内的节点

```python
class BlockingIndex:
    def __init__(self, con):
        self.con = con
        self.blocks = self._build_blocks()
    
    def _build_blocks(self):
        """
        构建分块索引
        策略：按 (type, name_first_char) 分块
        """
        blocks = defaultdict(list)
        
        for uid, label, typ in self.con.execute('SELECT uid, label, type FROM nodes'):
            if not label:
                continue
            
            # 分块键：类型 + 名字首字
            block_key = (typ, label[0] if label else '')
            blocks[block_key].append(uid)
        
        return blocks
    
    def get_candidates(self, new_node):
        """
        获取新节点的候选冲突节点
        """
        typ = new_node['type']
        label = new_node['label']
        
        if not label:
            return []
        
        # 同块：类型 + 名字首字
        block_key = (typ, label[0])
        candidates = self.blocks.get(block_key, [])
        
        # 扩展：相邻块（首字相近）
        # 例如：同音字、形近字
        for related_char in get_related_chars(label[0]):
            related_key = (typ, related_char)
            candidates.extend(self.blocks.get(related_key, []))
        
        return list(set(candidates))
```

### 3.3 分层过滤

```python
def find_conflicts_for_new_node(new_node, blocking_index):
    """
    分层过滤：粗筛 → 精筛
    """
    # 1. 粗筛：分块索引
    candidates = blocking_index.get_candidates(new_node)
    print(f"粗筛: {len(candidates)} 个候选")
    
    # 2. 中筛：名字相似度
    name_similar = []
    for uid in candidates:
        label = get_label(uid)
        sim = string_similarity(new_node['label'], label)
        if sim >= 0.6:  # 阈值
            name_similar.append((uid, sim))
    
    print(f"中筛（名字相似）: {len(name_similar)} 个候选")
    
    # 3. 精筛：属性 + 关系
    conflicts = []
    for uid, name_sim in name_similar:
        node = get_node(uid)
        
        # 属性相似度
        attr_sim = attribute_similarity(new_node, node)
        
        # 关系相似度
        rel_sim = relation_similarity(new_node, node)
        
        # 综合分数
        score = 0.4 * name_sim + 0.3 * attr_sim + 0.3 * rel_sim
        
        if score >= 0.7:  # 阈值
            conflicts.append({
                'uid': uid,
                'score': score,
                'name_sim': name_sim,
                'attr_sim': attr_sim,
                'rel_sim': rel_sim
            })
    
    print(f"精筛（综合分数）: {len(conflicts)} 个冲突")
    
    return conflicts
```

### 3.4 完整流程

```python
def process_new_node(new_node):
    """
    处理新节点：检测冲突 → 合并或新建
    """
    # 1. 初始化分块索引
    blocking_index = BlockingIndex(con)
    
    # 2. 检测冲突
    conflicts = find_conflicts_for_new_node(new_node, blocking_index)
    
    if not conflicts:
        # 无冲突：创建新节点
        uid = create_new_node(new_node)
        print(f"创建新节点: {uid}")
        return uid
    
    # 3. 选择最佳冲突
    conflicts.sort(key=lambda x: -x['score'])
    best = conflicts[0]
    
    if best['score'] >= 0.85:
        # 高置信度：自动合并
        merged_uid = merge_nodes(new_node['uid'], best['uid'], 'auto_merge', best['score'])
        print(f"自动合并: {new_node['uid']} -> {merged_uid}")
        return merged_uid
    
    elif best['score'] >= 0.70:
        # 中置信度：加入审核队列
        add_to_review_queue(new_node['uid'], best['uid'], best['score'])
        print(f"加入审核队列: {new_node['uid']} vs {best['uid']}")
        return new_node['uid']
    
    else:
        # 低置信度：创建新节点
        uid = create_new_node(new_node)
        print(f"创建新节点（低置信度冲突）: {uid}")
        return uid
```

---

## 4. 性能优化

### 4.1 索引结构

```sql
-- 名字索引（用于快速查找同名）
CREATE INDEX idx_nodes_label ON nodes(label, type);

-- 属性索引（用于快速查找同属性）
CREATE INDEX idx_nodes_attributes ON nodes(json_extract(payload, '$.attributes.birth_place'));
CREATE INDEX idx_nodes_attributes ON nodes(json_extract(payload, '$.attributes.reign'));

-- 关系索引（用于快速查找关系邻居）
CREATE INDEX idx_edges_subject ON edges(subject_uid);
CREATE INDEX idx_edges_object ON edges(object_uid);
```

### 4.2 批量处理

```python
def batch_process_new_nodes(new_nodes):
    """
    批量处理新节点
    """
    # 1. 构建分块索引（一次性）
    blocking_index = BlockingIndex(con)
    
    # 2. 批量检测冲突
    all_conflicts = []
    for node in new_nodes:
        conflicts = find_conflicts_for_new_node(node, blocking_index)
        all_conflicts.append((node, conflicts))
    
    # 3. 批量合并/新建
    results = []
    for node, conflicts in all_conflicts:
        result = process_new_node_with_conflicts(node, conflicts)
        results.append(result)
    
    # 4. 更新分块索引
    for node in new_nodes:
        blocking_index.add_node(node)
    
    return results
```

---

## 5. 实施计划

### Phase 1: 唯一性验证

1. 实现 `find_duplicate_names`
2. 实现 `find_duplicate_attributes`
3. 实现 `find_duplicate_relations`
4. 生成验证报告

### Phase 2: 分块索引

1. 实现 `BlockingIndex`
2. 实现分块策略
3. 测试候选集大小

### Phase 3: 分层过滤

1. 实现名字相似度
2. 实现属性相似度
3. 实现关系相似度
4. 测试过滤效果

### Phase 4: 批量处理

1. 实现批量处理接口
2. 性能测试
3. 优化索引

---

## 6. 预期效果

### 唯一性验证

- **检测速度**：1000 节点/秒
- **准确率**：> 90%（基于 AI 判定的 ground truth）
- **召回率**：> 80%（覆盖大部分重复）

### 新节点冲突检测

- **检测速度**：100 节点/秒（使用分块索引）
- **候选集大小**：平均 50 个候选（从 100 万中筛选）
- **准确率**：> 85%

---

## 7. 下一步行动

1. **立即执行**：对现有测试数据库运行唯一性验证
2. **生成报告**：输出重复节点列表
3. **人工审核**：对高置信度重复进行合并
4. **实现分块索引**：为新节点冲突检测做准备
