# -*- coding: utf-8 -*-
"""P1-B 新建 TIM 制度时间线层（会典最核心的价值：制度因革）

以「事目/制度名」为单位，把同一事目下的 RUL 按年号排成演变链：
  国初 → 洪武 → 永乐 → … → 弘治 → 正德
每条链给出：制度名、所属卷组、演变事件序列（立/改/罢/复/增/减）、
以及对应 rule_id / item_id / 原文摘录，回答「某制度从洪武到弘治如何演变」。
"""
import json, os, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
LAY = os.path.join(ROOT, "_layers")

ERA_ORDER = ["国初", "洪武", "永乐", "洪熙", "宣德", "正统", "景泰", "天顺",
             "成化", "弘治", "正德", "嘉靖", "隆庆", "万历"]

GROUP_RANGES = [("G0", 1, 1), ("G1", 2, 13), ("G2", 14, 41), ("G3", 42, 105),
                ("G4", 106, 129), ("G5", 130, 143), ("G6", 144, 163),
                ("G7", 164, 178), ("G8", 179, 180)]


def group_of(vol):
    for g, a, b in GROUP_RANGES:
        if a <= vol <= b:
            return g
    return "?"


def main():
    rules = json.load(open(os.path.join(LAY, "rules.json"), encoding="utf-8"))
    # 按事目(section)分组
    by_section = collections.defaultdict(list)
    for x in rules:
        sec = x.get("section") or ""
        if not sec:
            continue
        by_section[sec].append(x)

    tim = []
    n = 0
    for sec, rs in by_section.items():
        era_rs = [x for x in rs if x.get("era_first")]
        if not era_rs:
            continue
        # 排序：年号序 → 卷序
        era_rs.sort(key=lambda x: (ERA_ORDER.index(x["era_first"]) if x["era_first"] in ERA_ORDER else 99,
                                   x.get("volume") or 0))
        chain = []
        for x in era_rs:
            chain.append({
                "era": x.get("era_first"),
                "era_raw": x.get("era_raw", []),
                "event_types": x.get("event_types", []),
                "detail": (x.get("action") or "")[:120],
                "rule_id": x.get("id", ""),
                "item_id": x.get("item_id", ""),
                "volume": x.get("volume"),
            })
        vols = sorted({x.get("volume") for x in rs if x.get("volume")})
        groups = sorted({group_of(v) for v in vols})
        n += 1
        tim.append({
            "tim_id": "TIM-%03d" % n,
            "topic": sec,
            "group": groups[0] if len(groups) == 1 else "/".join(groups),
            "volumes": vols,
            "era_span": [chain[0]["era"], chain[-1]["era"]],
            "event_count": len(chain),
            "rule_count": len(rs),
            "era_chain": chain,
        })

    # 按事件数排序（链越长越有价值）
    tim.sort(key=lambda t: (-t["event_count"], t["topic"]))
    for i, t in enumerate(tim):
        t["tim_id"] = "TIM-%03d" % (i + 1)

    json.dump(tim, open(os.path.join(LAY, "tim.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    print("TIM 制度时间线层：%d 条" % len(tim))
    multi = [t for t in tim if t["event_count"] >= 2]
    print("  含 ≥2 个演变节点: %d 条" % len(multi))
    print("  节点总数: %d" % sum(t["event_count"] for t in tim))
    print("\n  最长演变链 Top8：")
    for t in tim[:8]:
        eras = "→".join(c["era"] for c in t["era_chain"][:8])
        print("    [%s] %s (%d节点) %s" % (t["group"], t["topic"], t["event_count"], eras))


if __name__ == "__main__":
    main()
