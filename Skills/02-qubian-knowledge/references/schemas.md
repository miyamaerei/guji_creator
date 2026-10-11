# 《蘧编》实例 Schema（启用层）

> 本文件只含启用层的具体 schema、ID 规则、触发词、枚举与
>
> **示例条目**
>
> 。未启用层（L2/L3/L4/REG/V1）无任何残留。
> 枚举规范值快照见 
>
> `enums.md`
>
> （基准库继承 + 本书增量）；翻译风格见 
>
> `translation-style.md`
>
> 。

## 0. 底座与 ID 规则

### 0.1 条目



* 输入：`蘧编_结构化.json`（章→节→段）。

* 章号：00 = 序 + 前言（2 条）；01–20 = 卷一～卷二十（71 条）；21 = 后记一 + 后记二（2 条）；22 = 附录校记（1 条）。共 **76 条**。

* item\_id = `NN-NNN`（卷 - 序）：01-001..20-001（入层 71 条）；00-001/00-002/21-001/21-002/22-001（不入层）。

* 入层规则：卷 01–20 全部条目入 8 层；卷 00/21/22 只入指纹库（layer\_count=0，无 TRL）。

### 0.2 业务 ID 段位（打包器自动分配，AI 不手写）



* 各层业务 ID 前缀：ENT- / APPT- / EVT- / REL- / LIT- / TRL- / MEM- / CHR-（命名空间全局唯一，只属本层）。

* 段位：`卷号 × 100 + 卷内顺序`（卷 01→101..，卷 20→2001..；容量 100 / 卷）。试点卷 01 用 1–99 预留。

* 源数据只写 "槽位"（卷内顺序），打包器按段位自动编 ID；validate 按层全局判重兜底。

### 0.3 源数据与注入



* AI 源数据只写条号 + 解读（不手抄原文）；打包器从 `_item_registry.json` 注入 original/norm。

* 记录必带 `volume` 字段与 `item_id`；各层单卷 JSON 顶层键统一 `records`。

## 1. 实体层（L1）

### schema



```
{
  "id": "ENT-xxx",            // 打包器分配（归一后主键）
  "text": "太夫人林氏",        // 原文词形
  "type": "person",            // 枚举见 enums.md 1.1
  "start": 0, "end": 5,        // 原文偏移
  "normalized": "林氏（叶向高母）", // 全局归一主形
  "confidence": 0.9,
  "source": "01-001",          // 卷-条号（provenance）
  "first_source": "01-001"     // 新建实体首次出现处
}
```



* 每卷标注 JSON → 全局归一（normalized\_inventory）→ 主键表（ENT-xxx + alias\_index：词形→ent\_id；复合解读词形手工映射，不动标注）。

* 同名异人：跨卷同名自动入 `data\ent\同名异人待核清单.csv`（V2），人工核前不合并。

### 高频实体子集（本书实测，执行期按 V3 校准）

person（家人：太夫人林氏 / 郭夫人 / 康夫人 / 先少师公 / 庶母林氏 / 夫人俞氏 / 弟亮永亨 / 子学 / 孙益蕃益荪；皇帝：明神宗 / 光宗 / 熹宗 / 思宗；同官：朱国祚 / 李廷机 / 韩爌 / 何如宠 / 沈鲤 / 于慎行；言官：杨涟 / 左光斗 / 魏大中 / 曹守勲 / 邓澄；宦官：魏忠贤 / 王安 / 陈矩 / 史宾；门生：文震孟 / 周顺昌 / 张纳 / 王三善）/official（督学 / 邑令 / 首辅 / 吏部尚书 / 南京太宰 / 九江别驾 / 给谏 / 大司徒 / 巡抚 / 总督 / 经略 / 太傅 / 上柱国 / 尚宝司丞 / 中书舍人）/institution（内阁 / 吏部 / 户部 / 工部 / 礼部 / 都察院 / 六科 / 锦衣卫 / 镇抚司 / 鸿胪寺 / 翰林院）/place（京师 / 留都 / 福清 / 镇东卫 / 龙江桥 / 三山 / 省城 / 吉水 / 山阴 / 东阿 / 武定府 / 大方）/era（嘉靖 / 隆庆 / 万历 / 泰昌 / 天启 / 崇祯）/work（《神惠记》《光庙实录》《苍霞草》婚牍）/posthumous（文忠 / 文懿 / 文肃）/unknown 兜底。

## 2. 职官任职层（C1 APPT）

### schema



```
{
  "appointment_id": "APPT-xxx",
  "item_id": "02-001",
  "person": "曾公（曾同亨）",  "person_ent_ids": ["ENT-xxx"],
  "office": "南京太宰",       "official_ent_ids": ["ENT-xxx"],
  "institution": "南京吏部",   "institution_ent_ids": ["ENT-xxx"],
  "when": "万历三十一年",      // 年号纪年；未明写"未明"
  "status": "现任",            // 枚举 enums.md 1.10
  "evidence": "起家为南太宰，屡使人邀余，余遂赴任",
  "original": "（打包器注入）"
}
```



* 触发词（规则引擎候选）：受业于 / 为 / 任 / 授 / 擢 / 迁 / 改 / 除 / 罢 / 谪 / 致仕 / 兼 / 领 / 督 / 巡抚 / 提督 / 考满 / 会推 / 入阁 / 升 / 降 / 起复 / 赠 / 荫 / 廷推 / 点用 / 推补。

* 一条目多任职拆多条共享 item\_id；追赠 / 荫子按追赠 / 举荐状态登记。

## 3. 事件层（L5 EVT）

### schema



```
{
  "event_id": "EVT-xxx",
  "item_id": "01-001",
  "type": "军事",              // 枚举 enums.md 1.3（22 顶层，只继承顶层）
  "who": "倭寇", "who_ent_ids": [],
  "action": "入寇闽地",
  "what": "倭乱闽已数载，太夫人避倭至外家分娩",
  "when": "嘉靖三十八年（1559）前数载",
  "where": "闽地", "where_ent_ids": []
}
```



* 事件类型继承基准库事件类型子库（`../00-book-knowledge-factory/references/enum-library.md` §1.3）顶层；本书为史书 → 不引入行政过程子类型。

* 未匹配值 → pending 收集 → 决议 → registerVersion+1 回溯（V3）。

* 与 MEM/CHR 分工：EVT = 事件本体；MEM = 君臣互动链；CHR = 年条总览。

## 4. 人物关系层（C3 REL）

### schema



```
{
  "rel_id": "REL-xxx",
  "item_id": "01-001",
  "person_a": "叶向高", "person_a_ent_ids": ["ENT-xxx"],
  "person_b": "太夫人林氏", "person_b_ent_ids": ["ENT-xxx"],
  "relation_type": "父子亲属",  // 枚举 enums.md 1.4
  "direction": "双向",
  "evidence": "太夫人林氏……余（生）时",
  "original": "（打包器注入）"
}
```



* 触发词：座师 / 门人 / 同年 / 同官 / 姻 / 亲 / 同乡 / 同里 / 故交 / 弟子 / 门生 / 师生。

* **宁缺毋滥**：只建有直接证据的关系；叶向高（"余"）为枢纽。

## 5. 文献资产层（C2 LIT）

### schema



```
{
  "lit_id": "LIT-xxx",
  "item_id": "15-001",
  "title": "上传谕内阁（论内操）",   // 无题取首句
  "author": "明熹宗", "author_ent_ids": ["ENT-xxx"],  // 佚名"未明"
  "type": "诏敕圣旨",              // 枚举 enums.md 1.11
  "content_location": "卷十五 15-001 第3段",
  "original": "（打包器注入）"
}
```



* 触发信号：整篇抄录谕旨 / 奏疏 / 婚牍 / 祭文 / 序文。

* 与 MEM 分工：LIT 收完整文献文本；MEM 收互动链；仅转述不抄全文归 MEM。

## 6. 古今翻译层（C5 TRL）

### schema



```
{
  "trl_id": "TRL-xxx",
  "item_id": "01-001",
  "translation": "……（现代汉语译文）",
  "style": "注释性翻译",           // 枚举 enums.md 1.13
  "note": "乳名'厕'缘于生于败厕颓垣旁",
  "confidence": 0.9,
  "original": "（打包器注入）"
}
```



* 全量 71 条（卷 01–20）逐条翻译；代码只验覆盖（条目数 = 翻译数）。

* 风格基准：余光中七条（见 `translation-style.md`）；专名保留 + 括注。

## 7. 奏疏谕旨互动层（自定义 MEM）

### schema



```
{
  "mem_id": "MEM-xxx",
  "item_id": "15-001",
  "actor": "叶向高", "actor_ent_ids": ["ENT-xxx"],
  "target": "明熹宗", "target_ent_ids": ["ENT-xxx"],
  "type": "具揭",                 // 枚举 enums.md 1.15
  "issue": "细民王德等阑入禁地称冤，枷号将毙，请宽宥",
  "response": "得旨：着锦衣卫打四十棍释放，以后决不轻宥",
  "result": "改拟",               // 枚举 enums.md 1.16
  "original": "（打包器注入）"
}
```



* 触发词（规则引擎候选）：臣方 —— 疏辞 / 再疏 / 三疏 / 具疏 / 具揭 / 疏请 / 条陈 / 乞休 / 乞罢 / 求去 / 引罪；君方 —— 得旨 / 奉旨 / 奉圣旨 / 上传 / 上谕 / 圣谕 / 传谕 / 批出 / 留中 / 不报 / 允 / 不允。

* 一条 MEM = 一次往来；一条目多往来拆多条共享 item\_id；皇帝主动下发（非回应）也登记（actor 为皇帝）。

## 8. 年谱纪年索引层（自定义 CHR）

### schema



```
{
  "chr_id": "CHR-xxx",
  "item_id": "01-001",
  "era": "嘉靖三十八年己未",
  "year": 1559,                  // 公元；未明"未明"
  "age": 0,                      // "余X岁"；未明"未明"
  "category": "幼年行迹",          // 枚举 enums.md 1.17
  "summary": "叶向高生于倭乱避难困厄之中，乳名'厕'，赖母与庶母护持得全",
  "ref_events": ["EVT-xxx"],
  "ref_appts": [],
  "first_person": true,
  "original": "（打包器注入）"
}
```



* 71 个年条各 1 条 CHR（与节一一对应）；summary 只写要点不抄原文；ref\_events/ref\_appts 在 EVT/APPT 完成后回填。

## 9. 示例条目（试点校验，2026-10-10 试跑通过）

> 试点条目：01-001（幼年倭乱）/ 02-001（朝政）/ 15-001（再入阁）/ 20-001（病逝）。判定 → 注入 → 校验通过，无字段 / 枚举 / ID 硬伤。

### 9.1 01-001 嘉靖三十八年己未（1559 年），七月三十日，亥时，余生。

**ent（节选）**



```
{"id":"ENT-001","text":"太夫人林氏","type":"person","start":0,"end":5,"normalized":"林氏（叶向高母）","confidence":0.9,"source":"01-001","first_source":"01-001"}
{"id":"ENT-002","text":"先少师公","type":"person","start":140,"end":145,"normalized":"叶朝荣（叶向高父）","confidence":0.85,"source":"01-001","first_source":"01-001"}
{"id":"ENT-003","text":"嘉靖","type":"era","normalized":"嘉靖","confidence":1.0,"source":"01-001","first_source":"01-001"}
```

**evt**



```
{"event_id":"EVT-001","item_id":"01-001","type":"军事","who":"倭寇","who_ent_ids":[],"action":"入寇闽地","what":"倭乱闽已数载，太夫人避倭至外家分娩，颠沛流离","when":"嘉靖三十八年（1559）前数载","where":"闽地","where_ent_ids":[]}
{"event_id":"EVT-002","item_id":"01-001","type":"轶事","who":"叶向高","who_ent_ids":["ENT-001"],"action":"生于败厕颓垣","what":"太夫人于野厕颓垣旁分娩，故乳名'厕'","when":"嘉靖三十八年七月三十日亥时","where":"化北里外家","where_ent_ids":[]}
```

**rel**



```
{"rel_id":"REL-001","item_id":"01-001","person_a":"叶向高","person_a_ent_ids":["ENT-001"],"person_b":"太夫人林氏","person_b_ent_ids":["ENT-001"],"relation_type":"父子亲属","direction":"双向","evidence":"太夫人林氏，化北里上井村林公寿女……余（生）时"}
{"rel_id":"REL-002","item_id":"01-001","person_a":"叶向高","person_a_ent_ids":[],"person_b":"先少师公","person_b_ent_ids":["ENT-002"],"relation_type":"父子亲属","direction":"双向","evidence":"越日，先少师公乃知，自担鸡酒往问"}
```

**chr**



```
{"chr_id":"CHR-001","item_id":"01-001","era":"嘉靖三十八年己未","year":1559,"age":0,"category":"幼年行迹","summary":"叶向高生于倭乱避难困厄之中，乳名'厕'，赖母与庶母护持得全","ref_events":["EVT-001","EVT-002"],"ref_appts":[],"first_person":true}
```

**trl（注释性翻译节选）**



```
{"trl_id":"TRL-001","item_id":"01-001","translation":"我的生母太夫人林氏，是化北里上井村林公寿的女儿；在我之前，父亲已有两位夫人。……我出生那会儿，倭寇侵扰福建已好几年。太夫人临产，恰好避倭躲回娘家，族人因风俗忌讳不高兴，太夫人明白他们的意思，便离开住处，野外有座废弃的茅厕和颓塌的土墙，就倚着那里生下了我，因此给我取乳名叫'厕'。","style":"注释性翻译","note":"乳名'厕'缘于生于败厕颓垣旁；'余前有二母'指父亲先有郭、康两位夫人","confidence":0.9}
```

### 9.2 02-001 万历三十一年癸卯（1603 年），余四十五岁。

**appt**



```
{"appointment_id":"APPT-001","item_id":"02-001","person":"曾公（曾同亨）","person_ent_ids":[],"office":"南京太宰","official_ent_ids":[],"institution":"南京吏部","institution_ent_ids":[],"when":"万历三十一年","status":"现任","evidence":"吉水见台曾公，起家为南太宰"}
{"appointment_id":"APPT-002","item_id":"02-001","person":"叶向高","person_ent_ids":[],"office":"（留都署部）","official_ent_ids":[],"institution":"南京","institution_ent_ids":[],"when":"万历三十一年","status":"现任","evidence":"余复署户、礼二部"}
```

**evt**



```
{"event_id":"EVT-003","item_id":"02-001","type":"司法","who":"楚宗人","who_ent_ids":[],"action":"讦其王非前王子","what":"楚藩事：楚宗人讦王，四明沈公护王，妖书事起，大索长安","when":"万历三十一年","where":"楚/京师"}
```

**mem**



```
{"mem_id":"MEM-001","item_id":"02-001","actor":"叶向高","actor_ent_ids":[],"target":"明神宗","target_ent_ids":[],"type":"具揭","issue":"两部（户部/工部）争神帛费用，请量费而缩","response":"祝给事裁去万余金，事乃息","result":"允准"}
```

**chr**



```
{"chr_id":"CHR-002","item_id":"02-001","era":"万历三十一年癸卯","year":1603,"age":45,"category":"宦途任职","summary":"赴南京任职，署户礼二部；历经楚藩案与妖书案，京师罢市、株连惨酷","ref_events":["EVT-003"],"ref_appts":["APPT-001","APPT-002"],"first_person":true}
```

### 9.3 15-001 天启三年癸亥（1623 年），余六十五岁。

**evt**



```
{"event_id":"EVT-004","item_id":"15-001","type":"人事任免","who":"钟羽正","who_ent_ids":[],"action":"求去","what":"工部尚书钟羽正为中官所辱求去，余拟旨慰留，竟予告去","when":"天启三年六月五日","where":"京师"}
{"event_id":"EVT-005","item_id":"15-001","type":"军政","who":"明熹宗","who_ent_ids":[],"action":"训练内操","what":"辽阳陷没后择中官三千人日夕训练，铳炮之声彻于远近，余谏不听","when":"天启三年","where":"京师"}
```

**lit**



```
{"lit_id":"LIT-001","item_id":"15-001","title":"上传谕内阁（论内操）","author":"明熹宗","author_ent_ids":[],"type":"诏敕圣旨","content_location":"卷十五 15-001 第3段","original":"（注入）朕览章疏，内有南京御史刘之凤奏罢内操。……"}
```

**mem**



```
{"mem_id":"MEM-002","item_id":"15-001","actor":"叶向高","actor_ent_ids":[],"target":"明熹宗","target_ent_ids":[],"type":"具揭","issue":"王德等细民阑入禁地称冤，枷号将毙，请宽宥","response":"得旨：着锦衣卫打四十棍释放，以后决不轻宥","result":"改拟"}
{"mem_id":"MEM-003","item_id":"15-001","actor":"王三善","actor_ent_ids":[],"target":"明熹宗","target_ent_ids":[],"type":"上疏","issue":"贵州巡抚王三善与总督不合，疏请径归","response":"余拟旨切责，得旨照旧供职，如已出省城即行重处","result":"不准"}
```

**chr**



```
{"chr_id":"CHR-003","item_id":"15-001","era":"天启三年癸亥","year":1623,"age":65,"category":"朝政事务","summary":"再入阁主持政务：钟羽正求去、内操之争、王三善请归诸事，屡疏乞休皆蒙慰留","ref_events":["EVT-004","EVT-005"],"ref_appts":[],"first_person":true}
```

### 9.4 20-001 天启七年丁卯（1627 年），余六十九岁。（卷二十，孙叶益荪续写）

**evt**



```
{"event_id":"EVT-006","item_id":"20-001","type":"文事","who":"叶向高","who_ent_ids":[],"action":"改觉是堂为祠","what":"改觉是堂为祠，移奉父、前母及母四主入祀，以贞烈姐、长卿弟附焉","when":"天启七年六月十六日","where":"福清"}
{"event_id":"EVT-007","item_id":"20-001","type":"其他","who":"叶向高","who_ent_ids":[],"action":"病逝","what":"病革，诵陶靖节'应尽便须尽，无复独多虑'，八月二十九日卯时不起","when":"天启七年八月二十九日","where":"福清"}
```

**rel**



```
{"rel_id":"REL-003","item_id":"20-001","person_a":"叶益荪","person_a_ent_ids":[],"person_b":"叶向高","person_b_ent_ids":[],"relation_type":"父子亲属","direction":"单向","evidence":"不孝孙益荪……为先臣受恩独重，度陈遗嘱沥谢"}
```

**chr**



```
{"chr_id":"CHR-004","item_id":"20-001","era":"天启七年丁卯","year":1627,"age":69,"category":"病逝后事","summary":"叶向高病逝，孙益荪续记临终与身后恩典（祭葬赠荫、谥文忠）；本卷为孙续写","ref_events":["EVT-006","EVT-007"],"ref_appts":[],"first_person":true}
```

> 试点结论：4 条覆盖幼年 / 朝政 / 再入阁 / 病逝四种年条形态，schema 字段、枚举值（MEM_TYPES/MEM_RESULTS/CHR_CATEGORIES）、ID 段位均无硬伤；示例记录即按此形态固化执行。