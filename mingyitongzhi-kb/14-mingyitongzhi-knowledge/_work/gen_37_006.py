# -*- coding: utf-8 -*-
import json, os

OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol37"

# ============================================================
# 靖虏卫 37-006
# ============================================================
jinglu = {
 "item_id": "37-006",
 "volume": "37",
 "source": "靖虏卫",
 "region": "陕西",
 "layers": {
  "ents": [
   {"ent_id": "ENT-001", "name": "靖虏卫", "type": "geo", "norm": "靖虏卫", "first_source": "37-006"},
   {"ent_id": "ENT-002", "name": "乌兰山", "type": "mtn", "norm": "乌兰山", "first_source": "37-006"},
   {"ent_id": "ENT-003", "name": "雪山", "type": "mtn", "norm": "雪山", "first_source": "37-006"},
   {"ent_id": "ENT-004", "name": "祖厉河", "type": "mtn", "norm": "祖厉河", "first_source": "37-006"},
   {"ent_id": "ENT-005", "name": "黄河", "type": "mtn", "norm": "黄河", "first_source": "37-006"},
   {"ent_id": "ENT-006", "name": "防宁郡", "type": "geo", "norm": "防宁郡", "first_source": "37-006"},
   {"ent_id": "ENT-007", "name": "安敬忠", "type": "person", "norm": "安敬忠", "first_source": "37-006"},
   {"ent_id": "ENT-008", "name": "章楶", "type": "person", "norm": "章楶", "first_source": "37-006"},
   {"ent_id": "ENT-009", "name": "郭斌", "type": "person", "norm": "郭斌", "first_source": "37-006"},
   {"ent_id": "ENT-010", "name": "张绣", "type": "person", "norm": "张绣", "first_source": "37-006"},
   {"ent_id": "ENT-011", "name": "程俊", "type": "person", "norm": "程俊", "first_source": "37-006"}
  ],
  "geos": [
   {
    "geo_id": "GEO-37006",
    "item_id": "37-006",
    "name": "靖虏卫",
    "type": "weisuo",
    "region": "陕西",
    "parent": "GEO-000",
    "children": [],
    "volume_range": "卷37",
    "attributes": {
     "borders": [
      {"direction": "东", "to_place": "海纳都", "distance_li": 200},
      {"direction": "西", "to_place": "虎豹口", "distance_li": 40},
      {"direction": "南", "to_place": "郭城驿", "distance_li": 90},
      {"direction": "北", "to_place": "黄河", "distance_li": 5}
     ],
     "to_capital": [
      {"capital": "京师", "distance_li": 3620},
      {"capital": "南京", "distance_li": 3630}
     ],
     "garrison_type": "卫",
     "jun_name": "防宁【唐名】",
     "topography": "面山背河地势险阻【新志】",
     "customs": "人习武艺不惮攻杀【新志】",
     "garrisons": [
      {"name": "迭烈孙堡", "type": "堡", "location_text": "在卫城北九十里，本朝置巡检司，每岁冬增戍兵"}
     ]
    },
    "cit_ids": ["CIT-001", "CIT-002"]
   }
  ],
  "evos": [
   {"evo_id": "EVO-001", "item_id": "37-006", "geo_id": "GEO-37006", "dynasty": "虞夏", "era": None, "institution_name": "雍州之域", "action": "属", "detail": "禹贡雍州之域，古西羌地"},
   {"evo_id": "EVO-002", "item_id": "37-006", "geo_id": "GEO-37006", "dynasty": "秦", "era": None, "institution_name": "陇西郡地", "action": "属郡", "detail": "秦属陇西郡"},
   {"evo_id": "EVO-003", "item_id": "37-006", "geo_id": "GEO-37006", "dynasty": "汉", "era": None, "institution_name": "金城郡", "action": "属郡", "detail": "汉属金城郡"},
   {"evo_id": "EVO-004", "item_id": "37-006", "geo_id": "GEO-37006", "dynasty": "东汉", "era": None, "institution_name": "金城武威二郡", "action": "属郡", "detail": "东汉属金城武威二郡"},
   {"evo_id": "EVO-005", "item_id": "37-006", "geo_id": "GEO-37006", "dynasty": "南北朝", "era": "后魏", "institution_name": "防宁县", "action": "置县", "detail": "后魏置防宁县"},
   {"evo_id": "EVO-006", "item_id": "37-006", "geo_id": "GEO-37006", "dynasty": "南北朝", "era": "西魏", "institution_name": "防州", "action": "置州", "detail": "西魏以县置防州"},
   {"evo_id": "EVO-007", "item_id": "37-006", "geo_id": "GEO-37006", "dynasty": "南北朝", "era": "后周", "institution_name": "鸣沙城", "action": "移治", "detail": "后周移州治鸣沙城"},
   {"evo_id": "EVO-008", "item_id": "37-006", "geo_id": "GEO-37006", "dynasty": "隋", "era": None, "institution_name": "防宁县/平凉郡", "action": "复置", "detail": "隋复置防宁县，属平凉郡"},
   {"evo_id": "EVO-009", "item_id": "37-006", "geo_id": "GEO-37006", "dynasty": "唐", "era": "贞观", "institution_name": "西防州/粟州/防州/防宁郡", "action": "置改", "detail": "唐置西防州，贞观中以足食故改粟州，寻改防州，后又改防宁郡；广德后没于吐蕃"},
   {"evo_id": "EVO-010", "item_id": "37-006", "geo_id": "GEO-37006", "dynasty": "宋", "era": None, "institution_name": "敷文县", "action": "收复置县", "detail": "宋收复，置敷文县"},
   {"evo_id": "EVO-011", "item_id": "37-006", "geo_id": "GEO-37006", "dynasty": "金", "era": None, "institution_name": "保川县/新防州", "action": "置废", "detail": "金置保川县，寻废；以州侨治防川城，号新防州"},
   {"evo_id": "EVO-012", "item_id": "37-006", "geo_id": "GEO-37006", "dynasty": "元", "era": None, "institution_name": "西宁县", "action": "迁治", "detail": "元初迁治西宁县，即今巩昌府防宁县"},
   {"evo_id": "EVO-013", "item_id": "37-006", "geo_id": "GEO-37006", "dynasty": "明", "era": "正统", "institution_name": "靖虏卫", "action": "置卫", "detail": "本朝正统二年复修其废城，置靖虏卫，领千户所四"}
  ],
  "mtns": [
   {"mtn_id": "MTN-001", "item_id": "37-006", "geo_id": "GEO-37006", "name": "乌兰山", "type": "山", "location_text": "在卫城南一百二十里", "description": "唐有乌兰县以此山名", "lore": ""},
   {"mtn_id": "MTN-002", "item_id": "37-006", "geo_id": "GEO-37006", "name": "雪山", "type": "山", "location_text": "在卫城北一百二十里", "description": "山势高峻，积雪不消", "lore": ""},
   {"mtn_id": "MTN-003", "item_id": "37-006", "geo_id": "GEO-37006", "name": "祖厉河", "type": "河", "location_text": "在卫城西南", "description": "北流经祖厉城，入河水", "lore": ""},
   {"mtn_id": "MTN-004", "item_id": "37-006", "geo_id": "GEO-37006", "name": "河水", "type": "河", "location_text": "在祖厉城西", "description": "与祖厉水合；唐史云有河池因雨生盐", "lore": ""},
   {"mtn_id": "MTN-005", "item_id": "37-006", "geo_id": "GEO-37006", "name": "黄河堰", "type": "堰", "location_text": "在卫城北", "description": "唐开元中刺史安敬忠筑以捍河流", "lore": ""},
   {"mtn_id": "MTN-006", "item_id": "37-006", "geo_id": "GEO-37006", "name": "法泉", "type": "泉", "location_text": "在卫城东一十五里石崖下", "description": "其味甘美，祈雨有应", "lore": ""}
  ],
  "pers": [
   {"pers_id": "PER-001", "item_id": "37-006", "geo_id": "GEO-37006", "name": "安敬忠", "dynasty": "唐", "source_section": "名宦", "note": "开元中为防州刺史，时河流冲逼州城，敬忠率团结兵作堰，于是水向西北流，遂免淹没"},
   {"pers_id": "PER-002", "item_id": "37-006", "geo_id": "GEO-37006", "name": "章楶", "dynasty": "宋", "source_section": "名宦", "note": "哲宗时克复防州有功"},
   {"pers_id": "PER-003", "item_id": "37-006", "geo_id": "GEO-37006", "name": "郭斌", "dynasty": "金", "source_section": "名宦", "note": "为金将，金亡，斌出保金兰定会四州；元兵围防州城，斌力战，驱妻子聚一室焚之，已而自投火中；有女奴自火中抱儿出泣授人曰将军尽忠忍使绝嗣此其儿也幸哀而收之，言毕复赴火中死；元将闻之恻然为保其孤"},
   {"pers_id": "PER-004", "item_id": "37-006", "geo_id": "GEO-37006", "name": "张绣", "dynasty": "三国", "source_section": "人物", "note": "武威祖厉人，麯胜袭杀祖厉长，时绣为县吏伺间杀胜，郡邑义之；后仕曹魏，官渡之功力战有功，累迁破羌将军"},
   {"pers_id": "PER-005", "item_id": "37-006", "geo_id": "GEO-37006", "name": "程俊", "dynasty": "宋", "source_section": "人物", "note": "会州人，绍兴初居栗亭之泥阳镇；始俊防稚父母陷灵夏，常号泣自毁；逮长捐家财数十万以赎焉，未至日北向号泣以请，饮食为废，夏人感动遂还其母"}
  ],
  "sites": [
   {"site_id": "SIT-001", "item_id": "37-006", "geo_id": "GEO-37006", "name": "靖虏卫学", "type": "学校", "location_text": "在卫治东南", "description": "正统间建"},
   {"site_id": "SIT-002", "item_id": "37-006", "geo_id": "GEO-37006", "name": "帅正堂", "type": "宫室", "location_text": "在卫城南", "description": "正统间建"},
   {"site_id": "SIT-003", "item_id": "37-006", "geo_id": "GEO-37006", "name": "乌兰关", "type": "关梁/关", "location_text": "在乌兰山上", "description": ""},
   {"site_id": "SIT-004", "item_id": "37-006", "geo_id": "GEO-37006", "name": "防宁关", "type": "关梁/关", "location_text": "在卫境", "description": "旧名颠耳，宋元符初赐名通防，寻改今名"},
   {"site_id": "SIT-005", "item_id": "37-006", "geo_id": "GEO-37006", "name": "迭烈孙堡", "type": "关梁/堡", "location_text": "在卫城北九十里", "description": "本朝置巡检司，每岁冬增戍兵"},
   {"site_id": "SIT-006", "item_id": "37-006", "geo_id": "GEO-37006", "name": "虎豹口", "type": "关梁/口", "location_text": "在卫城西四十里", "description": "有兵戍守之"},
   {"site_id": "SIT-007", "item_id": "37-006", "geo_id": "GEO-37006", "name": "红山寺", "type": "寺观", "location_text": "在卫城东一十五里", "description": "正统间建"},
   {"site_id": "SIT-008", "item_id": "37-006", "geo_id": "GEO-37006", "name": "祖厉城", "type": "古迹", "location_text": "在卫城西南一百三十里", "description": "本汉祖厉县，属安定郡，后汉属武威郡；前凉张轨时废；唐置乌兰县于此，宋废"},
   {"site_id": "SIT-009", "item_id": "37-006", "geo_id": "GEO-37006", "name": "安西城", "type": "古迹", "location_text": "在卫境", "description": "旧名汝遮，宋绍圣初进筑赐今名"},
   {"site_id": "SIT-010", "item_id": "37-006", "geo_id": "GEO-37006", "name": "防川城", "type": "古迹", "location_text": "在卫城西南一百里", "description": "宋元符初置，即金帅郭斌死节处"}
  ],
  "prods": [
   {"prod_id": "PROD-001", "item_id": "37-006", "geo_id": "GEO-37006", "name": "驼褐", "note": ""},
   {"prod_id": "PROD-002", "item_id": "37-006", "geo_id": "GEO-37006", "name": "野马革", "note": ""},
   {"prod_id": "PROD-003", "item_id": "37-006", "geo_id": "GEO-37006", "name": "豹", "note": ""},
   {"prod_id": "PROD-004", "item_id": "37-006", "geo_id": "GEO-37006", "name": "鹿", "note": ""},
   {"prod_id": "PROD-005", "item_id": "37-006", "geo_id": "GEO-37006", "name": "雉", "note": ""},
   {"prod_id": "PROD-006", "item_id": "37-006", "geo_id": "GEO-37006", "name": "兔", "note": ""}
  ],
  "cits": [
   {"cit_id": "CIT-001", "item_id": "37-006", "cited_work": "新志", "cited_work_ent_id": None, "context": "形胜/风俗", "original": "【新志】"},
   {"cit_id": "CIT-002", "item_id": "37-006", "cited_work": "唐史", "cited_work_ent_id": None, "context": "山川", "original": "【唐史云有河池因雨生盐】"}
  ]
 },
 "layer_count": 7,
 "validation": {
  "errs": [],
  "gap": 0,
  "notes": "靖虏卫主文件；原文领千户所四未具名故children为空；pers 5人、sites 10处均未达拆分阈值；张绣程俊属本卫人物（原文接于行都司之前）"
 }
}

with open(os.path.join(OUT, "37-006_靖虏卫.json"), "w", encoding="utf-8") as f:
    json.dump(jinglu, f, ensure_ascii=False, indent=1)

print("37-006 written")
