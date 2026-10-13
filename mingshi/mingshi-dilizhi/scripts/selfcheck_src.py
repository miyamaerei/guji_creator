# -*- coding: utf-8 -*-
"""只读自检脚本：校验 scripts/_*_ai_NN.py 源数据文件的 ERR/GAP。

与打包器口径一致（不额外设卡）；仅读取 registry 与源模块，不写任何共享文件。
用法：python selfcheck_src.py [--volumes 01,07] [--report scripts/_selftest_NN.txt]
退出码：存在 ERR 时为 1，否则 0。
"""

import argparse
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)


def load_registry():
    p = os.path.join(ROOT, "_item_registry.json")
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)


def load_mod(vol, kind):
    stem = "ents" if kind == "ent" else kind
    name = "_%s_ai_%s" % (stem, vol)
    try:
        return importlib.import_module(name)
    except Exception as exc:  # noqa: BLE001
        return None, "import 失败: %s" % exc
    return None, "missing"


KINDS = {
    "ent": ("ents", "ENTITIES"),
    "tme": ("tmes", "TME_AI"),
    "geo": ("geos", "GEO_AI"),
    "evo": ("evos", "EVO_AI"),
    "hyd": ("hyds", "HYD_AI"),
    "gar": ("gars", "GAR_AI"),
    "res": ("ress", "RES_AI"),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volumes", default=None)
    ap.add_argument("--report", default=None)
    ap.add_argument(
        "--coverage",
        action="store_true",
        help="检查 GEO/ENT 条目覆盖率并把缺失条目列出",
    )
    args = ap.parse_args()
    vols = [v.strip() for v in (args.volumes or "").split(",") if v.strip()] or [
        "%02d" % i for i in range(1, 8)
    ]

    reg = load_registry()
    import _kg_enums as E

    lines, total_err, total_gap = [], 0, 0
    for vol in vols:
        for kind, (dir_, varname) in KINDS.items():
            mod = load_mod(vol, kind)
            if isinstance(mod, tuple) and mod[0] is None:
                lines.append("[%s-%s] 无源文件/%s" % (vol, kind, mod[1]))
                continue
            recs = getattr(mod, varname, None)
            if recs is None:
                lines.append("[%s-%s] 缺变量 %s" % (vol, kind, varname))
                continue
            errs, gaps = check(kind, recs, reg, E)
            lines.append(
                "[%s-%s] 记录=%d ERR=%d GAP=%d"
                % (vol, kind, len(recs), len(errs), len(gaps))
            )
            total_err += len(errs)
            total_gap += len(gaps)
            for x in errs[:30]:
                lines.append("    ERR %s" % x)
            for x in gaps[:30]:
                lines.append("    GAP %s" % x)
            if len(errs) > 30:
                lines.append("    ... 其余 %d 条 ERR 省略" % (len(errs) - 30))
            if len(gaps) > 30:
                lines.append("    ... 其余 %d 条 GAP 省略" % (len(gaps) - 30))

    lines.insert(0, "SELFCHECK 合计 ERR=%d GAP=%d" % (total_err, total_gap))

    # ---- 覆盖率检查（可选 --coverage）：每个 registry 条目应至少被 ent 或 geo 覆盖 ----
    if args.coverage:
        per_vol_items = {}
        for k in reg:
            v = k.split("-")[0]
            per_vol_items.setdefault(v, []).append(k)
        for vol in vols:
            items = sorted(per_vol_items.get(vol, []))
            geo_ids = set()
            ent_ids = set()
            for kind, (dir_, varname) in KINDS.items():
                mod = load_mod(vol, kind)
                if isinstance(mod, tuple) or mod is None:
                    continue
                recs = getattr(mod, varname, []) or []
                if kind == "geo":
                    geo_ids = {
                        r.get("item_id") for r in recs if not r.get("is_virtual")
                    }
                elif kind == "ent":
                    ent_ids = {r.get("item_id") for r in recs}
            missing_all = [k for k in items if k not in geo_ids and k not in ent_ids]
            no_geo = [
                k
                for k in items
                if k not in geo_ids
                and not reg.get(k, {}).get("is_virtual")
                and k not in ("01-001", "01-002", "01-003", "01-004", "01-005")
            ]
            lines.append(
                "[%s-cover] 条目=%d GEO 节点=%d 无GEO无ENT=%d"
                % (vol, len(items), len(geo_ids), len(missing_all))
            )
            if no_geo:
                lines.append(
                    "    无 GEO 节点条目(%d): %s" % (len(no_geo), ",".join(no_geo))
                )
            if missing_all:
                lines.append(
                    "    无 GEO 也无 ENT 条目(%d): %s"
                    % (len(missing_all), ",".join(missing_all))
                )

    text = "\n".join(lines) + "\n"
    if args.report:
        d = os.path.dirname(os.path.abspath(args.report))
        if not os.path.isdir(d):
            os.makedirs(d)
        with io.open(args.report, "w", encoding="utf-8") as f:
            f.write(text)
    print(text)
    sys.exit(1 if total_err else 0)


def check(kind, recs, reg, E):
    errs, gaps = [], []
    for i, r in enumerate(recs, 1):
        iid = r.get("item_id")
        if iid not in reg:
            errs.append("%s item_id 不存在" % iid)
            continue
        norm = reg[iid]["norm"]
        if kind == "ent":
            if r.get("type") not in E.ENTITY_TYPES:
                errs.append("%s type 越界: %s" % (iid, r.get("type")))
            if r.get("text") and r["text"] not in norm:
                gaps.append("GAP %s text 未命中: %s" % (iid, r["text"]))
        elif kind == "tme":
            if r.get("category") not in E.TME_CATEGORIES:
                errs.append("%s category 越界: %s" % (iid, r.get("category")))
            if (
                r.get("reign")
                and r["reign"] != "未明"
                and r["reign"] not in E.REIGN_ORDER
            ):
                errs.append("%s reign 越界: %s" % (iid, r.get("reign")))
            era = r.get("era_raw")
            if not era:
                errs.append("%s 缺 era_raw" % iid)
            elif era != "未明" and era not in norm:
                gaps.append("GAP %s era_raw 未命中: %s" % (iid, era))
        elif kind == "geo":
            if r.get("level") not in E.GEO_LEVELS:
                errs.append("%s level 越界: %s" % (iid, r.get("level")))
            if r.get("node_type") not in E.GEO_NODES:
                errs.append("%s node_type 越界: %s" % (iid, r.get("node_type")))
            if (
                r.get("tusi_type")
                and r["tusi_type"] != "未明"
                and r["tusi_type"] not in E.TUSI_TYPES
            ):
                errs.append("%s tusi_type 越界: %s" % (iid, r.get("tusi_type")))
            if r.get("govern") and r["govern"] not in E.TUSI_GOVERN:
                errs.append("%s govern 越界: %s" % (iid, r.get("govern")))
            for bd in r.get("bearing_distance", []) or []:
                if bd.get("bearing") and bd["bearing"] not in E.GEOTOBEARINGS:
                    errs.append("%s bearing 越界: %s" % (iid, bd.get("bearing")))
                if bd.get("raw") and bd["raw"] not in norm:
                    gaps.append("GAP %s bearing.raw 未命中: %s" % (iid, bd["raw"]))
            for q in r.get("quantity", []) or []:
                if (
                    q.get("reign")
                    and q["reign"] != "未明"
                    and q["reign"] not in E.REIGN_ORDER
                ):
                    errs.append("%s quantity.reign 越界: %s" % (iid, q.get("reign")))
                if (
                    q.get("era_raw")
                    and q["era_raw"] != "未明"
                    and q["era_raw"] not in norm
                ):
                    gaps.append(
                        "GAP %s quantity.era_raw 未命中: %s" % (iid, q["era_raw"])
                    )
                if q.get("raw") and q["raw"] not in norm:
                    gaps.append("GAP %s quantity.raw 未命中: %s" % (iid, q["raw"]))
        elif kind == "evo":
            if r.get("change_type") not in E.EVO_TYPES:
                errs.append("%s change_type 越界: %s" % (iid, r.get("change_type")))
            if (
                r.get("reign")
                and r["reign"] != "未明"
                and r["reign"] not in E.REIGN_ORDER
            ):
                errs.append("%s reign 越界: %s" % (iid, r.get("reign")))
            if r.get("change") and r["change"] not in norm:
                gaps.append("GAP %s change 未命中: %s" % (iid, r["change"]))
        elif kind == "hyd":
            if r.get("type") not in E.HYD_TYPES:
                errs.append("%s type 越界: %s" % (iid, r.get("type")))
            if r.get("name") and r["name"] not in norm:
                gaps.append("GAP %s name 未命中: %s" % (iid, r["name"]))
            if r.get("flow") and r["flow"] not in norm:
                gaps.append("GAP %s flow 未命中: %s" % (iid, r["flow"]))
            for ev in r.get("events", []) or []:
                if ev.get("kind") not in E.HYD_EVENTS:
                    errs.append("%s events.kind 越界: %s" % (iid, ev.get("kind")))
                if (
                    ev.get("era_raw")
                    and ev["era_raw"] != "未明"
                    and ev["era_raw"] not in norm
                ):
                    gaps.append(
                        "GAP %s events.era_raw 未命中: %s" % (iid, ev["era_raw"])
                    )
        elif kind == "gar":
            if r.get("type") not in E.GAR_TYPES:
                errs.append("%s type 越界: %s" % (iid, r.get("type")))
            if r.get("territorial", "未明") not in E.GAR_TERRITORIAL:
                errs.append("%s territorial 越界: %s" % (iid, r.get("territorial")))
            if r.get("dusi", "未明") not in E.GAR_DUSI:
                errs.append("%s dusi 越界: %s" % (iid, r.get("dusi")))
            if r.get("name") and r["name"] not in norm:
                gaps.append("GAP %s name 未命中: %s" % (iid, r["name"]))
            est = r.get("established") or {}
            if (
                est.get("reign")
                and est["reign"] != "未明"
                and est["reign"] not in E.REIGN_ORDER
            ):
                errs.append("%s established.reign 越界: %s" % (iid, est.get("reign")))
            if (
                est.get("era_raw")
                and est["era_raw"] != "未明"
                and est["era_raw"] not in norm
            ):
                gaps.append(
                    "GAP %s established.era_raw 未命中: %s" % (iid, est["era_raw"])
                )
        elif kind == "res":
            if r.get("type") not in E.RES_TYPES:
                errs.append("%s type 越界: %s" % (iid, r.get("type")))
            if not r.get("raw"):
                errs.append("%s 缺 raw" % iid)
            elif r["raw"] not in norm:
                gaps.append("GAP %s raw 未命中: %s" % (iid, r["raw"]))
    return errs, gaps


if __name__ == "__main__":
    main()
