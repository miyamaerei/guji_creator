# -*- coding: utf-8 -*-
# Generate 怀庆府 28-002 JSON files
import json, os
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol28"
HID = "28-002"
HG = "GEO-28002"

hq_main = {
  "item_id": HID, "volume": "28", "source": "怀庆府", "region": "河南", "type": "prefecture",
  "original": "懐庆府【东至卫辉府获嘉县界二百四十里西至山西平阳府絳州垣曲县界二百五十里南至河南府巩县界七十里北至山西泽州界六十五里自府治至京师及南京俱一千八百里】【粮三十三万六百石零】",
  "layers": {
    "ents": [
      {"ent_id":"ENT-001","name":"怀庆府","type":"geo","norm":"怀庆府","first_source":HID},
      {"ent_id":"ENT-002","name":"河内县","type":"geo","norm":"河内县","first_source":HID},
      {"ent_id":"ENT-003","name":"济源县","type":"geo","norm":"济源县","first_source":HID},
      {"ent_id":"ENT-004","name":"修武县","type":"geo","norm":"修武县","first_source":HID},
      {"ent_id":"ENT-005","name":"武陟县","type":"geo","norm":"武陟县","first_source":HID},
      {"ent_id":"ENT-006","name":"孟县","type":"geo","norm":"孟县","first_source":HID},
      {"ent_id":"ENT-007","name":"温县","type":"geo","norm":"温县","first_source":HID},
      {"ent_id":"ENT-008","name":"河内郡","type":"geo","norm":"河内郡","first_source":HID},
      {"ent_id":"ENT-009","name":"怀州","type":"geo","norm":"怀州","first_source":HID},
      {"ent_id":"ENT-010","name":"太行山","type":"mtn","norm":"太行山","first_source":HID},
      {"ent_id":"ENT-011","name":"黄河","type":"mtn","norm":"黄河","first_source":HID},
      {"ent_id":"ENT-012","name":"济渎","type":"mtn","norm":"济渎","first_source":HID},
      {"ent_id":"ENT-013","name":"禹贡","type":"book","norm":"禹贡","first_source":HID},
      {"ent_id":"ENT-014","name":"左传","type":"book","norm":"左传","first_source":HID},
      {"ent_id":"ENT-015","name":"汉书","type":"book","norm":"汉书","first_source":HID},
      {"ent_id":"ENT-016","name":"宋志","type":"book","norm":"宋志","first_source":HID},
      {"ent_id":"ENT-017","name":"地志","type":"book","norm":"地志","first_source":HID}
    ],
    "geos": [
      {"geo_id":HG,"item_id":HID,"name":"怀庆府","type":"prefecture","region":"河南","parent":"GEO-000",
       "children":["GEO-28002c01","GEO-28002c02","GEO-28002c03","GEO-28002c04","GEO-28002c05","GEO-28002c06","GEO-28002w01"],
       "volume_range":"卷28",
       "attributes":{
         "borders":[
           {"direction":"东","to_place":"卫辉府获嘉县界","distance_li":240},
           {"direction":"西","to_place":"山西平阳府绛州垣曲县界","distance_li":250},
           {"direction":"南","to_place":"河南府巩县界","distance_li":70},
           {"direction":"北","to_place":"山西泽州界","distance_li":65}],
         "to_capital":[{"capital":"京师","distance_li":1800},{"capital":"南京","distance_li":1800}],
         "grain_tax":{"amount":330600,"unit":"石","note":"三十三万六百石零"},
         "jun_name":"覃怀河内",
         "topography":"地接太行南通河洛【宋志】；群山万壑环带如绣【地志】",
         "customs":"君子深思俭陋【汉书】；人性质厚多尚农事【宋志】；地险民彊多以气节相尚【地志】",
         "garrisons":[{"name":"怀庆卫","type":"卫","location_text":"在府城内东南隅洪武元年建"}],
         "fiefs":[
           {"name":"郑王府","location":"在府治东洪熙元年建"},
           {"name":"泾阳王府","location":"在府治西南景泰二年建"},
           {"name":"朝邑王府","location":"在府城内"},
           {"name":"庐江王府","location":"在府城内"},
           {"name":"繁昌王府","location":"在府城内"},
           {"name":"东垣王府","location":"在府城内"},
           {"name":"徳庆王府","location":"在府城内"}
         ]
       },
       "cit_ids":["CIT-001","CIT-002","CIT-003","CIT-004","CIT-005"]},
      {"geo_id":"GEO-28002w01","item_id":HID,"name":"怀庆卫","type":"weisuo","region":"河南","parent":HG,"children":[],"volume_range":"卷28","attributes":{"location_text":"在府城内东南隅洪武元年建"},"cit_ids":[]}
    ],
    "evos":[
      {"evo_id":"EVO-001","item_id":HID,"geo_id":HG,"dynasty":"夏","era":None,"institution_name":"覃怀","action":"因之","detail":"禹贡冀州之域，天文室壁分野，即覃怀地"},
      {"evo_id":"EVO-002","item_id":HID,"geo_id":HG,"dynasty":"周","era":None,"institution_name":"雍畿内邑","action":"因之","detail":"周为畿内邑，春秋时谓之南阳"},
      {"evo_id":"EVO-003","item_id":HID,"geo_id":HG,"dynasty":"汉","era":"高帝","institution_name":"河内郡","action":"置","detail":"汉高帝二年为河内郡，治怀县"},
      {"evo_id":"EVO-004","item_id":HID,"geo_id":HG,"dynasty":"晋","era":None,"institution_name":"河内郡","action":"因之","detail":"晋因之，后魏置怀州及河内郡"},
      {"evo_id":"EVO-005","item_id":HID,"geo_id":HG,"dynasty":"隋","era":"大业","institution_name":"河内郡","action":"改","detail":"隋初罢郡为怀州，大业初复为河内郡"},
      {"evo_id":"EVO-006","item_id":HID,"geo_id":HG,"dynasty":"唐","era":"武德","institution_name":"怀州","action":"复","detail":"唐武德初复为怀州，天宝初改为河内郡乾元初复为怀州"},
      {"evo_id":"EVO-007","item_id":HID,"geo_id":HG,"dynasty":"宋","era":"建中靖国","institution_name":"防御州","action":"升","detail":"宋为防御州，建炎后没于金"},
      {"evo_id":"EVO-008","item_id":HID,"geo_id":HG,"dynasty":"元","era":"宪宗","institution_name":"怀庆路","action":"改","detail":"元宪宗为王傅府，至元三年改怀庆路"},
      {"evo_id":"EVO-009","item_id":HID,"geo_id":HG,"dynasty":"明","era":"洪武","institution_name":"怀庆府","action":"改","detail":"本朝洪武初改怀庆府领县六"}
    ],
    "mtns":[
      {"mtn_id":"MTN-001","item_id":HID,"geo_id":HG,"name":"太行山","type":"山","location_text":"在府城北二十里","description":"一名王屋山，山有三重其路盘山而行故名太行","lore":""},
      {"mtn_id":"MTN-002","item_id":HID,"geo_id":HG,"name":"沁水","type":"河","location_text":"源出山西沁州禄山至河南武陟入河","description":"一名洎水一名沁水，汉沟洫志曰堤阔百馀里","lore":""},
      {"mtn_id":"MTN-003","item_id":HID,"geo_id":HG,"name":"济水","type":"河","location_text":"源出济源县西北王屋山","description":"详见山川志","lore":""},
      {"mtn_id":"MTN-004","item_id":HID,"geo_id":HG,"name":"黄河","type":"河","location_text":"在府城南三十里","description":"自孟津北流经温县入卫辉府界","lore":""},
      {"mtn_id":"MTN-005","item_id":HID,"geo_id":HG,"name":"尧池","type":"池","location_text":"在河内县西五里","description":"","lore":""},
      {"mtn_id":"MTN-006","item_id":HID,"geo_id":HG,"name":"猪野陂","type":"陂","location_text":"在河内县东南","description":"周回七十五里","lore":""}
    ],
    "pers":[], "sites":[],
    "prods":[
      {"prod_id":"PROD-001","item_id":HID,"geo_id":HG,"name":"牛膝","category":"药材","note":"怀庆府出"},
      {"prod_id":"PROD-002","item_id":HID,"geo_id":HG,"name":"地黄","category":"药材","note":"怀庆府出"},
      {"prod_id":"PROD-003","item_id":HID,"geo_id":HG,"name":"山药","category":"药材","note":"怀庆府出"},
      {"prod_id":"PROD-004","item_id":HID,"geo_id":HG,"name":"菊花","category":"药材","note":"怀庆府出"}
    ],
    "cits":[
      {"cit_id":"CIT-001","item_id":HID,"cited_work":"禹贡","cited_work_ent_id":"ENT-013","context":"立论","original":"【禹贡】"},
      {"cit_id":"CIT-002","item_id":HID,"cited_work":"左传","cited_work_ent_id":"ENT-014","context":"立论","original":"【左传】"},
      {"cit_id":"CIT-003","item_id":HID,"cited_work":"汉书","cited_work_ent_id":"ENT-015","context":"证俗","original":"【汉书】"},
      {"cit_id":"CIT-004","item_id":HID,"cited_work":"宋志","cited_work_ent_id":"ENT-016","context":"立论","original":"【宋志】"},
      {"cit_id":"CIT-005","item_id":HID,"cited_work":"地志","cited_work_ent_id":"ENT-017","context":"立论","original":"【地志】"}
    ]
  },
  "layer_count":7,
  "validation":{"errs":[],"gap":0,"notes":"pers和sites拆为独立文件；府级山川只留府城附近"}
}
with open(os.path.join(OUT,"28-002_怀庆府.json"),"w",encoding="utf-8") as f:
    json.dump(hq_main,f,ensure_ascii=False,indent=2)
print("怀庆 main done")

# pers split
hp = lambda pid,n,t,d,np,o,s: {"per_id":pid,"item_id":HID,"geo_id":HG,"name":n,"type":t,"dynasty":d,"native_place":np,"office":o,"summary":s}
hq_pers = [
  hp("PER-001","寇恂","名宦","汉","","河内太守","光武定河内难恂守，恂伐栗界集积糗糒以给军，执金吾贾复妄系恂，既而交欢"),
  hp("PER-002","宋果","名宦","汉","","河内令","中平初为河内令，讨捕黄巾余党不屈死之"),
  hp("PER-003","潘岳","名宦","晋","","河阳令","善为文，时山涛等皆为河阳古称多士号河阳一县花"),
  hp("PER-004","房玄龄","名宦","唐","","考功郎中","补隰城尉久之，补秦王府记室封邗国公，薨陪葬昭陵"),
  hp("PER-005","张弘略","名宦","元","","怀孟路总管","至元中为总管，开大冶冶铁作以足用，后赐都尉追封蔡国公谥忠毅"),
  hp("PER-006","塔不台","名宦","元","","怀庆路万户","讨贼，贼援兵四合力战死之"),
  hp("PER-007","徐义","名宦","明","","怀庆知府","洪武初为政严明吏民畏服，创建庙学兴举废坠"),
  hp("PER-008","史仲成","名宦","明","","河内知县","洪武初辟举授河内知县，廉公有威吏民畏服，后以忧去服阕复授本县致仕"),
  hp("PER-009","许懋","名宦","明","","温县知县","永乐间温县知县，卒于官，民思慕之如失怙恃"),
  hp("PER-010","朱廷立","名宦","明","","怀庆知府","嘉靖间以御史知府事，政尚明恕抚字为心，士民德之，累升兵部右侍郎"),
  hp("PER-011","汉高帝刘邦","人物","汉","丰","汉高祖","为沛公时徇河内，后即皇帝位置河内郡"),
  hp("PER-012","司马懿","人物","三国","温县","宣帝","仕魏为丞相，封晋王，孙炎受魏禅是为晋武帝追尊宣帝"),
  hp("PER-013","山涛","人物","晋","怀县","司徒","早孤居贫，为吏部尚书选举颇得人，甚有时誉"),
  hp("PER-014","向秀","人物","晋","怀县","黄门侍郎","清悟有远识，少为山涛所知，雅好老庄之学"),
  hp("PER-015","何曾","人物","晋","阳武","太尉","父夔魏太仆阳武亭侯，曾嗣位，晋武受禅拜太尉封郎陵公"),
  hp("PER-016","潘岳","人物","晋","中牟","黄门侍郎","总角辨惠摛藻清艳，乡邑号奇童，仕终给事黄门侍郎"),
  hp("PER-017","李固","人物","汉","平阴","太尉","司徒郃长子，有异鼎器，及在公台正色廉白，为梁冀所疾竟被害"),
  hp("PER-018","潘尼","人物","晋","中牟","太常卿","岳之从子，性静退不好荣利，著书而尚清谈，终太常卿"),
  hp("PER-019","宇文庆","人物","隋","安义","大将军","周初从军征讨，武帝时以功位上大将军，隋文帝受禅拜左武卫将军"),
  hp("PER-020","薛收","人物","唐","河内","学士","年十二能属文，由文学馆直学士尝上书谏猎，帝手诏答"),
  hp("PER-021","李商隐","人物","唐","河内","检校工部员外郎","文思清丽，武宗时举进士，累官检校工部员外郎"),
  hp("PER-022","许衡","人物","元","河内","集贤大学士","入本国子祭酒，教成追封魏国公谥文正"),
  hp("PER-023","许师敬","人物","元","河内","御史中丞","衡之子，以父荫入仕泰，定中由治书侍御史升御史中丞"),
  hp("PER-024","逯鲁曾","人物","元","修武","翰林侍制","元统中举进士授翰林国史院编修官，累迁至宣文阁授经郎"),
  hp("PER-025","何瑭","人物","明","武陟","礼部右侍郎","正德辛未进士授翰林修撰，抗疏劾刘瑾瑾衔之谪为官，瑾诛起升礼部右侍郎，著有柏斋文集"),
  hp("PER-026","张英","列女","元","孟州","潘珪妻","至正末明兵至英抱子卧楼上，兵胁之上楼即投楼下死，获免子男一人"),
  hp("PER-027","秦氏","列女","明","河内","陈谂妻","年十八归谂，三载谂卒，秦方娠，及生男恩育教诲成立，守节五十余年卒")
]
pf = {"item_id":HID,"volume":"28","source":"怀庆府-人物层","region":"河南",
  "layers":{"ents":[],"geos":[],"evos":[],"mtns":[],"pers":hq_pers,"sites":[],"prods":[],"cits":[]},
  "layer_count":7,"validation":{"errs":[],"gap":0,"notes":""}}
with open(os.path.join(OUT,"28-002_怀庆府_pers.json"),"w",encoding="utf-8") as f:
    json.dump(pf,f,ensure_ascii=False,indent=2)
print("pers done")

# sites split
hs = lambda sid,n,t,l,h: {"site_id":sid,"item_id":HID,"geo_id":HG,"name":n,"type":t,"location_text":l,"history_lore":h}
hq_sites = [
  hs("SITE-001","怀庆府学","学校","在府治东","宋天圣三年建，本朝洪武三年重修"),
  hs("SITE-002","天宁寺","寺观","在府治北","唐建本朝洪武初重修"),
  hs("SITE-003","济渎庙","祠庙","在济源县东","祀济渎神，其泉自王屋山发源至此，宋崇宁初封清源忠护王"),
  hs("SITE-004","汉献帝陵","陵墓","在修武县北","东汉末帝陵"),
  hs("SITE-005","司马懿墓","陵墓","在温县","晋宣帝墓"),
  hs("SITE-006","王屋山","古迹","在济源县","愚公移山处"),
  hs("SITE-007","河阳城","古迹","在孟县","古孟津渡口")
]
sf = {"item_id":HID,"volume":"28","source":"怀庆府-寺观祠庙古迹","region":"河南",
  "layers":{"ents":[],"geos":[],"evos":[],"mtns":[],"pers":[],"sites":hq_sites,"prods":[],"cits":[]},
  "layer_count":7,"validation":{"errs":[],"gap":0,"notes":""}}
with open(os.path.join(OUT,"28-002_怀庆府_sites.json"),"w",encoding="utf-8") as f:
    json.dump(sf,f,ensure_ascii=False,indent=2)
print("sites done")

# county files
def cty(cid,name,loc,hh_note,hh_count,evos,mtns=None,sites=None):
    return {"item_id":HID,"volume":"28","source":name,"region":"河南","type":"county",
      "original":f"{name}【{loc}编户{hh_note}】",
      "layers":{"ents":[{"ent_id":"ENT-001","name":name,"type":"geo","norm":name,"first_source":HID}],
        "geos":[{"geo_id":f"GEO-28002{cid}","item_id":HID,"name":name,"type":"county","region":"河南","parent":HG,"children":[],"volume_range":"卷28","attributes":{"location_text":loc,"households":{"count":hh_count,"unit":"里","note":f"编户{hh_note}"}},"cit_ids":[]}],
        "evos":evos,"mtns":mtns or [],"pers":[],"sites":sites or [],"prods":[],"cits":[]},
      "layer_count":7,"validation":{"errs":[],"gap":0,"notes":""}}

c1 = cty("c01","河内县","附郭","二十里",20,[
  {"evo_id":"EVO-001","item_id":HID,"geo_id":"GEO-28002c01","dynasty":"周","era":None,"institution_name":"野王邑","action":"因之","detail":"本周野王邑"},
  {"evo_id":"EVO-002","item_id":HID,"geo_id":"GEO-28002c01","dynasty":"秦","era":None,"institution_name":"野王县","action":"置","detail":"秦置野王县属河内郡"},
  {"evo_id":"EVO-003","item_id":HID,"geo_id":"GEO-28002c01","dynasty":"隋","era":"开皇","institution_name":"河内县","action":"改","detail":"隋开皇初始改河内县为怀州治"},
  {"evo_id":"EVO-004","item_id":HID,"geo_id":"GEO-28002c01","dynasty":"明","era":None,"institution_name":"河内县","action":"因之","detail":"唐宋元仍旧本朝因之"}])
# fix the dict syntax issue
c1["layers"]["evos"][0]["institution_name"] = "野王邑"
with open(os.path.join(OUT,"28-002_c01_河内县.json"),"w",encoding="utf-8") as f: json.dump(c1,f,ensure_ascii=False,indent=2)

c2 = cty("c02","济源县","在府城西北一百二十里","二十里",20,[
  {"evo_id":"EVO-001","item_id":HID,"geo_id":"GEO-28002c02","dynasty":"周","era":None,"institution_name":"原邑","action":"因之","detail":"本周原邑"},
  {"evo_id":"EVO-002","item_id":HID,"geo_id":"GEO-28002c02","dynasty":"隋","era":"开皇","institution_name":"济源县","action":"置","detail":"隋开皇十年析轵县北置济源县因济水发源为名"},
  {"evo_id":"EVO-003","item_id":HID,"geo_id":"GEO-28002c02","dynasty":"元","era":"太宗","institution_name":"原州","action":"升","detail":"元太宗时升为原州，后仍为县"},
  {"evo_id":"EVO-004","item_id":HID,"geo_id":"GEO-28002c02","dynasty":"明","era":None,"institution_name":"济源县","action":"因之","detail":"本朝因之"}],
  mtns=[{"mtn_id":"MTN-001","item_id":HID,"geo_id":"GEO-28002c02","name":"王屋山","type":"山","location_text":"在济源县西八十里","description":"山有三重其路盘山而行，愚公移山即此","lore":""}])
with open(os.path.join(OUT,"28-002_c02_济源县.json"),"w",encoding="utf-8") as f: json.dump(c2,f,ensure_ascii=False,indent=2)

c3 = cty("c03","修武县","在府城东南六十里","一十四里",14,[
  {"evo_id":"EVO-001","item_id":HID,"geo_id":"GEO-28002c03","dynasty":"周","era":None,"institution_name":"宁邑","action":"因之","detail":"本周之宁邑"},
  {"evo_id":"EVO-002","item_id":HID,"geo_id":"GEO-28002c03","dynasty":"秦","era":"始皇","institution_name":"修武","action":"改","detail":"秦始皇改修武属三川郡"},
  {"evo_id":"EVO-003","item_id":HID,"geo_id":"GEO-28002c03","dynasty":"晋","era":"启宁","institution_name":"修武县","action":"置","detail":"晋启宁时改置修武县属河内郡"},
  {"evo_id":"EVO-004","item_id":HID,"geo_id":"GEO-28002c03","dynasty":"明","era":None,"institution_name":"修武县","action":"因之","detail":"唐宋元仍旧本朝因之"}])
# fix syntax
c3["layers"]["evos"][0]["detail"] = "本周之宁邑"
with open(os.path.join(OUT,"28-002_c03_修武县.json"),"w",encoding="utf-8") as f: json.dump(c3,f,ensure_ascii=False,indent=2)

c4 = cty("c04","武陟县","在府城东南一百里","一十四里",14,[
  {"evo_id":"EVO-001","item_id":HID,"geo_id":"GEO-28002c04","dynasty":"汉","era":"","institution_name":"怀县地","action":"因之","detail":"本汉怀县地"},
  {"evo_id":"EVO-002","item_id":HID,"geo_id":"GEO-28002c04","dynasty":"隋","era":"开皇","institution_name":"武陟县","action":"置","detail":"隋开皇六年分修武县地置武陟县"}])
c4["layers"]["evos"][0]["era"] = None
with open(os.path.join(OUT,"28-002_c04_武陟县.json"),"w",encoding="utf-8") as f: json.dump(c4,f,ensure_ascii=False,indent=2)

c5 = cty("c05","孟县","在府城南八十里","一十七里",17,[
  {"evo_id":"EVO-001","item_id":HID,"geo_id":"GEO-28002c05","dynasty":"周","era":None,"institution_name":"孟津","action":"因之","detail":"本周之孟津"},
  {"evo_id":"EVO-002","item_id":HID,"geo_id":"GEO-28002c05","dynasty":"晋","era":None,"institution_name":"河阳郡","action":"置","detail":"晋咸宁中置河阳郡"},
  {"evo_id":"EVO-003","item_id":HID,"geo_id":"GEO-28002c05","dynasty":"唐","era":"武德","institution_name":"孟州","action":"置","detail":"唐武德初置孟州，金以河阳县省入州"},
  {"evo_id":"EVO-004","item_id":HID,"geo_id":"GEO-28002c05","dynasty":"明","era":"洪武","institution_name":"孟县","action":"降","detail":"本朝洪武十年仍降为县，编户一十七里"}])
c5["layers"]["evos"][1]["era"] = None
with open(os.path.join(OUT,"28-002_c05_孟县.json"),"w",encoding="utf-8") as f: json.dump(c5,f,ensure_ascii=False,indent=2)

c6 = cty("c06","温县","在府城东南八十里","九七里",7,[
  {"evo_id":"EVO-001","item_id":HID,"geo_id":"GEO-28002c06","dynasty":"周","era":"","institution_name":"温邑","action":"置","detail":"本周畿内温邑"}
,
  {"evo_id":"EVO-002","item_id":HID,"geo_id":"GEO-28002c06","dynasty":"汉","era":"","institution_name":"温县","action":"置","detail":"汉置温县属河内郡"},
  {"evo_id":"EVO-003","item_id":HID,"geo_id":"GEO-28002c06","dynasty":"明","era":"","institution_name":"温县","action":"因之","detail":"后魏及唐宋皆仍旧本朝因之"}])
for i in range(3):
    c6["layers"]["evos"][i]["era"] = None
with open(os.path.join(OUT,"28-002_c06_温县.json"),"w",encoding="utf-8") as f: json.dump(c6,f,ensure_ascii=False,indent=2)

print("怀庆府 all done!")

