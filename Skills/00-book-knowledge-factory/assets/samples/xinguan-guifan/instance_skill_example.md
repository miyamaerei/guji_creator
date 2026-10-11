# 参考样例：《新官轨范》书实例 skill 形态示意

> 本文件展示：如果现在用 book-knowledge-factory 实例化《新官轨范》，Phase ③ 会产出什么形态的实例 skill。
> 内容基于《新官轨范_使用报告.md》的真实产物清单与数字，仅作形态示意（不是完整实例）。
> 用途：作为 AI 执行 Phase ③ 的"示例"——示范实例 skill 的目录结构、SKILL.md 摘要与 references 内容。

---

## 实例 skill 目录结构

```
NN-xinguan-guifan-knowledge/      # 位于本技能库根目录（工厂 00-book-knowledge-factory 同级，编号命名）
├── SKILL.md                       # 执行规范（frontmatter + 底座→5层→整合→交付）
├── references/
│   ├── schemas.md                 # 启用层 schema：11 类实体枚举、规则触发词/槽位、
│   │                              #   流程/状态机、五维（LGR/TME/DOC/ACT/FRD）、
│   │                              #   事件类型 43 值 + 示例条目
│   └── enums.md                   # 封闭枚举单点：实体类型/规则类型/模态/事件类型/维度类型
└── assets/templates/
    ├── usage_report_template.md   # 使用报告母版（交付阶段用）
    └── project_summary_template.md # 项目总结报告母版（交付阶段用）
```

## SKILL.md 关键内容摘要

```markdown
---
name: xinguan-guifan-knowledge
description: 《新官轨范》（明代官箴书）知识工程实例 skill——按已确认方案执行：
  底座（12 章/275 条指纹库）→ 实体层（11 类）→ 规则层（273）→ 流程层（274/744+状态机）
  → 结构化层（五维 677）→ 事件层（229 五元组）→ 跨层索引（275 条目一行全看）→
  使用报告 + 项目总结报告。当用户需要处理/研读/查询《新官轨范》、补充数据时使用。
  由 book-knowledge-factory 实例化，方案已确认，直接执行无需重新设计。
---

# 《新官轨范》知识工程规范

## 0. 口径（已确认）
粒度=条（275 条）；判定=AI 逐条 + 代码验缺漏；交付=JSON + 汇总 + 跨层 CSV；
启用层=全部 5 层 + 索引；词典=全文本内生。

## 0.1 引导式反思记录（来源：工厂 Phase ②）
〔见 samples/xinguan-guifan/reflection_example.md：用户方向 5 条、各层证据、确认结论〕

## 1. 执行流程：底座 → L1实体 → L2规则 → L3流程 → L4结构化 → L5事件 → 跨层整合 → 交付

## 2. 底座
12 个 XHTML（00 版本说明 + 01 卷上 + 02 卷首注语 + 03~11 卷下）；
_extract\NN_卷名.txt（条N|正文）；_item_registry.json 275 条（key=NN-NNN，original/norm）。

## 3. 实体层
11 类封闭枚举（职官/人物/机构/地点/文书/制度/行为/器物/刑罚/时间/数量 + 兜底"类型待定"）；
全文本内生词典（词条必须出现原文）；ENT-001..N + alias_index（复合词形手工映射）。

## 4. 规则层
触发词：不可/不许/务要/须/止许/毋/勿/痛加责治/责罚/限一日/打三十；
类型：禁止/义务/允许/程序/时限/处罚/优先级；槽位：条件/主体(含 subject_ent_ids)/动作/对象/模态/目的/处罚/出处；
AI 逐条判定（代码引擎只作候选）。

## 5. 流程层
steps + next + agent（agent_ent_ids）；04 卷直日建 9 状态 10 迁移状态机（显式时序）；
其余卷散点判"点不是线"，不强行建模；events 显式引用事件层 ID。

## 6. 结构化层（五维）
LGR 文簿台账 / TME 县政时间 / DOC 公文生命周期 / ACT 角色-职责 / FRD 防弊机制；
每维封闭枚举；target 用 ID 引用。

## 7. 事件层
五元组 who(含 who_ent_ids)/action/what/when/where；未明显式写"未明"；
01 卷试点 50 条验收 → 全量；01 卷 44 条未建模如实单列缺口（补法：按需补 _event_ai_01.py）。

## 8. 跨层整合
ID 对齐审计（主键唯一/引用合法/item_id 回填/target 用 ID/枚举口径一致）；
_kg_join.json + _kg_join_flat.csv（275 行，layer_count）。

## 9. 管线与验证
源数据：_rules_ai_NN.py / _proc_ai_NN.py / _struct_ai_NN.py / _event_ai_NN.py / 标注源；
打包器：annotate / build_ent_keys / build_rules / build_proc / build_struct / build_event / build_kg_join
  + _kg_enums.py（枚举单点）+ _kg_pack_base.py（公共基座）；
验证：每层"验证缺漏清单.txt"问题数 0；验证写文件不依赖 stdout；--volumes 单卷重跑。

## 10. 交付清单
按层聚合交付（≤6 组）；使用报告（跨层 CSV 一行全看/实体主键反查/溯源/重跑/扩展）；
项目总结报告（时间线/反思/根因/方法论/缺口）。

## 11. 缺口与边界
01 卷 44 条未建模事件；复合解读词形（把门皂隶/六房吏）12-58 处需 alias 映射；
双库落库（kg_wf + kg_ming）待接（按用户要求，非默认）。
```

## references/schemas.md 内容要点（启用层）

- 实体：id/text/type/start/end/normalized/confidence/source + 归一 + 主键表 schema
- 规则：rule_id/item_id/type/modals/condition/subject(+subject_ent_ids)/action/object/purpose/punishment/original/confidence
- 流程：process_id/item_id/name/steps(step_id/seq/text/agent+agent_ent_ids/next)/state_machine(states/transitions)/events/original
- 结构：ledgers(LGR)/times(TME)/docs(DOC)/actors(ACT)/frauds(FRD)，均含 item_id + ent_ids
- 事件：event_id/item_id/type/who(+who_ent_ids)/action/what/when/where（未明=显式"未明"）
- 示例条目：试点校验的 3~5 条真实条目（固化样例，压缩后不重读）
