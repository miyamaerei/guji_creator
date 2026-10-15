# -*- coding: utf-8 -*-
"""Generate vol31 c09 光山, c10 固始, c11 息县, c12 商城."""
import json, os
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol31"

def dump(name, obj):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  {name}: {os.path.getsize(p)} bytes")

# c09 光山县
c09 = {
  "item_id": "31-001", "volume": "31", "source": "光山县", "region": "河南", "type": "county",
  "original": "光山县【在州西四十五里春秋为国汉为西阳县地属江夏郡晋置光山县刘宋改为光城县寻置光城郡梁置光州隋改县曰光山唐改郡为光州徙治定城县宋改光山为期思县寻复旧元属光州本朝因之编户三十一里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "光山县", "type": "geo", "norm": "光山县", "first_source": "31-001"},
      {"ent_id": "ENT-002", "name": "防龙山", "type": "mtn", "norm": "防龙山", "first_source": "31-001"},
      {"ent_id": "ENT-003", "name": "迎春山", "type": "mtn", "norm": "迎春山", "first_source": "31-001"},
      {"ent_id": "ENT-004", "name": "净居山", "type": "mtn", "norm": "净居山", "first_source": "31-001"},
      {"ent_id": "ENT-005", "name": "仙人山", "type": "mtn", "norm": "仙人山", "first_source": "31-001"},
      {"ent_id": "ENT-006", "name": "杏山", "type": "mtn", "norm": "杏山", "first_source": "31-001"},
      {"ent_id": "ENT-007", "name": "千金山", "type": "mtn", "norm": "千金山", "first_source": "31-001"},
      {"ent_id": "ENT-008", "name": "浮光山", "type": "mtn", "norm": "浮光山", "first_source": "31-001"},
      {"ent_id": "ENT-009", "name": "龙蟠山", "type": "mtn", "norm": "龙蟠山", "first_source": "31-001"},
      {"ent_id": "ENT-010", "name": "白压山", "type": "mtn", "norm": "白压山", "first_source": "31-001"},
      {"ent_id": "ENT-011", "name": "四面山", "type": "mtn", "norm": "四面山", "first_source": "31-001"},
      {"ent_id": "ENT-012", "name": "石盘山", "type": "mtn", "norm": "石盘山", "first_source": "31-001"},
      {"ent_id": "ENT-013", "name": "黑石山", "type": "mtn", "norm": "黑石山", "first_source": "31-001"},
      {"ent_id": "ENT-014", "name": "磨云山", "type": "mtn", "norm": "磨云山", "first_source": "31-001"},
      {"ent_id": "ENT-015", "name": "金泉山", "type": "mtn", "norm": "金泉山", "first_source": "31-001"},
      {"ent_id": "ENT-016", "name": "五马山", "type": "mtn", "norm": "五马山", "first_source": "31-001"},
      {"ent_id": "ENT-017", "name": "春风岭", "type": "mtn", "norm": "春风岭", "first_source": "31-001"},
      {"ent_id": "ENT-018", "name": "官渡河", "type": "mtn", "norm": "官渡河", "first_source": "31-001"},
      {"ent_id": "ENT-019", "name": "临仙河", "type": "mtn", "norm": "临仙河", "first_source": "31-001"},
      {"ent_id": "ENT-020", "name": "寨河", "type": "mtn", "norm": "寨河", "first_source": "31-001"},
      {"ent_id": "ENT-021", "name": "高陌河", "type": "mtn", "norm": "高陌河", "first_source": "31-001"},
      {"ent_id": "ENT-022", "name": "紫水", "type": "mtn", "norm": "紫水", "first_source": "31-001"},
      {"ent_id": "ENT-023", "name": "司马井", "type": "mtn", "norm": "司马井", "first_source": "31-001"},
      {"ent_id": "ENT-024", "name": "西施陂", "type": "mtn", "norm": "西施陂", "first_source": "31-001"},
      {"ent_id": "ENT-025", "name": "茹由故城", "type": "geo", "norm": "茹由故城", "first_source": "31-001"},
      {"ent_id": "ENT-026", "name": "仙居废县", "type": "geo", "norm": "仙居废县", "first_source": "31-001"},
      {"ent_id": "ENT-027", "name": "西阳废县", "type": "geo", "norm": "西阳废县", "first_source": "31-001"},
      {"ent_id": "ENT-028", "name": "黄川故城", "type": "geo", "norm": "黄川故城", "first_source": "31-001"},
      {"ent_id": "ENT-029", "name": "司马光", "type": "person", "norm": "司马光", "first_source": "31-001"},
      {"ent_id": "ENT-030", "name": "司马池", "type": "person", "norm": "司马池", "first_source": "31-001"},
      {"ent_id": "ENT-031", "name": "龚友福", "type": "person", "norm": "龚友福", "first_source": "31-001"},
      {"ent_id": "ENT-032", "name": "唐氏", "type": "person", "norm": "唐氏", "first_source": "31-001"}
    ],
    "geos": [{
      "geo_id": "GEO-31001c09", "item_id": "31-001", "name": "光山县", "type": "county", "region": "河南",
      "parent": "GEO-31001s02", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在州西四十五里", "households": {"count": 31, "unit": "里", "note": "编户三十一里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-001", "geo_id": "GEO-31001c09", "dynasty": "周", "era": None, "institution_name": "弦国", "action": "置", "detail": "春秋为弦国"},
      {"evo_id": "EVO-002", "item_id": "31-001", "geo_id": "GEO-31001c09", "dynasty": "汉", "era": None, "institution_name": "西阳县地", "action": "置", "detail": "汉为西阳县地属江夏郡"},
      {"evo_id": "EVO-003", "item_id": "31-001", "geo_id": "GEO-31001c09", "dynasty": "晋", "era": None, "institution_name": "光山县", "action": "置", "detail": "晋置光山县，刘宋改为光城县，寻置光城郡"},
      {"evo_id": "EVO-004", "item_id": "31-001", "geo_id": "GEO-31001c09", "dynasty": "隋", "era": None, "institution_name": "光山县", "action": "改", "detail": "梁置光州，隋改县曰光山"},
      {"evo_id": "EVO-005", "item_id": "31-001", "geo_id": "GEO-31001c09", "dynasty": "唐", "era": None, "institution_name": "光山县", "action": "因之", "detail": "唐改郡为光州徙治定城县"},
      {"evo_id": "EVO-006", "item_id": "31-001", "geo_id": "GEO-31001c09", "dynasty": "宋", "era": None, "institution_name": "光山县", "action": "复旧", "detail": "宋改光山为期思县寻复旧，元属光州，本朝因之"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "防龙山", "type": "山", "location_text": "在光山县南四十里", "description": "二山并峙如两龙相防", "lore": ""},
      {"mtn_id": "MTN-002", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "迎春山", "type": "山", "location_text": "在光山县南四十里", "description": "山色郁葱至春愈秀", "lore": ""},
      {"mtn_id": "MTN-003", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "净居山", "type": "山", "location_text": "在光山县西南四十五里", "description": "旧有梵元寺", "lore": ""},
      {"mtn_id": "MTN-004", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "仙人山", "type": "山", "location_text": "在光山县南五十里", "description": "上有仙迹", "lore": ""},
      {"mtn_id": "MTN-005", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "杏山", "type": "山", "location_text": "在光山县西六十里", "description": "山有抱朴子仙迹", "lore": ""},
      {"mtn_id": "MTN-006", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "千金山", "type": "山", "location_text": "在光山县东南八十里", "description": "", "lore": ""},
      {"mtn_id": "MTN-007", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "浮光山", "type": "山", "location_text": "在光山县北八十里一名浮弋山即弋阳山也", "description": "奇形伟观未可殚尽，俯映长淮每有光曜，山出名玉及黑石堪为棋子", "lore": ""},
      {"mtn_id": "MTN-008", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "龙蟠山", "type": "山", "location_text": "在光山县南八十里", "description": "以形似名，云兴则雨", "lore": ""},
      {"mtn_id": "MTN-009", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "白压山", "type": "山", "location_text": "在光山县南八十里", "description": "绝顶有洞，洞有古井", "lore": ""},
      {"mtn_id": "MTN-010", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "四面山", "type": "山", "location_text": "在光山县南八十里", "description": "其峰四而相向，流水萦回俨似图画，为光山胜地", "lore": ""},
      {"mtn_id": "MTN-011", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "石盘山", "type": "山", "location_text": "在光山县南九十里", "description": "山势盘旋险峻，山顶平整，旧有塞栅可屯千兵", "lore": ""},
      {"mtn_id": "MTN-012", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "黑石山", "type": "山", "location_text": "在光山县南一百里", "description": "上有黑龙王庙", "lore": ""},
      {"mtn_id": "MTN-013", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "磨云山", "type": "山", "location_text": "在光山县南一百里", "description": "山头云出常旋转凝结不散", "lore": ""},
      {"mtn_id": "MTN-014", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "金泉山", "type": "山", "location_text": "在光山县南一百里", "description": "泉水出而不竭，祷雨辄应", "lore": ""},
      {"mtn_id": "MTN-015", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "五马山", "type": "山", "location_text": "在光山县南一百里", "description": "", "lore": ""},
      {"mtn_id": "MTN-016", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "三山", "type": "山", "location_text": "在光山县南七十里", "description": "以三峰并峙而名", "lore": ""},
      {"mtn_id": "MTN-017", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "春风岭", "type": "岭", "location_text": "在光山县西六十里", "description": "", "lore": ""},
      {"mtn_id": "MTN-018", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "官渡河", "type": "河", "location_text": "在光山县南五里", "description": "源出分水岭，至光州为小黄河，北流合梅林泊陂张师等河及蒋沟磨子港入淮", "lore": ""},
      {"mtn_id": "MTN-019", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "临仙河", "type": "河", "location_text": "在光山县东一十五里", "description": "水自官渡河北流入淮", "lore": ""},
      {"mtn_id": "MTN-020", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "寨河", "type": "河", "location_text": "在光山县北二十五里", "description": "水合清流河北流入淮", "lore": ""},
      {"mtn_id": "MTN-021", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "高陌河", "type": "河", "location_text": "在光山县南四十五里", "description": "源自白压山东流入临仙河", "lore": ""},
      {"mtn_id": "MTN-022", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "紫水", "type": "河", "location_text": "在光山县", "description": "源出仙居山", "lore": ""},
      {"mtn_id": "MTN-023", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "司马井", "type": "井", "location_text": "在光山县学内", "description": "世传宋司马光生时汲井水以浴之因名，上有亭", "lore": ""},
      {"mtn_id": "MTN-024", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "西施陂", "type": "陂", "location_text": "在光山县南八里", "description": "唐永徽中刺史裴大觉开陂溉田，号曰雨施", "lore": ""}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "司马池", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "知光山县", "summary": "天禧中知光山县，于民有信，事不俟催促而集；光生于此"},
      {"per_id": "PER-002", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "司马光", "type": "人物", "dynasty": "宋", "native_place": "光山", "office": "温国公", "summary": "父池为光山令时生光于此，后人构书堂祀之；元敕修祠"},
      {"per_id": "PER-003", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "龚友福", "type": "人物", "dynasty": "元", "native_place": "光山", "office": "中书参政", "summary": "仕为翰林学士，拜中书参政兼丞相事，号淮南夫子"},
      {"per_id": "PER-004", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "唐氏", "type": "列女", "dynasty": "明", "native_place": "光山", "office": "孝女", "summary": "性烈，葬父见冢不高，自用裙幅包土以封，人以孝女称，今有孝女墓"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "光山县学", "type": "学校", "location_text": "在县治西", "history_lore": "洪武七年因元旧址重建"},
      {"site_id": "SITE-002", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "洓水书院", "type": "书院", "location_text": "在光山县治西", "history_lore": "洓水先生宋司马光号也，光父池为光山令时生光于此，后人因构书堂祀光，本朝正统九年重修"},
      {"site_id": "SITE-003", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "尊经阁", "type": "宫室", "location_text": "在光山县学", "history_lore": "本朝正统十年建"},
      {"site_id": "SITE-004", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "柴亭", "type": "宫室", "location_text": "在光山县", "history_lore": "宋建"},
      {"site_id": "SITE-005", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "五关", "type": "关梁", "location_text": "在光山县西南", "history_lore": "曰白沙土门斗木岭黄土岭修善冲，宋绍兴间江州都统赵廞建"},
      {"site_id": "SITE-006", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "木陵关", "type": "关梁", "location_text": "在光山县南一百三十二里", "history_lore": "齐陈接境齐置此关，隋废"},
      {"site_id": "SITE-007", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "司马温公庙", "type": "祠庙", "location_text": "在光山县治西", "history_lore": "温公宋司马光也，洪武六年重建"},
      {"site_id": "SITE-008", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "司马池墓", "type": "陵墓", "location_text": "在光山县西南", "history_lore": ""},
      {"site_id": "SITE-009", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "茹由故城", "type": "古迹", "location_text": "在光山县南六十里", "history_lore": "晋安帝置县"},
      {"site_id": "SITE-010", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "仙居废县", "type": "古迹", "location_text": "在光山县", "history_lore": "本梁宋安县，隋废，唐初复置后更名仙居，宋省入光山"},
      {"site_id": "SITE-011", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "西阳废县", "type": "古迹", "location_text": "在光山县西二十里", "history_lore": "汉置县属江夏郡，晋弋阳郡治此"},
      {"site_id": "SITE-012", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "黄川故城", "type": "古迹", "location_text": "在光山县", "history_lore": "旧为郡，梁废"}
    ],
    "prods": [
      {"prod_id": "PROD-001", "item_id": "31-001", "geo_id": "GEO-31001c09", "name": "棋子石", "category": "矿", "location_text": "光山出"}
    ],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
dump("31-001_c09_光山县.json", c09)

print("DONE c09")
