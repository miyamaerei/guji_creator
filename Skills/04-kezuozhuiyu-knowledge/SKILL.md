---
name: kezuo-zhuiyu-knowledge
description: 《客座赘语》知识工程实例 skill——按已确认方案执行：底座（章节拆分+条目指纹库）→ 启用层逐层抽取（实体/事件/引书/名物/方言风俗/明代纪事/南京地理古迹/职官任职/名录谱牒/文献资产/作者按语论说/人物关系/古今翻译）→ 跨层整合 → 交付可查询、可溯源、可重跑的知识资产与报告。当用户需要处理、研读、查询《客座赘语》（明·顾起元）、把《客座赘语》做成知识库、或基于本实例继续补充数据时使用。由 book-knowledge-factory 实例化，方案已与用户确认，直接执行即可，无需重新设计层。
---

# 《客座赘语》知识工程规范（书实例 skill）

> 由 book-knowledge-factory 实例化：2026-10-10 确认方案。通用方法论见工厂 `book-knowledge-factory` 的 references；本实例只保留该书特有的内容，独立可执行。

## 0. 研读目标与口径（已确认）

| 项 | 选择 |
|---|---|
| 研读目标 | 建库查询 + 研究辅助（全书可查询知识库） |
| 粒度 | 条（按【标题】切分，`NN-NNN` 卷-序主键） |
| 判定方式 | AI 逐条 + 代码验缺漏 |
| 交付形态 | JSON + CSV（按层聚合，≤6 组）+ 两份报告 |
| 启用层 | 底座 L0 + 13 数据层（ENT/EVT/CIT/OBJ/CUS/MING/GEO/APPT/NAM/LIT/OPN/REL/TRL）+ VOL 卷阅读模式索引 + V2 人工校验闭环 + V3 枚举校准 + 跨层索引 |

## 0.1 引导式反思记录（来源：工厂 Phase ②，本实例的源头）

**用户提出的方向**（第一输入，原话或要点）：「book-knowledge-factory 帮忙创建客座赘语的技能」；书稿原在会话临时目录，现归档于仓库 `kezuozhuiyu-kb/_source/客座赘语_txt/`（全本 `客座赘语_全本.txt` + 卷一至卷十分卷 + 附录）。

**层库参考与自定义征询**：展示层库（L0 底座 / L1 实体 / L2 规则 / L3 流程 / L4 结构化 / L5 事件 / C1-C12 自定义层 / V1-V3 组件）；用户选择「完整包」，并提出自定义层「南京地理古迹层」。

**各层建/不建证据**（来源标注：用户提出 / 层库参考 / 自定义）：

| 层 | 来源 | 建/不建 | 理由与数据证据 |
|---|---|---|---|
| 底座 L0 | 层库参考 | 建 | 任何书必做；10 卷 + 附录，条目约 460-480 条 |
| ENT 实体层 | 层库参考 | 建 | 人物/职官/地名/文献/制度词成体系；人物字号表述 98 处、书名号《》1331 处 |
| EVT 事件层 | 层库参考 | 建 | 纪事密集（卷一至卷十叙事条目过半）；事件类型继承动态枚举库 23 顶层 |
| CIT 引书索引层 | 层库参考 | 建 | 引书《》1331 处为全本最大特征之一；点校说明专述引文随意/简称问题（考辨价值高） |
| OBJ 名物层 | 层库参考 | 建 | 名物考据条（物产/饮食/服饰/珍宝）全卷分布 |
| CUS 方言风俗层 | 层库参考 | 建 | 金陵风俗/方言/谚语/节令条（如俗谓、方言、习俗）；南都留都风土为主轴之一 |
| MING 明代纪事层 | 层库参考 | 建 | 明代内容自成体系；涉明（国朝/本朝/年号/亲历）信号密集 |
| GEO 南京地理古迹层 | **自定义** | 建 | 本书以南京故实为纲：金陵238/寺332/陵346/桥215/秦淮29/钟山52/南都62/留都25，多为志乘补阙的考证内容（南唐宫阙、金陵古城、后湖、桥名、城内外诸水、诸寺诸陵） |
| APPT 职官任职层 | 层库参考 | 建 | 职官制度信号密集：尚书115/御史67/侍郎31/总督/巡抚/致仕表述遍布 |
| NAM 名录谱牒层 | 层库参考 | 建 | 题名/科目/谱牒式条目（如科第、题名、先贤名录），卷十名录尤密 |
| LIT 文献资产层 | 层库参考 | 建 | 书中收录/转引诗文、碑记、奏议、诏敕全文（如碑文、记、诗） |
| OPN 作者按语论说层 | 层库参考 | 建 | 考证按语为全书五大强信号之一：按：61、余臆断1、余尝19、因思3（密度低于《五杂俎》，以考证按语为主，如实标注） |
| REL 人物关系层 | 层库参考 | 建 | 叙事/轶事/传记密集，同僚/师生/姻亲/同乡/同科等关系可提取 |
| TRL 古今翻译层 | 层库参考 | 建 | 明代文言笔记，需要现代汉语译文供理解/检索；沿用余光中风格基准 |
| VOL 卷阅读模式 | 层库参考 | 建 | 10 卷内容形态差异明显（卷二名物/卷五古迹异闻/卷七制度/卷十名录制度），按卷针对性处理 |
| 跨层索引 | 公共 | 建 | 启用 ≥13 层，必做 |

**确认结论**：用户三次确认：① 完整包；② 建立 GEO 南京地理古迹层（新自定义层，回写工厂层库 registerVersion+1）；③ 锁层清单全部确认（底座 + 13 数据层 + VOL + V2 + V3 + 跨层索引）。未启用：L2 规则层（本书为笔记体，无规范句体系，触发词不可/不许/务要等缺失）、L3 流程层（无显式步骤/时序流程素材，判"点不是线"）、L4 结构化层（无台账/时间/生命周期对象体系）、C11 奏疏谕旨层（本书非年谱/奏议集，君臣互动不成链）、C12 年谱纪年层（本书非编年体）。

## 1. 执行流程总览

按序执行，每阶段收尾对照 checklists：

```
底座（拆分 + 指纹库） → 启用层逐层抽取（AI 判定 + 代码验证） → 跨层整合 → 交付
```

## 2. 底座（公共地基，先做）

1. 输入文件：仓库相对路径 `../../kezuozhuiyu-kb/_source/客座赘语_txt/`（相对本实例目录；含 `客座赘语_全本.txt` + `客座赘语_卷一到卷十.txt` + `客座赘语_附录.txt`），处理路径：直接拆分（UTF-8 文本，无需转码/OCR）。源文本也可用环境变量 `KZZ_SRC` 指向别处。
2. 章节划分：10 卷 + 版本说明卷（00，收录总序/导读/点校说明/四库提要），命名规则 `NN_卷名.txt`。
3. 条目切分：以原文【标题】为条边界，一条 = 一个【标题】下正文；复合条目（如"花木二十二则""前记异闻一百则"）保持单条，条内用子序号 `NN-NNN-SS` 标注子则；无标题连排正文按段义切分并人工复核。预计 **约 460-480 条**。→ `_extract\NN_卷名.txt`（格式 `条N|正文`）。
4. 指纹库 `_item_registry.json`：key=`NN-NNN`，value=original/norm；norm 归一规则：异体字、缺字（□）、重文号、标点统一为现代标点。
5. 全部条目建 task 清单（**按卷建"卷帙级 task"**：一卷一个里程碑：通读 → 写入 → 三连自检 → build → 复核，串行推进）。

## 2.1 装填前置规则（卷一实证，全卷强制）

卷一装填暴露两大根因性教训，固化为本工程**每卷装填的强制前置规则**（顺序执行，缺一不可）：

**规则 A：ent 先行（实体标注先行）**

- 写任何一层源数据之前，先通读本卷 `_extract/NN_卷N.txt`，按「人物/地名/职官/书目/名物/制度词」盘点本卷**必标实体清单**；
- ENT 源数据先补齐本卷全部必标实体并登记词形；名物尤其留意植物/动物/饮食/器物——卷一 01-012~018 曾因 obj 层名物在 ENT 未标注，导致第一批 `*_ent_ids` 引用未解析批量爆发，事后补标约 90 条（ENT 508→598），成本远高于装填前摊开；
- 其他 12 层写数据时，凡引用人物/书名/地名/职官，**先查 ENT 是否已登记**该词形，未登记先补 ENT，再写入引用。

**规则 B：名称规范化（引用侧主名 + 括注仅消歧）**

- 引用字段（person/office/cited_work/name 等 `*_ent_ids` 对应文本）一律写**主名**，不写别名词形；
- 括注只用于消歧，写法 `主名（括注）`，如 `皇太子（朱高炽）`→主名 `皇太子`；打包器按「剥括注 → 括注内 → 双向子串」逐级解析；
- 别名/异称（字/号/谥/籍贯称）必须先在 ENT 登记（alias/surfaces），再允许他层引用；**未登记的自造词形不得写入引用字段**（卷一教训：`郑宣化/王公/顾起元` 等曾因 ENT 无精确词形导致引用未解析）；
- 占位词（未明/不明/无）不记引用，不得填入 person/office/cited_work 等引用槽位。

**规则 C：复合条拆条粒度基准（卷二~卷五实证强制）**

- 复合条保持单条（item_id 唯一），条内按「一则一拆」为基准粒度：巨型复合条（如卷五 05-005 前记异闻 90 则、05-015 古碑刻 60+ 条）先列则目/碑刻清单，再逐则逐碑拆成独立业务记录（EVT/CIT 等）；
- 注文/考辨性段落按段拆条，不得再细分到句；落笔前对照邻近卷既有拆条粒度确认，宁粗勿碎，防同卷粒度漂移。

**词形一致性兜底（validate 强制）**：`validate_layers.py` 会扫描非 ENT 层引用侧文本，凡命中 ENT 已登记「normalized≠text」的别名词形即输出 warning——命中须回查改主名；注文/考辨类引述（如「王僧辨《梁书》作王僧辩」）允许保留旧词形，validate 同样告警、由人工判定。

**验收顺序（引用未解析时）**：先查 ENT 是否缺标注 → 再查词形是否规范 → 最后才查匹配逻辑；先补数据，后动打包器。

## 3. ENT 实体层方案

- 实体类型枚举：继承基准库 18 值快照：person 人物 / official 职官 / institution 机构 / place 地名 / era 年号朝代 / work 文献书名 / object 名物 / animal 动物 / plant 植物 / food 饮食 / doc 文书 / system 制度 / behavior 行为 / punishment 刑罚 / time 时间 / quantity 数量 / posthumous 谥号 / unknown 类型待定。本书高频：official（尚书/御史/侍郎/总督公等）、place（金陵/秦淮/钟山/后湖及各寺各桥）、posthumous（谥 62 处）、work（引书）。
- 种子词典规则：全文本内生（词条必须出现在原文，否则自动剔除）。
- 归一规则：同人异称（名/字/号/谥/籍贯称）归并到主键，surfaces 记录全部词形（人物字号表述 98 处为重要归一线索）。
- 主键表：ENT-001..N + alias_index（词形 → ent_id；复合解读词形如"留都辅臣"→辅臣手工映射，不动标注）。
- 每卷标注 JSON + 全局归一 + 标注总报告；ID 前缀 `ENT-`。

## 4. EVT 事件层方案

- 五元组：who/action/what/when/where；未明显式写"未明"。
- 事件类型枚举：继承基准库事件类型子库 `../00-book-knowledge-factory/references/enum-library.md` §1.3 规范全集（23 顶层）：朝政/政变/军事/军政/边事/人事任免/弹劾/礼仪/科举/文事/建言/灾异/轶事/祭祀/经济/司法/神异传说/疾疫/御灾赈济/缉捕防盗/巡查监察/家事/其他。本书高频：科举（乡试 19）、文事（著述刻书）、灾异、轶事、朝政、祭祀；本书新增值走 V3 registerVersion 动态回填。
- 执行方式：试点 1 卷验收 → 全量（建议试点卷四或卷五）；未建模条目如实单列缺口。

## 5. CIT 引书索引层

- 定义：条目级引用登记——"哪条引了哪书、怎么引、为什么引"。
- schema：cit_id / item_id / cited_work(含 ent_ids，type=work) / citation_type / context / original。
- 枚举：引用方式 = 直引/转引/泛引/暗用/考辨；引用目的 = 立论/证俗/考源/反驳/补遗/其他（基准库快照；本书"考辨"为特色——点校说明专述引文随意/简称）。
- 执行流程：书名实体归 ENT（type=work）；一条引多书拆多条共享 item_id；与 LIT 分工：LIT 收整篇收录/抄录的文献，CIT 收引用/征引。ID 前缀 `CIT-`。
- 注意：本书引文常随意省称（如简称书名），norm 归一时登记全称→省称映射。

## 6. OBJ 名物层方案

- schema：obj_id / item_id / name(含 ent_ids) / category / attributes(文本可证键值对，无则留空) / lore(AI 解读) / original。
- 枚举：名物类别 = 器物/动物/植物/饮食/珍宝/材料/建筑/服饰/其他（基准库快照；本书饮食/器物/建筑为高频——如花木、奇石、服饰、酒馔）。
- 执行流程：名物实体归 ENT（type=object/animal/plant/food）；OBJ 做条目级考据登记并引用 ENT；attributes 无则留空不编造。ID 前缀 `OBJ-`。

## 7. CUS 方言风俗层方案

- schema：cus_id / item_id / type / region(含 ent_ids) / term / description / original。
- 枚举：类型 = 方言词/民俗/禁忌/谚语/节令/物产习俗/其他（基准库快照；本书俗谓、方言、习俗、节令、物产成体系）。
- 执行流程：region 引用 ENT 地名（金陵/南都/留都归一为南京）；方言词含音证/字源考据时 term+description 记录；一俗多卷互见可合并（count 字段）。ID 前缀 `CUS-`。

## 8. MING 明代纪事层方案

- schema：ming_id / item_id / era(年号+年份) / who(含 ent_ids) / what / when / where / category / first_person / ref_events(引用 EVT ID) / original。
- 枚举：涉明类型 = 朝政/人物/科举/风俗/灾异/亲历见闻/制度/其他（基准库快照；本书制度/人物/朝政/亲历为高频——作者顾起元为南京人，多亲历见闻）。
- 执行流程：与 EVT 分工——MING 只做涉明条目索引 + 亲历标记，不重复建模事件，ref_events 引用 EVT；一条目多涉明类型拆多条共享 item_id。ID 前缀 `MING-`。

## 9. GEO 南京地理古迹层方案（自定义新层，回写工厂层库）

- 定义：以南京为纲的地理古迹登记——山水/寺观/桥渡/都邑沿革/陵墓/水利/园第坊巷的方位、沿革、形胜与考证。
- schema：geo_id / item_id / name(含 ent_ids) / category / location(含 ent_ids，方位/辖属) / history(沿革，AI 解读) / evidence(考证依据，可引 CIT) / original。
- 枚举（本书归纳，封闭 + 兜底）：GEO_TYPES = 山水 / 寺观 / 桥渡 / 都邑宫阙 / 陵墓 / 水利沟渠 / 园第坊巷 / 其他。判定依据：金陵238/寺332/陵346/桥215/秦淮29/钟山52/南都62/留都25。
- 执行流程：地理实体归 ENT（type=place，如"金陵""秦淮""钟山""后湖"归一主键）；GEO 做条目级沿革考证登记并引用 ENT；一寺/一桥多卷互见可合并（count + 多 item_id 引用）；本书多志乘补阙内容，写入 history 时区分"原文所述沿革"与"顾起元考证按语"（后者的考证来源记入 evidence）。
- ID 前缀：`GEO-`（全局唯一，只属本层）。

## 10. APPT 职官任职层方案

- schema：appointment_id / item_id / person(含 person_ent_ids) / office(含 official_ent_ids) / institution(含 ent_ids) / when(未明写"未明") / status / evidence / original。
- 枚举：任职状态 = 现任/致仕/升迁/贬谪/罢黜/兼领/暂代/追赠/未明（基准库快照 9 值；本书致仕表述极多——明代南京为留都，致仕官员聚居）。
- 执行流程：任职动词词典（授/擢/迁/改/除/罢/谪/致仕/兼/领/督/巡抚/提督/尚书/侍郎等）+ 官职词典 → 正则候选 → AI 复核 → 人工校验闭环（V2）；一条目多任职拆多条共享 item_id。ID 前缀 `APPT-`。

## 11. NAM 名录谱牒层方案

- schema：nam_id / item_id / name / category / scope / entries(条目数组：seq/person/courtesy_name/hometown/office 四元组) / ent_ids / original。
- 枚举：名录类型 = 官员题名/同僚题名/迁谪录/谱牒/题名记/科第名录/其他（基准库快照 + 本书高频"科第名录"——乡试/登科题名条）。
- 执行流程：表格式名录整体一条 NAM 记录（entries 数组化）；分列小标题作为行 office 上下文；仅提及无完整表者登记话题（entries 空 + evidence），不强行展开。ID 前缀 `NAM-`。

## 12. LIT 文献资产层方案

- schema：lit_id / item_id / title(无题取首句) / author(含 author_ent_ids，佚名"未明") / type / content_location / original。
- 枚举：文献类型 = 诏敕圣旨/碑文/奏议/书启/诗/记/题跋/序/祭文/其他（基准库快照 10 值；本书碑文/记/诗/序为高频——诸寺碑记、金陵先贤碑文）。
- 执行流程：整卷抄录长文各算一条；事件层对长文按语义拆事件；title 无题取首句。ID 前缀 `LIT-`。

## 13. OPN 作者按语论说层方案

- schema：opn_id / item_id / topic / stance / argument(AI 解读非原文) / evidence_refs(可引用 CIT) / original。
- 枚举：立场 = 肯定/否定/怀疑/讽刺/中立（基准库快照 5 值）。
- 本书特色：以**考证按语**为主（按：61 处，余臆断/因思/余尝等论说句），论说 registerVersion 快照如实标注"密度低于《五杂俎》194 次"。
- 执行流程：AI 逐条判定按语/论说句（触发词表：按/余按/臆断/因思/余尝/余谓/愚谓）；argument 只写要点概要不抄原文；引证可链接 CIT。ID 前缀 `OPN-`。

## 14. REL 人物关系层方案

- schema：rel_id / item_id / person_a(含 ent_ids) / person_b(含 ent_ids) / relation_type / direction(单向/双向/未明) / evidence / original。
- 枚举：关系类型 = 同僚/师生/姻亲/同乡/同科/举荐/弹劾/恩怨/上下级/父子亲属/敌对/其他（基准库快照 12 值，本书同乡/同科/师生/同僚为高频——金陵缙绅交往圈）。
- 执行流程：只建文本有直接证据的关系，推测关系不建（宁缺毋滥）；同名异人先登记 V2 待核清单，人工核前不合并。ID 前缀 `REL-`。

## 15. TRL 古今翻译层方案

- schema：trl_id / item_id / translation / style / note / confidence / original。
- 枚举：翻译风格 = 直译/意译/注释性翻译（基准库快照）。
- 风格基准：沿用余光中七条（固化于本实例 `references/translation-style.md`）；专名保留原词+括注；职官术语符合明史口径；书名保留《》；长文分句群翻译保留分段。
- 执行流程：AI 逐条翻译（代码只验覆盖：条目数=翻译数）；缺字/异体按 norm 归一后译；支持按卷分步（VOL 模式指引翻译优先级）。ID 前缀 `TRL-`。

## 16. VOL 卷阅读模式索引（非数据层，不占 ID 命名空间）

- 产出：`references/volume-profile.md`——卷标注表（卷/主导/次要/阅读模式/判定依据）+ 阅读模式处理指引。
- 阅读模式枚举（基准库 13 值按本书定制）：制度优先 / 人物优先 / 文献优先 / 谱牒优先 / 名录优先 / 文事优先 / 论理优先 / 风土优先 / 名物优先 / 世情优先 / 轶事优先 / 灾异优先 / 均衡全层。本书预判：卷四/卷五古迹异闻→风土优先；卷七/卷九/卷十制度名物→制度优先/名物优先；卷一/卷二人物轶事→人物优先/轶事优先。
- 执行流程：① 全书按卷抽样（首尾段+关键词密度）→ AI 逐卷判定；② 固化标注表；③ 执行任一卷前查模式，按其处理重点分配抽取优先级；④ 卷完成后对照主导/次要类型检查覆盖缺口；⑤ 与卷内实际不符 → 以实际为准回填修正。

## 17. 跨层整合

- ID 对齐审计点：实体主键唯一 / 引用槽位合法（subject_ent_ids/agent_ent_ids/who_ent_ids/ref_events/ref_appts/evidence_refs 全部指向存在的 ID）/ item_id 全回填 / target 用 ID / 枚举口径一致。
- 跨层索引：`_kg_join.json` + `_kg_join_flat.csv`（每行 = 一条目，layer_count 贯通层数；13 层全贯通 = 13）。
- 枚举治理：枚举单点文件 + registerVersion（新增值 version+1 回溯存量；基准库继承值不改，本书增量值独立版本线）。
- 治理组件：V2 人工校验闭环（同名异人待核清单.csv + provenance）；V3 枚举校准（收集-报告-暂存 + dry-run 回溯，见工厂 enum-induction-guide.md）。

## 18. 管线与验证

- 源数据文件：`_ent_ai_NN.py` / `_event_ai_NN.py` / `_cit_ai_NN.py` / `_obj_ai_NN.py` / `_cus_ai_NN.py` / `_ming_ai_NN.py` / `_geo_ai_NN.py` / `_appt_ai_NN.py` / `_nam_ai_NN.py` / `_lit_ai_NN.py` / `_opn_ai_NN.py` / `_rel_ai_NN.py` / `_trl_ai_NN.py` / 标注源，只含条号 + 解读字段（不手抄原文）；**写任何一层源数据前，先执行 §2.1 ent 先行盘点与名称规范化检查**。
- 打包器（build_ 前缀、可重跑、幂等）：build_ent_keys / build_events / build_cit / build_obj / build_cus / build_ming / build_geo / build_appts / build_nam / build_lit / build_opn / build_rel / build_trl / build_kg_join + 公共基座（_item_registry 注入）+ 枚举单点。
- 验证：每层"验证缺漏清单.txt"问题数 = 0；验证脚本写文件输出，不依赖 stdout。
- 重跑命令：`bash build_all.sh`（全量）/ `bash build_all.sh --volumes 01 02`（单卷重跑，空格分隔卷号）。
- 批量验收统一序列：逐卷 build → 全量 build_all → audit 逐卷巡检 → status 对账。
- **源数据 schema 自检（写数据后、build 前必跑）**：`python check_src_schema.py --volumes NN`——
  逐层断言 13 层 `_src/_<layer>_ai_NN.py` 的 RECORDS：must_fields（排除打包器注入的 start/end/original/norm/volume）必须存在且非空、item_id 格式 NN-NNN 且卷号与文件名一致、已登记 registry、不得自带注入字段；全 13 层 0 错误方可 build。产物 `_validate/check_src_report_NN.json`。
- **统一打包（build --zip）**：`python build_layers.py --volumes NN --zip` →
  `_deliver/kezuozhuiyu_volNN_layers.zip`，固定 17 项（13 层 json + `_kg_join.json` + `_kg_join_flat.csv` + `kg_join_report.json` + `t3_report_NN.json`），arcname 一律 basename；
  先跑 validate 再生 zip 可保证 17 项齐全（t3 缺失时降级打包 16 项并打印提示）。
- **validate_layers.py 追加检查（卷五起内置）**：
  - 词形一致性（warning 级，不阻断 PASS）：引用侧文本命中 ent 层 normalized≠text 的旧词形 → 记 warning 并须回查主名；
  - 建议回查清单（report 的 `review_hints`）：复合条 top5（按条内记录数跨层合计）/ 词形差异条（warning 涉及的 item_id）/ rel+opn 密集条（rels≥2 或 opns≥2），供卷后人工抽查。

## 19. 交付清单

- 按层聚合交付（每层一组：归一汇总 + 验证清单 + 卷示例 + 跨层索引），≤6 组聚合。
- 《使用报告》：快速查询（跨层 CSV 一行全看 / 实体主键反查 / 各层归一汇总）、全文回查溯源、可重跑管线、扩展指南（模板见本实例 assets/templates/usage_report_template.md）。
- 《项目总结报告》：时间线、反思、根因、方法论沉淀、缺口与建议（模板见本实例 assets/templates/project_summary_template.md）。
- 交付物说明验证方式、覆盖范围与仍存在的缺口。

## 20. 缺口与边界（执行中持续更新）

| 缺口 | 现状 | 补法 |
|---|---|---|
| 条目总数待底座切分确认 | 预计约 460-480 条（【】标题 473 处 + 复合条目内则） | 底座切分后用代码核对 registry 条数与标题数 |
| GEO 层为新层 | 枚举 8 值首建，待全卷执行校验 | 试点校验通过后注册回写工厂层库 |
| 引书省称/异名 | 点校说明已指出引文随意/简称问题 | norm 归一 + 全称→省称映射表 |
| OPN 密度低于《五杂俎》 | 以考证按语为主，论说句 80+ 处 | 如实标注，不强行凑数 |

## 资源索引

- `references/schemas.md`：本实例启用层的具体 schema、枚举快照、ID、触发词、**示例条目**（写源数据/打包器时读）
- `references/translation-style.md`：TRL 余光中风格基准（翻译时对照）
- `references/volume-profile.md`：VOL 卷阅读模式标注表（执行前生成）
- `assets/templates/usage_report_template.md`：《使用报告》母版（交付阶段用）
- `assets/templates/project_summary_template.md`：《项目总结报告》母版（交付阶段用）
- 通用方法论/检查单/枚举库/坑：引用工厂 `book-knowledge-factory` 的 references