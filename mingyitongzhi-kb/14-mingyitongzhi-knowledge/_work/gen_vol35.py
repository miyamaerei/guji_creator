# -*- coding: utf-8 -*-
import json, os

OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol35"
os.makedirs(OUT, exist_ok=True)

def dump(name, obj):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    sz = os.path.getsize(p)
    print(f"{name}: {sz} bytes")
    return sz

# ============================================================
# 平凉府 35-001
# ============================================================
PJ = "35-001"
GJ = "GEO-35001"

# --- geos ---
geos_pj = [
 {"geo_id":GJ,"item_id":PJ,"name":"平凉府","type":"prefecture","region":"陕西","parent":"GEO-000",
  "children":[f"{GJ}-c01",f"{GJ}-c02",f"{GJ}-c03",f"{GJ}-c04",f"{GJ}-s01",f"{GJ}-s02",f"{GJ}-s03",
              f"{GJ}-w01",f"{GJ}-w02",f"{GJ}-w03"],
  "volume_range":"卷35",
  "attributes":{
    "borders":[
      {"direction":"东","to_place":"西安府邠州界","distance_li":220},
      {"direction":"南","to_place":"凤翔府陇州界","distance_li":240},
      {"direction":"西","to_place":"巩昌府会宁县界","distance_li":410},
      {"direction":"北","to_place":"庆阳府环县界","distance_li":290}],
    "to_capital":[
      {"capital":"京师","distance_li":3400},
      {"capital":"南京","distance_li":3180}],
    "households":{"count":None,"unit":"里","note":"领州三县七；各属州县编户见下"},
    "grain_tax":{"amount":150000,"unit":"石","note":"粮一十五万石零"},
    "jun_name":"安定【汉名】泾原【宋名】",
    "topography":"山川秀拔【国经秦陇之地以山立郭平凉山川最为秀拔】；中华襟带【文献通考镇戎军山川险阻旁扼夷落为中华襟带】；水土杂于河西人烟接于北地【寰宇记】；外边羌夏【原州防壁记郡介于泾原环庆之间而外边羌夏】；襟带西凉咽喉灵武【宋郑文宅城萧关议】；左控五原右带兰会黄流在其北崆峒阻其南【元开成志】；控制西垂实为要地【金胥鼎云】；陇水环流绕带河渭【德顺州志】",
    "customs":"婚姻丧葬颇近古风【郡志平凉民俗醇厚不尚侈靡专业耕种不为寇盗其婚姻丧葬颇近古风】；士尚气略人以骑射为先【同上】；质朴尚勇穴处者多【镇原志】；女工机织男多游手【开城志】；好猎务农民淳易化【静宁州志】；被文王之化而风俗美【方舆枢要泾州古密须之国被文王之化而风俗美】",
    "garrisons":[
      {"name":"陕西行太仆寺","type":"寺","location_text":"在府治东洪武三十年建"},
      {"name":"陕西苑马寺","type":"寺","location_text":"在府治东永乐四年建领六监二十四苑"},
      {"name":"固原卫","type":"卫","location_text":"在州城中"},
      {"name":"平凉卫","type":"卫","location_text":"在府治东南旧在府治东洪武三年建永乐六年移治于此"},
      {"name":"安东中护卫","type":"卫","location_text":"在府治东洪熙元年为韩府置"}],
    "fiefs":[
      {"name":"韩王府","type":"王府","note":"府城中洪熙元年建"},
      {"name":"襄陵王府","type":"王府","note":"府治西"},
      {"name":"乐平王府","type":"王府","note":"府治西"},
      {"name":"通渭王府","type":"王府","note":"府治西"},
      {"name":"褒城王府","type":"王府","note":"府治西"},
      {"name":"高平王府","type":"王府","note":"府城内"},
      {"name":"西德王府","type":"王府","note":"府城内"},
      {"name":"宁远王府","type":"王府","note":"府城内"},
      {"name":"长防王府","type":"王府","note":"府城内"},
      {"name":"永福王府","type":"王府","note":"府城内"},
      {"name":"建宁王府","type":"王府","note":"府城内"},
      {"name":"长洲王府","type":"王府","note":"府城内"},
      {"name":"昆山王府","type":"王府","note":"府城内"},
      {"name":"长乐王府","type":"王府","note":"府城内"},
      {"name":"庆阳王府","type":"王府","note":"府城内"},
      {"name":"高淳王府","type":"王府","note":"府城内"},
      {"name":"休宁王府","type":"王府","note":"府城内"},
      {"name":"通安王府","type":"王府","note":"府城内"}]
  },
  "cit_ids":["CIT-001","CIT-002","CIT-003","CIT-004","CIT-005","CIT-006","CIT-007","CIT-008",
             "CIT-009","CIT-010","CIT-011","CIT-012","CIT-013"]},
 # counties
 {"geo_id":f"{GJ}-c01","item_id":PJ,"name":"平凉县","type":"county","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"附郭","households":{"count":23,"unit":"里","note":"编户二十三里"}}},
 {"geo_id":f"{GJ}-c02","item_id":PJ,"name":"崇信县","type":"county","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府城东南八十里","households":{"count":4,"unit":"里","note":"编户四里"}}},
 {"geo_id":f"{GJ}-c03","item_id":PJ,"name":"华亭县","type":"county","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府城南一百二十里","households":{"count":8,"unit":"里","note":"编户八里"}}},
 {"geo_id":f"{GJ}-c04","item_id":PJ,"name":"镇原县","type":"county","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府城北一百三十里","households":{"count":20,"unit":"里","note":"编户二十里"}}},
 # sub-prefectures
 {"geo_id":f"{GJ}-s01","item_id":PJ,"name":"固原州","type":"subprefecture","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府城西北一百三十里","households":{"count":10,"unit":"里","note":"编户一十里"}}},
 {"geo_id":f"{GJ}-s02","item_id":PJ,"name":"泾州","type":"subprefecture","region":"陕西","parent":GJ,
  "children":[f"{GJ}-c05"],"volume_range":"卷35",
  "attributes":{"location_text":"在府城东一百五十里","households":{"count":17,"unit":"里","note":"编户一十七里领县一"}}},
 {"geo_id":f"{GJ}-c05","item_id":PJ,"name":"灵台县","type":"county","region":"陕西","parent":f"{GJ}-s02","children":[],
  "volume_range":"卷35","attributes":{"location_text":"在州城南九十里","households":{"count":20,"unit":"里","note":"编户二十里"}}},
 {"geo_id":f"{GJ}-s03","item_id":PJ,"name":"静宁州","type":"subprefecture","region":"陕西","parent":GJ,
  "children":[f"{GJ}-c06",f"{GJ}-c07"],"volume_range":"卷35",
  "attributes":{"location_text":"在府城西二百三十里","households":{"count":14,"unit":"里","note":"编户一十四里领县二"}}},
 {"geo_id":f"{GJ}-c06","item_id":PJ,"name":"庄浪县","type":"county","region":"陕西","parent":f"{GJ}-s03","children":[],
  "volume_range":"卷35","attributes":{"location_text":"在州城东南九十里","households":{"count":7,"unit":"里","note":"编户七里"}}},
 {"geo_id":f"{GJ}-c07","item_id":PJ,"name":"隆德县","type":"county","region":"陕西","parent":f"{GJ}-s03","children":[],
  "volume_range":"卷35","attributes":{"location_text":"在州城东九十里","households":{"count":5,"unit":"里","note":"编户五里"}}},
 # weisuo
 {"geo_id":f"{GJ}-w01","item_id":PJ,"name":"固原卫","type":"weisuo","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在州城中","garrison_type":"卫"}},
 {"geo_id":f"{GJ}-w02","item_id":PJ,"name":"平凉卫","type":"weisuo","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府治东南洪武三年建永乐六年移治于此","garrison_type":"卫"}},
 {"geo_id":f"{GJ}-w03","item_id":PJ,"name":"安东中护卫","type":"weisuo","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府治东洪熙元年为韩府置","garrison_type":"卫"}},
]

evos_pj = [
 {"evo_id":"EVO-001","item_id":PJ,"geo_id":GJ,"dynasty":"周","era":None,"institution_name":"雍州之域","action":"因之","detail":"禹贡雍州之域，天文井鬼分野"},
 {"evo_id":"EVO-002","item_id":PJ,"geo_id":GJ,"dynasty":"春秋","era":None,"institution_name":"朝那故地","action":"因之","detail":"春秋为朝那故地"},
 {"evo_id":"EVO-003","item_id":PJ,"geo_id":GJ,"dynasty":"秦","era":None,"institution_name":"北地郡","action":"置郡","detail":"秦属北地郡"},
 {"evo_id":"EVO-004","item_id":PJ,"geo_id":GJ,"dynasty":"汉","era":None,"institution_name":"安定郡","action":"置","detail":"汉析置安定郡治高平"},
 {"evo_id":"EVO-005","item_id":PJ,"geo_id":GJ,"dynasty":"晋","era":None,"institution_name":"临泾","action":"迁","detail":"晋徙治临泾"},
 {"evo_id":"EVO-006","item_id":PJ,"geo_id":GJ,"dynasty":"后魏","era":None,"institution_name":"武州","action":"置","detail":"后魏于潘原县置武州属太平郡"},
 {"evo_id":"EVO-007","item_id":PJ,"geo_id":GJ,"dynasty":"后周","era":None,"institution_name":"原州","action":"改","detail":"后周属原州"},
 {"evo_id":"EVO-008","item_id":PJ,"geo_id":GJ,"dynasty":"隋","era":None,"institution_name":"安定郡/平凉郡","action":"析置","detail":"隋安定郡治安定县，又析置平凉郡治平高"},
 {"evo_id":"EVO-009","item_id":PJ,"geo_id":GJ,"dynasty":"唐","era":"元和","institution_name":"行渭州","action":"置","detail":"唐初属原州，元和中以原州平凉县置行渭州，后没于吐蕃，中和间复置"},
 {"evo_id":"EVO-010","item_id":PJ,"geo_id":GJ,"dynasty":"宋","era":"政和","institution_name":"平凉军","action":"升","detail":"宋为泾原路经略安抚使治所，政和中置平凉军"},
 {"evo_id":"EVO-011","item_id":PJ,"geo_id":GJ,"dynasty":"金","era":None,"institution_name":"平凉府","action":"改","detail":"金为平凉府"},
 {"evo_id":"EVO-012","item_id":PJ,"geo_id":GJ,"dynasty":"元","era":None,"institution_name":"平凉府","action":"因之","detail":"元为平凉府"},
 {"evo_id":"EVO-013","item_id":PJ,"geo_id":GJ,"dynasty":"明","era":None,"institution_name":"平凉府","action":"因之","detail":"本朝因之，领州三县七"},
]

mtns_pj = [
 ("天坛山","山","在府城北五里","亦名卧虎山，上有朝元宫",""),
 ("可蓝山","山","在府城西南二十里","亦名都卢山，赫连据平凉尝屯兵此山","寰宇记赫连定畋于凉州登可蓝山望统万城"),
 ("崆峒山","山","在府城西三十里","上有问道宫，庄子谓黄帝学道于广成子盖在此山","宋游师雄诗"),
 ("笄头山","山","在崆峒山西","以形似名，史记黄帝西至于崆峒登笄头山即此",""),
 ("翠屏山","山","崆峒峰之最高者","俗呼屏风山，上有圆石如珠，一名垂珠峰","游师雄诗"),
 ("大统山","山","在崆峒山东","崆峒山西北有望家山",""),
 ("断万山","山","在崇信县西四十里","",""),
 ("五马山","山","在崇信县西南四十里","状如五马",""),
 ("王母山","山","在华亭县治南","",""),
 ("义山","山","在华亭县东二里","县西北二里又有铧尖山",""),
 ("齐山","山","在华亭县西一十三里","",""),
 ("桦岭山","山","在华亭县东五十里","山多桦树",""),
 ("皛然山","山","在华亭县西北七十里","",""),
 ("飞凤山","山","在华亭县西北一百里","形如飞凤",""),
 ("潜夫山","山","在镇原县治北","东汉王符隐此",""),
 ("东山","山","在镇原县东三里","",""),
 ("玉山","山","在镇原县东","山多白石，阴雨之后明艶如玉",""),
 ("雉头山","山","在镇原县西三十里","状如雉头，又县西五十里有鸡头山，隗嚣尝使其将王孟塞鸡头道以拒汉兵",""),
 ("大垄山","山","在镇原县西七十里","",""),
 ("六盘山","山","在固原州西二十里","曲折高峻，元世祖尝于此驻跸，后安西王于此建避暑楼",""),
 ("马屯山","山","在固原州西","前秦苻登与姚苌战败奔于此",""),
 ("回中山","山","在泾州西五里","上有王母宫，汉武帝幸雍道回中遂北出萧关即此",""),
 ("笔峰山","山","在泾州南五里","又东有山三峰峭峻，俗呼米面山",""),
 ("苍山","山","在灵台县南二里","林木苍翠故名",""),
 ("隐形山","山","在灵台县东北二里","",""),
 ("台山","山","在灵台县东北一十里","山多奇木异禽甘泉秀石，又固原州南三里亦有台山，以上有烽火台而名",""),
 ("保岩山","山","在灵台县东三十里","山势峭拔回旋百折，其颠有泾台，下常有云雾",""),
 ("兼山","山","在灵台县西九十里","乃泾州主山也",""),
 ("横山","山","在静宁州北一十里","蕃部所居",""),
 ("陇山","山","在静宁州南一百五十里","以近陇州之地故名",""),
 ("盘龙山","山","在庄浪县南四十里","状如盘龙",""),
 ("襟山","山","在隆德县南一十里","状如衣襟",""),
 ("美高山","山","在隆德县东南二十里","",""),
 ("香炉峰","峰","在崆峒山","一名香炉台，自香炉台望倒插石上巨下锐尤为奇怪","游师雄诗"),
 ("皂鹤洞","洞","在崆峒山东岩之半","上有皂鹤，每见必主兵革","游师雄诗"),
 ("广成子洞","洞","在东岩北别峰之阴","有穴曰广成子洞","游师雄诗"),
 ("青龙洞","洞","在翠屏山上","雨晴云辄归洞中，一名归云洞","游师雄诗"),
 ("碧泉洞","洞","在泾州废临泾县境","其中水皆青色，四时长流，味苦不堪食",""),
 ("雕窠峡","峡","在府城南三十里","","宋蔡挺诗"),
 ("金佛峡","峡","在府城西六十里","上有金妆佛三","宋王素诗"),
 ("弹筝峡","峡","在府城西一百里","风吹流水音韵铿锵如弹筝声","唐储光羲诗"),
 ("石门硖","峡","在静宁州南一百五十里","山石如门，其路斩截，即陇山北垂也",""),
 ("桃坡","原","在镇原县治西","其地有桃万株故名",""),
 ("卧龙原","原","在灵台县东一十里","",""),
 ("和戎原","原","在临泾废县南二十五里","",""),
 ("白石原","原","在灵台县西北","其原首起废良原县西南三十里，东下三十里分为两原，一更名良原，一更名良杜原",""),
 ("望儿原","原","在灵台县废良原县东三十里","",""),
 ("泾河","河","自府城西南白岩发源","至泾州又东南至邠州界，又东北至西安府高陵县界入于渭",""),
 ("横河","河","在府城西三十里","源出华亭县流至此，与境内大岔南谷诸水俱入于泾河",""),
 ("胡卢河","河","本名蔚茹水","源出镇原西南颓沙山下流入泾河，唐志白草军在蔚茹水之西谓此",""),
 ("阁川河","河","在泾州西南三里","流入泾河",""),
 ("汭水","河","自陇州流经本府崇信华亭两县境","至泾州又东流入泾河",""),
 ("武村水","河","在华亭县南一十里","武村",""),
 ("策底水","河","在华亭县北三十里","流入泾河",""),
 ("肥水","河","在镇原县西北四十里","与自延水俱注高平川",""),
 ("蒲水","河","在镇原县北五十里","发源南蒲谷，与灵台细川水合",""),
 ("三水","河","在镇原县东北六十里","水流三派归一川，又有水五源俱出陇山合而为一，又名一水",""),
 ("阳晋水","河","在西蕃界","东流至镇源县又流入泾州界",""),
 ("大黑水","河","在固原州北一百五十里","流入黄河，旁有小黑水流入焉",""),
 ("三香水","河","在灵台县东五十里","源出麟游县东，亦名三交川水",""),
 ("苦水","河","在庄浪县西二十里","其水味苦，又静宁州西五里有苦水河",""),
 ("好水","河","在隆德县西二里","源出六盘山西流合苦水",""),
 ("底堡水","河","在隆德县西二里","源出美高山，其西有堡故名",""),
 ("胭脂川","川","在华亭县西北一百里","东流入泾河",""),
 ("高平川","川","在镇原县治南","源出大垄山若水谷，又名若水",""),
 ("三川","川","在镇原县西北三十里","其源本一流而为三入高平川",""),
 ("南川","川","有二","大南川在固原州东六十里，小南川在州东南五十里",""),
 ("干川","川","在固原州东北一百六十里","",""),
 ("达溪川","川","在灵台县南二里","流达泾河",""),
 ("妲己川","川","在灵台县西七十里","",""),
 ("威戎川","川","在静宁州南四十里","宋于此筑威戎堡，金置威戎县因名",""),
 ("通遍川","川","在静宁州东一百五十里","以道路四通故名",""),
 ("水洛川","川","在静宁州南一百五十里","源出陇山西南流合椟奴水，又经石门峡流入秦州界",""),
 ("曹务川","川","在庄浪县北三十里","川旁有姓曹名务者居之故名",""),
 ("阳三川","川","在庄浪县西南七十里","山阳有三川故名",""),
 ("孤树川","川","在隆德县北三十里","旁有孤树",""),
 ("武延川","川","在隆德县西北七十里","昔有武延者居此川之旁故名，宋曹玮知渭州日与陈兴秦翰破章埋族于武延川即此",""),
 ("柳湖","湖","在府城北三十里","湖畔柳数千株",""),
 ("朝那湫","湫","在固原州","湫有二，俱出山间，一在县东十五里，一在县西北三十里，土人谓之东海西海，方四十里，水停不流，冬夏不增减，不生草木",""),
 ("灵湫","湫","在隆德县东北四十里","其水四时常溢，旱祷有应，有元天历中碑记",""),
 ("琉璃泉","泉","在崆峒山","","游师雄诗"),
 ("西岩泉","泉","在崆峒山","泉甚甘美","游师雄诗"),
 ("暖泉","泉","在府城北二里","其水涌出四时温然，又泾州西五里亦有暖泉",""),
 ("石泉","泉","在镇原县治西","水从石孔中出，四时不涸",""),
 ("百泉","泉","在泾州西三十五里","泉眼极多，四时不涸",""),
 ("甘泉","泉","在灵台县东北一十里","水味甘美",""),
 ("温冷泉","泉","出保岩山之阴","半温半冷，有疾者于此洗涤即愈",""),
 ("马跑泉","泉","在灵台县西一百三十五里","俗传秦王至此马跑泉出",""),
 ("官泉","泉","在隆德县治东","源出于山，四时不涸",""),
]

cits_pj = [
 ("CIT-001","国经","立论","【国经秦陇之地以山立郭平凉山川最为秀拔】"),
 ("CIT-002","文献通考","立论","【文献通考镇戎军山川险阻旁扼夷落为中华襟带】"),
 ("CIT-003","寰宇记","立论","【寰宇记水土杂于河西人烟接于北地】"),
 ("CIT-004","原州防壁记","立论","【原州防壁记郡介于泾原环庆之间而外边羌夏】"),
 ("CIT-005","宋郑文宅城萧关议","立论","【宋郑文宅城萧关议襟带西凉咽喉灵武】"),
 ("CIT-006","元开成志","立论","【元开成志左控五原右带兰会黄流在其北崆峒阻其南】"),
 ("CIT-007","金胥鼎云","立论","【金胥鼎云控制西垂实为要地】"),
 ("CIT-008","德顺州志","立论","【德顺州志陇水环流绕带河渭】"),
 ("CIT-009","郡志","证俗","【郡志平凉民俗醇厚不尚侈靡专业耕种不为寇盗其婚姻丧葬颇近古风】"),
 ("CIT-010","镇原志","证俗","【镇原志质朴尚勇穴处者多】"),
 ("CIT-011","开城志","证俗","【开城志女工机织男多游手】"),
 ("CIT-012","静宁州志","证俗","【静宁州志好猎务农民淳易化】"),
 ("CIT-013","方舆枢要","证俗","【方舆枢要泾州古密须之国被文王之化而风俗美】"),
]

ents_pj = [
 {"ent_id":"ENT-001","name":"平凉府","type":"geo","norm":"平凉府","first_source":PJ},
 {"ent_id":"ENT-002","name":"崆峒山","type":"mtn","norm":"崆峒山","first_source":PJ},
 {"ent_id":"ENT-003","name":"六盘山","type":"mtn","norm":"六盘山","first_source":PJ},
 {"ent_id":"ENT-004","name":"泾河","type":"mtn","norm":"泾河","first_source":PJ},
 {"ent_id":"ENT-005","name：":"王符","type":"person","norm":"王符","first_source":PJ},
]
# fix typo
ents_pj[-1] = {"ent_id":"ENT-005","name":"王符","type":"person","norm":"王符","first_source":PJ}

# Build main file
main_pj = {
 "item_id":PJ,"volume":"35","source":"平凉府","region":"陕西",
 "layers":{
   "ents":ents_pj,
   "geos":geos_pj,
   "evos":evos_pj,
   "mtns":[{"mtn_id":f"MTN-{i+1:03d}","item_id":PJ,"geo_id":GJ,"name":n,"type":t,"location_text":loc,"description":d,"lore":l}
           for i,(n,t,loc,d,l) in enumerate(mtns_pj)],
   "pers":[],
   "sites":[],
   "prods":[
     {"prod_id":"PROD-001","item_id":PJ,"geo_id":GJ,"name":"黑瓷器","note":"平凉华亭二县出"},
     {"prod_id":"PROD-002","item_id":PJ,"geo_id":GJ,"name":"甘草","note":"镇原县静宁州出"},
     {"prod_id":"PROD-003","item_id":PJ,"geo_id":GJ,"name":"秦艽","note":"平凉县出"},
     {"prod_id":"PROD-004","item_id":PJ,"geo_id":GJ,"name":"苁蓉","note":"平凉县出"},
     {"prod_id":"PROD-005","item_id":PJ,"geo_id":GJ,"name":"天南星","note":"崇信华亭二县出"},
     {"prod_id":"PROD-006","item_id":PJ,"geo_id":GJ,"name":"款冬花","note":"静宁州及庄浪县出"},
     {"prod_id":"PROD-007","item_id":PJ,"geo_id":GJ,"name":"苦参","note":"静宁州及庄浪县出"},
   ],
   "cits":[{"cit_id":c,"item_id":PJ,"cited_work":w,"cited_work_ent_id":None,"context":ctx,"original":o}
           for c,w,ctx,o in cits_pj]
 },
 "layer_count":7,
 "validation":{
   "errs":[],"gap":0,
   "notes":"pers 层拆至 35-001_pers1_名宦.json 与 35-001_pers2_人物列女仙释.json；sites 层拆至 35-001_sites1_古迹陵墓祠庙寺观.json 与 35-001_sites2_宫室关梁公署学校.json"
 }
}
dump("35-001_平凉府.json", main_pj)

# County/stub files for 平凉府
counties_pj = [
 ("c01","平凉县","county",GJ,"附郭",23),
 ("c02","崇信县","county",GJ,"在府城东南八十里",4),
 ("c03","华亭县","county",GJ,"在府城南一百二十里",8),
 ("c04","镇原县","county",GJ,"在府城北一百三十里",20),
 ("c05","灵台县","county",f"{GJ}-s02","在州城南九十里",20),
 ("c06","庄浪县","county",f"{GJ}-s03","在州城东南九十里",7),
 ("c07","隆德县","county",f"{GJ}-s03","在州城东九十里",5),
 ("s01","固原州","subprefecture",GJ,"在府城西北一百三十里",10),
 ("s02","泾州","subprefecture",GJ,"在府城东一百五十里",17),
 ("s03","静宁州","subprefecture",GJ,"在府城西二百三十里",14),
 ("w01","固原卫","weisuo",GJ,"在州城中",None),
 ("w02","平凉卫","weisuo",GJ,"在府治东南洪武三年建永乐六年移治于此",None),
 ("w03","安东中护卫","weisuo",GJ,"在府治东洪熙元年为韩府置",None),
]
for cid,name,typ,parent,loc,hh in counties_pj:
    attrs = {"location_text":loc}
    if hh:
        attrs["households"] = {"count":hh,"unit":"里","note":f"编户{hh}里"}
    else:
        attrs["garrison_type"] = "卫"
    obj = {
      "item_id":PJ,"volume":"35","source":name,"region":"陕西",
      "layers":{
        "ents":[{"ent_id":f"ENT-{cid}","name":name,"type":"geo","norm":name,"first_source":PJ}],
        "geos":[{"geo_id":f"{GJ}-{cid}","item_id":PJ,"name":name,"type":typ,"region":"陕西",
                 "parent":parent,"children":[],"volume_range":"卷35","attributes":attrs}],
        "evos":[],"mtns":[],"pers":[],"sites":[],"prods":[],"cits":[]
      },
      "layer_count":7
    }
    dump(f"35-001_{cid}_{name}.json", obj)

print("=== 平凉府 main + stubs done ===")
