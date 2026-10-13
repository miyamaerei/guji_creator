# 《平平言》实例案例反馈（case-feedback-pingpingyan）

> 工厂学习回路的**过程**记录（探查/反思/实例化/试点全过程），实例只固化结论。登记：实例 12-pingpingyan-knowledge，2026-10-13。

## 1. 探查（Phase ①）

**接收**：用户指定使用工厂 `E:\git\ToolBox\guji\Skills\00-book-knowledge-factory`，对"平平言"（实为《平平言》）提炼 skills；书籍在 `E:\git\ToolBox\guji\pingpingyan-kb\`，原文在 `原文/` 目录。

**探查动作**：
- 读序（4 篇：杜贵墀序+续序、卞宝第序、但湘良序）、凡例、跋 → 书目性质确认：清·方大湜（菊人，巴陵人）著，官箴/吏治书，凡例自述"专言吏治""独详于州县""但求可行……件系条分"，为训子弟而作。
- 卷结构：本工程存 4 卷（序称六卷，现存卷一~四）。条目体：`○标题 + 正文`。
- 密度统计（代码）：卷一 84 条 / 卷二 87 条 / 卷三 43 条 / 卷四 70 条 = **284 条**。
- 抽样（首/中/尾卷各 3~5 条）：卷一（造福莫如州县/公罪私罪/大计）→ 规范句 + 论说 + 则例摘录；卷二（门丁不可用十弊/官须自做/权不下移）→ 规范句 + 长文积弊论述 + 亲历记事；卷四（旌表则例/保甲/仓谷/钱粮/交代）→ 制度条文成片（礼部则例/会典事例/通行）。

**形态判定**：政书规则型（官箴书），与吕公实政录（07）/政学录（08）/福惠全书（11）同族。

**编码发现**：`原文/平平言_原文_全卷合并.txt` 为 GBK 编码（PowerShell 直读乱码）；分卷 txt 为 UTF-8 正常。→ 实例内统一 UTF-8 重合并，留 `scripts/prepare_sources.py` 可重跑。

## 2. 反思（Phase ②）

**第 1 轮（AI 汇报 + 收方向）**：汇报结构性探查发现 + 层库匹配信号，用 interaction_ask 收方向（2 问）：
1. 层方案：规则型 7 层（推荐）/ 规则型+事件层 / 手册型 8 层 fqh 同款 / 自定义
2. 工程对接：沿用 shizhenglu-kb 契约线 / 本地默认交付

**用户拍板（原话要点）**："规则型7层（推荐）" + "沿用契约线"。

**锁层**：L0 底座（284 条）+ L1 实体 + L2 规则 + L4 四维（ACT·FRD·LGR·TME）+ REG 制度（政书英文键）+ OPN 论说 + 跨层索引；不建 L3 流程 / L5 事件 / DOC 文书 / REL 角色 / CIT 引书；不建 TRL 翻译层（白话文作对照源，沿用 lgs/xzl/fqh 口径）。

**证据要点**：
- L5 不建：前代故事+亲历案例约 40+ 处，但为说理引证（法戒）非纪事主线，判"点不是线"；
- DOC 不建：文书式内容不密集（告示/详/禀多提及无程式实例）；
- REL 不建：人物关系以角色论说为主，ACT 可承载；
- OPN 建：作者亲历按语 + 引论密集（"余令广济凡五年…""余篆襄阳县事…"+吕坤/汪辉祖/刘衡/袁守定等）。

## 3. 实例化（Phase ③）

- 命名：`12-pingpingyan-knowledge`（编号 12 = 台账现有最大编号 11 + 1；06 预留新官轨范，05 属另一工厂不入本台账）。
- 位置：内含式 `pingpingyan-kb/12-pingpingyan-knowledge/`（与工程同仓，近期实例惯例）。
- 骨架：SKILL.md + references/schemas.md + assets/sources/（UTF-8 合并版原文/白话 + 卷拆分主源 + 序凡例跋）+ assets/templates/（两份报告母版）+ scripts/prepare_sources.py。
- 契约台账 C1–C7 固化（docs/新书开工流程.md Step 0 + tools/book-mcp contract.json 实查）。
- 枚举单点 `_kg_enums.py` V1.0 设计（ENTITY 20 继承 / RULE 7 中文键 / EVENT 27 备用 / REG 政书英文键 10（v6）/ OPN 5 / 四维继承 lgs/xzl 快照）。

## 4. 试点（Phase ④）

5 条真实条目试跑（01-001 造福莫如州县 / 01-002 造孽莫如州县 / 01-025 各房呈须知册 / 01-026 清查前任命盗各案 / 01-032 公罪私罪），覆盖全部 5 层：
- ent：州县/章枫山/须知册/公罪/私罪/级纪/笞杖（official/person/doc/system/punishment 类型命中）；
- rule：禁止型（万不可造孽/私罪必不可有）、程序型（须知册发还细查、清查命盗开摺送阅）；
- struct：ACT-0501（official）/ FRD-0501（abuse）/ LGR-0501（ledger）/ TME-0501（deadline）；
- reg：REG-0501（justice_prison 命盗清查审限参限）/ REG-0502（official_system 公罪私罪抵销则例）；
- opn：OPN-0501（肯定）/ OPN-0502（否定）；
- 验证"说理条不抽规则"口径：01-001 纯说理条只建 ent/opn 无 rule。
- ID 段位：卷 01×500+1 = 501 全部正确，无撞号。示例固化 schemas.md §4。

## 5. 候选提案（→ pending-review.md，待评审）

1. **官箴规则型 7 层组合（ppy 型）**：L0+L1+L2+L4+REG（政书键）+OPN+跨层索引——介于 lgs/xzl 四件套（缺 OPN）与 fqh 8 层手册型之间的官箴论说型组合。
2. **坑·GBK 合并源文件编码**：脚本产物合并文件可能 GBK，实例内须统一 UTF-8 重合并 + 可重跑脚本。
3. **坑·官箴说理/亲历记事句不抽规则**：防止规则层被议论句污染（归 OPN/FRD）。

## 6. 待办（实例执行期）

- `build_base.py` 底座切分 284 条（卷一 84 / 卷二 87 / 卷三 43 / 卷四 70）→ `_item_registry.json`；
- `_kg_enums.py` 落盘（pingpingyan-kb 根）→ 各层打包器 → `_kg_join` → validate ERR=0/GAP=0；
- 交付进 `_deliver/`；联邦库 `federation.py load --book ppy` + kb-mcp drift 体检（契约线后续步骤，开工时执行）。
