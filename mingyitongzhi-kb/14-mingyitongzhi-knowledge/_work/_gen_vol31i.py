# -*- coding: utf-8 -*-
"""Generate vol31 c11 息县, c12 商城."""
import json, os
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol31"

def dump(name, obj):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  {name}: {os.path.getsize(p)} bytes")

# c11 息县
c11 = {
  "item_id": "31-001", "volume": "31", "source": "息县", "region": "河南", "type": "county",
  "original": "息县【在州西北九十里春秋为息侯国汉置息县属汝南郡后徙于东改曰新息晋为汝南郡治后魏置东豫州梁改曰西豫州又改曰淮州东魏复曰东豫州后周改息州隋废唐复置贞观初废以县属蔡州金复置息州元属汝宁府本朝改州为息县初属颍州后改属光州编户二十八里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "息县", "type": "geo", "norm": "息县", "first_source": "31-001"},
      {"ent_id": "ENT-002", "name": "谷河", "type": "mtn", "norm": "谷河", "first_source": "31-001"},
      {"ent_id": "ENT-003", "name": "泥河", "type": "mtn", "norm": "泥河", "first_source": "31-001"},
      {"ent_id": "ENT-004", "name": "闾河", "type": "mtn", "norm": "闾河", "first_source": "31-001"},
      {"ent_id": "ENT-005", "name": "营河", "type": "mtn", "norm": "营河", "first_source": "31-001"},
      {"ent_id": "ENT-006", "name": "黄漂港", "type": "mtn", "norm": "黄漂港", "first_source": "31-001"},
      {"ent_id": "ENT-007", "name": "连桥港", "type": "mtn", "norm": "连桥港", "first_source": "31-001"},
      {"ent_id": "ENT-008", "name": "曲吕港", "type": "mtn", "norm": "曲吕港", "first_source": "31-001"},
      {"ent_id": "ENT-009", "name": "涧头港", "type": "mtn", "norm": "涧头港", "first_source": "31-001"},
      {"ent_id": "ENT-010", "name": "玉梁渠", "type": "mtn", "norm": "玉梁渠", "first_source": "31-001"},
      {"ent_id": "ENT-011", "name": "珉玉坑", "type": "mtn", "norm": "珉玉坑", "first_source": "31-001"},
      {"ent_id": "ENT-012", "name": "古息国", "type": "geo", "norm": "古息国", "first_source": "31-001"},
      {"ent_id": "ENT-013", "name": "新息废县", "type": "geo", "norm": "新息废县", "first_source": "31-001"},
      {"ent_id": "ENT-014", "name": "阳安故城", "type": "geo", "norm": "阳安故城", "first_source": "31-001"},
      {"ent_id": "ENT-015", "name": "褒信废县", "type": "geo", "norm": "褒信废县", "first_source": "31-001"},
      {"ent_id": "ENT-016", "name": "白公城", "type": "geo", "norm": "白公城", "first_source": "31-001"},
      {"ent_id": "ENT-017", "name": "贾彪", "type": "person", "norm": "贾彪", "first_source": "31-001"},
      {"ent_id": "ENT-018", "name": "傅尧俞", "type": "person", "norm": "傅尧俞", "first_source": "31-001"},
      {"ent_id": "ENT-019", "name": "宜仲庸", "type": "person", "norm": "宜仲庸", "first_source": "31-001"},
      {"ent_id": "ENT-020", "name": "王平", "type": "person", "norm": "王平", "first_source": "31-001"},
      {"ent_id": "ENT-021", "name": "孟祯", "type": "person", "norm": "孟祯", "first_source": "31-001"}
    ],
    "geos": [{
      "geo_id": "GEO-31001c11", "item_id": "31-001", "name": "息县", "type": "county", "region": "河南",
      "parent": "GEO-31001s02", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在州西北九十里", "households": {"count": 28, "unit": "里", "note": "编户二十八里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-001", "geo_id": "GEO-31001c11", "dynasty": "周", "era": None, "institution_name": "息侯国", "action": "置", "detail": "春秋为息侯国"},
      {"evo_id": "EVO-002", "item_id": "31-001", "geo_id": "GEO-31001c11", "dynasty": "汉", "era": None, "institution_name": "息县/新息", "action": "置", "detail": "汉置息县属汝南郡，后徙于东改曰新息，晋为汝南郡治"},
      {"evo_id": "EVO-003", "item_id": "31-001", "geo_id": "GEO-31001c11", "dynasty": "南北朝", "era": None, "institution_name": "东豫州/息州", "action": "改", "detail": "后魏置东豫州，梁改西豫州又改淮州，东魏复东豫州，后周改息州"},
      {"evo_id": "EVO-004", "item_id": "31-001", "geo_id": "GEO-31001c11", "dynasty": "唐", "era": "贞观", "institution_name": "息县", "action": "废州", "detail": "隋废，唐复置，贞观初废以县属蔡州"},
      {"evo_id": "EVO-005", "item_id": "31-001", "geo_id": "GEO-31001c11", "dynasty": "金", "era": None, "institution_name": "息州", "action": "复置", "detail": "金复置息州，元属汝宁府"},
      {"evo_id": "EVO-006", "item_id": "31-001", "geo_id": "GEO-31001c11", "dynasty": "明", "era": None, "institution_name": "息县", "action": "改州为县", "detail": "本朝改州为息县，初属颍州后改属光州"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "谷河", "type": "河", "location_text": "在息县东南四十里", "description": "水自竖扶堰东流入淮", "lore": ""},
      {"mtn_id": "MTN-002", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "泥河", "type": "河", "location_text": "在息县东南四十五里", "description": "水自万安塘东流入淮", "lore": ""},
      {"mtn_id": "MTN-003", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "闾河", "type": "河", "location_text": "在息县东北九十里", "description": "水自高皇陂东流合撞陂港入淮", "lore": ""},
      {"mtn_id": "MTN-004", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "营河", "type": "河", "location_text": "在息县东北一百里", "description": "水自汶河东南流入淮", "lore": ""},
      {"mtn_id": "MTN-005", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "黄漂港", "type": "港", "location_text": "在息县南八十里", "description": "水自确陂塘南流入淮", "lore": ""},
      {"mtn_id": "MTN-006", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "连桥港", "type": "港", "location_text": "在息县东一百里", "description": "水自蚁陂塘东流入淮", "lore": ""},
      {"mtn_id": "MTN-007", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "曲吕港", "type": "港", "location_text": "在息县东北一百四十里", "description": "水自清沟东流入汝", "lore": ""},
      {"mtn_id": "MTN-008", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "涧头港", "type": "港", "location_text": "在息县东五百里", "description": "水自莫陂塘东流入汝", "lore": ""},
      {"mtn_id": "MTN-009", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "玉梁渠", "type": "渠", "location_text": "在息县西北五十里", "description": "隋仁寿初尝浚以溉田，唐开元中县令薛务更加疏导为陂十六所溉田至三十余顷", "lore": ""},
      {"mtn_id": "MTN-010", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "珉玉坑", "type": "坑", "location_text": "在息县西北", "description": "旧出珉玉其色青白堪为器物，隋时置官采之，唐时为淮水所没，开元中淮水东移坑重出", "lore": ""}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "贾彪", "type": "名宦", "dynasty": "汉", "native_place": "", "office": "新息长", "summary": "延熹中新息长，小民贫窭多不养子，彪严为之制，数年养子千数，佥曰贾父所长"},
      {"per_id": "PER-002", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "傅尧俞", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "知新息县", "summary": "清而不耀，直而不激，司马光称其贤"},
      {"per_id": "PER-003", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "宜仲庸", "type": "名宦", "dynasty": "明", "native_place": "", "office": "息县知县", "summary": "优于政事，凡有科办必誓于神，官无堕事民无怨辞，尤留心学校勉励生徒"},
      {"per_id": "PER-004", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "孟祯", "type": "人物", "dynasty": "明", "native_place": "息县", "office": "四川左布政使", "summary": "聪敏力学处事知大体，洪武中以儒士举累官四川左布政使"},
      {"per_id": "PER-005", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "王平", "type": "人物", "dynasty": "明", "native_place": "息县", "office": "交趾左布政使", "summary": "有高才善辩说，以清白自持刚明果决，洪武中以国子生释褐拜监察御史，累官左佥都御史"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "息县学", "type": "学校", "location_text": "在县治西南", "history_lore": "洪武八年建"},
      {"site_id": "SITE-002", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "大慈寺", "type": "寺观", "location_text": "在息县东", "history_lore": "永乐末建"},
      {"site_id": "SITE-003", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "贾君庙", "type": "祠庙", "location_text": "在息县", "history_lore": "后汉贾彪为新息长有政绩，人为立祠"},
      {"site_id": "SITE-004", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "息侯庙", "type": "祠庙", "location_text": "在新息废县西南一十里", "history_lore": "息侯周时息国君"},
      {"site_id": "SITE-005", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "桐柏庙", "type": "祠庙", "location_text": "在新息废县南", "history_lore": "祀桐柏山之神"},
      {"site_id": "SITE-006", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "唐庄桥", "type": "关梁", "location_text": "在息县东北褒信里", "history_lore": "跨闾河上"},
      {"site_id": "SITE-007", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "古息国", "type": "古迹", "location_text": "在息县北三十里", "history_lore": "春秋时息国，汉为新息县，唐置息州，元省县入州"},
      {"site_id": "SITE-008", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "阳安故城", "type": "古迹", "location_text": "在息县西南一十里", "history_lore": "春秋时江国，汉置阳安县属汝南郡，晋因之"},
      {"site_id": "SITE-009", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "白公城", "type": "古迹", "location_text": "在息县", "history_lore": "其城楚太子建内，旧有庙"},
      {"site_id": "SITE-010", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "褒信废县", "type": "古迹", "location_text": "在息县东北", "history_lore": "本汉郾县地，东汉析置此县，刘宋改曰包信，隋复旧，唐改曰包孚，元省入息州"}
    ],
    "prods": [
      {"prod_id": "PROD-001", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "棋子石", "category": "矿", "location_text": "息县出"},
      {"prod_id": "PROD-002", "item_id": "31-001", "geo_id": "GEO-31001c11", "name": "红花", "category": "药", "location_text": "息县出"}
    ],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
dump("31-001_c11_息县.json", c11)

# c12 商城县
c12 = {
  "item_id": "31-001", "volume": "31", "source": "商城县", "region": "河南", "type": "county",
  "original": "商城县【在州北一百里春秋时为黄国战国属楚秦属九江郡西汉属汝南郡东汉属淮阳国晋属汝隂郡刘宋置殷城县唐初改置义州寻废以地属弋阳郡宋复置商城县寻省入固始县金元仍旧本朝初因之成化十一年复置改今属编户二十六里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "商城县", "type": "geo", "norm": "商城县", "first_source": "31-001"},
      {"ent_id": "ENT-002", "name": "黄国", "type": "geo", "norm": "黄国", "first_source": "31-001"}
    ],
    "geos": [{
      "geo_id": "GEO-31001c12", "item_id": "31-001", "name": "商城县", "type": "county", "region": "河南",
      "parent": "GEO-31001s02", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在州北一百里", "households": {"count": 26, "unit": "里", "note": "编户二十六里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-001", "geo_id": "GEO-31001c12", "dynasty": "周", "era": None, "institution_name": "黄国", "action": "置", "detail": "春秋时为黄国"},
      {"evo_id": "EVO-002", "item_id": "31-001", "geo_id": "GEO-31001c12", "dynasty": "汉", "era": None, "institution_name": "汝南郡地", "action": "置", "detail": "西汉属汝南郡，东汉属淮阳国，晋属汝阴郡"},
      {"evo_id": "EVO-003", "item_id": "31-001", "geo_id": "GEO-31001c12", "dynasty": "南北朝", "era": "刘宋", "institution_name": "殷城县", "action": "置", "detail": "刘宋置殷城县"},
      {"evo_id": "EVO-004", "item_id": "31-001", "geo_id": "GEO-31001c12", "dynasty": "唐", "era": None, "institution_name": "义州", "action": "废", "detail": "唐初改置义州寻废以地属弋阳郡"},
      {"evo_id": "EVO-005", "item_id": "31-001", "geo_id": "GEO-31001c12", "dynasty": "宋", "era": None, "institution_name": "商城县", "action": "复置", "detail": "宋复置商城县，寻省入固始县，金元仍旧"},
      {"evo_id": "EVO-006", "item_id": "31-001", "geo_id": "GEO-31001c12", "dynasty": "明", "era": "成化", "institution_name": "商城县", "action": "复置", "detail": "本朝初因之，成化十一年复置改今属"}
    ],
    "mtns": [],
    "pers": [],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-001", "geo_id": "GEO-31001c12", "name": "商城县学", "type": "学校", "location_text": "在县治东", "history_lore": "成化十三年因置县始建"}
    ],
    "prods": [],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": "县志简，山川无额外条目"}
}
dump("31-001_c12_商城县.json", c12)

print("DONE c11-c12")
