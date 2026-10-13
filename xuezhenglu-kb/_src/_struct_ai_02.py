# -*- coding: utf-8 -*-
"""《政学录》卷二 结构化层源数据（四维 ACT/FRD/LGR/TME，AI 逐条判定，2026-10-12）。
纪律：dim 必填 + 维度类型字段必填且命中枚举；target 用 ID 引用（暂可空）；evidence 写要点不抄长文。"""

RECORDS = [
    # ---- 02-001 直隶 ----
    {"item_id": "02-001", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "兵备道控御职责：特设道臣驻札获鹿县控御西面崇山峻岭不法之徒"},
    {"item_id": "02-001", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "阜平县议复：张官置吏度地建城用资弹压，稽查保甲/输纳钱粮/控诉事宜"},
    {"item_id": "02-001", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "辽东不隶山东有深意：登莱布运海道两便，后因夹带私货禁止海船遂废"},
    # ---- 02-002 江南 ----
    {"item_id": "02-002", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "苏松重赋积弊：压欠新旧带征催呼日迫民力日疲逋负侵那杂出"},
    {"item_id": "02-002", "dim": "LGR", "lgr_type": "ledger",
     "target": "", "evidence": "新订全书：苏州平米二百五十余万石松江一百二十余万石每亩科至三斗六七升"},
    {"item_id": "02-002", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "考成必责十分全完之弊：席未暇暖褫削旋加日怀参奏处分之惧莫展催科抚字之长"},
    # ---- 02-003 河南 ----
    {"item_id": "02-003", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "河夫派夫之苦：道路奔驰费出不赀星眠露立逃亡行县勾摄"},
    # ---- 02-004 山东 ----
    {"item_id": "02-004", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "山东水陆三路冲繁职守：东路中路水路应付夫马车辆船只纤夫昼夜不绝"},
    {"item_id": "02-004", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "青登莱鱼盐之利：三面临海地皆斥卤恃鱼盐之利，海运罢而商贾往来不绝"},
    {"item_id": "02-004", "dim": "TME", "tme_type": "season",
     "target": "", "evidence": "海运历史窗口：元时东南百万之粮由登莱海道直达天津"},
    # ---- 02-005 山西 ----
    {"item_id": "02-005", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "地砂土瘠之困：无江湖水利之饶亦无沃野平原之广又无杂产树木之利"},
    # ---- 02-006 陕西 ----
    {"item_id": "02-006", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "陕甘宁抚裁并：康熙四年宁抚裁并归甘抚管辖驻札兰州为宁甘适中之地"},
    {"item_id": "02-006", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "明时北边总制大臣：东路宣大西路陕西延绥宁夏甘肃，西路总制治固原"},
    {"item_id": "02-006", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "三面逼邻番夷止间一墙：榆林外部落效顺距西安遥制已可寒心"},
    # ---- 02-007 浙江 ----
    {"item_id": "02-007", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "浙省巡道复设：复宁波巡海道兼辖处州/复嘉兴守道兼辖杭湖/复衢州守道兼辖金严，十一府皆有道员统辖"},
    {"item_id": "02-007", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "驻防兵丁烧柴之累：杭嘉湖绍水乡无尺土可樵采，禁则烧柴无措"},
    {"item_id": "02-007", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "海塘防坍：七郡地势洼下赖海塘捍卫，不修则基址圮坏风涛深入七郡尽付浩渺"},
    {"item_id": "02-007", "dim": "LGR", "lgr_type": "board",
     "target": "", "evidence": "海塘编立字号（明始易以石编立字号）"},
    # ---- 02-008 福建 ----
    {"item_id": "02-008", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "台湾形势：地非小/流寓民数万/土沃衍，丝紬油钉药材茶纸仰给内地"},
    # ---- 02-009 广西 ----
    {"item_id": "02-009", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "广西巡道弹压职责：桂巡道辖九属/梧巡驻郁林/左江巡道驻南宁兼辖四郡/右江巡道驻宾州兼辖三郡"},
    {"item_id": "02-009", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "猺獞杂处防患：府江险要延袤甚远接连怀贺八排素称贼薮必资专设巡道"},
    # ---- 02-010 广东 ----
    {"item_id": "02-010", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "粤东形势南北差异：靠北山绵土瘠向少稻粱靠南水沃田腴兼鱼盐之利"},
    # ---- 02-011 江西 ----
    {"item_id": "02-011", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "南贑十三处调防：瑞金罗汉岩宁都小田赣县曲村均村等设官兵把守险要"},
    {"item_id": "02-011", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "江西湖广设提军抚治之官（南贑山深人狡郧阳土旷民贫奸宄易聚）"},
    # ---- 02-012 湖广 ----
    {"item_id": "02-012", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "湖广复道：武昌道驻蕲州兼武汉黄/上荆南道驻荆州兼土司屯民/郧郡守道兼襄阳/澧州道管岳常/沅州道统辰沅靖/永州道管衡永郴"},
    {"item_id": "02-012", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "郧阳抚治防盗：筦巴蜀门户扼全楚上游地形便利四出可窥伺山险不平人犷难理"},
    # ---- 02-013 四川 ----
    {"item_id": "02-013", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "川省镇营罗列边防：松潘漳腊迭溪协营/建昌永宁峩边马边黎雅各镇营/重夔巫山黔彭各镇营/保顺潼设一镇数营"},
    {"item_id": "02-013", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "全川处处急边：接壤天全乌蒙打箭炉尽是蒙古部落土司猓蛮内多改土设流"},
    # ---- 02-014 贵州 ----
    {"item_id": "02-014", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "水西改土设流建官：设平远大定黔西三府各知府通判经历司狱儒学教授比喇府增设推官，分巡毕节道改整饬三府分巡贵宁道驻比喇"},
    {"item_id": "02-014", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "治苗防乱：苗民争杀一体追究则头目逃躲深匿，许照治苗旧例头目讲明曲直"},
    {"item_id": "02-014", "dim": "LGR", "lgr_type": "ledger",
     "target": "", "evidence": "新设平大黔威四府户口田粮：人民一万六千一百四十七户田十万二千三百九十七亩零地六万六千四百一十亩零"},
    {"item_id": "02-014", "dim": "TME", "tme_type": "deadline",
     "target": "", "evidence": "水西平后设流顺序：先设三府以试其治，后地广人多再为添设"},
    # ---- 02-015 云南 ----
    {"item_id": "02-015", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "省司府职责体系：督抚拊绥/布政司宣布承流/按察司弹压觉举/守巡道督察料理/知府督率州县/州县父母官"},
    {"item_id": "02-015", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "守令层层受剥削：府厅辖之司道辖之督抚又辖之层层管辖之人大半皆层层剥削之人"},
    {"item_id": "02-015", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "十吏之弊：喜事/昏庸/耗蠹/木痹/惰慢/柔邪/狡伪/谄谀/酷暴/贪鄙"},
    {"item_id": "02-015", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "官评底本防失察：自太府而下人各二叶小官各半叶日访月积兼听博访"},
    {"item_id": "02-015", "dim": "LGR", "lgr_type": "ledger",
     "target": "", "evidence": "税课额账：油行既税店又税油屠行既税生又税死"},
    {"item_id": "02-015", "dim": "LGR", "lgr_type": "ledger",
     "target": "", "evidence": "滇省九井盐课：正课银十四万四千八百零九两零内除小尽无征实征十四万四千一百六十一两零"},
    {"item_id": "02-015", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "文武统辖：世祖定制文统乎武，近奉新令文武不相统属之弊（武臣害民司文者不能禁）"},
    {"item_id": "02-015", "dim": "TME", "tme_type": "assessment",
     "target": "", "evidence": "州县四项考语：荒残/冲疲/充实/简易，按册周知利病观政辨贤否"},
]
