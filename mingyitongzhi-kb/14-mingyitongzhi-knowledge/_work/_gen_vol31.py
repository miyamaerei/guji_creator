# -*- coding: utf-8 -*-
"""Generate vol31 JSON files for 汝宁府 and 汝州."""
import json, os

OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol31"
os.makedirs(OUT, exist_ok=True)

def dump(name, obj):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    sz = os.path.getsize(p)
    print(f"  {name}: {sz} bytes")
    return sz

# ============================================================
# 31-001 汝宁府 (prefecture)
# ============================================================
runing = {
  "item_id": "31-001",
  "volume": "31",
  "source": "汝宁府",
  "region": "河南",
  "type": "prefecture",
  "original": "汝宁府【东至直隶鳯阳府頴州界二百三十里西至南阳府裕州舞阳县界一百四十里南至湖广黄州府黄陂县界四百五十里北至开封府陈州西华县界一百十五里自府治至京师二千三百里至南京二千二百五十里】【粮十二万一千七百石零】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "汝宁府", "type": "geo", "norm": "汝宁府", "first_source": "31-001"},
      {"ent_id": "ENT-002", "name": "汝阳县", "type": "geo", "norm": "汝阳县", "first_source": "31-001"},
      {"ent_id": "ENT-003", "name": "真阳县", "type": "geo", "norm": "真阳县", "first_source": "31-001"},
      {"ent_id": "ENT-004", "name": "上蔡县", "type": "geo", "norm": "上蔡县", "first_source": "31-001"},
      {"ent_id": "ENT-005", "name": "新蔡县", "type": "geo", "norm": "新蔡县", "first_source": "31-001"},
      {"ent_id": "ENT-006", "name": "西平县", "type": "geo", "norm": "西平县", "first_source": "31-001"},
      {"ent_id": "ENT-007", "name": "遂平县", "type": "geo", "norm": "遂平县", "first_source": "31-001"},
      {"ent_id": "ENT-008", "name": "信阳州", "type": "geo", "norm": "信阳州", "first_source": "31-001"},
      {"ent_id": "ENT-009", "name": "罗山县", "type": "geo", "norm": "罗山县", "first_source": "31-001"},
      {"ent_id": "ENT-010", "name": "确山县", "type": "geo", "norm": "确山县", "first_source": "31-001"},
      {"ent_id": "ENT-011", "name": "光州", "type": "geo", "norm": "光州", "first_source": "31-001"},
      {"ent_id": "ENT-012", "name": "光山县", "type": "geo", "norm": "光山县", "first_source": "31-001"},
      {"ent_id": "ENT-013", "name": "固始县", "type": "geo", "norm": "固始县", "first_source": "31-001"},
      {"ent_id": "ENT-014", "name": "息县", "type": "geo", "norm": "息县", "first_source": "31-001"},
      {"ent_id": "ENT-015", "name": "商城县", "type": "geo", "norm": "商城县", "first_source": "31-001"},
      {"ent_id": "ENT-016", "name": "汝南郡", "type": "geo", "norm": "汝南郡", "first_source": "31-001"},
      {"ent_id": "ENT-017", "name": "蔡州", "type": "geo", "norm": "蔡州", "first_source": "31-001"},
      {"ent_id": "ENT-018", "name": "信阳卫", "type": "geo", "norm": "信阳卫", "first_source": "31-001"},
      {"ent_id": "ENT-019", "name": "汝宁守御千户所", "type": "geo", "norm": "汝宁守御千户所", "first_source": "31-001"},
      {"ent_id": "ENT-020", "name": "天中山", "type": "mtn", "norm": "天中山", "first_source": "31-001"},
      {"ent_id": "ENT-021", "name": "汝水", "type": "mtn", "norm": "汝水", "first_source": "31-001"},
      {"ent_id": "ENT-022", "name": "淮水", "type": "mtn", "norm": "淮水", "first_source": "31-001"},
      {"ent_id": "ENT-023", "name": "悬瓠城", "type": "mtn", "norm": "悬瓠城", "first_source": "31-001"},
      {"ent_id": "ENT-024", "name": "史记", "type": "book", "norm": "史记", "first_source": "31-001"},
      {"ent_id": "ENT-025", "name": "隋志", "type": "book", "norm": "隋志", "first_source": "31-001"},
      {"ent_id": "ENT-026", "name": "寰宇记", "type": "book", "norm": "寰宇记", "first_source": "31-001"},
      {"ent_id": "ENT-027", "name": "舆地纪胜", "type": "book", "norm": "舆地纪胜", "first_source": "31-001"},
      {"ent_id": "ENT-028", "name": "元志", "type": "book", "norm": "元志", "first_source": "31-001"},
      {"ent_id": "ENT-029", "name": "新唐书", "type": "book", "norm": "新唐书", "first_source": "31-001"},
      {"ent_id": "ENT-030", "name": "刘敞", "type": "person", "norm": "刘敞", "first_source": "31-001"},
      {"ent_id": "ENT-031", "name": "李愬", "type": "person", "norm": "李愬", "first_source": "31-001"},
      {"ent_id": "ENT-032", "name": "裴度", "type": "person", "norm": "裴度", "first_source": "31-001"},
      {"ent_id": "ENT-033", "name": "狄仁杰", "type": "person", "norm": "狄仁杰", "first_source": "31-001"},
      {"ent_id": "ENT-034", "name": "顔真卿", "type": "person", "norm": "顔真卿", "first_source": "31-001"},
      {"ent_id": "ENT-035", "name": "陈胜", "type": "person", "norm": "陈胜", "first_source": "31-001"},
      {"ent_id": "ENT-036", "name": "袁绍", "type": "person", "norm": "袁绍", "first_source": "31-001"},
      {"ent_id": "ENT-037", "name": "袁术", "type": "person", "norm": "袁术", "first_source": "31-001"},
      {"ent_id": "ENT-038", "name": "许劭", "type": "person", "norm": "许劭", "first_source": "31-001"},
      {"ent_id": "ENT-039", "name": "袁安", "type": "person", "norm": "袁安", "first_source": "31-001"},
      {"ent_id": "ENT-040", "name": "陈蕃", "type": "person", "norm": "陈蕃", "first_source": "31-001"}
    ],
    "geos": [
      {
        "geo_id": "GEO-31001",
        "item_id": "31-001",
        "name": "汝宁府",
        "type": "prefecture",
        "region": "河南",
        "parent": "GEO-000",
        "children": ["GEO-31001c01","GEO-31001c02","GEO-31001c03","GEO-31001c04","GEO-31001c05","GEO-31001c06","GEO-31001s01","GEO-31001c07","GEO-31001c08","GEO-31001s02","GEO-31001c09","GEO-31001c10","GEO-31001c11","GEO-31001c12"],
        "volume_range": "卷31",
        "attributes": {
          "borders": [
            {"direction": "东", "to_place": "直隶鳯阳府頴州界", "distance_li": 230},
            {"direction": "西", "to_place": "南阳府裕州舞阳县界", "distance_li": 140},
            {"direction": "南", "to_place": "湖广黄州府黄陂县界", "distance_li": 450},
            {"direction": "北", "to_place": "开封府陈州西华县界", "distance_li": 115}
          ],
          "to_capital": [
            {"capital": "京师", "distance_li": 2300},
            {"capital": "南京", "distance_li": 2250}
          ],
          "grain_tax": {"amount": 121700, "unit": "石", "note": "十二万一千七百石零"},
          "jun_name": "汝南【秦名】淮康【宋名】",
          "topography": "水若垂瓠【水经汝水屈曲形若垂瓠然】其水洄曲其地平舒【北史图经】面山负野限淮为圻【光州赏心堂记】隐然巨屏端若长城【舆地纪胜】襟带长淮控扼颍蔡【光州图经】四方最中【元志豫州于四方最中汝南于豫州又最中】北接陈汝控带许洛【寰宇记信阳北接陈汝控带许洛宋齐以来尝为边镇】九塞之一【舆地记罗山九塞之一】三关之塞【新唐志义阳有三闗之塞】",
          "customs": "剽轻寡积【史记汝南其俗剽轻易发怒地薄寡于积聚】夸奢尚气力好商贾【寰宇记】人性躁劲风气果决【隋志】尚淳质好俭约【同上自平陈之后其俗颇变尚淳质好俭约丧纪婚姻率渐于礼】多事农桑不尚华丽【信阳图志民性劲直多事农桑不尚华丽以俭相尚】俗美民淳【宋光州守劝学文俗美民淳其间异才秀民业儒术以自见于世】人性清和乡闾孝友【舆地志人性清和乡闾孝友男务垦辟女脩织絍士风习尚文质彬彬盖欧阳父子棠隂相映也】人重信义士尚质文【新志汝宁在汝坟之间为文王化行之地人重信义士尚质文富庶淳厚视昔有加】俗好禨祥【宋刘敞新息文宣王庙记】",
          "garrisons": [
            {"name": "信阳卫", "type": "卫", "location_text": "在县治东洪武二十五年建"},
            {"name": "直隶汝宁守御千户所", "type": "千户所", "location_text": "在府治东南永乐三年建隶中都留守司"}
          ],
          "fiefs": []
        },
        "cit_ids": ["CIT-001","CIT-002","CIT-003","CIT-004","CIT-005","CIT-006"]
      },
      {
        "geo_id": "GEO-31001w01",
        "item_id": "31-001",
        "name": "信阳卫",
        "type": "weisuo",
        "region": "河南",
        "parent": "GEO-31001",
        "children": [],
        "volume_range": "卷31",
        "attributes": {"location_text": "在县治东洪武二十五年建"},
        "cit_ids": []
      },
      {
        "geo_id": "GEO-31001w02",
        "item_id": "31-001",
        "name": "汝宁守御千户所",
        "type": "weisuo",
        "region": "河南",
        "parent": "GEO-31001",
        "children": [],
        "volume_range": "卷31",
        "attributes": {"location_text": "在府治东南永乐三年建隶中都留守司"},
        "cit_ids": []
      }
    ],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-001", "geo_id": "GEO-31001", "dynasty": "周", "era": None, "institution_name": "沈蔡二国地", "action": "置", "detail": "禹贡豫州之域，天文角亢氐分野，春秋为沈蔡二国地"},
      {"evo_id": "EVO-002", "item_id": "31-001", "geo_id": "GEO-31001", "dynasty": "秦", "era": None, "institution_name": "颍川郡", "action": "置", "detail": "秦属颍川郡"},
      {"evo_id": "EVO-003", "item_id": "31-001", "geo_id": "GEO-31001", "dynasty": "汉", "era": None, "institution_name": "汝南郡", "action": "置", "detail": "汉置汝南郡"},
      {"evo_id": "EVO-004", "item_id": "31-001", "geo_id": "GEO-31001", "dynasty": "南北朝", "era": "刘宋", "institution_name": "司州", "action": "置", "detail": "刘宋立司州，号其城曰悬瓠；后魏改为豫州；东魏置行台；后周置总管府，后改舒州，寻复曰豫州，又改为溱州，后改蔡州汝南郡如故"},
      {"evo_id": "EVO-005", "item_id": "31-001", "geo_id": "GEO-31001", "dynasty": "隋", "era": None, "institution_name": "汝南郡", "action": "改", "detail": "隋初废郡，大业初废州，复为汝南郡汝阳县"},
      {"evo_id": "EVO-006", "item_id": "31-001", "geo_id": "GEO-31001", "dynasty": "唐", "era": None, "institution_name": "豫州/蔡州", "action": "改", "detail": "唐初置豫州，天宝初改汝南郡，乾元初复为豫州，宝应初仍改蔡州"},
      {"evo_id": "EVO-007", "item_id": "31-001", "geo_id": "GEO-31001", "dynasty": "宋", "era": None, "institution_name": "淮康军节度使", "action": "置", "detail": "宋为淮康军节度使"},
      {"evo_id": "EVO-008", "item_id": "31-001", "geo_id": "GEO-31001", "dynasty": "金", "era": None, "institution_name": "镇南军", "action": "改", "detail": "金改镇南军"},
      {"evo_id": "EVO-009", "item_id": "31-001", "geo_id": "GEO-31001", "dynasty": "元", "era": None, "institution_name": "汝宁府", "action": "升", "detail": "元为蔡州，后升汝宁府"},
      {"evo_id": "EVO-010", "item_id": "31-001", "geo_id": "GEO-31001", "dynasty": "明", "era": None, "institution_name": "汝宁府", "action": "因之", "detail": "本朝因之，领州二县十二"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-001", "geo_id": "GEO-31001", "name": "天中山", "type": "山", "location_text": "在府城北三里亦名天台山", "description": "高尺余，土上下石，以其在天地之中故曰天中，自古考日景测分数莫正于此", "lore": "宋刘敞尝作记以表其地，又有诗云开辟以来传至今形势虽小当天心斗极回旋未易测日景短长犹可寻"},
      {"mtn_id": "MTN-002", "item_id": "31-001", "geo_id": "GEO-31001", "name": "汝水", "type": "河", "location_text": "源出天息山东流入境", "description": "经汝阳上蔡新蔡西平入淮", "lore": ""},
      {"mtn_id": "MTN-003", "item_id": "31-001", "geo_id": "GEO-31001", "name": "淮水", "type": "河", "location_text": "淮出桐柏山自西南东流入境", "description": "经确山信阳息县入颍州界", "lore": ""},
      {"mtn_id": "MTN-004", "item_id": "31-001", "geo_id": "GEO-31001", "name": "溱水", "type": "河", "location_text": "在府城南一十八里", "description": "水出青衣山入淮，今称溱口", "lore": ""},
      {"mtn_id": "MTN-005", "item_id": "31-001", "geo_id": "GEO-31001", "name": "滇水", "type": "河", "location_text": "在府城南六十里", "description": "流入淮，隋因此水置滇阳县", "lore": ""},
      {"mtn_id": "MTN-006", "item_id": "31-001", "geo_id": "GEO-31001", "name": "汶水", "type": "河", "location_text": "在府城南九十里", "description": "水自青龙陂入汝，今称汶口", "lore": ""},
      {"mtn_id": "MTN-007", "item_id": "31-001", "geo_id": "GEO-31001", "name": "澺水", "type": "河", "location_text": "在府城南汝水湾", "description": "有栗园，今栗洲是也", "lore": ""},
      {"mtn_id": "MTN-008", "item_id": "31-001", "geo_id": "GEO-31001", "name": "洪河", "type": "河", "location_text": "在府城东六十里", "description": "水自上蔡县东流，合戚桥河入汝水", "lore": ""},
      {"mtn_id": "MTN-009", "item_id": "31-001", "geo_id": "GEO-31001", "name": "东冈", "type": "冈", "location_text": "在府城东南四十里", "description": "", "lore": ""},
      {"mtn_id": "MTN-010", "item_id": "31-001", "geo_id": "GEO-31001", "name": "中冈", "type": "冈", "location_text": "在府城南六十里", "description": "", "lore": ""},
      {"mtn_id": "MTN-011", "item_id": "31-001", "geo_id": "GEO-31001", "name": "西湖", "type": "湖", "location_text": "在府城西", "description": "旧志云颍许陈蔡四州皆有西湖，此州之西湖有翠光亭待月台", "lore": "宋孔武仲诗有亭下湖光凝不流及百尺湖台蘸春绿之句"},
      {"mtn_id": "MTN-012", "item_id": "31-001", "geo_id": "GEO-31001", "name": "柴潭", "type": "潭", "location_text": "在府城外一名东泽", "description": "唐李愬夜半抵悬瓠柴潭谓此；金天兴初宋遣孟珙攻蔡，珙决柴潭水介汝", "lore": "宋刘敞诗欲暖水流初汛汛半闲人意正悠悠又云乘兴柴潭须一到会令鱼鸟见防机"},
      {"mtn_id": "MTN-013", "item_id": "31-001", "geo_id": "GEO-31001", "name": "悬瓠池", "type": "池", "location_text": "在府城北门外", "description": "唐李愬雪夜击鹅鹜以乱军声即此，俗呼为鹅鸭池", "lore": ""},
      {"mtn_id": "MTN-014", "item_id": "31-001", "geo_id": "GEO-31001", "name": "蛰渊池", "type": "池", "location_text": "在府城东北", "description": "池上有水鉴亭，本名芷亭，宋刘敞更今名", "lore": "有诗云昔人种白芷既以名此亭今我通蛰渊复以木鉴名"},
      {"mtn_id": "MTN-015", "item_id": "31-001", "geo_id": "GEO-31001", "name": "西阳池", "type": "池", "location_text": "在府治内", "description": "", "lore": "宋刘敞诗出郭无所诣入门少佳趣空有西阳池犹为赏心具"},
      {"mtn_id": "MTN-016", "item_id": "31-001", "geo_id": "GEO-31001", "name": "葛陂", "type": "陂", "location_text": "在府城西南三十里", "description": "即费长房投杖处，东汉于此置葛陂县后废，今有葛仙庙", "lore": ""},
      {"mtn_id": "MTN-017", "item_id": "31-001", "geo_id": "GEO-31001", "name": "鸿郄陂", "type": "陂", "location_text": "在府城东一十里", "description": "汉成帝时关东数水陂溢为害，翟方进奏罢陂；建武中许阳复为陂", "lore": ""},
      {"mtn_id": "MTN-018", "item_id": "31-001", "geo_id": "GEO-31001", "name": "黄溪", "type": "溪", "location_text": "在府城南", "description": "水色纯黄故名", "lore": ""},
      {"mtn_id": "MTN-019", "item_id": "31-001", "geo_id": "GEO-31001", "name": "锦绣溪", "type": "溪", "location_text": "在府城南", "description": "", "lore": "宋刘敞诗锦绣溪边春几许欲寻清浅翠芳菲"},
      {"mtn_id": "MTN-020", "item_id": "31-001", "geo_id": "GEO-31001", "name": "秔陂港", "type": "港", "location_text": "在府城东南一百三十里", "description": "水自青龙陂入汝", "lore": ""},
      {"mtn_id": "MTN-021", "item_id": "31-001", "geo_id": "GEO-31001", "name": "龙陂港", "type": "港", "location_text": "在府城南二百里", "description": "源出洪山，下流合清水港入淮", "lore": ""}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-001", "geo_id": "GEO-31001", "name": "蔡仲", "type": "名宦", "dynasty": "周", "native_place": "", "office": "蔡国始封", "summary": "武王封叔度于蔡，后挟武庚作乱，周公放之；其子胡改行率德，成王复封之蔡，是为蔡仲"},
      {"per_id": "PER-002", "item_id": "31-001", "geo_id": "GEO-31001", "name": "吕侯", "type": "名宦", "dynasty": "周", "native_place": "", "office": "穆王卿士", "summary": "穆王时吕侯言于王，徙下蔡，作修刑辟，命曰甫刑"},
      {"per_id": "PER-003", "item_id": "31-001", "geo_id": "GEO-31001", "name": "端木赐", "type": "名宦", "dynasty": "周", "native_place": "", "office": "信阳宰", "summary": "春秋时为魏信阳宰，将行辞孔子，孔子曰勤之慎之，吾闻知为吏者奉法以利民"},
      {"per_id": "PER-004", "item_id": "31-001", "geo_id": "GEO-31001", "name": "郑当时", "type": "名宦", "dynasty": "汉", "native_place": "", "office": "汝南太守", "summary": "武帝时汝南太守，有声，数岁以官卒，家亡余财"},
      {"per_id": "PER-005", "item_id": "31-001", "geo_id": "GEO-31001", "name": "召信臣", "type": "名宦", "dynasty": "汉", "native_place": "", "office": "上蔡长", "summary": "视民如子，所居见称"},
      {"per_id": "PER-006", "item_id": "31-001", "geo_id": "GEO-31001", "name": "寇恂", "type": "名宦", "dynasty": "汉", "native_place": "", "office": "汝南太守", "summary": "建武初汝南太守，讨平盗贼，郡界清净，乃大修学校教生徒"},
      {"per_id": "PER-007", "item_id": "31-001", "geo_id": "GEO-31001", "name": "邓晨", "type": "名宦", "dynasty": "汉", "native_place": "", "office": "汝南太守", "summary": "建武中汝南太守，兴鸿郄陂数千顷，汝土以丰，鱼稻之饶流衍他郡"},
      {"per_id": "PER-008", "item_id": "31-001", "geo_id": "GEO-31001", "name": "鲍昱", "type": "名宦", "dynasty": "汉", "native_place": "", "office": "汝南太守", "summary": "永平中汝南太守，郡多陂池岁决坏，昱乃上作方梁石洫，水常饶足，溉田倍多"},
      {"per_id": "PER-009", "item_id": "31-001", "geo_id": "GEO-31001", "name": "何敞", "type": "名宦", "dynasty": "汉", "native_place": "", "office": "汝南太守", "summary": "和帝时汝南太守，以宽和为政，修理鲖阳旧渠，百姓赖其利，吏民共刻石颂德"},
      {"per_id": "PER-010", "item_id": "31-001", "geo_id": "GEO-31001", "name": "贾彪", "type": "名宦", "dynasty": "汉", "native_place": "", "office": "新息长", "summary": "延熹中新息长，小民贫窭多不养子，彪严为之制，数年养子千数，佥曰贾父所长"},
      {"per_id": "PER-011", "item_id": "31-001", "geo_id": "GEO-31001", "name": "王允", "type": "名宦", "dynasty": "汉", "native_place": "", "office": "豫州刺史", "summary": "豫州刺史，奏除禁党，讨击黄巾别帅大破之，降数十万人"},
      {"per_id": "PER-012", "item_id": "31-001", "geo_id": "GEO-31001", "name": "满宠", "type": "名宦", "dynasty": "三国", "native_place": "", "office": "魏汝南太守", "summary": "魏汝南太守，时袁绍盛于河朔而汝南绍本郡门生宾客拥兵拒守，宠讨平之，领豫州刺史有政绩"},
      {"per_id": "PER-013", "item_id": "31-001", "geo_id": "GEO-31001", "name": "贾逵", "type": "名宦", "dynasty": "三国", "native_place": "", "office": "魏豫州刺史", "summary": "黄初中豫州刺史，考绩二千石以下不如法奏免，文帝称为真刺史，修军旅内理民事，造为陂渠"},
      {"per_id": "PER-014", "item_id": "31-001", "geo_id": "GEO-31001", "name": "张苌年", "type": "名宦", "dynasty": "南北朝", "native_place": "", "office": "后魏汝南太守", "summary": "郡人有兄弟分一牛争讼不能决者，苌年赐以己牛一头使均之，于是境中相戒咸至敬让"},
      {"per_id": "PER-015", "item_id": "31-001", "geo_id": "GEO-31001", "name": "王肃", "type": "名宦", "dynasty": "南北朝", "native_place": "", "office": "后魏豫州刺史", "summary": "太和中豫州刺史，尝于四望陂筑城以御梁"},
      {"per_id": "PER-016", "item_id": "31-001", "geo_id": "GEO-31001", "name": "狄仁杰", "type": "名宦", "dynasty": "唐", "native_place": "", "office": "豫州刺史", "summary": "豫州刺史，时越王兵败支党余二千人论死，仁杰密疏申理，诏悉谪戍边"},
      {"per_id": "PER-017", "item_id": "31-001", "geo_id": "GEO-31001", "name": "姚崇", "type": "名宦", "dynasty": "唐", "native_place": "", "office": "申州刺史", "summary": "与宋璟谋出太平公主，贬申州刺史，崇虽被黜而声名自此昭著"},
      {"per_id": "PER-018", "item_id": "31-001", "geo_id": "GEO-31001", "name": "吴育", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "知蔡州", "summary": "知蔡州，设伍保法以检制盗贼；时告妖人千数聚确山者，育曰此特乡民用浮屠法相聚利钱财尔，一弓手召之可致"},
      {"per_id": "PER-019", "item_id": "31-001", "geo_id": "GEO-31001", "name": "富弼", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "知蔡州", "summary": "以大学士徙知蔡州，不以名位自骄，专意民事，有情必达"},
      {"per_id": "PER-020", "item_id": "31-001", "geo_id": "GEO-31001", "name": "欧阳修", "type": "名宦", "dynasty": "宋", "native_place": "永丰", "office": "知蔡州", "summary": "知蔡州，初镇太原自请易蔡州，大略曰时多喜新奇而臣惟守拙，众方兴功利而臣惟循常"},
      {"per_id": "PER-021", "item_id": "31-001", "geo_id": "GEO-31001", "name": "刘敞", "type": "名宦", "dynasty": "宋", "native_place": "临江新喻", "office": "通判蔡州", "summary": "通判蔡州，凿池开河以利灌溉；其弟攽亦知是州，文章政事侔古循吏"},
      {"per_id": "PER-022", "item_id": "31-001", "geo_id": "GEO-31001", "name": "丁讽", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "知蔡州", "summary": "治平中知蔡州，设法赈饥活者六十万人，蔡人攀慕号呼，闭城拆桥不得行者累日"},
      {"per_id": "PER-023", "item_id": "31-001", "geo_id": "GEO-31001", "name": "吕公著", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "知蔡州", "summary": "治平中知蔡州，酿水泉灌田，易军营草舍以瓦，修孔子庙，荐举孝行善政为多"},
      {"per_id": "PER-024", "item_id": "31-001", "geo_id": "GEO-31001", "name": "张升", "type": "名宦", "dynasty": "元", "native_place": "", "office": "知汝宁府", "summary": "至大中知汝宁府，民有告寄束书于其家者逾三年取阅有禁书一编，升亟呼吏焚其书曰妄言诬民"},
      {"per_id": "PER-025", "item_id": "31-001", "geo_id": "GEO-31001", "name": "万孟雅", "type": "名宦", "dynasty": "明", "native_place": "", "office": "汝宁知府", "summary": "洪武初汝宁知府，公威厉吏民畏服，奏清天下户口禁除奸弊，时称其能"},
      {"per_id": "PER-026", "item_id": "31-001", "geo_id": "GEO-31001", "name": "李兴邦", "type": "名宦", "dynasty": "明", "native_place": "", "office": "知汝宁府", "summary": "永乐初知汝宁府，知吏弊民艰，凡催办公务不遣人下属惟发信牌皆依期完集，政誉赫然"},
      {"per_id": "PER-027", "item_id": "31-001", "geo_id": "GEO-31001", "name": "申达", "type": "名宦", "dynasty": "明", "native_place": "", "office": "知汝宁府", "summary": "永乐中知汝宁府，练达时政善革奸弊，汝民素勤耕稼不通贸易，创立集场军民便之"},
      {"per_id": "PER-028", "item_id": "31-001", "geo_id": "GEO-31001", "name": "马祖常", "type": "流寓", "dynasty": "元", "native_place": "西域", "office": "御史中丞", "summary": "父润同知漳州路家于光州，祖常七岁知学，延祐初廷试第二，累官御史中丞，工文章务去陈腐自成一家，文宗谓中原硕儒唯祖常"},
      {"per_id": "PER-029", "item_id": "31-001", "geo_id": "GEO-31001", "name": "陈胜", "type": "人物", "dynasty": "秦", "native_place": "汝阳", "office": "张楚王", "summary": "阳城人，少时尝与人佣耕；秦二世发闾左戍渔阳，胜与吴广谋举事，行至陈据之，胜自立为王号张楚"},
      {"per_id": "PER-030", "item_id": "31-001", "geo_id": "GEO-31001", "name": "翟方进", "type": "人物", "dynasty": "汉", "native_place": "汝南上蔡", "office": "丞相", "summary": "以射策甲科为郎，永始中拜相，以儒雅缘饰吏事号通明相，封高陵侯"},
      {"per_id": "PER-031", "item_id": "31-001", "geo_id": "GEO-31001", "name": "袁安", "type": "人物", "dynasty": "汉", "native_place": "汝南汝阳", "office": "司徒", "summary": "传父孟氏易，永平中拜楚郡太守，徵为河南尹，累迁司徒；子敞孙汤曾孙逢四世三公"},
      {"per_id": "PER-032", "item_id": "31-001", "geo_id": "GEO-31001", "name": "陈蕃", "type": "人物", "dynasty": "汉", "native_place": "汝南平舆", "office": "太傅", "summary": "年十五闲处一室，曰大丈夫当扫除天下；累迁太尉，窦后临朝复为太傅录尚书事"},
      {"per_id": "PER-033", "item_id": "31-001", "geo_id": "GEO-31001", "name": "黄宪", "type": "人物", "dynasty": "汉", "native_place": "汝南慎阳", "office": "征君", "summary": "郭泰曰叔度汪汪若千顷陂，澄之不清淆之不浊不可量也，天下号曰征君"},
      {"per_id": "PER-034", "item_id": "31-001", "geo_id": "GEO-31001", "name": "许劭", "type": "人物", "dynasty": "汉", "native_place": "汝南平舆", "office": "郡功曹", "summary": "好核论乡党人物，每月辄更其品题，故汝南俗有月旦评；兄虔亦知名，汝南人称平舆渊有二龙"},
      {"per_id": "PER-035", "item_id": "31-001", "geo_id": "GEO-31001", "name": "袁绍", "type": "人物", "dynasty": "汉", "native_place": "汝南汝阳", "office": "大将军", "summary": "袁安四世孙，有姿貌威容爱士养名，倾心折节，士无贵贱与之抗礼"},
      {"per_id": "PER-036", "item_id": "31-001", "geo_id": "GEO-31001", "name": "袁术", "type": "人物", "dynasty": "汉", "native_place": "汝南汝阳", "office": "南阳太守", "summary": "绍从弟，举孝廉累官至河南尹，董卓谋废立术奔南阳，后为曹操所败"},
      {"per_id": "PER-037", "item_id": "31-001", "geo_id": "GEO-31001", "name": "费祎", "type": "人物", "dynasty": "三国", "native_place": "江夏𫑡", "office": "蜀尚书令", "summary": "在蜀与董允齐名，后主时为黄门侍郎，后代蒋琬为尚书令，当国功名略与琬比"},
      {"per_id": "PER-038", "item_id": "31-001", "geo_id": "GEO-31001", "name": "干宝", "type": "人物", "dynasty": "晋", "native_place": "新蔡", "office": "散骑常侍", "summary": "博览书记为著作郎，着晋记三十卷咸称良史，又着搜神记三十卷，刘惔曰卿可谓鬼之董狐"},
      {"per_id": "PER-039", "item_id": "31-001", "geo_id": "GEO-31001", "name": "朱序", "type": "人物", "dynasty": "晋", "native_place": "义阳", "office": "梁州刺史", "summary": "宁康初拜梁州刺史镇襄阳，苻坚围序，序母韩自登城履行，领婢于西北角斜筑城，贼果攻破西北角众守新筑城"},
      {"per_id": "PER-040", "item_id": "31-001", "geo_id": "GEO-31001", "name": "王潮", "type": "人物", "dynasty": "唐", "native_place": "光州固始", "office": "威武军节度使", "summary": "与弟审邽审知并以材气知名，僖宗时举兵略定闽地，作四门义学还流亡定赋敛，后为威武军节度使；审知后为闽王"},
      {"per_id": "PER-041", "item_id": "31-001", "geo_id": "GEO-31001", "name": "孙何", "type": "人物", "dynasty": "宋", "native_place": "汝阳", "office": "知制诰", "summary": "笃孝嗜古十五能属文，与丁谓齐名时号孙丁，举进士礼部廷试俱第一，着有驳史通十余卷文集四十卷"},
      {"per_id": "PER-042", "item_id": "31-001", "geo_id": "GEO-31001", "name": "谢良佐", "type": "人物", "dynasty": "宋", "native_place": "上蔡", "office": "学者称上蔡先生", "summary": "学于程门记问该赡，对人称前史至不差一字；与程颐别一年来见，曰但去得一矜字，颐叹其善学"},
      {"per_id": "PER-043", "item_id": "31-001", "geo_id": "GEO-31001", "name": "高兴", "type": "人物", "dynasty": "元", "native_place": "蔡州", "office": "右丞相", "summary": "少慷慨多大节，从丞相巴延累立战功，官至右丞相商议河南省事，卒追封梁国公谥武宣，后加封南阳王"},
      {"per_id": "PER-044", "item_id": "31-001", "geo_id": "GEO-31001", "name": "费长房", "type": "仙释", "dynasty": "汉", "native_place": "汝南", "office": "", "summary": "为市吏，从壶公入深山学道，后得竹杖骑任所之，投葛陂中化龙；桓景学于长房，九月九日登高饮菊花酒避灾"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-001", "geo_id": "GEO-31001", "name": "汝宁府学", "type": "学校", "location_text": "在府治东", "history_lore": "洪武六年因元旧址重建"},
      {"site_id": "SITE-002", "item_id": "31-001", "geo_id": "GEO-31001", "name": "汝南书院", "type": "书院", "location_text": "在府城南", "history_lore": "成化十一年建"},
      {"site_id": "SITE-003", "item_id": "31-001", "geo_id": "GEO-31001", "name": "悬瓠楼", "type": "宫室", "location_text": "在府城上", "history_lore": "后魏平南王肃起高堞于小城，建层楼于隅阿下际水湄，宋更为汝南楼"},
      {"site_id": "SITE-004", "item_id": "31-001", "geo_id": "GEO-31001", "name": "燕誉堂", "type": "宫室", "location_text": "在府治旧东园", "history_lore": "宋郡守吴育与刘敞尝有赋咏"},
      {"site_id": "SITE-005", "item_id": "31-001", "geo_id": "GEO-31001", "name": "木雁堂", "type": "宫室", "location_text": "在府治", "history_lore": "刘敞有诗"},
      {"site_id": "SITE-006", "item_id": "31-001", "geo_id": "GEO-31001", "name": "见山亭", "type": "宫室", "location_text": "在府治前牙城上", "history_lore": "远见诸山前后拱揖故名"},
      {"site_id": "SITE-007", "item_id": "31-001", "geo_id": "GEO-31001", "name": "临波亭", "type": "宫室", "location_text": "在府治后圃", "history_lore": "宋刘敞诗水影时翻高槛动天形略抱曲城低"},
      {"site_id": "SITE-008", "item_id": "31-001", "geo_id": "GEO-31001", "name": "牡丹亭", "type": "宫室", "location_text": "在府治旧东园", "history_lore": "郡守吴育诗咏甚多，刘敞诗最工"},
      {"site_id": "SITE-009", "item_id": "31-001", "geo_id": "GEO-31001", "name": "奇生亭", "type": "宫室", "location_text": "在府治东园", "history_lore": "吴育取夏侯湛赋羡石榴奇生之句以名"},
      {"site_id": "SITE-010", "item_id": "31-001", "geo_id": "GEO-31001", "name": "翠光亭", "type": "宫室", "location_text": "在府之西湖", "history_lore": "宋孔武仲诗有亭下湖光凝不流之句"},
      {"site_id": "SITE-011", "item_id": "31-001", "geo_id": "GEO-31001", "name": "待月台", "type": "台", "location_text": "在府之西湖", "history_lore": "宋孔武仲诗有百尺湖台蘸春绿之句"},
      {"site_id": "SITE-012", "item_id": "31-001", "geo_id": "GEO-31001", "name": "幽兰轩", "type": "宫室", "location_text": "在府治内一名幽兰阁", "history_lore": "金义宗自归德奔汝宁以府治为行宫，宋端平初孟珙攻城甚急，义宗自尽于此"},
      {"site_id": "SITE-013", "item_id": "31-001", "geo_id": "GEO-31001", "name": "济民桥", "type": "关梁", "location_text": "在府城东关", "history_lore": ""},
      {"site_id": "SITE-014", "item_id": "31-001", "geo_id": "GEO-31001", "name": "北门桥", "type": "关梁", "location_text": "在府城北关", "history_lore": ""},
      {"site_id": "SITE-015", "item_id": "31-001", "geo_id": "GEO-31001", "name": "溱济桥", "type": "关梁", "location_text": "在府城南八十里", "history_lore": ""},
      {"site_id": "SITE-016", "item_id": "31-001", "geo_id": "GEO-31001", "name": "开元寺", "type": "寺观", "location_text": "在府城内", "history_lore": "唐开元中始建，本朝洪武中重建"},
      {"site_id": "SITE-017", "item_id": "31-001", "geo_id": "GEO-31001", "name": "悬瓠观", "type": "寺观", "location_text": "在府城北十五里", "history_lore": "旧名悬壶，本费长房旧宅，唐天宝间建，本朝正统中重修"},
      {"site_id": "SITE-018", "item_id": "31-001", "geo_id": "GEO-31001", "name": "荆将军庙", "type": "祠庙", "location_text": "在府城西", "history_lore": "祀荆轲"},
      {"site_id": "SITE-019", "item_id": "31-001", "geo_id": "GEO-31001", "name": "光武庙", "type": "祠庙", "location_text": "在府城东", "history_lore": ""},
      {"site_id": "SITE-020", "item_id": "31-001", "geo_id": "GEO-31001", "name": "狄梁公庙", "type": "祠庙", "location_text": "在府城南", "history_lore": "梁公唐相狄仁杰也"},
      {"site_id": "SITE-021", "item_id": "31-001", "geo_id": "GEO-31001", "name": "裴晋公庙", "type": "祠庙", "location_text": "在府城内", "history_lore": "晋公唐相裴度也，平淮西有功故立庙祀之"},
      {"site_id": "SITE-022", "item_id": "31-001", "geo_id": "GEO-31001", "name": "三公庙", "type": "祠庙", "location_text": "在府治西", "history_lore": "祀唐名臣狄仁杰颜真卿裴度"},
      {"site_id": "SITE-023", "item_id": "31-001", "geo_id": "GEO-31001", "name": "颜鲁公庙", "type": "祠庙", "location_text": "在府城内", "history_lore": "唐德宗朝奉诏谕李希烈为所杀，后家人启柩状貌如生"},
      {"site_id": "SITE-024", "item_id": "31-001", "geo_id": "GEO-31001", "name": "李愬庙", "type": "祠庙", "location_text": "在府城西", "history_lore": "愬唐将也，俗呼白马将军庙"},
      {"site_id": "SITE-025", "item_id": "31-001", "geo_id": "GEO-31001", "name": "高平庙", "type": "祠庙", "location_text": "在府城闾巷口", "history_lore": "兴元丞相封河南汝阳王"},
      {"site_id": "SITE-026", "item_id": "31-001", "geo_id": "GEO-31001", "name": "平舆故城", "type": "古迹", "location_text": "在府城东汝水南", "history_lore": "春秋沈子国地，汉置县汝南郡治，后废隋复置，王世充置舆州，唐州废，元省入汝阳"},
      {"site_id": "SITE-027", "item_id": "31-001", "geo_id": "GEO-31001", "name": "宜春城", "type": "古迹", "location_text": "在府城西南", "history_lore": "汉旧县属汝南郡，晋改曰北宜春"},
      {"site_id": "SITE-028", "item_id": "31-001", "geo_id": "GEO-31001", "name": "安成故城", "type": "古迹", "location_text": "在府城东南汝水北", "history_lore": "汉旧县属汝南郡，晋因之"},
      {"site_id": "SITE-029", "item_id": "31-001", "geo_id": "GEO-31001", "name": "汝南废县", "type": "古迹", "location_text": "在汝水之南", "history_lore": "唐贞元中割汝阳置县，元和中省入汝阳"},
      {"site_id": "SITE-030", "item_id": "31-001", "geo_id": "GEO-31001", "name": "平淮西碑", "type": "古迹", "location_text": "在府城内裴晋公庙中", "history_lore": "唐韩愈撰文多归功裴度；宋陈珦磨去段文仍刻韩文"},
      {"site_id": "SITE-031", "item_id": "31-001", "geo_id": "GEO-31001", "name": "袁安墓", "type": "陵墓", "location_text": "在府城东", "history_lore": ""}
    ],
    "prods": [
      {"prod_id": "PROD-001", "item_id": "31-001", "geo_id": "GEO-31001", "name": "栀子", "category": "药", "location_text": ""},
      {"prod_id": "PROD-002", "item_id": "31-001", "geo_id": "GEO-31001", "name": "蜈蚣", "category": "虫", "location_text": ""},
      {"prod_id": "PROD-003", "item_id": "31-001", "geo_id": "GEO-31001", "name": "红花", "category": "药", "location_text": "西平遂平息县三县俱出"}
    ],
    "cits": [
      {"cit_id": "CIT-001", "item_id": "31-001", "cited_work": "史记", "cited_work_ent_id": "ENT-024", "context": "证俗", "original": "【史记】"},
      {"cit_id": "CIT-002", "item_id": "31-001", "cited_work": "隋志", "cited_work_ent_id": "ENT-025", "context": "证俗", "original": "【隋志】"},
      {"cit_id": "CIT-003", "item_id": "31-001", "cited_work": "寰宇记", "cited_work_ent_id": "ENT-026", "context": "证俗", "original": "【寰宇记】"},
      {"cit_id": "CIT-004", "item_id": "31-001", "cited_work": "舆地纪胜", "cited_work_ent_id": "ENT-027", "context": "立论", "original": "【舆地纪胜】"},
      {"cit_id": "CIT-005", "item_id": "31-001", "cited_work": "元志", "cited_work_ent_id": "ENT-028", "context": "立论", "original": "【元志】"},
      {"cit_id": "CIT-006", "item_id": "31-001", "cited_work": "新唐书", "cited_work_ent_id": "ENT-029", "context": "立论", "original": "【新唐志】"}
    ]
  },
  "layer_count": 7,
  "validation": {"errs": [], "gap": 0, "notes": "府级名宦人物择要录入；其余州县条目入县文件；废浍州等入SITE层"}
}

dump("31-001_汝宁府.json", runing)
print("DONE 31-001")
