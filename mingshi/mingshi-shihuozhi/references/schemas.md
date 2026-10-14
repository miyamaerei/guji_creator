# 《明史·食货志》知识工程 — Schema 规范

> 本文件是实例 `mingshi-shihuozhi-knowledge` 的**各层 schema 唯一说明**。
> 枚举取值以 `scripts/_kg_enums.py` 为唯一来源；本文件是**人读快照**，两者不一致时以代码为准。
> 版本：v1.0（2026-10-16 首次实例化，shz 型 8 层）

---

## 0. 通用约定

### 0.1 四处同源（工厂 B 族纪律）

| 位置 | 值 |
|---|---|
| 物理目录 | `_layers/<dir>/` |
| 文件名前缀 | `<dir>_<vol>.json` |
| 索引槽位名 | `LAYER_SPECS` 第二元 |
| 记录键名 | `"records"` |

**八层一律复数**：`ents` / `rules` / `regs` / `procs` / `structs` / `appts` / `tmes` / `opns`。

### 0.2 层文件外形

```json
{ "volume": "01", "records": [ ... ] }
```

### 0.3 ID 分配

- **源数据只写 `slot`**（条目内语义顺序），**绝不手写 ID**。
- 打包器按**记录全局序号** `enumerate(records, 1)` 分配：`<PREFIX><卷段位><序号>`，段容量 500。
- 子节点 ID 由父 ID 派生：`<父ID>#<序号>`，**保留记录里已有的 id**（不覆盖）。
- `ENT-` 是**实体主键**，同一实体多次出现共用同一 ID —— 唯一性校验**须豁免 ENT 前缀**。

| 前缀 | 层 |
|---|---|
| `ENT-` | L1 实体 |
| `RULE-` | L2 规则 |
| `REG-` | REG 制度 |
| `PROC-` | L3 流程 |
| `QUAN-` `INST-` `EVO-` `FISC-` | L4 食货四维 |
| `APPT-` | C1 任职 |
| `TME-` | C14 时间沿革 |
| `OPN-` | C9 论说 |
| `LED-` | C16 总账树节点 |
| `TRANS-` | 运送链 |
| `HK-` `LAND-` | 户籍 / 田制 |
| `BOOK-` | 全书性专表（虚拟卷 00） |

### 0.4 时间字段

```python
"era": {"text": "洪武二十六年", "dynasty": "明", "reign": "洪武", "year": 26}
# 排序键：time_key("洪武", 26) == (1, 26)
# REIGN_ORDER：吴0 洪武1 建文2 永乐3 洪熙4 宣德5 正统6 景泰7 天顺8
#              成化9 弘治10 正德11 嘉靖12 隆庆13 万历14 泰昌15 天启16 崇祯17 未明99
```

**裸写纪年**（原文只写 `十三年`）须回填年号（`洪武十三年`）——承职官志实例的经验。

---

## 1. L0 底座

| 产物 | 说明 |
|---|---|
| `_item_registry.json` | 条目注册表：`item_id` / `volume` / `original`（原文全段）/ `norm`（归一）/ `title` / `line_no` |
| `_data/base/fingerprint.json` | 指纹库（317 条规模） |
| `_extract/<vol>.txt` | 逐卷抽取原文 |
| `chapters/<vol>_食货N.md` | 可读章节 |

**切分口径**：`◆` 卷标 → `◎` 卷内标题 → 子目行（`○` 标记 **或** 「被正文包围的无句号短行」）→ 正文段。
**卷五十三无 ○**，子目 `户口田制(屯田庄田)`（L5，10 字）走短行判据。

**本书卷段**：五十三 食货一（L1–28，25 段）/ 五十四 食货二（L30–71，39 段）/ 五十五 食货三（L73–106，31 段）/ 五十六 食货四（L108–180，70 段）/ 五十七 食货五（L182–231，47 段）/ 五十八 食货六（L233–287，53 段）。

---

## 2. L1 实体层

```python
{
  "slot": 1, "item_id": "01-003",
  "text": "黄册",                    # 原文词形（必须逐字命中原文）
  "norm": "黄册",                    # 归一形
  "type": "doc",                     # ENTITY_TYPES 20 值
  "ent_id": "ENT-0001",              # 打包器分配
  "evidence": "太祖籍天下户口，置户帖、户籍",
  "confidence": 0.95
}
```

**`ENTITY_TYPES` 20 值**（继承基准库，不裁剪）：
`person` `official` `institution` `place` `era` `work` `object` `animal` `plant` `food` `doc` `system` `behavior` `punishment` `time` `quantity` `posthumous` `star` `event` `unknown`

**本书高频类型**：`doc`（黄册/户帖/鱼鳞图册/盐引/由单/勘合）、`system`（一条鞭法/开中/兑运/里甲）、`quantity`（数额）、`institution`（户部/太仓/茶马司）、`place`（府州县/边镇/运道节点）。

**词形纪律**（承职官志 GAP 修法）：
1. `text` 必须**逐字命中原文**，不得写规范形（原文 `锦衣` 就不能写 `锦衣卫`）。
2. 并列枚举取**并列原字串**（原文 `武德、龙骧…十七卫` → 实体取 `武德`，不取 `武德卫`）。
3. 纪年**去朝代前缀**（卷首已领 `洪武三年`，后续原文只写 `四年` → `text="四年"`）。

---

## 3. L2 规则层

```python
{
  "slot": 1, "item_id": "02-014",
  "rule_type": "义务型",             # RULE_TYPES 7 值
  "modal": "义务",                  # RULE_MODALS 7 值
  "subject": {"text": "有司", "ent_ids": ["ENT-0112"]},
  "action": "徵收税粮",
  "condition": "凡秋粮…",
  "object": {"text": "税粮", "ent_ids": []},
  "deadline": "",
  "penalty": "",
  "evidence": "凡有司徵收，…",
  "confidence": 0.9
}
```

**`RULE_TYPES` 7 值**：禁止型 / 义务型 / 允许型 / 程序型 / 时限型 / 处罚型 / 优先级。

**抽取纪律**（工厂坑 #7 #34）：
- **只收规范性语句**；制度说明句、记账句、时序叙事句**不抽**。
- 本书规则密度信号：`凡` 86 句 / `不得` 32 / `不许` 3 / `毋得` 3 / `禁` 76 / `违者` 2 / `罪之` 8。

---

## 4. REG 制度层（本书骨架）

### 4.1 完整 schema（13 属性 + 6 辅助字段）

```python
{
  "slot": 1,
  "item_id": "02-014",
  "reg_id": "REG-014",

  # ① 制度名称
  "name": "一条鞭法",

  # ② 所属类别  → INST_TYPES 15 值（↻ 可追加）
  "category": "赋役",

  # ③ 创设时间沿革（原文引语 + 关联时间点）
  "evolution": "嘉靖间，数行数止，至万历九年乃尽行之。",
  "tme_ids": ["TME-021", "TME-022"],

  # ④ 主管部门 [list] —— 联动《明史·职官志》知识库
  "agencies": [
    {"text": "户部", "ent_ids": ["ENT-0203"],
     "cross_kb": "mingshi-zhiguanzhi", "cross_id": "ORG-505"}
  ],

  # ⑤ 征收对象 / 适用人群 [list]
  "targets": ["民户", "丁", "田土"],

  # ⑥ 征收物 [list] —— 物品/形态/数量/单位 四元组
  "levied_items": [
    {"item": "银", "form": "白银", "amount": 1, "unit": "两",
     "basis": "计亩徵银", "item_ent_ids": []}
  ],

  # ⑦ 法定税率核定 [list]
  "rates": [
    {"rate_text": "计亩徵银", "basis": "亩", "amount": None, "unit": "两",
     "note": "量地计丁，丁粮毕输于官"}
  ],

  # ⑧ 覆盖范围
  "scope": "全国",
  "regions": ["浙江", "江西", "南直隶"],

  # ⑨ 文书载体 [list] → REG_DOCS 12 值
  "documents": ["由单", "易知由单"],

  # ⑩ 执行者 [list] → REG_AGENT_KINDS 6 值
  "agents": [
    {"kind": "品官", "text": "户部尚书"},
    {"kind": "役", "text": "里长"}
  ],

  # ⑪ 目的 [list] → REG_PURPOSES 8 值
  "purposes": ["财政", "户籍管控"],

  # ⑫ 弊病与改革尝试 [list] ← 接 OPN 层
  "abuses": [
    {"abuse": "逋欠之多，县各数十万", "reform": "行一条鞭法",
     "era": {"reign": "万历", "year": 9}, "opn_ids": ["OPN-006"]}
  ],

  # ⑬ 史料来源
  "source": "明史食货志",
  "source_item_id": "02-014",
  "evidence": "一条鞭法者，总括一州县之赋役，量地计丁，丁粮毕输于官。",

  # ---- 辅助字段 ----
  "status": "遵行",                  # REG_STATUS 8 值
  "quota_type": "岁额",              # REG_QUOTA_TYPES 6 值
  "ext_折耗": "…",                   # ext_ 前缀 = 自由扩展字段
  "confidence": 0.92
}
```

### 4.2 枚举清单

| 字段 | 枚举 | 值 |
|---|---|---|
| `category` | `INST_TYPES` | 户口 / 田制 / 赋役 / 漕运 / 仓库 / 盐法 / 茶法 / 钱钞 / 坑冶 / 商税 / 采造 / 俸饷 / 会计 / 赈济 / 其他 |
| `status` | `REG_STATUS` | 初置 / 定制 / 遵行 / 弊坏 / 改革 / 复设 / 废罢 / 未明 |
| `quota_type` | `REG_QUOTA_TYPES` | 岁额 / 正额 / 额外 / 加派 / 无定额 / 未明 |
| `scope` | `REG_SCOPES` | 全国 / 直隶 / 部分布政司 / 边镇 / 一府州县 / 未明 |
| `levied_items[].form` | `REG_LEVIED_FORMS` | 实物 / 白银 / 钞 / 钱 / 混合 / 未明 |
| `documents[]` | `REG_DOCS` | 黄册 / 鱼鳞图册 / 户帖 / 盐引 / 由单 / 勘合 / 粮长勘合 / 帖文 / 榜文 / 图格 / 其他 / 未明 |
| `agents[].kind` | `REG_AGENT_KINDS` | 品官 / 役 / 卫所军 / 宗室勋戚 / 商人 / 未明 |
| `purposes[]` | `REG_PURPOSES` | 财政 / 军事 / 户籍管控 / 保安 / 备荒 / 礼仪 / 其他 / 未明 |
| `source` | `REG_SOURCES` | 明史食货志 / 明会典 / 实录 / 方志 / 奏议 / 未明 |

### 4.3 动态追加字段规则

1. **枚举类字段**新增值 → 改 `_kg_enums.py` + `VERSION` +1 + 同步本文件 §4.2 表；
   若为跨书通用值 → 另走工厂 `references/enum-induction-guide.md`（registerVersion+1）回写基准库。
2. **自由字段**用 `ext_<key>` 前缀（如 `ext_折耗` / `ext_运费` / `ext_损耗率`）；
   打包器**不校验**其值，但键名须在本文件登记含义。
3. 追加时在 `_kg_enums.py` 维护 `REG_EXT_KEYS: {键名: 说明}` 供漂移检查。

### 4.4 与 L4-INST 的分工

| | REG 制度层 | L4-INST |
|---|---|---|
| 粒度 | 一条制度一整条记录（13 属性） | structs 记录上的类型标签 |
| 用途 | 查「这制度是什么、谁执行、征收什么」 | 查「哪些条属于盐法」 |
| 关系 | **单点真相源** | `inst.reg_id` 反指 REG，**REG 不反记 INST** |

---

## 5. L3 流程层

```python
{
  "slot": 1, "item_id": "03-008",
  "proc_id": "PROC-008",
  "name": "漕粮递运流程",
  "scope": "漕运",
  "steps": [
    {"seq": 1, "text": "江西、湖广、浙江民运粮至淮安仓",
     "agent": {"text": "民", "agent_ent_ids": []},
     "condition": "", "next": [2]},
    {"seq": 2, "text": "自淮至徐以浙、直军輓运",
     "agent": {"text": "官军", "agent_ent_ids": []},
     "condition": "", "next": [3]}
  ],
  "evidence": "自淮至徐以浙、直军，自徐至德以京卫军，自德至通以山东、河南军。以次递运，岁凡四次。",
  "confidence": 0.9
}
```

**本书流程清单（候选）**：漕粮递运流程 / 交兑流程 / 过淮程限流程 / 盐开中流程 / 茶马易换流程 / 黄册攒造流程 / 里甲催征流程 / 税课司征税流程 / 一条鞭法徵收流程 / 赈济流程。

---

## 6. L4 食货四维

> **分派顺序定死**（工厂坑 #38）：`children` → `change_type` → `line_type` → `posts` → `quan` → `led`。
> 顺序写错会产生成批假 ERR。**假 ERR 指纹**：值全为 `None` 且集中在新记录 → 先怀疑分派。

### 6.1 QUAN 数额定额

```python
{
  "quan": {
    "amount": 132000,          # 由 cn2int 解析（含约数后缀处理）
    "unit": "石",              # QUAN_UNITS
    "form": "本色",            # QUAN_FORMS 6 值
    "raw": "屯粮十三万二千馀石",  # 原文原串（校验用）
    "origin": "屯田",          # QUAN_ORIGINS 20 值
    "side": "主兵",            # QUAN_SIDES 3 值
    "confidence": 0.95
  }
}
```

**`QUAN_FORMS` 6**：本色 / 折色 / 银 / 钞 / 钱 / 未明
**`QUAN_UNITS`**（单位→量纲）：容量（石斗升合勺）· 重量（两斤钱分厘）· 货币（贯文锭）· 织物（匹疋端）· 土地（顷亩）· 计数（引束员名人）
**`QUAN_ORIGINS` 20**：屯田 / 民运 / 盐引 / 盐课 / 京运 / 漕粮 / 地亩 / 牛具 / 盐钞 / 荒田 / 工食 / 抚赏 / 犒军 / 犒赏 / 税课 / 加派 / 存留 / 起运 / 其他 / 未明
**`QUAN_SIDES` 3**：主兵 / 客兵 / 未分

**解析纪律**（坑 #48 #64）：
- 约数标记 `馀 / 有奇` **全串剔除**（可夹在数字中间：`四百三十馀万束` = 4,300,000）。
- 量纲前缀：`一千四十四` = 1044。
- 返回 `None` 必须当**错误**处理，不得静默当 0。

### 6.2 INST 制度类型

```python
"inst": {"type": "盐法", "reg_id": "REG-007"}
```

### 6.3 EVO 沿革阶段

```python
"evolution": {"stage": "弊坏", "tme_ids": ["TME-021"], "evidence": "…"}
```

**`EVO_STAGES` 9**：初置 / 定制定型 / 增改 / 裁革 / 复设 / 变法 / 弊坏 / 复原 / 未明

**触发词**：初置（始置/初设）· 定制定型（**遂为定制**/**著为令**/**著为定规**/为常/为例）· 增改（增置/加增/添设）· 裁革（裁并/革罢/寻罢/寻废）· 复设（复置/仍旧）· 变法（改革/更定/立法）· 弊坏（法坏/弊滋/积弊/不可止）· 复原（悉复旧制/复如旧）

### 6.4 FISC 财政流转

```python
"fisc": {"stage": "解京", "from": "州县", "to": "太仓"}
```

**`FISC_STAGES` 12**：徵收 / 起运 / 存留 / 解京 / 内库 / 边镇 / 支放 / 加派 / 蠲免 / 折纳 / 转运 / 其他

**原文依据**：`而折色、本色递年轮收，本色归内库，折色归太仓。`；`旧制以七分经费而存积三分备兵、歉。`

### 6.5 总账树 C16（LEDGER）与运送链（TRANS）

见 `SKILL.md` §6 / §7。结构锚点：食货六 L272–L285。
**13 镇**：宣府·大同·山西·延绥·宁夏·甘肃·固原·辽东·蓟州·密云·昌平·易州（L282 为过渡叙述；甘肃/固原无 `side` 分列 → `未分`）。

```python
{
  "led": {
    "ledger_id": "LED-003",
    "levels": ["九边钱粮总账", "宣府", "主兵", "屯粮", "…"],  # LEDGER_LEVELS 5 层
    "town": "宣府", "side": "主兵", "origin": "屯田",
    "quan_id": "QUAN-012", "parent": "LED-002", "children": []
  },
  "trans": {
    "trans_id": "TRANS-001", "mode": "递运",
    "steps": ["起运", "交兑", "过淮", "至京", "入仓"],
    "from": "淮安", "to": "徐州", "agent": "浙、直军", "endpoints": ["淮安", "徐州", "德州", "通州"]
  }
}
```

**`LEDGER_LEVELS` 5**：总账 / 镇 / 兵种 / 收入类别 / 明细
**`TRANS_MODES` 13** / **`TRANS_STEPS` 12**：见 `_kg_enums.py`

### 6.6 户籍 HUKOU 与田制 LAND

```python
"hk":   {"hk_id": "HK-001", "category": "户籍制度", "hk_class": "民户",
         "era": {...}, "content": "…", "evidence": "凡户三等：曰民，曰军，曰匠。"}
"land": {"land_id": "LAND-001", "land_type": "官田", "aspect": "科则",
         "rate": {"amount": 5, "unit": "升", "note": "五升三合五勺"},
         "evidence": "凡官田亩税五升三合五勺，民田减二升…"}
```

**`HK_CATEGORIES` 12** / **`HK_CLASSES` 5** / **`LAND_TYPES` 14** / **`LAND_ASPECTS` 9**：见 `_kg_enums.py`。

---

## 7. C1 任职层

```python
{
  "slot": 1, "item_id": "04-012",
  "appt_id": "APPT-012",
  "person": {"text": "杨一清", "person_ent_ids": ["ENT-0451"]},
  "office": {"text": "督理马政都御史", "official_ent_ids": []},
  "institution": {"text": "茶马司", "ent_ids": ["ENT-0302"]},
  "when": {"text": "正德", "dynasty": "明", "reign": "正德", "year": None},
  "status": "现任",                  # APPT_STATUS 12 值
  "evidence": "以督理马政都御史杨一清兼理之。",
  "confidence": 0.9
}
```

**`APPT_STATUS` 12**：世袭 / 举荐 / 兼领 / 升迁 / 暂代 / 未明 / 现任 / 罢黜 / 致仕 / 贬谪 / 起复 / 追赠

---

## 8. C14 时间沿革层

```python
{
  "slot": 1, "item_id": "02-014",
  "tme_id": "TME-021",
  "era": {"text": "万历九年", "dynasty": "明", "reign": "万历", "year": 9},
  "target": {"text": "一条鞭法", "ent_ids": ["ENT-0088"]},
  "action": "尽行",
  "content": "至万历九年乃尽行之。",
  "category": "职掌变更",             # TME_CATEGORIES 13 值
  "related_evo": "EVO-014",           # ↔ 双向引用（打包器校验，单向报 ERR）
  "related_ledger": "",
  "ref_item": "02-014",
  "confidence": 0.95
}
```

**`TME_CATEGORIES` 13**：初置 / 改置 / 增员 / 复设 / 废置 / 改称 / 裁并 / 移驻 / 职掌变更 / 升秩降秩 / **定额变更** / **法弊** / 未明
（后两者为本书新增：食货志的制度沿革不只是机构变动，还有**定额调整**与**法弊**）

**派生视图**：`_views/timeline/<制度或机构>.json`（打包器生成，按 `time_key` 升序）。

---

## 9. C9 论说层（OPN）

```python
{
  "slot": 1, "item_id": "04-021",
  "opn_id": "OPN-021",
  "type": "奏议",                    # OPN_TYPES 6 值
  "stance": "批评",                  # OPN_STANCES 5 值：褒扬/批评/辨析/陈述/存疑
  "speaker": {"text": "杨一清", "person_ent_ids": ["ENT-0451"]},
  "target": {"text": "茶法", "ent_ids": ["ENT-0088"]},
  "quote": "茶法、马政、边防於是俱坏矣。",     # 引语原文
  "length": 14,                      # 字数（校验 ≥ OPN_MIN_LEN=40）
  "markers": ["坏"],                 # 命中的 OPN_CLAIM_MARKERS
  "era": {"reign": "正德", "year": None},
  "evidence": "言：…",
  "confidence": 0.9
}
```

**准入判据**（写死供校验器）：
```
len(quote) >= OPN_MIN_LEN(40)  AND  any(m in quote for m in OPN_CLAIM_MARKERS)
```
`OPN_CLAIM_MARKERS` 18 词：请 / 宜 / 乞 / 恐 / 弊 / 坏 / 苦 / 忧 / 患 / 不可 / 非 / 当 / 议 / 驳 / 论 / 言其 / 疏论 / 极言

**反例（不抽）**：无主张的记账句、纯制度说明句（纪律同工厂坑 #34）。

---

## 10. 跨层索引

`_kg_join.json`：319（条目）条记录，逐条登记各层挂载的 ID。

```json
{
  "item_id": "02-014",
  "volume": "02",
  "layers": {
    "ents": ["ENT-0088", "ENT-0203"],
    "rules": ["RULE-014"],
    "regs": ["REG-014"],
    "procs": [],
    "structs": ["QUAN-021", "INST-007", "EVO-014", "FISC-009"],
    "appts": [],
    "tmes": ["TME-021"],
    "opns": ["OPN-006"]
  },
  "layer_count": 5
}
```

**验收**：各层条数 vs 索引层计数**须对账**（工厂 A 族 #28/#29：单复数不一致会静默空回填且 ERR=0）。

---

## 11. 校验与交付

### 11.1 ERR / GAP 二分（不可混读）

| 类 | 含义 | 处理 |
|---|---|---|
| **ERR** | 值**非法**（枚举越界 / ID 撞号 / 层级非法） | 必须修 |
| **GAP** | 引用**悬空**（`ent_ids` 命不中实体 / 词形不命中原文） | 必须修 |

### 11.2 交付必报三表（工厂 A 族纪律）

1. **ERR/GAP 表** —— 层内自洽。
2. **字段填充率表** —— 每层每扩展字段「已填 / 总数」；**填充率 = 0 直接判失败**。
   排查顺序固定：**先查是否被调用 → 再查解析覆盖面 → 最后才接受「原文确实没有」**。
3. **目标查询问句逐问验收表** —— 对 `SKILL.md` §0.3 的 12 问逐条实测作答。

### 11.3 交付形态

- **知识资产**：`_layers/`（8 层 JSON）+ `_views/`（查询视图）+ `_kg_join.json`
- **报告**：`《明史·食货志》使用报告.md` + `《明史·食货志》项目总结报告.md`
- **口径说明**：Q9 县级税额 / Q10 马政总账为「原文没有」，须在报告中明写

---

## 12. 枚举快照（`_kg_enums.py` VERSION = "1.3"）

| 枚举 | 条数 | 来源 |
|---|---|---|
| `ENTITY_TYPES` | 20 | 继承 |
| `RULE_TYPES` / `RULE_MODALS` | 7 / 7 | 继承 |
| `REIGN_ORDER` | 18+兜底 | 继承 |
| `APPT_STATUS` | 12 | 继承 |
| `OPN_STANCES` | 5 | 继承 |
| `QUAN_FORMS` / `QUAN_UNITS` / `QUAN_ORIGINS` / `QUAN_SIDES` | 6 / 34 / 24 / 3 | **本书定制** |
| `INST_TYPES` | 15 | **本书定制** |
| `EVO_STAGES` | 9 | **本书定制** |
| `FISC_STAGES` | 12 | **本书定制** |
| `REG_STATUS` / `REG_QUOTA_TYPES` / `REG_SCOPES` / `REG_LEVIED_FORMS` | 8 / 6 / 6 / 6 | **本书定制** |
| `REG_DOCS` / `REG_AGENT_KINDS` / `REG_PURPOSES` / `REG_SOURCES` | 19 / 6 / 8 / 6 | **本书定制** |
| `TME_CATEGORIES` | 14 | 继承 11 + 本书 3（定额变更 / 法弊 / 废置） |
| `OPN_TYPES` / `OPN_CLAIM_MARKERS` | 6 / 18 | **本书定制** |
| `LEDGER_LEVELS` / `TRANS_MODES` / `TRANS_STEPS` | 5 / 13 / 14 | **本书定制** |
| `HK_CATEGORIES` / `HK_CLASSES` / `LAND_TYPES` / `LAND_ASPECTS` | 12 / 5 / 14 / 9 | **本书定制** |

---

## 13. 变更历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-10-16 | 首次实例化：shz 型 8 层 + 食货四维 + REG 13 属性 + C16 总账树 + 运送链 + 户籍/田制 |
| v1.3 | 2026-10-13 | 卷五/六枚举扩充：REG_DOCS 增关防/店历/红单/金叶勘合/大明宝钞，TRANS_STEPS 增支放/解京，QUAN_UNITS 计数类增件/倍 |
