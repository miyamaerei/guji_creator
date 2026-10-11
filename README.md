# guji_creator

> 把古籍纯文本 → 条粒度指纹库 → 多层语义标注 → 跨层知识图谱 → 交付物 的**可重跑工程集**。

仓库由两部分组成：

- **`*-kb/`** —— 5 部已做完结构化的书，每部一个独立目录：底座拆分脚本、分层打包脚本、AI/人工填写的源数据、验证器与交付物。
- **`Skills/`** —— 沉淀下来的**生成技能**：两套「工厂」+ 5 个「书实例 skill」，用来把这套方法复用到下一本书。
- **`xianjinyifeng-kb/`** —— 正在建的第六本（《先进遗风》），**第一个「先有 skill、再建工程」**的书，工程与它的实例 skill 同目录。

**原书正文默认不入库**（放在各项目 `_source/`，用环境变量或脚本常量指向）；`Skills/` 内实例自带的 `assets/sources/` 是唯一的例外，见 §8。

---

## 0. 先纠正一个叫法

这 6 部**不是小说**，都是明代史料／子部文献：

| 目录                  | 书      | 作者 · 时代       | 文献性质                                      |
| ------------------- | ------ | ------------- | ----------------------------------------- |
| `kezuozhuiyu-kb/`   | 《客座赘语》 | 明 · 顾起元       | 笔记（专记南都金陵掌故、方言、风俗、名物）                     |
| `wuzazu-kb/`        | 《五杂俎》  | 明 · 谢肇淛       | 笔记（天·地·人·物·事五部，考辨+纪事+论说）                  |
| `shuidongriji-kb/`  | 《水东日记》 | 明 · 叶盛        | 笔记（明代职官、典章、文献史料富矿）                        |
| `xinguanguifan-kb/` | 《新官轨范》 | 明 · 佚名        | 官箴书（新任官员到任、理政、断案、赈灾全流程规范）                 |
| `qubian_kb/`        | 《蘧编》   | 明 · 叶向高       | 自订年谱（20 卷，第一人称逐年记事）                       |
| —（仅 skill）          | 《先进遗风》 | 明 · 耿定向撰，毛在增补 | 笔记（二卷，仿宋人《典型录》体，记明代名臣遗闻琐事；四库入子部小说家类·杂事之属） |

---

## 1. 六部书一览

| 目录                  | 卷/章         | 条目数             | 语义层                                               | 主入口                                                        | 对应 skill                            | 进度                             |
| ------------------- | ----------- | --------------- | ------------------------------------------------- | ---------------------------------------------------------- | ----------------------------------- | ------------------------------ |
| `kezuozhuiyu-kb/`   | 10 卷 + 00 卷 | 476             | **13** 层                                          | `build_base.py` → `build_layers.py` → `validate_layers.py` | `Skills/04-kezuozhuiyu-knowledge`   | ✅ 全卷装填完成，已出交付包                 |
| `wuzazu-kb/`        | 16 卷 + 00 卷 | 1758            | **11** 层                                          | `build_all.py`（17 阶段一键）/`_vol_prompt.py` + `_mk_vol.py`    | `Skills/03-wuzazu-knowledge`        | ✅ 全卷装填完成（分层验证「无问题」）            |
| `shuidongriji-kb/`  | 38 卷 + 00 卷 | 1197            | **8** 层                                           | `run_all.py`（`/ --volumes NN`）                             | `Skills/01-shuidong-riji-knowledge` | ✅ 全书完成（ERR=0 / GAP=0 / OK=322） |
| `xinguanguifan-kb/` | 11 章        | 275             | 结构 / 规则 / 流程 / 事件 4 类                             | `build_struct_ai_新官轨范.py` 等 + `build_kg_join.py`           | ❌ **无**（当时还没这套 skill）               | ✅ 含网页阅读器 + epub 导出             |
| `qubian_kb/`        | 20 卷 + 序/前言 | 76              | **8** 类（ents/evts/chrs/mems/rels/lits/appts/trls） | `build_base.py` → `build_layers.py` → `build_trl.py`       | `Skills/02-qubian-knowledge`        | ✅ 全卷交付说明已出                     |
| `xianjinyifeng-kb/` | 2 卷（上/下）    | 约 100 条（空行段落 = 条） | **6** 层（ENT/APPT/REL/EVT/OPN/TRL）              | `05-xianjinyifeng-knowledge/scripts/annotate.py`          | `xianjinyifeng-kb/05-xianjinyifeng-knowledge` | 🚧 工程在建：2026-10-11 定方案，脚本编写中    |

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

| 角色         | 客座赘语               | 五杂俎                 | 水东日记            | 新官轨范               | 蘧编                         |
| ---------- | ------------------ | ------------------- | --------------- | ------------------ | -------------------------- |
| 源数据（手写/AI） | `_src/`            | `_src/_vol_<NN>.py` | `sources/`      | `新官轨范_*_ai/`       | `_ai_<NN>.py`              |
| 公共基座       | `_kg_pack_base.py` | `_kg_pack_base.py`  | `common.py`     | `_kg_pack_base.py` | `build_base.py`            |
| 枚举单点       | （内嵌）               | `_kg_enums.py`      | `_kg_enums.py`  | `_kg_enums.py`     | （内嵌）                       |
| 底座切分产物     | `_extract/`        | `_extract/`         | `_extract/`     | `_extract/`        | `_extract/`                |
| 分层成品       | `_layers/`         | `_layers/`          | `data/<layer>/` | `新官轨范_标注/` 等       | `_kg_<NN>.json`            |
| 汇总/报告/日志   | `_build/`          | `_build/`           | `data/`         | —                  | `volume_summary.csv`       |
| 验证输出       | `_validate/`       | `_validate/`        | `reports/`      | `*验证*.txt`         | `*验证缺漏清单.txt`              |
| 交付物        | `_deliver/`        | `_deliver/`         | `交付物/`          | `新官轨范_阅读器/`        | `trl_*.txt` / `全卷交付说明.txt` |

---

## 4. 语义层术语表

同一批缩写贯穿五书，含义固定：

| 缩写            | 含义                    | 缩写     | 含义                    |
| ------------- | --------------------- | ------ | --------------------- |
| `ENT`         | 实体（人物/机构/地名/书名…）+ 主键表 | `NAM`  | 名录谱牒（科举题名、家族世系四元组）    |
| `APPT`        | 职官任职（谁·何时·何官·何状态）     | `CIT`  | 引书索引（本书征引了哪些文献）       |
| `EVT`/`EVENT` | 事件（纪事条目结构化）           | `OBJ`  | 名物（器物、动植物、建筑…）        |
| `REL`         | 人物关系（亲缘/师友/政争…）       | `CUS`  | 方言风俗                  |
| `LIT`         | 文献资产（成书、版本、著录）        | `OPN`  | 作者观点论说                |
| `GEO`         | 地理（沿革、方位、里程）          | `MING` | 明代纪事（本朝专记）            |
| `REG`         | 典章制度                  | `TRL`  | 古今翻译（全量逐条，硬校验条目数=译条数） |
| `CHR`         | 编年（蘧编：年谱逐年条目）         | `MEM`  | 备忘录/奏疏文书（蘧编）          |

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
- 已完成：16 卷统一卷源齐备，`_validate/layer_validation_summary.md` 各层均「无问题」；  
  跨层整合 1288 条（`empty_items=0`），实体 3998 个。
- 两道安全网：`_vol_roundtrip.py`（合并→摊平→逐条比对，断言零丢失）、`_vol_ab_regression.py`（新旧路径产物逐字段比对）。
- 端到端自检：`python run_selftest.py`（迷你样本 → 31 项断言 → 逐字节还原）。
- 自带 `skill/`（SKILL.md + schemas.md + volume-profile.md + 报告模板），是把这套方法复用到新书时的模板源。

### 5.3 `shuidongriji-kb/` 《水东日记》

38 卷、1197 条，面向**明朝职官知识图谱**供料。**五本里唯一走完全部 S1–S4 分片的**，状态最完整。

- 按「卷阅读模式」分层优先级：制度优先 / 名录优先 / 谱牒优先 / 文献优先 / 人物优先 / 文事优先 / 均衡全层 —— 执行某卷前先查模式，避免平均用力。
- 卷脚手架：`python scaffold_volume.py --volumes 02` 生成 8 层源数据模板。
- 口径冻结在 `口径规范.md`（含各层 ID 段位分配：卷号×500，杜绝跨卷撞号）。
- **已完成**：38 卷 × 8 层 = 304 份源数据齐备；实体 2291 个（ENT-001..2291）、ent 标注 2253 条；  
  appt 237 / event 234 / reg 72 / lit 180 / rel 126 / nam 54 / trl 1192（= 正文条目数，零缺口）；  
  跨层索引 1197 条；全量验证 **ERR=0 / GAP=0 / OK=322**。
- 交付物：`交付物/层聚合/`（8 层 × JSON+CSV）、跨层索引 CSV、实体主键表 CSV、  
  `《水东日记》全书记译文本（38卷合册）.md`（1192 条白话记译）。
- 唯一未落地的是 `Vue3多书知识阅读器设计文档.md` —— 只有设计稿，前端尚未实现。

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

### 5.6 `xianjinyifeng-kb/` 《先进遗风》（在建）

明 · 耿定向撰、毛在增补，二卷笔记，记明代名臣遗闻琐事。**唯一「先有 skill、后建工程」的一本**。

- 已提取正文：卷上 / 卷下 / 全本 txt（100 段 / 27031 字，四库本含提要）。
- 方案（2026-10-11 确认）6 层：`ENT` 实体 / `APPT` 职官任职 / `REL` 人物关系 / `EVT` 事件 / `OPN` 作者论说 / `TRL` 古今翻译 + V2 人工校验 + V3 枚举校准 + 跨层索引。
- 切条方案：这本书**没有条目标题**（纯段落连排），粒度定为**空行段落 = 条**，卷标记与书名段不入条目。
- 实例与工程同目录：`xianjinyifeng-kb/05-xianjinyifeng-knowledge/`（`SKILL.md` + `references/schemas.md` + `scripts/`）。

---

## 6. `Skills/`：把这套方法复用到新书

前面五本都是「先有工程、后补 skill」，《先进遗风》是第一个「先有 skill」的。这个目录里其实有**两套工厂**，别搞混：

### 6.1 两套工厂

|         | `Skills/00-book-knowledge-factory`                                                | `Skills/book-skill-factory`                                                        |
| ------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| 定位      | **重方法论的 meta-skill**：结构性探查 → 引导式反思定层 → 用户确认 → 生成书实例                               | **轻量结构工厂**：六组启发式问询 → 答案翻译成 `structure.json` → 渲染薄壳实例                               |
| 实例能做什么  | 全套知识工程：底座切条 → 8~13 个语义层逐层抽取 → 跨层整合 → 报告                                           | 只做**四级结构提取**：目录 / 卷 / 标题 / 段落，输出分卷 txt、全本 txt、目录 txt                               |
| 实例命名    | `<NN>-<book-slug>-knowledge`                                                      | `book-<slug>`（本仓库落为 `05-xianjinyifeng-knowledge`）                                  |
| 实例产物    | `SKILL.md` + `references/`（schemas / 枚举 / 卷阅读模式 / 翻译风格）+ `assets/templates/` 报告母版 | `SKILL.md` + `structure.json`（结构规则唯一真源）+ `scripts/extract.py`（薄壳，引擎复用工厂 `common/`） |
| 改一本书的代价 | 重新反思定层 → 改实例 SKILL.md                                                             | **改 `structure.json`，不碰代码**                                                        |
| 已产出     | 01 / 02 / 03 / 04                                                                 | 05                                                                                 |

两者的关系：工厂 A 管「这本书该建哪些语义层」，工厂 B 管「这本书的正文怎么拆成卷/条」。**要做完整的知识工程用 A；只是想把书拆开看用 B。** 台账里也写明 B 及其产物不属 A 的生态。

### 6.2 书实例清单

| 目录                           | 书    | 出自 | 启用层 / 结构                                                        | 源文本（实例内相对路径）                                 |
| ---------------------------- | ---- | -- | --------------------------------------------------------------- | -------------------------------------------- |
| `01-shuidong-riji-knowledge` | 水东日记 | A  | 8 层：实体/职官任职/事件/典章制度/文献资产/人物关系/名录谱牒/古今翻译 + 卷阅读模式 + 跨层索引          | `assets/sources/水东日记.txt`                    |
| `02-qubian-knowledge`        | 蘧编   | A  | 8 层：实体/职官任职/事件/人物关系/文献资产/古今翻译/奏疏谕旨互动/年谱纪年索引 + V2 人工校验 + V3 枚举校准 | `assets/sources/蘧编_结构化.json`                 |
| `03-wuzazu-knowledge`        | 五杂俎  | A  | 11 层：实体/事件/人物关系/名录谱牒/引书索引/名物/方言风俗/作者论说/明代纪事/职官任职/古今翻译 + 卷阅读模式   | `assets/sources/五杂俎.txt`                     |
| `04-kezuozhuiyu-knowledge`   | 客座赘语 | A  | 13 层（含自定义「南京地理古迹层」）+ V2 + V3                                    | 不随实例存放，指向 `kezuozhuiyu-kb/_source/客座赘语_txt/` |
| `05-xianjinyifeng-knowledge` | 先进遗风 | B → **A** | 初版（B）：只做结构提取，2 卷 / 100 段 / 27031 字，无条目标题 → **已由工厂 A 重新实例化为 6 层 KG**（ENT/APPT/REL/EVT/OPN/TRL + V2/V3 + 跨层索引；粒度=空行段落），现驻 `xianjinyifeng-kb/05-xianjinyifeng-knowledge/` | `assets/sources/先进遗风_全本.txt` |

### 6.3 覆盖矩阵：谁有工程、谁有 skill

| 书                      | `-kb/` 工程目录         | 书实例 skill                    |
| ---------------------- | ------------------- | ---------------------------- |
| 水东日记 / 蘧编 / 五杂俎 / 客座赘语 | ✅                   | ✅                            |
| 新官轨范                   | ✅                   | ❌ **缺** —— 它是第一本，做的时候还没有这套工厂 |
| 先进遗风                   | 🚧 **在建**（2026-10-11 起）               | ✅（先 B 后 A，见下）                |

《先进遗风》的路径很典型，值得记一笔：先用**工厂 B** 快速拆出结构（分卷/全本/目录 txt），发现这本书没有条目标题、切条没法直接做；于是交给**工厂 A** 重新反思定层，把粒度定为「空行段落 = 条」，一次定下 6 层 KG 方案，再开 `xianjinyifeng-kb/` 建工程。即 **B 探底、A 定案**。

《新官轨范》仍是唯一缺口：工程已完成，但方案没固化成实例。要补的话，`00-book-knowledge-factory/assets/samples/xinguan-guifan/` 里已经躺着他当年实例化时的**样例**（`instance_skill_example.md` + `reflection_example.md`），照着回填即可，编号取 `06-`。

### 6.4 新开一本书走哪条路

```bash
# A：要建多层知识库（重方案）
#    在会话里调用 book-knowledge-factory，按 ①定向 ②反思 ③实例化 ④试点校验 ⑤交付 走

# B：只做结构提取（快）
cd Skills/book-skill-factory
python generate.py --book /path/to/书.txt            # 交互问询六组问题
python generate.py --book /path/to/书.txt --answers a.json   # Agent 代填答案
cd ../05-xianjinyifeng-knowledge
python scripts/extract.py --mode volumes             # 输出分卷 txt
python scripts/extract.py --mode full                # 输出全本 txt（含目录 + 正文）
```

工厂 B 的铁律：**结构识别不准就改 `structure.json`，不要在实例里写死解析代码**（`HEURISTICS.md` 有六个字段的说明）。实例里的 `extract.py` 是模板渲染出来的，重跑 `generate.py` 会覆盖——手工改动要同步回模板。

---

## 6.6 MCP 服务：两条线（存量线 / 契约线）

> 两条线不重叠：**存量线管「已经长歪的」，契约线管「别让它长歪」。**
> 新书开工走契约线，交付之后才移交存量线接管体检。

### 6.6.1 `tools/kb-mcp/` —— 存量线，枚举治理（P0 只读）

> **⚠️ 只服务已交付的存量书，新书不接入。**
> 它是**事后体检**：扫已有层产物的实际取值、比已有快照与工厂库。新书还没有产物可扫，接进来只会空转。

六部书的枚举散在五种互不兼容的载体里（工厂 Markdown 库、四种形态的 `_kg_enums.py`、
层产物 JSON），人工核对既慢又容易漏。`tools/kb-mcp/` 把它变成可查询、可比对的工具。

**当前 P0：全部只读**，不写任何文件。六个工具：

| 工具 | 回答什么 |
|---|---|
| `kb_books` | 哪几本书能被读到？各自枚举后端是什么形态？ |
| `enum_list` | 工厂基准库 / 某本书现在有哪些规范值和别名？ |
| `enum_get` | 某个值到底有没有定义？在层产物里被用了多少次？ |
| `enum_drift` | **层产物实际跑出多少种取值，有没有超出定义集？** |
| `enum_sync` | 工厂库 / 实例 `_kg_enums.py` / `schemas.md` 三处差多少？ |
| `enum_checklist` | 缺兜底值吗？树超深吗？哪一层压根没有枚举护栏？ |

零第三方依赖（手写 MCP 协议，标准库实现），既可挂为 MCP 服务，也能直接命令行跑：

```bash
cd tools/kb-mcp
python server.py selftest                      # 自检
python server.py drift --book kezuozhuiyu-kb   # 漂移报告
python server.py checklist                     # 全库体检
```

首次体检暴露的三件事：**客座赘语 6 层漂移 / 704 条库外记录**（#27 的实时佐证）；
**新官轨范 proc、struct 两层完全没有枚举定义**（942 条记录无护栏）；
蘧编与客座赘语**没有单点 `_kg_enums.py`**，只能用工厂库当基准。

详见 `tools/kb-mcp/README.md`。（P1 写链路已冻结——不为已完成的旧书补 add/deprecate。）

### 6.6.2 `tools/book-mcp/` —— 契约线，新书格式契约（C0 只读）

> **给第 7 本及以后的新书用。** 存量书不归它管。

不治理数据，**只回答「格式是什么」**：目录结构、ID 命名空间、底座、层定义、
枚举单点、产物交付、元数据，共 **C1–C7 七条**。契约本体是 `contract.json`（机器可读，唯一真源），
`server.py` 只是读取并回答，零第三方依赖。

```bash
cd tools/book-mcp
python server.py selftest              # 自检（20 项）
python server.py list                  # C1–C7 七条契约
python server.py get --id C5           # 某条契约（如 C5 = 枚举单点必建）
python server.py layers                # 层库全部候选层（22 项）
python server.py layer --key appt      # 某一层（key / code / 前缀 / 名称片段均可）
python server.py enums                 # 基准枚举库 17 组
python server.py enum --group EVENT    # 某组枚举：顶层值 + 子类值 + 别名映射
```

六个工具：`contract_list` / `contract_get`（格式怎么定）、
`layer_list` / `layer_get`（层怎么定义）、`enum_list` / `enum_get`（基准枚举值有哪些）。

每条契约带 `why`（现状为什么乱）、`rules`（可校验点）、正反例与条文出处。
`rules` 已按 `{check, args}` 结构化，将来 `book_check` 可直接遍历执行。
**层定义与枚举值不抄进契约**——运行时从 `Skills/00-…/references/` 实时读，避免副本过期。

**当前只做 C0**（最小的处理）：不扫任何书的数据、不生成脚手架、不做 `book_check`、不提供增改删。

详见 `docs/mcp-契约规划.md`。

> **新书怎么起步**：见 `docs/新书开工流程.md`——把「工厂五阶段 → 四段式管线 → 格式契约」
> 串成一条动线，含命令序列与逐步自检清单。

### 6.6.3 `tools/kb-federation/` —— 联邦线，跨书合并成统一库（F0-a + F1 已完成）

把六本书的产物合并进一个 SQLite（零依赖）联邦库：复合主键 `(book_id, …)` 隔离撞号、
所有层统一落 `records` 表、原文只存指针、Tier1/2 全部可重建（库文件 `kb.sqlite` 不入库）。

- **F0-a 撞号体检已实证**：总 ID 14302 / 跨书撞号 2847（ENT 2448 为主）——正是复合主键隔离要解决的硬约束。
- **F1 先进遗风单书试点已实证**：`items=100`、`records=19`（ent9/appt2/rel1/event2/opn1/trl4）、零主键重复、重跑幂等。
- 用法：`python tools/kb-federation/federation.py create|collision|extract|load --book xyf`
- 设计：详见 `docs/跨书合并方案.md` / `docs/跨书合并-ELT设计.md` / `docs/跨书合并-数据库设计.md` / `docs/跨书合并-ELT实现步骤.md`。

> **三线条关系**：存量线（`kb-mcp`）治已交付书的体检、契约线（`book-mcp`）管新书格式、联邦线（`kb-federation`）
> 消费六书产物做跨书合并——三条互不修改，联邦线只读六书、绝不回写。

---

## 7. 环境要求与源文本放置

- Python **3.12+**（五书均只用标准库，无第三方依赖，无需 `pip install`）
- **所有路径都是相对的**：脚本用 `os.path.dirname(os.path.abspath(__file__))` 自行推导项目根，  
  整个目录拷到任何机器、任何盘符都能直接跑，不需要改代码。

原书正文不入库（体积大且涉整理者署名与版权）。放在各项目根目录的 `_source/` 下即可被自动找到：

| 项目                  | 放到 `_source/` 的文件       | 覆盖用环境变量   |
| ------------------- | ----------------------- | --------- |
| `kezuozhuiyu-kb/`   | `客座赘语_txt/`（10 卷分卷 txt） | `KZZ_SRC` |
| `wuzazu-kb/`        | `五杂俎.txt`               | `WZZ_TXT` |
| `shuidongriji-kb/`  | `水东日记.txt`              | `SDR_TXT` |
| `xinguanguifan-kb/` | `新官轨范.txt`              | `XGG_TXT` |
| `qubian_kb/`        | `蘧编_结构化.json`           | `QB_SRC`  |

优先级：**环境变量 > `_source/` 默认位置**。想放在别处就设环境变量，脚本逻辑不用动。  
各 `_source/README.md` 里有逐步说明。

---

## 8. 仓库约定：什么入库，什么不入库

见根目录 `.gitignore`，原则一句话：**只存「丢了就再也拿不回来的东西」**。

| 入库 ✅                                                | 不入库 ❌（可 `build_*.py` 重跑）                       |
| --------------------------------------------------- | ---------------------------------------------- |
| 所有 `.py`（打包器、验证器、`_src/`、`sources/`、各 `*_ai_NN.py`） | `_extract/` 底座切分正文                             |
| `_item_registry.json` 条粒度指纹库（重建成本高）                 | `_layers/`、`_build/`、`_validate/`、`data/` 分层产物 |
| `README` / `口径规范.md` / 各书复盘与总结                      | `归一_*.json`、`_kg_join*.json`、`层聚合/` 巨量聚合       |
| `skill/`、`samples/`、`references/`                   | `__pycache__/`、`*.pyc`                         |


| `_deliver/` 里的报告与 CSV | `*.zip`、`*_global_layers/`、`*.epub`、阅读器 `raw/` |  
| `新官轨范_阅读器/*.html`、`data.js` | `_tmp*/`、`_backup*/`、`_shots/`、`.dumate/` |  
| `_source/README.md`（放置说明） | `_source/` 里的原书正文与源数据 |  
| `Skills/` **整个目录**（两套工厂 + 6 个实例） | `Skills/**/__pycache__/` |

> 原始体积约 275 MB，按上表裁剪后入库约 **31 MB / 1105 个文件**（不含本次新增的 `Skills/`，约 2.3 MB）。
>
> **一处已声明的例外**：`Skills/*/assets/sources/` 里的原书正文**随 skill 入库**（合计约 1.6 MB）。  
> 理由是书实例要能自包含执行（台账把「源文件（实例内相对路径）」列为实例的登记字段）。  
> 若不想公开这些正文，在 `.gitignore` 追加一行 `**/assets/sources/**` 即可，skill 的其余部分不受影响。

---

## 9. 已知待办

- ~~**硬编码本机路径**~~ ✅ 已解决：全部脚本改为由 `__file__` 推导项目根，源文本走 `_source/` + 环境变量。
- **《客座赘语》侧需按 v4 回溯存量**：`00-book-knowledge-factory` 的枚举库已升 **v4**（回写客座全卷增量八组：GEO 新段 / LIT 四部树 / 事件 +4 顶层 / 名物 / 风俗 / 涉明 / 名录 / 实体），
  但客座实例 `references/schemas.md` 与实际数据仍是旧口径（GEO 跑出 52 种子类、EVT 111 种），需按归并表 registerVersion+1 回溯，走 `increment-upgrade.md`。
- **《先进遗风》实例有两份**：`Skills/05-xianjinyifeng-knowledge/`（工厂 B 初版，只剩 SKILL.md + schemas.md + 模板）与
  `xianjinyifeng-kb/05-xianjinyifeng-knowledge/`（工厂 A 重做的 6 层版，在活跃开发）。工程完工后应保留后者、归档前者。
- **新实例的枚举快照仍是 v3 口径**：`xianjinyifeng-kb/.../references/schemas.md` 写的是 ENTITY 18 值 / EVENT 23 值，
  而基准库已升 v4（20 / 27）。本书讲名臣清操轶事，`异闻` `宗教` 两类新顶层可能用得上，实例化收尾时同步一次。
- **层命名未统一**：同为职官层，有的叫 `appt`、有的在 `data/appt/`；交付目录有 `_deliver/` 与 `交付物/` 两种写法。后续可考虑抽一层公共包。
- **《水东日记》阅读器只有设计稿**：`交付物/Vue3多书知识阅读器设计文档.md` 尚未实现前端（全书知识资产本身已完成）。
- **两条 MCP 线要分清**：
  - **存量线** `tools/kb-mcp/`（已落地，P0 只读）：服务六本已交付的书，做漂移/同步/体检。
    写操作（`propose / review / add / deprecate`）还没做，且**客座赘语、蘧编缺 `_kg_enums.py` 单点**（P1.5 前置）。
    ⚠️ 对已完成书籍做写链路价值有限——真正的教训应由**下一本书的契约线**承接，不再回头补旧书。
  - **契约线** `tools/book-mcp/`（**已落地 C0**，`docs/mcp-契约规划.md`）：面向第 7 本及以后的新书，
    **开工前规定格式**（目录 / ID 命名空间 / 底座 / 层定义 / 枚举单点 / 产物 / 元数据，C1–C7），
    把"长歪"挡在写入之前。当前只回答格式，**不做校验与生成**（C1/C2 待定）。
- **子项目 README 的「当前状态」章节可能过期**：五本的知识资产实际均已装填完成（本书目表已按实测核对），  
  但各子项目 README 里的进度段落是不同时点写的。`shuidongriji-kb/README.md` 已修正，其余四本待下次动工时同步。
