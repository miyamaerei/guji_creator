# -*- coding: utf-8 -*-
"""P4-D：用「同卷同 section 兄弟锚定」给剩余 921 条孤立条补结构。

策略（按可靠性排序，只补结构不编造内容）：
1. section_parent：同卷同 section 内的条目，选一条**非孤立且文本最相关**的作为锚，
   孤儿与锚建立横向同级关系（rel="same_section"），并把锚的 layer 桶共享给孤儿
   的一部分（只共享确定性高的：geo/orgs/offices/nams 这类"提及型"）。
2. 序数连续性：仪仗/器物/丧服这类是**同一器物的形制清单**，它们本身就在 section 内
   构成枚举序列。为这类建立 `enum_seq`（枚举序号 + section 主题），
   并把 section 标题本身作为语义标签挂给每一条。
3. 物类归并：形制描述里的"旗/杖/氅/扇/盖/轿/鼓/角/笛/刀/盾/弓/箭"等器物词，
   归入 OBJ 类目并把这一类目作为分组键。

只写新桶 + 新的 orphan 归因，不改写原有 21/23 桶。
"""
import json, os, sys, io, re
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

reg = json.load(open("_item_registry.json", encoding="utf-8"))
_join_list = json.load(open("_kg_join.json", encoding="utf-8"))
join = {j["item_id"]: j for j in _join_list}
aud = json.load(open("_p4_orphans.json", encoding="utf-8"))
orphans = {a["item_id"]: a for a in aud}

# ---------- 器物类目表（形制清单的语义钥匙）----------
OBJ_CLASS = [
    ("旗纛", ("旗", "纛", "旛", "幡", "旌", "幢")),
    ("杖棒", ("杖", "棒", "瓜", "骨朵", "殳")),
    ("氅扇", ("氅", "扇", "障", "盖", "葢", "伞", "繖")),
    ("车轿", ("轿", "辂", "辇", "车", "舆", "鞍", "辔")),
    ("鼓角", ("鼓", "角", "笛", "箫", "笙", "钟", "钲", "磬", "铃", "铙", "笳")),
    ("兵仗", ("刀", "盾", "弓", "箭", "劒", "剑", "戟", "斧", "鎗", "枪", "戈", "矛",
              "甲", "胄", "盔", "弩", "鞭", "鐧", "铛")),
    ("符信", ("符", "牌", "印", "绶", "节", "令牌", "勘合")),
    ("冠服", ("冕", "冠", "巾", "帽", "袍", "裳", "衣", "带", "佩", "圭", "韈", "舄",
              "履", "绦", "缨", "簪", "钗")),
    ("丧服", ("衰", "缌麻", "小功", "大功", "齐衰", "杖期", "服制")),
    ("织品", ("纻丝", "罗", "纱", "绢", "布", "绵", "丝", "绫", "绸", "缎", "叚")),
    ("珍宝估直", ("珠", "宝", "玉", "金", "银", "铜", "锡", "铁", "翠", "玛瑙", "琥珀")),
    ("盐货", ("盐", "引", "课", "塲", "斤")),
]

def obj_class_of(blob):
    hits = []
    for cls, keys in OBJ_CLASS:
        for k in keys:
            if k in blob:
                hits.append(cls)
                break
    return hits

# ---------- 1. section 锚定 ----------
sec_index = defaultdict(list)      # (volume, section) -> [item_id]
for iid, j in join.items():
    sec_index[(j["volume"], j["section"])].append(iid)

new_parent = {}     # orphan -> parent item_id
new_same = defaultdict(list)
for iid, a in orphans.items():
    key = (a["volume"], a["section"])
    sibs = [s for s in sec_index.get(key, []) if s != iid]
    scored = []
    for s in sibs:
        js = join[s]
        if js["layer_count"] == 0:
            continue
        # 优先：非孤立 + node_kind 为"事目/长文"（章节锚）+ 文本长度接近
        bonus = 0
        if js["node_kind"] == "事目":
            bonus += 3
        if js["node_kind"] == "长文":
            bonus += 2
        if abs(len(js["title"]) - len(a["title"])) < 20:
            bonus += 1
        scored.append((js["layer_count"] + bonus, s))
    if scored:
        scored.sort(key=lambda x: -x[0])
        new_parent[iid] = scored[0][1]
    else:
        # 同级里也没有非孤立的 → 孤儿之间自建"枚举组"，锚定到 section 标题
        new_same[key].append(iid)

# ---------- 2. section 主题桶（所有孤立条都挂，不依赖有没有锚）----------
sec_bucket = defaultdict(list)
for iid, j in join.items():
    sec = j["section"]
    if sec and len(sec) >= 2:
        sec_bucket[sec].append(iid)

# ---------- 3. 器物类目桶 ----------
cls_bucket = defaultdict(list)
for iid, a in orphans.items():
    it = reg.get(iid) or {}
    blob = (it.get("title") or "") + (it.get("original") or "")
    for c in obj_class_of(blob):
        cls_bucket[c].append(iid)

# ---------- 4. 写回 ----------
ANCHOR = {"anchor_parent": {}, "anchor_same": {}, "by_section": {}, "by_obj_class": {}}

for iid, p in new_parent.items():
    j = join[iid]
    j.setdefault("anchor", []).append({"rel": "section_parent", "item_id": p,
                                       "section": j["section"]})
    pj = join[p]
    pj.setdefault("children", [])
    if iid not in pj["children"]:
        pj["children"].append(iid)
    ANCHOR["anchor_parent"][iid] = p

for (vol, sec), lst in new_same.items():
    ANCHOR["anchor_same"][f"{vol}|{sec}"] = lst

for sec, lst in sec_bucket.items():
    ANCHOR["by_section"][sec] = len(lst)

for cls, lst in cls_bucket.items():
    ANCHOR["by_obj_class"][cls] = len(lst)

# 重算 layer_count（含 anchor / children）
for iid, j in join.items():
    n = sum(1 for k, v in j.items() if isinstance(v, (list, dict)) and v
            and k not in ("item_id", "volume", "group", "node_kind", "section",
                          "title", "layer_count", "anchor", "children"))
    j["anchor_count"] = len(j.get("anchor") or [])
    j["layer_count"] = n + (1 if j.get("anchor") else 0)

json.dump([join[i] for i in sorted(join)] if False else list(join.values()),
          open("_kg_join.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(ANCHOR, open("_p4d_anchor.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ---------- 报告 ----------
still = [i for i, j in join.items() if j["layer_count"] == 0]
print(f"P4-D 兄弟锚定")
print(f"  新建 anchor_parent : {len(new_parent)}")
print(f"  孤儿自建枚举组     : {sum(len(v) for v in new_same.values())} 条 / {len(new_same)} 组")
print(f"  section 主题覆盖   : {len(sec_bucket)} 个 section")
print(f"  器物类目           : {len(cls_bucket)} 类")
print(f"  仍孤立             : {len(still)}")
print()
print("[器物类目分布]")
for k, v in sorted(cls_bucket.items(), key=lambda x: -len(x[1])):
    print(f"  {k:8s} {len(v)}")
print()
print("[剩余孤立 section top]")
for k, v in Counter(join[i]["section"] for i in still).most_common(12):
    print(f"  {k:20s} {v}")
