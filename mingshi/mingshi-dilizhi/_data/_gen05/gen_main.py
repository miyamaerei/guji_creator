# -*- coding: utf-8 -*-
"""卷05 7层AI源数据 临时生成器（非交付物）：合并数据分片 → 校验命中 → 生成 7 个 .py 源文件。"""

import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
SCRIPTS = os.path.join(ROOT, "scripts")

with io.open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8") as f:
    REG = json.load(f)

ENTITY_ALIAS = {}
try:
    sys.path.insert(0, SCRIPTS)
    import _kg_enums as E

    ENTITY_ALIAS = E.ENTITY_ALIAS
except Exception:
    pass


def norm_of(iid):
    return REG[iid]["norm"]


def chk(iid, field, s, allow_missing=False):
    """s 必须为 norm 子串；s 为空且 allow_missing 时跳过。"""
    if not s:
        if allow_missing:
            return
        raise AssertionError("[%s] %s 为空" % (iid, field))
    if s not in norm_of(iid):
        raise AssertionError("[%s] %s 未命中 norm: %r" % (iid, field, s))


CN = {
    "零": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}


def cn2int(s):
    """中文数字 → 阿拉伯数字（支持 十/百/千/万/亿 组合；s 内已无空白）。"""
    if s.isdigit():
        return int(s)
    total, section, num = 0, 0, 0
    unit_map = {"十": 10, "百": 100, "千": 1000, "万": 10000, "亿": 100000000}
    for ch in s:
        if ch in CN:
            num = CN[ch]
        elif ch in unit_map:
            u = unit_map[ch]
            if u >= 10000:
                section = (section + num) * u
                total += section
                section, num = 0, 0
            else:
                section += (num if num else 1) * u
                num = 0
    return total + section + num


def dump_py(path, varname, doc, records):
    lines = ["# -*- coding: utf-8 -*-", '"""%s"""' % doc, "", "%s = [" % varname]
    for r in records:
        lines.append("    " + _fmt(r, 0) + ",")
    lines.append("]")
    lines.append("")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _fmt(v, indent):
    pad = "    " * (indent + 1)
    if isinstance(v, dict):
        inner = []
        for k, val in v.items():
            inner.append(
                "%s%s: %s,"
                % (pad, json.dumps(k, ensure_ascii=False), _fmt(val, indent + 1))
            )
        return "{\n" + "\n".join(inner) + "\n" + "    " * indent + "}"
    if isinstance(v, list):
        if not v:
            return "[]"
        inner = []
        for val in v:
            inner.append("%s%s," % (pad, _fmt(val, indent + 1)))
        return "[\n" + "\n".join(inner) + "\n" + "    " * indent + "]"
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    return repr(v)


def merge(parts):
    data = {}
    for p in parts:
        for iid, rec in p.items():
            data.setdefault(iid, {}).update(rec)
    return data


def main():
    parts = []
    for fn in sorted(os.listdir(HERE)):
        if fn.startswith("data_part") and fn.endswith(".py"):
            ns = {}
            src = io.open(os.path.join(HERE, fn), encoding="utf-8").read()
            exec(compile(src, fn, "exec"), ns)
            parts.append(ns["PART"])
    data = merge(parts)
    missing = [k for k in REG if k.startswith("05-") and k not in data]
    if missing:
        print("WARN 未标注条目: %s" % ",".join(missing))

    ents, tmes, geos, evos, hyds, gars, ress = [], [], [], [], [], [], []
    for iid in sorted(k for k in REG if k.startswith("05-")):
        d = data.get(iid, {})
        base = {"item_id": iid}
        # ---- ENT ----
        n = 0
        for e in d.get("ents", []) or []:
            text = e["text"]
            chk(iid, "ent.text", text)
            etype = ENTITY_ALIAS.get(e.get("type", ""), e.get("type", ""))
            if etype not in E.ENTITY_TYPES:
                raise AssertionError("[%s] ent.type 越界: %s" % (iid, etype))
            n += 1
            ents.append(
                {
                    "slot": n,
                    "item_id": iid,
                    "text": text,
                    "type": etype,
                    "count": e.get("count", 1),
                    "provenance": e.get("provenance", "条目名"),
                }
            )
        # ---- TME ----
        for t in d.get("tme", []) or []:
            era = t.get("era_raw")
            if era and era != "未明":
                chk(iid, "tme.era_raw", era)
            if t.get("event") != "未明" and t.get("event"):
                chk(iid, "tme.event", t["event"], allow_missing=True)
            tmes.append(
                base
                | {
                    k: t[k]
                    for k in ("reign", "year", "era_raw", "category", "event", "place")
                    if k in t
                }
            )
        # ---- GEO ----
        g = d.get("geo") or {}
        if g:
            name = g["name"]
            chk(iid, "geo.name", name, allow_missing=False)
            geo = {
                "slot": 0,
                "item_id": iid,
                "name": name,
                "level": g["level"],
                "node_type": g.get("node_type", "政区"),
                "parent": g.get("parent", {"text": "", "rel": ""}),
            }
            if g.get("tusi_type"):
                geo["tusi_type"] = g["tusi_type"]
            if g.get("govern"):
                geo["govern"] = g["govern"]
            bd = []
            for b in g.get("bearing_distance", []) or []:
                if b.get("raw"):
                    chk(iid, "geo.bearing.raw", b["raw"])
                bd.append(
                    {
                        "bearing": b.get("bearing", ""),
                        "to_anchor": b.get("to_anchor", ""),
                        "distance": b.get("distance", 0),
                        "unit": b.get("unit", "里"),
                        "raw": b.get("raw", ""),
                    }
                )
            geo["bearing_distance"] = bd
            qs = []
            for q in g.get("quantity", []) or []:
                if q.get("era_raw") and q["era_raw"] != "未明":
                    chk(iid, "geo.quantity.era_raw", q["era_raw"])
                if q.get("raw"):
                    chk(iid, "geo.quantity.raw", q["raw"])
                qs.append(
                    {
                        "kind": q.get("kind", ""),
                        "reign": q.get("reign", "未明"),
                        "year": q.get("year", 0),
                        "era_raw": q.get("era_raw", "未明"),
                        "num": q.get("num", 0),
                        "unit": q.get("unit", ""),
                        "raw": q.get("raw", ""),
                    }
                )
            geo["quantity"] = qs
            geo["note"] = g.get("note", "")
            if g.get("is_virtual"):
                geo["is_virtual"] = True
            geos.append(geo)
        # ---- EVO ----
        for ev in d.get("evo", []) or []:
            if ev.get("era_raw") and ev["era_raw"] != "未明":
                chk(iid, "evo.era_raw", ev["era_raw"])
            if ev.get("change"):
                chk(iid, "evo.change", ev["change"])
            evos.append(
                base
                | {
                    k: ev[k]
                    for k in (
                        "phase",
                        "era_raw",
                        "reign",
                        "year",
                        "change_type",
                        "change",
                        "owner",
                    )
                    if k in ev
                }
            )
        # ---- HYD ----
        for h in d.get("hyd", []) or []:
            if h.get("name"):
                chk(iid, "hyd.name", h["name"])
            if h.get("flow") and h["flow"] != "未明":
                chk(iid, "hyd.flow", h["flow"], allow_missing=True)
            events = []
            for ev in h.get("events", []) or []:
                if ev.get("era_raw") and ev["era_raw"] != "未明":
                    chk(iid, "hyd.events.era_raw", ev["era_raw"])
                events.append({k: ev.get(k) for k in ("kind", "era_raw") if k in ev})
            hyds.append(
                {
                    "slot": 0,
                    "item_id": iid,
                    "name": h.get("name", ""),
                    "alt": h.get("alt", ""),
                    "type": h["type"] if isinstance(h["type"], str) else "未明",
                    "flow": h.get("flow", ""),
                    "anchor": h.get("anchor", {"anchor": "", "context": ""}),
                    "events": events,
                }
            )
        # ---- GAR ----
        for ga in d.get("gar", []) or []:
            if ga.get("name"):
                chk(iid, "gar.name", ga["name"])
            est = ga.get("established") or {}
            if est.get("era_raw") and est["era_raw"] != "未明":
                chk(iid, "gar.established.era_raw", est["era_raw"])
            gars.append(
                base
                | {
                    "name": ga["name"],
                    "type": ga["type"],
                    "territorial": ga.get("territorial", "未明"),
                    "established": {
                        "reign": est.get("reign", "未明"),
                        "year": est.get("year", 0),
                        "era_raw": est.get("era_raw", "未明"),
                    },
                    "place": ga.get("place", ""),
                    "dusi": ga.get("dusi", "未明"),
                    "note": ga.get("note", ""),
                }
            )
        # ---- RES ----
        for r in d.get("res", []) or []:
            if r.get("raw"):
                chk(iid, "res.raw", r["raw"])
            ress.append(
                base
                | {
                    "name": r["name"],
                    "type": r["type"],
                    "place": r.get("place", ""),
                    "site": r.get("site", ""),
                    "importance": r.get("importance", ""),
                    "raw": r["raw"],
                }
            )

    # slot 连续编号
    for lst in (ents, tmes, geos, hyds):
        for i, r in enumerate(lst, 1):
            r["slot"] = i

    # 输出文件
    dump_py(
        os.path.join(SCRIPTS, "_ents_ai_05.py"),
        "ENTITIES",
        "卷05 实体标注（湖广/浙江 或区名·山川·卫所·年号·帝王等 择要）",
        ents,
    )
    dump_py(
        os.path.join(SCRIPTS, "_tme_ai_05.py"),
        "TME_AI",
        "卷05 时间沿革事件点（纪年→事件）",
        tmes,
    )
    dump_py(
        os.path.join(SCRIPTS, "_geo_ai_05.py"),
        "GEO_AI",
        "卷05 政区树（湖广/浙江 布政司→府→州→县 + 土司/卫所节点）",
        geos,
    )
    dump_py(
        os.path.join(SCRIPTS, "_evo_ai_05.py"),
        "EVO_AI",
        "卷05 多阶段沿革关键政区",
        evos,
    )
    dump_py(
        os.path.join(SCRIPTS, "_hyd_ai_05.py"),
        "HYD_AI",
        "卷05 水系（河/江/湖/溪/井等）",
        hyds,
    )
    dump_py(
        os.path.join(SCRIPTS, "_gar_ai_05.py"), "GAR_AI", "卷05 卫所关隘巡检司", gars
    )
    dump_py(
        os.path.join(SCRIPTS, "_res_ai_05.py"),
        "RES_AI",
        "卷05 经济资源（盐/银/铜/铁/锡等）",
        ress,
    )

    print(
        "OK ents=%d tme=%d geo=%d evo=%d hyd=%d gar=%d res=%d"
        % (len(ents), len(tmes), len(geos), len(evos), len(hyds), len(gars), len(ress))
    )


if __name__ == "__main__":
    main()
