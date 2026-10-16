# -*- coding: utf-8 -*-
"""build_mytz_remap.py —— 《明一统志》旧→新条目编号重映射表生成器

背景
----
《明一统志》经历「整书重建」后条目编号变更，而 7 个知识层
（`14-mingyitongzhi-knowledge/_layers/{cit,ent,evo,geo,mtn,per,site}/all.json`，
合计 49429 条）是按**旧编号**建的 —— 旧编号存疑于
`14-mingyitongzhi-knowledge/_item_registry.json`（217 键）。

重映射依据（五路，按置信度降序）
--------------------------------
1. `exact`     旧键本身就是新 iid           → 置信度 1.00
2. `title`     旧键 title 在书籍json 唯一命中同名条 → 0.95
3. `title-vol` 同名多条，但同卷唯一命中      → 0.85
4. `geo-name`  title 是占位批次标签（`pers1_名宦`/`t01_忠州`/`w01_景东卫`/`mtns1`），
               但该键在 geo 层有记录，其 `name` 在书籍json 唯一命中 → 0.80
5. `geo-name-vol` 同 4，但同名多条、同卷唯一命中 → 0.70
6. `title-amb` 同名多条且跨卷，同卷无唯一解（取首个）→ 0.40
7. `unmapped`  title 是占位串且 geo 层也给不出名字，或书籍json 中无同名条 → 0.00

产出
----
- `mingyitongzhi-kb/14-mingyitongzhi-knowledge/_item_remap.json`
    {"meta": {...}, "remap": {旧id: {new, title, confidence, method}}, "unmapped": [...]}
- `.../_item_remap.csv`  供人工校订（列：old_id,old_title,new_id,new_title,
   confidence,method,volume_new,region,type,note）
- `.../_item_remap.md`   人读报告（按 method 分组 + 待裁决清单）

用法
----
    python tools/kb-federation/build_mytz_remap.py [--check]

`--check` 只打印统计不落盘。幂等：重复运行结果一致（无随机、无时间戳）。
"""

import argparse
import csv
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))  # guji/

BOOK_ROOT = os.path.join(REPO_ROOT, "mingyitongzhi-kb")
KNOW = os.path.join(BOOK_ROOT, "14-mingyitongzhi-knowledge")
MAIN_JSON = os.path.join(BOOK_ROOT, "书籍json", "明一统志.json")
REGISTRY = os.path.join(KNOW, "_item_registry.json")
OUT_JSON = os.path.join(KNOW, "_item_remap.json")
OUT_CSV = os.path.join(KNOW, "_item_remap.csv")
OUT_MD = os.path.join(KNOW, "_item_remap.md")

LAYERS = ["cit", "ent", "evo", "geo", "mtn", "per", "site"]

# 占位 title 形态：知识层生成期遗留的「批次标签」，不是条目名
PLACEHOLDER_RE = re.compile(r"^(?:pers\d+|t\d+|s\d+|w\d+|geo\d+|mtns?\d*)_")

CONF = {
    "exact": 1.00,
    "title": 0.95,
    "title-vol": 0.85,
    "geo-name": 0.80,
    "geo-name-vol": 0.70,
    "title-amb": 0.40,
    "unmapped": 0.00,
}

METHOD_ORDER = ["exact", "title", "title-vol", "geo-name", "geo-name-vol", "title-amb", "unmapped"]


def load_json(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def iter_iid(rec):
    """一条层记录的 item_id 可能是 str 或 list，统一产出字符串。"""
    v = rec.get("item_id")
    if isinstance(v, list):
        for x in v:
            if x:
                yield str(x)
    elif v:
        yield str(v)


def resolve_by_title(name, by_title, vol_of, old_vol):
    """按名称在书籍json 中定位条目，返回 (method, new_iid) 或 (None, None)。

    唯一命中 → 'title'；同名多条且同卷唯一 → 'title-vol'；
    同名多条且同卷无唯一解 → 'title-amb'（取首个）；无同名 → (None, None)。
    """
    if not name:
        return None, None
    cands = by_title.get(name, [])
    if not cands:
        return None, None
    if len(cands) == 1:
        return "title", cands[0]
    same = [c for c in cands if vol_of.get(c) == old_vol]
    if len(same) == 1:
        return "title-vol", same[0]
    return "title-amb", (same or cands)[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只打印统计，不落盘")
    args = ap.parse_args()

    doc = load_json(MAIN_JSON)
    registry = load_json(REGISTRY)

    # --- 书籍json 侧索引 ---
    title_of = {}
    vol_of = {}
    for v in doc["volumes"]:
        for it in v.get("items") or []:
            iid = it["id"]
            title_of[iid] = it.get("title") or ""
            vol_of[iid] = v["no"]
    book_iids = set(title_of)

    by_title = defaultdict(list)
    for iid, t in title_of.items():
        if t:
            by_title[t].append(iid)
    for t in by_title:
        by_title[t].sort()

    # --- geo 层索引：占位键 → 该键下 geo 记录的 name 序列（按 geo_id 排序） ---
    # 占位键（persN_xxx 等）自身没有可读条目名，但其 geo 层首条
    # 往往就是「该卷所属府」，可反查书籍json 条目。
    geo_by_iid = defaultdict(list)
    geo_path = os.path.join(KNOW, "_layers", "geo", "all.json")
    if os.path.exists(geo_path):
        for g in load_json(geo_path)["records"]:
            iid = g.get("item_id")
            if isinstance(iid, str) and iid:
                geo_by_iid[iid].append(g)
    for iid in geo_by_iid:
        geo_by_iid[iid].sort(key=lambda g: str(g.get("geo_id") or ""))

    def geo_names(iid):
        """该占用键下 geo 记录的候选名称（去重保序），府级优先。"""
        out = []
        for g in geo_by_iid.get(iid, []):
            nm = g.get("name") or ""
            if nm and nm not in out:
                out.append(nm)
        return out

    # --- 建映射 ---
    remap = {}
    for old in sorted(registry):
        meta = registry[old] or {}
        old_title = meta.get("title") or ""
        old_vol = old.split("-")[0]
        method = new = None
        via = ""

        if old in book_iids:
            method, new = "exact", old
        else:
            # 第一路：registry title 直接匹配（也可处理非占位名）
            method, new = resolve_by_title(old_title, by_title, vol_of, old_vol)
            if new:
                via = old_title
            else:
                # 第二路：title 是占位串（或无 title）→ 借 geo 层的 name 反查
                for nm in geo_names(old):
                    m2, n2 = resolve_by_title(nm, by_title, vol_of, old_vol)
                    if n2:
                        # 经 geo 间接定位，置信度降一档
                        method = "geo-name-vol" if m2 == "title-vol" else "geo-name"
                        new, via = n2, nm
                        break

        if not new:
            method = "unmapped"

        remap[old] = {
            "new": new,
            "old_title": old_title,
            "new_title": title_of.get(new, "") if new else "",
            "confidence": CONF[method],
            "method": method,
            "via": via,
            "volume_new": vol_of.get(new) if new else None,
            "volume_old": meta.get("volume"),
            "region": meta.get("region"),
            "type": meta.get("type"),
            "note": (
                "占位 title 且 geo 层无可用名称，无法定位"
                if method == "unmapped" and PLACEHOLDER_RE.match(old_title)
                else ("书籍json 中无同名条目" if method == "unmapped" else "")
            ),
        }

    # --- 层记录的挂载统计 ---
    stats = {}
    for layer in LAYERS:
        p = os.path.join(KNOW, "_layers", layer, "all.json")
        recs = load_json(p)["records"]
        c = Counter()
        for r in recs:
            methods = set()
            for x in iter_iid(r):
                if x in book_iids:
                    methods.add("exact")
                elif x in remap and remap[x]["new"]:
                    methods.add(remap[x]["method"])
                else:
                    methods.add("unmapped")
            # 一条记录只要有一个可用 item_id 就算挂得上，取最优
            for m in METHOD_ORDER:
                if m in methods:
                    c[m] += 1
                    break
        stats[layer] = {"total": len(recs), **c}

    print("=" * 74)
    print("旧→新映射（%d 个 registry 键）" % len(remap))
    mc = Counter(v["method"] for v in remap.values())
    for m in ("exact", "title", "title-vol", "title-amb", "unmapped"):
        if mc[m]:
            print("  %-10s %3d  (置信度 %.2f)" % (m, mc[m], CONF[m]))
    print("  可定位 = %d / %d" % (len(remap) - mc["unmapped"], len(remap)))

    print()
    print("层记录挂载情况（原位优先，其次重映射）")
    tot = avail = 0
    for layer in LAYERS:
        s = stats[layer]
        ok = s["total"] - s.get("unmapped", 0)
        tot += s["total"]
        avail += ok
        print("  %-5s 总 %-6d 可挂 %-6d (%.1f%%)   [exact %d / title %d / vol %d / amb %d]" % (
            layer, s["total"], ok, 100.0 * ok / max(1, s["total"]),
            s.get("exact", 0), s.get("title", 0), s.get("title-vol", 0), s.get("title-amb", 0)))
    print("  合计 %d / %d = %.1f%%" % (avail, tot, 100.0 * avail / max(1, tot)))

    if args.check:
        print("\n[--check] 未落盘")
        return

    # --- 落盘 JSON ---
    payload = {
        "meta": {
            "book": "明一统志",
            "book_id": "myt",
            "source_registry": "_item_registry.json",
            "target": "书籍json/明一统志.json volumes[].items[].id",
            "registry_keys": len(remap),
            "locatable": len(remap) - mc["unmapped"],
            "unmapped": mc["unmapped"],
            "method_counts": {m: mc[m] for m in CONF if mc[m]},
            "confidence": CONF,
            "note": (
                "旧编号系知识层生成期所用；书籍json 经整书重建后编号变更。"
                "重映射只按 title 同名判定，ambiguous 者需人工校订。"
            ),
        },
        "remap": remap,
        "unmapped": sorted(k for k, v in remap.items() if not v["new"]),
    }
    with io.open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print("\n已写 %s" % OUT_JSON)

    # --- 落盘 CSV（供人工校订） ---
    with io.open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "old_id", "old_title", "new_id", "new_title",
            "confidence", "method", "volume_old", "volume_new",
            "region", "type", "note",
        ])
        for old in sorted(remap):
            r = remap[old]
            w.writerow([
                old, r["old_title"], r["new"] or "", r["new_title"],
                "%.2f" % r["confidence"], r["method"],
                r["volume_old"] if r["volume_old"] is not None else "",
                r["volume_new"] or "", r["region"] or "", r["type"] or "", r["note"],
            ])
    print("已写 %s" % OUT_CSV)

    # --- 落盘 MD ---
    lines = []
    lines.append("# 《明一统志》旧→新条目编号重映射表\n")
    lines.append("自动生成，源：`_item_registry.json`（旧 %d 键）→ "
                 "`书籍json/明一统志.json`（新 %d 条）。\n" % (len(remap), len(book_iids)))
    lines.append("## 判定口径\n")
    lines.append("| method | 含义 | 置信度 | 键数 |")
    lines.append("|---|---|---|---|")
    desc = {
        "exact": "旧键本身即新 iid",
        "title": "title 在书籍json 唯一命中同名条",
        "title-vol": "同名多条，但同卷唯一命中",
        "title-amb": "同名跨卷，同卷无唯一解（取首个，**需校订**）",
        "unmapped": "占位 title 或书籍json 无同名条（**不可用**）",
    }
    for m in ("exact", "title", "title-vol", "title-amb", "unmapped"):
        lines.append("| `%s` | %s | %.2f | %d |" % (m, desc[m], CONF[m], mc[m]))
    lines.append("")
    lines.append("## 层记录挂载统计\n")
    lines.append("| 层 | 总记录 | 可挂载 | 占比 | exact | title | title-vol | title-amb | 不可用 |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for layer in LAYERS:
        s = stats[layer]
        ok = s["total"] - s.get("unmapped", 0)
        lines.append("| %s | %d | %d | %.1f%% | %d | %d | %d | %d | %d |" % (
            layer, s["total"], ok, 100.0 * ok / max(1, s["total"]),
            s.get("exact", 0), s.get("title", 0), s.get("title-vol", 0),
            s.get("title-amb", 0), s.get("unmapped", 0)))
    lines.append("| **合计** | **%d** | **%d** | **%.1f%%** | | | | | |" % (
        tot, avail, 100.0 * avail / max(1, tot)))
    lines.append("")

    amb = [k for k, v in remap.items() if v["method"] == "title-amb"]
    if amb:
        lines.append("## 待校订：title 有歧义（%d 条）\n" % len(amb))
        lines.append("| 旧 id | 旧 title | 自动择定 | 全部同名候选 |")
        lines.append("|---|---|---|---|")
        for k in sorted(amb):
            r = remap[k]
            t = r["old_title"]
            lines.append("| `%s` | %s | `%s` | %s |" % (
                k, t, r["new"], ", ".join("`%s`" % c for c in by_title.get(t, []))))
        lines.append("")

    unm = sorted(k for k, v in remap.items() if not v["new"])
    if unm:
        lines.append("## 不可用：无对应条目（%d 条）\n" % len(unm))
        lines.append("这些条目的 title 是知识层生成期的批次标签（`persN_xxx` / `tNN_xxx` / "
                     "`wNN_xxx` / `mtnsN`）或书籍json 中确无同名条，"
                     "涉及层记录约 %d 条，须回源头修复后才可挂载。\n" % sum(
                         stats[l].get("unmapped", 0) for l in LAYERS))
        lines.append("| 旧 id | 旧 title | region | type |")
        lines.append("|---|---|---|---|")
        for k in unm:
            r = remap[k]
            lines.append("| `%s` | %s | %s | %s |" % (
                k, r["old_title"], r["region"] or "", r["type"] or ""))
        lines.append("")

    with io.open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("已写 %s" % OUT_MD)

    print()
    print("=" * 74)
    print("下一步：人工校订 %s 中 method=title-amb / unmapped 的行。" % os.path.basename(OUT_CSV))
    print("校订后 adapter 会自动读取 _item_remap.json（无需改代码）。")


if __name__ == "__main__":
    main()
