# -*- coding: utf-8 -*-
# _geo_ai_02.py  卷二 南京地理古迹层源数据（AI 判定）
# category 枚举：山水/寺观祠庙/桥渡/都邑宫阙/陵墓/水利沟渠/园第坊巷/其他

RECORDS = [
    # ===== 02-002 蒋山 =====
    {
        "item_id": "02-002",
        "name": {"text": "钟山", "name_ent_ids": []},
        "category": "山水",
        "location": {"text": "南京东北郊", "location_ent_ids": []},
        "history": "即钟山，洪武五年广荐佛会设奉天前殿于此，宋濂撰记；金陵名山，明初佛会道场所在",
        "evidence": "原文'洪武五年正月……蒋山设广荐佛会'",
    },
    {
        "item_id": "02-002",
        "name": {"text": "灵谷寺", "name_ent_ids": []},
        "category": "寺观祠庙",
        "location": {"text": "蒋山之阳", "location_ent_ids": []},
        "history": "哈立麻尝居此奏请授记、撰《灵谷寺塔影记》；宝公法函藏此寺；海水雪景画壁、宋璲书《金刚经》刻石俱在其地",
        "evidence": "原文'灵谷寺塔影记''宝公法函''海水雪景'",
    },
    # ===== 02-003 鸡鸣寺 =====
    {
        "item_id": "02-003",
        "name": {"text": "鸡鸣寺", "name_ent_ids": []},
        "category": "寺观祠庙",
        "location": {"text": "南京城东北鸡鸣山", "location_ent_ids": []},
        "history": "铁冠道人侍太祖游此；高皇帝于此设施食台，为六代白骨施食；台下有万人坑遗迹",
        "evidence": "原文'尝游鸡鸣寺''施食台'",
    },
    # ===== 02-006 王谢居址诸迹 =====
    {
        "item_id": "02-006",
        "name": {"text": "朱雀桁（朱雀桥）", "name_ent_ids": []},
        "category": "桥渡",
        "location": {"text": "今镇淮桥，聚宝门内", "location_ent_ids": []},
        "history": "六朝朱雀桁，刘禹锡诗所咏朱雀桥，今名镇淮桥，顾起元考其方位沿革",
        "evidence": "原文'朱雀桥即朱雀桁，今镇淮桥'",
    },
    {
        "item_id": "02-006",
        "name": {"text": "乌衣巷", "name_ent_ids": []},
        "category": "园第坊巷",
        "location": {"text": "聚宝门内剪子巷、武定桥一带", "location_ent_ids": []},
        "history": "六朝王谢诸族聚居之地，今剪子巷一带；杨吴时掘城壕曾得王谢遗物",
        "evidence": "原文'乌衣巷在剪子巷至武定桥一带'",
    },
    {
        "item_id": "02-006",
        "name": {"text": "桃叶渡", "name_ent_ids": []},
        "category": "桥渡",
        "location": {"text": "今武定桥一带秦淮河畔", "location_ent_ids": []},
        "history": "王献之大令迎妾桃叶处，六朝风流遗址，今舟航往复",
        "evidence": "原文'桃叶渡为大令迎妾处'",
    },
    {
        "item_id": "02-006",
        "name": {"text": "光宅寺", "name_ent_ids": []},
        "category": "寺观祠庙",
        "location": {"text": "秣陵同夏里南冈下", "location_ent_ids": []},
        "history": "周子隐读书台所在，梁武帝生于此，宅基在南冈下即今报恩寺西天寺地",
        "evidence": "原文'周子隐读书台在光宅寺，梁武帝生秣陵同夏里'",
    },
    {
        "item_id": "02-006",
        "name": {"text": "大报恩寺", "name_ent_ids": []},
        "category": "寺观祠庙",
        "location": {"text": "聚宝门外长干里", "location_ent_ids": []},
        "history": "即大报恩寺，梁武帝宅基所在南冈之下，旁有西天寺、重译桥，六朝遗迹之地",
        "evidence": "原文'报恩寺、西天寺……长干'",
    },
    # ===== 02-007 陶镇葛乡 =====
    {
        "item_id": "02-007",
        "name": {"text": "陶吴镇", "name_ent_ids": []},
        "category": "都邑宫阙",
        "location": {"text": "秣陵县境", "location_ent_ids": []},
        "history": "陶弘景（贞白先生）故里所在之镇，今成市镇，因陶姓得名",
        "evidence": "原文'陶吴镇……陶隐居栖隐之地'",
    },
    {
        "item_id": "02-007",
        "name": {"text": "葛仙乡", "name_ent_ids": []},
        "category": "其他",
        "location": {"text": "秣陵县境", "location_ent_ids": []},
        "history": "葛仙公遗迹所在之乡，并有葛塘、葛公炼丹池（方山），葛氏仙迹相望",
        "evidence": "原文'葛仙乡、葛塘……葛公炼丹池'",
    },
    {
        "item_id": "02-007",
        "name": {"text": "方山", "name_ent_ids": []},
        "category": "山水",
        "location": {"text": "秣陵东南", "location_ent_ids": []},
        "history": "葛公炼丹池所在，形如方印，金陵名山",
        "evidence": "原文'方山有葛公炼丹池'",
    },
    {
        "item_id": "02-007",
        "name": {"text": "茅山", "name_ent_ids": []},
        "category": "山水",
        "location": {"text": "句曲境，金陵地肺", "location_ent_ids": []},
        "history": "陶弘景晚年栖隐之地（茅山朱阳馆），道教仙灵窟宅，与秣陵葛迹相望",
        "evidence": "原文'句曲、茅山……金陵地肺'",
    },
    # ===== 02-010 旧扁字诸寺观 =====
    {
        "item_id": "02-010",
        "name": {"text": "清凉广慧寺", "name_ent_ids": []},
        "category": "寺观祠庙",
        "location": {"text": "金陵石头城清凉山", "location_ent_ids": []},
        "history": "寺有德庆堂扁，南唐后主李煜撮襟书，为金陵旧扁名迹",
        "evidence": "原文'清凉广慧寺德庆堂，南唐后主撮襟书'",
    },
    {
        "item_id": "02-010",
        "name": {"text": "摄山妙因寺", "name_ent_ids": []},
        "category": "寺观祠庙",
        "location": {"text": "摄山（栖霞山）", "location_ent_ids": []},
        "history": "南唐徐铉书扁，与栖霞寺并称之名刹",
        "evidence": "原文'摄山妙因寺，南唐徐铉书'",
    },
    {
        "item_id": "02-010",
        "name": {"text": "栖霞寺", "name_ent_ids": []},
        "category": "寺观祠庙",
        "location": {"text": "摄山", "location_ent_ids": []},
        "history": "寺有仁宗旧题诸迹，金陵古刹",
        "evidence": "原文'栖霞寺……仁宗'",
    },
    # ===== 02-011 樱桃园 =====
    {
        "item_id": "02-011",
        "name": {"text": "樱桃园", "name_ent_ids": []},
        "category": "园第坊巷",
        "location": {"text": "南郭", "location_ent_ids": []},
        "history": "南郭名园，嘉靖乙卯倭寇三十六人焚掠于此，指挥蒋钦、朱湘御之死事",
        "evidence": "原文'嘉靖乙卯……樱桃园'",
    },
    # ===== 02-015 南京水陆诸路 =====
    {
        "item_id": "02-015",
        "name": {"text": "上新河", "name_ent_ids": []},
        "category": "水利沟渠",
        "location": {"text": "南京西南江滨", "location_ent_ids": []},
        "history": "金陵水陆要津，舟楫辐辏，水路线路之一",
        "evidence": "原文'上新河'",
    },
    {
        "item_id": "02-015",
        "name": {"text": "龙江关", "name_ent_ids": []},
        "category": "桥渡",
        "location": {"text": "南京西北江滨", "location_ent_ids": []},
        "history": "金陵江关要地，水路冲要",
        "evidence": "原文'龙江关'",
    },
    # ===== 02-026 坊厢乡（坊名） =====
    {
        "item_id": "02-026",
        "name": {"text": "十八坊", "name_ent_ids": []},
        "category": "都邑宫阙",
        "location": {"text": "上元县", "location_ent_ids": []},
        "history": "国初上元诸坊，以坊统民，坊名散见织锦、技艺诸类",
        "evidence": "原文'上元十八坊'",
    },
]
