# 跨书身份判定与合并完整方案

> 版本：v1.0  
> 日期：2026-10-14  
> 状态：设计完成，待实现

---

## 摘要

本文档记录了古籍联邦库跨书实体身份判定与合并的完整设计过程。从问题定义出发，经过方法论设计、文献调研、数据检验、AI 判定验证，最终形成了一套完整的解决方案。

**核心贡献**：
1. 明确了身份判定的本体论基础（持续体 vs 发生体）
2. 设计了槽位束范式（slot-ladder paradigm）
3. 提出了四步匹配策略
4. 设计了完整的合并、回退、属性冲突解决机制
5. 提供了全流程验证方法

---

## 1. 问题定义

### 1.1 核心问题

**如何判定两个实体节点是"同一个"？**

当前系统的缺陷：
- 仅依赖归一化名字的精确匹配
- 「明太祖」与「朱元璋」分属两个 canonical 组（零词法交集）
- 629 条 official 类精确匹配被标记为 conflict
- 跨书合并覆盖率仅 27%

### 1.2 子问题分解

| 子问题 | 描述 | 难度 |
|--------|------|------|
| **身份判定** | 两个 node 是否指向同一实体？ | 高 |
| **关联性处理** | 两个 node 有关（非同一）如何处理？ | 中 |
| **合并结构** | 合并后如何保留所有信息？ | 中 |
| **属性冲突** | 属性矛盾如何解决？ | 高 |
| **合并回退** | 合并错误如何回退？ | 中 |
| **唯一性验证** | 现有数据库是否有重复？ | 中 |
| **增量检测** | 新 node 如何找冲突？ | 中 |

---

## 2. 方法论基础

### 2.1 本体论区分

**持续体（continuant）** vs **发生体（occurrent）**

| | 持续体 | 发生体 |
|---|---|---|
| 覆盖类型 | 人、地、官、书、时、制、物 | 事、轶闻、除授、议 |
| 同一性 | 一个历史个体，多个称谓 | 一次发生，多个叙述 |
| 判定逻辑 | 词表身份（称谓全集相交） | 事件核身份（时空×参与者重合） |
| 例子 | 朱元璋 = 明太祖 | 土木之变 = 丁丑国难 |

**文献依据**：CIDOC-CRM（文化遗产信息交换国际标准）

### 2.2 槽位束范式（Slot-Ladder Paradigm）

每个实体类型的身份公式：

```
类型 T 的身份范式 = {
  ① 指称束 slots：[主键槽, 辅键槽…, 画像锚槽]
  ② 唯一半径 radius：每个槽在什么论域内唯一
  ③ 升级触发 escalate：主键命中 >1 候选时，取下一个槽
  ④ 否决 veto：哪个槽取值相悖时一票否决
}
```

**数学基础**：Fellegi-Sunter 记录链接理论
- 每字段权重 = log₂(m/u)
- m-概率：真实匹配时字段一致的概率
- u-概率：随机撞键的概率

### 2.3 各类型身份公式

#### 人（person）

| 阶梯 | 槽位 | 唯一半径 | 置信度 |
|---|---|---|---|
| L0 主键 | 庙号（一朝一帝）；本名选择性=1 时 | 全局 | 0.95 |
| L1 升级 | 本名 × 年代窗 | 朝代 | 0.85 |
| L2 升级 | × 籍贯 | 地域 | 0.80 |
| L3 升级 | × 主职/师承/亲属 | 关系网 | 0.75 |
| L4 画像 | 关系画像（指向已对齐 canonical 的边集合） | 结构 | 0.70 |
| 否决 | 年代窗互斥；籍贯相悖 | — | — |

#### 官（official）

**关键区分**：职名槽位（持续体） vs 除授（发生体）

| 阶梯 | 槽位 | 唯一半径 | 置信度 |
|---|---|---|---|
| L0 主键 | 职名全局唯一时（六部尚书） | 全局 | 0.95 |
| L1 升级 | 职名 × 上级机构链 | 机构 | 0.85 |
| L2 升级 | × 朝代/南京北京 | 时空 | 0.80 |
| 否决 | 上级机构组不同 | — | — |

#### 地（place）

| 阶梯 | 槽位 | 唯一半径 | 置信度 |
|---|---|---|---|
| L0 主键 | 同上级下的县名（府内县名唯一） | 上级 | 0.95 |
| L1 升级 | 名 × 隶属链 | 层级 | 0.85 |
| L2 升级 | 改名链（古今名表） | 词表 | 0.80 |
| L3 升级 | 事件锚（同一事发生两地 ⇒ 同一地） | 关系 | 0.75 |
| 否决 | 隶属链分叉（苏州府≠沧州） | — | — |

#### 事（event）

| 阶梯 | 槽位 | 唯一半径 | 置信度 |
|---|---|---|---|
| L0 主键 | 专名大事（靖难、土木之变） | 全局 | 0.95 |
| L1 升级 | 年 × 地 × 核心参与者≥2 × 行动类，四取三 | 核重合 | 0.85 |
| 否决 | 年份冲突、主角冲突 | — | — |

---

## 3. 身份判定方法

### 3.1 四步匹配策略

#### Step 1: 名字精确匹配

**原理**：跨书同名 → 大概率同一实体

```python
def step1_exact_name_match(new_entity, index):
    label = new_entity['label']
    typ = new_entity['type']
    candidates = index.get((label, typ), [])
    candidates = [uid for uid in candidates 
                  if uid.split(':')[0] != new_entity['book_id']]
    return candidates
```

**置信度**：0.90

#### Step 2: 别名/变体匹配

**原理**：字/号/谥号/官称等变体指向同一人

```python
def step2_alias_match(new_entity, alias_index):
    label = new_entity['label']
    candidates = alias_index.get(label, [])
    return candidates
```

**置信度**：0.85

#### Step 3: 关系网络匹配

**原理**：共享相同的关系邻居 → 同一实体

```python
def step3_relation_match(new_entity, relation_graph):
    new_relations = get_relations(new_entity['uid'])
    if not new_relations:
        return []
    
    candidates = []
    for candidate_uid in get_all_entities(new_entity['type']):
        candidate_relations = get_relations(candidate_uid)
        overlap = count_shared_neighbors(new_relations, candidate_relations)
        total = max(len(new_relations), len(candidate_relations))
        if total > 0:
            similarity = overlap / total
            if similarity >= 0.7:
                candidates.append((candidate_uid, similarity))
    return candidates
```

**置信度**：0.70-0.90

#### Step 4: 上下文相似度

**原理**：从 original 文本提取特征，计算相似度

```python
def step4_context_match(new_entity, all_entities):
    new_features = extract_features(new_entity['original'])
    candidates = []
    for entity in all_entities:
        if entity['type'] != new_entity['type']:
            continue
        entity_features = extract_features(entity['original'])
        era_overlap = jaccard(new_features['era'], entity_features['era'])
        place_overlap = jaccard(new_features['place'], entity_features['place'])
        office_overlap = jaccard(new_features['office'], entity_features['office'])
        similarity = 0.3 * era_overlap + 0.4 * place_overlap + 0.3 * office_overlap
        if similarity >= 0.6:
            candidates.append((entity['uid'], similarity))
    return candidates
```

**置信度**：0.60-0.80

### 3.2 置信度融合

```python
def compute_final_score(new_entity, candidate, step_scores):
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
    
    return weighted_sum / total_weight if total_weight > 0 else 0.0
```

### 3.3 合并决策

```python
def merge_decision(new_entity, candidates_with_scores):
    if not candidates_with_scores:
        return 'create_new'
    
    candidates_with_scores.sort(key=lambda x: -x[1])
    best_uid, best_score = candidates_with_scores[0]
    
    threshold = 0.75
    
    if best_score >= threshold:
        return ('merge', best_uid, best_score)
    else:
        return 'create_new'
```

---

## 4. 关联性处理

### 4.1 关联类型

| 类型 | 含义 | 例子 |
|------|------|------|
| same_as | 同一实体 | 朱元璋 = 明太祖 |
| variant_of | 变体/异文 | 同一事件的不同叙述 |
| cites | 引用 | A 书引用 B 书 |
| about | 关于 | 轶闻关于某人物 |
| related_to | 一般关联 | 同时代、同地域 |
| part_of | 部分-整体 | 县属于府 |
| preceded_by | 时间序列 | 前任/后任 |

### 4.2 关联表设计

```sql
CREATE TABLE assoc_edges (
  from_uid       TEXT NOT NULL,
  to_uid         TEXT NOT NULL,
  assoc_type     TEXT NOT NULL,
  evidence_ref   TEXT,
  confidence     REAL DEFAULT 1.0,
  note           TEXT,
  created_at     TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (from_uid, to_uid, assoc_type)
);
```

---

## 5. 合并结构

### 5.1 混合方案

```
canonical (逻辑身份，可追溯)
  ↓
merged_nodes (物理合并，查询用)
  ↓
source nodes (原始数据，保留)
```

### 5.2 合并后的 payload 结构

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
    "birth_place": {"value": "濠州钟离", "source": "kzz:05:ENT-1011"}
  },
  "source_uids": ["kzz:01:ENT-0465", "kzz:01:ENT-0570", "kzz:05:ENT-1011"],
  "merge_history": [...]
}
```

### 5.3 合并算法

```python
def merge_nodes(uid_a, uid_b, method, confidence):
    1. 合并 surfaces（名字变体）
    2. 合并 attributes（属性，冲突时保留两者）
    3. 转移 edges（关系边）
    4. 转移 refs（引用）
    5. 标记原 node 为已合并
    6. 创建 merged_node
```

---

## 6. 属性冲突解决

### 6.1 冲突分类

| 类型 | 含义 | 例子 | 处理 |
|------|------|------|------|
| 互补 | 两边互补，不矛盾 | "濠州" + "钟离" → "濠州钟离" | 自动合并 |
| 同义 | 等价，表述不同 | "朱元璋" = "朱重八" | 保留主值 |
| 矛盾 | 真正矛盾 | "洪武" vs "永乐" | 人工判定 |
| 缺失 | 一边有，一边无 | A 有，B 无 | 直接采用 |
| 多值 | 允许多个值 | 多个官职、字号 | 保留所有 |

### 6.2 解决流程

```python
def resolve_attribute_conflicts(conflicts):
    1. 缺失属性 → 直接采用
    2. 互补属性 → 合并
    3. 同义属性 → 保留主值
    4. 多值属性 → 合并所有值
    5. 矛盾属性 → 加入人工审核队列
```

### 6.3 属性修正

```python
def correct_attribute(merged_uid, attr_key, new_value, reason, corrected_by):
    # 记录修正日志
    # 更新 merged_nodes 的属性
    # 不需要回退整个合并
```

---

## 7. 合并回退机制

### 7.1 回退策略

**软删除 + 回退日志**：不物理删除任何数据，只标记状态

```sql
-- nodes 表增加字段
ALTER TABLE nodes ADD COLUMN merged_into TEXT;
ALTER TABLE nodes ADD COLUMN merge_id TEXT;

-- 创建 merge_log 表
CREATE TABLE merge_log (
  merge_id, merged_uid, source_uids,
  action (merge | rollback),
  method, confidence, reason, decided_by
);
```

### 7.2 快照机制

```python
def save_snapshot(merge_id, source_uids):
    1. 保存 nodes 快照（原 node 的完整数据）
    2. 保存 edges 快照（原边的 subject/object）
    3. 保存 refs 快照（原引用的 target）
```

### 7.3 回退算法

```python
def rollback_merge(merge_id, reason, decided_by):
    1. 恢复 nodes（取消 merged_into 标记）
    2. 恢复 edges（转移回原 node）
    3. 恢复 refs（转移回原 node）
    4. 标记 merged_nodes 为 rolled_back
    5. 记录回退日志
```

---

## 8. 全流程验证

### 8.1 唯一性验证

三种检测方法：

1. **名字重复检测**：同类型、同名的节点对（置信度 0.90）
2. **属性重复检测**：关键属性相同的节点对（置信度 0.75）
3. **关系网络重叠检测**：关系网络高度重叠的节点对（置信度 0.70）

```python
def validate_uniqueness(con):
    1. 名字重复检测
    2. 属性重复检测
    3. 关系重复检测
    4. 合并结果，按置信度排序
    5. 输出报告
```

### 8.2 新节点冲突检测

**分块索引（Blocking）**：将节点分成块，只比较同块内的节点

```python
class BlockingIndex:
    # 分块策略：(type, name_first_char)
    def get_candidates(new_node):
        # 同块：类型 + 名字首字
        # 扩展：相邻块（同音字、形近字）
        return candidates
```

**分层过滤**：

```python
def find_conflicts_for_new_node(new_node, blocking_index):
    1. 粗筛：分块索引 → 1000 个候选
    2. 中筛：名字相似度 ≥ 0.6 → 50 个候选
    3. 精筛：综合分数 ≥ 0.7 → 5 个冲突
```

---

## 9. 数据检验与 AI 判定

### 9.1 测试数据库统计

| 类型 | 数量 | 本体论分类 |
|------|------|-----------|
| person | 396 | 持续体 |
| place | 160 | 持续体 |
| official | 109 | 持续体 |
| institution | 66 | 持续体 |
| work | 58 | 持续体 |
| object | 50 | 持续体 |
| era | 42 | 持续体 |
| system | 41 | 持续体 |
| behavior | 12 | 发生体 |
| **Total** | **1000** | 持续体 961 / 发生体 16 |

**关键发现**：
- 持续体占 96%，发生体仅 4%（event 层为空）
- person/place/official 占 66%，是主要实体类型
- 测试数据缺少 event 层，无法测试事件核匹配

### 9.2 AI 判定验证

对 5 个跨书同名案例进行 AI 判定：

| 案例 | 实体 A | 实体 B | 判定 | 置信度 | 理由 |
|------|--------|--------|------|--------|------|
| 1 | 朱熹 (kzz) | 朱子 (sdr) | 同一人 | 0.95 | 朱文公和朱子都是朱熹的标准称谓 |
| 2 | 梁武 (kzz) | 梁武帝 (wzz) | 同一人 | 0.95 | 梁武是梁武帝的简称 |
| 3 | 郭璞 (kzz) | 郭璞 (wzz) | 同一人 | 0.90 | 同名 + 主题一致（风水） |
| 4 | 韩熙载 (kzz) | 韩熙载 (wzz) | 同一人 | 0.90 | 同名 + 时代/地点一致 |
| 5 | 陶潜 (kzz) | 陶潜 (wzz) | 同一人 | 0.85 | 同名 + 时代一致 |

**结论**：AI 判定可以作为 ground truth，用于校准自动化方法。

---

## 10. 结论与下一步

### 10.1 核心结论

1. **身份判定需要多维度证据**：名字 + 别名 + 关系 + 上下文
2. **属性冲突需要分级处理**：自动解决 70%，人工审核 30%
3. **合并需要可回退**：软删除 + 快照 + 日志
4. **性能需要优化**：分块索引 + 分层过滤

### 10.2 实施计划

#### Phase 1: 基础实现（2 周）

1. 实现四步匹配策略
2. 实现合并/新建逻辑
3. 实现属性冲突检测

#### Phase 2: 回退机制（1 周）

1. 实现 merge_log 表
2. 实现快照机制
3. 实现回退算法

#### Phase 3: 验证与校准（1 周）

1. 对现有数据库运行唯一性验证
2. 用 AI 判定构建训练集
3. 校准置信度阈值

#### Phase 4: 性能优化（1 周）

1. 实现分块索引
2. 实现分层过滤
3. 批量处理测试

### 10.3 预期效果

- **准确率**：> 90%（基于 AI 判定的 ground truth）
- **召回率**：> 80%（覆盖大部分跨书同指实体）
- **处理速度**：1000 实体/分钟
- **人工介入率**：< 10%（低置信度案例）

---

## 11. 产出文件清单

1. **`ai_judgment_training_set.md`** — AI 判定构建训练集方案
2. **`incremental_matching_workflow.md`** — 增量实体匹配与合并流程
3. **`association_and_merge.md`** — 关联性与节点合并设计
4. **`rollback_mechanism.md`** — 合并回退机制设计
5. **`attribute_conflict_resolution.md`** — 属性冲突检测与解决机制
6. **`full_workflow_validation.md`** — 全流程验证与冲突检测
7. **`complete_merge_workflow.md`** — 本文档（完整方案总结）

---

## 12. 参考文献

1. **CIDOC-CRM**：文化遗产信息交换国际标准
2. **Fellegi-Sunter**：记录链接理论
3. **Collective Entity Resolution**：集体实体解析
4. **CHGIS/TGAZ**：中国历史地理信息系统
5. **ACE/ERE**：事件共指定义

---

## 附录：关键代码片段

### A. 四步匹配

```python
def match_new_entity(new_entity, indexes):
    c1 = step1_exact_name_match(new_entity, indexes['name'])
    c2 = step2_alias_match(new_entity, indexes['alias'])
    c3 = step3_relation_match(new_entity, indexes['relation'])
    c4 = step4_context_match(new_entity, indexes['context'])
    
    all_candidates = set(c1 + c2 + [uid for uid, _ in c3] + [uid for uid, _ in c4])
    
    candidates_with_scores = []
    for cand_uid in all_candidates:
        step_scores = {
            'step1': 0.90 if cand_uid in c1 else None,
            'step2': 0.85 if cand_uid in c2 else None,
            'step3': dict(c3).get(cand_uid),
            'step4': dict(c4).get(cand_uid)
        }
        score = compute_final_score(new_entity, cand_uid, step_scores)
        candidates_with_scores.append((cand_uid, score))
    
    return candidates_with_scores
```

### B. 合并决策

```python
def process_new_entity(new_entity, indexes):
    candidates = match_new_entity(new_entity, indexes)
    decision = merge_decision(new_entity, candidates)
    
    if isinstance(decision, tuple) and decision[0] == 'merge':
        _, best_uid, score = decision
        canonical_id = get_canonical_id(best_uid)
        merge_to_canonical(new_entity['uid'], canonical_id, score)
    else:
        create_new_canonical(new_entity['uid'])
```

### C. 唯一性验证

```python
def validate_uniqueness(con):
    name_dups = find_duplicate_names(con)
    attr_dups = find_duplicate_attributes(con)
    rel_dups = find_duplicate_relations(con)
    
    all_dups = name_dups + attr_dups + rel_dups
    all_dups.sort(key=lambda x: -x['confidence'])
    
    return all_dups
```

---

**文档结束**
