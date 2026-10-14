---
name: progress-dashboard-integration
description: 各书籍项目进度如何被采集器识别并接入古集看板（Summary/html/dashboard.html）的操作规范，含每书目录最后更新时间的基线对比（last_seen.json）。当需要查哪些书籍项目有了更新、刷新看板进度数据（times.js/data.js）、把新书项目接入看板、或诊断某书阶段时间/卷进度为何采不到时使用。典型触发："刷新看板"、"更新进度"、"哪些项目有更新"、"把X接入看板"、"看板时间线缺某本书"。
---

# 进度采集接入看板（Progress Dashboard Integration）

## 定位与数据流

看板是**纯静态、离线（file://）消费四个数据文件**的 Vue3 单页；本技能只管"把各书项目的磁盘状态搬进这四个文件"。

```
各书项目目录 ──(collect_times.js 扫描 mtime/卷文件)──▶ _collect_out.json ──(人工校准)──▶ times.js   ┐
data.js（书目台账，手写）                                                                    ├──▶ dashboard.html
stages.js（七段流程语义，手写，改流程才动）                                                     ┘
```

| 文件 | 性质 | 何时改 |
|---|---|---|
| `Summary/html/data.js` | 手写台账：每书 id/dir/title/status/stageStates/layers/notes/drift | 新书接入、层记录数变化、阶段推进 |
| `Summary/html/times.js` | 校准快照：GTIMES（7 阶段最后写入 ms）+ GVOLS（total/fill/pack/note） | 例行刷新（见下） |
| `Summary/html/stages.js` | GSTAGES：七段流程 {name,goal,mark,next}，书目/详情/时间线共用 | 仅流程定义本身变化 |
| `Summary/html/collect_times.js` | 采集器：DIRS 映射 + 阶段分类正则（导出 DIRS/walk 供本技能脚本复用） | 新书接入 / 目录改名 |
| `Summary/html/last_seen.json` | 基线：每书目录文件 mtime 的最后扫描值（随刷新提交） | check_updates.js 自动维护 |

**GTIMES 列序 = 流程顺序** `[原料,底座,装填,打包,跨层,验证,交付]`；采集器内部按优先序
`[交付,验证,跨层,装填,底座,打包,原料]` 存列，写 times.js 时须用 `[6,4,3,5,2,1,0]` 重映射。

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

## 新书接入（checklist）

1. `data.js` 加书条目（照现有 21 书格式；stageStates 是 7 位 0/1/2，与 GTIMES 对得上）。
2. `collect_times.js` 的 `DIRS` 加 `id: '相对目录'`。
3. 跑 `node Summary/html/collect_times.js` 看全表。
4. **布局不合契约的书必须人工校准 GVOLS 行**（加 note 说明口径），不要为了过采集器去改书籍目录结构。
5. （可选）`data.js` 的 `fieldMatrix` 补该书各层字段清单，同层对比页才有格子。
6. 浏览器开 `dashboard.html`：书目行、详情流程表、时间线三处都出现该书即接入完成。

## 例行刷新

1. **定位动过的书**：`node Skills/progress-dashboard-integration/scripts/check_updates.js`
   —— 与 `last_seen.json` 基线（每书目录文件 mtime）对比，列出上次记录后有新文件的书及最新改动文件。首次使用 `--seed` 按 git 各目录最后提交时间初始化基线。
2. `node Skills/progress-dashboard-integration/scripts/diff_times.js`
   —— 跑采集器、与现行 times.js 逐阶段对比，只报变化（`*不同*` = 采集启发 vs 人工登记不一致，多为已知盲区，核对后定夺），并自清中间文件。
3. 对上面列出的书**以磁盘实况为准复核装填/打包卷数**（数 `_layers/` 或逐卷文件里 records 非空的卷），不要信体积启发，也不要信执行侧的完成汇报——一切以 JSON 实际内容计。
4. 改 `times.js`：GTIMES/GVOLS 对应书那一行；改 `data.js`：layers 计数、notes、必要时 stageStates。
5. 刷新完成后 `check_updates.js --update` 回写基线，与看板数据一起提交（`chore(Summary): 看板进度刷新 <日期>`）。在途未收口的书（如野获编补卷）在 note 里写明"快照 <日期>，卷X 在途"。

## 已知盲区（登记值优先，勿被采集器覆盖）

| 书 | 现象 | 口径 |
|---|---|---|
| mhd 明会典 | pack 采集 0 | 成品按部门聚合、不按卷打包 → pack=null |
| xjz 选举志 | fill 采集 0 | 装填为单文件全卷抽取 → 人工记 3 |
| yhb 野获编 | fill 采集严重少报 | 装填直写 `_layers/` 层文件，与打包同步 → 按 pack 计 |
| bz 兵志 | 全 0 | 仅卷66 卫所树试点 → 人工记 1 |
| xgg 新官轨范 | pack 采集 0 | 成品在书特化目录 `新官轨范_章节/`（带书名前缀），不匹配打包契约正则 → 人工记 11（按章） |
| 原料列 | 任何 `.txt/.json` 都算 | 报告/清单类文件会污染原料时间，慎采 |

## 看板侧硬约束（改 dashboard.html 时）

- in-DOM 模板里 `el-*` 组件**必须显式闭合**（`<el-input/>` 会吞掉后续兄弟节点，且生产版 Vue 静默失败）；渲染异常时用 vue.dev.js 副本看模板编译报错。
- JSON 中文注释走 `hlJson` 的 `//` 备注引擎（字段值不替换）。
- 阶段数据单一来源：`stageStates + GTIMES + GVOLS + GSTAGES`，任何新视图复用同一结构，不另造平行数据。

## Resources

- `scripts/check_updates.js`：基线对比器（哪本书动过；--seed 按 git 初始化 / --update 回写基线）。
- `scripts/diff_times.js`：times.js 刷新对比器（跑采集器 + 报阶段变化 + 清理中间文件）。
- 采集器本体在 `Summary/html/collect_times.js`（正则与 DIRS 的唯一维护处）。
