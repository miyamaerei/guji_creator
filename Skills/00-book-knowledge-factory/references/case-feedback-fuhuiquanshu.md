# 《福惠全书》实例反馈（case-feedback-fuhuiquanshu.md）

> 工厂 Phase ②/⑤ 记录：结构性探查 → 引导式反思 → 设计结论 → 试点 → 坑。过程存工厂，实例只固化结论（实例 SKILL.md §0.1）。

## 1. 基本盘

- 清·黄六鸿《福惠全书》康熙三十三年（1694）自序，32 卷 14 部 + 禀启附，原文全卷合并 306,193 字。
- 内容形态：**政书全流程手册**——自序"自筮仕以迄升迁，部十有四"；筮仕部、莅任部、钱谷部、编审部、清丈部、刑名部（三卷）、保甲部、典礼部、教养部、荒政部、邮政部、庶政部、升迁部 + 禀启附（四六大启 20 + 四六小启 13）。
- 符号体例：正文 `○标题` 起条（兼条内注）、`△目` 为文书式（状式/票单/结状）、卷首另有标题列表（**与 lgs/xzl 的 ○ 同行标题不同，底座切分须专用逻辑**）。
- 密度信号：规范句触发词密集（禁 1373/不许 1172/务须 361/限 296/不得 256）→ 规则层；文书式密集（状式/票单/结状/牌批/谕告/结状）→ DOC 层；作者按语"愚按/余按"密集 → OPN 层；流程步骤链（签稿→行催→起解 / 验尸→审问→详报）→ PROC 层。

## 2. 引导式反思记录（用户方向原话）

- 用户拍板口径："默认条 / 政书 / 交付 JSON+CSV、白话文仅对照不建翻译层"。
- 用户网络研究启发（开工期）：郭润涛状式研究 / 杨志玖释六赃 / 云南高校公文程式 / 广陵书社简介——用户问"这书内容挺丰富，还有哪些结构可提取？"
- 用户拍板层方案："ok，8层，文书式按文书条目建模"——**DOC 文书层为本书特色**（文书式条目建模，区别于 lgs/xzl 无 DOC 层）。
- 用户要求："要从卷一开始执行"→ 延续"执行卷3以及以后所有卷"→ 全卷至全量交付；"移交，并且联邦库并入"→ kb-mcp 移交 + 联邦并入 + conflict 裁决。

## 3. 设计结论（固化进实例）

- 条目口径：**274 条** = 卷01-32 正文 241 + 卷33 禀启附 33 篇（按篇成条，稿目不重复计数）；卷33 原文 original 冗余（33-020 带小启标题列表）不影响锚点。
- 启用层：ent（ENTITY_ACTIVE 12 值）+ rule（RULE 7 中文键）+ struct 四维（ACT 5/FRD 4/LGR 6/TME 6，继承 lgs 归纳快照）+ reg（REG 政书英文键 10 值）+ opn（OPN 5 值）+ proc（L3 流程）+ doc（DOC 8 值本书归纳）+ rel（REL 12+角色版 4 值）+ 跨层索引。
- 不建：翻译层（白话文仅对照引用源）、QUANT/EVT 层（政书规范体非叙事体，密度实测后按密度未建）。

## 4. 试点（5 条真实条目，schema 无硬伤，固化 schemas.md §8）

01-001 总论（官箴体：RULE 义务型 + ACT official + OPN 肯定）、13-001 告盗情状式（状式：DOC 状词 + LGR template_form + RULE 时限）、22-001 编审保甲（保甲：REG baojia_xiangyue + proc 步骤链 + REL 保甲隶属）、27-002 积贮（荒政：rule 义务 + reg governance + proc 采买步骤）、33-001 大启（启禀：doc 启禀 + ent 施公）。

## 5. 本书特有坑（已入 pending-review 待评审 / 固化实例 schemas.md §9）

| 类别 | 坑 | 处理 |
|---|---|---|
| 跨层索引 | **目录名缺陷**：join 槽位单数层名 vs 产物复数目录 → 7 层静默空回填、validate 全绿不报 | build_kg_join.py 修复 (dir,key,id_key) 三元组；全量交付前查 layer_count 分布与 0 空条目率 |
| 联邦并入 | **adapter 单数 key 扫复数目录** → 首稿仅 ent 646 入库（7 层漏扫） | FqhAdapter LAYER_DIR_NAMES 复数映射（目录名+文件名前缀双映射），修复后 8 层 2104 条 |
| 枚举键位 | RULE_TYPES 用中文键 vs 工厂 RULE 英文键 → drift 报"库外 100%" | 如实记录为键位命名差异（同 REG 政书分支既有处理），提案 pending-review 归一 |
| 引用边 | 八层 `*_ent_ids` 全部未回填 → 联邦 refs 0 条 | 如实记缺口（nodes/canonicals 照常建立）；后续可走增量回填 |
| 源数据写入 | 多段源数据一次 Write 写全（卷26-32 rules 四段合并模板） | `_tmp_merge_rules{31,32}.py` dry-run 合并后写盘再删分文件，卷31 四段 16 条/卷32 四段 25 条核对无误 |

## 6. 全量执行结果（2026-10-12 收尾）

- **状态**：全量执行完成——33 卷 × 8 层 + 跨层索引；`validate_layers.py` 验收闸门 **ERR=0 / GAP=0**。
- **规模**：底座 274 条；ent 716 / rule 534 / struct 332 / reg 99 / opn 103 / proc 73 / doc 206 / rel 111 = **2174 条**；`_kg_join.json` 274 条全回填（layer_count 1~8 层齐全、0 空条目，分布 {1:32,2:50,3:54,4:49,5:40,6:23,7:12,8:14}）。
- **移交存量线**：kb-mcp `drift --book fuhuiquanshu-kb` 漂移 0 层（rules 库外 100% 为中英键位命名差异非真漂移；docs DOC 8/8、ent 12/20、regs 8/10、structs 4/21 全正常）；`sync` 11 组比对（EVENT 未启用正常、REG 政书分支 vs 中文 12 值既有口径、RULE 键位差、DOC/四维/REL 角色版工厂无段待提案）。
- **联邦并入**：`federation.py load --book fqh`（8 层 2104 条：ent 646 跨卷去重 + rule 534 + struct 332 + reg 99 + opn 103 + proc 73 + doc 206 + rel 111，折叠 0）+ transform（nodes 20804 / canonicals 1182 / members 4880）+ refs（`*_ent_ids` 未回填 → 引用边 0，如实缺口）。并入前备份 `kb.sqlite.bak_20261012_fqh`。
- **conflict 裁决**：fqh 侧待判 14 组全部裁决——**13 lock**（doc 卯簿/批回/揭帖/易知由单/甘结 + official 上司/佐贰官/典史/守备/广文/方伯/营官 + time 康熙九年，跨书概念同名同一实体）+ **1 reject**（person 方伯施公 vs 蘧编施公同名异人）；locked 190→203、rejected 1→2、fqh 侧待判清零；fed_search 验证（典史/守备/康熙九年跨书归一 lock 生效）。
- **交付**：`_deliver\` 全量交付说明 / 使用报告 / 项目总结报告 / `kg_join_flat_全量.csv`（275 行 utf-8-sig）。

## 7. 学习回路入库状态

- registry.md：11 行已登记（状态=全量执行完成；实例目录 11-fuhuiquanshu-knowledge——**与明会典 10 撞号，改号 11**）。
- pending-review.md：DOC 文书层模板 / 政书 8 层组合 / 跨层索引目录坑 / DOC_TYPES 8 值 / REL 角色版 4 值 / RULE 键位归一 6 项提案已追加（待评审）。
- 枚举：四维继承 v5 §1.18、REG 政书分支 v6 §1.12 已入库，本书不新增值；DOC/REL 角色版为本书归纳 → 提案 pending-review，未直接入库（待用户确认）。

## 8. 收尾增量（2026-10-12：引用回填 + 提案评审入库）

- **`*_ent_ids` 引用回填**（用户"要补的话走增量流程做一轮回填"）：
  - 写 `fuhuiquanshu-kb\_backfill_entids.py`（确定性匹配：ent_keys 词形 exact 全等 > contains 最长词形≥2 > split 标点拆分；宁缺毋滥，泛称角色如士君子/官/皇帝/绅衿 未标实体如实留空；幂等不覆盖已有值；产物备份 `_build\backfill_backup\`）。
  - 实测匹配率：rules.subject 534 可匹配命中 42（8%，主体多为泛称角色）、structs.target 68 命中 24（35%）、rels.person_a 111 命中 45（41%）、person_b 111 命中 60（54%）——命中样例质量可信（吏书/代书/京债/三连串票/粮长/排年 全对）。
  - 回填 171 处：subject_ent_ids 42（exact 22/contains 20）、target_ent_ids 24（exact 18）、person_a_ent_ids 45（exact 43）、person_b_ent_ids 60（exact 55）。
  - 联邦侧：refs.py REF_FIELDS/TEXT_FOR_FIELD 补 `target_ent_ids`（object/target）；重载 load fqh（2104 条折叠 0）+ refs（**records 2104 / refs 171 / resolved 170 / ambiguous 0**）+ transform（members 4880）→ fqh 侧待判 0、引用边 171（person_a 45/person_b 60/subject 42/target 24）。
- **6 项提案评审入库**（用户"请你评估一下然后入库"）：
  - 门槛核查：6 项全部满足（跨书复用 / 归并优先 / 用户确认）。
  - layer-library v12：C13 文书条目层（DOC）+ 方案组合"政书全流程手册 8 层（fqh 型）"。
  - enum-library v7（双写 enum-changelog）：§1.19 DOC_TYPES 8 值新段；§1.4 REL 角色版分支 4 值；§1.2 RULE 键位说明（中英皆可、drift"库外"为键位口径差）。
  - pitfalls v5：#28 跨层索引目录名缺陷、#29 联邦 adapter 目录名映射偏移、#30 实例编号撞号。
  - pending-review.md 6 项状态改"已升级"、去向登记；registry.md 11 行状态/备注同步更新。
