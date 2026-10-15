---
name: pingpingyan-knowledge
description: 《平平言》知识工程实例 skill——按已确认方案执行：底座（卷→条目指纹库）→ 启用层逐层抽取（实体/规则/结构化四维/制度/论说）→ 跨层整合 → 交付可查询、可溯源、可重跑的知识资产与报告。当用户需要处理/研读/查询《平平言》、清·方大湜吏治官箴书、把这本书做成知识库、或基于本实例继续补充数据时使用。由 book-knowledge-factory 实例化（编号 12），方案与格式契约已与用户确认，直接执行即可，无需重新设计层。
---

# 《平平言》知识工程规范（书实例 skill）

> 由 book-knowledge-factory 实例化：2026-10-13 确认方案；按 `docs/新书开工流程.md` Step 0 查契约（tools/book-mcp）后固化契约台账。通用方法论见工厂 `../../Skills/00-book-knowledge-factory/references/`；本实例只保留该书特有的内容，独立可执行。

## 0. 研读目标与口径（已确认）

| 项 | 选择 |
|---|---|
| 研读目标 | 知识抽取 + 建库查询（把方大湜州县吏治言论与制度条文转成可查询、可溯源、可重跑的知识资产） |
| 粒度 | 条目级：**284 条**（卷一 84 / 卷二 87 / 卷三 43 / 卷四 70，正文 `○` 标题条目）；正文"一曰/一曰……"条款不单独编号（保留在条目原文内） |
| 判定方式 | AI 逐条判定 + 代码验缺漏（触发词引擎只作候选，不作结论） |
| 交付形态 | JSON + 汇总报告 + 跨层 CSV（Excel 直接打开） |
| 启用层 | L0 底座 / L1 实体 / L2 规则 / L4 结构化（ACT·FRD·LGR·TME 四维）/ REG 制度 / OPN 论说 / TRL 古今翻译（2026-10-14 增量）/ 跨层索引 / V2+V3 治理组件 |
| 翻译 | **TRL 已建**（2026-10-14 增量，推翻原"不建"口径）：`build_trl.py` 读 `白话文/卷一~卷四_白话.txt` 对照引用源整段入层 → `_layers/trl/`，284 条全覆盖，注释性翻译 |

## 0.1 引导式反思记录（来源：工厂 Phase ②，本实例的源头）

> 只固化**结论与锁层依据**（下方三块）；探查/反思的完整过程与用户原话存工厂案例档 `../../Skills/00-book-knowledge-factory/references/case-feedback-pingpingyan.md`，不进实例。后续增量的结论以增量条目**追加**在此，不重写历史。

**用户提出的方向**（第一输入，原话或要点）：
- "帮忙使用 E:\git\ToolBox\guji\Skills\00-book-knowledge-factory，这个技能，对平平言这本书进行提炼 skills"（书名即《平平言》，书在 `pingpingyan-kb/原文`）
- interaction_ask 拍板：层方案选"**规则型 7 层（推荐）**"（底座 + L1 实体 + L2 规则 + L4 四维 + REG 制度 + OPN 论说 + 跨层索引，不含事件层）；工程对接选"**沿用契约线**"（docs/新书开工流程.md + tools/book-mcp + 联邦库 federation.py + kb-mcp）

**层库参考与自定义征询**：展示 L0 底座 / L1 实体 / L2 规则 / L3 流程 / L4 结构化 / L5 事件 / REG 制度 / OPN 论说 / DOC 文书 / REL 角色关系 / CIT 引书 候选，附全书信号匹配说明（密度统计见 case-feedback）。

**各层建/不建证据**（来源标注：用户提出 / 层库参考 / 自定义）：

| 层 | 来源 | 建/不建 | 理由与数据证据 |
|---|---|---|---|
| L0 底座 | 公共 | 建 | 必做：284 条锚点是全部层原文注入源 |
| L1 实体层 | 层库参考 | 建 | 人物（方大湜/吕坤/汪辉祖/刘衡/袁守定/朱桓/蓝鼎元/杜贵墀等）、书名（会典/律例/洗冤录/学治臆说/庸吏庸言/福惠全书/折狱龟鉴等）、职官吏役（州县/佐杂/幕友/门丁/书差/保正/绅士/跟班）、地域（广济/襄阳/武昌/荆州/宜昌/江陵/监利/鹤峰等）成体系 |
| L2 规则层 | 层库参考 | 建 | 规范句触发词密集（不可/不许/不得/切勿/宜/须/务必/严禁/限 N 日/违者/犯者），全书"应当/禁止/程序/时限"型条文为主体（凡例自述"但求可行……件系条分"） |
| L3 流程层 | 层库参考 | 不建 | 用户选规则型 7 层未含；舆图绘制/保甲编查/清查命盗等有步骤链但散落于条目叙事，判"点不是线"，规则层程序/时限型可承载 |
| L4 结构化层 | 层库参考 | 建 | 四维证据：ACT 官民胥役角色职责成体系（州县/佐杂/幕友/门丁/书差/保正/绅士/家丁）；FRD 防弊与积弊论述密集（门丁十弊/保甲四难/陋规/亏空/官价/私宰包庇）；LGR 簿册台账成体系（须知册/舆图/钱粮实征底册/四簿/流水总簿/门牌/交代二摺/券根/回批/领状）；TME 期限会期成体系（正五九月/四绝四离/审限参限/旌表年限/三年大计） |
| L5 事件层 | 层库参考 | 不建 | 用户拍板规则型 7 层未含；前代故事+亲历案例约 40+ 处但为说理引证（法戒），非纪事主线，判"点不是线" |
| REG 制度层 | 层库参考 | 建 | 制度条文成片（公罪私罪抵销则例/大计/旌表则例/保甲/仓谷霉烂例/钱粮/交代/礼部则例/会典事例），卷四尤甚 |
| OPN 论说层 | 层库参考 | 建 | 作者按语与引论密集（"余令广济凡五年……""余篆襄阳县事……"亲历按语 + 引吕新吾/汪龙庄/刘簾舫/袁易斋/朱性齐/陈文恭等论说） |
| DOC 文书层 | 自定义参考 | 不建 | 文书式内容不密集（告示/详/禀多提及但无程式实例），密度不足，不单独建模 |
| REL 角色关系层 | 自定义参考 | 不建 | 人物关系以角色论说为主（非具体人物间直接证据关系），ACT 角色维度可承载 |
| CIT 引书层 | 自定义参考 | 不建 | 引书出现但以"应读之书目录 + 引论"为主，未成引用索引体系；书名归 L1 work 实体即可 |
| 跨层索引 | 公共 | 建 | 启用 ≥2 层必做 |

**确认结论**：用户拍板——规则型 7 层（L0+L1+L2+L4 四维+REG+OPN+跨层索引）、条目粒度（284 条）、JSON+CSV、不建翻译层（白话文对照源）、沿用契约线（未来可并入联邦库）。锁层即按此执行，无需再设计。

**2026-10-14 增量（TRL 翻译层，推翻原"不建"口径）**：用户要求"把白话文写入 trl 层"。新增 `build_trl.py`：读分卷白话对照源（`白话文/卷一~卷四_白话.txt`），按 ○ 标题顺序与指纹库硬校验对齐（条目数=翻译数=284，标题零差异），产出 `_layers/trl/trl_NN.json` + `trl_summary.json` + `全书白话译本/*.md`；trl_id = `TRL-<卷NN><条NNN>`（可由 item_id 还原）；`_kg_enums.py` 增 `TRL_STYLES`；`validate_layers.py` 纳入 trl 校验（字段/风格枚举/id 规则/original+norm 注入/翻译覆盖，TRL 未打包报 GAP，不受 `--skip-baseline` 豁免）。§9"白话文对照映射未建"缺口由本层关闭，`_baihua_map.json` 计划废止（译文即 TRL 记录）。

## 0.2 本书契约台账（来源：docs/新书开工流程.md Step 0，tools/book-mcp 实查）

| 契约 | 本书的决定 | 状态 |
|---|---|---|
| C1 目录 | **内含式**：skill 与工程同仓同版本——实例 `pingpingyan-kb/12-pingpingyan-knowledge/`，工程数据（`_extract/_src/_layers/_build/_validate/_deliver/`）在 `pingpingyan-kb/` 根；交付目录只叫 `_deliver/` | ✅ 定 |
| C2 ID | item_id = `NN-NNN`（卷-序）全书唯一；prefix_registry：`ent→ENT-`、`rule→RULE-`、`struct 四维→ACT-/FRD-/LGR-/TME-`、`reg→REG-`、`opn→OPN-`；前缀全局唯一、禁止跨层占用 | ✅ 定 |
| C3 底座 | `_item_registry.json` 扁平 dict `{item_id: {original, norm}}`，原文唯一源只入不出；`_src/` AI 源数据**绝不手抄原文**，original 由打包器注入 | ✅ 定 |
| C4 层 | 启用层：`ent`/`rule`/`struct`/`reg`/`opn`（layer_key=目录名，snake_case 单数无别名）；schema_fields/enum_fields 见 `references/schemas.md` §2 登记表 | ✅ 定 |
| C5 枚举 | 单点 `_kg_enums.py`（pingpingyan-kb 根）：ENTITY_TYPES 20 值 + RULE_TYPES 7 值继承基准库快照，ACT/FRD/LGR/TME 四维继承 lgs/xzl 快照，REG_TYPES 政书英文键 10 值（基准库 v6），OPN_STANCES 5 值；打包器只从它读、未注册值记 ERR 不静默放行 | ✅ 定 |
| C6 产物 | 层 JSON 必填字段按 §2 登记 schema_fields 校验完整性；`_kg_join.json` + `_kg_join_flat.csv` 必建；交付物统一进 `_deliver/` | ✅ 定 |
| C7 元数据 | frontmatter `name: pingpingyan-knowledge` == 目录 slug 部分（`12-pingpingyan-knowledge`）；登记工厂 `references/registry.md` | ✅ 定 |

## 1. 执行流程总览

按**四段式**执行（`docs/新书开工流程.md` §8），每阶段收尾对照工厂 `../../Skills/00-book-knowledge-factory/references/checklists.md`：

```
① build_base.py（切卷切条 → _extract/ + _item_registry.json）
→ ② _src/ 装填（AI 逐条：只写条号 + 解读字段，绝不手抄原文）
→ ③ build_<layer>.py（打包：ID 分配 / 归一 / 枚举硬校验 / 从指纹库注入 original）
→ ④ build_kg_join.py + validate_layers.py（跨层索引 → 校验 → _deliver/）
```

## 2. 底座（C3，公共地基，先做）

1. 输入文件：`assets/sources/平平言_原文_全卷合并.txt`（**唯一权威来源**，随实例存放，UTF-8；底本为清·方大湜《平平言》，本工程存 4 卷：卷一 84 条 / 卷二 87 条 / 卷三 43 条 / 卷四 70 条，序/凡例/跋按原书顺序并入合并版）。**卷拆分 txt（`assets/sources/卷一.txt`~`卷四.txt`）为切分主源**，合并版作交叉校验（逐条对账）。外部资料只作内容性质/学术定位辅助，不作条目抽取依据。
   - ⚠️ 编码备忘：工程根 `pingpingyan-kb/原文/平平言_原文_全卷合并.txt` 为 **GBK 编码**（Windows 直读乱码）；本实例内所有源文件已统一 **UTF-8**（`scripts/prepare_sources.py` 可重跑）。原 GBK 文件仅作底本参照。
2. 白话文对照引用源：`assets/sources/平平言_白话文_全卷合并.txt`（UTF-8，与原文结构对应）。**不作抽取依据**，仅在需要译文时按条目对应引用（`_baihua_map.json` 按需维护 item_id→白话文段落）。
3. 章节划分：**4 卷**，卷号按原书顺序直接映射（01 卷一=立志修身与到任 / 02 卷二=衙门管理与事上同寅 / 03 卷三=刑名听讼 / 04 卷四=教化风化·钱粮·荒政·旌表·交代；卷号表见 `references/schemas.md` §1）。**序/凡例/跋为版本说明卷（00），不进入条目库**（用户口径：底座 = 正文 284 条）。
4. 条目切分（仅条目级）：
   - **标题条目**：正文 `○` 开头的标题行，每个标题与其后正文（至下一标题或卷尾）为一条；`○` 与正文之间空一格（`○造福莫如州縣` 为标题本身，正文自标题行后）；
   - 卷首标题清单行（卷一~四卷首无 `○` 的标题列表）**不计数**、不进入条目正文，仅作切分参考与逐条对照（正文 `○` 数 = 标题清单行数，差值即条内注/缺漏）；
   - 产出 `_extract\NN_卷名.txt`（格式 `条N|○标题|正文`），预计 **284 条**（卷1=84/卷2=87/卷3=43/卷4=70）。
5. 指纹库 `_item_registry.json`：`{item_id: {original, norm}}`；**norm 归一规则**：繁体/异体字归一为规范简体（厯→历、廵→巡、覈→核、曡→叠、賸→剩、衞→卫、嚮→向、註→注），缺字/`■〈…〉` 保留原形不臆补，标点按现代句读归一（`【 懋】` 型注音/夹注括注归一为 `〔懋〕` 或保留 `【懋】` 视底本统一，执行期定死一种并记录）。
6. 全部条目建 task 清单（阶段可见、完成可核）。
7. **业务 ID 由打包器自动分配**：AI 源数据只写卷内顺序槽位，不手写业务 ID；打包器按「卷号 × 段容量 +1」段位分配，段容量默认 500（C2）。
8. **写盘与并行纪律**：写文件一律「临时文件 + rename 落盘」；共享汇总文件统一增量合并语义（`--volumes` 只重算请求卷、合并写回）；验证脚本写文件输出，不依赖 stdout。

## 3. 实体层方案（ent，启用）

- layer_key=`ent`，前缀 `ENT-`，目录 `_layers/ent/`；schema_fields = `ent_id, item_id, text, type, start, end, normalized, confidence, source`；enum_fields = `type`。
- 实体类型枚举（**继承基准库 §1.1 20 值快照 → 落 `_kg_enums.py`**，封闭 + 兜底"unknown"）：本书实际启用子集 = `person / official / institution / place / era / work / doc / system / behavior / punishment / time / quantity / unknown`（object/animal/plant/food/star/event/posthumous 本书无成体系证据，不启用，但保留在单点文件中作封闭全集）。
- 种子词典规则：全文本内生（词条必须出现在原文，否则自动剔除）；种子来源：人物（方大湜（菊人/方伯/夫子）、吕坤（吕新吾）、汪辉祖（汪龙庄）、刘衡（刘簾舫）、袁守定（袁易斋）、朱桓、蓝鼎元、杜贵墀（仲丹）、卞宝第、但湘良、刘燡、赵凤、李德裕、宋均、程明道、王文正、寇莱公 等）、职官吏役（州县/牧令/督抚藩臬道府/佐杂/幕友/门丁/书差/保正/绅士/绅耆/跟班/仵作/禁子/刑房）、书名（大清会典/会典事例/大清律例/洗冤录/处分则例/学治臆说/庸吏庸言/福惠全书/图民录/牧令书/佐治药言/折狱龟鉴/邸钞/海国图志 等）、地域（广济/襄阳/武昌/荆州/宜昌/江陵/监利/鹤峰/青州/成都/越州 等）、制度（钱粮/保甲/仓谷/旌表/交代/大计/考成/陋规/公罪/私罪）、文书（须知册/舆图/门牌/实征底册/交代二摺/告示/详/禀/甘结/保结）。
- 归一规则：异体/繁体→简体（同底座 norm）；同义复合词形（"门丁""门上""把门人役"→门丁；"汪龙庄明府"→汪辉祖）用 alias_index 手工映射，不动标注。
- **跨书对齐（重要）**：本书与《吕公实政录》《政学录》《福惠全书》同属政书/官箴书，吏治术语、幕友书名、律例则例名高度重叠——归一与主键表尽量对齐 lgs/xzl/fqh 词形（官箴术语/簿册名/则例名），联邦库并入时跨书查重价值高。
- 主键表：ENT-001..N + alias_index（词形 → ent_id）。

## 4. 规则层方案（rule，启用）

- layer_key=`rule`，前缀 `RULE-`，目录 `_layers/rule/`；schema_fields = `rule_id, item_id, type, modals, condition, subject, subject_ent_ids, action, object, purpose, punishment, original, confidence`；enum_fields = `type`。
- 触发词表（候选引擎，AI 逐条复核）：`不可 / 不许 / 不得 / 切勿 / 断不可 / 万不可 / 切不可 / 务必 / 必须 / 须 / 宜 / 宜须 / 禁 / 严禁 / 责 / 罚 / 限 N 日 / 不过 N 日 / 违者 / 犯者 / 依律 / 照例 / 例 / 着 / 应 / 当`。
- 规则类型枚举（**继承基准库快照 → `_kg_enums.py` RULE_TYPES 7 值，中文键**，与 lgs/xzl/fqh 一致）：禁止型 / 义务型 / 允许型 / 程序型 / 时限型 / 处罚型 / 优先级型。
- **组合规则口径（定死）**：一条规范句 = 一个规则单元，type 取行为规范的主模态；"违者/犯者……"处罚并入同条 punishment 槽位，不单拆处罚型；一句话并列多个独立行为规范（"一曰……二曰……"型）拆多条共享 item_id；一句多模态（如"许X 但限 N 日"）type 取约束更强的一方。
- 官箴体处理：戒条（"官不可貪""勿用门丁"等禁令）逐条抽规则；**纯说理/劝诫句（"呜呼/嗟夫"引出的议论）不抽规则**（归 OPN 论说层）；**亲历记事句（"余令广济凡五年……""余篆襄阳县事……"）不抽规则**（归 OPN/实体/FRD 承载）；制度沿革叙事（"旧例……后改……"）抽规则时取**现行有效**规范，历史演变说明不抽（归 REG evolution）。

## 5. 结构化层方案（struct，启用，四维）

- layer_key=`struct`，目录 `_layers/struct/`；维度 ID 前缀（C2 登记，全局唯一）：`ACT-` / `FRD-` / `LGR-` / `TME-`；schema_fields = `struct_id, item_id, dim, …(维度字段), target, evidence, original, confidence`；enum_fields = `dim` + 各维度类型字段。
- 维度与对象（**继承 lgs/xzl 归纳枚举快照 → `_kg_enums.py`**）：

| 维度 | 前缀 | 本书中的对象 | 类型枚举（继承快照，封闭+兜底"other"） |
|---|---|---|---|
| 角色-职责网络 | ACT | 官职（州县/牧令/佐杂/督抚藩臬）、吏役角色（幕友/门丁/书差/跟班/仵作）、乡保角色（保正/甲长/牌长/乡约）、士绅（绅士/绅耆）、家内角色（子弟/女眷/长随） | ACT_TYPES：official / justice_role / clerk_role / xiangyue_role / other |
| 防弊/风险机制库 | FRD | 积弊（门丁十弊/书差需索/保甲四难/陋规/官价/亏空/贪赃/私宰包庇/妇女烧香）、防弊措施（不恶而严/银钱兼收/四簿稽核/责成住持/官禁不如私禁/发放钱票）、恶风（奢华/嗜酒/溺女/私创寺庙/烧香聚众） | FRD_TYPES：abuse / guard / evil_custom / other |
| 文簿台账体系 | LGR | 簿册（须知册/钱粮实征底册/正入正出杂入杂出四簿/流水总簿/保甲册/门牌/交代二摺/券根/回批/领状）、图（舆图/开方计里图）、牌榜（门牌/告示）、单据（钱票/由单） | LGR_TYPES：ledger / geye / template_form / board / voucher / other |
| 时间制度 | TME | 期限（审限/参限/保辜/限 N 日）、考绩期（三年大计/卓异/六年）、旌表年限（15 年改 10 年改 6 年/幼女出家 40 岁）、时令禁忌（正五九月/四绝四离四不祥/月忌/农忙） | TME_TYPES：deadline / meeting / assessment / season / age_limit / other |

- target 用 ID 引用而非文本（角色/簿册/时间引用 ENT 主键或 struct 自身 ID）。

## 5.5 制度层方案（reg，启用）

- layer_key=`reg`，目录 `_layers/reg/`；ID 前缀 `REG-`（全局唯一）；schema_fields = `reg_id, item_id, name, type, content, evolution, target, original, confidence`；enum_fields = `type`。
- **定位**：制度本体静态描述登记（制度名 + 内容要点 + 沿革 + 出处）。与 L1 system 实体分工：L1 标制度**词**为实体；REG 记制度**条目级描述**。与 L4 分工：L4 从维度切片对象（角色/防弊/文簿/时限），REG 收制度本身。
- 制度类型枚举（**政书英文键分支 v6，10 值** → `_kg_enums.py` REG_TYPES）：`official_system 官制 / selection_assessment 铨选考课 / fiscal 财政赋役 / justice_prison 司法狱政 / baojia_xiangyue 保甲乡约 / education_sacrifice 文教祭祀 / military 军政 / post_transport 驿传运输 / governance 治理总纲 / other`。
- 执行口径：一条目含多个制度可拆多条共享 item_id；沿革要点（"旧例…后改…"）记 evolution 不另拆事件；content 写要点不抄原文（C3）；本书制度主题预估：官制考成（公罪私罪/抵销/大计/卓异/处分则例）、铨选（候补/缺分冲繁疲难/到任）、钱粮赋役（钱粮征收/银钱兼收/税契/交代/亏空追赔）、刑名狱政（命盗清查/审限参限/洗冤检验/私宰）、保甲乡约（保甲编查/门牌/连坐/十家牌）、文教祭祀（旌表节孝/义学/禁建寺庙/禁幼女出家）、荒政（仓谷/赈饥查户/平粜/流民/孤贫口粮）、教化风化（禁溺女/禁妇女烧香/禁烧香聚众）、驿递河工（驿站/河工/堤防）。

## 5.6 论说层方案（opn，启用）

- layer_key=`opn`，目录 `_layers/opn/`；ID 前缀 `OPN-`（全局唯一）；schema_fields = `opn_id, item_id, topic, stance, argument, evidence_refs, original, confidence`；enum_fields = `stance`。
- **定位**：作者直接议论/判断/评价 + 引述他人论说登记（"余谓/余令/余曰/吾邑"型作者按语 + "吕新吾先生曰""汪龙庄学治臆说云"型引论）。
- 立场枚举（**继承基准库 §1.8 5 值** → `_kg_enums.py` OPN_STANCES）：肯定 / 否定 / 怀疑 / 讽刺 / 中立。
- 执行口径：一条目论说句可多条共享 item_id；topic 取议论主题（如"官须自做""勿用门丁"）；argument **只写要点概要不抄原文**（C3）；evidence_refs 引用支持该论说的引书/人物实体（如引《学治臆说》时引用该 work ent_id）；stance 取作者对该议题的立场（引他人论说以支撑自己论点者，按作者本人立场记 stance）。

## 6. 跨层整合（kg_join，必建）

- ID 对齐审计点：实体主键唯一 / 引用槽位合法 / item_id 全回填（284 条全覆盖）/ target 用 ID / 枚举口径一致。
- 跨层索引：`_kg_join.json` + `_kg_join_flat.csv`（每行 = 一条目）：`item_id / volume / source / rules / regs / opns / structs / ents / layer_count`（槽位按启用层裁剪，本书无 L3/L5/DOC/REL）。
- 枚举治理（C5）：单点 `_kg_enums.py` + registerVersion（新增值 version+1 回溯存量）；校验用**「收集-报告-暂存」**模式，未匹配值入 pending 表不中断，收尾统一决议；改值须双写 `enum-changelog.md`。

## 6.5 治理组件（默认启用）

- **V2 人工校验闭环**（layer_key=`review`）：同名异人/存疑判定（如官职异名、人物字号与名对应、"某县"指代）自动收集入"待核清单"CSV（含 provenance），人工核前不强行合并（宁建勿并），核后回写。
- **V3 枚举校准**（layer_key=`enum_calib`）：执行期未匹配枚举值 → 收集-报告-暂存 → 收尾决议（新增/归并/改名）→ registerVersion+1 → 回溯存量；新增值必须有实例证据。

## 7. 管线与验证（四段式）

- 工程根：`pingpingyan-kb/`（与实例同目录，内含式）。
- 命令序列（从工程根执行）：
  - `python build_base.py` —— ① 底座：切卷切条 → `_extract/` + `_item_registry.json`
  - `python build_ent_keys.py --volumes NN` —— 实体层（含主键表）
  - `python build_rules.py --volumes NN` —— 规则层
  - `python build_struct.py --volumes NN` —— 结构化层
  - `python build_reg.py --volumes NN` —— 制度层
  - `python build_opn.py --volumes NN` —— 论说层
  - `python build_kg_join.py --volumes NN` —— 跨层整合
  - `python build_trl.py [--volumes NN]` —— 翻译层（白话文对照源整段入层，幂等）
  - `python validate_layers.py` —— 校验（`_validate/` 缺漏清单 ERR=0/GAP=0 才算过）
  - `python run_all.py [--volumes NN]` —— 全量 / 单卷幂等重跑
- **键名约定**：各层产物顶层键统一 `records`；打包器内建源数据键名映射表（SRC_KEY），源数据键名与打包容器键分处声明；`_src/` 只写条号 + 解读字段（C3）。
- 验证：每层"验证缺漏清单.txt"问题数 = 0（实体未归一 / 规则缺 item_id / struct target 悬空 / item_id 未全回填 / trl 翻译未覆盖或未打包等）；区分结构性错误 ERR 与执行缺口 GAP；验证脚本写文件输出，不依赖 stdout；未注册枚举值记 ERR 不静默放行（C5）。

## 8. 交付清单

- 交付物统一进 `_deliver/`（C1）。
- 按层聚合交付（每层一组：归一汇总 + 验证清单 + 卷示例 + 跨层索引），≤6 组。
- 《使用报告》：快速查询（跨层 CSV 一行全看 / 实体主键反查 / 各层归一汇总）、全文回查溯源（指纹库）、白话文对照引用（TRL 层 `_layers/trl/`，可读版 `全书白话译本/`）、可重跑管线、扩展指南（模板见 `assets/templates/usage_report_template.md`）。
- 《项目总结报告》：时间线、反思、根因、方法论沉淀、缺口与建议（模板见 `assets/templates/project_summary_template.md`）。
- 交付物按环境可用方式交付（本地文件路径或打包视图），说明验证方式、覆盖范围与仍存在的缺口。

## 9. 缺口与边界（执行中持续更新）

| 缺口 | 现状 | 补法 |
|---|---|---|
| 序/凡例/跋 | 版本说明卷（00），不进入条目库（用户口径 284 条） | 如需将凡例"体例自述"纳入抽取，增量加 00 卷条目 |
| 工程根 GBK 合并文件 | 底本参照；实例内统一 UTF-8（scripts/prepare_sources.py 已重合并） | 执行期一律读 `assets/sources/` 下 UTF-8 文件 |
| 前代故事/亲历案例（约 40+ 处） | 未建 L5 事件层（用户口径），由 OPN/FRD/实体承载 | 若后续需事件检索，走工厂增量升级流程加 L5 |
| 白话文对照映射 | ✅ 2026-10-14 已由 TRL 层关闭（`build_trl.py` 全量入层，284 条） | 译文查询走 `_layers/trl/`；`_baihua_map.json` 计划废止 |
| 原文缺字/异体/夹注括注 | 保留原形入 norm，标注待核 | 人工校验闭环回填 |
| 卷三内容形态 | 刑名听讼为主，执行时核对听讼类规则的条目边界 | 底座切分时核定 |

## 资源索引

- `references/schemas.md`：本实例启用层的 schema/枚举/ID/触发词/契约登记表 + **示例条目**（写源数据/打包器时读）
- `assets/sources/平平言_原文_全卷合并.txt`：原文（唯一权威来源，随实例存放，UTF-8）
- `assets/sources/卷一.txt`~`卷四.txt` + 序/凡例/跋：卷拆分切分主源（随实例存放，UTF-8）
- `assets/sources/平平言_白话文_全卷合并.txt`：白话文对照引用源（不参与抽取）
- `assets/templates/usage_report_template.md`：《使用报告》母版（交付阶段用）
- `assets/templates/project_summary_template.md`：《项目总结报告》母版（交付阶段用）
- `scripts/prepare_sources.py`：源文件准备/编码归一脚本（可重跑）
- 格式契约：`../../tools/book-mcp/`（`python server.py list / layers / enums`；contract.json 唯一真源）
- 通用方法论/检查单/坑：见工厂 `../../Skills/00-book-knowledge-factory/references/`（methodology.md / checklists.md / pitfalls.md / enum-library.md）
