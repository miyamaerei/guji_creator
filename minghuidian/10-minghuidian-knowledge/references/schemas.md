# 《明会典》实例 Schema 与枚举（执行参考）

> 写源数据/打包器时读本文件。所有枚举是**探针归纳的基线**，不是封闭终态。
>
> **⚠ 枚举缺漏总则（用户原话："枚举可能有缺漏，要注明如有缺需补上"）**
> - 本文件枚举来自 85.4 万字中的 10+ 处抽样，**必然不全**。
> - 执行期遇到不匹配值，**禁止强行塞、禁止自行删除条目**。
> - 必须收集到 `_pending_enums.csv`，格式：`层名|枚举字段|未匹配值|来源 item_id|上下文片段|建议归类`。
> - 每完成一个大卷组，输出枚举使用分布报告，批处理决议：新增 / 归并 / 改名。
> - 决议后 registerVersion+1，回溯存量（dry-run 后 commit）。

---

## 0. 层节点注册表（父子树，执行前必读）

> 每个节点标 `parent`（父节点）和 `kind`（节点性质）。
> 打包器/校验脚本 `scripts/verify_tree.py` 读本表做父子关系校验。
> 新增节点必须在此表登记，并指定 parent 与 kind。

### 0.1 节点性质枚举（kind）

| kind | 含义 | 例子 |
|---|---|---|
| `root` | 七大层根节点（L0–L6），无父 | L0/L1/L2/L3/L4/L5/L6 |
| `common_type` | L1 下的实体子类型 | ENT-org / ENT-off |
| `common_child` | 通用层下的子层 | RUL / TIM / ORG / GEO / NUM / CIT |
| `business_domain` | 六部业务域（挂在 L4 下） | SEL / FIN / RIT / MIL / LAW / ENG |
| `business_sub` | 业务域下的子层 | SEL-XUAN / FIN-SHUI / RIT-SI |

### 0.2 节点注册表

| node_id | name | parent | kind | 启用卷组 | 说明 |
|---|---|---|---|---|---|
| L0 | 底座 | — | root | G0–G8 全部 | 卷-事目-条-指纹库 |
| L1 | 实体 | — | root | G0–G8 全部 | 实体归一 |
| L1.org | 衙门实体 | L1 | common_type | G0–G8 | org 衙门 |
| L1.off | 官职实体 | L1 | common_type | G1/G4/G7/G8 | off 官职 |
| L1.geo | 地名实体 | L1 | common_type | G2/G3/G4/G6 | geo 地名 |
| L1.doc | 典籍实体 | L1 | common_type | G1/G5 | doc 典籍 |
| L1.obj | 器物实体 | L1 | common_type | G3/G6/G8 | obj 器物 |
| L1.era | 年号实体 | L1 | common_type | G0–G8 全部 | era 年号 |
| L2 | 规则与时间 | — | root | G0–G8 全部 | RUL + TIM |
| L2.RUL | 事例规则 | L2 | common_child | G0–G8 全部 | "凡..."IF-THEN |
| L2.TIM | 制度时间线 | L2 | common_child | G1/G2/G3/G4/G5/G6 | 立改罢复 |
| L3 | 结构关系 | — | root | G0–G8 全部 | 会典灵魂 |
| L3.ORG | 部门结构树 | L3 | common_child | G0/G1/G7/G8 | 部→司→事目 |
| L3.GEO | 地理管辖树 | L3 | common_child | G2/G4 | 布政司→府→卫→驿 |
| L3.RANK | 品级等级树 | L3 | common_child | G1/G3 | 品阶→章服→车舆 |
| L3.NJC | 两京对照 | L3 | common_child | G3/G7 | 北京 vs 南京异制 |
| L3.XREF | 互见索引 | L3 | common_child | G1/G2/G7 | 见某司/今归某司/已上某 |
| L4 | 六部业务域 | — | root | 按卷组启用 | 业务纵深 |
| L4.SEL | 吏部域 | L4 | business_domain | G1/G7 | 铨选/考满/封赠/吏员/丁忧/贴黄 |
| L4.SEL.XUAN | 铨选 | L4.SEL | business_sub | G1/G7 | 科举/荐举/除授 |
| L4.SEL.KAO | 考满考察 | L4.SEL | business_sub | G1/G7 | 考满/八法 |
| L4.SEL.FENG | 封赠荫叙 | L4.SEL | business_sub | G1 | 诰敕/封赠 |
| L4.SEL.LI | 吏员资格 | L4.SEL | business_sub | G1 | 攒迁/出职 |
| L4.SEL.DING | 丁忧起复 | L4.SEL | business_sub | G1/G7 | 丁忧/致仕/起复 |
| L4.SEL.HUANG | 贴黄脚色 | L4.SEL | business_sub | G1 | 履历/脚色 |
| L4.FIN | 户部域 | L4 | business_domain | G2 | 财政赋役 |
| L4.FIN.TIAN | 土田户口 | L4.FIN | business_sub | G2 | 黄册/里甲 |
| L4.FIN.SHUI | 税粮则例 | L4.FIN | business_sub | G2 | 夏税/秋粮/起运/存留 |
| L4.FIN.CAO | 漕运海运 | L4.FIN | business_sub | G2 | 漕运卫所 |
| L4.FIN.CANG | 仓庚库藏 | L4.FIN | business_sub | G2 | 仓名/粮数 |
| L4.FIN.LU | 俸禄折色 | L4.FIN | business_sub | G2 | 俸米/折钞/折银 |
| L4.FIN.TU | 土贡方物 | L4.FIN | business_sub | G2 | 土贡 |
| L4.FIN.ZA | 盐茶钱法 | L4.FIN | business_sub | G2 | 盐/茶/钱 |
| L4.RIT | 礼部域 | L4 | business_domain | G3 | 礼仪祭祀 |
| L4.RIT.CHAO | 朝仪班序 | L4.RIT | business_sub | G3 | 正旦/冬至/万寿 |
| L4.RIT.SI | 郊庙祭祀 | L4.RIT | business_sub | G3 | 大祀/中祀/小祀 |
| L4.RIT.JIA | 冠婚丧祭 | L4.RIT | business_sub | G3 | 嘉礼/凶礼 |
| L4.RIT.FU | 冠服车舆 | L4.RIT | business_sub | G3 | 与 L3.RANK 交叉 |
| L4.RIT.GONG | 朝贡互市 | L4.RIT | business_sub | G3 | 四夷/贡道/回赐 |
| L4.RIT.SENG | 僧管道录 | L4.RIT | business_sub | G3 | 度牒/寺额 |
| L4.RIT.YUE | 乐章乐器 | L4.RIT | business_sub | G3 | 乐章词+曲名 |
| L4.RIT.SHEN | 神祇地理 | L4.RIT | business_sub | G3 | 某神某府县祭 |
| L4.MIL | 兵部域 | L4 | business_domain | G4/G8 | 军政卫所 |
| L4.MIL.XUAN | 武选袭替 | L4.MIL | business_sub | G4/G8 | 武官/袭替 |
| L4.MIL.WEI | 卫所镇守 | L4.MIL | business_sub | G4/G8 | 卫所/额军 |
| L4.MIL.GUAN | 关津巡检 | L4.MIL | business_sub | G4 | 巡检司名录 |
| L4.MIL.YI | 驿传递运 | L4.MIL | business_sub | G4 | 驿名/程限 |
| L4.MIL.MA | 马政牧养 | L4.MIL | business_sub | G4 | 马额/草料 |
| L4.MIL.QI | 军器军装 | L4.MIL | business_sub | G4 | 与 L4.ENG.JUN 交叉引用（XREF） |
| L4.LAW | 刑部域 | L4 | business_domain | G5 | 刑名律例 |
| L4.LAW.LI | 明律条款 | L4.LAW | business_sub | G5 | 律条/罪名 |
| L4.LAW.WU | 五刑比例 | L4.LAW | business_sub | G5 | 笞杖徒流死 |
| L4.LAW.HUI | 会审审录 | L4.LAW | business_sub | G5 | 三法司/朝审 |
| L4.LAW.ZANG | 追赃赎罪 | L4.LAW | business_sub | G5 | 追赃/纳赎 |
| L4.LAW.TU | 土官诉讼 | L4.LAW | business_sub | G5 | 土官争端 |
| L4.ENG | 工部域 | L4 | business_domain | G6 | 营造工料 |
| L4.ENG.DIAN | 内府宫殿 | L4.ENG | business_sub | G6 | 宫殿 |
| L4.ENG.WANG | 亲王府制 | L4.ENG | business_sub | G6 | 王府/郡王府 |
| L4.ENG.LING | 陵寝坟茔 | L4.ENG | business_sub | G6 | 陵寝 |
| L4.ENG.YU | 舟车仪仗 | L4.ENG | business_sub | G6 | G8 锦衣卫仪仗经 XREF 引用本节点 |
| L4.ENG.JUN | 军器军装 | L4.ENG | business_sub | G6 | 军器（与 MIL.QI 交叉） |
| L4.ENG.LIAO | 物料工价 | L4.ENG | business_sub | G6 | 工料价 |
| L4.ENG.HE | 河渠水利 | L4.ENG | business_sub | G6 | 河渠/道路 |
| L5 | 数字与名物 | — | root | 按卷组启用 | NUM/NAM/OBJ |
| L5.NUM | 数字则例 | L5 | common_child | G2/G6 | 键值对 |
| L5.NAM | 名录 | L5 | common_child | G0/G2/G3/G4/G8 | 仓/卫/驿/器物清单 |
| L5.OBJ | 器物 | L5 | common_child | G3/G6/G8 | 尺寸/材质/数量 |
| L6 | 引用与文册 | — | root | 按卷组启用 | CIT/REPORT |
| L6.CIT | 典籍直引 | L6 | common_child | G1/G3/G5 | 祖训/大诰/明律 |
| L6.REPORT | 文册勘合 | L6 | common_child | G2 | 黄册/勘合 |

### 0.3 父子关系校验规则（由 scripts/verify_tree.py 强制）

1. **root 节点 parent 必为空**：L0–L6 七大层根不允许有父
2. **parent 必须存在**：任何节点引用的父节点必须在表内
3. **kind 与 parent 必须匹配**：
   - `common_type` 只能挂在 L1 下
   - `common_child` 只能挂在对应 root 下（RUL/TIM→L2；ORG/GEO/RANK/NJC/XREF→L3；NUM/NAM/OBJ→L5；CIT/REPORT→L6）
   - `business_domain` 只能挂在 L4 下
   - `business_sub` 只能挂在 `business_domain` 下
4. **禁止跨层挂接**：business_sub 不能挂在 common_child 下，反之亦然
5. **无环**：从任一节点沿 parent 上溯必到 root，不能成环
6. **卷组-层映射一致**：`启用卷组`列声明的卷组，必须与 `volume-map.md` 一致
7. **业务子层不越界**：SEL.XUAN 只出现在 G1/G7，FIN.* 只出现在 G2，以此类推；交叉引用（如 MIL.QI ↔ ENG.JUN）须在说明列注明
8. **新增节点必须登记**：执行期若需新子层，先在本表加行 + 走 V3 枚举校准流程，不允许代码里私自挂节点

---

## 1. ID 规则

| 前缀 | 归属层 | 段位 | 例子 |
|---|---|---|---|
| `item_id` | L0 底座 | `GG-NNN`（GG=G0–G8，NNN=组内条序） | `G1-001` |
| `ENT-` | L1 实体 | `ENT-NNN` 全局递增 | `ENT-001` |
| `RUL-` | L2 规则 | `RUL-NNN` | `RUL-001` |
| `TIM-` | L2 时间线 | `TIM-NNN` | `TIM-001` |
| `ORG-` | L3 部门 | `ORG-NNN` | `ORG-001` |
| `GEO-` | L3 地理 | `GEO-NNN` | `GEO-001` |
| `RANK-` | L3 品级 | `RANK-NNN` | `RANK-001` |
| `NJC-` | L3 两京 | `NJC-NNN` | `NJC-001` |
| `XREF-` | L3 互见 | `XREF-NNN` | `XREF-001` |
| `SEL-xxx-` | L4 吏部域 | 子层前缀+NNN | `SEL-XUAN-001` |
| `FIN-xxx-` | L4 户部域 | 同上 | `FIN-SHUI-001` |
| `RIT-xxx-` | L4 礼部域 | 同上 | `RIT-SI-001` |
| `MIL-xxx-` | L4 兵部域 | 同上 | `MIL-WEI-001` |
| `LAW-xxx-` | L4 刑部域 | 同上 | `LAW-LI-001` |
| `ENG-xxx-` | L4 工部域 | 同上 | `ENG-YU-001` |
| `NUM-` | L5 数字 | `NUM-NNN` | `NUM-001` |
| `NAM-` | L5 名录 | `NAM-NNN` | `NAM-001` |
| `OBJ-` | L5 器物 | `OBJ-NNN` | `OBJ-001` |
| `CIT-` | L6 典籍 | `CIT-NNN` | `CIT-001` |
| `REPORT-` | L6 文册 | `REPORT-NNN` | `REPORT-001` |

---

## 2. L1 实体层 schema

```json
{
  "ent_id": "ENT-001",
  "text": "吏部",
  "norm": "吏部",
  "type": "org",
  "first_source": "G1-001",
  "aliases": ["吏曹", "吏部衙门"],
  "note": ""
}
```

### 2.1 ENT_TYPE 枚举（基线）

| 值 | 说明 | 例子 |
|---|---|---|
| `org` | 衙门 | 宗人府/吏部/文选清吏司/都察院/锦衣卫/太仓银库/杭卅卫 |
| `off` | 官职 | 尚书/侍郎/郎中/员外郎/总督/巡抚/巡按御史/百户/大使 |
| `geo` | 地名 | 浙江布政司/杭州府/海宁县/金山卫/海宁驿/苏州府 |
| `doc` | 典籍 | 皇明祖训/大诰/大明令/诸司职掌/明集礼/洪武礼制/稽古定制 |
| `obj` | 器物 | 大辂/玉辂/黄麾/绛引旛/品级伞/印信/勘合 |
| `era` | 年号 | 吴元年/洪武/永乐/洪熙/宣德/正统/景泰/天顺/成化/弘治 |
| `type_pending` | 兜底 | 未归类暂存，V3 决议 |

**⚠ 待补候选**（探针中见到但未列）：
- `rite` 仪式名（正旦朝贺/万寿圣节/郊祀/太庙时享）
- `charge` 罪名/法条名（斗殴/骂詈/越诉/贼盗）
- `subject` 科目名（进士/举人/监生/岁贡/荐举）
- `tribe` 朝贡国（朝鲜/安南/琉球/哈密）
- `deity` 神祇名（北极真武/天妃/文昌/关帝）
- `rank_title` 封爵（公/侯/伯/世子/将军）

**执行期见一个收一个，不自行开放枚举。**

---

## 3. L2 规则层 schema

### 3.1 RUL 事例条

```json
{
  "rule_id": "RUL-001",
  "item_id": "G1-001",
  "type": "义务",
  "modality": "凡",
  "source_marker": "凡",
  "era": "洪武二十六年",
  "condition": "内外官员考满侍亲丁忧",
  "subject": "吏部",
  "subject_ent_ids": ["ENT-吏部"],
  "action": "付案呈本部立案作缺",
  "object": "选簿",
  "punishment": "",
  "original": "凡内外官员考满侍亲致仕丁忧残疾极刑考功司勋来付案呈本部立案作缺..."
}
```

### 3.2 RUL_TYPE 枚举（基线）

| 值 | 说明 |
|---|---|
| `禁止` | 不许/毋/勿/禁 |
| `义务` | 凡/须/务要/俱 |
| `允许` | 听/许/如旧 |
| `程序` | 步骤/流程 |
| `时限` | 限X日/每月/每年 |
| `处罚` | 笞/杖/徒/流/充军/为民/治罪 |
| `优先级` | 从旧/从重/从轻 |

**⚠ 待补候选**：`折算`（折色/折钞/折银）、`俸禄`（月支/折支）、`名额`（额设X员）。

### 3.3 SOURCE_MARKER 文体标记枚举（凡例自陈）

| 值 | 说明 |
|---|---|
| `诏` | 皇帝主动下诏 |
| `敕` | 皇帝敕谕 |
| `奏准` | 臣下奏事，皇帝批准 |
| `议准` | 廷议后批准 |
| `奏定` | 臣下定规则 |
| `议定` | 廷议定规则 |
| `令` | 总书"令" |
| `凡` | 常行无所考据，以凡字别之 |

**⚠ 待补候选**：`敕谕`（长篇训话）、`榜谕`、`条约`、`例`、`则例`。

### 3.4 MODALITY 模态词表（触发词典）

`不许 / 毋 / 勿 / 务要 / 须 / 止许 / 俱 / 照例 / 违者 / 治罪 / 听 / 许 / 限 / 照例 / 不许`

---

## 4. L3 结构关系层 schema

### 4.1 ORG 部门结构

```json
{
  "org_id": "ORG-001",
  "name": "吏部",
  "parent_org": "",
  "children_orgs": ["文选清吏司", "验封清吏司", "稽勋清吏司", "考功清吏司"],
  "rank": "正二品",
  "establishment": "洪武元年始置",
  "history": ["洪武元年置", "洪武十三年升正二品", "永乐北京置行在吏部"],
  "nanjing_version": "南京吏部（后加南京二字）",
  "original": "国初因前代之制置中书省...洪武十三年革...",
  "item_id": "G1-001"
}
```

### 4.2 GEO 地理管辖

```json
{
  "geo_id": "GEO-001",
  "name": "浙江布政司",
  "type": "布政司",
  "parent": "",
  "children": ["杭州府", "绍兴府", "宁波府", ...],
  "administered_by": "户部/兵部",
  "garrisons": ["杭州前卫", "杭州右卫", ...],
  "post_stations": [...],
  "granaries": [...],
  "original": "浙江布政使司...",
  "item_id": "G2-001"
}
```

**GEO_TYPE 枚举**：`布政司 / 府 / 州 / 县 / 都司 / 卫 / 所 / 驿 / 巡检司 / 仓 / 关 / 镇`
**⚠ 待补**：`土官宣慰司/宣抚司/安抚司/长官司`、`盐运司`、`苑马寺`。

### 4.3 RANK 品级等级

```json
{
  "rank_id": "RANK-001",
  "level": "一品",
  "category": "文职",
  "housing": "正堂七间九架",
  "clothing": "仙鹤补子",
  "carriage": "其间金妆饰银螭绣带青幔",
  "umbrella": "银浮屠顶茶褐罗表红绢里三檐",
  "tableware": "酒注酒盏用金",
  "original": "公侯一品二品酒注酒盏用金余用银...",
  "item_id": "G3-xxx"
}
```

**RANK_LEVEL 枚举**：`公 / 侯 / 伯 / 一品 / 二品 / 三品 / 四品 / 五品 / 六品 / 七品 / 八品 / 九品 / 未入流 / 庶民`
**⚠ 待补**：`世子 / 郡王子 / 将军 / 中尉`（宗室品级）、`命妇`（母妻品级）。

### 4.4 NJC 两京对照

```json
{
  "njc_id": "NJC-001",
  "beijing_item": "G1-xxx",
  "nanjing_item": "G1-yyy",
  "topic": "吏部建置",
  "difference": "永乐迁都后北京称行在吏部，南京加南京二字",
  "original": "..."
}
```

### 4.5 XREF 互见

```json
{
  "xref_id": "XREF-001",
  "from_item": "G1-xxx",
  "from_layer": "SEL-DING",
  "ref_type": "见某司 / 今归某司 / 已上某分组",
  "target_org": "考功司",
  "note": "丁忧起复旧制本司掌行后归考功",
  "original": "旧制官员致仕隶本司掌行后归考功司"
}
```

---

## 5. L4 六部业务域 schema（子层字段）

### 5.1 SEL 吏部域

| 子层 | 关键字段 |
|---|---|
| SEL-XUAN 铨选 | source_pool(进士/举人/监生/吏员) / target_office / route(除授/升调/改降) / age / special(特简/推升) |
| SEL-KAO 考满考察 | kao_man_term(三年/六年/九年) / grade(称职/平常/不称职) / eight_method(贪/酷/浮/躁/老/病/罢/不谨) |
| SEL-FENG 封赠 | recipient / level(诰命/敕命) / generation(本身/父母/祖父母/妻) |
| SEL-LI 吏员资格 | entry(学生/民人/罚充) / rank(通吏/令史/典吏/掾史) / promotion_term(三年/六年/九年) |
| SEL-DING 丁忧起复 | parent / mourning_months(27月) / back_office / qi_fu(起复/夺情) |
| SEL-HUANG 贴黄 | person / career_history / birthplace / clan |

### 5.2 FIN 户部域

| 子层 | 关键字段 |
|---|---|
| FIN-TIAN 土田户口 | huangce(黄册) / lijia(110户里长十户) / grade(上中下) |
| FIN-SHUI 税粮 | summer_wheat / autumn_rice / qiyun(起运) / cunliu(存留) / zhe_se(折色) / rate |
| FIN-CAO 漕运 | wei(运粮卫) / route / shi(石) |
| FIN-CANG 仓庚 | granary_name / location / storage_shi |
| FIN-LU 俸禄 | office / rank / monthly_shi / zhe_chao(折钞) / zhe_yin(折银) |
| FIN-TU 土贡 | item / origin / amount |
| FIN-ZA 盐茶钱法 | salt_department / tea_department / coinage |

### 5.3 RIT 礼部域

| 子层 | 关键字段 |
|---|---|
| RIT-CHAO 朝仪 | event(正旦/冬至/万寿/中宫千秋) / order / music |
| RIT-SI 郊庙祭祀 | level(大祀/中祀/小祀) / altar / season / victim(太牢/少牢/素) |
| RIT-JIA 冠婚丧祭 | ceremony_type(冠/婚/丧/祭) / subject(天子/太子/品官/庶人) |
| RIT-FU 冠服车舆 | subject_rank / garment / carriage |
| RIT-GONG 朝贡 | country / tribute / frequency / route / return_gift |
| RIT-SENG 僧道 | temple / degree_diploma(度牒) / monk_official |
| RIT-YUE 乐章 | event / tune_name(圣安之曲/治安之曲) / instruments / lyrics_ref |
| RIT-SHEN 神祇地理 | deity / location / sacrifice_day / offering_official |

### 5.4 MIL 兵部域

| 子层 | 关键字段 |
|---|---|
| MIL-XUAN 武选 | hereditary(袭替) / rank(都督/都指挥/指挥/千百户) |
| MIL-WEI 卫所 | wei_name / garrison_location / troop_strength |
| MIL-GUAN 关津巡检 | xunjian_si / county / responsibility(缉捕/盘诘) |
| MIL-YI 驿传 | station_name / route / distance / horses |
| MIL-MA 马政 | pasture / horse_count / fodder(料豆/草) |
| MIL-QI 军器 | weapon / quantity / workshop |

### 5.5 LAW 刑部域

| 子层 | 关键字段 |
|---|---|
| LAW-LI 明律 | clause_name / law_text / severity |
| LAW-WU 五刑 | 笞/杖/徒/流/死 / 充军 / 为民 / 凌迟 |
| LAW-HUI 会审 | event(朝审/热审/大审) / participants(三法司/锦衣卫/科道) |
| LAW-ZANG 追赃 | amount / return / redemption |
| LAW-TU 土官诉讼 | tribe / dispute_type |

### 5.6 ENG 工部域

| 子层 | 关键字段 |
|---|---|
| ENG-DIAN 内府宫殿 | building / dimensions / material |
| ENG-WANG 亲王府制 | prince_rank / hall / gate / dimensions |
| ENG-LING 陵寝 | emperor / location / dimensions |
| ENG-YU 舟车仪仗 | object / height / material / color / count |
| ENG-JUN 军器 | weapon / workshop / annual_output |
| ENG-LIAO 物料工价 | material / unit_price(银X两) / quantity |
| ENG-HE 河渠水利 | river / weir / repair |

**⚠ 所有 L4 子层字段都是基线。执行期若发现新业务字段（如礼部"谥法"有谥字表里、户部"盐引"有引目编号），收集后决议。**

---

## 6. L5 数字与名物 schema

### 6.1 NUM 数字则例

```json
{
  "num_id": "NUM-001",
  "item_id": "G2-001",
  "topic": "浙江夏税",
  "key_value_pairs": [
    {"key": "夏税京库折银麦", "value": "80000石", "rate": "每石折银2钱5分"},
    {"key": "丝绵", "value": "320000两", "rate": "每20两折绢1疋"}
  ],
  "era": "弘治十五年",
  "original": "浙江布政使司 夏税京库折银麦八万石每石折银二钱五分..."
}
```

### 6.2 NAM 名录

```json
{
  "nam_id": "NAM-001",
  "item_id": "G2-040",
  "name": "浙江布政司仓名名录",
  "category": "仓",
  "region": "浙江布政司",
  "entries": [
    {"admin": "杭州府", "places": ["广丰仓", "广积仓"]},
    {"admin": "海宁县", "places": ["永平仓"]}
  ],
  "original": "杭州府 广丰仓 广积仓 海宁县 永平仓..."
}
```

**NAM_CATEGORY 枚举**：`仓 / 卫 / 所 / 驿 / 巡检司 / 府县 / 仪仗器物 / 诸王命名谱系 / 祀庙`
**⚠ 待补**：`铁券 / 印信 / 符牌 / 节`.

### 6.3 OBJ 器物

```json
{
  "obj_id": "OBJ-001",
  "item_id": "G6-150",
  "name": "大辂",
  "category": "仪仗",
  "dimensions": "高一丈一尺三寸四分",
  "material": "硃红漆抹金铜",
  "color": "黄绮销金云凤文",
  "quantity": "一乘",
  "original": "辂一乘 高一丈一尺三寸四分..."
}
```

---

## 7. L6 引用与文册 schema

### 7.1 CIT 典籍直引

```json
{
  "cit_id": "CIT-001",
  "item_id": "G1-001",
  "source_book": "皇明祖训",
  "chapter": "",
  "citation_type": "直引",
  "context": "吏部建置沿革",
  "text": "自古三公论道六卿分职并不曾设立丞相...",
  "original": "皇明祖训 一自古三公论道..."
}
```

**CIT_SOURCE_BOOK 枚举**（凡例列的十二书）：
`皇明祖训 / 大诰 / 大明令 / 诸司职掌 / 明集礼 / 洪武礼制 / 礼仪定式 / 稽古定制 / 孝慈录 / 教民榜文 / 大明律 / 军法定律 / 宪纲`

### 7.2 REPORT 文册勘合

```json
{
  "report_id": "REPORT-001",
  "item_id": "G2-001",
  "doc_type": "黄册",
  "frequency": "十年大造",
  "deadline": "年终到部",
  "office_responsible": "布政司/府/州/县",
  "format": "一百一十户为里...",
  "original": "洪武十四年诏天下府州县编赋役黄册..."
}
```

---

## 8. 示例条目（试点 3 条真实文本）

### 示例 1：卷二吏部文选司"凡进士第一甲除翰林院修撰"

```json
{
  "item_id": "G1-014",
  "rul": {
    "rule_id": "RUL-014",
    "type": "义务",
    "modality": "凡",
    "source_marker": "凡",
    "era": "洪武间",
    "subject": "吏部",
    "action": "除授",
    "object": "进士第一甲",
    "detail": "第一甲第一名除翰林院修撰，第二名第三名除编修，其余分送各衙门办事"
  },
  "sel_xuan": {
    "source_pool": "进士",
    "target_office": "翰林院修撰/编修",
    "route": "除授"
  },
  "ents": [
    {"text": "翰林院", "type": "org"},
    {"text": "修撰", "type": "off"},
    {"text": "编修", "type": "off"}
  ]
}
```

### 示例 2：卷二十三户部"浙江夏税"

```json
{
  "item_id": "G2-023",
  "num": {
    "num_id": "NUM-023",
    "topic": "弘治十五年浙江夏税",
    "key_value_pairs": [
      {"key": "京库折银麦", "value": "80000石", "rate": "每石折银2钱5分"},
      {"key": "丝绵", "value": "320000两", "rate": "每20两折绢196000疋"}
    ]
  },
  "geo": {"name": "浙江布政司", "type": "布政司"}
}
```

### 示例 3：卷一百八十锦衣卫"凡圣节正旦冬至大朝会"

```json
{
  "item_id": "G8-180",
  "rul": {
    "rule_id": "RUL-180",
    "type": "义务",
    "modality": "凡",
    "source_marker": "凡",
    "era": "洪武永乐间",
    "subject": "锦衣卫",
    "action": "提督所属官校依次陈列卤簿仪仗",
    "condition": "圣节正旦冬至大朝会郊祀等项车驾出入"
  },
  "org": {"name": "锦衣卫", "parent": "五军都督府", "note": "职掌异于诸卫"},
  "rit_chao": {"event": "大朝会", "participant": "锦衣卫"}
}
```

### 示例 4：卷四十二礼部"正旦冬至朝贺仪"（流程层 + 乐章层）

```json
{
  "item_id": "G3-042",
  "prc": {
    "process_id": "PRC-CHAO-001",
    "name": "正旦冬至朝贺仪",
    "steps": [
      {"seq": 1, "text": "前一日尚宝司陈设御座于奉天殿", "agent": "尚宝司"},
      {"seq": 2, "text": "锦衣卫陈卤簿仪仗于丹陛丹墀", "agent": "锦衣卫"},
      {"seq": 3, "text": "鼓初严，文武官具朝服齐班于午门外", "agent": "教坊司/文武官"},
      {"seq": 4, "text": "皇帝衮冕升座，钟鸣，中和韶乐奏圣安之曲", "agent": "皇帝/教坊司"},
      {"seq": 5, "text": "赞四拜，宣表，山呼万岁", "agent": "仪礼司"}
    ]
  },
  "rit_chao": {
    "event": "正旦冬至朝贺",
    "music": ["圣安之曲", "治安之曲", "万岁乐", "朝天子", "定安之曲"]
  },
  "rit_yue": {
    "tune_name": "圣安之曲",
    "instruments": ["麾", "箫", "笙", "编钟", "编磬", "应鼓", "柷", "敔"]
  }
}
```

### 示例 5：卷一百三十一刑部"斗殴"律条（LAW 子层 + CIT）

```json
{
  "item_id": "G5-131",
  "cit": {
    "cit_id": "CIT-131",
    "source_book": "大明律",
    "citation_type": "直引",
    "context": "刑律·斗殴"
  },
  "law_li": {
    "clause_name": "斗殴",
    "law_text": "凡斗殴以手足殴人不成伤者笞二十，成伤及以他物殴人不成伤者笞三十，成伤者笞四十...",
    "severity_ladder": [
      {"circumstance": "手足殴人不成伤", "punishment": "笞二十"},
      {"circumstance": "他物殴人成伤", "punishment": "笞四十"},
      {"circumstance": "折人一齿一指", "punishment": "杖一百"},
      {"circumstance": "折人肢体瞎人一目", "punishment": "杖一百徒三年"},
      {"circumstance": "杀人", "punishment": "绞/斩"}
    ]
  },
  "law_wu": {"five_punishments_used": ["笞", "杖", "徒", "流", "死"]}
}
```

---

## 9. 待办（执行期持续补）

- [ ] 每完成一个大卷组，输出 `_pending_enums.csv` 决议报告
- [ ] 礼部 G3（64卷）跑完后，回头补 RIT 子层可能缺的分支
- [ ] 两京对照 NJC 条目数目标 ≥30（凡例明言异者别出）
- [ ] OCR 错字归一表累积：目前仅"防→会/御"，执行期补
