# 《五杂俎》启用层 Schema 与 ID 规范

> 写源数据、打包器、验证脚本时对照本文。所有 schema 已在 Phase ③ 锁死，执行期不再改动。
> 启用层：实体 L1 / 事件 EVT / 人物关系 REL / 名录谱牒 NAM / 引书索引 CIT / 名物 OBJ / 方言风俗 CUS / 作者论说 OPN / 明代纪事 MING / 卷阅读模式 V1 / 跨层索引。未启用层无任何 schema。

## 1. 全局约定

- **条粒度主键**：`item_id = NN-NNN`（卷-序，如 `01-023`；序卷为 `00-001`），全书唯一，是所有层的共同锚点。
- **ID 命名空间**（每层唯一前缀，禁止跨层占用；**业务 ID 全部由打包器自动分配**，AI 源数据只写卷内顺序槽位，不手写 ID）：

| 层 | 前缀 | 示例 |
|---|---|---|
| 实体主键 | `ENT-` | ENT-323 |
| 事件 | `WZZ-E-` | WZZ-E-012 |
| 人物关系 | `REL-` | REL-007 |
| 名录谱牒 | `NAM-` | NAM-003 |
| 引书索引 | `CIT-` | CIT-015 |
| 名物 | `OBJ-` | OBJ-042 |
| 方言风俗 | `CUS-` | CUS-008 |
| 作者论说 | `OPN-` | OPN-021 |
| 明代纪事 | `MING-` | MING-005 |
| 职官任职 | `APPT-` | APPT-001 |
| 古今翻译 | `TRL-` | TRL-001 |
| 跨层索引 | `_kg_join` | — |

- **original 不手抄**：AI 源数据只写条号与解读字段；打包器从 `_item_registry.json` 注入 `original`/`norm`。
- **容器键统一**：各层单卷 JSON 顶层键统一为 `records`（不做 annotations/records 特判）；每记录必带 `volume` 字段。
- **枚举校验模式**：收集-报告-暂存（未匹配值入 pending 表不中断）；新增值 registerVersion+1 回溯存量，必须有实例证据。
- **枚举基准与树状**：所有枚举 = 基准值继承（权威源：工厂 `enum-library.md` 树状基准库，实例按启用层固化快照）+ 新书归纳增量（流程见工厂 `enum-induction-guide.md`）；值多时按树组织（顶层大类封闭 → 子类 → 叶子，深度 ≤3，父类计数=子类求和）；事件类型明细见工厂 `enum-library.md` §1.3 事件类型子库。

## 2. 底座 schema

### `_item_registry.json`（指纹库）
```json
{
  "01-023": { "original": "正德初，彗星扫文昌。文昌者，馆阁之应也。……", "norm": "正德初，彗星扫文昌。文昌者，馆阁之应也。……" }
}
```
- `norm`：异体字/缺字/标点归一后的版本，比对与检索用。后续每层 `original` 从本库注入，修正差异以本库为准。

### 章节文件
- 每章一个 XHTML/MD，命名 `NN_卷名.xhtml`（`00_版本说明与序`，`01_天部一` ~ `16_事部四`）。

### 卷概要 `volume_summary.json`
```json
{ "volume": "01", "name": "天部一", "count": 125, "item_range": ["01-001","01-125"], "mode_hint": "论理/灾异优先" }
```

## 3. L1 实体层 schema

### 每卷标注 JSON（顶层键 records）
```json
{
  "records": [
    {
      "volume": "01",
      "id": "ENT-000", "item_id": "01-023", "text": "张居正",
      "type": "person", "start": 88, "end": 91,
      "normalized": "张居正", "confidence": 0.98, "source": "原文片段"
    }
  ]
}
```
- `type`：封闭枚举（见下）+ 兜底 `unknown`。
- `start/end`：在原文中的字符偏移，用于定位与去重。

### 实体类型枚举（继承基准库 enum-library.md §1.1 规范值快照；词形归一 office→official、book→work）
`person 人物 / place 地名 / work 书名（文献）/ official 职官 / era 年号朝代 / object 名物 / animal 动物 / plant 植物 / food 饮食 / unknown 类型待定`

### 归一汇总 JSON
```json
{
  "normalized_inventory": [
    { "normalized": "张居正", "type": "person", "count": 2,
      "first_source": "01-023", "surfaces": ["张居正","江陵"] }
  ]
}
```

### 主键表 JSON
```json
{
  "entities": [
    { "ent_id": "ENT-001", "normalized": "张居正", "type": "person",
      "count": 2, "first_source": "01-023", "surfaces": ["张居正"] }
  ],
  "alias_index": { "张居正": "ENT-001", "林太守春泽公": "ENT-xxx" }
}
```
- `alias_index`：词形 → ent_id 反查；复合解读词形（"林太守春泽公"→林春泽）手工加映射，不动标注。
- **同名异人**：跨卷同名自动收集待核清单（`同名异人待核清单.csv`），人工核前不强行合并（宁建勿并）。

## 4. 事件层 schema（WZZ-E）

```json
{
  "record": {
    "volume": "01",
    "event_id": "WZZ-E-012", "item_id": "01-023",
    "type": "朝政",
    "who": { "text": "张居正", "who_ent_ids": ["ENT-001"] },
    "action": "夺情杖言官", "what": "万历丁丑十月异星见，张居正以夺情事杖赵用贤、吴中行、艾穆、邹元标等，编管远方",
    "when": "万历丁丑（1577）", "where": "未明"
  }
}
```
- 未明字段必须显式写 `"未明"`，不省略。
- 事件类型枚举（**跨书动态库规范全集快照 v1，22 值 + 兜底"其他"**；权威源 = 工厂 `../00-book-knowledge-factory/references/enum-library.md` §1.3 事件类型子库；本书初版 9 值经别名映射归一——政事→朝政 / 军务→军事 / 科第→科举 / 刑罚→司法；本书新增值走 registerVersion 动态回填：收集-报告-暂存 → 决议 → +1 → 回溯存量）：
  `朝政 / 政变 / 军事 / 军政 / 边事 / 人事任免 / 弹劾 / 礼仪 / 科举 / 文事 / 建言 / 灾异 / 轶事 / 祭祀 / 经济 / 司法 / 神异传说 / 疾疫 / 御灾赈济 / 缉捕防盗 / 巡查监察 / 其他`
- 一条目多事件（如 01-023 含正德彗星、万历异星两事）拆多条 EVT 共享 item_id。

### 示例条目（试点固化，压缩后不重读）
```json
{
  "volume": "01", "event_id": "WZZ-E-012", "item_id": "01-023",
  "type": "朝政",
  "who": { "text": "张居正", "who_ent_ids": ["ENT-001"] },
  "action": "夺情杖言官",
  "what": "万历丁丑十月异星见西南，无何张居正以夺情事杖赵用贤等，朝中正人为之一空",
  "when": "万历丁丑", "where": "未明"
}
```

## 5. 人物关系层 schema（REL）

```json
{
  "record": {
    "volume": "01",
    "rel_id": "REL-007", "item_id": "01-023",
    "person_a": { "text": "张居正", "ent_ids": ["ENT-001"] },
    "person_b": { "text": "赵用贤", "ent_ids": ["ENT-010"] },
    "relation_type": "恩怨", "direction": "单向", "evidence": "杖赵用贤等编管远方"
  }
}
```
- 关系类型枚举（继承基准库 §1.4，12 值）：`师生 / 举荐 / 弹劾 / 同僚 / 姻亲 / 同乡 / 同科 / 父子亲属 / 恩怨 / 敌对 / 上下级（别名：主从）/ 其他`
- **只建文本有直接证据的关系**（宁缺毋滥）；推测关系不建。
- 一条多关系拆多条记录共享 item_id。

### 示例条目
```json
{
  "volume": "01", "rel_id": "REL-007", "item_id": "01-023",
  "person_a": { "text": "张居正", "ent_ids": ["ENT-001"] },
  "person_b": { "text": "赵用贤", "ent_ids": ["ENT-010"] },
  "relation_type": "恩怨", "direction": "单向", "evidence": "杖赵用贤等编管远方"
}
```

## 6. 名录谱牒层 schema（NAM）

```json
{
  "record": {
    "volume": "05",
    "nam_id": "NAM-003", "item_id": "05-018",
    "name": "历代高寿者录", "category": "长寿名录", "scope": "历代至明高寿者",
    "entries": [
      { "seq": 1, "person": "王士能", "courtesy_name": "", "hometown": "山东济宁州", "office": "" },
      { "seq": 2, "person": "茹文中", "courtesy_name": "", "hometown": "未明", "office": "" }
    ],
    "ent_ids": ["ENT-100","ENT-101"]
  }
}
```
- 名录类型枚举（继承基准库 §1.5，12 值；本书常用子集）：`长寿名录 / 巨富名录 / 异相名录 / 灾异名录 / 科第名录 / 器物名录 / 其他`（基准库另含官员题名 / 同僚题名 / 迁谪录 / 谱牒 / 题名记，按需引入）
- 表格式名录整体一条 NAM（entries 数组化）；仅提及无完整表者登记话题（entries 空 + evidence），不强行展开。
- 跨行四元组（姓名/字/籍贯/官职）按表重组，不按行硬拆。

### 示例条目
```json
{
  "volume": "05", "nam_id": "NAM-003", "item_id": "05-018",
  "name": "历代高寿者录", "category": "长寿名录", "scope": "历代至明高寿者",
  "entries": [
    { "seq": 1, "person": "王士能", "courtesy_name": "", "hometown": "山东济宁州", "office": "" },
    { "seq": 2, "person": "茹文中", "courtesy_name": "", "hometown": "未明", "office": "" },
    { "seq": 3, "person": "林春泽", "courtesy_name": "", "hometown": "闽中", "office": "太守" }
  ],
  "ent_ids": ["ENT-100","ENT-101","ENT-102"]
}
```

## 7. 引书索引层 schema（CIT）

```json
{
  "record": {
    "volume": "01",
    "cit_id": "CIT-015", "item_id": "01-010",
    "cited_work": { "text": "汉书", "ent_ids": ["ENT-200"] },
    "citation_type": "考辨", "context": "辨阳九百六两说之异",
    "original": "（打包器注入）"
  }
}
```
- 引用方式枚举（继承基准库 §1.15）：`直引 / 转引 / 泛引 / 暗用 / 考辨`
- context 枚举（继承基准库 §1.15）：`立论 / 证俗 / 考源 / 反驳 / 补遗 / 其他`
- 一条引多书拆多条记录共享 item_id；同一书多次引同一条目可合并为一条（count 字段可选）。

### 示例条目
```json
{
  "volume": "01", "cit_id": "CIT-015", "item_id": "01-010",
  "cited_work": { "text": "汉书", "ent_ids": ["ENT-200"] },
  "citation_type": "考辨", "context": "辨阳九、百六两说互异",
  "original": "（打包器注入）"
}
```

## 8. 名物层 schema（OBJ）

```json
{
  "record": {
    "volume": "09",
    "obj_id": "OBJ-042", "item_id": "09-001",
    "name": { "text": "龙", "ent_ids": ["ENT-300"] },
    "category": "动物", "attributes": { "习性": "人得而豢之", "掌故": "莫灵于龙而可豢" },
    "lore": "龙虎虽灵猛，因有欲故为人所豢槛（AI 解读）",
    "original": "（打包器注入）"
  }
}
```
- 名物类别枚举（继承基准库 §1.6）：`器物 / 动物 / 植物 / 饮食 / 珍宝 / 材料 / 建筑 / 服饰 / 其他`
- attributes 为文本可证的键值对（产地/形制/用法/功效/习性等），无则留空，不编造；lore 为 AI 解读非原文。

### 示例条目（试点固化：09-001 首条论龙虎豢养）
```json
{
  "volume": "09", "obj_id": "OBJ-042", "item_id": "09-001",
  "name": { "text": "龙", "ent_ids": ["ENT-300"] },
  "category": "动物", "attributes": { "习性": "人得而豢之", "掌故": "莫灵于龙而可豢" },
  "lore": "龙虎虽灵猛，因有欲故为人所豢槛",
  "original": "（打包器注入）"
}
```

## 9. 方言风俗层 schema（CUS）

```json
{
  "record": {
    "volume": "01",
    "cus_id": "CUS-008", "item_id": "01-014",
    "type": "方言词", "region": { "text": "闽", "ent_ids": ["ENT-400"] },
    "term": "雨为辅", "description": "今闽人方音尚以雨为辅，记《礼统》'雨者辅也'之音证",
    "original": "（打包器注入）"
  }
}
```
- 类型枚举（继承基准库 §1.7）：`方言词 / 民俗 / 禁忌 / 谚语 / 节令 / 物产习俗 / 其他`

### 示例条目
```json
{
  "volume": "01", "cus_id": "CUS-008", "item_id": "01-014",
  "type": "方言词", "region": { "text": "闽", "ent_ids": ["ENT-400"] },
  "term": "雨为辅", "description": "《礼统》云雨者辅也，今闽人方音尚以雨为辅",
  "original": "（打包器注入）"
}
```

## 10. 作者观点论说层 schema（OPN）

```json
{
  "record": {
    "volume": "13",
    "opn_id": "OPN-021", "item_id": "13-022",
    "topic": "读书养生", "stance": "否定",
    "argument": "夜读书不可过子时，诸血归心，不得睡则血耗生病；古人读书明义理，今人读书取科第而以身殉之，可惑",
    "evidence_refs": ["CIT-001"], "original": "（打包器注入）"
  }
}
```
- 立场枚举（继承基准库 §1.8）：`肯定 / 否定 / 怀疑 / 讽刺 / 中立`
- argument 为 AI 解读（要点概要），非原文；evidence_refs 可引用 CIT ID。

### 示例条目
```json
{
  "volume": "13", "opn_id": "OPN-021", "item_id": "13-022",
  "topic": "读书养生", "stance": "否定",
  "argument": "夜读书过子时耗血生病；古之读书明义理，今之读书但取科第而以身殉之，惑也",
  "evidence_refs": [], "original": "（打包器注入）"
}
```

## 11. 明代纪事层 schema（MING）

```json
{
  "record": {
    "volume": "01",
    "ming_id": "MING-005", "item_id": "01-023",
    "era": "万历丁丑（1577）", "who": { "text": "张居正", "ent_ids": ["ENT-001"] },
    "what": "夺情杖言官，逐王锡爵张位，朝中正人为之一空",
    "when": "万历丁丑十月", "where": "未明",
    "category": "朝政", "first_person": false, "ref_events": ["WZZ-E-012"],
    "original": "（打包器注入）"
  }
}
```
- 涉明类型枚举（继承基准库 §1.9）：`朝政 / 人物 / 科举 / 风俗 / 灾异 / 亲历见闻 / 制度 / 其他`
- 与 EVT 分工：MING 只做涉明条目索引登记 + 亲历标记；有事件建模时 ref_events 引用 WZZ-E ID，不重复建模。
- 一条目多涉明类型（如 01-023 含作者亲历异星 + 朝政夺情）拆多条 MING 共享 item_id。

### 示例条目
```json
{
  "volume": "01", "ming_id": "MING-005", "item_id": "01-023",
  "era": "万历丁丑", "who": { "text": "张居正", "ent_ids": ["ENT-001"] },
  "what": "夺情杖言官，逐王锡爵等，朝中正人为之一空",
  "when": "万历丁丑十月", "where": "未明",
  "category": "朝政", "first_person": false, "ref_events": ["WZZ-E-012"],
  "original": "（打包器注入）"
}
```

## 12. 职官任职层 schema（APPT）

```json
{
  "record": {
    "volume": "01",
    "appointment_id": "APPT-001", "item_id": "01-023",
    "person": { "text": "刘健", "person_ent_ids": ["ENT-020"] },
    "office": { "text": "内阁", "official_ent_ids": ["ENT-030"] },
    "institution": { "text": "未明", "ent_ids": [] },
    "when": "正德初", "status": "罢黜",
    "evidence": "逆瑾出首，逐内阁刘健、谢迁",
    "original": "（打包器注入）"
  }
}
```
- 任职状态枚举（继承基准库 §1.10，12 值）：`现任 / 致仕 / 升迁 / 贬谪 / 罢黜 / 兼领 / 暂代 / 追赠 / 未明`（基准库另含 起复 / 世袭 / 举荐，按需引入）
- 任职动词词典：为/任/授/擢/迁/改/除/罢/谪/致仕/兼/领/督/巡抚/提督 → 正则候选 → AI 复核；一条目多任职拆多条共享 item_id。
- 本书官职词偏散（108 次）：宁少勿滥，无任职表述的条目不建；官职实体归 L1（type=office），APPT 引用 ENT ID。

### 示例条目（试点固化：01-023 逆瑾逐刘健谢迁）
```json
{
  "volume": "01", "appointment_id": "APPT-001", "item_id": "01-023",
  "person": { "text": "刘健", "person_ent_ids": ["ENT-020"] },
  "office": { "text": "内阁", "official_ent_ids": ["ENT-030"] },
  "institution": { "text": "未明", "ent_ids": [] },
  "when": "正德初", "status": "罢黜",
  "evidence": "逆瑾出首，逐内阁刘健、谢迁",
  "original": "（打包器注入）"
}
```

## 13. 古今翻译层 schema（TRL）

```json
{
  "record": {
    "volume": "13",
    "trl_id": "TRL-001", "item_id": "13-001",
    "translation": "圣人看重知命，是说安于命运、不趋利避害；今人想知命，却是为了趋利避害，这不能叫知命，该叫逆天。",
    "style": "直译", "note": "专名'知命'保留原词", "confidence": 0.95,
    "original": "（打包器注入）"
  }
}
```
- 翻译风格枚举（继承基准库 §1.13）：`直译 / 意译 / 注释性翻译`
- **风格基准已固化（2026-10-10 用户指定）**：所有 TRL 译文一律按 `references/translation-style.md` 余光中风格七条执行（译原意/并联句法/白以为常/精简防冗余/四字格/忌翻译体/专名保留+括注）；style 字段填直译/意译/注释性翻译（风格判定），note 标注"余光中风格基准"；偏离基准须在 note 说明理由。
- AI 逐条翻译（代码只验覆盖：条目数=翻译数）；专名保留原词+括注；缺字/异体按 norm 归一后译；长文分句群翻译保留分段；支持按卷分步；交付 TRL 前逐条对照 translation-style.md 校验清单自查。

### 示例条目（试点固化：13-001 知命论，余光中风格基准）
```json
{
  "volume": "13", "trl_id": "TRL-001", "item_id": "13-001",
  "translation": "圣人看重“知命”，是说安于命运，不趋利避害；今人想“知命”，却是为了趋利避害——这不能叫知命，该叫逆天。",
  "style": "直译", "note": "余光中风格基准；“知命”保留原词加引号", "confidence": 0.95,
  "original": "（打包器注入）"
}
```

## 14. 卷阅读模式（V1）

- 产出 `references/volume-profile.md`：卷标注表 + 阅读模式处理指引。
- 阅读模式枚举（本书定制，基准库 §1.14 可组合复用）：`论理优先 / 风土优先 / 人物优先 / 名物优先 / 世情优先 / 轶事优先 / 灾异优先 / 均衡全层`
- 判定：每卷首段+尾段抽样 + 关键词密度，AI 逐卷判定；执行前查模式分配层优先级；与卷内实际不符以实际为准回填（registerVersion）。

## 15. 跨层索引 schema

```json
{
  "item_id": "01-023",
  "volume": "01", "source": "原文",
  "events": ["WZZ-E-012"], "rels": ["REL-007"], "nams": [],
  "cits": [], "objs": [], "cuss": [], "opns": [], "mings": ["MING-005"],
  "appts": ["APPT-001"], "trls": [],
  "ents": ["ENT-001","ENT-010"],
  "layer_count": 5
}
```
- 扁平 CSV 同字段平铺一行，`layer_count` 表示贯通层数。
