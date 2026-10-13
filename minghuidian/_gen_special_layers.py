# -*- coding: utf-8 -*-
"""单开专门层：GEO地理区划 / ORG组织机构沿革 / OFFICIAL官职名录"""
import json, os, re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ===== 1. GEO 地理区划层（承接G2户部的府州县名录） =====
# schema: geo_id / item_id / name / level(省/府/州/县) / parent / original

GEO_LEVELS = {
    "布政司": "省",
    "府": "府",
    "州": "州",
    "县": "县",
    "卫": "卫",
    "千户所": "所",
}

def extract_geo(title, original):
    """从名录条目中提取地理实体"""
    geos = []
    # 匹配 "XX府" "XX州" "XX县" 模式
    # 短行标题（名录类）
    if len(title) < 20 and ("府" in title or "州" in title or "县" in title):
        # 按空格分割多个地名
        parts = re.split(r"[\s　]+", title)
        for p in parts:
            p = p.strip()
            if not p:
                continue
            # 判断级别
            level = None
            for suffix, lv in GEO_LEVELS.items():
                if p.endswith(suffix):
                    level = lv
                    break
            if level:
                geos.append({"name": p, "level": level})
    return geos

# ===== 2. ORG 组织机构沿革层（承接G1吏部的官制沿革） =====
# schema: org_id / item_id / org_name / event_type(设置/改名/罢革/复设) / time / original

ORG_EVENTS = ["置", "设", "改", "罢", "革", "复", "升", "降", "分", "并"]

def extract_org_event(title, original):
    """从沿革条目中提取组织机构事件"""
    events = []
    # 匹配 "国初置XX" "洪武X年改XX为XX" 模式
    if "国初" in original or "洪武" in original or "永乐" in original:
        # 提取衙门名
        orgs = re.findall(r"(置|设|改|罢|革|复|升|降)([^，。；]{2,15})(司|寺|监|府|部|院|局|仓|库|厂)", original)
        for action, name, suffix in orgs:
            events.append({
                "org_name": name + suffix,
                "event_type": action,
            })
    return events

# ===== 3. OFFICIAL 官职名录层（承接G7/G8诸文职/武职名录） =====
# schema: off_id / item_id / office_name / rank / belong_to / original

OFFICE_RANKS = ["正一品", "从一品", "正二品", "从二品", "正三品", "从三品",
                "正四品", "从四品", "正五品", "从五品", "正六品", "从六品",
                "正七品", "从七品", "正八品", "从八品", "正九品", "从九品"]

def extract_office(title, original):
    """从官职名录条目中提取官职"""
    offices = []
    # 短行标题（官职名录）
    if len(title) < 15 and not title.endswith(("府", "州", "县", "卫", "所")):
        # 看起来像官职名
        if any(kw in title for kw in ["大夫", "郎", "御史", "少卿", "寺丞", "主事", "郎中", "员外郎"]):
            offices.append({"name": title.strip()})
    return offices

# ===== 批量提取 =====
geo_records = []
org_records = []
off_records = []

geo_seq = org_seq = off_seq = 0

for iid, item in reg.items():
    vol = int(iid.split("-")[0])
    title = item["title"]
    original = item["original"]

    # G2 户部（卷14-41）：提取地理
    if 14 <= vol <= 41:
        geos = extract_geo(title, original)
        for g in geos:
            geo_seq += 1
            geo_records.append({
                "geo_id": f"GEO-{geo_seq:04d}",
                "item_id": iid,
                "name": g["name"],
                "level": g["level"],
            })

    # G1 吏部（卷2-13）：提取组织机构沿革
    if 2 <= vol <= 13:
        events = extract_org_event(title, original)
        for e in events:
            org_seq += 1
            org_records.append({
                "org_id": f"ORG-{org_seq:04d}",
                "item_id": iid,
                "org_name": e["org_name"],
                "event_type": e["event_type"],
            })

    # G7/G8 诸文职/武职（卷164-180）：提取官职
    if 164 <= vol <= 180:
        offices = extract_office(title, original)
        for o in offices:
            off_seq += 1
            off_records.append({
                "off_id": f"OFF-{off_seq:04d}",
                "item_id": iid,
                "office_name": o["name"],
            })

print("=" * 60)
print("新层提取结果")
print("=" * 60)

print(f"\n【GEO 地理区划层】{len(geo_records)} 条")
if geo_records:
    level_dist = Counter(g["level"] for g in geo_records)
    for lv, c in level_dist.most_common():
        print(f"  {lv}: {c}")

print(f"\n【ORG 组织机构沿革层】{len(org_records)} 条")
if org_records:
    event_dist = Counter(o["event_type"] for o in org_records)
    for ev, c in event_dist.most_common():
        print(f"  {ev}: {c}")

print(f"\n【OFFICIAL 官职名录层】{len(off_records)} 条")

# 保存
for name, data in [("geo", geo_records), ("org_events", org_records), ("offices", off_records)]:
    outpath = os.path.join(ROOT, "_layers", f"{name}.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"已保存: {outpath}")
