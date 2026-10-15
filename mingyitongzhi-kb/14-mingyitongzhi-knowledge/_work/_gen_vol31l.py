# -*- coding: utf-8 -*-
"""Generate vol31 汝州 c02郏县 c03宝丰 c04伊阳."""
import json, os
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol31"

def dump(name, obj):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  {name}: {os.path.getsize(p)} bytes")

# c02 郏县
c02 = {
  "item_id": "31-002", "volume": "31", "source": "郏县", "region": "河南", "type": "county",
  "original": "郏县【在州东九十里春秋时郑地后为楚边邑战国属韩汉置郏县属頴州郡东汉省三国魏复置后魏改龙山县属襄城郡东魏以县置顺阳郡隋初改龙山为汝南县寻改辅城县属汝州大业中又改郏城县以期城县省入唐因之宋属许州金属汝州元初省入梁县后复置郏县本朝因之编户四十四里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "郏县", "type": "geo", "norm": "郏县", "first_source": "31-002"},
      {"ent_id": "ENT-002", "name": "峨眉山", "type": "mtn", "norm": "峨眉山", "first_source": "31-002"},
      {"ent_id": "ENT-003", "name": "凤翅山", "type": "mtn", "norm": "凤翅山", "first_source": "31-002"},
      {"ent_id": "ENT-004", "name": "紫云山", "type": "mtn", "norm": "紫云山", "first_source": "31-002"},
      {"ent_id": "ENT-005", "name": "大刘山", "type": "mtn", "norm": "大刘山", "first_source": "31-002"},
      {"ent_id": "ENT-006", "name": "长桥河", "type": "mtn", "norm": "长桥河", "first_source": "31-002"},
      {"ent_id": "ENT-007", "name": "三苏祠", "type": "geo", "norm": "三苏祠", "first_source": "31-002"},
      {"ent_id": "ENT-008", "name": "二苏墓", "type": "geo", "norm": "二苏墓", "first_source": "31-002"},
      {"ent_id": "ENT-009", "name": "苏轼", "type": "person", "norm": "苏轼", "first_source": "31-002"},
      {"ent_id": "ENT-010", "name": "苏辙", "type": "person", "norm": "苏辙", "first_source": "31-002"},
      {"ent_id": "ENT-011", "name": "苏过", "type": "person", "norm": "苏过", "first_source": "31-002"},
      {"ent_id": "ENT-012", "name": "范士衡", "type": "person", "norm": "范士衡", "first_source": "31-002"},
      {"ent_id": "ENT-013", "name": "杜思进", "type": "person", "norm": "杜思进", "first_source": "31-002"},
      {"ent_id": "ENT-014", "name": "傅子荣", "type": "person", "norm": "傅子荣", "first_source": "31-002"},
      {"ent_id": "ENT-015", "name": "王玺", "type": "person", "norm": "王玺", "first_source": "31-002"},
      {"ent_id": "ENT-016", "name": "张鉴", "type": "person", "norm": "张鉴", "first_source": "31-002"},
      {"ent_id": "ENT-017", "name": "袁恺", "type": "person", "norm": "袁恺", "first_source": "31-002"},
      {"ent_id": "ENT-018", "name": "李希颜", "type": "person", "norm": "李希颜", "first_source": "31-002"}
    ],
    "geos": [{
      "geo_id": "GEO-31002c02", "item_id": "31-002", "name": "郏县", "type": "county", "region": "河南",
      "parent": "GEO-31002", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在州东九十里", "households": {"count": 44, "unit": "里", "note": "编户四十四里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-002", "geo_id": "GEO-31002c02", "dynasty": "周", "era": None, "institution_name": "郑地/楚边邑", "action": "置", "detail": "春秋时郑地，后为楚边邑，战国属韩"},
      {"evo_id": "EVO-002", "item_id": "31-002", "geo_id": "GEO-31002c02", "dynasty": "汉", "era": None, "institution_name": "郏县", "action": "置", "detail": "汉置郏县属颍川郡，东汉省"},
      {"evo_id": "EVO-003", "item_id": "31-002", "geo_id": "GEO-31002c02", "dynasty": "南北朝", "era": "后魏", "institution_name": "龙山县/辅城县", "action": "改", "detail": "三国魏复置，后魏改龙山县属襄城郡，东魏以县置顺阳郡；隋初改龙山为汝南县寻改辅城县属汝州"},
      {"evo_id": "EVO-004", "item_id": "31-002", "geo_id": "GEO-31002c02", "dynasty": "隋", "era": "大业", "institution_name": "郏城县", "action": "改", "detail": "大业中又改郏城县，以期城县省入"},
      {"evo_id": "EVO-005", "item_id": "31-002", "geo_id": "GEO-31002c02", "dynasty": "元", "era": None, "institution_name": "郏县", "action": "复置", "detail": "宋属许州，金属汝州，元初省入梁县后复置郏县，本朝因之"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "峨眉山", "type": "山", "location_text": "在郏县西北三十五里", "description": "与扈阳山相近，下有广庆寺，寺内有三苏祠", "lore": ""},
      {"mtn_id": "MTN-002", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "凤翅山", "type": "山", "location_text": "在郏县西北四十里", "description": "以形似名，上有灵泉祷雨有应", "lore": ""},
      {"mtn_id": "MTN-003", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "紫云山", "type": "山", "location_text": "在郏县东南六十里", "description": "其上常有云气舒布，隆冬雪霁青紫可爱，其阴有白虎潭", "lore": ""},
      {"mtn_id": "MTN-004", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "大刘山", "type": "山", "location_text": "在郏县北三十里", "description": "世传汉高祖入关驻此名沛公垒，东汉光武亦驻，后人立庙山间，因有大刘小刘之异", "lore": ""},
      {"mtn_id": "MTN-005", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "长桥河", "type": "河", "location_text": "在郏县东四十里", "description": "又呼蓝桥，发源自钧州南流入于汝河", "lore": ""}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "范士衡", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "郏县令", "summary": "兴学造士，建大成殿于县治"},
      {"per_id": "PER-002", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "杜思进", "type": "名宦", "dynasty": "明", "native_place": "", "office": "知郏县", "summary": "洪武中知郏县，课农桑均徭役，谦己爱人抚字得宜，以治称最"},
      {"per_id": "PER-003", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "傅子荣", "type": "名宦", "dynasty": "明", "native_place": "", "office": "郏县丞", "summary": "正统间任郏县丞，持身廉谨案牍无滞，秩满百姓保留复任，卒于官吏民甚哀悼为立永思碑"},
      {"per_id": "PER-004", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "王玺", "type": "名宦", "dynasty": "明", "native_place": "", "office": "知郏县", "summary": "天顺间知郏县，以廉能著绩升去，士民泣送"},
      {"per_id": "PER-005", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "张鉴", "type": "名宦", "dynasty": "明", "native_place": "", "office": "郏县簿", "summary": "天顺初主郏县簿，有猷有为，征税弭盗尤得其法，修举废坠无不善理，寻以疾乞休吏民不舍为立去思碑"},
      {"per_id": "PER-006", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "袁恺", "type": "人物", "dynasty": "明", "native_place": "郏县", "office": "副都御史", "summary": "由进士累官副都御史，总督南京粮储"},
      {"per_id": "PER-007", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "李希颜", "type": "人物", "dynasty": "明", "native_place": "郏县", "office": "左春坊赞善大夫", "summary": "博通经史穷极根抵，洪武初被征为左春坊赞善大夫，进讲经筵多所裨益，尝注大学中庸心法"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "郏县学", "type": "学校", "location_text": "在县治东南", "history_lore": "金建，本朝洪武三年重建"},
      {"site_id": "SITE-002", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "青云书院", "type": "书院", "location_text": "在郏县城内", "history_lore": "成化五年建"},
      {"site_id": "SITE-003", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "婆娑园", "type": "古迹", "location_text": "在郏县", "history_lore": "宋崔鶠居此，又名石牛庄，鶠诗晚禽噪竹千百翅残菊横枝三两花"},
      {"site_id": "SITE-004", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "钧台", "type": "台", "location_text": "在郏县西", "history_lore": "相传黄帝问道广成驻跸于此，大奏钧天之乐故名"},
      {"site_id": "SITE-005", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "神龟台", "type": "台", "location_text": "在郏县西", "history_lore": "郡国志隋开皇初获神龟腹文曰天下杨兴，左有尹字右有月字即此地"},
      {"site_id": "SITE-006", "item_id": "SITE-006", "geo_id": "GEO-31002c02", "name": "望仙台", "type": "台", "location_text": "在郏县西望仙村内", "history_lore": ""},
      {"site_id": "SITE-007", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "义济桥", "type": "关梁", "location_text": "在郏县西十里沪涧溪上", "history_lore": ""},
      {"site_id": "SITE-008", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "汝河桥", "type": "关梁", "location_text": "在郏县东南十五里汝河上", "history_lore": ""},
      {"site_id": "SITE-009", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "长桥", "type": "关梁", "location_text": "在郏县东四十里跨长桥河", "history_lore": ""},
      {"site_id": "SITE-010", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "开元寺", "type": "寺观", "location_text": "在郏县治东", "history_lore": "后魏建，唐改胜法寺"},
      {"site_id": "SITE-011", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "龙兴寺", "type": "寺观", "location_text": "一在郏县东", "history_lore": ""},
      {"site_id": "SITE-012", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "玉阳观", "type": "寺观", "location_text": "在郏县治东南", "history_lore": "元建"},
      {"site_id": "SITE-013", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "萧酂侯庙", "type": "祠庙", "location_text": "在郏县治内", "history_lore": "祀萧何"},
      {"site_id": "SITE-014", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "唐太宗庙", "type": "祠庙", "location_text": "在郏县东北", "history_lore": ""},
      {"site_id": "SITE-015", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "汉寿亭侯庙", "type": "祠庙", "location_text": "在郏县城内", "history_lore": "洪武中建"},
      {"site_id": "SITE-016", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "三苏祠", "type": "祠庙", "location_text": "在郏县西北峨眉山", "history_lore": "元至正间建"},
      {"site_id": "SITE-017", "item_id": "31-002", "geo_id": "GEO-31002c02", "name": "二苏墓", "type": "陵墓", "location_text": "在郏县峨眉山", "history_lore": "苏轼卒于常州，长子迈卜葬于此山遵治命也，辙后亦葬焉"}
    ],
    "prods": [],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
c02["layers"]["sites"][5]["item_id"] = "31-002"
dump("31-002_c02_郏县.json", c02)

# c03 宝丰县
c03 = {
  "item_id": "31-002", "volume": "31", "source": "宝丰县", "region": "河南", "type": "county",
  "original": "宝丰县【在州东南八十里春秋郑地后入蔡战国属韩秦汉属汝州唐置龙兴县宋更名寳豊县辽金因之元省本朝初仍旧成化十年复置寳豊县属汝州编户三十一里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "宝丰县", "type": "geo", "norm": "宝丰县", "first_source": "31-002"},
      {"ent_id": "ENT-002", "name": "香山", "type": "mtn", "norm": "香山", "first_source": "31-002"},
      {"ent_id": "ENT-003", "name": "九里山", "type": "mtn", "norm": "九里山", "first_source": "31-002"},
      {"ent_id": "ENT-004", "name": "五朵山", "type": "mtn", "norm": "五朵山", "first_source": "31-002"},
      {"ent_id": "ENT-005", "name": "青条岭", "type": "mtn", "norm": "青条岭", "first_source": "31-002"},
      {"ent_id": "ENT-006", "name": "贾复", "type": "person", "norm": "贾复", "first_source": "31-002"}
    ],
    "geos": [{
      "geo_id": "GEO-31002c03", "item_id": "31-002", "name": "宝丰县", "type": "county", "region": "河南",
      "parent": "GEO-31002", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在州东南八十里", "households": {"count": 31, "unit": "里", "note": "编户三十一里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-002", "geo_id": "GEO-31002c03", "dynasty": "周", "era": None, "institution_name": "郑地/蔡地", "action": "置", "detail": "春秋郑地后入蔡，战国属韩"},
      {"evo_id": "EVO-002", "item_id": "31-002", "geo_id": "GEO-31002c03", "dynasty": "唐", "era": None, "institution_name": "龙兴县", "action": "置", "detail": "唐置龙兴县"},
      {"evo_id": "EVO-003", "item_id": "31-002", "geo_id": "GEO-31002c03", "dynasty": "宋", "era": None, "institution_name": "宝丰县", "action": "改", "detail": "宋更名宝丰县，辽金因之"},
      {"evo_id": "EVO-004", "item_id": "31-002", "geo_id": "GEO-31002c03", "dynasty": "元", "era": None, "institution_name": "宝丰县", "action": "省", "detail": "元省入梁县，本朝初仍旧"},
      {"evo_id": "EVO-005", "item_id": "31-002", "geo_id": "GEO-31002c03", "dynasty": "明", "era": "成化", "institution_name": "宝丰县", "action": "复置", "detail": "成化十年复置宝丰县属汝州"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-002", "geo_id": "GEO-31002c03", "name": "香山", "type": "山", "location_text": "在宝丰县东二十里", "description": "旧名火珠，有大龙山小龙山，相传大悲观音证道之所，唐时寺塔并存，塔后有天地池架石梁", "lore": ""},
      {"mtn_id": "MTN-002", "item_id": "31-002", "geo_id": "GEO-31002c03", "name": "九里山", "type": "山", "location_text": "在宝丰县东三十里", "description": "相传汉高祖败项羽于此", "lore": ""},
      {"mtn_id": "MTN-003", "item_id": "31-002", "geo_id": "GEO-31002c03", "name": "五朵山", "type": "山", "location_text": "在宝丰县西八十里", "description": "五山叠翠俨若屏风，青拥县门故名", "lore": ""},
      {"mtn_id": "MTN-004", "item_id": "31-002", "geo_id": "GEO-31002c03", "name": "青条岭", "type": "岭", "location_text": "在宝丰县西二十里", "description": "", "lore": ""}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-002", "geo_id": "GEO-31002c03", "name": "贾复", "type": "人物", "dynasty": "汉", "native_place": "", "office": "胶东侯", "summary": "汉将，墓在汝州城东南，后人为立胶东侯庙于宝丰县城西北隅"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-002", "geo_id": "GEO-31002c03", "name": "宝丰县学", "type": "学校", "location_text": "在县治东", "history_lore": "成化十一年建"},
      {"site_id": "SITE-002", "item_id": "31-002", "geo_id": "GEO-31002c03", "name": "程子书院", "type": "书院", "location_text": "在宝丰县", "history_lore": "成化十六年建"},
      {"site_id": "SITE-003", "item_id": "31-002", "geo_id": "GEO-31002c03", "name": "龙兴寺", "type": "寺观", "location_text": "一在宝丰县南，一在宝丰县北", "history_lore": ""},
      {"site_id": "SITE-004", "item_id": "31-002", "geo_id": "GEO-31002c03", "name": "灵相寺", "type": "寺观", "location_text": "在宝丰县城西南隅", "history_lore": "金大安初建"},
      {"site_id": "SITE-005", "item_id": "31-002", "geo_id": "GEO-31002c03", "name": "神应观", "type": "寺观", "location_text": "在宝丰县城北", "history_lore": ""},
      {"site_id": "SITE-006", "item_id": "31-002", "geo_id": "GEO-31002c03", "name": "胶东侯祠", "type": "祠庙", "location_text": "在宝丰县城西北隅", "history_lore": "祀汉时贾复"},
      {"site_id": "SITE-007", "item_id": "31-002", "geo_id": "GEO-31002c03", "name": "通济桥", "type": "关梁", "location_text": "在宝丰县净肠河", "history_lore": ""},
      {"site_id": "SITE-008", "item_id": "31-002", "geo_id": "GEO-31002c03", "name": "石桥", "type": "关梁", "location_text": "在宝丰县双酒务保", "history_lore": ""}
    ],
    "prods": [],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
dump("31-002_c03_宝丰县.json", c03)

# c04 伊阳县
c04 = {
  "item_id": "31-002", "volume": "31", "source": "伊阳县", "region": "河南", "type": "county",
  "original": "伊阳县【在州西五十里春秋秦晋迁陆浑之城创伊川即此战国属韩秦置新城县属三辅郡两汉因之三国属魏晋复为陆浑属河南府唐置伊州陆浑隶焉寻改为伊阳县五代及宋皆因之隶河南府绍兴九年改为顺川寻复伊阳元改为嵩州属南阳府本朝洪武初改州为县成化十一年仍置伊阳县改隶汝州编户一十八里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "伊阳县", "type": "geo", "norm": "伊阳县", "first_source": "31-002"},
      {"ent_id": "ENT-002", "name": "云夢山", "type": "mtn", "norm": "云夢山", "first_source": "31-002"},
      {"ent_id": "ENT-003", "name": "岘山", "type": "mtn", "norm": "岘山", "first_source": "31-002"},
      {"ent_id": "ENT-004", "name": "筛子垛山", "type": "mtn", "norm": "筛子垛山", "first_source": "31-002"},
      {"ent_id": "ENT-005", "name": "甘泉山", "type": "mtn", "norm": "甘泉山", "first_source": "31-002"},
      {"ent_id": "ENT-006", "name": "九皋山", "type": "mtn", "norm": "九皋山", "first_source": "31-002"},
      {"ent_id": "ENT-007", "name": "凤凰山", "type": "mtn", "norm": "凤凰山", "first_source": "31-002"},
      {"ent_id": "ENT-008", "name": "九女泉", "type": "mtn", "norm": "九女泉", "first_source": "31-002"},
      {"ent_id": "ENT-009", "name": "不救关", "type": "geo", "norm": "不救关", "first_source": "31-002"}
    ],
    "geos": [{
      "geo_id": "GEO-31002c04", "item_id": "31-002", "name": "伊阳县", "type": "county", "region": "河南",
      "parent": "GEO-31002", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在州西五十里", "households": {"count": 18, "unit": "里", "note": "编户一十八里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-002", "geo_id": "GEO-31002c04", "dynasty": "周", "era": None, "institution_name": "陆浑/伊川地", "action": "置", "detail": "春秋秦晋迁陆浑之戎，创伊川即此"},
      {"evo_id": "EVO-002", "item_id": "31-002", "geo_id": "GEO-31002c04", "dynasty": "秦", "era": None, "institution_name": "新城县", "action": "置", "detail": "战国属韩，秦置新城县属三川郡，两汉因之"},
      {"evo_id": "EVO-003", "item_id": "31-002", "geo_id": "GEO-31002c04", "dynasty": "晋", "era": None, "institution_name": "陆浑县", "action": "因之", "detail": "三国属魏，晋复为陆浑属河南郡"},
      {"evo_id": "EVO-004", "item_id": "31-002", "geo_id": "GEO-31002c04", "dynasty": "唐", "era": None, "institution_name": "伊阳县", "action": "改", "detail": "唐置伊州陆浑隶焉，寻改为伊阳县"},
      {"evo_id": "EVO-005", "item_id": "31-002", "geo_id": "GEO-31002c04", "dynasty": "元", "era": None, "institution_name": "嵩州", "action": "改", "detail": "五代及宋皆因之隶河南府，绍兴九年改为顺川寻复伊阳，元改为嵩州属南阳府"},
      {"evo_id": "EVO-006", "item_id": "31-002", "geo_id": "GEO-31002c04", "dynasty": "明", "era": "成化", "institution_name": "伊阳县", "action": "改州为县", "detail": "本朝洪武初改州为县，成化十一年仍置伊阳县改隶汝州"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "云夢山", "type": "山", "location_text": "在伊阳县东南七里", "description": "相传鬼谷修道处，其北有水自洞下注如垂帘，名水帘洞", "lore": ""},
      {"mtn_id": "MTN-002", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "岘山", "type": "山", "location_text": "在伊阳县南四十里", "description": "昔唐文帝经此，以其危峰独见遂名", "lore": ""},
      {"mtn_id": "MTN-003", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "筛子垛山", "type": "山", "location_text": "在伊阳县西七十里", "description": "产铜矿，洞口最多有似筛子眼故名", "lore": ""},
      {"mtn_id": "MTN-004", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "甘泉山", "type": "山", "location_text": "在伊阳县北五里", "description": "中有泉水味甘", "lore": ""},
      {"mtn_id": "MTN-005", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "九皋山", "type": "山", "location_text": "在伊阳县西北二十五里", "description": "昔有鹤鸣于上故名", "lore": ""},
      {"mtn_id": "MTN-006", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "凤凰山", "type": "山", "location_text": "在伊阳县北三十里", "description": "以形似故名", "lore": ""},
      {"mtn_id": "MTN-007", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "九女泉", "type": "泉", "location_text": "在伊阳县南三十里", "description": "", "lore": ""}
    ],
    "pers": [],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "伊阳县学", "type": "学校", "location_text": "在县治西南", "history_lore": "成化十二年建"},
      {"site_id": "SITE-002", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "不救关", "type": "关梁", "location_text": "在伊阳县西南", "history_lore": ""},
      {"site_id": "SITE-003", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "紫罗桥", "type": "关梁", "location_text": "在伊阳县城东", "history_lore": ""},
      {"site_id": "SITE-004", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "漫流桥", "type": "关梁", "location_text": "在伊阳县城外", "history_lore": ""},
      {"site_id": "SITE-005", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "枣林桥", "type": "关梁", "location_text": "在伊阳县城西", "history_lore": ""},
      {"site_id": "SITE-006", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "练溪寺", "type": "寺观", "location_text": "在伊阳县城外", "history_lore": "元大德初建"},
      {"site_id": "SITE-007", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "清凉寺", "type": "寺观", "location_text": "在伊阳县城外", "history_lore": "宋熙宁五年建"},
      {"site_id": "SITE-008", "item_id": "31-002", "geo_id": "GEO-31002c04", "name": "太古观", "type": "寺观", "location_text": "在伊阳县城外", "history_lore": ""}
    ],
    "prods": [],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
dump("31-002_c04_伊阳县.json", c04)

print("DONE c02-c04")
