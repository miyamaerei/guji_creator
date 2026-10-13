---
name: fuhuiquanshu-knowledge
description: 《福惠全书》（清·黄六鸿，康熙州县施政全流程手册，32 卷 14 部）书实例 skill——按"政书规则型 + 全流程 + 文书系统 + 角色网络"八层知识工程执行：L1 实体 / L2 规则 / L4 结构化四维（ACT·FRD·LGR·TME）/ REG 制度（政书英文键）/ OPN 论说 / L3 流程 / DOC 文书 / REL 角色关系 + 跨层索引。用户传《福惠全书》或说"处理福惠全书/福惠/黄六鸿"时使用。
---

# 福惠全书 知识工程实例（11-fuhuiquanshu-knowledge）

## 0. 定位与口径

- 书：清·黄六鸿《福惠全书》，康熙甲戌（1694）自序，32 卷 14 部 + 凡例 + 自序 + 禀启附，原文全卷合并 306,193 字；白话文 32 卷已配齐（`../白话文/`），**仅对照引用、不建翻译层**（用户口径延续 lgs/xzl/ysz）。
- 形态：**政书则例体 + 全流程手册**——"自筮仕以迄升迁为部十有四，自谒选以迄辞上官为条二百一十有九，钱谷刑名又分晣为条一百一十有九，每部首缀以总论"（自序）。
- 符号体例（凡例）：正文 `○标题` 起条（兼条内注）、`△款目` 为文书式、卷首另有标题列表——**与 lgs/xzl 的 ○ 同行标题不同，底座切分须专用逻辑**（见 §2）。
- 交付形态：JSON + 跨层 CSV（`_kg_join_flat.csv` utf-8-sig）+ 交付说明；白话文仅对照。

## 1. 引导式反思记录（用户方向原话 + 决策）

| 轮 | 用户原话 / 决策 | 结论 |
|---|---|---|
| 探查 | "帮忙看一下这个新书……然后做一个开工计划" | Phase ① 结构性探查完成：14 部 32 卷、自序 338+ 条、○/△ 体例 |
| 启发 | "搜一下网络，对于这本书，还有哪些结构可以提取的……因为这书的内容还是挺丰富的" | 网络研究（郭润涛状式研究/杨志玖释六赃/云南高校公文程式）→ 补充 L3 流程 / DOC 文书 / REL 角色 / QUANT 候选 |
| 锁层 | "ok，8层，文书式按文书条目建模" | **8 层主方案**：ent + rule + struct 四维 + REG + OPN + L3 流程 + DOC 文书 + REL 关系；△ 文书式按 DOC 文书条目建模（不独立成底座条） |
| 粒度 | "默认条" | 粒度=条（正文 ○ 标题条，约 355~370 条） |
| REG | "政书" | REG 用**政书英文键分支**（enum-library §1.12 v6：official_system/selection_assessment/fiscal/justice_prison/baojia_xiangyue/education_sacrifice/military/post_transport/governance/other） |
| 交付 | "延续 JSON+CSV、白话文仅对照不建翻译层" | 已锁定 |
| 未定 | QUANT 数据层 / EVT 事件 / CUS 风俗 | 试点后按密度定（不在 8 层内） |

## 2. 底座方案（L0）

- **条目 = 正文 `○标题` 起条**（每卷正文以 ○ 引导条目，标题 2~10 字）；**△款目（文书式）不独立成条**——由 DOC 层按文书条目建模，doc.related_item 关联所属底座条。
- 卷首标题列表（◆ 部 + 无符号标题行）作**交叉校验**（正文 ○ 数 ≥ 列表数，差值为条内注误标，以列表为准）。
- 总论/余论/说 14 篇**独立成条**；禀启附按篇成条；自序/凡例不入底座。
- 产出 `_item_registry.json`（item_id `NN-NNN` 卷-序 + original 指纹 + norm）；所有层 original 注入自指纹库，AI 源数据不手抄原文。
- 计数参照：自序 219 + 119 = 338 主体 + 14 论说 + 禀启附 ≈ 355~370 条。**动工先查 `_item_registry.json` 实际条数，不按标题数直推**（坑：宛署卷14 底座 5 条≠标题 1）。

## 3. 启用层方案（8 层 + 跨层索引）

### L1 实体层（ent）
- schema：ent_id / item_id / text / type / start / end / normalized / confidence / source。
- 枚举：ENTITY_TYPES 继承基准库 20 值（person/official/institution/place/doc/system/behavior 等）。
- 主键：`_global\ent_keys.json` + `alias_index.json`；build_ent_keys 先查后建。

### L2 规则层（rule）
- schema：rule_id / item_id / type / modals / condition / subject(含 subject_ent_ids) / action / object / purpose / punishment / original / confidence。
- 枚举：RULE_TYPES 7（禁止/义务/允许/程序/时限/处罚/优先级）+ RULE_MODALS 7；处罚词密集（杖/徒/流/斩/绞/罪）。
- 判定：AI 逐条；组合规则拆/并按实例口径（一条多模态 → 主模态 + modals 数组）。

### L4 结构化四维（struct）
- 继承 lgs/xzl 归纳快照（ACT_TYPES 5 / FRD_TYPES 4 / LGR_TYPES 6 / TME_TYPES 6），**本书不新增值**。
- schema：struct_id / item_id / dim（ACT|FRD|LGR|TME）/ act_type|frd_type|lgr_type|tme_type（按 dim 必填且命中枚举）/ target / content / original。
- 主战场：FRD（凡例"首严剔弊"：弊204/隐漏/需索/侵/贿）、LGR（册340/簿261/状269/式296）、ACT（责之责成/吏役470/保长153）、TME（限320/定限）。

### REG 制度层（reg）
- schema：reg_id / item_id / name / type / content / evolution / target / original。
- 枚举：**政书英文键分支 v6**（official_system/selection_assessment/fiscal/justice_prison/baojia_xiangyue/education_sacrifice/military/post_transport/governance/other）。
- 主战场：钱谷（卷6-8）/编审（9）/清丈（10）/刑名（11-20）/保甲（21-23）/邮政（28-29）。

### OPN 论说层（opn）
- schema：opn_id / item_id / topic / stance / argument / evidence_refs / original。
- 枚举：OPN_STANCES 5（肯定/否定/怀疑/讽刺/中立）。
- 主战场：总论 4 / 余论 5 / 说 5 + 条末按语（如卷十清丈余论）。

### L3 流程层（proc）
- schema：process_id / item_id / name / steps（step_id/seq/text/agent 含 agent_ent_ids/next）/ state_machine / events / original。
- 显式时序才建 state_machine；散点素材判"点不是线"不强行建模（坑：lgs 事件纪年 5 点不建）。
- 主战场：刑名（放告→准状→投词→审断→详报→发落）、钱谷（征比→解送→存留）、清丈（立册→自首→抽丈）、保甲（编组→稽查→保结）、升迁（交代→交盘→受代）。

### DOC 文书层（doc）★本书自定义
- schema：doc_id / item_id / name / category / format（格式要点，如状式"格眼三行一百四十字"）/ purpose / flow（文书流向）/ related_item（所属底座条）/ original。
- 枚举：DOC_TYPES 本书归纳 8 类——状词 / 票单 / 册簿 / 牌批 / 谕告 / 结状 / 启禀 / 其他（封闭+兜底）。
- △ 款目（202 个文书式）**按文书条目建模**：每个 △ 文书式 = 1 条 doc 记录，related_item 指向所属底座条；正文内叙述文书格式者（状式格眼等）也建 doc。
- 与 LGR 分工：LGR 收"文书簿册的防弊/治理切片"（template_form 等），DOC 收"文书本身（种类/格式/用途/流向）"。

### REL 角色关系层（rel）★本书定制（角色网络版）
- schema：rel_id / item_id / person_a(含 ent_ids) / person_b(含 ent_ids) / relation_type / direction / evidence / original。
- 枚举：REL_TYPES 本书归纳（继承 C3 12 值 + 本书角色类）——同僚/上下级/师生/姻亲/同乡/同科/举荐/弹劾/恩怨/敌对/父子亲属/**保甲隶属/吏役职责/诉讼三方/幕宾聘用**/其他（封闭+兜底，执行期按 V3 决议）。
- 三张角色网：诉讼角色（原告/被告/干证/代书/两邻）、保甲组织（保正-甲长-牌头-乡约-里长）、吏役系统（皂隶/仵作/禁卒/更夫/经承/幕友刑名钱谷）。
- 纪律：只建文本有直接证据的关系，推测不建（宁缺毋滥）。

### 跨层索引
- `_kg_join.json`（item_id / volume / source / ents / rules / structs / regs / opns / procs / docs / rels / layer_count）+ `_kg_join_flat.csv`。
- ID 对齐审计：实体主键唯一 / 引用槽位合法 / item_id 全回填 / target 用 ID / 枚举口径一致。

## 4. 枚举单点（_kg_enums.py）

- 工程根 `_kg_enums.py`（V1.0 + 兼容别名）：ENTITY 20 / RULE 7+7 / EVENT 27（备用）/ REG 政书英文键 10 / OPN 5 / ACT 5 / FRD 4 / LGR 6 / TME 6 / DOC 8（本书归纳）/ REL 本书归纳（C3 12 + 角色类）。
- 执行期未匹配值走 V3 收集（pending-review 提案，不就地自造，pitfalls #27）。

## 5. 管线（工程根）

```
build_base.py（底座切分）→ _item_registry.json
build_ent_keys.py（实体先查后建 + alias_index + find_span）
build_rules.py / build_structs.py / build_regs.py / build_opns.py
build_procs.py / build_docs.py / build_rels.py（8 打包器，枚举硬校验 + original 注入）
build_kg_join.py（跨层索引 + _kg_join_flat.csv utf-8-sig）
validate_layers.py --skip-baseline（NOT_EMPTY + PRESENT_OK + 枚举 + 悬空引用回填，退出码 0/1）
run_all.py '--volumes=NN' / --all
```

- 层源数据文件名单数：`_src\_ents_/_rules_/_structs_/_regs_/_opns_/_procs_/_docs_/_rels_ai_NN.py`。
- 多段源数据**一次 Write 写全**（坑：lgs 卷14/15 覆盖事故）；打包后必查 `_build\<layer>_errors.txt`（ERR 静默丢条）。

## 6. 验证与交付清单

- 每卷打包后：`python run_all.py '--volumes=NN'; python build_kg_join.py; python validate_layers.py --skip-baseline` → ERR=0/GAP=0 + 逐层条数对账。
- 全量收尾：`_deliver\` 全量交付说明 / 使用报告 / 项目总结 + `_kg_join_flat.csv`；白话文对照不建翻译层。
- 移交：kb-mcp 登记 `fuhuiquanshu-kb`；联邦库 FqhAdapter（book_id=fqh）+ fed_search 跨书查重 + conflict 裁决。
- 工厂学习回路：case-feedback-fuhuiquanshu.md + pending-review 提案（8 层政书组合 / DOC 层 / REL 角色版 / QUANT 候选）+ registry 10 行。

## 资源索引

- 源文件：`assets/sources/福惠全书_原文_全卷合并.txt`（+工程根 `原文\` 32 卷拆分作交叉校验 / `白话文\` 对照引用）。
- schema 明细/枚举快照/示例条目：`references/schemas.md`。
- 工厂（深化阅读，非执行依赖）：`E:\git\ToolBox\guji\Skills\00-book-knowledge-factory\`（methodology/pitfalls/enum-library/layer-library）。
