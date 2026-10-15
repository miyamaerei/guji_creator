# -*- coding: utf-8 -*-
import json, os

OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol37"

# ===== children geos (14 sub-weisuo) =====
children_geos = [
 {"geo_id":"GEO-37007-w01","item_id":"37-007","name":"甘州左卫","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"附郭；本匈奴昆邪王地，汉置张掖郡，取张国臂掖之义；后又置属国都尉以主蛮夷降者；魏晋并因之；后魏改张掖军寻改军为郡又置西凉州；西魏更名甘州，取州东甘浚山泉味甘冽为名；后周复为张掖郡；唐初为甘州，天宝初复为郡，乾元初复为甘州；宋初为西夏所据，改镇夷郡又改宣德府；元改甘肃路寻改甘州路；本朝为甘肃卫寻分置甘州左卫","garrison_type":"卫"}},
 {"geo_id":"GEO-37007-w02","item_id":"37-007","name":"甘州右卫","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"附郭，洪武二十八年建","garrison_type":"卫"}},
 {"geo_id":"GEO-37007-w03","item_id":"37-007","name":"甘州中卫","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"附郭，洪武二十八年建","garrison_type":"卫"}},
 {"geo_id":"GEO-37007-w04","item_id":"37-007","name":"甘州前卫","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"附郭，洪武二十八年建","garrison_type":"卫"}},
 {"geo_id":"GEO-37007-w05","item_id":"37-007","name":"甘州后卫","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"附郭，洪武二十八年建","garrison_type":"卫"}},
 {"geo_id":"GEO-37007-w06","item_id":"37-007","name":"肃州卫","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"在都司城西五百一十里；本月支地，汉置酒泉郡，东汉晋皆因之；后魏亦为酒泉郡；隋初废郡置肃州，大业初省入张掖郡；唐复置肃州或为酒泉郡治酒泉县；元置肃州路；本朝改置肃州卫","garrison_type":"卫"}},
 {"geo_id":"GEO-37007-w07","item_id":"37-007","name":"山丹卫","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"在都司城东北一百二十里；本汉删丹县属张掖郡，东汉末属西郡，晋因之；唐属甘州；宋时为西夏所据置甘肃军；元置山丹州隶亦集乃路；本朝州废置山丹卫","garrison_type":"卫"}},
 {"geo_id":"GEO-37007-w08","item_id":"37-007","name":"永昌卫","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"在都司城东南三百一十里；本汉武威郡地，唐为凉州地；宋初为西凉府地，景德中陷入西夏；元至元中以永昌王宫殿所在立永昌路；本朝改置永昌卫","garrison_type":"卫"}},
 {"geo_id":"GEO-37007-w09","item_id":"37-007","name":"凉州卫","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"在都司城东南五百里；本匈奴休屠王地，汉置武威郡治姑臧县，又于此置凉州；后魏立武威郡；隋为凉州；唐初为李轨所据寻克平之复置凉州，天宝初改武威郡；宋改为西凉府；元改西凉州；本朝改置凉州卫","garrison_type":"卫"}},
 {"geo_id":"GEO-37007-w10","item_id":"37-007","name":"镇番卫","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"在都司城东五百五十里；本汉武威郡界，元号小河滩城；本朝洪武中置镇番卫","garrison_type":"卫"}},
 {"geo_id":"GEO-37007-w11","item_id":"37-007","name":"庄浪卫","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"在都司城南九百四十里；本汉武威郡地，唐为凉州地；元置庄浪县属永昌路；本朝洪武中改置庄浪卫","garrison_type":"卫"}},
 {"geo_id":"GEO-37007-w12","item_id":"37-007","name":"西宁卫","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"在都司城东南一千三百五十里；古西羌所居谓之湟中，汉置破羌县属金城郡；东汉置西平郡；晋永嘉末为秃发乌孤所据；后魏置鄯州，后周改置乐都郡；隋初郡废置鄯州，大业初废州置西平郡；唐因之治湟水县，上元间没于吐蕃号青唐城；宋收复置鄯州寻改西宁州；元属亦集乃路；本朝改置西宁卫","garrison_type":"卫"}},
 {"geo_id":"GEO-37007-w13","item_id":"37-007","name":"镇夷守御千户所","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"在都司城西北三百里；本汉张掖郡地；本朝洪武间置镇夷守御千户所寻省，永乐初复置","garrison_type":"守御千户所"}},
 {"geo_id":"GEO-37007-w14","item_id":"37-007","name":"古浪守御千户所","type":"weisuo","region":"陕西行都司","parent":"GEO-37007","children":[],"volume_range":"卷37",
  "attributes":{"location_text":"在都司城东南六百四十里；本汉武威郡地，唐筑和戎城；元为古浪城立巡检司属永昌路；本朝正统间置古浪守御千户所","garrison_type":"守御千户所"}}
]

main_geo = {
 "geo_id":"GEO-37007","item_id":"37-007","name":"陕西行都指挥使司","type":"weisuo","region":"陕西行都司",
 "parent":"GEO-000","children":[c["geo_id"] for c in children_geos],"volume_range":"卷37",
 "attributes":{
  "borders":[
   {"direction":"东","to_place":"临洮府兰县黄河","distance_li":1175},
   {"direction":"西","to_place":"肃州卫嘉峪山","distance_li":570},
   {"direction":"南","to_place":"西宁卫黄河","distance_li":1575},
   {"direction":"北","to_place":"亦集乃地","distance_li":1500}
  ],
  "to_capital":[
   {"capital":"京师","distance_li":5400},
   {"capital":"南京","distance_li":5310}
  ],
  "garrison_type":"行都司",
  "jun_name":"张掖【汉名】武威【汉名】酒泉【汉名】西平【汉名】",
  "topography":"河山襟带为羌戎通驿之路【元肃州志】；环以祁连合黎之山浸以居延鲜卑之水【元甘州志】；凉州险绝地土饶沃【元志】；万山环抱三峡重围红岸峙其左青海潴于右【西宁卫志】",
  "customs":"民俗质朴【汉窦融传】；号有华风【北史胡叟传凉州虽地居戎域然自张氏以来号有华风】；风土壮猛便习兵事【晋载记】；人性坚刚慷慨【寰宇记】；土人穴居野处采猎为生【图经】；以织毛褐为业【元肃州志居民杂处以织毛褐为业】；崇尚释教【元山丹州志】"
 },
 "cit_ids":["CIT-001","CIT-002","CIT-003","CIT-004","CIT-005","CIT-006","CIT-007","CIT-008","CIT-009","CIT-010","CIT-011","CIT-012","CIT-013"]
}

evos = [
 {"evo_id":"EVO-001","item_id":"37-007","geo_id":"GEO-37007","dynasty":"虞夏","era":None,"institution_name":"雍州之域","action":"属","detail":"禹贡雍州之域，天文井鬼分野"},
 {"evo_id":"EVO-002","item_id":"37-007","geo_id":"GEO-37007","dynasty":"先秦","era":None,"institution_name":"月支国/匈奴","action":"居","detail":"汉以前为月支国地，后为匈奴所据"},
 {"evo_id":"EVO-003","item_id":"37-007","geo_id":"GEO-37007","dynasty":"汉","era":"武帝","institution_name":"酒泉武威张掖等郡","action":"置郡","detail":"武帝时始置酒泉武威张掖等郡以断匈奴右臂，时号河西五郡"},
 {"evo_id":"EVO-004","item_id":"37-007","geo_id":"GEO-37007","dynasty":"晋","era":None,"institution_name":"前凉/后凉/西凉/北凉","action":"割据","detail":"晋时张轨据河西为前凉，吕光继之为后凉；及李暠迁酒泉号西凉，沮渠防逊据张掖号北凉"},
 {"evo_id":"EVO-005","item_id":"37-007","geo_id":"GEO-37007","dynasty":"南北朝","era":"后魏","institution_name":"西凉州","action":"分置","detail":"后魏分置西凉州"},
 {"evo_id":"EVO-006","item_id":"37-007","geo_id":"GEO-37007","dynasty":"南北朝","era":"西魏","institution_name":"甘州","action":"更名","detail":"西魏更名甘州"},
 {"evo_id":"EVO-007","item_id":"37-007","geo_id":"GEO-37007","dynasty":"唐","era":None,"institution_name":"陇右道/吐蕃","action":"属陷","detail":"唐时地属陇右道，天宝中没于吐蕃，大中间收复故地"},
 {"evo_id":"EVO-008","item_id":"37-007","geo_id":"GEO-37007","dynasty":"宋金","era":None,"institution_name":"西夏","action":"据","detail":"宋金俱为西夏所据"},
 {"evo_id":"EVO-009","item_id":"37-007","geo_id":"GEO-37007","dynasty":"元","era":None,"institution_name":"甘肃路总管府/甘肃等处行中书省","action":"置","detail":"元立甘肃路总管府，寻添立宣慰司，后改甘肃等处行中书省理于此以控河西诸郡"},
 {"evo_id":"EVO-010","item_id":"37-007","geo_id":"GEO-37007","dynasty":"明","era":"洪武","institution_name":"陕西行都指挥使司","action":"置司","detail":"本朝洪武二十四年置甘肃卫，二十六年始于此置陕西行都指挥使司，领卫十二守御千户所二"}
]

mtns = [
 {"mtn_id":"MTN-001","item_id":"37-007","geo_id":"GEO-37007","name":"人祖山","type":"山","location_text":"在都司城东北四十里","description":"其山不毛","lore":""},
 {"mtn_id":"MTN-002","item_id":"37-007","geo_id":"GEO-37007","name":"合黎山","type":"山","location_text":"在都司城西北四十里","description":"禹贡导弱水至于合黎即此","lore":""},
 {"mtn_id":"MTN-003","item_id":"37-007","geo_id":"GEO-37007","name":"甘浚山","type":"山","location_text":"在都司城西南八十里","description":"有泉甘冽因名，又名绀峻","lore":""},
 {"mtn_id":"MTN-004","item_id":"37-007","geo_id":"GEO-37007","name":"马蹄山","type":"山","location_text":"在都司城南一百里","description":"山岩石间有神骥足在焉，又有临松青松丹霞三名","lore":""},
 {"mtn_id":"MTN-005","item_id":"37-007","geo_id":"GEO-37007","name":"祁连山","type":"山","location_text":"在都司城西南一百里","description":"山甚峻广，本名天山，匈奴呼天为祁连因名；山上草木茂美冬温夏凉宜收放","lore":"后失此歌曰夺我祁连山使我六畜不蕃息"},
 {"mtn_id":"MTN-006","item_id":"37-007","geo_id":"GEO-37007","name":"红寺山","type":"山","location_text":"在山丹卫城北二十五里","description":"其上土色多红","lore":""},
 {"mtn_id":"MTN-007","item_id":"37-007","geo_id":"GEO-37007","name":"甘凌山","type":"山","location_text":"在山丹卫城西北三十里","description":"连亘甘州，中有三石洞，其下有泉，岁旱于此取水祷雨有应","lore":""},
 {"mtn_id":"MTN-008","item_id":"37-007","geo_id":"GEO-37007","name":"焉支山","type":"山","location_text":"在山丹卫城东南一百二十里","description":"一名删丹山；唐哥舒翰建神祠于山麓，天宝间封山神为宁济公","lore":"后汉匈奴失此山歌曰失我焉支山使我妇女无颜色"},
 {"mtn_id":"MTN-009","item_id":"37-007","geo_id":"GEO-37007","name":"西山","type":"山","location_text":"在凉州卫城西二十里","description":"中有莲花峰，峰下有石五色成纹如兽形","lore":""},
 {"mtn_id":"MTN-010","item_id":"37-007","geo_id":"GEO-37007","name":"天梯山","type":"山","location_text":"在凉州卫城南八十里","description":"山路崎岖如梯","lore":""},
 {"mtn_id":"MTN-011","item_id":"37-007","geo_id":"GEO-37007","name":"第五山","type":"山","location_text":"在旧姑藏县界","description":"有清泉茂林悬岩石室，自昔为隐士所居","lore":""},
 {"mtn_id":"MTN-012","item_id":"37-007","geo_id":"GEO-37007","name":"臧南山","type":"山","location_text":"在凉州卫城西南一百二十里","description":"上多积雪","lore":""},
 {"mtn_id":"MTN-013","item_id":"37-007","geo_id":"GEO-37007","name":"青岩山","type":"山","location_text":"在旧姑藏县界","description":"下有湫甚广，人触之风雹立至","lore":""},
 {"mtn_id":"MTN-014","item_id":"37-007","geo_id":"GEO-37007","name":"金山","type":"山","location_text":"在永昌卫城北二里","description":"又在故昌松县南，丽水出焉","lore":""},
 {"mtn_id":"MTN-015","item_id":"37-007","geo_id":"GEO-37007","name":"白岭山","type":"山","location_text":"在凉州卫西南","description":"山顶冬夏积雪望之皓然故名","lore":""},
 {"mtn_id":"MTN-016","item_id":"37-007","geo_id":"GEO-37007","name":"崆峒山","type":"山","location_text":"在肃州卫城东南六十里","description":"旧属福禄县；史记黄帝伐山通道西至于崆峒谓此","lore":""},
 {"mtn_id":"MTN-017","item_id":"37-007","geo_id":"GEO-37007","name":"嘉峪山","type":"山","location_text":"在肃州卫城西","description":"一名玉石山","lore":""},
 {"mtn_id":"MTN-018","item_id":"37-007","geo_id":"GEO-37007","name":"黑山","type":"山","location_text":"在肃州卫城北沙漠中","description":"望之惟见黑山","lore":""},
 {"mtn_id":"MTN-019","item_id":"37-007","geo_id":"GEO-37007","name":"昆仑山","type":"山","location_text":"在肃州卫城西南二百五十里","description":"南与甘州山连，其颠峻极经夏积雪不消，世呼雪山；后凉张骏时酒泉太守马岌言周穆王见王母于此宜立王母祠，骏从之","lore":""},
 {"mtn_id":"MTN-020","item_id":"37-007","geo_id":"GEO-37007","name":"苏武山","type":"山","location_text":"在镇番卫城东南三十里","description":"相传汉苏武牧羝处，旧有苏武庙","lore":""},
 {"mtn_id":"MTN-021","item_id":"37-007","geo_id":"GEO-37007","name":"来伏山","type":"山","location_text":"在镇番卫城西北八十里","description":"","lore":""},
 {"mtn_id":"MTN-022","item_id":"37-007","geo_id":"GEO-37007","name":"石佛山","type":"山","location_text":"在庄浪卫城东北三十里","description":"崖上有石佛像","lore":""},
 {"mtn_id":"MTN-023","item_id":"37-007","geo_id":"GEO-37007","name":"大松山","type":"山","location_text":"在庄浪卫城东一百二十里","description":"山多大松；又城东北一百里有小松山","lore":""},
 {"mtn_id":"MTN-024","item_id":"37-007","geo_id":"GEO-37007","name":"峡口山","type":"山","location_text":"在西宁卫城东","description":"地极险阻为湟鄯往来咽喉地，汉时名湟陿，唐人尝修阁道，宋筑省章城控制要害，又名绥远阁","lore":""},
 {"mtn_id":"MTN-025","item_id":"37-007","geo_id":"GEO-37007","name":"积石山","type":"山","location_text":"在西宁卫境废龙支县之南","description":"即禹贡导河之所","lore":""},
 {"mtn_id":"MTN-026","item_id":"37-007","geo_id":"GEO-37007","name":"热水山","type":"山","location_text":"在西宁卫城南五百里","description":"山南出暖水流入青海，北有泉即西宁河源","lore":""},
 {"mtn_id":"MTN-027","item_id":"37-007","geo_id":"GEO-37007","name":"鸣沙山","type":"山","location_text":"在沙州城南七里","description":"一名沙角山，峰崿危峻沙如干糖，天气清明时沙鸣闻于城内，其沙或随人足而堕经宿复还山上","lore":""},
 {"mtn_id":"MTN-028","item_id":"37-007","geo_id":"GEO-37007","name":"三危山","type":"山","location_text":"在沙州城东南二十里","description":"其山三峰峭绝因名；舜窜三苗于三危，禹贡导黑水至于三危皆谓此","lore":""},
 {"mtn_id":"MTN-029","item_id":"37-007","geo_id":"GEO-37007","name":"羊膊山","type":"山","location_text":"在沙州城南","description":"多岩石无草木，山北有一岩曰羊膊","lore":""},
 {"mtn_id":"MTN-030","item_id":"37-007","geo_id":"GEO-37007","name":"龙勒山","type":"山","location_text":"在沙州城东一百二十里","description":"汉龙勒县因山以名","lore":""},
 {"mtn_id":"MTN-031","item_id":"37-007","geo_id":"GEO-37007","name":"三陇山","type":"山","location_text":"在玉关外","description":"流沙碛在玉关外，有三断石极大，世谓之三陇山","lore":""},
 {"mtn_id":"MTN-032","item_id":"37-007","geo_id":"GEO-37007","name":"北塞山","type":"山","location_text":"在沙州境","description":"汉武帝时天马朝发京师夕至炖煌北塞山下即此","lore":""},
 {"mtn_id":"MTN-033","item_id":"37-007","geo_id":"GEO-37007","name":"白龙堆","type":"碛","location_text":"在炖煌正西关外","description":"郡国记炖煌正西关外有白龙堆沙","lore":""},
 {"mtn_id":"MTN-034","item_id":"37-007","geo_id":"GEO-37007","name":"分水岭","type":"岭","location_text":"在庄浪卫城西一百五十里","description":"岭峤有泉分流，南为庄浪河北为古浪河","lore":""},
 {"mtn_id":"MTN-035","item_id":"37-007","geo_id":"GEO-37007","name":"居延海","type":"海","location_text":"在都司城西北","description":"地理志渡张掖河西北至合黎口峡口傍河东壖曲屈行千五百里是也","lore":""},
 {"mtn_id":"MTN-036","item_id":"37-007","geo_id":"GEO-37007","name":"西海","type":"海","location_text":"在西宁卫城西三百余里","description":"海方数百里有鱼无鳞背负黑点；汉平帝时王莽秉政风卑禾羌献西海之地置西海郡，莽败郡废；一名卑禾羌海，俗呼青海","lore":""},
 {"mtn_id":"MTN-037","item_id":"37-007","geo_id":"GEO-37007","name":"白亭海","type":"海","location_text":"在凉州卫东北境","description":"卫西南五涧谷水流入此海，以水色洁白故名，一名小阔端海子","lore":""},
 {"mtn_id":"MTN-038","item_id":"37-007","geo_id":"GEO-37007","name":"张掖河","type":"河","location_text":"在都司城西一十里","description":"源出摆通川经祁连山西出合黎北名合黎水，又名鲜水，流入亦集乃界","lore":""},
 {"mtn_id":"MTN-039","item_id":"37-007","geo_id":"GEO-37007","name":"清水河","type":"河","location_text":"在肃州卫城北四十里","description":"下流会讨来河","lore":""},
 {"mtn_id":"MTN-040","item_id":"37-007","geo_id":"GEO-37007","name":"沙河","type":"河","location_text":"在肃州卫城东四十里","description":"源出雪山下流入讨来河","lore":""},
 {"mtn_id":"MTN-041","item_id":"37-007","geo_id":"GEO-37007","name":"讨来河","type":"河","location_text":"在肃州卫城北一百里","description":"源出雪山，下流三百里入黑河","lore":""},
 {"mtn_id":"MTN-042","item_id":"37-007","geo_id":"GEO-37007","name":"大通河","type":"河","location_text":"在庄浪卫城南一百二十里","description":"","lore":""},
 {"mtn_id":"MTN-043","item_id":"37-007","geo_id":"GEO-37007","name":"苏木连河","type":"河","location_text":"在西宁卫城北山之阴","description":"按汉书湟水出金城郡临羌县西北东至允吾入河，又舆地纲目湟水经卑禾羌海疑即此水也","lore":""},
 {"mtn_id":"MTN-044","item_id":"37-007","geo_id":"GEO-37007","name":"西宁河","type":"河","location_text":"在西宁卫城北","description":"源出热水山，北流五里经伯颜川又合那海川，流五百里入黄河","lore":""},
 {"mtn_id":"MTN-045","item_id":"37-007","geo_id":"GEO-37007","name":"黑河","type":"河","location_text":"在镇夷千户所城西四里","description":"即古张掖河，流经石峡口入居延海","lore":""},
 {"mtn_id":"MTN-046","item_id":"37-007","geo_id":"GEO-37007","name":"潴野泽","type":"泽","location_text":"在凉州卫城东北","description":"禹贡至于潴野即此，一名休屠泽","lore":""},
 {"mtn_id":"MTN-047","item_id":"37-007","geo_id":"GEO-37007","name":"南草湖","type":"湖","location_text":"在山丹卫城南","description":"周围九里","lore":""},
 {"mtn_id":"MTN-048","item_id":"37-007","geo_id":"GEO-37007","name":"西草湖","type":"湖","location_text":"在山丹卫城西一十里","description":"周围七里，与南草湖水皆可灌田","lore":""},
 {"mtn_id":"MTN-049","item_id":"37-007","geo_id":"GEO-37007","name":"弱水","type":"河","location_text":"在甘州卫城西","description":"环合黎山东北入东莎界；禹贡导弱水至于合黎余波入于流沙；按西域传弱水在条支自长安西行万二千里又百余日方至其地疑别有所谓弱水也","lore":""},
 {"mtn_id":"MTN-050","item_id":"37-007","geo_id":"GEO-37007","name":"黑水","type":"河","location_text":"源出肃州卫城西北一十五里","description":"地志云黑水出张掖县鸡山","lore":""},
 {"mtn_id":"MTN-051","item_id":"37-007","geo_id":"GEO-37007","name":"白水","type":"河","location_text":"源出肃州卫城西南二十里","description":"下流与红水黑水合","lore":""},
 {"mtn_id":"MTN-052","item_id":"37-007","geo_id":"GEO-37007","name":"红水","type":"河","location_text":"在肃州卫城东南三十里","description":"源出卫南山谷中，下流与黑水白水合","lore":""},
 {"mtn_id":"MTN-053","item_id":"37-007","geo_id":"GEO-37007","name":"浩亹水","type":"河","location_text":"在西宁卫西北","description":"一名阁门水，源出塞外东至允吾界入湟水","lore":""},
 {"mtn_id":"MTN-054","item_id":"37-007","geo_id":"GEO-37007","name":"宗水","type":"河","location_text":"在西宁卫境","description":"来自青海迳卫境入于湟水，水之南有宗谷口","lore":""},
 {"mtn_id":"MTN-055","item_id":"37-007","geo_id":"GEO-37007","name":"渥洼水","type":"水","location_text":"在沙州境","description":"汉元鼎四年秋天马生渥洼水中","lore":""},
 {"mtn_id":"MTN-056","item_id":"37-007","geo_id":"GEO-37007","name":"灵泉池","type":"池","location_text":"在凉州卫治南","description":"后凉吕光尝宴群臣于此","lore":""},
 {"mtn_id":"MTN-057","item_id":"37-007","geo_id":"GEO-37007","name":"红盐池","type":"池","location_text":"在山丹卫城北五百里","description":"池产红盐；又居延泽旁亦有池产白盐，采之不竭","lore":""},
 {"mtn_id":"MTN-058","item_id":"37-007","geo_id":"GEO-37007","name":"石井","type":"井","location_text":"在祁连山下","description":"石洞四时不竭","lore":""},
 {"mtn_id":"MTN-059","item_id":"37-007","geo_id":"GEO-37007","name":"红泉","type":"泉","location_text":"在凉州卫城东五十里","description":"水色微红","lore":""},
 {"mtn_id":"MTN-060","item_id":"37-007","geo_id":"GEO-37007","name":"暖泉","type":"泉","location_text":"在永昌卫城西南三十五里","description":"二穴涌出四时常温，东北流入水磨川","lore":""},
 {"mtn_id":"MTN-061","item_id":"37-007","geo_id":"GEO-37007","name":"湫泉","type":"泉","location_text":"在西宁卫治西一十里","description":"其深莫测涌喷有声，岁旱祷雨辄应","lore":""},
 {"mtn_id":"MTN-062","item_id":"37-007","geo_id":"GEO-37007","name":"玄泉","type":"泉","location_text":"在龙勒山","description":"汉李广利伐大宛还士众渴甚，广利引刀刺山泉涌出","lore":""}
]

prods = [
 {"prod_id":"PROD-001","item_id":"37-007","geo_id":"GEO-37007","name":"毛褐","note":"各卫俱出"},
 {"prod_id":"PROD-002","item_id":"37-007","geo_id":"GEO-37007","name":"楸子","note":"其色赤味甘而酸，居人取其汁熬为果单"},
 {"prod_id":"PROD-003","item_id":"37-007","geo_id":"GEO-37007","name":"圆根","note":"似萝卜而圆青色味甘苦"},
 {"prod_id":"PROD-004","item_id":"37-007","geo_id":"GEO-37007","name":"白柰","note":"一名白擒"},
 {"prod_id":"PROD-005","item_id":"37-007","geo_id":"GEO-37007","name":"茄莲","note":"叶似蓝根似萝卜味甘脆"},
 {"prod_id":"PROD-006","item_id":"37-007","geo_id":"GEO-37007","name":"沙葱","note":"似葱"},
 {"prod_id":"PROD-007","item_id":"37-007","geo_id":"GEO-37007","name":"沙枣","note":"甘州出"},
 {"prod_id":"PROD-008","item_id":"37-007","geo_id":"GEO-37007","name":"甜瓜","note":"甘州出"},
 {"prod_id":"PROD-009","item_id":"37-007","geo_id":"GEO-37007","name":"胡麻","note":"甘州肃州古浪俱出"},
 {"prod_id":"PROD-010","item_id":"37-007","geo_id":"GEO-37007","name":"石油","note":"肃州南山出，然之极明不可食"},
 {"prod_id":"PROD-011","item_id":"37-007","geo_id":"GEO-37007","name":"肉苁蓉","note":"肃州出"},
 {"prod_id":"PROD-012","item_id":"37-007","geo_id":"GEO-37007","name":"锁阳","note":"肃州出"},
 {"prod_id":"PROD-013","item_id":"37-007","geo_id":"GEO-37007","name":"甘草","note":"肃州出"},
 {"prod_id":"PROD-014","item_id":"37-007","geo_id":"GEO-37007","name":"雌黄","note":"肃州出"},
 {"prod_id":"PROD-015","item_id":"37-007","geo_id":"GEO-37007","name":"硫黄","note":"肃州出"},
 {"prod_id":"PROD-016","item_id":"37-007","geo_id":"GEO-37007","name":"枸杞子","note":"镇番卫出"},
 {"prod_id":"PROD-017","item_id":"37-007","geo_id":"GEO-37007","name":"青盐","note":"镇番卫出"},
 {"prod_id":"PROD-018","item_id":"37-007","geo_id":"GEO-37007","name":"白盐","note":"镇番卫出"},
 {"prod_id":"PROD-019","item_id":"37-007","geo_id":"GEO-37007","name":"马鸡","note":"嘴脚红羽毛青绿"},
 {"prod_id":"PROD-020","item_id":"37-007","geo_id":"GEO-37007","name":"山鸡","note":"项黑花身斑色"},
 {"prod_id":"PROD-021","item_id":"37-007","geo_id":"GEO-37007","name":"野马","note":"皮可为裘"},
 {"prod_id":"PROD-022","item_id":"37-007","geo_id":"GEO-37007","name":"野牛","note":"大者重千觔"},
 {"prod_id":"PROD-023","item_id":"37-007","geo_id":"GEO-37007","name":"犛牛","note":"尾可作缨，出西番"},
 {"prod_id":"PROD-024","item_id":"37-007","geo_id":"GEO-37007","name":"犏牛","note":"力能载重"},
 {"prod_id":"PROD-025","item_id":"37-007","geo_id":"GEO-37007","name":"洮羊","note":"尾如鹿，西宁卫出"},
 {"prod_id":"PROD-026","item_id":"37-007","geo_id":"GEO-37007","name":"源羊","note":"大者重百觔角环盘，西宁卫出"},
 {"prod_id":"PROD-027","item_id":"37-007","geo_id":"GEO-37007","name":"土豹","note":"镇番卫出"},
 {"prod_id":"PROD-028","item_id":"37-007","geo_id":"GEO-37007","name":"麝香","note":"沙州出"},
 {"prod_id":"PROD-029","item_id":"37-007","geo_id":"GEO-37007","name":"绛矾黄矾","note":"沙州出"}
]

cits = [
 {"cit_id":"CIT-001","item_id":"37-007","cited_work":"元肃州志","cited_work_ent_id":None,"context":"形胜/风俗","original":"【元肃州志】"},
 {"cit_id":"CIT-002","item_id":"37-007","cited_work":"元甘州志","cited_work_ent_id":None,"context":"形胜","original":"【元甘州志】"},
 {"cit_id":"CIT-003","item_id":"37-007","cited_work":"元志","cited_work_ent_id":None,"context":"形胜","original":"【元志】"},
 {"cit_id":"CIT-004","item_id":"37-007","cited_work":"西宁卫志","cited_work_ent_id":None,"context":"形胜","original":"【西宁卫志】"},
 {"cit_id":"CIT-005","item_id":"37-007","cited_work":"汉窦融传","cited_work_ent_id":None,"context":"风俗","original":"【汉窦融传】"},
 {"cit_id":"CIT-006","item_id":"37-007","cited_work":"北史胡叟传","cited_work_ent_id":None,"context":"风俗","original":"【北史胡叟传】"},
 {"cit_id":"CIT-007","item_id":"37-007","cited_work":"晋载记","cited_work_ent_id":None,"context":"风俗","original":"【晋载记】"},
 {"cit_id":"CIT-008","item_id":"37-007","cited_work":"寰宇记","cited_work_ent_id":None,"context":"风俗","original":"【寰宇记】"},
 {"cit_id":"CIT-009","item_id":"37-007","cited_work":"图经","cited_work_ent_id":None,"context":"风俗","original":"【图经】"},
 {"cit_id":"CIT-010","item_id":"37-007","cited_work":"元山丹州志","cited_work_ent_id":None,"context":"风俗","original":"【元山丹州志】"},
 {"cit_id":"CIT-011","item_id":"37-007","cited_work":"史记","cited_work_ent_id":None,"context":"山川","original":"【史记黄帝伐山通道西至于崆峒】"},
 {"cit_id":"CIT-012","item_id":"37-007","cited_work":"郡国记","cited_work_ent_id":None,"context":"山川","original":"【郡国记】"},
 {"cit_id":"CIT-013","item_id":"37-007","cited_work":"汉书地理志","cited_work_ent_id":None,"context":"建置/山川","original":"【禹贡雍州之域】"}
]

# ents - key entities
ents = [
 {"ent_id":"ENT-001","name":"陕西行都指挥使司","type":"geo","norm":"陕西行都指挥使司","first_source":"37-007"},
 {"ent_id":"ENT-002","name":"甘州左卫","type":"geo","norm":"甘州左卫","first_source":"37-007"},
 {"ent_id":"ENT-003","name":"肃州卫","type":"geo","norm":"肃州卫","first_source":"37-007"},
 {"ent_id":"ENT-004","name":"山丹卫","type":"geo","norm":"山丹卫","first_source":"37-007"},
 {"ent_id":"ENT-005","name":"永昌卫","type":"geo","norm":"永昌卫","first_source":"37-007"},
 {"ent_id":"ENT-006","name":"凉州卫","type":"geo","norm":"凉州卫","first_source":"37-007"},
 {"ent_id":"ENT-007","name":"镇番卫","type":"geo","norm":"镇番卫","first_source":"37-007"},
 {"ent_id":"ENT-008","name":"庄浪卫","type":"geo","norm":"庄浪卫","first_source":"37-007"},
 {"ent_id":"ENT-009","name":"西宁卫","type":"geo","norm":"西宁卫","first_source":"37-007"},
 {"ent_id":"ENT-010","name":"祁连山","type":"mtn","norm":"祁连山","first_source":"37-007"},
 {"ent_id":"ENT-011","name":"合黎山","type":"mtn","norm":"合黎山","first_source":"37-007"},
 {"ent_id":"ENT-012","name":"焉支山","type":"mtn","norm":"焉支山","first_source":"37-007"},
 {"ent_id":"ENT-013","name":"昆仑山","type":"mtn","norm":"昆仑山","first_source":"37-007"},
 {"ent_id":"ENT-014","name":"居延海","type":"mtn","norm":"居延海","first_source":"37-007"},
 {"ent_id":"ENT-015","name":"西海","type":"mtn","norm":"西海","first_source":"37-007"},
 {"ent_id":"ENT-016","name":"张掖河","type":"mtn","norm":"张掖河","first_source":"37-007"},
 {"ent_id":"ENT-017","name":"弱水","type":"mtn","norm":"弱水","first_source":"37-007"},
 {"ent_id":"ENT-018","name":"嘉峪关","type":"geo","norm":"嘉峪关","first_source":"37-007"},
 {"ent_id":"ENT-019","name":"玉门关","type":"geo","norm":"玉门关","first_source":"37-007"},
 {"ent_id":"ENT-020","name":"阳关","type":"geo","norm":"阳关","first_source":"37-007"},
 {"ent_id":"ENT-021","name":"马援","type":"person","norm":"马援","first_source":"37-007"},
 {"ent_id":"ENT-022","name":"金日磾","type":"person","norm":"金日磾","first_source":"37-007"},
 {"ent_id":"ENT-023","name":"张奂","type":"person","norm":"张奂","first_source":"37-007"},
 {"ent_id":"ENT-024","name":"段颎","type":"person","norm":"段颎","first_source":"37-007"},
 {"ent_id":"ENT-025","name":"贾诩","type":"person","norm":"贾诩","first_source":"37-007"},
 {"ent_id":"ENT-026","name":"索靖","type":"person","norm":"索靖","first_source":"37-007"},
 {"ent_id":"ENT-027","name":"赵娥","type":"person","norm":"赵娥","first_source":"37-007"}
]

main = {
 "item_id":"37-007","volume":"37","source":"陕西行都指挥使司","region":"陕西行都司",
 "layers":{
  "ents":ents,
  "geos":[main_geo]+children_geos,
  "evos":evos,
  "mtns":mtns,
  "pers":[],
  "sites":[],
  "prods":prods,
  "cits":cits
 },
 "layer_count":8,
 "validation":{
  "errs":[],
  "gap":0,
  "notes":"陕西行都司主文件；pers 68人超50拆为pers1名宦流寓/pers2人物列女；sites 66处超30拆为sites1古迹祠庙寺观/sites2宫室关梁学校公署；children含14卫所"
 }
}

with open(os.path.join(OUT,"37-007_陕西行都司.json"),"w",encoding="utf-8") as f:
 json.dump(main,f,ensure_ascii=False,indent=1)
print("37-007 main written")

# ===== pers1: 名宦+流寓 =====
pers1 = [
 {"pers_id":"PER-001","item_id":"37-007","geo_id":"GEO-37007","name":"辛武贤","dynasty":"汉","source_section":"名宦","note":"酒泉太守，时赵充国欲俟虏疲剧乃击之，武贤上言以秋分兵击罕开夺其人畜冬复击之，帝嘉纳其言赐玺书拜为破羌将军"},
 {"pers_id":"PER-002","item_id":"37-007","geo_id":"GEO-37007","name":"辛庆忌","dynasty":"汉","source_section":"名宦","note":"张掖太守，徙酒泉，所在著名"},
 {"pers_id":"PER-003","item_id":"37-007","geo_id":"GEO-37007","name":"窦融","dynasty":"汉","source_section":"名宦","note":"更始初为张掖属国都尉，政尚宽和，后为吏民所推行河西五郡大将军事；光武即位遣使入贡，因赐玺书拜凉州牧"},
 {"pers_id":"PER-004","item_id":"37-007","geo_id":"GEO-37007","name":"任延","dynasty":"汉","source_section":"名宦","note":"武威太守，光武戒之曰善事上官无失名誉，延对曰履正奉公臣子之节善事上官臣不敢奉诏；帝叹息曰卿言是也；在郡威行境内，修理沟渠人蒙其利"},
 {"pers_id":"PER-005","item_id":"37-007","geo_id":"GEO-37007","name":"梁统","dynasty":"汉","source_section":"名宦","note":"酒泉太守，从政尚严猛，威行邻郡"},
 {"pers_id":"PER-006","item_id":"37-007","geo_id":"GEO-37007","name":"第五访","dynasty":"汉","source_section":"名宦","note":"张掖太守，岁饥开廪振给，吏惧谴争欲上言，访曰若上须报是弃民也太守乐以一身救百姓，遂出谷赋人，玺书嘉之"},
 {"pers_id":"PER-007","item_id":"37-007","geo_id":"GEO-37007","name":"种暠","dynasty":"汉","source_section":"名宦","note":"凉州刺史，甚得百姓欢心，被征当迁，吏民诣阙请留，乃许复留一年"},
 {"pers_id":"PER-008","item_id":"37-007","geo_id":"GEO-37007","name":"邓训","dynasty":"汉","source_section":"名宦","note":"护羌校尉，湟中诸胡感其恩信相率归附；训遂罢屯兵惟分理屯田修坞壁，边境以宁"},
 {"pers_id":"PER-009","item_id":"37-007","geo_id":"GEO-37007","name":"孔奋","dynasty":"汉","source_section":"名宦","note":"守姑臧，常力行清洁；后被征单车就路，姑臧吏民敛送牛马诸物一无所受"},
 {"pers_id":"PER-010","item_id":"37-007","geo_id":"GEO-37007","name":"翟酺","dynasty":"汉","source_section":"名宦","note":"安帝时酒泉太守，时叛羌掠郡境，酺击之诛灭殆尽，威名大震"},
 {"pers_id":"PER-011","item_id":"37-007","geo_id":"GEO-37007","name":"皇甫规","dynasty":"汉","source_section":"名宦","note":"中郎将，讨先零诸羌破之，羌遂遣使乞降，凉州复通"},
 {"pers_id":"PER-012","item_id":"37-007","geo_id":"GEO-37007","name":"徐邈","dynasty":"三国","source_section":"名宦","note":"魏明帝时凉州刺史，立学明训，禁厚葬断淫祠，进善黜恶风化大行，西域流通"},
 {"pers_id":"PER-013","item_id":"37-007","geo_id":"GEO-37007","name":"仓慈","dynasty":"三国","source_section":"名宦","note":"魏炖煌太守，抑挫权右抚恤贫羸，民夷翕然称其德惠；数年卒，吏民悲感图画其形"},
 {"pers_id":"PER-014","item_id":"37-007","geo_id":"GEO-37007","name":"马隆","dynasty":"晋","source_section":"名宦","note":"武帝时树机能陷凉州，隆将兵讨破之，凉州遂平"},
 {"pers_id":"PER-015","item_id":"37-007","geo_id":"GEO-37007","name":"张轨","dynasty":"晋","source_section":"名宦","note":"凉州牧，时鲜卑寇掠，轨讨破之威着西土，遂据凉州号前凉"},
 {"pers_id":"PER-016","item_id":"37-007","geo_id":"GEO-37007","name":"司马望","dynasty":"晋","source_section":"名宦","note":"持节都督雍凉二州军事，在任八年威化明肃"},
 {"pers_id":"PER-017","item_id":"37-007","geo_id":"GEO-37007","name":"李暠","dynasty":"晋","source_section":"名宦","note":"肃州西曹掾从事，补司马别驾转炖煌太守领护西夷校尉；后为凉州牧称西凉王"},
 {"pers_id":"PER-018","item_id":"37-007","geo_id":"GEO-37007","name":"杨恭仁","dynasty":"隋","source_section":"名宦","note":"仁寿中甘州刺史，临事不苛细，徼人安之；文帝谓其父雄曰匪特朕得人乃卿善教子矣"},
 {"pers_id":"PER-019","item_id":"37-007","geo_id":"GEO-37007","name":"李大亮","dynasty":"唐","source_section":"名宦","note":"西北道安抚大使，诏欲贮粮碛口以赈西突厥，大亮言劳费无益不如罢之，其或自立君长求内属者羁縻受之使居塞外为中国藩蔽，此乃施虚惠而收实利，帝从之"},
 {"pers_id":"PER-020","item_id":"37-007","geo_id":"GEO-37007","name":"唐璿","dynasty":"唐","source_section":"名宦","note":"凉州都督，时吐蕃寇凉州，璿率众击之，六战皆克"},
 {"pers_id":"PER-021","item_id":"37-007","geo_id":"GEO-37007","name":"郭震","dynasty":"唐","source_section":"名宦","note":"凉州都督，先是突厥吐蕃常逼城下，震始控其冲要寇不复至；又令凉州刺史李汉通垦置屯田积粟数千斛，军用以足，夷夏畏慕"},
 {"pers_id":"PER-022","item_id":"37-007","geo_id":"GEO-37007","name":"王方翼","dynasty":"唐","source_section":"名宦","note":"高宗时肃州刺史，烽逻精明，河西蝗独不至方翼境，而他郡民或馁死，方翼治下全活甚众，芝产其地"},
 {"pers_id":"PER-023","item_id":"37-007","geo_id":"GEO-37007","name":"杜希望","dynasty":"唐","source_section":"名宦","note":"玄宗时鄯州都督，时军屡兴府库虚寡，希望居数岁刍粟金帛丰余"},
 {"pers_id":"PER-024","item_id":"37-007","geo_id":"GEO-37007","name":"张守珪","dynasty":"唐","source_section":"名宦","note":"开元中为瓜州刺史，虏奄至众失色，守珪置酒城上会诸将作乐，虏疑有备不敢攻引去，守珪纵兵击败之，迁瓜州都督"},
 {"pers_id":"PER-025","item_id":"37-007","geo_id":"GEO-37007","name":"高永年","dynasty":"宋","source_section":"名宦","note":"知西宁州，时夏人寇泾原，赊罗撒合兵逼城，永年出御之被执不屈而死"},
 {"pers_id":"PER-026","item_id":"37-007","geo_id":"GEO-37007","name":"巴图","dynasty":"元","source_section":"名宦","note":"延佑初甘肃行省平章政事，时米价腾涌陆挽一石费二百缗，乃为经画计所省至四百余万缗，自是诸仓充溢，岁饥则发粟赈之，春缺种则贷之，于是兵饷既足民食亦给"},
 {"pers_id":"PER-027","item_id":"37-007","geo_id":"GEO-37007","name":"濮瑛","dynasty":"明","source_section":"名宦","note":"凉州卫指挥使，洪武中修葺城楼仓库措置有方，士卒不劳而事集，郡称智能；寻以擒叛贼功升右军都督佥事掌陕西行都司事"},
 {"pers_id":"PER-028","item_id":"37-007","geo_id":"GEO-37007","name":"刘林","dynasty":"明","source_section":"名宦","note":"凉州卫百户，洪武中土官额森特穆尔等逃叛攻掠凉州，林击贼至城西土台力战而殁；事闻上嘉其忠勇，遣祭于台下"},
 {"pers_id":"PER-029","item_id":"37-007","geo_id":"GEO-37007","name":"宋晟","dynasty":"明","source_section":"名宦","note":"洪武中讨哈密有功，永乐初又遣都指挥史昭出兵擒火者厮通西域贡道；加封晟至西宁侯镇守甘肃；子琥袭父爵亦在甘肃镇守"},
 {"pers_id":"PER-030","item_id":"37-007","geo_id":"GEO-37007","name":"蒋贵","dynasty":"明","source_section":"名宦","note":"正统初敌人犯边，贵充总兵至甘肃击败敌众，以功升定西伯镇守甘肃，边境宁谧"},
 {"pers_id":"PER-031","item_id":"37-007","geo_id":"GEO-37007","name":"马援","dynasty":"汉","source_section":"流寓","note":"茂陵人，少有大志，王莽末避地凉州，隗嚣以为绥德将军；后归汉累功拜伏波将军"}
]

pers1_file = {
 "item_id":"37-007","volume":"37","source":"陕西行都指挥使司","region":"陕西行都司",
 "layer":"pers","subsection":"名宦+流寓",
 "pers":pers1,
 "validation":{"errs":[],"count":len(pers1),"notes":"名宦30人+流寓马援1人=31人"}
}
with open(os.path.join(OUT,"37-007_pers1_名宦.json"),"w",encoding="utf-8") as f:
 json.dump(pers1_file,f,ensure_ascii=False,indent=1)
print("pers1 written:",len(pers1))

# ===== pers2: 人物+列女 =====
pers2 = [
 {"pers_id":"PER-032","item_id":"37-007","geo_id":"GEO-37007","name":"金日磾","dynasty":"汉","source_section":"人物","note":"张掖人，休屠王子，没入官，武帝奇其壮貌拜为侍中赐姓金氏；尝欲纳其女于后宫日磾不肯；后为车骑将军与霍光同受遗诏辅政，着忠勋之节，封秺侯卒谥曰敬；二子赏建，昭帝时俱为侍中，赏嗣侯爵"},
 {"pers_id":"PER-033","item_id":"37-007","geo_id":"GEO-37007","name":"金伦","dynasty":"汉","source_section":"人物","note":"日磾弟，惇笃有智，仕为侍中封侯；四子常敞岑明，敞元帝时为侍中，与萧望之周堪刘向同心谋议；敞之子涉成帝时拜侍中；涉从弟钦平帝时为京兆尹，以家世忠孝迁光禄大夫"},
 {"pers_id":"PER-034","item_id":"37-007","geo_id":"GEO-37007","name":"张奂","dynasty":"汉","source_section":"人物","note":"炖煌酒泉人，父惇为汉阳太守，奂举贤良对策第一，为安定属国都尉，正身修德威化大行，拜武威太守；长子芝以善草书知名"},
 {"pers_id":"PER-035","item_id":"37-007","geo_id":"GEO-37007","name":"段颎","dynasty":"汉","source_section":"人物","note":"武威姑臧人，少便习弓马尚游侠轻财，长乃折节好古学，举孝廉为司隶校尉，与皇甫规张奂并显名于时"},
 {"pers_id":"PER-036","item_id":"37-007","geo_id":"GEO-37007","name":"盖勋","dynasty":"汉","source_section":"人物","note":"炖煌广至人，初举孝廉为汉阳长史，后领汉阳太守；时人饥相渔食，勋谷廪之存活者千余人，拜讨虏校尉；及董卓废少帝自公卿以下莫不卑下于卓，唯勋长揖争礼"},
 {"pers_id":"PER-037","item_id":"37-007","geo_id":"GEO-37007","name":"庞淯","dynasty":"三国","source_section":"人物","note":"酒泉福禄人，初以凉州从事守破羌长；会武威太守张猛反杀刺史邯郸商，淯闻之弃官奔哭丧所讫，徐诣猛门衷匕首欲杀猛，猛知其义士敕遣不杀；后太守徐揖请为主簿，郡人黄昂反围城，淯冒围出告急于张掖炖煌二郡，军未至而城陷揖死，淯乃收敛揖丧送还本郡；曹操闻之辟为掾属，文帝时赐爵关内侯"},
 {"pers_id":"PER-038","item_id":"37-007","geo_id":"GEO-37007","name":"贾诩","dynasty":"三国","source_section":"人物","note":"武威人，少时人莫知，惟阎忠异之谓其有良平之奇，察孝廉为郎历平津都尉；魏文帝即位以为太尉，卒谥敬侯"},
 {"pers_id":"PER-039","item_id":"37-007","geo_id":"GEO-37007","name":"贾疋","dynasty":"晋","source_section":"人物","note":"武威人，诩曾孙，愍帝时为雍州刺史封酒泉郡公，尝击败刘曜袭荡仲杀之；后为荡仲子夫护所害；疋勇略有志节以匡复晋室为己任，不幸颠坠，时人咸痛惜之"},
 {"pers_id":"PER-040","item_id":"37-007","geo_id":"GEO-37007","name":"索靖","dynasty":"晋","source_section":"人物","note":"炖煌人，累叶宦族，善草书；仕晋为尚书郎，初与乡人汜衷张彪索紾索永同诣太学驰名海内称炖煌五龙；四人并早亡，惟靖累官尚书郎，后为游击将军与贼战被伤而卒"},
 {"pers_id":"PER-041","item_id":"37-007","geo_id":"GEO-37007","name":"祁嘉","dynasty":"晋","source_section":"人物","note":"酒泉人，少清贫好学，年二十余西至炖煌依学宫诵书，贫无衣食为诸生都养以自给，遂博通经传精究大义；征为儒林祭酒，性和裕教训不倦，门生受业独拜床下者至二千余人"},
 {"pers_id":"PER-042","item_id":"37-007","geo_id":"GEO-37007","name":"宋纤","dynasty":"晋","source_section":"人物","note":"炖煌人，少有逸操，隐居酒泉南山，弟子受业者三千余人；时太守马岌具威仪造焉，纤拒不见，岌铭诗于壁曰丹崖百丈青壁万寻奇木蓊郁蔚若邓林其人如玉为国之琛室迩人遐实劳我心；卒年八十，谥曰玄虚先生"},
 {"pers_id":"PER-043","item_id":"37-007","geo_id":"GEO-37007","name":"索綝","dynasty":"晋","source_section":"人物","note":"靖子，少有逸群之量，靖每曰綝廊庙之才非简札之用州郡吏不足污吾儿也；仕晋累官至尚书左仆射，后为刘聪所获遇害"},
 {"pers_id":"PER-044","item_id":"37-007","geo_id":"GEO-37007","name":"贾彝","dynasty":"南北朝","source_section":"人物","note":"武威姑臧人，父为苻坚钜鹿太守坐讪谤系狱，彝年十岁诣长安讼父获伸，远近叹之；弱冠为慕容垂辽西王农记室参军；魏道武闻其名常遣使求彝，及即位拜为尚书左丞参谋预国政"},
 {"pers_id":"PER-045","item_id":"37-007","geo_id":"GEO-37007","name":"刘延明","dynasty":"南北朝","source_section":"人物","note":"后魏炖煌人，父宝以儒学称；延明年十四就博士郭瑀受业，瑀妻以女；后隐居酒泉不应州郡命，弟子受业者五百余人；凉武昭王征为儒林祭酒从事中郎，迁抚夷护军，虽有政务手不释卷"},
 {"pers_id":"PER-046","item_id":"37-007","geo_id":"GEO-37007","name":"宋繇","dynasty":"南北朝","source_section":"人物","note":"炖煌人，少以孝闻，随妹夫张彦至酒泉追师就学昼夜不倦，博通经史；事凉武昭王历位通显，家无余财，虽兵革间讲诵不辍；后入魏拜河西王相，赐爵清河公"},
 {"pers_id":"PER-047","item_id":"37-007","geo_id":"GEO-37007","name":"宋游道","dynasty":"南北朝","source_section":"人物","note":"繇曾孙，事母以孝闻，后魏时为殿中侍御史，台中语曰见恶能讨宋游道；孝庄即位除左兵中军，后入北齐为尚书左丞"},
 {"pers_id":"PER-048","item_id":"37-007","geo_id":"GEO-37007","name":"源贺","dynasty":"南北朝","source_section":"人物","note":"西平人，伟容貌善风仪，事魏太武赐爵西平侯，以功进平西将军；太武征凉州以为乡导，累官冀州刺史封陇西王，尝上十二阵图，卒赠侍中谥曰宣；子思礼谦恭宽雅有大度，文成末为侍御中散，诏持节巡行北边镇恒燕朔三州，上事宜三十余条皆见嘉纳"},
 {"pers_id":"PER-049","item_id":"37-007","geo_id":"GEO-37007","name":"段荣","dynasty":"南北朝","source_section":"人物","note":"姑臧人，祖信以豪族徙家五原郡，荣好历术专意星象；后魏正光中谓人曰吾今观玄象察人事不及十年当有乱矣；及齐神武起兵荣赞成之，论功封姑臧县侯，历相济秦三州，所至百姓爱之"},
 {"pers_id":"PER-050","item_id":"37-007","geo_id":"GEO-37007","name":"段韶","dynasty":"南北朝","source_section":"人物","note":"荣子，有将领略，以武明皇后甥齐神武益器爱之；韶袭父爵，事神武文襄加广平郡公，出总军旅入参帷幄功高望重；又教训子弟闺门雍睦，事后母以孝闻，齐代勋贵罕有及者"},
 {"pers_id":"PER-051","item_id":"37-007","geo_id":"GEO-37007","name":"阴铿","dynasty":"南北朝","source_section":"人物","note":"武威人，善五言诗，为梁湘东法曹参军；尝与宾友宴饮以酒炙授行觞者，众皆笑，铿曰吾侪终日酣醉执爵者不知其味非人情也；后遇侯景乱被贼擒，或救免之，乃前行觞者"},
 {"pers_id":"PER-052","item_id":"37-007","geo_id":"GEO-37007","name":"阴寿","dynasty":"隋","source_section":"人物","note":"武威人，少果烈有武干；文帝尝遣韦孝宽击尉迟迥，命寿监军，时孝宽有疾不能亲总戎事，三军纲纪皆决于寿；以功进位上柱国，拜幽州总管封赵郡公"},
 {"pers_id":"PER-053","item_id":"37-007","geo_id":"GEO-37007","name":"阴世师","dynasty":"隋","source_section":"人物","note":"寿子，性忠厚多武艺，以功臣子拜仪同；炀帝即位拜张掖太守甚为戎狄所惮，后迁左翊卫将军与代王留守京师；唐军至，世师自以世荷隋恩拒守不下见杀"},
 {"pers_id":"PER-054","item_id":"37-007","geo_id":"GEO-37007","name":"薛万均","dynasty":"唐","source_section":"人物","note":"本炖煌人，与弟万彻等客幽州事唐；从李靖讨吐谷浑，又副侯君集讨高昌皆有功，贞观中封潞国公；万彻及万淑万备俱以战功显为时名将，万淑封梁国公；万备有志行居母丧庐墓，太宗诏表其门，后仕至左卫将军"},
 {"pers_id":"PER-055","item_id":"37-007","geo_id":"GEO-37007","name":"赵武孟/赵彦昭","dynasty":"唐","source_section":"人物","note":"甘州张掖人，少游猎以所获馈其母，母泣曰汝不好书而敖荡吾安望哉不为食，武孟感激遂力学淹该书记，自长安丞为右台御史，着河西人物志十篇；子彦昭少豪迈风骨秀爽，及进士第，景龙中累迁中书侍郎同平章事"},
 {"pers_id":"PER-056","item_id":"37-007","geo_id":"GEO-37007","name":"乌承玼","dynasty":"唐","source_section":"人物","note":"张掖人，开元中与族兄承恩皆为平卢先锋，沈勇而决号辕门二龙；后破奚契丹，从战捺禄走可突于，渤海扰海上吏民逃徙失业，承玼以兵塞要路堑原累石绵四百里，寇不得入；其后又说史思明降，官至检校殿中监封昌化郡王"},
 {"pers_id":"PER-057","item_id":"37-007","geo_id":"GEO-37007","name":"段平仲","dynasty":"唐","source_section":"人物","note":"武威人，擢进士第为监察御史，有气节嗜酒敢言；德宗春秋高躬自听断，平仲对及由是坐废；元和初为谏议大夫再迁尚书左丞，朝廷有得失未尝不论奏"},
 {"pers_id":"PER-058","item_id":"37-007","geo_id":"GEO-37007","name":"李抱玉","dynasty":"唐","source_section":"人物","note":"本安兴贵曾孙，世居河西，为人沉毅有谋，李光弼引为裨校有战功；安禄山乱，抱玉上言世居凉州耻与逆臣共宗，诏赐姓李，官至司空兼兵部尚书加山南西道副元帅，卒赠太保"},
 {"pers_id":"PER-059","item_id":"37-007","geo_id":"GEO-37007","name":"李抱真","dynasty":"唐","source_section":"人物","note":"抱玉从弟，沈虑而断，抱玉属以军事；代宗时授泽潞节度副使，抱真以泽潞兵所走集乃籍户丁给弓矢习射，三年皆为精兵；田悦反抱真战走之，又说王武俊共破朱滔，累官检校司空"},
 {"pers_id":"PER-060","item_id":"37-007","geo_id":"GEO-37007","name":"乌重胤","dynasty":"唐","source_section":"人物","note":"承玼子，少为潞牙将兼左司马；节度使卢从史奉诏讨贼阴与贼连，重胤乃缚从史帐下叱兵士曰天子有命违者斩，士敛手还部无敢动者；宪宗嘉其功擢河阳节度使封张掖郡公；重胤善抚士待官属有礼，其在河阳名士如温造石洪皆辟致幕下人多称之"},
 {"pers_id":"PER-061","item_id":"37-007","geo_id":"GEO-37007","name":"李琪","dynasty":"五代","source_section":"人物","note":"炖煌人，举进士博学宏辞，事梁为翰林学士，梁兵征伐四方诏书皆琪所为下笔辄得太祖意；梁亡仕唐累官至右仆射；琪少以文章知名，既贵乃刻牙板为金字曰前乡贡进士李琪，常置坐侧"},
 {"pers_id":"PER-062","item_id":"37-007","geo_id":"GEO-37007","name":"刘容","dynasty":"元","source_section":"人物","note":"其先西宁青海人，父海川徙云京后遂为云京人；容喜读书亦善骑射，中统初入侍皇太子，每退直即诣祭酒许衡游，后累官太子司议出为广平路总管有治声"},
 {"pers_id":"PER-063","item_id":"37-007","geo_id":"GEO-37007","name":"昂吉尔","dynasty":"元","source_section":"人物","note":"张掖人，世为西夏将家，父堪布率所部归元为千户，及卒昂吉尔领父军从征诸国有功；又略地淮南，世祖时累官行尚书省右丞；时欲征日本，昂吉尔疏谏不从，既而师果无功；昂吉尔屡为直言，帝虽怒甚其辞不少屈"},
 {"pers_id":"PER-064","item_id":"37-007","geo_id":"GEO-37007","name":"余阙","dynasty":"元","source_section":"人物","note":"武威人，徙庐州，少丧父授徒以养母；元统初赐进士及第，授同知泗州事，历翰林修撰待制；至正中盗起以阙为都元帅府佥事分兵守安庆，俄升都元帅，论保障功拜淮南行省参政仍守安庆；群盗四集以孤军血战，城陷自刭，妻子皆赴井死"},
 {"pers_id":"PER-065","item_id":"37-007","geo_id":"GEO-37007","name":"吴允诚","dynasty":"明","source_section":"人物","note":"凉州人，永乐中累立战功，历升左都督进封恭顺伯"},
 {"pers_id":"PER-066","item_id":"37-007","geo_id":"GEO-37007","name":"吴管者","dynasty":"明","source_section":"人物","note":"允诚子，历官都指挥同知效劳于国，洪熙初进封广义伯"},
 {"pers_id":"PER-067","item_id":"37-007","geo_id":"GEO-37007","name":"吴克忠","dynasty":"明","source_section":"人物","note":"允诚子，袭恭顺伯，洪熙初加封恭顺侯太子太保，能以忠节自励，从征边寇力战而没，追封邠国公谥壮勇；弟克勤为都督，与兄克忠同没于阵，谥僖敏"},
 {"pers_id":"PER-068","item_id":"37-007","geo_id":"GEO-37007","name":"赵娥","dynasty":"汉","source_section":"列女","note":"酒泉人，父安为同县李寿所杀，娥兄弟三人同时病死，寿家防备懈弛，娥自伤父雠不报乃帏车袖剑白日刺寿于都亭前，徐诣县颜色不变曰父雠已报请受戮；县长尹嘉欲弛法纵娥，娥不肯去，遂强载还家，后遇赦得免，州郡叹赏刊石表闾；子即庞淯也"}
]

pers2_file = {
 "item_id":"37-007","volume":"37","source":"陕西行都指挥使司","region":"陕西行都司",
 "layer":"pers","subsection":"人物+列女",
 "pers":pers2,
 "validation":{"errs":[],"count":len(pers2),"notes":"人物36人+列女赵娥1人=37人；赵娥即庞淯之母"}
}
with open(os.path.join(OUT,"37-007_pers2_人物列女.json"),"w",encoding="utf-8") as f:
 json.dump(pers2_file,f,ensure_ascii=False,indent=1)
print("pers2 written:",len(pers2))

print("DONE")
