# 《先进遗风》实例 Schema 与 ID 规范

> 写源数据、打包器、验证脚本时对照本文。所有 schema 在 Phase ③《操作指南》中按书定制后锁死，执行期不再改动。
> 工厂路径引用：`../book-knowledge-factory/references/`（本机工厂目录名，无 `00-` 前缀）。

## 1. 全局约定

* **条粒度主键**：`item_id = NN-NNN`（卷 - 序，如 `01-003`），全书唯一，是所有层的共同锚点。卷号映射：卷上=01、卷下=02；书名/卷标记行不入条目。

* **ID 命名空间**（每层唯一前缀，禁止跨层占用）：

| 层 | 前缀 | 示例 |
|---|---|---|
| 实体主键 | `ENT-` | ENT-001 |
| 职官任职（APPT） | `APPT-` | APPT-001 |
| 人物关系（REL） | `REL-` | REL-001 |
| 事件（L5） | `XJF-E-` | XJF-E-001 |
| 作者论说（OPN） | `OPN-` | OPN-001 |
| 古今翻译（TRL） | `TRL-` | TRL-001 |
| 跨层索引 | `_kg_join` | — |

> 命名空间唯一归属：`XJF-E-` 只属于事件层，其余层只显式引用事件 ID。业务 ID 由打包器按「卷号 × 段容量（默认 500）+ 槽位」自动分配，AI 源数据不手写 ID（pitfalls #13/#22）。

* **original 不手抄**：AI 源数据只写条号与解读字段；打包器从 `_item_registry.json` 注入 `original`/`norm`。

* **枚举基准**：本实例启用层枚举继承工厂 `../book-knowledge-factory/references/enum-library.md` 规范值快照（下方各节已拉取），不自创词形；同义值走别名映射归并；新值走 registerVersion（见 §11）。

## 2. 底座 schema

### `_item_registry.json`（指纹库）

```
{
  "01-003": { "original": "原文全文", "norm": "归一化后的原文" }
}
```

* `norm`：异体字归一（濓/濂、竒/奇、徃/往 等）、缺字括注 `■〈□〉` 保留原字形、标点统一为现代标点。
* 后续每层的 `original` 字段都从本库注入，修正差异以本库为准。

### 章节文件

* 每卷一个 TXT：`_extract\01_先进遗风卷上.txt` / `02_先进遗风卷下.txt`（格式 `条N|正文`），预计约 100 条。

## 3. L1 实体层 schema

### 每卷标注 JSON

```
{
  "volume": "01",
  "annotations": [
    {
      "id": "ENT-000", "item_id": "01-001", "text": "宋濓",
      "type": "person", "start": 0, "end": 2,
      "normalized": "宋濂", "confidence": 0.98, "source": "原文片段"
    }
  ]
}
```

* `type`：封闭枚举 ENTITY_TYPES（下方快照 18 值）+ 兜底 `unknown`。本书预期高频：person / official / institution / place / era / work / posthumous / system / behavior / doc / unknown。
* `start/end`：在原文中的字符偏移，用于定位与去重。

### ENTITY_TYPES 快照（继承基准库 §1.1，18 值）

```
person 人物 / official 职官（别名 office）/ institution 机构（别名 org）/ place 地名
/ era 年号朝代 / work 文献书名（别名 book）/ object 名物（别名 artifact）
/ animal 动物 / plant 植物 / food 饮食 / doc 文书 / system 制度
/ behavior 行为 / punishment 刑罚 / time 时间 / quantity 数量
/ posthumous 谥号 / unknown 类型待定（兜底）
```

### 归一汇总 JSON

```
{
  "normalized_inventory": [
    { "normalized": "宋濂", "type": "person", "count": 3,
      "first_source": "01-001", "surfaces": ["宋濓","学士宋文宪公濓"] }
  ]
}
```

### 主键表 JSON

```
{
  "entities": [
    { "ent_id": "ENT-001", "normalized": "宋濂", "type": "person",
      "count": 3, "first_source": "01-001", "surfaces": ["宋濓","学士宋文宪公濓"] }
  ],
  "alias_index": { "宋濓": "ENT-001", "学士宋文宪公濓": "ENT-001" }
}
```

* `alias_index`：词形 → ent_id 反查；复合解读词形（如"学士宋文宪公濓"→宋濂）手工加映射，不动标注。

## 4. APPT 职官任职层 schema（层库 C1 定制）

### 每卷标注 JSON

```
{
  "appointments": [
    {
      "appt_id": "APPT-001", "item_id": "01-001",
      "person": { "text": "宋濂", "person_ent_ids": ["ENT-001"] },
      "office": { "text": "学士", "official_ent_ids": ["ENT-005"] },
      "institution": { "text": "翰林", "ent_ids": ["ENT-006"] },
      "when": "未明", "status": "现任",
      "evidence": "……（AI 解读要点）", "original": "（打包器注入）"
    }
  ]
}
```

* 一条目多任职拆多条记录共享 `item_id`。
* `status`：封闭枚举 APPT_STATUS（下方快照 12 值）。
* `when`：有明确年号/纪年写实值，否则显式写 `"未明"`。

### APPT_STATUS 快照（继承基准库 §1.10，12 值）

```
现任 / 致仕 / 升迁 / 贬谪 / 罢黜 / 兼领 / 暂代 / 追赠 / 未明
+ 起复 / 世袭 / 举荐
```

### 触发词词典（本实例定制）

```
授 / 擢 / 迁 / 改 / 除 / 罢 / 谪 / 致仕 / 兼 / 领 / 督 / 巡抚 / 提督
/ 荐 / 升 / 召 / 起 / 历官 / 累官 / 累迁 / 徙 / 转 / 调 / 出（为/叅）/ 佥 / 掌
+ 官职词典（全文本内生）：学士 / 尚书 / 侍郎 / 御史 / 都给事中 / 给事中
/ 佥都御史 / 副都御史 / 按察使 / 布政使 / 佥事 / 参政 / 知府 / 知州 / 知县
/ 主事 / 郎中 / 员外郎 / 洗马 / 司业 / 祭酒 / 翰林 / 太常卿 / 兵备 / 总制 等
```

## 5. REL 人物关系层 schema（层库 C3 定制）

### 每卷标注 JSON

```
{
  "relations": [
    {
      "rel_id": "REL-001", "item_id": "01-001",
      "person_a": { "text": "杨溥", "person_ent_ids": ["ENT-020"] },
      "person_b": { "text": "范理", "person_ent_ids": ["ENT-021"] },
      "relation_type": "举荐", "direction": "单向",
      "evidence": "……（原文直接证据）", "original": "（打包器注入）"
    }
  ]
}
```

* `relation_type`：封闭枚举 REL_TYPES（下方快照 13 值）。
* `direction`：单向 / 双向 / 未明。
* **执行纪律**：只建文本有直接证据的关系，推测关系不建（宁缺毋滥）。

### REL_TYPES 快照（继承基准库 §1.4，13 值）

```
同僚 / 师生 / 姻亲 / 同乡 / 同科 / 举荐 / 弹劾 / 恩怨
/ 上下级（别名：主从）/ 父子亲属 / 敌对 / 同窗 / 其他
```

## 6. L5 事件层 schema

### 每卷标注 JSON

```
{
  "event_id": "XJF-E-001", "item_id": "01-001",
  "type": "轶事",
  "who": { "text": "宋濂", "who_ent_ids": ["ENT-001"] },
  "action": "却金", "what": "却日本使百金之献",
  "when": "未明", "where": "未明"
}
```

* 未明字段必须显式写 `"未明"`，不省略。
* `type`：封闭枚举 EVENT_TYPES 顶层规范全集（下方快照 23 值，**笔记/轶事体只继承顶层，不引入行政过程子类型**——enum-library §1.3 粒度规则）。

### EVENT_TYPES 顶层快照（继承基准库 §1.3.1，23 值）

```
朝政 / 政变 / 军事 / 军政 / 边事 / 人事任免 / 弹劾 / 礼仪 / 科举 / 文事
/ 建言 / 灾异 / 轶事 / 祭祀 / 经济 / 司法 / 神异传说 / 疾疫 / 御灾赈济
/ 缉捕防盗 / 巡查监察 / 家事 / 其他（兜底）
```

本书预期高频：朝政 / 人事任免 / 弹劾 / 建言 / 科举 / 文事 / 轶事 / 经济（却金拒贿类）/ 家事。

## 7. OPN 作者论说层 schema（层库 C9 定制）

### 每卷标注 JSON

```
{
  "opn_id": "OPN-001", "item_id": "01-001",
  "topic": "却金持节", "stance": "肯定",
  "argument": "（AI 解读要点，非原文）",
  "evidence_refs": [], "original": "（打包器注入）"
}
```

* `stance`：封闭枚举 OPN_STANCES（下方快照 5 值）。
* `argument` 只写要点概要不抄原文；与事件层分工：OPN 收"作者评价"，具体事件归 EVT。
* 触发词：论曰 / 愚按 / 耿子曰 / 余按 / 予谓 / 余以为 / 余闻 / 盖尝论（作者直接议论、判断、评价句）。

### OPN_STANCES 快照（继承基准库 §1.8，5 值）

```
肯定 / 否定 / 怀疑 / 讽刺 / 中立
```

## 8. TRL 古今翻译层 schema（层库 C5 定制）

### 每卷翻译 JSON

```
{
  "trl_id": "TRL-001", "item_id": "01-001",
  "translation": "……（现代译文）", "style": "直译",
  "note": "（翻译说明/专名处理，可选）", "confidence": 0.9,
  "original": "（打包器注入）"
}
```

* `style`：封闭枚举 TRL_STYLES（下方快照 3 值）。
* 全覆盖要求：代码验翻译数 = 条目数。
* 风格基准：默认"直译为主、意译达意、专名保留、四字格点缀"（未固化专属风格文件；必要时用户要求后再固化 `references/translation-style.md`）。

### TRL_STYLES 快照（继承基准库 §1.13，3 值）

```
直译 / 意译 / 注释性翻译
```

## 9. 跨层索引 schema

```
{
  "item_id": "01-001",
  "volume": "01", "source": "原文",
  "appts": ["APPT-001"], "rels": ["REL-001"],
  "events": ["XJF-E-001"], "opns": ["OPN-001"], "trls": ["TRL-001"],
  "ents": ["ENT-001","ENT-005","ENT-006"],
  "layer_count": 6
}
```

* 扁平 CSV 同字段平铺一行，`layer_count` 表示贯通层数（六层全贯通 = 6）。

## 10. 示例条目（试点校验样板）

> 2026-10-11 试点校验（Phase ④）通过：4 条真实条目（01-001 / 01-007 / 01-008 / 01-039）按六启用层试跑，字段/枚举/ID 命名空间无硬伤，见下表。执行期以此口径逐条判定；`original` 一律由打包器从 `_item_registry.json` 注入，AI 源数据不手写。

### 10.1 01-001（宋濂却金）

原文节选：`学士宋文宪公濓公尝曰……日本使奉勅请文以百金为献公郄不受上以问公公对曰天朝侍从之臣而受小夷金非所以崇国体也`

| 层 | 判定记录 |
|---|---|
| L1 实体 | person「宋濓→宋濂」ENT-001；official「学士」ENT-002（此处为"学士承旨"类侍从官简称）；place「日本」ENT-003；behavior「郄（却）不受」ENT-004；place「青萝山」ENT-005 |
| APPT | APPT-001 宋濂—学士—翰林（侍从）—when=未明—status=现任；APPT-002 宋濂—致仕—when=未明—status=致仕（"致仕居青萝山"） |
| REL | （无直接双主体证据，不建） |
| L5 事件 | XJF-E-001 type=轶事 who=宋濂 action=却金 what=却日本使百金之献 when=未明 where=未明 |
| OPN | （本条无作者直接议论，不建） |
| TRL | TRL-001 style=直译——"学士宋文宪公濂尝说：古人做学问，要使心正身修、落实于行事，俯仰无愧即可……日本使者奉敕请文、以百金为献，宋公推辞不受。皇上问起，公答道：天朝侍从之臣而受小夷之金，不是尊崇国体之道。" |

### 10.2 01-007（论曰：鲁公/刘忠宣并论）

原文节选：`论曰鲁公初第时即不忍厉其梓里如此……按鲁范两公皆天台人……（挽近世俗子一离黉序……）`

| 层 | 判定记录 |
|---|---|
| L1 实体 | person「鲁穆（鲁公）」ENT-010；person「刘忠宣（大夏）」ENT-011；person「范理（范令）」ENT-012；official「佥都御史」ENT-013；place「天台」ENT-014 |
| APPT | APPT-010 鲁穆—佥事（福建）—status=现任（"佥闽臬"）；APPT-011 鲁穆—佥都御史—status=升迁（文敏荐于宣庙"遂拜"）；APPT-012 刘忠宣—发解（举人）—status=未明 |
| REL | REL-010 杨文敏(荣)→鲁穆 举荐 单向；REL-011 杨文定(溥)→范理 举荐 单向（"文定之荐范令同"） |
| L5 事件 | XJF-E-010 type=科举 who=鲁穆 action=却赆 what=初第时恳辞台司佐赆 when=未明 where=未明；XJF-E-011 type=弹劾 who=鲁穆 action=绳法 what=法绳执政之家不少贷 when=未明 where=福建 |
| OPN | OPN-010 topic=鲁公初第却赆与绳法之事 stance=肯定 argument=赞鲁穆衷笃识远、念乡阻饥辞赆，斥挽近世俗子媚权贵。证据：「论曰」「达可知已」 |
| TRL | TRL-010 style=直译+注释性翻译（专名范理/鲁穆保留，括注身份） |

### 10.3 01-008（杨溥荐范理）

原文节选：`杨文定公溥执政时其子自乡来省至京邸……文定默识之即荐升徳安府知府甚有惠政民到今颂之再擢为贵州左布政使……逮后文定卒乃祭而哭之以谢知己云`

| 层 | 判定记录 |
|---|---|
| L1 实体 | person「杨溥（文定）」ENT-020；person「范理」ENT-021；official「知府」ENT-022；official「左布政使」ENT-023；place「德安府」ENT-024；place「贵州」ENT-025 |
| APPT | APPT-020 杨溥—宰相（执政）—when=未明—status=现任；APPT-021 范理—德安府知府—status=升迁（"荐升"）；APPT-022 范理—贵州左布政使—status=升迁（"再擢"） |
| REL | REL-020 杨溥→范理 举荐 单向（荐升知府）；REL-021 范理→杨溥 其他（感恩知己，致祭哭谢）方向=双向（原文"谢知己"为情感归属） |
| L5 事件 | XJF-E-020 type=人事任免 who=范理 action=荐升知府 what=杨文定默识范理贤而荐升德安府知府 when=未明 where=德安府；XJF-E-021 type=礼仪 who=范理 action=祭哭 what=文定卒后祭而哭之以谢知己 when=未明 where=未明 |
| OPN | （无作者直接议论句式，不建；"其贤""有惠政"属事件层判断） |
| TRL | TRL-020 style=直译——"杨文定公溥执政时，其子自乡来京……文定默记于心，即荐升（范理）为德安府知府，（范理）政绩甚佳，民到今颂之；后又擢为贵州左布政使……文定卒后，（范理）往祭而哭，以谢知己。" |

### 10.4 01-039（王阳明屠豕）

原文节选：`新建伯文成王先生守仁今制刑部有提牢厅置狱吏若干员……先生遂令屠豕割以分给诸囚狱吏到今不复豕云……嗣余贰刑曹时举以语同志友符卿孟秋氏问曰然则豕当终不屠耶余曰藉令先生知学后处此必微婉默运令发自堂卿不使善归已过归人矣`

| 层 | 判定记录 |
|---|---|
| L1 实体 | person「王守仁（文成）」ENT-030；official「主政」ENT-031；institution「刑部」ENT-032；institution「提牢厅」ENT-033；official「狱吏」ENT-034；punishment「大辟」ENT-035；animal「豕」ENT-036 |
| APPT | APPT-030 王守仁—主政（刑部提牢）—institution=刑部—status=现任（"筮仕刑曹适轮提牢"） |
| REL | （文中管姓主政/赵麟阳/孟秋仅叙及，关系证据不足，不建） |
| L5 事件 | XJF-E-030 type=司法 who=王守仁 action=禁豢豕 what=禁狱吏取囚饭豢豕、令屠豕分给诸囚 when=未明 where=刑部提牢厅；XJF-E-031 type=轶事 who=王守仁 action=自省 what=晚年悔少年屠豕以为不仁 when=未明 where=家居 |
| OPN | OPN-030 topic=屠豕自省 stance=肯定 argument=谓先生晚年自觉少年凭意见行事置堂卿于何地即不仁，非徒立异；作者（耿子）借孟秋问答引申"知学后必微婉默运、不使善归己过归人"。证据：「余曰藉令先生知学后处此……」 |
| TRL | TRL-030 style=意译+注释性翻译（"率兽食人食"引《孟子》典，译注并出） |

### 10.5 试点校验结论

- 六层字段全部符合 §3–§8 schema；ID 命名空间无跨层占用（ENT-/APPT-/REL-/XJF-E-/OPN-/TRL- 各自唯一）。
- 枚举值均命中基准库快照（ENTITY_TYPES 18 / APPT_STATUS 12 / REL_TYPES 13 / EVENT_TYPES 顶层 23 / OPN_STANCES 5 / TRL_STYLES 3），未触发新值收集。
- 无直接证据的关系（01-001/01-039 的旁及人物）按"宁缺毋滥"不建；"谢知己"用 REL 首选值「其他」+ 方向说明，避免臆造新枚举。
- 无作者论说句式（01-001/01-008）不强行建 OPN；作者评价句与事件记录按 §7 分工。
- norm 归一示例：濓→濂、竒→奇、徳→德、郄→却、豕 保留原字形、闾→闾（字形不变）；缺字括注 `■〈□〉` 保留。修正差异一律以 `_item_registry.json` 为唯一真源。

## 11. 枚举治理（registerVersion 模式 + V2/V3）

* 所有枚举收进 `scripts/_kg_enums.py`（单点文件）。
* **基准值继承**：本实例启用层枚举 = 上方快照（继承 `enum-library.md`），不自创词形；同义值别名映射归并。
* **本书归纳增量**：本书出现基准库外新值 → 收集-报告-暂存（pending 表，不中断）→ 收尾决议（新增/归并/暂存，新增须有实例证据 + 使用说明）→ registerVersion+1 → 回溯存量 → 更新基准库与实例快照（流程见工厂 `../book-knowledge-factory/references/enum-induction-guide.md`）。
* **V2 人工校验闭环**：同名异人（同号/同谥/同姓名，如书内多"文定公"）/存疑判定自动收集入"待核清单"CSV（含卷-条号 + evidence），人工核前不强行合并（宁建勿并），核后回写（合并 ENT / 改 normalized → 重跑对应打包器）。
* **V3 枚举校准**：执行期未匹配枚举值 → 收集-报告-暂存 → 收尾决议 → registerVersion+1 → 回溯存量；新增值必须有实例证据。
* **树状管理**：实例只继承顶层（事件/实体无子树）；枚举值带 `version`；新增值必须 version+1 并回溯全部存量，不允许静默扩容。
* 口径漂移检测：注释/文档中的枚举数与代码一致，验证脚本比对。