# kb-mcp —— 古籍知识工程 MCP 服务（**存量线 / legacy**）

> ## ⚠️ 定位：只服务「已交付的存量书」，新书不要接入本服务
>
> 本服务是**事后体检工具**——它的全部价值建立在「书已经做完了、层产物已经跑出来了」这个前提上。
> `enum_drift` 扫的是已有 `_layers/*.json` 的实际取值，`enum_sync` 比的是已有快照与工厂库。
> 对**还没开始的新书**而言，这些接口全部无输入可扫，等于空转——这是本服务的边界，不是缺陷。
>
> - ✅ **适用**：`kezuozhuiyu-kb` / `wuzazu-kb` / `shuidongriji-kb` / `xinguanguifan-kb` /
>   `qubian_kb` / `xianjinyifeng-kb` 这六本**已交付或在执行**的书，做存量漂移与三处同步体检。
> - ❌ **不适用**：第 7 本及以后的新书。新书要的是「开工前就把格式定死」，
>   走**契约线** —— `tools/book-mcp/`（C0 已落地：`contract.json` + `contract_list` / `contract_get`）。
>
> 一句话区分：**kb-mcp 治"已经长歪的"，契约线管"别让它长歪"。**
> 新书交付之后，才移交到本服务接管体检。

把「枚举治理」从**人工读 Markdown**变成**可查询、可比对、可体检**的工具。

当前阶段：**P0，全部只读**。不写任何文件，不改动任何一本书的数据。

---

## 1. 它解决什么

枚举散在五种互不兼容的载体里（工厂 Markdown 库、四种形态的 `_kg_enums.py`、
层产物 JSON），一次「新增一个值」要同步三处并双写 changelog——客座赘语那次
（`pitfalls.md` #27：EVT 跑到 111 种、LIT 114 种）本质就是这三件事全漏了。

P0 不解决"加值"，只解决**发现问题**：

| 工具 | 回答什么 |
|---|---|
| `kb_books` | 哪几本书能被读到？各自的枚举后端是什么形态？ |
| `enum_list` | 工厂基准库 / 某本书现在有哪些规范值和别名？ |
| `enum_get` | 某个值到底有没有定义？在层产物里被用了多少次？ |
| `enum_drift` | **某本书的层产物实际跑出了多少种取值，有没有超出定义集？** |
| `enum_sync` | 工厂库 / 实例 `_kg_enums.py` / `schemas.md` 三处差多少？ |
| `enum_checklist` | 缺兜底值吗？树超深吗？哪一层压根没有枚举护栏？ |

`enum_drift` 是核心：客座赘语那类事故，靠它能在装填期当场暴露，而不是等交付复盘。

---

## 2. 快速开始（不需要装任何东西）

**零第三方依赖**，只用 Python 标准库，随仓库即用：

```bash
cd tools/kb-mcp

python server.py selftest                      # 跑一遍全部工具，验证可跑通
python server.py books                         # 列出受管辖的书
python server.py drift --book kezuozhuiyu-kb   # 漂移报告
python server.py sync   --book wuzazu-kb       # 三处一致性
python server.py checklist                     # 全库体检
python server.py list --scope factory --enum GEO
python server.py get --enum ENTITY --value star
```

加 `--format json` 可以拿到完整结构化输出（默认 `brief` 是人类可读简报）。

---

## 3. 作为 MCP 服务挂载

协议：`initialize` / `tools/list` / `tools/call`，JSON-RPC 2.0 over stdio，
协议版本 `2024-11-05`。日志走 stderr，stdout 只有协议消息。

在 `~/.workbuddy/mcp.json` 的 `mcpServers` 里加：

```json
{
  "guji-kb-enum": {
    "command": "python",
    "args": ["E:/git/ToolBox/guji/tools/kb-mcp/server.py"]
  }
}
```

> 路径换成你本机的实际路径。注册后需要在连接器管理页点「信任」才会生效。
> 想用其它 Python 解释器，把 `command` 换成绝对路径即可。
> 建议注册名保留 `-legacy` 之类后缀（如 `guji-kb-enum-legacy`），
> 与将来的契约线服务区分开，避免 Agent 拿到新书却调用了体检工具。

**为什么不用官方 MCP SDK**：六本书的管线是「纯标准库零依赖」（见根 README §6）。
P0 只读场景用不上 SDK 的高级能力，因此手写协议，避免仓库多出一份需要
`pip install` 的东西。若后续 P2 需要资源订阅等能力，再评估引入。

---

## 4. 作用域与只读边界

| 数据 | 权限 | 理由 |
|---|---|---|
| 工厂 `enum-library.md` / `enum-changelog.md` | 读 | 权威基准 |
| 各书 `_kg_enums.py` | 读 | 实例快照 |
| 各书 `schemas.md` | 读（文本命中判断） | 第三处一致性线索 |
| 层产物 `_layers/` `data/` | 读 | drift 的数据源 |
| `ent_keys.json` | 读 | 累积状态，P4 才开放写 |
| `_item_registry.json` | **不碰** | 原文唯一源，四条铁律之一 |

P0 不提供任何写接口。写操作（propose / review / add / deprecate）在 P1–P2，
且必须过护栏链：归并优先 → 证据必填 → version+1 → 回溯存量 → 双写 changelog。

---

## 5. 首次体检结果（2026-10-11）

对六本书实跑 `enum_drift`：

| 书 | 层数 | 记录数 | 漂移层 | 无基准层 | 库外记录 |
|---|---|---|---|---|---|
| 客座赘语 | 8 | 11967 | **6** | 0 | **704** |
| 五杂俎 | 6 | 7350 | 0 | 0 | 0 |
| 水东日记 | 5 | 2793 | 0 | 0 | 0 |
| 新官轨范 | 5 | 3927 | 0 | **2** | 1137 |
| 蘧编 | 6 | 1810 | 0 | 0 | 115 |
| 先进遗风 | 2 | 11 | 0 | 0 | 0（在建，样本极小） |

要点：

- **客座赘语 6 层漂移**是 #27 的实时佐证：LIT 实际 114 种 / OBJ 72 种 / MING 94 种 /
  GEO 58 种 / CUS 53 种 / EVT 111 种。基准已升 v4，但**实例侧存量还没回溯**。
- **新官轨范 proc / struct 两层完全无枚举定义**（548 + 394 条记录处于无护栏状态），
  工厂库里既没有 `PROC` 也没有 `STRUCT` 段——这是新书接入时的真实盲区。
- **五杂俎、水东日记库外 0**：它们的打包器带封闭集硬校验，确有效果。
- 蘧编、客座赘语**没有单点 `_kg_enums.py`**，只能用工厂库当基准（P1.5 要补的前置）。

---

## 6. 设计取舍

**适配器优先，不假设统一后端。** 四态并存（五杂俎 `BASE_ENUMS` 运行时 + 原子写 /
先进遗风 `ENUM_REGISTRY` 字段路由 / 水东新官纯 dict / 客座蘧编无单点），
所以 `registry.py` 里逐书登记后端与层产物路径，新增一本书只改这张表。

**宁可报「无基准」，不猜基准。** 解析不出来就如实说没有，绝不用猜测的值去支撑
漂移结论——那正是 #27 的成因。

**不解析也不重写 `.py`**。`_kg_enums.py` 是 Python 源码，机器改写风险高；
P0 用 ast 静态解析，拿不到才回退到 import（仅五杂俎 `BASE_ENUMS` 属此类），
且整段包在 try 里。

**第三处（schemas.md）只做文本命中，不做结构解析。** 各书排版差异极大，
结构解析的误报率高于收益；文本命中足以发现"快照没跟上工厂库"。

---

## 7. P0 明确不做

- ❌ 不写任何文件（P1 起才有 propose / review）
- ❌ 不碰 `_item_registry.json`
- ❌ 不提供批量导入（批量入口 = 绕过归并优先，正是 #27 成因）
- ❌ 不做硬删除（只有 deprecate）
- ❌ 不在 MCP 里做 AI 判定——判定主体仍是人/AI 逐条，代码只负责收集与比对

---

## 8. 文件结构

```
tools/kb-mcp/
├── server.py              # MCP 协议（stdio）+ CLI 自检入口，零依赖
└── kb_mcp/
    ├── registry.py        # 书注册表：后端形态、层产物路径、枚举名归一（唯一需人工维护）
    ├── adapters.py        # 五种载体的读取适配 + 层产物扫描
    └── tools.py           # 六个只读工具
```

---

## 9. 参考

- 规划全文：`docs/mcp-规划.md`（P0–P4 路线与待办）
- `Skills/00-book-knowledge-factory/references/enum-library.md`（权威源 v4）
- `Skills/00-book-knowledge-factory/references/enum-changelog.md`（版本历史）
- `Skills/00-book-knowledge-factory/references/pitfalls.md` #27（封闭枚举被就地吸收）
