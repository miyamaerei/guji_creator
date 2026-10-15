# 增量实体匹配与合并流程

> 版本：v1.0  
> 日期：2026-10-14

---

## 1. 问题定义

当新书加入联邦库时，需要：
1. **查重**：新实体是否已存在于联邦库？
2. **合并**：如果存在，如何合并到已有的 canonical 组？
3. **新建**：如果不存在，如何创建新的 canonical？

---

## 2. 整体流程

```
新书加入
  ↓
提取实体 (ent 层)
  ↓
对每个新实体 E:
  ↓
  ├─ Step 1: 名字精确匹配 → 候选集 C1
  ├─ Step 2: 别名/变体匹配 → 候选集 C2
  ├─ Step 3: 关系网络匹配 → 候选集 C3
  ├─ Step 4: 上下文相似度 → 候选集 C4
  ↓
  合并候选集 C = C1 ∪ C2 ∪ C3 ∪ C4
  ↓
  对每个候选 C_i:
    计算置信度 score(E, C_i)
  ↓
  选择最高分的候选 C_best
  ↓
  if score(E, C_best) ≥ threshold:
    合并到 C_best 的 canonical 组
  else:
    创建新的 canonical 组
  ↓
  更新索引
```

---

## 3. 四步匹配策略

### Step 1: 名字精确匹配

**原理**：跨书同名 → 大概率同一实体

**实现**：
```python
def step1_exact_name_match(new_entity, index):
    """
    new_entity: {label, type, book_id, ...}
    index: name → [uid] 的倒排索引
    """
    label = new_entity['label']
    typ = new_entity['type']
    
    # 查询同名实体
    candidates = index.get((label, typ), [])
    
    # 过滤：排除同书（同书同名可能是同名异人）
    candidates = [uid for uid in candidates 
                  if uid.split(':')[0] != new_entity['book_id']]
    
    return candidates  # 返回 uid 列表
```

**置信度**：0.90（高，但不绝对）

**适用类型**：person, place, work, institution

---

### Step 2: 别名/变体匹配

**原理**：字/号/谥号/官称等变体指向同一人

**实现**：
```python
def step2_alias_match(new_entity, alias_index):
    """
    alias_index: alias → [uid] 的倒排索引
    """
    label = new_entity['label']
    
    # 查询别名索引
    candidates = alias_index.get(label, [])
    
    return candidates
```

**别名来源**：
- ent_keys.json 的 aliases 字段
- name_rules.json 的 alias_map
- 从 original 文本提取的括注同位语

**置信度**：0.85（高，但需要别名词典质量）

**适用类型**：person（庙号/谥号/字/号）, place（古今地名）

---

### Step 3: 关系网络匹配

**原理**：如果两个实体共享相同的关系邻居 → 同一实体

**实现**：
```python
def step3_relation_match(new_entity, relation_graph):
    """
    relation_graph: uid → [(predicate, other_uid)] 的邻接表
    """
    # 获取新实体的关系邻居
    new_relations = get_relations(new_entity['uid'])
    
    if not new_relations:
        return []  # 无关系信息，跳过
    
    # 对每个候选，计算关系网络重叠度
    candidates = []
    for candidate_uid in get_all_entities(new_entity['type']):
        candidate_relations = get_relations(candidate_uid)
        
        # 计算 Jaccard 相似度
        overlap = count_shared_neighbors(new_relations, candidate_relations)
        total = max(len(new_relations), len(candidate_relations))
        
        if total > 0:
            similarity = overlap / total
            if similarity >= 0.7:  # 阈值
                candidates.append((candidate_uid, similarity))
    
    return candidates
```

**置信度**：0.70-0.90（取决于关系数量和质量）

**适用类型**：person, official（有关系的实体）

**限制**：需要新实体已经有关系边（rel/appt 层）

---

### Step 4: 上下文相似度

**原理**：从 original 文本提取特征，计算相似度

**实现**：
```python
def step4_context_match(new_entity, all_entities):
    """
    从 original 文本提取特征向量，计算余弦相似度
    """
    # 提取特征
    new_features = extract_features(new_entity['original'])
    # features = {era: [...], place: [...], office: [...], relation: [...]}
    
    candidates = []
    for entity in all_entities:
        if entity['type'] != new_entity['type']:
            continue
        
        entity_features = extract_features(entity['original'])
        
        # 计算特征重叠度
        era_overlap = jaccard(new_features['era'], entity_features['era'])
        place_overlap = jaccard(new_features['place'], entity_features['place'])
        office_overlap = jaccard(new_features['office'], entity_features['office'])
        
        # 加权平均
        similarity = 0.3 * era_overlap + 0.4 * place_overlap + 0.3 * office_overlap
        
        if similarity >= 0.6:  # 阈值
            candidates.append((entity['uid'], similarity))
    
    return candidates
```

**特征提取**：
```python
def extract_features(original_text):
    features = {
        'era': extract_reigns(original_text),      # 年号
        'place': extract_places(original_text),    # 地名
        'office': extract_offices(original_text),  # 官职
        'relation': extract_relations(original_text)  # 关联人物
    }
    return features
```

**置信度**：0.60-0.80（取决于文本质量和特征提取准确率）

**适用类型**：所有有 original 文本的实体

---

## 4. 置信度融合

对每个候选 C_i，综合四步的分数：

```python
def compute_final_score(new_entity, candidate, step_scores):
    """
    step_scores: {
        'step1': 0.90 or None,
        'step2': 0.85 or None,
        'step3': 0.75 or None,
        'step4': 0.65 or None
    }
    """
    # 加权平均（权重可调）
    weights = {
        'step1': 0.4,  # 名字精确匹配最重要
        'step2': 0.3,  # 别名匹配次之
        'step3': 0.2,  # 关系网络
        'step4': 0.1   # 上下文相似度
    }
    
    total_weight = 0
    weighted_sum = 0
    
    for step, score in step_scores.items():
        if score is not None:
            weighted_sum += weights[step] * score
            total_weight += weights[step]
    
    if total_weight == 0:
        return 0.0
    
    return weighted_sum / total_weight
```

---

## 5. 合并决策

```python
def merge_decision(new_entity, candidates_with_scores):
    """
    candidates_with_scores: [(uid, score), ...]
    """
    if not candidates_with_scores:
        return 'create_new'
    
    # 按分数排序
    candidates_with_scores.sort(key=lambda x: -x[1])
    best_uid, best_score = candidates_with_scores[0]
    
    # 阈值判定
    threshold = 0.75  # 可调
    
    if best_score >= threshold:
        return ('merge', best_uid, best_score)
    else:
        return 'create_new'
```

---

## 6. 合并操作

### 6.1 合并到已有 canonical

```python
def merge_to_canonical(new_uid, canonical_id, score):
    """
    将新实体合并到已有的 canonical 组
    """
    con = sqlite3.connect('kb_federation.sqlite')
    
    # 插入 members 表
    con.execute('''
        INSERT INTO members (canonical_id, uid, method, confidence, status, evidence_count)
        VALUES (?, ?, ?, ?, 'auto', 1)
    ''', (canonical_id, new_uid, 'incremental_match', score))
    
    # 更新 canonical 的 repr_label（如果新实体置信度更高）
    current_best = con.execute('''
        SELECT uid FROM members WHERE canonical_id=? ORDER BY confidence DESC LIMIT 1
    ''', (canonical_id,)).fetchone()
    
    if current_best and current_best[0] == new_uid:
        new_label = get_label(new_uid)
        con.execute('''
            UPDATE canonical SET repr_label=? WHERE canonical_id=?
        ''', (new_label, canonical_id))
    
    con.commit()
```

### 6.2 创建新 canonical

```python
def create_new_canonical(new_uid):
    """
    为新实体创建新的 canonical 组
    """
    con = sqlite3.connect('kb_federation.sqlite')
    
    # 生成新的 canonical_id
    row = con.execute('SELECT MAX(canonical_id) FROM canonical').fetchone()
    if row[0]:
        last_num = int(row[0].split('-')[1])
        new_canonical_id = f'canon-{last_num + 1:05d}'
    else:
        new_canonical_id = 'canon-00001'
    
    # 插入 canonical 表
    label = get_label(new_uid)
    typ = get_type(new_uid)
    con.execute('''
        INSERT INTO canonical (canonical_id, repr_type, repr_label, status)
        VALUES (?, ?, ?, 'open')
    ''', (new_canonical_id, typ, label))
    
    # 插入 members 表
    con.execute('''
        INSERT INTO members (canonical_id, uid, method, confidence, status, evidence_count)
        VALUES (?, ?, 'new_entity', 1.0, 'auto', 0)
    ''', (new_canonical_id, new_uid))
    
    con.commit()
    
    return new_canonical_id
```

---

## 7. 增量更新索引

合并后，更新倒排索引：

```python
def update_indexes(new_uid, label, typ, aliases):
    """
    更新名字索引和别名索引
    """
    # 名字索引
    name_index[(label, typ)].append(new_uid)
    
    # 别名索引
    for alias in aliases:
        alias_index[alias].append(new_uid)
```

---

## 8. 完整流程伪代码

```python
def process_new_book(book_id):
    """
    处理新书加入
    """
    # 1. 提取实体
    new_entities = extract_entities(book_id)
    
    # 2. 加载现有索引
    name_index = load_name_index()
    alias_index = load_alias_index()
    relation_graph = load_relation_graph()
    
    # 3. 对每个新实体
    for entity in new_entities:
        # 四步匹配
        c1 = step1_exact_name_match(entity, name_index)
        c2 = step2_alias_match(entity, alias_index)
        c3 = step3_relation_match(entity, relation_graph)
        c4 = step4_context_match(entity, get_all_entities(entity['type']))
        
        # 合并候选集
        all_candidates = set(c1 + c2 + [uid for uid, _ in c3] + [uid for uid, _ in c4])
        
        # 计算每个候选的分数
        candidates_with_scores = []
        for cand_uid in all_candidates:
            step_scores = {
                'step1': 0.90 if cand_uid in c1 else None,
                'step2': 0.85 if cand_uid in c2 else None,
                'step3': dict(c3).get(cand_uid),
                'step4': dict(c4).get(cand_uid)
            }
            score = compute_final_score(entity, cand_uid, step_scores)
            candidates_with_scores.append((cand_uid, score))
        
        # 合并决策
        decision = merge_decision(entity, candidates_with_scores)
        
        if isinstance(decision, tuple) and decision[0] == 'merge':
            _, best_uid, score = decision
            canonical_id = get_canonical_id(best_uid)
            merge_to_canonical(entity['uid'], canonical_id, score)
        else:
            create_new_canonical(entity['uid'])
        
        # 更新索引
        update_indexes(entity['uid'], entity['label'], entity['type'], entity.get('aliases', []))
    
    # 4. 提交
    commit()
```

---

## 9. 边界案例处理

### 9.1 同名异人

**场景**：两个"张伟"在不同时代

**处理**：
- Step 1 会找到同名候选
- Step 4 会检测时代冲突（era 不重叠）
- 最终分数降低，可能低于阈值 → 创建新 canonical

### 9.2 一名多人（历史人物 vs 地名）

**场景**："中山"既指中山王，也指中山地名

**处理**：
- 类型过滤：type 不同 → 不匹配
- 如果 type 相同，靠上下文区分

### 9.3 低置信度案例

**场景**：score = 0.70，接近阈值

**处理**：
- 标记为 `status='pending'`
- 进入人工审核队列
- 人工判定后标记为 `status='locked'`

---

## 10. 性能优化

### 10.1 索引结构

- **名字索引**：`(label, type) → [uid]`，用 SQLite 索引
- **别名索引**：`alias → [uid]`，用 SQLite 索引
- **关系图**：`uid → [(predicate, other_uid)]`，用内存 dict

### 10.2 批量处理

- 新书的所有实体一次性提取
- 批量查询索引，减少数据库访问
- 批量写入 members/canonical 表

### 10.3 增量更新

- 不重建整个联邦库
- 只处理新实体
- 索引增量更新

---

## 11. 监控与日志

```python
def log_incremental_match(new_uid, decision, score):
    """
    记录增量匹配日志
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'new_uid': new_uid,
        'decision': decision,
        'score': score,
        'status': 'auto' if score >= 0.75 else 'pending'
    }
    
    with open('incremental_match_log.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
```

---

## 12. 实施计划

1. **Phase 1**：实现 Step 1（名字精确匹配）+ 合并/新建逻辑
2. **Phase 2**：添加 Step 2（别名匹配）
3. **Phase 3**：添加 Step 3（关系网络匹配）
4. **Phase 4**：添加 Step 4（上下文相似度）
5. **Phase 5**：实现置信度融合 + 阈值校准
6. **Phase 6**：实现监控/日志 + 人工审核队列

---

## 13. 预期效果

- **准确率**：> 90%（基于 AI 判定的 ground truth）
- **召回率**：> 80%（覆盖大部分跨书同指实体）
- **处理速度**：1000 实体/分钟
- **人工介入率**：< 10%（低置信度案例）
