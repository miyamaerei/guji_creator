# -*- coding: utf-8 -*-
"""AI校验修正：逐个部门检查每个字段，用明代官制知识修正"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ===== 明代官制标准知识（AI校验基准） =====
# 从互联网搜索整理的标准信息
STANDARD_KNOWLEDGE = {
    "宗人府": {
        "rank": "正一品",
        "staff": "宗人令1人，左/右宗正各1人，左/右宗人各1人",
        "duties": "掌皇九族之属籍，修玉牒，书宗室子女嫡庶名封生卒婚嫁谥葬",
        "history": "洪武三年置大宗正院，二十二年改为宗人府",
        "category": "中央文职",
    },
    "吏部": {
        "rank": "正二品",
        "staff": "尚书1人，左右侍郎各1人，文选/验封/稽勋/考功4司各郎中1人员外郎1人主事1人",
        "duties": "掌天下官吏选授封考之政令",
        "history": "洪武元年始置，正三品，十三年升正二品",
        "category": "中央文职",
    },
    "户部": {
        "rank": "正二品",
        "staff": "尚书1人，左右侍郎各1人，十三清吏司各郎中1人员外郎1人主事1人",
        "duties": "掌天下户口田赋经费之政令",
        "history": "洪武元年始置，正三品，十三年升正二品",
        "category": "中央文职",
    },
    "礼部": {
        "rank": "正二品",
        "staff": "尚书1人，左右侍郎各1人，仪制/祠祭/主客/精膳4司各郎中1人员外郎1人主事1人",
        "duties": "掌天下礼仪祭祀宴贡之政令",
        "history": "洪武元年始置，正三品，十三年升正二品",
        "category": "中央文职",
    },
    "兵部": {
        "rank": "正二品",
        "staff": "尚书1人，左右侍郎各1人，武选/职方/车驾/武库4司各郎中1人员外郎1人主事1人",
        "duties": "掌天下武卫官军选授简练之政令",
        "history": "洪武元年始置，正三品，十三年升正二品",
        "category": "中央文职",
    },
    "刑部": {
        "rank": "正二品",
        "staff": "尚书1人，左右侍郎各1人，十三清吏司各郎中1人员外郎1人主事1人",
        "duties": "掌天下刑名及徒隶勾覆关禁之政令",
        "history": "洪武元年始置，正三品，十三年升正二品",
        "category": "中央文职",
    },
    "工部": {
        "rank": "正二品",
        "staff": "尚书1人，左右侍郎各1人，营缮/虞衡/都水/屯田4司各郎中1人员外郎1人主事1人",
        "duties": "掌天下百工屯田水利之政令",
        "history": "洪武元年始置，正三品，十三年升正二品",
        "category": "中央文职",
    },
    "都察院": {
        "rank": "正二品",
        "staff": "左/右都御史各1人，左/右副都御史各1人，左/右佥都御史各1人，十三道监察御史110人",
        "duties": "职专纠劾百司，辩明冤枉，提督各道，为天子耳目风纪之司",
        "history": "洪武十五年设都察院，十七年定正二品",
        "category": "中央文职",
    },
    "通政司": {
        "rank": "正三品",
        "staff": "通政使1人，左右通政各1人，左右参议各1人",
        "duties": "掌内外章奏封驳申辩之事",
        "history": "洪武十年置",
        "category": "中央文职",
    },
    "大理寺": {
        "rank": "正三品",
        "staff": "卿1人，左右少卿各1人，左右寺丞各1人",
        "duties": "掌审谳平反刑狱之政令",
        "history": "洪武十四年置",
        "category": "中央文职",
    },
    "太常寺": {
        "rank": "正三品",
        "staff": "卿1人，少卿2人，寺丞2人",
        "duties": "掌祭祀礼乐郊庙社稷之事",
        "history": "洪武三十年改太常司为太常寺",
        "category": "中央文职",
    },
    "光禄寺": {
        "rank": "从三品",
        "staff": "卿1人，少卿2人，寺丞2人",
        "duties": "掌祭享宴劳酒醴膳羞之事",
        "history": "洪武八年改光禄寺",
        "category": "中央文职",
    },
    "鸿胪寺": {
        "rank": "正四品",
        "staff": "卿1人，左右少卿各1人，左右寺丞各1人",
        "duties": "掌朝会宾客吉凶礼仪相礼之事",
        "history": "洪武三十年改殿庭仪礼司为鸿胪寺",
        "category": "中央文职",
    },
    "太仆寺": {
        "rank": "从三品",
        "staff": "卿1人，少卿2人，寺丞2人",
        "duties": "掌牧马之政令",
        "history": "洪武六年置",
        "category": "中央文职",
    },
    "国子监": {
        "rank": "从四品",
        "staff": "祭酒1人，司业1人，监丞1人，博士5人，助教15人",
        "duties": "掌国学诸生训导之政令",
        "history": "洪武元年置国子学，十五年改国子监",
        "category": "中央文职",
    },
    "翰林院": {
        "rank": "正五品",
        "staff": "学士1人，侍读学士/侍讲学士各2人，侍读/侍讲各2人，修撰3人，编修4人，检讨4人",
        "duties": "掌制诰史册文翰之事",
        "history": "洪武初置",
        "category": "中央文职",
    },
    "钦天监": {
        "rank": "正五品",
        "staff": "监正1人，监副2人",
        "duties": "掌天文历数镜像推候之事",
        "history": "洪武元年置司天监，三年改钦天监",
        "category": "中央文职",
    },
    "太医院": {
        "rank": "正五品",
        "staff": "院使1人，院判2人",
        "duties": "掌医疗之法",
        "history": "洪武六年置",
        "category": "中央文职",
    },
    "上林苑监": {
        "rank": "正五品",
        "staff": "左/右监正各1人，左/右监副各1人，左/右监丞各1人",
        "duties": "掌苑囿园池牧养种树之事",
        "history": "洪武十四年置",
        "category": "中央文职",
    },
    "五军都督府": {
        "rank": "正一品",
        "staff": "左/右都督各1人，都督同知，都督佥事",
        "duties": "掌军旅之事，分领都司卫所",
        "history": "洪武十三年改大都督府为五军都督府",
        "category": "军事",
    },
}

# ===== 加载现有数据，然后用标准知识修正 =====
org_profiles = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

corrected = []
issues = []

for org in org_profiles:
    name = org["org_name"]
    if name in STANDARD_KNOWLEDGE:
        std = STANDARD_KNOWLEDGE

        # 检查每个字段，如果不对就修正
        corrections = []

        # 品级
        if "rank" in std and org.get("rank") != std["rank"]:
            corrections.append(f"品级: {org.get('rank', '?')} → {std['rank']}")
            org["rank"] = std["rank"]
            org["rank_source"] = "AI校验（标准明代官制）"

        # 编制
        if "staff" in std and (not org.get("staff") or len(org.get("staff", "")) < 10):
            corrections.append(f"编制: {org.get('staff', '?')[:20] if org.get('staff') else '无'} → 标准编制")
            org["staff"] = std["staff"]
            org["staff_source"] = "AI校验（标准明代官制）"

        # 职责
        if "duties" in std and (not org.get("duties") or len(org.get("duties", "")) < 10):
            corrections.append(f"职责: {org.get('duties', '?')[:20] if org.get('duties') else '无'} → 标准职责")
            org["duties"] = std["duties"]
            org["duties_source"] = "AI校验（标准明代官制）"

        # 沿革
        if "history" in std and not org.get("history"):
            corrections.append(f"沿革: 无 → {std['history'][:30]}")
            org["history"] = std["history"]
            org["history_source"] = "AI校验（标准明代官制）"

        # 位置
        if "category" in std and org.get("category") != std["category"]:
            corrections.append(f"位置: {org.get('category', '?')} → {std['category']}")
            org["category"] = std["category"]
            org["category_source"] = "AI校验（标准明代官制）"

        if corrections:
            issues.append((name, corrections))

    corrected.append(org)

# ===== 输出修正结果 =====
print("=" * 70)
print("AI校验修正结果")
print("=" * 70)

print(f"\n共修正 {len(issues)} 个部门:")
for name, corrections in issues:
    print(f"\n【{name}】")
    for c in corrections:
        print(f"  - {c}")

# ===== 验证报告 =====
print(f"\n\n{'=' * 70}")
print("验证报告：密度与规范性")
print("=" * 70)

# 检查每个部门的字段完整度
fields = ["rank", "staff", "duties", "history", "category"]
field_names = {
    "rank": "品级",
    "staff": "编制",
    "duties": "职责",
    "history": "沿革",
    "category": "位置",
}

print(f"\n字段完整度:")
print(f"{'部门':12s}", end="")
for f in fields:
    print(f" {field_names[f]:6s}", end="")
print()
print("-" * 50)

low_density = []
for org in corrected:
    name = org["org_name"]
    print(f"{name:12s}", end="")
    missing = []
    for f in fields:
        if org.get(f):
            print(f" ✅    ", end="")
        else:
            print(f" ❌    ", end="")
            missing.append(field_names[f])
    if missing:
        low_density.append((name, missing))
    print()

print(f"\n\n密度不够的部门（有缺失字段）:")
for name, missing in low_density:
    print(f"  - {name}: 缺 {', '.join(missing)}")

# 保存
with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(corrected, f, ensure_ascii=False, indent=1)

print(f"\n已保存修正后的org_profiles.json")
