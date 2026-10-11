# Schema 与 ID 规范（《客座赘语》实例）

> 写源数据、打包器、验证脚本时对照本文。所有 schema 在实例化时按书定制后锁死，执行期不再改动；枚举值继承工厂基准库规范值快照（见来源列），本书增量走 V3 registerVersion 动态回填。
> 书稿：明·顾起元《客座赘语》10 卷 + 附录；条目约 460-480 条。

## 1. 全局约定

* **条粒度主键**：`item_id = NN-NNN`（卷-序，如 `01-015`），全书唯一，是所有层的共同锚点；复合条目用 `NN-NNN-SS` 表达子则（条切分见 SKILL.md §2）。
* **ID 命名空间**（每层唯一前缀，禁止跨层占用）：

| 层 | 前缀 | 示例 |
|---|---|---|
| 实体主键 | `ENT-` | ENT-0001 |
| 事件 | `EVT-` | EVT-0001 |
| 引书索引 | `CIT-` | CIT-0001 |
| 名物 | `OBJ-` | OBJ-0001 |
| 方言风俗 | `CUS-` | CUS-0001 |
| 明代纪事 | `MING-` | MING-0001 |
| 南京地理古迹 | `GEO-` | GEO-0001 |
| 职官任职 | `APPT-` | APPT-0001 |
| 名录谱牒 | `NAM-` | NAM-0001 |
| 文献资产 | `LIT-` | LIT-0001 |
| 作者按语论说 | `OPN-` | OPN-0001 |
| 人物关系 | `REL-` | REL-0001 |
| 古今翻译 | `TRL-` | TRL-0001 |
| 跨层索引 | `_kg_join` | — |

> 命名空间唯一归属：EVT- 只属事件层，其他层只引用；GEO- 只属地理古迹层；各层 ID 从 0001 起连续编号。

* **original 不手抄**：AI 源数据只写条号与解读字段；打包器从 `_item_registry.json` 注入 `original`/`norm`。

## 2. 底座 schema

### `_item_registry.json`（指纹库）

```
{
  "01-015": { "original": "原文全文", "norm": "归一化后的原文" }
}
```

* `norm`：异体字 / 缺字（□）/ 重文号 / 标点归一后的版本，比对与检索用。
* 后续每层的 `original` 字段都从本库注入，修正差异以本库为准。

### 章节文件

* 每章一个 MD/TXT，命名 `NN_卷名.txt`；`00` 为版本说明卷（总序/导读/点校说明/四库提要）。
* `_extract\NN_卷名.txt`：格式 `条N|正文`（N 从 1 起，对应 `NN-NNN` 的 NNN）。

## 3. ENT 实体层 schema

### 每卷标注 JSON

```
{
  "volume": "01",
  "annotations": [
    { "id": "ENT-0001", "item_id": "01-015", "text": "顾起元",
      "type": "person", "start": 12, "end": 15,
      "normalized": "顾起元", "confidence": 0.95, "source": "原文片段" }
  ]
}
```

* `type`：封闭枚举 18 值（见下）+ 兜底 `unknown`。
* `start/end`：在原文中的字符偏移，用于定位与去重。

### 归一汇总 JSON

```
{
  "normalized_inventory": [
    { "normalized": "顾起元", "type": "person", "count": 12,
      "first_source": "01-015", "surfaces": ["顾起元","顾太史","起元"] }
  ]
}
```

### 主键表 JSON

```
{
  "entities": [
    { "ent_id": "ENT-0001", "normalized": "顾起元", "type": "person",
      "count": 12, "first_source": "01-015", "surfaces": ["顾起元","顾太史"] }
  ],
  "alias_index": { "顾起元": "ENT-0001", "金陵": "ENT-0100", "秦淮": "ENT-0101" }
}
```

* `alias_index`：词形 → ent\_id 反查；复合解读词形（如"留都辅臣"→辅臣、"南都"→南京）手工加映射，不动标注。
* **同人异称归并**（本书特色）：名/字/号/谥/籍贯称（如"文简公"谥称）归并主键，surfaces 记录全部词形；无法确定同一性时登记 V2 同名异人待核清单，人工核前不合并（宁建勿并）。

### 实体类型枚举（继承基准库 18 值）

```
person 人物 / official 职官 / institution 机构 / place 地名 / era 年号朝代
/ work 文献书名 / object 名物 / animal 动物 / plant 植物 / food 饮食
/ doc 文书 / system 制度 / behavior 行为 / punishment 刑罚 / time 时间
/ quantity 数量 / posthumous 谥号 / unknown 类型待定
```

> 本书高频提示：official（尚书/御史/侍郎/总督/巡抚/致仕表述）、place（金陵/秦淮/钟山/后湖/诸寺诸桥）、posthumous（谥 62+）、work（引书 1331+）。来源：工厂 enum-library.md v2 §1.1。

## 4. EVT 事件层 schema

```
{
  "event_id": "EVT-0001", "item_id": "01-015",
  "type": "科举",
  "who": { "text": "顾起元", "who_ent_ids": ["ENT-0001"] },
  "action": "登第", "what": "……",
  "when": "未明", "where": "未明"
}
```

* 未明字段必须显式写 `"未明"`，不省略。
* 事件类型枚举（继承动态枚举库 23 顶层）：朝政/政变/军事/军政/边事/人事任免/弹劾/礼仪/科举/文事/建言/灾异/轶事/祭祀/经济/司法/神异传说/疾疫/御灾赈济/缉捕防盗/巡查监察/家事/其他。来源：工厂 `../00-book-knowledge-factory/references/enum-library.md` §1.3 事件类型子库（并入前 event-type-library v2 §1）。本书高频：科举（乡试 19）、文事、灾异、轶事、朝政、祭祀；未匹配值入 pending 表走 V3 决议。

## 5. CIT 引书索引层 schema

```
{
  "cit_id": "CIT-0001", "item_id": "01-015",
  "cited_work": { "text": "《南史》", "cited_ent_ids": ["ENT-0200"] },
  "citation_type": "直引", "context": "考源",
  "original": "（打包器注入）"
}
```

* 枚举：引用方式 = 直引/转引/泛引/暗用/考辨；引用目的 = 立论/证俗/考源/反驳/补遗/其他。来源：工厂 enum-library.md v2 §1.15。
* 一条引多书拆多条（CIT-0001/0002…共享 item_id）；本书引文省称频繁，norm 时登记全称→省称映射；与 LIT 分工：LIT 收整篇收录文献，CIT 收引用征引。

## 6. OBJ 名物层 schema

```
{
  "obj_id": "OBJ-0001", "item_id": "02-010",
  "name": { "text": "……", "name_ent_ids": ["ENT-0300"] },
  "category": "器物",
  "attributes": { "产地": "……", "形制": "……" },   // 文本可证键值对，无则留空
  "lore": "……（AI 解读）",
  "original": "（打包器注入）"
}
```

* 枚举：名物类别 = 器物/动物/植物/饮食/珍宝/材料/建筑/服饰/其他。来源：工厂 enum-library.md v2 §1.6。

## 7. CUS 方言风俗层 schema

```
{
  "cus_id": "CUS-0001", "item_id": "04-020",
  "type": "方言词",
  "region": { "text": "金陵", "region_ent_ids": ["ENT-0100"] },
  "term": "……", "description": "……",
  "original": "（打包器注入）"
}
```

* 枚举：类型 = 方言词/民俗/禁忌/谚语/节令/物产习俗/其他。来源：工厂 enum-library.md v2 §1.7。
* region 引用 ENT 地名；一俗多卷互见可合并（count 字段 + 多 item_id）。

## 8. MING 明代纪事层 schema

```
{
  "ming_id": "MING-0001", "item_id": "07-033",
  "era": "万历", "who": { "text": "……", "who_ent_ids": ["ENT-0001"] },
  "what": "……", "when": "未明", "where": "未明",
  "category": "制度", "first_person": false,
  "ref_events": ["EVT-0001"],
  "original": "（打包器注入）"
}
```

* 枚举：涉明类型 = 朝政/人物/科举/风俗/灾异/亲历见闻/制度/其他。来源：工厂 enum-library.md v2 §1.9。
* first_person：作者顾起元亲历/亲见/亲闻为 true（本书为南京人所记，亲历见闻多）。
* 与 EVT 分工：MING 只做涉明条目索引 + 亲历标记，ref_events 引用 EVT，不重复建模事件。

## 9. GEO 南京地理古迹层 schema（自定义新层，回写工厂层库）

```
{
  "geo_id": "GEO-0001", "item_id": "05-003",
  "name": { "text": "钟山", "name_ent_ids": ["ENT-0400"] },
  "category": "山水",
  "location": { "text": "朝阳门外", "location_ent_ids": ["ENT-0401"] },
  "history": "……（沿革，AI 解读，标注"原文所述"）",
  "evidence": "……（考证依据/AI 解读；顾起元按语部分可引 CIT）",
  "original": "（打包器注入）"
}
```

* 枚举（本书归纳，封闭 + 兜底）：GEO_TYPES = 山水 / 寺观祠庙（含庙宇、先贤祠、宫观）/ 桥渡 / 都邑宫阙（含宫城、古城、苑囿）/ 陵墓 / 水利沟渠 / 园第坊巷 / 其他。
* 执行要点：地理实体归 ENT（type=place）；GEO 做条目级沿革考证登记并引用 ENT；一寺/一桥/一陵多卷互见可合并（count + 多 item_id）；history 区分"原文所述沿革"与"顾起元考证按语"（后者考证来源记入 evidence）；点校说明所述引文随意问题在 CIT/evidence 中如实标注。

## 10. APPT 职官任职层 schema

```
{
  "appointment_id": "APPT-0001", "item_id": "07-012",
  "person": { "text": "……", "person_ent_ids": ["ENT-0001"] },
  "office": { "text": "礼部侍郎", "office_ent_ids": ["ENT-0500"] },
  "institution": { "text": "南京礼部", "institution_ent_ids": ["ENT-0501"] },
  "when": "未明", "status": "现任",
  "evidence": "……",
  "original": "（打包器注入）"
}
```

* 枚举：任职状态 = 现任/致仕/升迁/贬谪/罢黜/兼领/暂代/追赠/未明。来源：工厂 enum-library.md v2 §1.10（9 值；起复/世袭/举荐为待回溯建议值，本书执行期按需决议）。
* 执行流程：任职动词/官职词典 → 正则候选 → AI 复核 → V2 人工校验闭环；一条目多任职拆多条共享 item_id；本书致仕表述极多（留都聚居致仕官员），致仕为高频状态。

## 11. NAM 名录谱牒层 schema

```
{
  "nam_id": "NAM-0001", "item_id": "09-008",
  "name": "……题名", "category": "科第名录",
  "scope": "……（范围说明）",
  "entries": [
    { "seq": 1, "person": "……", "courtesy_name": "……", "hometown": "……", "office": "……" }
  ],
  "ent_ids": [],
  "original": "（打包器注入）"
}
```

* 枚举：名录类型 = 官员题名/同僚题名/迁谪录/谱牒/题名记/科第名录/其他。来源：工厂 enum-library.md v2 §1.5（12 值，本书高频科第名录——乡试/登科题名条；长寿/巨富/异相/灾异名录视文本匹配）。
* 表格式名录整体一条 NAM 记录；仅提及无完整表者登记话题（entries 空 + evidence）。

## 12. LIT 文献资产层 schema

```
{
  "lit_id": "LIT-0001", "item_id": "08-005",
  "title": "……", "author": { "text": "……", "author_ent_ids": ["ENT-0600"] },
  "type": "碑文", "content_location": "……",
  "original": "（打包器注入）"
}
```

* 枚举：文献类型 = 诏敕圣旨/碑文/奏议/书启/诗/记/题跋/序/祭文/其他。来源：工厂 enum-library.md v2 §1.11（10 值；集为待回溯建议值）。
* 佚名作者写"未明"；无题 title 取首句。

## 13. OPN 作者按语论说层 schema

```
{
  "opn_id": "OPN-0001", "item_id": "03-021",
  "topic": "……（论说主题）",
  "stance": "中立",
  "argument": "……（AI 解读要点，非原文）",
  "evidence_refs": ["CIT-0001"],
  "original": "（打包器注入）"
}
```

* 枚举：立场 = 肯定/否定/怀疑/讽刺/中立。来源：工厂 enum-library.md v2 §1.8。
* 触发词表：按 / 余按 / 臆断 / 因思 / 余尝 / 余谓 / 愚谓 / 吾郡。本书以考证按语为主（按：61），论说句密度低于《五杂俎》，如实标注。

## 14. REL 人物关系层 schema

```
{
  "rel_id": "REL-0001", "item_id": "01-030",
  "person_a": { "text": "……", "person_a_ent_ids": ["ENT-0001"] },
  "person_b": { "text": "……", "person_b_ent_ids": ["ENT-0002"] },
  "relation_type": "同乡", "direction": "双向",
  "evidence": "……",
  "original": "（打包器注入）"
}
```

* 枚举：关系类型 = 同僚/师生/姻亲/同乡/同科/举荐/弹劾/恩怨/上下级/父子亲属/敌对/其他；方向 = 单向/双向/未明。来源：工厂 enum-library.md v2 §1.4（12 值，本书同乡/同科/同僚/师生为高频）。
* 只建文本有直接证据的关系；同名异人先 V2 待核，不强行合并。

## 15. TRL 古今翻译层 schema

```
{
  "trl_id": "TRL-0001", "item_id": "01-015",
  "translation": "……（现代汉语译文）",
  "style": "意译", "note": "……", "confidence": 0.9,
  "original": "（打包器注入）"
}
```

* 枚举：翻译风格 = 直译/意译/注释性翻译。来源：工厂 enum-library.md v2 §1.13。
* 风格基准：余光中七条（`references/translation-style.md`）；专名保留原词+括注；职官术语符合明史口径；书名保留《》；缺字/异体按 norm 译。

## 16. VOL 卷阅读模式索引（非数据层）

* 产出 `references/volume-profile.md`，卷标注表如下（执行底座后逐卷判定填充）：

| 卷 | 主导 | 次要 | 阅读模式 | 判定依据 |
|---|---|---|---|---|
| 00 版本说明 | — | — | — | 总序/导读/点校说明/四库提要 |
| 01 | 〔待判定〕 | 〔待判定〕 | 〔模式〕 | 〔抽样+关键词〕 |
| 02 | 〔待判定〕 | 〔待判定〕 | 〔模式〕 | 名物条预判高 |
| … | | | | |
| 10 | 〔待判定〕 | 〔待判定〕 | 〔制度/名录优先〕 | 名录制度条预判高 |

* 阅读模式枚举（基准库 13 值按本书定制）：制度优先 / 人物优先 / 文献优先 / 谱牒优先 / 名录优先 / 文事优先 / 论理优先 / 风土优先 / 名物优先 / 世情优先 / 轶事优先 / 灾异优先 / 均衡全层。来源：工厂 enum-library.md v2 §1.14。

## 17. 跨层索引 schema

```
{
  "item_id": "01-015",
  "volume": "01", "source": "原文",
  "ents": ["ENT-0001"], "events": ["EVT-0001"], "cits": ["CIT-0001"],
  "objs": [], "cuss": [], "mings": ["MING-0001"], "geos": [],
  "appts": [], "nams": [], "lits": [], "opns": [], "rels": [],
  "trls": ["TRL-0001"],
  "layer_count": 5
}
```

* 扁平 CSV 同字段平铺一行；`layer_count` = 贯通层数（13 层全贯通 = 13）。

## 18. 枚举治理（registerVersion + 基准值继承）

* 所有枚举收进单文件 `_kg_enums.py`（含版本号；基准库继承值标注来源版本，本书增量值独立版本线）。
* 基准值继承：启用层枚举继承工厂 `enum-library.md`（含事件类型子库 §1.3）规范值快照，不自创词形；同义值走别名映射归并。
* 新书归纳增量：本书出现基准库外新值 → 收集 - 报告 - 暂存（pending 表，不中断）→ 决议（新增/归并/暂存，新增须有实例证据 + 使用说明）→ registerVersion+1 → 回溯存量 → 更新基准库与实例快照。
* 树状管理：值 ≥15 或有天然层级时按树组织（顶层大类封闭 → 子类 → 叶子，深度 ≤3）；枚举值带 version；新增值必须 version+1 并回溯全部存量数据。
* 口径漂移检测：注释/文档中的枚举数与代码一致，验证脚本比对。

## 19. 示例条目（试点校验固化区）

> 工厂 Phase ④ 试点校验已通过（2026-10-10）：取三条真实条目（各卷首条 01-001 / 05-001 / 10-001），按启用层 schema 试跑判定-注入-校验，字段/枚举/ID 无硬伤。以下为固化范本，写源数据/打包器时照此格式。
> 源数据只写 `item_id` + 解读字段；`original`/`norm` 由打包器从 `_item_registry.json` 注入。

### 19.1 条目 01-001《经义兼古注疏》（卷一，科举制度考证条）

原文要点：洪武三年初设科举条格；洪武十七年颁科举成式；顾起元按语考证"兼用古注疏"制度后遭废弃，主张申明初制。

**EVT 源数据（AI 判定）**：
```
{ "event_id": "EVT-0001", "item_id": "01-001", "type": "科举",
  "who": { "text": "朝廷", "who_ent_ids": [] },
  "action": "初设科举条格", "what": "洪武三年初设科举，定五经义各试本经一道",
  "when": "洪武三年五月初一日", "where": "未明" },
{ "event_id": "EVT-0002", "item_id": "01-001", "type": "科举",
  "who": { "text": "礼部", "who_ent_ids": [] },
  "action": "颁行科举成式", "what": "洪武十七年命礼部颁行科举成式，定乡会试年例与场数",
  "when": "洪武十七年三月初一日", "where": "未明" }
```

**CIT 源数据（AI 判定）**：
```
{ "cit_id": "CIT-0001", "item_id": "01-001",
  "cited_work": { "text": "《易》程朱氏注", "cited_ent_ids": [] },
  "citation_type": "泛引", "context": "考源" }
```

**OPN 源数据（AI 判定）**：
```
{ "opn_id": "OPN-0001", "item_id": "01-001", "topic": "科举注疏去取之制",
  "stance": "否定",                     // 对"斥古注疏不用"持否定
  "argument": "顾起元按语：初制兼用古注疏及诸家传，圣制彰明；后不知何故斥古注疏不用，致举子师心剿说，宜申明初制",
  "evidence_refs": ["CIT-0001"] }
```

**MING 源数据（AI 判定）**：
```
{ "ming_id": "MING-0001", "item_id": "01-001", "era": "洪武", "who": { "text": "未明", "who_ent_ids": [] },
  "what": "初设科举与颁行科举成式", "when": "洪武三年至十七年", "where": "未明",
  "category": "制度", "first_person": false, "ref_events": ["EVT-0001","EVT-0002"] }
```

**TRL 源数据（AI 判定）**：
```
{ "trl_id": "TRL-0001", "item_id": "01-001",
  "translation": "洪武三年五月初一，朝廷首次设立科举，条格诏书中规定第一场考五经经义……",
  "style": "意译", "note": "职官术语按明史口径", "confidence": 0.9 }
```

> 本条目 EVT/CIT/OPN/MING/TRL 命中；ENT 实体（科举、礼部、各经书名）由 ENT 层独立标注，此处引用待回填；GEO/OBJ/CUS/APPT/NAM/LIT/REL 不命中，如实不建。

### 19.2 条目 05-001《礼乐群英像》（卷五，地理+名录条）

原文要点：宋嘉定五年黄度作晋元帝新庙于石头东，两庑设礼乐群英三十六人像，叶适作记；顾起元按语逐一列出三十六人名号。

**GEO 源数据（AI 判定）**：
```
{ "geo_id": "GEO-0001", "item_id": "05-001",
  "name": { "text": "晋元帝新庙", "name_ent_ids": [] },
  "category": "寺观祠庙",
  "location": { "text": "石头东", "location_ent_ids": [] },
  "history": "宋嘉定五年黄度作晋元帝新庙于石头东，两庑设礼乐群英三十六人像，叶适为记；原文所述",
  "evidence": "顾起元按语逐一列三十六人名号（王导、谢安、刘琨、祖逖等），存先贤庙像之制" }
```

**NAM 源数据（AI 判定）**：
```
{ "nam_id": "NAM-0001", "item_id": "05-001",
  "name": "礼乐群英三十六人像", "category": "其他",
  "scope": "晋元帝新庙两庑先贤像，三十六人",
  "entries": [
    { "seq": 1, "person": "王导", "courtesy_name": "茂弘", "hometown": "未明", "office": "未明" }
    // ……seq 2-36 依原文按序
  ],
  "ent_ids": [] }
```

**OPN 源数据（AI 判定）**：
```
{ "opn_id": "OPN-0002", "item_id": "05-001", "topic": "礼乐群英三十六人",
  "stance": "中立",
  "argument": "顾起元按语：逐一考证三十六人名号（含字），存晋元帝庙先贤像之制",
  "evidence_refs": [] }
```

**TRL 源数据（AI 判定）**：
```
{ "trl_id": "TRL-0002", "item_id": "05-001",
  "translation": "宋朝嘉定五年，黄度在石头城东建晋元帝新庙……",
  "style": "意译", "note": "人名保留原词；三十六人名单长句群分段", "confidence": 0.9 }
```

> 本条目 GEO/NAM/OPN/TRL 命中；ENT 实体（三十六人、黄度、叶适、晋元帝庙、石头）由 ENT 层独立标注；EVT 无匹配事件类型（营建庙宇非既有 23 顶层，若执行期多卷出现可入 pending 表决议新增，本例如实不建）；REL 无直接证据不建。

### 19.3 条目 10-001《官军粮赏则例》（卷十，制度则例条）

原文要点：月粮则例（指挥使八石至军只身六斗等）、赏赐则例（冬赏/夏赏布匹折银）等则例。

**MING 源数据（AI 判定）**：
```
{ "ming_id": "MING-0002", "item_id": "10-001", "era": "未明", "who": { "text": "未明", "who_ent_ids": [] },
  "what": "官军月粮与赏赐则例", "when": "未明", "where": "未明",
  "category": "制度", "first_person": false, "ref_events": [] }
```

**TRL 源数据（AI 判定）**：
```
{ "trl_id": "TRL-0003", "item_id": "10-001",
  "translation": "月粮则例：指挥使每月八石……",
  "style": "直译", "note": "则例数字对照表直译保留；职官名保留原词", "confidence": 0.95 }
```

> 本条目 MING/TRL 命中；ENT 实体（指挥使/同知/佥事/千户/百户等职官、月粮制度）由 ENT 层独立标注；EVT 为静态则例（无事件，不强行建模）；APPT 为非任职记录（不建）；NAM 为则例非名录（不建）；OPN 无按语（不建）。**要点**：制度条文类条目如实按"低层命中"处理，不以凑层数强行建模。