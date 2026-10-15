# -*- coding: utf-8 -*-
"""Generate vol122 (澂江府) and vol123 (蒙化府) JSON files."""
import json, os

BASE = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data"

def dump(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print("WROTE", path)

# ============================================================
# vol122 澂江府
# ============================================================
V = "122"
ITEM = "122-001"
REGION = "云南"
GEO = "GEO-122001"

# ---- ents ----
ents = [
    {"ent_id": "ENT-001", "name": "澂江府", "type": "geo", "norm": "澂江府", "first_source": ITEM},
    {"ent_id": "ENT-C01", "name": "河阳县", "type": "geo", "norm": "河阳县", "first_source": ITEM},
    {"ent_id": "ENT-C02", "name": "江川县", "type": "geo", "norm": "江川县", "first_source": ITEM},
    {"ent_id": "ENT-C03", "name": "阳宗县", "type": "geo", "norm": "阳宗县", "first_source": ITEM},
    {"ent_id": "ENT-S01", "name": "新兴州", "type": "geo", "norm": "新兴州", "first_source": ITEM},
    {"ent_id": "ENT-S02", "name": "路南州", "type": "geo", "norm": "路南州", "first_source": ITEM},
]

# ---- geos ----
geos = [
    {
        "geo_id": GEO, "item_id": ITEM, "name": "澂江府", "type": "prefecture",
        "region": REGION, "parent": "GEO-000",
        "children": [f"{GEO}-c01", f"{GEO}-c02", f"{GEO}-c03", f"{GEO}-s01", f"{GEO}-s02"],
        "volume_range": "卷122",
        "attributes": {
            "borders": [
                {"direction": "东", "to_place": "广西府弥勒州界", "distance_li": 200},
                {"direction": "南", "to_place": "临安府宁州界", "distance_li": 90},
                {"direction": "西", "to_place": "云南府晋宁州界", "distance_li": 25},
                {"direction": "北", "to_place": "云南府宜良县界", "distance_li": 55},
            ],
            "to_capital": [
                {"capital": "南京", "distance_li": 7300},
                {"capital": "京师", "distance_li": 10745},
            ],
            "households": {"count": None, "unit": "里", "note": "领州二县三；各属编户见下"},
            "grain_tax": {"amount": 9080, "unit": "石", "note": "粮九千八十石零"},
            "jun_name": "河阳【蒙氏名】",
            "topography": "山水明秀【澂江志东跨旸溥西倚涌拔回抚仙而背罗藏山水明秀之地】；崎岖崖石地鲜平夷【云南志】；有湖山之胜【旧志南北有湖山之胜东西分云南广西之间】",
            "customs": "蚕衣耕食民安于富【云南志】；其性质野其俗豪强【元志】；嚚讼难理【蒙麽徒白子二种赋性顽愚常怀嫉恶嚚讼难理】",
        },
        "cit_ids": ["CIT-001", "CIT-002", "CIT-003", "CIT-004", "CIT-005", "CIT-006"],
    },
    {"geo_id": f"{GEO}-c01", "item_id": ITEM, "name": "河阳县", "type": "county", "region": REGION,
     "parent": GEO, "children": [], "volume_range": "卷122",
     "attributes": {"location_text": "附郭", "households": {"count": 6, "unit": "里", "note": "编户六里"}}},
    {"geo_id": f"{GEO}-c02", "item_id": ITEM, "name": "江川县", "type": "county", "region": REGION,
     "parent": GEO, "children": [], "volume_range": "卷122",
     "attributes": {"location_text": "在府东南六十里", "households": {"count": 2, "unit": "里", "note": "编户二里"}}},
    {"geo_id": f"{GEO}-c03", "item_id": ITEM, "name": "阳宗县", "type": "county", "region": REGION,
     "parent": GEO, "children": [], "volume_range": "卷122",
     "attributes": {"location_text": "在府城北四十里", "households": {"count": 5, "unit": "里", "note": "编户五里"}}},
    {"geo_id": f"{GEO}-s01", "item_id": ITEM, "name": "新兴州", "type": "department", "region": REGION,
     "parent": GEO, "children": [], "volume_range": "卷122",
     "attributes": {"location_text": "在府西一百二十里", "households": {"count": 2, "unit": "里", "note": "编户二里"}}},
    {"geo_id": f"{GEO}-s02", "item_id": ITEM, "name": "路南州", "type": "department", "region": REGION,
     "parent": GEO, "children": [], "volume_range": "卷122",
     "attributes": {"location_text": "在府东一百三十里", "households": {"count": 3, "unit": "里", "note": "编户三里"}}},
]

# ---- evos ----
evos = [
    {"evo_id": "EVO-001", "item_id": ITEM, "geo_id": GEO, "dynasty": "夏", "era": None,
     "institution_name": "梁州之界", "action": "因之", "detail": "禹贡梁州之界，天文井鬼分野，古西南夷"},
    {"evo_id": "EVO-002", "item_id": ITEM, "geo_id": GEO, "dynasty": "战国楚", "era": None,
     "institution_name": "滇国地", "action": "因之", "detail": "战国楚时为滇国地"},
    {"evo_id": "EVO-003", "item_id": ITEM, "geo_id": GEO, "dynasty": "汉", "era": "元封",
     "institution_name": "俞元县/益州郡", "action": "置", "detail": "汉元封初置俞元县属益州郡"},
    {"evo_id": "EVO-004", "item_id": ITEM, "geo_id": GEO, "dynasty": "蜀汉", "era": None,
     "institution_name": "建宁郡", "action": "因之", "detail": "蜀汉属建宁郡"},
    {"evo_id": "EVO-005", "item_id": ITEM, "geo_id": GEO, "dynasty": "梁", "era": None,
     "institution_name": "南宁州", "action": "因之", "detail": "梁属南宁州"},
    {"evo_id": "EVO-006", "item_id": ITEM, "geo_id": GEO, "dynasty": "隋", "era": None,
     "institution_name": "昆州", "action": "因之", "detail": "隋置昆州此地属焉"},
    {"evo_id": "EVO-007", "item_id": ITEM, "geo_id": GEO, "dynasty": "唐", "era": "天宝",
     "institution_name": "南宁/昆二州/罗伽甸", "action": "没", "detail": "唐为南宁昆二州地，天宝末没于蛮号罗伽甸；初麽些蛮居之后为僰蛮所夺"},
    {"evo_id": "EVO-008", "item_id": ITEM, "geo_id": GEO, "dynasty": "南诏", "era": None,
     "institution_name": "河阳郡", "action": "置", "detail": "南诏蒙氏于此置河阳郡"},
    {"evo_id": "EVO-009", "item_id": ITEM, "geo_id": GEO, "dynasty": "宋大理", "era": None,
     "institution_name": "三部/罗伽部", "action": "析", "detail": "宋时大理段氏析蛮为三部曰强宗曰休制曰步雄；其步雄部后居罗伽甸者号罗伽部"},
    {"evo_id": "EVO-010", "item_id": ITEM, "geo_id": GEO, "dynasty": "元", "era": None,
     "institution_name": "罗伽万户府/中路/澂江路", "action": "改", "detail": "元置罗伽万户府后改为中路，至元中改置澂江路属云南行省"},
    {"evo_id": "EVO-011", "item_id": ITEM, "geo_id": GEO, "dynasty": "明", "era": "洪武",
     "institution_name": "澂江府", "action": "改", "detail": "本朝洪武十五年改为澂江府，领州二县三"},
]

# ---- mtns ----
def mtn(i, geo_id, name, typ, loc, desc="", lore=""):
    return {"mtn_id": f"MTN-{i:03d}", "item_id": ITEM, "geo_id": geo_id,
            "name": name, "type": typ, "location_text": loc, "description": desc, "lore": lore}

mtns = [
    mtn(1, f"{GEO}-c01", "金莲山", "山", "在府治",
        "一名龟山，高圆平正如莲花然，府治学校皆建其上"),
    mtn(2, f"{GEO}-c01", "罗藏山", "山", "在府治西北",
        "东汉志曰装山出铜，后讹曰藏；又蛮语虎棚为罗藏，谓造棚以射虎也。其上宽平有龙湫，时兴云雾，元梁王结寨其上，又名梁王山。南有泉流为罗藏溪南入抚仙湖，北有泉流为锦溪经阳宗县西，西有泉流为弥勒石溪经阳宗县东，俱入于明湖"),
    mtn(3, f"{GEO}-c01", "玗扎山", "山", "在府治北",
        "一名无诈，今名乌劄；其麓有泉流为玗扎溪，南入抚仙湖"),
    mtn(4, f"{GEO}-c01", "旸溥山", "山", "在府治东南"),
    mtn(5, f"{GEO}-c01", "涌拔山", "山", "在府西南三十里",
        "屹立抚仙湖不与群山接，高耸独秀状如玉笋，又名玉笋山"),
    mtn(6, f"{GEO}-c02", "西山", "山", "在江川县西四里",
        "峰峦起伏，山麓多泉合流入星云湖"),
    mtn(7, f"{GEO}-c02", "蟠坤山", "山", "在江川县南一十五里",
        "东临抚仙湖，西际星云湖，山顶皆石赭无草木"),
    mtn(8, f"{GEO}-c02", "屈颡颠山", "山", "在江川县北一十五里",
        "昔有猎于是山终日而不获一，土人谓屈为犬、颡为惜、颠为劳而无获，因名屈颡颠山；势如寨，其半涌泉三派，西入滇池，东入抚仙湖，南为阿件溪入星云湖，溉田极为民利"),
    mtn(9, f"{GEO}-c02", "绿笼山", "山", "在江川县西北一十五里",
        "林木苍翠，下有泉为六部溪，东南入星云湖"),
    mtn(10, f"{GEO}-c03", "夹浦山", "山", "在阳宗县治西",
        "弥勒石溪及冷水塘三水夹之"),
    mtn(11, f"{GEO}-c03", "碁和山", "山", "在阳宗县南东二里",
        "顶若碁坪"),
    mtn(12, f"{GEO}-c03", "化石祖山", "山", "在阳宗县西北七里",
        "其南有泉流为曰角溪，东北入明湖"),
    mtn(13, f"{GEO}-s01", "奇梨山", "山", "在新兴州治西",
        "林木茂蔚，下有泉流为奇梨溪，入大溪"),
    mtn(14, f"{GEO}-s01", "灵照山", "山", "在新兴州东一十里"),
    mtn(15, f"{GEO}-s01", "大棋山", "山", "在新兴州西北一十五里",
        "上有石，俗传有仙弈碁于此"),
    mtn(16, f"{GEO}-s01", "罗麽山", "山", "在新兴州东北二十里",
        "今名石崖山，下有白龙泉流为罗麽溪，九曲入于大溪"),
    mtn(17, f"{GEO}-s01", "蒙习山", "山", "在新兴州西北七十里",
        "一名适饥山，山顶与晋宁州分界"),
    mtn(18, f"{GEO}-s02", "照镜山", "山", "在路南州西北二里",
        "前有池如镜"),
    mtn(19, f"{GEO}-s02", "休柔山", "山", "在路南州北一十五里",
        "今名九盘山，下有泉流为休柔溪，南入盘江"),
    mtn(20, f"{GEO}-s02", "遮日山", "山", "在路南州东南一十五里",
        "今名些亦山"),
    mtn(21, f"{GEO}-s02", "劄龙山", "山", "在路南州东八十里",
        "峰峦高耸，下有小石可以链铜"),
    mtn(22, f"{GEO}-s02", "羊鼻山", "山", "在旧邑市县东北一十五里",
        "山顶有泉流灌田亩"),
    mtn(23, f"{GEO}-s02", "木龙山", "山", "在旧邑市县东南一十五里",
        "高可五百余仞"),
    mtn(24, f"{GEO}-s02", "铁赤河", "河", "在路南州西四十里",
        "源自陆凉州，经邑市县过瓦渡龙溪普双龙溪，至州境西南又过兴宁溪，下流入盘溪"),
    mtn(25, f"{GEO}-s02", "巴盘江", "江", "源自陆凉州",
        "流经路南州邑市宜良，入广西府界"),
    mtn(26, f"{GEO}-c01", "抚仙湖", "湖", "在府治南",
        "周二百余里，一名罗伽湖，一名青鱼戏月湖；渟蓄清澈其中多石，东流入盘江"),
    mtn(27, f"{GEO}-c02", "星云湖", "湖", "在江川县治南",
        "周八十余里，东流五里入抚仙湖，两湖相通鱼不往来"),
    mtn(28, f"{GEO}-c03", "明湖", "湖", "在阳宗县北",
        "一名曰夷休，一名阳宗湖；湖源出罗蔵山下流入元江，周七十余里，两崖陡绝，山水黑色鱼味甚美"),
    mtn(29, f"{GEO}-c01", "龙泉溪", "溪", "在府西一十五里",
        "乱石中流入抚仙湖"),
    mtn(30, f"{GEO}-s01", "大溪", "溪", "源出夹雄山",
        "自新兴州东北流绕西南，过罗麽奇梨二溪，出嶍峨县入曲江"),
    mtn(31, f"{GEO}-c01", "空谷泉", "泉", "在府治东北",
        "汇而为池，春时颇温，浴之可去痒疴"),
    mtn(32, f"{GEO}-c02", "双井温泉", "泉", "在江川县海西村",
        "两井皆温泉，流入星云湖；邑市县治北亦有温泉"),
    mtn(33, f"{GEO}-c02", "冷水泉", "泉", "在江川县西北七里",
        "源出西山，流入星云湖；旧邑市县东亦有冷泉"),
    mtn(34, f"{GEO}-c01", "北坡泉", "泉", "在府治北"),
    mtn(35, f"{GEO}-c01", "西浦泉", "泉", "在府西十一里"),
    mtn(36, f"{GEO}-s02", "黑龙泉", "泉", "在路南州东八里"),
    mtn(37, f"{GEO}-s01", "莲花池", "池", "在新兴州北一十里",
        "下流入于大溪"),
]

# ---- cits ----
cits = [
    {"cit_id": "CIT-001", "item_id": ITEM, "cited_work": "澂江志", "cited_work_ent_id": None,
     "context": "形胜", "original": "【澂江志东跨旸溥西倚涌拔回抚仙而背罗藏山水明秀之地】"},
    {"cit_id": "CIT-002", "item_id": ITEM, "cited_work": "云南志", "cited_work_ent_id": None,
     "context": "形胜", "original": "【云南志崎岖崖石地鲜平夷】"},
    {"cit_id": "CIT-003", "item_id": ITEM, "cited_work": "旧志", "cited_work_ent_id": None,
     "context": "形胜", "original": "【旧志南北有湖山之胜东西分云南广西之间】"},
    {"cit_id": "CIT-004", "item_id": ITEM, "cited_work": "云南志", "cited_work_ent_id": None,
     "context": "风俗", "original": "【云南志蚕衣耕食民安于富】"},
    {"cit_id": "CIT-005", "item_id": ITEM, "cited_work": "元志", "cited_work_ent_id": None,
     "context": "风俗", "original": "【元志其性质野其俗豪强】"},
    {"cit_id": "CIT-006", "item_id": ITEM, "cited_work": "元志", "cited_work_ent_id": None,
     "context": "风俗", "original": "【蒙麽徒白子二种赋性顽愚常怀嫉恶嚚讼难理】"},
]

# ---- main file ----
main122 = {
    "item_id": ITEM, "volume": V, "source": "澂江府", "region": REGION,
    "layers": {
        "ents": ents, "geos": geos, "evos": evos, "mtns": mtns,
        "pers": [], "sites": [],
        "prods": [
            {"prod_id": "PROD-001", "item_id": ITEM, "geo_id": f"{GEO}-s02", "name": "铜", "note": "路南州出"},
            {"prod_id": "PROD-002", "item_id": ITEM, "geo_id": f"{GEO}-s01", "name": "铁", "note": "新兴州出"},
            {"prod_id": "PROD-003", "item_id": ITEM, "geo_id": f"{GEO}-c01", "name": "鲌鮮鱼", "note": "河阳县出，一名康郎鱼，云南诸府买为瘴药"},
            {"prod_id": "PROD-004", "item_id": ITEM, "geo_id": f"{GEO}-c03", "name": "青鱼胆", "note": "明湖出，可疗恶疮化痰"},
            {"prod_id": "PROD-005", "item_id": ITEM, "geo_id": f"{GEO}-c03", "name": "毛褐毡茶", "note": "阳宗县出"},
            {"prod_id": "PROD-006", "item_id": ITEM, "geo_id": f"{GEO}-c01", "name": "仙茅", "note": "河阳县出"},
            {"prod_id": "PROD-007", "item_id": ITEM, "geo_id": f"{GEO}-s01", "name": "麝", "note": "新兴州出"},
        ],
        "cits": cits,
    },
    "layer_count": 7,
    "validation": {"errs": [], "gap": 0, "notes": "pers拆至pers2；sites拆至sites1/2"},
    "title": "澂江府",
}
dump(main122, os.path.join(BASE, "vol122", "122-001_澂江府.json"))

# ---- county/department placeholders ----
def placeholder(name, kind, geo_short):
    return {
        "item_id": ITEM, "volume": V, "source": name, "region": REGION,
        "layers": {
            "ents": [{"ent_id": f"ENT-{kind.upper()}", "name": name, "type": "geo",
                      "norm": name, "first_source": ITEM}],
            "geos": [], "evos": [], "mtns": [], "pers": [], "sites": [], "prods": [], "cits": [],
        },
        "layer_count": 7, "title": "澂江府",
    }

dump(placeholder("河阳县", "c01", "c01"), os.path.join(BASE, "vol122", "122-001_c01_河阳县.json"))
dump(placeholder("江川县", "c02", "c02"), os.path.join(BASE, "vol122", "122-001_c02_江川县.json"))
dump(placeholder("阳宗县", "c03", "c03"), os.path.join(BASE, "vol122", "122-001_c03_阳宗县.json"))
dump(placeholder("新兴州", "s01", "s01"), os.path.join(BASE, "vol122", "122-001_s01_新兴州.json"))
dump(placeholder("路南州", "s02", "s02"), os.path.join(BASE, "vol122", "122-001_s02_路南州.json"))

# ---- pers2 人物 ----
pers2 = {
    "item_id": ITEM, "volume": V, "source": "澂江府", "region": REGION,
    "layers": {"ents": [], "geos": [], "evos": [], "mtns": [],
        "pers": [
            {"per_id": "PER-001", "item_id": ITEM, "geo_id": f"{GEO}-c01", "name": "李恢",
             "type": "人物", "dynasty": "三国", "native_place": "俞元人", "office": "庲降都督",
             "summary": "为郡督邮，劾不法；后迎昭烈帝于绵竹，与诸葛亮讨雍闿朱褒，南土平定，恢功居多，封兴亭侯",
             "original": "三国李恢【俞元人为郡督邮始夫爨习为建伶令违法恢正之习免官后迎昭烈帝于绵竹授功曹书佐主簿后为庲降都督与诸葛亮讨雍闿朱褒南土平定恢功居多封兴亭侯】"},
            {"per_id": "PER-002", "item_id": ITEM, "geo_id": f"{GEO}-c01", "name": "段文瑞",
             "type": "人物", "dynasty": "元", "native_place": "河阳人", "office": "临安路总管",
             "summary": "读书奉母尽孝，母没哀痛逾礼，以手履地行一里外负土营坟，百五十日始成；元表其门，授本路学正，官至临安路总管",
             "original": "元段文瑞【河阳人读书奉母尽孝母没哀痛逾礼以手履地行一里外负土营坟百五十日始成元表其门授本路学正官至临安路总管】"},
        ], "sites": [], "prods": [], "cits": []},
    "layer_count": 7, "title": "澂江府",
}
dump(pers2, os.path.join(BASE, "vol122", "122-001_pers2_人物.json"))

# ---- sites1 寺观祠庙 ----
def site(i, geo_id, name, typ, loc, original):
    return {"site_id": f"SITE-{i:03d}", "item_id": ITEM, "geo_id": geo_id,
            "name": name, "type": typ, "location_text": loc,
            "history_lore": loc, "original": original}

sites1 = {
    "item_id": ITEM, "volume": V, "source": "澂江府", "region": REGION,
    "layers": {"ents": [], "geos": [], "evos": [], "mtns": [], "pers": [],
        "sites": [
            site(1, GEO, "华藏寺", "寺观", "在府治北缺摩村",
                 "华藏寺【在府治北缺摩村】"),
            site(2, GEO, "溥照寺", "寺观", "在旸溥山",
                 "溥照寺【在旸溥山】"),
            site(3, f"{GEO}-s02", "正觉寺", "寺观", "在路南州白邑村",
                 "正觉寺【在路南州白邑村】"),
            site(4, GEO, "蟠坤神庙", "祠庙", "在蟠坤山石岩中",
                 "蟠坤神庙【在蟠山石岩中庙久废一日庙址有马迹大如碗平之次日愈多土人复其庙】"),
        ], "prods": [], "cits": []},
    "layer_count": 7, "title": "澂江府",
}
dump(sites1, os.path.join(BASE, "vol122", "122-001_sites1_寺观祠庙.json"))

# ---- sites2 关梁学校 ----
sites2 = {
    "item_id": ITEM, "volume": V, "source": "澂江府", "region": REGION,
    "layers": {"ents": [], "geos": [], "evos": [], "mtns": [], "pers": [],
        "sites": [
            site(5, GEO, "普济桥", "关梁", "在府西北二里", "普济桥【在府西北二里】"),
            site(6, GEO, "清平桥", "关梁", "在府西二里", "清平桥【在府西二里】"),
            site(7, f"{GEO}-c02", "海门桥", "关梁", "在江川县东南八里", "海门桥【在江川县东南八里】"),
            site(8, f"{GEO}-s01", "玉溪桥", "关梁", "在新兴州治西", "玉溪桥【在新兴州治西】"),
            site(9, f"{GEO}-s02", "板桥", "关梁", "在路南州治南", "板桥【在路南州治南】"),
            site(10, GEO, "澂江府学", "学校", "在府治西，元大德间建，本朝洪武十六年重修",
                 "澂江府学【在府治西元大德间定本朝洪武十六年重修】"),
            site(11, f"{GEO}-s01", "新兴州学", "学校", "在州治南，本朝建",
                 "新兴州学【在州治南本朝建】"),
            site(12, f"{GEO}-c02", "江川县学", "学校", "在县治南，本朝建",
                 "江川县学【在县治南本朝建】"),
        ], "prods": [], "cits": []},
    "layer_count": 7, "title": "澂江府",
}
dump(sites2, os.path.join(BASE, "vol122", "122-001_sites2_关梁学校.json"))

# ============================================================
# vol123 蒙化府
# ============================================================
V = "123"
ITEM = "123-001"
GEO = "GEO-123001"

ents123 = [
    {"ent_id": "ENT-001", "name": "蒙化府", "type": "geo", "norm": "蒙化府", "first_source": ITEM},
    {"ent_id": "ENT-W01", "name": "蒙化卫", "type": "geo", "norm": "蒙化卫", "first_source": ITEM},
]

geos123 = [
    {
        "geo_id": GEO, "item_id": ITEM, "name": "蒙化府", "type": "prefecture",
        "region": REGION, "parent": "GEO-000",
        "children": [f"{GEO}-w01"],
        "volume_range": "卷123",
        "attributes": {
            "borders": [
                {"direction": "东", "to_place": "大理府赵州界", "distance_li": 38},
                {"direction": "西", "to_place": "顺宁府界", "distance_li": 150},
                {"direction": "南", "to_place": "楚雄府定远县界", "distance_li": 6},
                {"direction": "北", "to_place": "大理府太和县界", "distance_li": 90},
            ],
            "to_capital": [
                {"capital": "南京", "distance_li": 7970},
                {"capital": "京师", "distance_li": 11410},
            ],
            "households": {"count": 30, "unit": "里", "note": "亲领编户三十里"},
            "grain_tax": {"amount": 4800, "unit": "石", "note": "粮四千八百石零"},
            "jun_name": "阳瓜【唐名】",
            "topography": "四山环堵【郡志诸山拱于前后左右连峰接岫若环堵然】；北距蒙苍襟带西洱【云南志】；南接楚雄北距蹀榆【郡志】",
            "customs": "民善射猎【郡志境内有曰摩察者乃黑爨之别种相传昔从蒙氏细奴逻徙此常执弓药矢遇禽兽则射之鲜不获者然其性犷心很遇强则拒遇弱则劫】；俗变故习【近城居者多僰人男女勤于耕织会饮序齿婚姻必察性行自开设学校以来渐染礼义俗变故习非前代之比】",
            "garrisons": [
                {"name": "蒙化卫", "type": "卫", "location_text": "在府治东洪武三十三年建"},
            ],
        },
        "cit_ids": ["CIT-001", "CIT-002", "CIT-003", "CIT-004", "CIT-005"],
    },
    {"geo_id": f"{GEO}-w01", "item_id": ITEM, "name": "蒙化卫", "type": "weisuo", "region": REGION,
     "parent": GEO, "children": [], "volume_range": "卷123",
     "attributes": {"location_text": "在府治东洪武三十三年建", "garrison_type": "卫"}},
]

evos123 = [
    {"evo_id": "EVO-001", "item_id": ITEM, "geo_id": GEO, "dynasty": "汉", "era": None,
     "institution_name": "益州郡地", "action": "因之", "detail": "汉为益州郡地"},
    {"evo_id": "EVO-002", "item_id": ITEM, "geo_id": GEO, "dynasty": "东汉", "era": None,
     "institution_name": "永昌郡", "action": "因之", "detail": "东汉属永昌郡"},
    {"evo_id": "EVO-003", "item_id": ITEM, "geo_id": GEO, "dynasty": "唐", "era": None,
     "institution_name": "姚州都督府/蒙舍诏", "action": "因之",
     "detail": "唐属姚州都督府；初罗罗摩及僰蛮居此，后蒙氏细逻奴筑城居之，号蒙舍诏，改称南诏"},
    {"evo_id": "EVO-004", "item_id": ITEM, "geo_id": GEO, "dynasty": "唐", "era": "永泰",
     "institution_name": "阳瓜州", "action": "改", "detail": "永泰初改蒙舍城为阳瓜州"},
    {"evo_id": "EVO-005", "item_id": ITEM, "geo_id": GEO, "dynasty": "宋大理", "era": None,
     "institution_name": "开南县", "action": "改", "detail": "宋时段氏改开南县"},
    {"evo_id": "EVO-006", "item_id": ITEM, "geo_id": GEO, "dynasty": "元", "era": "至元",
     "institution_name": "蒙舍千户所/蒙化府/路/州", "action": "改",
     "detail": "元初置蒙舍千户所，至元中改蒙化府寻升为路，后复降为州属大理路"},
    {"evo_id": "EVO-007", "item_id": ITEM, "geo_id": GEO, "dynasty": "明", "era": "正统",
     "institution_name": "蒙化府", "action": "升",
     "detail": "本朝仍为州属大理府，正统间复升为府，亲领编户三十里"},
]

def mtn123(i, name, typ, loc, desc="", lore=""):
    return {"mtn_id": f"MTN-{i:03d}", "item_id": ITEM, "geo_id": GEO,
            "name": name, "type": typ, "location_text": loc, "description": desc, "lore": lore}

mtns123 = [
    mtn123(1, "甸尾山", "山", "在府城东",
           "下有温泉，相传蒙细奴逻母病浴此泉遂愈"),
    mtn123(2, "伏虎山", "山", "在府城东北一十五里"),
    mtn123(3, "巍山", "山", "在府城东南二十里",
           "峰峦高耸冠于群山"),
    mtn123(4, "龙宇图山", "山", "在府城西北三十五里",
           "蒙氏龙伽独自哀牢将其子细奴逻居其上，筑龙宇图城，自立为奇王，号蒙舍诏；今上有浮图及云隐寺"),
    mtn123(5, "石母山", "山", "在府城北七十里",
           "产石黄，下有泉为睒中溪，南入罗盘江"),
    mtn123(6, "阳江", "江", "在府城西",
           "源出甸头涧，过定远县入澜沧江"),
    mtn123(7, "样备江", "江", "在府城西一百五十里",
           "源自剑川州，过大理西洱河入境，南合于澜沧江"),
    mtn123(8, "澜沧江", "江", "在府城西南一百五十里",
           "其南岸有马耳坡"),
]

cits123 = [
    {"cit_id": "CIT-001", "item_id": ITEM, "cited_work": "郡志", "cited_work_ent_id": None,
     "context": "形胜", "original": "【郡志诸山拱于前后左右连峰接岫若环堵然】"},
    {"cit_id": "CIT-002", "item_id": ITEM, "cited_work": "云南志", "cited_work_ent_id": None,
     "context": "形胜", "original": "【云南志北距蒙苍襟带西洱】"},
    {"cit_id": "CIT-003", "item_id": ITEM, "cited_work": "郡志", "cited_work_ent_id": None,
     "context": "形胜", "original": "【郡志南接楚雄北距蹀榆】"},
    {"cit_id": "CIT-004", "item_id": ITEM, "cited_work": "郡志", "cited_work_ent_id": None,
     "context": "风俗", "original": "【郡志境内有曰摩察者乃黑爨之别种相传昔从蒙氏细奴逻徙此常执弓药矢遇禽兽则射之鲜不获者然其性犷心很遇强则拒遇弱则劫】"},
    {"cit_id": "CIT-005", "item_id": ITEM, "cited_work": "郡志", "cited_work_ent_id": None,
     "context": "风俗", "original": "【近城居者多僰人男女勤于耕织会饮序齿婚姻必察性行自开设学校以来渐染礼义俗变故习非前代之比】"},
]

main123 = {
    "item_id": ITEM, "volume": V, "source": "蒙化府", "region": REGION,
    "layers": {
        "ents": ents123, "geos": geos123, "evos": evos123, "mtns": mtns123,
        "pers": [], "sites": [],
        "prods": [
            {"prod_id": "PROD-001", "item_id": ITEM, "geo_id": GEO, "name": "铁", "note": "府境出"},
            {"prod_id": "PROD-002", "item_id": ITEM, "geo_id": GEO, "name": "石黄", "note": "石母山出"},
            {"prod_id": "PROD-003", "item_id": ITEM, "geo_id": GEO, "name": "麝", "note": "府境出"},
            {"prod_id": "PROD-004", "item_id": ITEM, "geo_id": GEO, "name": "椒", "note": "府境出"},
            {"prod_id": "PROD-005", "item_id": ITEM, "geo_id": GEO, "name": "斑竹", "note": "府境出"},
            {"prod_id": "PROD-006", "item_id": ITEM, "geo_id": GEO, "name": "箭竹", "note": "府境出"},
        ],
        "cits": cits123,
    },
    "layer_count": 7,
    "validation": {"errs": [], "gap": 0, "notes": "亲领无属县；pers拆至pers2；sites拆至sites1/2"},
    "title": "蒙化府",
}
dump(main123, os.path.join(BASE, "vol123", "123-001_蒙化府.json"))

# w01 placeholder
w01 = {
    "item_id": ITEM, "volume": V, "source": "蒙化卫", "region": REGION,
    "layers": {"ents": [{"ent_id": "ENT-W01", "name": "蒙化卫", "type": "geo",
                         "norm": "蒙化卫", "first_source": ITEM}],
               "geos": [], "evos": [], "mtns": [], "pers": [], "sites": [], "prods": [], "cits": []},
    "layer_count": 7, "title": "蒙化府",
}
dump(w01, os.path.join(BASE, "vol123", "123-001_w01_蒙化卫.json"))

# pers2
pers2_123 = {
    "item_id": ITEM, "volume": V, "source": "蒙化府", "region": REGION,
    "layers": {"ents": [], "geos": [], "evos": [], "mtns": [],
        "pers": [
            {"per_id": "PER-001", "item_id": ITEM, "geo_id": GEO, "name": "张彦成",
             "type": "人物", "dynasty": "唐", "native_place": "蒙舍川人", "office": "",
             "summary": "南诏蒙晟逻皮遣彦成使于唐，礼待甚厚，赐以浮屠像以归；南中事佛自兹始",
             "original": "唐张彦成【蒙舍川人南诏蒙晟逻皮遣彦成使于唐礼待甚厚赐以浮屠像以归南中事佛自兹始】"},
        ], "sites": [], "prods": [], "cits": []},
    "layer_count": 7, "title": "蒙化府",
}
dump(pers2_123, os.path.join(BASE, "vol123", "123-001_pers2_人物.json"))

# sites1 寺观祠庙
def site123(i, name, typ, loc, original):
    return {"site_id": f"SITE-{i:03d}", "item_id": ITEM, "geo_id": GEO,
            "name": name, "type": typ, "location_text": loc,
            "history_lore": loc, "original": original}

sites1_123 = {
    "item_id": ITEM, "volume": V, "source": "蒙化府", "region": REGION,
    "layers": {"ents": [], "geos": [], "evos": [], "mtns": [], "pers": [],
        "sites": [
            site123(1, "等觉寺", "寺观", "在府治东，蒙氏建",
                    "等觉寺【在府治东蒙氏建】"),
            site123(2, "伏虎寺", "寺观", "在伏虎山，蒙氏时有西域僧俱卢与南国僧道葺役二虎拽本以创寺，寺成乘二虎而去",
                    "伏虎寺【在伏虎山蒙氏时有西域僧俱卢你与南国僧道葺役二虎拽本以创寺寺成乗二虎而去】"),
            site123(3, "玄珠观", "寺观", "在府城东，前有莲池构亭其上以为游赏之所",
                    "玄珠观【在府城东前有莲池构亭其上以为游赏之所】"),
            site123(4, "嵯岈武宣王庙", "祠庙", "在府治东南，祀蒙氏十三代孙名法者，土人祈祷有应",
                    "嵯岈武宣王庙【在府治东南祀蒙氏十三代孙名法者土人祈祷有应】"),
        ], "prods": [], "cits": []},
    "layer_count": 7, "title": "蒙化府",
}
dump(sites1_123, os.path.join(BASE, "vol123", "123-001_sites1_寺观祠庙.json"))

# sites2 关梁学校
sites2_123 = {
    "item_id": ITEM, "volume": V, "source": "蒙化府", "region": REGION,
    "layers": {"ents": [], "geos": [], "evos": [], "mtns": [], "pers": [],
        "sites": [
            site123(5, "蒙城桥", "关梁", "在府治西", "蒙城桥【在府治西】"),
            site123(6, "甸头桥", "关梁", "在府城北六十五里", "甸头桥【在府城北六十五里】"),
            site123(7, "样备桥", "关梁", "在府城西北一十五里", "样备桥【在府城西北一十五里】"),
            site123(8, "蒙化府学", "学校", "在府治东南，旧为州学，景泰元年改建",
                    "蒙化府学【在府治东南旧为州学景泰元年改建】"),
        ], "prods": [], "cits": []},
    "layer_count": 7, "title": "蒙化府",
}
dump(sites2_123, os.path.join(BASE, "vol123", "123-001_sites2_关梁学校.json"))

print("DONE")
