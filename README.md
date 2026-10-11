# guji_creator

> 把古籍纯文本 → 条粒度指纹库 → 多层语义标注 → 跨层知识图谱 → 交付物 的**可重跑工程集**。

仓库里装的是 5 部明代文献各自的「知识工程实例」：每部书一个独立目录，内含底座拆分脚本、分层打包脚本、AI/人工填写的源数据、验证器与交付物。**原书正文不入库**（源文件在机器本地，由环境变量或脚本常量指向）。

---

## 0. 先纠正一个叫法

这 5 部**不是小说**，都是明代史料／子部文献：

| 目录 | 书 | 作者 · 时代 | 文献性质 |
| --- | --- | --- | --- |
| `kezuozhuiyu-kb/` | 《客座赘语》 | 明 · 顾起元 | 笔记（专记南都金陵掌故、方言、风俗、名物） |
| `wuzazu-kb/` | 《五杂俎》 | 明 · 谢肇淛 | 笔记（天·地·人·物·事五部，考辨+纪事+论说） |
| `shuidongriji-kb/` | 《水东日记》 | 明 · 叶盛 | 笔记（明代职官、典章、文献史料富矿） |
| `xinguanguifan-kb/` | 《新官轨范》 | 明 · 佚名 | 官箴书（新任官员到任、理政、断案、赈灾全流程规范） |
| `qubian_kb/` | 《蘧编》 | 明 · 叶向高 | 自订年谱（20 卷，第一人称逐年记事） |

---

## 1. 五部书一览

| 目录 | 卷/章 | 条目数 | 语义层 | 主入口 | 进度 |
| --- | --- | --- | --- | --- | --- |
| `kezuozhuiyu-kb/` | 10 卷 + 00 卷 | 476 | **13** 层 | `build_base.py` → `build_layers.py` → `validate_layers.py` | ✅ 全卷装填完成，已出交付包 |
| `wuzazu-kb/` | 17 卷 | 1758 | **11** 层 | `build_all.py`（17 阶段一键）/`_vol_prompt.py` + `_mk_vol.py` | ✅ 框架+装填主体完成 |
| `shuidongriji-kb/` | 38 卷 + 00 卷 | 1197 | **8** 层 | `run_all.py`（`/ --volumes NN`） | ⏳ 试点卷 01、17 完成，余 36 卷待铺 |
| `xinguanguifan-kb/` | 11 章 | 275 | 结构 / 规则 / 流程 / 事件 4 类 | `build_struct_ai_新官轨范.py` 等 + `build_kg_join.py` | ✅ 含网页阅读器 + epub 导出 |
| `qubian_kb/` | 20 卷 + 序/前言 | 76 | **8** 类（ents/evts/chrs/mems/rels/lits/appts/trls） | `build_base.py` → `build_layers.py` → `build_trl.py` | ✅ 全卷交付说明已出 |

---

## 2. 统一的生成逻辑

五部书风格各异，但**管线骨架完全一致**，都是「四段式」：

```
  原书 .txt（外部，不入库）
        │
        │  ①  底座 build_base.py
        │      切卷 → 切条 → 归一 → 指纹库 → 对账报告
        ▼
  _extract/NN_卷名.txt       条粒度正文（条N|正文）
  _item_registry.json        {NN-NNN: {original, norm}}  ← 不可重建，入库
        │
        │  ②  装填 _src/_<layer>_ai_NN.py 或 _vol_<NN>.py
        │      只写「条号 + 解读」，绝不手抄原文
        ▼
        │  ③  打包 build_<layer>.py
        │      ID 分配 / 形状归一 / 跨层回填 / 枚举校验 / 原文注入
        ▼
  _layers/<layer>_NN.json    各层单卷成品（顶层键 records）
        │
        │  ④  整合 + 验证 + 交付
        ▼
  _kg_join.json / _kg_join_flat.csv（一条一行，全层回链）
  validate_layers.py → 缺漏清单（ERR=0 才算过）
  _deliver/  CSV、全书记译本、复盘报告
```

**四条铁律**（各书 README 反复强调，是这套工程的核心）：

1. **原文只在指纹库里存一份。** 源数据文件只写条号与解读，`original` 由打包器从 `_item_registry.json` 注入 —— 杜绝抄写漂移。
2. **枚举封闭。** 所有取值来自单点枚举文件 `_kg_enums.py`，未知值走「收集 → 报告 → 暂存」三级流程，不现场造词。
3. **先查后建。** 实体主键表（`ent_keys.json` / `_global/` 去重）随卷累积，跨卷同名实体先查再决定是否新建。
4. **一切可重跑。** 单卷重跑是幂等的（`--volumes NN` 只覆盖该卷，不动共享汇总）；验证器退出码为唯一验收闸门。

---

## 3. 目录命名对照（五书不一致，看这张表）

同样是「AI 源数据」「层产物」「交付物」，五个目录用了不同名字，容易踩空：

| 角色 | 客座赘语 | 五杂俎 | 水东日记 | 新官轨范 | 蘧编 |
| --- | --- | --- | --- | --- | --- |
| 源数据（手写/AI） | `_src/` | `_src/_vol_<NN>.py` | `sources/` | `新官轨范_*_ai/` | `_ai_<NN>.py` |
| 公共基座 | `_kg_pack_base.py` | `_kg_pack_base.py` | `common.py` | `_kg_pack_base.py` | `build_base.py` |
| 枚举单点 | （内嵌） | `_kg_enums.py` | `_kg_enums.py` | `_kg_enums.py` | （内嵌） |
| 底座切分产物 | `_extract/` | `_extract/` | `_extract/` | `_extract/` | `_extract/` |
| 分层成品 | `_layers/` | `_layers/` | `data/<layer>/` | `新官轨范_标注/` 等 | `_kg_<NN>.json` |
| 汇总/报告/日志 | `_build/` | `_build/` | `data/` | — | `volume_summary.csv` |
| 验证输出 | `_validate/` | `_validate/` | `reports/` | `*验证*.txt` | `*验证缺漏清单.txt` |
| 交付物 | `_deliver/` | `_deliver/` | `交付物/` | `新官轨范_阅读器/` | `trl_*.txt` / `全卷交付说明.txt` |

---

## 4. 语义层术语表

同一批缩写贯穿五书，含义固定：

| 缩写 | 含义 | 缩写 | 含义 |
| --- | --- | --- | --- |
| `ENT` | 实体（人物/机构/地名/书名…）+ 主键表 | `NAM` | 名录谱牒（科举题名、家族世系四元组） |
| `APPT` | 职官任职（谁·何时·何官·何状态） | `CIT` | 引书索引（本书征引了哪些文献） |
| `EVT`/`EVENT` | 事件（纪事条目结构化） | `OBJ` | 名物（器物、动植物、建筑…） |
| `REL` | 人物关系（亲缘/师友/政争…） | `CUS` | 方言风俗 |
| `LIT` | 文献资产（成书、版本、著录） | `OPN` | 作者观点论说 |
| `GEO` | 地理（沿革、方位、里程） | `MING` | 明代纪事（本朝专记） |
| `REG` | 典章制度 | `TRL` | 古今翻译（全量逐条，硬校验条目数=译条数） |
| `CHR` | 编年（蘧编：年谱逐年条目） | `MEM` | 备忘录/奏疏文书（蘧编） |

---

## 5. 各书速览

### 5.1 `kezuozhuiyu-kb/` 《客座赘语》
最完整的一本，13 层全卷装填完毕，可作为**范式样本**先读它。
- 切分特例已固化：`【巾】【履】` 相邻标题合并、卷五「前记异闻一百则」复合条按 `05-005-SS` 子则拆分等，详见其 README §4。
- `_global/` 放全局实体去重（merge_map / 去重报告），是跨卷实体治理的落点。
- 重跑：`python build_base.py` → `python build_layers.py` → `python validate_layers.py`；`check_src_schema.py` 可单独查源数据形状。

### 5.2 `wuzazu-kb/` 《五杂俎》
工程化做得最重的一本，**按卷扇出**：一卷一次 AI 调用，11 层一次装完，原文只读一遍（省 token）。
- 唯一手写区是 `_src/_vol_<NN>.py`（统一卷源），落盘后自动摊平成 `_src/_<layer>_ai_<NN>.py`。
- 两道安全网：`_vol_roundtrip.py`（合并→摊平→逐条比对，断言零丢失）、`_vol_ab_regression.py`（新旧路径产物逐字段比对）。
- 端到端自检：`python run_selftest.py`（迷你样本 → 31 项断言 → 逐字节还原）。
- 自带 `skill/`（SKILL.md + schemas.md + volume-profile.md + 报告模板），是把这套方法复用到新书时的模板源。

### 5.3 `shuidongriji-kb/` 《水东日记》
38 卷、1197 条，面向**明朝职官知识图谱**供料。
- 按「卷阅读模式」分层优先级：制度优先 / 名录优先 / 谱牒优先 / 文献优先 / 人物优先 / 文事优先 / 均衡全层 —— 执行某卷前先查模式，避免平均用力。
- 卷脚手架：`python scaffold_volume.py --volumes 02` 生成 8 层源数据模板。
- 口径冻结在 `口径规范.md`（含各层 ID 段位分配：卷号×500，杜绝跨卷撞号）。
- 当前：卷 01、卷 17 全量完成，剩余 36 卷按 S1–S4 四片推进。

### 5.4 `xinguanguifan-kb/` 《新官轨范》
唯一有**前端阅读器**的一本，也是唯一把「流程」当一等公民建模的一本。
- 四路并行：`结构`（章节骨架）/ `规则`（施政条文）/ `流程`（政务流转步骤）/ `事件`（案例纪事），`_ai` 结尾是 AI 源数据，无后缀是打包成品。
- `build_kg_join.py` 做跨类整合，`build_reader_data.py` 生成 `新官轨范_阅读器/data.js`，`build_新官轨范_epub.py` 导出 epub。
- 章节原文存 `.xhtml`（`新官轨范_章节/`），便于带格式回看。
- 关键文档：`新官轨范_知识体系设计.md` / `新官轨范_目录.md` / `新官轨范_项目总结报告.md`。

### 5.5 `qubian_kb/` 《蘧编》
叶向高自订年谱，20 卷。**条粒度最粗**（76 条），但每条信息密度最高（逐年记事 + 奏疏 + 家族 + 交游）。
- 与其它书不同：没有层层摊平的 `_src/`，而是 `_ai_01.py` … `_ai_20.py` 一卷一个源数据文件，直接产出 `_kg_<NN>.json`。
- 8 类归一：`ents / evts / chrs / mems / rels / lits / appts / trls`，聚合为 `归一_*.json`。
- TRL 层产出最实用：`trl_全书记译_卷01-20.txt` 是全书白话记译合册。

---

## 6. 环境要求与源文本放置

- Python **3.12+**（五书均只用标准库，无第三方依赖，无需 `pip install`）
- **所有路径都是相对的**：脚本用 `os.path.dirname(os.path.abspath(__file__))` 自行推导项目根，
  整个目录拷到任何机器、任何盘符都能直接跑，不需要改代码。

原书正文不入库（体积大且涉整理者署名与版权）。放在各项目根目录的 `_source/` 下即可被自动找到：

| 项目 | 放到 `_source/` 的文件 | 覆盖用环境变量 |
| --- | --- | --- |
| `kezuozhuiyu-kb/` | `客座赘语_txt/`（10 卷分卷 txt） | `KZZ_SRC` |
| `wuzazu-kb/` | `五杂俎.txt` | `WZZ_TXT` |
| `shuidongriji-kb/` | `水东日记.txt` | `SDR_TXT` |
| `xinguanguifan-kb/` | `新官轨范.txt` | `XGG_TXT` |
| `qubian_kb/` | `蘧编_结构化.json` | `QB_SRC` |

优先级：**环境变量 > `_source/` 默认位置**。想放在别处就设环境变量，脚本逻辑不用动。
各 `_source/README.md` 里有逐步说明。

---

## 7. 仓库约定：什么入库，什么不入库

见根目录 `.gitignore`，原则一句话：**只存「丢了就再也拿不回来的东西」**。

| 入库 ✅ | 不入库 ❌（可 `build_*.py` 重跑） |
| --- | --- |
| 所有 `.py`（打包器、验证器、`_src/`、`sources/`、各 `*_ai_NN.py`） | `_extract/` 底座切分正文 |
| `_item_registry.json` 条粒度指纹库（重建成本高） | `_layers/`、`_build/`、`_validate/`、`data/` 分层产物 |
| `README` / `口径规范.md` / 各书复盘与总结 | `归一_*.json`、`_kg_join*.json`、`层聚合/` 巨量聚合 |
| `skill/`、`samples/`、`references/` | `__pycache__/`、`*.pyc` |
| `_deliver/` 里的报告与 CSV | `*.zip`、`*_global_layers/`、`*.epub`、阅读器 `raw/` |
| `新官轨范_阅读器/*.html`、`data.js` | `_tmp*/`、`_backup*/`、`_shots/`、`.dumate/` |
| `_source/README.md`（放置说明） | `_source/` 里的原书正文与源数据 |

> 原始体积约 275 MB，按上表裁剪后入库约 **31 MB / 1105 个文件**。

---

## 8. 已知待办

- ~~**硬编码本机路径**~~ ✅ 已解决：全部脚本改为由 `__file__` 推导项目根，源文本走 `_source/` + 环境变量。
- **层命名未统一**：同为职官层，有的叫 `appt`、有的在 `data/appt/`；交付目录有 `_deliver/` 与 `交付物/` 两种写法。后续可考虑抽一层公共包。
- **《水东日记》剩余 36 卷**待按 S1–S4 分片装填。
