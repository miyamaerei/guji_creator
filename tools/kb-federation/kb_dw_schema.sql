-- ============================================================
-- 古籍联邦库 · 数据仓库维度模型 DDL（kb_dw.sqlite）
-- 纯 SQLite，零第三方依赖（守项目铁律）。
--
-- 架构：星座模型（Fact Constellation）
--   - 一致性维度（总线脊柱）：dim_book / dim_layer / dim_volume /
--     dim_entity_raw / dim_entity_resolved / dim_enum_* / dim_time_year
--   - 桥表：bridge_entity_member（canonical ↔ raw 节点，多值）
--   - 事实表：f_annotation / f_relationship / f_resolution /
--             f_citation / f_drift
--   - 预聚合视图：v_entity_mentions / v_cross_book_alignment
--
-- 本库是联邦库（kb.sqlite）的纯派生，可重建、不入 git、绝不回写联邦库。
-- 每次 build_dw.py 全量 DROP+CREATE 重建（幂等）。
-- ============================================================

PRAGMA foreign_keys = OFF;

-- ============================================================
-- 一致性维度
-- ============================================================

-- 书（总线第一柱）
CREATE TABLE IF NOT EXISTS dim_book (
  book_id        TEXT PRIMARY KEY,
  code           TEXT,
  name           TEXT,
  source_root    TEXT,
  status         TEXT,
  schema_version INTEGER,
  loaded_at      TEXT
);

-- 层（含 kind 路由：node/edge/annotation/profile）
CREATE TABLE IF NOT EXISTS dim_layer (
  book_id        TEXT NOT NULL,
  layer_key      TEXT NOT NULL,
  layer_code     TEXT,
  layer_name     TEXT,
  container_kind TEXT,
  kind           TEXT,
  id_prefix      TEXT,
  status         TEXT,
  record_count   INTEGER,
  PRIMARY KEY (book_id, layer_key)
);

-- 卷（从 items/records 的 volume 字段派生；volumes 目录表当前为空）
CREATE TABLE IF NOT EXISTS dim_volume (
  book_id      TEXT NOT NULL,
  volume       TEXT NOT NULL,
  reading_mode TEXT,
  PRIMARY KEY (book_id, volume)
);

-- 实体·原始（书内 ent 节点；总线脊柱的「书内」一端）
CREATE TABLE IF NOT EXISTS dim_entity_raw (
  uid        TEXT PRIMARY KEY,   -- book_id:local_id
  book_id    TEXT,
  layer_key  TEXT,
  local_id   TEXT,
  label      TEXT,
  type       TEXT
);

-- 实体·解析后（跨书一致；canonical）
CREATE TABLE IF NOT EXISTS dim_entity_resolved (
  canonical_id TEXT PRIMARY KEY,
  repr_type    TEXT,
  repr_label   TEXT,
  status       TEXT,             -- open | locked
  member_count INTEGER,          -- 该 canonical 含多少 raw 成员
  book_span    INTEGER           -- 横跨几本书
);

-- 枚举组（雪花 outrigger，当前数据为空，待 enum-library 导入）
CREATE TABLE IF NOT EXISTS dim_enum_group (
  enum_group TEXT PRIMARY KEY,
  name       TEXT,
  version    TEXT,
  section    TEXT
);

-- 枚举值（真树：enum_group → value → parent → alias）
CREATE TABLE IF NOT EXISTS dim_enum_value (
  enum_group TEXT NOT NULL,
  value      TEXT NOT NULL,
  is_top     INTEGER,
  parent     TEXT,
  alias      TEXT,
  PRIMARY KEY (enum_group, value)
);

-- 时间（角色扮演维度；best-effort 提取 1200–1700 区间 4 位年份，稀疏）
CREATE TABLE IF NOT EXISTS dim_time_year (
  year     INTEGER PRIMARY KEY,
  dynasty  TEXT,
  century  INTEGER,
  is_ming  INTEGER
);

-- ============================================================
-- 桥表（多值）：canonical ↔ raw 节点
-- ============================================================
CREATE TABLE IF NOT EXISTS bridge_entity_member (
  canonical_id  TEXT NOT NULL,
  uid           TEXT NOT NULL,
  book_id       TEXT,             -- 从 uid 派生（uid 首段），便于按书钻取
  method        TEXT,
  confidence    REAL,
  status        TEXT,             -- auto | conflict | locked | pending
  evidence_count INTEGER,
  is_confirmed  INTEGER,          -- 1 = (auto|locked)，参与桥计数；0 = conflict/pending 排除
  PRIMARY KEY (canonical_id, uid)
);

-- ============================================================
-- 事实表（五个业务过程）
-- ============================================================

-- F1 抽取覆盖（源：records）
CREATE TABLE IF NOT EXISTS f_annotation (
  book_id         TEXT NOT NULL,
  layer_key       TEXT NOT NULL,
  local_id        TEXT NOT NULL,
  volume          TEXT,
  entity_raw_uid  TEXT,           -- 仅 ent 层：本记录即该 ent 节点
  item_id         TEXT,
  payload_bytes   INTEGER,
  ref_entity_count INTEGER,       -- payload 内 *_ent_ids 引用总数（覆盖度指标）
  has_enum_drift  INTEGER,        -- 该书该层是否出现枚举漂移
  PRIMARY KEY (book_id, layer_key, local_id)
);

-- F2 关系断言（源：edges）
CREATE TABLE IF NOT EXISTS f_relationship (
  book_id           TEXT NOT NULL,
  layer_key         TEXT NOT NULL,
  local_id          TEXT NOT NULL,
  volume            TEXT,
  predicate         TEXT,
  subject_raw_uid   TEXT,
  object_raw_uid    TEXT,
  subject_resolved  TEXT,         -- 经桥表升到的 canonical_id（可空）
  object_resolved   TEXT,
  event_year        INTEGER,      -- best-effort 年份（稀疏）
  is_resolved       INTEGER,      -- 主宾都解析到节点 = 1
  PRIMARY KEY (book_id, layer_key, local_id)
);

-- F3 实体解析（源：members，即桥表的「事实版」）
CREATE TABLE IF NOT EXISTS f_resolution (
  canonical_id   TEXT NOT NULL,
  uid            TEXT NOT NULL,
  book_id        TEXT,
  method         TEXT,
  confidence     REAL,
  status         TEXT,
  evidence_count INTEGER,
  PRIMARY KEY (canonical_id, uid)
);

-- F4 引用物化（源：record_refs）
CREATE TABLE IF NOT EXISTS f_citation (
  ref_id          TEXT PRIMARY KEY,
  book_id         TEXT,
  layer_key       TEXT,
  local_id        TEXT,
  field           TEXT,
  ref_index       INTEGER,
  volume          TEXT,
  role            TEXT,
  target_raw_uid  TEXT,           -- 引用的目标节点 uid
  target_resolved TEXT,           -- 经桥表升到的 canonical_id（可空）
  target_ambiguous INTEGER,
  item_id         TEXT
);

-- F5 枚举漂移（源：enum_drift，当前为空）
CREATE TABLE IF NOT EXISTS f_drift (
  book_id     TEXT NOT NULL,
  layer_key   TEXT,
  field       TEXT,
  enum_group  TEXT,
  value       TEXT,
  drift_count INTEGER,
  in_library  INTEGER,
  PRIMARY KEY (book_id, layer_key, field, enum_group, value)
);

-- ============================================================
-- 增量水印（数仓侧）
-- ============================================================
-- dw_watermark：每本书最近一次被数仓装载时对应的源库装载完成时刻。
-- 增量 build 时与 kb.sqlite 的 load_runs.finished_at 比对：
--   若某书最新 finished_at 晚于 last_loaded_at（或无记录），该书需重建；
--   否则跳过其重的 per-book 抽取（跨书解析层仍全局刷新以保证一致）。
CREATE TABLE IF NOT EXISTS dw_watermark (
  book_id       TEXT PRIMARY KEY,
  last_loaded_at TEXT,            -- 对应的 load_runs.finished_at
  built_at      TEXT              -- 本次数仓构建时刻
);

-- ============================================================
-- 索引（加速 drill-across / 一致性事实查询）
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_fa_layer ON f_annotation(book_id, layer_key);
CREATE INDEX IF NOT EXISTS idx_fa_ent    ON f_annotation(entity_raw_uid);
CREATE INDEX IF NOT EXISTS idx_fr_subj   ON f_relationship(subject_raw_uid);
CREATE INDEX IF NOT EXISTS idx_fr_obj    ON f_relationship(object_raw_uid);
CREATE INDEX IF NOT EXISTS idx_fr_res    ON f_relationship(subject_resolved);
CREATE INDEX IF NOT EXISTS idx_fc_tgt    ON f_citation(target_raw_uid);
CREATE INDEX IF NOT EXISTS idx_fc_res    ON f_citation(target_resolved);
CREATE INDEX IF NOT EXISTS idx_fres_can  ON f_resolution(canonical_id);
CREATE INDEX IF NOT EXISTS idx_bridge_uid ON bridge_entity_member(uid);

-- ============================================================
-- 预聚合视图（一致性事实 realized）
-- ============================================================

-- 每个跨书实体，在三个过程里的「被提及次数」（conformed fact: mention_count）
CREATE VIEW IF NOT EXISTS v_entity_mentions AS
SELECT
  r.canonical_id,
  r.repr_label,
  r.repr_type,
  r.book_span,
  r.member_count,
  (SELECT COUNT(*) FROM f_annotation fa
     JOIN bridge_entity_member b ON b.uid = fa.entity_raw_uid
     WHERE b.canonical_id = r.canonical_id AND b.is_confirmed = 1) AS mention_annotation,
  (SELECT COUNT(*) FROM f_relationship fr
     WHERE fr.subject_resolved = r.canonical_id
        OR fr.object_resolved = r.canonical_id)                    AS mention_relationship,
  (SELECT COUNT(*) FROM f_citation fc
     WHERE fc.target_resolved = r.canonical_id)                    AS mention_citation
FROM dim_entity_resolved r;

-- 跨书对齐总览（实体跨哪几本书、是否锁定）
CREATE VIEW IF NOT EXISTS v_cross_book_alignment AS
SELECT
  r.canonical_id,
  r.repr_label,
  r.repr_type,
  r.status,
  r.member_count,
  r.book_span,
  GROUP_CONCAT(DISTINCT b.book_id) AS book_ids
FROM dim_entity_resolved r
JOIN bridge_entity_member b
  ON b.canonical_id = r.canonical_id AND b.is_confirmed = 1
GROUP BY r.canonical_id, r.repr_label, r.repr_type, r.status, r.member_count, r.book_span;
