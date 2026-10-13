# 《先进遗风》知识工程基准管线（scripts/）

基于本实例技能（SKILL.md §0 六层 + §10 管线验证）搭建的可复用、可重跑基准代码。
**用途**：把「底座构建 → 启用层逐层抽取 → 跨层整合 → 校验交付」四阶段固化为脚本，
使每卷装填、每次重跑、每个验收都有确定入口与可审计产物。

---

## 1. 工程结构

```
05-xianjinyifeng-knowledge/
├── SKILL.md                        技能契约（六层定义、管线、交付约定）
├── references/schemas.md           数据 schema（ID 命名、字段、枚举快照）
├── assets/sources/先进遗风_全本.txt  唯一权威源（annotate 只读它）
└── scripts/                        本基准代码
    ├── _kg_config.py               配置单点：路径/卷映射/段容量/层注册/期望条数
    ├── _kg_enums.py                枚举单点：六封闭集+别名+registerVersion
    ├── _kg_pack_base.py            公共基座：原子写/指纹库/ID段位/original注入/
    │                                源数据加载/枚举校验/增量合并/CSV逻辑行
    ├── _kg_layer_builder.py        通用层构建引擎（appt/rel/event/opn/trl 复用）
    ├── annotate.py                 底座：全本 -> 分卷条目 + 指纹库(100条)
    ├── build_ent_keys.py           L1 实体（组级ID + alias_index + 跨卷归并）
    ├── build_appt.py               APPT 职官任职
    ├── build_rel.py                REL 人物关系
    ├── build_event.py              L5 事件
    ├── build_opn.py                OPN 作者论说
    ├── build_trl.py                TRL 古今翻译（要求全覆盖）
    ├── build_kg_join.py            跨层整合索引（kg_join.json + 逻辑行CSV）
    ├── validate_layers.py          构建校验（ERR/GAP 分类，写文件输出）
    ├── run_all.py                  一键重跑（收敛者入口）
    └── samples/                    源数据样例（AI 写源数据的参照模板，6 层各 1）
```

执行期数据目录（脚本自动创建，不入库）：

```
data/
├── _extract/           分卷条目 TXT（条N|正文），annotate 产物
├── _item_registry.json 指纹库（key=NN-NNN，{original, norm}，唯一真源）
├── _src/               AI 源数据 _<layer>_ai_<vol>.py|.json（唯一人工投入点）
├── _layers/            层产物（*_<vol>.json 卷产物、*_all.json 全局聚合、
│                       ent_keys.json 实体主键表、kg_join.* 跨层索引）
├── _validate/          验证输出（各层打包问题、缺漏清单、待核清单、枚举分布）
└── _deliver/           交付打包目录
```

---

## 2. 快速开始

```bash
cd 05-xianjinyifeng-knowledge/scripts

# ① 全量重跑（底座 + 六层 + 跨层 + 校验），验收标尺：验证缺漏清单.txt 问题数 = 0
python run_all.py

# ② 底座已构建、只需重跑打包与校验
python run_all.py --skip-annotate

# ③ 只重算卷 01（增量合并，其余卷保留；装填推进中的日常操作）
python run_all.py --skip-annotate --volumes 01

# ④ 冒烟验证（把 scripts/samples/ 拷入 _src 跑通全管线）
python run_all.py --smoke --skip-annotate --volumes 01

# ⑤ 分步执行（等同 run_all 内部顺序）
python annotate.py --expect "01:58,02:42"          # 底座
python build_ent_keys.py --volumes 01              # L1 实体
python build_appt.py --volumes 01                  # APPT
python build_rel.py --volumes 01                   # REL
python build_event.py --volumes 01                 # L5
python build_opn.py --volumes 01                   # OPN
python build_trl.py --volumes 01                   # TRL
python build_kg_join.py --volumes 01               # 跨层整合
python validate_layers.py                          # 构建校验（全量基线）
python validate_layers.py --skip-baseline          # 冒烟/部分装填阶段
```

---

## 3. 工作流与产物（对应 SKILL.md §10）

| 阶段 | 入口 | 输入 | 产物 |
| --- | --- | --- | --- |
| 底座 | `annotate.py` | 全本 txt | `_extract/` 分卷条目、`_item_registry.json`（100 条指纹库） |
| L1 实体 | `build_ent_keys.py` | `_src/_ent_ai_*.py` | `ent_keys.json` + `ent_<vol>.json` / `ent_all.json` |
| APPT/REL/L5/OPN/TRL | `build_*.py` | 对应 `_src` 源数据 | 各层 `<layer>_<vol>.json` / `<layer>_all.json` |
| 跨层整合 | `build_kg_join.py` | 各层聚合 + 指纹库 | `kg_join.json` + `kg_join_flat.csv`（逻辑行） |
| 校验 | `validate_layers.py` | 以上全部 | 缺漏清单 / 待核清单 / 枚举分布 |

**数据流**：全本 → 条目指纹库 → AI 逐条判定（写 `_src`）→ 打包器（注入 original、
分配业务 ID、枚举硬校验）→ 全局聚合 → 跨层索引 → 校验报告。

---

## 4. 写源数据的约定（AI 侧唯一工作）

每卷每层一个文件：`data/_src/_<layer>_ai_<vol>.py`，顶层键见 `_kg_config.LAYERS`。

- **必写** `item_id`（条号 NN-NNN，引用指纹库）；**禁止**手抄 original/norm（打包器注入，差
  异以指纹库为准，pitfalls #3）、**禁止**手写业务 ID（打包器按段位分配）。
- 枚举字段必须命中封闭集；拿不准的写作别名或规范值，执行期自动归并并进 pending
  （`data/_validate/_enum_pending.json`）。
- 原文没有的信息显式写「未明」，不空着（schema/覆盖校验按 GAP 单列）。
- 参照模板：`scripts/samples/_*_ai_01.py`（基于试点条目 01-001/01-007/01-008/01-039）。

---

## 5. 历史经验的内嵌落点（可复用方法）

| 方法 | 落点 |
| --- | --- |
| 批次追加锚点（《五杂俎》大量批改） | `_kg_config` 卷映射 + `annotate` 卷边界识别 + 增量合并 |
| 磁盘末尾读取（大文件可靠性） | `_kg_pack_base.atomic_write_json`（临时文件+rename，原子落盘） |
| 枚举修正（收集-报告-暂存-决议） | `_kg_enums` 单点 + `check_enum_fields` pending 表 + 验证漂移比值 >1.5 告警 |
| 构建驱动修复（以校验报告反推源数据问题） | `validate_layers` ERR/GAP 分类，问题清单即修复清单 |
| 增量合并只重算请求卷（#12） | `merge_layer_all` + `annotate.build_registry` |
| 不依赖读取顺序的卷映射（#24） | `VOLUME_MAP` 汉字卷名直接映射 |

---

## 6. 扩展点

- **换书**：改 `_kg_config.VOLUME_MAP / SOURCE_FILE / DEFAULT_EXPECT_ITEMS`，枚举换
  `_kg_enums` 快照；层注册表 `LAYERS` 是六层装配点。
- **加层**：`LAYERS` 加一项（ID 前缀 / src_key / builder）→ 写层源样本 → 复用
  `_kg_layer_builder` 或新写打包器 → `LAYER_ORDER` 登记顺序。
- **枚举新增（决议后）**：`_kg_enums` 加值 → `REGISTER_VERSION+1` → 回溯存量 → 同步
  验证脚本期望。禁止静默扩容（与工厂 enum-library 的差异已注记在文件头）。
- **段容量**：`SEGMENT_CAPACITY` 撞号时调大后全量重跑（业务 ID 编号语义见
  `_kg_pack_base.alloc_id`）。

---

## 7. 可溯源 / 可重跑约定

1. **唯一源**：正文只出自 `assets/sources/先进遗风_全本.txt`，条目正文以指纹库
   `original` 为准（#3）；AI 源数据不携带未见于原文的内容判定依据。
2. **幂等**：全部产出自 `run_all.py` 可整链重跑；同一输入重跑产物字节级一致
   （原子写 + 确定性排序；`updated_at` 时间戳仅入 meta）。
3. **增量**：`--volumes NN` 只重算该卷，共享文件（`*_all.json` / 指纹库 / `ent_keys`）
   其余卷保留不回退（#12）；全量（不带参数）= 权威口径重建。
4. **验收**：`data/_validate/验证缺漏清单.txt` 的 **ERR 问题数 = 0** 是唯一验收标尺；
   GAP（未建模条目/枚举 pending/未装填卷）如实单列，不并入总量（#9）。
5. **审计**：问题清单均落盘（#6 不依赖 stdout）；`kg_join_flat.csv` 一行一逻辑记录
   （#18），附原始 JSON 便于 diff 审计。

---

## 8. 与技能工厂的绑定

- 枚举基准：工厂 `../book-knowledge-factory/references/enum-library.md`（本实例取
  schemas.md 锁定的快照，差异记在 `_kg_enums.py` 文件头）。
- 层定义与 schema：`references/schemas.md`（业务 ID 命名、字段、枚举快照的唯一权威）。
- 本基准是工厂书实例技能的生产代码约定，不随技能模板变更自动更新，改口径须改此处。