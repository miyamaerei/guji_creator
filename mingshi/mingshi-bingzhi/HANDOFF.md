# 交接文档 — 兵志 skill 实例 · 阶段二前置步（块级 Notes 复核）

> 生成日期：2026-10-14 ｜ 交接对象：后续接手人（AI 或人工）
> 实例：`E:\git\ToolBox\guji\mingshi\mingshi-bingzhi`（bz 型正史典志体·兵志门 skill 实例）
> 工厂基线：`E:\git\ToolBox\guji\Skills\00-book-knowledge-factory`

## 1. 任务背景

按 `pilot-plan.md` §3 阶段二（AI 复核 + 问句验收）要求，对候选树
`_data/weis/candidates_66_old.json`（卷66 旧编成卫所树，L52-120）中的**块级节点 notes**
（在京/都司/府等块层括注）逐条复核，判定归属 **REG 制度层** 或 **C14 时间沿革层**，
并给出转归槽位草稿与验收记录。卫/所叶节点的 88 条括注不在本次范围。

**本次请求收尾方式**：判定的结论与分析已完成，按用户要求落地为 3 份文件 + 本交接文档，
后续续做（卫级括注复核、定稿打包）由接手人继续。

## 2. 判定的核心依据（复核时对照）

| 依据 | 位置 | 要点 |
|---|---|---|
| C14/TME schema | `references/schemas/bz_schemas.json` 的 `C14` | `record_fields` 12 槽位（AI 只填 slot，id 由打包器注入）；`TME_CATEGORIES_13`（移驻/改称/初置/裁并…）；触发源②：**卷66 括注（调北京=事件，纪年由张本行领（永乐十八年））** |
| REG schema | 同文件的 `REG` | attrs_13 + 兵志 7 token（geo_ref/num_value/…mil_class）；enums MIL_CLASS_8 / INST_TYPES_BZ_13 等 |
| 块级注规则 | SKILL.md §7 / §256 | 「已上…」为区块级注应挂块节点 notes；括注内容必须置于 notes[]，不得并入卫名 |
| 阶段二流程 | `pilot-plan.md` §3 | 复核 → save_name_index → 打包器 assign_ids/护栏 → 定稿树 `_data/weis/weis_66_old.json` → 十问验收 |
| 验收模板 | `references/query-acceptance-template.md` | 十问逐问实测；答不了须分类「原文确无」/「结构缺陷」；不得预填「能答」 |

## 3. 已完成（本次交付）

### 3.1 复核结论（块级 notes 共 2 条，全判 C14）

| 注 ID | 源文行 | 块节点 | 括注原文 | 判定 | C14 类别 | 置信 |
|---|---|---|---|---|---|---|
| BN-01 | 卷66-L57 | 左军都督府 > 在京 | 凡本府在京属卫，曾经永乐十八年调守北京者，各注其下曰“调北京”，其年月不重出。后四府同。 | C14 | 移驻 | 0.9 |
| BN-02 | 卷66-L112 | 后军都督府 > 在外 > 北平行都司 | 后为大宁都司 | C14 | 改称 | 0.85 |

- **BN-01 关键判断**：本条是 C14 触发源②所述的**纪年张本行**——为全树卫级 `(调北京)` 括注提供纪年（永乐十八年）与标注规则，故不是单纯凡例，转 C14 事件「调守北京」。
- **BN-02 关键判断**：机构沿革事件「北平行都司→大宁都司」，命中「改称」；原文仅“后为”无纪年，era=**未明**，不得补造纪年。
- **REG/C9 = 0 条**：两条均非制度实体、无论说主体，不硬塞层（工厂纪律）。

### 3.2 落地产物清单（本次新增 3 份）

| 文件 | 内容 |
|---|---|
| `_data/weis/block_notes_review.json` | 逐条复核注解：verdict + C14 转写槽位草稿（era/target/action/category/content/ref_item）+ rationale + reg_check/c9_check + deferred（已 JSON 校验通过） |
| `_data/weis/acceptance_phase2_blocknotes.md` | 按验收模板结构：复核清单与转归明细表、C14 槽位对照表、十问逐问验收（问1/9 半答，其余结构可达）、遗留与后续 |
| `HANDOFF.md`（本文件） | 交接说明 |

### 3.3 既有相关文件（接手续做时对照）

```
SKILL.md                                  # 实例主技能（§7 C14、§13 试点验收、§16-7 双证据纪律）
pilot-plan.md                             # §3 阶段二流程、§4 后定树预研
references/schemas/bz_schemas.json        # REG/C14/C17/C9 … 层 schema（判定唯一依据）
references/query-acceptance-template.md   # 十问验收模板
assets/sources/兵志.txt                    # 唯一权威源（卷66 = L42-263；L57/L112 为两条块级注行）
assets/tools/_weisuo_builder.py           # 解析器（阶段一已修复 3 风险点）
scripts/_common.py                        # 共享工具
_data/weis/candidates_66_old.json         # 候选树（阶段一产物，coverage 100%）
_data/weis/wei_name_index.json            # 卫名词典 377 词（仅覆盖 L52-120 旧编成段）
_data/weis/seed_old_full.json             # 词典生成依据（AI 复核切分痕迹，可追溯材料）
_data/weis/block_notes_review.json        # ★本次：块级注复核注解
_data/weis/acceptance_phase2_blocknotes.md # ★本次：验收记录
```

## 4. 遗留事项（接手人后续处理）

1. **卫级 88 条括注复核**（下一批次，本次明确不做）：
   - 类型：`(调北京)` ×6+ `(革)` `(后为xx卫)` `(后改属后府)` `(后为临清卫)` 等；
   - `(调北京)` 的纪年统一领自 BN-01（永乐十八年），复核后把对应 `WEI-*` 回填 BN-01 的 `ref_item`；
   - 复核接口契约：`review_candidates()` 仅 merge/rename/delete/split 四动作，split 必带 `new_names`。
2. **「已上」区块注归位**（解析器阶段一遗留，pilot-plan 未决待办）：
   - 实测发现 `已上俱改为亲军`（L111 通州卫叶）、`已上俱属后府`（L111 居庸关千户所叶）、`俱改调京卫已上俱属后府`（L112 会州卫叶）按 SKILL.md §256 属**区块级注**，当前被解析器挂到段尾卫叶——应提升至块级节点 notes；
   - 处置前先复核归属块边界，避免误动卫叶括注计数器（当前 bracket_notes_total=88）。
3. **打包器定稿**：随卫级复核完成后统一跑 `assign_ids`/护栏（FieldCoverage / assert_no_silent_zero / check_enum）→ 定稿树 `_data/weis/weis_66_old.json`；**断言豁免 `("ENT-","WEI-")`**（设计事实，勿改）。
4. **后定编成树（`--ver new`）与全卷展开**：词典现仅覆盖旧编成段 L52-120；后定编成 L122-251（含南京三子树）按同一流程：回填词典 → 重跑 → 验收覆盖率 ≥95%（pilot-plan §4；三潭子树不得混挂 SKILL.md §16-8）。
5. **九边/昌平**：昌平 0 次为原文确无，不得补造；九边走 C14/L4-EVO 叙事体质态，不入 C17 卫名。

## 5. 接手后续步骤建议

1. 通读上述 3 份落地文件 + `references/query-acceptance-template.md`，确认判定口径一致；
2. 按第 4 节督办清单逐项推进（建议先做卫级括注复核批次，再处理「已上」区块注归位，二者都会影响 88 条计数器与括注归属）；
3. 定稿前跑打包器护栏，产出 `_data/weis/weis_66_old.json`；
4. 全卷展开（卷65/67/68）按 SKILL.md §13 与工厂 A 族纪律交付三表（ERR/GAP、字段填充率、十问验收）。