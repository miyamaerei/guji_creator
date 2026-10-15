# 《治谱》实例 Schema 与枚举快照（06-zhipu-knowledge）

## 1. 契约登记

| 契约 | 状态 |
|---|---|
| C1 书 ID | zp（治谱，明·佘自强） |
| C2 层清单 | ent/rule/struct/reg/opn/trl + 跨层索引（无 L3/L5/DOC/REL/CIT） |
| C3 ID 段位 | 层前缀 × 卷×500 + seq（RULE-0501 起 = 卷01×500+1）；ent 主键全局归一（ENT-0001 起跨卷去重，同 ppy 先例）；item_id = NN-NNN（01-001~11-056） |
| C4 枚举组 | ENTITY/RULE/REG/OPN/ACT/FRD/LGR/TME/TRL |
| C5 枚举硬校验 | 打包器校验 type/dim/stance 命中枚举，未注册 → ERR |
| C6 指纹库 | `_item_registry.json`（original 注入源，AI 源数据不手抄） |
| C7 校验闸门 | `validate_layers.py` 退出码 0 = ERR 0 / GAP 0 |

## 2. 层 schema（6 层）

### 2.1 ent
```
ent_id / item_id / text / type / start / end / normalized / confidence / source
ID: ENT-（全局主键表顺序）；type ∈ ENTITY_TYPES
```

### 2.2 rule
```
rule_id / item_id / type / modals[] / condition / subject(含 subject_ent_ids[]) /
action / object / purpose / punishment / original / confidence
ID: RULE-；type ∈ RULE_TYPES 7；modals ∈ RULE_MODALS 7
```

### 2.3 struct（四维）
```
struct_id / item_id / dim(ACT|FRD|LGR|TME) / act_type|frd_type|lgr_type|tme_type /
target(含 ent_ids[]) / content / original / confidence
ID: ACT-/FRD-/LGR-/TME-
```

### 2.4 reg
```
reg_id / item_id / name / type / content / evolution / target / original / confidence
ID: REG-；type ∈ REG_TYPES 10（政书英文键）
```

### 2.5 opn
```
opn_id / item_id / topic / stance / argument / evidence_refs[] / original / confidence
ID: OPN-；stance ∈ OPN_STANCES 5
```

### 2.6 trl
```
trl_id / item_id / style / translation / original / confidence
ID: TRL-NN-NNN（与 item_id 对应）；style ∈ TRL_STYLES
translation 整段白话，不切条；original 由指纹库注入
```

## 3. 枚举快照（见 `_kg_enums.py` V1.0）

- ENTITY_TYPES 20 值（本书启用 13 子集）
- RULE_TYPES 7 中文键 + RULE_MODALS 7
- REG_TYPES 10 政书英文键
- OPN_STANCES 5
- ACT_TYPES / FRD_TYPES / LGR_TYPES / TME_TYPES
- TRL_STYLES 3

## 4. 探针示例（待跑通后回填）

挑 4 条跨门探针：
- `04-001` 准状不妨多（词讼门）
- `05-?` 钱粮门一条（放籴/平粜）
- `09-?` 待人门一条（待佐贰五段）
- `11-?` 补遗一条（初仕录或祥刑要览）

跑通后回填本表：每层 ID、关键字段样例、ERR/GAP 数。

## 5. 坑注

1. 官箴体"一、二、三"条款：一条目内并列多条规则时拆多条共享 item_id。
2. 说理/按语句不抽规则（归 OPN）；亲历记事不抽规则。
3. REG 用政书英文键，勿混中文值。
4. TRL 直接用现成白话文对位，不另译。
5. 封闭枚举不就地吸收新值，走 V3 收集-报告-暂存。
6. 校勘记里的〔原文残〕〔按〕标注保留在 original，不臆补。
