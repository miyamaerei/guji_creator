# 《五杂俎》知识工程 · 基础代码框架

明·谢肇淛《五杂俎》知识工程实例的**可重跑**代码底座。全部脚本纯标准库（Python 3.12），
无第三方依赖，零配置即可从一份纯文本源文件重建到跨层知识资产。

```
底座拆分 → 卷模式标注 → 统一卷源摊平 → L1 实体 → 事件 → 关系 → 名录 → 引书 → 名物
         → 方言风俗 → 作者观点 → 明代纪事 → 职官任职 → 古今翻译 → 跨层整合 → 双层验证 → 交付
```

> 本框架只搭"管道"，不含"解读内容"。各层的语义装填由**统一卷源**
> `_src/_vol_<NN>.py` 承载 —— **一卷一次 AI 调用，11 层一次产完，原文只读一遍**
> （成本口径见 §9）。打包器负责摊平、ID 分配、形状归一、跨层回填、枚举校验、
> 原文注入、增量合并与验证。

---

## 1. 目录结构

```
wuzazu/
├─ 源文本（外部，可用环境变量覆盖）
│   _source/五杂俎.txt                # 默认位置；环境变量 WZZ_TXT 可覆盖
│
├─ 底座与引擎（公共代码）
│   _kg_pack_base.py      公共基座：路径/常量/IO/词形归一/源数据装载/ID 分配/CLI
│   _kg_enums.py          枚举单点：14 棵枚举树 + 别名 + 未知值暂存 + 版本登记
│   _kg_entity.py         实体层与词形索引（ent_index.json 供其余各层回填）
│   _kg_layers.py         配置驱动打包引擎（11 层字段契约 ENGINE + 归一/回填）
│   _kg_layer_runner.py   统一层入口（layer_cli）与字段自查（layer_fields）
│
├─ 底座与各层入口
│   build_base.py         底座：切卷切条 + 指纹库 + 对账报告
│   build_volume_profile.py  卷阅读模式标注（17 卷的阅读侧重 + 层装填优先级）
│   build_ent.py           L1 实体层（含主键表/别名索引/归一清单/同名异人待核）
│   build_event.py         EVT 事件层          build_rel.py   REL 关系层
│   build_nam.py           NAM 名录谱牒层      build_cit.py   CIT 引书索引层
│   build_obj.py           OBJ 名物层          build_cus.py   CUS 方言风俗层
│   build_opn.py           OPN 观点论说层      build_ming.py  MING 明代纪事层
│   build_appt.py          APPT 职官任职层     build_trl.py   TRL 古今翻译层
│
├─ 装填层（按卷扇出：一卷一次 AI 调用，产出 11 层）
│   _vol_schema.py        统一卷源契约：split 摊平 / merge 折叠 / audit 巡检 / status
│   _vol_prompt.py        装填提示词生成器（字段契约与枚举从代码自动派生）
│   _mk_vol.py            落盘器：机器校验 → 原子写入 → 自动摊平 → 可选打包
│   _vol_roundtrip.py     安全网：合并→摊平→逐条比对，断言零丢失
│   _vol_ab_regression.py 安全网：老路径 vs 新路径产物逐字段比对
│   _salvage_workflow.py  workflow 溢出文件抢救（落盘用）
│
├─ 整合 · 验证 · 自检
│   build_kg_join.py      跨层整合（_kg_join.json + _kg_join_index.json + CSV）
│   validate_layers.py    分层验证（15 类检查，退出码 1 = 有 error）
│   validate_kg_join.py   贯通验证（7 类检查，覆盖闸门）
│   build_all.py          一键重跑 17 阶段（--volumes/--stage/--skip-validate）
│   run_selftest.py       端到端自检（迷你样本 → 31 项断言 → 逐字节还原）
│
├─ 输入 / 中间 / 产物
│   samples/                    源数据契约样例（不参与打包，照抄即可）
│   _src/_vol_<NN>.py           **统一卷源（唯一手写/AI 产出区，一卷 11 层）**
│   _src/_<layer>_ai_<NN>.py    摊平产物（自动生成，勿手改）
│   _src/_legacy/               覆盖前的分层文件备份
│   _extract/NN_卷名.txt        底座切出的分卷正文（条N|正文）
│   _item_registry.json         条粒度指纹库 {item_id:{original,norm}}
│   _layers/<layer>_NN.json     各层单卷成品（顶层键 records）
│   _layers/ent_*.json          实体主键表 / 别名索引 / 归一清单
│   _layers/_kg_join.json       跨层贯通（一条一行，含全层回链）
│   _build/                     汇总、任务、报告、日志、枚举状态、_prompt_NN.md
│   _validate/                  验证 JSON + Markdown 摘要
│   _deliver/                   交付用 CSV
└─ README.md
```

---

## 2. 快速开始

### 2.1 装填一本书（**按卷扇出**，一卷一次 AI 调用）

```bash
# ① 打印某卷的装填提示词（字段契约与枚举从代码自动派生，永不漂移）
python _vol_prompt.py 01
python _vol_prompt.py 01 --save          # 存到 _build/_prompt_01.md

# ② AI 按提示词产出统一卷源 → 机器校验 → 落盘 → 自动摊平成 11 个分层文件
python _mk_vol.py 01 _src/_vol_01.py
python _mk_vol.py 01 _src/_vol_01.py --build    # 顺带打包+验证

# ③ 打包 + 双层验证
python build_all.py --volumes 01

# 进度与一致性
python _vol_schema.py status                   # 各卷装填进度
python _vol_schema.py audit  --volumes 01 02   # 统一卷源 vs 分层文件是否漂移
python _vol_schema.py merge  --volumes 01      # 11 个分层文件折回统一卷源
```

> **为什么按卷不按层**：token 成本的第一决定因素是「同一份原文被读几遍」。
> 按层扇出（11 层 × N 卷）会把同一份原文读 11 遍；按卷扇出只读 1 遍，
> 11 层在**一次调用内**产出，层间引用交给打包器回填。详见 §11。

### 2.2 重跑与校验

```bash
# 全量重跑：底座 →摊平 → 11 层 → 跨层整合 → 双层验证
python build_all.py

# 只重算若干卷（增量语义：共享汇总按卷覆盖，不动其他卷）
python build_all.py --volumes 01,02
python build_event.py --volumes 09

# 只看阶段清单 / 跳过验证 / 只跑指定阶段
python build_all.py --list
python build_all.py --skip-validate
python build_all.py --stage base,ent,join

# 底座自检（只读源文件并输出对账报告，不写盘）
python build_base.py --check

# 枚举总览 / 落盘枚举树
python _kg_enums.py && cat _build/_kg_enums_tree.json

# 查看某层字段契约（写数据前先看形状和枚举）
python -c "import _kg_layer_runner as R; print(R.layer_fields('event'))"

# 端到端自检（临时样本，跑完逐字节还原 _src 与 _layers）
python run_selftest.py            # 或 --keep 保留样本产物

# 统一卷源的两道安全网
python _vol_roundtrip.py --apply      # 合并→摊平→逐条比对，断言零丢失
python _vol_ab_regression.py          # 老路径 vs 新路径产物逐字段比对
```

---

## 3. 底座：切卷、切条、指纹库

`build_base.py` 是唯一读源文本的脚本，产出三条下游全部依赖的底座：

| 产物 | 说明 |
| --- | --- |
| `_extract/NN_卷名.txt` | 分卷正文，每行 `条N|正文`，人工校对友好的纯文本 |
| `_item_registry.json` | 条粒度指纹库，主键 `item_id = NN-NNN`（序卷 `00`） |
| `_build/volume_summary.json` | 分卷条目数、条号区间、阅读模式提示 |
| `_build/split_reconciliation.json` | **切分对账**：字符数守恒、未归属行、结论 |
| `_build/base_report.json` | 总条目/总字数/源文件 sha256/缺口登记 |

切分规则（实测源排版而定，不是想当然的空行分段）：

- 卷标记：行首（可带空白）`●序` → 卷 `00`；`●卷一 天部一` → 卷 `01`，共 17 个标记。
- 条目起点：**段首全角双空格 `U+3000`** 起段，段内不换行（源文件 1781 行只有 1 个空行，
  按"空行分段"只会切出 18 条，这是本框架实测踩过的坑）。
- 无缩进行（书名行、序末落款、页脚）：并入当前条，不丢字。
- 段首缩进是排版空格，落库时丢弃，并在对账报告中显式记账（`dropped_indent_chars`）。

词形归一：`normalize_text()` 做全角空格/制表符 → 单空格、连续空白压缩、`VARIANT_MAP`
异体字替换（数据驱动空表，遇到异体字往表里加一条即可，全流程自动生效）。
`original` 永不改动，`norm` 只做等价替换。

---

## 4. 源数据契约（写数据的唯一入口）

### 4.1 统一卷源（`_src/_vol_<NN>.py`）—— 推荐的唯一手写区

```python
# _src/_vol_01.py  《五杂俎》卷01（天部一）统一卷源 —— 11 层一次装填
SRC = {
"01-006": {                                    # 条号，与指纹库 key 严格一致
    "ent":   [("老子", "person", "老子（指老聃）")],   # 紧凑元组：text, type, normalized?
    "event": [{"type": "文事", "who": "老子", "action": "作璇玑玉衡以齐七政",
               "what": "…", "when": "未明", "where": "未明"}],
    "cit":   [("易", "暗用", "立论")],                # cited_work, citation_type, context
    "rel":   [("汉文帝", "邓通", "其他", "双向", "即汉文帝之于邓通…")],
    "trl":   "白话译文……",                          # 字符串 = 一条
},# 无材料的层整个键省略，不要写空 list
}
```

- **一卷一次 AI 调用，11 层一起产出** —— 原文只读1 遍（见 §11）。
- 只需写两样：条号（本文件的key）、各层语义字段。
- **不写**业务 ID（`ENT-`/`WZZ-E-`…由打包器分配）；
  **不抄** `original`/`norm`（指纹库注入）；**不写** `volume`（由文件名推导）；
  **不写** `*_ent_ids`（跨层回填由打包器统一做 —— 这是能一次写完 11 层的前提）。
- 紧凑元组顺序：`ent` = text/type/normalized?，`rel` = person_a/person_b/relation_type/direction/evidence，
  `cit` = cited_work/citation_type/context；其余层用完整 dict。
- `_mk_vol.py` 会在落盘前把上述每一条规则**机器校验**（禁写键、条号存在性、枚举合法性、
  空串未明），不通过就不落盘。

### 4.2 摊平产物（`_src/_<layer>_ai_<NN>.py`）

`_vol_schema.py split` 自动把统一卷源摊平成打包器熟悉的 11 个分层文件
（头部带「自动生成，勿手改」标记）。**这些文件不需要手工维护**，
但仍可被手工编辑；改完后 `merge` 可折回统一卷源。

分层文件的形状与旧版完全兼容，`samples/` 里的样板对两者都适用：

```python
# _src/_event_ai_01.py（摊平产物，也可手写）
RECORDS = [
    {"item_id": "01-006", "type": "文事", "who": "舜",
     "action": "作璇玑玉衡以齐七政", "what": "…", "when": "未明", "where": "未明"},
]
```

- 字段别名宽容：`ent_id`/`who_ids`/`a_ids` … 会自动映射到规范字段名。

### 4.3 形状约定

| 形状 | 写法 | 打包器行为 |
| --- | --- | --- |
| `scalar` | `"action": "作璇玑玉衡以齐七政"` | 直存；必填缺省则补 `未明` |
| `undecided` | `"when": "未明"` | 未考之处**必须显式写「未明」**，不留空 |
| `enum` | `"type": "文事"` | 走枚举归一；别名自动纠正；未知值进 pending |
| `dict` | `"who": "舜"` | 字符串自动升格 `{"text":"舜","who_ent_ids":[…]}` |
| `dictlist` | 名录 `entries` | 字符串列表自动升格为对象列表 |
| `list` | `"evidence_refs": ["WZZ-E-000123"]` | 列表保序去空 |

### 4.4 跨层回填（实体引用）

写 `who`/`person_a`/`name` 等引用字段时**只写词形**，打包器查 `ent_index.json` 回填
`*_ent_ids`。命中即填，未命中**不报错、不阻断**，只在 `_build/_<layer>_logs.json` 里
记一条软缺（`ref_softmiss`）。想让引用更结实，就先跑 `build_ent.py`（或
`python build_event.py --rebuild-index`）。

示例：实体层写了 `{"item_id":"01-007","text":"汉明帝","type":"person"}`，事件层写
`"who": "汉明帝"`，产物即 `{"text":"汉明帝","who_ent_ids":["ENT-000009"]}`。

---

## 5. 各层字段契约速查

`_kg_layers.py` 的 `ENGINE` 是**唯一权威**，`python -c "import _kg_layer_runner as R; print(R.layer_fields('REL'.lower()))"`
可随时打印。要点：

| 层 | 主键 | 关键字段 |
| --- | --- | --- |
| ent | `ENT-` | `text` `type`(10 类) `start` `end` `normalized` `confidence` `source` |
| event | `WZZ-E-` | `type`(22 类) `who` `action` `what` `when` `where` |
| rel | `REL-` | `person_a` `person_b` `relation_type`(12 类) `direction` `evidence` |
| nam | `NAM-` | `name` `category` `scope` `entries[]{person,courtesy_name,hometown,office}` |
| cit | `CIT-` | `cited_work` `citation_type` `context` |
| obj | `OBJ-` | `name` `category` `attributes{自由键}` `lore` |
| cus | `CUS-` | `type` `region` `term` `description` |
| opn | `OPN-` | `topic` `stance` `argument` `evidence_refs[]` |
| ming | `MING-` | `era` `who` `what` `when` `where` `category` `first_person` `ref_events[]` |
| appt | `APPT-` | `person` `office` `institution` `when` `status` `evidence` |
| trl | `TRL-` | `translation` `style` `note` `confidence`（note 缺省自动填「余光中风格基准」） |

**新增一层**只需四步：① 在 `_kg_enums.py` 的 `BASE_ENUMS` 加枚举树；
② 在 `_kg_layers.py` 的 `ENGINE` 加字段契约、在 `_kg_pack_base.py` 的 `LAYERS`
加 `id_prefix/id_field/key_fields`；③ 复制一个三行入口 `build_xxx.py`；④ 在
`build_all.py` 的 `STAGES` 与 `build_kg_join.py` 的层键里登记。验证器与自检自动覆盖。

---

## 6. 枚举三级流程（收集 → 报告 → 暂存）

语义装填时遇到新词（新官职、新风俗类型）**不中断打包**：

1. **收集**：`_kg_enums.validate()` 判值，未知则归一为最接近的兜底值（或 `其他`）；
2. **报告**：未知值连同 `item_id`/字段写入 `_build/_enums_pending.json`；
3. **暂存 + 回归**：人工确认后 `register_version(name, value, evidence)` 版本号 +1，
   存量数据按新版本重跑即自动归位。

别名表让历史写法自动收敛：`主从 → 上下级`、`军务 → 军事`、`科第 → 科举`、
`政事 → 朝政`（含实例别名 `INSTANCE_ALIAS`）。枚举树落盘：`_build/_kg_enums_tree.json`。

---

## 7. 验证与贯通

```bash
python validate_layers.py     # 15 类检查：ID 前缀/重复/必填/未明/形状/枚举/原文漂移/悬空引用
python validate_kg_join.py    # 7 类检查：重复/未知条号/悬空引用/层数与数组不符/条目缺失
```

- 产物：`_validate/layer_validation.json` + `layer_validation_summary.md`、
  `_validate/kg_join_validation.json` + `_kg_join_validation_summary.md`。
- 退出码 1 = 有 `error`（`warning` 不阻断，用于软缺引用等可容忍项）。
- **跨层整合**：`_kg_join.json` 每个条号一行，携带 `events/rels/…/trls/ents` 全层回链、
  `layer_count`、`source/original/norm`；`_deliver/_kg_join_flat.csv` 给人看（含
  `event_actions`、`rel_pairs`、`translation` 等人读标签列）。

---

## 8. 设计约定（为什么这样写）

- **原文零漂移**：`original` 由指纹库注入，任何层都不许手抄；验证器逐条比对指纹库，
  漂移即 error。可重跑、可溯源的前提。
- **ID 分配与排序稳定**：ID 在打包时按 `(卷, 条内序号, 关键字段)` 排序后分配，
  同一份源数据重跑 ID 恒定；增补条目只影响其后的号段。
- **增量合并**：`--volumes 01` 只重算 01，共享汇总文件（`*__summary.json`、
  `_kg_join`）按卷覆盖式合并，其他卷原地保留。
- **写盘原子**：一切落盘走"临时文件 + `os.replace`"，中断不会留下半个 JSON。
- **形状归一在一处**：字段映射、字符串升格、未明补齐、枚举归一全在 `_kg_layers.py`，
  各层入口只有三行，改口径不用改 11 个文件。
- **控制台编码**：Windows GBK 控制台下父子进程都 `reconfigure(utf-8, replace)`
  并设 `PYTHONIOENCODING`，避免生僻字导致 `UnicodeEncodeError` 打断流水线
  （这也是实测踩过的坑）。
- **验证器入口壳子恒返 0**：判断验证是否通过要看 `_validate/*.json` 的 `errors`
  计数，`build_all.py` 与 `run_selftest.py` 已按此口径判定。
- **提示词从代码派生**：字段契约来自 `_kg_layers.ENGINE`、枚举来自 `_kg_enums`，
  装填提示词由 `_vol_prompt.py`现场生成 —— 改代码即改提示词，永不漂移，
  且不必让每个 agent 完整读一遍 34.5K 字符的静态文档。
- **格式错误挡在打包之前**：`_mk_vol.py` 先校验再落盘，禁写键/臆造条号/枚举串值
  都不会流到打包器，避免"跑完十几个阶段才发现填错"。

---

## 9. 为什么按卷扇出（成本口径）

AI 解析书籍时，token 成本的第一决定因素是**同一份原文被读了几遍**，
与 prompt 写得多好、模型多强都无关。

| | 旧做法（按层扇出） | 新做法（按卷扇出） |
| --- | --- | --- |
| 单元 | 1 层 × 1 卷 = 1 次调用 | **1 卷 = 1 次调用** |
| 卷01+02 的原文被读 | 11 层 × 2 卷 = **22 遍** | **1 遍** |
| 每 agent 的 skill 包 | 34.5K 字符静态文档 | 4.4K（`--compact` 2.6K）现场派生 |
| 阶段依赖 | P0→P1→P2→P3 串行，每阶段回读上层产物 | 无，卷内一次产完 |
| 同一原文重读放大 | **11×**（再乘阶段回读与拆批复核） | **1×** |

配套的三处压缩：

1. **紧凑元组**：最密的 `ent`/`rel`/`cit` 三层用元组代替 dict，
   每条省掉重复的 `"item_id": …,` 与键名，约省 30~40% 输出字符。
2. **提示词按需裁剪**：`_vol_prompt.py --compact` 省掉枚举明细，
   枚举速查表在需要时查 `_kg_enums.py` 即可。
3. **消灭拆批返工**：旧做法因单 agent 吐 630 条实体撑不住，被迫拆
   `partA` + `064-125` 两批再加一轮复核 ≈ 多跑两遍全卷；
   按卷装填后一条一个 `SRC`，不再需要拆批。

安全网（换格式不改下游的三道证明）：

- `_vol_roundtrip.py`：merge → split 逐条比对，断言零丢失（按内容集合，
  因为打包器 `pack_volume` 自己会 `sort`，记录顺序与 ID 无关）。
- `_vol_ab_regression.py`：老路径与新路径各跑一遍打包器，
  **7 层产物逐字段一致**（含 ID 分配与 `*_ent_ids` 回填结果）。
- `run_selftest.py`：31 项断言，且自检前把真实源数据整体暂存隔离，
  跑完逐字节还原 —— 不再被残留真实数据污染出假失败。

---

## 10. 实测基线（脚手架自证）

- `python build_all.py`：17 阶段全部 exit=0，分层验证 0 error / 0 warn，贯通验证
  覆盖率 100%（源数据为空时的期望值）。
- `python run_selftest.py`：31 项断言全 PASS，含 who 升格与实体回填、枚举别名归一
  （主从→上下级）、未明显式落库、跨层 layer_count 一致性、双层验证 0 error。
- `python _vol_ab_regression.py`：卷01+02 的 7 个已装填层，老路径与新路径
  产物逐字段一致（ent 630 / event 112 / rel 29 / nam 11 / cit 175 / obj 58 / cus 61）。
- 底座实测：源文件 758051 字节 / sha256 `771012247877e100e8575424af827ac2f22353a88edfa9b9f2cf6a82dd1974b8`，
  切出 1758 条 / 248695 字，空条目 0，切分对账 `unassigned_count=0`（正文零丢失）。

分卷条目数（实测，`_build/volume_summary.json`）：

| 卷 | 名称 | 条数 | 卷 | 名称 | 条数 |
| --- | --- | ---: | --- | --- | ---: |
| 00 | 版本说明与序 | 2 | 09 | 物部一 | 163 |
| 01 | 天部一 | 125 | 10 | 物部二 | 103 |
| 02 | 天部二 | 105 | 11 | 物部三 | 113 |
| 03 | 地部一 | 122 | 12 | 物部四 | 121 |
| 04 | 地部二 | 116 | 13 | 事部一 | 101 |
| 05 | 人部一 | 107 | 14 | 事部二 | 73 |
| 06 | 人部二 | 79 | 15 | 事部三 | 107 |
| 07 | 人部三 | 93 | 16 | 事部四 | 143 |
| 08 | 人部四 | 85 | — | **合计** | **1758** |

- **待登记缺口**：方案基线 1761 条（序 3 + 正文 1758）vs 实测 1758 条（序 2 + 正文 1756），
  序卷 00 缺"独立版本说明条"；差额已在 `_build/base_report.json` 的
  `gap_items/gap_main/gap_preface` 与 `baseline_note` 登记，不静默改口径。

---

## 11. 下一步（框架之后的工作）

1. 分卷阅读模式标注复核（`build_volume_profile.py` 产物 + 原文抽检）。
2. **按卷装填 `_src/_vol_<NN>.py`**（一卷一次调用出 11 层）：
   ```bash
   python _vol_prompt.py NN --save        # 生成提示词
   # → AI 产出统一卷源
   python _mk_vol.py NN _src/_vol_NN.py  # 校验 + 落盘 + 摊平
   python build_all.py --volumes NN      # 即时验证
   ```
   进度用 `python _vol_schema.py status` 盯。
3. 全量完成后按 skill 交付流程产出查询接口与报告（`_deliver/`）。
4. 若要继续手写分层文件（旧方式），改完记得 `merge` 回统一卷源，保持单一真源。
