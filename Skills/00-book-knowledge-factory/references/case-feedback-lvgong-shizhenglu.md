# 《吕公实政录》实例案例反馈（case-feedback）

> 来源：book-knowledge-factory 实例化《吕公实政录》（07-lvgong-shizhenglu-knowledge），2026-10-12。
> 本文件存**探查/反思过程与用户方向原话**；实例 SKILL.md 只固化结论。候选新层/新坑/新枚举见 `pending-review.md` 待评审区。

## 1. 用户方向原话（第一输入）

- 初始："[book-knowledge-factory] 帮忙创建一个技能，用来解析 E:\git\ToolBox\guji\shizhenglu-kb\原文\吕公实政录_原文_全卷合并.txt 的，翻译就不用了，因为已经翻译好了，如果要做得话，直接引用白话文那版做翻译就行了"
- 澄清（interaction_ask 回答）：层方案=推荐方案（5 项）；粒度=仅条目级；交付=JSON+CSV（推荐）
- 中途纠偏："我帮你查看最新的skills……要先读 E:\git\ToolBox\guji 里的 readme，用这个版本的00的那个skills工厂为准……1.删掉目前的skills，2.以最新的skills指导为准，再创建一次skills"
- 进一步要求："阅读 readme，里边有使用 mcp 的方法介绍，你在创建 skills 的时候，要思考这个问题"

## 2. 探查发现摘要

- 《吕公实政录》明·吕坤撰，万历朝政书（官箴）；4 分部（明职/民务/乡甲约/风宪约）× 15 卷 × 119 条（111 个 ○/△ 标题条目 + 8 个卷级条目：3 序引卷 + 乡甲约 5 个无标题卷）。
- 分部形态：明职=职官训谕体；民务=民政条款体（"一…"密集）；乡甲约=乡约保甲操作条文（会规/格叶/和处/改过/编甲）；风宪约=刑狱监察（提刑五十二款/按察二十款/状式 28 种/宪纲十要）。
- 白话文合并版与原文结构一一对应（15 卷 ◆ 标题、111 个 ○/△ 标题一致），可作引用对照源。

## 3. 反思与锁层过程

- 第 1 轮：AI 汇报探查发现 + 展示层库候选（L0–L5/C1/C5/C11）+ 请用户拍板 → 用户选"推荐方案 5 项"。
- AI 补证据：L1 实体（官职/机构/簿册/刑罚成体系）；L2 规则（规范句触发词密集）；L4 四维（ACT 官职乡约角色 / FRD 积弊防弊 / LGR 簿册状式 / TME 期限会期）；L3 流程/ L5 事件 / C1 职官任职 / C11 奏疏互动 判不建（政书条文体、讲"职"不讲"人任职"、非互动链体例）；C5 翻译不建（用户明确，白话文作引用源）。
- 确认结论：L0+L1+L2+L4（ACT·FRD·LGR·TME）+ 跨层索引；仅条目级（119 条）；JSON+CSV；不建翻译层。

## 4. 两次实例化的纠偏记录（重要过程）

1. **第一版（旧路径）**：按 `.user_skills/book-knowledge-factory`（无编号副本）实例化到 `.user_skills/05-lvgong-shizhenglu-knowledge`。
2. **用户纠偏**：仓库 `guji/README.md` 与 `Skills/00-book-knowledge-factory` 才是权威版本；且 README §6.6/`docs/新书开工流程.md` 规定第 7 本起必须走**契约线**（Step 0 先查 tools/book-mcp 的 C1–C7）。
3. **第二版（权威路径）**：
   - 删除 `.user_skills` 中旧工厂副本与旧实例（用户明确要求；删除时 SKILL.md 曾被占用，重试后成功）；
   - 按 `docs/新书开工流程.md`：Step 0 实查 `python server.py list / layers / enum --group ENTITY / RULE`，固化 C1–C7 契约台账（内含式、ENT-/RULE-/ACT-/FRD-/LGR-/TME- 前缀、`_kg_enums.py` 单点、`_deliver/`）；
   - 实例建到 **`shizhenglu-kb/07-lvgong-shizhenglu-knowledge/`（内含式）**，编号 07（README 预留 06 予《新官轨范》补实例）；
   - 试点 5 条（仓官之职/振举医学/乡甲至要/人命十二款/告盗情状式）schema 校验通过，示例固化进实例 `references/schemas.md`。

## 5. 候选经验（已入 pending-review.md 待评审）

| 类型 | 内容 | 理由 |
|---|---|---|
| 坑·切分纪律 | 卷首篇目与正文标题同名重复 → 以正文 ○/△ 行为准 | 政书/类书普遍；跨书可复用 |
| 坑·实例落盘环境 | `.user_skills`（workspace）对 `NN-` 前缀目录名剥离/还原 → 实例建到 git 仓库内 | 影响后续实例化落盘选择；环境相关但通用 |
| 方法·契约线 | 第 7 本起 Step 0 先用 tools/book-mcp 拉层/枚举种子再锁层，schema 与枚举直接从契约获取，避免"事后补格式" | 本实例首个完整落实；对后续新书是必走流程 |

## 6. 全量执行结果（2026-10-12 收尾）

- **状态**：全量执行完成——15 卷 × 4 层（L1/L2/L4 四维）+ 跨层索引；`validate_layers.py` 验收闸门 **ERR=0 / GAP=0**。
- **规模**：底座 119 条（01-001..15-009）；ent 651 标注 / 573 唯一实体（ENT-0001..0573）；rule 664 条；struct 235 条（ACT 56 / FRD 72 / LGR 77 / TME 30）；`_kg_join.json` 119 条全回填（layer_count 3=76 / 2=37 / 1=2 / 0=4）。
- **执行期踩坑（已入 pending-review 待评审）**：① 卷14/15 规则源文件多段 Write 整体覆盖（55→5 / 67→17），重读原文一次写全修复；② 卷09–12 曾共用 09 源文件（拆独立文件）；③ struct 维度类型字段必填枚举，卷05 错值 / 卷15 漏写均导致静默丢条；④ 全量缺省模式 `parse_volumes` 返回 None（修复为扫描 `_src` 推导卷号）。
- **MCP 契约线**：book-mcp selftest 20 项 / list C1–C7 / enum ENTITY 20+3 别名 / RULE 7 值，与 `_kg_enums.py` 一致；federation-mcp fed_conflicts（现库 243）/ fed_assoc identity_bridge 查"吕坤"空（六书无此人）——本书跨书查重待并入联邦库。
- **交付**：`_deliver\` 已出全量交付说明 / 使用报告 / 项目总结报告 / `kg_join_flat_全量.csv`（119 条）。白话文版全程仅作对照引用源，未建翻译层（用户口径）。
- **后续**：按开工流程 §9 移交存量线（kb-mcp 体检）；本书并入联邦库（kb.sqlite）后可跨书实体查重。

## 7. 移交 + 联邦库并入结果（2026-10-12 收尾）

- **联邦库并入**（用户要求"联邦库并入"）：`tools/kb-federation/` 新增 `adapters/lgs_adapter.py`（LgsAdapter：`_layers/<key>/<key>_NN.json` 子目录形态；ent 按 ent_id 跨卷去重 651→573；rule/struct 直取 rule_id/struct_id；fingerprints 读工程根 `_kg_join.json`），注册 `BOOK_ROOTS/NAMES/LAYERS/LAYER_DECL/BOOK_REGISTRY`（book_id=lgs）；`refs.py` REF_FIELDS 增 `subject_ent_ids`。跑 `load --book lgs`（items 119 / records 1472：ent 573 + rule 664 + struct 235，折叠 0）+ `transform`（nodes 18725 / canonicals 890 / members 4023）+ `refs`（4605 条引用边，resolved 3983 / ambiguous 218）。
- **跨书查重**：`fed_search 吕坤` → `lgs:ENT-0001`（exact_label 1.0，独立 canonical——六书无此人，符合预期）；conflict 323 含本书同名泛称职官（总兵/排年等 0.6 exact_normalized 待人工裁决）；"新吾先生"未命中（本书未标注该词形，正常）。
- **存量线移交**：`tools/kb-mcp/kb_mcp/registry.py` 登记 `shizhenglu-kb`（enum_backend=flat `_kg_enums.py`；globs `_layers/*/*.json`）；`adapters.py` `_TYPE_FIELDS` 增 `dim`（struct 维度类型字段）、`load_ent_keys` 候选路径增 `_global/ent_keys.json`。体检：`drift --book shizhenglu-kb` **漂移 0 层 / 库外 0 条**（ent ENTITY 11/20 正常、rule RULE 7/7 正常）；struct 层 235 条"无对应枚举定义"（工厂 enum-library 无 ACT/FRD/LGR/TME 段——本书四维归纳值已提案 pending-review 待评审入库，与新官轨范 struct 同类盲区）；sync 6 组比对：RULE 中英标签口径差、LGR/TME/ACT/FRD 工厂无段。
- **备份**：并入前已备份 `kb.sqlite` → `kb.sqlite.bak_20261012_lgs`。

## 8. 收尾：conflict 裁决 + struct 枚举评审入库（2026-10-12）

- **conflict 人工裁决**（用户要求"根据关系进行裁决"）：涉及 lgs 的 **89 条 conflict 全部为 official 类型**（职官概念实体：总兵/排年/检讨/巡抚/推官/主簿/守备/给事中等，非具体人名）。裁决依据：同一明代职官概念跨书同名 → 并簇语义正确（非"同名异人"）→ `lock` 保持并簇。`decide(action=lock)` 批量写入 89 + `replay_overrides` 重放：**overrides 89 / locked 89 / rejected 0 / split 0；conflict 323 → 234**（剩余 234 条为六书存量，不在本书范围）。审计留痕 `override_log`（decided_by=mcp-batch-lgs）。
- **struct 四维枚举评审入库**（用户要求"走评审入库"）：`enum-library.md` **v4 → v5**，新增 **§1.18 STRUCT 结构化四维**（5 顶层 + 子类树状：ACT 角色职责 5 / FRD 防弊风险 4 / LGR 文簿台账 6 / TME 时间制度 6 + 其他兜底）；`enum-changelog.md` 版本索引 + v5 条目（5.1 变更 / 5.2 判定依据 / 5.3 入库快照 / 5.4 待办）；`pending-review.md` 提案 →「已升级（用户 2026-10-12 确认入库）」去向 enum-library v5 §1.18。
- **护栏恢复验证**：kb-mcp `drift --book shizhenglu-kb` **三层全恢复**——ent ENTITY 651 条 11 种 正常(0.0%)；rule RULE 664 条 7 种 正常(0.0%)；**struct STRUCT 235 条 4 种 正常(0.0%)**；漂移 0 层、无基准 0 层、库外 0 条。`enum_list --scope factory --enum STRUCT` 解析 21 值；checklist STRUCT 兜底警告消除；selftest 全部通过。
- **已知口径差（登记不处理）**：sync 的 RULE 中英标签差（工厂中文标签 / 实例英文 key）与四维子类分组（工厂单段 STRUCT / 实例四组独立变量 ACT_TYPES 等）为标签映射口径，不属本书范围；《新官轨范》actor/fraud/ledger/time 子层可对照 §1.18 归一（v5 待办，走 xgf 侧增量）。

