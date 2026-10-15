# -*- coding: utf-8 -*-
"""Generate vol31 汝州 4 counties: c01鲁山 c02郏县 c03宝丰 c04伊阳."""
import json, os
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol31"

def dump(name, obj):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  {name}: {os.path.getsize(p)} bytes")

# c01 鲁山县
c01 = {
  "item_id": "31-002", "volume": "31", "source": "鲁山县", "region": "河南", "type": "county",
  "original": "鲁山县【在州南一百二十里夏后时刘累醢龙惧罪迁于鲁即此春秋时为郑邑汉为鲁阳县属南阳郡三国魏为广州晋复置县属南阳国后魏置鲁阳郡又置鲁州隋初郡废大业初废州为鲁县属防城郡唐初复置鲁州改县曰鲁山贞观中州废以滍阳县省入鲁山属汝州宋元仍旧本朝因之编户二十三里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "鲁山县", "type": "geo", "norm": "鲁山县", "first_source": "31-002"},
      {"ent_id": "ENT-002", "name": "大盂山", "type": "mtn", "norm": "大盂山", "first_source": "31-002"},
      {"ent_id": "ENT-003", "name": "鲁山", "type": "mtn", "norm": "鲁山", "first_source": "31-002"},
      {"ent_id": "ENT-004", "name": "尧山", "type": "mtn", "norm": "尧山", "first_source": "31-002"},
      {"ent_id": "ENT-005", "name": "扶安山", "type": "mtn", "norm": "扶安山", "first_source": "31-002"},
      {"ent_id": "ENT-006", "name": "黑山", "type": "mtn", "norm": "黑山", "first_source": "31-002"},
      {"ent_id": "ENT-007", "name": "吴大岭", "type": "mtn", "norm": "吴大岭", "first_source": "31-002"},
      {"ent_id": "ENT-008", "name": "清水河", "type": "mtn", "norm": "清水河", "first_source": "31-002"},
      {"ent_id": "ENT-009", "name": "秋河", "type": "mtn", "norm": "秋河", "first_source": "31-002"},
      {"ent_id": "ENT-010", "name": "当齐河", "type": "mtn", "norm": "当齐河", "first_source": "31-002"},
      {"ent_id": "ENT-011", "name": "琴台", "type": "geo", "norm": "琴台", "first_source": "31-002"},
      {"ent_id": "ENT-012", "name": "鲁阳城", "type": "geo", "norm": "鲁阳城", "first_source": "31-002"},
      {"ent_id": "ENT-013", "name": "犨城", "type": "geo", "norm": "犨城", "first_source": "31-002"},
      {"ent_id": "ENT-014", "name": "平皋城", "type": "geo", "norm": "平皋城", "first_source": "31-002"},
      {"ent_id": "ENT-015", "name": "元结", "type": "person", "norm": "元结", "first_source": "31-002"},
      {"ent_id": "ENT-016", "name": "牛皋", "type": "person", "norm": "牛皋", "first_source": "31-002"},
      {"ent_id": "ENT-017", "name": "王义", "type": "person", "norm": "王义", "first_source": "31-002"},
      {"ent_id": "ENT-018", "name": "王文政", "type": "person", "norm": "王文政", "first_source": "31-002"},
      {"ent_id": "ENT-019", "name": "俞永", "type": "person", "norm": "俞永", "first_source": "31-002"},
      {"ent_id": "ENT-020", "name": "张钊", "type": "person", "norm": "张钊", "first_source": "31-002"},
      {"ent_id": "ENT-021", "name": "邓顺", "type": "person", "norm": "邓顺", "first_source": "31-002"}
    ],
    "geos": [{
      "geo_id": "GEO-31002c01", "item_id": "31-002", "name": "鲁山县", "type": "county", "region": "河南",
      "parent": "GEO-31002", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在州南一百二十里", "households": {"count": 23, "unit": "里", "note": "编户二十三里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-002", "geo_id": "GEO-31002c01", "dynasty": "夏", "era": None, "institution_name": "刘累迁鲁", "action": "置", "detail": "夏后时刘累醢龙惧罪迁于鲁即此"},
      {"evo_id": "EVO-002", "item_id": "31-002", "geo_id": "GEO-31002c01", "dynasty": "汉", "era": None, "institution_name": "鲁阳县", "action": "置", "detail": "春秋时为郑邑，汉为鲁阳县属南阳郡"},
      {"evo_id": "EVO-003", "item_id": "31-002", "geo_id": "GEO-31002c01", "dynasty": "南北朝", "era": "后魏", "institution_name": "鲁阳郡/鲁州", "action": "置", "detail": "后魏置鲁阳郡又置鲁州"},
      {"evo_id": "EVO-004", "item_id": "31-002", "geo_id": "GEO-31002c01", "dynasty": "隋", "era": None, "institution_name": "鲁县", "action": "废州", "detail": "隋初郡废，大业初废州为鲁县属防城郡"},
      {"evo_id": "EVO-005", "item_id": "31-002", "geo_id": "GEO-31002c01", "dynasty": "唐", "era": "贞观", "institution_name": "鲁山县", "action": "改", "detail": "唐初复置鲁州改县曰鲁山，贞观中州废以滍阳县省入鲁山属汝州"},
      {"evo_id": "EVO-006", "item_id": "31-002", "geo_id": "GEO-31002c01", "dynasty": "明", "era": None, "institution_name": "鲁山县", "action": "因之", "detail": "宋元仍旧，本朝因之"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "大盂山", "type": "山", "location_text": "在鲁山县西南七十里", "description": "山顶并窊四围若城，俗呼为大团城小团城山", "lore": ""},
      {"mtn_id": "MTN-002", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "鲁山", "type": "山", "location_text": "在鲁山县东一百八十里一名露山", "description": "高出群山为一邑巨镇，因以名县，山顶有瑞云观", "lore": ""},
      {"mtn_id": "MTN-003", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "尧山", "type": "山", "location_text": "在鲁山县西", "description": "滍水所出，昔尧之末孙刘累以豢龙事夏后，后惧罪迁于鲁，立尧祠于此因名尧山", "lore": ""},
      {"mtn_id": "MTN-004", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "扶安山", "type": "山", "location_text": "在鲁山县东南五十里", "description": "上有唐秦王庙，世传秦王驻马于此", "lore": ""},
      {"mtn_id": "MTN-005", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "黑山", "type": "山", "location_text": "在鲁山县南二十五里", "description": "相传汉光武经此值日昏暮因名；又西北三十里有明山，谓光武经此遇天晴明因以为名", "lore": ""},
      {"mtn_id": "MTN-006", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "吴大岭", "type": "岭", "location_text": "在鲁山县西九十里", "description": "", "lore": ""},
      {"mtn_id": "MTN-007", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "清水河", "type": "河", "location_text": "在鲁山县东二十里", "description": "源自赤城村东流入沙河", "lore": ""},
      {"mtn_id": "MTN-008", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "秋河", "type": "河", "location_text": "在鲁山县南五十里", "description": "源自杨家林，流经宝丰县界合沙河", "lore": ""},
      {"mtn_id": "MTN-009", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "当齐河", "type": "河", "location_text": "在鲁山县西三十里", "description": "发源焦山北流至竹岭村达沙河", "lore": ""}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "元结", "type": "人物", "dynasty": "唐", "native_place": "鲁山", "office": "道州刺史", "summary": "少聪悟宏达倜傥不羁，撰大唐中兴颂刻于浯溪"},
      {"per_id": "PER-002", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "牛皋", "type": "人物", "dynasty": "宋", "native_place": "汝州鲁山", "office": "捧日天武四厢指挥使", "summary": "初为射士，战败金人，后为岳飞部将，复随州襄阳擒杨么"},
      {"per_id": "PER-003", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "王义", "type": "名宦", "dynasty": "元", "native_place": "", "office": "鲁山尹", "summary": "至元间守鲁山，兴废补弊抑强扶弱，以清介著名"},
      {"per_id": "PER-004", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "王文政", "type": "名宦", "dynasty": "元", "native_place": "", "office": "鲁山尹", "summary": "至元中为鲁山尹，发奸擿伏政令一新，课农劝士惠政及民，及去邑人为立去思碑"},
      {"per_id": "PER-005", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "俞永", "type": "名宦", "dynasty": "明", "native_place": "", "office": "知鲁山县", "summary": "洪武中知鲁山县，首革吏弊修举学校，亲为诸生讲说经史正句读校文理，士风翕然以盛"},
      {"per_id": "PER-006", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "张钊", "type": "名宦", "dynasty": "明", "native_place": "", "office": "知鲁山县", "summary": "宣德初知鲁山县，询民隐抚流亡劝耕桑均赋役，民用富足"},
      {"per_id": "PER-007", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "邓顺", "type": "人物", "dynasty": "元", "native_place": "鲁山", "office": "礼部侍郎", "summary": "举进士博学有治才，仕至礼部侍郎"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "鲁山县学", "type": "学校", "location_text": "在县治东南", "history_lore": "元建，本朝洪武八年重建"},
      {"site_id": "SITE-002", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "琴台", "type": "台", "location_text": "在鲁山县", "history_lore": "唐元紫芝建，颜真卿有文，前贤题咏甚多；金赵秉文为书琴台二字刻于石，元好问诗千山为公台万籁为公琴"},
      {"site_id": "SITE-003", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "歇马岭关", "type": "关梁", "location_text": "在鲁山县西北八十里", "history_lore": "相传汉光武歇马于此故名"},
      {"site_id": "SITE-004", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "三里桥", "type": "关梁", "location_text": "在鲁山县三里河上", "history_lore": ""},
      {"site_id": "SITE-005", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "董家桥", "type": "关梁", "location_text": "在鲁山县东南四里", "history_lore": ""},
      {"site_id": "SITE-006", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "观音寺", "type": "寺观", "location_text": "在鲁山县治东北", "history_lore": "元至正间建"},
      {"site_id": "SITE-007", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "润国寺", "type": "寺观", "location_text": "在鲁山县城外", "history_lore": "隋开皇中建"},
      {"site_id": "SITE-008", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "大觉寺", "type": "寺观", "location_text": "在鲁山县城外", "history_lore": "洪武二年建"},
      {"site_id": "SITE-009", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "南华观", "type": "寺观", "location_text": "在鲁山县治东南", "history_lore": "元至正中建"},
      {"site_id": "SITE-010", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "八蜡庙", "type": "祠庙", "location_text": "在鲁山县东关", "history_lore": ""},
      {"site_id": "SITE-011", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "三圣庙", "type": "祠庙", "location_text": "在鲁山县孙村保", "history_lore": "祀尧舜禹三圣"},
      {"site_id": "SITE-012", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "汉寿亭侯庙", "type": "祠庙", "location_text": "在鲁山县西北", "history_lore": "洪武末重建"},
      {"site_id": "SITE-013", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "鲁阳公墓", "type": "陵墓", "location_text": "在鲁山县二十五里", "history_lore": "墓有石碑止存四字"},
      {"site_id": "SITE-014", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "元结墓", "type": "陵墓", "location_text": "在鲁山县北青条岭陂泉之原", "history_lore": "葬唐元结，有颜真卿所书碑碣"},
      {"site_id": "SITE-015", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "鲁阳城", "type": "古迹", "location_text": "在鲁山县治南", "history_lore": "古鲁县，夏时刘累迁此，汉为鲁阳县"},
      {"site_id": "SITE-016", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "绕角城", "type": "古迹", "location_text": "在鲁山县东南", "history_lore": "左传晋师遁于绕角"},
      {"site_id": "SITE-017", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "犨城", "type": "古迹", "location_text": "在鲁山县东南", "history_lore": "汉县属南阳郡，隋曰犨城县属襄城郡"},
      {"site_id": "SITE-018", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "平皋城", "type": "古迹", "location_text": "在鲁山县", "history_lore": "后周筑于三鸦镇以御寇"}
    ],
    "prods": [
      {"prod_id": "PROD-001", "item_id": "31-002", "geo_id": "GEO-31002c01", "name": "石炭", "category": "矿", "location_text": "鲁山县出"}
    ],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
dump("31-002_c01_鲁山县.json", c01)

print("DONE c01")
