# -*- coding: utf-8 -*-
"""实用性检验：用户的查询场景，现有数据能否回答"""
import json, os
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

layers = {}
for layer in ["rules", "nams", "ents", "cits", "laws", "rituals", "geo", "org_events", "offices", "materials", "inspect", "dress", "foreign"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        layers[layer] = json.load(open(p, encoding="utf-8"))
    else:
        layers[layer] = []

layers["ents"] = [e for e in layers["ents"] if not e.get("item_id", "").startswith("VIRT")]

print("=" * 80)
print("实用性检验：用户的查询场景 vs 现有数据能力")
print("=" * 80)

# 以「吏部」为例，测试各个查询维度
print("\n【查询示例：吏部】")
print("-" * 60)

# 1. 上级/下级/平级部门
print("\n1. 组织架构（上级/下级/平级）")
print("   现有数据：")
ents = layers["ents"]
org_events = layers["org_events"]

# 找吏部相关的实体
libu_ents = [e for e in ents if "吏部" in e.get("text", "")]
print(f"   - ents层含'吏部'的实体: {len(libu_ents)}条")
if libu_ents:
    for e in libu_ents[:3]:
        print(f"     - {e.get('text')} (type={e.get('type')}, parent_id={e.get('parent_id', '无')})")

# 父子节点
has_parent = [e for e in ents if e.get("parent_id")]
print(f"   - 有parent_id的实体: {len(has_parent)}条 / {len(ents)}条 ({len(has_parent)*100//len(ents)}%)")
print(f"   → 能否回答'上级/下级': ❌ 基本不能，父子关系覆盖率仅1.6%")

# 2. 主管、人数、官职
print("\n2. 人员配置（主管/人数/官职）")
offices = layers["offices"]
libu_offices = [o for o in offices if "吏" in o.get("office_name", "") or "文选" in o.get("office_name", "")]
print(f"   - offices层含吏部相关官职: {len(libu_offices)}条")
if libu_offices:
    for o in libu_offices[:5]:
        print(f"     - {o.get('office_name')}")
print(f"   → 能否回答'主管是谁': 🟡 有官职名，但没有'人数配置'字段")
print(f"   → 能否回答'编制人数': ❌ 没有人员配置数")

# 3. 沿革、薪酬、任务
print("\n3. 职能信息（沿革/薪酬/任务）")
print(f"   - org_events机构沿革: {len(org_events)}条")
libu_org = [o for o in org_events if "吏" in o.get("org_name", "")]
print(f"     - 吏部相关沿革: {len(libu_org)}条")
print(f"   → 能否回答'部门沿革': 🟡 有42条，但吏部相关很少")
print(f"   → 能否回答'薪酬': ❌ 没有专门的薪酬层")
print(f"   → 能否回答'任务职责': 🟡 rules层有规则，但不是专门的职能描述")

# 4. 区域（中央/地方）、品级
print("\n4. 属性信息（区域/品级）")
print(f"   → 能否回答'中央/地方': ❌ 实体没有这个字段")
print(f"   → 能否回答'品级': ❌ 实体没有品级字段")

# 5. 其他可查询维度
print("\n5. 还能怎么查询？")
print(f"   ✅ 能查：这个部门有哪些规则条文（rules层）")
print(f"   ✅ 能查：这个部门有哪些名录（nams层）")
print(f"   ✅ 能查：这个部门涉及哪些地理（geo层）")
print(f"   ✅ 能查：这个部门涉及哪些法律（laws层）")
print(f"   ✅ 能查：这个部门涉及哪些礼仪（rituals层）")

print(f"\n{'='*80}")
print(f"总结：哪些能回答，哪些不能")
print(f"{'='*80}")

capabilities = [
    ("上级/下级/平级部门", "❌ 不能", "父子节点覆盖率仅1.6%，层级关系没建"),
    ("主管官职", "🟡 部分", "有官职名，但不完整"),
    ("编制人数", "❌ 不能", "没有人员配置数字段"),
    ("部门沿革", "🟡 部分", "org_events仅42条，太少"),
    ("薪酬待遇", "❌ 不能", "没有专门的薪酬层"),
    ("任务职责", "🟡 部分", "rules层有规则，但不是职能描述"),
    ("中央/地方", "❌ 不能", "实体没有这个字段"),
    ("品级", "❌ 不能", "实体没有品级字段"),
]

print(f"{'查询维度':20s} {'能否回答':10s} {'原因'}")
print("-" * 70)
for q, can, reason in capabilities:
    print(f"{q:20s} {can:10s} {reason}")
