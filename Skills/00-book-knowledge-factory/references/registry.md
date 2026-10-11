# 实例台账（Instance Registry）

> 工厂的唯一实例索引。**Phase ③ 实例化、Phase ⑤ 交付、以及每次增量升级（见 `increment-upgrade.md`）后必须更新本表**。
> 实例编号规则：`<NN>-<book-slug>-knowledge`，NN = 本目录现有最大编号 +1；实例生成到本技能同级目录。同一本书的**第二套结构化方案**加变体段：`<NN>-<book-slug>-<variant>-knowledge`，"方案/变体"列记录差异来源。
> 领域技能（如 `ming-officials-kg`，非书实例）不入本表，仅作实体层种子等复用来源。另一套独立轻量工厂（`book-skill-factory` 及其生成的 `book-先进遗风`）不属本工厂生态，不入表。

| 实例目录 | 书名 | 方案/变体 | 状态 | 首次实例化 | 最近增量 | 启用层 | 源文件（实例内相对路径） | 案例反馈 | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| 01-shuidong-riji-knowledge | 水东日记 | 标准（全层 KG） | 全量执行完成（38 卷 × 8 层） | 2026-10-10 | 2026-10-10（追加 NAM 名录谱牒 + TRL 古今翻译） | L1/APPT/L5/REG/LIT/REL/NAM/TRL + V1 + 跨层索引 | `assets/sources/水东日记.txt` | [case-feedback-shuidong-riji.md](case-feedback-shuidong-riji.md) | 其案例反馈催生坑库 #11–#20 与枚举库 v2 |
| 02-qubian-knowledge | 蘧编 | 标准（全层 KG） | 已交付（执行状态见实例） | 2026-10-10 | 2026-10-10（追加 APPT + TRL） | L1/APPT/EVT/REL/LIT/TRL/MEM/CHR + V2/V3 + 跨层索引 | `assets/sources/蘧编_结构化.json` | —（教训已并入坑库 #21–#24） | 首个配齐 V2/V3 治理组件的实例；ID 段位 ×500 |
| 03-wuzazu-knowledge | 五杂俎 | 标准（全层 KG） | 已交付（执行状态见实例） | 2026-10-10 | 2026-10-10（追加 APPT + TRL） | L1/EVT/REL/NAM/CIT/OBJ/CUS/OPN/MING/APPT/TRL + V1 + 跨层索引 | `assets/sources/五杂俎.txt` | — | 13 层为现有实例中最多；ID 由打包器段位分配 |
| 04-kezuozhuiyu-knowledge | 客座赘语 | 标准（全层 KG） | 全量执行完成（10 卷 + 00 卷 × 13 层，见 `kezuozhuiyu-kb/`） | 2026-10-10（SKILL.md 标注） | — | 13 层（实体/事件/引书/名物/方言风俗/明代纪事/南京地理古迹/职官任职/名录谱牒/文献资产/作者按语论说/人物关系/古今翻译）+ 跨层索引 | （未随实例存放：源文本在仓库 `kezuozhuiyu-kb/_source/客座赘语_txt/`，实例内不复制） | — | 目录已纳入编号；SKILL.md 输入路径已相对化。遗留：frontmatter `name: kezuo-zhuiyu-knowledge` 与目录拼写不一致（工厂原则 6 要求一致，待统一） |

## 维护说明

- **状态**取值：`探查中` / `反思中` / `实例化中` / `已交付（待执行）` / `执行中` / `全量执行完成` / `已归档`。
- **方案/变体**列：标准方案填"标准（全层 KG）"；同书第二套方案填变体名 + 差异来源（如"index=摘要索引方案，仅做条目索引与摘要，区别于标准 KG 全层方案"）。
- **案例反馈**列指向工厂内的 `references/case-feedback-<book-slug>.md`；实例的反思**过程**记录存这里，实例本身只固化结论。
- 表中信息与实例实际不一致时，以实例 SKILL.md 为准并回改本表。
- 新实例交付时同时在本表登记；实例退役/归档只改状态不删行。
