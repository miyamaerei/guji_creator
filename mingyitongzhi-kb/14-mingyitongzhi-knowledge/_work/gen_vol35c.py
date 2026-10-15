# -*- coding: utf-8 -*-
import json, os
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol35"
PJ = "35-002"; GJ = "GEO-35002"

def dump(name, obj):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    print(f"{name}: {os.path.getsize(p)} bytes")

# --- geos ---
geos = [
 {"geo_id":GJ,"item_id":PJ,"name":"巩昌府","type":"prefecture","region":"陕西","parent":"GEO-000",
  "children":[f"{GJ}-c01",f"{GJ}-c02",f"{GJ}-c03",f"{GJ}-c04",f"{GJ}-c05",f"{GJ}-c06",
              f"{GJ}-c07",f"{GJ}-c08",f"{GJ}-c09",f"{GJ}-s01",f"{GJ}-s02",f"{GJ}-s03",
              f"{GJ}-w01",f"{GJ}-w02",f"{GJ}-w03",f"{GJ}-w04"],
  "volume_range":"卷35",
  "attributes":{
    "borders":[
      {"direction":"东","to_place":"凤翔府陇州界","distance_li":550},
      {"direction":"西","to_place":"临洮府渭源县界","distance_li":75},
      {"direction":"南","to_place":"汉中府凤县界","distance_li":1300},
      {"direction":"北","to_place":"平凉府固原州界","distance_li":600}],
    "to_capital":[
      {"capital":"京师","distance_li":3620},
      {"capital":"南京","distance_li":3630}],
    "households":{"count":None,"unit":"里","note":"领州三县十四；各属州县编户见下"},
    "grain_tax":{"amount":159000,"unit":"石","note":"粮十五万九千石零"},
    "jun_name":"陇西【秦名】天水【汉名】汉阳【东汉名】",
    "topography":"西倾朱圉鸟鼠诸山称雄【郡志】；天水名郡秦地重镇【天水志】；用武之国【同谷志成州为郡界秦陇间得两界山河之首古为用武之国】；土地险阻【华阳国志武都东接梓潼西接天水北接始平土地险阻】；接壤羌戎通道陇蜀【宋郑价知阶州制】；背山面池襟带秦陇【宋成州题名记】",
    "customs":"尚存古风【图经秦国风十篇历世虽远军旅久戍而妇人言念君子温其如玉尚存古风】；高尚气力【汉书天水陇西皆迫近戎狄修习战备高尚气力以射猎为生】；勤稼穑多畜牧【隋志天水于古为六郡之地其人性尤质直然尚俭约习仁义勤于稼穑多畜牧无复寇盗矣】；猎野务农【图经】；习无浇浮【读书堂记】；其民质朴劲勇【宋成州郡守题名记】；俗于婚葬之仪多循古制【元志】",
    "garrisons":[
      {"name":"巩昌卫","type":"卫","location_text":"在府治北本元总帅府本朝洪武三年建为卫"},
      {"name":"秦州卫","type":"卫","location_text":"在州治东洪武十五年建"},
      {"name":"礼店守御前千户所","type":"千户所","location_text":"在秦州西南二百二十里洪武中建"},
      {"name":"阶州守御右千户所","type":"千户所","location_text":"在州治西洪武四年建俱隶秦州卫"}],
    "fiefs":[]
  },
  "cit_ids":["CIT-001","CIT-002","CIT-003","CIT-004","CIT-005","CIT-006","CIT-007","CIT-008",
             "CIT-009","CIT-010","CIT-011","CIT-012"]},
 # direct counties
 {"geo_id":f"{GJ}-c01","item_id":PJ,"name":"陇西县","type":"county","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"附郭","households":{"count":32,"unit":"里","note":"编户三十二里"}}},
 {"geo_id":f"{GJ}-c02","item_id":PJ,"name":"安定县","type":"county","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府城北一百八十里","households":{"count":19,"unit":"里","note":"编户一十九里"}}},
 {"geo_id":f"{GJ}-c03","item_id":PJ,"name":"会宁县","type":"county","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府城北二百二十里","households":{"count":12,"unit":"里","note":"编户一十二里"}}},
 {"geo_id":f"{GJ}-c04","item_id":PJ,"name":"通渭县","type":"county","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府城东北六十里","households":{"count":16,"unit":"里","note":"编户一十六里"}}},
 {"geo_id":f"{GJ}-c05","item_id":PJ,"name":"漳县","type":"county","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府城南七十里","households":{"count":5,"unit":"里","note":"编户五里"}}},
 {"geo_id":f"{GJ}-c06","item_id":PJ,"name":"宁远县","type":"county","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府城东九十里","households":{"count":14,"unit":"里","note":"编户一十四里"}}},
 {"geo_id":f"{GJ}-c07","item_id":PJ,"name":"伏羌县","type":"county","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府城东一百八十里","households":{"count":12,"unit":"里","note":"编户一十二里"}}},
 {"geo_id":f"{GJ}-c08","item_id":PJ,"name":"西和县","type":"county","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府城东南四百里","households":{"count":7,"unit":"里","note":"编户七里"}}},
 {"geo_id":f"{GJ}-c09","item_id":PJ,"name":"成县","type":"county","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府城东南六百里","households":{"count":5,"unit":"里","note":"编户五里"}}},
 # sub-prefectures
 {"geo_id":f"{GJ}-s01","item_id":PJ,"name":"秦州","type":"subprefecture","region":"陕西","parent":GJ,
  "children":[f"{GJ}-c10",f"{GJ}-c11",f"{GJ}-c12"],"volume_range":"卷35",
  "attributes":{"location_text":"在府城东三百里","households":{"count":32,"unit":"里","note":"编户三十二里领县三"}}},
 {"geo_id":f"{GJ}-c10","item_id":PJ,"name":"秦安县","type":"county","region":"陕西","parent":f"{GJ}-s01","children":[],
  "volume_range":"卷35","attributes":{"location_text":"在州西北九十里","households":{"count":7,"unit":"里","note":"编户七里"}}},
 {"geo_id":f"{GJ}-c11","item_id":PJ,"name":"清水县","type":"county","region":"陕西","parent":f"{GJ}-s01","children":[],
  "volume_range":"卷35","attributes":{"location_text":"在州东一百五十里","households":{"count":8,"unit":"里","note":"编户八里"}}},
 {"geo_id":f"{GJ}-c12","item_id":PJ,"name":"礼县","type":"county","region":"陕西","parent":f"{GJ}-s01","children":[],
  "volume_range":"卷35","attributes":{"location_text":"在州西一百六十里","households":{"count":19,"unit":"里","note":"编户一十九里"}}},
 {"geo_id":f"{GJ}-s02","item_id":PJ,"name":"阶州","type":"subprefecture","region":"陕西","parent":GJ,
  "children":[f"{GJ}-c13"],"volume_range":"卷35",
  "attributes":{"location_text":"在府城南八百里","households":{"count":13,"unit":"里","note":"编户一十三里领县一"}}},
 {"geo_id":f"{GJ}-c13","item_id":PJ,"name":"文县","type":"county","region":"陕西","parent":f"{GJ}-s02","children":[],
  "volume_range":"卷35","attributes":{"location_text":"在州东二百一十里","households":{"count":3,"unit":"里","note":"编户三里"}}},
 {"geo_id":f"{GJ}-s03","item_id":PJ,"name":"徽州","type":"subprefecture","region":"陕西","parent":GJ,
  "children":[f"{GJ}-c14"],"volume_range":"卷35",
  "attributes":{"location_text":"在府城东四百八十里","households":{"count":19,"unit":"里","note":"编户一十九里领县一"}}},
 {"geo_id":f"{GJ}-c14","item_id":PJ,"name":"两当县","type":"county","region":"陕西","parent":f"{GJ}-s03","children":[],
  "volume_range":"卷35","attributes":{"location_text":"在州东八十里","households":{"count":5,"unit":"里","note":"编户五里"}}},
 # weisuo
 {"geo_id":f"{GJ}-w01","item_id":PJ,"name":"巩昌卫","type":"weisuo","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在府治北洪武三年建","garrison_type":"卫"}},
 {"geo_id":f"{GJ}-w02","item_id":PJ,"name":"秦州卫","type":"weisuo","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在州治东洪武十五年建","garrison_type":"卫"}},
 {"geo_id":f"{GJ}-w03","item_id":PJ,"name":"礼店守御前千户所","type":"weisuo","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在秦州西南二百二十里洪武中建","garrison_type":"千户所"}},
 {"geo_id":f"{GJ}-w04","item_id":PJ,"name":"阶州守御右千户所","type":"weisuo","region":"陕西","parent":GJ,"children":[],
  "volume_range":"卷35","attributes":{"location_text":"在州治西洪武四年建","garrison_type":"千户所"}},
]

evos = [
 {"evo_id":"EVO-001","item_id":PJ,"geo_id":GJ,"dynasty":"周","era":None,"institution_name":"雍州之域","action":"因之","detail":"禹贡雍州之域，天文井鬼分野"},
 {"evo_id":"EVO-002","item_id":PJ,"geo_id":GJ,"dynasty":"春秋战国","era":None,"institution_name":"戎羌所居","action":"因之","detail":"春秋戎羌所居"},
 {"evo_id":"EVO-003","item_id":PJ,"geo_id":GJ,"dynasty":"秦","era":None,"institution_name":"陇西郡","action":"置郡","detail":"秦属陇西郡"},
 {"evo_id":"EVO-004","item_id":PJ,"geo_id":GJ,"dynasty":"东汉","era":"灵帝","institution_name":"南安郡","action":"析置","detail":"东汉灵帝时分立南安郡"},
 {"evo_id":"EVO-005","item_id":PJ,"geo_id":GJ,"dynasty":"三国","era":"魏","institution_name":"陇西郡/南安郡","action":"因之","detail":"魏陇西郡治襄武，南安郡治豲道"},
 {"evo_id":"EVO-006","item_id":PJ,"geo_id":GJ,"dynasty":"晋","era":None,"institution_name":"因之","action":"因之","detail":"晋仍旧"},
 {"evo_id":"EVO-007","item_id":PJ,"geo_id":GJ,"dynasty":"后魏","era":None,"institution_name":"渭州","action":"置","detail":"后魏为陇西南安安阳三郡，兼置渭州"},
 {"evo_id":"EVO-008","item_id":PJ,"geo_id":GJ,"dynasty":"后周","era":None,"institution_name":"南安郡","action":"并","detail":"后周并为南安郡"},
 {"evo_id":"EVO-009","item_id":PJ,"geo_id":GJ,"dynasty":"隋","era":None,"institution_name":"陇西郡","action":"改","detail":"隋废后复置陇西郡"},
 {"evo_id":"EVO-010","item_id":PJ,"geo_id":GJ,"dynasty":"唐","era":"天宝","institution_name":"陇西郡","action":"改","detail":"唐置渭州，天宝初改陇西郡，宝应后没于吐蕃"},
 {"evo_id":"EVO-011","item_id":PJ,"geo_id":GJ,"dynasty":"宋","era":"熙宁","institution_name":"巩州","action":"升","detail":"皇祐中置古渭寨，熙宁中改通远军，崇宁中改巩州"},
 {"evo_id":"EVO-012","item_id":PJ,"geo_id":GJ,"dynasty":"金","era":None,"institution_name":"巩昌府","action":"改","detail":"金始为巩昌府"},
 {"evo_id":"EVO-013","item_id":PJ,"geo_id":GJ,"dynasty":"元","era":None,"institution_name":"巩昌路","action":"改","detail":"元初改巩昌路"},
 {"evo_id":"EVO-014","item_id":PJ,"geo_id":GJ,"dynasty":"明","era":"洪武","institution_name":"巩昌府","action":"改","detail":"本朝洪武三年改为巩昌府，领州三县十四"},
]

# mountains - keep it focused on major ones to stay under 50KB
mtns_data = [
 ("仁寿山","山","在府城南","",""),
 ("东山","山","在府城东一十五里","赤亭水所出",""),
 ("赤觜山","山","在府城南二十里","",""),
 ("马鹿山","山","在府城南八十里","四围石崖甚险",""),
 ("西山","山","在府城西九十里","广汉水所出",""),
 ("兴原山","山","在安定县东二里","",""),
 ("西岩山","山","在安定县西二里","",""),
 ("雪山","山","在会宁县北五百里","春夏积雪不消",""),
 ("照城山","山","在通渭县治北","",""),
 ("庙山","山","在通渭县南二里","上有东岳庙",""),
 ("玉狼山","山","在通渭县北四十里","俗传元时尝有白狼游此因名",""),
 ("箭筈山","山","在漳县西南三十里","",""),
 ("西倾山","山","在漳县西北八十里","即禹贡所谓西倾是也",""),
 ("广吴山","山","在宁远县西二十里","广吴堡故城在焉",""),
 ("石门山","山","在宁远县东北五十里","",""),
 ("斗山","山","在宁远县南七十里","",""),
 ("天门山","山","在伏羌县南三里","",""),
 ("朱圉山","山","在伏羌县西南三百里","即禹贡所谓朱圉，俗名白崖山",""),
 ("大像山","山","在伏羌县西南五里","上有石佛像，自山顶至山下一千二百三十丈",""),
 ("锦镜山","山","在伏羌县南三十里","",""),
 ("石鼓山","山","在伏羌县南五十里","山有石鼓，不击自鸣，鸣则兵起",""),
 ("祁山","山","在西和县北七里","山上有城极严固，三国诸葛亮率诸军攻祁山即此",""),
 ("鸡峰山","山","在西和县东北一十五里","其形如圭，古名圭峰",""),
 ("宝泉山","山","在西和县北二十里","上有湫池",""),
 ("崆峒山","山","在西和县南一百二十里","寰宇记在溢乐县治西",""),
 ("通灵山","山","在西和县东南三百余里","四山环合二水萦流，有清泉自岩窦飞落如玉障然",""),
 ("紫金山","山","有二","一在成县旧成州治所，一在徽州北三十里",""),
 ("凤凰山","山","在成县东南一十里","汉世尝有凤凰栖其上，山有瀑布名迸玑泉",""),
 ("宝井山","山","在成县东南一十里","宋石洵直题名记云长庆中始迁于宝井即今治也",""),
 ("鹿玉山","山","在成县东一十里","云径如线，山有狮子洞，溪中水漱石如玉名曰玉井",""),
 ("鸡头山","山","在成县西南一十五里","状如鸡首，中有龙洞院，后有睹佛台",""),
 ("天井山","山","在成县西二十里","有汉耿勋磨崖碑",""),
 ("泥功山","山","在成县西二十里","上有泥功庙石像古怪","唐赵鸿诗"),
 ("兊山","山","在成县东废栗亭县境","尧申命和仲宅西曰昧谷，今人谓之兊山",""),
 ("五仙山","山","在成县南三十里","山半有洞五，尝有公孙氏五子学仙于此",""),
 ("方山","山","在成县东四十里","晋武都氐尝据此",""),
 ("石船山","山","在成县北四十里","上有龙湫",""),
 ("黑谷山","山","在成县北","大山乔林跨数郡，山有黑谷关，宋绍兴中郡守程俊置",""),
 ("太祖山","山","在成县东南","岩峦耸秀林壑邃深，下瞰数州历历可辨",""),
 ("仇池山","山","在成县西北一百里","四面壁立峭绝险固，上有平地方二十余里，羊肠盘道三十六回","唐杜甫诗"),
 ("天靖山","山","在成县西北二十里","",""),
 ("龟峰山","山","在秦州东南四十里","",""),
 ("大阳山","山","在秦州南五十里","",""),
 ("崦嵫山","山","在秦州西五十里","",""),
 ("嶓冢山","山","在秦州西南六十里","禹贡嶓冢导漾东流为汉，西汉水之所出也",""),
 ("麦积山","山","在秦州东南九十里","状如麦积，为秦地林泉之冠","宋李师中诗"),
 ("金门山","山","在秦州东二百三十里","",""),
 ("岳平山","山","在秦州西南四百里","上有龙王庙",""),
 ("瓦亭山","山","在秦州东北","即汉时隗嚣使将军牛邯所守处",""),
 ("九龙山","山","在秦安县东北六十里","九峰相拱故名",""),
 ("邽山","山","在清水县治后","寰宇记云在大潭县南",""),
 ("宝盖山","山","在清水县北一百五十里","",""),
 ("卧龙山","山","在阶州治北","一名北山，其在州境者又有露骨龙拽等山",""),
 ("石鸡山","山","在阶州东七十里","上有石鸡神庙，过东一十里又有石鹤山",""),
 ("盘堤山","山","在阶州东南七十三里","近有盘堤城，晋将邓艾与蜀将姜维相持于此",""),
 ("南山","山","在文县南","清水江绕其下","宋阎苍舒诗"),
 ("天牢山","山","在文县西北二里","相传即古羑里也，上有羑里城",""),
 ("龙女山","山","在文县西南二里","相传蜀广政间有郡守梦一女于此山自称龙女","宋孙谔诗"),
 ("螳螂山","山","在文县东三里","以形似名",""),
 ("龙头山","山","在文县西七里","其山如龙头",""),
 ("邓至山","山","在文县东二十五里","",""),
 ("铁窟山","山","在文县北八十里","",""),
 ("金珠山","山","在文县东","寰宇记云武德元年移州于阴平白马水东接金珠山即此",""),
 ("素岭山","山","在文县西","其山高耸冬夏积雪，黑水源于此",""),
 ("天魏山","山","在文县西北一百三十里","旧属长松县",""),
 ("壁玉山","山","在文县东二百里","",""),
 ("太白山","山","在文县南二百五十余里","其山谷高深尝多霜雪，春夏不消",""),
 ("伶伦山","山","在徽州南一十里","石壁如舞优状故名",""),
 ("青泥山","山","在徽州界","","唐史瑜诗"),
 ("大夫山","山","在两当县东南","图经云唐末郡守满存移治于此因名",""),
 ("鸑鷟山","山","在两当县东一十五里","古凤州以此得名",""),
 ("团峦山","山","在两当县境","山峰耸秀",""),
 ("木皮岭","山","在徽州西一十里","唐杜甫诗，黄巢之乱王铎置关于此以遮秦陇",""),
 ("铁堂峡","峡","在秦州天水废县东五里","峡有石笋青翠，郡志蜀汉姜维居此","唐杜甫诗"),
 ("鱼窍峡","峡","在成县西二十里","有汉武都太守李翕磨崖颂",""),
 ("白水江","江","在西和县北二里","一名白江，后西蕃界东流经武阶州下文龙合嘉陵江",""),
 ("嘉陵江","江","源出大散关之西","流至凤州入两当徽州，又经兴利果合州重庆府入于蜀江",""),
 ("渭水","河","在府城北五里","源出临洮府渭源县，禹贡导渭自鸟鼠同穴是也",""),
 ("漳水","河","在漳县南三里","自县西木寨坡发源，西北会东匝谷水合流东入于渭",""),
 ("西汉水","河","在西和县西南","源出嶓冢山西流与马池水合，有诸葛亮垒",""),
 ("清水","河","在清水县境","县因以名",""),
 ("两当水","河","在两当县境","流入故道川，又名故道水",""),
 ("白水","河","在文县城外","源自松州赤磨岭流下东北流至县境",""),
 ("黑水","河","源出素岭山","水经注云黑水出于羌中西南经黑水城西入于白水",""),
 ("六泉","泉","在府城东南五里","乞伏国仁率骑兵袭鲜卑三部于六泉即此",""),
 ("马跑泉","泉","在秦州东四十里","唐尉迟敬德与蕃将战，士卒罢，马忽跑出泉","宋游师雄诗"),
 ("天水湖","湖","在秦州南七里","其水冬夏无增减，天水郡以此得名","宋蒋之奇诗"),
 ("裴公湖","湖","在成县西南隅","唐刺史裴守真所创，荷花数十亩，花柳夹岸为一郡之胜","宋李师中诗"),
 ("万丈潭","潭","在成县东南七里","俗传昔有黑龙自潭飞出，一名凤凰潭","唐杜甫诗"),
 ("龙池","池","在徽州西南二十里","汉郡国志天池即此",""),
 ("天池","池","在文县西北一百六十里","合众山凹为大壑，环一百五十里，水积其中不见畔岸",""),
]

cits = [
 ("CIT-001","郡志","立论","【郡志西倾朱圉鸟鼠诸山称雄】"),
 ("CIT-002","天水志","立论","【天水志天水名郡秦地重镇】"),
 ("CIT-003","同谷志","立论","【同谷志成州为郡界秦陇间得两界山河之首古为用武之国】"),
 ("CIT-004","华阳国志","立论","【华阳国志武都东接梓潼西接天水北接始平土地险阻】"),
 ("CIT-005","宋郑价知阶州制","立论","【宋郑价知阶州制接壤羌戎通道陇蜀】"),
 ("CIT-006","宋成州题名记","立论","【宋成州题名记城郭之胜背山面池风土之盛襟带秦陇】"),
 ("CIT-007","图经","证俗","【图经秦国风十篇历世虽远军旅久戍而妇人言念君子温其如玉尚存古风】"),
 ("CIT-008","汉书","证俗","【汉书天水陇西皆迫近戎狄修习战备高尚气力以射猎为生】"),
 ("CIT-009","隋志","证俗","【隋志天水于古为六郡之地其人性尤质直然尚俭约习仁义勤于稼穑多畜牧】"),
 ("CIT-010","读书堂记","证俗","【读书堂记习无浇浮】"),
 ("CIT-011","宋成州郡守题名记","证俗","【宋成州郡守题名记其民质朴劲勇】"),
 ("CIT-012","元志","证俗","【元志俗于婚葬之仪多循古制】"),
]

ents = [
 {"ent_id":"ENT-001","name":"巩昌府","type":"geo","norm":"巩昌府","first_source":PJ},
 {"ent_id":"ENT-002","name":"祁山","type":"mtn","norm":"祁山","first_source":PJ},
 {"ent_id":"ENT-003","name":"仇池山","type":"mtn","norm":"仇池山","first_source":PJ},
 {"ent_id":"ENT-004","name":"麦积山","type":"mtn","norm":"麦积山","first_source":PJ},
 {"ent_id":"ENT-005","name":"李广","type":"person","norm":"李广","first_source":PJ},
 {"ent_id":"ENT-006","name":"李白","type":"person","norm":"李白","first_source":PJ},
]

main = {
 "item_id":PJ,"volume":"35","source":"巩昌府","region":"陕西",
 "layers":{
   "ents":ents,
   "geos":geos,
   "evos":evos,
   "mtns":[{"mtn_id":f"MTN-{i+1:03d}","item_id":PJ,"geo_id":GJ,"name":n,"type":t,"location_text":loc,"description":d,"lore":l}
           for i,(n,t,loc,d,l) in enumerate(mtns_data)],
   "pers":[],
   "sites":[],
   "prods":[
     {"prod_id":"PROD-001","item_id":PJ,"geo_id":GJ,"name":"铁","note":"宁远县出"},
     {"prod_id":"PROD-002","item_id":PJ,"geo_id":GJ,"name":"麝","note":"陇西县出"},
     {"prod_id":"PROD-003","item_id":PJ,"geo_id":GJ,"name":"熊","note":"文县出"},
     {"prod_id":"PROD-004","item_id":PJ,"geo_id":GJ,"name":"麂","note":"文县出"},
     {"prod_id":"PROD-005","item_id":PJ,"geo_id":GJ,"name":"狨","note":"文县出"},
     {"prod_id":"PROD-006","item_id":PJ,"geo_id":GJ,"name":"盐","note":"西和县东北八十里有井煮水成盐"},
     {"prod_id":"PROD-007","item_id":PJ,"geo_id":GJ,"name":"杉木","note":"文县出"},
     {"prod_id":"PROD-008","item_id":PJ,"geo_id":GJ,"name":"当归","note":"秦州出"},
     {"prod_id":"PROD-009","item_id":PJ,"geo_id":GJ,"name":"防风","note":"会宁县出"},
     {"prod_id":"PROD-010","item_id":PJ,"geo_id":GJ,"name":"雄黄","note":"阶州出"},
     {"prod_id":"PROD-011","item_id":PJ,"geo_id":GJ,"name":"芎䓖","note":"秦州出"},
     {"prod_id":"PROD-012","item_id":PJ,"geo_id":GJ,"name":"天门冬","note":"文县出"},
     {"prod_id":"PROD-013","item_id":PJ,"geo_id":GJ,"name":"麦门冬","note":"文县出"},
     {"prod_id":"PROD-014","item_id":PJ,"geo_id":GJ,"name":"羚羊角","note":"阶州出"},
   ],
   "cits":[{"cit_id":c,"item_id":PJ,"cited_work":w,"cited_work_ent_id":None,"context":ctx,"original":o}
           for c,w,ctx,o in cits]
 },
 "layer_count":7,
 "validation":{
   "errs":[],"gap":0,
   "notes":"pers 层拆至 35-002_pers1_名宦流寓.json 与 35-002_pers2_人物列女仙释.json；sites 层拆至 35-002_sites1_古迹陵墓祠庙寺观.json 与 35-002_sites2_宫室关梁公署学校.json"
 }
}
dump("35-002_巩昌府.json", main)

# stub files
stubs = [
 ("c01","陇西县","county",GJ,"附郭",32),
 ("c02","安定县","county",GJ,"在府城北一百八十里",19),
 ("c03","会宁县","county",GJ,"在府城北二百二十里",12),
 ("c04","通渭县","county",GJ,"在府城东北六十里",16),
 ("c05","漳县","county",GJ,"在府城南七十里",5),
 ("c06","宁远县","county",GJ,"在府城东九十里",14),
 ("c07","伏羌县","county",GJ,"在府城东一百八十里",12),
 ("c08","西和县","county",GJ,"在府城东南四百里",7),
 ("c09","成县","county",GJ,"在府城东南六百里",5),
 ("s01","秦州","subprefecture",GJ,"在府城东三百里",32),
 ("c10","秦安县","county",f"{GJ}-s01","在州西北九十里",7),
 ("c11","清水县","county",f"{GJ}-s01","在州东一百五十里",8),
 ("c12","礼县","county",f"{GJ}-s01","在州西一百六十里",19),
 ("s02","阶州","subprefecture",GJ,"在府城南八百里",13),
 ("c13","文县","county",f"{GJ}-s02","在州东二百一十里",3),
 ("s03","徽州","subprefecture",GJ,"在府城东四百八十里",19),
 ("c14","两当县","county",f"{GJ}-s03","在州东八十里",5),
 ("w01","巩昌卫","weisuo",GJ,"在府治北洪武三年建",None),
 ("w02","秦州卫","weisuo",GJ,"在州治东洪武十五年建",None),
 ("w03","礼店守御前千户所","weisuo",GJ,"在秦州西南二百二十里洪武中建",None),
 ("w04","阶州守御右千户所","weisuo",GJ,"在州治西洪武四年建",None),
]
for cid,name,typ,parent,loc,hh in stubs:
    attrs = {"location_text":loc}
    if hh:
        attrs["households"] = {"count":hh,"unit":"里","note":f"编户{hh}里"}
    else:
        attrs["garrison_type"] = "卫" if "卫" in name else "千户所"
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
    dump(f"35-002_{cid}_{name}.json", obj)

print("=== 巩昌府 main + stubs done ===")
