# -*- coding: utf-8 -*-
"""批量补全org_profiles的location和salary字段"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
orgs = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

# ===== 俸禄表（来自卷29 俸给一） =====
SALARY_TABLE = {
    "正一品": {"monthly_shi": 87, "yearly_shi": 1044, "note": "月支米87石，岁该1044石"},
    "从一品": {"monthly_shi": 74, "yearly_shi": 888, "note": "月支米74石，岁该888石"},
    "正二品": {"monthly_shi": 61, "yearly_shi": 732, "note": "月支米61石，岁该732石"},
    "从二品": {"monthly_shi": 48, "yearly_shi": 576, "note": "月支米48石，岁该576石"},
    "正三品": {"monthly_shi": 35, "yearly_shi": 420, "note": "月支米35石，岁该420石"},
    "从三品": {"monthly_shi": 26, "yearly_shi": 312, "note": "月支米26石，岁该312石"},
    "正四品": {"monthly_shi": 24, "yearly_shi": 288, "note": "月支米24石，岁该288石"},
    "从四品": {"monthly_shi": 21, "yearly_shi": 252, "note": "月支米21石，岁该252石"},
    "正五品": {"monthly_shi": 16, "yearly_shi": 192, "note": "月支米16石，岁该192石"},
    "从五品": {"monthly_shi": 14, "yearly_shi": 168, "note": "月支米14石，岁该168石"},
    "正六品": {"monthly_shi": 10, "yearly_shi": 120, "note": "月支米10石，岁该120石"},
    "从六品": {"monthly_shi": 8, "yearly_shi": 96, "note": "月支米8石，岁该96石"},
    "正七品": {"monthly_shi": 7.5, "yearly_shi": 90, "note": "月支米7.5石，岁该90石"},
    "从七品": {"monthly_shi": 7, "yearly_shi": 84, "note": "月支米7石，岁该84石"},
    "正八品": {"monthly_shi": 6.5, "yearly_shi": 78, "note": "月支米6.5石，岁该78石"},
    "从八品": {"monthly_shi": 6, "yearly_shi": 72, "note": "月支米6石，岁该72石"},
    "正九品": {"monthly_shi": 5.5, "yearly_shi": 66, "note": "月支米5.5石，岁该66石"},
    "从九品": {"monthly_shi": 5, "yearly_shi": 60, "note": "月支米5石，岁该60石"},
    "未入流": {"monthly_shi": 3, "yearly_shi": 36, "note": "未入流杂职，月支米约3石"},
}

# ===== Location判断规则 =====
# 北京中央机构
BEIJING_CENTRAL = {
    "宗人府", "吏部", "户部", "礼部", "兵部", "刑部", "工部",
    "都察院", "通政司", "大理寺", "太常寺", "光禄寺", "鸿胪寺", "太仆寺",
    "国子监", "翰林院", "钦天监", "太医院", "上林苑监",
    "五军都督府", "中军都督府", "左军都督府", "右军都督府", "前军都督府", "后军都督府",
    "司礼监", "御马监", "内官监", "御用监", "司设监", "尚宝监", "尚膳监", "尚衣监", "印绶监",
    "文选清吏司", "验封清吏司", "稽勋清吏司", "考功清吏司",
    "浙江清吏司", "江西清吏司", "福建清吏司", "湖广清吏司", "山东清吏司", "山西清吏司", "河南清吏司", "陕西清吏司", "四川清吏司", "广东清吏司", "广西清吏司", "云南清吏司", "贵州清吏司",
    "仪制清吏司", "祠祭清吏司", "主客清吏司", "精膳清吏司",
    "武选清吏司", "职方清吏司", "车驾清吏司", "武库清吏司",
    "营缮清吏司", "虞衡清吏司", "都水清吏司", "屯田清吏司",
    "司务厅", "照磨所", "检校",
    "求贤科", "开设科", "都书科", "缺科", "升调科",
}

# 地方行政机构
LOCAL_GOV = {
    "顺天府", "应天府",
}

def get_location(org):
    """判断部门位置"""
    name = org["org_name"]
    category = org.get("category", "")
    
    if name in BEIJING_CENTRAL:
        return "北京·中央"
    elif name in LOCAL_GOV:
        if name == "顺天府":
            return "北京·地方（京府）"
        elif name == "应天府":
            return "南京·地方（留都）"
    
    if category == "宦官机构":
        return "北京·中央（内府）"
    elif category == "中央军事":
        return "北京·中央"
    elif category == "中央文职":
        return "北京·中央"
    elif category == "地方行政":
        return "地方"
    
    return "未明"

def get_salary(org):
    """根据品级获取俸禄"""
    rank = org.get("rank", "")
    if rank in SALARY_TABLE:
        s = SALARY_TABLE[rank].copy()
        s["source"] = "029-001~029-009（俸给一）"
        s["note_detail"] = "明代实行米钞兼支制度，永乐以后折色比例多次变动"
        return s
    return None

# ===== 执行批量补全 =====
updated_count = 0
for org in orgs:
    # 补location
    if "location" not in org:
        org["location"] = get_location(org)
        org["location_source"] = "AI根据机构性质推断"
        updated_count += 1
    
    # 补salary
    if "salary" not in org:
        org["salary"] = get_salary(org)
        if org["salary"]:
            org["salary_source"] = "029-001（俸给一）"
            updated_count += 1

# 保存
with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(orgs, f, ensure_ascii=False, indent=2)

print(f"补全完成！")
print(f"共 {len(orgs)} 个部门")
print(f"更新字段: {updated_count} 个")

# 统计
print(f"\n===== Location分布 =====")
loc_count = {}
for org in orgs:
    loc = org.get("location", "未明")
    loc_count[loc] = loc_count.get(loc, 0) + 1
for loc, cnt in sorted(loc_count.items(), key=lambda x: -x[1]):
    print(f"  {loc}: {cnt}个")

print(f"\n===== Salary覆盖 =====")
has_salary = [o for o in orgs if o.get("salary")]
no_salary = [o for o in orgs if not o.get("salary")]
print(f"  有salary: {len(has_salary)}个")
print(f"  无salary: {len(no_salary)}个")
if no_salary:
    print(f"  无salary的部门: {', '.join([o['org_name'] for o in no_salary[:10]])}...")

# 抽几个例子看看
print(f"\n===== 抽样验证 =====")
for name in ["吏部", "文选清吏司", "司礼监", "顺天府"]:
    org = next((o for o in orgs if o["org_name"] == name), None)
    if org:
        print(f"\n【{name}】")
        print(f"  location: {org.get('location')}")
        sal = org.get("salary")
        if sal:
            print(f"  salary: 月{sal['monthly_shi']}石 / 岁{sal['yearly_shi']}石")
        else:
            print(f"  salary: 无")
