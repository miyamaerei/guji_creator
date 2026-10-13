# -*- coding: utf-8 -*-
"""修复官职数据：补上级、修正散官俸禄、加别名"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
offices = json.load(open(os.path.join(ROOT, "_layers", "office_profiles.json"), encoding="utf-8"))

# ===== 1. 补全上级官职映射 =====
# 规则：根据官职名推断上级
PARENT_MAP = {
    # 六部司官
    "吏部": "吏部尚书",
    "户部": "户部尚书",
    "礼部": "礼部尚书",
    "兵部": "兵部尚书",
    "刑部": "刑部尚书",
    "工部": "工部尚书",
}

def infer_parent(name):
    """根据官职名推断上级"""
    
    # 六部各司郎中/员外郎/主事 → 上级是侍郎
    if "清吏司郎中" in name:
        bu = name.split("清吏司")[0][-2:]  # 取最后两个字判断是哪个部
        if "吏部" in name: return "吏部左侍郎"
        if "户部" in name: return "户部左侍郎"
        if "礼部" in name: return "礼部左侍郎"
        if "兵部" in name: return "兵部左侍郎"
        if "刑部" in name: return "刑部左侍郎"
        if "工部" in name: return "工部左侍郎"
    if "清吏司员外郎" in name:
        return name.replace("员外郎", "郎中")
    if "清吏司主事" in name:
        return name.replace("主事", "郎中")
    
    # 六部尚书 → 皇帝
    if name.endswith("尚书"):
        return "皇帝"
    
    # 六部侍郎 → 尚书
    if "左侍郎" in name:
        bu = name.replace("左侍郎", "尚书")
        return bu
    if "右侍郎" in name:
        bu = name.replace("右侍郎", "尚书")
        return bu
    
    # 都察院系统
    if "左都御史" == name: return "皇帝"
    if "右都御史" == name: return "皇帝"
    if "左副都御史" in name: return "左都御史"
    if "右副都御史" in name: return "右都御史"
    if "左佥都御史" in name: return "左副都御史"
    if "右佥都御史" in name: return "右副都御史"
    if "道监察御史" in name: return "都御史"
    if "都察院经历" in name: return "都御史"
    if "都察院都事" in name: return "都御史"
    if "都察院司务" in name: return "都御史"
    if "都察院照磨" in name: return "都御史"
    if "都察院检校" in name: return "照磨"
    if "都察院司狱" in name: return "都御史"
    
    # 六科
    if "科都给事中" in name: return "皇帝"
    if "科左给事中" in name: return name.replace("左给事中", "都给事中")
    if "科右给事中" in name: return name.replace("右给事中", "都给事中")
    if "科给事中" in name and "都" not in name and "左" not in name and "右" not in name:
        ke = name.replace("科给事中", "科都给事中")
        return ke
    
    # 五寺
    if name == "大理寺卿": return "皇帝"
    if "大理寺左少卿" in name: return "大理寺卿"
    if "大理寺右少卿" in name: return "大理寺卿"
    if "大理寺左寺丞" in name: return "大理寺左少卿"
    if "大理寺右寺丞" in name: return "大理寺右少卿"
    if "大理寺左寺正" in name: return "左寺丞"
    if "大理寺右寺正" in name: return "右寺丞"
    if "大理寺左寺副" in name: return "左寺正"
    if "大理寺右寺副" in name: return "右寺正"
    if "大理寺评事" in name: return "寺正"
    if "大理寺司务" in name: return "大理寺卿"
    
    if name == "太常寺卿": return "皇帝"
    if "太常寺少卿" in name: return "太常寺卿"
    if "太常寺寺丞" in name: return "少卿"
    if "太常寺典簿" in name: return "寺丞"
    if "太常寺博士" in name: return "寺丞"
    if "太常寺协律郎" in name: return "寺丞"
    if "太常寺赞礼郎" in name: return "寺丞"
    if "太常寺司乐" in name: return "寺丞"
    
    if name == "光禄寺卿": return "皇帝"
    if "光禄寺少卿" in name: return "光禄寺卿"
    if "光禄寺寺丞" in name: return "少卿"
    if "光禄寺典簿" in name: return "寺丞"
    
    if name == "鸿胪寺卿": return "皇帝"
    if "鸿胪寺左少卿" in name: return "鸿胪寺卿"
    if "鸿胪寺右少卿" in name: return "鸿胪寺卿"
    if "鸿胪寺左寺丞" in name: return "左少卿"
    if "鸿胪寺右寺丞" in name: return "右少卿"
    if "鸿胪寺主簿" in name: return "寺丞"
    if "鸿胪寺鸣赞" in name: return "寺丞"
    if "鸿胪寺序班" in name: return "寺丞"
    
    if name == "太仆寺卿": return "皇帝"
    if "太仆寺少卿" in name: return "太仆寺卿"
    if "太仆寺寺丞" in name: return "少卿"
    if "太仆寺主簿" in name: return "寺丞"
    
    # 翰林院
    if name == "翰林院学士": return "皇帝"
    if "翰林院侍读学士" in name: return "学士"
    if "翰林院侍讲学士" in name: return "学士"
    if "翰林院侍读" in name: return "侍读学士"
    if "翰林院侍讲" in name: return "侍讲学士"
    if "翰林院修撰" in name: return "学士"
    if "翰林院编修" in name: return "学士"
    if "翰林院检讨" in name: return "学士"
    if "翰林院五经博士" in name: return "学士"
    if "翰林院待诏" in name: return "学士"
    if "翰林院典籍" in name: return "学士"
    if "翰林院主簿" in name: return "学士"
    
    # 国子监
    if name == "国子监祭酒": return "礼部"
    if "国子监司业" in name: return "祭酒"
    if "国子监监丞" in name: return "司业"
    if "国子监博士" in name: return "司业"
    if "国子监助教" in name: return "司业"
    if "国子监学正" in name: return "司业"
    if "国子监学录" in name: return "学正"
    if "国子监典簿" in name: return "司业"
    if "国子监典籍" in name: return "司业"
    
    # 地方官
    if name == "布政使": return "六部"
    if "布政司左参政" in name: return "布政使"
    if "布政司右参政" in name: return "布政使"
    if "布政司左参议" in name: return "布政使"
    if "布政司右参议" in name: return "布政使"
    
    if name == "按察使": return "都察院"
    if "按察司副使" in name: return "按察使"
    if "按察司佥事" in name: return "按察使"
    
    if name == "知府": return "布政使"
    if "府同知" in name: return "知府"
    if "府通判" in name: return "知府"
    if "府推官" in name: return "知府"
    if "府经历" in name: return "知府"
    if "府照磨" in name: return "经历"
    if "府司狱" in name: return "知府"
    
    if name == "知州": return "知府"
    if "州同知" in name: return "知州"
    if "州判官" in name: return "知州"
    
    if name == "知县": return "知州/知府"
    if "县丞" in name: return "知县"
    if "县主簿" in name: return "知县"
    if "典史" in name: return "知县"
    if "巡检司巡检" in name: return "知县"
    
    # 学官
    if "府儒学教授" in name: return "知府"
    if "府儒学训导" in name: return "教授"
    if "州儒学学正" in name: return "知州"
    if "州儒学训导" in name: return "学正"
    if "县儒学教谕" in name: return "知县"
    if "县儒学训导" in name: return "教谕"
    
    # 军事
    if name == "左都督" or name == "右都督": return "皇帝"
    if "都督同知" in name: return "都督"
    if "都督佥事" in name: return "都督同知"
    
    if name == "都指挥使": return "五军都督府"
    if "都指挥同知" in name: return "都指挥使"
    if "都指挥佥事" in name: return "都指挥同知"
    
    if name == "卫指挥使": return "都指挥使"
    if "卫指挥同知" in name: return "指挥使"
    if "卫指挥佥事" in name: return "指挥同知"
    if "卫镇抚" in name: return "指挥佥事"
    
    if name == "正千户": return "卫指挥使"
    if "副千户" in name: return "正千户"
    if "千户所镇抚" in name: return "副千户"
    
    if name == "百户": return "正千户"
    if "总旗" in name: return "百户"
    if "小旗" in name: return "总旗"
    
    # 差遣
    if name == "总兵官": return "皇帝/兵部"
    if name == "副总兵": return "总兵官"
    if name == "参将": return "总兵官/副总兵"
    if name == "游击将军": return "参将"
    if name == "守备": return "游击将军"
    if name == "把总": return "守备"
    
    # 宦官
    if "掌印太监" in name: return "内府"
    if "左右少监" in name: return "掌印太监"
    if "左右监丞" in name: return "掌印太监"
    
    # 散官/虚衔 → 无上级
    if "大夫" in name or "郎" in name:
        return ""  # 散官无上级
    if "太师" in name or "太傅" in name or "太保" in name:
        return ""  # 虚衔无上级
    if "太子" in name:
        return ""  # 虚衔无上级
    
    return ""  # 默认空

# ===== 2. 修正散官俸禄 =====
def fix_salary(org):
    type_ = org.get("type", "")
    if type_ == "散官":
        org["salary"] = None
        org["salary_note"] = "散官是品级称号，非实职，按实际职务支俸"
    elif type_ == "虚衔":
        org["salary"] = None
        org["salary_note"] = "虚衔加官，无俸禄"
    return org

# ===== 3. 执行修复 =====
fixed_parent = 0
fixed_salary = 0

for org in offices:
    # 补上级
    if not org.get("parent_org"):
        parent = infer_parent(org["office_name"])
        if parent:
            org["parent_org"] = parent
            fixed_parent += 1
    
    # 修正散官俸禄
    old_salary = org.get("salary")
    org = fix_salary(org)
    if old_salary and not org.get("salary"):
        fixed_salary += 1

# ===== 4. 加几个笼统的官职别名 =====
aliases = [
    {"office_name": "监察御史", "rank": "正七品", "type": "实职", "system": "文职",
     "headcount": 110, "duties": "掌巡按地方，监察百官，纠劾不法（十三道统称）",
     "parent_office": "都御史", "child_offices": [], "location": "中央/地方",
     "history": [], "note": "十三道监察御史的统称"},
    {"office_name": "郎中", "rank": "正五品", "type": "实职", "system": "文职",
     "headcount": "约20", "duties": "掌一司之事（六部各司统称）",
     "parent_office": "侍郎", "child_offices": [], "location": "中央",
     "history": [], "note": "六部各司郎中的统称"},
    {"office_name": "员外郎", "rank": "从五品", "type": "实职", "system": "文职",
     "headcount": "约20", "duties": "贰郎中，掌司事之贰（统称）",
     "parent_office": "郎中", "child_offices": [], "location": "中央",
     "history": [], "note": "六部各司员外郎的统称"},
    {"office_name": "主事", "rank": "正六品", "type": "实职", "system": "文职",
     "headcount": "约40", "duties": "掌司务，办理文书（统称）",
     "parent_office": "郎中", "child_offices": [], "location": "中央",
     "history": [], "note": "六部各司主事的统称"},
    {"office_name": "翰林修撰", "rank": "从六品", "type": "实职", "system": "文职",
     "headcount": "无定员", "duties": "掌修国史（状元授官）",
     "parent_office": "学士", "child_offices": [], "location": "中央",
     "history": [], "note": "翰林院修撰的别名"},
]

# 检查是否已存在，不存在就加
existing_names = {o["office_name"] for o in offices}
for alias in aliases:
    if alias["office_name"] not in existing_names:
        # 补salary
        if alias["rank"] in ["正五品", "从五品", "正六品", "从六品", "正七品"]:
            salary_map = {
                "正五品": {"monthly_shi": 16, "yearly_shi": 192},
                "从五品": {"monthly_shi": 14, "yearly_shi": 168},
                "正六品": {"monthly_shi": 10, "yearly_shi": 120},
                "从六品": {"monthly_shi": 8, "yearly_shi": 96},
                "正七品": {"monthly_shi": 7.5, "yearly_shi": 90},
            }
            alias["salary"] = salary_map.get(alias["rank"])
        offices.append(alias)

# ===== 保存 =====
with open(os.path.join(ROOT, "_layers", "office_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(offices, f, ensure_ascii=False, indent=2)

print(f"修复完成！")
print(f"总官职数: {len(offices)}")
print(f"补全上级官职: {fixed_parent}个")
print(f"修正散官俸禄: {fixed_salary}个")
print(f"新增别名官职: {len(aliases)}个")

# 统计上级填充率
has_parent = sum(1 for o in offices if o.get("parent_org"))
print(f"\n上级官职填充率: {has_parent}/{len(offices)} ({has_parent*100//len(offices)}%)")

# 再抽查几个
print(f"\n===== 修复后抽查 =====")
check = ["吏部文选清吏司郎中", "知府", "监察御史", "翰林修撰", "特进光禄大夫"]
for name in check:
    org = next((o for o in offices if o["office_name"] == name), None)
    if org:
        print(f"  {name}: 上级={org.get('parent_org', '空')}, 俸禄={'有' if org.get('salary') else '无'}")
    else:
        print(f"  {name}: ❌ 未找到")
