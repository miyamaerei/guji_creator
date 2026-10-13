# 《吕公实政录》实例 schema、枚举与触发词（启用层 + 契约登记）

> 本文件是本实例启用的**仅** L0/L1/L2/L4（ACT·FRD·LGR·TME）/跨层索引 的具体 schema、枚举、ID、触发词与**示例条目**（2026-10-12 试点校验通过后固化，压缩后不重读）。未启用层（L3 流程/L5 事件/C1/C5/C11）不写。写源数据与打包器时读本文件。
> 格式契约见 `../../tools/book-mcp/`（C1–C7）；通用枚举基准见工厂 `../../Skills/00-book-knowledge-factory/references/enum-library.md`（实体/规则类型继承其规范值）；本书归纳增量（ACT/FRD/LGR/TME 类型）落 `_kg_enums.py`，执行期新增走 V3 枚举校准。

---

## 1. 卷号映射表（底座固定，不改）

分部 → 卷号 → 卷名 → 条目方式 → 条目数：

| NN | 分部 | 卷名 | 条目方式 | 条数 | 条目 ID 范围 |
|---|---|---|---|---|---|
| 01 | 明职 | 明职·新吾吕先生实政录序 | 卷级条目 | 1 | 01-001 |
| 02 | 明职 | 明职·明职引 | 卷级条目 | 1 | 02-001 |
| 03 | 明职 | 明职·卷一 | ○/△ 标题条目 | 26 | 03-001..03-026 |
| 04 | 民务 | 民务·卷之二 | ○/△ 标题条目 | 13 | 04-001..04-013 |
| 05 | 民务 | 民务·卷之三 | ○/△ 标题条目 | 8 | 05-001..05-008 |
| 06 | 民务 | 民务·卷之四 | ○/△ 标题条目 | 14 | 06-001..06-014 |
| 07 | 乡甲约 | 乡甲约·卷之一 | 卷级条目（长文告示） | 1 | 07-001 |
| 08 | 乡甲约 | 乡甲约·卷之二 | ○/△ 标题条目 | 6 | 08-001..08-006 |
| 09 | 乡甲约 | 乡甲约·卷之三 | 卷级条目（格叶：和处） | 1 | 09-001 |
| 10 | 乡甲约 | 乡甲约·卷之四 | 卷级条目（格叶：纪善） | 1 | 10-001 |
| 11 | 乡甲约 | 乡甲约·卷之五 | 卷级条目（格叶：纪恶） | 1 | 11-001 |
| 12 | 乡甲约 | 乡甲约·卷之六 | 卷级条目（格叶：改过） | 1 | 12-001 |
| 13 | 风宪约 | 风宪约·重刊风宪约序 | 卷级条目 | 1 | 13-001 |
| 14 | 风宪约 | 风宪约·卷之一 | ○/△ 标题条目 | 35 | 14-001..14-035 |
| 15 | 风宪约 | 风宪约·卷之二 | ○/△ 标题条目 | 9 | 15-001..15-009 |

合计 **119 条**。条目标题清单：各卷按原书顺序；正文 `○`/`△` 行即为标题行（`（卷首篇目）` 列表仅供切分参考，**不重复计数**——见 §9 坑注）。标题行中 `【…】` 括注为编者批注，保留在条目标题内。

---

## 2. 契约登记表（C4，Step 2 锁层产物；打包器与验证器照此表执行）

| layer_key | 目录 | ID 前缀（C2） | schema_fields（C6 必填） | enum_fields（C5 护栏） |
|---|---|---|---|---|
| ent | `_layers/ent/` | `ENT-` | ent_id, item_id, text, type, start, end, normalized, confidence, source | type |
| rule | `_layers/rule/` | `RULE-` | rule_id, item_id, type, modals, condition, subject, subject_ent_ids, action, object, purpose, punishment, original, confidence | type |
| struct | `_layers/struct/` | `ACT-` / `FRD-` / `LGR-` / `TME-`（维度前缀） | struct_id, item_id, dim, <维度字段>, target, evidence, original, confidence | dim + 各维度类型字段（act_type/frd_type/lgr_type/tme_type） |
| kg_join | `_kg_join.json` / `_kg_join_flat.csv` | — | item_id, volume, source, rules, structs, ents, layer_count | — |
| review（V2） | `_validate/同名异人待核清单.csv` | — | ent_id 或源位置, 人名, 身份四元组, 来源卷, nam_id, 原因, 建议 | — |
| enum_calib（V3） | `_validate/_pending_enums.csv` | — | layer, field, value, item_id, 证据 | — |

- ID 前缀全局唯一（C2）：ENT-/RULE-/ACT-/FRD-/LGR-/TME- 不与任何其他层撞。
- item_id = `NN-NNN`（卷-序）全书唯一（C2/C3）。
- 结构化层 struct_id 分配：`<维度前缀><段位序号>`（打包器分配）；rule 同 `RULE-<段位序号>`；ent 同 `ENT-<段位序号>`（全局主键表，跨卷累积）。

---

## 3. 底座 schema（C3）

### 3.1 条目切分（_extract\NN_卷名.txt）

```
条N|○标题文本|正文（自标题行后至下一标题/卷尾，去除（正文）（卷首篇目）标注行）
```
卷级条目：`条1|卷名|整卷正文（含"计开"与条件列表，不单独编号）`

### 3.2 指纹库（_item_registry.json，只读、只入不出）

```json
{
  "03-002": {
    "original": "○仓官之职\n朝廷钱粮黎庶膏血…",
    "norm": "朝廷钱粮黎庶膏血…（异体归一后）"
  }
}
```
- norm 归一规则：繁体/异体→规范简体（廵→巡、飬→养、枽→桑、貯→贮）；缺字 `□`/`■〈…〉` 保留原形；标点按现代句读。
- `_src/` AI 源数据**绝不手抄原文**（C3），original 由打包器从指纹库注入。
- 白话文对照：`_baihua_map.json` 维护 `item_id → 白话文段落`（从 `assets/sources/吕公实政录_白话文_全卷合并.txt` 按 ◆/○/△ 标题对应截取；卷级条目按卷截取）。

---

## 4. 枚举单点 _kg_enums.py（C5，shizhenglu-kb 根；打包器只从它读）

```python
# -*- coding: utf-8 -*-
"""《吕公实政录》枚举单点。版本：1.0（2026-10-12 实例化）。
继承基准库快照（enum-library.md v4）+ 本书归纳增量；改值须 version+1 并双写 enum-changelog.md。"""

VERSION = "1.0"

ENTITY_TYPES = [
    "person", "official", "institution", "place", "era", "work",
    "object", "animal", "plant", "food", "doc", "system",
    "behavior", "punishment", "time", "quantity", "posthumous",
    "star", "event", "unknown",          # 基准库 20 值封闭全集
]
# 本书实际启用子集（未启用值保留在全集，标注不参与本书判定）：
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

### 5.1 标注 schema（每卷 `_src/_ents_ai_NN.py`）

```json
{"records": [
  {"slot": 1, "item_id": "03-002", "text": "仓官", "type": "official",
   "start": 0, "end": 2, "normalized": "仓官", "confidence": "high", "source": "03-002"}
]}
```
- 槽位规则：AI 源数据只写卷内顺序槽位（slot），业务 ID（ENT-xxx）由打包器分配（C2）。
- 归一：同义复合词形（"把门皂隶"→皂隶）进 alias_index 手工映射，不动标注。
- 种子词表（全文本内生校验）：见 SKILL.md §3 清单；词条必须出现在原文。

### 5.2 主键表

- `ENT-001..N` + `alias_index.json`（词形 → ent_id）。

---

## 6. 规则层（rule）schema

### 6.1 触发词表（候选引擎 → AI 逐条复核）

```
不许 / 不得 / 务要 / 须 / 止许 / 只许 / 许 / 毋 / 勿 / 禁 / 禁约 / 严禁
/ 责罚 / 重责 / 枷号 / 挐问 / 访察 / 参降 / 革役 / 注考 / 限 N 日 / 不过 N 日
/ 违者 / 犯者 / 依律 / 定行 / 即 / 仍
```

### 6.2 规则 schema（每卷 `_src/_rules_ai_NN.py`）

```json
{"records": [
  {"slot": 1, "item_id": "03-002", "type": "obligation",
   "modals": ["务使", "常要"],
   "condition": "为仓官者收谷之时",
   "subject": "仓官", "subject_ent_ids": [],
   "action": "收时要极干极净，量时要极早极平",
   "object": "仓谷",
   "purpose": "米谷不红腐、出纳无亏",
   "punishment": "",
   "confidence": "high"}
]}
```
（original 由打包器从指纹库注入，源数据不写。）

### 6.3 组合规则口径（定死）

1. 一条规范句 = 一个规则单元，type 取主模态；
2. "违者/犯者…"处罚并入同条 `punishment`，不单拆处罚型；
3. 一句并列多个独立行为规范（"一不许X 二不许Y"）拆多条共享 item_id；
4. 一句多模态（"许X 但限 N 日"）type 取约束更强一方；
5. 明职训谕体逐规范句抽规则；纯说理/劝诫（"呜呼/嗟夫/试自思之"段）不抽。

---

## 7. 结构化层（struct）schema（四维）

### 7.1 记录 schema（每卷 `_src/_struct_ai_NN.py`）

```json
{"records": [
  {"slot": 1, "item_id": "03-002", "dim": "ACT", "act_type": "official",
   "role": "仓官", "role_ent_ids": [],
   "responsibility": "收谷极干极净、量谷极早极平、防雨湿水浸雀鼠、盛暑翻谷、出纳升合不欠、册籍明",
   "target": "", "evidence": "为仓官者收时要极干极净…", "confidence": "high"},
  {"slot": 2, "item_id": "03-002", "dim": "FRD", "frd_type": "abuse",
   "issue": "仓官积弊", "detail": "收时刁难纳户、滥派湿粃、斗头加耗、短升少合零取碎侵",
   "countermeasure": "", "target": "", "evidence": "而今做仓官的地湿房漏全然不理…", "confidence": "high"}
]}
```
- `target` 用 ID 引用（如 ACT 引用 ENT / LGR 引用自身 ID），不写文本。
- 一条目多记录：多 slot；同一维度多记录共享 item_id。
- 维度字段（随 dim 出现）：ACT→`role, role_ent_ids, responsibility`；FRD→`issue, detail, countermeasure`；LGR→`item, purpose, template_fields, usage_note`；TME→`name, detail`。

---

## 8. 跨层索引 schema（kg_join，打包器产出）

```json
{"records": [
  {"item_id": "03-002", "volume": "03", "source": "明职·卷一",
   "rules": ["RULE-0001", "RULE-0002", "RULE-0003"],
   "structs": ["ACT-0001", "FRD-0001", "LGR-0001", "TME-0001"],
   "ents": ["ENT-0001", "ENT-0002"],
   "layer_count": 4}
]}
```
- `_kg_join_flat.csv` 同结构拍平（每行一条目，Excel 直开）。
- 规则/结构化业务 ID 由打包器分配（段位制：卷号 × 500 + 卷内序）。

---

## 9. 示例条目（2026-10-12 试点校验，schema 验证通过后固化）

> 试跑 5 条真实条目：03-002 仓官之职（明职·训谕体）、04-011 振举医学（民务·条款体）、08-001 乡甲至要（乡甲约·规则体）、14-002 人命（十二款）（风宪约·程序/时限体）、14-011 告盗情状式（风宪约·状式模板）。校验结论：条目 ID/实体类型/规则类型/四维枚举均在启用值内；状式类条目无规则、归 LGR（type=template_form）；训谕体逐规范句抽规则、说理段不抽；枚举值全部落在 `_kg_enums.py` 定义集（C5 无 ERR）。以下为有代表性的精简示例（每条 1-2 条记录），全量以真实标注为准。

### 9.1 03-002 仓官之职（训谕体 → 规则 5+ 条）

```json
{"rules": [
  {"slot": 1, "item_id": "03-002", "type": "obligation", "modals": ["务使", "常要"],
   "condition": "为仓官者收谷", "subject": "仓官", "subject_ent_ids": [],
   "action": "收时要极干极净，量时要极早极平；仓中之地务使干燥，上防雨湿下防水浸",
   "object": "仓谷", "purpose": "米谷不红腐", "punishment": "", "confidence": "high"},
  {"slot": 2, "item_id": "03-002", "type": "obligation", "modals": ["要", "务使"],
   "condition": "盛暑连阴之月", "subject": "仓官",
   "action": "禀讨官钥将谷翻上倒下，务使熏蒸湿热之气得以宣泄，每岁如此三番",
   "object": "仓谷", "purpose": "米谷不红腐", "punishment": "", "confidence": "high"}
]}
```

### 9.2 04-011 振举医学（条款体 → 规则 + 结构化）

```json
{"rules": [
  {"slot": 1, "item_id": "04-011", "type": "obligation", "modals": ["合行", "遵照"],
   "condition": "为此振兴医教作养医人", "subject": "州县",
   "action": "刻板榜于医学永久遵照施行；令医人多读医书深究医理",
   "object": "医学", "purpose": "病者赖以回生，医者赖以糊口", "punishment": "", "confidence": "high"}
],
 "structs": [
  {"slot": 1, "item_id": "04-011", "dim": "FRD", "frd_type": "abuse",
   "issue": "庸医误杀", "detail": "有司全不念及，字不通之庸医一年一邑误杀不知几多",
   "countermeasure": "振兴医教、作养医人、令读医书", "target": "", "evidence": "遂使骨肉急大之危病求一字不通之庸医…", "confidence": "high"}
 ]}
```

### 9.3 08-001 乡甲至要（"五不扰"规则体）

```json
{"rules": [
  {"slot": 1, "item_id": "08-001", "type": "prohibit", "modals": ["不许"],
   "condition": "选约长保长", "subject": "约长保长",
   "action": "不许用无身家棍徒，使挟倚外需索", "object": "乡民",
   "purpose": "一不扰", "punishment": "", "confidence": "high"},
  {"slot": 2, "item_id": "08-001", "type": "prohibit", "modals": ["不许"],
   "condition": "乡约保甲实行", "subject": "掌印官",
   "action": "不许委佐贰首领及快壮查点廵逻，掌印官自己抽查", "object": "乡约",
   "purpose": "四不扰", "punishment": "", "confidence": "high"},
  {"slot": 3, "item_id": "08-001", "type": "procedure", "modals": ["方许", "不许"],
   "condition": "乡甲中有事", "subject": "约众",
   "action": "系贼盗人命方许呈报；鬪殴小事等项听民自便，不许呈报",
   "object": "乡甲", "purpose": "五不扰", "punishment": "", "confidence": "high"}
]}
```

### 9.4 14-002 人命（十二款）（程序/时限体）

```json
{"rules": [
  {"slot": 1, "item_id": "14-002", "type": "procedure", "modals": ["即", "限以"],
   "condition": "被殴", "subject": "尸亲",
   "action": "即自解衣眼同见证，照状式告辜投递到官；官亲相验登记伤痕，限以保辜日期责令凶犯寻医调理案候在官；身死之日即照状式告检",
   "object": "官/凶犯", "purpose": "生死出入之界不可不慎",
   "punishment": "被殴不告辜限者除登时打死及三日之内者姑准检究外，其余死后告人命者俱以假伤骗诈及自殴诬人论，不准真正人命",
   "confidence": "high"},
  {"slot": 2, "item_id": "14-002", "type": "deadline", "modals": ["不许过", "不许过"],
   "condition": "人命招情批详到日", "subject": "承委官",
   "action": "实时解任赴检当场审定即日具招申；赴检不许过两时，具招不许过当日",
   "object": "人命案件", "purpose": "至严",
   "punishment": "委官批到三日不赴检、检后五日不具招者，官以才力不及注考", "confidence": "high"}
],
 "structs": [
  {"slot": 1, "item_id": "14-002", "dim": "LGR", "lgr_type": "template_form",
   "item": "人命告辜式/人命告检式", "purpose": "告辜登记伤痕、告检依法检验",
   "template_fields": [], "usage_note": "", "target": "", "evidence": "即照状式告辜…即照状式告检", "confidence": "high"},
  {"slot": 2, "item_id": "14-002", "dim": "TME", "tme_type": "deadline",
   "name": "保辜限期", "detail": "登时及三日之内姑准检究；辜限隔月查大建小建",
   "target": "", "evidence": "…此生死出入之界不可不慎也", "confidence": "high"}
 ]}
```

### 9.5 14-011 告盗情状式（状式模板 → 无规则，归 LGR）

```json
{"structs": [
  {"slot": 1, "item_id": "14-011", "dim": "LGR", "lgr_type": "template_form",
   "item": "告盗情状式", "purpose": "告盗情立案",
   "template_fields": ["原告籍贯名姓", "事由", "月日更时分", "强窃盗人数", "凶器",
                       "所劫财物若干件（花样记号）", "银钱若干数", "保甲人救护情况", "请求"],
   "usage_note": "不许多开一物，不许多报一盗，违者重究仍不准理",
   "target": "", "evidence": "某州某县人某人为盗情事某月日更时分不知名强窃盗约有几名各持凶器…伏乞案候严拏上告",
   "confidence": "high"}
]}
```

---

## 10. 坑注（本书特有的切分/抽取注意）

- **卷首篇目与正文标题重复**：部分卷 `（卷首篇目）` 列表与正文 `○/△` 标题同名（如"告盗情状式"在篇目与正文各出现一次）。**切分以正文 ○/△ 行为准**，篇目列表不重复计数、不参与抽取（本坑已记工厂 `pending-review.md` 待评审）。
- 乡甲约卷之三/四/五/六为格叶体（"一…事"开头 + 计开条件），整卷一条卷级条目，计开条件不单独编号；规则/结构化在条目内逐句/逐款产出。
- 明职序/引、风宪约重刊序为卷级条目，内容为说理/记事，规则抽取极低；实体与结构化照常。

## 11. 白话文对照引用（非层，交付辅助）

- 文件：`assets/sources/吕公实政录_白话文_全卷合并.txt`（15 卷 ◆ 标题 + 111 个 ○/△ 标题与原文一一对应）。
- 产出：`_baihua_map.json`（item_id → 白话文段落）。**禁止**把白话文当原文抽取；仅交付/查询时引用。

---

## 12. 执行期枚举校准（V3，C5）

- 实体类型/规则类型继承基准库，本书不新增（如需新增走 pending-review 评审）；
- ACT/FRD/LGR/TME 类型为本书归纳（封闭 + 兜底），执行期未匹配值 → `_validate/_pending_enums.csv` 收集 → 收尾决议 → registerVersion+1 回写本文件 §4。
