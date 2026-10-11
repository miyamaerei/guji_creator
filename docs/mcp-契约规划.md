# 新书契约 MCP 规划（草案 v1）—— **契约线**

> 提出：2026-10-11 用户指出「MCP 应该给之后的书用；对已做完的书做治理是无用功，**MCP 只要规定一个格式就好了**」。
> 状态：**待拍板**。本文只做规划，未写任何服务代码。
> 定位一句话：**开工前把格式定死，让"长歪"这件事根本没机会发生。**

---

## 1. 结论先行

存量线（`tools/kb-mcp/`，见 `docs/mcp-规划.md`）做的事是**跑完之后数一遍**：
扫 `_layers/*.json` 的实际取值，比快照与工厂库，报漂移。
它有价值，但价值是**复盘性的**——客座赘语那 704 条库外记录，报到的时候早就写进去了。

对**第 7 本及以后的新书**，正确姿势是反过来：

```
格式在开工前定死 → 脚手架按格式生成 → 每步写入前按格式校验 → 长歪的当场被拒
```

所以新 MCP **不治理数据，只规定格式**（contract），并提供按格式**生成**与**校验**的能力。
它不需要 `add/update/delete`——那些是治理动作，属于存量线；契约线只要：

| 能力 | 干什么 |
|---|---|
| **规定** | 格式以机器可读形式存一份，人和代码都读同一份 |
| **生成** | 新书按格式长出脚手架，不用每次凭记忆搭 |
| **校验** | 违反格式当场报错，而不是交付后复盘 |

**这就是用户说的"只要规定一个格式就好了"的全部内容。** 做多了就又是无用功。

---

## 2. 与存量线的分工（别再混）

| | 存量线 `tools/kb-mcp/` | 契约线（本文） |
|---|---|---|
| 服务对象 | 已交付的 6 本 | 第 7 本起的新书 |
| 时机 | 事后 | 事前 |
| 核心动作 | 比对、漂移、同步 | 规定、生成、校验 |
| 对数据 | 只读扫描 | 只在 `book_init` 时写脚手架 |
| 状态 | P0 已落地，P1+ 冻结 | 待拍板 |

新书**交付之后**才移交存量线接管体检。两条线不重叠、不互相写。

---

## 3. 契约清单：到底要规定哪些格式

这是本规划的主体。每条给出「规定什么 / 现在为什么乱 / 契约怎么定」。
编号 C1–C7，**C 号即机器可读契约里的 key**。

### C1 目录结构

- **规定**：四段式目录各自做什么、哪些必建、交付目录叫什么。
- **现在的乱**：交付目录有 `_deliver/` 与 `交付物/` 两种写法（根 README §9 已记为待办）。
- **契约**：`_extract`(切条原文) / `_src`(AI 源数据) / `_layers`(层产物) / `_build`(打包) /
  `_validate`(校验报告) / `_deliver`(交付) / `_source`(源文本，不入库)。
  层目录一律放 `_layers/<layer_key>/`，不另开 `data/<layer>/`（见 C4）。

### C2 ID 命名空间

- **规定**：`item_id = NN-NNN`（卷-序，全书唯一）；每层一个 ID 前缀，**前缀不得跨层占用**。
- **现在的乱**：`schemas.md` 已有前缀表（ENT- / XGF-R- / XGF-P- / XGF-E- / LGR,TME,DOC,ACT,FRD- / `_kg_join`），
  但它是**示例表**（XGF 是《新官轨范》专用），新书照抄就会撞命名空间。
- **契约**：开工时登记 `prefix_registry`——层 key → 前缀，登记后唯一；新增层必须先申请前缀。
  校验项：`item_id` 正则、前缀全局唯一、同前缀不跨层。

### C3 底座：`_item_registry.json`

- **规定**：扁平 dict，`{item_id: {original, norm}}`；**原文唯一源，只入不出**；
  `_src/` 里的 AI 源数据**不手抄原文**，只写条号与解读字段，由打包器注入 `original`。
- **契约**：写死 shape + 只读标记。这是四条铁律之一，校验器要能报"你把原文抄进 `_src/` 了"。

### C4 层定义（最需要定死的一条）

- **规定**：启用哪些层、每层叫什么、放哪、字段有哪些、ID 前缀是什么、哪些字段受枚举护栏。
- **现在的乱**：同为职官层，有的叫 `appt`、有的放 `data/appt/`（根 README §9）。
- **契约**：每层注册一条 `{layer_key, dir, prefix, schema_fields[], enum_fields[]}`。
  **层 key 与目录名必须一致**，取 snake_case 单数形式，不给别名。

### C5 枚举单点（客座/蘧编事故的直接对策）

- **规定**：**每本书必须建单点 `_kg_enums.py`**，打包器只从它读，禁止把枚举值内嵌进打包器。
- **现在的乱**：四种后端并存；客座与蘧编**根本没有单点**，值内嵌在各打包器里，
  于是执行期被就地吸收——EVT 跑到 111 种、LIT 114 种（`pitfalls.md` #27）。
- **契约**（关键三条）：
  1. **后端定一种**：`BASE_ENUMS{version, tree, canonical, alias}` 存值
     （取五杂俎，已验证 + 原子写）+ `ENUM_FIELD_MAP` 做字段路由（取先进遗风）
     + 打包器接**硬校验**（未注册值记 ERR，不静默放行）。
  2. **封闭集 + 兜底值**：归类型枚举必须有"无法归类/待定"兜底（分类型如 APPT/OPN/REL 不强求）。
  3. **值变更走版本**：`version+1` + 双写 changelog —— 这条纪律从存量线整体迁移过来，
     只是执行点从"事后补"前移成"改的时候就拦"。

### C6 产物与交付

- **规定**：层 JSON 必填字段、跨层索引 `_kg_join` 必建、交付物命名（`_deliver/`）。
- **契约**：字段完整性校验 + 交付目录名唯一。

### C7 元数据

- **规定**：实例必须登记进 `registry.md`；SKILL.md frontmatter 的 `name` **必须等于目录名**。
- **现在的乱**：客座赘语 frontmatter 写 `kezuo-zhuiyu-knowledge`，目录是 `04-kezuozhuiyu-knowledge`（`registry.md` 备注已记）。
- **契约**：校验器直接比这两个字符串。

---

## 4. 工具集（就这四个，不多）

```
contract_list()                      # 列出 C1–C7 全部契约项与当前 format_version
contract_get(id)                     # 取某条契约：规定 + 正例 + 反例 + 违反后果
book_init(book, layers, prefixes)    # 按契约生成脚手架：目录 + _kg_enums.py + ID 前缀表 + schemas 骨架
book_check(book)                     # 按契约校验全书，报违反项（C1–C7 逐条）
```

`book_check` 是真正的主力——它把存量线的 `enum_drift` 从"交付后"挪到"写入前"。
其余（`add/update/delete`、`ent_merge`）**一律不做**，那些是治理动作，属于存量线。

---

## 5. 设计原则（四条，都是踩过的坑换来的）

1. **契约必须机器可读。** JSON 是本体，Markdown 只是渲染视图。
   现在枚举散在 Markdown 里要"人工读 + 人工比对"，正是漂移的根源；
   如果契约也写成 Markdown 让人读，等于把同一个坑再踩一遍。
2. **校验前置，不做事后复盘。** 校验器挂在装填/打包之前，违反即拒，不留到交付。
3. **不回头治理存量。** 契约线对旧书**只读不写、不强制回溯**。旧书的账由存量线自己结。
4. **契约自身要版本化。** `format_version` + changelog，改契约走同样的版本纪律。

---

## 6. 契约文件形态（草案，待拍板后落地）

建议落 `tools/book-mcp/contract.json`（零第三方依赖，与存量线同风格）：

```json
{
  "format_version": "0.1.0-draft",
  "dirs": {
    "_extract":  {"required": true,  "note": "NN_卷名.txt，行格式 条N|正文"},
    "_src":      {"required": true,  "note": "AI 源数据，禁止手抄原文"},
    "_layers":   {"required": true,  "note": "层产物，可重建，位置 _layers/<layer_key>/"},
    "_build":    {"required": true},
    "_validate": {"required": true},
    "_deliver":  {"required": true,  "banned_aliases": ["交付物"]},
    "_source":   {"required": true,  "vcs": "ignored"}
  },
  "files": {
    "_item_registry.json": {"required": true, "writable": false,
                            "shape": {"<item_id>": ["original", "norm"]}},
    "_kg_enums.py":        {"required": true, "note": "枚举单点，禁止内嵌打包器"},
    "ent_keys.json":       {"required": "if L1 enabled", "writable": true}
  },
  "id": {
    "item_id_pattern": "^\\d{2}-\\d{3}$",
    "prefix_registry": "层 key -> 前缀，开工登记，全局唯一，禁止跨层占用"
  },
  "layers": {
    "naming": "layer_key 与目录名一致，snake_case 单数，无别名",
    "register_fields": ["layer_key", "dir", "prefix", "schema_fields", "enum_fields"]
  },
  "enum": {
    "backend": "BASE_ENUMS{version,tree,canonical,alias} + ENUM_FIELD_MAP",
    "closed": true,
    "fallback_required_for": ["categorical"],
    "hard_validate_in_packer": true,
    "banned": "内嵌在打包器内的字面量枚举"
  },
  "meta": {
    "registry_md_entry": true,
    "skill_frontmatter_name_equals_dirname": true
  }
}
```

---

## 7. 与已有资产的关系（**不重复造轮子**）

| 已有资产 | 契约线怎么用 |
|---|---|
| `Skills/book-skill-factory/generate.py` | **上游**。它负责"解析源书结构"（`structure.json` + 薄壳 `extract.py`）。<br>契约线接在它**下游**：解析实例建好后，由 `book_init` 长出 KG 目录骨架 + 枚举单点 + ID 前缀表。<br>⚠️ `book_init` 应薄封装/复用模板，**不要另写一套脚手架生成器**。 |
| `Skills/00-…/references/layer-library.md` | 选层的**候选池**（引导参考板，不是强制清单）。选完的层进契约 C4 注册。 |
| `Skills/00-…/references/enum-library.md`（v4） | 新书枚举的**种子值来源**（不是照抄，按书归纳后落单点）。 |
| `Skills/00-…/references/schemas.md` | C2/C3/C6 的**现有条文出处**；契约把它从"示例表"升级成"可校验规约"。 |

---

## 8. 分阶段

| 阶段 | 内容 | 验收 |
|---|---|---|
| **C0** | `contract.json`（C1–C7）+ `contract_list` / `contract_get` | 人问"新书目录该长什么样"，工具能答，且与 Markdown 规约一致 |
| **C1** | `book_check` | 拿《先进遗风》（最小最新）试跑，能报出它违反的契约项 |
| **C2** | `book_init` | 从第 7 本书起，脚手架由它生成，含 `_kg_enums.py` 单点 |
| **C3** | 接入管线：打包器前置 `book_check` | 违反契约即拒，不再静默写入 |

**C0+C1 就够回本**——"格式能被机器回答 + 违反能被当场发现"，其余都是加分项。

---

## 9. 待拍板的四个问题

1. **存量兼容**：C1（交付目录）与 C4（层位置）定死后，旧书是**保持现状**（契约只管新书），
   还是**顺手统一**？我倾向前者——改旧书风险大于收益，且这正是"为过去买单"。
2. **枚举后端**：确认取"五杂俎 `BASE_ENUMS` + 先进遗风 `ENUM_FIELD_MAP` 硬校验"的合体吗？
   还是直接沿用其中一种？
3. **与 `book-skill-factory` 的边界**：`book_init` 是**薄封装**它的模板，还是契约线**只管校验**（`book_check`）不管生成？
   只做校验的话，落地成本最低，也最贴合"只要规定一个格式"。
4. **现在做吗、做到哪**：C0 即可 / C0+C1 / 全做。

---

## 10. 参考

- `docs/mcp-规划.md`（存量线，本文的定位对照）
- `tools/kb-mcp/README.md`（存量线已落地部分，已标注"新书不接入"）
- `Skills/00-book-knowledge-factory/references/schemas.md`（C2/C3/C6 条文出处）
- `Skills/00-book-knowledge-factory/references/layer-library.md`（C4 候选池）
- `Skills/00-book-knowledge-factory/references/enum-library.md`（C5 种子值，v4）
- `Skills/00-book-knowledge-factory/references/pitfalls.md` #27（C5 的直接成因）
- `Skills/book-skill-factory/generate.py`（C2 阶段的上游，勿重复造轮子）
