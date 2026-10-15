# -*- coding: utf-8 -*-
"""Generate vol31 c07 罗山, c08 确山."""
import json, os
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol31"

def dump(name, obj):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  {name}: {os.path.getsize(p)} bytes")

# c07 罗山县
c07 = {
  "item_id": "31-001", "volume": "31", "source": "罗山县", "region": "河南", "type": "county",
  "original": "罗山县【在府城南一百四十里春秋时蔡地战国时为楚地秦属颍川郡汉为鄳县属江夏郡晋属汝南郡北齐置髙安县隋初罢后复置改为罗山县唐初置南维州寻罢州以县属申州宋初省入义阳复复置属信阳军元属信阳州后迁州于故县以县治移于西南即今所也本朝因之编户二十里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "罗山县", "type": "geo", "norm": "罗山县", "first_source": "31-001"},
      {"ent_id": "ENT-002", "name": "鹊山", "type": "mtn", "norm": "鹊山", "first_source": "31-001"},
      {"ent_id": "ENT-003", "name": "罗山", "type": "mtn", "norm": "罗山", "first_source": "31-001"},
      {"ent_id": "ENT-004", "name": "子路山", "type": "mtn", "norm": "子路山", "first_source": "31-001"},
      {"ent_id": "ENT-005", "name": "小确山", "type": "mtn", "norm": "小确山", "first_source": "31-001"},
      {"ent_id": "ENT-006", "name": "大确山", "type": "mtn", "norm": "大确山", "first_source": "31-001"},
      {"ent_id": "ENT-007", "name": "牢山", "type": "mtn", "norm": "牢山", "first_source": "31-001"},
      {"ent_id": "ENT-008", "name": "灵山", "type": "mtn", "norm": "灵山", "first_source": "31-001"},
      {"ent_id": "ENT-009", "name": "六斗山", "type": "mtn", "norm": "六斗山", "first_source": "31-001"},
      {"ent_id": "ENT-010", "name": "仙居山", "type": "mtn", "norm": "仙居山", "first_source": "31-001"},
      {"ent_id": "ENT-011", "name": "转山湖", "type": "mtn", "norm": "转山湖", "first_source": "31-001"},
      {"ent_id": "ENT-012", "name": "竹竿河", "type": "mtn", "norm": "竹竿河", "first_source": "31-001"},
      {"ent_id": "ENT-013", "name": "九重关", "type": "geo", "norm": "九重关", "first_source": "31-001"},
      {"ent_id": "ENT-014", "name": "张庸", "type": "person", "norm": "张庸", "first_source": "31-001"},
      {"ent_id": "ENT-015", "name": "蒋良辅", "type": "person", "norm": "蒋良辅", "first_source": "31-001"},
      {"ent_id": "ENT-016", "name": "徐廷璋", "type": "person", "norm": "徐廷璋", "first_source": "31-001"},
      {"ent_id": "ENT-017", "name": "郑氏", "type": "person", "norm": "郑氏", "first_source": "31-001"}
    ],
    "geos": [{
      "geo_id": "GEO-31001c07", "item_id": "31-001", "name": "罗山县", "type": "county", "region": "河南",
      "parent": "GEO-31001s01", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在府城南一百四十里", "households": {"count": 20, "unit": "里", "note": "编户二十里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-001", "geo_id": "GEO-31001c07", "dynasty": "周", "era": None, "institution_name": "蔡地/楚地", "action": "置", "detail": "春秋时蔡地，战国时为楚地"},
      {"evo_id": "EVO-002", "item_id": "31-001", "geo_id": "GEO-31001c07", "dynasty": "汉", "era": None, "institution_name": "鄳县", "action": "置", "detail": "汉为鄳县属江夏郡，晋属汝南郡"},
      {"evo_id": "EVO-003", "item_id": "31-001", "geo_id": "GEO-31001c07", "dynasty": "南北朝", "era": "北齐", "institution_name": "高安县/罗山县", "action": "改", "detail": "北齐置高安县，隋初罢后复置改为罗山县"},
      {"evo_id": "EVO-004", "item_id": "31-001", "geo_id": "GEO-31001c07", "dynasty": "唐", "era": None, "institution_name": "罗山县", "action": "因之", "detail": "唐初置南维州寻罢州以县属申州"},
      {"evo_id": "EVO-005", "item_id": "31-001", "geo_id": "GEO-31001c07", "dynasty": "元", "era": None, "institution_name": "罗山县", "action": "迁治", "detail": "宋初省入义阳复置属信阳军，元属信阳州，后迁州于故县以县治移于西南即今所也，本朝因之"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "鹊山", "type": "山", "location_text": "在罗山县南九里", "description": "山水清秀为一县奇观，俗传昔有群鹊栖此山，遇风雨鹊必先群噪故名", "lore": ""},
      {"mtn_id": "MTN-002", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "罗山", "type": "山", "location_text": "在罗山县西南一十里", "description": "峰峦环抱，隋因山名县", "lore": ""},
      {"mtn_id": "MTN-003", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "子路山", "type": "山", "location_text": "在罗山县西南四十五里", "description": "", "lore": ""},
      {"mtn_id": "MTN-004", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "小确山", "type": "山", "location_text": "在罗山县西南七十里", "description": "", "lore": ""},
      {"mtn_id": "MTN-005", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "大确山", "type": "山", "location_text": "在罗山县南七十九里", "description": "", "lore": ""},
      {"mtn_id": "MTN-006", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "牢山", "type": "山", "location_text": "在罗山县东南九十里", "description": "层峦叠嶂势极险峻", "lore": ""},
      {"mtn_id": "MTN-007", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "灵山", "type": "山", "location_text": "在罗山县西南一百四十里", "description": "视众山最高，云兴则雨，旧名霸山", "lore": ""},
      {"mtn_id": "MTN-008", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "六斗山", "type": "山", "location_text": "在罗山县西南一百九十里", "description": "六峰如南斗形", "lore": ""},
      {"mtn_id": "MTN-009", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "仙居山", "type": "山", "location_text": "在罗山县南二百三十里", "description": "昔有人于此得道故名，旧尝以此山名县", "lore": ""},
      {"mtn_id": "MTN-010", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "转山湖", "type": "湖", "location_text": "在罗山县治南", "description": "水绕山下", "lore": ""},
      {"mtn_id": "MTN-011", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "竹竿河", "type": "河", "location_text": "在罗山县东三十里", "description": "源出窟垅山，比流合伞柄羊马二河入淮", "lore": ""}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "蒋良辅", "type": "名宦", "dynasty": "明", "native_place": "", "office": "罗山知县", "summary": "凡有科差量户贫富多寡适均，民有争讼以至公断之，修举废坠不劳民伤财"},
      {"per_id": "PER-002", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "徐廷璋", "type": "人物", "dynasty": "明", "native_place": "罗山", "office": "右副都御史", "summary": "由进士除工科给事中，言论侃侃不避权贵，累官右副都御史"},
      {"per_id": "PER-003", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "郑氏", "type": "列女", "dynasty": "元", "native_place": "罗山", "office": "李思齐妾", "summary": "元末汝颍兵起，思齐卒，郑氏自经死，事闻追赠淑人谥曰贞烈"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "罗山县学", "type": "学校", "location_text": "在县治东北", "history_lore": "洪武四年因元旧址重建"},
      {"site_id": "SITE-002", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "御书楼", "type": "宫室", "location_text": "在罗山县学内", "history_lore": "本朝建以藏颁赐书籍"},
      {"site_id": "SITE-003", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "九重关", "type": "关梁", "location_text": "在罗山县西南一百二十里", "history_lore": "即古黄岘关"},
      {"site_id": "SITE-004", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "破关", "type": "关梁", "location_text": "在罗山县南一百二十里", "history_lore": ""},
      {"site_id": "SITE-005", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "大胜关", "type": "关梁", "location_text": "在罗山县南一百四十里", "history_lore": ""},
      {"site_id": "SITE-006", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "白胜寺", "type": "寺观", "location_text": "在罗山县治东北", "history_lore": "相传为楚白公胜别业，洪武中因旧重建"},
      {"site_id": "SITE-007", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "高安城", "type": "古迹", "location_text": "在罗山县西南一百里", "history_lore": "北齐县，隋初废"},
      {"site_id": "SITE-008", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "𫑡县城", "type": "古迹", "location_text": "在废仙居县北四十里", "history_lore": "汉置属江夏郡，惠帝封黎朱仓为侯即此，晋属弋阳郡"}
    ],
    "prods": [
      {"prod_id": "PROD-001", "item_id": "31-001", "geo_id": "GEO-31001c07", "name": "茶", "category": "茶", "location_text": "罗山县出"}
    ],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
dump("31-001_c07_罗山县.json", c07)

# c08 确山县
c08 = {
  "item_id": "31-001", "volume": "31", "source": "确山县", "region": "河南", "type": "county",
  "original": "确山县【在府城西五十里本春秋江国汉为安昌县地属汝南郡东汉末置朗山县晋改曰安昌梁属陈州后魏移县治朗陵故城属初安郡隋初复移县治今所属豫州仍改为朗山县唐属蔡州宋改为确山县金元因之本朝初省入汝阳洪武十四年复置编户二十一里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "确山县", "type": "geo", "norm": "确山县", "first_source": "31-001"},
      {"ent_id": "ENT-002", "name": "蟠山", "type": "mtn", "norm": "蟠山", "first_source": "31-001"},
      {"ent_id": "ENT-003", "name": "二浪山", "type": "mtn", "norm": "二浪山", "first_source": "31-001"},
      {"ent_id": "ENT-004", "name": "确山", "type": "mtn", "norm": "确山", "first_source": "31-001"},
      {"ent_id": "ENT-005", "name": "秀山", "type": "mtn", "norm": "秀山", "first_source": "31-001"},
      {"ent_id": "ENT-006", "name": "大仪山", "type": "mtn", "norm": "大仪山", "first_source": "31-001"},
      {"ent_id": "ENT-007", "name": "乐山", "type": "mtn", "norm": "乐山", "first_source": "31-001"},
      {"ent_id": "ENT-008", "name": "金顶山", "type": "mtn", "norm": "金顶山", "first_source": "31-001"},
      {"ent_id": "ENT-009", "name": "朗陵山", "type": "mtn", "norm": "朗陵山", "first_source": "31-001"},
      {"ent_id": "ENT-010", "name": "马鹿山", "type": "mtn", "norm": "马鹿山", "first_source": "31-001"},
      {"ent_id": "ENT-011", "name": "黄酉湖", "type": "mtn", "norm": "黄酉湖", "first_source": "31-001"},
      {"ent_id": "ENT-012", "name": "沙河", "type": "mtn", "norm": "沙河", "first_source": "31-001"},
      {"ent_id": "ENT-013", "name": "朗陵故城", "type": "geo", "norm": "朗陵故城", "first_source": "31-001"},
      {"ent_id": "ENT-014", "name": "道城", "type": "geo", "norm": "道城", "first_source": "31-001"},
      {"ent_id": "ENT-015", "name": "四望城", "type": "geo", "norm": "四望城", "first_source": "31-001"},
      {"ent_id": "ENT-016", "name": "沈义", "type": "person", "norm": "沈义", "first_source": "31-001"},
      {"ent_id": "ENT-017", "name": "鲁有开", "type": "person", "norm": "鲁有开", "first_source": "31-001"},
      {"ent_id": "ENT-018", "name": "张熹", "type": "person", "norm": "张熹", "first_source": "31-001"}
    ],
    "geos": [{
      "geo_id": "GEO-31001c08", "item_id": "31-001", "name": "确山县", "type": "county", "region": "河南",
      "parent": "GEO-31001s01", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在府城西五十里", "households": {"count": 21, "unit": "里", "note": "编户二十一里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-001", "geo_id": "GEO-31001c08", "dynasty": "周", "era": None, "institution_name": "江国", "action": "置", "detail": "本春秋江国"},
      {"evo_id": "EVO-002", "item_id": "31-001", "geo_id": "GEO-31001c08", "dynasty": "汉", "era": None, "institution_name": "安昌县地", "action": "置", "detail": "汉为安昌县地属汝南郡"},
      {"evo_id": "EVO-003", "item_id": "31-001", "geo_id": "GEO-31001c08", "dynasty": "南北朝", "era": None, "institution_name": "朗山县", "action": "改", "detail": "东汉末置朗山县，晋改曰安昌，后魏移县治朗陵故城属初安郡，隋仍改为朗山县"},
      {"evo_id": "EVO-004", "item_id": "31-001", "geo_id": "GEO-31001c08", "dynasty": "宋", "era": None, "institution_name": "确山县", "action": "改", "detail": "唐属蔡州，宋改为确山县，金元因之"},
      {"evo_id": "EVO-005", "item_id": "31-001", "geo_id": "GEO-31001c08", "dynasty": "明", "era": "洪武", "institution_name": "确山县", "action": "复置", "detail": "本朝初省入汝阳，洪武十四年复置"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "蟠山", "type": "山", "location_text": "在确山县南二里", "description": "蟠绕县城，其形如龙", "lore": ""},
      {"mtn_id": "MTN-002", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "二浪山", "type": "山", "location_text": "在确山县西南一里", "description": "山上有二浪庙", "lore": ""},
      {"mtn_id": "MTN-003", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "确山", "type": "山", "location_text": "在确山县南一十里", "description": "世传晋何曾见山有臼杵自动有声，取之不出寻失其所", "lore": ""},
      {"mtn_id": "MTN-004", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "秀山", "type": "山", "location_text": "在确山县西北一十里", "description": "飞烟积翠视诸山特秀", "lore": ""},
      {"mtn_id": "MTN-005", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "大仪山", "type": "山", "location_text": "在确山县西南一十五里", "description": "", "lore": ""},
      {"mtn_id": "MTN-006", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "独山/惊牛山/黄山", "type": "山", "location_text": "俱在确山县东南二十五里", "description": "山势联属其名各殊", "lore": ""},
      {"mtn_id": "MTN-007", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "乐山", "type": "山", "location_text": "在确山县西北四十里一名朗山", "description": "避宋讳改今名，山顶有池名皓月池，中生四季莲花可供游赏", "lore": ""},
      {"mtn_id": "MTN-008", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "金顶山", "type": "山", "location_text": "在确山县西四十里", "description": "一名马鞍，上多绯云紫雾盘旋不绝", "lore": ""},
      {"mtn_id": "MTN-009", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "朗陵山", "type": "山", "location_text": "在确山县南四十里一名大明山", "description": "下有朗陵城，汉末因山名县", "lore": ""},
      {"mtn_id": "MTN-010", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "三山", "type": "山", "location_text": "在确山县南五十里", "description": "以三峰并峙而名", "lore": ""},
      {"mtn_id": "MTN-011", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "马鹿山", "type": "山", "location_text": "在确山县西南五十里", "description": "", "lore": ""},
      {"mtn_id": "MTN-012", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "黄酉湖", "type": "湖", "location_text": "在确山县北三十五里", "description": "源出乐山东流合断济练家二河入汝水", "lore": ""},
      {"mtn_id": "MTN-013", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "沙河", "type": "河", "location_text": "在确山县南四十五里一名吴寨河", "description": "源出桐柏山东流合三里河入汝水", "lore": ""}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "鲁有开", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "知确山县", "summary": "大姓把持官政，有开治其最甚者遂以无事，兴废陂溉田数千顷，富弼守蔡荐之"},
      {"per_id": "PER-002", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "沈义", "type": "名宦", "dynasty": "明", "native_place": "", "office": "确山知县", "summary": "洪武间确山知县，操守清介好尚儒雅，兴学劝农爱民如子，不一年风气和洽风俗淳美"},
      {"per_id": "PER-003", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "张熹", "type": "名宦", "dynasty": "汉", "native_place": "", "office": "平舆令", "summary": "汉平舆令，祷旱焚身而雨，后人感而祀之"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "确山县学", "type": "学校", "location_text": "在县治东", "history_lore": "洪武十四年因宋旧址重建"},
      {"site_id": "SITE-002", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "三里桥/杨村桥", "type": "关梁", "location_text": "俱在确山县北", "history_lore": ""},
      {"site_id": "SITE-003", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "北泉寺", "type": "寺观", "location_text": "在确山县西北一十五里", "history_lore": "唐名资福，即叛臣李希烈害颜真卿处，本朝洪武中重修"},
      {"site_id": "SITE-004", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "白云观", "type": "寺观", "location_text": "在确山县东五里", "history_lore": "宣德初因元旧址重建"},
      {"site_id": "SITE-005", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "张明府庙", "type": "祠庙", "location_text": "在确山县北", "history_lore": "汉平舆令张熹祷旱焚身而雨，后人感而祀之"},
      {"site_id": "SITE-006", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "灵应庙", "type": "祠庙", "location_text": "在确山县西北三十里朗山", "history_lore": "有碑，俗传汉相陈平主之，宋崇宁初赐额，水旱祷之有应"},
      {"site_id": "SITE-007", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "高皇台", "type": "台", "location_text": "一在确山县东南四十里", "history_lore": "世传汉高祖筑"},
      {"site_id": "SITE-008", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "朗陵故城", "type": "古迹", "location_text": "在确山县西南三十五里", "history_lore": "汉置县，晋封何曾为朗陵公即此"},
      {"site_id": "SITE-009", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "道城", "type": "古迹", "location_text": "在确山县北", "history_lore": "即春秋道国地"},
      {"site_id": "SITE-010", "item_id": "31-001", "geo_id": "GEO-31001c08", "name": "四望城", "type": "古迹", "location_text": "在确山县东南", "history_lore": "后魏王肃于四望陂南筑之以御梁"}
    ],
    "prods": [],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
dump("31-001_c08_确山县.json", c08)

print("DONE c07-c08")
