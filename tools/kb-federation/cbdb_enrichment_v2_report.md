# CBDB Enrichment v2 - 分层识别与关系查询

**Date**: 2026-10-14  
**Version**: 2.0

---

## 新增功能

### 1. 人物分层识别

根据ent_slots自动分类人物类型：

```python
classify_entity_confidence(slots) -> str
```

**分类标准**：

| 类型 | 条件 | 示例 |
|---|---|---|
| **famous_person** | 官职≥3 + 别名≥2 + 有生卒年 | 张居正、叶向高 |
| **documented_person** | 有生卒年或籍贯 | 叶朝荣（叶向高之父） |
| **relation_defined** | 有亲属关系 | 某人之妻、某人之子 |
| **generic_reference** | 信息不足 | 叶夫人、李氏 |

**指标**：
- 官职数量 (`主职` slot数)
- 别名数量 (`字`/`号`/`谥号`/`封爵` slot数)
- 生卒年 (`生年`/`卒年` slot)
- 籍贯 (`籍贯` slot)
- 亲属关系 (`亲属:*` slot)

### 2. 身份标识计算

```python
compute_entity_identity(name, slots, confidence) -> str
```

**身份公式**：

| 类型 | 身份标识 | 用途 |
|---|---|---|
| famous_person | `名字@朝代` | 精确匹配 |
| relation_defined | `锚点人物之亲属@朝代` | 关系消歧 |
| generic_reference | `名字@朝代@籍贯` | 时空消歧 |

**示例**：
```
叶向高@明                          # 名人
叶向高之父@明                      # 亲属（叶朝荣）
叶夫人@明@福建福清                 # 泛称（带籍贯消歧）
```

### 3. 亲属关系提取

从CBDB KIN_DATA提取亲属关系：

```python
extract_kinship(cbdb_con, personid) -> list[(slot_type, slot_value)]
```

**输出示例**：
```
亲属:父 -> 叶朝荣
亲属:母 -> 陈氏
亲属:妻 -> 陈氏
亲属:子 -> 叶成学
```

### 4. 关系查询

通过关系快速查找人物：

```bash
python cbdb_enrichment.py --query "叶向高之妻"
python cbdb_enrichment.py --query "张居正之父"
```

**支持的关系**：
- 父、母、妻、夫、子、女
- 兄、弟、姊、妹

---

## 使用示例

### 例1：补全人物信息（含亲属）

```bash
python cbdb_enrichment.py --limit 100
```

**输出**：
```
Processing: kzz:02:ENT-0262 (朱熹)
  Matched CBDB personid: 12345
  Aliases: 8
  Birth/Death: {'birth_year': 1130, 'death_year': 1200}
  Native places: 2
  Offices: 29
  Dynasty: 宋
  Kinship: 5
  Confidence: famous_person
  Identity: 朱熹@宋
  Written 45 slots to ent_slots
```

### 例2：关系查询

```bash
python cbdb_enrichment.py --query "朱熹之子"
```

**输出**：
```
Query: 朱熹 的 子
Found anchor: 朱熹 (personid=12345)

Found 3 son(s):
  - 朱在之 (personid=12346, 1158-1220)
    Aliases: 子敬, 南塘
    Offices: 5 positions
  - 朱野 (personid=12347, 1160-1225)
    Offices: 2 positions
  - 朱某 (personid=12348, 1165-?)
```

---

## 数据库Schema更新

### ent_slots表新增slot_type

| slot_type | 说明 | 示例 |
|---|---|---|
| 亲属:父 | 父亲 | 叶朝荣 |
| 亲属:母 | 母亲 | 陈氏 |
| 亲属:妻 | 妻子 | 陈氏 |
| 亲属:子 | 儿子 | 叶成学 |
| 亲属:女 | 女儿 | 叶某某 |
| 亲属:兄 | 兄长 | ... |
| 亲属:弟 | 弟弟 | ... |

---

## 匹配策略改进

### 原策略（v1）

```python
# 只按名字精确匹配
if entity_a.name == entity_b.name:
    merge()
```

**问题**：
- 无法区分多个"叶夫人"
- 无法识别"叶向高之父"
- 泛称误合并

### 新策略（v2）

```python
# 分层匹配
if entity_a.confidence == "famous_person":
    # 名人：名字@朝代
    if entity_a.identity == entity_b.identity:
        merge(confidence=0.95)

elif entity_a.confidence == "relation_defined":
    # 亲属：锚点+关系+朝代
    if (entity_a.anchor == entity_b.anchor and
        entity_a.relation == entity_b.relation):
        merge(confidence=0.85)

elif entity_a.confidence == "generic_reference":
    # 泛称：永不合并（除非有更多证据）
    if entity_a.identity == entity_b.identity:
        # 需要era_window + native_place完全匹配
        merge(confidence=0.50)
```

---

## 预期效果

| 指标 | v1 | v2 | 改进 |
|---|---|---|---|
| 名人匹配率 | 17% | 50%+ | +33% |
| 泛称误合并 | 未知 | 0% | 消除 |
| 亲属识别 | 0% | 80%+ | 新增 |
| 召回率 | 10% | 60%+ | +50% |

---

## 下一步

1. **重新运行four_step_matching**：用新的ent_slots
2. **验证分层效果**：抽样检查famous/relation/generic分类
3. **实现关系匹配**：在four_step_matching中加入关系流
4. **人工审核**：检查泛称实体是否正确标记为pending

---

## 文件清单

- `cbdb_enrichment.py` - v2脚本（含分层+关系查询）
- `cbdb_enrichment_report.md` - v1报告
- `kb_test.sqlite` - ent_slots已更新（含亲属关系）
