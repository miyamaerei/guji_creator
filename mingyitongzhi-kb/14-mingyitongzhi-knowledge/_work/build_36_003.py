# -*- coding: utf-8 -*-
"""Build 36-003 延安府 knowledge-base JSON files."""
import json, os

OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol36"
os.makedirs(OUT, exist_ok=True)

IID = "36-003"
VOL = "36"
GID = "GEO-36003"
REGION = "陕西"

# ---------- geo nodes ----------
def county(gcode, name, parent, loc, hh, hhnote):
    return {
        "geo_id": f"{GID}-{gcode}", "item_id": IID, "name": name,
        "type": "county", "region": REGION, "parent": parent,
        "children": [], "volume_range": "卷36",
        "attributes": {"location_text": loc,
                       "households": {"count": hh, "unit": "里", "note": hhnote}},
    }

def subpref(gcode, name, parent, loc, hh, hhnote, children=None):
    return {
        "geo_id": f"{GID}-{gcode}", "item_id": IID, "name": name,
        "type": "subprefecture", "region": REGION, "parent": parent,
        "children": children or [], "volume_range": "卷36",
        "attributes": {"location_text": loc,
                       "households": {"count": hh, "unit": "里", "note": hhnote}},
    }

def weisuo(gcode, name, parent, loc, gtype):
    return {
        "geo_id": f"{GID}-{gcode}", "item_id": IID, "name": name,
        "type": "weisuo", "region": REGION, "parent": parent,
        "children": [], "volume_range": "卷36",
        "attributes": {"location_text": loc, "garrison_type": gtype},
    }

# direct children of 府
direct_counties = [
    county("c01", "肤施县", GID, "附郭", 27, "编户二十七里"),
    county("c02", "安塞县", GID, "在府城西北四十里", 16, "编户一十六里"),
    county("c03", "甘泉县", GID, "在府城西南九十里", 23, "编户二十三里"),
    county("c04", "安定县", GID, "在府城北一百九十里", 9, "编户九里"),
    county("c05", "保安县", GID, "在府城西北一百八十里", 8, "编户八里"),
    county("c06", "宜川县", GID, "在府城东南二百八十里", 24, "编户二十四里"),
    county("c07", "延川县", GID, "在府城东二百里", 11, "编户一十一里"),
    county("c08", "延长县", GID, "在府城东一百五十里", 11, "编户一十一里"),
]

s01 = subpref("s01", "鄜州", GID, "在府城南一百八十里", 51, "编户五十一里领县三",
              [f"{GID}-c10", f"{GID}-c11", f"{GID}-c12"])
c10 = county("c10", "洛川县", f"{GID}-s01", "在州城东六十里", 64, "编户六十四里")
c11 = county("c11", "中部县", f"{GID}-s01", "在州城南一百四十里", 24, "编户二十四里")
c12 = county("c12", "宜君县", f"{GID}-s01", "在州城南二百一十里", 38, "编户三十八里")

s02 = subpref("s02", "绥德州", GID, "在府城东北三百六十里", 10, "编户一十里领县二",
              [f"{GID}-c09", f"{GID}-c13"])
c09 = county("c09", "青涧县", f"{GID}-s02", "在州城南一百二十里", 9, "编户九里")
c13 = county("c13", "米脂县", f"{GID}-s02", "在州城北八十里", 13, "编户一十三里")

s03 = subpref("s03", "葭州", GID, "在府城北五百八十里", 8, "编户八里领县三",
              [f"{GID}-c14", f"{GID}-c15", f"{GID}-c16"])
c14 = county("c14", "吴堡县", f"{GID}-s03", "在州城南八十里", 3, "编户三里")
c15 = county("c15", "神木县", f"{GID}-s03", "在州城东北三百里", 5, "编户五里")
c16 = county("c16", "府谷县", f"{GID}-s03", "在州城东北五百里", 6, "编户六里")

w01 = weisuo("w01", "延安卫", GID, "在府治北洪武二年建", "卫")
w02 = weisuo("w02", "绥德卫", GID, "在绥德州治北洪武六年建", "卫")
w03 = weisuo("w03", "榆林卫", GID, "在府城东北七百五十里正德二年建", "卫")
w04 = weisuo("w04", "塞门守御百户所", GID, "在安塞县北一百五十里洪武十二年建", "百户所")
w05 = weisuo("w05", "安定守御百户所", GID, "在安定县治北洪武二年建", "百户所")
w06 = weisuo("w06", "保安守御百户所", GID, "在保安县治南洪武十二年建", "百户所")
w07 = weisuo("w07", "镇羌守御百户所", GID, "在神木县治西正德二年建", "百户所")

all_counties = direct_counties + [c09, c10, c11, c12, c13, c14, c15, c16]
all_sub = [s01, s02, s03]
all_wei = [w01, w02, w03, w04, w05, w06, w07]

pref_children = (
    [f"{GID}-c0{i}" for i in range(1, 9)] +
    [f"{GID}-s01", f"{GID}-s02", f"{GID}-s03"] +
    [f"{GID}-w0{i}" for i in range(1, 8)]
)

pref = {
    "geo_id": GID, "item_id": IID, "name": "延安府",
    "type": "prefecture", "region": REGION, "parent": "GEO-000",
    "children": pref_children, "volume_range": "卷36",
    "attributes": {
        "borders": [
            {"direction": "东", "to_place": "山西黄河界", "distance_li": 450},
            {"direction": "西", "to_place": "庆阳府合水县界", "distance_li": 200},
            {"direction": "南", "to_place": "西安府同官县界", "distance_li": 415},
            {"direction": "北", "to_place": "沙漠界", "distance_li": 500},
        ],
        "to_capital": [
            {"capital": "京师", "distance_li": 2200},
            {"capital": "南京", "distance_li": 4840},
        ],
        "households": {"count": None, "unit": "里", "note": "领州三县十六；各属州县编户见下"},
        "grain_tax": {"amount": 410000, "unit": "石", "note": "粮四十一万石零"},
        "jun_name": "上郡【秦名】金明【元魏名】",
        "topography": "形胜之地【宋赵卨奏绥实形胜之地宜增广边障乃无穷之利】；五路襟喉【宋王庶传延安五路襟喉】；长城因河为塞洛水之交三水所会【俱图经】；边陲之郡【寰宇记其城据山四面甚险边陲之郡也】；秦地要区【元志延安古郡秦地要区】",
        "customs": "人勤稼穑【延安旧志】；俗尚鬼神【图经俗尚鬼神而信祈祷】；不崇侈靡颇习程法【肤施图经俗尚淳俭不崇侈靡善营市利颇习程法】；以夏月游赏为重【鄜州图经】；人皆精于制兵器【坊州图经】；人性勇直好尚武力【葭州图经蕃汉互居人性勇直好尚武力守望相助】；性朴少文俗尚俭约【延川县志】",
    },
    "cit_ids": [f"CIT-{i:03d}" for i in range(1, 13)],
}

geos = [pref] + direct_counties + [s01, c10, c11, c12, s02, c09, c13, s03, c14, c15, c16] + all_wei

# ---------- ents ----------
ents = [
    {"ent_id": "ENT-001", "name": "延安府", "type": "geo", "norm": "延安府", "first_source": IID},
    {"ent_id": "ENT-002", "name": "嘉岭山", "type": "mtn", "norm": "嘉岭山", "first_source": IID},
    {"ent_id": "ENT-003", "name": "清凉山", "type": "mtn", "norm": "清凉山", "first_source": IID},
    {"ent_id": "ENT-004", "name": "黄河", "type": "mtn", "norm": "黄河", "first_source": IID},
    {"ent_id": "ENT-005", "name": "洛河", "type": "mtn", "norm": "洛河", "first_source": IID},
    {"ent_id": "ENT-006", "name": "无定河", "type": "mtn", "norm": "无定河", "first_source": IID},
    {"ent_id": "ENT-007", "name": "延水", "type": "mtn", "norm": "延水", "first_source": IID},
    {"ent_id": "ENT-008", "name": "桥山", "type": "mtn", "norm": "桥山", "first_source": IID},
    {"ent_id": "ENT-009", "name": "黄帝", "type": "person", "norm": "黄帝", "first_source": IID},
    {"ent_id": "ENT-010", "name": "杜甫", "type": "person", "norm": "杜甫", "first_source": IID},
    {"ent_id": "ENT-011", "name": "韩世忠", "type": "person", "norm": "韩世忠", "first_source": IID},
    {"ent_id": "ENT-012", "name": "范仲淹", "type": "person", "norm": "范仲淹", "first_source": IID},
]

# ---------- evos ----------
evos = [
    {"evo_id": f"EVO-{i:03d}", "item_id": IID, "geo_id": GID, "dynasty": d, "era": e,
     "institution_name": n, "action": a, "detail": det}
    for i, (d, e, n, a, det) in enumerate([
        ("上古", None, "雍州之域", "因之", "禹贡雍州之域，天文井鬼分野"),
        ("春秋", None, "白翟所居", "因之", "春秋时白翟所居"),
        ("秦", None, "上郡", "属", "秦属上郡"),
        ("汉", None, "翟国/上郡", "属", "汉初属翟国，寻属上郡"),
        ("东汉", None, "郡邑俱废", "废", "东汉时郡邑俱废"),
        ("晋", None, "陷于戎", "陷", "晋陷于戎"),
        ("后魏", None, "统万镇/金明郡/东夏州", "置", "后魏以为统万镇，未几置金明郡，又改东夏州"),
        ("后魏", None, "延州", "改", "后魏改为延州，取延水为名"),
        ("隋", None, "延安郡", "改", "隋初仍为州，大业初改延安郡"),
        ("唐", "天宝", "延安郡", "改", "唐初复为延州，天宝初改延安郡"),
        ("唐", "乾元", "延州", "复", "乾元初复为延州"),
        ("五代梁", None, "忠义军节度", "置", "五代梁置忠义军节度"),
        ("后唐", None, "彰武军", "改", "后唐改彰武军"),
        ("宋", "元祐", "延安府", "升", "宋初仍为延州属鄜延路，元祐中升为延安府"),
        ("金", None, "延安府", "因之", "金仍旧"),
        ("元", None, "延安路", "改", "元改延安路"),
        ("明", None, "延安府", "复", "本朝复改延安府，领州三县十六"),
    ], start=1)
]

# ---------- mtns ----------
def mtn(i, name, typ, loc, desc, lore=""):
    return {"mtn_id": f"MTN-{i:03d}", "item_id": IID, "geo_id": GID,
            "name": name, "type": typ, "location_text": loc,
            "description": desc, "lore": lore}

mtns = [
    mtn(1, "嘉岭山", "山", "在府城东南", "形势高峻", "宋范仲淹尝大书嘉岭山三字于石"),
    mtn(2, "清凉山", "山", "在府城东北", "上有尸毗岩，相传昔尸毗王修行处；又有万佛洞，内大小石佛万余；又有仙石洞在山北", "金皇统九年梁文仙凿；山半有鹫峰泉，寺僧于悬崖上垂绳汲之"),
    mtn(3, "重覆山", "山", "在府城东南旧门山县境", "山形重叠故名", ""),
    mtn(4, "伏龙山", "山", "在府城北五里", "以形似名", ""),
    mtn(5, "碧簪山", "山", "在府城北一十里", "形尖如碧簪，高可数百丈", "一名虎头山"),
    mtn(6, "五龙山", "山", "在肤施县北一十二里", "上有五龙祠", ""),
    mtn(7, "伏陆山", "山", "在甘泉县东北", "唐置伏陆县因此山而名", ""),
    mtn(8, "雕阴山", "山", "在甘泉县南二十里", "山多土穴，为鹰雕所居", "唐韦庄诗雕阴寒食足游人金凤罗衣湿麝熏"),
    mtn(9, "温泉山", "山", "在甘泉县南四十三里", "下有温泉", ""),
    mtn(10, "三塠山", "山", "在安塞县旧敷政县境", "", ""),
    mtn(11, "九吾山", "山", "在保安县西五十里", "上有湫，岁旱祷雨辄应", "宋立庙封神为应顺王，今民犹岁时祀之"),
    mtn(12, "凤翅山", "山", "在宜川县东南五里", "以形似名", ""),
    mtn(13, "安乐山", "山", "在宜川县南一十里", "", ""),
    mtn(14, "库利山", "山", "在宜川县境", "亦与旧临真县相接", ""),
    mtn(15, "云岩山", "山", "在宜川县北八十里", "山形重叠如云", "金尝于此置云岩镇"),
    mtn(16, "孟门山", "山", "在宜川县北石溞下三里黄河中流", "相传有石扼东河流，俗谓之石溞", ""),
    mtn(17, "青眉山", "山", "在延川县西北六十里", "后魏时有土蕃青眉族居此", ""),
    mtn(18, "屏山", "山", "在延长县治南", "其形如屏", ""),
    mtn(19, "高奴山", "山", "在延长县北二十里", "上有古塞", ""),
    mtn(20, "独战山", "山", "在延长县东北六十里", "山险峻，一人独战可以当千", ""),
    mtn(21, "龟山", "山", "在鄜州城西", "以形似名", ""),
    mtn(22, "樱桃山", "山", "在鄜州南四里", "上多樱桃树", ""),
    mtn(23, "桥山", "山", "在中部县治北", "下有沮水，或云水从山底经过如桥", "即轩辕黄帝葬衣冠之所"),
    mtn(24, "玉仙山", "山", "在中部县西五里", "时有仙人往来于此", ""),
    mtn(25, "石堂山", "山", "在中部县治西北", "一名翟道山", "周穆王传天子命驾八骏之马造父为御南征朔野径绝翟道升于大行即此"),
    mtn(26, "凤凰山", "山", "在中部县西一百里", "以形似名", ""),
    mtn(27, "玉华山", "山", "在宜君县西南四十里", "唐太宗建玉华宫以此山名", "宋雍熙初于此山获一角兽时以为麒；金于此置玉华镇"),
    mtn(28, "疏属山", "山", "在绥德州境", "", "山海经贰负之臣曰危与贰负杀窫窳，帝乃梏之疏属山；汉宣帝使人发上郡疏属山于盘石室中得一人，刘向按此言之"),
    mtn(29, "笔架山", "山", "在青涧县治西", "以形似名", ""),
    mtn(30, "龙眼山", "山", "在神木县治东南", "峰上有二孔透穿如龙眼", ""),
    mtn(31, "五虎山", "山", "在府谷县治东", "上有五峰势若伏虎", ""),
    mtn(32, "凤凰岭", "岭", "在绥德州东三十里", "", ""),
    mtn(33, "仙掌岩", "岩", "在中部县西北三里", "以形似名", ""),
    mtn(34, "漱玉岩", "岩", "在延长县治东", "其中可容百人，泉出如练", ""),
    mtn(35, "苇谷", "谷", "在鄜州境", "谷有水东南流入三川", "唐郑玉诗水会三川漾碧波雕阴人唱采花歌"),
    mtn(36, "凤凰谷", "谷", "在宜君县西南五十里", "尝有五色雀现于此因名", "唐玉华宫建于此谷"),
    mtn(37, "兰芝谷", "谷", "在宜君县西五十里", "", ""),
    mtn(38, "开元坡", "坡", "在鄜州城北", "", "唐韦庄诗开元坡下日初斜拜扫归来走钿车"),
    mtn(39, "野猪峡", "峡", "在甘泉县北四十五里", "山峡险窄", ""),
    mtn(40, "黄河", "河", "在府城东北", "流经宜川延川二县境", ""),
    mtn(41, "洛河", "河", "在甘泉县治西", "源出庆阳府洛源县", ""),
    mtn(42, "吃莫河", "河", "在保安县境", "源出蕃部吃莫川，南流入洛河，不胜船筏", ""),
    mtn(43, "无定河", "河", "在青涧县东六十里", "南入黄河，一名奢延水，又名银水", "舆地广记唐立银州东北有无定河即圁水也；后人因溃沙急流深浅不定故更今名；唐陈祐诗无定河边暮笛声"),
    mtn(44, "葭芦河", "河", "在葭州西五里", "岸多芦苇故名", "宋元丰中于此立寨"),
    mtn(45, "延水", "河", "在府城东门外", "源出安塞县西北芦关岭，东南流入肤施县境，又流经延长县入黄河", "俗称濯筋水，相传昔尸毗王割身饲鸽身肉并尽于此水濯其筋骨因名"),
    mtn(46, "汾川水", "河", "在宜川县北八十里", "源出甘泉县界，东流入黄河", ""),
    mtn(47, "清化水", "河", "在肤施县东四十里", "源出嘉泉，东流入濯筋河", ""),
    mtn(48, "龙尾水", "河", "在肤施县北", "即龙尾溪", ""),
    mtn(49, "清水", "河", "在肤施县北", "流至老人谷，俗呼为老人水，又东经古高奴县地合丰水", ""),
    mtn(50, "大理水", "河", "在绥德州西", "", "宋种谔复绥州夜渡大理水驻师即此"),
    mtn(51, "三川水", "河", "在鄜州南六十里", "以华池水黑源水洛水同会谓之三川", "唐杜甫诗三川不可到归路晚山稠"),
    mtn(52, "沮水", "河", "在中部县南门外", "源发子午岭，东南入于洛", ""),
    mtn(53, "慈乌水", "河", "在宜君县西北四十里", "源自分水岭东流入本县界", ""),
    mtn(54, "子午水", "河", "在宜君县西北一百三十五里", "源出子午岭，东南流入中部县合沮水", ""),
    mtn(55, "库利川", "川", "在甘泉县东北", "相传上田沃壤五谷丰饶，羌人称贮旧谷为库利", ""),
    mtn(56, "屈野川", "川", "在神木县西南一百五十里", "旧属银城县", ""),
    mtn(57, "柳湖", "湖", "在府城南", "", "宋范仲淹诗种柳穿湖后延安盛可游"),
    mtn(58, "延利渠", "渠", "在府城南", "", "宋司马光和庞籍诗枝分清浅流纵横贯城市"),
    mtn(59, "三岔沟", "沟", "在保安县北九十里", "", ""),
    mtn(60, "玉莲池", "池", "在宜川县境", "池有万顷，为一方之胜", ""),
    mtn(61, "暖泉井", "井", "在府治南", "泉有九眼，味甘美，冬温夏冷，遇大寒流溢不冻，甚济居人", ""),
    mtn(62, "龙潭井", "井", "在安塞县西南一百三十里", "潭深水清四时不竭，祷雨辄应", ""),
    mtn(63, "石井", "井", "在青涧县治西", "宋种世衡所凿。初世衡城青涧处险无泉，凿地十五丈遇石，世衡命屑石一畚酬百金，卒得泉", ""),
    mtn(64, "嘉泉", "泉", "在肤施县境旧丰林废县东北", "水涌出地如团碾可嘉，因名", ""),
    mtn(65, "呜咽泉", "泉", "在绥德州南三里", "即秦扶苏死处", "唐胡曾诗举国贤良尽泪垂扶苏屈死树边时"),
    mtn(66, "一线泉", "泉", "在中部县治西南", "酌之可以疗疾", ""),
    mtn(67, "甘泉", "泉", "在甘泉县治南五里", "岩谷中飞流激下，隋炀帝游此饮而甘之", "泉侧有奇鸟身白足赤如小山鹊，其声数种"),
    mtn(68, "五龙泉", "泉", "在府城东北石罅中涌出", "有雄吼之声，汇而为池，上有五龙堂", "水经五龙池泉在左山上，有牧龙川多产骏马"),
]

# ---------- prods ----------
prods = [
    {"prod_id": f"PROD-{i:03d}", "item_id": IID, "geo_id": GID, "name": n, "note": note}
    for i, (n, note) in enumerate([
        ("牡丹", "本府出，宋欧阳修花谱延安红丹州红皆彼产之杰然者，自丹延以西尤多与荆棘无异，土人刈以为薪"),
        ("麝香", "鄜州出"),
        ("甘草", "府谷县出"),
        ("石油", "延川延长二县出，自石中流出，每岁秋后居民取之可以燃灯疗疮"),
        ("玛瑙", "府谷神木二县出，元时尝遣人采取"),
        ("苁蓉", "保安县出"),
        ("大防", "宜君县出"),
        ("土硫黄", "宜君县出"),
        ("甘遂", "绥德州出"),
        ("全蝎", "葭州出"),
        ("黄防", "延川青涧神木三县出"),
    ], start=1)
]

# ---------- cits ----------
cits = [
    {"cit_id": f"CIT-{i:03d}", "item_id": IID, "cited_work": w, "cited_work_ent_id": None,
     "context": ctx, "original": f"【{w}{body}】"}
    for i, (w, ctx, body) in enumerate([
        ("宋赵卨奏", "立论", "绥实形胜之地宜增广边障乃无穷之利"),
        ("宋王庶传", "立论", "延安五路襟喉"),
        ("图经", "立论", "长城因河为塞洛水之交三水所会"),
        ("寰宇记", "立论", "其城据山四面甚险边陲之郡也"),
        ("元志", "立论", "延安古郡秦地要区"),
        ("延安旧志", "证俗", "人勤稼穑"),
        ("图经", "证俗", "俗尚鬼神而信祈祷"),
        ("肤施图经", "证俗", "俗尚淳俭不崇侈靡善营市利颇习程法"),
        ("鄜州图经", "证俗", "以夏月游赏为重"),
        ("坊州图经", "证俗", "人皆精于制兵器"),
        ("葭州图经", "证俗", "蕃汉互居人性勇直好尚武力守望相助"),
        ("延川县志", "证俗", "性朴少文俗尚俭约"),
    ], start=1)
]

# ---------- main file ----------
main = {
    "item_id": IID, "volume": VOL, "source": "延安府", "region": REGION,
    "layers": {
        "ents": ents, "geos": geos, "evos": evos, "mtns": mtns,
        "prods": prods, "cits": cits,
        "pers": [], "sites": [],
    },
    "layer_count": 7,
    "validation": {
        "errs": [], "gap": 0,
        "notes": "pers 层拆至 36-003_pers1_名宦.json 与 36-003_pers2_人物列女仙释.json；sites 层拆至 36-003_sites1_古迹陵墓祠庙寺观.json 与 36-003_sites2_宫室关梁公署学校.json"
    }
}

with open(os.path.join(OUT, "36-003_延安府.json"), "w", encoding="utf-8") as f:
    json.dump(main, f, ensure_ascii=False, indent=1)

# ---------- county small files ----------
def small_geo(node, label):
    return {
        "item_id": IID, "volume": VOL, "source": label, "region": REGION,
        "layers": {
            "ents": [{"ent_id": f"ENT-{node['geo_id'].split('-')[-1]}", "name": node["name"],
                      "type": "geo", "norm": node["name"], "first_source": IID}],
            "geos": [node], "evos": [], "mtns": [], "pers": [],
            "sites": [], "prods": [], "cits": [],
        },
        "layer_count": 7,
    }

name_map = {
    "c01": "肤施县", "c02": "安塞县", "c03": "甘泉县", "c04": "安定县",
    "c05": "保安县", "c06": "宜川县", "c07": "延川县", "c08": "延长县",
    "c09": "青涧县", "c10": "洛川县", "c11": "中部县", "c12": "宜君县",
    "c13": "米脂县", "c14": "吴堡县", "c15": "神木县", "c16": "府谷县",
    "s01": "鄜州", "s02": "绥德州", "s03": "葭州",
    "w01": "延安卫", "w02": "绥德卫", "w03": "榆林卫",
    "w04": "塞门守御百户所", "w05": "安定守御百户所",
    "w06": "保安守御百户所", "w07": "镇羌守御百户所",
}

for node in geos[1:]:  # skip prefecture itself
    code = node["geo_id"].split("-")[-1]  # e.g. c01
    label = name_map[code]
    fn = os.path.join(OUT, f"36-003_{code}_{label}.json")
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(small_geo(node, label), f, ensure_ascii=False, indent=1)

print("main + small geos done")
print(f"ents={len(ents)} geos={len(geos)} evos={len(evos)} mtns={len(mtns)} prods={len(prods)} cits={len(cits)}")
