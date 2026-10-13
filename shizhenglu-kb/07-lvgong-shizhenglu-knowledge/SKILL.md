---
name: lvgong-shizhenglu-knowledge
description: 《吕公实政录》知识工程实例 skill——按已确认方案执行：底座（卷→条目指纹库）→ 启用层逐层抽取（实体/规则/结构化）→ 跨层整合 → 交付可查询、可溯源、可重跑的知识资产与报告。当用户需要处理/研读/查询《吕公实政录》《实政录》吕坤政书、把这本书做成知识库、或基于本实例继续补充数据时使用。由 book-knowledge-factory 实例化，方案与格式契约已与用户确认，直接执行即可，无需重新设计层。
---

# 《吕公实政录》知识工程规范（书实例 skill）

> 由 book-knowledge-factory 实例化：2026-10-12 确认方案；按 `docs/新书开工流程.md` Step 0 查契约（tools/book-mcp）后固化契约台账。通用方法论见工厂 `../../Skills/00-book-knowledge-factory/references/`；本实例只保留该书特有的内容，独立可执行。

## 0. 研读目标与口径（已确认）

| 项 | 选择 |
|---|---|
| 研读目标 | 知识抽取 + 建库查询（把吕坤政令条文转成可查询、可溯源、可重跑的知识资产） |
| 粒度 | 条目级：111 个 ○/△ 标题条目 + 8 个卷级条目（3 序引卷 + 乡甲约 5 个无标题卷）= **119 条**；正文"一……"条款不单独编号（保留在条目原文内） |
| 判定方式 | AI 逐条判定 + 代码验缺漏（触发词引擎只作候选，不作结论） |
| 交付形态 | JSON + 汇总报告 + 跨层 CSV（Excel 直接打开） |
| 启用层 | L0 底座 / L1 实体 / L2 规则 / L4 结构化（ACT·FRD·LGR·TME 四维）/ 跨层索引 |
| 翻译 | **不建 TRL 层**（用户明确：已有白话文译本）。白话文合并版随实例存放，作**对照引用源**——未来需要译文时从该文件按条目对应引用，不新增翻译数据 |

## 0.1 引导式反思记录（来源：工厂 Phase ②，本实例的源头）

> 只固化**结论与锁层依据**（下方三块）；探查/反思的完整过程与用户原话存工厂案例档 `../../Skills/00-book-knowledge-factory/references/case-feedback-lvgong-shizhenglu.md`，不进实例。后续增量的结论以增量条目**追加**在此，不重写历史。

**用户提出的方向**（第一输入，原话或要点）：
- "翻译就不用了，因为已经翻译好了，如果要做得话，直接引用白话文那版做翻译就行了" → 不建翻译层，白话文文件作引用源
- 层方案选"推荐方案（5 项）"；粒度选"仅条目级"；交付选"JSON+CSV（推荐）"
- "创建 skills 时要思考 MCP/契约" → 按 `docs/新书开工流程.md` Step 0 查契约，固化 C1–C7 台账（本实例 §0.2）

**层库参考与自定义征询**：展示 L0 底座 / L1 实体 / L2 规则 / L3 流程 / L4 结构化 / L5 事件 / C1 职官任职 / C5 翻译 / C11 奏疏互动 等候选（含 `python server.py layers` 22 项候选池），并附全书信号匹配说明。

**各层建/不建证据**（来源标注：用户提出 / 层库参考 / 自定义）：

| 层 | 来源 | 建/不建 | 理由与数据证据 |
|---|---|---|---|
| L0 底座 | 公共 | 建 | 必做：119 条锚点是全部层原文注入源 |
| L1 实体层 | 层库参考 | 建 | 官职/机构/簿册/刑罚/制度名词成体系：明职 26 条全为官职训谕；全书职官、衙署、簿册、罪名词密集 |
| L2 规则层 | 层库参考 | 建 | 规范句触发词密集（不许/务要/须/止许/责罚/限 N 日），全书"应当/禁止/程序"型条文为主体（民务、乡甲约、风宪约尤甚） |
| L3 流程层 | 层库参考 | 不建 | 用户选推荐方案未含流程层；本书操作程序（验尸/编甲/教学）有时序但散落，判"点不是线"，规则层可承载 |
| L4 结构化层 | 层库参考 | 建 | 四维证据：ACT 官职+乡约角色职责成体系（明职全卷+乡甲约）；FRD 官场积弊与防弊论述密集（库官之弊/快壮之弊/关防八条）；LGR 簿册台账成体系（乡甲四簿/格叶/状式 28 种/报政实单）；TME 期限成体系（保辜三日十日/会期/限期） |
| L5 事件层 | 层库参考 | 不建 | 政书条文体，非叙事纪事体，无事件叙事密度 |
| C1 职官任职层 | 自定义参考 | 不建 | 本书讲"职"之职责而非"某人任某职"，任职表述零星，不成体系 |
| C5 古今翻译层 | 用户提出 | 不建 | 用户明确不建，白话文版已存在，作引用源 |
| C11 奏疏互动层 | 自定义参考 | 不建 | 有"本院""奉旨"字样但非君臣往来互动链体例 |
| 跨层索引 | 公共 | 建 | 启用 ≥2 层必做 |

**确认结论**：用户拍板——推荐方案 5 项（L0+L1+L2+L4 四维+跨层索引）、仅条目级（119 条）、JSON+CSV、不建翻译层。锁层即按此执行，无需再设计。

## 0.2 本书契约台账（来源：docs/新书开工流程.md Step 0，tools/book-mcp 实查）

| 契约 | 本书的决定 | 状态 |
|---|---|---|
| C1 目录 | **内含式**：skill 与工程同仓同版本——实例 `shizhenglu-kb/07-lvgong-shizhenglu-knowledge/`，工程数据（`_source/_extract/_src/_layers/_build/_validate/_deliver/`）在 `shizhenglu-kb/` 根；交付目录只叫 `_deliver/` | ✅ 定 |
| C2 ID | item_id = `NN-NNN`（卷-序）全书唯一；prefix_registry：`ent→ENT-`、`rule→RULE-`、`struct 四维→ACT-/FRD-/LGR-/TME-`；前缀全局唯一、禁止跨层占用 | ✅ 定 |
| C3 底座 | `_item_registry.json` 扁平 dict `{item_id: {original, norm}}`，原文唯一源只入不出；`_src/` AI 源数据**绝不手抄原文**，original 由打包器注入 | ✅ 定 |
| C4 层 | 启用层：`ent`/`rule`/`struct`（layer_key=目录名，snake_case 单数无别名）；`_layers/ent/`、`_layers/rule/`、`_layers/struct/`；schema_fields/enum_fields 见 `references/schemas.md` §2 登记表 | ✅ 定 |
| C5 枚举 | 单点 `_kg_enums.py`（shizhenglu-kb 根）：ENTITY_TYPES 20 值 + RULE_TYPES 7 值继承基准库快照，ACT_TYPES/FRD_TYPES/LGR_TYPES/TME_TYPES 本书归纳（封闭+兜底）；打包器只从它读、未注册值记 ERR 不静默放行 | ✅ 定 |
| C6 产物 | 层 JSON 必填字段按 §2 登记 schema_fields 校验完整性；`_kg_join.json` + `_kg_join_flat.csv` 必建；交付物统一进 `_deliver/` | ✅ 定 |
| C7 元数据 | frontmatter `name: lvgong-shizhenglu-knowledge` == 目录 slug 部分；登记工厂 `references/registry.md` | ✅ 定 |

## 1. 执行流程总览

按**四段式**执行（`docs/新书开工流程.md` §8），每阶段收尾对照工厂 `../../Skills/00-book-knowledge-factory/references/checklists.md`：

```
① build_base.py（切卷切条 → _extract/ + _item_registry.json）
→ ② _src/ 装填（AI 逐条：只写条号 + 解读字段，绝不手抄原文）
→ ③ build_<layer>.py（打包：ID 分配 / 归一 / 枚举硬校验 / 从指纹库注入 original）
→ ④ build_kg_join.py + validate_layers.py（跨层索引 → 校验 → _deliver/）
```

## 2. 底座（C3，公共地基，先做）

1. 输入文件：`assets/sources/吕公实政录_原文_全卷合并.txt`（**唯一权威来源**，随实例存放；底本为明·吕坤《实政录》，合并文本按原书顺序：明职序引及卷一、民务卷二至四、乡甲约卷一至六、风宪约序及卷一至二；与工程目录 `shizhenglu-kb/原文/` 同源）。外部资料只作内容性质/学术定位辅助，不作条目抽取依据。
2. 白话文对照引用源：`assets/sources/吕公实政录_白话文_全卷合并.txt`（与原文结构一一对应：15 卷 ◆ 标题、111 个 ○/△ 标题一致）。**不作抽取依据**，仅在需要译文时按条目对应引用（`_baihua_map.json` 维护 item_id→白话文段落）。
3. 章节划分：**4 分部（明职/民务/乡甲约/风宪约）× 15 卷**，卷号按原书顺序直接映射（卷号表见 `references/schemas.md` §1，序/引卷=01/02/13，卷级条目=NN-001）。
4. 条目切分（仅条目级）：
   - **标题条目**：正文 `○`/`△` 开头的标题行，每个标题与其后正文（至下一标题或卷尾）为一条；
   - **卷级条目**：无 ○/△ 标题的卷（明职序、明职引、风宪约重刊序、乡甲约卷一/三/四/五/六），整卷为一条（含"计开"后条件列表，不单独编号）；
   - 产出 `_extract\NN_卷名.txt`（格式 `条N|正文`），预计 **119 条**；`（卷首篇目）`、`（正文）` 等结构性标注行不进入条目正文，仅作切分参考。
5. 指纹库 `_item_registry.json`：`{item_id: {original, norm}}`；**norm 归一规则**：繁体/异体字归一为规范简体（廵→巡、飬→养、枽→桑、貯→贮），缺字/□ 保留原形，不臆补；标点按现代句读归一。
6. 全部条目建 task 清单（阶段可见、完成可核）。
7. **业务 ID 由打包器自动分配**：AI 源数据只写卷内顺序槽位，不手写业务 ID；打包器按「卷号 × 段容量 +1」段位分配，段容量默认 500（C2）。
8. **写盘与并行纪律**：写文件一律「临时文件 + rename 落盘」；共享汇总文件统一增量合并语义（`--volumes` 只重算请求卷、合并写回）；验证脚本写文件输出，不依赖 stdout。

## 3. 实体层方案（ent，启用）

- layer_key=`ent`，前缀 `ENT-`，目录 `_layers/ent/`；schema_fields = `ent_id, item_id, text, type, start, end, normalized, confidence, source`；enum_fields = `type`。
- 实体类型枚举（**继承基准库快照 → 落 `_kg_enums.py`**，封闭 + 兜底"unknown"）：本书实际启用子集 = `person / official / institution / place / era / work / doc / system / behavior / punishment / time / quantity / unknown`（object/animal/plant/food/star/event/posthumous 本书无成体系证据，不启用，但保留在单点文件中作封闭全集）。
- 种子词典规则：全文本内生（词条必须出现在原文，否则自动剔除）；种子来源：明职官职名（吏承/仓官/廵检/驿递/税课司/司狱官/库官/教官/知州知县/同知通判推官/知府/盐运司/守廵道/提学道/按察司/布政司/督抚等）、乡约角色（约正/约副/约讲/约史/甲长/保正/保副/四邻）、司法角色（掌印官/问官/承委官/仵作/快壮/皂隶/吏书）、簿册文书（见 LGR）、刑罚（杖/笞/徒/流/绞/斩/枷号/充军）、机构（州县/府/按察司/布政司/都察院/巡按/保甲/乡约/社学/预备仓/社仓/申明亭/旌善亭）。
- 归一规则：异体/繁体→简体（同底座 norm）；同义复合词形（"把门皂隶"→皂隶）用 alias_index 手工映射，不动标注。
- 主键表：ENT-001..N + alias_index（词形 → ent_id）。

## 4. 规则层方案（rule，启用）

- layer_key=`rule`，前缀 `RULE-`，目录 `_layers/rule/`；schema_fields = `rule_id, item_id, type, modals, condition, subject, subject_ent_ids, action, object, purpose, punishment, original, confidence`；enum_fields = `type`。
- 触发词表（候选引擎，AI 逐条复核）：`不许 / 不得 / 务要 / 须 / 止许 / 只许 / 许 / 毋 / 勿 / 禁 / 禁约 / 严禁 / 责罚 / 重责 / 枷号 / 挐问 / 访察 / 参降 / 革役 / 限 N 日 / 不过 N 日 / 违者 / 犯者 / 依律 / 定行`。
- 规则类型枚举（**继承基准库快照 → `_kg_enums.py` RULE_TYPES 7 值**）：禁止型 / 义务型 / 允许型 / 程序型 / 时限型 / 处罚型 / 优先级型。
- **组合规则口径（定死）**：一条规范句 = 一个规则单元，type 取行为规范的主模态；"违者/犯者……"处罚并入同条 punishment 槽位，不单拆处罚型；一句话并列多个独立行为规范（"一不许X 二不许Y"型）拆多条共享 item_id；一句多模态（如"许X 但限 N 日"）type 取约束更强的一方。
- 明职训谕体处理：整篇为"职责要求"体，逐规范句抽规则；纯说理/劝诫句（"呜呼""嗟夫"引出的议论）不抽规则。

## 5. 结构化层方案（struct，启用，四维）

- layer_key=`struct`，目录 `_layers/struct/`；维度 ID 前缀（C2 登记，全局唯一）：`ACT-` / `FRD-` / `LGR-` / `TME-`；schema_fields = `struct_id, item_id, dim, …(维度字段), target, evidence, original, confidence`；enum_fields = `dim` + 各维度类型字段。
- 维度与对象：

| 维度 | 前缀 | 本书中的对象 | 类型枚举（本书归纳 → `_kg_enums.py`，封闭+兜底"其他"） |
|---|---|---|---|
| 角色-职责网络 | ACT | 官职职责（明职 26 条全部）、乡约体系角色（约正/约副/约讲/约史/甲长/保正/保副/四邻）、司法刑狱角色（掌印官/问官/承委官/仵作/快壮/皂隶/牢头狱霸）、文书角色（书手/吏书） | ACT_TYPES：官职 / 乡约角色 / 司法刑狱角色 / 文书角色 / 其他 |
| 防弊/风险机制库 | FRD | 官场积弊（仓官之弊/库官吏之弊三/快壮之弊/驿递之弊等）、防弊措施（廉生威/关防八条/隔别细审/四不扶同甘结）、负面机制（买尸做伤/卖放/窝主）、恶风当戒者十 | FRD_TYPES：积弊 / 防弊措施 / 恶风禁忌 / 其他 |
| 文簿台账体系 | LGR | 簿册（纪善簿/纪恶簿/纪和簿/纪改簿/进德簿/修业簿/卯簿）、格叶（乡甲格叶/善恶格叶）、状式（告辜式/告检式/告盗情状式等 28 种）、榜牌（旌善亭/申明亭/竖牌）、单据（保状式/丁引/审失单/报政实单/和事牌）、榜文（教民榜文） | LGR_TYPES：簿册 / 格叶 / 状式 / 榜牌 / 单据 / 其他 |
| 时间制度 | TME | 期限（保辜三日/十日、限 N 日）、会期（每月初二/十六）、考绩期（三年/六年/九年/十二年、双月一查、三考）、季节规定（麦忙/秋忙放会、十月后三月前操练） | TME_TYPES：期限 / 会期 / 考绩期 / 节令农时 / 年龄时限 / 其他 |

- target 用 ID 引用而非文本（角色/簿册/时间引用 ENT 主键或 struct 自身 ID）。

## 6. 跨层整合（kg_join，必建）

- ID 对齐审计点：实体主键唯一 / 引用槽位合法 / item_id 全回填（119 条全覆盖）/ target 用 ID / 枚举口径一致。
- 跨层索引：`_kg_join.json` + `_kg_join_flat.csv`（每行 = 一条目）：`item_id / volume / source / rules / structs / ents / layer_count`（本书无 L3/L5，槽位按启用层裁剪）。
- 枚举治理（C5）：单点 `_kg_enums.py` + registerVersion（新增值 version+1 回溯存量）；校验用**「收集-报告-暂存」**模式，未匹配值入 pending 表不中断，收尾统一决议；改值须双写 `enum-changelog.md`。

## 6.5 治理组件（默认启用）

- **V2 人工校验闭环**（layer_key=`review`）：同名异人/存疑判定（如官职异名、复合词形）自动收集入"待核清单"CSV（含 provenance），人工核前不强行合并（宁建勿并），核后回写。
- **V3 枚举校准**（layer_key=`enum_calib`）：执行期未匹配枚举值 → 收集-报告-暂存 → 收尾决议（新增/归并/改名）→ registerVersion+1 → 回溯存量；新增值必须有实例证据。

## 7. 管线与验证（四段式）

- 工程根：`shizhenglu-kb/`（与实例同目录，内含式）。
- 命令序列（从工程根执行）：
  - `python build_base.py` —— ① 底座：切卷切条 → `_extract/` + `_item_registry.json`
  - `python annotate.py --expect "01:1,02:1,03:26,04:13,05:8,06:14,07:1,08:6,09:1,10:1,11:1,12:1,13:1,14:35,15:9"` —— 底座自校验（可选）
  - `python build_ent_keys.py --volumes NN` —— 实体层（含主键表）
  - `python build_rules.py --volumes NN` —— 规则层
  - `python build_struct.py --volumes NN` —— 结构化层
  - `python build_kg_join.py --volumes NN` —— 跨层整合
  - `python validate_layers.py` —— 校验（`_validate/` 缺漏清单 ERR=0/GAP=0 才算过）
  - `python run_all.py [--volumes NN]` —— 全量 / 单卷幂等重跑
- **键名约定**：各层产物顶层键统一 `records`；打包器内建源数据键名映射表（SRC_KEY），源数据键名与打包容器键分处声明；`_src/` 只写条号 + 解读字段（C3）。
- 验证：每层"验证缺漏清单.txt"问题数 = 0（实体未归一 / 规则缺 item_id / struct target 悬空 / item_id 未全回填等）；区分结构性错误 ERR 与执行缺口 GAP；验证脚本写文件输出，不依赖 stdout；未注册枚举值记 ERR 不静默放行（C5）。

## 8. 交付清单

- 交付物统一进 `_deliver/`（C1）。
- 按层聚合交付（每层一组：归一汇总 + 验证清单 + 卷示例 + 跨层索引），≤6 组。
- 《使用报告》：快速查询（跨层 CSV 一行全看 / 实体主键反查 / 各层归一汇总）、全文回查溯源（指纹库）、白话文对照引用（`_baihua_map.json`）、可重跑管线、扩展指南（模板见 `assets/templates/usage_report_template.md`）。
- 《项目总结报告》：时间线、反思、根因、方法论沉淀、缺口与建议（模板见 `assets/templates/project_summary_template.md`）。
- 交付物按环境可用方式交付（本地文件路径或打包视图），说明验证方式、覆盖范围与仍存在的缺口。

## 9. 缺口与边界（执行中持续更新）

| 缺口 | 现状 | 补法 |
|---|---|---|
| 卷之四/卷之五（乡甲约格叶） | 执行时核对"计开"条件是否需拆分引用 | 按需补结构化记录 |
| 原文缺字/异体 | 保留原形入 norm，标注待核 | 人工校验闭环回填 |
| 状式 28 种细节 | 执行时逐式核对字段 | 按 LGR 登记 |

## 资源索引

- `references/schemas.md`：本实例启用层的 schema/枚举/ID/触发词/契约登记表 + **示例条目**（写源数据/打包器时读）
- `assets/sources/吕公实政录_原文_全卷合并.txt`：原文（唯一权威来源，随实例存放）
- `assets/sources/吕公实政录_白话文_全卷合并.txt`：白话文对照引用源（不参与抽取）
- `assets/templates/usage_report_template.md`：《使用报告》母版（交付阶段用）
- `assets/templates/project_summary_template.md`：《项目总结报告》母版（交付阶段用）
- 格式契约：`../../tools/book-mcp/`（`python server.py list / layers / enums`；contract.json 唯一真源）
- 通用方法论/检查单/坑：见工厂 `../../Skills/00-book-knowledge-factory/references/`（methodology.md / checklists.md / pitfalls.md / enum-library.md）
