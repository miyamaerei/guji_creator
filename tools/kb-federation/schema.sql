-- ============================================================
-- 古籍联邦库 schema —— 跨书合并 SQLite 数据库
-- 纯标准库 sqlite3 兼容（零第三方依赖，守项目铁律）
--
-- 三层存储：
--   Tier 0  联邦目录   books / book_meta / layer_catalog / layer_fields —— 扩展点（新书/新层只插这里）
--   Tier 1  忠实装载   items / records                        —— 无损、真源、原文只存指针
--   Tier 2  派生图谱   nodes / edges / canonical / members /  —— 可重建、不入 git
--                       candidate_links / pending_refs
--   枚举/校验  enum_registry / enum_values / enum_drift
--   辅助      volumes / load_runs / federation_meta / fts_nodes(可选)
--
-- 扩展原则：schema 固定不变。第 7 本起的新书、以及任何新层（C13…）
--   只往 layer_catalog / layer_fields 插行即可，T 阶段按目录自动抽取，
--   无需 ALTER TABLE、无需改任何 loader 逻辑。
-- ============================================================

PRAGMA foreign_keys = OFF;   -- 目录驱动，loader 自管写入顺序（先删后插幂等）

-- ============================================================
-- Tier 0：联邦目录（扩展点）
-- ============================================================

-- 书登记表：每本书一个书级命名空间（复合主键的第一段）
CREATE TABLE IF NOT EXISTS books (
  book_id        TEXT PRIMARY KEY,       -- 'kzz'/'wzz'/... 书级前缀
  code           TEXT,                  -- 内部代号
  name           TEXT,                  -- 客座赘语
  source_root    TEXT,                  -- 工程目录（相对仓库根）
  status         TEXT DEFAULT 'active', -- active | deprecated
  schema_version INTEGER,               -- 本书产物版本号
  loaded_at      TEXT,                  -- 最近装载时间（ISO8601）
  checksum       TEXT,                  -- 内容指纹（records 级，books 级未启用）
  source_rev     TEXT                   -- 源工程目录的 git rev / 快照 id（增量水印；见 §增量）
);

-- 著录元数据（C8 消费侧）：一书的「谁写的/什么朝代/什么体裁」书级一句话档案。
-- 真源是各书 <书>/书籍json/<书>_校对版.json 的 meta 块（book-json/1.1 就地载体），
-- 本表只是它的扁平化副本，便于 SQL 直接按朝代/体裁筛选跨书统计。
CREATE TABLE IF NOT EXISTS book_meta (
  book_id    TEXT PRIMARY KEY,
  name       TEXT NOT NULL,             -- 书名（与 books.name 一致，便于单独查看本表）
  dynasty    TEXT NOT NULL,             -- 朝代：明 / 清 / …
  author     TEXT NOT NULL,             -- 作者；集体著作可写「某某等」；不详写「佚名」
  genre      TEXT NOT NULL,             -- 体裁（短语）：笔记 / 政书 / 年谱 / 官箴书 / 志书 / 遗闻录
  subject    TEXT NOT NULL,             -- 主题一句话
  source     TEXT NOT NULL,             -- 著录依据（书目/工具书/仓库内配置）
  confidence TEXT NOT NULL DEFAULT 'high', -- high / medium / low；无把握置 low 不臆造
  note       TEXT,                      -- 附注（卷数诸本不一、库内数据问题等）
  updated_at TEXT NOT NULL
);

-- 层目录：声明「某书有哪些层、各层是什么形态」
-- 新层 = 在这里插一行，T 阶段据 kind 自动决定抽成 node 还是 edge
CREATE TABLE IF NOT EXISTS layer_catalog (
  book_id        TEXT NOT NULL,
  layer_key      TEXT NOT NULL,         -- 归一后的 key：'ent'/'appt'/'evt'/...
                                        --   本列是联邦侧唯一层码口径：一律单数。盘上目录/文件名
                                        --   可为复数（qb/shz/zgz 的 ents/structs…），复数原形只记在
                                        --   adapters 的 LAYER_DIR_NAMES，看板按盘上形显示——两者不是漂移。
  layer_code     TEXT,                  -- 层库原编号：'L1'/'C1'/...
  layer_name     TEXT,                  -- 实体层 / 职官任职层
  container_kind TEXT,                  -- rows|list|entries|records|fingerprints
  kind           TEXT DEFAULT 'annotation', -- node | edge | annotation | profile
  id_prefix      TEXT,                  -- 本书实际 ID 前缀：'ENT-'/'APPT-'/...
  status         TEXT DEFAULT 'enabled',
  record_count   INTEGER,
  loaded_at      TEXT,
  PRIMARY KEY (book_id, layer_key),
  FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- 层字段目录：声明每层的字段语义（哪些字段是实体引用、哪些是枚举）
-- T 阶段据此把边解析到节点、把枚举值送去做漂移校验。新字段 = 插一行。
CREATE TABLE IF NOT EXISTS layer_fields (
  book_id        TEXT NOT NULL,
  layer_key      TEXT NOT NULL,
  field_name     TEXT NOT NULL,         -- 'person_a'/'who'/'cited_work'/...
  field_type     TEXT DEFAULT 'text',   -- text | json | id
  role           TEXT DEFAULT 'attr',   -- node_ref | enum | attr | id | time
  ref_layer      TEXT,                  -- role=node_ref 时指向的层 key（一般 'ent'）
  enum_group     TEXT,                  -- role=enum 时指向的枚举组（'EVENT'/'OFFICE'/...）
  PRIMARY KEY (book_id, layer_key, field_name),
  FOREIGN KEY (book_id, layer_key) REFERENCES layer_catalog(book_id, layer_key)
);

-- ============================================================
-- Tier 1：忠实装载（无损，真源）
-- ============================================================

-- 条目锚点：只存指针，不抄正文（守「原文只在指纹库」铁律）
CREATE TABLE IF NOT EXISTS items (
  book_id        TEXT NOT NULL,
  item_id        TEXT NOT NULL,         -- 本地 item_id（NN-NNN），不带书前缀
  volume         TEXT,
  title          TEXT,
  fingerprint_ref TEXT,                 -- 指向 _item_registry 的键（回查原文用）
  layer_count    INTEGER,
  PRIMARY KEY (book_id, item_id),
  FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- 层记录总表：每一层的每一条记录原样入库（JSON 无损）
-- 这是「所有的层」的统一落点 —— 新增任何层都不会改这张表的结构
CREATE TABLE IF NOT EXISTS records (
  book_id        TEXT NOT NULL,
  layer_key      TEXT NOT NULL,
  local_id       TEXT NOT NULL,         -- 本书层内 ID（ENT-001 / APPT-001 / ...）
  item_id        TEXT,                  -- 关联条目（跨层索引等可为空）
  volume         TEXT,
  payload        TEXT NOT NULL,         -- 整条记录的 JSON 原文
  checksum       TEXT,
  loaded_at      TEXT,
  PRIMARY KEY (book_id, layer_key, local_id),
  FOREIGN KEY (book_id, layer_key) REFERENCES layer_catalog(book_id, layer_key)
);
CREATE INDEX IF NOT EXISTS idx_records_item      ON records(book_id, item_id);
CREATE INDEX IF NOT EXISTS idx_records_booklayer ON records(book_id, layer_key);

-- ============================================================
-- Tier 2：派生知识图谱（可重建，不入 git）
-- ============================================================

-- 节点：当前仅 ent；未来任何 kind='node' 的层自动落入此表
-- 所有跨书可对齐的对象（人/地/书/名物/机构/概念）都是 node，靠 type 区分
CREATE TABLE IF NOT EXISTS nodes (
  uid            TEXT PRIMARY KEY,       -- 'kzz:ENT-001' = book_id:local_id
  book_id        TEXT NOT NULL,
  layer_key      TEXT NOT NULL,
  local_id       TEXT NOT NULL,
  label          TEXT,                  -- 显示名
  type           TEXT,                  -- person|place|book|object|institution|concept|...
  payload        TEXT,                  -- 该节点的归一层 JSON（normalized/alias 等）
  FOREIGN KEY (book_id, layer_key, local_id) REFERENCES records(book_id, layer_key, local_id)
);
CREATE INDEX IF NOT EXISTS idx_nodes_label ON nodes(label);
CREATE INDEX IF NOT EXISTS idx_nodes_type  ON nodes(type);

-- 边：关系层 / 引用层（REL/APPT/EVT/CIT/LIT/OBJ/CUS/NAM/MING/MEM/CHR）
-- subject/object 经 T1（名字→ent_id）解析为节点 uid；解析失败则留 *_pending
CREATE TABLE IF NOT EXISTS edges (
  uid            TEXT PRIMARY KEY,       -- book_id:layer_key:local_id
  book_id        TEXT NOT NULL,
  layer_key      TEXT NOT NULL,
  local_id       TEXT NOT NULL,
  predicate      TEXT,                  -- relation_type / office / cited_work / region / ...
  subject_uid    TEXT,                  -- 解析后节点 uid（可空=待决）
  object_uid     TEXT,
  subject_pending TEXT,                  -- 解析失败时的原始名字（进 pending_refs 复制）
  object_pending  TEXT,
  payload        TEXT,
  FOREIGN KEY (book_id, layer_key, local_id) REFERENCES records(book_id, layer_key, local_id)
);
CREATE INDEX IF NOT EXISTS idx_edges_subject ON edges(subject_uid);
CREATE INDEX IF NOT EXISTS idx_edges_object  ON edges(object_uid);
CREATE INDEX IF NOT EXISTS idx_edges_pred    ON edges(predicate);

-- 跨书等价代表：一个 canonical = 一组「同一对象」的成员
CREATE TABLE IF NOT EXISTS canonical (
  canonical_id   TEXT PRIMARY KEY,       -- 'canon-0001'
  repr_type      TEXT,
  repr_label     TEXT,
  status         TEXT DEFAULT 'open',    -- open | locked（人工确认后锁，防 T 覆盖）
  created_at     TEXT,
  note           TEXT
);

-- 成员：去歧义合并的结果（物理不合并，只建链接）
CREATE TABLE IF NOT EXISTS members (
  canonical_id   TEXT NOT NULL,
  uid            TEXT NOT NULL,          -- 成员节点 uid
  method         TEXT,                  -- exact | alias | relation
  confidence     REAL,
  status         TEXT DEFAULT 'auto',    -- auto | conflict | pending | locked
  evidence_count INTEGER DEFAULT 0,
  PRIMARY KEY (canonical_id, uid),
  FOREIGN KEY (canonical_id) REFERENCES canonical(canonical_id),
  FOREIGN KEY (uid) REFERENCES nodes(uid)
);

-- 候选链接：T2/T3 中间产物（精确 + 别名 + 关系传播后的候选对）
CREATE TABLE IF NOT EXISTS candidate_links (
  a_uid          TEXT NOT NULL,
  b_uid          TEXT NOT NULL,
  method         TEXT,
  confidence     REAL,
  supporting_edges INTEGER DEFAULT 0,
  PRIMARY KEY (a_uid, b_uid)
);

-- 待决引用：名字在 ent_keys 查不到，边悬空，留待人工补实体
CREATE TABLE IF NOT EXISTS pending_refs (
  book_id        TEXT NOT NULL,
  layer_key      TEXT NOT NULL,
  local_id       TEXT NOT NULL,
  field          TEXT,
  raw_name       TEXT,
  reason         TEXT,
  created_at     TEXT
);

-- ============================================================
-- Tier 2b：物化引用（F4）
-- 上面 edges 装的是「关系层」（rel/appt/event 等有语义谓词的边）。
-- 但各层 payload 内部还有大量 *_ent_ids 结构化引用（cit.cited_ent_ids /
-- lit.author_ent_ids / obj.name_ent_ids / ming.who_ent_ids …），
-- 若只在查询时现解 JSON 则无法走 SQL 索引。这里把它们物化成边。
-- ============================================================

-- 记录 → 实体 的引用边（payload 内 *_ent_ids 的展开）
-- 注意：payload 里的 ent_id 是「裸 ID」（如 ENT-0001），而 records.local_id
--   因 F2 加卷前缀/去重后可能是 '01:ENT-0001' / '01:ENT-001#2'。
--   故本表的 target_uid 可能对应多个候选（见 target_ambiguous），
--   查询端用 CANONICAL 归一后的 nodes 判同。
CREATE TABLE IF NOT EXISTS record_refs (
  ref_id         TEXT PRIMARY KEY,       -- book_id:layer_key:local_id:field#n
  book_id        TEXT NOT NULL,
  layer_key      TEXT NOT NULL,
  local_id       TEXT NOT NULL,         -- 引用方记录
  field          TEXT NOT NULL,         -- 'cited_ent_ids'/'author_ent_ids'/...
  role           TEXT,                  -- 语义角色：cited/author/agent/subject/...
  raw_target     TEXT NOT NULL,         -- payload 里的裸 ID
  target_text    TEXT,                  -- 同一对象里的可读名（若随行）
  target_uid     TEXT,                  -- 解析到的 nodes.uid（唯一时）
  target_ambiguous INTEGER DEFAULT 0,   -- 1 = 裸 ID 跨卷重名，未唯一解析
  item_id        TEXT,
  volume         TEXT,
  FOREIGN KEY (book_id, layer_key, local_id) REFERENCES records(book_id, layer_key, local_id)
);
CREATE INDEX IF NOT EXISTS idx_refs_target ON record_refs(target_uid);
CREATE INDEX IF NOT EXISTS idx_refs_field  ON record_refs(field);
CREATE INDEX IF NOT EXISTS idx_refs_src    ON record_refs(book_id, layer_key, local_id);

-- ============================================================
-- Tier 2c：人工裁决（F4）
-- T3 自动消歧会产生同名异人的误并（status='conflict'）。
-- 人工裁决必须【独立于 transform 可重跑】——否则一重跑就被覆盖。
-- 故裁决单独存表，transform 之后由 replay_overrides() 重放。
-- ============================================================

-- 人工裁决：锁定（确认同一人，确认合并）/ 解除（确认不同人，拆出）
--   action = 'lock'   → 成员强制留在 canonical，status 置 'locked'，T3 不得拆
--   action = 'reject' → 成员移出 canonical 成为独立节点，status 置 'rejected'
-- 幂等键 (uid)：一个 uid 至多一条有效裁决，后写覆盖先写。
CREATE TABLE IF NOT EXISTS member_overrides (
  uid            TEXT PRIMARY KEY,       -- 被裁决的 nodes.uid
  action         TEXT NOT NULL,          -- lock | reject
  canonical_id   TEXT,                  -- lock 时所属 canonical；reject 时记原属
  reason         TEXT,
  decided_by     TEXT,
  decided_at     TEXT,
  created_at     TEXT
);

-- 裁决审计日志（只增不改）
CREATE TABLE IF NOT EXISTS override_log (
  log_id         INTEGER PRIMARY KEY AUTOINCREMENT,
  uid            TEXT,
  action         TEXT,
  canonical_id   TEXT,
  reason         TEXT,
  decided_by     TEXT,
  decided_at     TEXT
);

-- ============================================================
-- 枚举与校验
-- ============================================================

-- 枚举组注册（镜像 enum-library 的组元信息）
CREATE TABLE IF NOT EXISTS enum_registry (
  enum_group     TEXT PRIMARY KEY,       -- 'EVENT'/'OFFICE'/...
  name           TEXT,
  version        TEXT,
  section        TEXT
);

-- 枚举值（顶层值 / 子类值 / 别名）—— 从 enum-library 一次性导入，派生可重建
CREATE TABLE IF NOT EXISTS enum_values (
  enum_group     TEXT NOT NULL,
  value          TEXT NOT NULL,
  is_top         INTEGER DEFAULT 0,
  parent         TEXT,
  alias          TEXT,
  PRIMARY KEY (enum_group, value),
  FOREIGN KEY (enum_group) REFERENCES enum_registry(enum_group)
);

-- 枚举漂移：数据里用到、但库里没有的值（治理用，对应 #27）
CREATE TABLE IF NOT EXISTS enum_drift (
  book_id        TEXT NOT NULL,
  layer_key      TEXT,
  field          TEXT,
  enum_group     TEXT,
  value          TEXT,
  in_library     INTEGER,
  count          INTEGER DEFAULT 1,
  PRIMARY KEY (book_id, layer_key, field, enum_group, value)
);

-- ============================================================
-- 辅助表
-- ============================================================

-- 卷阅读模式索引（V1，profile 层，不占 ID 命名空间）
CREATE TABLE IF NOT EXISTS volumes (
  book_id        TEXT NOT NULL,
  volume         TEXT NOT NULL,
  dominant_type  TEXT,
  secondary_type TEXT,
  reading_mode   TEXT,
  basis          TEXT,
  PRIMARY KEY (book_id, volume)
);

-- 装载运行日志（幂等 / 审计）
CREATE TABLE IF NOT EXISTS load_runs (
  run_id         INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id        TEXT,
  started_at     TEXT,
  finished_at    TEXT,
  status         TEXT,
  record_counts  TEXT                   -- JSON：各层条数
);

-- 联邦元信息（schema 版本号等）
CREATE TABLE IF NOT EXISTS federation_meta (
  key            TEXT PRIMARY KEY,
  value          TEXT
);

-- ============================================================
-- 全文索引（可选，派生可重建）
-- 仅当 sqlite3 编译含 FTS5 时由 loader 创建；缺失则跳过，不影响其余表
-- ============================================================
-- CREATE VIRTUAL TABLE IF NOT EXISTS fts_nodes
--   USING fts5(uid UNINDEXED, label, normalized, raw_name);
