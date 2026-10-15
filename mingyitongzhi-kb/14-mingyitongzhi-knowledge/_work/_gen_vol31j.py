# -*- coding: utf-8 -*-
"""Generate vol31 31-002 汝州 (department) + 4 counties."""
import json, os
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol31"

def dump(name, obj):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  {name}: {os.path.getsize(p)} bytes")

# 31-002 汝州 (department, parent=GEO-000)
ruzhou = {
  "item_id": "31-002", "volume": "31", "source": "汝州", "region": "河南", "type": "department",
  "original": "汝州【东至开封府许州襄城县界七十里西至河南府洛阳县界八十里南至南阳府南召县界九十里北至河南府登封县界五十里自州治至京师一千七百五十里至南京一千七百五十里】【粮十四万七千七百石零】",
  "layers": {
    "ents": [
      {"ent_id": "ENT-001", "name": "汝州", "type": "geo", "norm": "汝州", "first_source": "31-002"},
      {"ent_id": "ENT-002", "name": "鲁山县", "type": "geo", "norm": "鲁山县", "first_source": "31-002"},
      {"ent_id": "ENT-003", "name": "郏县", "type": "geo", "norm": "郏县", "first_source": "31-002"},
      {"ent_id": "ENT-004", "name": "宝丰县", "type": "geo", "norm": "宝丰县", "first_source": "31-002"},
      {"ent_id": "ENT-005", "name": "伊阳县", "type": "geo", "norm": "伊阳县", "first_source": "31-002"},
      {"ent_id": "ENT-006", "name": "承休县/梁县", "type": "geo", "norm": "梁县", "first_source": "31-002"},
      {"ent_id": "ENT-007", "name": "临汝郡", "type": "geo", "norm": "临汝郡", "first_source": "31-002"},
      {"ent_id": "ENT-008", "name": "风穴山", "type": "mtn", "norm": "风穴山", "first_source": "31-002"},
      {"ent_id": "ENT-009", "name": "崆峒山", "type": "mtn", "norm": "崆峒山", "first_source": "31-002"},
      {"ent_id": "ENT-010", "name": "广成泽", "type": "mtn", "norm": "广成泽", "first_source": "31-002"},
      {"ent_id": "ENT-011", "name": "汝水", "type": "mtn", "norm": "汝水", "first_source": "31-002"},
      {"ent_id": "ENT-012", "name": "广成子", "type": "person", "norm": "广成子", "first_source": "31-002"},
      {"ent_id": "ENT-013", "name": "巢父", "type": "person", "norm": "巢父", "first_source": "31-002"},
      {"ent_id": "ENT-014", "name": "许由", "type": "person", "norm": "许由", "first_source": "31-002"},
      {"ent_id": "ENT-015", "name": "元结", "type": "person", "norm": "元结", "first_source": "31-002"},
      {"ent_id": "ENT-016", "name": "颜真卿", "type": "person", "norm": "颜真卿", "first_source": "31-002"},
      {"ent_id": "ENT-017", "name": "苏轼", "type": "person", "norm": "苏轼", "first_source": "31-002"},
      {"ent_id": "ENT-018", "name": "苏辙", "type": "person", "norm": "苏辙", "first_source": "31-002"},
      {"ent_id": "ENT-019", "name": "富弼", "type": "person", "norm": "富弼", "first_source": "31-002"},
      {"ent_id": "ENT-020", "name": "程颢", "type": "person", "norm": "程颢", "first_source": "31-002"},
      {"ent_id": "ENT-021", "name": "牛皋", "type": "person", "norm": "牛皋", "first_source": "31-002"},
      {"ent_id": "ENT-022", "name": "钦定四库全书", "type": "book", "norm": "钦定四库全书", "first_source": "31-002"}
    ],
    "geos": [
      {
        "geo_id": "GEO-31002", "item_id": "31-002", "name": "汝州", "type": "department", "region": "河南",
        "parent": "GEO-000", "children": ["GEO-31002c01","GEO-31002c02","GEO-31002c03","GEO-31002c04","GEO-31002w01"],
        "volume_range": "卷31",
        "attributes": {
          "borders": [
            {"direction": "东", "to_place": "开封府许州襄城县界", "distance_li": 70},
            {"direction": "西", "to_place": "河南府洛阳县界", "distance_li": 80},
            {"direction": "南", "to_place": "南阳府南召县界", "distance_li": 90},
            {"direction": "北", "to_place": "河南府登封县界", "distance_li": 50}
          ],
          "to_capital": [
            {"capital": "京师", "distance_li": 1750},
            {"capital": "南京", "distance_li": 1750}
          ],
          "grain_tax": {"amount": 147700, "unit": "石", "note": "十四万七千七百石零"},
          "jun_name": "汝阳【晋名】",
          "topography": "右矕三涂左概嵩岳【旧志汝州之境右矕三涂左概嵩岳面据衡阴箕背王屋浸以陂溠演以荣洛】土壤膏沃风气绵密【鲁山峰峦环抱河流萦带土壤膏沃风气绵密】",
          "customs": "渐濡道学【旧志汝颍多奇士乃伊川游宦之邦道学渐濡者众】民尚淳厚士习诗礼男耕女织与往古同辙【汝州志】隐然伊洛之遗风【伊阳志农务耒耜士乐诗书隐然伊洛之遗风焉】",
          "garrisons": [
            {"name": "汝州卫", "type": "卫", "location_text": "在州城内"}
          ],
          "fiefs": [],
          "households": {"count": 50, "unit": "里", "note": "编户五十里领县四"}
        },
        "cit_ids": []
      },
      {
        "geo_id": "GEO-31002w01", "item_id": "31-002", "name": "汝州卫", "type": "weisuo", "region": "河南",
        "parent": "GEO-31002", "children": [], "volume_range": "卷31",
        "attributes": {"location_text": "在州城内"},
        "cit_ids": []
      }
    ],
    "evos": [
      {"evo_id": "EVO-001", "item_id": "31-002", "geo_id": "GEO-31002", "dynasty": "周", "era": None, "institution_name": "王畿地/戎蛮子邑", "action": "置", "detail": "禹贡豫州之域，天文心分野，周为王畿地，春秋为戎蛮子邑"},
      {"evo_id": "EVO-002", "item_id": "31-002", "geo_id": "GEO-31002", "dynasty": "战国", "era": None, "institution_name": "韩/魏", "action": "因之", "detail": "战国属韩后属魏"},
      {"evo_id": "EVO-003", "item_id": "EVO-003", "geo_id": "GEO-31002", "dynasty": "秦", "era": None, "institution_name": "三川郡", "action": "置", "detail": "秦属三川郡"},
      {"evo_id": "EVO-004", "item_id": "31-002", "geo_id": "GEO-31002", "dynasty": "汉", "era": None, "institution_name": "河南郡梁县地", "action": "置", "detail": "汉为河南郡梁县地"},
      {"evo_id": "EVO-005", "item_id": "31-002", "geo_id": "GEO-31002", "dynasty": "南北朝", "era": "东魏", "institution_name": "北荆州/和州", "action": "置", "detail": "后魏属汝北鲁阳二郡，东魏置北荆州，后周改曰和州"},
      {"evo_id": "EVO-006", "item_id": "31-002", "geo_id": "GEO-31002", "dynasty": "隋", "era": None, "institution_name": "汝州/襄城郡", "action": "改", "detail": "隋改汝州以汝水为名，寻改襄城郡治承休县"},
      {"evo_id": "EVO-007", "item_id": "31-002", "geo_id": "GEO-31002", "dynasty": "唐", "era": None, "institution_name": "汝州/临汝郡", "action": "改", "detail": "唐复为汝州，改承休为梁县，天宝初改州为临汝郡，乾元初复为汝州"},
      {"evo_id": "EVO-008", "item_id": "31-002", "geo_id": "GEO-31002", "dynasty": "宋", "era": None, "institution_name": "陆海军节度", "action": "置", "detail": "宋置陆海军节度"},
      {"evo_id": "EVO-009", "item_id": "31-002", "geo_id": "GEO-31002", "dynasty": "金", "era": None, "institution_name": "汝州", "action": "因之", "detail": "金废军州县仍旧"},
      {"evo_id": "EVO-010", "item_id": "31-002", "geo_id": "GEO-31002", "dynasty": "元", "era": None, "institution_name": "汝州", "action": "属南阳府", "detail": "元属南阳府"},
      {"evo_id": "EVO-011", "item_id": "31-002", "geo_id": "GEO-31002", "dynasty": "明", "era": "成化", "institution_name": "汝州", "action": "升直隶州", "detail": "本朝初以梁县省入仍旧属，成化十二年增置宝丰伊阳二县，直隶河南布政司"}
    ],
    "mtns": [
      {"mtn_id": "MTN-001", "item_id": "31-002", "geo_id": "GEO-31002", "name": "风穴山", "type": "山", "location_text": "在州城东北二十里", "description": "上有风穴，旧有吴公洞读书庵雅才亭俱废", "lore": "宋李廌有诗，吴芾复隐此"},
      {"mtn_id": "MTN-002", "item_id": "31-002", "geo_id": "GEO-31002", "name": "霍山", "type": "山", "location_text": "在州城东南二十里", "description": "左传谓楚袭梁及霍即此，汉立霍山县因山而名，今故城俗谓张侯城", "lore": ""},
      {"mtn_id": "MTN-003", "item_id": "31-002", "geo_id": "GEO-31002", "name": "鹿台山", "type": "山", "location_text": "在州城北二十里", "description": "有台状若蹲鹿", "lore": ""},
      {"mtn_id": "MTN-004", "item_id": "31-002", "geo_id": "GEO-31002", "name": "灶君山", "type": "山", "location_text": "在州城西南三十里", "description": "山有石刻灶君山三字", "lore": "鲁山县东关有普济庙以祀灶君山神，祷雨有应"},
      {"mtn_id": "MTN-005", "item_id": "31-002", "geo_id": "GEO-31002", "name": "玉羊山", "type": "山", "location_text": "在州城西北四十里", "description": "石多羊迹", "lore": ""},
      {"mtn_id": "MTN-006", "item_id": "31-002", "geo_id": "GEO-31002", "name": "云夢山", "type": "山", "location_text": "在州城西南五十里", "description": "相传鬼谷子修道处", "lore": ""},
      {"mtn_id": "MTN-007", "item_id": "31-002", "geo_id": "GEO-31002", "name": "鱼齿山", "type": "山", "location_text": "在州城东南五十里", "description": "左传楚伐郑次于鱼陵涉于鱼齿之下即此，山下有涉水", "lore": ""},
      {"mtn_id": "MTN-008", "item_id": "31-002", "geo_id": "GEO-31002", "name": "崆峒山", "type": "山", "location_text": "在州城西南六十里", "description": "昔广成子隐此今有墓存，山下有洞其户上出，相传洞中白犬常游洞外故号小冢为玉狗峰", "lore": "相传崆峒有三，一在安定一在临洮；庄子述黄帝问道崆峒遂言游襄城登具茨访大隗皆与此山接壤；上有广成庙及崆峒观，下有广成城"},
      {"mtn_id": "MTN-009", "item_id": "31-002", "geo_id": "GEO-31002", "name": "鸣皋山", "type": "山", "location_text": "在州城西南六十里一名狼皋山", "description": "南旧有唐贞观中所建清暑宫，汝水自山东出硖谓之汝阨", "lore": ""},
      {"mtn_id": "MTN-010", "item_id": "31-002", "geo_id": "GEO-31002", "name": "重金山", "type": "山", "location_text": "在州城北四十里", "description": "其出多黄石，其形叠叠日夕掩映山色如金", "lore": ""},
      {"mtn_id": "MTN-011", "item_id": "31-002", "geo_id": "GEO-31002", "name": "黄涧河", "type": "河", "location_text": "在州城东三十里俗名赵落河", "description": "源发于左村之北山流合汝河达淮", "lore": ""},
      {"mtn_id": "MTN-012", "item_id": "31-002", "geo_id": "GEO-31002", "name": "西湖", "type": "湖", "location_text": "一名龙塘陂在汝州城西八里", "description": "其水四时不竭，灌田千余顷", "lore": ""},
      {"mtn_id": "MTN-013", "item_id": "31-002", "geo_id": "GEO-31002", "name": "太史湖", "type": "湖", "location_text": "在州城", "description": "宋太守王素浚治为一郡之胜，名曰太史湖", "lore": "李廌有记"},
      {"mtn_id": "MTN-014", "item_id": "31-002", "geo_id": "GEO-31002", "name": "广成泽", "type": "泽", "location_text": "在州城西四十里一名黄陂", "description": "周回百里，汉广成苑地，有灌溉之利百姓赖之", "lore": ""},
      {"mtn_id": "MTN-015", "item_id": "31-002", "geo_id": "GEO-31002", "name": "烧车水", "type": "河", "location_text": "源出花山下", "description": "注澧河东流入汝水", "lore": "即光武烧王寻辎重处"},
      {"mtn_id": "MTN-016", "item_id": "31-002", "geo_id": "GEO-31002", "name": "巢父井", "type": "井", "location_text": "在州城西郭门外", "description": "其旁有巢由庙", "lore": "宋宗舜臣尝刻王通叟吊巢父文于石"},
      {"mtn_id": "MTN-017", "item_id": "31-002", "geo_id": "GEO-31002", "name": "马跑泉", "type": "泉", "location_text": "在州城东南", "description": "相传汉光武军渴乏水，忽马跑地而得此泉", "lore": ""},
      {"mtn_id": "MTN-018", "item_id": "31-002", "geo_id": "GEO-31002", "name": "龙泉", "type": "泉", "location_text": "在州城西南", "description": "其水莹洁，中秋之夕阴云蔽月俯观泉中兔形自若", "lore": "时人有我欲龙泉观夜月崆峒烟雨阻人行之句"},
      {"mtn_id": "MTN-019", "item_id": "31-002", "geo_id": "GEO-31002", "name": "温汤泉", "type": "泉", "location_text": "在州城西南六十里源有九眼", "description": "东南流注广成泽可疗疾", "lore": "唐武后尝幸于此有温汤碑；其侧又有寒泉南流注滍水，虽盛夏肃如冰谷；又州城南三十里有武后流杯池碑"},
      {"mtn_id": "MTN-020", "item_id": "31-002", "geo_id": "GEO-31002", "name": "石龙涡", "type": "泉", "location_text": "在州城", "description": "四壁千仞散泉如雨", "lore": "唐孟郊有诗"}
    ],
    "pers": [
      {"per_id": "PER-001", "item_id": "31-002", "geo_id": "GEO-31002", "name": "冯鲂", "type": "名宦", "dynasty": "汉", "native_place": "", "office": "郏令", "summary": "为郏令捕降盗贼，县界清净，光武曰此健令也使降诸盗"},
      {"per_id": "PER-002", "item_id": "31-002", "geo_id": "GEO-31002", "name": "华谭", "type": "名宦", "dynasty": "晋", "native_place": "", "office": "郏令", "summary": "永宁初为郏令，时兵乱之后境内饥馑，倾心抚字甚有政绩"},
      {"per_id": "PER-003", "item_id": "31-002", "geo_id": "GEO-31002", "name": "元德秀", "type": "名宦", "dynasty": "唐", "native_place": "", "office": "鲁山令", "summary": "有盗系狱会虎为暴，盗请格虎自赎许之，明日盗果尸虎还；所得俸禄悉散孤遗，岁满笥余一缣驾柴车去"},
      {"per_id": "PER-004", "item_id": "31-002", "geo_id": "GEO-31002", "name": "令狐绪", "type": "名宦", "dynasty": "唐", "native_place": "", "office": "汝州刺史", "summary": "有佳政，汝人请刻石颂德，绪以弟绹当国固让，宣宗嘉其意乃止"},
      {"per_id": "PER-005", "item_id": "31-002", "geo_id": "GEO-31002", "name": "杨亿", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "知汝州", "summary": "大中祥符间知汝州，清修正直誉冠当时，士民得其片文只字以为矜式"},
      {"per_id": "PER-006", "item_id": "31-002", "geo_id": "GEO-31002", "name": "王素", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "知汝州", "summary": "知汝州，政余书不去手，遇事立决不停讼，待寮宾以谦恭待吏民以宽厚"},
      {"per_id": "PER-007", "item_id": "31-002", "geo_id": "GEO-31002", "name": "富弼", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "判汝州", "summary": "熙宁初判汝州，上言新法不可以治郡，愿归洛养疾许之，百姓去思甚切"},
      {"per_id": "PER-008", "item_id": "31-002", "geo_id": "GEO-31002", "name": "程颢", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "监汝州盐税", "summary": "神宗时罢邑以亲老求近乡监局，得监汝州盐税，寻以宗正丞召之"},
      {"per_id": "PER-009", "item_id": "31-002", "geo_id": "GEO-31002", "name": "蒋之奇", "type": "名宦", "dynasty": "宋", "native_place": "", "office": "知汝州", "summary": "元符末知汝州，孜孜民事和平乐易，郡人诵之"},
      {"per_id": "PER-010", "item_id": "31-002", "geo_id": "GEO-31002", "name": "张复", "type": "名宦", "dynasty": "明", "native_place": "", "office": "知汝州", "summary": "永乐初知汝州，清廉刚直不遣吏卒摧摄，民无横扰而公事易集"},
      {"per_id": "PER-011", "item_id": "31-002", "geo_id": "GEO-31002", "name": "官谦", "type": "名宦", "dynasty": "明", "native_place": "", "office": "知汝州", "summary": "永乐中知汝州，恭慎慈爱为政知缓急，四出招抚流民归者动以千数，庙学颓圮首割己俸倡之"},
      {"per_id": "PER-012", "item_id": "31-002", "geo_id": "GEO-31002", "name": "沈贵", "type": "名宦", "dynasty": "明", "native_place": "", "office": "知汝州", "summary": "至即询宿弊编民户等级以均差役，循行田里教民树艺作陂堰溉田，修学校礼师儒，卒于官吏民追慕为立祠"},
      {"per_id": "PER-013", "item_id": "31-002", "geo_id": "GEO-31002", "name": "臧宫", "type": "人物", "dynasty": "汉", "native_place": "颍川郏", "office": "辅威将军朗陵侯", "summary": "从光武征战以勇称，击诸郡平之后平蜀拜广汉太守，封朗陵侯"},
      {"per_id": "PER-014", "item_id": "31-002", "geo_id": "GEO-31002", "name": "铫期", "type": "人物", "dynasty": "汉", "native_place": "颍川郏", "office": "卫尉安成侯", "summary": "容貌绝异矜严有威，从徇蓟，封安成侯，重信义在朝忧国爱主能犯颜谏诤"},
      {"per_id": "PER-015", "item_id": "31-002", "geo_id": "GEO-31002", "name": "元结", "type": "人物", "dynasty": "唐", "native_place": "鲁山", "office": "道州刺史御史中丞", "summary": "少聪悟宏达倜傥不羁，天宝中进士，撰大唐中兴颂刻于浯溪，大历初拜御史中丞"},
      {"per_id": "PER-016", "item_id": "31-002", "geo_id": "GEO-31002", "name": "马燧", "type": "人物", "dynasty": "唐", "native_place": "汝州郏城", "office": "北平郡王", "summary": "姿度魁杰沉勇多算，从抱玉入朝，代宗雅闻其才，后屡立大功封北平郡王"},
      {"per_id": "PER-017", "item_id": "31-002", "geo_id": "GEO-31002", "name": "牛皋", "type": "人物", "dynasty": "宋", "native_place": "汝州鲁山", "office": "荆湖南路马步军副总管", "summary": "初为射士，战败金人累迁，后为岳飞部将，复随州襄阳擒杨么以功最"},
      {"per_id": "PER-018", "item_id": "31-002", "geo_id": "GEO-31002", "name": "孔旼", "type": "流寓", "dynasty": "宋", "native_place": "", "office": "隐者", "summary": "孔子四十六代孙，宋时隐居汝州滍阳城，事亲至孝读书循礼法，州以行义闻特赐旌表"},
      {"per_id": "PER-019", "item_id": "31-002", "geo_id": "GEO-31002", "name": "崔鶠", "type": "流寓", "dynasty": "宋", "native_place": "阳翟", "office": "筠州推官", "summary": "进士为筠州推官，徽宗初立以日食求直言，鶠上言，后蔡京借上书人免鶠官，久之移病居郏城治田百亩为婆娑园"},
      {"per_id": "PER-020", "item_id": "31-002", "geo_id": "GEO-31002", "name": "范祖述", "type": "流寓", "dynasty": "宋", "native_place": "成都", "office": "朝请大夫", "summary": "累官知台州主管西京御史台，靖康多难避地汝州，汝守赵子淔邀与共守，旁郡尽陷汝独全"},
      {"per_id": "PER-021", "item_id": "31-002", "geo_id": "GEO-31002", "name": "王氏二妇", "type": "列女", "dynasty": "宋", "native_place": "汝州", "office": "", "summary": "建炎初金人至汝州，二妇为所掠拥置舟中，遂投汉江以死，尸皆浮出不坏，时人收葬城外江上为双冢"},
      {"per_id": "PER-022", "item_id": "31-002", "geo_id": "GEO-31002", "name": "袁氏", "type": "列女", "dynasty": "明", "native_place": "汝州", "office": "马元吉妻", "summary": "永乐初元吉卒于京师，袁氏携幼子负骨归葬，养舅姑以天年终，守节四十余年，正统间旌其门曰贞节"},
      {"per_id": "PER-023", "item_id": "31-002", "geo_id": "GEO-31002", "name": "王粉儿", "type": "列女", "dynasty": "明", "native_place": "汝州", "office": "张得山未娶妻", "summary": "许嫁同里张得山未行而得山殁，粉儿即柩旁恸哭几绝，既葬复至墓所奠哭遂自缢青杨树下"},
      {"per_id": "PER-024", "item_id": "31-002", "geo_id": "GEO-31002", "name": "张元化", "type": "仙释", "dynasty": "宋", "native_place": "", "office": "道士", "summary": "葛玄弟子尝寓汝州有前知之明，宋政和中封冲妙先生"}
    ],
    "sites": [
      {"site_id": "SITE-001", "item_id": "31-002", "geo_id": "GEO-31002", "name": "汝州学", "type": "学校", "location_text": "在州治西", "history_lore": "洪武三年因元旧祠堂建"},
      {"site_id": "SITE-002", "item_id": "31-002", "geo_id": "GEO-31002", "name": "望嵩楼", "type": "宫室", "location_text": "在州子城内", "history_lore": "唐时建，刘禹锡送廖彦谋诗有望嵩楼上忽相见之句；宋李廷老更名汝阳楼"},
      {"site_id": "SITE-003", "item_id": "31-002", "geo_id": "GEO-31002", "name": "龙兴楼", "type": "宫室", "location_text": "在州城中", "history_lore": "宋崔鶠诗老去未觉跻攀难一表独立青冥里"},
      {"site_id": "SITE-004", "item_id": "31-002", "geo_id": "GEO-31002", "name": "郑公堂", "type": "宫室", "location_text": "在州城治", "history_lore": "宋富弼尝封郑国两偃藩于汝，民思之后守来典郡为建此堂刻公诗于石"},
      {"site_id": "SITE-005", "item_id": "31-002", "geo_id": "GEO-31002", "name": "此君堂", "type": "宫室", "location_text": "在州城", "history_lore": "元祐时知州文大方构"},
      {"site_id": "SITE-006", "item_id": "31-002", "geo_id": "GEO-31002", "name": "致雨亭", "type": "宫室", "location_text": "在州北园跨西池上", "history_lore": "宋咸平中赵况为守时建，有苏辙祈雨文刻石"},
      {"site_id": "SITE-007", "item_id": "31-002", "geo_id": "GEO-31002", "name": "思贤亭", "type": "宫室", "location_text": "在州治后", "history_lore": "宋祥符中杨义知汝州有贤名，后王晌瑜来作守思之因建此亭，刘攽作记"},
      {"site_id": "SITE-008", "item_id": "31-002", "geo_id": "GEO-31002", "name": "香远亭", "type": "宫室", "location_text": "在州治后圃", "history_lore": "金大定中乌古论知汝州时建，亭前有茶蘼三株，宋子初取苏轼无风香自远之句名之"},
      {"site_id": "SITE-009", "item_id": "31-002", "geo_id": "GEO-31002", "name": "虚舟亭", "type": "宫室", "location_text": "在州治后圃", "history_lore": "金兴定初防御使完颜建，赵思文有记"},
      {"site_id": "SITE-010", "item_id": "31-002", "geo_id": "GEO-31002", "name": "疏岚亭", "type": "宫室", "location_text": "在州东北风穴山上", "history_lore": "登台则州可见"},
      {"site_id": "SITE-011", "item_id": "SITE-011", "geo_id": "GEO-31002", "name": "擂鼓台", "type": "台", "location_text": "在州城", "history_lore": "相传汉高祖与项羽战于此"},
      {"site_id": "SITE-012", "item_id": "31-002", "geo_id": "GEO-31002", "name": "纪氏台", "type": "台", "location_text": "在州东百余里", "history_lore": "续汉书曰世祖车驾西征降群盗于此"},
      {"site_id": "SITE-013", "item_id": "31-002", "geo_id": "GEO-31002", "name": "龙门关", "type": "关梁", "location_text": "在州东大龙山下", "history_lore": ""},
      {"site_id": "SITE-014", "item_id": "31-002", "geo_id": "GEO-31002", "name": "洗耳桥", "type": "关梁", "location_text": "旧名石桥在州城西门外洗耳河上", "history_lore": ""},
      {"site_id": "SITE-015", "item_id": "31-002", "geo_id": "GEO-31002", "name": "塔亭寺", "type": "寺观", "location_text": "在州城东关", "history_lore": "宋元祐初建"},
      {"site_id": "SITE-016", "item_id": "31-002", "geo_id": "GEO-31002", "name": "宝应寺", "type": "寺观", "location_text": "在州城西南隅", "history_lore": "唐开元初建"},
      {"site_id": "SITE-017", "item_id": "31-002", "geo_id": "GEO-31002", "name": "白云寺", "type": "寺观", "location_text": "在州城东北风穴山", "history_lore": "唐大中初建"},
      {"site_id": "SITE-018", "item_id": "31-002", "geo_id": "GEO-31002", "name": "丹阳观", "type": "寺观", "location_text": "在州城内", "history_lore": ""},
      {"site_id": "SITE-019", "item_id": "31-002", "geo_id": "GEO-31002", "name": "清溪观", "type": "寺观", "location_text": "在州城东关", "history_lore": ""},
      {"site_id": "SITE-020", "item_id": "31-002", "geo_id": "GEO-31002", "name": "汉高祖庙", "type": "祠庙", "location_text": "在州城陂北保", "history_lore": ""},
      {"site_id": "SITE-021", "item_id": "31-002", "geo_id": "GEO-31002", "name": "许由庙", "type": "祠庙", "location_text": "在州城西关", "history_lore": ""},
      {"site_id": "SITE-022", "item_id": "31-002", "geo_id": "GEO-31002", "name": "颍大夫庙", "type": "祠庙", "location_text": "在州城", "history_lore": "祀颍考叔有墓存，宋苏辙有诗吊之"},
      {"site_id": "SITE-023", "item_id": "31-002", "geo_id": "GEO-31002", "name": "颜鲁公祠", "type": "祠庙", "location_text": "在州治东龙兴寺", "history_lore": "祀唐忠臣颜真卿，宋李廌诗古寺今如昔泉扃夜不晨"},
      {"site_id": "SITE-024", "item_id": "31-002", "geo_id": "GEO-31002", "name": "汉寿亭侯庙", "type": "祠庙", "location_text": "在州城内", "history_lore": "正统初建"},
      {"site_id": "SITE-025", "item_id": "31-002", "geo_id": "GEO-31002", "name": "魏陵", "type": "陵墓", "location_text": "在州城东南大龙山巅", "history_lore": "魏元氏所葬"},
      {"site_id": "SITE-026", "item_id": "31-002", "geo_id": "GEO-31002", "name": "魏悼园", "type": "陵墓", "location_text": "在州城西北牛脾山", "history_lore": "宋秦王廷美之墓，附兆二十余"},
      {"site_id": "SITE-027", "item_id": "31-002", "geo_id": "GEO-31002", "name": "贾复墓", "type": "陵墓", "location_text": "在州城东南", "history_lore": "葬汉将军贾复，后人为立胶东侯庙"},
      {"site_id": "SITE-028", "item_id": "31-002", "geo_id": "GEO-31002", "name": "父城", "type": "古迹", "location_text": "在州城东南父城保", "history_lore": "本殷时历国，左传楚城父城即此，汉置县属颍川郡"},
      {"site_id": "SITE-029", "item_id": "31-002", "geo_id": "GEO-31002", "name": "周承休城", "type": "古迹", "location_text": "在州城东南", "history_lore": "汉元帝置此县，光武封姬常为承休公主周祀即此地，隋曰承休县，唐又改为梁县"},
      {"site_id": "SITE-030", "item_id": "31-002", "geo_id": "GEO-31002", "name": "贾复城", "type": "古迹", "location_text": "在州城东南一百余里一名通鸦城", "history_lore": "复击郾所筑，俗讹为寡妇城"},
      {"site_id": "SITE-031", "item_id": "31-002", "geo_id": "GEO-31002", "name": "汝北城/王坞城", "type": "古迹", "location_text": "在州城南", "history_lore": "高齐置郡后改曰汝阴，后周废"},
      {"site_id": "SITE-032", "item_id": "31-002", "geo_id": "GEO-31002", "name": "临汝城", "type": "古迹", "location_text": "在州城西南六十里", "history_lore": "唐置县属汝州"},
      {"site_id": "SITE-033", "item_id": "31-002", "geo_id": "GEO-31002", "name": "宝丰城", "type": "古迹", "location_text": "在州城东", "history_lore": "本汉郏城县地，唐析置龙兴县，宋改宝丰，元省入梁县"},
      {"site_id": "SITE-034", "item_id": "31-002", "geo_id": "GEO-31002", "name": "废梁县", "type": "古迹", "location_text": "在州城子城东", "history_lore": "本隋承休县，又有梁县在西南四十五里属汝州，唐贞观初省梁县更承体曰，本朝省入州"},
      {"site_id": "SITE-035", "item_id": "31-002", "geo_id": "GEO-31002", "name": "蛮中聚", "type": "古迹", "location_text": "在州城西南", "history_lore": "即戎蛮子国，俗呼麻城"},
      {"site_id": "SITE-036", "item_id": "31-002", "geo_id": "GEO-31002", "name": "阳人聚", "type": "古迹", "location_text": "在州城西", "history_lore": "秦迁东周于此，吴孙坚大破董卓军亦此地"},
      {"site_id": "SITE-037", "item_id": "31-002", "geo_id": "GEO-31002", "name": "沛公垒", "type": "古迹", "location_text": "在州城东北大刘山南", "history_lore": "汉高帝入关驻此，又世祖西征亦驻此，故山有大刘小刘之异"},
      {"site_id": "SITE-038", "item_id": "31-002", "geo_id": "GEO-31002", "name": "汝帖碑", "type": "古迹", "location_text": "在州城治", "history_lore": "石凡十二刻，皆历代名人所书"}
    ],
    "prods": [
      {"prod_id": "PROD-001", "item_id": "31-002", "geo_id": "GEO-31002", "name": "铁", "category": "矿", "location_text": "州境出"},
      {"prod_id": "PROD-002", "item_id": "31-002", "geo_id": "GEO-31002", "name": "锡", "category": "矿", "location_text": "州境出"},
      {"prod_id": "PROD-003", "item_id": "31-002", "geo_id": "GEO-31002", "name": "何首乌", "category": "药", "location_text": "州境属县俱出"},
      {"prod_id": "PROD-004", "item_id": "31-002", "geo_id": "GEO-31002", "name": "荆芥", "category": "药", "location_text": "州境属县俱出"},
      {"prod_id": "PROD-005", "item_id": "31-002", "geo_id": "GEO-31002", "name": "牵牛", "category": "药", "location_text": "州境属县俱出"},
      {"prod_id": "PROD-006", "item_id": "31-002", "geo_id": "GEO-31002", "name": "草乌", "category": "药", "location_text": "州境属县俱出"},
      {"prod_id": "PROD-007", "item_id": "31-002", "geo_id": "GEO-31002", "name": "牛膝", "category": "药", "location_text": "州境属县俱出"}
    ],
    "cits": []
  },
  "layer_count": 7, "validation": {"errs": [], "gap": 0, "notes": "汝州直隶州，parent=GEO-000"}
}
ruzhou["layers"]["sites"][10]["item_id"] = "31-002"
dump("31-002_汝州.json", ruzhou)

print("DONE 31-002")
