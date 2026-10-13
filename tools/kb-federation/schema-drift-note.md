# 联邦库 schema 漂移与稀疏诊断补充说明

> 位置：`tools/kb-federation/schema-drift-note.md`
> 配套文档：`docs/联邦库原表增量与稀疏诊断.md`（原表增量/稀疏主报告）、`docs/数据仓库设计.md`
> 数据基准：`kb.sqlite`（实测于本次盘点，9 书 / 37100 records / 20158 nodes / 1113 canonical）

本说明只**记录现状**，不修改 `schema.sql`。用户已明确「`canonical.note` 先不写」，故 `note` 列保持空。

---

## 0. 一句话结论

`schema.sql` 的声明与 `kb.sqlite` 实表**大体一致**（本次只新增了 `books.source_rev`，
见 §4）。真正的「漂移」不在表结构本身，而在三处**语义/落点错位**：

1. `nodes` 没有 `normalized` / `text` 列，但注释掉的 `fts_nodes` 却引用了它们 → FTS 定义与实表脱节。
2. 枚举「哪层哪个字段走哪个枚举组」这一关系**只活在 Python 硬编码**（`enum_import.LAYER_ENUM_FIELDS`），库内没有 `enum_fields` 注册表。
3. `books` 缺作者/朝代/卷数等书目元数据列，`edges` 缺 `volume` 列 —— 二者按需下钻时只能解析 `payload` JSON。

另有若干「看着像稀疏、其实是设计如此」的表（见 §3），以及一批本次盘点残留的临时脚本（见 §5）。

---

## 1. 实表列普查（权威快照）

下列为 `PRAGMA table_info` 实测，非读 schema.sql 推断：

| 表 | 实际列 | 备注 |
| --- | --- | --- |
| `books` | book_id, code, name, source_root, status, schema_version, loaded_at, checksum, **source_rev** | name=书名；无 author/dynasty/title 分列 |
| `nodes` | uid, book_id, layer_key, local_id, label, type, payload | **无 normalized / text 列**（见 D1） |
| `edges` | uid, book_id, layer_key, local_id, predicate, subject_uid, object_uid, subject_pending, object_pending, payload | **无 volume 列**（见 D5） |
| `canonical` | canonical_id, repr_type, repr_label, status, created_at, **note** | note 100% 空（见 D2） |
| `enum_registry` | enum_group, name, version, section | 19 组 |
| `enum_values` | enum_group, value, is_top, parent, alias | 402 值（顶层 296） |
| `enum_drift` | book_id, layer_key, field, enum_group, value, in_library, count | 1308 行 |
| `records` | book_id, layer_key, local_id, item_id, volume, payload, checksum, loaded_at | 有 volume |
| `volumes` | book_id, volume, dominant_type, secondary_type, reading_mode, basis | 116 行 |
| `load_runs` | run_id, book_id, started_at, finished_at, status, record_counts | 9 行 |

---

## 2. 漂移清单（D1–D8）

### D1 · `nodes` 缺 `normalized` / `text`，且 `fts_nodes` 定义悬空
- `nodes` 只有 `label` / `type` / `payload` 三列。跨书归一所需的 `normalized` 与 `text` 并不落表——
  归一完全靠 `name_resolver.py` **运行时从 `records.payload` 现抽**，配置文件是 `name_rules.json`。
- `schema.sql` 第 317–318 行那段注释掉的
  `CREATE VIRTUAL TABLE fts_nodes USING fts5(uid UNINDEXED, label, normalized, raw_name)`
  **引用了 `normalized` 和 `raw_name` 两个根本不存在的列**。若日后直接 `CREATE` 这段，会立刻报「no such column」。
- 结论：要么给 `nodes` 补 `normalized` / `raw_name` 列再启用 FTS5，要么把 fts 定义改成只索引 `label` +
  从 `payload` 提取，二者必须对齐。

### D2 · `canonical.note` 100% 空
- 实测 1113 行 canonical，**0 行**有非空 note。该列是预留的治理备注位，目前未用。
- 按用户指示「note 先不写」，本说明**不回填**任何 note。

### D3 · 枚举字段映射未固化进库（只有 Python 硬编码）
- 早期文档称「`enum_groups`」，实表已改名为 `enum_registry` + `enum_values` + `enum_drift`（命名已对齐，非漂移）。
- 但「**哪层哪个字段走哪个枚举组**」这一关键关系**没有 DB 表**承载：
  - `layer_fields` 表有 `role='enum'` 和 `enum_group` 列，理论上应承载它；
  - 实际 `layer_fields` 里的 `enum_group` 并未被 `enum_import` 消费——映射靠
    `enum_import.py` 里的 `LAYER_ENUM_FIELDS` 字典（25 层硬编码）。
- 建议：把 `LAYER_ENUM_FIELDS` 落成 `layer_fields.enum_group` 的真实数据，或新增一张
  `enum_fields(book_id, layer_key, field, enum_group)` 注册表，让「层→字段→枚举组」进库、可查询，
  而非散落在 Python。

### D4 · `books` 缺作者 / 朝代 / 卷数等书目元数据列
- 现有 `books` 只有 `name`（书名）和 `code`（内部代号）。作者、朝代、总卷数等没有结构化列。
- 目前在 Python 侧用 `BOOK_NAMES` / `BOOK_REGISTRY` 补丁式携带，未落库。
- 代价提示：加列需 `ALTER TABLE`（会破「schema 固定不变」铁律一次，已为 `source_rev` 破例过一次）。
  若要做书目检索（按朝代筛书），建议在 Tier0 加 `author / dynasty / vol_count` 三列。

### D5 · `edges` 无 `volume` 列
- 关系按「卷」下钻时，`volume` 信息只埋在 `payload` JSON 里（部分层有，部分没有）。
- `records` 表有独立的 `volume` 列，但 `edges` 没有冗余卷列 → 按卷过滤边必须 `json_extract(payload, ...)`。
- 代价提示：加 `volume` 列需 `ALTER`，且需在 `refs.py` / `transform.py` 写边时顺手填。

### D6 · `time` 无联邦库专属持久表
- 时间信息散落在 `records.payload` 与各层的 date 字段，联邦库没有独立 time 维表。
- 时间维只在**数仓侧**物化为 `dim_time_year`（501 年）。这是设计选择（时间不在联邦做归一），
  但与「Tier2 派生图谱」的命名容易让人误以为库内有时间维。

### D7 · `checksum` 两级用途不一致
- `books.checksum` 注释写「books 级未启用」（实测确实为空）。
- `records.checksum` 已逐条启用（37100 条都有）。
- 增量水印改用 `books.source_rev`（git rev / dir hash）替代 books 级 checksum，见 §4。

### D8 · 本次盘点残留临时脚本
- `_calib.py` / `_fields.py` / `_fields2.py` / `_chk.py` 是本次枚举漂移校准用的临时诊断脚本，
  **未入库（untracked）**。应清理或移入 `_tmp/`，避免混进工程目录。
  （已在 git status 中标记为 `??`，可安全删除。）

---

## 3. 稀疏表观察（多数「看着稀疏，实为设计」）

| 表 | 行数 | 是否稀疏 | 说明 |
| --- | --- | --- | --- |
| `enum_drift` | 1308 | **假性稀疏** | 绝大多数是 `cit.context→CIT_CONTEXT`（407 行），而 CIT_CONTEXT 在 `enum-library` 里本就是**自由文本（引用书目名）**，不该当封闭枚举校验 → 治理噪音，建议降级为「建议值」而非「封闭校验」（见 §6 R3） |
| `pending_refs` | 838 | **真缺口** | 悬空引用，名字在 ent_keys 查不到、边悬空，待补实体 |
| `record_refs` (target_ambiguous=1) | 218 | **真歧义** | 跨卷重名裸 ID 未唯一解析（历史已知坑） |
| `edges` | 1699 | **设计如此** | 语义谓词层（rel/appt/event/cit…）；payload 内 `*_ent_ids` 已另物化为 `record_refs`（4605） |
| `volumes` | 116 | 不稀疏 | 9 书 × 各卷阅读模式索引（profile 层摘要） |
| `load_runs` | 9 | 不稀疏 | 每本 1 行，作增量水印源足够 |
| `canonical` / `members` | 1113 / 4780 | 丰满 | 消歧合并骨架完整 |

**结论**：联邦库没有结构性稀疏表。唯一需要治理的是 `enum_drift` 的「误报噪音」（CIT_CONTEXT 类），
和 `pending_refs` / `record_refs.target_ambiguous` 的真实数据缺口（补实体 / 人工裁决）。

---

## 4. 本轮回填 / 新增的能力（已落地，非漂移）

### T8 · 枚举漂移管线重写（`enum_import.py`）
- 重写解析器：支持多分隔符切分 + **括号深度保护**（别名如 `民俗（别名：习俗 / 礼俗）` 不再被切断）、
  树形 `顶层 ─ 子类`、§1.3.3 归并表排除、§1.15 双组（CIT_TYPES + CIT_CONTEXT）解析。
- `LAYER_ENUM_FIELDS` 覆盖 25 层 → 19 枚举组映射。
- 实测：groups=19，values=402（顶层 296），drift=1308 行且 **0 脏值**（此前因解析 bug 大量误报）。
- 最大真实漂移（供治理优先级）：
  `cit.context→CIT_CONTEXT` 407（自由文本，非真漂移）· `appt.status→APPT_STATUS` 203 ·
  `rel.relation_type→REL_TYPES` 190 · `opn.stance→OPN_STANCES` 94 · `event.type→EVENT_TYPES` 88 ·
  `cit.citation_type→CIT_TYPES` 83 · `ming.category→MING_TYPES` 77 · `lit.type→LIT_TYPES` 63 ·
  `obj.category→OBJ_TYPES` 30 · `cus.type→CUS_TYPES` 21 · `nam.category→NAM_TYPES` 17 ·
  `rule.type→RULE_TYPES` 13（中英混）· `evt.type→EVENT_TYPES` 10（英文）· `geo.category→GEO_TYPES` 8 ·
  `reg.type→REG_TYPES` 2 · `trl.style→TRL_STYLES` 1 · `ent.type→ENTITY_TYPES` 1（document 英文 vs 中文 doc）。

### T9 · 数仓增量水印（`kb_dw_schema.sql` + `build_dw.py`）
- 新增 `dw_watermark(book_id, last_loaded_at, built_at)`。
- `build_dw.py` 比对 `load_runs.finished_at`（每本 MAX）与 watermark，算出「需重建集合」；
  支持 `--full` 全量 + 默认增量（无变化则「已是最新」no-op）。
- 实测：全量基线建好 11 张表（dim_book=9 / dim_layer=72 / dim_volume=140 / dim_entity_raw=20158 /
  dim_entity_resolved=1113 / dim_enum_group=19 / dim_enum_value=402 / dim_time_year=501 /
  bridge_entity_member=4780 / f_annotation=37100 / f_relationship=1699 / f_resolution=4780 /
  f_citation=4605 / f_drift=1308）；ysz 单本 bump `finished_at`→2099 触发「1 本增量重建」。

### source_rev 回填（`books.source_rev` + `federation.py source-rev`）
- `books` 表已加 `source_rev TEXT`（schema.sql L34）。
- `load.py` 的 `source_rev(book_id)`：优先 `git -C <root> log -1 --format=%H -- <dir>`，
  无 git 或目录变更则用 `dir:<md5>` 兜底。
- `federation.py` 新增 `source-rev` 子命令（`--db` / `--force`）回填。
- 实测 9 本全部填入：kzz/qb/wzz/xgf 共享 git `3021c2cc…`；sdr `c06a3db…`；xyf `720b4b34…`；
  lgs `dir:34278cdb…`、xzl `dir:a6f531a9…`、ysz `dir:a07b20ad…`（三本无统一 git 根，走 dir hash）。

---

## 5. 给用户的「想办法添加」清单（按代价排序）

| 项 | 改动 | 破 schema 铁律？ | 建议 |
| --- | --- | --- | --- |
| R1 `books.author` / `books.dynasty` / `books.vol_count` | ALTER + 填数据 | 是（同 source_rev 已破例） | 若需按朝代/作者检索书目则加 |
| R2 `edges.volume` | ALTER + `refs.py`/`transform.py` 填卷 | 是 | 若频繁按卷下钻关系统加 |
| R3 `CIT_CONTEXT` 降级为「建议值」 | 仅改 `enum_import` 校验逻辑 | 否 | **强烈建议**：消除 407 行治理噪音 |
| R4 `enum_fields` 注册表 | 新建表 + 迁移 `LAYER_ENUM_FIELDS` | 否（扩展点） | 让「层→字段→枚举组」进库可查 |
| R5 启用 FTS5 | 先补 `nodes.normalized/raw_name` 或改写 fts 定义 | 否（派生可重建） | 搜索性能需求时做，先对齐 D1 |
| R6 `canonical.note` 回填 | 仅写数据 | 否 | **用户已说先不写**，暂缓 |
| R7 清理 `_calib/_fields/_fields2/_chk.py` | 删 untracked 文件 | 否 | 立即清理，避免混进工程目录 |

> 说明：R1/R2 涉及 ALTER，与「schema 固定不变」铁律冲突，需你拍板是否接受破例；
> R3/R4/R5/R7 都在现有扩展原则内，可随时动手。

---

## 6. 本次未做（明确 defer）

- **不写 `canonical.note`**：用户明确「note 先不写」，保持 100% 空。
- **不动 `schema.sql` 结构**：本说明仅记录，所有 ALTER 类改动（R1/R2）待你确认。
- **不重建枚举漂移历史**：`enum_drift` 已重算为干净值，未删旧行（幂等 DELETE+INSERT 已覆盖）。
