# 跨书合并 ELT —— 实现步骤（编码路线图）

> 承接：`docs/跨书合并方案.md`（定位与四层架构）、  
> `docs/跨书合并-ELT设计.md`（E/L/T 三段与去歧义算法）、  
> `docs/跨书合并-数据库设计.md` + `tools/kb-federation/schema.sql`（三层存储与 18 张表）。
>
> 本文把这些设计**落成可编码的任务分解**：先定程序骨架，再按 F0→F4 分五阶段实现，  
> 每步给「目标 / 输入 / 输出 / 关键接口 / 验收」，照着写即可。
>
> **铁律不变**：零第三方依赖（仅 `sqlite3`、`json`、`re`、`os`、`argparse`）；  
> 复合主键 `(book_id, …)` 隔离撞号；原文只存指针；Tier1/2 全部可重建、不入 git；联邦只读六书、绝不回写。

> **落地进度（2026-10-11）**：F0-a / F1 / **F2（六书全量装载）均已落地并实证**。
>
> - `tools/kb-federation/` 已落地可跑：`kbdb.py` / `collision.py` / `extract.py` / `load.py` / `federation.py` / `schema.sql` / `adapters/{__init__,base,layers_adapter,vol_layer_adapter,data_layer_adapter,norm_layer_adapter,xgf_adapter}.py`，均为零第三方依赖。
> - **撞号体检**：总 ID **14302** / 跨书撞号 **2847**（占 19.9%）/ ENT **2448**（详见 §2）。将 8MB 扫描上限提到 64MB 后数字不变（蘧编 `归一_ents.json` 11MB 纳入后，其 ENT-5xx 段早已被他书撞过，不改总计）。
> - **F1 实证**：先进遗风 `items=100`、`records=19`、复合主键零重复、重跑幂等。
> - **F2 实证（六书全量）**：`federation.py load-all` 一次装载六书，结果——  
>   `items=3407`（kzz476/wzz1288/sdr1197/xgf275/qb71/xyf100）、  
>   `records=32647`（kzz13779/wzz10582/sdr4348/xgf1975/qb1944/xyf19）、  
>   `load_runs=6`（全 `done`）、`layer_catalog` 申报 55 个层（13/11/8/9/8/6）。  
>   **折叠丢失 = 0**：所有跨书撞号（含 ENT-2448）均由复合主键 `(book_id,layer_key,local_id)` 消解，DB 内 0 个重复主键组。
> - **数据特征修正（F1/F2 已实现）**：
>   1. 先进遗风 ent 层无显式 `id` 且同 `item_id` 同层重复 → local_id 取 `item_id#层内序号`。
>   2. **客座/五杂俎 ID 按卷重排**（vol02 又从 `ENT-0001` 起）→ `local_id` 统一加卷前缀 `卷:ENT-xxxx` 隔离。
>   3. **水东/新官 的 `id` 是「按实体」复用标识**（同一实体在多处出现，如 `ENT-263` 在一卷出现 6 次、`XGF-R-008` 出现 3 次）→ 用 `dedup_local_id` 追加 `#n` 后缀去重，保证每条记录都落到库里、零折叠。
>   4. 蘧编 `归一_ents.json` 达 11MB（>旧 8MB 上限）→ 上限提到 64MB，否则实体层会被静默丢弃。

---

## 0. 程序骨架（先定目录与模块，再写逻辑）

```
tools/kb-federation/
├── schema.sql              # 已存在（18 表，可建库）
├── federation.py           # CLI 入口：create / collision / load / align / query
├── kbdb.py                 # 低层 DB 工具：连接、建库、uid 生成、幂等 upsert
├── adapters/
│   ├── __init__.py         # 注册表：book_id → adapter 类 + 每书 catalog 声明 + LAYER_DECL
│   ├── base.py             # BookAdapter 抽象基类 + LayerSlice + pick_id/build_local_id/dedup_local_id
│   ├── layers_adapter.py   # 先进遗风（xyf）：{fingerprints:[],layers:{key:[rec]}}
│   ├── vol_layer_adapter.py# 客座/五杂俎（kzz/wzz）：_layers/<layer>_<vol>.json
│   ├── data_layer_adapter.py # 水东（sdr）：data/<layer>/*.json（ent 用 annotations，余用 records）
│   ├── norm_layer_adapter.py # 蘧编（qb）：归一_<layer>.json（跨卷单文件，ID 全局唯一）
│   └── xgf_adapter.py      # 新官（xgf）：多份「归一_汇总」文件（实体/规则/流程/事件/结构×5）
├── extract.py              # E 阶段：调 adapter → 标准中间表
├── load.py                 # L 阶段：中间表 → Tier1（items/records）+ 写 catalog（含折叠告警）
├── transform.py            # T 阶段编排：T0→T1→T2→T3
├── name_resolver.py        # T1：ent_keys 名字 → node uid
├── align.py                # T2/T3：候选生成 + 集体消歧（并查集/传播/剪枝）
├── collision.py            # F0-a：撞号体检（固化 2847 数字，作为装载前置断言）
└── query.py                # L3 查询层 API
```

依赖方向（无环）：

```
federation.py → {collision, extract, load, transform, query}
extract      → adapters.*
load         → kbdb + schema.sql
transform    → kbdb + name_resolver + align
name_resolver→ kbdb
align        → kbdb
query        → kbdb
```

---

## 1. 核心数据结构与接口

### 1.1 `adapters/base.py` —— 中间表

```python
@dataclass
class LayerSlice:
    book_id: str
    layer_key: str                 # 归一 key：'ent'/'appt'/'evt'/...
    container_kind: str            # rows|list|entries|records|fingerprints
    kind: str                      # node|edge|annotation|profile
    id_prefix: str                 # 本书实际前缀 'ENT-'/'APPT-'/...
    records: list[dict]            # 每条 = {'local_id':..., 'payload':{...}, 'item_id':...}

class BookAdapter:
    def __init__(self, book_id, source_root): ...
    def discover(self) -> dict[str, LayerSlice]:
        """扫描 source_root，返回 layer_key -> LayerSlice。
           必须填充 kind / container_kind / id_prefix（来自 __init__.py 的 catalog 声明）。"""
    def _read_json(self, rel_path) -> dict: ...   # 带大小上限（>8MB 跳过）
```

### 1.2 `adapters/__init__.py` —— 注册表 + 每书 catalog 声明

```python
BOOK_REGISTRY = {
    'kzz': {'class': RowsAdapter,         'root': 'kezuozhuiyu-kb',
            'join': '_layers/_kg_join.json'},
    'wzz': {'class': RowsAdapter,         'root': 'wuzazu-kb',
            'join': '_layers/_kg_join.json'},
    'sdr': {'class': ListAdapter,         'root': 'shuidongriji-kb',
            'join': 'data/join/_kg_join.json'},
    'xgf': {'class': EntriesAdapter,      'root': 'xinguanguifan-kb',
            'join': '_kg_join.json'},
    'qb':  {'class': RecordsAdapter,      'root': 'qubian_kb',
            'join': '_kg_join.json'},
    'xyf': {'class': LayersAdapter,       'root': 'xianjinyifeng-kb/05-xianjinyifeng-knowledge',
            'join': 'data/_layers/kg_join.json'},
}
# 每层声明（kind/container_kind/id_prefix）也在此登记，discover() 直接复用，
# 不靠运行时猜——避免 #27 那种「容器键 events/evts 不一」的踩坑。
LAYER_DECL = {
    'kzz': {'ent':('node','rows','ENT-'), 'rel':('edge','rows','REL-'), ...},
    'xyf': {'ent':('node','layers','ENT-'), 'appt':('edge','layers','APPT-'), ...},
    # ... 六书 × 各层
}
```

> **要点**：`LAYER_DECL` 把「层 key ↔ 形态 ↔ 前缀」显式登记，取代运行时试探。  
> 这正是 `docs/mcp-契约规划.md` C4/C5 在联邦线侧的兑现——新书只要在此加几行，loader 不改动。

### 1.3 `kbdb.py` —— DB 工具

```python
def connect(path) -> sqlite3.Connection: ...
def ensure_schema(con): con.executescript(open('schema.sql').read())  # 跳过 FTS 注释段
def make_uid(book_id, local_id) -> str: return f"{book_id}:{local_id}"
def upsert(con, table, rows, pk_cols, conflict='REPLACE'): ...   # 批量、事务
def wipe_book(con, book_id):   # 清 books/layer_catalog/items/records + 关联 nodes/edges
```

> `PRAGMA foreign_keys=OFF`（schema 已设）：目录驱动，loader 自管写入顺序（先删后插幂等）。

---

## 2. F0 前置基建与体检（回本第一块）

### F0-a 撞号体检 `collision.py` ✅ 已实现并实证

**目标**：把「14302 个 ID 中 2847 个跨书撞号」固化为可重复脚本，作为 E 阶段前置断言——  
撞号必须被复合主键消解，否则程序在 load 前就报错（而不是静默污染，对应 #27 反制）。

**输入**：六书源目录（默认读 `BOOK_REGISTRY`，可用 `--roots` 覆盖）。  
**输出**：`CollisionReport`（总 ID 数、跨书撞号数、按前缀分布、样例）。  
**关键函数**：

```python
ID = re.compile(r'\b([A-Z]{2,4}(?:-[A-Z])?)-(\d+)\b')

def scan_ids(roots: dict[str,str]) -> dict[str, set[str]]:
    """书 -> {id}。walk 时跳过 _backup/_tmp/_validate/_build/交付物/阅读器，文件>8MB 跳过。"""
def check_collision(roots) -> CollisionReport:
    owner = defaultdict(set)            # id -> {书}
    for b, ids in scan_ids(roots).items():
        for k in ids: owner[k].add(b)
    multi = {k:v for k,v in owner.items() if len(v) > 1}
    return CollisionReport(len(owner), len(multi), by_prefix(multi))
```

**验收**：重跑结果与已记录数字一致（总 14302 / 撞号 2847 / ENT 2448 / 新官 591 全落五杂俎）。脚本可作为 `federation.py collision` 子命令。

### F0-b 建库与元信息

**目标**：`federation.py create [--db PATH]` 跑 `schema.sql` + 写 `federation_meta`（`schema_version`、`created_at`）。  
**验收**：空库 18 表就绪，FTS5 可用则建 `fts_nodes`（注释段取消注释），不可用则跳过不报错。

### F0-c 写 `LayerSlice` / `BookAdapter` / `BOOK_REGISTRY` / `LAYER_DECL`

**目标**：抽象基类与注册表就位，至少 `LayersAdapter`（先进遗风）能 `discover()` 出 6 层。  
**验收**：`extract.py` 对先进遗风返回 `{'ent':Slice,'appt':Slice,...}`，每个 Slice 的 `kind/id_prefix/records` 正确。

---

## 3. F1 单书 loader 试点（先进遗风，最小最规整）✅ 已实现并实证

> 选先进遗风：它只有 76 条、`fingerprints+layers` 形态最新、无历史包袱，最适合先证明「六本书能安全躺在同一个库」。

### 3.1 E —— `extract.py`

```python
def extract_book(book_id, source_root) -> dict[str, LayerSlice]:
    adapter = BOOK_REGISTRY[book_id]['class'](book_id, source_root)
    return adapter.discover()
```

**验收**：返回先进遗风全部已建层（ent/appt/evt/rel/opn/trl）的 Slice。

### 3.2 L —— `load.py`（忠实装载，先删后插）

```python
def register_catalog(con, book_id, slices):
    # 写 books（source_root/schema_version）+ layer_catalog（kind/container_kind/id_prefix）
    # + layer_fields 初版（字段名 + role 默认 attr，T0 阶段再细化）
def load_records(con, book_id, slices):
    # 1) items：从 ent 层 / _item_registry 抽 item 指针（fingerprint_ref 不抄正文）
    # 2) records：每 Slice.records 逐条 INSERT（payload=JSON 原文），含 volume/item_id
    # 3) 写 load_runs（started/finished/status/record_counts JSON）
def load_book(con, book_id, *, wipe_first=True) -> LoadReport:
    wipe_book(con, book_id) if wipe_first else None
    slices = extract_book(book_id, root)
    register_catalog(con, book_id, slices)
    load_records(con, book_id, slices)
```

**验收**（关键，均已实测通过）：

- 先进遗风 **items=100**（= `fingerprints` 数）+ **records=19**（= ent9/appt2/rel1/event2/opn1/trl4 之和）。
- `items` 只存 `fingerprint_ref` 指针 + 前 50 字 title 摘要，**不含正文大段**。
- 复合主键工作：`records` 按 `(book_id,layer_key,local_id)` 零重复；`xyf:01-039#0`（王守仁）与 `kzz:ENT-001` 互不干扰。
- 重跑幂等：第二次 load（`wipe_first=True` 先删后插）后总数不变。

> **local_id 约定**（已落地）：层记录有显式 `id`（rel/event）即用 `id`；无 `id` 的层（ent/appt/opn/trl）用 `item_id#层内序号`。  
> 理由：先进遗风 ent 层同 `item_id` 在同层内重复（同条目多实体），纯 `item_id` 会触发 `INSERT OR REPLACE` 折叠丢失记录。

---

## 4. F2 全量装载（补齐其余 4 个 adapter）✅ 已实现并实证

### 4.1 四个 adapter（实际形态与初版设计不同，按真实源数据落地）

初版设计的 `RowsAdapter/EntriesAdapter/ListAdapter/RecordsAdapter`（假设 join 是平铺容器列表）  
与真实源数据不符——实测六书的层产物是**各自分散的层文件**，且部分书的 `id` 是「按实体」复用标识。  
故改为按真实形态实现四个 adapter：

| adapter            | 书                | 真实源形态                                                              | 抽取要点 / 坑                                                                                   |
| ------------------ | ---------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `LayersAdapter`    | 先进遗风 xyf         | `data/_layers/kg_join.json`：`{fingerprints:[],layers:{key:[rec]}}` | 全量最新；无 `id` 的层用 `item_id#层内序号`                                                             |
| `VolLayerAdapter`  | 客座 kzz / 五杂俎 wzz | `_layers/<layer>_<vol>.json`，wrapper 含 `records`                   | **ID 按卷重排**（vol02 又起 `ENT-0001`）→ `local_id` 加卷前缀；跳过 `ent_alias/ent_keys/ent_index` 等非层文件  |
| `DataLayerAdapter` | 水东 sdr           | `data/<layer>/*.json`，wrapper `{volume, annotations/records}`      | ent 用 `annotations`，其余 7 层用 `records`；跳过 `ent_keys.json` 等非 wrapper；`id` 按实体复用 → 需 `#n` 去重 |
| `NormLayerAdapter` | 蘧编 qb            | `归一_<layer>.json`（跨卷单文件，`records` 列表）                              | ID 全局唯一；`归一_ents.json` 达 11MB（>旧 8MB）→ 扫描/装载上限提到 64MB                                      |
| `XgfAdapter`       | 新官 xgf           | 多份「归一_汇总」：实体/规则/流程/事件/结构(ledger/time/doc/actor/fraud)              | `id` 按实体复用（`XGF-R-008` 出现 3 次）→ `#n` 去重；事件可借 `derived_from` 反推 item_id                     |

> **统一去重**：`base.build_local_id` 产出候选 `local_id`（有 `id` 直接用、可加卷前缀；无 `id` 用 `item_id#idx`）；  
> `base.dedup_local_id` 在 `(book,layer)` 内对重复候选追加 `#1/#2/...`，保证 `(book_id,layer_key,local_id)` 唯一、  
> 零 OR-REPLACE 折叠。这是 #27 反制的具体落地。

**验收**：每书 `discover()` 返回的 Slice 数 = 该书实测层数（kzz13/wzz11/sdr8/qb8/xgf9/xyf6），且装载后 DB 内 0 个重复主键组。

### 4.2 六书全量 load

```bash
python federation.py create --db kb.sqlite
python federation.py collision           # 前置断言：撞号必须存在且被隔离
python federation.py load-all            # 按 xyf→kzz→wzz→sdr→qb→xgf 顺序六书全装
```

**验收（均通过）**：

- 撞号体检脚本通过（14302 ID / 2847 撞号 / ENT2448，全部以 `book_id` 前缀区分，零主键冲突）。
- 六书 `records=32647`、`items=3407`，与各层产物之和一致；`load_runs=6` 全 `done`。
- **折叠丢失 = 0**：`federation.py load-all` 在装载后比对「插入条数」与「去重主键数」，若有 `OR REPLACE` 折叠会告警；本次六书零折叠，跨书撞号已被复合主键完整消解。
- 全文检索（FTS5 可用时）：`fts_nodes` 可建，可搜「王守仁」并只命中含该名的书（隔离未被打破）。


## 6. F4 查询、裁决与导出（L3）——**已落地并实证（2026-10-11）**

> 落地为三个新模块 + 一套 MCP：`tools/kb-federation/{refs,curate,assoc}.py`
> 与 `tools/federation-mcp/server.py`（第三条线）。
> CLI 增 `refs`/`assoc`/`conflicts`/`lock`/`unlock`。

### 6.0 F4 的前置补丁：物化引用边（`refs.py`）

**动手前发现的硬事实**：F2 为消解撞号给 `records.local_id` 加了卷前缀与 `#n` 后缀
（`01:ENT-001#2`），但各层 payload 内的 `*_ent_ids` 仍是**裸 ID**（`ENT-001`）。
直接 join `records` 命中率实测 **0%**——所有跨层关联查询都做不出来。

解法不是回退 F2（那会把 2847 个撞号放回来），而是补一张**裸 ID 别名索引**：
`(book_id, 裸 ID) → [uid…]`，裸 ID = local_id 剥掉 `卷:` 与 `#n`。
客座/五杂俎的 `ENT-0001` 每卷都有（天然歧义），再用**同卷消歧**（引用方与被引方
通常同条同卷）解决。

| 阶段 | 引用解析率 |
| --- | --- |
| 直接 join `records` | 0% |
| 裸 ID 索引（唯一命中） | 1701 / 4605 = 37% |
| + 同卷消歧 | **3983 / 4605 = 86.5%** |

余下 218 条为真歧义。`record_refs` 表把 16 类引用字段物化成边：
`*_ent_ids` → 语义 `role`（cited/author/agent/subject/object/region…）
+ `target_text` + `target_ambiguous`。可重跑（先删后插），实测幂等。

### 6.1 名字归一补两组配置（`name_rules.json`）

关联查询暴露出两个此前没覆盖的称呼形态，按「配置驱动、不写死」原则补上：

- `wrapping_marks`：成对标记 `《》〈〉「」『』【】（）`。
  《礼记》与「礼记」是同一部书，一处带书名号一处不带，不剥就对不上。
- `work_tail_suffix`：注本尾缀 `正义/集说/集注/注疏/笺`。
  「礼记正义」是《礼记》的注本，应回落到书名本身（同样带「剩余≥2字」防误伤）。

`normalize()` 改为按 `strip_order` **泛化遍历**配置分组，不再硬编码任何具体标记。
效果实测：candidates 6589→6678、canonicals 812→824。

### 6.2 人工裁决（`curate.py`）：与「一切可重跑」共存

T3 是可重跑的（重跑会 `DELETE FROM canonical/members` 重建）。若把人工判断直接写进
`members.status`，一重跑就丢。故**裁决与派生分离**：

```
member_overrides（人工裁决，输入，只增）+  override_log（审计，只增）
canonical / members（派生，可随时重建）+  replay_overrides()（每次 transform 后重放）
```

- `lock`（确认同一人）：成员 `status='locked'`、canonical `status='locked'`，
  即便 T3 这次没并进来也强制留在簇内（人工优先于算法）。
- `reject`（解除误并）：成员移出簇成为独立节点；若簇已不足 2 人则连 canonical 一并删除，
  否则标 `status='split'` 并记 note。
- 幂等键 = uid（后写覆盖）；`undecide` 撤销回 T3 自动判定（无可撤销记录时报错，不静默成功）。

**实证**：reject 一个成员后 `members 3746→3745`、`canonicals 812→811`；
重跑 transform（回到 3746/812）→ `replay_overrides()` → 恢复 3745/811。裁决不丢。

### 6.3 十个关联查询（`assoc.py`）

设计标准四条：**有数据支撑**（跑得出非空结果）、**跨书**（单书检索用不上联邦库）、
**带出处**（每条结论可回指 `book/layer/local_id`）、**不重造轮子**（归一/置信度一律
复用 `name_resolver` + `canonical/members`）。

| # | 查询 | 价值 | 所用层 |
| --- | --- | --- | --- |
| Q1 | `identity_bridge` | 一人的跨书身份对照：各书怎么记、置信度、异文、活跃度 | canonical/members + record_refs |
| Q2 | `person_network` | 关系网按类聚合；**A 书说师徒、B 书说敌对**这类矛盾只有跨书才看得出 | edges.rel + record_refs.person_* |
| Q3 | `career_chain` | 跨书仕宦时间线（`appt.when` 排年份） | edges.appt |
| Q4 | `citation_network` | 某部书被哪些书引用、在什么条目 | record_refs.cited + cit/lit |
| Q5 | `work_author` | 作者作品，并标出**跨书共见的同名作品** | record_refs.author + lit |
| Q6 | `place_culture` | 地方志式聚合：方言风俗+名物+地理+纪事，**跨书拼才完整** | record_refs.region/location + cus/obj/geo |
| Q7 | `object_lineage` | 某名物在各书的形制/习性/传说对照 | record_refs.name + obj/nam |
| Q8 | `event_opinion` | 同一实体的事件+观点+纪事跨书并列，**显出不同立场** | event/opn/ming |
| Q9 | `parallel_reading` | 跨书对读入口：同题材条目的译文并列 | trl + record_refs 共现实体 |
| Q10 | `dangling_refs` | 未解析的名字/ID 引用——既是缺口，也是**下一本书的补录清单** | pending_refs + record_refs |

**踩过的坑（都写进代码注释了）**：
- 引用字段嵌在**子对象**里（`{"person":{"text":…,"person_ent_ids":[…]}}`），
  必须递归收集；平铺扫描会漏掉九成。
- 「科举」是 `event.type` 的**枚举分类**不是实体，Q8 只走实体引用必然返回空，
  故 Q8 需双路径（关键词匹配 + 实体引用）。
- `cross_search(limit=…)` 的 limit 是**输出条数**，不能当检索范围用——
  苏轼有 35 个 uid，`limit=2` 恰好漏掉唯一有关系边的那个。统一走 `_identity_uids()`
  （合并所有 group + 按活跃度降序）。
- 同标签实体跨卷重复（kzz 有 10 个「陈沂」），不按**活跃度**重排会漏掉真正被
  lit 层引用的那个（`kzz:01:ENT-0136`，即《金陵图》的作者）。
- Q9 各书 trl 条目**几乎无共现实体**（卷首各讲各的），跨书对读无天然轴。
  此时如实返回 `natural_alignment:false` + 各书题材指纹，**不用 item_id
  （各书卷首编号撞号但题材无关）或文本指纹（措辞必不同）硬凑**。

### 6.4 MCP 服务（`tools/federation-mcp/server.py`）

与另两条线同构：手写 JSON-RPC 2.0 over stdio，协议 2024-11-05，零第三方依赖，
server 名 `guji-federation`。工具 8 个（3 检索 + 3 关联入口 + 2 裁决）：

```
fed_books / fed_search / fed_entity
fed_assoc_list / fed_assoc（统一入口，assoc=<十选一>）
fed_conflicts / fed_lock / fed_unlock
```

写操作**仅限 `member_overrides`**（人工裁决），绝不触碰源书数据——总库只读六书。

```bash
python server.py selftest            # 18 项自检（10 个查询逐个实跑）
python server.py books
python server.py search 王忠毅公
python server.py assoc identity_bridge --arg name=苏轼
python server.py conflicts --limit 5
python server.py lock kzz:01:ENT-0136 --reason '确为同一人'
```

### 6.5 可选 Neo4j 导出

仅当需要做跨书关系网络遍历时：`nodes/edges/canonical/members` 导出为节点-关系 CSV，
导入 Neo4j 作**查询目标**而非主库。SQLite 仍是真源。

---

## 7. 执行顺序与回滚

**顺序**（严格递增依赖）：

```
F0-a 撞号体检 → F0-b 建库 → F0-c 抽象+注册表
   → F1 先进遗风 E/L 单书试点（验证隔离/指针/幂等）
   → F2 其余 4 adapter + 六书全量 load（collision 断言）
   → F3 T0-T3（先 T1 名字解析，再 T2/T3 对齐）
   → F4 query + 可选 Neo4j
```

**回滚原则**：

- Tier1/2 全可重建：`wipe_book()` 清单书即可重跑；`kb.sqlite` 不入 git，丢了从六书产物重建。
- **绝不回写六书**：任何阶段都不许 `UPDATE` 原工程目录，联邦库只读它们。
- `canonical` 的 `status='locked'` 行 T 阶段不覆盖（人工确认后的合并受保护）。

---

## 8. 与现有三条线的衔接

| 线                   | 角色       | 衔接点                                                     |
| ------------------- | -------- | ------------------------------------------------------- |
| 存量线 `kb-mcp`        | 已交付六书的体检 | `collision.py` 复刻其撞号逻辑（不重造）；`enum_drift` 用其 adapters 解析 |
| 契约线 `book-mcp`      | 新书格式约定   | 第 7 本起由 C2 带书级前缀 → 天然无撞号；`LAYER_DECL` 是新书 loader 的登记处   |
| 联邦线 `kb-federation` | 本文       | 消费六书产物，产出跨书知识库                                          |

> 联邦线**不改**任何一条既有线；它只是六书产物的「只读消费者 + 派生库」。

---

## 9. 最小可跑闭环建议

按 §7 顺序，**做到 F1 完成即回本**：

- 先进遗风安全落库、复合主键隔离验证、原文只存指针、重跑幂等——这四点证明「合并可行」。
- 再补 F0-a（撞号脚本固化）= 完整 F0+F1，足以向用户证明联邦库不是空中楼阁。
- F2–F4 是增量增强，可逐书/逐层开启，不必一次全做。
