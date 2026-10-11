# 《水东日记》知识工程 —— 项目框架

> 依据 
>
> `shuidong-riji-knowledge`
>
>  书实例 skill（2026-10-10 已确认方案）搭建的可重跑知识工程管线。
> 目标：服务明朝职官知识图谱（人物 / 职官任职 / 机构 / 制度供料）+ 独立可查询知识库。
> 粒度：条（每条记事 / 引文为一条）。判定方式：词典 + 规则先行候选 → AI 逐条判定 → 人工校验闭环。

## 一、目录结构



```
new-chat-2/
├── README.md                    本文件
├── _kg_enums.py                 枚举单点（registerVersion 治理，全管线唯一权威）
├── common.py                    公共基座（路径 / 指纹库 / 源数据加载 / norm 归一）
├── build_base.py                底座：卷拆分(38+00) + 条目切分 + 指纹库
├── build_ent_keys.py            L1 实体主键表 + alias_index（先查后建，随卷累积）
├── build_appt.py                APPT 职官任职打包器
├── build_event.py               L5 事件打包器
├── build_reg.py                 REG 典章制度打包器
├── build_lit.py                 LIT 文献资产打包器
├── build_rel.py                 REL 人物关系打包器
├── build_nam.py                 NAM 名录谱牒打包器
├── build_trl.py                 TRL 古今翻译打包器 + 全书记译本
├── build_kg_join.py             跨层索引（_kg_join.json / _kg_join_flat.csv）
├── validate.py                  全量验证（输出 reports/验证缺漏清单.txt）
├── run_all.py                   全量重跑入口（一条命令跑完整管线）
├── scaffold_volume.py           卷脚手架：为指定卷生成 8 层 AI 源数据模板
├── _extract/                    底座产物（volumes/ + items/ + 指纹库 + 卷概要）
├── sources/                     AI 源数据（_ent_ai_NN.py ... _trl_ai_NN.py，只写条号+解读）
├── data/                        打包器产物（ent/appt/event/reg/lit/rel/nam/trl/join）
└── reports/                     验证缺漏清单、使用报告、项目总结（交付时）
```

## 二、数据流（一次做好，处处复用）



```
水东日记.txt（13.3 万字，无句读）
   │  build_base.py
   ▼
_extract/_item_registry.json（指纹库：1197 条 = {NN-NNN: {original, norm}}）
   │  ← sources/_<layer>_ai_NN.py（AI 判定，只写条号+解读；original 由打包器注入）
   ▼
build_ent_keys → data/ent/ent_keys.json（ENT-xxx 主键 + alias_index）
build_appt/event/reg/lit/rel/nam/trl → data/<layer>/<layer>_NN.json + 汇总
   ▼
build_kg_join → data/join/_kg_join.json + _kg_join_flat.csv（跨层一行全看）
   ▼
validate.py → reports/验证缺漏清单.txt（结构性问题 = 0 为通过标准）
```

## 三、常用命令（PowerShell，工作目录 = 项目根）



```
# 全量重跑（底座 → 实体主键 → 8 层 → 跨层索引 → 验证）
python run_all.py

# 仅重跑指定卷（幂等，不破坏其他卷）
python run_all.py --volumes 01 17

# 为指定卷生成 8 层 AI 源数据模板（含该卷条目清单，供逐条填写）
python scaffold_volume.py --volumes 02
python scaffold_volume.py --volumes 02 --force   # 覆盖重建

# 单层重跑
python build_ent_keys.py --volumes 01
python build_nam.py --volumes 17
```

## 四、卷阅读模式（执行某卷前必查）

38 卷逐卷 "主导类型 / 阅读模式" 标注表见 skill `references/volume-profile.md`。

执行某卷前查该卷模式，按模式分配层优先级：

`制度优先`(05/06/30) / `名录优先`(17/29) / `谱牒优先`(15/16/18/20) / `文献优先`(19/22/35 等) / `人物优先` / `文事优先` / `均衡全层`(01)。

底座已在 `_extract/volume_summary.csv` 输出每卷行数 / 字数 / 最长行 + 模式提示，供快速参考。

## 五、底座切分规则（已探查确认，2026-10-10）



* 卷首 = "水东日记卷 X" 前一行含 "钦定四库全书"（38 个卷首 + 卷 00 四库提要）

* 卷尾落款 = 行尾 "水东日记卷 X"，剥离（独立标题行剥离后整行丢弃）

* 卷内正文按换行分行，**每行 = 一条候选条目**（叙事 / 文献卷行 = 条成立）

* **例外**：名录 / 谱牒卷（17/18/29 等）行为表格行（一行多人或跨行四元组），

  由 NAM/APPT 层按卷阅读模式重组（NAM entries 四元组），底座不做语义合并

* 装饰行剔除：`<子部...>` 书签行、卷首标题行（明　叶盛　撰）、"钦定四库全书" 行

* 卷 00（四库提要）单独 5 条，不要求 8 层

## 六、源数据填写规范（AI 判定逐卷填写）

每个 `sources/_<layer>_ai_NN.py` 模板含：本卷条目清单（条号 | 原文首 30 字）、

字段键、示例记录（schemas.md §11 示例 A\~E）、枚举表。填写规则：



1. **只写条号 + 解读字段，不手抄原文**（original 由打包器从指纹库注入）

2. 枚举封闭：值必须取自 `_kg_enums.py`（实体类型 / 任职状态 / 事件 / 制度 / 文献 / 关系 / 名录 / 翻译风格）

3. 未建模条目如实注释登记缺口，不强行编造

4. TRL 全量逐条（条目数 = 翻译数，validate 硬校验为执行缺口 GAP）

5. NAM 名录表 entries 四元组：{seq, person, courtesy\_name, hometown, office}（无则 "未明"）

## 七、当前状态（✅ 全书完成，2026-10-10）

> 早前的「试点卷 01/17、剩余 36 卷待铺」是**框架搭建阶段**的旧状态，已作废。
> 38 卷 × 8 层现已全部装填完毕，全量验证 ERR=0 / GAP=0 / OK=322。

| 项 | 状态 |
| --- | --- |
| 底座 | ✅ 39 卷（38 正文 + 卷 00 四库提要）拆分，1197 条指纹库，卷概要 CSV |
| 源数据 | ✅ **38 卷 × 8 层 = 304 个** `sources/_<layer>_ai_NN.py` 全部齐备（含 TRL 全量逐条） |
| 实体主键 | ✅ `ent_keys.json` **2291** 个归一实体（ENT-001..ENT-2291，其中名录人物补建 391 个 ENT-1901..2291）；alias_index 2291 / surfaces 2185 |
| ent 标注 | ✅ 全卷 **2253** 条标注（text 可在 original 定位、type 8 类枚举、normalized、confidence、source） |
| 各层记录 | ✅ appt **237** / event **234** / reg **72** / lit **180** / rel **126** / nam **54** / trl **1192** |
| TRL 覆盖 | ✅ **1192 条 = 正文条目数，零缺口**；38 卷逐卷「条目数 = 翻译数」硬校验全过 |
| 跨层索引 | ✅ `_kg_join.json` 1197 条（一条一行，含全层回链）；其中 5 条无层覆盖 = 卷 00 四库提要（按口径不要求 8 层） |
| 交付物 | ✅ `交付物/层聚合/`（8 层 × JSON+CSV）、`01_跨层索引.csv`、`02_实体主键表.csv`、`全书记译文本/《水东日记》全书记译文本（38卷合册）.md`（1192 条）、`Vue3多书知识阅读器设计文档.md` |
| 验证 | ✅ `python run_all.py` 全量：**结构性问题 ERR=0 / 执行缺口 GAP=0 / 通过项 OK=322** |

## 八、后续可选事项（非阻塞）

全书知识资产已交付完成，以下均为可选项：

1. **阅读器落地**：`交付物/Vue3多书知识阅读器设计文档.md` 是设计稿，尚未实现前端。
2. **双库落库**：按方案决策，数据库入库为非默认项，本期未做；产物保持 JSON/CSV/Markdown 文件形态。
3. **补建 L2/L3 抽象层**：方案明确「不建」，如需跨书推理再评估。
4. 日常复跑：`python run_all.py` 全量重跑；`python run_all.py --volumes NN` 单卷幂等重算。
5. 口径任何变更先改 `口径规范.md`，再重跑，避免层间漂移。