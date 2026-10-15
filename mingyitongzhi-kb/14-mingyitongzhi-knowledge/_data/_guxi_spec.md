# 广西 11 府装填规范（必须严格遵守）

## 工程根
`E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\`
原文：`E:\git\ToolBox\guji\mingyitongzhi-kb\明一统志.txt`（UTF-8，用 PowerShell `Get-Content -Encoding UTF8` 读取指定行范围）
输出目录：`_data/vol{96..106}/`（目录不存在则自建）

## 样板（先精读再动笔）
- 主文件：`_data/vol49/49-001_南昌府.json`
- 县占位：`_data/vol49/49-001_c01_南昌县.json`
- 卫所占位：`_data/vol49/49-001_w01_南昌前卫.json`
- 名宦分片：`_data/vol49/49-001_pers1_名宦.json`
- 人物分片：`_data/vol49/49-001_pers2_人物.json`
- 列女仙释分片：`_data/vol49/49-001_pers3_列女仙释.json`
- 寺观祠庙陵墓分片：`_data/vol49/49-001_sites1_寺观祠庙陵墓.json`
- 宫室关梁公署学校书院分片：`_data/vol49/49-001_sites2_宫室关梁公署学校.json`

## 文件命名与分片模式
主文件：`{vol}-001_{府名}.json`，例如 `96-001_桂林府.json`
- 直辖县占位：`{vol}-001_c{NN}_{县名}.json`（NN 从 01 起，按原文出现顺序）
- 普通属州占位：`{vol}-001_s{NN}_{州名}.json`
- 土州/土司占位：`{vol}-001_t{NN}_{州名}.json`
- 卫所占位：`{vol}-001_w{NN}_{卫名}.json`
- 名宦分片：`{vol}-001_pers1_名宦.json`
- 人物分片：`{vol}-001_pers2_人物.json`（本府无"人物"段则不建）
- 列女+仙释分片：`{vol}-001_pers3_列女仙释.json`（本府两段都没有则不建；只有一段也建此文件，放该段）
- 寺观+祠庙+陵墓分片：`{vol}-001_sites1_寺观祠庙陵墓.json`
- 宫室+关梁+公署+学校+书院分片：`{vol}-001_sites2_宫室关梁公署学校.json`

主文件内 `layers.pers`、`layers.sites`、`layers.prods` 一律为空数组 `[]`（数据全部分到分片文件）；`layers.ents/geos/evos/mtns/cits` 在主文件内填齐。

## ID 规则
- item_id：`{vol}-001`（如 `96-001`）
- 府 geo_id：`GEO-{vol}001`（如 `GEO-96001`），type=`prefecture`，parent=`GEO-000`，region=`广西`
- 直辖县：`GEO-{vol}001-cNN`，type=`county`
- 普通属州：`GEO-{vol}001-sNN`，type=`department`
- 土州/土司：`GEO-{vol}001-tNN`，type=`tusi`
- 卫所：`GEO-{vol}001-wNN`，type=`weisuo`
- 子节点 parent 一律指向府 geo_id；children 列表必须闭合（府节点 children 要把 c/s/t/w 全部列上，顺序按原文）
- ents：府/县/州/卫 各建一条 `ENT-…`（沿用样板 ENT-C01/ENT-S01/ENT-W01 风格；土州用 ENT-TNN）；山川/人物/古迹不要求全部进 ents，挑代表性的即可（参照样板 ents 数量，约 20-40 条）
- evo_id：`EVO-001` 起；mtn_id：`MTN-001` 起；per_id：`PER-001` 起；site_id：`SITE-001` 起；cit_id：`CIT-001` 起。各分片内独立连续编号（pers1 从 PER-001 起，pers2 从 PER-101 起，pers3 从 PER-201 起；sites1 从 SITE-001 起，sites2 从 SITE-201 起），避免跨分片撞号。

## 各层字段
### geos[].attributes
府节点：borders（东西南北到界+里数）、to_capital（南京/京师里数）、households、grain_tax、jun_name（郡名）、topography（形胜）、customs（风俗）、garrisons（卫所列表）。
县/州节点：location_text（在府城X里/附郭）、households（count 用里数数字，note 原文）。
卫所节点：location_text、garrison_type（卫/千户所）。

### evos[]
从"建置沿革"段切分：每条 dynasty / era / institution_name / action（置/改/升/因之/废）/detail。

### mtns[]
遍历"山川"段，把每座山、峰、岩、洞、石、江、江、水、溪、潭、湖、井、泉、池、塘、洲、滩、堤、关隘类自然水体都收为一条。字段：
`{mtn_id, item_id, geo_id(挂到所属县/州gid；府城周边挂府gid), name, type(山/峰/岩/洞/石/江/水/溪/潭/湖/井/泉/池/塘/洲/滩/堤/关), location_text, description, lore}`
- description 取描述正文；lore 取诗/传说（无则空串 ""）。
- 密度要求：桂林/梧州/南宁/浔州等大府 mtn 尽量 60-150 条；太平/思明/思恩/镇安等小府原文只有十几条，有多少收多少，不要编造。

### pers[]（分到 pers1/2/3）
- pers1=名宦段，pers2=人物段，pers3=列女+仙释段。
- 字段：`{per_id, item_id, geo_id(挂所属县gid；府级挂府gid), name, type(名宦/人物/列女/仙释), dynasty, native_place, office, summary, original}`
- original 保留原文【…】整段；summary 提炼。

### sites[]（分到 sites1/2）
- sites1=寺观+祠庙+陵墓段；sites2=宫室+关梁+公署+学校+书院段。
- 字段：`{site_id, item_id, geo_id, name, type(寺观/祠庙/陵墓/宫室/关梁/公署/学校/书院), location_text, history_lore, original}`

### cits[]
从"形胜""风俗"段的引文切分：`{cit_id, item_id, cited_work, cited_work_ent_id:null, context(形势/风俗), original(带【】原文)}`。

## 文字规范
- name/norm/summary/description/history_lore 用规范简体（远/宁/御/都/里等），不要保留 OCR 异体（防→都/御按语境，逺→远，寜→宁，賔→宾，逹→达，瀆→渎等）。
- original 字段**照抄原文**，不改字。
- JSON：UTF-8、ensure_ascii=False、缩进 2 空格。写完用 `python -c "import json;json.load(open(...encoding='utf-8'))"` 校验每个文件可解析。

## 硬约束
1. 只写 `_data/vol96/` 到 `_data/vol106/`；不得动 `_layers/`、`_item_registry.json`、任何 merge 脚本。
2. region 一律填 `广西`。
3. 镇安府之后的田州/泗城州/利州/奉议等"八州"不在本次范围，不要装填。
4. 每个县/州/卫都要有占位文件，且主文件 geos 列表与占位文件一一对应。
