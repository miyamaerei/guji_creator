# -*- coding: utf-8 -*-
"""建官职主档层（office_profiles）"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ===== 俸禄表 =====
SALARY_TABLE = {
    "正一品": {"monthly_shi": 87, "yearly_shi": 1044},
    "从一品": {"monthly_shi": 74, "yearly_shi": 888},
    "正二品": {"monthly_shi": 61, "yearly_shi": 732},
    "从二品": {"monthly_shi": 48, "yearly_shi": 576},
    "正三品": {"monthly_shi": 35, "yearly_shi": 420},
    "从三品": {"monthly_shi": 26, "yearly_shi": 312},
    "正四品": {"monthly_shi": 24, "yearly_shi": 288},
    "从四品": {"monthly_shi": 21, "yearly_shi": 252},
    "正五品": {"monthly_shi": 16, "yearly_shi": 192},
    "从五品": {"monthly_shi": 14, "yearly_shi": 168},
    "正六品": {"monthly_shi": 10, "yearly_shi": 120},
    "从六品": {"monthly_shi": 8, "yearly_shi": 96},
    "正七品": {"monthly_shi": 7.5, "yearly_shi": 90},
    "从七品": {"monthly_shi": 7, "yearly_shi": 84},
    "正八品": {"monthly_shi": 6.5, "yearly_shi": 78},
    "从八品": {"monthly_shi": 6, "yearly_shi": 72},
    "正九品": {"monthly_shi": 5.5, "yearly_shi": 66},
    "从九品": {"monthly_shi": 5, "yearly_shi": 60},
}

# ===== 61个官职的完整信息 =====
OFFICE_PROFILES = [
    # ===== 中枢重臣 =====
    {"office_name": "尚书", "rank": "正二品", "type": "实职", "system": "文职",
     "headcount": 6, "duties": "掌一部之政令，为一部之长",
     "parent_office": "皇帝", "child_offices": ["侍郎", "郎中"],
     "location": "中央", "history": [{"year": "洪武元年", "event": "始置六部尚书，正三品"}, {"year": "洪武十三年", "event": "升正二品"}],
     "note": "六部尚书：吏/户/礼/兵/刑/工各1人"},
    
    {"office_name": "侍郎", "rank": "正三品", "type": "实职", "system": "文职",
     "headcount": 12, "duties": "贰尚书，掌一部之贰",
     "parent_office": "尚书", "child_offices": ["郎中"],
     "location": "中央", "history": [{"year": "洪武元年", "event": "始置六部侍郎，正四品"}, {"year": "洪武十三年", "event": "升正三品"}],
     "note": "六部左右侍郎各1人，共12人"},
    
    {"office_name": "左侍郎", "rank": "正三品", "type": "实职", "system": "文职",
     "headcount": 6, "duties": "佐尚书掌部事，位在右侍郎上",
     "parent_office": "尚书", "child_offices": [],
     "location": "中央", "history": [], "note": "六部左侍郎各1人"},
    
    {"office_name": "右侍郎", "rank": "正三品", "type": "实职", "system": "文职",
     "headcount": 6, "duties": "佐尚书掌部事，位在左侍郎下",
     "parent_office": "尚书", "child_offices": [],
     "location": "中央", "history": [], "note": "六部右侍郎各1人"},
    
    # ===== 都察院系统 =====
    {"office_name": "都御史", "rank": "正二品", "type": "实职", "system": "文职",
     "headcount": 2, "duties": "掌都察院事，为天子耳目风纪之司",
     "parent_office": "皇帝", "child_offices": ["副都御史", "佥都御史", "监察御史"],
     "location": "中央", "history": [{"year": "洪武十五年", "event": "改御史台为都察院"}],
     "note": "左都御史、右都御史各1人"},
    
    {"office_name": "右都御史", "rank": "正二品", "type": "实职", "system": "文职",
     "headcount": 1, "duties": "掌都察院事",
     "parent_office": "皇帝", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "副都御史", "rank": "正三品", "type": "实职", "system": "文职",
     "headcount": 4, "duties": "贰都御史，掌院事之贰",
     "parent_office": "都御史", "child_offices": ["佥都御史"],
     "location": "中央", "history": [], "note": "左右副都御史各2人"},
    
    {"office_name": "右副都御史", "rank": "正三品", "type": "实职", "system": "文职",
     "headcount": 2, "duties": "贰右都御史",
     "parent_office": "右都御史", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "佥都御史", "rank": "正四品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "掌分道监察",
     "parent_office": "副都御史", "child_offices": ["监察御史"],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "右佥都御史", "rank": "正四品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "掌分道监察",
     "parent_office": "右副都御史", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "御史", "rank": "正七品", "type": "实职", "system": "文职",
     "headcount": 110, "duties": "掌察核百官，辩明冤枉，提督各道",
     "parent_office": "都御史", "child_offices": [],
     "location": "中央/地方", "history": [{"year": "洪武十五年", "event": "置十三道监察御史"}],
     "note": "十三道监察御史，共110人"},
    
    {"office_name": "监察御史", "rank": "正七品", "type": "实职", "system": "文职",
     "headcount": 110, "duties": "掌巡按地方，监察百官，纠劾不法",
     "parent_office": "都御史", "child_offices": [],
     "location": "中央/地方", "history": [{"year": "洪武十五年", "event": "分十三道各设监察御史"}],
     "note": "十三道：浙江/江西/福建/四川/陕西/湖广/广东/广西/河南/山西/山东/南京/贵州"},
    
    # ===== 六科给事中 =====
    {"office_name": "六科给事中", "rank": "从七品", "type": "实职", "system": "文职",
     "headcount": 58, "duties": "掌侍从规谏，补阙拾遗，稽察六部弊误",
     "parent_office": "皇帝", "child_offices": [],
     "location": "中央", "history": [{"year": "洪武六年", "event": "设给事中"}, {"year": "洪武二十四年", "event": "分六科"}],
     "note": "吏/户/礼/兵/刑/工六科，每科都给事中1人，左右给事中各1人，给事中若干"},
    
    # ===== 翰林院系统 =====
    {"office_name": "学士", "rank": "正五品", "type": "实职", "system": "文职",
     "headcount": 1, "duties": "掌制诰史册文翰之事",
     "parent_office": "皇帝", "child_offices": ["侍读学士", "侍讲学士", "修撰", "编修", "检讨"],
     "location": "中央", "history": [{"year": "洪武十八年", "event": "改翰林院"}],
     "note": "翰林院学士"},
    
    {"office_name": "侍读学士", "rank": "从五品", "type": "实职", "system": "文职",
     "headcount": 2, "duties": "掌侍读经史",
     "parent_office": "学士", "child_offices": ["侍读"],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "侍讲学士", "rank": "从五品", "type": "实职", "system": "文职",
     "headcount": 2, "duties": "掌侍讲经史",
     "parent_office": "学士", "child_offices": ["侍讲"],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "侍读", "rank": "正六品", "type": "实职", "system": "文职",
     "headcount": 2, "duties": "掌侍读经史",
     "parent_office": "侍读学士", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "侍讲", "rank": "正六品", "type": "实职", "system": "文职",
     "headcount": 2, "duties": "掌侍讲经史",
     "parent_office": "侍讲学士", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "修撰", "rank": "从六品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "掌修国史，会试监考",
     "parent_office": "学士", "child_offices": [],
     "location": "中央", "history": [], "note": "一甲第一名状元授修撰"},
    
    {"office_name": "编修", "rank": "正七品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "掌修国史，会试试卷",
     "parent_office": "学士", "child_offices": [],
     "location": "中央", "history": [], "note": "一甲第二名榜眼、第三名探花授编修"},
    
    {"office_name": "检讨", "rank": "从七品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "掌修国史",
     "parent_office": "学士", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    # ===== 殿阁大学士（内阁） =====
    {"office_name": "华盖殿大学士", "rank": "正五品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "掌献替可否，奉陈规诲，点检题奏，票拟批答",
     "parent_office": "皇帝", "child_offices": [],
     "location": "中央", "history": [{"year": "洪武十五年", "event": "设殿阁大学士"}, {"year": "永乐", "event": "内阁渐成"}],
     "note": "明中期后大学士成为实际宰相"},
    
    {"office_name": "谨身殿大学士", "rank": "正五品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "票拟批答，掌内阁事",
     "parent_office": "皇帝", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "武英殿大学士", "rank": "正五品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "票拟批答，掌内阁事",
     "parent_office": "皇帝", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "文华殿大学士", "rank": "正五品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "票拟批答，掌内阁事",
     "parent_office": "皇帝", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "文渊阁大学士", "rank": "正五品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "票拟批答，掌内阁事",
     "parent_office": "皇帝", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "东阁大学士", "rank": "正五品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "票拟批答，掌内阁事",
     "parent_office": "皇帝", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    # ===== 五寺系统 =====
    {"office_name": "大理寺卿", "rank": "正三品", "type": "实职", "system": "文职",
     "headcount": 1, "duties": "掌审谳平反刑狱之政令",
     "parent_office": "皇帝", "child_offices": ["大理寺少卿", "寺丞"],
     "location": "中央", "history": [{"year": "洪武十四年", "event": "置大理寺"}],
     "note": "三法司：刑部、都察院、大理寺"},
    
    {"office_name": "大理寺少卿", "rank": "正四品", "type": "实职", "system": "文职",
     "headcount": 2, "duties": "贰卿，掌寺事之贰",
     "parent_office": "大理寺卿", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "太常寺卿", "rank": "正三品", "type": "实职", "system": "文职",
     "headcount": 1, "duties": "掌祭祀礼乐之事",
     "parent_office": "皇帝", "child_offices": ["少卿", "寺丞"],
     "location": "中央", "history": [{"year": "洪武三十年", "event": "改太常司为太常寺"}],
     "note": ""},
    
    {"office_name": "光禄寺卿", "rank": "从三品", "type": "实职", "system": "文职",
     "headcount": 1, "duties": "掌祭物酒醴膳羞之政令",
     "parent_office": "皇帝", "child_offices": ["光禄寺少卿", "寺丞"],
     "location": "中央", "history": [{"year": "洪武元年", "event": "改宣徽院为光禄寺"}],
     "note": ""},
    
    {"office_name": "光禄寺少卿", "rank": "正五品", "type": "实职", "system": "文职",
     "headcount": 2, "duties": "贰卿，掌寺事之贰",
     "parent_office": "光禄寺卿", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "鸿胪寺卿", "rank": "正四品", "type": "实职", "system": "文职",
     "headcount": 1, "duties": "掌朝会宾客吉凶礼仪之事",
     "parent_office": "皇帝", "child_offices": ["鸿胪寺少卿", "寺丞"],
     "location": "中央", "history": [{"year": "洪武三十年", "event": "改殿庭仪礼司为鸿胪寺"}],
     "note": ""},
    
    {"office_name": "鸿胪寺少卿", "rank": "从五品", "type": "实职", "system": "文职",
     "headcount": 2, "duties": "贰卿，掌寺事之贰",
     "parent_office": "鸿胪寺卿", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "太仆寺卿", "rank": "从三品", "type": "实职", "system": "文职",
     "headcount": 1, "duties": "掌牧马之政令",
     "parent_office": "皇帝", "child_offices": ["太仆寺少卿", "寺丞"],
     "location": "中央", "history": [{"year": "洪武六年", "event": "改群牧监为太仆寺"}],
     "note": ""},
    
    {"office_name": "太仆寺少卿", "rank": "正四品", "type": "实职", "system": "文职",
     "headcount": 2, "duties": "贰卿，掌寺事之贰",
     "parent_office": "太仆寺卿", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "寺丞", "rank": "正六品", "type": "实职", "system": "文职",
     "headcount": "各寺不同", "duties": "掌寺署之事",
     "parent_office": "寺卿", "child_offices": [],
     "location": "中央", "history": [], "note": "太常/光禄/鸿胪/太仆各寺皆有寺丞"},
    
    # ===== 通政司 =====
    {"office_name": "通政使", "rank": "正三品", "type": "实职", "system": "文职",
     "headcount": 1, "duties": "掌受内外章疏敷奏封驳之事",
     "parent_office": "皇帝", "child_offices": ["左右通政", "左右参议"],
     "location": "中央", "history": [{"year": "洪武十年", "event": "改察言司为通政使司"}],
     "note": ""},
    
    # ===== 国子监 =====
    {"office_name": "祭酒", "rank": "从四品", "type": "实职", "system": "文职",
     "headcount": 1, "duties": "掌国学诸生训导之政令",
     "parent_office": "礼部", "child_offices": ["司业"],
     "location": "中央", "history": [{"year": "洪武十五年", "event": "改国子学为国子监"}],
     "note": ""},
    
    {"office_name": "司业", "rank": "正六品", "type": "实职", "system": "文职",
     "headcount": 2, "duties": "贰祭酒，掌监事之贰",
     "parent_office": "祭酒", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    # ===== 六部司官 =====
    {"office_name": "郎中", "rank": "正五品", "type": "实职", "system": "文职",
     "headcount": "约20", "duties": "掌一司之事，为司之长",
     "parent_office": "侍郎", "child_offices": ["员外郎", "主事"],
     "location": "中央", "history": [{"year": "洪武元年", "event": "每部设郎中"}],
     "note": "六部各司郎中：吏部4/户部13/礼部4/兵部4/刑部13/工部4"},
    
    {"office_name": "员外郎", "rank": "从五品", "type": "实职", "system": "文职",
     "headcount": "约20", "duties": "贰郎中，掌司事之贰",
     "parent_office": "郎中", "child_offices": ["主事"],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "主事", "rank": "正六品", "type": "实职", "system": "文职",
     "headcount": "约40", "duties": "掌司务，办理文书",
     "parent_office": "郎中", "child_offices": [],
     "location": "中央", "history": [], "note": "各司主事，事务繁简增减不同"},
    
    # ===== 宗人府 =====
    {"office_name": "宗人令", "rank": "正一品", "type": "实职", "system": "文职",
     "headcount": 1, "duties": "掌皇九族之属籍，修玉牒",
     "parent_office": "皇帝", "child_offices": ["左宗正", "右宗正", "左宗人", "右宗人"],
     "location": "中央", "history": [{"year": "洪武三年", "event": "置大宗正院"}, {"year": "洪武二十二年", "event": "改为宗人府"}],
     "note": "以亲王领宗人府事"},
    
    {"office_name": "右宗正", "rank": "正一品", "type": "实职", "system": "文职",
     "headcount": 1, "duties": "佐宗人令掌府事",
     "parent_office": "宗人令", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    {"office_name": "右宗人", "rank": "正一品", "type": "实职", "system": "文职",
     "headcount": 1, "duties": "佐宗人令掌府事",
     "parent_office": "宗人令", "child_offices": [],
     "location": "中央", "history": [], "note": ""},
    
    # ===== 地方文官 =====
    {"office_name": "布政使", "rank": "从二品", "type": "实职", "system": "文职",
     "headcount": 13, "duties": "掌一省之民政、财政，承宣政令",
     "parent_office": "六部", "child_offices": ["参政", "参议", "知府"],
     "location": "地方", "history": [{"year": "洪武九年", "event": "改行中书省为承宣布政使司"}],
     "note": "十三布政司左右布政使各1人"},
    
    {"office_name": "按察使", "rank": "正三品", "type": "实职", "system": "文职",
     "headcount": 13, "duties": "掌一省之司法、监察，澄清吏治",
     "parent_office": "都察院", "child_offices": ["副使", "佥事"],
     "location": "地方", "history": [{"year": "洪武三十年", "event": "按察司设按察使"}],
     "note": "十三按察司各1人"},
    
    {"office_name": "知府", "rank": "正四品", "type": "实职", "system": "文职",
     "headcount": "约150", "duties": "掌一府之政，宣风化，平狱讼，均赋役",
     "parent_office": "布政使", "child_offices": ["同知", "通判", "推官", "知州", "知县"],
     "location": "地方", "history": [], "note": "府一级行政长官"},
    
    {"office_name": "同知", "rank": "正五品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "贰知府，掌府事之贰",
     "parent_office": "知府", "child_offices": [],
     "location": "地方", "history": [], "note": "府同知，或派管河、粮、捕盗等事"},
    
    {"office_name": "通判", "rank": "正六品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "掌粮运、督捕、水利等事",
     "parent_office": "知府", "child_offices": [],
     "location": "地方", "history": [], "note": "府通判，分掌粮盐督捕之事"},
    
    {"office_name": "推官", "rank": "从六品", "type": "实职", "system": "文职",
     "headcount": "每府1人", "duties": "掌一府刑狱，司理刑法",
     "parent_office": "知府", "child_offices": [],
     "location": "地方", "history": [], "note": ""},
    
    {"office_name": "知州", "rank": "从五品", "type": "实职", "system": "文职",
     "headcount": "约200", "duties": "掌一州之政",
     "parent_office": "知府", "child_offices": ["州同知", "州判官"],
     "location": "地方", "history": [], "note": "直隶州属布政司，属州属府"},
    
    {"office_name": "知县", "rank": "正七品", "type": "实职", "system": "文职",
     "headcount": "约1100", "duties": "掌一县之政，审决狱讼，劝农课桑，均赋役",
     "parent_office": "知州/知府", "child_offices": ["县丞", "主簿", "典史"],
     "location": "地方", "history": [], "note": "亲民之官，县令"},
    
    # ===== 军事系统 =====
    {"office_name": "都督", "rank": "正一品", "type": "实职", "system": "武职",
     "headcount": "无定员", "duties": "掌军旅之事，领都司卫所",
     "parent_office": "皇帝", "child_offices": ["都督同知", "都督佥事"],
     "location": "中央", "history": [{"year": "洪武十三年", "event": "改大都督府为五军都督府"}],
     "note": "五军都督府左右都督，正一品"},
    
    {"office_name": "五军都督", "rank": "正一品", "type": "实职", "system": "武职",
     "headcount": 10, "duties": "分领在京各卫所及在外各都司卫所",
     "parent_office": "皇帝", "child_offices": ["都督同知"],
     "location": "中央", "history": [{"year": "洪武十三年", "event": "分五军都督府"}],
     "note": "中/左/右/前/后五府，每府左右都督各1人"},
    
    {"office_name": "都指挥", "rank": "正二品", "type": "实职", "system": "武职",
     "headcount": "约20", "duties": "掌一省之都司，统辖卫所",
     "parent_office": "五军都督府", "child_offices": ["都指挥同知", "都指挥佥事"],
     "location": "地方", "history": [{"year": "洪武八年", "event": "改都卫为都指挥使司"}],
     "note": "十三都司各都指挥使1人"},
    
    {"office_name": "总兵官", "rank": "无品级（差遣）", "type": "差遣", "system": "武职",
     "headcount": "无定员", "duties": "掌镇守一方，总领军务",
     "parent_office": "皇帝/兵部", "child_offices": ["副总兵", "参将"],
     "location": "地方", "history": [{"year": "洪熙", "event": "始设总兵官镇守地方"}],
     "note": "差遣官，无品级，以公侯伯或都督充任"},
    
    {"office_name": "副总兵", "rank": "无品级（差遣）", "type": "差遣", "system": "武职",
     "headcount": "无定员", "duties": "佐总兵官掌军务",
     "parent_office": "总兵官", "child_offices": ["参将"],
     "location": "地方", "history": [], "note": "差遣官"},
    
    {"office_name": "参将", "rank": "无品级（差遣）", "type": "差遣", "system": "武职",
     "headcount": "无定员", "duties": "分掌一路之军务",
     "parent_office": "总兵官/副总兵", "child_offices": [],
     "location": "地方", "history": [], "note": "差遣官"},
    
    # ===== 行人司 =====
    {"office_name": "行人", "rank": "正八品", "type": "实职", "system": "文职",
     "headcount": 36, "duties": "掌捧节、奉使之事，传旨册封",
     "parent_office": "司正", "child_offices": [],
     "location": "中央/地方", "history": [{"year": "洪武二十七年", "event": "行人司设行人"}],
     "note": "以进士除授，捧诏谕出使"},
]

# ===== 补salary字段 =====
for office in OFFICE_PROFILES:
    rank = office.get("rank", "")
    if "无品级" in rank:
        office["salary"] = None
        office["salary_note"] = "差遣官，无固定品级俸禄，按原品级支俸"
    elif rank in SALARY_TABLE:
        s = SALARY_TABLE[rank]
        office["salary"] = s.copy()
        office["salary"]["source"] = "029-001（俸给一）"
    else:
        office["salary"] = None

# ===== 保存 =====
output_path = os.path.join(ROOT, "_layers", "office_profiles.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(OFFICE_PROFILES, f, ensure_ascii=False, indent=2)

print(f"官职主档层已建立！")
print(f"共 {len(OFFICE_PROFILES)} 个官职")
print(f"保存到: {output_path}")

# 统计
print(f"\n===== 官职类型分布 =====")
type_count = {}
for o in OFFICE_PROFILES:
    t = o.get("type", "未知")
    type_count[t] = type_count.get(t, 0) + 1
for t, cnt in sorted(type_count.items(), key=lambda x: -x[1]):
    print(f"  {t}: {cnt}个")

print(f"\n===== 官职系统分布 =====")
sys_count = {}
for o in OFFICE_PROFILES:
    s = o.get("system", "未知")
    sys_count[s] = sys_count.get(s, 0) + 1
for s, cnt in sorted(sys_count.items(), key=lambda x: -x[1]):
    print(f"  {s}: {cnt}个")

print(f"\n===== 有俸禄的官职 =====")
has_salary = [o for o in OFFICE_PROFILES if o.get("salary")]
print(f"  {len(has_salary)}/{len(OFFICE_PROFILES)} 个有俸禄数据")
