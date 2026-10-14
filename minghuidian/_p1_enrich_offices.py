# -*- coding: utf-8 -*-
"""P1-C 补 office_profiles 的沿革 / 属官 / 职责出处（v2，含消歧）

现状：566 个官职中 history 仅 4 条、child_offices 73 条、duties_source 198 条。

关键改进（相比 v1）：
  - 消歧：官职名若被更长的官职名「包含」（如 太师 ⊂ 太子太师），该处出现不计，
    避免「太师」误捡「太子太师」的句子。
  - 邻近性：官职名与沿革动词需相邻（≤25 字）。
  - history 统一为 {era, event, detail, item_id}，并保留/转换既有条目。
"""
import json, os, re, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
LAY = os.path.join(ROOT, "_layers")

ERA = re.compile(r"(洪武|永乐|洪熙|洪熈|宣德|宣徳|正统|景泰|天顺|成化|弘治|正德|嘉靖|隆庆|万历|万厯)([元一二三四五六七八九十百零]{0,5}年)?")
EVENT = re.compile(r"(设立|添设|废|置|设|改|罢|革|复|增|减|裁|并|升|降)")
ERA_CANON = {"洪熈": "洪熙", "宣徳": "宣德", "万厯": "万历"}
RANK_MAP = {"正一品": 1, "从一品": 2, "正二品": 3, "从二品": 4, "正三品": 5, "从三品": 6,
            "正四品": 7, "从四品": 8, "正五品": 9, "从五品": 10, "正六品": 11, "从六品": 12,
            "正七品": 13, "从七品": 14, "正八品": 15, "从八品": 16, "正九品": 17, "从九品": 18,
            "未入流": 19, "无品级": 99}


def rank_val(r):
    return RANK_MAP.get(r.strip(), 99) if isinstance(r, str) else 99


def split_clauses(t):
    return [c for c in re.split(r"[。；;]", t or "") if c.strip()]


def main():
    reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
    offices = json.load(open(os.path.join(LAY, "office_profiles.json"), encoding="utf-8"))
    all_names = sorted({x.get("office_name") for x in offices if x.get("office_name")}, key=len, reverse=True)
    name_set = set(all_names)
    # 以 name 结尾的更长官职名
    ends_with = collections.defaultdict(list)
    for o in all_names:
        for nm in all_names:
            if o != nm and o.endswith(nm):
                ends_with[nm].append(o)

    hist_items = [(k, v.get("original", "")) for k, v in reg.items()
                  if v.get("original") and EVENT.search(v["original"])
                  and (ERA.search(v["original"]) or "国初" in v["original"])]
    duty_items = [(k, v.get("original", "")) for k, v in reg.items() if "掌" in v.get("original", "")]
    # 衙门沿革索引（用于官职继承所属衙门的沿革）
    org_hist = {}
    for op in json.load(open(os.path.join(LAY, "org_profiles.json"), encoding="utf-8")):
        if op.get("history"):
            org_hist[op.get("org_name")] = op["history"]

    for o in offices:
        name = o.get("office_name", "")
        if not name:
            continue
        # --- 归一既有 history 格式 ---
        hist = []
        for h in o.get("history", []):
            if isinstance(h, dict):
                if "era" in h:
                    hist.append(h)
                elif "year" in h:
                    hist.append({"era": h.get("year", ""), "event": h.get("event", ""),
                                 "detail": "", "item_id": ""})
        # --- 抽取 ---
        for k, t in hist_items:
            if name not in t:
                continue
            for cl in split_clauses(t):
                p = cl.find(name)
                if p < 0:
                    continue
                # 消歧：该处被更长官职名包含则跳过
                if any(cl[:p + len(name)].endswith(o2) for o2 in ends_with.get(name, [])):
                    continue
                ev = EVENT.search(cl)
                if not ev or abs(p - ev.start()) > 15:
                    continue
                m = ERA.search(cl)
                era = ""
                if m:
                    era = ERA_CANON.get(m.group(1), m.group(1)) + (m.group(2) or "")
                elif "国初" in cl:
                    era = "国初"
                if not era:
                    continue
                hist.append({"era": era, "event": ev.group(1), "detail": cl[:80], "item_id": k})
        seen = set()
        uniq = []
        for h in hist:
            key = (h["era"], h["event"], h["detail"][:16])
            if key in seen:
                continue
            seen.add(key)
            uniq.append(h)
        if uniq:
            o["history"] = uniq[:12]
        # --- duties_source ---
        if o.get("duties") and not o.get("duties_source"):
            core = o["duties"][:12]
            for k, t in duty_items:
                if core and core in t:
                    o["duties_source"] = k
                    break
        # --- child_offices：同衙门内品级更低的官职 ---
        if not o.get("child_offices"):
            org = o.get("parent_org", "")
            if org:
                lower = sorted({x.get("office_name") for x in offices
                                if x.get("parent_org") == org and x.get("office_name") != name
                                and rank_val(x.get("rank")) > rank_val(o.get("rank"))})
                if lower:
                    o["child_offices"] = lower[:15]
        # --- org_name / org_history：由官职名反查所属衙门（官职名含衙门名）---
        org_names = sorted(org_hist.keys(), key=len, reverse=True)
        hit = next((g for g in org_names if g in name), None)
        if hit:
            o["org_name"] = hit
            o["org_history"] = org_hist[hit]
            o["org_history_source"] = hit

    json.dump(offices, open(os.path.join(LAY, "office_profiles.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    n = len(offices)
    for k in ["history", "duties_source", "child_offices"]:
        c = sum(1 for x in offices if x.get(k))
        print("  %-14s %4d/%d (%.0f%%)" % (k, c, n, 100 * c / n))


if __name__ == "__main__":
    main()
