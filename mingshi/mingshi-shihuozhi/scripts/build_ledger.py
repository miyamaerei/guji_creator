#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C16 总账树构建器 —— 《明史·食货六》诸边及近京镇兵饷。

源：食货志.txt L272–L286（registry 06-036 … 06-050）
产出：
  _data/ledger_tree.json     五层嵌套树（总账→镇→兵种→收入类别→明细）
  _data/ledger_flat.csv      扁平明细（每行一个金额）
  _data/ledger_towns.json    14 镇汇总（便于核对）

五层口径（_kg_enums.LEDGER_LEVELS）：
  总账 / 镇 / 兵种 / 收入类别 / 明细

关键判据：
  · 「镇：」行首 = 镇名；无「主兵/客兵」分段者（甘肃、固原）side = 未分
  · 「主兵，…；客兵，…」以全角分号切分兵种段
  · 每段内以「，」切分账目，「<术语><数字><单位>」正则抽金额
  · 「有奇」「馀」→ approx=True，「万」单独出现 = 10000（坑 #64 已修）
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    BASE_DIR, DATA_DIR, LEDGER_FLAT_FILE, LEDGER_TREE_FILE, LAYER_SPECS,
    LEDGER_TOWNS, LEDGER_LEVELS, QUAN_ORIGINS, QUAN_FORMS, QUAN_SIDES,
    _QUAN_RE, load_json, save_json, save_csv, match_ledger_term,
    unit_dimension, layer_file, normalize_entity_type,
)

REGISTRY = load_json(BASE_DIR / "_data" / "registry.json")

# 兵种段头
_SIDE_RE = re.compile(r"^(主兵|客兵)\s*[，,]?\s*")
# 镇名行：`宣府：…` / `甘肃：…`
_TOWN_RE = re.compile(r"^([\u4e00-\u9fff]{2,4})\s*[：:]\s*(.*)$", re.S)
# 账目切分（全角/半角逗号、顿号不作切分——顿号在「淮、浙」内）
_ITEM_SPLIT_RE = re.compile(r"[，,]")

# 账目短语清洗：去掉「主兵/客兵」残余与括号注
_CLEAN_RE = re.compile(r"^(?:主兵|客兵)\s*[：:，,]?\s*")


def _strip_paren(s: str) -> str:
    return re.sub(r"[（(][^）)]*[）)]", "", s).strip()


def split_sides(body: str) -> list[tuple[str, str]]:
    """把镇记录体切成 [(side, 段文本)]。

    规则：先按全角分号 `；` 切；某片若以「主兵/客兵」开头则开新 side，
    否则续接上一 side（甘肃、固原无分段 → side='未分'）。
    """
    out: list[tuple[str, str]] = []
    cur_side, cur_buf = "未分", []

    for chunk in re.split(r"[；;]", body):
        chunk = chunk.strip()
        if not chunk:
            continue
        m = _SIDE_RE.match(chunk)
        if m:
            if cur_buf:
                out.append((cur_side, "，".join(cur_buf)))
            cur_side, cur_buf = m.group(1), [chunk[m.end():]]
        else:
            # 段首未标 side，且尚无「主兵/客兵」→ 保持 未分
            cur_buf.append(chunk)
    if cur_buf:
        out.append((cur_side, "，".join(cur_buf)))
    return [(s, b) for s, b in out if b.strip()]


def parse_amounts(text: str) -> list[dict]:
    """从账目短语中抽出全部「数字+单位」。"""
    found = []
    for m in _QUAN_RE.finditer(text):
        num_s, unit = m.group("num"), m.group("unit")
        approx = bool(m.group("qi") or m.group("tail"))
        try:
            from _common import parse_amount
            val, _ = parse_amount(num_s)
        except Exception as e:  # 解析失败必须暴露，不静默跳过
            raise RuntimeError(f"金额解析失败 {num_s!r} in {text!r}") from e
        # 短语标签 = 数字之前的文字（去空格）
        label = text[:m.start()].strip("，,、 ")
        found.append({
            "num_raw": num_s, "amount": val, "unit": unit,
            "dimension": unit_dimension(unit), "approx": approx,
            "label": label or "未明",
        })
    return found


def parse_town(item_id: str, text: str) -> dict:
    text = text.strip()
    m = _TOWN_RE.match(text)
    if not m:
        raise RuntimeError(f"{item_id} 不是镇记录: {text[:30]!r}")
    town, body = m.group(1), m.group(2)
    if town not in LEDGER_TOWNS:
        raise RuntimeError(f"{item_id} 镇名不在 LEDGER_TOWNS: {town!r}")

    sides = []
    for side, seg in split_sides(body):
        if side not in QUAN_SIDES:
            raise RuntimeError(f"{item_id} 非法兵种 {side!r}")
        entries = []
        for phrase in _ITEM_SPLIT_RE.split(seg):
            phrase = _CLEAN_RE.sub("", _strip_paren(phrase)).strip()
            if not phrase:
                continue
            amts = parse_amounts(phrase)
            if not amts:
                continue
            term = match_ledger_term(phrase) or {}
            origin = term.get("origin", "未明")
            form = term.get("form", "未明")
            if origin not in QUAN_ORIGINS:
                raise RuntimeError(f"{item_id} 非法 origin {origin!r} <- {phrase!r}")
            if form not in QUAN_FORMS:
                raise RuntimeError(f"{item_id} 非法 form {form!r} <- {phrase!r}")
            for a in amts:
                entries.append({
                    "origin": origin, "form": form, "object": term.get("object", "未明"),
                    "origin_alt": term.get("origin_alt", ""),
                    "combined": bool(term.get("combined")),
                    "ambiguous": bool(term.get("ambiguous")),
                    "phrase": phrase, "label": a["label"], "matched_key": term.get("matched_key"),
                    "amount": a["amount"], "unit": a["unit"],
                    "dimension": a["dimension"], "approx": a["approx"],
                    "num_raw": a["num_raw"],
                })
        if entries:
            sides.append({"side": side, "entries": entries})
    return {"item_id": item_id, "town": town, "sides": sides}


def build():
    print("=== C16 总账树构建 ===")
    towns_raw = []
    for item_id, reg in sorted(REGISTRY.items()):
        if reg["volume"] != "食货六":
            continue
        if not (37 <= reg["no"] <= 50):
            continue
        towns_raw.append((item_id, reg["original"]))

    if len(towns_raw) != len(LEDGER_TOWNS):
        raise RuntimeError(
            f"镇记录数不符：源 {len(towns_raw)} 条，LEDGER_TOWNS {len(LEDGER_TOWNS)} 个")
    src_towns = [parse_town(i, t)["town"] for i, t in towns_raw]
    if src_towns != LEDGER_TOWNS:
        raise RuntimeError(f"镇顺序/名称不符\n源: {src_towns}\n枚举: {LEDGER_TOWNS}")

    # ★ 上下文补注：裸「折色银」承前省略，按同段前一条已定 origin 记 note（不改 origin）
    parsed_all = [parse_town(*t) for t in towns_raw]
    for parsed in parsed_all:
        for s in parsed["sides"]:
            prev_known = None
            for e in s["entries"]:
                if e["ambiguous"] and prev_known:
                    e["note"] = f"承前省略，疑为「{prev_known}」之折色"
                elif e["combined"]:
                    e["note"] = f"原文合记，实含 {e['origin']} + {e['origin_alt']}，未拆分比例"
                else:
                    e["note"] = ""
                if not e["ambiguous"] and e["origin"] != "未明":
                    prev_known = e["origin"]

    # ---- 明细层（复用带 note 的已解析对象）----
    details, flat_rows = [], []
    seq = 0
    for parsed in parsed_all:
        for s in parsed["sides"]:
            for e in s["entries"]:
                seq += 1
                did = f"LED-{seq:04d}"
                details.append({
                    "id": did, "item_id": parsed["item_id"], "town": parsed["town"],
                    "side": s["side"], **e,
                })
                flat_rows.append({
                    "id": did, "item_id": parsed["item_id"], "镇": parsed["town"],
                    "兵种": s["side"], "收入类别": e["origin"], "形态": e["form"],
                    "对象": e["object"], "原短语": e["phrase"],
                    "数值": e["amount"], "单位": e["unit"], "量纲": e["dimension"],
                    "约数": "是" if e["approx"] else "",
                    "原文数字": e["num_raw"],
                    "备注": e.get("note", ""),
                })

    # ---- 五层树 ----
    tree = {
        "name": "诸边及近京镇兵饷总账",
        "source": {"file": "食货志.txt", "lines": "L272–L286",
                   "items": [i for i, _ in towns_raw]},
        "levels": LEDGER_LEVELS,
        "level1_total": {"name": "总账", "towns": []},
    }
    for parsed in parsed_all:
        node = {
            "name": parsed["town"], "item_id": parsed["item_id"],
            "level": "镇", "sides": [],
            "summary": {"条目数": 0, "银_两": 0, "粮_石": 0, "草_束": 0, "盐_引": 0},
        }
        for s in parsed["sides"]:
            snode = {"name": s["side"], "level": "兵种", "categories": []}
            cats: dict[str, list] = {}
            for e in s["entries"]:
                cats.setdefault(e["origin"], []).append(e)
                node["summary"]["条目数"] += 1
                if e["unit"] == "两":
                    node["summary"]["银_两"] += e["amount"]
                elif e["unit"] == "石":
                    node["summary"]["粮_石"] += e["amount"]
                elif e["unit"] == "束":
                    node["summary"]["草_束"] += e["amount"]
                elif e["unit"] == "引":
                    node["summary"]["盐_引"] += e["amount"]
            for origin, ents in cats.items():
                snode["categories"].append({
                    "name": origin, "level": "收入类别",
                    "details": [{
                        "level": "明细", "object": e["object"], "form": e["form"],
                        "phrase": e["phrase"], "amount": e["amount"],
                        "unit": e["unit"], "dimension": e["dimension"],
                        "approx": e["approx"], "num_raw": e["num_raw"],
                        "ambiguous": e["ambiguous"], "combined": e["combined"],
                        "origin_alt": e["origin_alt"], "note": e.get("note", ""),
                    } for e in ents],
                })
            node["sides"].append(snode)
        tree["level1_total"]["towns"].append(node)

    # ---- 镇汇总表 ----
    towns_summary = [{
        "镇": n["name"], "item_id": n["item_id"],
        "兵种数": len(n["sides"]),
        "条目数": n["summary"]["条目数"],
        "银(两)": n["summary"]["银_两"],
        "粮(石)": n["summary"]["粮_石"],
        "草(束)": n["summary"]["草_束"],
        "盐(引)": n["summary"]["盐_引"],
    } for n in tree["level1_total"]["towns"]]

    save_json(LEDGER_TREE_FILE, tree)
    save_csv(LEDGER_FLAT_FILE, flat_rows, [
        "id", "item_id", "镇", "兵种", "收入类别", "形态", "对象",
        "数值", "单位", "量纲", "约数", "原文数字", "原短语", "备注",
    ])
    save_json(DATA_DIR / "ledger_towns.json", towns_summary)

    # ---- 控制台核对 ----
    print(f"\n  镇数: {len(towns_summary)} / 明细: {len(flat_rows)} 条")
    print(f"\n  {'镇':<6}{'兵种':>4}{'条目':>6}{'银(两)':>14}{'粮(石)':>14}{'草(束)':>12}{'盐(引)':>10}")
    print("  " + "-" * 66)
    for r in towns_summary:
        print(f"  {r['镇']:<6}{r['兵种数']:>4}{r['条目数']:>6}"
              f"{r['银(两)']:>14,}{r['粮(石)']:>14,}{r['草(束)']:>12,}{r['盐(引)']:>10,}")
    tot = {k: sum(r[k] for r in towns_summary)
           for k in ("条目数", "银(两)", "粮(石)", "草(束)", "盐(引)")}
    print("  " + "-" * 66)
    print(f"  {'合计':<6}{'':>4}{tot['条目数']:>6}"
          f"{tot['银(两)']:>14,}{tot['粮(石)']:>14,}{tot['草(束)']:>12,}{tot['盐(引)']:>10,}")
    print(f"\n  树层级: {LEDGER_LEVELS}")
    return tree, towns_summary, flat_rows


if __name__ == "__main__":
    build()
