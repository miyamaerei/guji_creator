# -*- coding: utf-8 -*-
"""P2.5-B: 卫所→府/州/县 挂靠「去伪」。

旧版仅按名称匹配（卫所多以驻地府县为名），会把跨省的同名地名错配
（如 浙江都司·金乡卫 → 山东兖州府·金乡县）。

新版引入**省份约束**：卫所的根祖先（都司/留守司）与候选地名的根祖先（布政司/直隶）
须属同一省区，方可挂靠；跨省同名一律弃权（宁缺勿滥）。输出分两档：
  match="prov+name" 高置信（省+名双匹配）
  match="name"      低置信（无省可约束，如京卫/亲军卫，仅名匹配）
"""
import json, re
from collections import defaultdict

geo = json.load(open("_layers/geo.json", encoding="utf-8"))
DIRS = "左右前后中"
VAR = str.maketrans("蘓呉髙徳寳峯鎭鳯頴澂栁亰衞廵闗畨邉槀", "苏吴高德宝峰镇凤颍澄柳京卫巡关番边藁")


def nv(s):
    return s.translate(VAR)

# 幂等：清空上一次的驻防挂载
for g in geo:
    g["garrisons"] = []
    g.pop("stationed_at", None)
    g.pop("stationed_at_id", None)

by_id = {g["geo_id"]: g for g in geo}


def root_name(g):
    cur, seen = g, set()
    while cur.get("parent_id") and cur["parent_id"] in by_id and cur["geo_id"] not in seen:
        seen.add(cur["geo_id"])
        cur = by_id[cur["parent_id"]]
    return cur["name"]


def prov_of(name):
    """根祖先名 → 省区标签。"""
    SPECIAL = {"北平都司": "北直隶", "大宁都司": "北直隶", "万全都司": "北直隶",
               "中都留守司": "南直隶", "辽东都司": "辽东",
               "亲军卫": None, "南京": "南直隶", "五军都督府": None}
    if name in SPECIAL:
        return SPECIAL[name]
    if name.endswith("都督府"):          # 中军/左军/…都督府（京卫、南京卫混杂）→ 不约束
        return None
    for suf in ("都指挥使司", "行都司", "都司", "布政使司", "布政司"):
        if name.endswith(suf):
            return name[:-len(suf)]
    if name in ("北直隶", "南直隶"):
        return name
    return nv(name)


places = [g for g in geo if g["type"] in ("府", "州", "县")]
wei = [g for g in geo if g["type"] in ("卫", "所", "护卫")]

# 候选索引：base(去后缀/去方位, 归一 OCR 变体) -> [place]；并记录 place 的省
idx = defaultdict(list)
for g in places:
    idx[nv(g["name"][:-1])].append(g)
PRI = {"府": 0, "州": 1, "县": 2}


def base_of(name):
    for suf in ("守御千户所", "千户所", "百户所", "护卫", "卫"):
        if name.endswith(suf):
            b = name[:-len(suf)]
            break
    else:
        return None
    while b and b[-1] in DIRS:      # 杭州右卫 -> 杭州
        b = b[:-1]
    return nv(b) or None


links = []
dropped_cross = []
for w in wei:
    b = base_of(w["name"])
    if not b:
        continue
    cands = idx.get(b)
    if not cands:
        continue
    wprov = prov_of(root_name(w))
    # 省份约束：卫所有省可定 → 只留同省候选；否则保留全部（低置信）
    if wprov:
        same = [c for c in cands if prov_of(root_name(c)) == wprov]
        if not same:
            dropped_cross.append((w["name"], wprov, [c["name"] for c in cands]))
            continue
        pool, conf = same, "prov+name"
    else:
        pool, conf = cands, "name"
    tgt = sorted(pool, key=lambda x: PRI[x["type"]])[0]   # 府 > 州 > 县
    links.append({"place_id": tgt["geo_id"], "place": tgt["name"], "place_type": tgt["type"],
                  "garrison_id": w["geo_id"], "garrison": w["name"],
                  "garrison_type": w["type"], "match": conf})
    tgt.setdefault("garrisons", [])
    if w["name"] not in tgt["garrisons"]:
        tgt["garrisons"].append(w["name"])
    w["stationed_at"] = tgt["name"]
    w["stationed_at_id"] = tgt["geo_id"]

json.dump(geo, open("_layers/geo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(links, open("_layers/geo_station.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump([{"garrison": a, "prov": b, "same_name_places": c} for a, b, c in dropped_cross],
          open("_layers/geo_station_dropped.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

n_place = sum(1 for g in places if g.get("garrisons"))
print(f"卫所 {len(wei)}，挂靠 {len(links)} = {len(links)/len(wei)*100:.1f}%")
print(f"  高置信 prov+name: {sum(1 for x in links if x['match']=='prov+name')}")
print(f"  低置信 name     : {sum(1 for x in links if x['match']=='name')}")
print(f"  跨省同名弃权     : {len(dropped_cross)}")
print(f"获驻防记录的府/州/县：{n_place}/{len(places)} = {n_place/len(places)*100:.1f}%")
for t in ("府", "州", "县"):
    c = sum(1 for g in places if g["type"] == t and g.get("garrisons"))
    tot = sum(1 for g in places if g["type"] == t)
    print(f"  {t}: {c}/{tot} 有驻防")
print("跨省弃权示例:")
for x in dropped_cross[:12]:
    print(f"  {x[0]}({x[1]}) ✗ {x[2]}")
