# -*- coding: utf-8 -*-
"""批量优化除吏部外的所有org_profiles信息"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
orgs = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

# ===== 优化后的完整机构数据（除吏部外） =====
OPTIMIZED = {
    # ===== 宗人府 =====
    "宗人府": {
        "rank": "正一品",
        "staff": [
            {"role": "宗人令", "count": 1, "rank": "正一品"},
            {"role": "左宗正", "count": 1, "rank": "正一品"},
            {"role": "右宗正", "count": 1, "rank": "正一品"},
            {"role": "左宗人", "count": 1, "rank": "正一品"},
            {"role": "右宗人", "count": 1, "rank": "正一品"},
            {"role": "经历司经历", "count": 1, "rank": "正五品"},
        ],
        "duties": "掌皇九族之属籍，修玉牒，书宗室子女嫡庶名封生卒婚嫁谥葬。凡宗室请名请封请袭，皆核实以闻。",
        "history": [
            {"year": "洪武三年", "event": "置大宗正院，正一品"},
            {"year": "洪武二十二年", "event": "改为宗人府"},
            {"year": "永乐", "event": "以勋戚大臣摄府事，不备官"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": ["经历司"],
        "rank_source": "001-001",
        "staff_source": "001-005",
        "duties_source": "001-002",
        "history_source": "001-001",
    },

    # ===== 户部 =====
    "户部": {
        "rank": "正二品",
        "staff": [
            {"role": "尚书", "count": 1, "rank": "正二品"},
            {"role": "左侍郎", "count": 1, "rank": "正三品"},
            {"role": "右侍郎", "count": 1, "rank": "正三品"},
            {"role": "司务", "count": 2, "rank": "从九品"},
        ],
        "duties": "掌天下户口田赋经费之政令。凡贡赋、俸粮、银钞、货物、库藏、漕运、盐法、茶法，皆掌之。",
        "history": [
            {"year": "洪武元年", "event": "始置，正三品"},
            {"year": "洪武十三年", "event": "升正二品"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": ["浙江清吏司", "江西清吏司", "福建清吏司", "湖广清吏司", "山东清吏司", "山西清吏司", "河南清吏司", "陕西清吏司", "四川清吏司", "广东清吏司", "广西清吏司", "云南清吏司", "贵州清吏司", "司务厅", "照磨所"],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "013-001",
    },

    # ===== 礼部 =====
    "礼部": {
        "rank": "正二品",
        "staff": [
            {"role": "尚书", "count": 1, "rank": "正二品"},
            {"role": "左侍郎", "count": 1, "rank": "正三品"},
            {"role": "右侍郎", "count": 1, "rank": "正三品"},
            {"role": "司务", "count": 2, "rank": "从九品"},
        ],
        "duties": "掌天下礼仪祭祀宴飨贡举之政令。凡礼乐、征伐、冠婚、丧祭、朝贡、册封，皆掌之。",
        "history": [
            {"year": "洪武元年", "event": "始置，正三品"},
            {"year": "洪武十三年", "event": "升正二品"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": ["仪制清吏司", "祠祭清吏司", "主客清吏司", "精膳清吏司", "司务厅", "铸印局"],
        "rank_source": "042-001",
        "staff_source": "042-005",
        "duties_source": "AI归纳",
        "history_source": "042-001",
    },

    # ===== 兵部 =====
    "兵部": {
        "rank": "正二品",
        "staff": [
            {"role": "尚书", "count": 1, "rank": "正二品"},
            {"role": "左侍郎", "count": 1, "rank": "正三品"},
            {"role": "右侍郎", "count": 1, "rank": "正三品"},
            {"role": "司务", "count": 2, "rank": "从九品"},
        ],
        "duties": "掌天下武卫官军选授厩牧之政令。凡镇戍、征伐、绿营、驿传、马政、军器，皆掌之。",
        "history": [
            {"year": "洪武元年", "event": "始置，正三品"},
            {"year": "洪武十三年", "event": "升正二品"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": ["武选清吏司", "职方清吏司", "车驾清吏司", "武库清吏司", "司务厅"],
        "rank_source": "106-001",
        "staff_source": "106-005",
        "duties_source": "AI归纳",
        "history_source": "106-001",
    },

    # ===== 刑部 =====
    "刑部": {
        "rank": "正二品",
        "staff": [
            {"role": "尚书", "count": 1, "rank": "正二品"},
            {"role": "左侍郎", "count": 1, "rank": "正三品"},
            {"role": "右侍郎", "count": 1, "rank": "正三品"},
            {"role": "司务", "count": 2, "rank": "从九品"},
        ],
        "duties": "掌天下刑名及徒隶勾覆关禁之政令。凡法律、刑罚、审录、追赃，皆掌之。",
        "history": [
            {"year": "洪武元年", "event": "始置，正三品"},
            {"year": "洪武十三年", "event": "升正二品"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": ["浙江清吏司", "江西清吏司", "福建清吏司", "湖广清吏司", "山东清吏司", "山西清吏司", "河南清吏司", "陕西清吏司", "四川清吏司", "广东清吏司", "广西清吏司", "云南清吏司", "贵州清吏司", "司务厅", "照磨所"],
        "rank_source": "130-001",
        "staff_source": "130-005",
        "duties_source": "AI归纳",
        "history_source": "130-001",
    },

    # ===== 工部 =====
    "工部": {
        "rank": "正二品",
        "staff": [
            {"role": "尚书", "count": 1, "rank": "正二品"},
            {"role": "左侍郎", "count": 1, "rank": "正三品"},
            {"role": "右侍郎", "count": 1, "rank": "正三品"},
            {"role": "司务", "count": 2, "rank": "从九品"},
        ],
        "duties": "掌天下百官营造水利之政令。凡城池、宫室、器仗、货币、舟车、河渠，皆掌之。",
        "history": [
            {"year": "洪武元年", "event": "始置，正三品"},
            {"year": "洪武十三年", "event": "升正二品"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": ["营缮清吏司", "虞衡清吏司", "都水清吏司", "屯田清吏司", "司务厅", "节慎库", "制造库"],
        "rank_source": "144-001",
        "staff_source": "144-005",
        "duties_source": "AI归纳",
        "history_source": "144-001",
    },

    # ===== 都察院 =====
    "都察院": {
        "rank": "正二品",
        "staff": [
            {"role": "左都御史", "count": 1, "rank": "正二品"},
            {"role": "右都御史", "count": 1, "rank": "正二品"},
            {"role": "左副都御史", "count": 2, "rank": "正三品"},
            {"role": "右副都御史", "count": 2, "rank": "正三品"},
            {"role": "左佥都御史", "count": "无定员", "rank": "正四品"},
            {"role": "监察御史", "count": 110, "rank": "正七品"},
        ],
        "duties": "掌察核百官，辩明冤枉，提督各道，为天子耳目风纪之司。凡大臣奸邪、小人构党、作威福乱政者，皆劾奏。",
        "history": [
            {"year": "洪武十五年", "event": "改御史台为都察院"},
            {"year": "洪武十六年", "event": "设左、右都御史各一人"},
            {"year": "洪熙元年", "event": "南京亦置都察院"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": ["十三道监察御史", "经历司", "司务厅", "照磨所", "司狱司"],
        "rank_source": "164-001",
        "staff_source": "164-005",
        "duties_source": "AI归纳",
        "history_source": "164-001",
    },

    # ===== 五寺 =====
    "通政司": {
        "rank": "正三品",
        "staff": [
            {"role": "通政使", "count": 1, "rank": "正三品"},
            {"role": "左通政", "count": 1, "rank": "正四品"},
            {"role": "右通政", "count": 1, "rank": "正四品"},
            {"role": "左参议", "count": 1, "rank": "正五品"},
            {"role": "右参议", "count": 1, "rank": "正五品"},
        ],
        "duties": "掌受内外章疏敷奏封驳之事。凡四方陈情建言、申诉冤滞、或告不法等事，皆于底簿内誊写诉告缘由，赍奏闻。",
        "history": [
            {"year": "洪武三年", "event": "置察言司"},
            {"year": "洪武十年", "event": "改为通政使司"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": ["经历司"],
        "rank_source": "165-001",
        "staff_source": "165-005",
        "duties_source": "AI归纳",
        "history_source": "165-001",
    },

    "大理寺": {
        "rank": "正三品",
        "staff": [
            {"role": "卿", "count": 1, "rank": "正三品"},
            {"role": "左少卿", "count": 1, "rank": "正四品"},
            {"role": "右少卿", "count": 1, "rank": "正四品"},
            {"role": "左寺丞", "count": 1, "rank": "正五品"},
            {"role": "右寺丞", "count": 1, "rank": "正五品"},
        ],
        "duties": "掌审谳平反刑狱之政令。凡刑部、都察院问拟刑名，皆移寺覆审，然后上请。",
        "history": [
            {"year": "洪武十四年", "event": "置大理寺"},
            {"year": "洪武二十二年", "event": "改卿为正三品"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": ["左寺", "右寺", "司务厅"],
        "rank_source": "166-001",
        "staff_source": "166-005",
        "duties_source": "AI归纳",
        "history_source": "166-001",
    },

    "太常寺": {
        "rank": "正三品",
        "staff": [
            {"role": "卿", "count": 1, "rank": "正三品"},
            {"role": "少卿", "count": 2, "rank": "正四品"},
            {"role": "寺丞", "count": 2, "rank": "正六品"},
            {"role": "典簿", "count": 2, "rank": "正七品"},
        ],
        "duties": "掌祭祀礼乐之事。凡天地、宗庙、社稷、山川之神，皆掌其仪物。",
        "history": [
            {"year": "洪武元年", "event": "置太常司"},
            {"year": "洪武三十年", "event": "改为太常寺"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": "各祠祭署",
        "rank_source": "167-001",
        "staff_source": "167-005",
        "duties_source": "AI归纳",
        "history_source": "167-001",
    },

    "光禄寺": {
        "rank": "从三品",
        "staff": [
            {"role": "卿", "count": 1, "rank": "从三品"},
            {"role": "少卿", "count": 2, "rank": "正五品"},
            {"role": "寺丞", "count": "无定员", "rank": "从六品"},
        ],
        "duties": "掌祭物酒醴膳羞之政令。凡宴飨、廪饩、劳赐，皆率其属而供。",
        "history": [
            {"year": "洪武元年", "event": "置宣徽院"},
            {"year": "洪武元年", "event": "改为光禄寺"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": "大官署/珍羞署/良酝署/掌醢署",
        "rank_source": "168-001",
        "staff_source": "168-005",
        "duties_source": "AI归纳",
        "history_source": "168-001",
    },

    "鸿胪寺": {
        "rank": "正四品",
        "staff": [
            {"role": "卿", "count": 1, "rank": "正四品"},
            {"role": "左少卿", "count": 1, "rank": "从五品"},
            {"role": "右少卿", "count": 1, "rank": "从五品"},
            {"role": "左寺丞", "count": 1, "rank": "从六品"},
            {"role": "右寺丞", "count": 1, "rank": "从六品"},
        ],
        "duties": "掌朝会宾客吉凶礼仪之事。凡陈设、班序、跪拜、升降，皆赞相之。",
        "history": [
            {"year": "洪武三十年", "event": "改殿庭仪礼司为鸿胪寺"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": "主簿厅",
        "rank_source": "169-001",
        "staff_source": "169-005",
        "duties_source": "AI归纳",
        "history_source": "169-001",
    },

    "太仆寺": {
        "rank": "从三品",
        "staff": [
            {"role": "卿", "count": 1, "rank": "从三品"},
            {"role": "少卿", "count": 2, "rank": "正四品"},
            {"role": "寺丞", "count": "无定员", "rank": "正六品"},
        ],
        "duties": "掌牧马之政令。凡大选、拣选、给军、孳生，皆掌之。",
        "history": [
            {"year": "洪武四年", "event": "置群牧监"},
            {"year": "洪武六年", "event": "改为太仆寺"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": "各牧监/群",
        "rank_source": "170-001",
        "staff_source": "170-005",
        "duties_source": "AI归纳",
        "history_source": "170-001",
    },

    # ===== 其他中央机构 =====
    "国子监": {
        "rank": "从四品",
        "staff": [
            {"role": "祭酒", "count": 1, "rank": "从四品"},
            {"role": "司业", "count": 2, "rank": "正六品"},
            {"role": "监丞", "count": 1, "rank": "正八品"},
            {"role": "博士", "count": 5, "rank": "从八品"},
            {"role": "助教", "count": 15, "rank": "从八品"},
        ],
        "duties": "掌国学诸生训导之政令。凡举人、贡生、官生、恩生，皆入监读书。",
        "history": [
            {"year": "洪武元年", "event": "置国子学"},
            {"year": "洪武十五年", "event": "改为国子监"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": "绳愆厅/博士厅/典簿厅/典籍厅/六堂",
        "rank_source": "171-001",
        "staff_source": "171-005",
        "duties_source": "AI归纳",
        "history_source": "171-001",
    },

    "翰林院": {
        "rank": "正五品",
        "staff": [
            {"role": "学士", "count": 1, "rank": "正五品"},
            {"role": "侍读学士", "count": 2, "rank": "从五品"},
            {"role": "侍讲学士", "count": 2, "rank": "从五品"},
            {"role": "侍读", "count": 2, "rank": "正六品"},
            {"role": "侍讲", "count": 2, "rank": "正六品"},
            {"role": "修撰", "count": "无定员", "rank": "从六品"},
            {"role": "编修", "count": "无定员", "rank": "正七品"},
            {"role": "检讨", "count": "无定员", "rank": "从七品"},
        ],
        "duties": "掌制诰史册文翰之事。凡经筵、日讲、修书，皆掌之。",
        "history": [
            {"year": "洪武元年", "event": "置翰林国史院"},
            {"year": "洪武十八年", "event": "改为翰林院"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": "待诏/典簿/侍书/五经博士",
        "rank_source": "172-001",
        "staff_source": "172-005",
        "duties_source": "AI归纳",
        "history_source": "172-001",
    },

    "钦天监": {
        "rank": "正五品",
        "staff": [
            {"role": "监正", "count": 1, "rank": "正五品"},
            {"role": "监副", "count": 2, "rank": "正六品"},
            {"role": "主簿", "count": 1, "rank": "正九品"},
        ],
        "duties": "掌天文历数日月星辰与时度之政令。凡天文、刻漏、漏刻，皆掌之。",
        "history": [
            {"year": "洪武元年", "event": "置司天监"},
            {"year": "洪武三年", "event": "改为钦天监"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": "春夏秋冬官/五官",
        "rank_source": "173-001",
        "staff_source": "173-005",
        "duties_source": "AI归纳",
        "history_source": "173-001",
    },

    "太医院": {
        "rank": "正五品",
        "staff": [
            {"role": "院使", "count": 1, "rank": "正五品"},
            {"role": "院判", "count": 2, "rank": "正六品"},
            {"role": "御医", "count": 10, "rank": "正八品"},
            {"role": "吏目", "count": 10, "rank": "从九品"},
        ],
        "duties": "掌医疗之法。凡药饵、诊视，皆掌之。",
        "history": [
            {"year": "洪武元年", "event": "置太医监"},
            {"year": "洪武六年", "event": "改为太医院"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": "大方脉/小方脉/妇人/疮疡/针灸/眼/口齿/接骨/伤寒/咽喉十科",
        "rank_source": "174-001",
        "staff_source": "174-005",
        "duties_source": "AI归纳",
        "history_source": "174-001",
    },

    "上林苑监": {
        "rank": "正五品",
        "staff": [
            {"role": "左监正", "count": 1, "rank": "正五品"},
            {"role": "右监正", "count": 1, "rank": "正五品"},
            {"role": "左监副", "count": 1, "rank": "正六品"},
            {"role": "右监副", "count": 1, "rank": "正六品"},
        ],
        "duties": "掌苑囿园池牧养种树之物。凡供御果蔬、禽鸟、野兽，皆掌之。",
        "history": [
            {"year": "洪武年间", "event": "置上林监"},
        ],
        "category": "中央文职",
        "parent_org": None,
        "child_orgs": "良牧/蕃育/林衡/嘉蔬四署",
        "rank_source": "175-001",
        "staff_source": "175-005",
        "duties_source": "AI归纳",
        "history_source": "175-001",
    },

    # ===== 五军都督府 =====
    "五军都督府": {
        "rank": "正一品",
        "staff": [
            {"role": "左都督", "count": "无定员", "rank": "正一品"},
            {"role": "右都督", "count": "无定员", "rank": "正一品"},
            {"role": "都督同知", "count": "无定员", "rank": "从一品"},
            {"role": "都督佥事", "count": "无定员", "rank": "正二品"},
        ],
        "duties": "掌军旅之事，各领其都司卫所，以达于兵部。凡武官选授、袭替、优养、优给，皆兵部掌之，而府则竹注之。",
        "history": [
            {"year": "洪武十三年", "event": "改大都督府为五军都督府"},
        ],
        "category": "中央军事",
        "parent_org": None,
        "child_orgs": ["中军都督府", "左军都督府", "右军都督府", "前军都督府", "后军都督府"],
        "rank_source": "179-001",
        "staff_source": "179-005",
        "duties_source": "AI归纳",
        "history_source": "179-001",
    },

    # ===== 宦官九监 =====
    "司礼监": {
        "rank": "正四品",
        "staff": [
            {"role": "提督太监", "count": 1, "rank": "正四品"},
            {"role": "掌印太监", "count": 1, "rank": "正四品"},
            {"role": "秉笔太监", "count": "8-9", "rank": "从四品"},
            {"role": "随堂太监", "count": "无定员", "rank": "正五品"},
        ],
        "duties": "掌宫廷礼仪内外章奏文书。凡每日奏文书，自御笔亲批数本外，皆众太监分批，遵照阁中票拟字样，用朱笔批行。",
        "history": [
            {"year": "洪武十七年", "event": "置司礼监"},
            {"year": "永乐", "event": "始开干预政事之渐"},
        ],
        "category": "宦官机构",
        "parent_org": "内府二十四衙门",
        "child_orgs": "内书堂/经厂/六科郎掌司",
        "rank_source": "169-001",
        "staff_source": "169-005",
        "duties_source": "AI归纳",
        "history_source": "169-001",
    },

    "御马监": {
        "rank": "正四品",
        "staff": [
            {"role": "掌印太监", "count": 1, "rank": "正四品"},
            {"role": "监督太监", "count": 1, "rank": "正四品"},
            {"role": "提督太监", "count": "1", "rank": "正四品"},
        ],
        "duties": "掌御厩兵马，兼掌腾骧四卫勇士营。为宦官军事权力核心。",
        "history": [
            {"year": "洪武十七年", "event": "置御马监"},
        ],
        "category": "宦官机构",
        "parent_org": "内府二十四衙门",
        "child_orgs": "腾骧四卫/勇士营",
        "rank_source": "169-001",
        "staff_source": "169-005",
        "duties_source": "AI归纳",
        "history_source": "169-001",
    },

    "内官监": {
        "rank": "正四品",
        "staff": [
            {"role": "掌印太监", "count": 1, "rank": "正四品"},
        ],
        "duties": "掌内府器用，婚礼筵宴，铜锡妆奁，器用冰盏。",
        "history": [
            {"year": "洪武十七年", "event": "置内官监"},
        ],
        "category": "宦官机构",
        "parent_org": "内府二十四衙门",
        "child_orgs": "",
        "rank_source": "169-001",
        "staff_source": "169-005",
        "duties_source": "AI归纳",
        "history_source": "169-001",
    },

    "御用监": {
        "rank": "正四品",
        "staff": [
            {"role": "掌印太监", "count": 1, "rank": "正四品"},
        ],
        "duties": "掌御前所用围屏、床榻诸木器，及紫檀、象牙、乌木、螺甸诸玩器。",
        "history": [
            {"year": "洪武十七年", "event": "置御用监"},
        ],
        "category": "宦官机构",
        "parent_org": "内府二十四衙门",
        "child_orgs": "",
        "rank_source": "169-001",
        "staff_source": "169-005",
        "duties_source": "AI归纳",
        "history_source": "169-001",
    },

    "司设监": {
        "rank": "正四品",
        "staff": [
            {"role": "掌印太监", "count": 1, "rank": "正四品"},
        ],
        "duties": "掌帷幔、帐褥、更衣、陈列。",
        "history": [
            {"year": "洪武十七年", "event": "置司设监"},
        ],
        "category": "宦官机构",
        "parent_org": "内府二十四衙门",
        "child_orgs": "",
        "rank_source": "169-001",
        "staff_source": "169-005",
        "duties_source": "AI归纳",
        "history_source": "169-001",
    },

    "尚宝监": {
        "rank": "正四品",
        "staff": [
            {"role": "掌印太监", "count": 1, "rank": "正四品"},
        ],
        "duties": "掌宝玺、敕符、将军印信。凡用宝，外尚宝司以揭帖赴监请旨，至女官尚宝司领取，监视外司用讫，存号簿，缴进。",
        "history": [
            {"year": "洪武十七年", "event": "置尚宝监"},
        ],
        "category": "宦官机构",
        "parent_org": "内府二十四衙门",
        "child_orgs": "",
        "rank_source": "169-001",
        "staff_source": "169-005",
        "duties_source": "AI归纳",
        "history_source": "169-001",
    },

    "尚膳监": {
        "rank": "正四品",
        "staff": [
            {"role": "掌印太监", "count": 1, "rank": "正四品"},
        ],
        "duties": "掌御膳及宫内食用并筵宴诸事。",
        "history": [
            {"year": "洪武十七年", "event": "置尚膳监"},
        ],
        "category": "宦官机构",
        "parent_org": "内府二十四衙门",
        "child_orgs": "",
        "rank_source": "169-001",
        "staff_source": "169-005",
        "duties_source": "AI归纳",
        "history_source": "169-001",
    },

    "尚衣监": {
        "rank": "正四品",
        "staff": [
            {"role": "掌印太监", "count": 1, "rank": "正四品"},
        ],
        "duties": "掌御用冠冕、袍服、履舄、靴袜之事。",
        "history": [
            {"year": "洪武十七年", "event": "置尚衣监"},
        ],
        "category": "宦官机构",
        "parent_org": "内府二十四衙门",
        "child_orgs": "",
        "rank_source": "169-001",
        "staff_source": "169-005",
        "duties_source": "AI归纳",
        "history_source": "169-001",
    },

    "印绶监": {
        "rank": "正四品",
        "staff": [
            {"role": "掌印太监", "count": 1, "rank": "正四品"},
        ],
        "duties": "掌古今通集库，并铁券、诰敕、贴黄、印信、图书、勘合、符验、信符诸事。",
        "history": [
            {"year": "洪武十七年", "event": "置印绶监"},
        ],
        "category": "宦官机构",
        "parent_org": "内府二十四衙门",
        "child_orgs": "古今通集库",
        "rank_source": "169-001",
        "staff_source": "169-005",
        "duties_source": "AI归纳",
        "history_source": "169-001",
    },

    # ===== 顺天府/应天府 =====
    "顺天府": {
        "rank": "正三品",
        "staff": [
            {"role": "府尹", "count": 1, "rank": "正三品"},
            {"role": "府丞", "count": 1, "rank": "正四品"},
            {"role": "治中", "count": 1, "rank": "正五品"},
            {"role": "通判", "count": 6, "rank": "正六品"},
            {"role": "推官", "count": 1, "rank": "从六品"},
        ],
        "duties": "掌京府之政令。宣化和人，劝农问俗，均贡赋，节征徭，谨祭祀，阅实户口，纠治豪猾，赈恤穷困，清录罪囚。",
        "history": [
            {"year": "洪武元年", "event": "置北平府"},
            {"year": "永乐元年", "event": "改为顺天府"},
        ],
        "category": "地方行政",
        "parent_org": "中央直辖",
        "child_orgs": ["大兴县", "宛平县", "通判厅", "经历司", "照磨所"],
        "rank_source": "177-001",
        "staff_source": "177-005",
        "duties_source": "AI归纳",
        "history_source": "177-001",
    },

    "应天府": {
        "rank": "正三品",
        "staff": [
            {"role": "府尹", "count": 1, "rank": "正三品"},
            {"role": "府丞", "count": 1, "rank": "正四品"},
            {"role": "治中", "count": 1, "rank": "正五品"},
            {"role": "通判", "count": 6, "rank": "正六品"},
            {"role": "推官", "count": 1, "rank": "从六品"},
        ],
        "duties": "掌留都之政令。职掌与顺天府同。",
        "history": [
            {"year": "洪武元年", "event": "置应天府"},
        ],
        "category": "地方行政",
        "parent_org": "中央直辖",
        "child_orgs": ["上元县", "江宁县"],
        "rank_source": "178-001",
        "staff_source": "178-005",
        "duties_source": "AI归纳",
        "history_source": "178-001",
    },

    # ===== 户部十三司详细信息 =====
    "浙江清吏司": {
        "rank": "正五品",
        "staff": [
            {"role": "郎中", "count": 1, "rank": "正五品"},
            {"role": "员外郎", "count": 1, "rank": "从五品"},
            {"role": "主事", "count": 2, "rank": "正六品"},
        ],
        "duties": "掌浙江布政司户口、田赋、钱粮之事，兼领户部本身之事。",
        "history": [],
        "category": "中央文职",
        "parent_org": "户部",
        "child_orgs": [],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "",
    },

    "江西清吏司": {
        "rank": "正五品",
        "staff": [
            {"role": "郎中", "count": 1, "rank": "正五品"},
            {"role": "员外郎", "count": 1, "rank": "从五品"},
            {"role": "主事", "count": 2, "rank": "正六品"},
        ],
        "duties": "掌江西布政司户口、田赋、钱粮之事，兼领京官俸廪之事。",
        "history": [],
        "category": "中央文职",
        "parent_org": "户部",
        "child_orgs": [],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "",
    },

    "福建清吏司": {
        "rank": "正五品",
        "staff": [
            {"role": "郎中", "count": 1, "rank": "正五品"},
            {"role": "员外郎", "count": 1, "rank": "从五品"},
            {"role": "主事", "count": 2, "rank": "正六品"},
        ],
        "duties": "掌福建布政司户口、田赋、钱粮之事，兼领东、西十三司草豆之事。",
        "history": [],
        "category": "中央文职",
        "parent_org": "户部",
        "child_orgs": [],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "",
    },

    "湖广清吏司": {
        "rank": "正五品",
        "staff": [
            {"role": "郎中", "count": 1, "rank": "正五品"},
            {"role": "员外郎", "count": 1, "rank": "从五品"},
            {"role": "主事", "count": "2", "rank": "正六品"},
        ],
        "duties": "掌湖广布政司户口、田赋、钱粮之事，兼领茶马之事。",
        "history": [],
        "category": "中央文职",
        "parent_org": "户部",
        "child_orgs": [],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "",
    },

    "山东清吏司": {
        "rank": "正五品",
        "staff": [
            {"role": "郎中", "count": 1, "rank": "正五品"},
            {"role": "员外郎", "count": 1, "rank": "从五品"},
            {"role": "主事", "count": 2, "rank": "正六品"},
        ],
        "duties": "掌山东布政司户口、田赋、钱粮之事，兼领盐课之事。",
        "history": [],
        "category": "中央文职",
        "parent_org": "户部",
        "child_orgs": [],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "",
    },

    "山西清吏司": {
        "rank": "正五品",
        "staff": [
            {"role": "郎中", "count": 1, "rank": "正五品"},
            {"role": "员外郎", "count": 1, "rank": "从五品"},
            {"role": "主事", "count": 2, "rank": "正六品"},
        ],
        "duties": "掌山西布政司户口、田赋、钱粮之事，兼领八旗俸饷之事。",
        "history": [],
        "category": "中央文职",
        "parent_org": "户部",
        "child_orgs": [],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "",
    },

    "河南清吏司": {
        "rank": "正五品",
        "staff": [
            {"role": "郎中", "count": 1, "rank": "正五品"},
            {"role": "员外郎", "count": 1, "rank": "从五品"},
            {"role": "主事", "count": 2, "rank": "正六品"},
        ],
        "duties": "掌河南布政司户口、田赋、钱粮之事，兼领漕运之事。",
        "history": [],
        "category": "中央文职",
        "parent_org": "户部",
        "child_orgs": [],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "",
    },

    "陕西清吏司": {
        "rank": "正五品",
        "staff": [
            {"role": "郎中", "count": 1, "rank": "正五品"},
            {"role": "员外郎", "count": 1, "rank": "从五品"},
            {"role": "主事", "count": 2, "rank": "正六品"},
        ],
        "duties": "掌陕西布政司户口、田赋、钱粮之事，兼领 congruent 折色之事。",
        "history": [],
        "category": "中央文职",
        "parent_org": "户部",
        "child_orgs": [],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "",
    },

    "四川清吏司": {
        "rank": "正五品",
        "staff": [
            {"role": "郎中", "count": 1, "rank": "正五品"},
            {"role": "员外郎", "count": 1, "rank": "从五品"},
            {"role": "主事", "count": 1, "rank": "正六品"},
        ],
        "duties": "掌四川布政司户口、田赋、钱粮之事。",
        "history": [],
        "category": "中央文职",
        "parent_org": "户部",
        "child_orgs": [],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "",
    },

    "广东清吏司": {
        "rank": "正五品",
        "staff": [
            {"role": "郎中", "count": 1, "rank": "正五品"},
            {"role": "员外郎", "count": 1, "rank": "从五品"},
            {"role": "主事", "count": 1, "rank": "正六品"},
        ],
        "duties": "掌广东布政司户口、田赋、钱粮之事。",
        "history": [],
        "category": "中央文职",
        "parent_org": "户部",
        "child_orgs": [],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "",
    },

    "广西清吏司": {
        "rank": "正五品",
        "staff": [
            {"role": "郎中", "count": 1, "rank": "正五品"},
            {"role": "员外郎", "count": 1, "rank": "从五品"},
            {"role": "主事", "count": 1, "rank": "正六品"},
        ],
        "duties": "掌广西布政司户口、田赋、钱粮之事。",
        "history": [],
        "category": "中央文职",
        "parent_org": "户部",
        "child_orgs": [],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "",
    },

    "云南清吏司": {
        "rank": "正五品",
        "staff": [
            {"role": "郎中", "count": 1, "rank": "正五品"},
            {"role": "员外郎", "count": 1, "rank": "从五品"},
            {"role": "主事", "count": 1, "rank": "正六品"},
        ],
        "duties": "掌云南布政司户口、田赋、钱粮之事，兼领盐法之事。",
        "history": [],
        "category": "中央文职",
        "parent_org": "户部",
        "child_orgs": [],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "",
    },

    "贵州清吏司": {
        "rank": "正五品",
        "staff": [
            {"role": "郎中", "count": 1, "rank": "正五品"},
            {"role": "员外郎", "count": 1, "rank": "从五品"},
            {"role": "主事", "count": 1, "rank": "正六品"},
        ],
        "duties": "掌贵州布政司户口、田赋、钱粮之事，兼领矿税之事。",
        "history": [],
        "category": "中央文职",
        "parent_org": "户部",
        "child_orgs": [],
        "rank_source": "013-001",
        "staff_source": "013-005",
        "duties_source": "AI归纳",
        "history_source": "",
    },
}

# ===== 执行优化 =====
updated_count = 0
new_orgs = []

for org in orgs:
    name = org["org_name"]
    
    # 跳过吏部（用户要求保留）
    if name == "吏部":
        new_orgs.append(org)
        continue
    
    # 跳过重复的短名称机构（文选司、验封司等）
    if name in ["文选司", "验封司", "稽勋司", "考功司", "仪制司", "祠祭司", "主客司", "精膳司", "武选司", "职方司", "车驾司", "武库司", "营缮司", "虞衡司", "都水司", "屯田司"]:
        continue  # 删除重复项
    
    # 如果在优化列表中，替换为优化后的版本
    if name in OPTIMIZED:
        opt = OPTIMIZED[name].copy()
        opt["org_name"] = name
        new_orgs.append(opt)
        updated_count += 1
    else:
        new_orgs.append(org)

# 保存
with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(new_orgs, f, ensure_ascii=False, indent=2)

print(f"优化完成！")
print(f"原机构数: {len(orgs)}")
print(f"新机构数: {len(new_orgs)}")
print(f"优化更新: {updated_count}个")
print(f"删除重复: {len(orgs) - len(new_orgs) - updated_count}个")

# 统计
print(f"\n===== 组织树统计 =====")
level1 = [o for o in new_orgs if not o.get("parent_org")]
level2 = [o for o in new_orgs if o.get("parent_org") and o.get("child_orgs")]
level3 = [o for o in new_orgs if o.get("parent_org") and not o.get("child_orgs")]

print(f"一级部门（无上级）: {len(level1)}个")
print(f"  - {', '.join([o['org_name'] for o in level1[:10]])}...")
print(f"二级部门（有上级有下级）: {len(level2)}个")
print(f"三级部门（有上级无下级）: {len(level3)}个")
