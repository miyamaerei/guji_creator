# -*- coding: utf-8 -*-
# _cit_ai_01.py  卷一 引书索引层源数据（AI 判定）
# citation_type：直引/转引/泛引/暗用/考辨；context：立论/证俗/考源/反驳/补遗/其他

RECORDS = [
    # 01-001 经义兼古注疏（科举成式所定注本体系）
    {
        "item_id": "01-001",
        "cited_work": {"text": "《易》程朱氏注", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "考源",
    },
    {
        "item_id": "01-001",
        "cited_work": {"text": "《书》蔡氏传", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "考源",
    },
    {
        "item_id": "01-001",
        "cited_work": {"text": "《诗》朱氏传", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "考源",
    },
    {
        "item_id": "01-001",
        "cited_work": {"text": "《春秋》左氏、公羊、穀梁、张洽传", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "考源",
    },
    {
        "item_id": "01-001",
        "cited_work": {"text": "《礼记》古注疏", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "考源",
    },
    {
        "item_id": "01-001",
        "cited_work": {"text": "《四书》朱子《集注》", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "考源",
    },
    {
        "item_id": "01-001",
        "cited_work": {"text": "《礼记》陈灏集说", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "考源",
    },
    # 01-005 辨讹
    {
        "item_id": "01-005",
        "cited_work": {"text": "《论语》", "cited_ent_ids": []},
        "citation_type": "直引",
        "context": "立论",
    },
    {
        "item_id": "01-005",
        "cited_work": {"text": "韩愈《辛卯年雪》诗", "cited_ent_ids": []},
        "citation_type": "直引",
        "context": "考源",
    },
    # 01-009 父母称谓
    {
        "item_id": "01-009",
        "cited_work": {"text": "《北史》", "cited_ent_ids": []},
        "citation_type": "直引",
        "context": "考源",
    },
    {
        "item_id": "01-009",
        "cited_work": {"text": "唐小说", "cited_ent_ids": []},
        "citation_type": "直引",
        "context": "考源",
    },
    # 01-011 南唐都城
    {
        "item_id": "01-011",
        "cited_work": {"text": "陈同甫言（陈亮）", "cited_ent_ids": []},
        "citation_type": "转引",
        "context": "立论",
    },
    {
        "item_id": "01-011",
        "cited_work": {"text": "陈鲁南《金陵图》", "cited_ent_ids": []},
        "citation_type": "转引",
        "context": "考源",
    },
    {
        "item_id": "01-011",
        "cited_work": {"text": "《记》（六朝都城方位）", "cited_ent_ids": []},
        "citation_type": "转引",
        "context": "立论",
    },
    # 01-012 珍物
    {
        "item_id": "01-012",
        "cited_work": {"text": "周颙语（秋末晚菘）", "cited_ent_ids": []},
        "citation_type": "直引",
        "context": "考源",
    },
    {
        "item_id": "01-012",
        "cited_work": {"text": "《南畿志》", "cited_ent_ids": []},
        "citation_type": "转引",
        "context": "补遗",
    },
    # 01-013 花木二十二则
    {
        "item_id": "01-013",
        "cited_work": {"text": "卢苑马《东篱品汇录》", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "证俗",
    },
    {
        "item_id": "01-013",
        "cited_work": {"text": "游九言《丽春花谱》", "cited_ent_ids": []},
        "citation_type": "转引",
        "context": "考源",
    },
    {
        "item_id": "01-013",
        "cited_work": {"text": "戴凯之《竹谱》", "cited_ent_ids": []},
        "citation_type": "直引",
        "context": "考源",
    },
    # 01-014 禽鱼十一则
    {
        "item_id": "01-014",
        "cited_work": {"text": "谢庄《赤鹦鹉赋》", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "考源",
    },
    # 01-015 笼养
    {
        "item_id": "01-015",
        "cited_work": {"text": "段柯古《肉攫部》", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "考源",
    },
    # 01-018 七妙
    {
        "item_id": "01-018",
        "cited_work": {"text": "陶秀实《清异录》", "cited_ent_ids": []},
        "citation_type": "直引",
        "context": "证俗",
    },
    # 01-021 水灾
    {
        "item_id": "01-021",
        "cited_work": {
            "text": "前史（吴太元、东晋、义熙、梁天监水患）",
            "cited_ent_ids": [],
        },
        "citation_type": "泛引",
        "context": "考源",
    },
    # 01-022 米价
    {
        "item_id": "01-022",
        "cited_work": {"text": "《南史》", "cited_ent_ids": []},
        "citation_type": "直引",
        "context": "考源",
    },
    # 01-026 壬午
    {
        "item_id": "01-026",
        "cited_work": {"text": "弇州（王世贞）论正统复出之说", "cited_ent_ids": []},
        "citation_type": "转引",
        "context": "立论",
    },
    {
        "item_id": "01-026",
        "cited_work": {"text": "纪（葬帝以天子礼）", "cited_ent_ids": []},
        "citation_type": "转引",
        "context": "立论",
    },
    # 01-028 五三绝
    {
        "item_id": "01-028",
        "cited_work": {"text": "陆龟蒙《古锦记》", "cited_ent_ids": []},
        "citation_type": "转引",
        "context": "补遗",
    },
    # 01-029 解道
    {
        "item_id": "01-029",
        "cited_work": {"text": "王丹丘先生所记", "cited_ent_ids": []},
        "citation_type": "转引",
        "context": "立论",
    },
    # 01-030 宝船厂
    {
        "item_id": "01-030",
        "cited_work": {"text": "《星槎胜览》", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "考源",
    },
    {
        "item_id": "01-030",
        "cited_work": {"text": "《周官》", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "立论",
    },
    {
        "item_id": "01-030",
        "cited_work": {"text": "《王会》", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "立论",
    },
    # 01-032 国初历式
    {
        "item_id": "01-032",
        "cited_work": {"text": "《授时历》", "cited_ent_ids": []},
        "citation_type": "泛引",
        "context": "考源",
    },
    # 01-034 僻姓
    {
        "item_id": "01-034",
        "cited_work": {"text": "弇州《奇事述》", "cited_ent_ids": []},
        "citation_type": "转引",
        "context": "补遗",
    },
    {
        "item_id": "01-034",
        "cited_work": {"text": "《南畿志》", "cited_ent_ids": []},
        "citation_type": "转引",
        "context": "补遗",
    },
    {
        "item_id": "01-034",
        "cited_work": {"text": "《京学志》", "cited_ent_ids": []},
        "citation_type": "转引",
        "context": "补遗",
    },
]
