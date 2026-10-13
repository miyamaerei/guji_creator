# 《政学录》实例反馈（case-feedback-xuezhenglu.md）

> 工厂 Phase ②/⑤ 记录：结构性探查 → 引导式反思 → 设计结论 → 试点 → 坑。过程存工厂，实例只固化结论（实例 SKILL.md §0.1）。

## 1. 基本盘

- 清·郑端辑《畿辅丛书》本，5 卷约 11.6 万字；○166 + △20 = 186 标题，正文约 183 条。
- 内容分两大块：①卷一~二清初官制则例（内阁六部科道部院 + 直省事例，奏疏/部覆/奉旨体，顺治 10/康熙 45/万历 13 纪年）；②卷三~五官箴政术辑录（吕坤《实政录》条文 39 处 + 王守仁十家牌法 + 状式 + 刑戒 + 狱政）。
- 密度信号：规范句触发词密集（不可 236/不许 100/勿 47/毋 22/限 130）→ 规则层；文书簿册密集（状式 69/刻册 29/簿 76）→ LGR 维；时限密集（限 130 处）→ TME 维；官职机构（州县级 154/督抚 37 处）→ 实体层。

## 2. 引导式反思记录（用户方向原话）

- 用户拍板层方案："推荐四件套（L1+L2+L4四维）"——否掉加 L3 流程/C11 奏疏互动的扩展包（卷一"臣疏→部覆→奉旨"为则例叙事，点状不成链）。
- 用户拍板粒度："条（186 个标题条目）"。
- 用户口径（lgs 延续）：不建翻译层，白话文 `政学录_全文_白话.txt` 作对照引用源；交付 JSON+CSV。
- 契约线：book-mcp selftest 20 项全过（C1–C7）；ENTITY 20 值 + 3 别名、RULE 7 值，与 `_kg_enums.py` 一致。

## 3. 设计结论（固化进实例）

- 条目口径：**183 条** = 186 标题 − 6 个无正文 ○ 分组标题（吏部/户部/礼部/兵部/刑部/工部）+ 3 个卷级条目（卷一"内阁/六部/科道"无符号标题带正文）。卷一 23 / 卷二 15 / 卷三 111 / 卷四 2 / 卷五 32。
- 启用层：L1 实体（ENTITY_ACTIVE 13 值）+ L2 规则（RULE 7 值）+ L4 结构化四维（ACT 5 / FRD 4 / LGR 6 / TME 6，继承 lgs 归纳快照，本书不新增值）+ 跨层索引。
- 不建：L3 流程 / L5 事件 / C5 翻译 / C11 奏疏互动。

## 4. 试点（5 条真实条目，schema 无硬伤，固化 schemas.md §8）

01-004 选法（则例体：procedure+deadline 规则 + TME deadline + ACT official）、03-001 戒营求（官箴体：RULE prohibit + FRD abuse）、03-078 一条鞭（制度说明型：ent+rule 为主，struct 不强建）、05-001 人命告辜式（状式：LGR template_form + RULE deadline/prohibit + TME deadline）、05-025 五不打（刑戒：FRD guard + RULE prohibit 五条并列拆多条）。

## 5. 本书特有坑（已入 pending-review 待评审 / 固化实例 schemas.md §9）

| 类别 | 坑 | 处理 |
|---|---|---|
| 切分纪律 | 卷拆分文件**标题与正文分行**（`○戒营求` 为标题行，正文下一行起）——lgs 卷文件是"标题　正文"同行 | build_base.py 切分合并标题行+正文；全文合并版作交叉校验（186 标题逐一核对） |
| 切分纪律 | 卷一"内阁/六部/科道"3 个**无符号标题连续排列**（总目），正文在其后分三段（今之内阁…/督臣卢兴祖疏/台臣田六善疏） | 卷级缓冲 + 按"督臣/台臣"分界拆三条；与 lgs"卷首篇目不计数"坑同源异形 |
| 切分纪律 | 6 个 ○ 分组标题（吏部等）无独立正文 | 排除不计数（复用 lgs"卷首篇目不计数"口径） |
| 内容形态 | 则例体（卷一~二）为"旧例…后改…"沿革叙事 | 只抽现行有效规范，沿革说明归 L1 system + L4，不抽规则 |
| 内容形态 | 制度说明型条目（一条鞭） | struct 不强建（无防弊/文簿/时限对象时），ent+rule 为主 |

## 6. 学习回路入库状态

- registry.md：08 行已登记（状态=已交付（待执行））。
- pending-review.md：上述切分纪律候选已提案（待评审）。
- 枚举：四维类型继承 lgs 归纳快照（enum-library v5 §1.18 已含），本书**不新增值**，无需双写入库；执行期未匹配值走 V3 收集。

## 7. 增量升级（2026-10-12：REG 制度层 + L5 事件层）

- **触发**：用户指出设计时漏了事件层与制度层；密度探查两本对比后用户拍板——政学录 REG+L5 都建、lgs 不补。
- **密度证据**：政学录制度为全书主体形态（钱粮 133/令 260/例 80/状式 69/律 58/保甲 32，制度描述体）；事件集中在卷一~二沿革叙事（纪年 67/奏疏互动词 117，粗估 60~90 事件），卷三~五规范句为主。lgs 事件层不建（纪年 5/奏疏 5，点不是线）；制度层中低（规范体非制度描述体）不回填。
- **实例改动**：SKILL.md（§0.1 增量条目 + §5.5/§5.6 + C2/C4/C5 + 管线 build_reg/build_events + 口径 183 修正）；schemas.md（契约登记 reg/evt 行 + §7.5/§7.6 schema + §8.6~8.10 增量试点 5 条 + §9 坑注 7）；`_kg_enums.py` V1.0 → **V1.1**（REG_TYPES 10 本书归纳 + EVENT_TYPES 27 继承基准库顶层）。
- **试点 5 条**（01-004 选法/01-006 钱粮总归户部/03-078 一条鞭/04-002 十家牌法/05-001 告辜式）：REG 与 L4 分工清晰无冲突；EVT 沿革全链记 1 条；状式类 EVT 缺口如实记。
- **待评审**：REG 层模板入层库 + L5 沿革事件型适用说明（pending-review.md 已提案）。

## 8. 全量执行结果（2026-10-12 收尾）

- **状态**：全量执行完成——5 卷 × 5 层 + 跨层索引；`validate_layers.py` 验收闸门 **ERR=0 / GAP=0**。
- **规模**：底座 183 条（01-001..05-032）；ent 1159 标注 / 1102 唯一实体（ENT-0001..1102）；rule 293；struct 244；reg 103；evt 91；`_kg_join.json` 183 条全回填（layer_count 5=107 / 4=66 / 3=9 / 2=1）。
- **分卷**：卷一 23（ents 288/rules 56/structs 56/regs 23/evts 44）、卷二 15（334/24/40/20/33）、卷三 111（370/95/76/19/4）、卷四 2（97/86/42/21/8）、卷五 32（70/32/30/20/2）。卷三/五事件稀少属如实缺口（官箴/技术体无纪年锚点）。
- **执行期踩坑（已入 pending-review 待评审）**：① 卷四 evt 首稿 7 条误用英文枚举外值（disaster/relief/criminal_case → 应 calamity/disaster_relief/justice）；② ent 3 条 concept 未注册（六流/四法/楚谚 → behavior/unknown）；③ 卷四 GAP 5 处 text 未命中原文（保副/旌善亭/青苗法/保甲法/左副都御史 → 改原文词形）；④ 卷三/五 evt 4+2 条仅制度沿革锚点，其余如实记缺口。
- **交付**：`_deliver\全量交付说明_政学录.md`（统计/抽查/踩坑/下一步）；`_kg_join_flat.csv`（183 条 9 列）。

## 9. 移交 + 联邦库并入结果（2026-10-12 收尾）

- **存量线移交**：`tools/kb-mcp/kb_mcp/registry.py` 登记 `xuezhenglu-kb`（flat 后端 `_kg_enums.py`；globs `_layers/*/*.json`；schemas 指向 08 实例）。体检：`drift --book xuezhenglu-kb` **漂移 0 层 / 库外 0 条**（五层全恢复：ent ENTITY 13/20、evt EVENT 10/27、reg REG 8/10、rule RULE 6/7、struct STRUCT 4/21——四维 21 含子类）；2 项 warn 为英文键 other 非中文兜底口径差（非漂移）。
- **联邦库并入**：`tools/kb-federation/` 新增 `adapters/xzl_adapter.py`（XzlAdapter：与 LgsAdapter 同构但支持五层——ent 按 ent_id 跨卷去重 1159→1100；rule/struct/reg/evt 直取 rule_id/struct_id/reg_id/event_id；fingerprints 读工程根 `_kg_join.json`），注册 BOOK_ROOTS/NAMES/LAYERS/LAYER_DECL/BOOK_REGISTRY（book_id=xzl，五层声明 ent/rule/struct/reg/evt）。**首稿 id_key 误用 evt_id（产物字段为 event_id）致 50 条 OR REPLACE 折叠 → 修复后折叠 0**。跑 `load --book xzl`（items 183 / records 1831：ent 1100 + rule 293 + struct 244 + reg 103 + evt 91，折叠 0）+ `transform`（nodes 19825 / canonicals 1071 / members 4512）+ `refs`（4605 条引用边，resolved 3983 / ambiguous 218）。并入前已备份 `kb.sqlite` → `kb.sqlite.bak_20261012_xzl`。
- **跨书查重**：`fed_search 吕坤` → canon-00706（lgs:ENT-0001 + xzl:ENT-0151，exact_label 1.0 auto 合并——同一人，吕坤两书同现，符合预期）；`fed_conflicts --book xzl` 101 条待判全部按关系裁决 **lock**（职官泛称 55 / 文书簿册 32 / 十吏行为 13 / 时辰 1——与 lgs 裁决模式一致：泛称职官/文书/行为/时辰概念跨书同一对象），locked 89 → **190**。
- **枚举评审入库**：enum-library **v6**——§1.12 REG_TYPES 追加**政书分支**（英文键 10 值：official_system/selection_assessment/fiscal/justice_prison/baojia_xiangyue/education_sacrifice/military/post_transport/governance/other，六项与笔记体 12 值归并映射 + 三项政书特色）；EVENT 英文键继承登记（实际使用 10 种无新增值）；enum-changelog v6 双写完成。
