# -*- coding: utf-8 -*-
"""Generate all vol38 Hangzhou files in one shot."""
import json, os

BASE = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol38"
os.makedirs(BASE, exist_ok=True)

# ---- GEO ----
geos = [
    {"geo_id":"GEO-38001","item_id":"38-001","name":"杭州府","type":"prefecture","region":"浙江",
     "parent":"GEO-000","children":["GEO-38001-c01","GEO-38001-c02","GEO-38001-c03","GEO-38001-c04","GEO-38001-c05","GEO-38001-c06","GEO-38001-c07","GEO-38001-c08","GEO-38001-c09","GEO-38001-w01"],
     "volume_range":"卷38",
     "attributes":{
       "borders":[{"direction":"东","to_place":"赭山海口","distance_li":60},
                  {"direction":"西","to_place":"严州府桐庐县界","distance_li":135},
                  {"direction":"南","to_place":"绍兴府萧山县界","distance_li":45},
                  {"direction":"北","to_place":"湖州府德清县界","distance_li":45}],
       "to_capital":[{"capital":"南京","distance_li":900},{"capital":"京师","distance_li":4200}],
       "households":{"count":None,"unit":"里","note":"领县九；各属县编户见下"},
       "grain_tax":{"amount":234200,"unit":"石","note":"粮二十三万四千二百石零"},
       "jun_name":"钱塘【陈名】武林【因武林山而名】古杭【隋名】",
       "topography":"湖山暎带【宋欧阳修有美堂记】；山川秀丽【宋葛澧帝都赋】；左浙江右具区北大海南天目【宋晁无咎文】；龙山据其首西湖蟠其腹天竺耸其膺东山卧其背【西征记】；外带江海内抱湖山【宋秦观雪斋记】；水陆之防【宋苏轼云】；蟠幽宅阻面湖背海【宋王阮礼部对策】",
       "customs":"以船檝为车马【吴越春秋】；吴越尚勇【汉志】；俗尚侈靡【临安志】；尚礼厚厐【隋志】；人性敏慧【宋史地理志】；习俗工巧【宋欧阳修有美堂记】",
       "garrisons":[{"name":"杭州前卫","type":"卫","location_text":"在都司前洪武八年建"},
                    {"name":"杭州右卫","type":"卫","location_text":"在都司前洪武八年建"},
                    {"name":"海宁守御千户所","type":"千户所","location_text":"在海宁县东洪武二十年建"}]
     },
     "cit_ids":["CIT-001","CIT-002","CIT-003","CIT-004","CIT-005","CIT-006","CIT-007","CIT-008"]},
    {"geo_id":"GEO-38001-c01","item_id":"38-001","name":"钱塘县","type":"county","region":"浙江","parent":"GEO-38001","children":[],"volume_range":"卷38","attributes":{"location_text":"附郭","households":{"count":160,"unit":"里","note":"编户一百六十里"}}},
    {"geo_id":"GEO-38001-c02","item_id":"38-001","name":"仁和县","type":"county","region":"浙江","parent":"GEO-38001","children":[],"volume_range":"卷38","attributes":{"location_text":"附郭","households":{"count":360,"unit":"里","note":"编户三百六十里"}}},
    {"geo_id":"GEO-38001-c03","item_id":"38-001","name":"海宁县","type":"county","region":"浙江","parent":"GEO-38001","children":[],"volume_range":"卷38","attributes":{"location_text":"在府城东一百二十里","households":{"count":356,"unit":"里","note":"编户三百五十六里"}}},
    {"geo_id":"GEO-38001-c04","item_id":"38-001","name":"余杭县","type":"county","region":"浙江","parent":"GEO-38001","children":[],"volume_range":"卷38","attributes":{"location_text":"在府城西北七十里","households":{"count":73,"unit":"里","note":"编户七十三里"}}},
    {"geo_id":"GEO-38001-c05","item_id":"38-001","name":"临安县","type":"county","region":"浙江","parent":"GEO-38001","children":[],"volume_range":"卷38","attributes":{"location_text":"在府城西一百里","households":{"count":48,"unit":"里","note":"编户四十八里"}}},
    {"geo_id":"GEO-38001-c06","item_id":"38-001","name":"富阳县","type":"county","region":"浙江","parent":"GEO-38001","children":[],"volume_range":"卷38","attributes":{"location_text":"在府城西九十里","households":{"count":75,"unit":"里","note":"编户七十五里"}}},
    {"geo_id":"GEO-38001-c07","item_id":"38-001","name":"於潜县","type":"county","region":"浙江","parent":"GEO-38001","children":[],"volume_range":"卷38","attributes":{"location_text":"在府城西一百七十里","households":{"count":12,"unit":"里","note":"编户一十二里"}}},
    {"geo_id":"GEO-38001-c08","item_id":"38-001","name":"新城县","type":"county","region":"浙江","parent":"GEO-38001","children":[],"volume_range":"卷38","attributes":{"location_text":"在府城西一百四十里","households":{"count":15,"unit":"里","note":"编户一十五里"}}},
    {"geo_id":"GEO-38001-c09","item_id":"38-001","name":"昌化县","type":"county","region":"浙江","parent":"GEO-38001","children":[],"volume_range":"卷38","attributes":{"location_text":"在府城西二百一十里","households":{"count":10,"unit":"里","note":"编户一十里"}}},
    {"geo_id":"GEO-38001-w01","item_id":"38-001","name":"海宁守御千户所","type":"weisuo","region":"浙江","parent":"GEO-38001","children":[],"volume_range":"卷38","attributes":{"location_text":"在海宁县东洪武二十年建","garrison_type":"千户所"}}
]

# ---- EVO ----
evos = [
    {"evo_id":"EVO-001","item_id":"38-001","geo_id":"GEO-38001","dynasty":"夏","era":None,"institution_name":"扬州之域","action":"因之","detail":"禹贡扬州之域，天文斗分野"},
    {"evo_id":"EVO-002","item_id":"38-001","geo_id":"GEO-38001","dynasty":"春秋","era":None,"institution_name":"吴越地","action":"因之","detail":"春秋时属吴越"},
    {"evo_id":"EVO-003","item_id":"38-001","geo_id":"GEO-38001","dynasty":"战国","era":None,"institution_name":"楚地","action":"因之","detail":"战国时属楚"},
    {"evo_id":"EVO-004","item_id":"38-001","geo_id":"GEO-38001","dynasty":"秦","era":None,"institution_name":"会稽郡地","action":"置","detail":"秦为会稽郡地"},
    {"evo_id":"EVO-005","item_id":"38-001","geo_id":"GEO-38001","dynasty":"东汉","era":None,"institution_name":"吴郡地","action":"因之","detail":"东汉属吴郡"},
    {"evo_id":"EVO-006","item_id":"38-001","geo_id":"GEO-38001","dynasty":"三国吴","era":None,"institution_name":"东安郡","action":"置","detail":"三国吴分置东安郡治富春寻罢"},
    {"evo_id":"EVO-007","item_id":"38-001","geo_id":"GEO-38001","dynasty":"晋","era":None,"institution_name":"吴兴及吴郡","action":"因之","detail":"晋属吴兴及吴郡"},
    {"evo_id":"EVO-008","item_id":"38-001","geo_id":"GEO-38001","dynasty":"陈","era":None,"institution_name":"钱塘郡","action":"置","detail":"陈置钱塘郡"},
    {"evo_id":"EVO-009","item_id":"38-001","geo_id":"GEO-38001","dynasty":"隋","era":"大业","institution_name":"杭州/余杭郡","action":"改","detail":"隋废郡置杭州治余杭未几移治钱塘，大业初改州为余杭郡"},
    {"evo_id":"EVO-010","item_id":"38-001","geo_id":"GEO-38001","dynasty":"唐","era":"天宝/乾元","institution_name":"余杭郡/杭州","action":"改","detail":"唐初复为杭州，天宝初又为余杭郡，乾元初复为杭州，景福初号武胜军，光化初移镇海节度治于杭置大都督府"},
    {"evo_id":"EVO-011","item_id":"38-001","geo_id":"GEO-38001","dynasty":"五代","era":None,"institution_name":"吴越国","action":"因之","detail":"五代时为吴越国"},
    {"evo_id":"EVO-012","item_id":"38-001","geo_id":"GEO-38001","dynasty":"宋","era":None,"institution_name":"临安府","action":"升","detail":"宋为杭州，高宗南渡迁都于杭，升为临安府"},
    {"evo_id":"EVO-013","item_id":"38-001","geo_id":"GEO-38001","dynasty":"元","era":None,"institution_name":"杭州路","action":"改","detail":"元立两浙都督府寻改杭州路"},
    {"evo_id":"EVO-014","item_id":"38-001","geo_id":"GEO-38001","dynasty":"明","era":None,"institution_name":"杭州府","action":"因之","detail":"本朝改为杭州府，领县九"}
]

# ---- MTN ----
mtns = [
    {"mtn_id":"MTN-001","item_id":"38-001","geo_id":"GEO-38001-c01","name":"吴山","type":"山","location_text":"在府治东南","description":"吴人怜子胥以谏死立祠其上，又名胥山，左临大江右瞰西湖","lore":"因纪念伍子胥得名"},
    {"mtn_id":"MTN-002","item_id":"38-001","geo_id":"GEO-38001-c01","name":"凤凰山","type":"山","location_text":"在府治南二里","description":"下俯大江直望海门，山势若凤凰欲飞之状","lore":"南宋大内所在地"},
    {"mtn_id":"MTN-003","item_id":"38-001","geo_id":"GEO-38001-c01","name":"南屏山","type":"山","location_text":"在府城西三里","description":"怪石耸秀中穿一洞，其上石壁若屏","lore":""},
    {"mtn_id":"MTN-004","item_id":"38-001","geo_id":"GEO-38001-c01","name":"孤山","type":"山","location_text":"在府城外西湖上","description":"独立一峰为湖山胜绝处，上有林逋祠","lore":"林逋隐居处"},
    {"mtn_id":"MTN-005","item_id":"38-001","geo_id":"GEO-38001-c01","name":"秦望山","type":"山","location_text":"在府城南一十里","description":"秦始皇东游登此欲渡会稽故名","lore":""},
    {"mtn_id":"MTN-006","item_id":"38-001","geo_id":"GEO-38001-c01","name":"武林山","type":"山","location_text":"在府城西南一十五里","description":"武林水所出，亦曰灵隐曰灵苑，本名虎林唐避讳改武","lore":"杭州别称武林由此"},
    {"mtn_id":"MTN-007","item_id":"38-001","geo_id":"GEO-38001-c02","name":"皋亭山","type":"山","location_text":"在府城东北二十五里","description":"高百余丈，云出则雨","lore":"元巴延入宋临安时驻兵此山下"},
    {"mtn_id":"MTN-008","item_id":"38-001","geo_id":"GEO-38001-c02","name":"临平山","type":"山","location_text":"在府城东北六十里","description":"上有龙洞，山顶有井，旱亦不涸","lore":"苏轼有诗"},
    {"mtn_id":"MTN-009","item_id":"38-001","geo_id":"GEO-38001-c03","name":"紫微山","type":"山","location_text":"在海宁县东北六十里","description":"唐白居易尝登此山望硖石湖","lore":""},
    {"mtn_id":"MTN-010","item_id":"38-001","geo_id":"GEO-38001-c06","name":"小隐山","type":"山","location_text":"在富阳县治北","description":"为县治镇山，宋谢绛迁居于此","lore":"范仲淹有诗"},
    {"mtn_id":"MTN-011","item_id":"38-001","geo_id":"GEO-38001-c04","name":"大涤山","type":"山","location_text":"在余杭县西南一十八里","description":"中有日月分精金堂玉室，中峰之上有许迈升天坛","lore":"道家名山，洞霄宫所在地"},
    {"mtn_id":"MTN-012","item_id":"38-001","geo_id":"GEO-38001-c04","name":"天柱山","type":"山","location_text":"在余杭县西南一十八里","description":"四隅陡绝耸翠参天，为道家第五十七福地","lore":""},
    {"mtn_id":"MTN-013","item_id":"38-001","geo_id":"GEO-38001-c05","name":"衣锦山","type":"山","location_text":"在临安县治南","description":"本名石镜山，东峰有圆石其光如鉴，钱镠幼时游此","lore":"吴越王钱镠故里象征"},
    {"mtn_id":"MTN-014","item_id":"38-001","geo_id":"GEO-38001-c05","name":"天目山","type":"山","location_text":"在临安县西五十里","description":"为道家第三十四洞天，山下两湖若左右目故名","lore":"郭璞云天目山前两乳长龙飞凤舞到钱塘"},
    {"mtn_id":"MTN-015","item_id":"38-001","geo_id":"GEO-38001-c05","name":"径山","type":"山","location_text":"天目之东北峰","description":"有路可通天目故名径山，五峰周抱奇胜特异","lore":"佛教名山，径山寺所在地"},
    {"mtn_id":"MTN-016","item_id":"38-001","geo_id":"GEO-38001-c07","name":"西菩山","type":"山","location_text":"在於潜县西一十三里","description":"九锁交陈双峰对峙，上有明智寺，宋僧参寥子居此","lore":"苏轼有诗"},
    {"mtn_id":"MTN-017","item_id":"38-001","geo_id":"GEO-38001-c07","name":"生仙山","type":"山","location_text":"在於潜县南三十里","description":"汉天师张道陵生于此山之西因名","lore":""},
    {"mtn_id":"MTN-018","item_id":"38-001","geo_id":"GEO-38001-c09","name":"百丈山","type":"山","location_text":"在昌化县西三十里","description":"亦名潜山，相传尧时洪水惟此山潜水中不没者百丈故名","lore":""},
    {"mtn_id":"MTN-019","item_id":"38-001","geo_id":"GEO-38001-c09","name":"千顷山","type":"山","location_text":"在昌化县西北六十里","description":"上广千顷，山有龙湫鱼皆金银色祷雨多应","lore":""},
    {"mtn_id":"MTN-020","item_id":"38-001","geo_id":"GEO-38001-c01","name":"飞来峰","type":"峰","location_text":"在府城西二十里","description":"晋咸和中西天僧慧理登此山叹曰此是中天竺国灵鹫山之小岭不知何年飞来","lore":"佛教传说"},
    {"mtn_id":"MTN-021","item_id":"38-001","geo_id":"GEO-38001-c01","name":"南高峰","type":"峰","location_text":"在府城西一十二里","description":"上有古塔下有石屋","lore":""},
    {"mtn_id":"MTN-022","item_id":"38-001","geo_id":"GEO-38001-c01","name":"北高峰","type":"峰","location_text":"在府城西北二十三里","description":"上有塔高七层","lore":""},
    {"mtn_id":"MTN-023","item_id":"38-001","geo_id":"GEO-38001-c01","name":"风篁岭","type":"岭","location_text":"在府城西一十二里","description":"修篁怪石风韵萧爽因名","lore":"苏轼诗有问信风篁岭下梅句"},
    {"mtn_id":"MTN-024","item_id":"38-001","geo_id":"GEO-38001-c01","name":"栖霞岭","type":"岭","location_text":"在西湖上","description":"一名剑门岭，旧多桃花开时烂然如霞故名","lore":"岳飞墓在此岭下"},
    {"mtn_id":"MTN-025","item_id":"38-001","geo_id":"GEO-38001-c01","name":"浙江","type":"江","location_text":"在府城西三里","description":"出歙县玉山，经建德合婺溪过富春为浙江入于海，潮水投山十折而曲","lore":"卢肇曰浙者折也"},
    {"mtn_id":"MTN-026","item_id":"38-001","geo_id":"GEO-38001-c06","name":"富春江","type":"江","location_text":"在富阳县南","description":"即浙江之上流","lore":""},
    {"mtn_id":"MTN-027","item_id":"38-001","geo_id":"GEO-38001-c01","name":"西湖","type":"湖","location_text":"在府城西","description":"周回三十里，其源出于武林泉，自唐以来为东南游赏胜处，旧称西湖十景","lore":"白居易苏轼皆有诗；苏公堤即苏轼所筑"},
    {"mtn_id":"MTN-028","item_id":"38-001","geo_id":"GEO-38001-c04","name":"苕溪","type":"溪","location_text":"在余杭县治前","description":"发源天目山由于潜临安东流至余杭经钱塘入湖州，夹崖多苕花秋飘散水上如飞雪因名","lore":""},
    {"mtn_id":"MTN-029","item_id":"38-001","geo_id":"GEO-38001-c01","name":"虎跑泉","type":"泉","location_text":"在府城西南虎跑寺","description":"旧传性空禅师居大慈山无水，夜二虎跑地泉涌出故名","lore":""},
    {"mtn_id":"MTN-030","item_id":"38-001","geo_id":"GEO-38001-c01","name":"龙井","type":"泉","location_text":"在西湖上","description":"旧名龙泓，相传有龙居之，宋元丰中僧辩才即其处为亭","lore":"秦观记"},
    {"mtn_id":"MTN-031","item_id":"38-001","geo_id":"GEO-38001-c01","name":"六井","type":"井","location_text":"在钱塘县","description":"唐刺史李泌始引西湖作六井以便民汲，白居易复开治之","lore":"苏轼记其详情"},
    {"mtn_id":"MTN-032","item_id":"38-001","geo_id":"GEO-38001-c01","name":"钱塘","type":"塘","location_text":"在府城南","description":"唐功曹华信议立此塘以防海水，募能致土石一斛与千钱，旬月之间塘遂成因号钱塘","lore":"杭州地名由来"},
    {"mtn_id":"MTN-033","item_id":"38-001","geo_id":"GEO-38001-c01","name":"捍海塘","type":"塘","location_text":"在府城东三里","description":"梁开平中钱武肃王始建，潮水冲激板筑不就，因命强弩数百以射潮头，既而积石植木为塘","lore":"吴越王射潮传说"},
    {"mtn_id":"MTN-034","item_id":"38-001","geo_id":"GEO-38001-c01","name":"苏公堤","type":"堤","location_text":"在西湖上","description":"宋元祐中苏轼取葑田积湖中南北径三十里为长堤，植芙蓉杨柳其上望之如图画","lore":""}
]

# ---- CIT ----
cits = [
    {"cit_id":"CIT-001","item_id":"38-001","cited_work":"欧阳修有美堂记","cited_work_ent_id":None,"context":"形势","original":"【宋欧阳修有美堂记邑屋华丽十余万家环以湖山左右映带】"},
    {"cit_id":"CIT-002","item_id":"38-001","cited_work":"葛澧帝都赋","cited_work_ent_id":None,"context":"形势","original":"【宋葛澧帝都赋据东南之都会号繁盛之乐土】"},
    {"cit_id":"CIT-003","item_id":"38-001","cited_work":"晁无咎文","cited_work_ent_id":None,"context":"形势","original":"【宋晁无咎文左浙江右具区北大海南天目】"},
    {"cit_id":"CIT-004","item_id":"38-001","cited_work":"西征记","cited_work_ent_id":None,"context":"形势","original":"【西征记龙山据其首西湖蟠其腹天竺耸其膺东山卧其背】"},
    {"cit_id":"CIT-005","item_id":"38-001","cited_work":"秦观雪斋记","cited_work_ent_id":None,"context":"形势","original":"【宋秦观雪斋记外带涛江涨海之险内抱湖山竹林之盛】"},
    {"cit_id":"CIT-006","item_id":"38-001","cited_work":"吴越春秋","cited_work_ent_id":None,"context":"风俗","original":"【吴越春秋水行山处以船为车以檝为马】"},
    {"cit_id":"CIT-007","item_id":"38-001","cited_work":"汉志","cited_work_ent_id":None,"context":"风俗","original":"【汉志吴越之君皆尚勇故其民好用剑轻死易发】"},
    {"cit_id":"CIT-008","item_id":"38-001","cited_work":"隋志","cited_work_ent_id":None,"context":"风俗","original":"【隋志其人君子尚礼庸庶厚厐】"}
]

# ---- ENT ----
ents = [
    {"ent_id":"ENT-001","name":"杭州府","type":"geo","norm":"杭州府","first_source":"38-001"},
    {"ent_id":"ENT-002","name":"钱塘县","type":"geo","norm":"钱塘县","first_source":"38-001"},
    {"ent_id":"ENT-003","name":"仁和县","type":"geo","norm":"仁和县","first_source":"38-001"},
    {"ent_id":"ENT-004","name":"海宁县","type":"geo","norm":"海宁县","first_source":"38-001"},
    {"ent_id":"ENT-005","name":"余杭县","type":"geo","norm":"余杭县","first_source":"38-001"},
    {"ent_id":"ENT-006","name":"临安县","type":"geo","norm":"临安县","first_source":"38-001"},
    {"ent_id":"ENT-007","name":"富阳县","type":"geo","norm":"富阳县","first_source":"38-001"},
    {"ent_id":"ENT-008","name":"於潜县","type":"geo","norm":"於潜县","first_source":"38-001"},
    {"ent_id":"ENT-009","name":"新城县","type":"geo","norm":"新城县","first_source":"38-001"},
    {"ent_id":"ENT-010","name":"昌化县","type":"geo","norm":"昌化县","first_source":"38-001"},
    {"ent_id":"ENT-011","name":"海宁守御千户所","type":"geo","norm":"海宁守御千户所","first_source":"38-001"},
    {"ent_id":"ENT-012","name":"吴山","type":"mtn","norm":"吴山","first_source":"38-001"},
    {"ent_id":"ENT-013","name":"西湖","type":"mtn","norm":"西湖","first_source":"38-001"},
    {"ent_id":"ENT-014","name":"浙江","type":"mtn","norm":"浙江","first_source":"38-001"},
    {"ent_id":"ENT-015","name":"天目山","type":"mtn","norm":"天目山","first_source":"38-001"},
    {"ent_id":"ENT-016","name":"灵隐寺","type":"site","norm":"灵隐寺","first_source":"38-001"},
    {"ent_id":"ENT-017","name":"净慈寺","type":"site","norm":"净慈寺","first_source":"38-001"},
    {"ent_id":"ENT-018","name":"岳飞墓","type":"site","norm":"岳飞墓","first_source":"38-001"},
    {"ent_id":"ENT-019","name":"钱镠","type":"person","norm":"钱镠","first_source":"38-001"},
    {"ent_id":"ENT-020","name":"苏轼","type":"person","norm":"苏轼","first_source":"38-001"},
    {"ent_id":"ENT-021","name":"白居易","type":"person","norm":"白居易","first_source":"38-001"},
    {"ent_id":"ENT-022","name":"林逋","type":"person","norm":"林逋","first_source":"38-001"},
    {"ent_id":"ENT-023","name":"岳飞","type":"person","norm":"岳飞","first_source":"38-001"},
    {"ent_id":"ENT-024","name":"于谦","type":"person","norm":"于谦","first_source":"38-001"},
    {"ent_id":"ENT-025","name":"欧阳修","type":"person","norm":"欧阳修","first_source":"38-001"},
    {"ent_id":"ENT-026","name":"吴越春秋","type":"book","norm":"吴越春秋","first_source":"38-001"},
    {"ent_id":"ENT-027","name":"临安志","type":"book","norm":"临安志","first_source":"38-001"}
]

# ---- Main file ----
main = {
    "item_id":"38-001","volume":"38","source":"杭州府","region":"浙江",
    "layers":{"ents":ents,"geos":geos,"evos":evos,"mtns":mtns,"pers":[],"sites":[],"prods":[],"cits":cits},
    "layer_count":7,
    "validation":{"errs":[],"gap":0,"notes":"pers拆至pers1/2/3；sites拆至sites1/2"},
    "title":"杭州府"
}
with open(os.path.join(BASE,"38-001_杭州府.json"),"w",encoding="utf-8") as f:
    json.dump(main,f,ensure_ascii=False,indent=2)
print(f"主文件: ents={len(ents)} geos={len(geos)} evos={len(evos)} mtns={len(mtns)} cits={len(cits)}")

# ---- PERS1 名宦 ----
pers1 = [
    {"per_id":"PER-001","item_id":"38-001","geo_id":"GEO-38001-c04","name":"陈浑","type":"名宦","dynasty":"汉","native_place":"","office":"余杭令","summary":"嘉平间为余杭令，筑南湖塘凿石门以御水患，民立祠祀之","original":"汉陈浑【嘉平间为余杭令筑南湖塘凿石门以御水患民立祠祀之】"},
    {"per_id":"PER-002","item_id":"38-001","geo_id":"GEO-38001-c03","name":"陆逊","type":"名宦","dynasty":"三国吴","native_place":"吴郡","office":"海昌都尉","summary":"出为海昌都尉并领县事，开仓赈饥劝督农桑，讨贼所向皆服","original":"三国陆逊【出为海昌都尉并领县事开仓以赈饥民劝督农桑率所募兵以讨贼所向皆服】"},
    {"per_id":"PER-003","item_id":"38-001","geo_id":"GEO-38001-c01","name":"李泌","type":"名宦","dynasty":"唐","native_place":"京兆","office":"杭州刺史","summary":"大历中为杭州刺史，郡中卤水不可饮，乃引湖水入城为六井大为民利","original":"李泌【大厯中为杭州刺史有风绩郡中卤水不可饮泌乃引湖水入城为六井大为民利】"},
    {"per_id":"PER-004","item_id":"38-001","geo_id":"GEO-38001-c01","name":"白居易","type":"名宦","dynasty":"唐","native_place":"太原","office":"杭州刺史","summary":"长庆初筑堤捍钱塘湖溉田千顷，复浚李泌六井民赖其利","original":"白居易【长庆初为杭州刺史始筑隄捍钱塘湖钟泄其水溉田千顷复浚李泌六井民赖其利】"},
    {"per_id":"PER-005","item_id":"38-001","geo_id":"GEO-38001-c04","name":"归珧","type":"名宦","dynasty":"唐","native_place":"","office":"余杭令","summary":"宝历间因汉陈浑故迹置上下湖溉田千余顷，筑甬道通西北大路","original":"归珧【宝厯间为余杭令因汉陈浑故迹置上下湖溉田千余顷又筑甬道通西北大路】"},
    {"per_id":"PER-006","item_id":"38-001","geo_id":"GEO-38001-c01","name":"苏轼","type":"名宦","dynasty":"宋","native_place":"眉山","office":"知杭州","summary":"元祐初知杭州值大旱饥疫，请免上供米三之一，遣使督医分坊治病全活甚众，筑苏公堤","original":"苏轼【元祐初知杭州值大旱饥疫轼请免本路上供米三之一仍遣使督医分坊治病全活者甚众民为立生祠】"},
    {"per_id":"PER-007","item_id":"38-001","geo_id":"GEO-38001-c01","name":"范仲淹","type":"名宦","dynasty":"宋","native_place":"苏州","office":"知杭州","summary":"皇祐初知杭州，时郡中大饥，发粟募民存饷，又谕诸寺工作贸易饮食以惠贫者，两浙惟杭州晏然","original":"范仲淹【皇祐初知杭州时郡中大饥殍殣枕路仲淹发粟及募民存饷为术甚备自是两浙惟杭州晏然民不流徙】"},
    {"per_id":"PER-008","item_id":"38-001","geo_id":"GEO-38001-c01","name":"赵抃","type":"名宦","dynasty":"宋","native_place":"衢州","office":"知杭州","summary":"熙宁间知杭州，岁旱民病议筑城则罢之，杭多盗取情重者配他州余遂散去","original":"赵抃【熈寜间知杭州岁旱民病朝廷议欲筑城抃曰民未可劳罢之杭故多盗抃取其情重者配他州余遂散去境内以清】"},
    {"per_id":"PER-009","item_id":"38-001","geo_id":"GEO-38001-c04","name":"杨时","type":"名宦","dynasty":"宋","native_place":"将乐","office":"余杭令","summary":"为余杭令以教化为先务不为烦苛，去官民怀其惠立祠祀之","original":"杨时【为余杭令以教化为先务不为烦苛后去官民懐其惠立祠祀之】"},
    {"per_id":"PER-010","item_id":"38-001","geo_id":"GEO-38001-c03","name":"臧梦解","type":"名宦","dynasty":"元","native_place":"","office":"知海宁州","summary":"至元中知海宁州刚直廉慎，差役皆当其贫富，户增田辟政平讼简为诸州最","original":"臧梦解【至元中知海宁州刚直亷慎差役皆当其富贫以致户増田辟政平讼简为诸州最】"},
    {"per_id":"PER-011","item_id":"38-001","geo_id":"GEO-38001-c01","name":"王兴福","type":"名宦","dynasty":"明","native_place":"","office":"知杭州府","summary":"洪武初知杭州府，为政明于大体不尚苛刻，民赖以安，寻升吏部尚书","original":"本朝王兴福【洪武初知杭州府为政明于大体不尚苛刻民赖以安去任民遮道送之寻陞吏部尚书】"},
    {"per_id":"PER-012","item_id":"38-001","geo_id":"GEO-38001-c01","name":"于谦","type":"名宦","dynasty":"明","native_place":"钱塘","office":"兵部尚书","summary":"景泰初进本部尚书力拒南迁妄议京师赖之以安，英皇复位被诬赐死，成化初赠少保谥肃愍","original":"于谦【钱塘人永乐末登进士景泰初进本部尚书力拒南迁妄议京师赖之以安英皇复位石亨等诬以迎立外藩赐死成化初赠少保諡肃愍】"},
    {"per_id":"PER-013","item_id":"38-001","geo_id":"GEO-38001-c02","name":"刘大夏","type":"名宦","dynasty":"明","native_place":"华容","office":"浙江左布政","summary":"成化末浙江左布政，勤抚字缓催科务在节用爱人，提调弘治二年乡试得王守仁胡世宁孙燧诸人","original":"刘大夏【成化末浙江左布政勤抚字缓催科务在节用爱人提调治二年乡试得王守仁胡世宁孙燧诸人】"},
    {"per_id":"PER-014","item_id":"38-001","geo_id":"GEO-38001-c02","name":"杨继宗","type":"名宦","dynasty":"明","native_place":"","office":"浙江按察使","summary":"天顺中浙江按察使，军民爱之如父母，官吏畏之如神明","original":"杨继宗【天顺中浙江按察使军民爱之如父母官吏畏之如神明】"}
]
with open(os.path.join(BASE,"38-001_pers1_名宦.json"),"w",encoding="utf-8") as f:
    json.dump({"item_id":"38-001","volume":"38","source":"杭州府","region":"浙江","layers":{"ents":[],"geos":[],"evos":[],"mtns":[],"pers":pers1,"sites":[],"prods":[],"cits":[]},"layer_count":7,"title":"杭州府"},f,ensure_ascii=False,indent=2)
print(f"pers1名宦: {len(pers1)}")

# ---- PERS2 人物 ----
pers2 = [
    {"per_id":"PER-101","item_id":"38-001","geo_id":"GEO-38001-c05","name":"钱镠","type":"人物","dynasty":"五代","native_place":"临安","office":"吴越王","summary":"破黄巢讨刘汉宏，昭宗拜镇海镇东两军节度使，梁封吴越王，传至忠懿王俶纳土于宋","original":"钱镠【临安人黄巢乱镠以乡人破走之讨刘汉宏遂破越州昭宗拜为镇海镇东两军节度使梁封吴越王至忠懿王俶纳土于宋】"},
    {"per_id":"PER-102","item_id":"38-001","geo_id":"GEO-38001-c01","name":"褚遂良","type":"人物","dynasty":"唐","native_place":"钱塘","office":"尚书右仆射","summary":"博涉文史工楷书，受顾命辅高宗，帝将立武后遂良力谏不纳，累贬爱州刺史以忧卒","original":"褚遂良【亮子博涉文史工楷贞观中歴官谏议大夫迁尚书右仆射帝将立武后遂良力諌不纳后累贬爱州刺史竟以忧卒】"},
    {"per_id":"PER-103","item_id":"38-001","geo_id":"GEO-38001-c01","name":"林逋","type":"人物","dynasty":"宋","native_place":"钱塘","office":"隐居","summary":"少孤刻志为学，性恬淡好古弗趋荣利，善行书喜为诗，居西湖二十年未尝履城市，卒赐谥和靖先生","original":"林逋【钱塘人少孤刻志为学性恬澹好古弗趋荣利善行书喜为诗居西湖二十年未尝履城市仁宗时卒赐諡和靖先生】"},
    {"per_id":"PER-104","item_id":"38-001","geo_id":"GEO-38001-c01","name":"周邦彦","type":"人物","dynasty":"宋","native_place":"钱塘","office":"徽猷阁待制","summary":"元丰中献汴都赋万余言，世传其词调最工，有文集二十四卷","original":"周邦彦【钱塘人元丰中献汴都赋万余言世传其词调最工仕至徽猷阁待制】"},
    {"per_id":"PER-105","item_id":"38-001","geo_id":"GEO-38001-c07","name":"洪咨夔","type":"人物","dynasty":"宋","native_place":"於潜","office":"刑部尚书","summary":"嘉定初进士，历监察御史论权归人主，迁刑部尚书拜翰林学士知制诰，为人鲠亮忠悫","original":"洪咨防【于潜人嘉定初进士歴官监察御史迁吏部侍郞进刑部尚书拜翰林学士知制诰为人鲠亮忠慤】"},
    {"per_id":"PER-106","item_id":"38-001","geo_id":"GEO-38001-c06","name":"李宗勉","type":"人物","dynasty":"宋","native_place":"富阳","office":"左丞相兼枢密使","summary":"嘉熙中累迁至左丞相，守法度抑侥幸不私亲党，身居台辅家若贫儒，卒谥文清","original":"李宗勉【富阳人开禧初进士嘉熈中累迁至左丞相兼枢密使守法度抑侥幸不私亲党身居台辅家若贫儒卒諡文清】"},
    {"per_id":"PER-107","item_id":"38-001","geo_id":"GEO-38001-c08","name":"罗隐","type":"人物","dynasty":"唐","native_place":"新城","office":"给事中","summary":"有能诗名，劝钱镠讨朱温，表为钱塘令辟掌书记，所著有江南甲乙集","original":"罗隐【新城人有能诗名尝説钱镠举兵讨朱温唐光啓中镠表为钱塘令辟为掌书记后为给事中所著有江南甲乙集】"},
    {"per_id":"PER-108","item_id":"38-001","geo_id":"GEO-38001-c06","name":"黄公望","type":"人物","dynasty":"元","native_place":"富阳","office":"画家","summary":"聪敏绝伦尤工画山水，号大痴道人，元四家之一，放浪江湖年八十余卒","original":"黄公望【富阳人聪敏絶伦尤工画山水更名坚号一峯又自称大痴道人放浪江湖年八十余卒】"},
    {"per_id":"PER-109","item_id":"38-001","geo_id":"GEO-38001-c05","name":"赵孟頫","type":"人物","dynasty":"元","native_place":"湖州","office":"江浙儒学提举","summary":"博学多闻操履纯正，以诗文书法名世","original":"赵孟頫【江浙等处儒学提举博学多闻操履纯正以诗文鸣世】"}
]
with open(os.path.join(BASE,"38-001_pers2_人物.json"),"w",encoding="utf-8") as f:
    json.dump({"item_id":"38-001","volume":"38","source":"杭州府","region":"浙江","layers":{"ents":[],"geos":[],"evos":[],"mtns":[],"pers":pers2,"sites":[],"prods":[],"cits":[]},"layer_count":7,"title":"杭州府"},f,ensure_ascii=False,indent=2)
print(f"pers2人物: {len(pers2)}")

# ---- PERS3 列女仙释 ----
pers3 = [
    {"per_id":"PER-201","item_id":"38-001","geo_id":"GEO-38001-c04","name":"姚氏","type":"列女","dynasty":"元","native_place":"余杭","office":"","summary":"虎衔其母，姚仓卒往逐之以手殴虎，负母归求药疗之","original":"姚氏【元余杭人居山谷间虎衔其母姚仓卒往逐之即以手殴虎负母归求药疗之】"},
    {"per_id":"PER-202","item_id":"38-001","geo_id":"GEO-38001-c02","name":"平氏","type":"列女","dynasty":"明","native_place":"仁和","office":"何富妻","summary":"年十九归何富，五年而富没，生男誓不再适，事舅姑抚孤四十年如一日，洪武间表其闾","original":"平氏【仁和人年十九归同里何富五年而富没越五月生男誓不再适事舅姑惟谨抚孤至成人四十年如一日洪武间表其闾】"},
    {"per_id":"PER-203","item_id":"38-001","geo_id":"GEO-38001-c05","name":"许迈","type":"仙释","dynasty":"晋","native_place":"丹阳","office":"道士","summary":"永和间入临安西山登岩茹芝，着诗十二篇论神仙事，莫测所终皆谓之羽化","original":"许迈【晋永和间入临安西山登岩茹芝遂更名元字逺游着诗十二首论神仙事莫测所终皆谓之羽化云】"},
    {"per_id":"PER-204","item_id":"38-001","geo_id":"GEO-38001-c07","name":"道潜","type":"仙释","dynasty":"宋","native_place":"於潜","office":"诗僧","summary":"号参寥子，通内外典能文章尤善诗，苏轼守杭日卜智果精舍居之，苏辙称其诗无一点蔬笋气","original":"道潜【于潜人通内外典能文章尤善为诗苏轼守杭日卜智果精舍居之苏辙称其诗无一点蔬笋气体制絶似储光羲】"},
    {"per_id":"PER-205","item_id":"38-001","geo_id":"GEO-38001-c01","name":"明本","type":"仙释","dynasty":"元","native_place":"杭州","office":"禅师","summary":"号中峰，为文未尝构思援笔立就，四方从学者甚众，元仁宗赐号广慧禅师，文宗赐谥智觉","original":"明本【号中峯杭州人防聪悟博涉书史为文未尝搆思援笔立就元仁宗赐号广慧禅师及殁文宗赐諡智觉】"},
    {"per_id":"PER-206","item_id":"38-001","geo_id":"GEO-38001-c04","name":"邓牧","type":"仙释","dynasty":"元","native_place":"钱塘","office":"道士","summary":"字牧心，能通庄列诸书，尝居余杭洞霄宫超然馆，大德间无疾而逝，著有洞霄志","original":"邓牧【钱塘人能通庄列诸书尝居余杭洞霄宫之超然馆元大德间无疾而逝所着有洞霄志文藁】"}
]
with open(os.path.join(BASE,"38-001_pers3_列女仙释.json"),"w",encoding="utf-8") as f:
    json.dump({"item_id":"38-001","volume":"38","source":"杭州府","region":"浙江","layers":{"ents":[],"geos":[],"evos":[],"mtns":[],"pers":pers3,"sites":[],"prods":[],"cits":[]},"layer_count":7,"title":"杭州府"},f,ensure_ascii=False,indent=2)
print(f"pers3列女仙释: {len(pers3)}")

# ---- SITES1 寺观祠庙陵墓 ----
sites1 = [
    {"site_id":"SITE-001","item_id":"38-001","geo_id":"GEO-38001-c01","name":"灵隐寺","type":"寺观","location_text":"在武林山","history_lore":"晋咸和初建，寺有观风虚白候仙见山冷泉五亭，外夹道有九里松","original":"灵隐寺【在武林山晋咸和初建寺有观风虚白候仙见山冷泉五亭寺外夹道有九里松】"},
    {"site_id":"SITE-002","item_id":"38-001","geo_id":"GEO-38001-c01","name":"净慈寺","type":"寺观","location_text":"在西湖上","history_lore":"周显德中建，寺有五百罗汉各高数丈，苏轼有谒本长老诗","original":"净慈寺【在西湖上周显德中建寺有五百罗汉各髙数丈苏轼谒本长老诗】"},
    {"site_id":"SITE-003","item_id":"38-001","geo_id":"GEO-38001-c01","name":"上天竺寺","type":"寺观","location_text":"在府城西一十九里","history_lore":"晋天福中建，有乳窦白云狮子双桂诸峰拱揖左右","original":"上天竺寺【在府城西一十九里晋天福中建有乳窦白云狮子双桂诸峯拱揖左右】"},
    {"site_id":"SITE-004","item_id":"38-001","geo_id":"GEO-38001-c05","name":"径山寺","type":"寺观","location_text":"在天目山东北","history_lore":"寺多先贤碑文并名人题咏","original":"径山寺【在天目山东北寺多先贤碑文并名人题咏】"},
    {"site_id":"SITE-005","item_id":"38-001","geo_id":"GEO-38001-c04","name":"洞霄宫","type":"寺观","location_text":"在大涤山","history_lore":"宫有五洞交扃九峰回挹千岩万谷秀聚其中","original":"洞霄宫【在大涤山宫有五洞交扃九峯回挹千岩万谷秀聚其中】"},
    {"site_id":"SITE-006","item_id":"38-001","geo_id":"GEO-38001-c01","name":"伍子胥庙","type":"祠庙","location_text":"在吴山","history_lore":"子胥谏吴王不听伏剑死，吴人怜之立祠江上命曰胥山，唐封吴安王，本朝岁时致祭","original":"伍子胥庙【在吴山吴越春秋子胥谏吴王不听伏剑而死吴人怜之立祠江上命曰胥山本朝命有司岁时致祭】"},
    {"site_id":"SITE-007","item_id":"38-001","geo_id":"GEO-38001-c01","name":"岳武穆王庙","type":"祠庙","location_text":"在岳飞墓侧","history_lore":"武穆飞谥，本朝命有司岁时致祭","original":"岳武穆王庙【在岳飞墓侧武穆飞諡本朝命有司岁时致祭】"},
    {"site_id":"SITE-008","item_id":"38-001","geo_id":"GEO-38001-c01","name":"旌功祠","type":"祠庙","location_text":"在三台山","history_lore":"祀本朝于肃愍公，弘治间赐谥建祠岁春秋祭","original":"旌功祠【在三台山祀本朝于肃愍公治间赐諡建祠岁春秋祭】"},
    {"site_id":"SITE-009","item_id":"38-001","geo_id":"GEO-38001-c05","name":"武肃王墓","type":"陵墓","location_text":"在临安县城北茅山原","history_lore":"吴越王钱镠墓","original":"武肃王墓【在临安县城北茅山原】"},
    {"site_id":"SITE-010","item_id":"38-001","geo_id":"GEO-38001-c01","name":"林逋墓","type":"陵墓","location_text":"在孤山","history_lore":"逋自为墓于其庐侧","original":"林逋墓【在孤山逋自为墓于其庐侧】"},
    {"site_id":"SITE-011","item_id":"38-001","geo_id":"GEO-38001-c01","name":"岳飞墓","type":"陵墓","location_text":"在栖霞岭下","history_lore":"飞为秦桧所诬死葬于此，元赵孟頫有诗","original":"岳飞墓【在栖霞岭下飞为秦桧所中死葬于此元赵孟頫诗岳王坟上草离离】"},
    {"site_id":"SITE-012","item_id":"38-001","geo_id":"GEO-38001-c01","name":"宋大内","type":"古迹","location_text":"在凤凰山之东","history_lore":"本梁安国寺地，故吴越王宫，高宗南渡以州治为行宫增筑皇城","original":"宋大内【在鳯凰山之东本梁安国寺地故吴越王宫也宋为杭州治髙宗南渡以州治为行宫増筑皇城】"},
    {"site_id":"SITE-013","item_id":"38-001","geo_id":"GEO-38001-c01","name":"雷峰塔","type":"古迹","location_text":"在西湖南山之南","history_lore":"吴越王钱氏所建尚存","original":"雷峯塔【在西湖南山之南皮园吴越王钱氏所建尚存】"},
    {"site_id":"SITE-014","item_id":"38-001","geo_id":"GEO-38001-c01","name":"六和塔","type":"古迹","location_text":"在府城南十三里开化寺前","history_lore":"宋开宝中建塔有九层后废，绍兴间复建七层","original":"六和塔【在府城南十三里开化寺前宋开宝中建塔有九层后废绍兴间复建七层而止】"},
    {"site_id":"SITE-015","item_id":"38-001","geo_id":"GEO-38001-c01","name":"林逋庐","type":"古迹","location_text":"在西湖之孤山","history_lore":"逋结庐于此二十年足不及城市，有梅花诗疏影横斜水清浅暗香浮动月黄昏","original":"林逋庐【在西湖之孤山逋结庐于此二十年足不及城市有梅花诗云疎影横斜水清浅暗香浮动月黄昏】"},
    {"site_id":"SITE-016","item_id":"38-001","geo_id":"GEO-38001-c03","name":"许远庙","type":"祠庙","location_text":"在海宁县治西","history_lore":"五代梁初建，本朝洪武初以海宁故盐官乃远所生地独以祀远","original":"许逺庙【在海宁县治西五代梁初建本朝洪武初以海宁故盐官乃远所生地宜庙祀故独以祀远云】"}
]
with open(os.path.join(BASE,"38-001_sites1_寺观祠庙陵墓.json"),"w",encoding="utf-8") as f:
    json.dump({"item_id":"38-001","volume":"38","source":"杭州府","region":"浙江","layers":{"ents":[],"geos":[],"evos":[],"mtns":[],"pers":[],"sites":sites1,"prods":[],"cits":[]},"layer_count":7,"title":"杭州府"},f,ensure_ascii=False,indent=2)
print(f"sites1寺观祠庙陵墓: {len(sites1)}")

# ---- SITES2 宫室关梁公署学校 ----
sites2 = [
    {"site_id":"SITE-101","item_id":"38-001","geo_id":"GEO-38001-c01","name":"望海楼","type":"宫室","location_text":"在凤凰山下","history_lore":"唐武德中建一名东楼，白居易苏轼皆有诗","original":"望海楼【在鳯凰山下唐武德中建一名东楼白居易苏轼皆有诗】"},
    {"site_id":"SITE-102","item_id":"38-001","geo_id":"GEO-38001-c01","name":"有美堂","type":"宫室","location_text":"在凤凰山下","history_lore":"宋梅挚守杭时建，以仁宗赐诗有地有湖山美之句因名，欧阳修记","original":"有美堂【在鳯凰山下宋梅摰守杭时建以仁宗赐诗有地有湖山美之句因取有美名堂欧阳脩记】"},
    {"site_id":"SITE-103","item_id":"38-001","geo_id":"GEO-38001-c01","name":"苏公堤","type":"关梁","location_text":"在西湖上","history_lore":"宋元祐中苏轼取葑田积湖中为长堤，植芙蓉杨柳其上","original":"苏公堤【在西湖上宋元祐中苏轼取葑田积湖中南北径三十里为长隄植芙蓉杨栁其上】"},
    {"site_id":"SITE-104","item_id":"38-001","geo_id":"GEO-38001-c01","name":"西湖六桥","type":"关梁","location_text":"在西湖苏堤","history_lore":"曰映波锁澜望山压堤东浦跨虹凡六桥","original":"西湖六桥【在西湖苏隄曰暎波锁澜望山压隄东浦跨虬几六】"},
    {"site_id":"SITE-105","item_id":"38-001","geo_id":"GEO-38001-c01","name":"杭州府学","type":"学校","location_text":"在府治北","history_lore":"宋绍兴初徙置今所，元至元中增广之，本朝宣德四年重建","original":"杭州府学【在府治北旧在鳯凰山右宋绍兴初徙置今所元至元中郡守夏思忠复购地増广之本朝宣德四年重建】"},
    {"site_id":"SITE-106","item_id":"38-001","geo_id":"GEO-38001-c04","name":"龟山书院","type":"书院","location_text":"在余杭县治南","history_lore":"宋崇宁末杨时知县事去官有遗爱，民请立书院以祀之","original":"山书院【在余杭县治南宋崇寜末杨时知县事去官有遗爱于民民请立书院以祀之】"},
    {"site_id":"SITE-107","item_id":"38-001","geo_id":"GEO-38001-c01","name":"西湖书院","type":"书院","location_text":"在府治北","history_lore":"本宋太学故基，元至元末肃政廉访使徐琰改为书院","original":"西湖书院【在府治北本宋太学故基元至元末肃政亷访使徐琰改为书院】"},
    {"site_id":"SITE-108","item_id":"38-001","geo_id":"GEO-38001-c01","name":"两浙都转运盐使司","type":"公署","location_text":"在府治北","history_lore":"本朝洪武九年即元旧治重建","original":"两浙都转运盐使司【在府治北本朝洪武九年即元旧治重建】"},
    {"site_id":"SITE-109","item_id":"38-001","geo_id":"GEO-38001-c01","name":"表忠观","type":"寺观","location_text":"在龙山","history_lore":"宋郡守赵抃请于朝为钱氏坟庙赐额表忠，苏轼为碑铭，嘉靖三十九年以灵芝寺改建","original":"表忠观【在龙山宋郡守赵抃以钱氏坟庙芜废请于朝赐额表忠苏轼为碑铭嘉靖三十九年以灵芝寺改建】"}
]
with open(os.path.join(BASE,"38-001_sites2_宫室关梁公署学校.json"),"w",encoding="utf-8") as f:
    json.dump({"item_id":"38-001","volume":"38","source":"杭州府","region":"浙江","layers":{"ents":[],"geos":[],"evos":[],"mtns":[],"pers":[],"sites":sites2,"prods":[],"cits":[]},"layer_count":7,"title":"杭州府"},f,ensure_ascii=False,indent=2)
print(f"sites2宫室关梁公署: {len(sites2)}")

# ---- 县shell ----
counties = [("c01","钱塘县"),("c02","仁和县"),("c03","海宁县"),("c04","余杭县"),
            ("c05","临安县"),("c06","富阳县"),("c07","於潜县"),("c08","新城县"),("c09","昌化县")]
for cid, cname in counties:
    shell = {"item_id":"38-001","volume":"38","source":cname,"region":"浙江",
             "layers":{"ents":[{"ent_id":f"ENT-{cid}","name":cname,"type":"geo","norm":cname,"first_source":"38-001"}],
                       "geos":[],"evos":[],"mtns":[],"pers":[],"sites":[],"prods":[],"cits":[]},
             "layer_count":7,"title":"杭州府"}
    with open(os.path.join(BASE,f"38-001_{cid}_{cname}.json"),"w",encoding="utf-8") as f:
        json.dump(shell,f,ensure_ascii=False,indent=2)
print(f"县shell: {len(counties)}个")

# ---- 卫所shell ----
weisuo = {"item_id":"38-001","volume":"38","source":"海宁守御千户所","region":"浙江",
          "layers":{"ents":[{"ent_id":"ENT-w01","name":"海宁守御千户所","type":"geo","norm":"海宁守御千户所","first_source":"38-001"}],
                    "geos":[],"evos":[],"mtns":[],"pers":[],"sites":[],"prods":[],"cits":[]},
          "layer_count":7,"title":"杭州府"}
with open(os.path.join(BASE,"38-001_w01_海宁守御千户所.json"),"w",encoding="utf-8") as f:
    json.dump(weisuo,f,ensure_ascii=False,indent=2)
print("卫所shell: 1个")

print("\n=== 全部完成 ===")
