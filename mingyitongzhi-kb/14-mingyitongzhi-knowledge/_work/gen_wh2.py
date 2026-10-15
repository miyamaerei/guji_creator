# -*- coding: utf-8 -*-
# Generate 卫辉府 28-001 JSON files
import json, os
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol28"
WID = "28-001"
WG = "GEO-28001"

wh_main = {
  "item_id": WID, "volume": "28", "source": "卫辉府", "region": "河南", "type": "prefecture",
  "original": "卫辉府【东至直隷大名府滑县界五十里南至开封府延津县界四十里西至山西泽州陵川县界二百一十里北至彰徳府汤隂县界七十里自府治至京师一千四百里至南京一千五百里】【粮二十四万五千六百石零】",
  "layers": {
    "ents": [
      {"ent_id":"ENT-001","name":"卫辉府","type":"geo","norm":"卫辉府","first_source":WID},
      {"ent_id":"ENT-002","name":"汲县","type":"geo","norm":"汲县","first_source":WID},
      {"ent_id":"ENT-003","name":"胙城县","type":"geo","norm":"胙城县","first_source":WID},
      {"ent_id":"ENT-004","name":"新乡县","type":"geo","norm":"新乡县","first_source":WID},
      {"ent_id":"ENT-005","name":"获嘉县","type":"geo","norm":"获嘉县","first_source":WID},
      {"ent_id":"ENT-006","name":"淇县","type":"geo","norm":"淇县","first_source":WID},
      {"ent_id":"ENT-007","name":"辉县","type":"geo","norm":"辉县","first_source":WID},
      {"ent_id":"ENT-008","name":"朝歌","type":"geo","norm":"朝歌","first_source":WID},
      {"ent_id":"ENT-009","name":"卫州","type":"geo","norm":"卫州","first_source":WID},
      {"ent_id":"ENT-010","name":"苏门山","type":"mtn","norm":"苏门山","first_source":WID},
      {"ent_id":"ENT-011","name":"太行山","type":"mtn","norm":"太行山","first_source":WID},
      {"ent_id":"ENT-012","name":"史记","type":"book","norm":"史记","first_source":WID},
      {"ent_id":"ENT-013","name":"宋地理志","type":"book","norm":"宋地理志","first_source":WID},
      {"ent_id":"ENT-014","name":"元志","type":"book","norm":"元志","first_source":WID},
      {"ent_id":"ENT-015","name":"汉书","type":"book","norm":"汉书","first_source":WID},
      {"ent_id":"ENT-016","name":"舆地志","type":"book","norm":"舆地志","first_source":WID},
      {"ent_id":"ENT-017","name":"续郡志","type":"book","norm":"续郡志","first_source":WID}
    ],
    "geos": [
      {"geo_id":WG,"item_id":WID,"name":"卫辉府","type":"prefecture","region":"河南","parent":"GEO-000",
       "children":["GEO-28001c01","GEO-28001c02","GEO-28001c03","GEO-28001c04","GEO-28001c05","GEO-28001c06","GEO-28001w01"],
       "volume_range":"卷28",
       "attributes":{
         "borders":[
           {"direction":"东","to_place":"直隶大名府滑县界","distance_li":50},
           {"direction":"南","to_place":"开封府延津县界","distance_li":40},
           {"direction":"西","to_place":"山西泽州陵川县界","distance_li":210},
           {"direction":"北","to_place":"彰德府汤阴县界","distance_li":70}],
         "to_capital":[{"capital":"京师","distance_li":1400},{"capital":"南京","distance_li":1500}],
         "grain_tax":{"amount":245600,"unit":"石","note":"二十四万五千六百石零"},
         "jun_name":"古卫朝歌汲郡",
         "topography":"左孟门右太行【史记】；南滨大河西压上党【宋地理志】；峰麓奇峻地当冲要泉甘水温【俱元志】",
         "customs":"刚武尚气力【汉书】周末有子路夏育民人慕之故其俗刚武上气力；民情颇事商贾地饶俗淳勤于播种【俱元志】；重义疏财有先王遗风【舆地志】；人知向学彬彬有文【续郡志】",
         "garrisons":[{"name":"守御卫辉前千户所","type":"千户所","location_text":"在府城内东洪武二十三年建属怀庆卫"}],
         "fiefs":[{"name":"汝府","location":"在府城内"},{"name":"潞府","location":"在府城内万历十六年建"}]
       },
       "cit_ids":["CIT-001","CIT-002","CIT-003","CIT-004","CIT-005","CIT-006"]},
      {"geo_id":"GEO-28001w01","item_id":WID,"name":"守御卫辉前千户所","type":"weisuo","region":"河南","parent":WG,"children":[],"volume_range":"卷28","attributes":{"location_text":"在府城内东洪武二十三年建属怀庆卫"},"cit_ids":[]}
    ],
    "evos":[
      {"evo_id":"EVO-001","item_id":WID,"geo_id":WG,"dynasty":"商","era":None,"institution_name":"朝歌","action":"因之","detail":"禹贡冀州之域，天文室壁分野，本殷纣所都朝歌之地"},
      {"evo_id":"EVO-002","item_id":WID,"geo_id":WG,"dynasty":"周","era":None,"institution_name":"邶鄘卫","action":"置","detail":"周武王克殷分其北为邶南为鄘东为卫，后封康叔于卫"},
      {"evo_id":"EVO-003","item_id":WID,"geo_id":WG,"dynasty":"战国","era":None,"institution_name":"魏地","action":"因之","detail":"春秋时邶鄘入之，战国属魏"},
      {"evo_id":"EVO-004","item_id":WID,"geo_id":WG,"dynasty":"秦","era":None,"institution_name":"河东郡地","action":"置","detail":"秦属河东郡"},
      {"evo_id":"EVO-005","item_id":WID,"geo_id":WG,"dynasty":"汉","era":None,"institution_name":"汲县地","action":"置","detail":"汉为汲县地属河内郡，曹魏置朝歌郡属冀州"},
      {"evo_id":"EVO-006","item_id":WID,"geo_id":WG,"dynasty":"晋","era":None,"institution_name":"汲郡","action":"改","detail":"晋改汲郡，后魏徙郡治枋头城而于此置义州"},
      {"evo_id":"EVO-007","item_id":WID,"geo_id":WG,"dynasty":"北周","era":None,"institution_name":"卫州","action":"改","detail":"后周改卫州，隋大业初改汲郡"},
      {"evo_id":"EVO-008","item_id":WID,"geo_id":WG,"dynasty":"唐","era":None,"institution_name":"卫州","action":"复","detail":"唐武德初复为义州寻复改卫州，天宝初又为汲郡乾元初复为卫州属河北道"},
      {"evo_id":"EVO-009","item_id":WID,"geo_id":WG,"dynasty":"金","era":None,"institution_name":"河平军","action":"改","detail":"宋因之，金改河平军徙治胙城"},
      {"evo_id":"EVO-010","item_id":WID,"geo_id":WG,"dynasty":"元","era":None,"institution_name":"卫辉路","action":"改","detail":"元改卫辉路还治汲县"},
      {"evo_id":"EVO-011","item_id":WID,"geo_id":WG,"dynasty":"明","era":None,"institution_name":"卫辉府","action":"改","detail":"本朝改为卫辉府领县六"}
    ],
    "mtns":[
      {"mtn_id":"MTN-001","item_id":WID,"geo_id":WG,"name":"苍山","type":"山","location_text":"在府城西北四十里一名苍峪山","description":"产珉石上有龙潭神祠岁旱祷雨有应","lore":""},
      {"mtn_id":"MTN-002","item_id":WID,"geo_id":WG,"name":"卫河","type":"河","location_text":"源发苏门山东北流经府城北一里","description":"东入大名府濬县界","lore":""},
      {"mtn_id":"MTN-003","item_id":WID,"geo_id":WG,"name":"黄河","type":"河","location_text":"自新乡县西南敦留村入境","description":"东南流经胙城县入开封府原武县界","lore":""},
      {"mtn_id":"MTN-004","item_id":WID,"geo_id":WG,"name":"太公泉","type":"泉","location_text":"在府城西北二十五里","description":"下流达于卫河，上有周太公吕望庙","lore":""}
    ],
    "pers":[], "sites":[],
    "prods":[
      {"prod_id":"PROD-001","item_id":WID,"geo_id":WG,"name":"青铁","category":"矿物","note":"俱汲县苍山出"},
      {"prod_id":"PROD-002","item_id":WID,"geo_id":WG,"name":"珉石","category":"矿物","note":"俱汲县苍山出"},
      {"prod_id":"PROD-003","item_id":WID,"geo_id":WG,"name":"括蒌根","category":"药材","note":"胙城县出"},
      {"prod_id":"PROD-004","item_id":WID,"geo_id":WG,"name":"仙茅","category":"药材","note":"新乡县鲁包村出"},
      {"prod_id":"PROD-005","item_id":WID,"geo_id":WG,"name":"锡","category":"矿物","note":"俱淇县出"},
      {"prod_id":"PROD-006","item_id":WID,"geo_id":WG,"name":"青瓷","category":"矿物","note":"俱淇县出"}
    ],
    "cits":[
      {"cit_id":"CIT-001","item_id":WID,"cited_work":"史记","cited_work_ent_id":"ENT-012","context":"立论","original":"【史记】"},
      {"cit_id":"CIT-002","item_id":WID,"cited_work":"宋地理志","cited_work_ent_id":"ENT-013","context":"立论","original":"【宋地理志】"},
      {"cit_id":"CIT-003","item_id":WID,"cited_work":"元志","cited_work_ent_id":"ENT-014","context":"立论","original":"【俱元志】"},
      {"cit_id":"CIT-004","item_id":WID,"cited_work":"汉书","cited_work_ent_id":"ENT-015","context":"证俗","original":"【汉书】"},
      {"cit_id":"CIT-005","item_id":WID,"cited_work":"舆地志","cited_work_ent_id":"ENT-016","context":"证俗","original":"【舆地志】"},
      {"cit_id":"CIT-006","item_id":WID,"cited_work":"续郡志","cited_work_ent_id":"ENT-017","context":"证俗","original":"【续郡志】"}
    ]
  },
  "layer_count":7,
  "validation":{"errs":[],"gap":0,"notes":"pers和sites拆为独立文件；府级山川只留府城附近"}
}
with open(os.path.join(OUT,"28-001_卫辉府.json"),"w",encoding="utf-8") as f:
    json.dump(wh_main,f,ensure_ascii=False,indent=2)
print("卫辉 main done")

# pers split
wp = lambda pid,n,t,d,np,o,s: {"per_id":pid,"item_id":WID,"geo_id":WG,"name":n,"type":t,"dynasty":d,"native_place":np,"office":o,"summary":s}
wh_pers = [
  wp("PER-001","樊儵","名宦","汉","","南燕侯","封南燕侯，治春秋学之十年，自寿张侯徙封于此"),
  wp("PER-002","虞诩","名宦","汉","","朝歌长","先是剧盗攻杀长吏，诩至募壮士使入贼中诱令劫掠乃伏兵擒杀，贼由是骇散"),
  wp("PER-003","崔瑗","名宦","汉","","汲令","教民开稻田数百顷，为政七年人歌之曰天降神明君赐我慈仁父"),
  wp("PER-004","郭进","名宦","五代","","卫州刺史","周卫州刺史平河朔之盗，民得安居"),
  wp("PER-005","李之才","名宦","宋","","共城令","获嘉主簿摄共城令有治行，闻邵雍苦学亲造其庐而问之授以物理性命之学"),
  wp("PER-006","陈祐","名宦","元","","卫辉路总管","清介公正惠政及民，既去民思之如父母"),
  wp("PER-007","董文用","名宦","元","","卫辉路总管","时有重役妨农，文用驱胥校以应民用不困"),
  wp("PER-008","张俊","名宦","明","","汲县知县","洪武末革吏胥奸弊，赋役亲验版籍务得均平"),
  wp("PER-009","邢表","名宦","明","","卫辉知府","由进士知获嘉县寻升卫辉知府有惠政，及去民脱履遮留"),
  wp("PER-010","太公望","人物","周","汲","齐太公","姓姜名子牙，年八十余避纣居北海滨，周文王出猎遇于渭水之阳载归立为师，佐武王伐纣"),
  wp("PER-011","蘧伯玉","人物","周","卫","大夫","行年五十而知四十九年之非，孔子至卫主于其家，称之曰君子哉蘧伯玉"),
  wp("PER-012","卜商","人物","周","卫","孔门弟子","即子夏，居文学科，退而老于西河教授，门人魏文侯师事之"),
  wp("PER-013","端木赐","人物","周","卫","孔门弟子","即子贡，居言语科，颖悟明敏料事多中"),
  wp("PER-014","吴起","人物","周","卫","楚相","尝学于曾子好用兵，为鲁将破齐复为魏将击秦，楚悼王闻其贤以为相"),
  wp("PER-015","杜诗","人物","汉","汲","南阳太守","性至孝，迁南阳太守政治清平教化大行，及卒贫困无田宅丧无所归"),
  wp("PER-016","邵雍","流寓","宋","范阳","康节先生","幼随父古徙共城，受学李之才覃思于易，后迁居洛阳，元封康节"),
  wp("PER-017","姚枢","流寓","元","柳城","中书左丞","弃官来辉州作家庙读书，世祖在潜邸以礼聘至敷陈治道数千言"),
  wp("PER-018","许衡","流寓","元","河内","魏国公","从姚枢于苏门得程朱书，慨然以道为己任，仕至集贤大学士兼国子祭酒"),
  wp("PER-019","共姜","列女","周","卫","卫世子共伯妻","共伯早死共姜守义，父母欲夺而嫁之共姜不许，作柏舟之诗以死自誓"),
  wp("PER-020","夏侯氏","列女","唐","胙城","刘寂妻","父丧明无子，时已生二女求与寂绝归侍父，后五年父亡毁不胜丧"),
  wp("PER-021","刘海蟾","仙释","五代","","","白鹤观忽见道人谒于堂下，壁间有题字以仙书证乃秦人刘海蟾之笔")
]
pf = {"item_id":WID,"volume":"28","source":"卫辉府-人物层","region":"河南",
  "layers":{"ents":[],"geos":[],"evos":[],"mtns":[],"pers":wh_pers,"sites":[],"prods":[],"cits":[]},
  "layer_count":7,"validation":{"errs":[],"gap":0,"notes":""}}
with open(os.path.join(OUT,"28-001_卫辉府_pers.json"),"w",encoding="utf-8") as f:
    json.dump(pf,f,ensure_ascii=False,indent=2)
print("pers done")

# sites split
ws = lambda sid,n,t,l,h: {"site_id":sid,"item_id":WID,"geo_id":WG,"name":n,"type":t,"location_text":l,"history_lore":h}
wh_sites = [
  ws("SITE-001","卫辉府学","学校","在府城内西北隅","元至元间建，本朝洪武三年重建"),
  ws("SITE-002","比干庙","祠庙","在府城北北固社","比干纣诸父，魏文帝建后毁本朝重建，每岁四月四日有司致祭"),
  ws("SITE-003","太公庙","祠庙","在府城内西南","有汉崔瑗所书碑刻尚存"),
  ws("SITE-004","比干墓","陵墓","在府城北一十里","即武王所封者，有石题曰殷太师比干之墓，后魏孝文帝南巡亲幸吊祭"),
  ws("SITE-005","汲冢","古迹","在府城西南二十七里","汉初有人于此冢盗金得竹简书十余万言，世号汲冢书"),
  ws("SITE-006","牧野","古迹","在府城南陵西社","朝歌之南周武王伐纣陈师牧野即此"),
  ws("SITE-007","朝歌邑","古迹","在淇县北关西社","即殷旧都朝歌地，汉置县莽更曰雅歌"),
  ws("SITE-008","淇园","古迹","在淇县西北礼河社","昔卫武公年九十有五犹自箴警，国人赋诗曰瞻彼淇澳菉竹猗猗"),
  ws("SITE-009","天宁寺","寺观","在府治西","旧为院晋开运初建，本朝洪武中重建改为寺"),
  ws("SITE-010","延津关","关梁","在府城东南二十五里","")
]
sf = {"item_id":WID,"volume":"28","source":"卫辉府-寺观祠庙古迹","region":"河南",
  "layers":{"ents":[],"geos":[],"evos":[],"mtns":[],"pers":[],"sites":wh_sites,"prods":[],"cits":[]},
  "layer_count":7,"validation":{"errs":[],"gap":0,"notes":""}}
with open(os.path.join(OUT,"28-001_卫辉府_sites.json"),"w",encoding="utf-8") as f:
    json.dump(sf,f,ensure_ascii=False,indent=2)
print("sites done")

# county files
def cty(cid,name,loc,hh_note,hh_count,evos,mtns=None,sites=None):
    return {"item_id":WID,"volume":"28","source":name,"region":"河南","type":"county",
      "original":f"{name}【{loc}编户{hh_note}】",
      "layers":{"ents":[{"ent_id":"ENT-001","name":name,"type":"geo","norm":name,"first_source":WID}],
        "geos":[{"geo_id":f"GEO-28001{cid}","item_id":WID,"name":name,"type":"county","region":"河南","parent":WG,"children":[],"volume_range":"卷28","attributes":{"location_text":loc,"households":{"count":hh_count,"unit":"里","note":f"编户{hh_note}"}},"cit_ids":[]}],
        "evos":evos,"mtns":mtns or [],"pers":[],"sites":sites or [],"prods":[],"cits":[]},
      "layer_count":7,"validation":{"errs":[],"gap":0,"notes":""}}

c1 = cty("c01","汲县","附郭","四十里",40,[
  {"evo_id":"EVO-001","item_id":WID,"geo_id":"GEO-28001c01","dynasty":"殷","era":None,"institution_name":"牧野地","action":"因之","detail":"本殷牧野之地"},
  {"evo_id":"EVO-002","item_id":WID,"geo_id":"GEO-28001c01","dynasty":"汉","era":None,"institution_name":"汲县","action":"置","detail":"汉置汲县属河内郡，魏属朝歌郡，晋为汲郡治"},
  {"evo_id":"EVO-003","item_id":WID,"geo_id":"GEO-28001c01","dynasty":"隋","era":None,"institution_name":"汲县","action":"复","detail":"后魏置伍城郡及县，周以县属卫州，隋复改为汲县属汲郡"},
  {"evo_id":"EVO-004","item_id":WID,"geo_id":"GEO-28001c01","dynasty":"唐","era":None,"institution_name":"汲县","action":"因之","detail":"唐徙卫州治此，宋元仍旧本朝因之"}])
with open(os.path.join(OUT,"28-001_c01_汲县.json"),"w",encoding="utf-8") as f: json.dump(c1,f,ensure_ascii=False,indent=2)

c2 = cty("c02","胙城县","在府城东三十五里","一十九里",19,[
  {"evo_id":"EVO-001","item_id":WID,"geo_id":"GEO-28001c02","dynasty":"周","era":None,"institution_name":"胙国","action":"置","detail":"古胙国，周公别子封胙伯于此，春秋时为南燕国"},
  {"evo_id":"EVO-002","item_id":WID,"geo_id":"GEO-28001c02","dynasty":"汉","era":None,"institution_name":"南燕县","action":"置","detail":"汉置南燕县属东郡，晋时慕容德据之号东燕县"},
  {"evo_id":"EVO-003","item_id":WID,"geo_id":"GEO-28001c02","dynasty":"隋","era":None,"institution_name":"胙城县","action":"改","detail":"隋始改为胙城县属滑州，唐置胙州后州废，宋元仍旧本朝改今属"}])
with open(os.path.join(OUT,"28-001_c02_胙城县.json"),"w",encoding="utf-8") as f: json.dump(c2,f,ensure_ascii=False,indent=2)

c3 = cty("c03","新乡县","在府城西五十里","三十二里",32,[
  {"evo_id":"EVO-001","item_id":WID,"geo_id":"GEO-28001c03","dynasty":"汉","era":None,"institution_name":"获嘉汲二县地","action":"因之","detail":"本汉河内郡获嘉汲二县地"},
  {"evo_id":"EVO-002","item_id":WID,"geo_id":"GEO-28001c03","dynasty":"隋","era":None,"institution_name":"新乡县","action":"置","detail":"隋于古新乐城置新乡县，唐初属义州后属卫州"},
  {"evo_id":"EVO-003","item_id":WID,"geo_id":"GEO-28001c03","dynasty":"宋","era":"熙宁","institution_name":"废","action":"废","detail":"宋熙宁中省入汲县，元祐初复置"},
  {"evo_id":"EVO-004","item_id":WID,"geo_id":"GEO-28001c03","dynasty":"明","era":None,"institution_name":"新乡县","action":"因之","detail":"金元仍旧本朝因之"}])
with open(os.path.join(OUT,"28-001_c03_新乡县.json"),"w",encoding="utf-8") as f: json.dump(c3,f,ensure_ascii=False,indent=2)

c4 = cty("c04","获嘉县","在府城西北一百里","一十八里",18,[
  {"evo_id":"EVO-001","item_id":WID,"geo_id":"GEO-28001c04","dynasty":"殷","era":None,"institution_name":"宁邑","action":"因之","detail":"本殷之宁邑地，周为修武地"},
  {"evo_id":"EVO-002","item_id":WID,"geo_id":"GEO-28001c04","dynasty":"汉","era":None,"institution_name":"获嘉县","action":"置","detail":"汉武帝幸缑氏至汲县得南越相吕嘉首，因置县名获嘉属河内郡"},
  {"evo_id":"EVO-003","item_id":WID,"geo_id":"GEO-28001c04","dynasty":"隋","era":"开皇","institution_name":"获嘉县","action":"迁","detail":"北齐移获嘉治共城，隋开皇中移治于此，唐初置殷州贞观中州废以县属怀州"},
  {"evo_id":"EVO-004","item_id":WID,"geo_id":"GEO-28001c04","dynasty":"明","era":None,"institution_name":"获嘉县","action":"因之","detail":"宋元仍旧本朝因之"}],
  mtns=[{"mtn_id":"MTN-001","item_id":WID,"geo_id":"GEO-28001c04","name":"同盟山","type":"山","location_text":"在获嘉县东北五十里","description":"相传武王伐纣与诸侯同盟于此故名","lore":""}])
with open(os.path.join(OUT,"28-001_c04_获嘉县.json"),"w",encoding="utf-8") as f: json.dump(c4,f,ensure_ascii=False,indent=2)

c5 = cty("c05","淇县","在府城北五十里","二十二里",22,[
  {"evo_id":"EVO-001","item_id":WID,"geo_id":"GEO-28001c05","dynasty":"商","era":None,"institution_name":"朝歌","action":"因之","detail":"古朝歌地，周为沬邑"},
  {"evo_id":"EVO-002","item_id":WID,"geo_id":"GEO-28001c05","dynasty":"秦","era":None,"institution_name":"三川郡地","action":"因之","detail":"秦属三川郡"},
  {"evo_id":"EVO-003","item_id":WID,"geo_id":"GEO-28001c05","dynasty":"汉","era":None,"institution_name":"朝歌县","action":"置","detail":"汉置朝歌县属河内郡，三国魏属朝歌郡晋属汲郡"},
  {"evo_id":"EVO-004","item_id":WID,"geo_id":"GEO-28001c05","dynasty":"元","era":None,"institution_name":"淇州","action":"升","detail":"后魏废元置淇州"},
  {"evo_id":"EVO-005","item_id":WID,"geo_id":"GEO-28001c05","dynasty":"明","era":None,"institution_name":"淇县","action":"降","detail":"本朝降为县"}],
  sites=[
    {"site_id":"SITE-001","item_id":WID,"geo_id":"GEO-28001c05","name":"摘星楼","type":"宫室","location_text":"在淇县古朝歌城上","history_lore":"相传纣与妲己观斮朝涉之胫处"},
    {"site_id":"SITE-002","item_id":WID,"geo_id":"GEO-28001c05","name":"淇县学","type":"学校","location_text":"在县治西北","history_lore":"元至元间建，本朝洪武三年重修"}])
with open(os.path.join(OUT,"28-001_c05_淇县.json"),"w",encoding="utf-8") as f: json.dump(c5,f,ensure_ascii=False,indent=2)

c6 = cty("c06","辉县","在府城西六十里","三十六里",36,[
  {"evo_id":"EVO-001","item_id":WID,"geo_id":"GEO-28001c06","dynasty":"周","era":None,"institution_name":"共国","action":"置","detail":"古共伯之国，周共国地，春秋时并于卫"},
  {"evo_id":"EVO-002","item_id":WID,"geo_id":"GEO-28001c06","dynasty":"汉","era":None,"institution_name":"共县","action":"置","detail":"汉置共县属河内郡，晋属汲郡"},
  {"evo_id":"EVO-003","item_id":WID,"geo_id":"GEO-28001c06","dynasty":"隋","era":None,"institution_name":"共城县","action":"改","detail":"隋改为共城县，唐初以县置共州并析置凡城县寻废州"},
  {"evo_id":"EVO-004","item_id":WID,"geo_id":"GEO-28001c06","dynasty":"金","era":None,"institution_name":"辉州","action":"升","detail":"金改河平县又改苏门县后升为辉州，元因之"},
  {"evo_id":"EVO-005","item_id":WID,"geo_id":"GEO-28001c06","dynasty":"明","era":None,"institution_name":"辉县","action":"降","detail":"本朝仍为县"}],
  mtns=[
    {"mtn_id":"MTN-001","item_id":WID,"geo_id":"GEO-28001c06","name":"苏门山","type":"山","location_text":"在辉县西北七里一名百门山","description":"晋孙登隐此号苏门先生，阮籍往见之","lore":""},
    {"mtn_id":"MTN-002","item_id":WID,"geo_id":"GEO-28001c06","name":"共山","type":"山","location_text":"在辉县东北八里俗呼九山","description":"以九日登临故名","lore":""}],
  sites=[
    {"site_id":"SITE-001","item_id":WID,"geo_id":"GEO-28001c06","name":"辉县学","type":"学校","location_text":"在县治西","history_lore":"元至元间建，本朝洪武九年重修"},
    {"site_id":"SITE-002","item_id":WID,"geo_id":"GEO-28001c06","name":"百泉亭","type":"古迹","location_text":"在百门泉上","history_lore":"金明昌间建，元儒许衡尝与门生咏于此"}])
with open(os.path.join(OUT,"28-001_c06_辉县.json"),"w",encoding="utf-8") as f: json.dump(c6,f,ensure_ascii=False,indent=2)

print("卫辉府 all done!")
