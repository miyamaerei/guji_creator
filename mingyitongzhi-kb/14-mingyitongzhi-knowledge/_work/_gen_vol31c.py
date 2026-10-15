# -*- coding: utf-8 -*-
"""Generate vol31 county files part 2: c04-c06, s01."""
import json, os
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol31"

def dump(name, obj):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  {name}: {os.path.getsize(p)} bytes")

# c04 新蔡县
c04 = {
  "item_id": "31-001", "volume": "31", "source": "新蔡县", "region": "河南", "type": "county",
  "original": "新蔡县【在府城东五十里古吕国春秋时蔡平侯徙都此故曰新蔡汉置新蔡县属汝南郡晋属汝隂郡刘宋属新蔡郡南齐置北新蔡郡东魏置蔡州北齐为广宁郡隋初为舒州及广宁县寻改汝北县大业初州废县复旧名唐属蔡州宋因之金属息州元省入息州本朝洪武四年复置改今属编户一十二里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "新蔡县", "type": "geo", "norm": "新蔡县", "first_source": "31-001"},
      {"ent_id": "ENT-002", "name": "鲖水", "type": "mtn", "norm": "鲖水", "first_source": "31-001"},
      {"ent_id": "ENT-003", "name": "鲖阳故城", "type": "geo", "norm": "鲖阳故城", "first_source": "31-001"},
      {"ent_id": "ENT-004", "name": "大吕亭", "type": "geo", "norm": "大吕亭", "first_source": "31-001"},
      {"ent_id": "ENT-005", "name": "干宝", "type": "person", "norm": "干宝", "first_source": "31-001"}
    ],
    "geos": [{
      "geo_id": "GEO-31001c04", "item_id": "31-001", "name": "新蔡县", "type": "county", "region": "河南",
      "parent": "GEO-31001", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在府城东五十里", "households": {"count": 12, "unit": "里", "note": "编户一十二里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-001", "geo_id": "GEO-31001c04", "dynasty": "周", "era": None, "institution_name": "吕国/新蔡", "action": "置", "detail": "古吕国，春秋时蔡平侯徙都此故曰新蔡"},
      {"evo_id": "EVO-002", "item_id": "31-001", "geo_id": "GEO-31001c04", "dynasty": "汉", "era": None, "institution_name": "新蔡县", "action": "置", "detail": "汉置新蔡县属汝南郡"},
      {"evo_id": "EVO-003", "item_id": "31-001", "geo_id": "GEO-31001c04", "dynasty": "南北朝", "era": "东魏", "institution_name": "蔡州/广宁郡", "action": "改", "detail": "东魏置蔡州，北齐为广宁郡"},
      {"evo_id": "EVO-004", "item_id": "31-001", "geo_id": "GEO-31001c04", "dynasty": "隋", "era": None, "institution_name": "新蔡县", "action": "复旧", "detail": "隋初为舒州及广宁县，寻改汝北县，大业初州废县复旧名"},
      {"evo_id": "EVO-005", "item_id": "31-001", "geo_id": "GEO-31001c04", "dynasty": "元", "era": None, "institution_name": "新蔡县", "action": "省", "detail": "金属息州，元省入息州，本朝洪武四年复置改今属"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-001", "geo_id": "GEO-31001c04", "name": "鲖水", "type": "河", "location_text": "在新蔡县", "description": "汉因此水置鲖阳县", "lore": ""}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-001", "geo_id": "GEO-31001c04", "name": "干宝", "type": "人物", "dynasty": "晋", "native_place": "新蔡", "office": "散骑常侍", "summary": "博览书记为著作郎，着晋记三十卷，又着搜神记三十卷，刘惔曰卿可谓鬼之董狐"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-001", "geo_id": "GEO-31001c04", "name": "新蔡县学", "type": "学校", "location_text": "在县治东", "history_lore": "旧在县治东古城内，洪武十一年因元旧址重建，天顺二年徙于此"},
      {"site_id": "SITE-002", "item_id": "31-001", "geo_id": "GEO-31001c04", "name": "法隆寺", "type": "寺观", "location_text": "在新蔡县东北古城内", "history_lore": "正统初重建"},
      {"site_id": "SITE-003", "item_id": "31-001", "geo_id": "GEO-31001c04", "name": "鲖阳故城", "type": "古迹", "location_text": "在新蔡县界", "history_lore": "汉旧县属汝南郡，晋属汝阴郡，隋属淮阳郡"},
      {"site_id": "SITE-004", "item_id": "31-001", "geo_id": "GEO-31001c04", "name": "大吕亭", "type": "古迹", "location_text": "在新蔡县界", "history_lore": "东汉郡国志云故吕侯国也，县东北有栎亭，左传吴伐楚入栎即此"}
    ],
    "prods": [],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
dump("31-001_c04_新蔡县.json", c04)

# c05 西平县
c05 = {
  "item_id": "31-001", "volume": "31", "source": "西平县", "region": "河南", "type": "county",
  "original": "西平县【在府城西北一百三十里古栢子国汉置西平县属汝南郡东汉末废后魏复置并置襄城郡北齐改文城郡隋初郡废以县属蔡州大业初县废唐初复置贞观初省入郾城开元间再置属蔡州宋金元仍旧本朝因之改今属编户二十二里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "西平县", "type": "geo", "norm": "西平县", "first_source": "31-001"},
      {"ent_id": "ENT-002", "name": "棠溪", "type": "mtn", "norm": "棠溪", "first_source": "31-001"},
      {"ent_id": "ENT-003", "name": "周家泊", "type": "mtn", "norm": "周家泊", "first_source": "31-001"},
      {"ent_id": "ENT-004", "name": "邓艾陂", "type": "mtn", "norm": "邓艾陂", "first_source": "31-001"},
      {"ent_id": "ENT-005", "name": "柏亭桥", "type": "mtn", "norm": "柏亭桥", "first_source": "31-001"},
      {"ent_id": "ENT-006", "name": "郅恽", "type": "person", "norm": "郅恽", "first_source": "31-001"},
      {"ent_id": "ENT-007", "name": "李郃", "type": "person", "norm": "李郃", "first_source": "31-001"},
      {"ent_id": "ENT-008", "name": "和元恕", "type": "person", "norm": "和元恕", "first_source": "31-001"},
      {"ent_id": "ENT-009", "name": "李不作", "type": "person", "norm": "李不作", "first_source": "31-001"}
    ],
    "geos": [{
      "geo_id": "GEO-31001c05", "item_id": "31-001", "name": "西平县", "type": "county", "region": "河南",
      "parent": "GEO-31001", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在府城西北一百三十里", "households": {"count": 22, "unit": "里", "note": "编户二十二里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-001", "geo_id": "GEO-31001c05", "dynasty": "周", "era": None, "institution_name": "柏子国", "action": "置", "detail": "古柏子国"},
      {"evo_id": "EVO-002", "item_id": "31-001", "geo_id": "GEO-31001c05", "dynasty": "汉", "era": None, "institution_name": "西平县", "action": "置", "detail": "汉置西平县属汝南郡，东汉末废"},
      {"evo_id": "EVO-003", "item_id": "31-001", "geo_id": "GEO-31001c05", "dynasty": "南北朝", "era": "后魏", "institution_name": "襄城郡/文城郡", "action": "置", "detail": "后魏复置并置襄城郡，北齐改文城郡"},
      {"evo_id": "EVO-004", "item_id": "31-001", "geo_id": "GEO-31001c05", "dynasty": "唐", "era": None, "institution_name": "西平县", "action": "复置", "detail": "隋初郡废以县属蔡州，大业初县废；唐初复置，贞观初省入郾城，开元间再置属蔡州"},
      {"evo_id": "EVO-005", "item_id": "31-001", "geo_id": "GEO-31001c05", "dynasty": "明", "era": None, "institution_name": "西平县", "action": "因之", "detail": "宋金元仍旧，本朝因之改今属"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "棠溪", "type": "溪", "location_text": "在西平县西", "description": "有村，苏秦说韩王谓剑防出于棠溪即此", "lore": ""},
      {"mtn_id": "MTN-002", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "周家泊", "type": "湖", "location_text": "在西平县东北二十五里", "description": "水则出鱼，涸则生苇", "lore": ""},
      {"mtn_id": "MTN-003", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "邓艾陂", "type": "陂", "location_text": "在西平县", "description": "艾所置陂凡二十有四因名", "lore": ""}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "郅恽", "type": "人物", "dynasty": "汉", "native_place": "汝南西平", "office": "长沙太守", "summary": "举孝廉为上东门侯，光武出猎夜还恽拒关不纳；后授皇太子韩诗，迁长沙太守"},
      {"per_id": "PER-002", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "李不作", "type": "名宦", "dynasty": "元", "native_place": "", "office": "西平县尹", "summary": "化民以德不尚威严，民兴礼让；汝水泛溢率民筑防补罅，其患遂息"},
      {"per_id": "PER-003", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "和元恕", "type": "名宦", "dynasty": "元", "native_place": "", "office": "西平县尹", "summary": "劝农兴学折节好贤，民有讼不勤鞭朴惟谕以曲直，在任五年公无负租蝗不入境"},
      {"per_id": "PER-004", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "王敬", "type": "名宦", "dynasty": "明", "native_place": "", "office": "西平知县", "summary": "天顺初西平知县，刚果有为，吏畏民服"},
      {"per_id": "PER-005", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "甘镛", "type": "名宦", "dynasty": "明", "native_place": "", "office": "西平县典史", "summary": "永乐中西平县典史，政宜于民，荐升监察御史"},
      {"per_id": "PER-006", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "徐理", "type": "人物", "dynasty": "明", "native_place": "西平", "office": "武康伯", "summary": "国初从诸将征伐有功，洪武末从靖内难大小数十战皆贾勇争先，累官都督佥事封武康伯"},
      {"per_id": "PER-007", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "毛鹏霄", "type": "人物", "dynasty": "明", "native_place": "西平", "office": "邠州知州", "summary": "永乐乙酉科举人，除陕西邠州知州；子祥山进士仕终云南参政"},
      {"per_id": "PER-008", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "尹聪", "type": "人物", "dynasty": "明", "native_place": "西平", "office": "山东左参议", "summary": "永乐辛卯科举人，累官山东左参议"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "西平县学", "type": "学校", "location_text": "在县治东南隅", "history_lore": "洪武三年建"},
      {"site_id": "SITE-002", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "宝岩寺", "type": "寺观", "location_text": "在西平县治东", "history_lore": ""},
      {"site_id": "SITE-003", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "柏亭桥", "type": "关梁", "location_text": "在西平县治西", "history_lore": ""},
      {"site_id": "SITE-004", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "西平故城", "type": "古迹", "location_text": "在西平县西", "history_lore": "汉旧县治此"}
    ],
    "prods": [
      {"prod_id": "PROD-001", "item_id": "31-001", "geo_id": "GEO-31001c05", "name": "红花", "category": "药", "location_text": "西平出"}
    ],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
dump("31-001_c05_西平县.json", c05)

# c06 遂平县
c06 = {
  "item_id": "31-001", "volume": "31", "source": "遂平县", "region": "河南", "type": "county",
  "original": "遂平县【在府城西九十里本春秋房子国汉为吴房县属汝南郡后魏改遂宁县属襄城郡隋复为吴房县属汝南郡唐贞观初县废寻复置属蔡州元和中改遂平县属唐州长庆初还属蔡州宋金仍旧元初省入汝阳大徳间复置属汝宁府本朝因之编户二十八里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "遂平县", "type": "geo", "norm": "遂平县", "first_source": "31-001"},
      {"ent_id": "ENT-002", "name": "嵖岈山", "type": "mtn", "norm": "嵖岈山", "first_source": "31-001"},
      {"ent_id": "ENT-003", "name": "洪山", "type": "mtn", "norm": "洪山", "first_source": "31-001"},
      {"ent_id": "ENT-004", "name": "奥来山", "type": "mtn", "norm": "奥来山", "first_source": "31-001"},
      {"ent_id": "ENT-005", "name": "石洋河", "type": "mtn", "norm": "石洋河", "first_source": "31-001"},
      {"ent_id": "ENT-006", "name": "神沟", "type": "mtn", "norm": "神沟", "first_source": "31-001"},
      {"ent_id": "ENT-007", "name": "上渠沟", "type": "mtn", "norm": "上渠沟", "first_source": "31-001"},
      {"ent_id": "ENT-008", "name": "吴房城", "type": "geo", "norm": "吴房城", "first_source": "31-001"},
      {"ent_id": "ENT-009", "name": "张庸", "type": "person", "norm": "张庸", "first_source": "31-001"}
    ],
    "geos": [{
      "geo_id": "GEO-31001c06", "item_id": "31-001", "name": "遂平县", "type": "county", "region": "河南",
      "parent": "GEO-31001", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在府城西九十里", "households": {"count": 28, "unit": "里", "note": "编户二十八里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-001", "geo_id": "GEO-31001c06", "dynasty": "周", "era": None, "institution_name": "房子国", "action": "置", "detail": "本春秋房子国"},
      {"evo_id": "EVO-002", "item_id": "31-001", "geo_id": "GEO-31001c06", "dynasty": "汉", "era": None, "institution_name": "吴房县", "action": "置", "detail": "汉为吴房县属汝南郡"},
      {"evo_id": "EVO-003", "item_id": "31-001", "geo_id": "GEO-31001c06", "dynasty": "南北朝", "era": "后魏", "institution_name": "遂宁县", "action": "改", "detail": "后魏改遂宁县属襄城郡，隋复为吴房县"},
      {"evo_id": "EVO-004", "item_id": "31-001", "geo_id": "GEO-31001c06", "dynasty": "唐", "era": "元和", "institution_name": "遂平县", "action": "改", "detail": "唐贞观初县废寻复置属蔡州，元和中改遂平县属唐州，长庆初还属蔡州"},
      {"evo_id": "EVO-005", "item_id": "31-001", "geo_id": "GEO-31001c06", "dynasty": "元", "era": "大德", "institution_name": "遂平县", "action": "复置", "detail": "元初省入汝阳，大德间复置属汝宁府，本朝因之"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-001", "geo_id": "GEO-31001c06", "name": "嵖岈山", "type": "山", "location_text": "在遂平县西七十里一名嵯峨山", "description": "其山中空有洞穴可深入，前有马鞍山", "lore": "唐书节度李观及吴元济战嵖岈山；五代史黄巢由颍蔡保嵖岈山"},
      {"mtn_id": "MTN-002", "item_id": "31-001", "geo_id": "GEO-31001c06", "name": "洪山", "type": "山", "location_text": "在遂平县西六十里", "description": "", "lore": ""},
      {"mtn_id": "MTN-003", "item_id": "31-001", "geo_id": "GEO-31001c06", "name": "奥来山", "type": "山", "location_text": "在遂平县西六十八里", "description": "过西二里有平头垛山", "lore": ""},
      {"mtn_id": "MTN-004", "item_id": "31-001", "geo_id": "GEO-31001c06", "name": "石洋河", "type": "河", "location_text": "在遂平县北五里", "description": "源出平头垛山东流入汝水", "lore": ""},
      {"mtn_id": "MTN-005", "item_id": "31-001", "geo_id": "GEO-31001c06", "name": "神沟", "type": "沟", "location_text": "在遂平县西北三十五里", "description": "有古岳庙基", "lore": ""},
      {"mtn_id": "MTN-006", "item_id": "31-001", "geo_id": "GEO-31001c06", "name": "上渠沟", "type": "沟", "location_text": "在遂平县西南三十五里", "description": "源出嵖岈山东流合阳奉沟入沙河", "lore": ""}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-001", "geo_id": "GEO-31001c06", "name": "张庸", "type": "名宦", "dynasty": "明", "native_place": "", "office": "遂平知县", "summary": "持身清洁处心正大，自莅政以来邑无堕业之民，岁无饥寒之患"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-001", "geo_id": "GEO-31001c06", "name": "遂平县学", "type": "学校", "location_text": "在县治东", "history_lore": "洪武三年因元旧址重建"},
      {"site_id": "SITE-002", "item_id": "31-001", "geo_id": "GEO-31001c06", "name": "兴国寺", "type": "寺观", "location_text": "在遂平县治西南", "history_lore": ""},
      {"site_id": "SITE-003", "item_id": "31-001", "geo_id": "GEO-31001c06", "name": "丹阳观", "type": "寺观", "location_text": "在遂平县城内东北", "history_lore": "景泰中建"},
      {"site_id": "SITE-004", "item_id": "31-001", "geo_id": "GEO-31001c06", "name": "沙河桥", "type": "关梁", "location_text": "在遂平县南沙河上", "history_lore": ""},
      {"site_id": "SITE-005", "item_id": "31-001", "geo_id": "GEO-31001c06", "name": "吴房城", "type": "古迹", "location_text": "在遂平县", "history_lore": "春秋为房子国，吴王阖闾弟夫槩奔楚封于此故曰房山，汉置吴房县，唐以吴元济叛改曰遂平"}
    ],
    "prods": [
      {"prod_id": "PROD-001", "item_id": "31-001", "geo_id": "GEO-31001c06", "name": "红花", "category": "药", "location_text": "遂平出"}
    ],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
dump("31-001_c06_遂平县.json", c06)

print("DONE c04-c06")
