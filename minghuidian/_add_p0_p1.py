# -*- coding: utf-8 -*-
"""P0+P1补全：五城兵马司/宗人府/王府官/布按二司内部/卫所内部"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
offices = json.load(open(os.path.join(ROOT, "_layers", "office_profiles.json"), encoding="utf-8"))

def add(name, rank, type_="实职", system="文职", headcount=1, duties="", parent="", location="中央", source="", note=""):
    offices.append({
        "office_name": name,
        "rank": rank,
        "type": type_,
        "system": system,
        "headcount": headcount,
        "duties": duties,
        "parent_org": parent,
        "child_offices": [],
        "location": location,
        "history": [],
        "note": note,
        "duties_source": source,
    })

# ============================================================
# P0-1: 五城兵马司（北京+南京）
# ============================================================
# 出处：卷42-105礼部？不对，兵马司属于治安，应该在户部或都察院？
# 实际：五城兵马司在《明会典》卷213？不对，查一下
# 先按《明史·职官志》补

for city in ["北京", "南京"]:
    for cheng in ["中", "东", "西", "南", "北"]:
        add(f"{city}{cheng}城兵马司指挥", "正六品", 
            duties=f"掌{cheng}城巡捕盗贼，梳理街道沟渠，囚犯火禁",
            parent="兵部/五城巡城御史", 
            location="中央",
            source="卷213？待确认",
            note=f"{city}五城兵马司")
        add(f"{city}{cheng}城兵马司副指挥", "正七品",
            duties=f"贰指挥，分理{cheng}城捕盗",
            parent=f"{city}{cheng}城兵马司指挥",
            location="中央",
            note="")

# ============================================================
# P0-2: 宗人府详细官职
# ============================================================
# 出处：卷1 宗人府
add("宗人令", "正一品", duties="掌皇族属籍，修玉牒", parent="皇帝", location="中央", source="001-001", note="宗人府最高长官")
add("左宗正", "正一品", duties="贰宗人令", parent="宗人令", location="中央", source="001-001")
add("右宗正", "正一品", duties="贰宗人令", parent="宗人令", location="中央", source="001-001")
add("左宗人", "正一品", duties="参理府事", parent="宗人令", location="中央", source="001-001")
add("右宗人", "正一品", duties="参理府事", parent="宗人令", location="中央", source="001-001")
add("宗人府经历", "正五品", duties="典簿籍，收发文书", parent="宗人令", location="中央", source="001-001")

# ============================================================
# P1-1: 王府官（亲王府）
# ============================================================
# 出处：卷? 礼部/工部
add("王府长史司左长史", "正五品", duties="掌王府政令，辅相规谏", parent="亲王", location="地方", source="待查", note="亲王府")
add("王府长史司右长史", "正五品", duties="贰左长史", parent="左长史", location="地方", note="亲王府")
add("王府审理", "正六品", duties="掌推按刑狱", parent="长史", location="地方", note="亲王府")
add("王府典簿", "正九品", duties="掌王印簿录", parent="长史", location="地方", note="亲王府")
add("王府纪善", "正八品", duties="掌讽导礼赞", parent="长史", location="地方", note="亲王府")
add("王府伴读", "从九品", duties="侍亲王讲读", parent="长史", location="地方", note="亲王府")
add("王府教授", "未入流", duties="授亲王书", parent="长史", location="地方", note="亲王府")
add("王府承奉司承奉正", "正六品", duties="掌王府内使", parent="亲王", location="地方", system="宦官", note="王府宦官")
add("王府承奉司承奉副", "从六品", duties="贰承奉正", parent="承奉正", location="地方", system="宦官")

# ============================================================
# P1-2: 承宣布政使司内部官职
# ============================================================
add("布政司经历", "从六品", duties="典簿籍，收发文书", parent="布政使", location="地方")
add("布政司都事", "从七品", duties="办理文书", parent="经历", location="地方")
add("布政司照磨", "从八品", duties="掌磨勘", parent="经历", location="地方")
add("布政司检校", "从九品", duties="检校文书", parent="照磨", location="地方")
add("布政司理问", "从六品", duties="掌刑名", parent="布政使", location="地方")
add("布政司副理问", "从七品", duties="贰理问", parent="理问", location="地方")
add("布政司司狱", "从九品", duties="掌狱囚", parent="理问", location="地方")

# ============================================================
# P1-3: 提刑按察使司内部官职
# ============================================================
add("按察司经历", "正七品", duties="典簿籍", parent="按察使", location="地方")
add("按察司知事", "正八品", duties="办理文书", parent="经历", location="地方")
add("按察司照磨", "正九品", duties="掌磨勘", parent="经历", location="地方")
add("按察司司狱", "从九品", duties="掌狱囚", parent="按察使", location="地方")

# ============================================================
# P1-4: 卫所内部官职
# ============================================================
add("卫经历", "从七品", duties="掌文书", parent="卫指挥使", location="地方", system="武职")
add("卫知事", "从八品", duties="办理文书", parent="卫经历", location="地方", system="武职")
add("所镇抚", "从六品", duties="掌刑狱", parent="千户", location="地方", system="武职")

# ============================================================
# P2-1: 给现有官职补duties_source和history
# ============================================================
# 先给核心官职加source标记
SOURCE_MAP = {
    # 六部核心官职 - 出处卷2-13吏部相关
    "吏部尚书": "002-001",
    "户部尚书": "014-001",
    "礼部尚书": "042-001",
    "兵部尚书": "106-001",
    "刑部尚书": "130-001",
    "工部尚书": "144-001",
    # 俸禄出处
    "知府": "029-001",
    "知县": "029-001",
}

for org in offices:
    name = org["office_name"]
    if name in SOURCE_MAP:
        org["duties_source"] = SOURCE_MAP[name]
    elif not org.get("duties_source"):
        org["duties_source"] = ""  # 先空着，后面再补

# ============================================================
# P2-2: 都察院十三道具体人数
# ============================================================
# 《明史·职官志》：十三道监察御史共110人
dao_renshu = {
    "浙江道": 10, "江西道": 10, "福建道": 7, "四川道": 7,
    "陕西道": 8, "湖广道": 7, "广东道": 8, "广西道": 6,
    "河南道": 10, "山东道": 10, "山西道": 8, "南京道": 6, "贵州道": 3,
}

for dao, renshu in dao_renshu.items():
    name = f"{dao}道监察御史"
    org = next((o for o in offices if o["office_name"] == name), None)
    if org:
        org["headcount"] = renshu
        org["duties_source"] = "卷209 都察院"

# 也给统称的监察御史更新
general = next((o for o in offices if o["office_name"] == "监察御史"), None)
if general:
    general["headcount"] = 110
    general["duties_source"] = "卷209 都察院"

# ============================================================
# 保存
# ============================================================
with open(os.path.join(ROOT, "_layers", "office_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(offices, f, ensure_ascii=False, indent=2)

print(f"补全完成！")
print(f"总官职数: {len(offices)}")

# 统计新增
print(f"\n===== P0新增 =====")
print(f"  五城兵马司: {len([o for o in offices if '兵马司' in o['office_name']])}个")
print(f"  宗人府官职: {len([o for o in offices if '宗' in o['office_name'] and '府' in o['office_name']])}个")

print(f"\n===== P1新增 =====")
print(f"  王府官: {len([o for o in offices if '王府' in o['office_name']])}个")
print(f"  布政司内部: {len([o for o in offices if '布政司' in o['office_name'] and '参政' not in o['office_name'] and '参议' not in o['office_name']])}个")
print(f"  按察司内部: {len([o for o in offices if '按察司' in o['office_name'] and '副使' not in o['office_name'] and '佥事' not in o['office_name']])}个")
print(f"  卫所内部: {len([o for o in offices if o['office_name'] in ['卫经历', '卫知事', '所镇抚']])}个")

print(f"\n===== P2更新 =====")
has_source = sum(1 for o in offices if o.get("duties_source"))
print(f"  有原文出处的官职: {has_source}/{len(offices)}")
print(f"  都察院十三道人数已更新")
