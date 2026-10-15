# 《万历野获编》知识工程 Schema 定义

> 本文件是各层 schema / 枚举 / ID / 触发词 / 示例条目的唯一真相源。
> 写源数据 / 打包器时读此文件；枚举值须与 `scripts/_kg_enums.py` 保持一致。

## 0. 通用规范

### 0.1 ID 命名空间

| 层 | ID 前缀 | 分配方式 |
|---|---|---|
| L0 底座 | `NN-NNN`（卷号-条序） | 打包器段位分配 |
| L1 实体 | `ENT-NNNN` | 全局顺序 |
| L2 规则 | `RULE-NN-NNN` | 卷×500 段位 |
| L5 事件 | `EVT-NN-NNN` | 卷×500 段位 |
| C1 任职 | `APPT-NN-NNN` | 卷×500 段位 |
| C3 关系 | `REL-NN-NNN` | 卷×500 段位 |
| C6 引书 | `CIT-NN-NNN` | 卷×500 段位 |
| C9 论说 | `OPN-NN-NNN` | 卷×500 段位 |
| C10 纪事 | `MING-NN-NNN` | 卷×500 段位 |
| C14 沿革 | `YHB-TME-NN-NNN` | 卷×500 段位 |
| REG 制度 | `REG-NN-NNN` | 卷×500 段位 |

### 0.2 跨层通用扩展字段

以下字段在多个层中重复出现，跨层语义一致：

| 字段 | 出现层 | 类型 | 说明 |
|---|---|---|---|
| `faction` | L1 / REL / APPT | enum | 政治派系 |
| `source_type` | L5 / MING | enum | 信息来源（亲历/传闻/文献/综合） |
| `vs_official_history` | L5 / MING / REG | enum | 与正史关系 |
| `firsthand_witness` | MING / OPN | enum | 亲历程度 |
| `reign_period` | 几乎所有层 | enum | 年号时段（用 REIGN_ORDER 排序） |

### 0.3 枚举治理

- 所有枚举值集中在 `scripts/_kg_enums.py`（单点真相源）
- 新增枚举值走 V3 校准流程：收集→报告→暂存→决议→registerVersion+1→回溯
- 继承基准库 `../00-book-knowledge-factory/references/enum-library.md` 的规范值快照

---

## 1. L0 底座 Schema

```python
# _item_registry.json 条目
{
    "item_id": "01-001",           # 卷号-条序
    "volume": "01",                # 卷号（01-34）
    "volume_name": "卷一",         # 卷名
    "volume_type": "正卷",         # 正卷/补遗/前言
    "subcategory": "列朝",         # ○ 标记的二级分类
    "entry_title": "告天即位",     # 【】内标题
    "original": "【告天即位】高皇帝将登宝位…",  # 原文指纹
    "norm": "【告天即位】高皇帝将登宝位…"      # 归一化原文
}
```

**卷号映射**：
- 00 = 前言（序/续编小引/补遗序/补遗跋/分类凡例）→ 不入条目库
- 01–30 = 正卷一~三十
- 31–34 = 补遗卷一~四

**条目切分规则**：
- 以 `【标题】` 为条目起始标记
- 条目结束 = 下一个 `【标题】` 或 `○` 或 `●` 之前
- `○` 标记为二级分类上下文，不单独成条
- 前言部分（00 卷）不入条目库

---

## 2. L1 实体层 Schema

```python
{
    "ent_id": "ENT-0001",
    "item_id": "01-001",
    "text": "高皇帝",               # 原文词形
    "type": "person",               # 实体类型枚举
    "normalized": "朱元璋",          # 归一化名称
    "start": 12,                    # 原文字符偏移
    "end": 15,
    "confidence": "high",           # high/medium/low
    "source": "01-001",             # 来源条目

    # === 本书扩展字段 ===
    "role_in_entry": ["主体"],       # 主体/客体/评论对象/引用人物/关联人物
    "faction": "无",                # 政治派系
    "exam_info": null,              # {year, era, rank, title} 或 null
    "career_span": "洪武元年—洪武三十一年"  # 仕宦时段
}
```

**实体类型枚举 ENTITY_TYPES**：
- person（人物）/ institution（机构）/ place（地名）/ official（职官）
- book（书名）/ ethnic（民族）/ religion（宗教）/ event_name（事件名）
- artifact（器物）/ custom（风俗）/ other（其他）/ 类型待定

**角色枚举 ENTRY_ROLES**：
- 主体 / 客体 / 评论对象 / 引用人物 / 关联人物

**派系枚举 FACTIONS**：
- 东林 / 楚党 / 齐党 / 浙党 / 昆党 / 宣党 / 宦官 / 无 / 待定

**置信度枚举 CONFIDENCE**：
- high / medium / low

---

## 3. L2 规则层 Schema

```python
{
    "rule_id": "RULE-01-001",
    "item_id": "01-001",
    "type": "义务",                 # 规则类型枚举
    "modals": ["须", "例"],         # 模态词
    "condition": "凡节候朔望",      # 条件
    "subject": "天子",              # 主体
    "subject_ent_ids": ["ENT-0001"],
    "action": "于大内瞻拜祭告",     # 动作
    "object": "先灵",               # 对象
    "purpose": "以奉先灵",          # 目的
    "punishment": null,             # 处罚
    "original": "凡节候朔望荐新以及忌日，俱于大内瞻拜祭告",
    "confidence": "high",

    # === 本书扩展字段 ===
    "rule_origin": "惯例",          # 祖制/诏令/惯例/奏议定/上谕/其他
    "actual_practice": "遵行",      # 遵行/变通/名存实亡/完全违背/未明
    "violation_evidence": null,     # 违背证据摘要
    "time_marker": "洪武年间"       # 适用时段
}
```

**规则类型枚举 RULE_TYPES**：
- 禁止 / 义务 / 允许 / 程序 / 时限 / 处罚 / 优先级

**规范来源枚举 RULE_ORIGINS**：
- 祖制 / 诏令 / 惯例 / 奏议定 / 上谕 / 其他

**实际执行枚举 ACTUAL_PRACTICE**：
- 遵行 / 变通 / 名存实亡 / 完全违背 / 未明

---

## 4. L5 事件层 Schema

```python
{
    "event_id": "EVT-01-001",
    "item_id": "01-001",
    "type": "朝政",                 # 事件类型枚举
    "who": "高皇帝",                # 行为主体
    "who_ent_ids": ["ENT-0001"],
    "action": "告天即位",           # 动作
    "what": "于钟山之阳设坛备仪昭告上帝",  # 事件内容
    "when": "洪武元年元旦",        # 时间
    "where": "钟山",                # 地点
    "original": "高皇帝将登宝位…告祭之日…上即位于南郊",

    # === 本书扩展字段 ===
    "event_significance": "重大政治",  # 重大政治/制度变动/人物转折/一般掌故/轶闻
    "political_impact": "明朝建立，定都南京",  # AI 概括
    "source_type": "文献转引",        # 亲历/传闻/文献转引/综合
    "vs_official_history": "与正史合",  # 补正史之阙/异于正史/正史不载/与正史合/未考
    "related_events": []             # 关联事件 ID
}
```

**事件类型枚举 EVENT_TYPES**（继承基准库 + 本书增量）：
- 朝政 / 制度变动 / 科举 / 军事 / 边政 / 司法 / 宫廷 / 人事 / 灾异 / 社会 / 宗教 / 文化 / 其他

**事件级别枚举 EVENT_SIGNIFICANCE**：
- 重大政治 / 制度变动 / 人物转折 / 一般掌故 / 轶闻

**信息来源枚举 SOURCE_TYPES**：
- 亲历 / 传闻 / 文献转引 / 综合

**正史对照枚举 VS_OFFICIAL_HISTORY**：
- 补正史之阙 / 异于正史 / 正史不载 / 与正史合 / 未考

---

## 5. C1 职官任职层 Schema（APPT）

```python
{
    "appt_id": "APPT-01-001",
    "item_id": "01-001",
    "person": "徐达",
    "person_ent_ids": ["ENT-0023"],
    "office": "大将军",
    "office_ent_ids": ["ENT-0100"],
    "institution": "中军都督府",
    "institution_ent_ids": ["ENT-0200"],
    "when": "洪武元年",
    "status": "现任",               # 任职状态枚举
    "evidence": "太祖命大将军徐达收其秘阁",
    "original": "太祖命大将军徐达，收其秘阁所藏图书典籍",

    # === 本书扩展字段 ===
    "appointment_context": "克故元时受命",  # 任命背景
    "controversy": "无争议",         # 无争议/有争议/遭弹劾/被驳回
    "faction_implication": null,     # 派系含义
    "concurrent_posts": []           # 兼职信息
}
```

**任职状态枚举 APPT_STATUS**：
- 现任 / 致仕 / 升迁 / 贬谪 / 罢黜 / 兼领 / 暂代 / 追赠 / 未明

**争议性枚举 CONTROVERSY**：
- 无争议 / 有争议 / 遭弹劾 / 被驳回

---

## 6. C3 人物关系层 Schema（REL）

```python
{
    "rel_id": "REL-01-001",
    "item_id": "01-001",
    "person_a": "朱元璋",
    "person_a_ent_ids": ["ENT-0001"],
    "person_b": "徐达",
    "person_b_ent_ids": ["ENT-0023"],
    "relation_type": "上下级",       # 关系类型枚举
    "direction": "单向",             # 单向/双向/未明
    "evidence": "太祖命大将军徐达",
    "original": "太祖命大将军徐达，收其秘阁所藏图书典籍",

    # === 本书扩展字段 ===
    "relationship_evolution": null,   # 关系演变
    "political_consequence": "收元秘阁典籍归金陵",  # 政治后果
    "evidence_strength": "直接表述",   # 直接表述/推断/旁证
    "time_span": "洪武初年"
}
```

**关系类型枚举 RELATION_TYPES**：
- 同僚 / 师生 / 姻亲 / 同乡 / 同科 / 举荐 / 弹劾 / 恩怨 / 上下级 / 父子亲属 / 敌对 / 党派 / 其他

**方向枚举 DIRECTION**：
- 单向 / 双向 / 未明

**证据强度枚举 EVIDENCE_STRENGTH**：
- 直接表述 / 推断 / 旁证

---

## 7. C6 引书索引层 Schema（CIT）

```python
{
    "cit_id": "CIT-01-001",
    "item_id": "01-001",
    "cited_work": "《归田录》",
    "cited_work_ent_ids": ["ENT-0500"],
    "citation_type": "泛引",         # 引用方式枚举
    "context": "仿欧阳修体例",       # 引用目的/上下文
    "original": "如欧阳《归田录》例",

    # === 本书扩展字段 ===
    "citation_purpose": "立论",       # 立论/佐证/对比/反驳/补遗/掌故引用
    "accuracy_note": null,            # 作者对被引文献的准确性评价
    "quoted_text": null               # 引文片段（短引保留）
}
```

**引用方式枚举 CITATION_TYPES**：
- 直引 / 转引 / 泛引 / 暗用 / 考辨

**引用目的枚举 CITATION_PURPOSES**：
- 立论 / 佐证 / 对比 / 反驳 / 补遗 / 掌故引用

---

## 8. C9 作者论说层 Schema（OPN）

```python
{
    "opn_id": "OPN-01-001",
    "item_id": "01-001",
    "topic": "太祖告天之诚意",       # 论说主题
    "stance": "肯定",                # 立场枚举
    "argument": "作者认为太祖以天下为公，不矫饰符命",  # AI 概括
    "original": "按是词先告上帝…真合尧舜汤武为心也。超千古而延万世，宜哉！",

    # === 本书扩展字段 ===
    "commentary_type": "褒扬",       # 褒扬/贬斥/考辨/感慨/讽刺/劝诫/中立评述
    "target_entities": ["ENT-0001"],  # 评论对象 ENT-ID
    "evidence_cited": "告天词原文",   # 作者引用的论据
    "historical_parallel": "尧舜汤武",  # 历史类比
    "tone": "严肃",                  # 严肃/愤慨/惋惜/嘲讽/客观
    "firsthand_witness": "不详"       # 亲历/亲闻/传闻/不详
}
```

**立场枚举 STANCES**：
- 肯定 / 否定 / 怀疑 / 讽刺 / 中立

**议论类型枚举 COMMENTARY_TYPES**：
- 褒扬 / 贬斥 / 考辨 / 感慨 / 讽刺 / 劝诫 / 中立评述

**语气枚举 TONES**：
- 严肃 / 愤慨 / 惋惜 / 嘲讽 / 客观

**亲历程度枚举 FIRSTHAND**：
- 亲历 / 亲闻 / 传闻 / 不详

---

## 9. C10 明代纪事层 Schema（MING）

```python
{
    "ming_id": "MING-01-001",
    "item_id": "01-001",
    "era": "洪武元年",              # 年号+年份
    "who": "高皇帝",
    "who_ent_ids": ["ENT-0001"],
    "what": "告天即位",
    "when": "洪武元年元旦",
    "where": "南京钟山",
    "category": "朝政",             # 涉明类型枚举
    "first_person": false,           # 是否第一人称亲历
    "ref_events": ["EVT-01-001"],   # 引用事件层 ID
    "original": "高皇帝将登宝位…上即位于南郊",

    # === 本书扩展字段 ===
    "reign_focus": "洪武",           # 主要涉及哪朝
    "firsthand_witness": "文献转引",  # 亲历/亲闻/传闻/不详
    "supplements_what": null          # 补正史之什么（AI 概括）
}
```

**涉明类型枚举 MING_CATEGORIES**：
- 朝政 / 人物 / 科举 / 风俗 / 灾异 / 亲历见闻 / 制度 / 边政 / 军事 / 社会 / 文化 / 宗教 / 其他

**朝代焦点枚举 REIGN_FOCUS**：
- 洪武 / 建文 / 永乐 / 洪熙 / 宣德 / 正统 / 景泰 / 天顺 / 成化 / 弘治 / 正德 / 嘉靖 / 隆庆 / 万历 / 跨朝

---

## 10. C14 时间沿革层 Schema（TME）

```python
{
    "tme_id": "YHB-TME-01-001",
    "item_id": "01-001",
    "era": {
        "dynasty": "明",
        "reign": "洪武",
        "year": 1,
        "order": 1,                  # REIGN_ORDER[洪武]
        "text": "洪武元年"
    },
    "target": "帝王庙",
    "target_ent_ids": ["ENT-0300"],
    "action": "建",
    "content": "太祖洪武六年建帝王庙于金陵",
    "category": "初置",             # 变动类型枚举
    "related_evo": null,
    "related_org": null,
    "ref_item": "01-001",
    "original": "太祖洪武六年建帝王庙于金陵",

    # === 本书扩展字段 ===
    "institution_target": "帝王庙",
    "cause": null,                   # 变动原因
    "before_after": {"before": null, "after": "建于金陵"}
}
```

**变动类型枚举 TME_CATEGORIES**：
- 初置 / 改置 / 升秩降秩 / 废置 / 复设 / 改称 / 裁并 / 增员 / 移驻 / 职掌变更 / 未明

**REIGN_ORDER 排序键**（继承 enum-library §1.21）：
```python
REIGN_ORDER = {
    "吴": 0, "洪武": 1, "建文": 2, "永乐": 3, "洪熙": 4,
    "宣德": 5, "正统": 6, "景泰": 7, "天顺": 8, "成化": 9,
    "弘治": 10, "正德": 11, "嘉靖": 12, "隆庆": 13, "万历": 14,
    "泰昌": 15, "天启": 16, "崇祯": 17,
}
```

---

## 11. REG 制度层 Schema（笔记掌造型 7 属性）

```python
{
    "reg_id": "REG-01-001",
    "item_id": "01-001",
    "name": "奉先殿祭祀",
    "category": "礼制",             # 制度类别枚举
    "establishment": "太祖所建",
    "tme_ids": ["YHB-TME-01-001"],
    "content_summary": "奉先殿为太祖所建以奉先灵，凡节候朔望荐新及忌日俱于大内瞻拜祭告，百官不得预列",
    "actual_practice": "遵行。主上每遇升殿受大朝必先谒奉先殿",
    "abuses_reform": [],
    "key_figures": ["ENT-0001"],     # 创设者/改革者/破坏者
    "original": "奉先殿者，太祖所建，以奉先灵…",

    # === 跨层通用扩展 ===
    "vs_official_history": "与正史合"
}
```

**制度类别枚举 REG_CATEGORIES**：
- 官制 / 科举 / 礼制 / 军事 / 财政 / 司法 / 边政 / 宦官 / 宗室 / 其他

---

## 12. 示例条目（试点用）

> 以下示例来自卷一【告天即位】条，用于 Phase ④ 试点校验。

### L1 实体示例

```json
[
    {"text": "高皇帝", "type": "person", "normalized": "朱元璋", "role_in_entry": ["主体"], "faction": "无", "exam_info": null, "career_span": "洪武元年—洪武三十一年"},
    {"text": "李善长", "type": "person", "normalized": "李善长", "role_in_entry": ["关联人物"], "faction": "无", "exam_info": null, "career_span": "洪武初"},
    {"text": "徐达", "type": "person", "normalized": "徐达", "role_in_entry": ["关联人物"], "faction": "无", "exam_info": null, "career_span": "洪武初"},
    {"text": "钟山", "type": "place", "normalized": "钟山", "role_in_entry": ["客体"]},
    {"text": "南郊", "type": "place", "normalized": "南郊", "role_in_entry": ["客体"]}
]
```

### C9 论说示例

```json
{
    "topic": "太祖告天之诚意",
    "stance": "肯定",
    "argument": "作者认为太祖以天下为公，不矫饰符命涂世耳目",
    "commentary_type": "褒扬",
    "target_entities": ["ENT-0001"],
    "historical_parallel": "尧舜汤武",
    "tone": "严肃",
    "firsthand_witness": "不详"
}
```

### L5 事件示例

```json
{
    "type": "朝政",
    "who": "朱元璋",
    "who_ent_ids": ["ENT-0001"],
    "action": "告天即位",
    "what": "于钟山之阳设坛备仪昭告上帝皇祗",
    "when": "洪武元年正月初四",
    "where": "钟山南郊",
    "event_significance": "重大政治",
    "political_impact": "明朝正式建立",
    "source_type": "文献转引",
    "vs_official_history": "与正史合"
}
```
