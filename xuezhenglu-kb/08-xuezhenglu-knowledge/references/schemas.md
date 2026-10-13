# 《政学录》实例 schema、枚举与触发词（启用层 + 契约登记）

> 本文件是本实例启用的**仅** L0/L1/L2/L4（ACT·FRD·LGR·TME）/跨层索引 的具体 schema、枚举、ID、触发词与**示例条目**（2026-10-12 试点校验通过后固化，压缩后不重读）。未启用层（L3 流程/L5 事件/C5/C11）不写。写源数据与打包器时读本文件。
> 格式契约见 `../../tools/book-mcp/`（C1–C7）；通用枚举基准见工厂 `../../Skills/00-book-knowledge-factory/references/enum-library.md`（实体/规则类型继承其规范值）；本书归纳增量（ACT/FRD/LGR/TME 类型）继承《吕公实政录》快照 + 本书校准，落 `_kg_enums.py`，执行期新增走 V3 枚举校准。

---

## 1. 卷号映射表（底座固定，不改）

| NN | 卷名 | 内容性质 | 条目方式 | 条数 | 条目 ID 范围 |
|---|---|---|---|---|---|
| 01 | 卷一（内阁/六部/科道 + 六部则例） | 清制则例 | 卷级条目（内阁/六部/科道 3 个）+ △ 标题条目 20 | 23 | 01-001..01-023 |
| 02 | 卷二（直省） | 直省事例 | ○ 标题条目 15（直隶~云南） | 15 | 02-001..02-015 |
| 03 | 卷三（官箴 + 钱粮技术·上） | 官箴政术（吕坤条文为主） | ○ 标题条目 111（戒营求~透支） | 111 | 03-001..03-111 |
| 04 | 卷四（吕叔简救命会 + 十家牌法） | 乡约保甲 | ○ 标题条目 2（超长条） | 2 | 04-001..04-002 |
| 05 | 卷五（状式 + 刑戒 + 狱政） | 刑狱（状式 24 + 刑戒 8） | ○ 标题条目 32 | 32 | 05-001..05-032 |

合计 **183 条**（180 个 ○/△ 标题条目 + 3 个卷级条目）。

**口径说明（与用户拍板"186 个标题条目"的关系）**：全本共 186 个 ○/△ 标题（○166 + △20）。其中 **6 个 ○ 为纯分组标题**（○吏部/户部/礼部/兵部/刑部/工部，无独立正文，其后直接 △ 条）**不作条目**（卷内分区标记，逻辑同《吕公实政录》排除"卷首篇目"列表）；另卷一"内阁/六部/科道"3 个无符号标题各有正文，作**卷级条目**。故 186 − 6 分组 + 3 卷级 = **183 条**。分组标题下的 △ 条、卷首"畿辅丛书/枣强郑端辑"署名行、"吏部/户部…"6 行总目、直省官职目录行（卷二卷首"督抚/布政司…"）均不计数。

## 2. 契约登记表（C4，Step 2 锁层产物；打包器与验证器照此表执行）

| layer_key | 目录 | ID 前缀（C2） | schema_fields（C6 必填） | enum_fields（C5 护栏） |
|---|---|---|---|---|
| ent | `_layers/ent/` | `ENT-` | ent_id, item_id, text, type, start, end, normalized, confidence, source | type |
| rule | `_layers/rule/` | `RULE-` | rule_id, item_id, type, modals, condition, subject, subject_ent_ids, action, object, purpose, punishment, original, confidence | type |
| struct | `_layers/struct/` | `ACT-` / `FRD-` / `LGR-` / `TME-`（维度前缀） | struct_id, item_id, dim, <维度字段>, target, evidence, original, confidence | dim + 各维度类型字段（act_type/frd_type/lgr_type/tme_type） |
| reg | `_layers/reg/` | `REG-` | reg_id, item_id, name, type, content, evolution, target, original, confidence | type |
| evt | `_layers/evt/` | `EVT-` | event_id, item_id, type, who, who_ent_ids, action, what, when, where, original, confidence | type |
| kg_join | `_kg_join.json` / `_kg_join_flat.csv` | — | item_id, volume, source, rules, regs, events, structs, ents, layer_count | — |
| review（V2） | `_validate/同名异人待核清单.csv` | — | ent_id 或源位置, 人名, 身份四元组, 来源卷, nam_id, 原因, 建议 | — |
| enum_calib（V3） | `_validate/_pending_enums.csv` | — | layer, field, value, item_id, 证据 | — |

- ID 前缀全局唯一（C2）：ENT-/RULE-/ACT-/FRD-/LGR-/TME-/REG-/EVT- 不与任何其他层撞。
- item_id = `NN-NNN`（卷-序）全书唯一（C2/C3）。
- 结构化层 struct_id 分配：`<维度前缀><段位序号>`（打包器分配）；rule 同 `RULE-<段位序号>`；ent 同 `ENT-<段位序号>`（全局主键表，跨卷累积）。

---

## 3. 底座 schema（C3）

### 3.1 条目切分（_extract\NN_卷名.txt）

```
条N|○/△标题（若有）|正文（自标题后至下一标题/卷尾，去除卷首署名行/总目行/官职目录行）
卷级条目：条N|标题|整段正文（卷一内阁/六部/科道）
```
- 卷拆分文件（`政学录_卷一~五.txt`）**标题与正文分行**：`○戒营求` 为标题行，其后各行至下一标题行为正文；切分时合并标题行 + 正文行。
- 全文合并版（`政学录_全文.txt`）为"标题　正文"同行格式，作**交叉校验**（每卷条数与标题名逐一比对）。
- 缺字 `□`/`■〈…〉` 保留原形。

### 3.2 指纹库（_item_registry.json，只读、只入不出）

```json
{
  "03-001": {
    "original": "○戒营求\n戒营求　临选时垂涎膻地营求打点…",
    "norm": "戒营求　临选时垂涎膻地营求打点…（异体归一后）"
  }
}
```
- norm 归一规则：繁体/异体→规范简体（厯→历、廵→巡、覈→核、曡→叠、賸→剩、悞→误、紏→纠、咨→咨）；缺字保留原形；标点按现代句读。
- `_src/` AI 源数据**绝不手抄原文**（C3），original 由打包器从指纹库注入。
- 白话文对照：`_baihua_map.json` 维护 `item_id → 白话文段落`（从 `assets/sources/政学录_全文_白话.txt` 按标题对应截取）。

---

## 4. 枚举单点 _kg_enums.py（C5，xuezhenglu-kb 根；打包器只从它读）

```python
# -*- coding: utf-8 -*-
"""《政学录》枚举单点。版本：1.0（2026-10-12 实例化）。
继承基准库快照（enum-library.md v5）+ 《吕公实政录》归纳快照 + 本书校准；改值须 version+1 并双写 enum-changelog.md。"""

VERSION = "1.0"

ENTITY_TYPES = [
    "person", "official", "institution", "place", "era", "work",
    "object", "animal", "plant", "food", "doc", "system",
    "behavior", "punishment", "time", "quantity", "posthumous",
    "star", "event", "unknown",          # 基准库 20 值封闭全集
]
ENTITY_ACTIVE = ["person", "official", "institution", "place", "era", "work",
                 "doc", "system", "behavior", "punishment", "time", "quantity", "unknown"]
ENTITY_ALIASES = {"office": "official", "org": "institution", "book": "work"}

RULE_TYPES = ["prohibit", "obligation", "allow", "procedure", "deadline", "penalty", "priority"]
RULE_TYPES_ZH = {"prohibit": "禁止型", "obligation": "义务型", "allow": "允许型",
                 "procedure": "程序型", "deadline": "时限型", "penalty": "处罚型", "priority": "优先级型"}

ACT_TYPES = ["official", "xiangyue_role", "justice_role", "clerk_role", "other"]
ACT_TYPES_ZH = {"official": "官职", "xiangyue_role": "乡约角色", "justice_role": "司法刑狱角色",
                "clerk_role": "文书角色", "other": "其他"}

FRD_TYPES = ["abuse", "guard", "evil_custom", "other"]
FRD_TYPES_ZH = {"abuse": "积弊", "guard": "防弊措施", "evil_custom": "恶风禁忌", "other": "其他"}

LGR_TYPES = ["ledger", "geye", "template_form", "board", "voucher", "other"]
LGR_TYPES_ZH = {"ledger": "簿册", "geye": "格叶", "template_form": "状式",
                "board": "榜牌", "voucher": "单据", "other": "其他"}

TME_TYPES = ["deadline", "meeting", "assessment", "season", "age_limit", "other"]
TME_TYPES_ZH = {"deadline": "期限", "meeting": "会期", "assessment": "考绩期",
                "season": "节令农时", "age_limit": "年龄时限", "other": "其他"}
```
- 打包器硬校验：任何 `type`/`dim`/`act_type`/`frd_type`/`lgr_type`/`tme_type` 取值不在上述定义集 → 记 **ERR**（写入验证缺漏清单，不静默放行）。
- 执行期未匹配值 → `_validate/_pending_enums.csv` 收集 → 收尾决议（新增/归并/改名）→ registerVersion+1 → 回溯存量（V3）。

---

## 5. 实体层（ent）schema

### 5.1 记录字段

| 字段 | 必填 | 说明 |
|---|---|---|
| ent_id | ✅ | 打包器分配 `ENT-<段位序号>`（全局唯一，跨卷复用） |
| item_id | ✅ | 条目 ID（`NN-NNN`） |
| text | ✅ | 原文词形（异体字保留） |
| type | ✅ | 枚举：ENTITY_ACTIVE |
| start/end | ✅ | 在原文中的字符偏移 |
| normalized | ✅ | 归一词形（异体→规范） |
| confidence | ✅ | 判定置信度（0-1） |
| source | ✅ | `"政学录·卷N"` |

### 5.2 触发词与种子（全文本内生，词条必须出现在原文）

- 衙门官职：内阁、六部、科道、部院、督抚、布政司、按察司、提学道、守巡道、盐运司、知府、同知、通判、推官、知州、知县、州县佐贰、教官、库官、司狱司、刑房吏、禁子、牢头、仵作、书办、掌印官、问官
- 制度：选法、考课、京察、大计、军政、考满、钱粮、漕运、漕粮、盐课、关税、钱法、秋审、结案、祀典、士额、屯田、逃人、纤夫、一条鞭、赋役
- 文书：状式（告辜式/告检式/告盗情状式/告辩盗状式/告奸情状式/告打诈状式/告地土状式/告婚姻状式/告赌博状式/告陵夺状式/告保盗状式/告贪污状式/告故勘状式/告科敛状式/告侵欺状式/告窝访状式/告土豪状式/告财产状式/告钱债状式/告欺害状式/告唆诬状式/告诡隐状式/告抗粮状式/告重收状式）、刻册、底簿、廒经流水、批回、由票、柜式、甘结、揭帖
- 人名：吕坤（吕叔简）、王守仁、邹南皋、卢兴祖、田六善、李天裕、姚文然、于可托、张松龄、戈英、季振宜、薛奋生、张冲翼、吴国龙、徐惺、林起龙、赵廷臣、宋礼、陈瑄、周文襄、胡亮、滕昭、张居正
- 地名：直隶、江南、河南、山东、山西、陕西、浙江、福建、广西、广东、江西、湖广、四川、贵州、云南 + 府州（泰安州/华阴县/衡山县…）
- 纪年：顺治、康熙、万历、洪武、永乐、嘉靖 + 年号纪年（顺治十八年七月/康熙二年五月…）

### 5.3 归一规则

- 异体/繁体→简体（同底座 norm）。
- 同义复合词形（"督臣卢兴祖"→卢兴祖、"台臣田六善"→田六善、"明臣吕坤"→吕坤）用 alias_index 手工映射，不动标注。
- **跨书对齐**：吕坤条文/状式名/狱政术语与《吕公实政录》词形尽量一致（状式名完全相同、钱粮条目同名），联邦并入时跨书查重。

---

## 6. 规则层（rule）schema

### 6.1 记录字段

| 字段 | 必填 | 说明 |
|---|---|---|
| rule_id | ✅ | 打包器分配 `RULE-<段位序号>` |
| item_id | ✅ | 条目 ID |
| type | ✅ | 枚举：RULE_TYPES |
| modals | ✅ | 模态词（不许/务要/须/限…） |
| condition | 条件式（"违者""限内""若有X"） |
| subject | ✅ | 主体（谁要遵守） |
| subject_ent_ids | 主体对应 ENT id 数组 |
| action | ✅ | 动作/行为规范 |
| object | 对象 |
| purpose | 目的（"以…""庶…"） |
| punishment | 处罚（"违者…责罚/革职/题参"） |
| original | ✅ | 原文句（打包器注入） |
| confidence | ✅ | 0-1 |

### 6.2 触发词表（候选引擎，AI 逐条复核）

`不许 / 不得 / 务要 / 须 / 止许 / 只许 / 许 / 毋 / 勿 / 禁 / 严禁 / 责罚 / 重责 / 枷号 / 挐问 / 访察 / 参降 / 革职 / 处分 / 题参 / 限 N 日 / 不过 N 日 / 违者 / 犯者 / 依律 / 定行 / 照例 / 例`

### 6.3 组合规则口径（定死）

- 一条规范句 = 一个规则单元，type 取行为规范主模态；"违者/犯者…"处罚并入同条 punishment 槽位，不单拆处罚型。
- 并列多个独立行为规范（"一不许X 二不许Y"型）拆多条共享 item_id。
- 一句多模态（"许X 但限 N 日"）type 取约束更强的一方。
- **则例体**（卷一~二）：部覆/奉旨引出的"见行事例"以程序/时限/禁止/义务型抽规则；制度沿革叙事（"旧例…后改…"）取**现行有效**规范抽，历史演变说明不抽（归 L1 制度实体 + L4）。
- **官箴体**（卷三~五）：戒条（"不可/勿/不许"）逐条抽；劝诫说理句（"嗟乎/呜呼"引出的议论）不抽。

---

## 7. 结构化层（struct）schema（四维）

| 字段 | 必填 | 说明 |
|---|---|---|
| struct_id | ✅ | 打包器分配 `<维度前缀><段位序号>`（ACT-/FRD-/LGR-/TME-） |
| item_id | ✅ | 条目 ID |
| dim | ✅ | 枚举：ACT / FRD / LGR / TME |
| act_type/frd_type/lgr_type/tme_type | ✅（按 dim） | 维度类型枚举（_kg_enums.py） |
| target | target 用 ID 引用（ENT-id 或 struct 自身 ID），可空 |
| evidence | ✅ | 判定依据（原文要点，非抄句） |
| original | ✅ | 原文句（打包器注入） |
| confidence | ✅ | 0-1 |

四维对象（继承 lgs 归纳，本书校准）：

| 维度 | 对象（本书） | 类型（启用子集） |
|---|---|---|
| ACT 角色职责 | 衙门职掌（内阁六部科道职责）、官职（督抚/州县/佐贰/首领官）、刑狱角色（掌印官/问官/狱卒/禁子/牢头/仵作/皂快）、书吏（刑房吏/书办）、乡约角色（十家牌法牌长） | official / xiangyue_role / justice_role / clerk_role / other |
| FRD 防弊风险 | 积弊（银库之弊/抬银之害/透支/逃人之弊/狱弊牢头/吏辈下乡/重迭催科）、防弊（银库防闲/禁抬银/查比批回/隔别细审/刻册稽核）、恶风（奢侈/健讼/窝盗） | abuse / guard / evil_custom / other |
| LGR 文簿台账 | 簿册（刻册/底簿/廒经流水/比较刻册/收支册/监仓二簿）、状式（告辜式等 24 种）、单据（由票/批回/甘结/揭帖/关防）、牌榜（十家牌/印册） | ledger / geye / template_form / board / voucher / other |
| TME 时间制度 | 限期（限 N 日/开征月份/奏销岁终）、考绩期（六年京察/三年大计/五年军政/考满）、会期（选法日期）、季节（农忙停催） | deadline / meeting / assessment / season / age_limit / other |

---

## 7.5 制度层（reg）schema（2026-10-12 增量启用）

| 字段 | 必填 | 说明 |
|---|---|---|
| reg_id | ✅ | 打包器分配 `REG-<段位序号>` |
| item_id | ✅ | 条目 ID |
| name | ✅ | 制度名（如"选法/一条鞭/十家牌法"） |
| type | ✅ | 枚举：REG_TYPES（_kg_enums.py） |
| content | ✅ | 制度内容要点（AI 解读非原文，不抄句） |
| evolution | 沿革要点（"旧例…后改…"），无则空 |
| target | 引用 L1 ent（制度名实体 ID）或 reg 自身 ID，可空 |
| original | ✅ | 原文句（打包器注入） |
| confidence | ✅ | 0-1 |

- 触发词：选法/考课/京察/大计/军政/考满/钱粮/赋役/漕粮/盐课/关税/钱法/一条鞭/十家牌/保甲/状式/狱政/保辜/秋审/结案/则例/屯田/纤夫/逃人/祀典/士额/兵制
- 一条目多制度拆多条共享 item_id；沿革叙事记 evolution，事件过程归 EVT（分工见 SKILL.md §5.5）。

## 7.6 事件层（evt）schema（2026-10-12 增量启用）

| 字段 | 必填 | 说明 |
|---|---|---|
| event_id | ✅ | 打包器分配 `EVT-<段位序号>` |
| item_id | ✅ | 条目 ID |
| type | ✅ | 枚举：EVENT_TYPES（继承基准库 §1.3 顶层 27 值，封闭+兜底） |
| who | ✅ | 行为主体（科臣/部院/皇帝/官员名，含 who_ent_ids） |
| action | ✅ | 动作（条陈/会覆/奉旨/改用/立…法） |
| what | ✅ | 事件内容要点（AI 解读） |
| when | 纪年（"顺治十八年七月"），未明写"未明" |
| where | 未明写"未明" |
| original | ✅ | 原文句（打包器注入） |
| confidence | ✅ | 0-1 |

- 触发词：条陈/会覆/疏称/疏曰/部覆/覆准/议准/奏准/奉旨/得旨/上谕/请旨/降旨 + 纪年（顺治/康熙/万历…+年月）+ 人名+动作（张松龄条陈/吴国龙条议/张居正改条鞭/王守仁立十家牌）
- 执行口径：**集中在卷一~二**（则例沿革叙事）；卷三~五规范句为主不强行造事件（如实记缺口）；"臣疏→部覆→奉旨"全链记 1 个 EVT（type 取主导）；沿革叙事 EVT + REG 双记（EVT 收过程、REG 收制度结果）。

---

## 8. 试点示例条目（2026-10-12 试点校验通过，schema 样例固化）

### 8.1 01-004 △选法（则例体）
- **ent**（节选）：`选法`(system, 01-004)、`大选`(system)、`急选`(system)、`投供点卯`(behavior)、`吏部`(institution)、`张松龄`(person)、`于可托`(person)、`戈英`(person)、`顺治十八年`(era)
- **rule**：
  - `RULE-*` 程序型："大选官员单月十五日投供点卯，双月二十三日选补；急选官员双月十五日投供，单月二十三日补授" → subject=应选官员, action=投供点卯/对缺封签/补授, modals=[单月/双月/十五日/二十三日], type=procedure, deadline 语义并入 condition
  - `RULE-*` 时限型："候选官员如丁忧患病亡故，该地方官随申报该抚，该抚报部注册扣选；迟延不报者以疏略之罪处分" → type=deadline + penalty
- **struct**：
  - `TME-*` deadline：选法日期制度（单月十五日投供/双月二十三日点卯/二十五日除选），target→ENT 选法
  - `ACT-*` official：吏部选法职掌（投供点卯/对缺封签），target→ENT 吏部

### 8.2 03-001 ○戒营求（官箴体）
- **ent**：`戒营求`(behavior)、`临选`(time)、`营求打点`(behavior)、`削籍`(punishment)
- **rule**：禁止型"临选时垂涎膻地营求打点" → subject=候选官, action=营求打点, punishment=为债所逼/削籍, modals=[可戒], type=prohibit
- **struct**：`FRD-*` abuse：营求打点积弊（临选营求→到任掣肘→削籍）

### 8.3 03-078 ○一条鞭（钱粮技术）
- **ent**：`一条鞭`(system)、`隆庆`(era)、`张居正`(person)、`漕南二米`(system)、`折银`(behavior)、`钱粮`(system)
- **rule**：义务型"凡一切应征应役等项尽折银一起征取，此外别无杂派" → subject=州县, action=一条鞭征收, purpose=简省明白/不误农时, type=obligation
- **struct**：`LGR-*` ledger？或 system 说明。一条鞭是赋役制度：`ACT-*` official（收头征取）或归 L1 system。struct 可记 `LGR-*` voucher（折银征收单据简化）？——口径：一条鞭属制度说明，不强行 struct；若记，记 FRD guard（防杂派之弊）。**试点口径：本类"制度说明型"条目以 ent+rule 为主，struct 视对象而定（防弊机制才记 FRD）**

### 8.4 05-001 ○人命告辜式（状式）
- **ent**：`人命告辜式`(doc)、`保辜`(system)、`状式`(doc)、`仵作`(official)
- **rule**：时限型"路远告辜不得过五日" → subject=告辜人, action=告辜, deadline=不得过五日, type=deadline；禁止型"不许多报一处，不许妄增一分，违者看明重究" → type=prohibit + penalty
- **struct**：
  - `LGR-*` template_form：人命告辜式（状式 24 种之一：首列限制语+本县某里某人为殴伤事…格式），target→ENT 人命告辜式
  - `TME-*` deadline：告辜期限（不得过五日），target→ENT 保辜

### 8.5 05-025 ○五不打（刑戒）
- **ent**：`五不打`(behavior)、`老不打`(behavior)、`拷讯`(behavior)、`律文`(work)
- **rule**：禁止型"老不打/幼不打/病不打/衣食不继不打/人打我不打" → subject=有司, action=用刑, condition=老幼病/衣食不继/已受刑, type=prohibit（五条并列拆多条共享 item_id）
- **struct**：`FRD-*` guard：刑戒防弊（五不打防用刑致死），target→ENT 五不打

> 试点结论：① 卷文件标题与正文分行，切分需合并；② 则例体规则取现行有效规范；③ 制度说明型条目（一条鞭）struct 不强建；④ 状式= LGR template_form + TME deadline 双维；⑤ 刑戒= FRD guard。schema 无硬伤，可全量执行。

### 8.6 01-004 △选法（REG + EVT 增量试点，则例体）
- **reg**：
  - `REG-*` 铨选考课：选法（大选/急选投供点卯制度：大选单月十五投供/双月二十三封签/二十五除选；急选双月十五投供/单月二十三封签/二十五补授），evolution="顺治十八年张松龄条陈改在籍候选；康熙二年于可托条陈寄凭之制"，target→ENT 选法
- **evt**：
  - `EVT-*` 建言/制度：who=科臣张松龄（科道），action=条陈，what=点卯候选旅寄京师之弊，请改在籍候选，when=顺治十八年七月
  - `EVT-*` 建言：who=科臣于可托，action=条陈，what=寄凭之制，when=康熙二年五月

### 8.7 01-006 △钱粮总归户部（REG + EVT 增量试点，则例体）
- **reg**：`REG-*` 钱粮赋役：钱粮归户部总理（赋役全书订算 + 各省简明赋役之书 + 易知由单止开丁地钱粮名色），evolution="康熙二年四月户部会覆吴国龙条议"，target→ENT 钱粮
- **evt**：`EVT-*` 制度/建言：who=户部 + 科臣吴国龙，action=条议/会覆，what=一应钱粮俱归户部总理，责令各抚造简明赋役之书，when=康熙二年四月

### 8.8 03-078 ○一条鞭（REG + EVT 增量试点，制度说明型）
- **reg**：`REG-*` 钱粮赋役：一条鞭（除漕南二米不折外一切应征应役尽折银一起征取，别无杂派），evolution="隆庆前差役烦琐→张居正当国改用条鞭"，target→ENT 一条鞭
- **evt**：`EVT-*` 制度：who=张居正，action=改用条鞭，what=一条鞭法（折银征收），when=万历初（隆庆后）
- **struct**：不强建（试点结论③延续）

### 8.9 04-002 ○王守仁十家牌法（REG + EVT 增量试点，超长条）
- **reg**：`REG-*` 保甲乡约：十家牌法（父老子弟各务孝慈和睦 + 十家牌式：某县某坊某人某籍×十家轮牌省晓），target→ENT 十家牌法
- **evt**：`EVT-*` 制度：who=王守仁，action=立十家牌法（告谕父老子弟），what=十家牌式劝勉惩戒，when=未明

### 8.10 05-001 ○人命告辜式（REG 增量试点，状式——EVT 记缺口）
- **reg**：`REG-*` 刑名狱政：保辜/告辜制度（告辜式限制语：不许多报一处/不许妄增一分/路远告辜不得过五日），target→ENT 保辜
- **evt**：无（状式为规范模板非叙事，**如实记缺口**，不强行造事件）

> 增量试点结论（2026-10-12）：① REG 与 L4 分工清晰（REG 收制度本体、L4 收维度切片），无冲突；② EVT 集中在卷一~二则例沿革，卷三~五多为缺口如实记；③ 沿革叙事 EVT+REG 双记（过程+结果）；④ 状式/刑戒类条目 EVT 为缺口不造事件。schema 无硬伤。

---

## 9. 坑注（本书特有，执行时对照）

1. **卷拆分文件标题与正文分行**（`○戒营求` 一行 + 正文下一行起）——切分时合并，勿把标题行当全文。
2. **○ 分组标题 6 个**（吏部等）无正文不作条目；卷首署名/总目/官职目录行不计数（口径见 §1）。
3. **正文内「【…】」括注**为编者批注（如告辜式首行限制语），保留在条目标题/正文内，抽取规则时作条件语。
4. **与 lgs 重叠条目**（状式/狱政/钱粮条文）归一尽量对齐，勿自造异形。
5. 源数据（_src 的 .py）**一次 Write 写全文件**（多次 Write 是整体覆盖不是追加，lgs 教训）。
6. struct 维度类型字段必填且值命中枚举，缺字段/错值会被打包器**静默丢条**（lgs 教训）。
7. **REG/EVT 执行口径（增量 2026-10-12）**：REG content 只写要点不抄原文；EVT 全链"臣疏→部覆→奉旨"记 1 条不拆多次；卷一~二重点抽事件，卷三~五事件稀少如实记缺口；EVENT_TYPES 继承基准库顶层 27 值不本书新增，未匹配值走 V3。
