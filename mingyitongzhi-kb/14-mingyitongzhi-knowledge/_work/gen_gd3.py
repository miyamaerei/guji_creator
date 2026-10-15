# -*- coding: utf-8 -*-
"""Generate 归德府 county/subprefecture files."""
import json, os

OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol27"

def county_file(cid, name, parent_geo, loc, households_note, households_count, evos, mtns=None, sites=None, pers=None):
    f = {
      "item_id": "27-001", "volume": "27", "source": name, "region": "河南", "type": "county",
      "original": f"{name}【{loc}编户{households_note}】",
      "layers": {
        "ents": [{"ent_id":"ENT-001","name":name,"type":"geo","norm":name,"first_source":"27-001"}],
        "geos": [{
          "geo_id": f"GEO-27001{cid}", "item_id": "27-001", "name": name, "type": "county",
          "region": "河南", "parent": parent_geo, "children": [], "volume_range": "卷27",
          "attributes": {"location_text": loc, "households": {"count": households_count, "unit": "里", "note": f"编户{households_note}"}},
          "cit_ids": []
        }],
        "evos": evos,
        "mtns": mtns or [],
        "pers": pers or [],
        "sites": sites or [],
        "prods": [],
        "cits": []
      },
      "layer_count": 7,
      "validation": {"errs": [], "gap": 0, "notes": ""}
    }
    return f

# ---- c01 商丘县 ----
sq = county_file("c01", "商丘县", "GEO-27001",
  "附郭", "二十七里", 27,
  [
    {"evo_id":"EVO-001","item_id":"27-001","geo_id":"GEO-27001c01","dynasty":"夏","era":None,"institution_name":"商丘","action":"置","detail":"本高辛氏子阏伯所居商丘也，相土代之继主火祀"},
    {"evo_id":"EVO-002","item_id":"27-001","geo_id":"GEO-27001c01","dynasty":"秦","era":None,"institution_name":"砀郡地","action":"因之","detail":"秦为砀郡地"},
    {"evo_id":"EVO-003","item_id":"27-001","geo_id":"GEO-27001c01","dynasty":"汉","era":None,"institution_name":"睢阳县","action":"置","detail":"汉置睢阳县属梁国，后汉魏晋俱因之"},
    {"evo_id":"EVO-004","item_id":"27-001","geo_id":"GEO-27001c01","dynasty":"隋","era":"开皇","institution_name":"宋城县","action":"改","detail":"隋开皇初改郡曰宋州改县曰宋城"},
    {"evo_id":"EVO-005","item_id":"27-001","geo_id":"GEO-27001c01","dynasty":"金","era":None,"institution_name":"睢阳县","action":"改","detail":"金为睢阳县，元以姑熟县省入"},
    {"evo_id":"EVO-006","item_id":"27-001","geo_id":"GEO-27001c01","dynasty":"明","era":"嘉靖","institution_name":"商丘县","action":"置","detail":"本朝洪武初降归德府为州省睢阳县，嘉靖二十四年升州为府置商丘县"}
  ],
  mtns=[
    {"mtn_id":"MTN-001","item_id":"27-001","geo_id":"GEO-27001c01","name":"幸山","type":"山","location_text":"在府城南三里","description":"宋高宗即皇帝位于此","lore":""},
    {"mtn_id":"MTN-002","item_id":"27-001","geo_id":"GEO-27001c01","name":"南湖","type":"湖","location_text":"在府城南五里","description":"宋晏元献放驯鹭于湖中","lore":"苏辙有记"},
  ],
  sites=[
    {"site_id":"SITE-001","item_id":"27-001","geo_id":"GEO-27001c01","name":"商丘县学","type":"学校","location_text":"在县治","history_lore":"附郭府学同城"},
  ]
)
with open(os.path.join(OUT,"27-001_c01_商丘县.json"),"w",encoding="utf-8") as f:
    json.dump(sq,f,ensure_ascii=False,indent=2)
print("c01 done")

# ---- c02 宁陵县 ----
nl = county_file("c02", "宁陵县", "GEO-27001",
  "在府城西六十里", "七里", 7,
  [
    {"evo_id":"EVO-001","item_id":"27-001","geo_id":"GEO-27001c02","dynasty":"周","era":None,"institution_name":"葛伯国","action":"置","detail":"本古葛伯国又为甯城，春秋时宋地"},
    {"evo_id":"EVO-002","item_id":"27-001","geo_id":"GEO-27001c02","dynasty":"汉","era":"元狩","institution_name":"宁陵县","action":"置","detail":"汉元狩初置宁陵县属陈留郡，后属梁国"},
    {"evo_id":"EVO-003","item_id":"27-001","geo_id":"GEO-27001c02","dynasty":"北齐","era":None,"institution_name":"废","action":"废","detail":"北齐废"},
    {"evo_id":"EVO-004","item_id":"27-001","geo_id":"GEO-27001c02","dynasty":"隋","era":None,"institution_name":"宁陵县","action":"复","detail":"隋复置属宋州，唐因之"},
    {"evo_id":"EVO-005","item_id":"27-001","geo_id":"GEO-27001c02","dynasty":"明","era":None,"institution_name":"宁陵县","action":"因之","detail":"宋属拱州后属应天府，金属归德府元仍旧，本朝因之"}
  ],
  mtns=[
    {"mtn_id":"MTN-001","item_id":"27-001","geo_id":"GEO-27001c02","name":"甘露岭","type":"岭","location_text":"在宁陵县西五里","description":"隋文帝幸岱至此甘露降因名","lore":""},
    {"mtn_id":"MTN-002","item_id":"27-001","geo_id":"GEO-27001c02","name":"圣水井","type":"井","location_text":"在宁陵县长乐乡","description":"","lore":""},
    {"mtn_id":"MTN-003","item_id":"27-001","geo_id":"GEO-27001c02","name":"黄龙井","type":"井","location_text":"在宁陵县东界","description":"甘露四年双龙见井中","lore":""},
  ],
  sites=[
    {"site_id":"SITE-001","item_id":"27-001","geo_id":"GEO-27001c02","name":"宁陵县学","type":"学校","location_text":"在县治后","history_lore":"旧在县治西南洪武三年建，成化十四年圮于水改建于此"},
  ]
)
with open(os.path.join(OUT,"27-001_c02_宁陵县.json"),"w",encoding="utf-8") as f:
    json.dump(nl,f,ensure_ascii=False,indent=2)
print("c02 done")

# ---- c03 鹿邑县 ----
ly = county_file("c03", "鹿邑县", "GEO-27001",
  "在府城南一百二十里", "三十四里", 34,
  [
    {"evo_id":"EVO-001","item_id":"27-001","geo_id":"GEO-27001c03","dynasty":"春秋","era":None,"institution_name":"鸣鹿","action":"置","detail":"春秋晋邑本曰鸣鹿，左传诸侯侵陈至于鸣鹿即此"},
    {"evo_id":"EVO-002","item_id":"27-001","geo_id":"GEO-27001c03","dynasty":"汉","era":None,"institution_name":"武平县","action":"置","detail":"汉为郸县地属沛郡，东汉析置武平县属陈国"},
    {"evo_id":"EVO-003","item_id":"27-001","geo_id":"GEO-27001c03","dynasty":"隋","era":None,"institution_name":"鹿邑县","action":"改","detail":"隋始改鹿邑县属陈州，唐属亳州，宋金元仍旧"},
    {"evo_id":"EVO-004","item_id":"27-001","geo_id":"GEO-27001c03","dynasty":"明","era":None,"institution_name":"鹿邑县","action":"因之","detail":"本朝改今属"}
  ],
  mtns=[
    {"mtn_id":"MTN-001","item_id":"27-001","geo_id":"GEO-27001c03","name":"阴灵山","type":"山","location_text":"在鹿邑县一十一里","description":"","lore":""},
    {"mtn_id":"MTN-002","item_id":"27-001","geo_id":"GEO-27001c03","name":"隐山","type":"山","location_text":"在鹿邑县东一十三里","description":"与阴灵山对峙，世传陈抟炼丹之处","lore":""},
    {"mtn_id":"MTN-003","item_id":"27-001","geo_id":"GEO-27001c03","name":"九龙井","type":"井","location_text":"在鹿邑县东皋乡太清宫","description":"世传老子诞生九龙吐水","lore":"今太极殿有井存焉"},
    {"mtn_id":"MTN-004","item_id":"27-001","geo_id":"GEO-27001c03","name":"灵溪池","type":"池","location_text":"在鹿邑县太清宫前","description":"世传九龙吐水浴老子池也","lore":""},
  ],
  sites=[
    {"site_id":"SITE-001","item_id":"27-001","geo_id":"GEO-27001c03","name":"鹿邑县学","type":"学校","location_text":"在县治东","history_lore":"洪武三年建嘉靖初重修"},
    {"site_id":"SITE-002","item_id":"27-001","geo_id":"GEO-27001c03","name":"太清宫","type":"寺观","location_text":"在鹿邑县东一十里","history_lore":"唐建初名明道宫，宋改今名"},
  ]
)
with open(os.path.join(OUT,"27-001_c03_鹿邑县.json"),"w",encoding="utf-8") as f:
    json.dump(ly,f,ensure_ascii=False,indent=2)
print("c03 done")

# ---- c04 夏邑县 ----
xy = county_file("c04", "夏邑县", "GEO-27001",
  "在府城东一百二十里", "一十四里", 14,
  [
    {"evo_id":"EVO-001","item_id":"27-001","geo_id":"GEO-27001c04","dynasty":"战国","era":None,"institution_name":"下邑地","action":"因之","detail":"战国时下邑地，秦属砀郡"},
    {"evo_id":"EVO-002","item_id":"27-001","geo_id":"GEO-27001c04","dynasty":"汉","era":None,"institution_name":"下邑县","action":"置","detail":"汉置下邑县属梁国，后魏置砀郡于此"},
    {"evo_id":"EVO-003","item_id":"27-001","geo_id":"GEO-27001c04","dynasty":"金","era":None,"institution_name":"夏邑县","action":"改","detail":"金始改夏邑县属永州，元初并入睢阳寻复置"},
    {"evo_id":"EVO-004","item_id":"27-001","geo_id":"GEO-27001c04","dynasty":"明","era":None,"institution_name":"夏邑县","action":"因之","detail":"以谷熟县省入，本朝因之"}
  ],
  sites=[
    {"site_id":"SITE-001","item_id":"27-001","geo_id":"GEO-27001c04","name":"夏邑县学","type":"学校","location_text":"在县治东南","history_lore":"金大定间建，本朝洪武三年重建嘉靖间修"},
    {"site_id":"SITE-002","item_id":"27-001","geo_id":"GEO-27001c04","name":"崇正书院","type":"书院","location_text":"在夏邑县慈胜寺西","history_lore":"嘉靖间重建"},
  ]
)
with open(os.path.join(OUT,"27-001_c04_夏邑县.json"),"w",encoding="utf-8") as f:
    json.dump(xy,f,ensure_ascii=False,indent=2)
print("c04 done")

# ---- c05 永城县 ----
yc = county_file("c05", "永城县", "GEO-27001",
  "在府城东一百八十里", "二十四里", 24,
  [
    {"evo_id":"EVO-001","item_id":"27-001","geo_id":"GEO-27001c05","dynasty":"春秋","era":None,"institution_name":"芒县","action":"置","detail":"本春秋芒县地亦名犬丘"},
    {"evo_id":"EVO-002","item_id":"27-001","geo_id":"GEO-27001c05","dynasty":"东汉","era":None,"institution_name":"临睢太丘","action":"改","detail":"东汉改芒曰临睢犬丘曰太丘，三国魏二县俱废"},
    {"evo_id":"EVO-003","item_id":"27-001","geo_id":"GEO-27001c05","dynasty":"隋","era":None,"institution_name":"永城县","action":"置","detail":"隋始置永城县属谯州后废，唐复置属亳州"},
    {"evo_id":"EVO-004","item_id":"27-001","geo_id":"GEO-27001c05","dynasty":"明","era":None,"institution_name":"永城县","action":"因之","detail":"宋仍旧元属归德，本朝因之"}
  ],
  mtns=[
    {"mtn_id":"MTN-001","item_id":"27-001","geo_id":"GEO-27001c05","name":"砀山","type":"山","location_text":"在永城县北八十里","description":"即汉高祖隐处又名磨山，白毛山石洞山黄土山戏山绵亘几二十里","lore":""},
    {"mtn_id":"MTN-002","item_id":"27-001","geo_id":"GEO-27001c05","name":"夫子岩","type":"岩","location_text":"在永城县北","description":"世传夫子经此后人因肖像壁间","lore":""},
  ],
  sites=[
    {"site_id":"SITE-001","item_id":"27-001","geo_id":"GEO-27001c05","name":"永城县学","type":"学校","location_text":"在县治西南","history_lore":"元建本朝洪武三年重建"},
    {"site_id":"SITE-002","item_id":"27-001","geo_id":"GEO-27001c05","name":"造律台","type":"古迹","location_text":"在永城县西南三里","history_lore":"上有汉酂侯萧何庙"},
  ]
)
with open(os.path.join(OUT,"27-001_c05_永城县.json"),"w",encoding="utf-8") as f:
    json.dump(yc,f,ensure_ascii=False,indent=2)
print("c05 done")

# ---- c06 虞城县 ----
yc2 = county_file("c06", "虞城县", "GEO-27001",
  "在府城东北六十里", "一十四里", 14,
  [
    {"evo_id":"EVO-001","item_id":"27-001","geo_id":"GEO-27001c06","dynasty":"虞","era":None,"institution_name":"虞国","action":"置","detail":"本古虞国即禹封商均之地"},
    {"evo_id":"EVO-002","item_id":"27-001","geo_id":"GEO-27001c06","dynasty":"汉","era":None,"institution_name":"虞县","action":"置","detail":"汉置虞县属梁国，后魏属沛郡，北齐省"},
    {"evo_id":"EVO-003","item_id":"27-001","geo_id":"GEO-27001c06","dynasty":"隋","era":None,"institution_name":"虞城县","action":"复","detail":"隋复置属宋州，唐置东虞州寻废改县曰虞城"},
    {"evo_id":"EVO-004","item_id":"27-001","geo_id":"GEO-27001c06","dynasty":"明","era":None,"institution_name":"虞城县","action":"因之","detail":"金废元复置属济宁路，本朝改今属"}
  ],
  mtns=[
    {"mtn_id":"MTN-001","item_id":"27-001","geo_id":"GEO-27001c06","name":"孟潴泽","type":"湖","location_text":"在虞城县西北一十里","description":"尔雅作孟诸，禹贡所谓导菏泽被孟诸即此","lore":"高适诗有我本渔樵孟诸野一生自是悠悠者之句"},
    {"mtn_id":"MTN-002","item_id":"27-001","geo_id":"GEO-27001c06","name":"空桐泽","type":"湖","location_text":"在虞城县南一十里","description":"睢水东南流经此泽有空桐亭","lore":""},
    {"mtn_id":"MTN-003","item_id":"27-001","geo_id":"GEO-27001c06","name":"李令泉","type":"泉","location_text":"在虞城县治内","description":"旧井水清而味苦，县令李锡下车尝之莞尔笑曰既苦且清足以符吾志","lore":"李白为送去思颂"},
  ],
  sites=[
    {"site_id":"SITE-001","item_id":"27-001","geo_id":"GEO-27001c06","name":"虞城县学","type":"学校","location_text":"在县治南","history_lore":"旧在县治西元建，本朝洪武四年重建嘉靖九年圮于水迁今地"},
  ]
)
with open(os.path.join(OUT,"27-001_c06_虞城县.json"),"w",encoding="utf-8") as f:
    json.dump(yc2,f,ensure_ascii=False,indent=2)
print("c06 done")

# ---- s01 睢州 ----
sz = {
  "item_id": "27-001", "volume": "27", "source": "睢州", "region": "河南", "type": "subprefecture",
  "original": "睢州【在府城东一百二十里春秋时宋陈地秦置襄邑县汉属陈留郡北齐并襄邑入雍丘隋复置襄邑属宋州唐属杞州后仍属宋州宋属应天府崇宁间建拱州以为东辅大观中废拱州后复置金改睢州元因之并以襄邑县为附郭本朝省入州属开封府嘉靖二十四年改今属编户三十九里领县二】",
  "layers": {
    "ents": [
      {"ent_id":"ENT-001","name":"睢州","type":"geo","norm":"睢州","first_source":"27-001"},
      {"ent_id":"ENT-002","name":"襄邑县","type":"geo","norm":"襄邑县","first_source":"27-001"},
      {"ent_id":"ENT-003","name":"拱州","type":"geo","norm":"拱州","first_source":"27-001"}
    ],
    "geos": [{
      "geo_id": "GEO-27001s01", "item_id": "27-001", "name": "睢州", "type": "subprefecture",
      "region": "河南", "parent": "GEO-27001", "children": ["GEO-27001c07", "GEO-27001c08"],
      "volume_range": "卷27",
      "attributes": {"location_text": "在府城东一百二十里", "households": {"count": 39, "unit": "里", "note": "编户三十九里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id":"EVO-001","item_id":"27-001","geo_id":"GEO-27001s01","dynasty":"春秋","era":None,"institution_name":"宋陈地","action":"因之","detail":"春秋时宋陈地"},
      {"evo_id":"EVO-002","item_id":"27-001","geo_id":"GEO-27001s01","dynasty":"秦","era":None,"institution_name":"襄邑县","action":"置","detail":"秦置襄邑县汉属陈留郡，北齐并襄邑入雍丘"},
      {"evo_id":"EVO-003","item_id":"27-001","geo_id":"GEO-27001s01","dynasty":"宋","era":"崇宁","institution_name":"拱州","action":"升","detail":"宋属应天府，崇宁间建拱州以为东辅，大观中废拱州后复置"},
      {"evo_id":"EVO-004","item_id":"27-001","geo_id":"GEO-27001s01","dynasty":"金","era":None,"institution_name":"睢州","action":"改","detail":"金改睢州元因之，并以襄邑县为附郭"},
      {"evo_id":"EVO-005","item_id":"27-001","geo_id":"GEO-27001s01","dynasty":"明","era":"嘉靖","institution_name":"睢州","action":"因之","detail":"本朝省入州属开封府，嘉靖二十四年改今属，领县二"}
    ],
    "mtns": [
      {"mtn_id":"MTN-001","item_id":"27-001","geo_id":"GEO-27001s01","name":"恒山","type":"山","location_text":"在睢州城西北一十二里","description":"","lore":""},
      {"mtn_id":"MTN-002","item_id":"27-001","geo_id":"GEO-27001s01","name":"骆驼冈","type":"冈","location_text":"在睢州襄公台后","description":"其形起伏如驼故名，环冈佳木郁葱地颇幽胜","lore":"说者谓襄公游玩地"},
      {"mtn_id":"MTN-003","item_id":"27-001","geo_id":"GEO-27001s01","name":"西湖","type":"湖","location_text":"在睢州城西骆驼岭后","description":"周四十里","lore":""},
      {"mtn_id":"MTN-004","item_id":"27-001","geo_id":"GEO-27001s01","name":"睢水","type":"河","location_text":"在睢州北七里","description":"州之得名以此，韩信败龙且睢水为之不流此即其上流也","lore":""},
    ],
    "pers": [],
    "sites": [
      {"site_id":"SITE-001","item_id":"27-001","geo_id":"GEO-27001s01","name":"睢州学","type":"学校","location_text":"在州治北","history_lore":"洪武三年建，正统弘治中俱重修"},
      {"site_id":"SITE-002","item_id":"27-001","geo_id":"GEO-27001s01","name":"锦襄书院","type":"书院","location_text":"在睢州骆驼冈","history_lore":"旧为僧寺，嘉靖初改建"},
      {"site_id":"SITE-003","item_id":"27-001","geo_id":"GEO-27001s01","name":"圣寿寺","type":"寺观","location_text":"在睢州南","history_lore":"元建本朝正统中重建"},
      {"site_id":"SITE-004","item_id":"27-001","geo_id":"GEO-27001s01","name":"襄陵","type":"陵墓","location_text":"在睢州东","history_lore":"一名古襄陵，宋襄公春秋五霸之一"},
    ],
    "prods": [],
    "cits": []
  },
  "layer_count": 7,
  "validation": {"errs": [], "gap": 0, "notes": ""}
}
with open(os.path.join(OUT,"27-001_s01_睢州.json"),"w",encoding="utf-8") as f:
    json.dump(sz,f,ensure_ascii=False,indent=2)
print("s01 done")

# ---- c07 考城县 (under 睢州) ----
kc = county_file("c07", "考城县", "GEO-27001s01",
  "在州城东北九十里", "一十一里", 11,
  [
    {"evo_id":"EVO-001","item_id":"27-001","geo_id":"GEO-27001c07","dynasty":"周","era":None,"institution_name":"戴国","action":"置","detail":"本周之戴国，春秋时郑取之改名谷城"},
    {"evo_id":"EVO-002","item_id":"27-001","geo_id":"GEO-27001c07","dynasty":"秦","era":None,"institution_name":"甾县","action":"置","detail":"秦置甾县汉属梁国"},
    {"evo_id":"EVO-003","item_id":"27-001","geo_id":"GEO-27001c07","dynasty":"东汉","era":None,"institution_name":"考城县","action":"改","detail":"东汉始改考城属陈留郡，晋省后魏置考阳县"},
    {"evo_id":"EVO-004","item_id":"27-001","geo_id":"GEO-27001c07","dynasty":"隋","era":None,"institution_name":"考城县","action":"复","detail":"隋复为考城县属宋州，金属睢州，本朝因之"}
  ],
  mtns=[
    {"mtn_id":"MTN-001","item_id":"27-001","geo_id":"GEO-27001c07","name":"葛冈","type":"冈","location_text":"在考城县南二里","description":"世传葛洪炼丹处又曰葛伯所筑未知孰是","lore":""},
    {"mtn_id":"MTN-002","item_id":"27-001","geo_id":"GEO-27001c07","name":"卧龙岗","type":"冈","location_text":"在考城县南十五里","description":"世传诸葛亮游寓于此故名","lore":""},
    {"mtn_id":"MTN-003","item_id":"27-001","geo_id":"GEO-27001c07","name":"葵丘","type":"古迹","location_text":"在考城县治东","description":"春秋诸侯盟于葵丘即此","lore":""},
  ],
  sites=[
    {"site_id":"SITE-001","item_id":"27-001","geo_id":"GEO-27001c07","name":"考城县学","type":"学校","location_text":"在县治东南","history_lore":"洪武二十四年建圮于水，正统间重建"},
  ]
)
with open(os.path.join(OUT,"27-001_c07_考城县.json"),"w",encoding="utf-8") as f:
    json.dump(kc,f,ensure_ascii=False,indent=2)
print("c07 done")

# ---- c08 柘城县 (under 睢州) ----
zc = county_file("c08", "柘城县", "GEO-27001s01",
  "在州城东南九十里", "九里", 9,
  [
    {"evo_id":"EVO-001","item_id":"27-001","geo_id":"GEO-27001c08","dynasty":"古","era":None,"institution_name":"朱襄氏邑","action":"置","detail":"古朱襄氏邑，春秋时为陈株野地"},
    {"evo_id":"EVO-002","item_id":"27-001","geo_id":"GEO-27001c08","dynasty":"汉","era":None,"institution_name":"柘县","action":"置","detail":"汉置柘县属淮阳国，以邑有柘沟故名，晋废"},
    {"evo_id":"EVO-003","item_id":"27-001","geo_id":"GEO-27001c08","dynasty":"隋","era":None,"institution_name":"柘城县","action":"复","detail":"隋复置改曰柘城县属宋州，金属睢州后省"},
    {"evo_id":"EVO-004","item_id":"27-001","geo_id":"GEO-27001c08","dynasty":"明","era":None,"institution_name":"柘城县","action":"因之","detail":"元复置本朝因之"}
  ],
  mtns=[
    {"mtn_id":"MTN-001","item_id":"27-001","geo_id":"GEO-27001c08","name":"廓山","type":"山","location_text":"在柘城东北二里","description":"","lore":""},
    {"mtn_id":"MTN-002","item_id":"27-001","geo_id":"GEO-27001c08","name":"霸王冈","type":"冈","location_text":"在柘城县西三十里","description":"世传项羽将台与汉高祖拒兵处","lore":""},
  ],
  sites=[
    {"site_id":"SITE-001","item_id":"27-001","geo_id":"GEO-27001c08","name":"柘城县学","type":"学校","location_text":"在县治东","history_lore":"旧在东南金大定初建，本朝洪武四年重建嘉靖间圮于水迁今地"},
  ]
)
with open(os.path.join(OUT,"27-001_c08_柘城县.json"),"w",encoding="utf-8") as f:
    json.dump(zc,f,ensure_ascii=False,indent=2)
print("c08 done")
print("All 归德府 files done!")
