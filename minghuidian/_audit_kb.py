# -*- coding: utf-8 -*-
"""全面检查知识库缺口"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))

print("=" * 80)
print("《明会典》知识库现状审计")
print("=" * 80)

# 1. 官职主档层
offices = json.load(open(os.path.join(ROOT, "_layers", "office_profiles.json"), encoding="utf-8"))
print(f"\n【1. 官职主档层 office_profiles.json】")
print(f"  总数: {len(offices)}个")

# 按系统统计
sys_count = {}
for o in offices:
    s = o.get("system", "未知")
    sys_count[s] = sys_count.get(s, 0) + 1
print(f"  系统分布:")
for s, cnt in sorted(sys_count.items(), key=lambda x: -x[1]):
    print(f"    - {s}: {cnt}个")

# 按类型统计
type_count = {}
for o in offices:
    t = o.get("type", "未知")
    type_count[t] = type_count.get(t, 0) + 1
print(f"  类型分布:")
for t, cnt in sorted(type_count.items(), key=lambda x: -x[1]):
    print(f"    - {t}: {cnt}个")

# 字段完整度
fields = ["office_name", "rank", "type", "system", "headcount", "duties", "parent_org", "location"]
print(f"  字段完整度:")
for f in fields:
    has = sum(1 for o in offices if o.get(f) not in [None, "", 0])
    print(f"    - {f}: {has}/{len(offices)} ({has*100//len(offices)}%)")

# 2. 部门主档层
orgs = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))
print(f"\n【2. 部门主档层 org_profiles.json】")
print(f"  总数: {len(orgs)}个")

# 3. 地理主档层
geo_path = os.path.join(ROOT, "_layers", "geo_profiles.json")
if os.path.exists(geo_path):
    geo = json.load(open(geo_path, encoding="utf-8"))
    print(f"\n【3. 地理主档层 geo_profiles.json】")
    print(f"  总数: {len(geo)}条")

# 4. 流程主档层
proc_path = os.path.join(ROOT, "_layers", "process_profiles.json")
if os.path.exists(proc_path):
    procs = json.load(open(proc_path, encoding="utf-8"))
    print(f"\n【4. 流程主档层 process_profiles.json】")
    print(f"  总数: {len(procs)}条")

# 5. 人物主档层
person_path = os.path.join(ROOT, "_layers", "person_profiles.json")
if os.path.exists(person_path):
    persons = json.load(open(person_path, encoding="utf-8"))
    print(f"\n【5. 人物主档层 person_profiles.json】")
    print(f"  总数: {len(persons)}条")

# 6. 底座
registry = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
print(f"\n【6. 底座条目指纹库】")
print(f"  总数: {len(registry)}条")

print(f"\n{'=' * 80}")
print("【还能补什么？】")
print("=" * 80)

gaps = [
    ("P0 - 五城兵马司", "北京/南京的治安机构，约10个官职", "治安/捕盗"),
    ("P0 - 宗人府详细官职", "现在只有宗人府机构名，缺具体官员", "皇室事务"),
    ("P1 - 陵海卫所具体官员", "现在只有卫指挥使层级，缺下面的经历司等", "军事"),
    ("P1 - 王府官", "亲王/郡王王府的官属（长史/审理等）", "王府"),
    ("P1 - 承宣布政使司内部官职", "现在只有布政使，缺经历/照磨/理问等", "地方"),
    ("P2 - 都察院十三道具体人数", "现在只有统称，缺每道具体几个人", "监察"),
    ("P2 - 每个官职的沿革", "现在只有备注，缺按年数组的history", "沿革"),
    ("P2 - 每个职责的原文出处", "现在duties没有xxx_source溯源", "溯源"),
    ("P3 - 人物主档层", "现在几乎是空的，缺具体人物", "人物"),
    ("P3 - 跨层整合", "部门→官职→地理→流程的关联还没做", "整合"),
]

for i, (name, desc, category) in enumerate(gaps, 1):
    print(f"\n  {i}. {name}")
    print(f"     说明: {desc}")
    print(f"     类别: {category}")

print(f"\n{'=' * 80}")
