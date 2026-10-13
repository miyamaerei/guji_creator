# 《福惠全书》实例 Schema 与枚举快照（11-fuhuiquanshu-knowledge）

## 1. 契约登记（book-mcp C1–C7）

| 契约 | 状态 |
|---|---|
| C1 书 ID | fqh（福惠全书） |
| C2 层清单 | ent/rule/struct/reg/opn/proc/doc/rel + 跨层索引 |
| C3 ID 段位 | 层前缀 × 卷×500 + seq（ENT-0001 起）；item_id = 卷-序（01-001..） |
| C4 枚举组 | ENUM_GROUPS：ENTITY/RULE/EVENT/REG/OPN/ACT/FRD/LGR/TME/DOC/REL |
| C5 枚举硬校验 | 打包器校验 type/dim 等字段命中枚举，未注册 → ERR 静默丢条 |
| C6 指纹库 | `_item_registry.json`（original 注入源，AI 源数据不手抄） |
| C7 校验闸门 | `validate_layers.py --skip-baseline` 退出码 0 = ERR 0 / GAP 0 |

## 2. 层 schema（8 层）

### 2.1 L1 实体层 ent
```
ent_id / item_id / text / type / start / end / normalized / confidence / source
ID: ENT-；type 枚举 ENTITY_TYPES（20 值见 §3.1）
```

### 2.2 L2 规则层 rule
```
rule_id / item_id / type / modals[] / condition / subject(含 subject_ent_ids[]) /
action / object / purpose / punishment / original / confidence
ID: RULE-；type ∈ RULE_TYPES 7；modals ∈ RULE_MODALS 7
判定：AI 逐条；组合规则主模态 + modals 数组
```

### 2.3 L4 结构化四维 struct
```
struct_id / item_id / dim(ACT|FRD|LGR|TME) / act_type|frd_type|lgr_type|tme_type /
target(含 ent_ids[]) / content / original / confidence
ID: ACT- / FRD- / LGR- / TME-（按 dim 前缀分配）
维度类型字段必填且命中枚举（缺字段/错值 → ERR 静默丢条，坑 lgs struct）
```

### 2.4 REG 制度层 reg
```
reg_id / item_id / name / type / content / evolution / target / original / confidence
ID: REG-；type ∈ REG_TYPES 政书英文键 10 值（§3.5）
```

### 2.5 OPN 论说层 opn
```
opn_id / item_id / topic / stance / argument / evidence_refs[] / original / confidence
ID: OPN-；stance ∈ OPN_STANCES 5
```

### 2.6 L3 流程层 proc
```
process_id / item_id / name / steps[{step_id, seq, text, agent(含 agent_ent_ids[]), next}] /
state_machine / events[] / original / confidence
ID: PROC-；显式时序才建 state_machine；散点判"点不是线"
```

### 2.7 DOC 文书层 doc（本书自定义）
```
doc_id / item_id / name / category / format / purpose / flow / related_item / original / confidence
ID: DOC-；category ∈ DOC_TYPES 8（§3.9）；related_item=所属底座条 item_id
△ 款目文书式 = 1 doc 条（related_item 指向所属条）；正文述文书格式者亦建 doc
```

### 2.8 REL 角色关系层 rel（本书定制·角色网络版）
```
rel_id / item_id / person_a(含 ent_ids[]) / person_b(含 ent_ids[]) /
relation_type / direction / evidence / original / confidence
ID: REL-；relation_type ∈ REL_TYPES（§3.10）；direction=单向|双向|未明
只建文本有直接证据的关系（宁缺毋滥）
```

## 3. 枚举快照（_kg_enums.py V1.0）

### 3.1 ENTITY_TYPES（继承基准库 §1.1 20 值）
person 人物 / official 职官(office) / institution 机构(org) / place 地名 / era 年号朝代 / work 文献书名(book) / object 名物(artifact) / animal 动物 / plant 植物 / food 饮食 / doc 文书 / system 制度 / behavior 行为 / punishment 刑罚 / time 时间 / quantity 数量 / posthumous 谥号 / star 星象 / event 事件名 / unknown 类型待定

### 3.2 RULE_TYPES（7）+ RULE_MODALS（7）
禁止型(prohibit) / 义务型(obligation) / 允许型(allow) / 程序型(procedure) / 时限型(deadline) / 处罚型(penalty) / 优先级型(priority)
必须(must) / 禁止(must_not) / 应该(should) / 可以(may) / 不必(need_not) / 不得(may_not) / 宜(prefer)

### 3.3 EVENT_TYPES（继承基准库 §1.3 27 顶层，备用）
朝政/政变/军事/军政/边事/人事任免/弹劾/礼仪/科举/文事/建言/灾异/轶事/祭祀/经济/司法/神异传说/疾疫/御灾赈济/缉捕防盗/巡查监察/家事/异闻/宗教/制度/沿革/其他

### 3.4 ACT_TYPES（继承 lgs/xzl 快照 5 值）
official / xiangyue_role / justice_role / clerk_role / other

### 3.5 FRD_TYPES（继承快照 4 值）
abuse / guard / evil_custom / other

### 3.6 LGR_TYPES（继承快照 6 值）
ledger / geye / template_form / board / voucher / other

### 3.7 TME_TYPES（继承快照 6 值）
deadline / meeting / assessment / season / age_limit / other

### 3.8 REG_TYPES（政书英文键分支 v6，10 值）
official_system 官制 / selection_assessment 铨选考课 / fiscal 财政赋役 / justice_prison 司法狱政 / baojia_xiangyue 保甲乡约 / education_sacrifice 文教祭祀 / military 军政 / post_transport 驿传运输 / governance 治理总纲 / other

### 3.9 DOC_TYPES（本书归纳 8 类，封闭+兜底）
状词（告状/诉状/投词/批词/状式）/ 票单（差票/火票/牌票/由单/截票/串票/谕单）/ 册簿（册/簿/循环簿/号簿/鱼鳞册/黄册）/ 牌批（门牌/里牌/朱批/批语）/ 谕告（告示/示谕/晓谕）/ 结状（结状/供状/保结）/ 启禀（禀帖/启式/四六启）/ 其他

### 3.10 REL_TYPES（C3 12 值 + 本书角色类，封闭+兜底）
同僚 / 师生 / 姻亲 / 同乡 / 同科 / 举荐 / 弹劾 / 恩怨 / 上下级 / 父子亲属 / 敌对 / 保甲隶属 / 吏役职责 / 诉讼三方 / 幕宾聘用 / 其他

### 3.11 OPN_STANCES（5）
肯定 / 否定 / 怀疑 / 讽刺 / 中立

> 执行期未匹配值走 V3 收集（pending-review 提案，不就地自造）。

## 4. 示例条目（试点 2026-10-12 固化）

试点 5 条真实条目（01-001 总论 / 01-002 谒选 / 11-002 词讼 / 16-001 人命下 / 21-002 选保甲长）按 8 层 schema 全通过（ERR=0 GAP=0）：

| 层 | 示例（ID） | 关键字段样例 |
|---|---|---|
| ent | ENT-0001 投牒需铨（01-001 behavior） | type ∈ ENTITY_TYPES；alias_index 归一；find_span 命中 |
| rule | RULE-0501（01-002 禁止型） | "勿轻借京债苛折重息"；modals=不得；punishment 可空 |
| struct | ACT-0501（01-001 official）FRD-0502（01-002 abuse） | dim 必填；维度字段 act_type/frd_type 命中枚举；ID 按 dim 前缀（ACT-/FRD-/LGR-/TME-） |
| reg | REG-0501（01-002 selection_assessment）REG-10501（21-002 baojia_xiangyue） | type 用政书英文键；evolution 记旧例沿革 |
| opn | OPN-0501（01-001 肯定） | topic/stance/argument（argument 只写要点不抄原文） |
| proc | PROC-5501（11-002 词讼 10 步） | steps 数组 step_id/seq/text/agent/next；流程链 考代书→立状式→放告→批阅→挂号→差拘→比差→销差→审讼→用刑 |
| doc | DOC-5501 状式（11-002 状词）DOC-5502 副状式 DOC-5503 人命粘单式 | category 枚举；format 记格眼字数/要件；related_item=所属条；△ 文书式建模验证通过 |
| rel | REL-5501（11-002 诉讼三方）REL-10501（21-002 保甲隶属） | relation_type 枚举；direction 单向/双向；evidence 只记直接证据 |

ID 段位验证：PROC-5501 = 卷11×500+1、REG-10501 = 卷21×500+1、ACT-0501 = 卷01×500+1——段位分配正确，无跨卷撞号。

## 5. 坑注（本书特有 + 跨书通用）

1. ○ 兼条目标记与条内注——底座以卷首标题列表为准，正文 ○ 交叉核对（差值=条内注）。
2. △ 款目不独立成条——DOC 层按文书条目建模（related_item 关联所属条）。
3. 底座条数≠标题数直觉——动工先查 `_item_registry.json`（自序 338+ 仅参照）。
4. struct 维度类型字段必填且命中枚举（缺/错 → ERR 静默丢条）。
5. 多段源数据一次 Write 写全；打包后必查 `_build\<layer>_errors.txt`。
6. REG 用政书英文键（fiscal/justice_prison…），勿混 ysz 中文值（财政/司法…）。
7. 封闭枚举不就地吸收新值（走 V3 决议）。
