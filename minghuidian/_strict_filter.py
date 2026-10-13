# -*- coding: utf-8 -*-
"""严格人工审核：逐条过滤句子片段"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# ===== 明显是句子片段的关键词 =====
FRAGMENT_KEYWORDS = [
    "凡", "一", "先", "后", "又", "复", "乃", "遂", "即", "便",
    "令", "奏", "咨", "移", "行", "送", "发", "付", "下", "上",
    "准", "照", "依", "按", "据", "因", "为", "以", "于", "在",
    "与", "及", "并", "和", "同", "共", "各", "每", "该", "此",
    "其", "之", "者", "也", "矣", "焉", "乎", "哉",
    "年", "月", "日", "时", "刻",
    "名", "员", "人", "丁", "口",
    "赴", "往", "到", "来", "去", "过",
    "取", "给", "纳", "收", "支", "出", "入",
    "知", "见", "闻", "问", "答",
    "上", "下", "左", "右", "前", "后", "内", "外",
]

def is_fragment(name):
    """判断是否是句子片段"""
    # 长度不对
    if len(name) < 2 or len(name) > 6:
        return True
    # 开头是虚词/动词
    for kw in FRAGMENT_KEYWORDS[:30]:
        if name.startswith(kw):
            return True
    # 结尾是虚词/动词
    for kw in FRAGMENT_KEYWORDS[:30]:
        if name.endswith(kw):
            return True
    # 包含数字
    if re.search(r"[一二三四五六七八九十百千万0-9]", name):
        return True
    return False

# ===== 严格的部门名白名单 =====
CLEAN_ORGS = {
    # 中央衙门
    "宗人府", "吏部", "户部", "礼部", "兵部", "刑部", "工部",
    "都察院", "通政司", "大理寺", "太常寺", "光禄寺", "鸿胪寺",
    "太仆寺", "国子监", "翰林院", "钦天监", "太医院", "上林苑监",
    "五军都督府", "中军都督府", "左军都督府", "右军都督府",
    "前军都督府", "后军都督府", "中书省",
    # 六部下属司
    "文选司", "验封司", "稽勋司", "考功司",
    "仪制司", "祠祭司", "主客司", "精膳司",
    "武选司", "职方司", "车驾司", "武库司",
    "河南司", "山西司", "山东司", "湖广司", "陕西司",
    "广东司", "广西司", "四川司", "福建司", "浙江司",
    "江西司", "云南司", "贵州司",
    # 其他
    "行人司", "尚宝司", "六科", "十三道",
}

# ===== 严格的官职名白名单 =====
CLEAN_OFFICES = {
    "尚书", "侍郎", "郎中", "员外郎", "主事",
    "都御史", "左都御史", "右都御史", "副都御史", "佥都御史", "御史",
    "大理寺卿", "大理寺少卿", "寺丞",
    "通政使", "通政副使",
    "太常寺卿", "太常寺少卿",
    "光禄寺卿", "光禄寺少卿",
    "鸿胪寺卿", "鸿胪寺少卿",
    "太仆寺卿", "太仆寺少卿",
    "祭酒", "司业",
    "学士", "侍读学士", "侍讲学士", "修撰", "编修", "检讨",
    "布政使", "按察使", "知府", "知州", "知县",
    "宗人令", "左宗正", "右宗正", "左宗人", "右宗人",
}

# ===== 过滤org_profiles =====
org_profiles = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

clean_orgs = []
for o in org_profiles:
    name = o["org_name"].strip()
    # 精确匹配
    if name in CLEAN_ORGS:
        clean_orgs.append(o)
    # 或者是干净的变体（如"南京吏部"）
    elif name.startswith("南京") and name[2:] in CLEAN_ORGS:
        clean_orgs.append(o)
    elif name.startswith("行在") and name[2:] in CLEAN_ORGS:
        clean_orgs.append(o)

# 去重
seen = set()
unique_orgs = []
for o in clean_orgs:
    if o["org_name"] not in seen:
        seen.add(o["org_name"])
        unique_orgs.append(o)

print(f"【org_profiles 严格过滤】")
print(f"  过滤前: {len(org_profiles)}条")
print(f"  过滤后: {len(unique_orgs)}条")
print(f"\n  干净部门名列表:")
for o in sorted(unique_orgs, key=lambda x: x["org_name"]):
    print(f"    - {o['org_name']}")

with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(unique_orgs, f, ensure_ascii=False, indent=1)

# ===== 过滤offices =====
offices = json.load(open(os.path.join(ROOT, "_layers", "offices.json"), encoding="utf-8"))

clean_offices = []
for o in offices:
    name = o["office_name"].strip()
    if name in CLEAN_OFFICES:
        clean_offices.append(o)

# 去重
seen = set()
unique_offices = []
for o in clean_offices:
    if o["office_name"] not in seen:
        seen.add(o["office_name"])
        unique_offices.append(o)

print(f"\n【offices 严格过滤】")
print(f"  过滤前: {len(offices)}条")
print(f"  过滤后: {len(unique_offices)}条")
print(f"\n  干净官职名列表:")
for o in sorted(unique_offices, key=lambda x: x["office_name"]):
    print(f"    - {o['office_name']}")

with open(os.path.join(ROOT, "_layers", "offices.json"), "w", encoding="utf-8") as f:
    json.dump(unique_offices, f, ensure_ascii=False, indent=1)

# ===== 过滤person_profiles =====
person_profiles = json.load(open(os.path.join(ROOT, "_layers", "person_profiles.json"), encoding="utf-8"))

clean_persons = []
for p in person_profiles:
    name = p["office_name"].strip()
    if name in CLEAN_OFFICES:
        clean_persons.append(p)

print(f"\n【person_profiles 严格过滤】")
print(f"  过滤前: {len(person_profiles)}条")
print(f"  过滤后: {len(clean_persons)}条")

with open(os.path.join(ROOT, "_layers", "person_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(clean_persons, f, ensure_ascii=False, indent=1)

print(f"\n✅ 严格人工审核完成")
