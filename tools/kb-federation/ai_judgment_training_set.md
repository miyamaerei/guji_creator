# AI 判定构建训练集方案

> 版本：v1.0  
> 日期：2026-10-14

---

## 1. 目标

用 AI（LLM）对跨书实体进行身份判定，生成 ground truth 标签，用于：
- 校准自动化方法的置信度阈值
- 评估不同匹配策略的准确率/召回率
- 发现需要人工介入的边界案例

---

## 2. 抽样策略

### 2.1 分层抽样

按实体类型和跨书出现情况分层：

| 层 | 条件 | 目标数量 | 理由 |
|---|---|---|---|
| L1 跨书同名 | 同一名字出现在 ≥2 本书 | 50 对 | 最可能的合并候选 |
| L2 跨书变体 | 名字不同但可能是同一人（如 朱元璋/明太祖） | 30 对 | 测试别名识别能力 |
| L3 同书同名 | 同一本书内同名实体 | 20 对 | 检测同名异人 |
| L4 随机对照 | 随机抽取不同名字 | 50 对 | 负样本，测试不误并能力 |

**总计**：150 对判定任务

### 2.2 抽样实现

```python
# 伪代码
def sample_pairs():
    # L1: 跨书同名
    L1 = query('''
        SELECT n1.uid, n1.label, n1.book_id, n2.uid, n2.book_id
        FROM nodes n1 JOIN nodes n2 
        ON n1.label=n2.label AND n1.type=n2.type AND n1.book_id < n2.book_id
        WHERE n1.type IN ('person', 'place', 'official')
        LIMIT 50
    ''')
    
    # L2: 跨书变体（需要别名词典或人工标注）
    L2 = load_alias_pairs()  # 从 ent_keys 或人工提供
    
    # L3: 同书同名
    L3 = query('''
        SELECT n1.uid, n1.label, n2.uid
        FROM nodes n1 JOIN nodes n2
        ON n1.label=n2.label AND n1.type=n2.type AND n1.uid < n2.uid
        WHERE n1.book_id = n2.book_id
        LIMIT 20
    ''')
    
    # L4: 随机对照
    L4 = random_pairs(n=50)
    
    return L1 + L2 + L3 + L4
```

---

## 3. AI 判定 Prompt 设计

### 3.1 输入格式

对每对实体 (A, B)，提供：

```
实体 A:
  uid: kzz:02:ENT-0262
  书名: 困学纪闻 (kzz)
  名字: 朱熹
  类型: person
  上下文 (前 300 字): 【旧扁字】清凉广慧寺德庆堂榜...府学"泮宫"二字，朱文公行书...

实体 B:
  uid: sdr:31:ENT-954
  书名: 四部友议 (sdr)
  名字: 朱子
  类型: person
  上下文 (前 300 字): 朱子答张仁叔之问曰...

问题: 这两个实体是否指向同一个历史人物？
```

### 3.2 输出格式

```json
{
  "judgment": "same",  // same | different | uncertain
  "confidence": 0.95,
  "reasoning": "朱文公和朱子都是朱熹的标准称谓，且时代一致（南宋）",
  "evidence": [
    "name_variant: 朱熹=朱文公=朱子",
    "era_consistent: 南宋",
    "context_match: 都与儒学/理学相关"
  ]
}
```

### 3.3 Prompt 模板

```
你是明史专家，精通明代人物、地理、职官、事件。

给定两个古籍中提到的实体，请判定它们是否指向同一个历史实体。

判定依据：
1. 名字匹配：完全相同、已知变体（字/号/谥号/官称）、缩写形式
2. 时代一致：上下文暗示的时代不冲突
3. 主题/事迹一致：提到的事迹、地点、关联人物相符
4. 历史知识：你的历史知识库

输出 JSON 格式：
{
  "judgment": "same" | "different" | "uncertain",
  "confidence": 0.0-1.0,
  "reasoning": "简短理由",
  "evidence": ["证据1", "证据2", ...]
}

---

实体 A:
{entity_a_info}

实体 B:
{entity_b_info}

请判定：
```

---

## 4. 批量判定流程

### 4.1 流程

```
1. 抽样 → 生成 pair_list.json
2. 对每对 (A, B):
   a. 从数据库读取 A 和 B 的完整信息
   b. 构造 prompt
   c. 调用 LLM API
   d. 解析输出 JSON
   e. 写入 judgments.jsonl
3. 汇总统计
4. 导出为训练集格式
```

### 4.2 实现代码

```python
import json
import sqlite3
from openai import OpenAI  # 或其他 LLM API

def generate_training_set():
    con = sqlite3.connect('kb_test.sqlite')
    
    # 1. 抽样
    pairs = sample_pairs()
    
    # 2. 批量判定
    client = OpenAI()
    judgments = []
    
    for pair in pairs:
        uid_a, uid_b = pair['uid_a'], pair['uid_b']
        
        # 读取实体信息
        entity_a = read_entity(con, uid_a)
        entity_b = read_entity(con, uid_b)
        
        # 构造 prompt
        prompt = build_prompt(entity_a, entity_b)
        
        # 调用 LLM
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        # 解析输出
        judgment = parse_response(response.choices[0].message.content)
        judgment['uid_a'] = uid_a
        judgment['uid_b'] = uid_b
        
        judgments.append(judgment)
    
    # 3. 保存
    with open('ai_judgments.jsonl', 'w', encoding='utf-8') as f:
        for j in judgments:
            f.write(json.dumps(j, ensure_ascii=False) + '\n')
    
    return judgments

def read_entity(con, uid):
    row = con.execute('''
        SELECT n.uid, n.label, n.type, n.book_id, r.payload
        FROM nodes n
        JOIN records r ON n.book_id=r.book_id AND n.layer_key=r.layer_key AND n.local_id=r.local_id
        WHERE n.uid=?
    ''', (uid,)).fetchone()
    
    uid, label, typ, book_id, pl = row
    payload = json.loads(pl)
    
    return {
        'uid': uid,
        'label': label,
        'type': typ,
        'book_id': book_id,
        'text': payload.get('text'),
        'original': payload.get('original', '')[:300]  # 截取前 300 字
    }

def build_prompt(entity_a, entity_b):
    return f"""你是明史专家，精通明代人物、地理、职官、事件。

给定两个古籍中提到的实体，请判定它们是否指向同一个历史实体。

判定依据：
1. 名字匹配：完全相同、已知变体（字/号/谥号/官称）、缩写形式
2. 时代一致：上下文暗示的时代不冲突
3. 主题/事迹一致：提到的事迹、地点、关联人物相符
4. 历史知识：你的历史知识库

输出 JSON 格式：
{{
  "judgment": "same" | "different" | "uncertain",
  "confidence": 0.0-1.0,
  "reasoning": "简短理由",
  "evidence": ["证据1", "证据2", ...]
}}

---

实体 A:
  uid: {entity_a['uid']}
  书名: {entity_a['book_id']}
  名字: {entity_a['label']}
  类型: {entity_a['type']}
  上下文: {entity_a['original']}

实体 B:
  uid: {entity_b['uid']}
  书名: {entity_b['book_id']}
  名字: {entity_b['label']}
  类型: {entity_b['type']}
  上下文: {entity_b['original']}

请判定："""
```

---

## 5. 训练集格式

### 5.1 输出文件

`ai_judgments.jsonl`：

```jsonl
{"uid_a": "kzz:02:ENT-0262", "uid_b": "sdr:31:ENT-954", "judgment": "same", "confidence": 0.95, "reasoning": "朱文公和朱子都是朱熹的标准称谓", "evidence": ["name_variant", "era_consistent"]}
{"uid_a": "kzz:10:ENT-0817", "uid_b": "wzz:15:ENT-3669", "judgment": "same", "confidence": 0.95, "reasoning": "梁武是梁武帝的简称", "evidence": ["name_abbreviation", "context_match"]}
...
```

### 5.2 统计报告

```python
def generate_report(judgments):
    from collections import Counter
    
    judgment_counts = Counter(j['judgment'] for j in judgments)
    avg_confidence = sum(j['confidence'] for j in judgments) / len(judgments)
    
    print(f"Total pairs: {len(judgments)}")
    print(f"Same: {judgment_counts['same']}")
    print(f"Different: {judgment_counts['different']}")
    print(f"Uncertain: {judgment_counts['uncertain']}")
    print(f"Average confidence: {avg_confidence:.2f}")
    
    # 按类型统计
    type_stats = {}
    for j in judgments:
        typ = get_entity_type(j['uid_a'])
        if typ not in type_stats:
            type_stats[typ] = {'same': 0, 'different': 0, 'uncertain': 0}
        type_stats[typ][j['judgment']] += 1
    
    print("\nBy type:")
    for typ, counts in type_stats.items():
        print(f"  {typ}: same={counts['same']}, diff={counts['different']}, uncertain={counts['uncertain']}")
```

---

## 6. 应用：校准自动化方法

### 6.1 阈值校准

用 AI 判定的 ground truth，测试不同置信度阈值下的准确率/召回率：

```python
def calibrate_threshold(ai_judgments, auto_scores):
    """
    ai_judgments: AI 判定的 ground truth
    auto_scores: 自动化方法给出的置信度分数
    """
    thresholds = [0.5, 0.6, 0.7, 0.8, 0.9]
    
    for t in thresholds:
        tp = fp = tn = fn = 0
        
        for j, score in zip(ai_judgments, auto_scores):
            predicted_same = score >= t
            actual_same = j['judgment'] == 'same'
            
            if predicted_same and actual_same:
                tp += 1
            elif predicted_same and not actual_same:
                fp += 1
            elif not predicted_same and actual_same:
                fn += 1
            else:
                tn += 1
        
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
        
        print(f"Threshold {t}: precision={precision:.2f}, recall={recall:.2f}, F1={f1:.2f}")
```

### 6.2 错误分析

找出自动化方法判定错误但 AI 判定正确的案例，分析原因：

```python
def error_analysis(ai_judgments, auto_judgments):
    errors = []
    
    for ai, auto in zip(ai_judgments, auto_judgments):
        if ai['judgment'] != auto['judgment']:
            errors.append({
                'uid_a': ai['uid_a'],
                'uid_b': ai['uid_b'],
                'ai_judgment': ai['judgment'],
                'auto_judgment': auto['judgment'],
                'ai_reasoning': ai['reasoning'],
                'auto_score': auto['score']
            })
    
    # 分析错误模式
    print(f"Total errors: {len(errors)}")
    for e in errors[:10]:
        print(f"  {e['uid_a']} vs {e['uid_b']}: AI={e['ai_judgment']}, Auto={e['auto_judgment']}")
        print(f"    AI reasoning: {e['ai_reasoning']}")
```

---

## 7. 实施步骤

1. **实现抽样逻辑**：按分层策略抽取 150 对
2. **实现 AI 判定脚本**：调用 LLM API，批量判定
3. **生成训练集**：输出 `ai_judgments.jsonl`
4. **统计报告**：生成判定分布、按类型统计
5. **校准自动化方法**：用 ground truth 测试不同阈值
6. **错误分析**：找出自动化方法的弱点
7. **迭代改进**：根据错误分析调整匹配策略

---

## 8. 预期产出

- `ai_judgments.jsonl`: 150 对 AI 判定结果
- `calibration_report.txt`: 阈值校准报告
- `error_analysis.txt`: 错误案例分析
- 校准后的置信度阈值配置

---

## 9. 成本估算

- LLM API 调用：150 次 × ~$0.01/次 = ~$1.5
- 人工审核：~2 小时（审核 AI 判定 + 分析错误）
- 总成本：~$1.5 + 2 小时人工

---

## 10. 风险与缓解

| 风险 | 缓解措施 |
|---|---|
| AI 判定错误 | 人工审核低置信度案例（confidence < 0.8） |
| LLM API 不稳定 | 本地缓存 + 重试机制 |
| 样本不具代表性 | 分层抽样，覆盖各类型 |
| 历史知识不足 | 使用 GPT-4 或专业历史模型 |
