---
name: progress-dashboard-integration
description: 各书籍项目进度如何被采集器识别并接入古集看板（Summary/html/dashboard.html）的操作规范，含每书目录最后更新时间的基线对比（last_seen.json）与「声明值 ↔ 盘上实测」归一门（collect_meta.js + check_summary.js）。当需要查哪些书籍项目有了更新、刷新看板进度数据（times.js/data.js）、把新书项目接入看板、核对 Summary 台账是否说假话、或诊断某书阶段时间/卷进度/层记录数为何采不到时使用。典型触发："刷新看板"、"更新进度"、"哪些项目有更新"、"把X接入看板"、"看板时间线缺某本书"、"数据对不对"。
---

# 进度采集接入看板（Progress Dashboard Integration）

## 定位与数据流

看板是**纯静态、离线（file://）消费四个数据文件**的 Vue3 单页；本技能只管"把各书项目的磁盘状态搬进这四个文件"，并保证搬进去的数字没有假话。

```
各书项目目录 ──(collect_times.js 扫描 mtime/卷文件)──▶ _collect_out.json ──(人工校准)──▶ times.js   ┐
        └────(collect_meta.js 实测三域)────▶ _meta_out.json ──┬──(check_summary.js 归一门)──▶ 报告 ERR/WARN/INFO
data.js（书目台账，手写，数字按门校准）                                                                  ├──▶ dashboard.html
stages.js（八段流程语义，手写，改流程才动）                                                                ┘
```

| 文件 | 性质 | 何时改 |
|---|---|---|
| `Summary/html/data.js` | 手写台账：每书 id/dir/title/status/stageStates/layers/notes/drift | 新书接入、层记录数变化、阶段推进 |
| `Summary/html/times.js` | 校准快照：GTIMES（前 7 阶段最后写入 ms）+ GVOLS（total/fill/pack/note） | 例行刷新（见下） |
| `Summary/html/stages.js` | GSTAGES：八段流程 {name,goal,mark,next,…}，书目/详情/时间线共用 | 仅流程定义本身变化 |
| `Summary/html/collect_times.js` | 采集器 V1：DIRS 映射 + 阶段分类正则（导出 DIRS/ROOT/walk 供其他脚本复用） | 新书接入 / 目录改名 |
| `Summary/html/collect_meta.js` | 采集器 V2：盘上实测三域（著录 C8 / 结构 C9 / 知识层）+ 联邦库对账，只读 | 书的目录几何变化 / 新增层件形态 |
| `scripts/check_summary.js` | 归一门：V2 实测 ↔ 声明（01 表 / 02 表 / data.js / times.js）逐字段对比，只读、ERR>0 退出码 1 | 每次改数后跑；新增校验维度时 |
| `Summary/html/last_seen.json` | 基线：每书目录文件 mtime 的最后扫描值（随刷新提交） | check_updates.js 自动维护 |

**GTIMES 列序 = 前七段流程** `[原料,底座,装填,打包,跨层,验证,交付]`（第八段「联邦入库」是数据库事件、目录无 mtime 信号，故只有 `stageStates[7]`，无时间戳列）；采集器内部按优先序
`[交付,验证,跨层,装填,底座,打包,原料]` 存列，写 times.js 时须用 `[6,4,3,5,2,1,0]` 重映射。
**stageStates 长度 8**，与 `GSTAGES` 一一对应，第 8 段按 `tools/kb-federation/kb.sqlite` 的 `books` 表核对（判定用 `federation.idMap` 的键，看板 id ≠ 联邦 book_id）。


## 目录契约（采集器认得的信号，首个命中即归类）

| 阶段 | 路径正则特征 |
|---|---|
| 交付 | `_deliver/`、`交付物/`、`交付报告/说明`、`全量交付` |
| 验证 | `_validate/`、`reports/`、`验证`、`验收` |
| 跨层 | `_kg_join`、`跨层索引` |
| 装填 | `_src/`、`_ai_NN/_vol_NN/_procs_ai/_struct_ai/annotate .py`、`_extract/layers/`、`新官轨范_*_ai/` |
| 底座 | `_item_registry.json`、`_extract/` |
| 打包 | `_layers/`、`data/<层>/`、`归一_`、`_标注`、`_kg_NN.json` |
| 原料 | `assets/sources/`、`_source/`、`原文/`、任意 `.txt/.json/.epub`（兜底，易污染） |

卷号从文件名抽：`_NN.py` / `_NN.json` / `NN_`；装填判定 = 文件 >800B 或 JSON 非空；打包判定 = JSON records 非空。遍历深度 6，跳过 `.`/`__`/`vendor`。

**卷数采集**：采集器对每书全目录（含原料区）文件名抽卷号，取最大值作 `GVOLS.est`（估算）；权威卷数以 `GVOLS.total` 登记为准（正史志书如选举志用原书卷号 45–47 命名分片、地理志源文件编号到 36，est 会虚高）。`data.js` 的 `items` **只写底座条数**（纯"N 条"，不带卷/章），卷数一律看 `GVOLS.total`（看板"卷数"列即读此值）；底座按卷段拆分、无条目号库的书（如选举志），条数取 SKILL 口径并写入 notes 说明。

## 归一门：声明 ↔ 实测（无白名单机制）

`collect_meta.js` 只测**事实**，`data.js`/`Summary/01`/`02`/`times.js` 只写**声明**，`check_summary.js` 把两边逐字段对撞。设计要点：

**1. 采集器只声明几何，不声明口径。** 每本书在 `LAYER_SPEC` 里能说的只有：层住在哪个目录（`dir`）、按子目录还是文件分层（`mode`/`fileRx`）、目录名→层码的别名（`dirs`）、多版本成品取哪个（`pick`）、文件名→真实层码（`fileLayer`）、哪些文件刻意不计数及原因（`ignore`）、尚未装填的整目录排除（`none`）。**「哪些层算数」不在这里决定**——注册状态来自 `data.js.books[].layers` 的层码集合（`loadDeclaredLayers()` 用 `vm` 读，不落第二份名单）。

**2. 盘上分桶，永不静默丢弃。** 一个层根内的 JSON 必落入五类之一，每类都带原因上报：
`layer`（注册层，计入 `totalRegistered`）/ `variant`（同层别版：`*_pilot/_v2/_clean/_auto…`、`.bak`）/ `assembly`（装配件：`_*`、`join/coverage/stats/tmp/scratch`）/ `ignore`（人工写明原因）/ `unregistered`（是层件但 data.js 没登记 → 门亮 WARN，要么补登记、要么在该书 `drift` 写为何不注册）。
分卷件与聚合件并存时**取分卷件**（`L.records = shardRecords || aggRecords`），聚合值另存 `aggRecords` 供门判"两口径都不合才是真错"。

**3. 影子目录永不是真值。** `SHADOW_SEG`（`_deliver/_build/_work*/_extract/_legacy/_backup*/_validate/_views/views/raw/成品/pilot/*_old/*_vN`）不参与层根评分；`_deliver/` 除外——它是 C1 规定的交付落点，只计交付证据、不计层记录数。层根靠打分定位（目录名命中 `_layers|layers|data|_data` +4、带层码子目录 ×6、目录内条数 ×0.05，平铺则 ×1.2）。

**4. 例外只写在三处，不写侧文件。** 几何例外 → `LAYER_SPEC` 的行内注释；口径例外 → `data.js` 该书 `drift[]`（看板书籍详情页直接显示）；方法论例外 → 本文件。**没有 `*_whitelist.json` 一类的旁路名单**：门看到分歧就报，人决定怎么归一，归一后的理由必须留在文档里而不是配置里。

**5. 分级与退出码。** `ERR`=声明会让看板说假话（条数/层数/状态与实测矛盾、声明了盘上不存在的层码、交付说完成但四类交付物全空、联邦入库状态与 `books` 表相反、同一本书 `book.meta.json` 与 `书籍json` 两载体并存）→ 必须改到 0，脚本退出码 1；
`WARN`=两口径都能自圆（分卷/聚合、著录卷数/底座前缀、契约落点缺口如交付未落 `_deliver/`、底座在影子目录）→ 写进 `drift`；
`INFO`=已知例外或待回填（C8 载体未回填、C9 无 spine 且按 `contract.json` v0.3.0 `scope.do_not_build` 只到卷级豁免、卷首/序/后记/校记段不计卷、状态位落后于盘上）。
**C8/C9 按载体判，不按文件名判**（`contract.json` 0.3.0）：新书认 `book.meta.json`，存量认 `书籍json/<书>_校对版.json` 的 meta 块（契约键 `book-json/1.1`）——整书页在场但无 `契约` 键＝本轮刻意跳过，报 INFO 不报 WARN；有 `契约` 键却缺 8 项或 null 无 `_依据/_来源`＝WARN（重跑 `tools/book_json_augment.py` 幂等可解）。
门自身**只读**：不改任何声明文件，报告每条都要人工归一到四处（`Summary/01`、`Summary/02`、`data.js`、`times.js`）。

**6. 卷数规则。** `GVOLS.total` 是著录口径；`item_id` 前缀（`NN-`）是盘上口径，常多出院首/序/后记/校记段——只要正文 `01..total` 全覆盖就只报 INFO。前缀语义不是卷号的书（如大明一统志按府/门编号）在 `GVOLS` 里加 `prefixBasis` 说明，门即不再拿前缀当卷数。`Summary/01` 的「卷数」列与 `GVOLS.total` 必须相等。

**7. 状态与交付判定。** 交付物分四档：`canonical`（`_deliver/`）> `alias`（`交付物/`、`成品/`）> `artifacts`（epub、交付说明/报告、阅读器 html）> `reports`（使用报告/项目总结/收官 md）。写"完成(2)"而四档全空 = ERR；只有别名/成品件 = WARN（C1 落点缺口）。

## 新书接入（checklist）

1. `data.js` 加书条目（照现有 22 书格式；`stageStates` 是 8 位 0/1/2，第 8 位=联邦入库）。
2. `collect_times.js` 的 `DIRS` 加 `id: '相对目录'`；`collect_meta.js` 的 `LAYER_SPEC` 只在几何不合标准契约时才加声明（不合就不加，采集器会自己打分定位层根）。
3. 跑 `node Summary/html/collect_times.js` 看全表；跑 `node Summary/html/collect_meta.js` 看实测。
4. **布局不合契约的书必须人工校准 GVOLS 行**（加 note 说明口径），不要为了过采集器去改书籍目录结构。
5. （可选）`data.js` 的 `fieldMatrix` 补该书各层字段清单，同层对比页才有格子。
6. 跑归一到 ERR=0（见下），`Summary/01`、`02` 同步补行/补节。
7. 浏览器开 `dashboard.html`：书目行、详情流程表、时间线三处都出现该书即接入完成。

## 例行刷新

1. **定位动过的书**：`node Skills/progress-dashboard-integration/scripts/check_updates.js`
   —— 与 `last_seen.json` 基线（每书目录文件 mtime）对比，列出上次记录后有新文件的书及最新改动文件。首次使用 `--seed` 按 git 各目录最后提交时间初始化基线。
2. `node Skills/progress-dashboard-integration/scripts/diff_times.js`
   —— 跑采集器、与现行 times.js 逐阶段对比，只报变化（`*不同*` = 采集启发 vs 人工登记不一致，`*卷数?*` = est 与登记 total 不符，多为已知盲区，核对后定夺），并自清中间文件。
3. 对上面列出的书**以磁盘实况为准复核装填/打包卷数**（数 `_layers/` 或逐卷文件里 records 非空的卷），不要信体积启发，也不要信执行侧的完成汇报——一切以 JSON 实际内容计。
4. 改 `times.js`：GTIMES/GVOLS 对应书那一行（含 `total` 卷数）；改 `data.js`：layers 计数、notes、`items`（只写底座条数，不写卷数）、必要时 stageStates。
5. **跑归一门直到 ERR=0**：`node Skills/progress-dashboard-integration/scripts/check_summary.js`（可加 `--only wzz,mhd`）。
   剩下的 WARN 逐条落进该书 `drift[]`；INFO 里的 C8 未回填（含刻意跳过的整书页）与 C9 卷级豁免属存量线，不是本轮要修的账。
6. 同步 `Summary/01_书目总览.md`（一行一书：层数/卷数/底座条目/产出记录数）与 `Summary/02_各书产出层.md`（一节一书、逐层记录数）——门会拿这两张表和 data.js 对撞，不一致直接报。
7. 刷新完成后 `check_updates.js --update` 回写基线，与看板数据一起提交（`chore(Summary): 看板进度刷新 <日期>`）。在途未收口的书（如野获编补卷）在 note 里写明"快照 <日期>，卷X 在途"。
8. 若看板要发布（Qoder Site / `dist/`），把 `data.js/times.js/dashboard_app.js/dashboard.css/stages.js/fields.js` 同步拷进 `Summary/html/dist/` 再上线。

## 已知盲区（登记值优先，勿被采集器覆盖）

| 书 | 现象 | 口径 |
|---|---|---|
| mhd 明会典 | pack 采集 0 | 成品按部门聚合、不按卷打包 → pack=null |
| xjz 选举志 | fill 采集 0 | 装填为单文件全卷抽取 → 人工记 3 |
| yhb 野获编 | fill 采集严重少报 | 装填直写 `_layers/` 层文件，与打包同步 → 按 pack 计（34 卷已于 2026-10-16 全落） |
| bz 兵志 | 全 0 | 仅卷66 卫所树试点 → 人工记 1；`LAYER_SPEC.bz.none` 声明整目录非层成品，门不把它当层件 |
| xgg 新官轨范 | pack 采集 0 | 成品在书特化目录 `新官轨范_章节/`（带书名前缀），不匹配打包契约正则 → 人工记 11（按章） |
| 原料列 | 任何 `.txt/.json` 都算 | 报告/清单类文件会污染原料时间，慎采 |
| 载体 `书籍json/` | 不参与七段时间、不估卷数、不进层账；**只在盘上无 `_item_registry.json` 时**当底座计量源 | `collect_times.js` 的 `CARRIER_SEG` 一处定义、两处用（阶段时间跳过、`collect_meta.js` 的 `collectLayersFor` 先滤）——它是从 `_item_registry.json` 派生的 C8/C9 成品，当成原料会把「资产化那天」冒充「原料改动那天」，当成层件会以乱码 key 冒充未注册层（2026-10-16 实见 mhd 180 / zp 11 / sdr 78）。第三种形态：《物理夜航船》这类不走工厂谱系的书，切条库就地只在载体里（§6b 就地路线）→ `registryFromCarrier()` 回退量条数/卷前缀，门把这类差异记为 **WARN+来源说明而非 ERR**（载体条=著录粒度，选举志 3 条 vs 声明 58 段就是这种情况），并在 `registry.fromCarrier` 上标形 |
| 卷数 est | qb 22 / zxl 8 / xjz 47 / dlz 36 虚高 | 原料或分片文件名带数字编号，est 只作核对线索，登记 total 为准 |
| myt 明一统志 | 装填/底座时间、fill/pack 全采不到 | 工程在 `mingyitongzhi-kb/14-mingyitongzhi-knowledge/`，布局 `_data/`+`pilot/`（非 `_extract`/`_layers`）；est=18 是 `_06_18` 文件名误抽 → GTIMES/GVOLS(total=90) 人工登记；`item_id` 前缀是府/门序号（`prefixBasis`），不是卷号 |

**层记录数采集盲区（collect_meta.js 已处理，改动时勿回退）**：
`_layers/*.json` 可能是裸数组、`{records:[]}`、`{层名:[]}` 多表、或按卷分片——`countRecords()` 按
`数组 → 多表 → 具名容器(records/items/…) → 单数组 → 整对象 → 最长数组(估) → null` 逐级回落，每级都在 `shapes` 里留痕；
`zgz` 的 `officials` 混在 `structs/` 目录里，靠 `fileLayer` 拆出来；`mhd` 的层是平铺裸数组且带 `office_tree/vocab/*.bak` 派生件，靠 `ignore`+variant 识别；
`sdr` 的 `data/聚合/` 是分卷件的副本，计进合计会翻倍（已 `ignore` 并写明原因）。

## 看板侧硬约束（改 dashboard 时）

- dashboard 已三分：`dashboard.html`（模板+引用）/ `dashboard.css`（样式）/ `dashboard_app.js`（Vue 应用逻辑）；改视图=改模板在 html、改行为在 app.js，勿把样式/逻辑再写回 html。

- in-DOM 模板里 `el-*` 组件**必须显式闭合**（`<el-input/>` 会吞掉后续兄弟节点，且生产版 Vue 静默失败）；渲染异常时用 vue.dev.js 副本看模板编译报错。
- JSON 中文注释走 `hlJson` 的 `//` 备注引擎（字段值不替换）。
- 阶段数据单一来源：`stageStates + GTIMES + GVOLS + GSTAGES`，任何新视图复用同一结构，不另造平行数据。

## Resources

- `scripts/check_updates.js`：基线对比器（哪本书动过；--seed 按 git 初始化 / --update 回写基线）。
- `scripts/diff_times.js`：times.js 刷新对比器（跑采集器 + 报阶段变化 + 清理中间文件）。
- `scripts/check_summary.js`：归一门（`collect_meta.js` 实测 ↔ `Summary/01`+`02`+`data.js`+`times.js` 声明，ERR/WARN/INFO 分级，ERR>0 退出码 1；`--only id,id` 限书）。
- 采集器 V1 在 `Summary/html/collect_times.js`（时间戳与卷进度的正则/DIRS 唯一维护处）；采集器 V2 在 `Summary/html/collect_meta.js`（层根几何 `LAYER_SPEC` 与三域实测唯一维护处，`_meta_out.json` 是 gitignore 的临时件）。
