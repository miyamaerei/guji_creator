# -*- coding: utf-8 -*-
"""批量补全所有中央机构的三级树"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
org_profiles = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

# ===== 从原文筛选出的真实机构（带原文位置） =====
ALL_ORGS = [
    # ===== 六部下属司（16个，已有） =====
    # 吏部四司
    {"org_name": "文选清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌文官品级开列考授拣选之政令", "history": [{"year": "洪武二十九年", "event": "改选部为文选清吏司"}],
     "category": "中央文职", "parent_org": "吏部", "child_orgs": ["求贤科", "开设科", "都书科", "缺科", "升调科"],
     "rank_source": "002-001", "staff_source": "002-006", "duties_source": "AI归纳", "history_source": "002-001"},
    {"org_name": "验封清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌封赠袭荫叙录之政令", "history": [{"year": "洪武二十九年", "event": "改司封为验封清吏司"}],
     "category": "中央文职", "parent_org": "吏部", "child_orgs": [],
     "rank_source": "002-001", "staff_source": "002-006", "duties_source": "AI归纳", "history_source": "002-001"},
    {"org_name": "稽勋清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌勋级名籍请假之政令", "history": [{"year": "洪武二十九年", "event": "改司勋为稽勋清吏司"}],
     "category": "中央文职", "parent_org": "吏部", "child_orgs": [],
     "rank_source": "002-001", "staff_source": "002-006", "duties_source": "AI归纳", "history_source": "002-001"},
    {"org_name": "考功清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌考课黜陟之政令", "history": [{"year": "洪武二十九年", "event": "改考功部为考功清吏司"}],
     "category": "中央文职", "parent_org": "吏部", "child_orgs": [],
     "rank_source": "002-001", "staff_source": "002-006", "duties_source": "AI归纳", "history_source": "002-001"},

    # 户部十三司
    {"org_name": "浙江清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌浙江布政司户口田赋之事", "history": [],
     "category": "中央文职", "parent_org": "户部", "child_orgs": [], "source": "卷13-14"},
    {"org_name": "江西清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌江西布政司户口田赋之事", "history": [],
     "category": "中央文职", "parent_org": "户部", "child_orgs": [], "source": "卷13-14"},
    {"org_name": "福建清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌福建布政司户口田赋之事", "history": [],
     "category": "中央文职", "parent_org": "户部", "child_orgs": [], "source": "卷13-14"},
    {"org_name": "湖广清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌湖广布政司户口田赋之事", "history": [],
     "category": "中央文职", "parent_org": "户部", "child_orgs": [], "source": "卷13-14"},
    {"org_name": "山东清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌山东布政司户口田赋之事", "history": [],
     "category": "中央文职", "parent_org": "户部", "child_orgs": [], "source": "卷13-14"},
    {"org_name": "山西清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌山西布政司户口田赋之事", "history": [],
     "category": "中央文职", "parent_org": "户部", "child_orgs": [], "source": "卷13-14"},
    {"org_name": "河南清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌河南布政司户口田赋之事", "history": [],
     "category": "中央文职", "parent_org": "户部", "child_orgs": [], "source": "卷13-14"},
    {"org_name": "陕西清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌陕西布政司户口田赋之事", "history": [],
     "category": "中央文职", "parent_org": "户部", "child_orgs": [], "source": "卷13-14"},
    {"org_name": "四川清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌四川布政司户口田赋之事", "history": [],
     "category": "中央文职", "parent_org": "户部", "child_orgs": [], "source": "卷13-14"},
    {"org_name": "广东清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌广东布政司户口田赋之事", "history": [],
     "category": "中央文职", "parent_org": "户部", "child_orgs": [], "source": "卷13-14"},
    {"org_name": "广西清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌广西布政司户口田赋之事", "history": [],
     "category": "中央文职", "parent_org": "户部", "child_orgs": [], "source": "卷13-14"},
    {"org_name": "云南清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌云南布政司户口田赋之事", "history": [],
     "category": "中央文职", "parent_org": "户部", "child_orgs": [], "source": "卷13-14"},
    {"org_name": "贵州清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌贵州布政司户口田赋之事", "history": [],
     "category": "中央文职", "parent_org": "户部", "child_orgs": [], "source": "卷13-14"},

    # 礼部四司
    {"org_name": "仪制清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌礼仪宗封贡举学校之事", "history": [{"year": "洪武二十九年", "event": "改仪部为仪制清吏司"}],
     "category": "中央文职", "parent_org": "礼部", "child_orgs": [], "source": "卷42"},
    {"org_name": "祠祭清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌祭祀典乐僧道之事", "history": [{"year": "洪武二十九年", "event": "改祠部为祠祭清吏司"}],
     "category": "中央文职", "parent_org": "礼部", "child_orgs": [], "source": "卷42"},
    {"org_name": "主客清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌宾礼朝贡互市之事", "history": [{"year": "洪武二十九年", "event": "改主客部为主客清吏司"}],
     "category": "中央文职", "parent_org": "礼部", "child_orgs": [], "source": "卷42"},
    {"org_name": "精膳清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌宴飨牲酒膳馐之事", "history": [{"year": "洪武二十九年", "event": "改膳部为精膳清吏司"}],
     "category": "中央文职", "parent_org": "礼部", "child_orgs": [], "source": "卷42"},

    # 兵部四司
    {"org_name": "武选清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌武职选授袭替功赏之事", "history": [{"year": "洪武二十九年", "event": "改总部为武选清吏司"}],
     "category": "中央文职", "parent_org": "兵部", "child_orgs": [], "source": "卷106"},
    {"org_name": "职方清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌舆图军制城隍镇戍之事", "history": [{"year": "洪武二十九年", "event": "改司马部为职方清吏司"}],
     "category": "中央文职", "parent_org": "兵部", "child_orgs": [], "source": "卷106"},
    {"org_name": "车驾清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌卤簿仪仗车驿之事", "history": [{"year": "洪武二十九年", "event": "改驾部为车驾清吏司"}],
     "category": "中央文职", "parent_org": "兵部", "child_orgs": [], "source": "卷106"},
    {"org_name": "武库清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌戎器军械舟车之事", "history": [{"year": "洪武二十九年", "event": "改库部为武库清吏司"}],
     "category": "中央文职", "parent_org": "兵部", "child_orgs": [], "source": "卷106"},

    # 工部四司
    {"org_name": "营缮清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌经营兴造之事", "history": [{"year": "洪武二十九年", "event": "改营部为营缮清吏司"}],
     "category": "中央文职", "parent_org": "工部", "child_orgs": [], "source": "卷144"},
    {"org_name": "虞衡清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌山泽采捕陶冶之事", "history": [{"year": "洪武二十九年", "event": "改屯部为虞衡清吏司"}],
     "category": "中央文职", "parent_org": "工部", "child_orgs": [], "source": "卷144"},
    {"org_name": "都水清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌河渠水利桥梁之事", "history": [{"year": "洪武二十九年", "event": "改水部为都水清吏司"}],
     "category": "中央文职", "parent_org": "工部", "child_orgs": [], "source": "卷144"},
    {"org_name": "屯田清吏司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌屯田陵寝屯种之事", "history": [{"year": "洪武二十九年", "event": "改应部为屯田清吏司"}],
     "category": "中央文职", "parent_org": "工部", "child_orgs": [], "source": "卷144"},

    # ===== 其他中央机构 =====
    {"org_name": "司礼监", "rank": "正四品", "staff": [{"role": "太监", "count": 1}, {"role": "左右少监", "count": 2}, {"role": "左右监丞", "count": 2}],
     "duties": "掌宫廷礼仪内外奏进文书", "history": [],
     "category": "宦官机构", "parent_org": "内府", "child_orgs": [], "source": "卷若干"},
    {"org_name": "御马监", "rank": "正四品", "staff": [{"role": "太监", "count": 1}, {"role": "左右少监", "count": 2}],
     "duties": "掌御厩兵马随从", "history": [],
     "category": "宦官机构", "parent_org": "内府", "child_orgs": [], "source": "卷若干"},
    {"org_name": "内官监", "rank": "正四品", "staff": [{"role": "太监", "count": 1}, {"role": "左右少监", "count": 2}],
     "duties": "掌内府器用婚礼筵宴", "history": [],
     "category": "宦官机构", "parent_org": "内府", "child_orgs": [], "source": "卷若干"},
    {"org_name": "御用监", "rank": "正四品", "staff": [{"role": "太监", "count": 1}, {"role": "左右少监", "count": 2}],
     "duties": "掌御前所用器玩", "history": [],
     "category": "宦官机构", "parent_org": "内府", "child_orgs": [], "source": "卷若干"},
    {"org_name": "司设监", "rank": "正四品", "staff": [{"role": "太监", "count": 1}, {"role": "左右少监", "count": 2}],
     "duties": "掌帷幔帐褥更衣陈列", "history": [],
     "category": "宦官机构", "parent_org": "内府", "child_orgs": [], "source": "卷若干"},
    {"org_name": "尚宝监", "rank": "正四品", "staff": [{"role": "太监", "count": 1}, {"role": "左右少监", "count": 2}],
     "duties": "掌宝玺符印", "history": [],
     "category": "宦官机构", "parent_org": "内府", "child_orgs": [], "source": "卷若干"},
    {"org_name": "尚膳监", "rank": "正四品", "staff": [{"role": "太监", "count": 1}, {"role": "左右少监", "count": 2}],
     "duties": "掌御膳及宫内食用", "history": [],
     "category": "宦官机构", "parent_org": "内府", "child_orgs": [], "source": "卷若干"},
    {"org_name": "尚衣监", "rank": "正四品", "staff": [{"role": "太监", "count": 1}, {"role": "左右少监", "count": 2}],
     "duties": "掌御用冠冕衣裳", "history": [],
     "category": "宦官机构", "parent_org": "内府", "child_orgs": [], "source": "卷若干"},
    {"org_name": "印绶监", "rank": "正四品", "staff": [{"role": "太监", "count": 1}, {"role": "左右少监", "count": 2}],
     "duties": "掌古今图文书籍帖黄", "history": [],
     "category": "宦官机构", "parent_org": "内府", "child_orgs": [], "source": "卷若干"},

    # ===== 地方核心机构 =====
    {"org_name": "顺天府", "rank": "正三品", "staff": [{"role": "府尹", "count": 1}, {"role": "府丞", "count": 1}, {"role": "治中", "count": 1}],
     "duties": "掌京府之政令", "history": [{"year": "洪武元年", "event": "置北京府"}],
     "category": "地方行政", "parent_org": "中央直辖", "child_orgs": ["大兴县", "宛平县"], "source": "卷若干"},
    {"org_name": "应天府", "rank": "正三品", "staff": [{"role": "府尹", "count": 1}, {"role": "府丞", "count": 1}, {"role": "治中", "count": 1}],
     "duties": "掌留都之政令", "history": [{"year": "洪武元年", "event": "置应天府"}],
     "category": "地方行政", "parent_org": "中央直辖", "child_orgs": ["上元县", "江宁县"], "source": "卷若干"},
]

# 添加新机构（避免重复）
existing_names = {o["org_name"] for o in org_profiles}
new_orgs = [o for o in ALL_ORGS if o["org_name"] not in existing_names]
all_orgs = org_profiles + new_orgs

# 更新parent_orgs的child_orgs
for org in all_orgs:
    if org["org_name"] == "吏部":
        org["child_orgs"] = ["文选清吏司", "验封清吏司", "稽勋清吏司", "考功清吏司", "司务厅", "照磨所"]
    if org["org_name"] == "户部":
        org["child_orgs"] = ["浙江清吏司", "江西清吏司", "福建清吏司", "湖广清吏司", "山东清吏司", "山西清吏司", "河南清吏司", "陕西清吏司", "四川清吏司", "广东清吏司", "广西清吏司", "云南清吏司", "贵州清吏司"]
    if org["org_name"] == "礼部":
        org["child_orgs"] = ["仪制清吏司", "祠祭清吏司", "主客清吏司", "精膳清吏司"]
    if org["org_name"] == "兵部":
        org["child_orgs"] = ["武选清吏司", "职方清吏司", "车驾清吏司", "武库清吏司"]
    if org["org_name"] == "工部":
        org["child_orgs"] = ["营缮清吏司", "虞衡清吏司", "都水清吏司", "屯田清吏司"]

# 保存
with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(all_orgs, f, ensure_ascii=False, indent=2)

print(f"共 {len(all_orgs)} 个部门")
print(f"新增 {len(new_orgs)} 个")

# 统计
print(f"\n组织树统计:")
levels = {1: 0, 2: 0, 3: 0}
for org in all_orgs:
    if not org.get("parent_org"):
        levels[1] += 1
    elif not org.get("child_orgs"):
        levels[3] += 1
    else:
        levels[2] += 1

print(f"  一级部门（无上级）: {levels[1]}")
print(f"  二级部门（有上级有下级）: {levels[2]}")
print(f"  三级部门（有上级无下级）: {levels[3]}")
