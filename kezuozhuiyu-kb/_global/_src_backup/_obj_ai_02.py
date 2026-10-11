# -*- coding: utf-8 -*-
# _obj_ai_02.py  卷二 名物层源数据（AI 判定）
# category 枚举：器物/动物/植物/饮食/珍宝/材料/建筑/服饰/其他
# attributes 为文本可证键值对，无则留空；lore 为 AI 解读（不抄原文）
# name_ent_ids 打包器按文本反查 ENT 回填

RECORDS = [
    # ===== 02-002 佛会道场 =====
    {
        "item_id": "02-002",
        "name": {"text": "金莲华", "name_ent_ids": []},
        "category": "植物",
        "attributes": {
            "出现场合": "哈立麻来朝佛会瑞应",
            "性状": "金色莲华，随佛光庆云涌现",
        },
        "lore": "佛会瑞应之征，与青莲华、冰桃、名荈并列，系梵僧献瑞的祥异记载",
    },
    {
        "item_id": "02-002",
        "name": {"text": "青莲华", "name_ent_ids": []},
        "category": "植物",
        "attributes": {"出现场合": "哈立麻来朝佛会瑞应"},
        "lore": "佛会祥瑞之一",
    },
    {
        "item_id": "02-002",
        "name": {"text": "冰桃", "name_ent_ids": []},
        "category": "饮食",
        "attributes": {"出现场合": "哈立麻来朝佛会瑞应"},
        "lore": "佛会献瑞之物，取其冰洁之意",
    },
    {
        "item_id": "02-002",
        "name": {"text": "名荈", "name_ent_ids": []},
        "category": "饮食",
        "attributes": {"出现场合": "哈立麻来朝佛会瑞应"},
        "lore": "名茶，佛会供献之品",
    },
    # ===== 02-003 铁冠道人 =====
    {
        "item_id": "02-003",
        "name": {"text": "铁冠", "name_ent_ids": []},
        "category": "服饰",
        "attributes": {"材料": "铁", "佩戴者": "张中（铁冠道人）"},
        "lore": "张中常戴铁冠，因以为号，是明初异人形象的标志性服饰",
    },
    {
        "item_id": "02-003",
        "name": {"text": "灵谷寺宝公法函", "name_ent_ids": []},
        "category": "其他",
        "attributes": {"所在": "灵谷寺"},
        "lore": "宝志公（宝公）遗物法函，太祖曾遣人启视",
    },
    # ===== 02-004 施食台 =====
    {
        "item_id": "02-004",
        "name": {"text": "万人坑", "name_ent_ids": []},
        "category": "建筑",
        "attributes": {"所在": "鸡鸣寺施食台旁"},
        "lore": "六代战场掩骨之坑，施食台所施之众即此暴露白骨",
    },
    {
        "item_id": "02-004",
        "name": {"text": "翟车", "name_ent_ids": []},
        "category": "器物",
        "attributes": {"乘者": "孝慈高皇后"},
        "lore": "皇后临观施食会所乘之车",
    },
    # ===== 02-005 海水雪景 =====
    {
        "item_id": "02-005",
        "name": {"text": "海水雪景画壁", "name_ent_ids": []},
        "category": "建筑",
        "attributes": {"所在": "灵谷寺", "画者": "相传吴道子笔法"},
        "lore": "灵谷寺名画壁，胡广、解缙、金幼孜、吴伟、吕柟等先后题咏的胜迹",
    },
    {
        "item_id": "02-005",
        "name": {"text": "折芦渡江图", "name_ent_ids": []},
        "category": "其他",
        "attributes": {"题材": "达摩折芦渡江故事"},
        "lore": "与《鸟巢佛印》并传的宗教题材画",
    },
    {
        "item_id": "02-005",
        "name": {"text": "鸟巢佛印图", "name_ent_ids": []},
        "category": "其他",
        "attributes": {"题材": "禅僧佛印故事"},
        "lore": "禅宗机锋题材画作",
    },
    # ===== 02-006 王谢居址 =====
    {
        "item_id": "02-006",
        "name": {"text": "乌衣巷", "name_ent_ids": []},
        "category": "建筑",
        "attributes": {
            "所在": "今聚宝门内剪子巷一带",
            "得名": "六朝王谢诸族聚居，乌衣子弟所居",
        },
        "lore": "刘禹锡'旧时王谢堂前燕'诗咏之名巷，顾起元考其即今而言之方位",
    },
    {
        "item_id": "02-006",
        "name": {"text": "桃叶渡", "name_ent_ids": []},
        "category": "建筑",
        "attributes": {"所在": "今武定桥一带", "得名": "王献之大令迎妾桃叶处"},
        "lore": "六朝风流遗址，今舟航往来之所",
    },
    # ===== 02-008 稚川贞白相类 =====
    {
        "item_id": "02-008",
        "name": {"text": "地动仪", "name_ent_ids": []},
        "category": "器物",
        "attributes": {"创制者": "张衡（陇西）", "见于": "葛洪所记"},
        "lore": "顾起元引葛洪所记陇西地动之仪以证其博识",
    },
    {
        "item_id": "02-008",
        "name": {"text": "炼丹炉灶", "name_ent_ids": []},
        "category": "器物",
        "attributes": {"人物": "陶弘景、葛洪"},
        "lore": "陶葛二子皆精合丹法式，为道教外丹之学的代表性人物",
    },
    # ===== 02-011 樱桃园 =====
    {
        "item_id": "02-011",
        "name": {"text": "樱桃园", "name_ent_ids": []},
        "category": "植物",
        "attributes": {"所在": "南郭", "事件": "嘉靖乙卯倭寇焚掠于此"},
        "lore": "南郭名园，因倭乱被焚而见载",
    },
    {
        "item_id": "02-011",
        "name": {"text": "火药", "name_ent_ids": []},
        "category": "材料",
        "attributes": {"用途": "御倭之具"},
        "lore": "蒋钦御倭时用火药之属",
    },
    # ===== 02-015 南京水陆诸路 =====
    {
        "item_id": "02-015",
        "name": {"text": "浮桥", "name_ent_ids": []},
        "category": "建筑",
        "attributes": {"用途": "跨江渡河"},
        "lore": "水陆诸路渡江之具",
    },
    # ===== 02-021 快船 =====
    {
        "item_id": "02-021",
        "name": {"text": "快船", "name_ent_ids": []},
        "category": "器物",
        "attributes": {"用途": "驾部差遣", "人工": "江卫济卫军士"},
        "lore": "南京水驿差船，岁费甚巨，倪君建言罢之",
    },
    {
        "item_id": "02-021",
        "name": {"text": "马船", "name_ent_ids": []},
        "category": "器物",
        "attributes": {"用途": "运载马匹军用"},
        "lore": "与快船并列的差船之属，其制后渐废",
    },
    # ===== 02-022 运船二则 =====
    {
        "item_id": "02-022",
        "name": {"text": "运船", "name_ent_ids": []},
        "category": "器物",
        "attributes": {"用途": "漕粮运输", "设备": "蓬桅猫缆"},
        "lore": "漕运之船，篷桅锚缆诸器皆运军自备，破敝则加耗赔补，为运军之苦",
    },
    # ===== 02-023 议籴 =====
    {
        "item_id": "02-023",
        "name": {"text": "仓庾", "name_ent_ids": []},
        "category": "建筑",
        "attributes": {"用途": "储籴之粟"},
        "lore": "顾起元议丰年多籴入仓、平岁出粜以权米价之物",
    },
    # ===== 02-026 坊厢乡 =====
    {
        "item_id": "02-026",
        "name": {"text": "木匠坊", "name_ent_ids": []},
        "category": "建筑",
        "attributes": {"所在": "上元县"},
        "lore": "以匠户职业命名的坊名",
    },
    {
        "item_id": "02-026",
        "name": {"text": "织锦坊", "name_ent_ids": []},
        "category": "建筑",
        "attributes": {"所在": "江宁", "行业": "织锦"},
        "lore": "以织锦行业聚居命名的坊名",
    },
    # ===== 02-029 杂赋 =====
    {
        "item_id": "02-029",
        "name": {"text": "芦课银", "name_ent_ids": []},
        "category": "其他",
        "attributes": {"性质": "芦洲地租", "归属": "南京工部"},
        "lore": "沿江芦洲之课，系明代南京杂赋之一种",
    },
    {
        "item_id": "02-029",
        "name": {"text": "酒醋课程钞", "name_ent_ids": []},
        "category": "其他",
        "attributes": {"性质": "酒醋酿造税", "归属": "南京户部"},
        "lore": "酒醋之课程钞，杂赋之一种",
    },
    # ===== 02-034 民利 =====
    {
        "item_id": "02-034",
        "name": {"text": "典当铺", "name_ent_ids": []},
        "category": "其他",
        "attributes": {"性质": "质贷之业"},
        "lore": "南都富民利薮之一，放贷取息之业",
    },
    {
        "item_id": "02-034",
        "name": {"text": "绸叚铺", "name_ent_ids": []},
        "category": "其他",
        "attributes": {"性质": "绸缎贸易之业"},
        "lore": "南都丝绸贸易之铺，富民所业",
    },
    {
        "item_id": "02-034",
        "name": {"text": "盐店", "name_ent_ids": []},
        "category": "其他",
        "attributes": {"性质": "盐业贸易"},
        "lore": "盐商之业，南都富民利薮",
    },
]
