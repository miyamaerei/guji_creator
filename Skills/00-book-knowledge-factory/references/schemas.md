# Schema 与 ID 规范

> 写源数据、打包器、验证脚本时对照本文。所有 schema 在 Phase ③《操作指南》中按书定制后锁死，执行期不再改动。

## 1. 全局约定



* **条粒度主键**：`item_id = NN-NNN`（卷 - 序，如 `04-002`），全书唯一，是所有层的共同锚点。

* **ID 命名空间**（每层唯一前缀，禁止跨层占用）：



| 层    | 前缀         | 示例                      |
| ---- | ---------- | ----------------------- |
| 实体主键 | `ENT-`     | ENT-323                 |
| 规则   | `XGF-R-`   | XGF-R-001               |
| 流程   | `XGF-P-`   | XGF-P-121               |
| 事件   | `XGF-E-`   | XGF-E-001               |
| 结构   | 按维度        | LGR/TME/DOC/ACT/FRD-001 |
| 跨层索引 | `_kg_join` | —                       |

> 命名空间唯一归属：XGF-E 必须只属于事件层，流程层只引用事件 ID。



* **original 不手抄**：AI 源数据只写条号与解读字段；打包器从 `_item_registry.json` 注入 `original`/`norm`。

## 2. 底座 schema

### `_item_registry.json`（指纹库）



```
{
  "04-002": { "original": "原文全文", "norm": "归一化后的原文" }
}
```



* `norm`：异体字 / 缺字 / 标点归一后的版本，比对与检索用。

* 后续每层的 `original` 字段都从本库注入，修正差异以本库为准。

### 章节文件



* 每章一个 XHTML/MD，命名 `NN_卷名.xhtml`；`00` 为版本说明卷。

## 3. L1 实体层 schema

### 每卷标注 JSON



```
{
  "volume": "03",
  "annotations": [
    {
      "id": "ENT-000", "item_id": "03-001", "text": "正官",
      "type": "official", "start": 12, "end": 14,
      "normalized": "正官", "confidence": 0.95, "source": "原文片段"
    }
  ]
}
```



* `type`：封闭枚举（从本书文本归纳）+ 兜底 `unknown`。

* `start/end`：在原文中的字符偏移，用于定位与去重。

### 归一汇总 JSON



```
{
  "normalized_inventory": [
    { "normalized": "正官", "type": "official", "count": 12,
      "first_source": "03-001", "surfaces": ["正官","正官人"] }
  ]
}
```

### 主键表 JSON



```
{
  "entities": [
    { "ent_id": "ENT-284", "normalized": "正官", "type": "official",
      "count": 12, "first_source": "03-001", "surfaces": ["正官"] }
  ],
  "alias_index": { "正官": "ENT-284", "把门皂隶": "ENT-xxx" }
}
```



* `alias_index`：词形 → ent\_id 反查；复合解读词形（如 "把门皂隶"→皂隶）手工加映射，不动标注。

## 4. L2 规则层 schema



```
{
  "rule_id": "XGF-R-001", "item_id": "03-002",
  "type": "prohibit",            // 禁止/义务/允许/程序/时限/处罚/优先级
  "modals": ["prohibit", "penalty"],
  "condition": "当……时",
  "subject": { "text": "官府（知县）", "subject_ent_ids": ["ENT-396"] },
  "action": "……",
  "object": "……",
  "purpose": "……",
  "punishment": "打三十",
  "original": "（打包器注入）", "confidence": 0.9
}
```



* 组合规则（一条含多个模态）拆为多条规则记录共享 item\_id，或单条多 modal 字段（按书定，写进《操作指南》）。

## 5. L3 流程层 schema



```
{
  "process_id": "XGF-P-121", "item_id": "04-002",
  "name": "直日时刻表",
  "steps": [
    { "step_id": "P-121-01", "seq": 1, "text": "卯时到任",
      "agent": { "text": "正官", "agent_ent_ids": ["ENT-284"] },
      "next": ["P-121-02"] }
  ],
  "state_machine": {            // 仅显式时序素材建此字段
    "states": ["卯时","辰时","巳时"],
    "transitions": [ { "from": "卯时", "to": "辰时", "on": "击鼓", "guard": "……" } ]
  },
  "events": ["XGF-E-012"],
  "original": "（打包器注入）"
}
```



* 时序为散点、无显式顺序 / 条件 / 迁移边时：不建 state\_machine，如实标注 "点不是线"。

## 6. L4 结构化层 schema（五维示例）



```
{
  "ledgers":  [ { "id": "LGR-001", "item_id": "03-005", "name": "钱粮簿", "type": "文簿", "fields": [], "ent_ids": [] } ],
  "times":    [ { "id": "TME-001", "item_id": "04-002", "name": "卯时", "type": "时辰", "ent_ids": [] } ],
  "docs":     [ { "id": "DOC-001", "item_id": "05-001", "name": "申文", "stage": "呈报", "ent_ids": [] } ],
  "actors":   [ { "id": "ACT-001", "item_id": "03-002", "name": "佐贰官", "role": "辅佐", "ent_ids": [] } ],
  "frauds":   [ { "id": "FRD-001", "item_id": "07-003", "name": "飞洒", "mechanism": "作弊", "ent_ids": [] } ]
}
```



* 每个维度一个封闭枚举（ROLE\_TYPES / MECH\_TYPES 等），维度按书增减。

## 7. L5 事件层 schema



```
{
  "event_id": "XGF-E-001", "item_id": "01-003",
  "type": "就任",
  "who": { "text": "新官", "who_ent_ids": ["ENT-323"] },
  "action": "到任", "what": "……",
  "when": "未明", "where": "未明"
}
```



* 未明字段必须显式写 `"未明"`，不省略。

## 8. 跨层索引 schema



```
{
  "item_id": "04-002",
  "volume": "04", "source": "原文",
  "rules": ["XGF-R-012"], "procs": ["XGF-P-121"],
  "events": ["XGF-E-012"], "structs": ["TME-001"],
  "ents": ["ENT-323","ENT-284"],
  "layer_count": 5
}
```



* 扁平 CSV 同字段平铺一行，`layer_count` 表示贯通层数（五层全贯通 = 5）。

## 9. 枚举治理（registerVersion 模式 + 基准值继承）



* 所有枚举（实体类型 / 规则类型 / 模态 / 事件类型 / 角色 / 机制 / ID 前缀等）收进单文件 `_kg_enums.py`（或对应语言枚举文件）。

* **基准值继承**：启用层枚举优先继承工厂 `references/enum-library.md`（通用基准库，树状）规范值快照，不自创词形；同义值走别名映射归并（如 office→official、book→work、主从→上下级、刑罚→司法）。

* **新书归纳增量**：本书出现基准库外的新值 → 收集 - 报告 - 暂存（pending 表，不中断）→ 决议（新增 / 归并 / 暂存，新增须有实例证据 + 使用说明）→ registerVersion+1 → 回溯存量 → 更新基准库与实例快照（流程见工厂 `references/enum-induction-guide.md`）。

* **树状管理**：枚举值 ≥15 或有天然层级时按树组织（顶层大类封闭 → 子类 → 叶子，深度 ≤3，父类计数 = 子类求和）；实例按需继承子树。

* 枚举值带 `version`；**新增值必须 version+1 并回溯全部存量数据**，不允许静默扩容。

* 口径漂移检测：注释 / 文档中的枚举数与代码一致，验证脚本比对。