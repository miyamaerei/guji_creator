# -*- coding: utf-8 -*-
"""补全剩余官职的上级关系（杂职小官）"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
offices = json.load(open(os.path.join(ROOT, "_layers", "office_profiles.json"), encoding="utf-8"))

# 杂职小官的上级映射
EXTRA_PARENT = {
    # 地方杂职
    "巡检司巡检": "知县",
    "税课局大使": "知府/知县",
    "税课局副使": "税课局大使",
    "仓大使": "知府/知县",
    "驿丞": "知府/知县",
    "河泊所官": "知府/知县",
    
    # 通政司
    "通政使": "皇帝",
    "左通政": "通政使",
    "右通政": "通政使",
    "左参议": "左通政",
    "右参议": "右通政",
    "通政司经历": "通政使",
    "通政司知事": "经历",
    
    # 尚宝司
    "尚宝司卿": "皇帝",
    "尚宝司少卿": "尚宝司卿",
    "尚宝司司丞": "少卿",
    
    # 行人司
    "行人司司正": "礼部",
    "行人司左司副": "司正",
    "行人司右司副": "司正",
    "行人": "司正",
    
    # 钦天监
    "钦天监监正": "礼部",
    "钦天监监副": "监正",
    "钦天监主簿": "监副",
    "钦天监春官正": "监副",
    "钦天监夏官正": "监副",
    "钦天监秋官正": "监副",
    "钦天监冬官正": "监副",
    "钦天监中官正": "监副",
    "钦天监五官灵台郎": "监副",
    "钦天监五官保章正": "监副",
    "钦天监五官挈壶正": "监副",
    "钦天监五官司历": "监副",
    "钦天监五官司辰": "监副",
    
    # 太医院
    "太医院院使": "礼部",
    "太医院院判": "院使",
    "太医院御医": "院判",
    "太医院吏目": "院判",
    
    # 上林苑监
    "上林苑监左监正": "礼部",
    "上林苑监右监正": "礼部",
    "上林苑监左监副": "左监正",
    "上林苑监右监副": "右监正",
    
    # 詹事府
    "詹事府詹事": "皇帝",
    "詹事府少詹事": "詹事",
    "詹事府府丞": "少詹事",
    "詹事府主簿": "府丞",
    
    # 别名官职的上级
    "监察御史": "都御史",
    "翰林修撰": "翰林院学士",
    
    # 六部司务
    "六部司务": "尚书",
    
    # 五城兵马司（如果有的话）
}

fixed = 0
for org in offices:
    if not org.get("parent_org"):
        name = org["office_name"]
        if name in EXTRA_PARENT:
            org["parent_org"] = EXTRA_PARENT[name]
            fixed += 1

# 保存
with open(os.path.join(ROOT, "_layers", "office_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(offices, f, ensure_ascii=False, indent=2)

print(f"补全杂职小官上级: {fixed}个")

# 统计
has_parent = sum(1 for o in offices if o.get("parent_org"))
print(f"上级官职填充率: {has_parent}/{len(offices)} ({has_parent*100//len(offices)}%)")

# 看看还有哪些没上级
no_parent = [o["office_name"] for o in offices if not o.get("parent_org")]
print(f"\n还有{len(no_parent)}个官职没上级:")
for n in no_parent[:20]:
    print(f"  - {n}")
if len(no_parent) > 20:
    print(f"  ... 等共{len(no_parent)}个")
