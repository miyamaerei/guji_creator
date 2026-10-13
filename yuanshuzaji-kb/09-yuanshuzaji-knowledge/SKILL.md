---
name: yuanshuzaji-knowledge
description: 《宛署杂记》知识工程实例 skill——按已确认方案执行：底座（卷→条目指纹库）→ 启用层逐层抽取（实体/职官任职/事件/文献资产/制度/名录谱牒/作者论说/方言风俗/地理古迹）→ 跨层整合 → 交付可查询、可溯源、可重跑的知识资产与报告。当用户需要处理/研读/查询《宛署杂记》、明·沈榜宛平方志性亲历杂记、把这本书做成知识库、或基于本实例继续补充数据时使用。由 book-knowledge-factory 实例化（编号 09），方案与格式契约已与用户确认，直接执行即可，无需重新设计层。
---

# 《宛署杂记》知识工程规范（书实例 skill）

> 由 book-knowledge-factory 实例化：2026-10-12 确认方案；按 `docs/新书开工流程.md` Step 0 查契约（tools/book-mcp selftest 20 项全过）后固化契约台账。通用方法论见工厂 `../../Skills/00-book-knowledge-factory/references/`；本实例只保留该书特有的内容，独立可执行。

## 0. 研读目标与口径（已确认）

| 项 | 选择 |
|---|---|
| 研读目标 | 知识抽取 + 建库查询（把宛平知县亲历亲记的方志性杂记转成可查询、可溯源、可重跑的知识资产） |
| 粒度 | 条目级：**155 条 = 165 个 ○/△ 标题 − 10 个 ○ 分组标题**（○/△ 标题行 = 条目，正文归其下至下一标题/卷尾；○ 分组标题无正文不作条目） |
| 判定方式 | AI 逐条判定 + 代码验缺漏（触发词引擎只作候选，不作结论） |
| 交付形态 | JSON + 汇总报告 + 跨层 CSV（Excel 直接打开） |
| 启用层 | L0 底座 / L1 实体 / APPT 职官任职 / L5 事件 / LIT 文献资产 / REG 制度 / NAM 名录谱牒 / OPN 作者论说 / CUS 方言风俗 / GEO 地理古迹 / 跨层索引 |
| 翻译 | **不建 TRL 层**（沿用 lgs/政学录口径：白话文 20 卷已全译）。`白话文/` 作**对照引用源**，不参与抽取 |

## 0.1 引导式反思记录（来源：工厂 Phase ②，本实例的源头）

> 只固化**结论与锁层依据**（下方三块）；探查/反思的完整过程与用户原话存工厂案例档 `../../Skills/00-book-knowledge-factory/references/case-feedback-yuanshuzaji.md`，不进实例。后续增量的结论以增量条目**追加**在此，不重写历史。

**用户提出的方向**（第一输入，原话或要点）：
- "下一本书就是苑署杂记，在yuanshuzaji-kb里，**这本书并不是类似新官上任的注意事项，而是知县本人的亲历亲记**，所以按照新书开工" → 否定官箴规则型方案（非 L1+L2+L4），指向笔记/亲历/方志型方案；用户确认 9 层方案后"ok，继续"；并强调"记得写开工手册"

**层库参考与自定义征询**：展示 L0 底座 / L1 实体 / APPT / L5 事件 / LIT / REG / NAM / OPN / CUS / GEO / OBJ / REL / MING / TRL 等候选，附全书信号匹配说明（密度统计见 case-feedback）。

**各层建/不建证据**（来源标注：用户提出 / 层库参考 / 自定义）：

| 层 | 来源 | 建/不建 | 理由与数据证据 |
|---|---|---|---|
| L0 底座 | 公共 | 建 | 必做：165 个 ○/△ 标题（155 条目 + 10 分组）锚点是全部层原文注入源 |
| L1 实体层 | 层库参考 | 建 | 人名（卷三知县题名 60+/诗文作者 60+/乡贤）、地名（宛平/芦沟桥/静乐堂/慈寿寺 等北京地理）、职官（知县/县丞/主簿/典史/府尹/巡按）、机构（礼仪房/司礼监/奶子府）、寺观祠庙名（僧道卷）、碑记书目——全书密集 |
| APPT 职官任职 | 层库参考（C1，水东首创） | 建 | 卷三职官题名（知县·县丞·主簿·典史历任，正德→万历百年，含籍贯/出身/任年/升迁去向）——APPT 富矿；志遗诗文作者各带官职（大学士/尚书/编修） |
| L5 事件层 | 层库参考 | 建 | 亲历见闻（"余初至宛平，曾选一女…"）+ 沿革叙事（万历六年革县丞/十二年复设）+ 人物传（乡贤徐邈/张华…）+ 营造事件（敕建慈寿寺/永济桥/芦沟河堤——含年月） |
| LIT 文献资产 | 层库参考（C2） | 建 | 整篇抄录体密集：历年宣谕全文（正德→万历 14 年）、万历敕谕 2 篇、敕建碑记全文 4 篇（张居正/李时/袁炜/商辂撰）、志遗诗文 60+ 人整篇收录 |
| REG 制度层 | 层库参考 | 建 | 宛平政务制度成体系：宣谕祖制/奶口/三婆/土工/吏役编制/马政/铺行/契税/经费（银两物品细目）/坟墓规制/祠祭/陵园 |
| NAM 名录谱牒 | 层库参考（C4） | 建 | 卷三知县题名碑（entries 四元组：人名/籍贯/出身/任年，典型题名录）+ 卷十六乡贤名录 + 志遗诗文作者名录 + 坟墓卷王坟/妃嫔/功臣名录 |
| OPN 作者论说 | 层库参考（C9） | 建 | 各卷末"按/愚谓/愚尝/闻之古"议论成体系（卷一宣谕末大段、卷三职官末"夫官倌也"、卷十三婆末、卷十土工末） |
| CUS 方言风俗 | 层库参考（C8） | 建 | 卷十一民风一（土俗）/民风二（方言）专卷 |
| GEO 地理古迹 | 层库参考（客座 GEO） | 建 | 卷五山川（山/水）/古迹/街道/铺舍、卷四署廨/古墨斋、卷九坟墓陵园——宛平=北京城西地理，GEO 高价值（同客座赘语） |
| OBJ 名物 | 层库参考 | 不预建 | 无物产专卷；执行期若物产/器物词成体系再走增量 |
| REL 人物关系 | 层库参考 | 不预建 | 传记中关系非主线（方志体不以人物关系为纲） |
| MING 明代纪事 | 层库参考 | 不建 | 全书即明志（作者亲历万历朝），"涉明索引"无增量价值 |
| L2 规则 / L3 流程 / L4 四维 | 层库参考 | 不建 | 宣谕为劝谕套话（"说与百姓每…"），非 IF-THEN 规范体；无统一防弊/文簿对象体系；用户点名"非新官上任注意事项" |
| TRL 翻译 | 用户提出（lgs 口径延续） | 不建 | 白话文 20 卷已全译，作对照引用源 |

**确认结论**：用户拍板——9 层方案（L0+L1+APPT+L5+LIT+REG+NAM+OPN+CUS+GEO+跨层索引）、条粒度（155 条 = 165 标题 − 10 分组）、JSON+CSV、不建翻译层/规则层/四维。锁层即按此执行，无需再设计。

## 0.2 本书契约台账（来源：docs/新书开工流程.md Step 0，tools/book-mcp 实查 2026-10-12）

| 契约 | 本书的决定 | 状态 |
|---|---|---|
| C1 目录 | **内含式**：skill 与工程同仓同版本——实例 `yuanshuzaji-kb/09-yuanshuzaji-knowledge/`，工程数据（`_extract/_src/_layers/_build/_validate/_deliver/`）在 `yuanshuzaji-kb/` 根；交付目录只叫 `_deliver/` | ✅ 定 |
| C2 ID | item_id = `NN-NNN`（卷-序）全书唯一；prefix_registry：`ent→ENT-`、`appt→APPT-`、`evt→EVT-`、`lit→LIT-`、`reg→REG-`、`nam→NAM-`、`opn→OPN-`、`cus→CUS-`、`geo→GEO-`；前缀全局唯一、禁止跨层占用 | ✅ 定 |
| C3 底座 | `_item_registry.json` 扁平 dict `{item_id: {original, norm}}`，原文唯一源只入不出；`_src/` AI 源数据**绝不手抄原文**，original 由打包器注入 | ✅ 定 |
| C4 层 | 启用层：`ent`/`appt`/`evt`/`lit`/`reg`/`nam`/`opn`/`cus`/`geo`（layer_key=目录名，snake_case 单数无别名）；schema_fields/enum_fields 见 `references/schemas.md` §2 登记表 | ✅ 定 |
| C5 枚举 | 单点 `_kg_enums.py`（yuanshuzaji-kb 根）：ENTITY_TYPES 20 / APPT_STATUS 12 / EVENT_TYPES 27（中文顶层）/ LIT_TYPES / REG_TYPES / NAM_TYPES / OPN_STANCES 5 / CUS_TYPES 12 / GEO_TYPES 继承基准库快照 + 本书归纳校准（封闭+兜底）；打包器只从它读、未注册值记 ERR 不静默放行 | ✅ 定 |
| C6 产物 | 层 JSON 必填字段按 §2 登记 schema_fields 校验完整性；`_kg_join.json` + `_kg_join_flat.csv` 必建；交付物统一进 `_deliver/` | ✅ 定 |
| C7 元数据 | frontmatter `name: yuanshuzaji-knowledge` == 目录 slug 部分；登记工厂 `references/registry.md` | ✅ 定 |

## 1. 执行流程总览

按**四段式**执行（`docs/新书开工流程.md` §8），每阶段收尾对照工厂 `../../Skills/00-book-knowledge-factory/references/checklists.md`：

```
① build_base.py（切卷切条 → _extract/ + _item_registry.json）
→ ② _src/ 装填（AI 逐条：只写条号 + 解读字段，绝不手抄原文）
→ ③ build_<layer>.py（打包：ID 分配 / 归一 / 枚举硬校验 / 从指纹库注入 original）
→ ④ build_kg_join.py + validate_layers.py（跨层索引 → 校验 → _deliver/）
```

## 2. 底座（C3，公共地基，先做）

1. 输入文件：`assets/sources/宛署杂记_原文_全卷合并.txt`（**唯一权威来源，随实例存放**；底本为明·沈榜《宛署杂记》万历刻本系统，20 卷 + 自序）。`白话文/` 卷文件作对照引用源，不参与抽取。
2. 章节划分：**20 卷**，卷号按原书顺序直接映射（01 卷一=宣谕 / 02 卷二=县始分土署廨古墨斋 / 03 卷三=职官 / 04 卷四=山川古迹 / 05 卷五=铺舍街道 / 06 卷六=地亩人丁繇赋力役 / 07 卷七=黄垡仓廊头 / 08 卷八=宫庄子粒 / 09 卷九=马政 / 10 卷十=奶口三婆土工 / 11 卷十一=驾相养济院孤老 / 12 卷十二=契税 / 13 卷十三=铺行 / 14 卷十四=经费上 / 15 卷十五=经费下 / 16 卷十六=人物 / 17 卷十七=民风 / 18 卷十八=恩泽坟墓 / 19 卷十九=僧道 / 20 卷二十=志遗），卷号表见 `references/schemas.md` §1。自序（【自序】）**不设条目**，仅作背景。
3. 条目切分：
   - **标题条目**：正文 `○`/`△` 开头的标题行，每个标题与其后正文（至下一 ○/△ 标题或卷尾）为一条；标题行内嵌小标（如"△敕撰"后跟碑记全文）并入条目原文；
   - **○ 分组标题不作条目**（复用政学录"分组不计数"坑的推广形态）：○山川/○经费上/○经费下/○人物/○恩泽/○志遗一~五 共 10 个为卷内分区标记（无独立正文、其后直接 △ 子目），仅作切分参考；其下 △ 子目为条目；
   - 正文段落（一段一行）全部归入其下最近标题条目；
   - 卷首【卷N】行与空行跳过；`（卷首篇目）` 若存在与正文标题同名重复 → **以正文 ○/△ 行为准**，篇目不重复计数（复用 lgs 坑）；
   - 产出 `_extract\NN_卷名.txt`（格式 `条N|○标题|正文`），预计 **155 条**（= 165 标题 − 10 分组，分布见 schemas.md §1；标题 165 全覆盖用于交叉校验，一个不能丢）。
4. 指纹库 `_item_registry.json`：`{item_id: {original, norm}}`；**norm 归一规则**：繁体/异体字归一为规范简体（厯→历、廵→巡、■〈…〉 缺字保留原形），标点按现代句读归一。
5. 全部条目建 task 清单（阶段可见、完成可核）。
6. **业务 ID 由打包器自动分配**：AI 源数据只写卷内顺序槽位，不手写业务 ID；打包器按「卷号 × 段容量 +1」段位分配，段容量默认 500（C2）。
7. **写盘与并行纪律**：写文件一律「临时文件 + rename 落盘」；共享汇总文件统一增量合并语义（`--volumes` 只重算请求卷、合并写回）；验证脚本写文件输出，不依赖 stdout。

## 3. 实体层方案（ent，启用）

- layer_key=`ent`，前缀 `ENT-`，目录 `_layers/ent/`；schema_fields = `ent_id, item_id, text, type, start, end, normalized, confidence, source`；enum_fields = `type`。
- 实体类型枚举（**继承基准库快照 → 落 `_kg_enums.py`**，封闭 + 兜底"unknown"）：本书启用子集 = `person / official / institution / place / era / work / object / doc / system / behavior / punishment / quantity / unknown`（animal/plant/food/star/event/posthumous 无成体系证据不启用，保留在单点文件中作封闭全集）。
- 种子词典规则：全文本内生（词条必须出现在原文，否则自动剔除）；种子来源：人名（知县题名 60+ / 诗文作者 60+ / 乡贤列女仙释 / 碑记作者）、职官（知县/县丞/主簿/典史/府尹/巡按/大学士/尚书/编修/检讨/指挥/太监）、机构（礼仪房/奶子府/司礼监/锦衣卫/光禄寺/文书房/兵马司）、地名（宛平/大兴/芦沟桥/静乐堂/北安门/慈寿寺/西山/浑河 等）、纪年（正德/嘉靖/隆庆/万历/洪武/永乐）、碑记书目（敕谕/敕建慈寿寺记/敕建永济桥记/敕修芦沟河堤记/敕修汉寿亭侯庙记）。
- 归一规则：异体/繁体→简体（同底座 norm）；同义复合词形用 alias_index 手工映射，不动标注。
- 主键表：ENT-001..N + alias_index（词形 → ent_id）。

## 4. 职官任职层方案（appt，启用）

- layer_key=`appt`，前缀 `APPT-`，目录 `_layers/appt/`；schema_fields = `appointment_id, item_id, person, person_ent_ids, office, official_ent_ids, institution, institution_ent_ids, when, status, evidence, original, confidence`；enum_fields = `status`。
- **定位**：人物-官职-时间-状态的任职记录（"谁在何时担任何职"）。
- 任职状态枚举（**继承基准库快照 → `_kg_enums.py` APPT_STATUS 12 值**）：现任 / 致仕 / 升迁 / 贬谪 / 罢黜 / 兼领 / 暂代 / 追赠 / 未明 / 起复 / 世袭 / 举荐。
- 执行口径：卷三职官题名（知县/县丞/主簿/典史历任）每人一条 APPT（person=人名、office=其职、when=任年、status=现任/升迁/未明，升迁记 evidence）；诗文作者官职（大学士/尚书/编修等）按文中明示任职登记；一条目多人任职拆多条共享 item_id。
- 任职动词/句式词典：`任 / 升 / 迁 / 改 / 除 / 授 / 起 / 致仕 / 兼 / 领 / 擢`；人名+官职+年号句式为主（无"到任交割"型流程，不建模）。

## 5. 事件层方案（evt，启用）

- layer_key=`evt`，前缀 `EVT-`，目录 `_layers/evt/`；schema_fields = `event_id, item_id, type, who, who_ent_ids, action, what, when, where, original, confidence`；enum_fields = `type`。
- **定位**：亲历见闻/沿革/营造/人物纪事五元组登记（who/action/what/when/where）。
- 事件类型：**继承基准库 `enum-library.md` §1.3 顶层 27 值（中文）**（朝政/制度/沿革/营造→其他/人物纪事→轶事/人事任免/经济/祭祀/文事…，封闭+兜底"其他"）→ `_kg_enums.py` EVENT_TYPES；本书不新增顶层，未匹配值走 V3 收集-决议。
- 执行口径：一条叙事 = 一个 EVT；碑记/敕谕全文中的营造/敕建事件（慈寿寺/永济桥/芦沟河堤/汉寿亭侯庙）按文中年月记 EVT（when=年号+年份）；人物传（乡贤）择要事记 EVT（如"张华赞伐吴功成封广武侯"）；亲历见闻（"余初至宛平曾选一女…"）记轶事；未建模条目如实记缺口（不强行造事件）。

## 6. 文献资产层方案（lit，启用）

- layer_key=`lit`，前缀 `LIT-`，目录 `_layers/lit/`；schema_fields = `lit_id, item_id, title, author, author_ent_ids, type, content_location, original, confidence`；enum_fields = `type`。
- **定位**：书中整篇收录/抄录的文献登记（宣谕全文/敕谕全文/敕建碑记全文/诗文整篇）。与 CIT 分工：本书无"征引考辨"体，CIT 不建；LIT 收全部抄录文本。
- 文献类型枚举（**继承基准库 §1.11 四部树快照 → `_kg_enums.py` LIT_TYPES**）：本书启用子集 = 诏敕（宣谕/敕谕）/ 碑记 / 诗文（诗/文）/ 记 / 题跋 / 奏议 / 其他；归入四部树（史部-诏令奏议、集部-别集诗文）。
- 执行口径：整篇抄录各算一条 LIT（title=文题/无题取首句，author=撰者，content_location=条目定位）；志遗三/四 △ 诗文作者每人一篇（首句为题）；宣谕历年全文按"某年宣谕"一条或多条（同体例可并，首句为题）；事件层对长文按语义拆事件，LIT 只管登记不拆。

## 7. 制度层方案（reg，启用）

- layer_key=`reg`，前缀 `REG-`，目录 `_layers/reg/`；schema_fields = `reg_id, item_id, name, type, content, evolution, target, original, confidence`；enum_fields = `type`。
- **定位**：制度本体静态描述登记（制度名 + 内容要点 + 沿革 + 出处）。与 L1 system 实体分工：L1 标制度**词**；REG 记制度**条目级描述**。
- 制度类型枚举（**继承基准库 §1.12 中文 12 值 + 本书归纳增量 → `_kg_enums.py` REG_TYPES**，封闭+兜底"其他"）：朝仪 / 官制 / 铨选考课 / 赋役 / 礼仪 / 祭祀 / 科举 / 司法 / 财政 / 军政 / 民政救济（本书：奶口/三婆/土工/养济院孤老）/ 宫禁内府（本书：礼仪房/奶子府/宫人殡送）/ 其他。
- 执行口径：一条目含多个制度可拆多条共享 item_id；沿革要点（"万历六年革县丞一员/十二年复设如故"）记 evolution 不另拆事件；content 写要点不抄原文（C3）；银两物品细目（奶口每季煤炭杂器清单）归 REG content 要点 + L1 quantity 实体，不逐项展开。

## 8. 名录谱牒层方案（nam，启用）

- layer_key=`nam`，前缀 `NAM-`，目录 `_layers/nam/`；schema_fields = `nam_id, item_id, name, category, scope, entries, ent_ids, original, confidence`；enum_fields = `category`。
- **定位**：表格式名录登记——卷三职官题名（知县/县丞/主簿/典史历任）、卷十六乡贤/列女/仙释、志遗诗文作者名录、坟墓卷王坟/妃嫔/功臣名录。
- 名录类型枚举（**继承基准库 §1.5 快照 → `_kg_enums.py` NAM_TYPES**）：本书启用子集 = 官员题名 / 题名记 / 人物 / 文人 / 僧侣 / 皇族 / 其他。
- 执行口径：表格式名录整体一条 NAM（entries 数组化：seq/person/courtesy_name/hometown/office 五元组，卷三题名即此型）；乡贤/列女/仙释按传主登记（entries 简化或空 + evidence）；志遗诗文作者名录按人登记；仅提及无完整表者登记话题（entries 空 + evidence），不强行展开。

## 9. 作者论说层方案（opn，启用）

- layer_key=`opn`，前缀 `OPN-`，目录 `_layers/opn/`；schema_fields = `opn_id, item_id, topic, stance, argument, evidence_refs, original, confidence`；enum_fields = `stance`。
- **定位**：作者直接议论/判断/评价登记（"按/愚谓/愚尝/闻之古/余谓"型论说段）。
- 立场枚举（**继承基准库快照 → `_kg_enums.py` OPN_STANCES 5 值**）：肯定 / 否定 / 怀疑 / 讽刺 / 中立。
- 执行口径：AI 逐条判定论说段（卷末"按"体议论）；argument 只写要点概要不抄原文；可引 LIT/EVT（evidence_refs 引用 ID）；一条目多段议论拆多条共享 item_id。

## 10. 方言风俗层方案（cus，启用）

- layer_key=`cus`，前缀 `CUS-`，目录 `_layers/cus/`；schema_fields = `cus_id, item_id, type, region, term, description, original, confidence`；enum_fields = `type`。
- **定位**：方言词、民俗、禁忌、谚语、节令、物产习俗记录（卷十一民风一土俗 + 民风二方言）。
- 类型枚举（**继承基准库 §1.7 快照 → `_kg_enums.py` CUS_TYPES 12 值**）：方言词 / 民俗 / 禁忌 / 谚语 / 节令 / 物产习俗 / 婚丧 / 信仰祭祀 / 称谓 / 风尚 / 技艺 / 其他。
- 执行口径：民风一逐条民俗（term+description）；民风二逐条方言词（term=方言词，description=释义/例证）；region 一律"宛平"（ent_id 引用）；一俗多卷互见可合并（count 字段）。

## 11. 地理古迹层方案（geo，启用）

- layer_key=`geo`，前缀 `GEO-`，目录 `_layers/geo/`；schema_fields = `geo_id, item_id, name, category, attributes, lore, ent_ids, original, confidence`；enum_fields = `category`。
- **定位**：宛平地理与古迹登记（山川/水/古迹/街道/铺舍/署廨/陵墓/寺观祠庙）。
- 类型枚举（**继承基准库 §1.17 GEO_TYPES 快照 → `_kg_enums.py` GEO_TYPES**）：本书启用子集 = 山水（山/水/潭/泉）/ 寺观祠庙 / 桥渡 / 都邑宫阙（城郭/官署/街道铺舍）/ 陵墓（陵寝/坟茔）/ 水利沟渠 / 园第坊巷 / 政区 / 其他。
- 执行口径：geo 对象按条目登记（name=地名/寺观名，category 命中枚举，attributes=文中方位/里程/形制键值对，lore=AI 解读）；与 L1 place 实体分工：L1 标地名词，GEO 记条目级地理对象描述；一寺观多卷互见可合并（count 字段）。

## 12. 跨层整合（kg_join，必建）

- ID 对齐审计点：实体主键唯一 / 引用槽位合法 / item_id 全回填（155 条全覆盖）/ target 用 ID / 枚举口径一致。
- 跨层索引：`_kg_join.json` + `_kg_join_flat.csv`（每行 = 一条目）：`item_id / volume / source / appts / events / lits / regs / nams / opns / cuss / geos / ents / layer_count`（槽位按启用层裁剪）。
- 枚举治理（C5）：单点 `_kg_enums.py` + registerVersion（新增值 version+1 回溯存量）；校验用**「收集-报告-暂存」**模式，未匹配值入 pending 表不中断，收尾统一决议；改值须双写 `enum-changelog.md`。

## 12.5 治理组件（默认启用）

- **V2 人工校验闭环**（layer_key=`review`）：同名异人/存疑判定（如知县重名、诗文作者官职异名）自动收集入"待核清单"CSV（含 provenance），人工核前不强行合并（宁建勿并），核后回写。
- **V3 枚举校准**（layer_key=`enum_calib`）：执行期未匹配枚举值 → 收集-报告-暂存 → 收尾决议（新增/归并/改名）→ registerVersion+1 → 回溯存量；新增值必须有实例证据。

## 13. 管线与验证（四段式）

- 工程根：`yuanshuzaji-kb/`（与实例同目录，内含式）。
- 命令序列（从工程根执行）：
  - `python build_base.py` —— ① 底座：切卷切条 → `_extract/` + `_item_registry.json`
  - `python build_ent_keys.py --volumes NN` —— 实体层（含主键表）
  - `python build_appts.py --volumes NN` —— 职官任职层
  - `python build_events.py --volumes NN` —— 事件层
  - `python build_lits.py --volumes NN` —— 文献资产层
  - `python build_regs.py --volumes NN` —— 制度层
  - `python build_nams.py --volumes NN` —— 名录谱牒层
  - `python build_opns.py --volumes NN` —— 作者论说层
  - `python build_cuss.py --volumes NN` —— 方言风俗层
  - `python build_geos.py --volumes NN` —— 地理古迹层
  - `python build_kg_join.py --volumes NN` —— 跨层整合
  - `python validate_layers.py` —— 校验（`_validate/` 缺漏清单 ERR=0/GAP=0 才算过）
  - `python run_all.py [--volumes NN]` —— 全量 / 单卷幂等重跑
- **键名约定**：各层产物顶层键统一 `records`；打包器内建源数据键名映射表（SRC_KEY），源数据键名与打包容器键分处声明；`_src/` 只写条号 + 解读字段（C3）。
- 验证：每层"验证缺漏清单.txt"问题数 = 0（实体未归一 / 缺 item_id / target 悬空 / item_id 未全回填等）；区分结构性错误 ERR 与执行缺口 GAP；验证脚本写文件输出，不依赖 stdout；未注册枚举值记 ERR 不静默放行（C5）。

## 14. 交付清单

- 交付物统一进 `_deliver/`（C1）。
- 按层聚合交付（每层一组：归一汇总 + 验证清单 + 卷示例 + 跨层索引），≤6 组。
- 《使用报告》：快速查询（跨层 CSV 一行全看 / 实体主键反查 / 各层归一汇总）、全文回查溯源（指纹库）、白话文对照引用、可重跑管线、扩展指南。
- 《项目总结报告》：时间线、反思、根因、方法论沉淀、缺口与建议。
- 交付物按环境可用方式交付（本地文件路径或打包视图），说明验证方式、覆盖范围与仍存在的缺口。

## 15. 缺口与边界（执行中持续更新）

| 缺口 | 现状 | 补法 |
|---|---|---|
| 卷号映射与条目分布 | 20 卷 155 条（165 标题 − 10 ○ 分组）已由底座实测核定，固化 schemas.md §1 | 已核定 |
| 历代宣谕同体例多条 | 卷一宣谕含正德→万历历年全文 | 按"某年宣谕"合并为 1~2 条 LIT 或逐年多条，执行期定 |
| 志遗诗文作者官职 | 部分作者官职文中明示（大学士/尚书），部分未明 | 明示者登 APPT，未明者 evidence 记"未明" |
| 与客座赘语/五杂俎跨书重叠 | 北京地理/寺观/人物（张华《博物志》等）与客座 GEO/人物可互证 | 联邦并入时跨书查重 |
| 原文缺字/异体 | 保留原形入 norm，标注待核 | 人工校验闭环回填 |

## 资源索引

- `references/schemas.md`：本实例启用层的 schema/枚举/ID/触发词/契约登记表 + **示例条目**（写源数据/打包器时读）
- `assets/sources/宛署杂记_原文_全卷合并.txt`：原文（唯一权威来源，随实例存放，切分主源）
- `assets/sources/` 卷拆分 + `白话文/`：对照引用源（不参与抽取）
- `assets/templates/usage_report_template.md`：《使用报告》母版（交付阶段用）
- `assets/templates/project_summary_template.md`：《项目总结报告》母版（交付阶段用）
- 格式契约：`../../tools/book-mcp/`（`python server.py list / layers / enums`；contract.json 唯一真源）
- 通用方法论/检查单/坑：见工厂 `../../Skills/00-book-knowledge-factory/references/`（methodology.md / checklists.md / pitfalls.md / enum-library.md）
