# -*- coding: utf-8 -*-
"""补全所有司的独立条目"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
org_profiles = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

# ===== 六部下属司的标准资料 =====
DEPARTMENT_OFFICES = [
    # 吏部四司
    {"org_name": "文选司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌文官品级开列考授拣选之政令", "history": [{"year": "洪武二十九年", "event": "改选部为文选清吏司"}],
     "category": "中央文职", "parent_org": "吏部", "child_orgs": []},
    {"org_name": "验封司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌封赠袭荫叙录之政令", "history": [{"year": "洪武二十九年", "event": "改司封为验封清吏司"}],
     "category": "中央文职", "parent_org": "吏部", "child_orgs": []},
    {"org_name": "稽勋司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌勋级名籍请假之政令", "history": [{"year": "洪武二十九年", "event": "改司勋为稽勋清吏司"}],
     "category": "中央文职", "parent_org": "吏部", "child_orgs": []},
    {"org_name": "考功司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌考课黜陟之政令", "history": [{"year": "洪武二十九年", "event": "改考功部为考功清吏司"}],
     "category": "中央文职", "parent_org": "吏部", "child_orgs": []},
    # 礼部四司
    {"org_name": "仪制司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌礼仪宗封贡举之政令", "history": [{"year": "洪武二十九年", "event": "改仪部为仪制清吏司"}],
     "category": "中央文职", "parent_org": "礼部", "child_orgs": []},
    {"org_name": "祠祭司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌祭祀典乐僧道之政令", "history": [{"year": "洪武二十九年", "event": "改祠部为祠祭清吏司"}],
     "category": "中央文职", "parent_org": "礼部", "child_orgs": []},
    {"org_name": "主客司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌宾礼朝贡互市之政令", "history": [{"year": "洪武二十九年", "event": "改主客部为主客清吏司"}],
     "category": "中央文职", "parent_org": "礼部", "child_orgs": []},
    {"org_name": "精膳司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌宴飨牲酒膳馐之政令", "history": [{"year": "洪武二十九年", "event": "改膳部为精膳清吏司"}],
     "category": "中央文职", "parent_org": "礼部", "child_orgs": []},
    # 兵部四司
    {"org_name": "武选司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌武职选授袭替功赏之政令", "history": [{"year": "洪武二十九年", "event": "改总部为武选清吏司"}],
     "category": "中央文职", "parent_org": "兵部", "child_orgs": []},
    {"org_name": "职方司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌舆图军制城隍镇戍之政令", "history": [{"year": "洪武二十九年", "event": "改司马部为职方清吏司"}],
     "category": "中央文职", "parent_org": "兵部", "child_orgs": []},
    {"org_name": "车驾司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌卤簿仪仗车驿之政令", "history": [{"year": "洪武二十九年", "event": "改驾部为车驾清吏司"}],
     "category": "中央文职", "parent_org": "兵部", "child_orgs": []},
    {"org_name": "武库司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌戎器军械舟车之政令", "history": [{"year": "洪武二十九年", "event": "改库部为武库清吏司"}],
     "category": "中央文职", "parent_org": "兵部", "child_orgs": []},
    # 工部四司
    {"org_name": "营缮司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌经营兴造之政令", "history": [{"year": "洪武二十九年", "event": "改营部为营缮清吏司"}],
     "category": "中央文职", "parent_org": "工部", "child_orgs": []},
    {"org_name": "虞衡司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌山泽采捕陶冶之政令", "history": [{"year": "洪武二十九年", "event": "改屯部为虞衡清吏司"}],
     "category": "中央文职", "parent_org": "工部", "child_orgs": []},
    {"org_name": "都水司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 2}],
     "duties": "掌河渠水利桥梁之政令", "history": [{"year": "洪武二十九年", "event": "改水部为都水清吏司"}],
     "category": "中央文职", "parent_org": "工部", "child_orgs": []},
    {"org_name": "屯田司", "rank": "正五品", "staff": [{"role": "郎中", "count": 1}, {"role": "员外郎", "count": 1}, {"role": "主事", "count": 1}],
     "duties": "掌屯田陵寝屯种之政令", "history": [{"year": "洪武二十九年", "event": "改应部为屯田清吏司"}],
     "category": "中央文职", "parent_org": "工部", "child_orgs": []},
]

# 添加到org_profiles
all_orgs = org_profiles + DEPARTMENT_OFFICES

# 保存
with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(all_orgs, f, ensure_ascii=False, indent=2)

# 展示文选司
print("=" * 60)
print("文选司资料:")
print("=" * 60)
wenxuan = [o for o in all_orgs if o["org_name"] == "文选司"][0]
print(json.dumps(wenxuan, ensure_ascii=False, indent=2))

print(f"\n\n共 {len(all_orgs)} 个部门（原25 + 新增16个司）")
