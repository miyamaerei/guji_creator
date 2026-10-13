# 《平平言》实例 Schema 与枚举快照（12-pingpingyan-knowledge）

## 1. 契约登记（book-mcp C1–C7）与卷号表

| 契约 | 状态 |
|---|---|
| C1 书 ID | ppy（平平言，清·方大湜） |
| C2 层清单 | ent/rule/struct/reg/opn + 跨层索引（无 L3/L5/DOC/REL/CIT） |
| C3 ID 段位 | 层前缀 × 卷×500 + seq（ENT-0501 起 = 卷01×500+1）；item_id = 卷-序（01-001..04-070） |
| C4 枚举组 | ENUM_GROUPS：ENTITY/RULE/EVENT/REG/OPN/ACT/FRD/LGR/TME |
| C5 枚举硬校验 | 打包器校验 type/dim/stance 等字段命中枚举，未注册 → ERR 静默丢条 |
| C6 指纹库 | `_item_registry.json`（original 注入源，AI 源数据不手抄） |
| C7 校验闸门 | `validate_layers.py --skip-baseline` 退出码 0 = ERR 0 / GAP 0 |

**卷号表**（卷号按原书顺序直接映射；序/凡例/跋 = 00 版本说明卷，不进入条目库）：

| 卷号 | 卷名 | 条目数 | 内容形态 |
|---|---|---|---|
| 01 | 卷一 | 84 | 立志修身·候补·到任·官箴总论（规范句 + 论说 + 则例摘录：公罪私罪/大计） |
| 02 | 卷二 | 87 | 衙门管理·幕友门丁书差·事上同寅（规范句 + 门丁十弊长文 + 亲历记事） |
| 03 | 卷三 | 43 | 刑名听讼（听讼原则 + 审案程序 + 律例引用） |
| 04 | 卷四 | 70 | 教化风化·钱粮·仓储荒政·旌表·交代（则例/会典事例条文密集） |
| 00 | 序/凡例/跋 | — | 版本说明卷，不入条目库 |

## 2. 层 schema（5 层）

### 2.1 L1 实体层 ent
```
ent_id / item_id / text / type / start / end / normalized / confidence / source
ID: ENT-；type ∈ ENTITY_TYPES（20 值见 §3.1，本书启用子集 13 值）
```

### 2.2 L2 规则层 rule
```
rule_id / item_id / type / modals[] / condition / subject(含 subject_ent_ids[]) /
action / object / purpose / punishment / original / confidence
ID: RULE-；type ∈ RULE_TYPES 7（中文键）；modals ∈ RULE_MODALS 7
判定：AI 逐条；组合规则主模态 + modals 数组；说理/亲历记事句不抽（归 OPN/FRD）
```

### 2.3 L4 结构化四维 struct
```
struct_id / item_id / dim(ACT|FRD|LGR|TME) / act_type|frd_type|lgr_type|tme_type /
target(含 ent_ids[]) / content / original / confidence
ID: ACT- / FRD- / LGR- / TME-（按 dim 前缀分配）
维度类型字段必填且命中枚举（缺字段/错值 → ERR 静默丢条）
```

### 2.4 REG 制度层 reg
```
reg_id / item_id / name / type / content / evolution / target / original / confidence
ID: REG-；type ∈ REG_TYPES 政书英文键 10 值（§3.5）
content 写要点不抄原文；沿革记 evolution
```

### 2.5 OPN 论说层 opn
```
opn_id / item_id / topic / stance / argument / evidence_refs[] / original / confidence
ID: OPN-；stance ∈ OPN_STANCES 5
argument 只写要点概要不抄原文；evidence_refs 引支撑论说的引书/人物实体
```

## 3. 枚举快照（_kg_enums.py V1.0，建于 pingpingyan-kb 根）

```python
# -*- coding: utf-8 -*-
"""《平平言》枚举单点（V1.0）——5 层方案（ent/rule/struct/reg/opn + 跨层索引）。
继承基准库快照 + lgs/xzl 归纳快照。执行期未匹配值走 V3 收集。"""

# ============ ENTITY_TYPES 实体类型（继承基准库 §1.1 20 值） ============
ENTITY_TYPES = [
    "person", "official", "institution", "place", "era", "work", "object",
    "animal", "plant", "food", "doc", "system", "behavior", "punishment",
    "time", "quantity", "posthumous", "star", "event", "unknown",
]

# ============ RULE_TYPES 规则类型（继承基准库 §1.2 7 值，中文键） ============
RULE_TYPES = ["禁止型", "义务型", "允许型", "程序型", "时限型", "处罚型", "优先级型"]
RULE_MODALS = ["必须", "禁止", "应该", "可以", "不必", "不得", "宜"]

# ============ EVENT_TYPES 事件类型（继承基准库 §1.3 27 顶层，备用） ============
EVENT_TYPES = [
    "朝政", "政变", "军事", "军政", "边事", "人事任免", "弹劾", "礼仪", "科举",
    "文事", "建言", "灾异", "轶事", "祭祀", "经济", "司法", "神异传说", "疾疫",
    "御灾赈济", "缉捕防盗", "巡查监察", "家事", "异闻", "宗教", "制度", "沿革", "其他",
]

# ============ REG_TYPES 制度类型（政书英文键分支 v6，10 值） ============
REG_TYPES = [
    "official_system", "selection_assessment", "fiscal", "justice_prison",
    "baojia_xiangyue", "education_sacrifice", "military", "post_transport",
    "governance", "other",
]

# ============ OPN_STANCES 作者论说立场（继承基准库 §1.8 5 值） ============
OPN_STANCES = ["肯定", "否定", "怀疑", "讽刺", "中立"]

# ============ STRUCT 结构化四维（继承 lgs/xzl 归纳快照，本书不新增值） ============
STRUCT_DIMS = ["ACT", "FRD", "LGR", "TME"]
ACT_TYPES = ["official", "justice_role", "clerk_role", "xiangyue_role", "other"]
FRD_TYPES = ["abuse", "guard", "evil_custom", "other"]
LGR_TYPES = ["ledger", "geye", "template_form", "board", "voucher", "other"]
TME_TYPES = ["deadline", "meeting", "assessment", "season", "age_limit", "other"]

# ============ 枚举组登记表（打包器/校验器用） ============
ENUM_GROUPS = {
    "ENTITY": ENTITY_TYPES,
    "RULE": RULE_TYPES,
    "EVENT": EVENT_TYPES,
    "REG": REG_TYPES,
    "OPN": OPN_STANCES,
    "ACT": ACT_TYPES,
    "FRD": FRD_TYPES,
    "LGR": LGR_TYPES,
    "TME": TME_TYPES,
}

# 兼容别名（历史文件用旧键）
RULE_TYPES_ALIAS = RULE_TYPES
OPN_TYPES = OPN_STANCES

VERSION = "1.0"
```

### 3.1 ENTITY_TYPES（继承基准库 §1.1 20 值）
person 人物 / official 职官(office) / institution 机构(org) / place 地名 / era 年号朝代 / work 文献书名(book) / object 名物(artifact) / animal 动物 / plant 植物 / food 饮食 / doc 文书 / system 制度 / behavior 行为 / punishment 刑罚 / time 时间 / quantity 数量 / posthumous 谥号 / star 星象 / event 事件名 / unknown 类型待定
> 本书启用子集：person/official/institution/place/era/work/doc/system/behavior/punishment/time/quantity/unknown（object/animal/plant/food/star/event/posthumous 无成体系证据不启用，保留封闭全集）。

### 3.2 RULE_TYPES（7，中文键）+ RULE_MODALS（7）
禁止型 / 义务型 / 允许型 / 程序型 / 时限型 / 处罚型 / 优先级型
必须 / 禁止 / 应该 / 可以 / 不必 / 不得 / 宜

### 3.3 EVENT_TYPES（继承基准库 §1.3 27 顶层，备用）
朝政/政变/军事/军政/边事/人事任免/弹劾/礼仪/科举/文事/建言/灾异/轶事/祭祀/经济/司法/神异传说/疾疫/御灾赈济/缉捕防盗/巡查监察/家事/异闻/宗教/制度/沿革/其他

### 3.4 ACT_TYPES（继承 lgs/xzl 快照 5 值）
official / justice_role / clerk_role / xiangyue_role / other

### 3.5 FRD_TYPES（继承快照 4 值）
abuse / guard / evil_custom / other

### 3.6 LGR_TYPES（继承快照 6 值）
ledger / geye / template_form / board / voucher / other

### 3.7 TME_TYPES（继承快照 6 值）
deadline / meeting / assessment / season / age_limit / other

### 3.8 REG_TYPES（政书英文键分支 v6，10 值）
official_system 官制 / selection_assessment 铨选考课 / fiscal 财政赋役 / justice_prison 司法狱政 / baojia_xiangyue 保甲乡约 / education_sacrifice 文教祭祀 / military 军政 / post_transport 驿传运输 / governance 治理总纲 / other

### 3.9 OPN_STANCES（5）
肯定 / 否定 / 怀疑 / 讽刺 / 中立

> 执行期未匹配值走 V3 收集（pending-review 提案，不就地自造）。

## 4. 示例条目（试点 2026-10-13 固化）

试点 5 条真实条目（01-001 造福莫如州县 / 01-002 造孽莫如州县 / 01-025 各房呈须知册 / 01-026 清查前任命盗各案 / 01-032 公罪私罪）按 5 层 schema 试跑，字段/枚举/ID 无硬伤（ERR=0 GAP=0）：

| 层 | 示例（ID） | 关键字段样例 |
|---|---|---|
| ent | ENT-0501 州县（01-001 official）；ENT-0503 章枫山（01-001 person）；ENT-0505 须知册（01-025 doc）；ENT-0509 公罪 / ENT-0510 私罪（01-032 system） | type ∈ ENTITY_TYPES；alias_index 归一（"章枫山先生"→章枫山，composite 词形手工映射）；find_span 命中 |
| rule | RULE-0501（01-002 禁止型） | "汝曹如有命作州县万不可造孽"；type=禁止型；modals=[禁止]；subject=作州县者；punishment 可空 |
| rule | RULE-0502（01-025 程序型） | "新官到任须将各房须知册发还细查，许添载更正，不准再漏再错"；type=程序型；modals=[应该,可以,不得] |
| rule | RULE-0503（01-026 程序型） | "到任之初须令刑房清查前任内命盗各案并开摺送阅，分情形赶紧处置"；type=程序型；modals=[必须,应该] |
| rule | RULE-0504（01-032 禁止型） | "私罪必不可有"；type=禁止型；modals=[禁止]；punishment 并入"虽有权纪不准抵销" |
| struct | ACT-0501（01-001 official 州县近民之责）；FRD-0501（01-002 abuse 积弊：贪酷罢软/胥役勾通）；LGR-0501（01-025 ledger 须知册）；TME-0501（01-026 deadline 审限参限） | dim 必填；维度字段 act_type/frd_type/lgr_type/tme_type 命中枚举；ID 按 dim 前缀分配 |
| reg | REG-0501（01-026 justice_prison 命盗清查审限参限制度）；REG-0502（01-032 official_system 公罪私罪抵销则例） | type 用政书英文键；content 写要点不抄原文；evolution 记旧例沿革 |
| opn | OPN-0501（01-001 肯定）；OPN-0502（01-002 否定） | topic/stance/argument（argument 只写要点不抄原文）；evidence_refs 可引 work/person 实体 |
| 说理条不抽规则 | 01-001 为纯说理条 → 只建 ent/opn，无 rule | 验证"说理/亲历记事句不抽规则"口径可执行 |

ID 段位验证：ENT-0501/RULE-0501/ACT-0501/REG-0501/OPN-0501 均为卷 01×500+1——段位分配正确，无跨卷撞号。

> **执行期实现注（2026-10-13 试点实际跑通）**：rule/struct/reg/opn 四层按段位分配（RULE-0501、ACT-0501、FRD-0501、LGR-0501、TME-0501、REG-0501、OPN-0501）✓；**ent 层主键 ID 用全局归一顺序（ENT-0001 起，跨卷去重复用）**，与 lgs/xzl/fqh 家族先例一致——示例中"ENT-0501"仅为契约段位设想，实际实现以主键表顺序为准（`_global/ent_keys.json` 唯一真源），跨层引用（struct target、opn evidence_refs）按实际 ent_id 引用。
> 试点源数据：`_src/_ents_ai_01.py` / `_rules_ai_01.py` / `_struct_ai_01.py` / `_regs_ai_01.py` / `_opns_ai_01.py`；打包结果 31 条层记录，validate ERR=0/GAP=0；kg_join 卷 01 全回填（84 条，试点 5 条 layer_count 3~4，其余 79 条如实 0 层）。

## 5. 坑注（本书特有 + 跨书通用）

1. ○ 兼条目标记与条内注——底座以卷首标题清单与正文 ○ 交叉核对（正文 ○ 数 = 标题清单行数，差值=条内注/缺漏）。
2. 卷首标题清单行不进入条目正文，仅作切分参考与逐条对照。
3. 原文夹注括注 `【 懋】` 型：norm 归一须定死一种括注形式（执行期定并记录），避免指纹漂移。
4. struct 维度类型字段必填且命中枚举（缺/错 → ERR 静默丢条）。
5. 说理/亲历记事句不抽规则——归 OPN/FRD 承载，防止规则层被议论句污染。
6. REG 用政书英文键（official_system/fiscal/justice_prison…），勿混笔记体中文值（官制/财政/司法…）。
7. 工程根 `原文/平平言_原文_全卷合并.txt` 为 GBK，实例内一律读 `assets/sources/` UTF-8 文件。
8. 封闭枚举不就地吸收新值（走 V3 决议 + enum-changelog 双写）。
