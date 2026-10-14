# 《大明一统志》启用层 Schema 与枚举

> 本文件记录所有启用层的字段定义、枚举值、ID 规则与试点示例。

---

## 0. 通用约定

- `item_id` = `NN-NNN`（卷号-卷内条序），所有层的共同锚点
- 业务 ID 由打包器 `assign_ids()` 按全局序号分配，AI 源数据只写槽位
- `original` 字段 = 原文指纹，不手抄正文
- 枚举新增值走 V3 校准：收集 → 报告 → 决议 → registerVersion+1 → 回溯

---

## 1. L1 实体层（ENT）

### Schema

```json
{
  "ent_id": "ENT-001",
  "name": "真定府",
  "type": "geo",
  "alias": ["恒山郡"],
  "first_source": "03-001",
  "norm": "真定府",
  "note": ""
}
```

### 实体类型枚举（封闭 + 兜底"待定"）

| type | 说明 | 示例 |
|---|---|---|
| `geo` | 地理单元 | 顺天府/井陉县/浙江布政使司/恒山 |
| `person` | 人物 | 马援/李贤/朱儁 |
| `mtn` | 山川 | 剑山/滹水/倒马关 |
| `site` | 古迹建筑 | 龙兴寺/北岳庙/百花楼 |
| `prod` | 物产 | 马/胡桃/葡萄/阿魏 |
| `book` | 典籍 | 通典/元史/图经/郡志 |
| `era` | 年号 | 洪武/永乐/宣德 |
| `dynasty` | 朝代 | 秦/汉/隋/唐/宋/元/明 |
| `待定` | 待分类 | — |

---

## 2. GEO 地理实体层（★骨架）

### 节点 Schema

```json
{
  "geo_id": "GEO-001",
  "item_id": "03-001",
  "name": "真定府",
  "type": "prefecture",
  "region": "北直隶",
  "parent": "GEO-000",
  "children": ["GEO-002", "GEO-003"],
  "volume_range": "卷3",
  "attributes": {
    "borders": [
      {"direction": "东", "to_place": "河间府献县界", "distance_li": 310},
      {"direction": "西", "to_place": "山西平定州界", "distance_li": 180},
      {"direction": "南", "to_place": "顺德府内丘县界", "distance_li": 210},
      {"direction": "北", "to_place": "保定府庆都县界", "distance_li": 170}
    ],
    "to_capital": [
      {"capital": "京师", "distance_li": 630},
      {"capital": "南京", "distance_li": 2100}
    ],
    "households": {"count": 14, "unit": "里"},
    "grain_tax": {"amount": 117000, "unit": "石", "note": "一十一万七千石零"},
    "jun_name": "恒山",
    "topography": "壮哉一都防…",
    "customs": "性缓尚儒仗义任侠…",
    "garrisons": [
      {"name": "真定卫", "type": "卫", "location_text": "在府治东南洪武三年建"},
      {"name": "神武右卫", "type": "卫", "location_text": "在真定卫西宣德五年建"}
    ],
    "fiefs": []
  },
  "cit_ids": ["CIT-001", "CIT-002"],
  "original": "真定府【东至…】"
}
```

### type 枚举

| type | 说明 |
|---|---|
| `metro` | 京师/南京（首都级） |
| `prefecture` | 府 |
| `department` | 直隶州（布政司直属州） |
| `subprefecture` | 属州（府属州） |
| `county` | 县 |
| `foreign` | 外夷国（卷89–90） |
| `other` | 其他 |

### region 枚举（封闭）

`北直隶 / 南直隶 / 山东 / 山西 / 河南 / 陕西 / 浙江 / 江西 / 湖广 / 四川 / 福建 / 广东 / 广西 / 云南 / 贵州 / 外夷`

---

## 3. EVO 建置沿革层

### Schema

```json
{
  "evo_id": "EVO-001",
  "item_id": "03-001",
  "geo_id": "GEO-001",
  "dynasty": "秦",
  "era": null,
  "institution_name": "钜鹿郡地",
  "action": "置郡",
  "detail": "禹贡冀州之域，周为并州地，春秋属鲜虞国，战国属赵，秦为钜鹿郡地",
  "original": "禹贡冀州之域…秦为钜鹿郡地"
}
```

### action 枚举

`置 / 废 / 改 / 并 / 复 / 因之 / 升 / 降 / 迁 / 未明`

---

## 4. MTN 山川层

### Schema

```json
{
  "mtn_id": "MTN-001",
  "item_id": "03-001",
  "geo_id": "GEO-001",
  "name": "剑山",
  "type": "山",
  "location_text": "在井陉县东一十里",
  "description": "其形似剑",
  "lore": "",
  "original": "剑山【在井陉县东一十里其形似剑】"
}
```

### type 枚举

`山 / 岭 / 峰 / 冈 / 岩 / 洞 / 泉 / 溪 / 江 / 河 / 湖 / 潭 / 池 / 堰 / 关 / 桥 / 井 / 其他`

---

## 5. PER 人物层

### Schema

```json
{
  "per_id": "PER-001",
  "item_id": "03-001",
  "geo_id": "GEO-001",
  "name": "张乔",
  "type": "名宦",
  "dynasty": "汉",
  "native_place": "",
  "office": "交州刺史",
  "summary": "顺帝时象林蛮区连入寇，乔单车至州，寇徒自弭",
  "original": "张乔【顺帝时象林蛮区连入寇州郡讨之不克于是选乔为交州刺史乔单车至州寇徒自弭】"
}
```

### type 枚举

`名宦 / 流寓 / 人物 / 列女 / 仙释 / 其他`

---

## 6. SITE 古迹建筑层

### Schema

```json
{
  "site_id": "SITE-001",
  "item_id": "03-001",
  "geo_id": "GEO-001",
  "name": "龙兴寺",
  "type": "寺观",
  "location_text": "在府治东",
  "history_lore": "宋建后有大悲阁内铸铜佛像高与阁等，本朝洪武初重修",
  "original": "龙兴寺【在府治东宋建后有大悲阁内铸铜佛像髙与阁等本朝洪武初重修】"
}
```

### type 枚举

`寺观 / 祠庙 / 陵墓 / 古迹 / 宫室 / 学校 / 书院 / 坛庙 / 城池 / 苑囿 / 关梁 / 其他`

---

## 7. PROD 物产层（薄层，仅外夷卷 89–90）

> **范围限定**：仅抽取卷 89–90（外夷诸国）。府级条目不做物产抽取。外夷卷物产密集（安南胡椒/占城犀象/暹罗苏木/西域玛瑙/珊瑚等），府级物产记载稀疏（全书仅 6 处）。

### Schema

```json
{
  "prod_id": "PROD-001",
  "item_id": "90-001",
  "geo_id": "GEO-XXX",
  "name": "胡椒",
  "category": "植物",
  "note": "蔓生似山薯春花秋实",
  "original": "胡椒【蔓生似山薯春花秋实】"
}
```

### category 枚举

`动物 / 植物 / 矿物 / 织物 / 饮食 / 珍宝 / 药材 / 其他 / 未明`

---

## 8. CIT 引书层

### Schema

```json
{
  "cit_id": "CIT-001",
  "item_id": "03-001",
  "cited_work": "通典",
  "cited_work_ent_id": "ENT-XXX",
  "context": "证俗",
  "original": "【通典】"
}
```

### context 枚举

`立论 / 证俗 / 考源 / 补遗 / 其他`

---

## 9. 跨层索引

### Schema（_kg_join.json）

```json
{
  "item_id": "03-001",
  "volume": "03",
  "source": "真定府",
  "ents": ["ENT-001", "ENT-002"],
  "geos": ["GEO-001"],
  "evos": ["EVO-001", "EVO-002"],
  "mtns": ["MTN-001", "MTN-002"],
  "pers": ["PER-001"],
  "sites": ["SITE-001"],
  "prods": [],
  "cits": ["CIT-001"],
  "layer_count": 7
}
```

---

## 10. 试点示例（Phase ④ 产出）

### 试点条目：真定府（卷3，item_id = 03-001）

已按 schema 试跑，GEO/EVO/MTN/PER/SITE/CIT 字段均命中，无 ERR。

- GEO-001：真定府，type=prefecture，region=北直隶，borders 4 条，to_capital 2 条，households=14里
- EVO-001~N：沿革链（禹贡→周→春秋→战国→秦→汉→后魏→后周→隋→唐→宋金→元→本朝）
- MTN-001~N：剑山/城山/云凤山/神山/陉山/…（井陉县境内）
- PER-001：名宦 张乔（汉）
- SITE-001：龙兴寺（府治东，宋建）
- CIT-001：【通典】（风俗段）
