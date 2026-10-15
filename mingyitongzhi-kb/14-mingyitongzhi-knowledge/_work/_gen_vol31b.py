# -*- coding: utf-8 -*-
"""Generate vol31 county files for 汝宁府."""
import json, os
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol31"

def dump(name, obj):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  {name}: {os.path.getsize(p)} bytes")

# c01 汝阳县 (附郭)
c01 = {
  "item_id": "31-001", "volume": "31", "source": "汝阳县", "region": "河南", "type": "county",
  "original": "汝阳县【附郭周为沈国地汉置汝阳县属汝南郡刘宋属汝阳郡隋初属豫州寻改为溵水县属陈州又析上蔡县地别置汝阳县省溵水入焉即今县也唐为蔡州治金仍旧元省平舆入焉本朝因之编户三十三里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "汝阳县", "type": "geo", "norm": "汝阳县", "first_source": "31-001"},
      {"ent_id": "ENT-002", "name": "潘河", "type": "mtn", "norm": "潘河", "first_source": "31-001"},
      {"ent_id": "ENT-003", "name": "陈尧叟", "type": "person", "norm": "陈尧叟", "first_source": "31-001"},
      {"ent_id": "ENT-004", "name": "蔡顺", "type": "person", "norm": "蔡顺", "first_source": "31-001"},
      {"ent_id": "ENT-005", "name": "董永", "type": "person", "norm": "董永", "first_source": "31-001"},
      {"ent_id": "ENT-006", "name": "许虔", "type": "person", "norm": "许虔", "first_source": "31-001"},
      {"ent_id": "ENT-007", "name": "许劭", "type": "person", "norm": "许劭", "first_source": "31-001"}
    ],
    "geos": [{
      "geo_id": "GEO-31001c01", "item_id": "31-001", "name": "汝阳县", "type": "county", "region": "河南",
      "parent": "GEO-31001", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "附郭", "households": {"count": 33, "unit": "里", "note": "编户三十三里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-001", "geo_id": "GEO-31001c01", "dynasty": "周", "era": None, "institution_name": "沈国地", "action": "置", "detail": "周为沈国地"},
      {"evo_id": "EVO-002", "item_id": "31-001", "geo_id": "GEO-31001c01", "dynasty": "汉", "era": None, "institution_name": "汝阳县", "action": "置", "detail": "汉置汝阳县属汝南郡"},
      {"evo_id": "EVO-003", "item_id": "31-001", "geo_id": "GEO-31001c01", "dynasty": "隋", "era": None, "institution_name": "汝阳县", "action": "改", "detail": "隋初属豫州，寻改为溵水县属陈州，又析上蔡县地别置汝阳县，省溵水入焉"},
      {"evo_id": "EVO-004", "item_id": "31-001", "geo_id": "GEO-31001c01", "dynasty": "唐", "era": None, "institution_name": "汝阳县", "action": "因之", "detail": "唐为蔡州治，金仍旧，元省平舆入焉，本朝因之"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-001", "geo_id": "GEO-31001c01", "name": "倚江亭下汝河", "type": "河", "location_text": "在汝阳县治东南城上", "description": "", "lore": ""}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-001", "geo_id": "GEO-31001c01", "name": "陈尧叟", "type": "人物", "dynasty": "宋", "native_place": "", "office": "名臣", "summary": "宋名臣，尝寓居汝阳，宅在县东北"},
      {"per_id": "PER-002", "item_id": "31-001", "geo_id": "GEO-31001c01", "name": "蔡顺", "type": "人物", "dynasty": "汉", "native_place": "汝南", "office": "孝子", "summary": "以至孝称，王莽末人相食，顺拾桑椹黑者奉母赤者自食，贼遗米受而不食；母终火逼其舍，顺伏棺号哭火遂越他舍"},
      {"per_id": "PER-003", "item_id": "31-001", "geo_id": "GEO-31001c01", "name": "董永", "type": "人物", "dynasty": "汉", "native_place": "汝南", "office": "孝子", "summary": "与蔡顺所居为二孝庄，在汝阳县西"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-001", "geo_id": "GEO-31001c01", "name": "汝阳县学", "type": "学校", "location_text": "在县治东", "history_lore": "洪武十一年建"},
      {"site_id": "SITE-002", "item_id": "31-001", "geo_id": "GEO-31001c01", "name": "来瑞亭", "type": "宫室", "location_text": "在府治", "history_lore": "宋刘敞通守蔡州日有白雀巢于庑下，作小赋记之，后建亭扁曰来瑞"},
      {"site_id": "SITE-003", "item_id": "31-001", "geo_id": "GEO-31001c01", "name": "然身台", "type": "台", "location_text": "在汝阳县东射桥保", "history_lore": "汉令张熹然身救旱处"},
      {"site_id": "SITE-004", "item_id": "31-001", "geo_id": "GEO-31001c01", "name": "二孝庄", "type": "古迹", "location_text": "在汝阳县西", "history_lore": "汉孝子蔡顺董永所居"},
      {"site_id": "SITE-005", "item_id": "31-001", "geo_id": "GEO-31001c01", "name": "月旦里", "type": "古迹", "location_text": "在汝阳县东北", "history_lore": "汉许虔许劭兄弟所居，故名二龙乡月旦里"},
      {"site_id": "SITE-006", "item_id": "31-001", "geo_id": "GEO-31001c01", "name": "陈尧叟宅", "type": "古迹", "location_text": "在汝阳县东北在城保", "history_lore": "尧叟宋名臣尝寓居于此"},
      {"site_id": "SITE-007", "item_id": "31-001", "geo_id": "GEO-31001c01", "name": "翟方进墓", "type": "陵墓", "location_text": "在汝阳县界内", "history_lore": "刘敞诗恃法虽深上不疑疏广何事触刑机"}
    ],
    "prods": [
      {"prod_id": "PROD-001", "item_id": "31-001", "geo_id": "GEO-31001c01", "name": "生姜", "category": "药", "location_text": "汝阳县出"}
    ],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
dump("31-001_c01_汝阳县.json", c01)

# c02 真阳县
c02 = {
  "item_id": "31-001", "volume": "31", "source": "真阳县", "region": "河南", "type": "county",
  "original": "真阳县【在府城南八十里本汉慎阳县地东魏置义阳郡北齐省入保城县隋废保城置真丘县后改曰真阳唐改曰淮阳寻复旧元省入息州本朝初因之治中复置编户一十五里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "真阳县", "type": "geo", "norm": "真阳县", "first_source": "31-001"}
    ],
    "geos": [{
      "geo_id": "GEO-31001c02", "item_id": "31-001", "name": "真阳县", "type": "county", "region": "河南",
      "parent": "GEO-31001", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在府城南八十里", "households": {"count": 15, "unit": "里", "note": "编户一十五里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-001", "geo_id": "GEO-31001c02", "dynasty": "汉", "era": None, "institution_name": "慎阳县地", "action": "置", "detail": "本汉慎阳县地"},
      {"evo_id": "EVO-002", "item_id": "31-001", "geo_id": "GEO-31001c02", "dynasty": "南北朝", "era": "东魏", "institution_name": "义阳郡", "action": "置", "detail": "东魏置义阳郡，北齐省入保城县"},
      {"evo_id": "EVO-003", "item_id": "31-001", "geo_id": "GEO-31001c02", "dynasty": "隋", "era": None, "institution_name": "真丘县/真阳县", "action": "改", "detail": "隋废保城置真丘县，后改曰真阳"},
      {"evo_id": "EVO-004", "item_id": "31-001", "geo_id": "GEO-31001c02", "dynasty": "唐", "era": None, "institution_name": "真阳县", "action": "改", "detail": "唐改曰淮阳，寻复旧"},
      {"evo_id": "EVO-005", "item_id": "31-001", "geo_id": "GEO-31001c02", "dynasty": "元", "era": None, "institution_name": "真阳县", "action": "省", "detail": "元省入息州，本朝初因之，宏治中复置"}
    ],
    "mtns": [],
    "pers": [],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-001", "geo_id": "GEO-31001c02", "name": "真阳县学", "type": "学校", "location_text": "在县治南", "history_lore": "宏治中重建"}
    ],
    "prods": [],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
dump("31-001_c02_真阳县.json", c02)

# c03 上蔡县
c03 = {
  "item_id": "31-001", "volume": "31", "source": "上蔡县", "region": "河南", "type": "county",
  "original": "上蔡县【在府城北四十五里古蔡国周武王封弟叔度于蔡成王封其子蔡仲即此汉置上蔡县属汝南郡后魏改临汝县北齐省隋初置武津县大业中复曰上蔡唐属蔡州宋金元并仍旧本朝因之编户三十六里】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "上蔡县", "type": "geo", "norm": "上蔡县", "first_source": "31-001"},
      {"ent_id": "ENT-002", "name": "芦山冈", "type": "mtn", "norm": "芦山冈", "first_source": "31-001"},
      {"ent_id": "ENT-003", "name": "蔡冈", "type": "mtn", "norm": "蔡冈", "first_source": "31-001"},
      {"ent_id": "ENT-004", "name": "朱马河", "type": "mtn", "norm": "朱马河", "first_source": "31-001"},
      {"ent_id": "ENT-005", "name": "邵店河", "type": "mtn", "norm": "邵店河", "first_source": "31-001"},
      {"ent_id": "ENT-006", "name": "蔡沟", "type": "mtn", "norm": "蔡沟", "first_source": "31-001"},
      {"ent_id": "ENT-007", "name": "光武井", "type": "mtn", "norm": "光武井", "first_source": "31-001"},
      {"ent_id": "ENT-008", "name": "蓍草", "type": "prod", "norm": "蓍草", "first_source": "31-001"},
      {"ent_id": "ENT-009", "name": "李斯", "type": "person", "norm": "李斯", "first_source": "31-001"},
      {"ent_id": "ENT-010", "name": "谢良佐", "type": "person", "norm": "谢良佐", "first_source": "31-001"},
      {"ent_id": "ENT-011", "name": "张元", "type": "person", "norm": "张元", "first_source": "31-001"}
    ],
    "geos": [{
      "geo_id": "GEO-31001c03", "item_id": "31-001", "name": "上蔡县", "type": "county", "region": "河南",
      "parent": "GEO-31001", "children": [], "volume_range": "卷31",
      "attributes": {"location_text": "在府城北四十五里", "households": {"count": 36, "unit": "里", "note": "编户三十六里"}},
      "cit_ids": []
    }],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-001", "geo_id": "GEO-31001c03", "dynasty": "周", "era": None, "institution_name": "蔡国", "action": "置", "detail": "古蔡国，周武王封弟叔度于蔡，成王封其子蔡仲即此"},
      {"evo_id": "EVO-002", "item_id": "31-001", "geo_id": "GEO-31001c03", "dynasty": "汉", "era": None, "institution_name": "上蔡县", "action": "置", "detail": "汉置上蔡县属汝南郡"},
      {"evo_id": "EVO-003", "item_id": "31-001", "geo_id": "GEO-31001c03", "dynasty": "南北朝", "era": "后魏", "institution_name": "临汝县", "action": "改", "detail": "后魏改临汝县，北齐省"},
      {"evo_id": "EVO-004", "item_id": "31-001", "geo_id": "GEO-31001c03", "dynasty": "隋", "era": None, "institution_name": "上蔡县", "action": "复置", "detail": "隋初置武津县，大业中复曰上蔡"},
      {"evo_id": "EVO-005", "item_id": "31-001", "geo_id": "GEO-31001c03", "dynasty": "明", "era": None, "institution_name": "上蔡县", "action": "因之", "detail": "唐属蔡州，宋金元并仍旧，本朝因之"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "芦山冈", "type": "冈", "location_text": "在上蔡县西五里", "description": "即今原王冈也", "lore": ""},
      {"mtn_id": "MTN-002", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "蔡冈", "type": "冈", "location_text": "在上蔡县东一十里", "description": "周五十里", "lore": ""},
      {"mtn_id": "MTN-003", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "朱马河", "type": "河", "location_text": "在上蔡县东二十七里", "description": "有东朱马西朱马二河", "lore": ""},
      {"mtn_id": "MTN-004", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "邵店河", "type": "河", "location_text": "在上蔡县东九十里", "description": "", "lore": ""},
      {"mtn_id": "MTN-005", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "蔡沟", "type": "沟", "location_text": "在上蔡县西南二里", "description": "其水盈涸无源，古有蔡河疑即此", "lore": ""},
      {"mtn_id": "MTN-006", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "光武井", "type": "井", "location_text": "在上蔡县东北", "description": "上有光武台故名", "lore": ""}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "吴公", "type": "人物", "dynasty": "汉", "native_place": "汝南上蔡", "office": "河南守", "summary": "文帝时为河南守，治平为天下第一，徵为廷尉"},
      {"per_id": "PER-002", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "翟方进", "type": "人物", "dynasty": "汉", "native_place": "汝南上蔡", "office": "丞相", "summary": "以射策甲科为郎，永始中拜相，封高陵侯"},
      {"per_id": "PER-003", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "曹恤", "type": "人物", "dynasty": "周", "native_place": "蔡", "office": "孔子弟子", "summary": "春秋蔡人孔子弟子，乐道明义，唐玄宗赠曹伯，宋真宗加封上蔡侯"},
      {"per_id": "PER-004", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "漆雕开", "type": "人物", "dynasty": "周", "native_place": "蔡", "office": "孔子弟子", "summary": "春秋蔡人孔子弟子，对曰吾斯之未能信，唐玄宗赠滕伯，宋真宗加封平舆侯"},
      {"per_id": "PER-005", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "秦冉", "type": "人物", "dynasty": "周", "native_place": "蔡", "office": "孔子弟子", "summary": "春秋蔡人孔子弟子，德艺有成，唐玄宗赠彭衙伯，宋真宗加封新息侯"},
      {"per_id": "PER-006", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "祖无择", "type": "人物", "dynasty": "宋", "native_place": "上蔡", "office": "知信阳军", "summary": "进士高第，出知袁州首建学官，后知信阳军；与王安石不合放弃不振，士论惜之"},
      {"per_id": "PER-007", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "谢良佐", "type": "人物", "dynasty": "宋", "native_place": "上蔡", "office": "学者称上蔡先生", "summary": "学于程门，所著有论语说"},
      {"per_id": "PER-008", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "李韶", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "上蔡令", "summary": "雍熙中上蔡令，防王师北征部送军粮至涿州，因上书愿效死边鄙，遂除殿中侍御史"},
      {"per_id": "PER-009", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "潘好礼", "type": "名宦", "dynasty": "唐", "native_place": "", "office": "上蔡令", "summary": "有治最，后迁豫州刺史，勤力于治清介无所私"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "上蔡县学", "type": "学校", "location_text": "在县治南", "history_lore": "洪武四年建"},
      {"site_id": "SITE-002", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "谢显道书院", "type": "书院", "location_text": "在上蔡县南", "history_lore": "建祀谢显道"},
      {"site_id": "SITE-003", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "八卦台", "type": "台", "location_text": "在上蔡县东三十八里", "history_lore": "有蓍草生焉，旁有白龟庙"},
      {"site_id": "SITE-004", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "高皇台", "type": "台", "location_text": "一在上蔡县东北", "history_lore": "世传汉高祖筑"},
      {"site_id": "SITE-005", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "光武台", "type": "台", "location_text": "在上蔡县东北", "history_lore": "世传汉光武所筑"},
      {"site_id": "SITE-006", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "福兴寺", "type": "寺观", "location_text": "在上蔡县西北", "history_lore": "洪武五年因元旧址重建"},
      {"site_id": "SITE-007", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "谢显道庙", "type": "祠庙", "location_text": "在上蔡县南门外", "history_lore": "正统五年因旧址重建，显道名良佐宋上蔡先生也"},
      {"site_id": "SITE-008", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "李斯墓", "type": "陵墓", "location_text": "在上蔡县西南二十里", "history_lore": "宋刘敞诗二世三公何足论忆牵黄犬出东门"},
      {"site_id": "SITE-009", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "古蔡国", "type": "古迹", "location_text": "在汝阳上蔡二县界", "history_lore": "相传此为古蔡国，李斯墓在城之东"},
      {"site_id": "SITE-010", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "洪桥", "type": "关梁", "location_text": "在上蔡县东北洪河上", "history_lore": ""}
    ],
    "prods": [
      {"prod_id": "PROD-001", "item_id": "31-001", "geo_id": "GEO-31001c03", "name": "蓍草", "category": "药", "location_text": "出上蔡县东八卦台上"}
    ],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": ""}
}
dump("31-001_c03_上蔡县.json", c03)

print("DONE c01-c03")
