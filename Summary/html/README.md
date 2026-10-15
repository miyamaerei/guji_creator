# 古集 · 进度看板

面向「古籍知识工程」仓库的**纯静态进度看板**：追踪约 22 部明清古籍（笔记 / 官箴书 / 政书 / 正史志书等）从原料到交付的全流程建设进度，可视化每本书的流程阶段、语义层产出、字段契约一致性与时间分布。

无后端、无构建工具，全部数据硬编码在 JS 文件中，浏览器直接打开即可用。

> 本文有两份完全相同的拷贝：`Summary/README.md`（盘点目录就近看）与 `Summary/html/README.md`（看板目录就近看）。改一处必须同步另一处——若要合并成一份，先确认没有外部链接指向被删的那份。

---

## 技术栈

| 依赖 | 用途 | 加载方式 |
|---|---|---|
| Vue 3（global build） | 单页应用框架 | `vendor/vue.global.prod.js` |
| Element Plus | UI 组件（表格 / 标签页 / 步骤条 / 折叠面板等） | `vendor/element-plus.*` |
| Apache ECharts | 时间线散点图 | `vendor/echarts.min.js` |
| Node.js（仅采集时用） | 扫描各书目录、生成阶段时间戳 | `collect_times.js` |

---

## 目录结构

```
Summary/html/
├── dashboard.html          # ★ 主应用（Vue3 单页，6 个 Tab）
├── dashboard_app.js         # 主应用逻辑（数据归一、对比、时间线渲染）
├── dashboard.css           # 主应用样式
│
├── data.js                 # GDATA 主数据集（书目 / 层记录数 / 层分组 / 字段矩阵）
├── fields.js               # FIELDS 字段词典（record 字段 → 中文释义）
├── times.js                # GTIMES 每书阶段最后执行时间戳 + GVOLS 卷进度
├── stages.js               # GSTAGES 八段流程定义（goal/mark/next/where/do/out/ref/pit）
├── collect_times.js        # 采集器 V1：扫描各书目录自动生成 times.js
├── collect_meta.js         # 采集器 V2：盘上实测三域（著录/结构/知识层），供归一门比对
├── last_seen.json          # 采集器增量状态
├── _meta_out.json          # collect_meta.js 的落盘快照（gitignore，只作临时查看）
│
├── index.html / book.html / layers.html / compare.html / style.css
│                           # 早期无框架静态版（已被 dashboard.html 取代，保留对照）
│
├── vendor/                 # Vue / Element Plus / ECharts 本地副本
├── dist/                   # 发布目录（dashboard.html 拷贝为 index.html）
└── _serve_dist.js          # 零依赖静态服务器（Node，端口 8793）
```

---

## 功能模块（dashboard.html 的 6 个 Tab）

### 1. 书目总览
全部书籍的汇总表格，每行一本书：

- 书名（点击进入书籍详情）、目录名、作者·时代、性质（体裁）
- 状态：✅ 完成 / 🚧 在建 / ⬜ 无产出
- 层数、底座条目数、卷数（悬停显示装填/打包明细）、产出记录数（各层 records 求和）
- 当前阶段标签、流程最后执行时间、总进度条（按八阶段状态加权百分比）
- 顶部过滤：关键词搜索（书名/目录/作者/性质）、状态筛选、当前阶段筛选

### 2. 书籍详情（点书名进入）
展示单本书的全流程画像：

- **八段流程步骤条**（el-steps），每步附执行时间与卷装填进度
- **当前节点卡片**：正在哪个阶段、该阶段的完成标志、下一步该做什么
- **逐阶段流程表**：这一步在做什么 / 完成标志 / 本书状态 / 执行时间 / 下一步动作
- **备注**与「⚠ 与标准流程/全量契约的偏移点」折叠面板（`drift`，记录本书自建层、命名特例、已知缺口等）
- **各层产出表**：层 key、含义、记录数、record 字段列表

### 3. 全量数据结构
以「层」为中心的全仓数据字典：

- 左侧按类别分组的层目录（通用核心层 / 规则政书型层 / 明史诸志特化层 / 明会典特化层），每层标注「几本书产出 / 合计多少条」
- 右侧层详情：
  - 该层是工厂层库还是本书自定义层、中文释义
  - **层 JSON 骨架**：union 字段全集，字段名后自动追加中文注释（来自 fields.js）
  - 多选书籍展开，每本书单独显示其实际采集字段，并自动标注 **偏移字段**（仅此书独有）与 **缺失共性字段**（他书都有而此书没有）

### 4. 同层对比
同一层下各书字段契约的横向对比矩阵：

- 行 = 字段，列 = 书；图例：绿 ✓ = 共性字段，黄 ● = 该书偏移/独有，红 ✗ = 他书共有而此书缺失，— = 沿工厂契约未逐字段采集
- 可高亮某本书、字段列显示中文释义、按「全有 / 少数」热度标注
- 下方「差异摘要」逐书列出偏移与缺项标签；各书 JSON 可一键全部展开/收起

### 5. 时间线
流程阶段执行的时间分布，三种视图共用同一份 `GTIMES` 数据：

- **全书时间轴（ECharts 散点）**：纵轴=书名，横轴=执行时刻，颜色=各流程阶段；底部缩放滑条可框选区间，支持滚轮/拖拽
- **单书时间轴**：下拉选一本书，放大看其阶段推进
- **按天·明细视图（DOM 泳道）**：按日期分组，每本书一条泳道，圆点落在一天内的时刻位置，可勾选显示哪些阶段

URL 支持深链：`dashboard.html?tab=timeline&id=kzz&layer=ent`（自动切 Tab、选中书/层）。

### 6. 联邦入库
追踪「交付之后」的第 8 步：把该书的层产物作为**一本新书**接入跨书联邦库
（`tools/kb-federation/kb.sqlite`），参与跨书实体对齐与关联查询。

- **库级汇总**：已入库书数 / 记录总条数 / 图谱节点数 / canonical 归并组 / 跨书成员引用 / 待定候选链接 / 人工裁决覆盖
- **已入库表**：按 records 降序，列出各书 book_id、源目录、层数、records、nodes、edges、items、装载日；书名可点击跳转书籍详情
- **未入库表**：写明每本书卡在哪（层产物就绪未写 adapter / 交付未收口 / 未开工），避免看着像漏做
- **入库操作 6 步** + **四条铁律**（原文不重抄 / ID 命名空间 / 物理不合并 / 单向只读）+ 可核验命令

数据源：`data.js` 的 `federation` 块。书目总览的「联邦入库」列由 `fedState()` 从 `idMap` + 层数实时推导
（`2=已入库 / 1=待入库 / 0=无产物`），不另存字段，避免两处数据打架。

> **两套 id 不同名**：看板 id ≠ 联邦 book_id。已入库 13 本里有 6 本不同名——
> `xgg↔xgf`、`fhs↔fqh`、`lgsz↔lgs`、`zxl↔xzl`、`wz↔ysz`、`xjy↔xyf`，
> 映射表在 `data.js` 的 `federation.idMap`。判定「是否已入库」必须用 idMap 的**键**（看板 id），
> 只看 `books` 表会把这 6 本误判成未入库。

---

## 核心数据模型

### 八段流程（stages.js → GSTAGES）
```
原料/原文 → 底座切条 → 装填解读 → 层成品打包 → 跨层索引 → 验证 → 交付 → 联邦入库
```
每本书的 `stageStates` 数组长度与 `D.stages` 一致（当前 8），取值 `0=未做 / 1=在建 / 2=完成`；看板上的步骤条、进度百分比、当前阶段均由它推导。

### 层（layer）与层名归一（NORM）
各书对同一概念层的命名不统一（单复数、缩写、中英文名混用），`dashboard_app.js` 顶部的 `NORM` 表把它们归一到 key，例如：
`ents→ent`、`evts/events→event`、`appts→appt`、`org_profiles/office_profiles→org_profile`、`标注→ent`、`geo_station→geo`。

### 字段矩阵（fieldMatrix，data.js）
`fieldMatrix[层key][书id] = 该书此层 record 的实际字段列表`（未逐字段采集的为 `null`，表示沿工厂契约）。第 3、4 个 Tab 的对比逻辑全部基于它。

### 偏移点（drift）
每本书一个字符串数组，记录该书与标准工厂契约的差异：自建层、目录命名特例、ID 段位约定、已知遗留缺口等——人工盘点录入，是本看板最有价值的上下文。

### 卷进度（GVOLS，times.js）
`{ total, fill, pack, note }`：总卷数 / 已装填卷 / 已打包卷；在建书（如《明会典》180 卷装填到 108）据此显示卷级进度。

---

## 如何运行

### 方式一：直接打开（开发/查看）
浏览器直接打开 `dashboard.html` 即可（vendor 为相对路径，无需服务器）。

### 方式二：静态服务器（发布目录）
```bash
node _serve_dist.js
# → http://localhost:8793  （服务 dist/ 目录）
```
修改 `dashboard.html / *.js / *.css` 后，需把变更文件拷贝到 `dist/` 才会反映在 8793 服务上。

---

## 如何更新数据

| 数据 | 更新方式 |
|---|---|
| `times.js`（阶段时间戳、卷进度） | 运行 `node collect_times.js`，自动扫描各书目录按路径正则归类阶段后重写 `times.js` |
| `data.js`（书目、层记录数、drift、字段矩阵） | **人工盘点后手动编辑**——数字来自 `node collect_meta.js` 的盘上实测，叙述来自 `Summary/01–04` 与各书交付说明 |
| `fields.js` | 字段词典增补，手动维护 |
| `stages.js` | 八段流程定义变更时手动维护 |

### 归一管线（改数后必跑）

```bash
node Summary/html/collect_meta.js                              # ① 盘上实测 → _meta_out.json（临时件）
node Skills/progress-dashboard-integration/scripts/check_summary.js   # ② 实测 ↔ 声明逐字段对比
```

门输出三级：`ERR`=看板正在说假话（必须改到 0，退出码 1）、`WARN`=口径分歧或契约落点缺口（要在该书 `drift` 里写明理由）、`INFO`=已知例外/待回填。
可加 `--only wzz,mhd` 只查几本。**门的纪律是只读**：它不改任何声明文件，报告列出的每一条都要人工归一到 `Summary/01`、`Summary/02`、`data.js`、`times.js` 四处。

几何例外（哪本书的层住在哪个目录、哪些文件是别版/装派件、哪些刻意不计数）写在 `collect_meta.js` 的 `LAYER_SPEC` 注释里，
口径例外写在 `data.js` 各书 `drift[]` 里（看板直接显示），**不落单独的白名单文件**——见 `Skills/progress-dashboard-integration/SKILL.md`。

> 采集器的阶段归类优先级（首个命中即归类）：交付 > 验证 > 跨层索引 > 装填源 > 底座条目库 > 层成品 > 原文素材；规则在 `collect_times.js` 的 `STAGES` 正则数组中，新增目录形态时需同步更新。

### data.js 的层数组有两种合法写法

`books[].layers` 支持两种元素形态，`dashboard_app.js` 顶部的 `normLayer()` 会在加载时统一归一，写哪种都能正常渲染：

```js
// 旧式：三元组 [键, 中文名, 记录数]
["ent","实体",8481]

// 新式：对象（可附带覆盖率与备注，信息更全）
{layer:"ent", count:649, covered:"328/401", note:"auto_v3 候选"}
```

归一后的内部形态是 `{key, name, count, covered, note, k}`——`name` 缺省时按 `layerNames` 回落到中文层名。
`covered`（覆盖率）与 `note` 是**新式独有**字段，旧式没有；两者混用时不会报错。

> ⚠️ 历史坑（2026-10-16 修复）：`normLayer()` 引入前，代码直接读 `l[2].toLocaleString()`。
> 新式条目下 `l[2]` 为 `undefined`，`dashboard_app.js` 顶层的 `D.books.forEach` 因而抛出
> `TypeError: Cannot read properties of undefined (reading 'toLocaleString')`。
> 该异常发生在 `mount("#app")` **之前**，会中断整个脚本 —— 表现为**页面完全空白**（DOM 里连 `{{ }}` 都还在），
> 而不是「表头在、数据空」。新增用新式写法的书时务必确认本条已生效。

同理，`stageStates` 数组长度按 `D.stages.length`（8）归一：多余的尾部元素截断，不足的补 0。

---

## 数据规模（快照 2026-10-16，数据截至 2026-10-16）

- 书目 22 部：完成并交付 14 部、在建 5 部、无结构化产出 3 部
- 注册层记录合计 **163,775 条**（`data.js` 各书逐层求和，与 `collect_meta.js` 盘上实测逐层一致）
- 归一层 45 种，书×层产出 170 对（原始层码 73 个，`NORM` 归一后 45 种）
- 阶段时间线 115 个事件，覆盖 21 部书（刑法志无时间戳）、8 个本地日期（2026-09-27 → 2026-10-16）
- 卷进度合计 520 卷、已装填 438 卷（`GVOLS`；明会典 108/180 为按部门选卷装填）
- **联邦入库**：已入库 13 部 / 未入库 9 部；联邦库 49,885 records、25,205 nodes、
  1,580 canonical、6,772 members、6,690 candidate_links、204 人工裁决

> 维护提示：根目录的 `data.js` / `times.js` / `dashboard_app.js` 才是源；
> `dist/` 是拷贝出的发布目录，改完源文件后**必须**同步拷贝，
> 否则 `node _serve_dist.js`（8793）看到的仍是旧版本 —— 两处数据曾因此长期不一致。
