# 古籍知识工程 MCP 服务规划（草案 v1）—— **存量线**

> 提出：2026-10-11 用户提议「做一个 MCP 服务，list / add / update / delete / checklist 管理枚举，并扩展到每一层，方便动态更新 ent」。
> 状态：**P0 已落地（`tools/kb-mcp/`）；P1 及以后冻结，不再推进。**
> 定位一句话：**MCP 是治理流程的执行器，不是文件编辑器。** 这条决定了它值不值得做。

> ## ⚠️ 2026-10-11 定位修正：本规划的服务对象收缩为「存量书」
>
> 用户指出：**MCP 的价值应该给之后的书用，前面的书已经做完了，回头治理是次要的。**
> 这条判断成立——P0 的 `enum_drift` / `enum_sync` 全部依赖「层产物已存在」，
> 对未开工的新书零输入；而给已交付的书补 `add/deprecate/backfill` 写链路，
> 属于**为过去的错误买单**，边际收益远低于让下一本书别再犯。
>
> 因此：
>
> | 线 | 服务对象 | 时机 | 状态 |
> |---|---|---|---|
> | **存量线**（本文） | 已交付的 6 本 | 事后体检 | P0 已落地，P1+ **冻结** |
> | **契约线**（`docs/mcp-契约规划.md`） | 第 7 本起的新书 | 开工前定格式 | 规划中，待拍板 |
>
> 本文以下内容保留作**存量体检的设计依据**，但其「P1–P4 写链路路线」不再主动推进；
> §5 护栏链、§8 明确不做的事，这些纪律整体迁移到契约线，变成**新书的准入校验**。
> 真正该沉淀的教训只有一句：**让格式在开工前就定死，别等跑完了再回头数。**

---

## 1. 结论先行

**可以做，而且现在正是时候**——因为五杂俎的 `_kg_enums.py` 已经长出了运行时（`BASE_ENUMS` / `canonical` / `_PENDING` / 原子写），先进遗风又有字段路由（`ENUM_FIELD_MAP` + 打包器硬校验）。它们合起来就是 MCP 的现成内核，不必从零造。

但要清醒：**真正的痛点不是"加个值慢"**（手改 Markdown 一分钟的事），而是这三件事最容易漏——

1. 工厂库 / 实例 `_kg_enums.py` / 实例 `schemas.md` **三处同步**；
2. `registerVersion+1` 后**回溯存量**；
3. 入库**双写** `enum-changelog.md`。

客座赘语那次事故（EVT 跑到 111 种、LIT 114 种，`pitfalls.md` #27）本质就是这三件事全漏了。所以 MCP 的价值 = **把纪律代码化**，而不是把改文件变快。

**最大的反向风险**：如果 MCP 让 `add` 太顺手，会加剧"随手造值"。因此设计上必须反向加摩擦（见 §5 护栏链）。

---

## 2. 现状盘点（决定了设计约束）

### 2.1 枚举有「四态」，不能假设统一后端

| 载体 | 形态 | 运行时能力 | 状态落盘 |
|---|---|---|---|
| 工厂 `enum-library.md` | Markdown 规范值表（v4） | 无 | 无 |
| **五杂俎** `_kg_enums.py`（380 行） | `BASE_ENUMS{version, tree, canonical, alias}` | `normalize_value` / `is_valid` / `validate` / `register_version` / `tree_report` / `dump_summary` / `flush_pending` | ✅ `_enum_state.json` + pending，**tmp+os.replace 原子写** |
| **先进遗风** `_kg_enums.py`（217 行） | `ENUM_REGISTRY` + `ENUM_FIELD_MAP` | 按层×字段做封闭集硬校验（validate 维度 E4：未注册记 ERR、比值 >1.5 告警） | ❌ |
| 水东（237 行）/ 新官（38 行） | 纯 `dict` + `*_VERSION` 常量 | 无校验 API | ❌ |
| **客座赘语 / 蘧编** | **无单点枚举文件**，值内嵌在各打包器里 | — | ❌ |

→ **结论**：MCP 必须先做一层**适配器（adapter）**，按书路由到不同后端；不能写死一种读写方式。
→ **前置任务**：客座、蘧编补出 `_kg_enums.py`（否则这两本进不了 MCP 管辖，仍是野分支温床）。

### 2.2 「动态更新 ent」要分清三种数据，权限完全不同

这是本规划最需要澄清的一点——用户说的"动态更新 ent"可能指三种东西，**只有第一种可写**：

| 数据 | 文件 | 性质 | MCP 权限 |
|---|---|---|---|
| 实体主键表 | `ent_keys.json`（`{meta, entities[], alias_index, normalized_inventory, pending}`，entity = `{ent_id, key, normalized, type, count, first_source, surfaces[]}`） | **累积状态，不可重建**（先查后建的产物） | ✅ 可读写（这正是"去重合并"场景） |
| 层产物 | `_layers/ent_01.json`、`data/ent/*.json` | **可重建**（由源数据 + 打包器生成） | ❌ 不可直接改——改了会被重跑覆盖，等于白改 |
| 原文指纹库 | `_item_registry.json`（`{item_id: {original, …}}`） | **原文唯一源**（四条铁律之一） | ⛔ 只读，MCP 一律不碰 |

→ 所以"方便动态更新 ent"的正确落法是：**改 `ent_keys.json`（实体表）+ 改 `_src/` 源数据 + 重跑该卷**，而不是直接改层产物。MCP 要引导到这条路径，不能提供"直接改 `ent_01.json`"的快捷方式。

---

## 3. 作用域模型

所有工具都带 `scope` 参数，三者隔离：

| scope | 目标 | 影响面 | 默认 dry-run |
|---|---|---|---|
| `factory` | `Skills/00-…/references/enum-library.md` + `enum-changelog.md` | **全部 6 本书** | ✅ 强制先 dry-run |
| `instance` | 某书的 `_kg_enums.py` + `references/schemas.md` | 单本书 | 否 |
| `data` | 某书的 `ent_keys.json` / pending 表 | 单本书某层 | 否 |

跨作用域操作（如工厂新增值后同步到各实例快照）走独立的 `sync` 工具，显式触发，不隐式联动。

---

## 4. 工具集设计

用户提议的 `list / add / update / delete / checklist` 我做了两点改造，理由见右列：

| 用户提议 | 规划方案 | 为什么改 |
|---|---|---|
| `list` | `enum_list` / `enum_get` / `ent_list` / `ent_search` | 保留，另加实体检索 |
| `add` | `enum_propose` → `enum_review` → `enum_add` | **拆成两步**：先入 pending 待评审区，评审通过才真入。直接 `add` = 绕过 `pending-review.md` 门槛制（`methodology.md` §2.5） |
| `update` | `enum_update`（改名 / 改 doc / 加别名） | 改名必须带存量回溯映射 |
| `delete` | `enum_deprecate`（**软删**） | 硬删会破坏已引用该值的存量数据；软删 = 标 `deprecated` + 保留别名映射指向替代值 |
| `checklist` | `enum_checklist`（健康度）+ `enum_drift`（漂移报告）+ `enum_sync`（三处一致性） | 这是真正值钱的部分 |

### 4.1 只读工具（P0，零风险）

```
enum_list(scope, book?, enum?)        # 列规范值 + 别名 + 使用说明 + 版本
enum_get(scope, book, enum, value)    # 单值详情：正反例、来源、首建实例
enum_drift(book)                      # 实际值种数 vs 定义数，比值 >1.5 判漂移
enum_sync(book)                       # 工厂库 / _kg_enums.py / schemas.md 三处差异
enum_checklist(book)                  # 兜底值是否存在、深度是否 ≤3、父类计数=子类求和
```

### 4.2 写工具（P1+，全部过护栏）

```
enum_propose(book, enum, value, evidence)      # 入 pending（含归并建议）
enum_review(book, pending_id, decision)        # 决议：新增 / 归并到 X / 暂存
enum_add(...)                                  # 真入库（内部跑 §5 全链）
enum_update(book, enum, old, new, backfill?)   # 改名 + 回溯映射
enum_deprecate(book, enum, value, replaced_by) # 软删 + 替代值
enum_backfill(book, dry_run=True)              # 存量回溯，默认只预览
```

### 4.3 层扩展工具（P4）

```
ent_search(book, query, type?)        # 先查（含别名命中）
ent_add(book, normalized, type, source)   # 后建（自动查重）
ent_merge(book, keep_id, merge_ids)   # 实体去重合并——客座赘语 223 实体那类场景
ent_alias(book, ent_id, alias)        # 加别名（如"刘忠宣"→刘大夏）
ent_stats(book)                       # 类型分布、未决待核清单
```

> `ent_merge` 是刚需：《客座赘语》有过一次全局实体去重（223 实体、`merge_map.json`），现在靠 `_global/apply_merge_map.py` 一次性脚本做。做成工具后这类操作可复用、可审计。

---

## 5. 护栏链（每次写操作必过，缺一步即拒绝）

```
① 归并优先 → ② 证据必填 → ③ registerVersion+1 → ④ 回溯存量 → ⑤ 双写 changelog
```

| 步 | 规则 | 违反后果 |
|---|---|---|
| ① 归并优先 | 新值先查别名表与归并映射表（`enum-library.md` §1.3.3）；命中近义则强制走"归并"，不得新增 | 值爆炸（#27） |
| ② 证据必填 | `evidence` 参数必填，须含条目号与原文片段；`factory` 级还要求"≥2 条或多卷出现" | 拍脑袋造值 |
| ③ version+1 | 自动递增 `REGISTER_VERSION` / 段内 `version`，拒绝手改 | 快照比对失效 |
| ④ 回溯存量 | 默认 `dry_run=True`，输出"将改写 N 条"预览；只对显式 `apply=True` 落盘 | 新旧口径混杂 |
| ⑤ 双写日志 | 改 `enum-library.md` 必须同时追加 `enum-changelog.md` 版本条目 | 历史断档（客座教训） |

`factory` 级操作额外要求：预览**受影响实例清单**（哪些书的快照会失配），并要求显式确认。

---

## 6. 技术方案

| 项 | 方案 | 说明 |
|---|---|---|
| 形态 | Python MCP server，**stdio 传输** | 本地工具，不需要 HTTP |
| 依赖 | `mcp` 或 `fastmcp`，装在**独立 venv** | ⚠️ 现有六本书是**纯标准库零依赖**（README §6 明文）。MCP server 是**外围工具、不进管线**，单独 venv 不破坏该原则——但必须在 README 写清这条边界 |
| 落盘 | 复用五杂俎的 `tmp + os.replace` 原子写 | 已验证模式，避免写坏文件 |
| 并发 | 单进程 + 文件锁（`.lock`） | 防止多会话同时改工厂库 |
| 注册 | 写入 `~/.workbuddy/mcp.json` | 需用户在连接器管理页点「信任」才生效 |
| 代码位置 | 建议 `tools/kb-mcp/`（仓库根新建） | 与书籍目录平级，跨书共用 |

### 6.1 关键技术难点：`_kg_enums.py` 是 Python 源码

机器改写 Python 源码（保留手写注释、兼顾 4 种形态）风险很高。建议方案：

**引入 `_enum_state.json` 作为唯一可变状态**，`_kg_enums.py` 降级为「加载器 + 手写注释区」。

- 五杂俎已经铺好这条路（它已有 `_load_state()` / `save_state()` / `ENUM_STATE_PATH`）；
- 其余书按同构改造；
- MCP 只读写 JSON，**永不解析/重写 `.py`**，把风险面缩到最小；
- 手写注释（如先进遗风顶部那段"与基准库 v4 的差异注记"）保留在 `.py` 里，不受影响。

---

## 7. 分阶段路线

| 阶段 | 内容 | 验收标准 | 风险 |
|---|---|---|---|
| **P0** | 只读四件套：`list` / `get` / `drift` / `sync` / `checklist` | 能对任一书跑出漂移报告；能报出三处不同步 | 零（只读） |
| **P1** | pending 工作流：`propose` / `review` | 新值只能经 pending 入库，pending 表与 `pending-review.md` 打通 | 低 |
| **P1.5** | **前置**：客座、蘧编补 `_kg_enums.py`；五态归一到 `_enum_state.json` | 6 本书都能被 `enum_list` 读到 | 中（要动老脚本） |
| **P2** | 写工厂库：`add` / `update` / `deprecate` + 双写 changelog + `backfill --dry-run` | 完整跑通"新增一个值"的端到端，changelog 自动追加 | 中 |
| **P3** | `sync` 跨作用域：工厂 → 实例快照同步 | 工厂改一个值，能列出受影响实例并生成同步补丁 | 中高 |
| **P4** | 层扩展：`ent_search` / `ent_add` / `ent_merge` / `ent_alias` | 替代 `_global/apply_merge_map.py` 一次性脚本 | 高（碰数据） |

**P0 + P1 就能回本**——漂移与三处同步的检测，正是现在最缺、也最容易出事的两件事。P2 之后每步都建议先在《先进遗风》（最小、最新、最干净）上试点。

---

## 8. 明确不做的事

- ❌ **不提供直接改 `_layers/*.json` / `_build/` 的接口**——产物可重建，改了会被重跑覆盖，是伪操作。
- ❌ **不碰 `_item_registry.json`**——原文唯一源，只入不出。
- ❌ **不做"批量导入枚举"**——批量入口等于绕过归并优先，正是 #27 的成因。
- ❌ **不做硬删除**——只有 `deprecate`。
- ❌ **不在 MCP 里做 AI 判定**——判定主体仍是 AI 逐条（代码只收集、不代判，`enum-induction-guide.md` §2）。

---

## 9. 待你拍板的四个问题

1. **范围**：先做 P0+P1（只读 + pending，约回本 80%、零风险），还是一次性做到 P2（能写工厂库）？
2. **依赖边界**：接受"MCP server 装在独立 venv、不进任何一本书的管线"吗？（否则会破坏"纯标准库零依赖"这条，六本书的脚本都得跟着变）
3. **形态归一**：接受 P1.5 吗？——把 4 种 `_kg_enums.py` 统一到「`_enum_state.json` + 加载器」，客座/蘧编还要先补出单点枚举文件。这一步要动老脚本，但它是后面所有阶段的地基。
4. **层扩展优先级**：`ent_*` 工具里最想要哪个？我判断 `ent_merge`（实体去重合并）最刚需，其次 `ent_search`（先查）。

---

## 10. 参考

- `Skills/00-book-knowledge-factory/references/enum-library.md`（权威源 v4）
- `Skills/00-book-knowledge-factory/references/enum-changelog.md`（版本历史）
- `Skills/00-book-knowledge-factory/references/enum-induction-guide.md`（流程与判定标准）
- `Skills/00-book-knowledge-factory/references/pitfalls.md` #27（封闭枚举在执行期被就地吸收）
- `Skills/00-book-knowledge-factory/references/increment-upgrade.md`（实例变更唯一通道，MCP 的写操作须与之对齐）
- `wuzazu-kb/_kg_enums.py`（现成的枚举运行时，内核参考）
- `xianjinyifeng-kb/05-xianjinyifeng-knowledge/scripts/_kg_enums.py`（字段路由 + 硬校验，内核参考）
