# 明一统志知识工程 — 交接文档（2026-10-15）

## 当前状态（干净）

- **registry: 70 条**
- **ERR: 0, GAP: 0**
- GEO 树 758 节点
- 层记录：ent3118 / geo758 / evo3057 / mtn4424 / per7239 / site6633 / cit347
- 最新 commit: `ed73a23`

## 已完成 region（按 volume-map 顺序）

| Region | 卷 | 条目数 | 状态 |
|---|---|---|---|
| 北直隶 | 1-5 | 13（京师+顺天+保定+河间+真定+顺德+广平+大名+永平+永宁州） | ✅ 7层全 |
| 南直隶 | 6-17 | 15 府 | ✅ 县节点补完 |
| 山西 | 19-21 | 8 府州 | ✅ 县节点补完 |
| 山东 | 22-25 | 7 府（济南/兖州/东昌/青州/登州/莱州+辽东都司） | ✅ |
| 河南 | 26-31 | 9（8府+汝州） | ✅ |
| 贵州 | 88 | 21（8府+4州+7卫+2土司） | ✅ |

## 下一个任务：陕西卷 32-37

**还没派子 Agent**——本会话两次 create_agent 都被打断。

### 派单提示词（直接复制给新会话）
```
请派子 Agent 处理明一统志陕西卷32-37。
工程根：E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\
先读 SKILL.md / references/schemas.md / references/volume-map.md / _data/vol22/22-001_济南府.json 样板。
陕西：西安/凤翔/汉中/延安/庆阳/平凉/巩昌/临洮府 + 秦邠泾固原州 + 陕西行都司卫所。
分片架构 _data/vol32-37/，府级 NN-001_名称.json，县 NN-001_cXX_名.json，州 -sXX，卫 -wXX。
pers>50 拆 _pers1_名宦/_pers2_人物/_pers3_列女仙释，sites>30 拆 sites1/2。
GEO 树 children 填真实 geo_id，parent 用 geo_id 或 GEO-000，禁止填中文。
卫所用 weisuo，土司用 tusi。
完成后跑 python validate_pilot.py，陕西相关 ERR=0。
```

## 关键脚本（在工程根）

| 脚本 | 作用 |
|---|---|
| `build_pack_pilot.py` | 老格式打包（北直隶试点+南直隶+山西+贵州） |
| `_patch_zhending_counties.py` | 真定府补县节点 |
| `_patch_nanzhili_shanxi.py` | 南直隶+山西补县节点 |
| `_merge_all.py` | **通用增量合并器**——扫 _data/volNN/*.json 追加进 _layers/（新 region 用这个） |
| `validate_pilot.py` | 校验：ERR（必须0）+ GAP（可登记） |

## 合并新 region 的标准流程

1. 子 Agent 交付 _data/volNN/*.json
2. `python _merge_all.py`（增量合并，不覆盖老数据）
3. `python validate_pilot.py`
4. 如有 ERR：修脏 item_id（EVO-xxx 类）、补缺失府级 geo 节点、去重 geo_id
5. `git add . && git commit`

## 已知陷阱

1. **build_merge.py 是全量合并，会覆盖老数据**——不要用它，用 `_merge_all.py` 增量版
2. **build_pack_pilot.py 会重置 registry**——如果跑了它，必须重跑所有 patch 脚本
3. **EVO-002/EVO-003 脏 item_id**——某些 evo 记录 item_id 填了 "EVO-002"，合并后要批量改成 "01-001"
4. **子 Agent 写文件可能覆盖 _layers/**——派单时明确告诉它"只写 _data/volNN/，不要改 _layers/"
5. **geo_id 重复**——南直隶子 Agent 曾顺手建山东县节点导致重复，_merge_all.py 已做 geo 层去重

## 后续 region 队列

陕西(32-37) → 浙江(38-42) → 江西(43-44) → 福建(45-48) → 湖广(49-58) → 四川(59-70) → 广东(71-75) → 广西(76-79) → 云南(86-87) → 外夷(89-90)
