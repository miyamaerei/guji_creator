# -*- coding: utf-8 -*-
"""Generate 彰德府 county/subprefecture files."""
import json, os
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol27"
IID = "27-002"

def cty(cid, name, parent, loc, hh_note, hh_count, evos, mtns=None, sites=None):
    return {
      "item_id": IID, "volume": "27", "source": name, "region": "河南", "type": "county",
      "original": f"{name}【{loc}编户{hh_note}】",
      "layers": {
        "ents": [{"ent_id":"ENT-001","name":name,"type":"geo","norm":name,"first_source":IID}],
        "geos": [{"geo_id":f"GEO-27002{cid}","item_id":IID,"name":name,"type":"county","region":"河南","parent":parent,"children":[],"volume_range":"卷27","attributes":{"location_text":loc,"households":{"count":hh_count,"unit":"里","note":f"编户{hh_note}"}},"cit_ids":[]}],
        "evos": evos, "mtns": mtns or [], "pers": [], "sites": sites or [], "prods": [], "cits": []
      },
      "layer_count": 7, "validation": {"errs":[],"gap":0,"notes":""}
    }

# c01 安阳县
ay = cty("c01","安阳县","GEO-27002","附郭","八十四里",84,[
  {"evo_id":"EVO-001","item_id":IID,"geo_id":"GEO-27002c01","dynasty":"商","era":None,"institution_name":"相","action":"因之","detail":"本纣都之地，左传茀阳即此地"},
  {"evo_id":"EVO-002","item_id":IID,"geo_id":"GEO-27002c01","dynasty":"战国","era":None,"institution_name":"宁新中邑","action":"置","detail":"战国为魏宁新中邑，秦更名安阳"},
  {"evo_id":"EVO-003","item_id":IID,"geo_id":"GEO-27002c01","dynasty":"晋","era":None,"institution_name":"安阳县","action":"置","detail":"汉省入荡阴县，晋始置安阳县"},
  {"evo_id":"EVO-004","item_id":IID,"geo_id":"GEO-27002c01","dynasty":"后周","era":None,"institution_name":"安阳县","action":"迁","detail":"后周自古邺城移相州治此，隋唐宋皆仍旧"},
  {"evo_id":"EVO-005","item_id":IID,"geo_id":"GEO-27002c01","dynasty":"明","era":None,"institution_name":"安阳县","action":"因之","detail":"本朝因之"}
],
mtns=[
  {"mtn_id":"MTN-001","item_id":IID,"geo_id":"GEO-27002c01","name":"韩陵山","type":"山","location_text":"在府城东北一十七里","description":"东魏高欢破尔朱荣于此","lore":""},
  {"mtn_id":"MTN-002","item_id":IID,"geo_id":"GEO-27002c01","name":"安阳河","type":"河","location_text":"一名洹水","description":"东经永和镇入卫河","lore":""},
],
sites=[
  {"site_id":"SITE-001","item_id":IID,"geo_id":"GEO-27002c01","name":"安阳县学","type":"学校","location_text":"在县治西北","history_lore":"元至元间建"},
])
with open(os.path.join(OUT,"27-002_c01_安阳县.json"),"w",encoding="utf-8") as f: json.dump(ay,f,ensure_ascii=False,indent=2)
print("c01 done")

# c02 汤阴县
ty = cty("c02","汤阴县","GEO-27002","在府城南四十五里","四十一里",41,[
  {"evo_id":"EVO-001","item_id":IID,"geo_id":"GEO-27002c02","dynasty":"周","era":None,"institution_name":"羑里","action":"因之","detail":"古羑里地，战国为魏荡阴地"},
  {"evo_id":"EVO-002","item_id":IID,"geo_id":"GEO-27002c02","dynasty":"汉","era":None,"institution_name":"荡阴县","action":"置","detail":"汉置荡阴县属河内郡，后魏省"},
  {"evo_id":"EVO-003","item_id":IID,"geo_id":"GEO-27002c02","dynasty":"隋","era":None,"institution_name":"汤阴县","action":"置","detail":"隋于县东十七里置汤阴县属汲郡，寻省入安阳后复分置汤源县"},
  {"evo_id":"EVO-004","item_id":IID,"geo_id":"GEO-27002c02","dynasty":"唐","era":"贞观","institution_name":"汤阴县","action":"改","detail":"唐初复置汤源县，贞观初改汤阴县属相州，金属彰德府元不改"},
  {"evo_id":"EVO-005","item_id":IID,"geo_id":"GEO-27002c02","dynasty":"明","era":None,"institution_name":"汤阴县","action":"因之","detail":"本朝因之"}
],
mtns=[
  {"mtn_id":"MTN-001","item_id":IID,"geo_id":"GEO-27002c02","name":"飞凤山","type":"山","location_text":"在汤阴县西三里","description":"以形似名","lore":""},
  {"mtn_id":"MTN-002","item_id":IID,"geo_id":"GEO-27002c02","name":"羑水","type":"河","location_text":"源出汤阴县西北鹤山","description":"流至羑城北会防水入汤水","lore":""},
],
sites=[
  {"site_id":"SITE-001","item_id":IID,"geo_id":"GEO-27002c02","name":"汤阴县学","type":"学校","location_text":"在县治东南","history_lore":"宋大观元年建，本朝洪武三年重建"},
  {"site_id":"SITE-002","item_id":IID,"geo_id":"GEO-27002c02","name":"文王庙","type":"祠庙","location_text":"在汤阴县北一十里","history_lore":"商纣囚文王于羑里，庙后方城即羑里也"},
])
with open(os.path.join(OUT,"27-002_c02_汤阴县.json"),"w",encoding="utf-8") as f: json.dump(ty,f,ensure_ascii=False,indent=2)
print("c02 done")

# c03 临漳县
lz = cty("c03","临漳县","GEO-27002","在府城东北一百一十里","三十六里",36,[
  {"evo_id":"EVO-001","item_id":IID,"geo_id":"GEO-27002c03","dynasty":"战国","era":None,"institution_name":"邺地","action":"因之","detail":"本邺地，魏文侯始封于此"},
  {"evo_id":"EVO-002","item_id":IID,"geo_id":"GEO-27002c03","dynasty":"汉","era":None,"institution_name":"魏郡地","action":"因之","detail":"汉属魏郡，东汉末魏公曹操居此"},
  {"evo_id":"EVO-003","item_id":IID,"geo_id":"GEO-27002c03","dynasty":"晋","era":None,"institution_name":"临漳县","action":"置","detail":"晋始改为临漳县，东魏复增置邺县"},
  {"evo_id":"EVO-004","item_id":IID,"geo_id":"GEO-27002c03","dynasty":"隋","era":None,"institution_name":"灵芝县","action":"改","detail":"后周移临漳治于城东二十里，隋改为灵芝县俄复旧"},
  {"evo_id":"EVO-005","item_id":IID,"geo_id":"GEO-27002c03","dynasty":"宋","era":None,"institution_name":"临漳县","action":"因之","detail":"宋省邺县入焉，金元仍旧本朝因之"}
],
sites=[
  {"site_id":"SITE-001","item_id":IID,"geo_id":"GEO-27002c03","name":"临漳县学","type":"学校","location_text":"在县治西","history_lore":"旧在县治东洪武十八年沦于河，二十七年徙建于此"},
  {"site_id":"SITE-002","item_id":IID,"geo_id":"GEO-27002c03","name":"铜雀台","古迹","location_text":"在临漳县治西","history_lore":"魏曹操筑，并金虎冰井三台相去各六十步"},
  {"site_id":"SITE-003","item_id":IID,"geo_id":"GEO-27002c03","name":"邺城","古迹","location_text":"在临漳县西二十里","history_lore":"三国魏后赵前燕东魏皆都于此"},
])
with open(os.path.join(OUT,"27-002_c03_临漳县.json"),"w",encoding="utf-8") as f: json.dump(lz,f,ensure_ascii=False,indent=2)
print("c03 done")

# c04 林县
lx = cty("c04","林县","GEO-27002","在府城西一百二十里","三十五里",35,[
  {"evo_id":"EVO-001","item_id":IID,"geo_id":"GEO-27002c04","dynasty":"汉","era":None,"institution_name":"隆虑县","action":"置","detail":"本汉隆虑县属河内郡"},
  {"evo_id":"EVO-002","item_id":IID,"geo_id":"GEO-27002c04","dynasty":"后汉","era":None,"institution_name":"林虑县","action":"改","detail":"后汉改林虑县，三国魏属朝歌郡，晋属汲郡"},
  {"evo_id":"EVO-003","item_id":IID,"geo_id":"GEO-27002c04","dynasty":"隋","era":None,"institution_name":"岩州县","action":"置","detail":"后魏复置兼置林虑郡，隋罢郡置岩州县仍旧"},
  {"evo_id":"EVO-004","item_id":IID,"geo_id":"GEO-27002c04","dynasty":"金","era":None,"institution_name":"林州","action":"升","detail":"唐初复置岩州寻罢，宋因之，金升为林州元因之"},
  {"evo_id":"EVO-005","item_id":IID,"geo_id":"GEO-27002c04","dynasty":"明","era":"洪武","institution_name":"林县","action":"降","detail":"本朝洪武三年降为县"}
],
mtns=[
  {"mtn_id":"MTN-001","item_id":IID,"geo_id":"GEO-27002c04","name":"太行山","type":"山","location_text":"在林县西二十里","description":"群山一带形势崔嵬，其在本府界者绵亘二百里总曰太行","lore":""},
  {"mtn_id":"MTN-002","item_id":IID,"geo_id":"GEO-27002c04","name":"黄华山","type":"山","location_text":"在林县西二十里一名林虑山","description":"山有三峰名仙人楼玉女台，北岩出瀑布","lore":"金王庭筠尝隐居于此"},
  {"mtn_id":"MTN-003","item_id":IID,"geo_id":"GEO-27002c04","name":"天平山","type":"山","location_text":"在林县西南三十里","description":"山势平坦有滴乳泉沿石而下如滴乳然","lore":""},
],
sites=[
  {"site_id":"SITE-001","item_id":IID,"geo_id":"GEO-27002c04","name":"林县学","type":"学校","location_text":"在县治东","history_lore":"元至元间建，本朝洪武七年重建"},
])
with open(os.path.join(OUT,"27-002_c04_林县.json"),"w",encoding="utf-8") as f: json.dump(lx,f,ensure_ascii=False,indent=2)
print("c04 done")

# s01 磁州
cz = {
  "item_id":IID,"volume":"27","source":"磁州","region":"河南","type":"subprefecture",
  "original":"磁州【在府城北七十里本秦邯郸郡地汉为魏郡武安县地后魏析置临水县后周割临水置滏阳县及成安郡隋罢郡于滏阳置磁州后罢唐改为惠州后复为磁州宋以昭义县省入滏阳元初升为滏源军节度属广平路后复为磁州本朝并省滏阳县入焉及改今属编户四十一里领县二】",
  "layers":{
    "ents":[{"ent_id":"ENT-001","name":"磁州","type":"geo","norm":"磁州","first_source":IID}],
    "geos":[{"geo_id":"GEO-27002s01","item_id":IID,"name":"磁州","type":"subprefecture","region":"河南","parent":"GEO-27002","children":["GEO-27002c05","GEO-27002c06"],"volume_range":"卷27","attributes":{"location_text":"在府城北七十里","households":{"count":41,"unit":"里","note":"编户四十一里"}},"cit_ids":[]}],
    "evos":[
      {"evo_id":"EVO-001","item_id":IID,"geo_id":"GEO-27002s01","dynasty":"秦","era":None,"institution_name":"邯郸郡地","action":"因之","detail":"本秦邯郸郡地，汉为魏郡武安县地"},
      {"evo_id":"EVO-002","item_id":IID,"geo_id":"GEO-27002s01","dynasty":"后魏","era":None,"institution_name":"临水县","action":"置","detail":"后魏析置临水县"},
      {"evo_id":"EVO-003","item_id":IID,"geo_id":"GEO-27002s01","dynasty":"隋","era":None,"institution_name":"磁州","action":"置","detail":"后周割临水置滏阳县及成安郡，隋罢郡于滏阳置磁州后罢"},
      {"evo_id":"EVO-004","item_id":IID,"geo_id":"GEO-27002s01","dynasty":"唐","era":None,"institution_name":"惠州","action":"改","detail":"唐改为惠州后复为磁州"},
      {"evo_id":"EVO-005","item_id":IID,"geo_id":"GEO-27002s01","dynasty":"明","era":None,"institution_name":"磁州","action":"因之","detail":"本朝并省滏阳县入焉，改今属领县二"}
    ],
    "mtns":[
      {"mtn_id":"MTN-001","item_id":IID,"geo_id":"GEO-27002s01","name":"贺兰山","type":"山","location_text":"在磁州城西北四十里","description":"相传昔宋贺兰真人尝居此","lore":""},
      {"mtn_id":"MTN-002","item_id":IID,"geo_id":"GEO-27002s01","name":"滏水","type":"河","location_text":"源出磁州西北神麋山","description":"涌沸如汤出滏东流至临漳县界入漳河","lore":""},
    ],
    "pers":[],"sites":[
      {"site_id":"SITE-001","item_id":IID,"geo_id":"GEO-27002s01","name":"磁州学","type":"学校","location_text":"在州治东","history_lore":"洪武五年建正统十四年重建"},
    ],
    "prods":[],"cits":[]
  },
  "layer_count":7,"validation":{"errs":[],"gap":0,"notes":""}
}
with open(os.path.join(OUT,"27-002_s01_磁州.json"),"w",encoding="utf-8") as f: json.dump(cz,f,ensure_ascii=False,indent=2)
print("s01 done")

# c05 武安县 (under 磁州)
wa = cty("c05","武安县","GEO-27002s01","在州城北一百二十里","三十四里",34,[
  {"evo_id":"EVO-001","item_id":IID,"geo_id":"GEO-27002c05","dynasty":"汉","era":None,"institution_name":"武安县","action":"置","detail":"汉置属魏郡，曹魏属广平郡"},
  {"evo_id":"EVO-002","item_id":IID,"geo_id":"GEO-27002c05","dynasty":"隋","era":None,"institution_name":"武安郡","action":"因之","detail":"隋属武安郡，唐初属洺州后改属磁州"},
  {"evo_id":"EVO-003","item_id":IID,"geo_id":"GEO-27002c05","dynasty":"元","era":None,"institution_name":"武安县","action":"复","detail":"元初省入邯郸县寻复置，本朝因之"}
],
mtns=[
  {"mtn_id":"MTN-001","item_id":IID,"geo_id":"GEO-27002c05","name":"粟山","type":"山","location_text":"在武安县东南一十二里","description":"相传秦白起拒赵廉颇于此，赵将绝粮起命将士以布囊盛积至山巅","lore":""},
  {"mtn_id":"MTN-002","item_id":"IID","geo_id":"GEO-27002c05","name":"鼓山","type":"山","location_text":"在武安县南二十里一名滏山","description":"有二石如鼓南北相当，邺城西有石鼓鸣则兵起","lore":""},
])
with open(os.path.join(OUT,"27-002_c05_武安县.json"),"w",encoding="utf-8") as f: json.dump(wa,f,ensure_ascii=False,indent=2)
print("c05 done")

# c06 涉县 (under 磁州)
sx = cty("c06","涉县","GEO-27002s01","在州城西二百里","一十八里",18,[
  {"evo_id":"EVO-001","item_id":IID,"geo_id":"GEO-27002c06","dynasty":"周","era":None,"institution_name":"沙侯国","action":"置","detail":"古沙侯国地"},
  {"evo_id":"EVO-002","item_id":IID,"geo_id":"GEO-27002c06","dynasty":"汉","era":None,"institution_name":"涉县","action":"置","detail":"汉置沙县，后因漳水人民徒涉遂名涉县属魏郡"},
  {"evo_id":"EVO-003","item_id":IID,"geo_id":"GEO-27002c06","dynasty":"隋","era":None,"institution_name":"涉县","action":"复","detail":"后魏并入临水县，后周移临水县治涉城，隋复于涉城置涉县隶韩州"},
  {"evo_id":"EVO-004","item_id":IID,"geo_id":"GEO-27002c06","dynasty":"金","era":None,"institution_name":"崇州","action":"升","detail":"宋仍旧金升为崇州，元罢州复置县属真定路"},
  {"evo_id":"EVO-005","item_id":IID,"geo_id":"GEO-27002c06","dynasty":"明","era":None,"institution_name":"涉县","action":"因之","detail":"本朝改隶磁州"}
],
sites=[
  {"site_id":"SITE-001","item_id":IID,"geo_id":"GEO-27002c06","name":"涉县学","type":"学校","location_text":"在县治西南","history_lore":"洪武三年建"},
])
with open(os.path.join(OUT,"27-002_c06_涉县.json"),"w",encoding="utf-8") as f: json.dump(sx,f,ensure_ascii=False,indent=2)
print("c06 done")
print("彰德府 all done!")
