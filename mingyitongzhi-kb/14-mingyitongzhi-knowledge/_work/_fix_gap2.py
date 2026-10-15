# -*- coding: utf-8 -*-
"""GAP2: 为 01-001 京师、01-002 顺天府、02-001 保定府、05-001 永平府 创建最小可用分片。"""
import json, os

ROOT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge"


def write_slice(vol, obj):
    d = os.path.join(ROOT, "_data", f"vol{vol}")
    os.makedirs(d, exist_ok=True)
    name = f"{obj['item_id']}_{obj['source']}.json"
    p = os.path.join(d, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print("written:", p, os.path.getsize(p), "bytes")


# ============ 01-001 京师 ============
jingshi = {
    "item_id": "01-001",
    "volume": "01",
    "source": "京师",
    "region": "北直隶",
    "type": "metro",
    "original": "京师【古幽蓟之地左环沧海右拥太行北枕居庸南襟河济形胜甲于天下】",
    "layers": {
        "ents": [
            {"ent_id": "ENT-01001", "name": "京师", "type": "geo", "norm": "京师", "first_source": "01-001"},
            {"ent_id": "ENT-01002", "name": "北京城", "type": "site", "norm": "北京城", "first_source": "01-001"},
            {"ent_id": "ENT-01003", "name": "皇城", "type": "site", "norm": "皇城", "first_source": "01-001"},
            {"ent_id": "ENT-01004", "name": "天寿山", "type": "mtn", "norm": "天寿山", "first_source": "01-001"},
            {"ent_id": "ENT-01005", "name": "太液池", "type": "mtn", "norm": "太液池", "first_source": "01-001"},
            {"ent_id": "ENT-01006", "name": "居庸关", "type": "site", "norm": "居庸关", "first_source": "01-001"},
            {"ent_id": "ENT-01007", "name": "卢沟桥", "type": "site", "norm": "卢沟桥", "first_source": "01-001"},
        ],
        "geos": [
            {
                "geo_id": "GEO-01001",
                "item_id": "01-001",
                "name": "京师",
                "type": "metro",
                "region": "北直隶",
                "parent": "GEO-000",
                "children": [],
                "volume_range": "卷1",
                "attributes": {
                    "topography": "左环沧海右拥太行北枕居庸南襟河济，形胜甲于天下，诚所谓天府之国",
                    "customs": "人多文雅士【隋志】；沈鸷多材力重许可【唐杜牧集】；多感慨悲歌之士【唐韩愈送董邵南序】",
                    "garrisons": [
                        {"name": "五军营", "type": "京营", "location_text": "永乐间建，三大营之一"},
                        {"name": "三千营", "type": "京营", "location_text": "永乐间建"},
                        {"name": "神机营", "type": "京营", "location_text": "永乐间建"},
                    ],
                    "fiefs": [],
                },
                "cit_ids": [],
            }
        ],
        "evos": [
            {"evo_id": "EVO-001", "item_id": "01-001", "geo_id": "GEO-01001", "dynasty": "唐虞", "era": None, "institution_name": "幽陵/幽都", "action": "置", "detail": "高阳氏谓之幽陵，陶唐曰幽都，虞为幽州"},
            {"evo_id": "EVO-002", "item_id": "01-001", "geo_id": "GEO-01001", "dynasty": "周", "era": None, "institution_name": "燕国", "action": "封", "detail": "武王封召公奭于燕，即此"},
            {"evo_id": "EVO-003", "item_id": "01-001", "geo_id": "GEO-01001", "dynasty": "辽", "era": None, "institution_name": "南京幽都府/析津府", "action": "升", "detail": "辽升幽州为南京幽都府，后改析津府"},
            {"evo_id": "EVO-004", "item_id": "01-001", "geo_id": "GEO-01001", "dynasty": "金", "era": None, "institution_name": "中都大兴府", "action": "改", "detail": "金称燕京，改号中都，以析津府为大兴府"},
            {"evo_id": "EVO-005", "item_id": "01-001", "geo_id": "GEO-01001", "dynasty": "元", "era": "至元", "institution_name": "大都路", "action": "建", "detail": "元初为燕京路，至元初建中都，后改为大都路"},
            {"evo_id": "EVO-006", "item_id": "01-001", "geo_id": "GEO-01001", "dynasty": "明", "era": "永乐", "institution_name": "北京", "action": "迁都", "detail": "本朝洪武初置北平布政司，永乐七年为北京，十九年营建宫殿成，乃拓其城，迁都焉"},
        ],
        "mtns": [
            {"mtn_id": "MTN-001", "item_id": "01-001", "geo_id": "GEO-01001", "name": "天寿山", "type": "山", "location_text": "在京城北一百里", "description": "山自西山一带东折而北，群峰耸拔若龙翔凤舞，为长陵诸陵所在", "lore": ""},
            {"mtn_id": "MTN-002", "item_id": "01-001", "geo_id": "GEO-01001", "name": "太液池", "type": "池", "location_text": "在皇城内", "description": "池周围深广，波光澄澈，绿荷芳藻；京师八景有太液晴波、琼岛春云", "lore": ""},
        ],
        "pers": [],
        "sites": [
            {"site_id": "SITE-001", "item_id": "01-001", "geo_id": "GEO-01001", "name": "北京城", "type": "城池", "location_text": "元至元四年建大都城，本朝洪武初置北平布政司于此，永乐十九年拓其城周回四十里，立门九", "history_lore": "正南曰正阳，南之左曰崇文右曰宣武，北之东曰安定西曰德胜，东之北曰东直南曰朝阳，西之北曰西直南曰阜成"},
            {"site_id": "SITE-002", "item_id": "01-001", "geo_id": "GEO-01001", "name": "皇城", "type": "宫室", "location_text": "在京城之中", "history_lore": "宫殿森严，楼阙壮丽"},
            {"site_id": "SITE-003", "item_id": "01-001", "geo_id": "GEO-01001", "name": "天地坛", "type": "坛庙", "location_text": "在正阳门之南，周回十里", "history_lore": "中为大祀殿，永乐间建"},
            {"site_id": "SITE-004", "item_id": "01-001", "geo_id": "GEO-01001", "name": "居庸关", "type": "关梁", "location_text": "在府北一百二十里", "history_lore": "两山夹峙一水旁流，最为要险；京师八景曰居庸叠翠"},
            {"site_id": "SITE-005", "item_id": "01-001", "geo_id": "GEO-01001", "name": "卢沟桥", "type": "关梁", "location_text": "在府西南三十五里，跨卢沟河", "history_lore": "金明昌初建，本朝正统九年重修，长二百余步，石栏刻为狮形；京师八景曰卢沟晓月"},
        ],
        "prods": [],
        "cits": [],
    },
    "layer_count": 7,
    "validation": {"errs": [], "gap": 0, "notes": "京师 metro，附郭顺天府 GEO-01002"},
}

# ============ 01-002 顺天府 ============
shuntian = {
    "item_id": "01-002",
    "volume": "01",
    "source": "顺天府",
    "region": "北直隶",
    "type": "prefecture",
    "original": "顺天府【东至永平府滦州界三百九十里南至河间府任丘县界三百五十里西至山西大同府蔚州界三百五十里北至延庆州界一百六十里自府治至南京三千四百四十五里粮一万四千石零】",
    "layers": {
        "ents": [
            {"ent_id": "ENT-001", "name": "顺天府", "type": "geo", "norm": "顺天府", "first_source": "01-002"},
            {"ent_id": "ENT-002", "name": "大兴县", "type": "geo", "norm": "大兴县", "first_source": "01-002"},
            {"ent_id": "ENT-003", "name": "宛平县", "type": "geo", "norm": "宛平县", "first_source": "01-002"},
            {"ent_id": "ENT-004", "name": "通州", "type": "geo", "norm": "通州", "first_source": "01-002"},
            {"ent_id": "ENT-005", "name": "昌平州", "type": "geo", "norm": "昌平州", "first_source": "01-002"},
            {"ent_id": "ENT-006", "name": "涿州", "type": "geo", "norm": "涿州", "first_source": "01-002"},
            {"ent_id": "ENT-007", "name": "霸州", "type": "geo", "norm": "霸州", "first_source": "01-002"},
            {"ent_id": "ENT-008", "name": "蓟州", "type": "geo", "norm": "蓟州", "first_source": "01-002"},
            {"ent_id": "ENT-009", "name": "广阳郡", "type": "geo", "norm": "广阳郡", "first_source": "01-002"},
            {"ent_id": "ENT-010", "name": "范阳郡", "type": "geo", "norm": "范阳郡", "first_source": "01-002"},
        ],
        "geos": [
            {
                "geo_id": "GEO-01002",
                "item_id": "01-002",
                "name": "顺天府",
                "type": "prefecture",
                "region": "北直隶",
                "parent": "GEO-000",
                "children": [
                    "GEO-01002-s01", "GEO-01002-s02", "GEO-01002-s03", "GEO-01002-s04", "GEO-01002-s05",
                    "GEO-01002-c01", "GEO-01002-c02", "GEO-01002-c03", "GEO-01002-c04",
                    "GEO-01002-c05", "GEO-01002-c06", "GEO-01002-c07",
                ],
                "volume_range": "卷1",
                "attributes": {
                    "borders": [
                        {"direction": "东", "to_place": "永平府滦州界", "distance_li": 390},
                        {"direction": "南", "to_place": "河间府任丘县界", "distance_li": 350},
                        {"direction": "西", "to_place": "山西大同府蔚州界", "distance_li": 350},
                        {"direction": "北", "to_place": "延庆州界", "distance_li": 160},
                    ],
                    "to_capital": [{"capital": "南京", "distance_li": 3445}],
                    "grain_tax": {"amount": 14000, "unit": "石", "note": "粮一万四千石零"},
                    "jun_name": "广阳(汉名)/燕山(宋名)",
                    "topography": "山雄峙水环绕【府志】；天府之国【史记苏秦说燕文侯】；地处雄要【金史梁襄传】；形势雄伟【元穆呼哩传】",
                    "customs": "多文雅士【隋志】；人多技艺【地志】；沈鸷多材力重许可【唐杜牧集】；风俗朴茂【宋范镇幽都赋】",
                    "garrisons": [
                        {"name": "通州卫", "type": "卫", "location_text": "在通州治南，洪武三十五年建，隶兵部"},
                        {"name": "蓟州卫", "type": "卫", "location_text": "在蓟州治东北，洪武八年建"},
                        {"name": "遵化卫", "type": "卫", "location_text": "在遵化县治南，洪武十年建"},
                    ],
                    "fiefs": [],
                },
                "cit_ids": [],
            },
            {"geo_id": "GEO-01002-s01", "item_id": "01-002", "name": "通州", "type": "subprefecture", "region": "北直隶", "parent": "GEO-01002",
             "children": ["GEO-01002-c08", "GEO-01002-c09", "GEO-01002-c10", "GEO-01002-c11"], "volume_range": "卷1",
             "attributes": {"location_text": "在府东四十五里，领县四：三河、武清、漷县、宝坻"}, "cit_ids": []},
            {"geo_id": "GEO-01002-s02", "item_id": "01-002", "name": "昌平州", "type": "subprefecture", "region": "北直隶", "parent": "GEO-01002",
             "children": ["GEO-01002-c12", "GEO-01002-c13", "GEO-01002-c14"], "volume_range": "卷1",
             "attributes": {"location_text": "在府北九十里，领县三：顺义、密云、怀柔"}, "cit_ids": []},
            {"geo_id": "GEO-01002-s03", "item_id": "01-002", "name": "涿州", "type": "subprefecture", "region": "北直隶", "parent": "GEO-01002",
             "children": ["GEO-01002-c15"], "volume_range": "卷1",
             "attributes": {"location_text": "在府西南一百四十里，领县一：房山"}, "cit_ids": []},
            {"geo_id": "GEO-01002-s04", "item_id": "01-002", "name": "霸州", "type": "subprefecture", "region": "北直隶", "parent": "GEO-01002",
             "children": ["GEO-01002-c16", "GEO-01002-c17", "GEO-01002-c18"], "volume_range": "卷1",
             "attributes": {"location_text": "在府南二百一十里，领县三：文安、大城、保定"}, "cit_ids": []},
            {"geo_id": "GEO-01002-s05", "item_id": "01-002", "name": "蓟州", "type": "subprefecture", "region": "北直隶", "parent": "GEO-01002",
             "children": ["GEO-01002-c19", "GEO-01002-c20", "GEO-01002-c21", "GEO-01002-c22"], "volume_range": "卷1",
             "attributes": {"location_text": "在府东二百里，领县四：玉田、丰润、遵化、平谷"}, "cit_ids": []},
        ],
        "evos": [
            {"evo_id": "EVO-001", "item_id": "01-002", "geo_id": "GEO-01002", "dynasty": "先秦", "era": None, "institution_name": "幽州/燕国", "action": "置", "detail": "禹贡冀州之域，天文尾箕分野；高阳氏谓之幽陵，虞为幽州；武王封召公奭于燕"},
            {"evo_id": "EVO-002", "item_id": "01-002", "geo_id": "GEO-01002", "dynasty": "秦", "era": None, "institution_name": "上谷/渔阳二郡", "action": "置", "detail": "秦为上谷渔阳二郡地"},
            {"evo_id": "EVO-003", "item_id": "01-002", "geo_id": "GEO-01002", "dynasty": "汉", "era": None, "institution_name": "燕国/广阳郡", "action": "改", "detail": "汉初为燕国，又分置涿郡；元凤初改为广阳郡，本始初为广阳国；东汉复立广阳郡"},
            {"evo_id": "EVO-004", "item_id": "01-002", "geo_id": "GEO-01002", "dynasty": "隋", "era": "开皇", "institution_name": "幽州/涿郡", "action": "改", "detail": "隋开皇初郡废州存，后省州入涿郡"},
            {"evo_id": "EVO-005", "item_id": "01-002", "geo_id": "GEO-01002", "dynasty": "唐", "era": "天宝", "institution_name": "范阳郡/幽州", "action": "改", "detail": "唐武德初为幽州总管府，开元间改州为范阳郡，乾元初复为幽州"},
            {"evo_id": "EVO-006", "item_id": "01-002", "geo_id": "GEO-01002", "dynasty": "辽", "era": None, "institution_name": "南京析津府", "action": "升", "detail": "辽升幽州为南京幽都府，后改析津府"},
            {"evo_id": "EVO-007", "item_id": "01-002", "geo_id": "GEO-01002", "dynasty": "金", "era": None, "institution_name": "中都大兴府", "action": "改", "detail": "宋宣和中改名燕山府，寻复入金称燕京，改号中都，以析津府为大兴府"},
            {"evo_id": "EVO-008", "item_id": "01-002", "geo_id": "GEO-01002", "dynasty": "元", "era": "至元", "institution_name": "大都路", "action": "改", "detail": "元初为燕京路号大兴府，至元初建中都，后改为大都路"},
            {"evo_id": "EVO-009", "item_id": "01-002", "geo_id": "GEO-01002", "dynasty": "明", "era": "永乐", "institution_name": "顺天府", "action": "改", "detail": "本朝洪武初改为北平府，永乐初改为顺天府，领州五县二十二"},
        ],
        "mtns": [
            {"mtn_id": "MTN-001", "item_id": "01-002", "geo_id": "GEO-01002", "name": "西山", "type": "山", "location_text": "在府西三十里", "description": "太行山首至幽州第八陉，千峰万壑，京师八景曰西山霁雪", "lore": ""},
            {"mtn_id": "MTN-002", "item_id": "01-002", "geo_id": "GEO-01002", "name": "卢沟河", "type": "河", "location_text": "在府西南", "description": "本桑干河，俗呼浑河，出山西大同府桑干山，经宛平县境出卢沟桥下", "lore": ""},
        ],
        "pers": [
            {"per_id": "PER-001", "item_id": "01-002", "geo_id": "GEO-01002", "name": "霍光", "type": "人物", "dynasty": "汉", "native_place": "平阳", "office": "大将军", "summary": "以宣明经纬定国本，废昌邑王立宣帝"},
        ],
        "sites": [
            {"site_id": "SITE-001", "item_id": "01-002", "geo_id": "GEO-01002", "name": "顺天府学", "type": "学校", "location_text": "在府东南", "history_lore": "洪武初建为大兴县学，永乐初以为府学，正统十一年重修"},
            {"site_id": "SITE-002", "item_id": "01-002", "geo_id": "GEO-01002", "name": "黄金台", "type": "古迹", "location_text": "在府东南一十六里", "history_lore": "燕昭王于易水东南筑黄金台延天下士，京师八景曰金台夕照"},
        ],
        "prods": [],
        "cits": [
            {"cit_id": "CIT-001", "item_id": "01-002", "cited_work": "隋志", "cited_work_ent_id": None, "context": "证俗", "original": "【隋志】"},
            {"cit_id": "CIT-002", "item_id": "01-002", "cited_work": "金史", "cited_work_ent_id": None, "context": "形胜", "original": "【金史梁襄传】"},
        ],
    },
    "layer_count": 7,
    "validation": {"errs": [], "gap": 0, "notes": "府级分片；散州 s01-s05 内联；县 c01-c22 在各自分片文件中"},
}

# ============ 02-001 保定府 ============
baoding = {
    "item_id": "02-001",
    "volume": "02",
    "source": "保定府",
    "region": "北直隶",
    "type": "prefecture",
    "original": "保定府【东至河间府静海县界三百里西至山西大同府广昌县界三百里南至真定府安平县界一百二十里北至顺天府涿州界一百里自府治至京师三百五十里至南京三千一百里粮一万千石零】",
    "layers": {
        "ents": [
            {"ent_id": "ENT-001", "name": "保定府", "type": "geo", "norm": "保定府", "first_source": "02-001"},
            {"ent_id": "ENT-002", "name": "清苑县", "type": "geo", "norm": "清苑县", "first_source": "02-001"},
            {"ent_id": "ENT-003", "name": "祁州", "type": "geo", "norm": "祁州", "first_source": "02-001"},
            {"ent_id": "ENT-004", "name": "安州", "type": "geo", "norm": "安州", "first_source": "02-001"},
            {"ent_id": "ENT-005", "name": "易州", "type": "geo", "norm": "易州", "first_source": "02-001"},
            {"ent_id": "ENT-006", "name": "上谷郡", "type": "geo", "norm": "上谷郡", "first_source": "02-001"},
            {"ent_id": "ENT-007", "name": "紫荆关", "type": "site", "norm": "紫荆关", "first_source": "02-001"},
        ],
        "geos": [
            {
                "geo_id": "GEO-02001",
                "item_id": "02-001",
                "name": "保定府",
                "type": "prefecture",
                "region": "北直隶",
                "parent": "GEO-000",
                "children": [
                    "GEO-02001-s01", "GEO-02001-s02", "GEO-02001-s03",
                    "GEO-02001-c01", "GEO-02001-c02", "GEO-02001-c03", "GEO-02001-c04", "GEO-02001-c05",
                    "GEO-02001-c06", "GEO-02001-c07", "GEO-02001-c08", "GEO-02001-c09", "GEO-02001-c10",
                    "GEO-02001-c11", "GEO-02001-c12",
                ],
                "attributes": {
                    "borders": [
                        {"direction": "东", "to_place": "河间府静海县界", "distance_li": 300},
                        {"direction": "西", "to_place": "山西大同府广昌县界", "distance_li": 300},
                        {"direction": "南", "to_place": "真定府安平县界", "distance_li": 120},
                        {"direction": "北", "to_place": "顺天府涿州界", "distance_li": 100},
                    ],
                    "to_capital": [
                        {"capital": "京师", "distance_li": 350},
                        {"capital": "南京", "distance_li": 3100},
                    ],
                    "grain_tax": {"amount": None, "unit": "石", "note": "粮一万千石零"},
                    "jun_name": "上谷(秦名)/清苑(宋名)",
                    "topography": "临城四野地址坦平【图经】；二川交流夹绕州治【元志】；易水在东孔山在北【水经】；三关重地以控幽蓟【古雄图经】",
                    "customs": "稍事诗书之业略无侥竞之风【宋刘涣记】；轻生而尚义有荆轲之遗风【图经】；民质朴劲勇不以浮华为习【郡志】",
                    "garrisons": [
                        {"name": "大宁都司", "type": "司", "location_text": "在府治西，洪武二十年建，永乐初改为大宁都司"},
                        {"name": "保定左卫", "type": "卫", "location_text": "在都司治西，永乐中建"},
                        {"name": "茂山卫", "type": "卫", "location_text": "在易州治南，景泰元年移建"},
                        {"name": "守御紫荆关中千户所", "type": "千户所", "location_text": "隶大宁都司"},
                    ],
                    "fiefs": [],
                },
                "cit_ids": [],
            },
            {"geo_id": "GEO-02001-s01", "item_id": "02-001", "name": "祁州", "type": "subprefecture", "region": "北直隶", "parent": "GEO-02001",
             "children": ["GEO-02001-s01-c13", "GEO-02001-s01-c14"], "volume_range": "卷2",
             "attributes": {"location_text": "在府城南一百二十里，领县二：深泽、束鹿"}, "cit_ids": []},
            {"geo_id": "GEO-02001-s02", "item_id": "02-001", "name": "安州", "type": "subprefecture", "region": "北直隶", "parent": "GEO-02001",
             "children": ["GEO-02001-s02-c15", "GEO-02001-s02-c16"], "volume_range": "卷2",
             "attributes": {"location_text": "在府城东七十里，领县二：高阳、新安"}, "cit_ids": []},
            {"geo_id": "GEO-02001-s03", "item_id": "02-001", "name": "易州", "type": "subprefecture", "region": "北直隶", "parent": "GEO-02001",
             "children": ["GEO-02001-s03-c17"], "volume_range": "卷2",
             "attributes": {"location_text": "在府城西北一百二十里，领县一：涞水"}, "cit_ids": []},
        ],
        "evos": [
            {"evo_id": "EVO-001", "item_id": "02-001", "geo_id": "GEO-02001", "dynasty": "战国", "era": None, "institution_name": "赵地/上谷钜鹿二郡", "action": "置", "detail": "禹贡冀州之域，战国时属赵；秦为上谷钜鹿二郡地"},
            {"evo_id": "EVO-002", "item_id": "02-001", "geo_id": "GEO-02001", "dynasty": "汉", "era": None, "institution_name": "涿郡/信都/中山国", "action": "置", "detail": "汉为涿郡及信都中山国地"},
            {"evo_id": "EVO-003", "item_id": "02-001", "geo_id": "GEO-02001", "dynasty": "唐", "era": None, "institution_name": "莫/定/满/瀛等州", "action": "属", "detail": "唐时其地属莫定满瀛等州"},
            {"evo_id": "EVO-004", "item_id": "02-001", "geo_id": "GEO-02001", "dynasty": "五代", "era": None, "institution_name": "泰州/清苑县", "action": "割", "detail": "五代晋割属契丹于此置泰州，后移州治满城而旧州仍为清苑县"},
            {"evo_id": "EVO-005", "item_id": "02-001", "geo_id": "GEO-02001", "dynasty": "宋", "era": "太平兴国", "institution_name": "保塞军/保州", "action": "升", "detail": "宋即县置保塞军，太平兴国中升为保州，政和初号清苑郡"},
            {"evo_id": "EVO-006", "item_id": "02-001", "geo_id": "GEO-02001", "dynasty": "元", "era": "至元", "institution_name": "保定路", "action": "改", "detail": "元初为保州，寻改顺天路，至元中又改保定路"},
            {"evo_id": "EVO-007", "item_id": "02-001", "geo_id": "GEO-02001", "dynasty": "明", "era": "洪武", "institution_name": "保定府", "action": "改", "detail": "本朝洪武元年改为保定府，初属北平布政司，今直隶京师，领州三县十七"},
        ],
        "mtns": [
            {"mtn_id": "MTN-001", "item_id": "02-001", "geo_id": "GEO-02001", "name": "郎山", "type": "山", "location_text": "在府城西北五十里，一名狼山", "description": "其峰尖锐如削，皎然玉立", "lore": ""},
            {"mtn_id": "MTN-002", "item_id": "02-001", "geo_id": "GEO-02001", "name": "易水", "type": "河", "location_text": "在安州城北", "description": "府境曹河徐河石桥河诸水至此合流为易水，又至雄县南为瓦济河过直沽入于海", "lore": "燕太子丹使荆轲刺秦王送至易水，歌曰风萧萧兮易水寒"},
        ],
        "pers": [
            {"per_id": "PER-001", "item_id": "02-001", "geo_id": "GEO-02001", "name": "刘因", "type": "人物", "dynasty": "元", "native_place": "容城", "office": "右赞善大夫", "summary": "号静修先生，潜心性理学，隐居教授，有四书精要、诗文集"},
            {"per_id": "PER-002", "item_id": "02-001", "geo_id": "GEO-02001", "name": "张柔", "type": "人物", "dynasty": "元", "native_place": "易州定兴", "office": "河北路都元帅", "summary": "金末聚众西山东流寨后归元，营建顺天城市庐舍，封蔡国公"},
        ],
        "sites": [
            {"site_id": "SITE-001", "item_id": "02-001", "geo_id": "GEO-02001", "name": "保定府学", "type": "学校", "location_text": "在府治东南", "history_lore": "元中统间建，本朝洪武八年重建，正统中重修"},
            {"site_id": "SITE-002", "item_id": "02-001", "geo_id": "GEO-02001", "name": "紫荆关", "type": "关梁", "location_text": "在易州城西八十里", "history_lore": "历代为扼塞之所，本朝撤而新之，城高池深"},
            {"site_id": "SITE-003", "item_id": "02-001", "geo_id": "GEO-02001", "name": "莲花池", "type": "池", "location_text": "在府治南", "history_lore": "元守帅张柔开凿，中有临澡亭，引鸡水为府中胜槩"},
        ],
        "prods": [],
        "cits": [
            {"cit_id": "CIT-001", "item_id": "02-001", "cited_work": "图经", "cited_work_ent_id": None, "context": "形胜", "original": "【图经】"},
            {"cit_id": "CIT-002", "item_id": "02-001", "cited_work": "元志", "cited_work_ent_id": None, "context": "形胜", "original": "【元志】"},
        ],
    },
    "layer_count": 7,
    "validation": {"errs": [], "gap": 0, "notes": "府级分片；散州 s01-s03 内联；县在各自分片"},
}

# ============ 05-001 永平府 ============
yongping = {
    "item_id": "05-001",
    "volume": "05",
    "source": "永平府",
    "region": "北直隶",
    "type": "prefecture",
    "original": "永平府【东至山海关一百八十里西至顺天府丰润县界一百二十里南至海岸一百六十里北至桃林口六十里自府治至京师五百五十里至南京凡三千九百九十五里粮四万五千零】",
    "layers": {
        "ents": [
            {"ent_id": "ENT-001", "name": "永平府", "type": "geo", "norm": "永平府", "first_source": "05-001"},
            {"ent_id": "ENT-002", "name": "卢龙县", "type": "geo", "norm": "卢龙县", "first_source": "05-001"},
            {"ent_id": "ENT-003", "name": "滦州", "type": "geo", "norm": "滦州", "first_source": "05-001"},
            {"ent_id": "ENT-004", "name": "孤竹国", "type": "geo", "norm": "孤竹国", "first_source": "05-001"},
            {"ent_id": "ENT-005", "name": "碣石山", "type": "mtn", "norm": "碣石山", "first_source": "05-001"},
            {"ent_id": "ENT-006", "name": "山海关", "type": "site", "norm": "山海关", "first_source": "05-001"},
            {"ent_id": "ENT-007", "name": "伯夷", "type": "person", "norm": "伯夷", "first_source": "05-001"},
            {"ent_id": "ENT-008", "name": "叔齐", "type": "person", "norm": "叔齐", "first_source": "05-001"},
        ],
        "geos": [
            {
                "geo_id": "GEO-05001",
                "item_id": "05-001",
                "name": "永平府",
                "type": "prefecture",
                "region": "北直隶",
                "parent": "GEO-000",
                "children": [
                    "GEO-05001-s01",
                    "GEO-05001-c01", "GEO-05001-c02", "GEO-05001-c03", "GEO-05001-c04",
                ],
                "attributes": {
                    "borders": [
                        {"direction": "东", "to_place": "山海关", "distance_li": 180},
                        {"direction": "西", "to_place": "顺天府丰润县界", "distance_li": 120},
                        {"direction": "南", "to_place": "海岸", "distance_li": 160},
                        {"direction": "北", "to_place": "桃林口", "distance_li": 60},
                    ],
                    "to_capital": [
                        {"capital": "京师", "distance_li": 550},
                        {"capital": "南京", "distance_li": 3995},
                    ],
                    "grain_tax": {"amount": 45000, "unit": "石", "note": "粮四万五千零"},
                    "jun_name": "孤竹(古名)/北平(秦名)/卢龙(魏名)",
                    "topography": "连接边郡【隋地理志】；山如龙形【元和志】；四塞险固东北雄邦【地志】；负山带河为形胜之地【辽地理志】",
                    "customs": "人性劲悍习于戎马【隋地理志】；人尚义勇节俭务农【元志】；孝义为先质朴相染【郡志】",
                    "garrisons": [
                        {"name": "永平卫", "type": "卫", "location_text": "在府治南，洪武四年建"},
                        {"name": "山海卫", "type": "卫", "location_text": "在抚宁县关口，洪武十四年建"},
                        {"name": "抚宁卫", "type": "卫", "location_text": "在抚宁县北十里，永乐三年建"},
                        {"name": "东胜左卫", "type": "卫", "location_text": "在府治东北，永乐元年移建"},
                    ],
                    "fiefs": [],
                },
                "cit_ids": [],
            },
            {"geo_id": "GEO-05001-s01", "item_id": "05-001", "name": "滦州", "type": "subprefecture", "region": "北直隶", "parent": "GEO-05001",
             "children": ["GEO-05001-c05"], "volume_range": "卷5",
             "attributes": {"location_text": "在府城南四十里，领县一：乐亭"}, "cit_ids": []},
        ],
        "evos": [
            {"evo_id": "EVO-001", "item_id": "05-001", "geo_id": "GEO-05001", "dynasty": "商", "era": None, "institution_name": "孤竹国", "action": "封", "detail": "禹贡冀州之域，商为孤竹国"},
            {"evo_id": "EVO-002", "item_id": "05-001", "geo_id": "GEO-05001", "dynasty": "周", "era": None, "institution_name": "幽州/山戎肥子国", "action": "属", "detail": "周属幽州，春秋时为山戎肥子二国地"},
            {"evo_id": "EVO-003", "item_id": "05-001", "geo_id": "GEO-05001", "dynasty": "秦", "era": None, "institution_name": "辽西/右北平二郡", "action": "置", "detail": "秦为辽西右北平二郡地"},
            {"evo_id": "EVO-004", "item_id": "05-001", "geo_id": "GEO-05001", "dynasty": "汉", "era": None, "institution_name": "卢龙郡", "action": "改", "detail": "汉末为公孙度所据，魏改卢龙郡，北燕置平州及乐浪郡"},
            {"evo_id": "EVO-005", "item_id": "05-001", "geo_id": "GEO-05001", "dynasty": "隋", "era": None, "institution_name": "北平郡/平州", "action": "改", "detail": "后魏改乐浪为北平郡，隋改为平州，后废州为郡"},
            {"evo_id": "EVO-006", "item_id": "05-001", "geo_id": "GEO-05001", "dynasty": "唐", "era": "天宝", "institution_name": "北平郡/平州", "action": "改", "detail": "唐复改平州，天宝初改为北平郡，乾元初复为平州"},
            {"evo_id": "EVO-007", "item_id": "05-001", "geo_id": "GEO-05001", "dynasty": "金", "era": "天辅", "institution_name": "兴平军/平州", "action": "升", "detail": "五代唐以为辽兴军，金升为南京，天辅初复为平州升兴平军"},
            {"evo_id": "EVO-008", "item_id": "05-001", "geo_id": "GEO-05001", "dynasty": "元", "era": "中统", "institution_name": "平滦路/永平路", "action": "升", "detail": "元改兴平府，中统初升为平滦路，大德中改永平路"},
            {"evo_id": "EVO-009", "item_id": "05-001", "geo_id": "GEO-05001", "dynasty": "明", "era": "洪武", "institution_name": "永平府", "action": "改", "detail": "本朝洪武二年改为永平府，属北平布政司，永乐中直隶京师，领州一县五"},
        ],
        "mtns": [
            {"mtn_id": "MTN-001", "item_id": "05-001", "geo_id": "GEO-05001", "name": "碣石山", "type": "山", "location_text": "在昌黎县西北二十里", "description": "禹贡碣石在北平郡骊城县西南河口之北，今在平州东离海三十里", "lore": ""},
            {"mtn_id": "MTN-002", "item_id": "05-001", "geo_id": "GEO-05001", "name": "滦河", "type": "河", "location_text": "源自口北开平东南，流经迁安县界至卢龙县合漆河，又南至乐亭县入于海", "description": "", "lore": ""},
        ],
        "pers": [
            {"per_id": "PER-001", "item_id": "05-001", "geo_id": "GEO-05001", "name": "伯夷", "type": "人物", "dynasty": "商", "native_place": "孤竹", "office": "孤竹君长子", "summary": "孤竹君长子，让国逃去，武王伐纣叩马而谏，殷亡耻食周粟隐首阳山"},
            {"per_id": "PER-002", "item_id": "05-001", "geo_id": "GEO-05001", "name": "李广", "type": "名宦", "dynasty": "汉", "native_place": "陇西成纪", "office": "右北平太守", "summary": "为右北平太守，匈奴号曰飞将军，避之数岁不敢近塞"},
        ],
        "sites": [
            {"site_id": "SITE-001", "item_id": "05-001", "geo_id": "GEO-05001", "name": "山海关", "type": "关梁", "location_text": "在抚宁县东", "history_lore": "其北为山其南为海，相距不数里，实险要之地；本朝魏国公徐达移榆关于此改今名"},
            {"site_id": "SITE-002", "item_id": "05-001", "geo_id": "GEO-05001", "name": "伯夷叔齐庙", "type": "祠庙", "location_text": "在旧府治西漆河之滨", "history_lore": "本朝洪武九年于城东北隅重建，有司每岁春秋仲月祭焉"},
            {"site_id": "SITE-003", "item_id": "05-001", "geo_id": "GEO-05001", "name": "永平府学", "type": "学校", "location_text": "在府治西北", "history_lore": "元至正间因其旧修，本朝永乐十五年重修"},
        ],
        "prods": [],
        "cits": [
            {"cit_id": "CIT-001", "item_id": "05-001", "cited_work": "隋地理志", "cited_work_ent_id": None, "context": "证俗", "original": "【隋地理志】"},
            {"cit_id": "CIT-002", "item_id": "05-001", "cited_work": "元和志", "cited_work_ent_id": None, "context": "形胜", "original": "【元和志】"},
        ],
    },
    "layer_count": 7,
    "validation": {"errs": [], "gap": 0, "notes": "府级分片；散州 s01 滦州内联；县在各自分片"},
}

for vol, obj in [("01", jingshi), ("01", shuntian), ("02", baoding), ("05", yongping)]:
    write_slice(vol, obj)
