# 实例详情（Registry Detail）

> `registry.md` 主表只留「一屏可扫」的状态；本文件承接各实例的**详细备注**——执行地点、规模数字、联邦库/kb-mcp 落地结果、修正记录、遗留项。
> 按实例分节，节标题与主表「实例目录」列同名。**新增实例先写主表一行，详情写本文件对应节**（不要写回主表备注列）。
> 版本：2026-10-15 首次分离（原主表 11 行的备注列合计 5,586 字符）。

---

## 01-shuidong-riji-knowledge（水东日记）

- **状态**：全量执行完成（38 卷 × 8 层）。
- **最近增量**：2026-10-10（追加 NAM 名录谱牒 + TRL 古今翻译）。
- 其案例反馈催生坑库 #11–#20 与枚举库 v2。

## 02-qubian-knowledge（蘧编）

首个配齐 V2/V3 治理组件的实例；ID 段位 ×500。

## 03-wuzazu-knowledge（五杂俎）

13 层为现有实例中最多；ID 由打包器段位分配。

## 04-kezuozhuiyu-knowledge（客座赘语）

目录已纳入编号；SKILL.md 输入路径已相对化。
**遗留**：frontmatter `name: kezuo-zhuiyu-knowledge` 与目录拼写不一致（工厂原则 6 要求一致，待统一）。

## 07-lvgong-shizhenglu-knowledge（吕公实政录）

- **内含式**：实例与 `shizhenglu-kb/` 工程同目录（`shizhenglu-kb/07-lvgong-shizhenglu-knowledge/`）。
- **首个按 `docs/新书开工流程.md` 契约线（tools/book-mcp C1–C7）实例化的新书**；编号 07（README 预留 06 予新官轨范）。
- 枚举单点 `_kg_enums.py` 建于工程根。
- **全量** 119 条 / ent 651（573 唯一）/ rule 664 / struct 235，ERR=0 GAP=0。
- 联邦库 `federation.py load --book lgs`（ent 573/rule 664/struct 235，折叠 0）+ transform + refs 完成。
- kb-mcp `drift --book shizhenglu-kb` 三层全恢复（ent/rule/struct 漂移 0、库外 0）——struct 段入库后护栏恢复（v5）。

## 08-xuezhenglu-knowledge（政学录）

- **内含式**：实例与 `xuezhenglu-kb/` 工程同目录（`xuezhenglu-kb/08-xuezhenglu-knowledge/`）。
- 按 `docs/新书开工流程.md` 契约线实例化（book-mcp C1–C7 实测 selftest 全过）；编号 08。
- 枚举单点 `_kg_enums.py` V1.1（四维继承 lgs 归纳快照 + REG_TYPES 10 本书归纳 + EVENT_TYPES 27 继承基准库顶层）。
- **全量** 183 条 / ent 1159（1102 唯一）/ rule 293 / struct 244 / reg 103 / evt 91，validate_layers ERR=0 GAP=0。
- 联邦库 `federation.py load --book xzl`（五层 1831 条：ent 1100/rule 293/struct 244/reg 103/evt 91，折叠 0——evt 首稿 id_key 误用 `evt_id` 致 50 折叠，修复为 `event_id` 后折叠 0）+ transform + refs。
- conflict 按关系裁决 101 lock（职官泛称 55/文书簿册 32/十吏行为 13/时辰 1，lgs 模式延续，locked 190）。
- kb-mcp `drift --book xuezhenglu-kb` 五层全恢复（漂移 0、库外 0）；REG 政书分支枚举 v6 入库 §1.12。
- 白话文作对照引用源不建翻译层（用户口径）。
- 底座 183 条 = 186 标题 − 6 无正文分组 ○ + 3 卷级。
- **增量**：用户指出漏事件/制度层，密度探查后拍板政学录 REG+L5 都建、lgs 不补（事件纪年 5 点不是线）。

## 09-yuanshuzaji-knowledge（宛署杂记）

- **内含式**：实例与 `yuanshuzaji-kb/` 工程同目录（`yuanshuzaji-kb/09-yuanshuzaji-knowledge/`）。
- 按 `docs/新书开工流程.md` 契约线实例化（book-mcp selftest 20 项全过）；编号 09。
- 枚举单点 `_kg_enums.py` V1.0（ENTITY 20 / APPT 12 / EVENT 27 顶层中文 / LIT 本书子集 / REG 12+2 本书归纳 / NAM 7 / OPN 5 / CUS 12 / GEO 9）。
- 底座 155 条 = 165 标题 − 10 无正文 ○ 分组（山川/经费上/经费下/人物/恩泽/志遗一~五）。
- 试点 5 条枚举全命中，固化 schemas.md §5；白话文作对照引用源不建翻译层（用户口径）。
- 用户定位「知县本人的亲历亲记」（否定官箴规则型 L1+L2+L4）；用户两次强调写开工手册（已落盘 `yuanshuzaji-kb/00_新书开工指引.md`）。

## 10-minghuidian-knowledge（明会典）

- **内含式**：实例与 `minghuidian/` 工程同目录（`minghuidian/10-minghuidian-knowledge/`）；编号 10。
- **迄今最大一本**（粗估 3000–5000 条，为吕公实政录 20–30 倍）。
- 父子树层架构（用户要求「按父子集划分、按组性质区分」）；执行单元 = 书 → 大卷组 (G0–G8) → 小卷组 → 事目 → 条（用户要求「不是一卷卷推」）。
- 9 大卷组：宗人府 / 吏 12 / 户 28 / 礼 64 / 兵 24 / 刑 14 / 工 20 / 文职 15 / 武 2。
- 枚举基线明确标注「缺漏待补」（用户原话），执行期走 V3 校准。
- **OCR 警告**：会→防、御→防 系统性误识；卷 128/129/130 标题 OCR 漏识别。

## 11-fuhuiquanshu-knowledge（福惠全书）

- **内含式**：实例与 `fuhuiquanshu-kb/` 工程同目录（`fuhuiquanshu-kb/11-fuhuiquanshu-knowledge/`）；编号 11（**与明会典 10 撞号，改号 11**）。
- 按 `docs/新书开工流程.md` 契约线实例化；枚举单点 `_kg_enums.py` V1.0（ENTITY 20 / RULE 7 中文键 / REG 政书英文键 10 / OPN 5 / 四维继承 v5 / DOC 8 本书归纳 / REL 12+角色版 4）。
- **全量** 274 条 / ent 716 / rule 534 / struct 332 / reg 99 / opn 103 / proc 73 / doc 206 / rel 111 = **2174 条**，validate ERR=0 GAP=0。
- 跨层索引 `_kg_join.json` 274 条全回填（layer_count 1~8 层 0 空条目）。
- 联邦库 `federation.py load --book fqh`（8 层 2104 条：ent 646 去重 + 七层直取，折叠 0——首稿 adapter 单数 key 扫复数目录仅 ent 646，修复 `LAYER_DIR_NAMES` 复数映射后 8 层）+ transform + refs（`*_ent_ids` 回填 171 处：subject 42 / target 24 / person_a 45 / person_b 60，确定性匹配 exact/长包含，泛称角色如实留空；refs.py 补 `target_ent_ids` 物化 → 引用边 171 条、resolved 170、ambiguous 0）。
- conflict 按关系裁决 14 组（doc 5 + official 7 + time 1 概念同名 lock 13、person 方伯施公 reject 1，locked 203）。
- kb-mcp `drift --book fuhuiquanshu-kb` 漂移 0 层（rules 库外 100% 为中英键位命名差异非真漂移）。
- 白话文作对照引用源不建翻译层（用户口径）；用户拍板「8 层，文书式按文书条目建模」（DOC 层为本书特色）。
- 底座 274 条 = 卷 01–32 正文 241 + 禀启附 33 篇。
- **学习回路**：6 提案评审入库（DOC 文书层 C13 + 政书 8 层组合 → layer-library v12；DOC_TYPES §1.19 + REL 角色版 + RULE 键位 → enum-library v7；跨层索引目录坑 #28/#29 + 撞号 #30 → pitfalls v5）。

## 12-pingpingyan-knowledge（平平言）

- **内含式**：实例与 `pingpingyan-kb/` 工程同目录（`pingpingyan-kb/12-pingpingyan-knowledge/`）；编号 12。
- 按 `docs/新书开工流程.md` 契约线实例化（C1–C7 台账固化）；枚举单点 `_kg_enums.py` V1.0（ENTITY 20 继承 / RULE 7 中文键 / 四维继承 lgs/xzl 快照 / REG 政书英文键 10（v6）/ OPN 5）。
- 底座 **284 条** = 卷一 84 + 卷二 87 + 卷三 43 + 卷四 70（卷首清单 × 正文 ○ 对齐切分，零警告，合并版交叉校验 OK）。
- **全量** 284 条 / ent 382 标注（337 归一主键）/ rule 262 / struct 231（ACT 63/FRD 136/LGR 24/TME 8）/ reg 20 / opn 265 = **1160 条层记录**，validate ERR=0 GAP=0。
- 跨层索引 `_kg_join.json` 284 条全回填（layer_count 1~5 层 0 空条目，分布 {1:24, 2:38, 3:106, 4:112, 5:4}）。
- 联邦库 `federation.py load --book ppy`（5 层 1115 条：ent 337 去重 + rule 262/struct 231/reg 20/opn 265，折叠 0）+ transform + refs（引用边 4776、resolved 4153、ambiguous 218）。
- conflict 0 待判（ppy 无跨书同名冲突）。
- kb-mcp `drift --book pingpingyan-kb` 四层恢复（ent/reg/struct 漂移 0、库外 0；rule 库外 100% 为中英键位差异非真漂移，同 fqh 先例；opn 层不参与 drift 为工具既有行为）。
- **执行期修正**：双题连排正文错位（01-039/040 按指纹 original 对调归位）、繁体枚举「懷疑」→简体「怀疑」、struct target 占位残留、**ent 主键 ID 用全局顺序（ENT-0001 起）非契约段位**（与 lgs/xzl/fqh 先例一致，已注 schemas.md §4）、kg_join 每卷重建 + PowerShell 多卷参数拆参致 0 条回填（收尾用缺省模式重跑）；清理 3 条历史遗留幽灵主键（ENT-0250/0278/0299 已分配无标注记录，主键表 340→337 与产物一致）。
- 序/凡例/跋归 00 版本说明卷不入条目库（用户口径）；白话文作对照引用源不建翻译层（用户口径）。
- **编码备忘**：工程根 `原文/平平言_原文_全卷合并.txt` 为 GBK（Windows 直读乱码），实例内统一 UTF-8（`scripts/prepare_sources.py` 可重跑）。
- 候选提案 3 项入 pending-review（官箴规则型 7 层组合 / GBK 合并源编码坑 / 官箴说理句不抽规则判定口径），执行期新增坑 2 项建议追加（kg_join 重建覆盖 + PowerShell 拆参 / 幽灵主键增量空洞）。

## mingshi-zhiguanzhi（明史·职官志）

> 目录名由用户指定，非工厂 `NN-<slug>-knowledge` 格式。

- **状态（全量）**：全五卷收官（5 卷 × 9 层 + 跨层索引，317/317 条）；validate ERR=0 GAP=0；跨层索引 0 空条目（填充率 100%）；v9 字段回填 + v10 C15 官职层（1241 节点）+ v11 机构附加属性族（seal/powers/assess/doc_channel/jurisdiction/station）+ v12 道制驻点（206 道 / 89 驻点）与三缺口修补；可用性审计 30 问：20 答得出 / 10 答不出（7 条原文确无、3 条结构缺陷已修）。
- **本实例是工厂四族工程侧错误的主要来源实例**（A/B/C/E/F 族贡献最集中），其沉淀直接催生工厂**首个打包器骨架** `assets/skeletons/packer_skeleton.py` + `self_test.py`；49 项提案入库（layer v15 / enum v8 / pitfalls v8–v14 的 #45–#62 / error-taxonomy v1.3）；枚举 `_kg_enums.py` V1.9。
- **最近增量（2026-10-15）**：v2 树形数组 → v3 员额置信度 → v4 差遣条目 → v5 层级判据·树深 → v6 南京关联·道杂职 → v7 取消模板容器 → v8 卷 05 军事卫所土司 → v9 全书性专表 + 字段回填 → v10 C15 官职层 + 俸禄两层 → v11 机构附加属性族 → v12 道制驻点 + 三缺口。
- **源文件**：`assets/sources/明史职官志.txt`（随实例存放，UTF-8，233256 字节 / 347 行 / 有效字 79839；底本 =《明史》职官志一~五）。
- **产出位置由用户显式指定**：`E:\git\ToolBox\guji\mingshi\mingshi-zhiguanzhi\`；frontmatter `name: mingshi-zhiguanzhi-knowledge` 与目录对齐。
- **工厂首个「正史典志体」实例**（既往为官箴政书/笔记/年谱/方志/会典）。
- **结构**：`◆章` 5 / `◎卷` 5，**无条级标记** → 切分口径「**被正文包围的无句号段**」，实测 **317 条**（逐卷 53/74/55/75/60）。底座：233,256 字节 / 347 行 / 有效字 79,839。
- **全量结果**：ent 3261 标注→2154 归一 / rule 282 / proc 52 / struct 993 / officials 1246 / appt 83 / tme 434 / chain 220 = **5105 条层记录**；ID 段位 `ENT-` 全局 + 其余卷×500；枚举单点 `_kg_enums.py` V1.9。
- **关键设计判断**：沿革三分承载（TME 时间 + L4-EVO 机构 + APPT 人物）故不建 L5 事件层；卷五总兵官清单归 L4 不建 NAM；职掌陈述句不抽规则。
- **迭代链 v2–v12** 逐轮根因与修法见 `case-feedback-mingshi-zhiguanzhi.md` §3「迭代版本表」（主档已按 A 案压缩：42,518 → 13,999 字符，原 §5 迭代流水全文存档于实例 `_data/case-feedback-§5-迭代过程存档.md`，27,508 字符）。
  逐轮：v2 树形数组 / v3 员额置信度 / v4 差遣条目 / v5 层级非递减+树深 ≤4 / v6 南京 `link_to_bj` / v7 取消 `ORG_TEMPLATES` 容器 / v8 军事编制 `level_ok` 内设机构放行 / v9 全书性专表+字段回填 / v10 C15 官职层 / v11 机构附加属性族 / v12 道制+三缺口。
- **可用性审计**：`_usability_audit.md` 30 问句实测 20 查得到 / 10 查不到。
- **交付**：`《明史·职官志》使用报告.md` + `《明史·职官志》项目总结报告.md`（2026-10-15，实例根目录）。

## mingshi-shihuozhi（明史·食货志）

> 目录名由用户指定，非工厂 `NN-<slug>-knowledge` 格式。

- **状态**：已交付（待执行）——Phase ① 探查取证 / Phase ② 方案确认 / Phase ③ 实例化落盘完成；**尚未开始 Phase ④ 试点与全量执行**。
- **产出位置由用户显式指定**：`E:\git\ToolBox\guji\mingshi\mingshi-shihuozhi\`；frontmatter `name: mingshi-shihuozhi-knowledge` 与目录对齐。
- **源文件**：`assets/sources/明史食货志.txt`（随实例存放，UTF-8，177,909 字节 / 288 总行 / 271 非空行 / 59,118 有效字；底本 =《明史》食货志一~六，卷五十三~五十八）。
- **与职官志「同源异形」**：同属《明史》典志体、同用汉字卷名切分与 C14 TME、同为「被正文包围的无句号短行」判据；但对象由**机构**换为**制度**，四维由 ORG/RANK/LINE/EVO 换为 QUAN/INST/EVO/FISC。**工厂第二个正史典志体实例，也是首个「食货门」实例。**
- **新建方案组合 shz 型（8 层 + C16）**：L0 底座 / L1 实体 / L2 规则 / **REG 制度（★本书骨架）** / L3 流程 / **L4 食货四维（QUAN 数额定额·INST 制度类型·EVO 沿革阶段·FISC 财政流转）** / **C16 总账树 LEDGER（本实例新增结构资产）** / C1 任职 / C14 时间沿革 / C9 论说 OPN + 跨层索引。
- **内容形态**：「**时序沿革叙事体**」（初置某制 → 其间增损 → 弊生 → 谋议 → 改革 → 结果），**不是**职官志的编制/职掌/沿革三段体。这是「骨架是 REG 而非 ORG」的直接原因。
- **切分**：`◆` 卷标 6 行 + `◎` 卷内标题 6 行 + `○` 子目标记**仅 5 行**（**卷五十三无 ○**，子目为无标记短行 L5 `户口田制(屯田庄田)`）→ 判据仍用「被正文包围的无句号短行」。行长度：最短 3 / 最长 902 / 中位 191 / 均值 218。
- **用户六项需求（m05345）与裁定（m05362）**：① 户口户籍 ✅ 证据充分（黄册 8/里甲 19/粮长 14；三次人口统计洪武二十六年 10,652,870 户 60,545,812 口 / 弘治四年 9,113,446 户 53,281,158 口 / 万历六年 10,621,436 户 60,692,856 口）；② 土地制度 ✅（官田 28/民田 26/屯田 27；`凡二等：曰官田，曰民田。`）；③ **OPN 论说层 → 用户裁定建**（`言：` 98 处长段奏议）；④ **制度层加 13 项属性 → 用户要求完善**（制度名称/类别/创设沿革/主管部门（联动官制库）/征收对象/征收物/税率定额/覆盖范围/文书载体/执行者（品官·役）/目的/弊病改革/史料来源；并须标注 list 与可拓展、支持动态追加）；⑤ **国家总账树形图 + 「一把捞」组装器** ✅ 原文有整段实体（食货六 L272–L285「九边钱粮总账」13 镇逐镇列主兵/客兵各项来源与数额）→ **C16 总账树**；**马政 → 用户裁定不建**（原文确无独立马政篇：太仆寺 0 / 苑马寺 0 / 种马 0 / 俵马 0 / 牧监 0，仅附茶法）；**县级税额 → 用户裁定不建查表**（原文无偿付定额，只有 `银额` 公式与一条鞭法 `皆计亩徵银`）；⑥ 征收物四元组 ✅ 原文完整支持（`{"item":"米","form":"本色","amount":4000000,"unit":"石"}`；全书折色 36/本色 37；L37 区有完整折纳定例）+ 运送途径 ✅ 存在但弱（递运链淮安→徐州→临清→德州→通州；程限逐省月日；`三年考成，违限者，运官降罚`；船制 `每船受正耗米四百七十二石`；漕粮定额成化八年四百万石）。
- **实例化时自检抓出并修入工厂骨架的两个真缺陷**：**#63** `check_naming_consistency()` 对 list 调 `.items()`（#62 修法本身引入回归，且 `self_test.py` 用与生产不一致的 dict 形状喂函数致自检通过——A6 子型教科书样本）；**#64** `cn2int('十三万二千馀')` → `None`（约数后缀 `馀/有奇` 未剥离，且可夹在数字中间如 `四百三十馀万束`；对本实例为 **CRITICAL**，13 镇数额几乎全带 `馀`，不修则 C16 整棵树为空且不报错）。二者促成 pitfalls **v15**（#0–#64）。
- **落盘文件**：`SKILL.md`（15,901 字符 / 543 行）/ `references/exploration-findings.md`（Phase ① 探查证据存档）/ `references/design-decisions.md`（Phase ② 方案确认记录）/ `references/schemas.md`（各层 schema 与示例）/ `scripts/_common.py`（工厂骨架复制 + `LAYER_SPECS` 填充）/ `scripts/_kg_enums.py`（枚举单点，VERSION 1.0）/ `assets/sources/` + `assets/templates/`；已建工作目录 `_data/ _extract/ chapters/ _layers/{ents,rules,regs,procs,structs,appts,tmes,opns}/ _views/`。
- **待回写工厂**：`layer-library.md` 新增 shz 型与 C16 自定义层；`enum-library.md` 新枚举（QUAN_FORMS/QUAN_ORIGINS/INST_TYPES/EVO_STAGES/FISC_STAGES/REG_DOCS/REG_AGENT_KINDS 等）；新坑入 `pending-review.md`。
