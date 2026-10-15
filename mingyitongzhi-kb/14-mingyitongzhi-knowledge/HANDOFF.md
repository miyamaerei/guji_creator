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

## 进行中：陕西卷 32-37（子 Agent 已在跑）

子 Agent 已产出 108 个分片文件：
- vol32: 西安府（31县+6州+5卫）
- vol34: 凤翔府（7县+陇州）
- vol35: 平凉府（7县+3州+3卫）+ 巩昌府（14县+3州+4卫）
- vol36: 临洮府
- vol37: 宁夏卫/宁夏中卫/洮州卫

**缺**: vol33 汉中府/延安府/庆阳府（待确认是否还在跑或已漏）

### 新会话接手步骤
```
cd E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge
python _merge_all.py
python validate_pilot.py
# 看 ERR/GAP，修脏 item_id
git add . && git commit
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
