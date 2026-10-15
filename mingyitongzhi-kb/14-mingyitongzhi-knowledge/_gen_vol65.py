# -*- coding: utf-8 -*-
"""Generate vol65 襄阳府 JSON files."""
import json, os

BASE = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol65"
ITEM = "65-001"
VOL = "65"
PREF = "襄阳府"
REGION = "湖广"

def dump(obj, fname):
    p = os.path.join(BASE, fname)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  {fname}: {os.path.getsize(p)} bytes")

# ---------- GEO tree ----------
GEO_ID = "GEO-65001"
children = [
    "GEO-65001-c01","GEO-65001-c02","GEO-65001-c03","GEO-65001-c04",
    "GEO-65001-c05","GEO-65001-c06","GEO-65001-s01",
    "GEO-65001-w01","GEO-65001-w02","GEO-65001-w03"
]

geo_pref = {
    "geo_id": GEO_ID, "item_id": ITEM, "name": PREF, "type": "prefecture",
    "region": REGION, "parent": "GEO-000", "children": children,
    "volume_range": "卷65",
    "attributes": {
        "borders": [
            {"direction":"东","to_place":"德安府随州界","distance_li":210},
            {"direction":"西","to_place":"陕西汉中府平利县界","distance_li":1000},
            {"direction":"南","to_place":"承天府荆门州界","distance_li":180},
            {"direction":"北","to_place":"河南南阳府新野县界","distance_li":90}
        ],
        "to_capital": [
            {"capital":"南京","distance_li":3700},
            {"capital":"京师","distance_li":6867}
        ],
        "households": {"count": None, "unit":"里", "note":"领州一县六；各属编户见下；粮六万三千七百石零"},
        "jun_name": "襄阳【魏名】",
        "topography": "跨连荆蜀控扼南北【本朝实录】；外带江汉内阻山陵【吴鲁肃说孙权云】；水陆之冲御寇要地【魏司马懿云】；挟大汉以为池面崇山以为固【晋顺阳国碑】；檀溪带其西岘山亘其南【晋习凿齿云】；北接宛许南阻汉水【晋庾亮表】；南极湖湘北控关洛【宋陈亮传】；东连汉沔西彻梁洋【均州志】",
        "customs": "江汉之俗好游【毛诗】；其民尚文其俗尚侈【襄阳图志】；尚礼义经籍【隋志】；其俗朴陋【旧图经】；信巫鬼重淫祀【均州地理志】；人民朴野【宋陆恺均州宗海楼记】；俗好楚歌【宋晏殊类要】；劲悍决烈兼秦楚之俗【宋范子长郡县志】；居室多编竹代陶瓦【郡志】",
        "garrisons": [
            {"name":"襄阳卫","type":"卫","location_text":"在府治西南正统初建"},
            {"name":"襄阳护卫","type":"卫","location_text":"在府城内天顺初为襄府置"},
            {"name":"均州守御前千户所","type":"千户所","location_text":"在州治东南"}
        ]
    },
    "cit_ids": ["CIT-001","CIT-002","CIT-003","CIT-004","CIT-005","CIT-006","CIT-007","CIT-008","CIT-009","CIT-010","CIT-011","CIT-012","CIT-013","CIT-014"]
}

counties = [
    ("c01","襄阳县","county","GEO-65001-c01","附郭",35,"编户三十五里"),
    ("c02","宜城县","county","GEO-65001-c02","在府城东南一百二十里",17,"编户一十七里"),
    ("c03","南漳县","county","GEO-65001-c03","在府城西南一百二十里",35,"编户三十五里"),
    ("c04","枣阳县","county","GEO-65001-c04","在府城东北一百四十里",45,"编户四十五里"),
    ("c05","谷城县","county","GEO-65001-c05","在府城西一百八十里",45,"编户四十五里"),
    ("c06","光化县","county","GEO-65001-c06","在府城西北一百八十里",37,"编户三十七里"),
]

depts = [
    ("s01","均州","department","GEO-65001-s01","在府城西北三百九十里",29,"编户二十九里"),
]

weis = [
    ("w01","襄阳卫","GEO-65001-w01","在府治西南正统初建","卫"),
    ("w02","襄阳护卫","GEO-65001-w02","在府城内天顺初为襄府置","卫"),
    ("w03","均州守御前千户所","GEO-65001-w03","在州治东南","千户所"),
]

geo_nodes = [geo_pref]
for code,name,typ,gid,loc,hcount,hnote in counties+depts:
    geo_nodes.append({
        "geo_id": gid, "item_id": ITEM, "name": name, "type": typ,
        "region": REGION, "parent": GEO_ID, "children": [],
        "volume_range": "卷65",
        "attributes": {"location_text": loc, "households": {"count": hcount, "unit":"里", "note": hnote}}
    })
for code,name,gid,loc,gt in weis:
    geo_nodes.append({
        "geo_id": gid, "item_id": ITEM, "name": name, "type": "weisuo",
        "region": REGION, "parent": GEO_ID, "children": [],
        "volume_range": "卷65",
        "attributes": {"location_text": loc, "garrison_type": gt}
    })

# ---------- Evo ----------
evos = [
    {"evo_id":"EVO-001","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"夏","era":None,"institution_name":"荆豫二州之域","action":"因之","detail":"禹贡荆豫二州之域，天文翼轸分野"},
    {"evo_id":"EVO-002","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"周","era":None,"institution_name":"谷邓鄾卢罗鄀之地","action":"因之","detail":"周为谷邓鄾卢罗鄀之地"},
    {"evo_id":"EVO-003","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"春秋战国","era":None,"institution_name":"楚地","action":"属","detail":"春秋时属楚"},
    {"evo_id":"EVO-004","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"秦","era":None,"institution_name":"南郡南阳郡地","action":"置","detail":"秦为南郡南阳郡地"},
    {"evo_id":"EVO-005","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"汉","era":None,"institution_name":"南郡南阳郡地","action":"因之","detail":"汉因之"},
    {"evo_id":"EVO-006","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"东汉末","era":None,"institution_name":"荆州治","action":"徙治","detail":"东汉末刘表为荆州刺史徙治襄阳县"},
    {"evo_id":"EVO-007","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"三国魏","era":None,"institution_name":"襄阳郡","action":"置","detail":"魏始置襄阳郡治宜城，以地在襄水之阳故名"},
    {"evo_id":"EVO-008","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"晋","era":None,"institution_name":"荆州治/雍州","action":"侨置","detail":"晋亦为荆州治所，东晋于襄阳侨置雍州"},
    {"evo_id":"EVO-009","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"梁","era":None,"institution_name":"南雍州","action":"置","detail":"梁置南雍州"},
    {"evo_id":"EVO-010","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"西魏","era":None,"institution_name":"襄州","action":"改","detail":"西魏改曰襄州"},
    {"evo_id":"EVO-011","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"隋","era":"大业","institution_name":"襄阳郡","action":"复置","detail":"隋初郡废州存，立山南道行台并总管府，帝时州府并罢，复置襄阳郡治襄阳县"},
    {"evo_id":"EVO-012","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"唐","era":None,"institution_name":"襄州/山南东道","action":"改","detail":"唐初复置襄州为山南东道治，后为襄阳郡又为襄阳府复为襄州"},
    {"evo_id":"EVO-013","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"五代","era":None,"institution_name":"忠义军","action":"置","detail":"五代梁唐置忠义军"},
    {"evo_id":"EVO-014","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"宋","era":None,"institution_name":"襄阳府","action":"复","detail":"宋复为襄阳府"},
    {"evo_id":"EVO-015","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"元","era":None,"institution_name":"襄阳路","action":"改","detail":"元改为襄阳路"},
    {"evo_id":"EVO-016","item_id":ITEM,"geo_id":GEO_ID,"dynasty":"明","era":None,"institution_name":"襄阳府","action":"复","detail":"本朝复为襄阳府，领州一县六"},
]

# ---------- Mtn ----------
# (name, type, loc, desc, lore, geo_suffix)
# geo_suffix: c01..c06, s01, or GEO_ID for prefecture-level
M = []
def m(name, typ, loc, desc, lore, g):
    M.append({"mtn_id": f"MTN-{len(M)+1:03d}", "item_id": ITEM,
              "geo_id": g, "name": name, "type": typ,
              "location_text": loc, "description": desc, "lore": lore})

C1="GEO-65001-c01"; C2="GEO-65001-c02"; C3="GEO-65001-c03"; C4="GEO-65001-c04"; C5="GEO-65001-c05"; C6="GEO-65001-c06"; S1="GEO-65001-s01"; P=GEO_ID

m("襄山","山","在府城西五里","","",C1)
m("紫盖山","山","在府城西北五里","宋时改名中岘山","",C1)
m("虎头山","山","在府城南五里","元阿珠过襄阳尝驻马此山，指汉东白河口曰若筑垒于此襄阳粮道可断也，后遂筑鹿门新城等堡","",C1)
m("凤山","山","在府城南五里","唐书孟浩然传云楚泽曾为刻碑凤林山南即此","",C1)
m("岘山","山","在府城南七里","晋羊祜每登此山置酒，尝谓从事邹湛曰自有宇宙便有此山，由来贤哲登此者多矣皆湮灭无闻。湛对曰公德冠四海闻望当与此山俱传。祜殁襄人感其德立祠刻碑其上，见者莫不流涕","唐孟浩然诗人事有代谢往来成古今江山留胜迹我辈复登临水落鱼梁浅天寒梦泽深羊公碑尚在读罢一沾巾",C1)
m("柳子山","山","在府城北七里","檀水出其下，又有柳子水，梁简文为州日泛舟穷柳子之源","",C1)
m("望楚山","山","在府城西南八里","旧有三名曰楚山马鞍山防山，图经秦与齐韩魏攻楚方城，秦军登山以望楚因名。一云宋武陵王骏屡登陟以望见鄢城改今名","晋刘弘山简九日尝登高于此",C1)
m("万山","山","在府城西一十里","旧与南郡邓县分界，相传郑交甫所见游女处此山之下曲隈是也","襄沔记以紫盖山万山岘山谓之三岘",C1)
m("卧龙山","山","在府城南一十里","下有高阳池","",C1)
m("白马山","山","在府城东南一十里","山有白马泉故名","南雍州记每年刺史三月三日禊饮于此",C1)
m("谷隐山","山","在府城东南一十三里","晋习凿齿隐遁处，一作谷隐，旧有紫金寺","",C1)
m("隆中山","山","在府城西北二十五里","下有隆中书院","汉诸葛亮尝隐于此",C1)
m("独乐山","山","在府城西北二十八里","","诸葛亮尝登此",C1)
m("百丈山","山","在府城南三十里","旧传有麝香兽栖止，刘表遣人采药遇坎穴得麝香数斗如石莲，馨香芬馥非世所有","元兵逼襄阳，宋来兴国以百艘侵百丈山即此",C1)
m("鹿门山","山","在府城东南二十里","旧名苏岭，上有二石鹿因改今名","汉庞德公唐庞蕴孟浩然皮日休俱隐居于此",C1)
m("伏龙山","山","在府城西南三十里","","宋曾巩守郡日祷雨数应",C1)
m("太岳太和山","山","在均州南一百二十里","山有二十七峰三十六岩二十四洞五台五井三泉三潭。初名仙室山，又名太岳山。真武奉元君之言游览至此改名太和。其中一峰最高者旧为天柱峰亦曰紫霄峰，岩曰紫霄岩。后人谓非玄武不足以当之又更名武当山","本朝永乐中营建宫馆一新复改今名",S1)
m("石阶山","山","在太和山","一名华岳地肺，一名肺山福地，有救穷草冬夏不枯，月食三寸绝谷不饥","",S1)
m("女思山","山","在太和山","汉来歙曾孙女嫁为河内张德子妇，随夫还至此山南望其父母，思慕而死遂葬于此","",S1)
m("外朝山","山","在太和山后","诸山皆朝拱太和山，唯此山外向","",S1)
m("鸡鸣山","山","在太和山之西","","",S1)
m("牛头山","山","在均州城东北五十里","其山高险，昔人曾于此置关，上有一石形如油瓶名油瓶关","",S1)
m("大观山","山","俱在均州东南汉江中","","",S1)
m("小观山","山","俱在均州东南汉江中","","",S1)
m("五车山","山","在宜城县东北二十里","俗传有庞居士舁金弃此山下","",C2)
m("石梁山","山","在宜城县西三十里","形似桥梁","上有庞德公祠",C2)
m("赤山","山","在宜城县东南八十里","土石皆赤，下有深潭","相传周吕望尝钓于此名钓鱼洞",C2)
m("清溪山","山","在南漳县临沮城界内","其山高峻，东有泉","晋郭璞为临沮长尝游此赋诗云清溪千余仞中有一道士",C3)
m("十望山","山","在南漳县北一十五里","","",C3)
m("舞旗山","山","在南漳县东二十里","","",C3)
m("四望山","山","在南漳县南三十里","东望襄阳西望房县南望荆州北望谷城皆见故名，一名太府山","",C3)
m("老鸦山","山","在南漳县南五十里","上接文阳洞下接三泉山，周回四十余里，洞险峻幽深人不可近","相传龙神所居，祷雨有应",C3)
m("八叠山","山","在南漳县西六十里","晋司马懿凿山开道屈曲八叠因名","",C3)
m("羊角山","山","在南漳县西一百二十里","","",C3)
m("司空山","山","在南漳县西一百三十里","","",C3)
m("鸡头山","山","在南漳县西一百八十里","北临漳水，一名临漳山","",C3)
m("荆山","山","在南漳县西北八十里","山三面险绝惟西南一隅通人径。山海经曰其阳多铁其阴多赤金。山顶有池旁有石室","相传卞和宅，上有抱玉岩",C3)
m("狮子山","山","在枣阳县南四十里","","上有汉光武庙",C4)
m("甘泉山","山","在枣阳县东北四十里","地肥而水甘故名","",C4)
m("武王山","山","在枣阳县东五十里","世传楚武王尝猎此，又名霸山","",C4)
m("资山","山","在枣阳县东南六十里","其上深邃阔远可以耕种，修篁大木环山之民皆资焉故名","",C4)
m("椒山","山","在枣阳县东北六十里","","上有寺",C4)
m("瀴源山","山","在枣阳县南七十里","山有二石名东西石虎","",C4)
m("赤眉山","山","在枣阳县西北八十里","","相传赤眉尝军此山下地名北寨",C4)
m("谷山","山","在谷城县西北一十里","有古谷城即春秋谷伯绥旧国","又有谷神山在县西一十里上有石城",C5)
m("屏风山","山","在谷城县北九十里","","昔白玉仙人得素书于此",C5)
m("薤山","山","在谷城县西南六十里","山有孤竹三茎三年生一笋，笋就竹死代谢不已","每诸山云起此山无云终不雨，土人以为验",C5)
m("马窟山","山","在光化县东五里","中有石窟，相传汉时有马数百匹从此窟出，形小似巴滇马","三国时吴陆逊攻襄阳又值北穴有马数十匹出逊载还建业，蜀使来有兵家滇池者识其马色云亡父所乘对之流涕",C6)
m("固封山","山","在光化县西北一十里","山之东旧为晋顺阳王城，本名崇山","唐改今名",C6)
m("三夫人峰","峰","在均州南","状若博山香炉","",S1)
m("谢公岩","岩","在府城西南五里","","昔谢希逸游此故名",C1)
m("书字崖","崖","在均州北五里","其崖高峻上有字刻","",S1)
m("九十九冈","冈","在枣阳县东","","宋邢居实诗岐路剧羊肠重冈九十九",C4)
m("圣人洞","洞","在府城南二十里","","唐贞观间见一翁游此形服异常故名",C1)
m("仙女洞","洞","有二，一在府城西北三十里","","一在南漳县西南五里抱玉岩东",C1)
m("黄龙洞","洞","在府城南三十里","","",C1)
m("圣马洞","洞","在南漳县治西南","有石室可容二三十人","旧传有白马饮水其中",C3)
# Waters
m("汉江","江","源出陇西嶓冢山由汉中流经郧县均州光化至府城北又东南经宜城抵安陆州至大别山入于江","其水因地而名曰漾曰沔曰汉曰沧浪，盖总名为汉别言之则有四耳","唐杜审言诗楚山横地出汉水接天回；元诗嶓冢去年寻漾水襄阳今日渡江濆",P)
m("清泥河","河","在府城西北源出均房","","宋末以襄阳受围五年即其地造轻舟百艘",C1)
m("白河","河","在府城东北源出南阳府鄀州界下入汉江","","",C1)
m("唐河","河","在府城东北一百里源出唐县入汉江","","",C1)
m("曾河","河","在均州南六里源出太和山东流经城南入汉江","","州东南七十里又有浪河源亦出太和山东流入汉江",S1)
m("清凉河","河","在南漳县东一十二里源出西溪洞与蛮河合","","",C3)
m("漳河","河","在南漳县南一百三十里","其水由当阳境入汉江","",C3)
m("滚河","河","在枣阳县西南合白河入汉江","","",C4)
m("泌河","河","在光化县东南流至府界与白河相合入汉江","","",C6)
m("蛮河","水","发源自房县界经南漳入宜城西南六十里入汉江","","桓温避父讳改名夷水",C3)
m("鸭湖","湖","在襄阳县","","汉昭烈乘的卢越檀溪曾经此",C1)
m("襄水","水","在府城西北源出柳子山北流为檀溪南流为襄水又名涑水","荆州记云水中有物如马甲如鲜鲤，七八月中好在碛上自曝，膝头似虎掌爪，小儿不知欲取戏弄便杀人","",C1)
m("均水","水","在均州前","","汉地理志丹水东流入均水",S1)
m("沧浪水","水","在均州北四十里","即禹贡沧浪之水","",S1)
m("潮水","水","在南漳县西一百里","其水一日一潮","",C3)
m("浕水","水","在枣阳县南源出浕山","","汉张衡南都赋屏澧泺浕是也",C4)
m("瀴水","水","在枣阳县东西流入汉","","西魏置瀴源县以此名",C4)
m("檀溪","溪","在府城西四里","","汉昭烈乘的卢西走至此溪一跃而过；梁武帝镇荆州潜造器械伐竹木沉檀溪为舟装之备即此处，今已涸",C1)
m("磨针涧","涧","在太和山北","真武修炼久之未契，玄元亟欲出山至此涧，忽遇老妪操铁杵磨石上，问磨此何为，妪曰为针耳，曰不亦难乎，妪曰功至自成。真武大悟即返岩精修卒得上道","因名曰磨针涧",S1)
m("沉碑潭","潭","在万山下潭中","晋杜预南征纪功勒为二碑，一立万山上一沉万山下潭中","唐鲍溶诗襄阳太守沉碑意身后身前几年事",C1)
m("昭王井","井","在宜城县","","唐韩愈宜城驿记井北有楚昭王庙",C2)
m("王粲井","井","有二，一在万山东","粲有故宅在焉","唐杜甫诗吾家碑不昧王氏井依然；一在习池上，宋孙信臣诗王粲初开井山翁旧醉池",C1)
m("葛井","井","在府城西","","荆州记诸葛亮宅有井",C1)
m("龙井","井","在太和山","","",S1)
m("甘露井","井","在太和山南岩宫前","","",S1)
m("甘泉","泉","有二，一在府城西南七里","","一在太和山后",C1)
m("饮马泉","泉","在府城西南一十里","","旧传关羽尝饮马于此",C1)
m("金泉","泉","在均州治","","宋王齐作记",S1)
m("白花泉","泉","在太和山","","",S1)
m("参斗泉","泉","在均州东","其水汲之虽干人不减不汲亦不增","相传参斗二星下临因名",S1)
m("金沙泉","泉","在宜城县东","其水造酒甘美，世谓宜城春又名竹叶春，久湮塞","",C2)
m("珍珠泉","泉","在宜城县东七十里流入汉江","","",C2)
m("一碗泉","泉","在南漳县西三百里歇马庙傍石上有坎仅容水一碗取之不竭","","",C3)
m("温水泉","泉","在光化县南五里一名温水河","旧有一泉其水温暖今塞河尚存","",C6)
m("习家池","池","在府城南八里","后汉习郁尝穿此池依范蠡养鱼法，中筑钓台。临殁谓其子曰必葬我近鱼池","山简镇襄阳每出游多之池上置酒辄醉名之曰高阳池；宋曾巩诗未脱迂疏笑山简更须同上习池游",C1)
m("黑龙池","池","在府城东五里水深而碧","","唐牛僧儒尝祷雨于此",C1)
m("濯笔池","池","在府城南虎头山","","相传汉昭烈濯笔于此",C1)
m("盐池","池","在太和山东南一百里","水气袭于草上如盐","",S1)
m("珍珠池","池","在南漳县北三十里双池寺内","人于地傍蹴呼则四围水涌跳如珠","",C3)
m("石羊池","池","在枣阳县南三里","池上有石如卧羊","",C4)
m("莲花池","池","有三，一在枣阳县西南二十里","","一在县东三里霍山顶；一在均州城西南五里，皆种莲",C4)
m("蔡子池","池","在枣阳县蔡伦宅傍","","宋王安石诗波工龟手诧今样鱼网肯数荆州池",C4)
m("木里沟","沟","在宜城县","后汉王宠为刺史凿广水与木里沟灌田六千顷","宋县令陈表臣复修以广灌溉，起水门四十六通旧陂四十有九",C2)
m("长渠","渠","在宜城县西","荆及康狼楚之西山水出二山之间曰沔水，楚屈瑕伐罗及鄢乱次以济是也。秦白起攻楚去鄢百里立碣壅是水为渠以灌鄢遂拔楚都","宋曾巩有长渠记",C2)
m("蔡洲","洲","在府城东北汉水中","","后汉蔡瑁居其上，曹操尝造其家",C1)
m("斩蛟渚","渚","在府城北沔水","先有蛟为患，汉邓遐守襄拔剑入水，蛟绕其足，遐挥剑斩之，自此无蛟患","",C1)
m("解佩渚","渚","在府城西一千里","","昔郑交甫游于江汉之渚遇湘妃二女解佩玉赠之即此处；宋颜荛诗爽籁尽成鸣凤曲游人多是弄珠仙",C1)
m("白公湍","湍","","秦白起伐楚涉此水因名","",P)
m("袁曹渡","渡","在谷城县","","曹操袁术争渡于此",C5)

print(f"MTN count: {len(M)}")

# ---------- Cits ----------
cits = [
    {"cit_id":"CIT-001","item_id":ITEM,"cited_work":"本朝实录","cited_work_ent_id":None,"context":"形胜","original":"【本朝实录跨连荆蜀控扼南北】"},
    {"cit_id":"CIT-002","item_id":ITEM,"cited_work":"吴鲁肃说孙权","cited_work_ent_id":None,"context":"形胜","original":"【吴鲁肃说孙权云外带江汉内阻山陵】"},
    {"cit_id":"CIT-003","item_id":ITEM,"cited_work":"魏司马懿","cited_work_ent_id":None,"context":"形胜","original":"【魏司马懿云水陆之冲御寇要地】"},
    {"cit_id":"CIT-004","item_id":ITEM,"cited_work":"晋顺阳国碑","cited_work_ent_id":None,"context":"形胜","original":"【晋顺阳国碑挟大汉以为池面崇山以为固】"},
    {"cit_id":"CIT-005","item_id":ITEM,"cited_work":"晋习凿齿","cited_work_ent_id":None,"context":"形胜","original":"【晋习凿齿云檀溪带其西岘山亘其南】"},
    {"cit_id":"CIT-006","item_id":ITEM,"cited_work":"晋庾亮表","cited_work_ent_id":None,"context":"形胜","original":"【晋庾亮表北接宛许南阻汉水】"},
    {"cit_id":"CIT-007","item_id":ITEM,"cited_work":"宋陈亮传","cited_work_ent_id":None,"context":"形胜","original":"【宋陈亮传南极湖湘北控关洛】"},
    {"cit_id":"CIT-008","item_id":ITEM,"cited_work":"均州志","cited_work_ent_id":None,"context":"形胜","original":"【均州志东连汉沔西彻梁洋】"},
    {"cit_id":"CIT-009","item_id":ITEM,"cited_work":"毛诗","cited_work_ent_id":None,"context":"风俗","original":"【毛诗汉有游女传云江汉之俗其女好游汉魏以后犹然如大堤之曲可见也】"},
    {"cit_id":"CIT-010","item_id":ITEM,"cited_work":"襄阳图志","cited_work_ent_id":None,"context":"风俗","original":"【襄阳图志其民尚文其俗尚侈宋玉王逸张梯习凿齿之徒实生此土故其民尚文北鱼南徐之习不替故其俗尚侈】"},
    {"cit_id":"CIT-011","item_id":ITEM,"cited_work":"隋志","cited_work_ent_id":None,"context":"风俗","original":"【隋志襄阳四方凑防故益多衣冠之绪稍尚礼义经籍焉】"},
    {"cit_id":"CIT-012","item_id":ITEM,"cited_work":"均州地理志","cited_work_ent_id":None,"context":"风俗","original":"【均州地理志信巫鬼重淫祀】"},
    {"cit_id":"CIT-013","item_id":ITEM,"cited_work":"宋陆恺均州宗海楼记","cited_work_ent_id":None,"context":"风俗","original":"【宋陆恺均州宗海楼记人民朴野】"},
    {"cit_id":"CIT-014","item_id":ITEM,"cited_work":"宋范子长郡县志","cited_work_ent_id":None,"context":"风俗","original":"【宋范子长郡县志劲悍决烈兼秦楚之俗】"},
]

# ---------- Ents ----------
ents = [
    {"ent_id":"ENT-001","name":PREF,"type":"geo","norm":PREF,"first_source":ITEM},
]
for i,(code,name,*_ ) in enumerate(counties,1):
    ents.append({"ent_id":f"ENT-C{i:02d}","name":name,"type":"geo","norm":name,"first_source":ITEM})
for i,(code,name,*_) in enumerate(depts,1):
    ents.append({"ent_id":f"ENT-S{i:02d}","name":name,"type":"geo","norm":name,"first_source":ITEM})
for i,(code,name,*_) in enumerate(weis,1):
    ents.append({"ent_id":f"ENT-W{i:02d}","name":name,"type":"geo","norm":name,"first_source":ITEM})

# ---------- Main file ----------
main = {
    "item_id": ITEM, "volume": VOL, "source": PREF, "region": REGION,
    "layers": {
        "ents": ents,
        "geos": geo_nodes,
        "evos": evos,
        "mtns": M,
        "pers": [],
        "sites": [],
        "prods": [],
        "cits": cits
    },
    "layer_count": 7,
    "validation": {"errs":[],"gap":0,"notes":"pers拆至pers1/2/3；sites拆至sites1/2"},
    "title": PREF
}
dump(main, f"{ITEM}_{PREF}.json")

# ---------- County/dept/weisuo placeholder files ----------
for code,name,typ,gid,loc,hcount,hnote in counties:
    n = int(code[1:])
    obj = {
        "item_id": ITEM, "volume": VOL, "source": name, "region": REGION,
        "layers": {
            "ents": [{"ent_id":f"ENT-c{n:02d}","name":name,"type":"geo","norm":name,"first_source":ITEM}],
            "geos": [], "evos": [], "mtns": [], "pers": [], "sites": [], "prods": [], "cits": []
        },
        "layer_count": 7, "title": PREF
    }
    dump(obj, f"{ITEM}_{code}_{name}.json")

for code,name,typ,gid,loc,hcount,hnote in depts:
    n = int(code[1:])
    obj = {
        "item_id": ITEM, "volume": VOL, "source": name, "region": REGION,
        "layers": {
            "ents": [{"ent_id":f"ENT-s{n:02d}","name":name,"type":"geo","norm":name,"first_source":ITEM}],
            "geos": [], "evos": [], "mtns": [], "pers": [], "sites": [], "prods": [], "cits": []
        },
        "layer_count": 7, "title": PREF
    }
    dump(obj, f"{ITEM}_{code}_{name}.json")

for code,name,gid,loc,gt in weis:
    n = int(code[1:])
    obj = {
        "item_id": ITEM, "volume": VOL, "source": name, "region": REGION,
        "layers": {
            "ents": [{"ent_id":f"ENT-W{n:02d}","name":name,"type":"geo","norm":name,"first_source":ITEM}],
            "geos": [], "evos": [], "mtns": [], "pers": [], "sites": [], "prods": [], "cits": []
        },
        "layer_count": 7, "title": PREF
    }
    dump(obj, f"{ITEM}_{code}_{name}.json")

print("vol65 base files done.")
