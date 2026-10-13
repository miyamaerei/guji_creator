# 《明史·选举志》Schema 与 ID 规范（xjz 完整型，11 层 + L5）

> 写源数据、打包器、验证脚本时对照本文。所有 schema 在实例 SKILL.md §6–§14 已按书定制后锁死，执行期不再改动。
> **原文不手抄**：AI 源数据只写条号与解读字段；打包器从 `_item_registry.json` 注入 `original`/`norm`。

## 1. 全局约定

- **条粒度主键**：`item_id = NN-NNN`（卷 - 序，如 `02-014`），全书唯一，是所有层的共同锚点。
- **ID 命名空间**（每层唯一前缀，禁止跨层占用，由 `scripts/_common.py` 的 `LAYER_SPECS` 单点声明）：

| 层 | 目录 | 前缀 | 示例 |
|---|---|---|---|
| L1 实体 | `ents/` | `ENT-` | ENT-0203 |
| L2 规则 | `rules/` | `RULE-` | RULE-014 |
| REG 制度 | `regs/` | `REG-` | REG-014 |
| L3 流程 | `procs/` | `PROC-` | PROC-014 |
| L4 四维 | `structs/` | `EVO-`/`QUAN-`/`INST-` | EVO-014 / QUAN-008 / INST-005 |
| C14 时间沿革 | `tmes/` | `TME-` | TME-021 |
| C9 论说 | `opns/` | `OPN-` | OPN-021 |
| NAM 名录 | `nams/` | `NAM-` | NAM-014 |
| FRD 防弊 | `frds/` | `FRD-` | FRD-008 |
| OBJ 名物 | `objs/` | `OBJ-` | OBJ-031 |
| L5 事件 | `events/` | `EVT-` | EVT-012 |

- **落盘文件**：每层 `_layers/<dir>/<vol>_<dir>.json`（如 `02_ents.json`），顶层键 `records`（列表）。
- **ENUM 治理**：启用层枚举继承基准库 `references/enum-library.md` 规范值快照 + 本书归纳增量；新增须 `registerVersion+1` 回溯存量；校验用「收集-报告-暂存」不中断。

---

## 2. L1 实体层 (`ents/` · `ENT-`)

```json
{
  "volume": "02",
  "records": [
    {"id": "ENT-0203", "item_id": "02-014", "text": "国子监",
     "type": "institution", "start": 12, "end": 15,
     "normalized": "国子监", "confidence": 0.95, "source": "原文片段"}
  ]
}
```

- `type` 封闭枚举（继承基准库，本书归纳增量）：`person` / `official` / `institution` / `school` / `place` / `era` / `work` / `object` / `quantity` / `system` / `unknown`。
- `start/end`：原文字符偏移，用于定位与去重。
- 归一汇总 `normalized_inventory` + 主键表 `entities[]` + `alias_index`（词形→ent_id）。

---

## 3. L2 规则层 (`rules/` · `RULE-`)

```json
{
  "rule_id": "RULE-014", "item_id": "02-026",
  "type": "程序型",
  "modals": ["程序型"],
  "condition": "应试者须……",
  "subject": {"text": "生员", "subject_ent_ids": ["ENT-xxx"]},
  "action": "……", "object": "……", "purpose": "……", "punishment": "",
  "original": "（打包器注入）", "confidence": 0.9
}
```

- `type`（RULE_TYPES 7）：禁止型/义务型/允许型/程序型/时限型/处罚型/优先级。
- **触发词**（实测 22 处信号）：著为令/定为常/著为例/凡/不许/不得/毋得/禁/罪之/罚/违者。
- **抽取纪律**：只收规范性语句；制度说明/记账/时序叙事不抽。

---

## 4. REG 制度层 (`regs/` · `REG-`)

13 属性 + 选举追加 token（★本书骨架）：

```json
{
  "slot": 1, "item_id": "02-014", "reg_id": "REG-014",
  "name": "科举乡试", "category": "科目",
  "selection_type": "科目", "exam_tier": "乡试", "school_type": "",
  "evolution": "初，洪武三年诏……", "tme_ids": ["TME-021"],
  "agencies": [{"text": "礼部", "ent_ids": ["ENT-0203"],
                "cross_kb": "mingshi-zhiguanzhi", "cross_id": "ORG-xxx"}],
  "targets": ["举人", "监生", "生员"],
  "levied_items": [{"item": "解额", "form": "录取名额", "amount": 100, "unit": "人",
                    "region": "直隶", "basis": "直隶百人", "item_ent_ids": []}],
  "rates": [], "scope": "全国", "regions": ["直隶", "各省"],
  "documents": ["科录"], "agents": [{"kind": "品官", "text": "考官"}],
  "purposes": ["选官"],
  "abuses": [{"abuse": "冒籍", "reform": "严核籍贯", "era": {"reign": "万历"}, "opn_ids": []}],
  "source": "明史选举志", "source_item_id": "02-014", "evidence": "……",
  "cross_ref": [{"kb": "mingshi-shihuozhi", "ref": "QUAN-xxx", "note": "科费/廪给"}],
  "src_loc": "卷46-L26", "status": "定制", "confidence": 0.92
}
```

**选举定制枚举**：
- `selection_type`（SELECTION_TYPES）：学校 / 科目 / 贡举 / 荐举 / 铨选
  - 注：源文卷45「选举之法，大略有四：曰学校，曰科目，曰荐举，曰铨选」，学校为四法之一；贡举为岁贡/选贡/恩贡/纳贡机制（学校之亚），并存为独立 token。
- `school_type`（SCHOOL_TYPES）：国学 / 府州县学 / 社学 / 武学 / 宗学 / 其他
- `exam_tier`（EXAM_TIERS）：童试 / 科考 / 乡试 / 会试 / 殿试 / 武乡试 / 武会试 / 武殿试 / 未明
- `category`（REG_CATEGORIES_XJZ）：学校制 / 科举制 / 荐举制 / 铨选制 / 保举 / 考察考满 / 武科 / 其他
- `status`（REG_STATUS）：初置 / 定制 / 遵行 / 弊坏 / 改革 / 复设 / 废罢 / 未明

---

## 5. L3 流程层 (`procs/` · `PROC-`)

```json
{
  "proc_id": "PROC-014", "item_id": "02-026", "name": "科举三级考试",
  "steps": [
    {"step_id": "PROC-014-01", "seq": 1, "text": "乡试（行省举行，中者曰举人）",
     "agent": {"text": "考官", "agent_ent_ids": ["ENT-xxx"]},
     "examiners": [{"text": "主考", "ent_ids": ["ENT-yyy"]}],
     "sessions": ["初场四书义/经义", "二场论/判/诏诰表", "三场经史时务策"],
     "next": ["PROC-014-02"]},
    {"step_id": "PROC-014-02", "seq": 2, "text": "会试（礼部举行，中者曰贡士）",
     "examiners": [{"text": "知贡举", "ent_ids": ["ENT-zzz"]}],
     "sessions": ["同乡试三场"], "next": ["PROC-014-03"]},
    {"step_id": "PROC-014-03", "seq": 3, "text": "殿试（皇帝亲策，中者曰进士，分三甲）",
     "examiners": [{"text": "皇帝", "ent_ids": ["ENT-emp"]}],
     "sessions": ["策一场"], "next": []}
  ],
  "events": ["EVT-012"], "original": "（打包器注入）"
}
```

- **字段要点**：`examiners[]`（考官 ent_ids，原文 11 处考官名）、`sessions[]`（三场内容，卷46 详载）。
- **状态机**：科举三级为散点步骤链，建 `steps` + `next`，**不建 state_machine**（点不是线）。

---

## 6. L4 四维 (`structs/` · `EVO-`/`QUAN-`/`INST-`)

### 6.1 EVO 沿革阶段（`EVO-`）
`{"stage": "定制定型", "tme_ids": ["TME-021"], "evidence": "著为令……"}`
- EVO_STAGES：初置 / 定制定型 / 增改 / 裁革 / 复设 / 变法 / 弊坏 / 复原 / 未明

### 6.2 QUAN 数量定额（`QUAN-`）
```json
{"amount": 100, "unit": "人", "form": "解额", "region": "直隶",
 "raw": "直隶百人", "origin": "乡试", "side": "未分", "confidence": 0.95}
```
- QUAN_FORMS：解额 / 会额 / 监生额 / 教官额 / 生员额 / 未明
- **关键定制**：`region` 维度（直隶/各省）必填——缺失则"各省解额差异"问句答不了；约数标记全串剔除，量纲前缀先合并，`None` 当错误。

### 6.3 INST 制度类型（`INST-`）
`{"inst_type": "学校制", "reg_id": "REG-014"}` —— 反指 REG，不重复建定义。

---

## 7. C14 时间沿革层 (`tmes/` · `TME-`)

```json
{"slot": 1, "item_id": "01-006", "tme_id": "TME-021",
 "era": {"text": "洪武三年", "dynasty": "明", "reign": "洪武", "year": 3},
 "target": {"text": "开科取士", "ent_ids": ["ENT-xxx"]},
 "action": "初置", "content": "诏设科举", "category": "初置",
 "related_evo": "EVO-014", "ref_item": "01-006", "confidence": 0.95}
```

- TME_CATEGORIES（15）：初置/改置/增员/复设/废置/改称/裁并/移驻/职掌变更/升秩降秩/未明/定额变更/法弊 + 定制定型 + 增改
- `era.year` 存年号内年数；不做公元换算。

---

## 8. C9 论说层 (`opns/` · `OPN-`)

```json
{"slot": 1, "item_id": "03-010", "opn_id": "OPN-021",
 "type": "疏", "stance": "批评",
 "speaker": {"text": "某臣", "person_ent_ids": ["ENT-xxx"]},
 "target": {"text": "掣签", "ent_ids": ["ENT-yyy"]},
 "quote": "……（≥40 字主张句）", "length": 40, "markers": ["请"],
 "era": {"reign": "万历", "year": 3}, "evidence": "……", "confidence": 0.9}
```

- OPN_TYPES：奏议 / 疏 / 建言 / 论 / 驳议 / 引书
- OPN_CLAIM_MARKERS（本书定制）：请/宜/乞/恐/弊/坏/苦/忧/患/不可/非/当/议/驳/论/言其/疏论/极言/便
- **准入**：`len(quote)>=40 AND any(m in quote for m in OPN_CLAIM_MARKERS)`；"言"出现 61 多为子串（名言/姓名），须抽验真实主张句。

---

## 9. NAM 名录层 (`nams/` · `NAM-`)

```json
{"slot": 1, "item_id": "02-030", "nam_id": "NAM-014",
 "name": "某科一甲题名", "category": "一甲题名",
 "entries": [{"seq": 1, "person": "王某", "courtesy_name": "", "hometown": "某省某府",
              "office": "某官", "person_ent_ids": ["ENT-xxx"]}],
 "ent_ids": ["ENT-xxx"], "evidence": "……", "confidence": 0.9}
```

- NAM_TYPES：一甲题名 / 考官题名 / 进士题名 / 监生名录
- 与 L1 分工：NAM 记"四元组条目"，L1 记归一实体；同名消歧靠 alias_index + provenance（宁建勿并）。

---

## 10. FRD 防弊层 (`frds/` · `FRD-`)

```json
{"slot": 1, "item_id": "02-035", "frd_id": "FRD-008",
 "name": "冒籍", "mechanism": "假托他省籍贯应试",
 "cases": [{"event_id": "EVT-012", "note": "某科冒籍案"}],
 "related_reg": "REG-xxx", "evidence": "……", "confidence": 0.9}
```

- FRD_TYPES：冒籍 / 倩代 / 怀挟 / 关节 / 通榜 / 其他
- 与 L5 互补：FRD 记手法，L5 记始末叙事。

---

## 11. OBJ 名物层 (`objs/` · `OBJ-`)

```json
{"slot": 1, "item_id": "02-021", "obj_id": "OBJ-031",
 "name": "八股", "obj_class": "文制", "alias": ["时文", "制义"],
 "specs": {"form": "破承起讲入手起股中股后股束股"},
 "evidence": "……谓之八股。", "src_loc": "卷46", "confidence": 0.9}
```

- OBJ_CLASSES（薄层）：文制 / 场屋 / 武科器械 / 其他

---

## 12. L5 事件层 (`events/` · `EVT-`)

```json
{"slot": 1, "item_id": "02-035", "evt_id": "EVT-012",
 "type": "科场案", "who": {"text": "刘三吾等", "who_ent_ids": ["ENT-xxx"]},
 "action": "南北榜争议", "what": "考官定榜引发争议",
 "when": "洪武三十年", "where": "未明",
 "related_frd": "FRD-008", "related_reg": "REG-xxx", "confidence": 0.9}
```

- EVT_TYPES_XJZ：科场案 / 制度争议 / 变革事件 / 其他
- 五元组 who/action/what/when/where；未明显式写"未明"。

---

## 13. 跨层索引 (`_kg_join.json` / `_kg_join_flat.csv`)

```json
{"item_id": "02-014", "volume": "02", "source": "原文",
 "rules": ["RULE-012"], "procs": ["PROC-014"], "regs": ["REG-014"],
 "structs": ["QUAN-008", "EVO-014"], "tmes": ["TME-021"], "opns": ["OPN-021"],
 "nams": ["NAM-014"], "frds": ["FRD-008"], "objs": ["OBJ-031"], "events": ["EVT-012"],
 "ents": ["ENT-0203"], "layer_count": 11}
```

- 扁平 CSV 同字段平铺一行，`layer_count` 表示贯通层数。
- ID 对齐审计：实体主键唯一 / 引用槽位合法 / item_id 全回填 / target 用 ID / 枚举口径一致。

---

## 14. ID 分配规则

- 业务 ID 由打包器 `assign_ids()` 分配（`enumerate(records,1)` + 卷段位），AI 源数据只写 `slot` 不写 ID。
- `ENT-` 主键豁免撞号校验（同一实体多次出现共用 ID）。
- 子节点 ID 走 `assign_child_ids()` 派生 `<父ID>#<序号>`，保留已有 ID。

---

## 15. 枚举治理

- 启用层枚举单点文件 `scripts/_kg_enums.py`（或对应语言枚举文件）。
- 基准值继承工厂 `references/enum-library.md`（权威源，树状）；本书新增值收集-报告-暂存 → 决议 → `registerVersion+1` → 回溯存量。
- 口径漂移检测：`drift_ratio() > 1.5` 告警。

---

## 16. Phase ④ 试点示例条目（卷46 真实条目，已过关）

> 取卷46 科举卷 5 组真实条目，按本 schema 试跑一轮（校验脚本 `_pilot_check.py`：OK=31 / FAIL=0）。
> 通过 `scripts/_common.py` 护栏：`cn2int()` 对真实纪年串（洪武三年→3 / 永乐二十二年→22 / 万历三十八年→38 / 崇祯四年→4）正确；ID 前缀合法；枚举封闭校验无越界；QUAN `region` 必填；L3 `examiners/sessions` 必填；NAM 四元组；L5↔FRD 互指；REG `cross_kb`/`cross_ref` 跨库联动字段存在。
> **试点发现并已修**：`EXAM_TIERS` 原缺武科 tier → 已补 武乡试/武会试/武殿试（见 §4/§6.2）。
> **已知限制（非 schema 硬伤）**：`cn2int("洪熙元年")` 返回 `None`（"元"不在数字表）；实例 TME 用显式 `era.year` 字段规避，不阻断抽取。

### 示例 1 — 八股（OBJ 薄层，卷46-L25）

```json
{"slot":1,"item_id":"02-001","obj_id":"OBJ-031","name":"八股","obj_class":"文制",
 "alias":["时文","制义","经义"],
 "specs":{"form":"破承起讲入手起股中股后股束股（体用排偶，代古人语气）"},
 "evidence":"其文略仿宋经义，然代古人语气为之，体用排偶，谓之八股，通谓之制义。",
 "src_loc":"卷46-L25","confidence":0.95}
```

### 示例 2 — 科举三级（L3 流程，卷46-L25）

```json
{"proc_id":"PROC-014","item_id":"02-001","name":"科举三级考试",
 "steps":[
  {"step_id":"PROC-014-01","seq":1,"text":"乡试（行省举行，中者曰举人，子午卯酉年八月）",
   "agent":{"text":"考官","agent_ent_ids":["ENT-0203"]},
   "examiners":[{"text":"主考二人","ent_ids":["ENT-2001"]}],
   "sessions":["初场《四书》义三道、经义四道","二场论一道、判五道、诏诰表内科一道","三场经史时务策五道"],
   "next":["PROC-014-02"]},
  {"step_id":"PROC-014-02","seq":2,"text":"会试（礼部举行，中者曰贡士，辰戌丑未年二月）",
   "examiners":[{"text":"知贡举","ent_ids":["ENT-2002"]}],
   "sessions":["同乡试三场"],"next":["PROC-014-03"]},
  {"step_id":"PROC-014-03","seq":3,"text":"殿试（皇帝亲策，中者曰进士，分三甲）",
   "examiners":[{"text":"皇帝","ent_ids":["ENT-emp"]}],
   "sessions":["策一场"],"next":[]}
 ],
 "events":["EVT-012"]}
```

### 示例 3 — 洪武三年开科（REG★骨架 + QUAN region + TME + NAM，卷46-L27）

```json
{"slot":1,"item_id":"02-003","reg_id":"REG-014","name":"科举乡试","category":"科举制",
 "selection_type":"科目","exam_tier":"乡试","school_type":"",
 "evolution":"初，洪武三年诏……明年，始特开科取士。","tme_ids":["TME-021"],
 "agencies":[{"text":"礼部","ent_ids":["ENT-0203"],"cross_kb":"mingshi-zhiguanzhi","cross_id":"ORG-xxx"}],
 "targets":["举人","监生","生员"],
 "levied_items":[
   {"item":"解额","form":"录取名额","amount":100,"unit":"人","region":"直隶","basis":"直隶贡额百人","item_ent_ids":[]},
   {"item":"解额","form":"录取名额","amount":40,"unit":"人","region":"河南","basis":"河南…皆四十人","item_ent_ids":[]}],
 "rates":[],"scope":"全国","regions":["直隶","河南","广西","广东"],
 "documents":["科录"],"agents":[{"kind":"品官","text":"考官"}],"purposes":["选官"],
 "abuses":[{"abuse":"冒籍","reform":"严核籍贯","era":{"reign":"万历"},"opn_ids":[]}],
 "source":"明史选举志","source_item_id":"02-003",
 "evidence":"于是京师行省各举乡试：直隶贡额百人，河南、山东、山西、陕西、北平、福建、江西、浙江、湖广皆四十人，广西、广东皆二十五人……",
 "cross_ref":[{"kb":"mingshi-shihuozhi","ref":"QUAN-xxx","note":"科费/廪给"}],
 "src_loc":"卷46-L27","status":"定制","confidence":0.92}

{"amount":100,"unit":"人","form":"解额","region":"直隶","raw":"直隶贡额百人","origin":"乡试","side":"未分","confidence":0.95}
{"amount":40,"unit":"人","form":"解额","region":"河南","raw":"河南…皆四十人","origin":"乡试","side":"未分","confidence":0.95}

{"slot":1,"item_id":"02-003","tme_id":"TME-021",
 "era":{"text":"洪武三年","dynasty":"明","reign":"洪武","year":3},
 "target":{"text":"开科取士","ent_ids":["ENT-xxx"]},
 "action":"初置","content":"诏设科举","category":"初置",
 "related_evo":"EVO-014","ref_item":"02-003","confidence":0.95}

{"slot":1,"item_id":"02-003","nam_id":"NAM-014","name":"洪武三年廷试第一题名","category":"一甲题名",
 "entries":[{"seq":1,"person":"吴伯宗","courtesy_name":"","hometown":"金溪（江西）","office":"礼部员外郎","person_ent_ids":["ENT-3001"]}],
 "ent_ids":["ENT-3001"],"evidence":"帝亲制策问，试于奉天殿，擢吴伯宗第一。","confidence":0.9}
```

### 示例 4 — 南北榜案（L5 事件 + FRD 防弊，卷46-L29）

```json
{"slot":1,"item_id":"02-007","evt_id":"EVT-012","type":"科场案",
 "who":{"text":"刘三吾、白信蹈等","who_ent_ids":["ENT-4001","ENT-4002"]},
 "action":"南北榜争议","what":"洪武丁丑考官刘三吾等所取皆南士，帝怒，覆阅后诛白信蹈等，戍三吾，亲取北士","when":"洪武三十年","where":"未明",
 "related_frd":"FRD-008","related_reg":"REG-014","confidence":0.9}

{"slot":1,"item_id":"02-007","frd_id":"FRD-008","name":"分地偏私","mechanism":"考官所定榜次偏重南士，致帝疑取士不公",
 "cases":[{"event_id":"EVT-012","note":"洪武丁丑南北榜案"}],"related_reg":"REG-014",
 "evidence":"自洪武丁丑，考官刘三吾、白信蹈所取宋琮等五十二人，皆南士。","confidence":0.9}
```

### 示例 5 — 武科（REG + TME + NAM，卷46-L38）

```json
{"slot":1,"item_id":"02-012","reg_id":"REG-015","name":"武科","category":"武科",
 "selection_type":"科目","exam_tier":"武会试","school_type":"",
 "evolution":"武科，自吴元年定。洪武二十年俞礼部请，立武学，用武举。","tme_ids":["TME-022"],
 "agencies":[{"text":"兵部","ent_ids":["ENT-0204"],"cross_kb":"mingshi-zhiguanzhi","cross_id":"ORG-yyy"}],
 "targets":["武举人","武进士"],
 "levied_items":[{"item":"武科会额","form":"录取名额","amount":100,"unit":"人","region":"全国","basis":"万历三十八年定会试之额，取中进士以百名为率","item_ent_ids":[]}],
 "rates":[],"scope":"全国","regions":["全国"],"documents":[],"agents":[{"kind":"武官","text":"考试官"}],
 "purposes":["选武官"],"abuses":[],"source":"明史选举志","source_item_id":"02-012",
 "evidence":"武科，自吴元年定。洪武二十年俞礼部请，立武学，用武举。","src_loc":"卷46-L38","status":"定制","confidence":0.9}

{"slot":1,"item_id":"02-012","tme_id":"TME-022",
 "era":{"text":"崇祯四年","dynasty":"明","reign":"崇祯","year":4},
 "target":{"text":"武举殿试","ent_ids":[]},"action":"初置","content":"武举殿试自此始","category":"初置",
 "related_evo":"EVO-015","ref_item":"02-012","confidence":0.9}

{"slot":1,"item_id":"02-012","nam_id":"NAM-015","name":"崇祯四年武科殿试第一题名","category":"一甲题名",
 "entries":[{"seq":1,"person":"王来聘","courtesy_name":"","hometown":"未明","office":"及第","person_ent_ids":["ENT-3002"]}],
 "ent_ids":["ENT-3002"],"evidence":"赐王来聘等及第、出身有差。武举殿试自此始也。","confidence":0.9}
```

> 以上 5 组覆盖：OBJ 薄层 / L3 流程+考官+场次 / REG★骨架+选举 token+跨库联动 / QUAN region 维度 / TME 纪年 / NAM 四元组 / L5 事件五元组 / FRD 手法+案例。字段、枚举、ID 命名、跨层互指均通过护栏，可进入全卷抽取。
