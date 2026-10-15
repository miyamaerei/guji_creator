# 治谱知识工程交付包

**书名**：《治谱》十卷 + 卷十补遗祥刑要览
**作者**：明·佘自强
**基底**：`校对/` 目录（用户指定）
**生成日期**：2026-10-15

## 文件清单

| 文件 | 内容 | 条数 |
|---|---|---|
| `_item_registry.json` | 底座指纹库（条目级） | 401 |
| `ent.json` | 实体 mention（每条目内出现的实体） | 649 |
| `ent_global.json` | 全局实体表（按 normalized 归并） | 556 |
| `rule.json` | 规则型条文（禁/义/允） | 1029 |
| `struct.json` | 四维结构化（ACT/FRD/LGR/TME） | 408 |
| `reg.json` | 典章制度引用 | 145 |
| `opn.json` | 作者论说 | 165 |
| `trl.json` | 白话文对位（直接取现成白话，不另译） | 401 |
| `kg_join.json` | 跨层索引（按 item_id 聚合六层） | 401 |
| `kg_join_flat.csv` | 扁平视图（Excel 直接打开） | 401 |

## 条目录入

每条目 `item_id` 格式 `NN-XXX`：
- `NN` = 卷号 01~11
- `XXX` = 卷内序号

卷号映射：
| 卷 | 门 | 条数 |
|---|---|---|
| 01 | 初选门 | 19 |
| 02 | 到任门 | 48 |
| 03 | 堂事门 | 5 |
| 04 | 词讼门 | 75 |
| 05 | 钱粮门 | 53 |
| 06 | 人命门 | 20 |
| 07 | 贼盗门 | 45 |
| 08 | 狱囚门 | 9 |
| 09 | 待人门 | 30 |
| 10 | 杂事门 | 41 |
| 11 | 补遗祥刑要览 | 56 |

## 层字段速查

### ent.json
- `ent_id`: ENT-XXXX（条目内唯一）
- `global_ent_id`: GENT-XXXX（全局归一，见 ent_global.json）
- `text`: 原文词
- `normalized`: 归一化名
- `type`: official/person/institution/doc/work/place/system/behavior/punishment/time/quantity/unknown/era

### struct.json
- `struct_id`: ACT/FRD/LGR/TME-XXXX
- `dim`: 维度
- `target`: 行为主体/对象字符串
- `target_ent_id`: 命中 ent.normalized 时填 GENT-XXXX，否则 null

### rule.json
- `rule_id`: RULE-XXXX
- `type`: prohibition/requirement/permission
- `subject`/`object`/`action`/`modal`

### opn.json
- `opn_id`: OPN-XXXX
- `stance`: positive/negative/neutral/prescriptive/descriptive
- `evidence_refs`: 当前为空（子 Agent 未填）

## 已知边界
1. **rule 是 auto_v3 启发式候选**（confidence=0.7），约 5% 误判待人工复核
2. **ent type=unknown** 22 条集中在卷十铳药法，待启用 object 枚举后批量改
3. **opn.evidence_refs** 全空，待补跨层引用
4. **struct.target 命中 ent** 58/408（14%），其余 target 是行为/动作非实体，正常
