# 跨书合并 ELT 设计：去歧义合并与关系消歧

> 本文是《跨书合并方案》的落地细化（联邦库四层里的 **L1 装载 + L2 装入 + T 变换**）。
> 聚焦用户两点诉求：**① 所有东西加一层去歧义合并；② 用关系识别同实体**。
> 状态：**F0-a / F1 / F2 / F3 已落地并实证**（2026-10-11）。本文随实现同步细化，
> 尤其 §3 的名字解析已升级为「配置驱动归一化 + 两级接入 + 置信度」。

---

## 1. 一句话设计

```
抽上来（不判断）  →  直载进库（复合主键隔离）  →  库内做去歧义合并（谨慎建链接，不破坏原数据）
     E                          L                              T
```

**「去歧义的合并」语义**（贯穿全局，不只对实体）：

- **物理不合并**——每本书的实体、层记录原样保留，复合主键 `(book_id, local_id)` 隔离。
- **逻辑建链接**——用一个 `canonical`（代表）+ `member`（成员列表）表达「这是同一人」。
- 查询时 `cross_search("王守仁")` 返回所有 member、各自出处、置信度、关系网。
- **宁可漏不可错**：同人的没并上可以补，两人的错并成一个会静默污染全库且难回滚。

> 这条原则适用于**所有可跨书对齐的对象**：实体（ENT）、地点（GEO）、职官（APPT 的人-职-机构三元组）、事件（MING 纪事），不只人名。

---

## 2. E / L / T 三段职责

### E — Extract：每书一个 adapter，纯抽取不判断

输入：该书 `_kg_join.json` + 各层产物 + `ent_keys.json` + `_item_registry` 指纹。

六种 join 形态（已由体检确认）由 adapter 各归一为四张中间表：

| 中间表 | 内容 | 来源 |
|---|---|---|
| `items` | `item_id, volume, title, layer_count` | join 的条目行 |
| `layer_records` | 层记录原样 + 归一后的 `layer_key` | 各层 json |
| `entities` | `local_id, normalized, type, count, first_source` | ent_keys |
| `aliases` | `alias → local_id` | ent_keys.alias_index |

**不改任何源数据**，只抽取。撞号在此阶段不处理（留给 L 的复合主键）。

### L — Load：直载进库，幂等隔离

- 所有表主键带 `(book_id, local_id)` 复合；`uid = book_id:local_id`。
- 幂等：`BEGIN; DELETE WHERE book_id=?; 批量 INSERT; COMMIT`——重跑结果一致（守「一切可重跑」）。
- `items` 只存指针（`book_id + item_id + fingerprint`），**不抄正文**（守「原文只在指纹库」铁律）。
- 此阶段书与书完全隔离，**撞号自然消解**（2847 个撞号无需改写 ID）。

### T — Transform：去歧义合并，核心

```
T0  层 key 归一    events→evt / ents→ent ... 映射表；未登记层报 WARN（反制 #27 静默吸收）
T1  名字→ID 解析  REL/APPT 里的「名字」经 ent_keys 解析成本书 ENT id，建 ENT-ENT 关系图
T2  候选生成      精确(normalized+type 一致) + 别名(alias_index 交叉)
T3  关系消歧      集体消歧（并查集 + 约束 + 迭代）→ entity_links
```

---

## 3. 关键发现：关系层存的是「名字」，不是 ID

实测（决定设计走向）：

```jsonc
// REL 层
{"item_id":"04-001", "person_a":"李廷珪", "person_b":"李超", "relation_type":"父子", ...}
// APPT 层
{"item_id":"07-001", "person":"海瑞", "office":"南右都御史", "institution":"南京都察院", ...}
```

两者都不直接引用 `ENT-xxx`。含义：**「用关系识别实体」不能直接用**——
必须先经 `ent_keys.normalized / alias_index` 把名字解析回本书 ENT id，才能建 ENT-ENT 关系图。
**T1 是关系消歧的前提，也是最容易漏的一步。**

解析失败处理：若 `person_a/b` 在 ent_keys 查不到（如「李超」未单独立实体），该边**悬空入库**为 pending 关系，不强行丢弃也不强行造实体。

---

## 3.1 名字解析的细化（2026-10-11 落地）：配置驱动 + 两级接入 + 置信度

用户细化要求：**「不管是什么称呼（别名/笔名/尊称/蔑称/带官称/带地名称呼/谥号/追谥…只要能识别到身份都要能查到，查询时给个置信度就好）」**，且**不要写死变体类型**。落地为三条铁律：

### ① 配置驱动归一化（`tools/kb-federation/name_rules.json`）

代码**不枚举**任何具体变体类型，只泛化处理一份配置：
- `decoration_groups`：装饰词按**出现位置**分三组——`honorific_suffix`（公/翁/先生/山人/居士…）、
  `title_prefix`（太师/尚书/巡抚…）、`place_suffix`、`posthumous_marker`（谥/追谥/赠/追赠）。
- `normalize(raw)` 依次：删谥号标记 → 剥官称前缀 → 剥尊称/地名后缀（单字尊称仅当剩余≥2字才删，防误伤二字名）。
- **新增一种称呼/变体，只往配置加 token，不改代码**——这是「不要写死」的落地方式。

实测（真实数据）：`学士宋文宪公濓`→`宋文宪公濓`（内嵌公不误剥）、`王忠毅公`→`王忠毅`、
`太师张居正`→`张居正`、`老子`→`老子`（单字「子」不误剥）。

### ② 两级接入（只有部分书有 `ent_keys.json`）

实测：仅 `sdr` 有正式 `ent_keys.json`，`wzz` 在 backup，`xyf` 在未提交目录，`kzz/xgf/qb` 没有。
故名字来源**两级**：
- **标准接入**：若某书在 `ent_keys_paths` 登记了标准 `ent_keys.json` 且结构标准，读其显式 alias 列表（最高价值）。
- **特殊接入**：否则从 `records` 的 ent 负载抽取 `normalized`+`text` 作为 surface（**所有书都有**，兜底）。

两路都归一到同一套 `surface → uid` 索引。实测各书的 ent 记录**没有结构化「字/号/别名」字段**——
`normalized` 是各书自己的规范名（已剥离装饰，如「学士宋文宪公濓」在 xyf 里 normalized 已是「宋濂」），
`surfaces`（xgf/sdr）实为**出处 item_id 列表**、非别名。所以「一个字尽量多能查到」主要靠
**把每个 ent 的所有出现形式都索引成 surface + 查询时按配置归一**，而非依赖结构化别名字段。

### ③ 置信度模型（查询端呈现，不隐藏不确定性）

匹配方法 → 基准置信度在 `match_confidence`：
`exact_normalized=0.98 / surface_alias=0.90 / normalized_stripped=0.65 / relation_propagated=0.55`。

**同名异人 / 泛称角色封顶**（`type_confidence_cap`）：
- `work/place/era/institution` 等实体跨书同名基本可断定同一 → 维持高置信；
- `person` 封顶 0.85（同名异人风险）、`official/org/quantity/unknown` 封顶 0.60（泛称角色，合并易失真）。

实测验证：查「王忠毅公」命中 sdr 三个变体形态——`王骥（谥忠毅）`、
`王忠毅公（王骥？谥忠毅，待考）`、`王骥（谥忠毅？即王靖远）`，全部 surface_alias=0.9。
这正是「带尊称/谥号的写法也能查到同一人」的目标形态。

---

## 4. 如何利用现有数据（逐条对应）

| 现有文件 / 层 | 在 ELT 中的用途 |
|---|---|
| `ent_keys.json`（`normalized`/`type`/`alias_index`） | **最值钱**：T1 名字解析 + T2 候选生成 |
| `REL` 层（`person_a`/`person_b`/`relation_type`） | T1 解析成 ENT-ENT 边（父子/师生/同僚…） |
| `APPT` 层（`person`/`office`/`institution`） | T1 解析成人-职-机构三类 ENT 的任职边 |
| `_item_registry.json`（指纹） | L 阶段 items 指针，原文回查 |
| 蘧编 `CHR` / 各书 `MING` | 时间一致性，T3 可选约束（同时代才可能是同一人） |
| `kb_mcp` 撞号体检 | E 阶段前置断言：撞号必须被复合主键消解，否则报错 |

---

## 5. 集体实体消歧算法（T3）——「用关系识别同实体」的落地

**核心思想**：同人不仅在名字上一致，其**关系网络**也该一致。
`A1(书1) ≡ A2(书2)` 的置信，可由「A1 的儿子 B1 与 A2 的儿子 B2 也已对齐」来增强（共指传递）。

**输入**：
- 候选对 `P`：T2 产出的 `(Ea, Eb)`（跨书、同 type）
- 关系图 `G`：节点 = ENT（带 book_id），边 = REL/APPT 派生关系（带 relation_type）
- 类型向量：每个 ENT 的 `type`

**算法（等价闭包 + 约束剪枝）**：

```
1. 初始化
   精确匹配对  conf = 1.0   入并查集
   别名匹配对  conf = 0.9   入并查集

2. 迭代 N 轮（相似度传播）：
   for 每条关系边 (u, v, rtype):
     if u≡u' 且 v≡v' 且边 (u',v',rtype) 存在:  强化两对候选（conf 取路径 min）
     if u≡u' 已知 且 (v, v') 有候选 且 rtype 一致:  提升 (v,v') 置信
     if v≡v' 已知 且 (u, u') 有候选 且 rtype 一致:  提升 (u,u') 置信

3. 约束剪枝（避免错并）：
   - 类型一致：person 不可 ≡ institution（跨 type 一律不 union）
   - 关系互斥：父子边跨书必须指向同一 canonical 父亲，否则解除该 union
   - 一对一：并查集天然保证每个 ENT 至多一个代表

4. 稳定后落库
   entity_links(canonical_uid, member_uid, method, confidence, status)
   method ∈ {exact, alias, relation}; status ∈ {auto, conflict, pending}
```

**并查集表达等价，约束违背则解除对应 union**——这是「去歧义」的硬闸门。

---

## 6. 输出与查询

| 产物 | 内容 |
|---|---|
| `canonical` / `members` | 跨书同人/同地/同书链接：method（exact/alias/stripped/relation）+ confidence + status（auto/conflict） |
| `candidate_links` | T2/T3 候选对（带方法与置信度），低于 floor 的不并入 canonical，留待人工 |
| `pending_refs` | 名字在 ent 索引查不到、边悬空的原始名字（供人工补实体） |
| `cross_search(name)` | `query.py` 的 `FederationQuery.cross_search`：返回 canonical 下所有 member、各自出处、匹配方法与置信度 |

## 7. 落地状态（2026-10-11）

F0-a（撞号体检）/ F1（单书试点）/ F2（六书全量）/ **F3（T0–T3 去歧义）均已落地并实证**：

- F3 实证（`python federation.py transform`）：nodes=18152、edges=1498（悬空 pending=666）、
  candidates=6589、canonicals=812、members=3746（auto 3478 / conflict 268）。重跑幂等（两次结果一致）。
- 名字解析（§3.1）已按「配置驱动 + 两级接入 + 置信度」落地，代码见
  `name_resolver.py` / `transform.py` / `query.py`，配置见 `name_rules.json`。
- CLI：`transform` / `search <名>` / `resolve <名>`。

> 下一步 F4：把 `cross_search` 包成查询接口/MCP，`conflict` 成员供人工校验闭环（锁定/解除误并）。

---

> 不先做 T 的原因：L 一旦有 bug（撞号没消解、幂等失效），T 的所有对账都是空中楼阁。
> 先让「六本书安全地躺在同一个库里互不踩踏」，再谈「把它们连起来」。

---

## 8. 与已落地工具的关系

- 不重复实现枚举/层解析：从 `Skills/00-…/references/` 读（同契约线做法）。
- `kb_mcp` 撞号体检 → 可作为 E 的前置断言，复用其 adapters 的扫描逻辑。
- 总库只读六本书，**绝不回写**；实体的「合并」只产生 links，不改动 `_layers/`。
