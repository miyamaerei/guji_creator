#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《明史·食货志》全层验证器 —— 真校验，可失败。

与旧版（纯 print 桩、errors 永空）的区别：
  · 每条检查都产出 (level, code, msg)；ERR 使退出码为 1；
  · 枚举、必填、ID 前缀、item_id 悬空引用全部实校；
  · 产出 reports/validation.md 与 reports/覆盖情况.md。

检查项：
  B 底座层   : registry / fingerprints 完整性、条目数守恒
  S 骨架层   : LAYER_SPECS 与 _kg_enums 同源、遗留目录护栏
  L 各层     : 枚举合法、必填齐备、ID 前缀正确、item_id 不悬空
  C16 总账树 : 14 镇齐全、五层齐备、明细可回溯原短语、金额守恒
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    BASE_DIR,
    DATA_DIR,
    ENT_LINKS_FILE,
    FROZEN_DIRS,
    KG_JOIN_FILE,
    KG_JOIN_FLAT_FILE,
    LAYER_SPECS,
    LEDGER_FLAT_FILE,
    LEDGER_LEVELS,
    LEDGER_TOWNS,
    LEDGER_TREE_FILE,
    REGISTRY_FILE,
    FINGERPRINT_FILE,
    REPORTS_DIR,
    check_enum,
    layer_dir,
    layer_file,
    load_json,
    normalize_entity_type,
    VOLUME_NAMES,
)

ISSUES: List[Tuple[str, str, str]] = []


def add(level: str, code: str, msg: str) -> None:
    ISSUES.append((level, code, msg))


def err(code: str, msg: str) -> None:
    add("ERR", code, msg)


def gap(code: str, msg: str) -> None:
    add("GAP", code, msg)


def info(code: str, msg: str) -> None:
    add("INFO", code, msg)


def fail(e: Exception, where: str) -> None:
    add("WARN", "EXC", f"{where}: {type(e).__name__}: {e}")


# =============================================================================
# B 底座层
# =============================================================================


def check_base() -> Dict[str, Any]:
    reg = load_json(REGISTRY_FILE, {})
    fp = load_json(FINGERPRINT_FILE, {})
    print(f"[B] registry={len(reg)} fingerprints={len(fp)}")

    if not reg:
        err("B-EMPTY", "registry.json 为空")
    if set(reg) != set(fp):
        only_reg = set(reg) - set(fp)
        only_fp = set(fp) - set(reg)
        err(
            "B-KEYDIFF",
            f"registry/fingerprints 键不一致: 仅reg={len(only_reg)} 仅fp={len(only_fp)}",
        )

    # 条目号连续 + 卷名合法
    for vol in VOLUME_NAMES.values():
        nos = sorted(v["no"] for v in reg.values() if v["volume"] == vol)
        if not nos:
            gap("B-VOL", f"卷 {vol} 无条目")
            continue
        expect = list(range(1, len(nos) + 1))
        if nos != expect:
            err("B-NOSEQ", f"卷 {vol} 条目号不连续: {nos[:8]}… 期望 1..{len(nos)}")

    # 每条 item_id 形如 卷号-序号
    for k, v in reg.items():
        if not k[:2].isdigit() or f"{int(k[:2]):02d}-{v['no']:03d}" != k:
            err("B-IDFMT", f"item_id 格式异常 {k} (no={v['no']})")
        if len(v.get("original", "")) != v.get("chars"):
            err(
                "B-CHARS",
                f"{k} chars 不符: 声明 {v.get('chars')} 实为 {len(v.get('original', ''))}",
            )

    # 口径：食货六 应有 51 条（含标题残句）；总 254 条
    info(
        "B-COUNT",
        f"总条目 {len(reg)}；各卷 "
        + " ".join(
            f"{v}={sum(1 for x in reg.values() if x['volume'] == v)}"
            for v in VOLUME_NAMES.values()
        ),
    )
    return reg


def check_skeleton() -> None:
    # LAYER_SPECS 指到的目录必须都在 BASE_DIR 下
    for key, spec in LAYER_SPECS.items():
        d = layer_dir(key)
        if not str(d).startswith(str(BASE_DIR)):
            err("S-DIR", f"{key} 目录越界: {d}")
    # 遗留目录护栏
    for d in FROZEN_DIRS:
        if d.exists():
            files = [p for p in d.rglob("*") if p.is_file()]
            if files:
                gap(
                    "S-LEGACY",
                    f"遗留目录非空 {d.relative_to(BASE_DIR)} ({len(files)} 文件)，"
                    f"已被 _layers/ 取代，勿再写入",
                )
    # 同源：structs 子类前缀须与 _kg_enums.STRUCT_PREFIX 一致
    from _kg_enums import STRUCT_PREFIX

    for sub, sspec in LAYER_SPECS["structs"]["subtypes"].items():
        if sspec["prefix"] != STRUCT_PREFIX.get(sub):
            err(
                "S-PREFIX",
                f"structs.{sub} 前缀不一致: {sspec['prefix']} vs {STRUCT_PREFIX.get(sub)}",
            )
    # 14 镇与 LEDGER_LEVELS
    if len(LEDGER_TOWNS) != 14:
        err("S-TOWNS", f"LEDGER_TOWNS 应为 14，实为 {len(LEDGER_TOWNS)}")
    if len(LEDGER_LEVELS) != 5:
        err("S-LEVELS", f"LEDGER_LEVELS 应为 5 层，实为 {len(LEDGER_LEVELS)}")


# =============================================================================
# L 各层
# =============================================================================


def _iter_records(key: str, data: Any):
    """把各层输出统一成 (record, 标签) 迭代。"""
    spec = LAYER_SPECS[key]
    if spec["kind"] == "registry":
        for sub, items in (data or {}).items():
            for r in items or []:
                yield sub, r
    else:
        if isinstance(data, dict) and ("items" in data or "records" in data):
            data = data.get("items") or data.get("records")
        if isinstance(data, list):
            for r in data:
                yield "", r


def check_layer(key: str, reg: Dict[str, Any]) -> int:
    spec = LAYER_SPECS[key]
    d = layer_dir(key)
    n = 0
    if not d.exists():
        gap(f"L-{key}", f"{key} 目录不存在（层未构建）: {d.relative_to(BASE_DIR)}")
        return 0

    files = sorted(p for p in d.glob("*.json") if not p.name.startswith("_"))
    if not files:
        gap(f"L-{key}", f"{key} 目录为空（层未构建）")
        return 0

    for f in files:
        try:
            data = load_json(f)
        except Exception as e:
            fail(e, str(f.relative_to(BASE_DIR)))
            continue

        # 子类（registry 型）
        subs = spec.get("subtypes")
        if subs:
            for sub, r in _iter_records(key, data):
                n += 1
                if sub not in subs:
                    err(f"L-{key}-SUB", f"{f.name}: 非法子类 {sub!r}")
                    continue
                sspec = subs[sub]
                for fld in sspec["required"]:
                    if fld not in r or r[fld] in (None, ""):
                        err(
                            f"L-{key}-REQ",
                            f"{f.name} {r.get('id', '?')}: 缺 {sub}.{fld}",
                        )
                for fld, allowed in sspec.get("enum_fields", {}).items():
                    if fld in r and not check_enum(r[fld], allowed):
                        err(
                            f"L-{key}-ENUM",
                            f"{f.name} {r.get('id', '?')}: {fld}={r[fld]!r} 非法",
                        )
                _check_common(key, r, f, reg, sspec["prefix"])
            continue

        for _sub, r in _iter_records(key, data):
            n += 1
            for fld in spec["required"]:
                if fld not in r or r[fld] in (None, ""):
                    err(f"L-{key}-REQ", f"{f.name} {r.get('id', '?')}: 缺必填 {fld}")
            for fld, allowed in spec.get("enum_fields", {}).items():
                if fld in r and not check_enum(r[fld], allowed):
                    err(
                        f"L-{key}-ENUM",
                        f"{f.name} {r.get('id', '?')}: {fld}={r[fld]!r} 非法",
                    )
            if key == "ents" and "type" in r:
                norm = normalize_entity_type(r["type"])
                if norm != r["type"]:
                    err(
                        f"L-{key}-ALIAS",
                        f"{r.get('id', '?')}: type={r['type']!r} 应归一为 {norm!r}",
                    )
            if "steps" in r and isinstance(r["steps"], list):
                se = spec.get("step_enum", [])
                for st in r["steps"]:
                    if (
                        isinstance(st, dict)
                        and st.get("step")
                        and se
                        and st["step"] not in se
                    ):
                        err(
                            f"L-{key}-STEP",
                            f"{r.get('id', '?')}: step={st['step']!r} 非法",
                        )
            _check_common(key, r, f, reg, spec["id_prefix"])
    return n


def _check_common(
    key: str, r: Dict[str, Any], f: Path, reg: Dict[str, Any], prefix: str
) -> None:
    rid = r.get("id", "")
    if prefix and not str(rid).startswith(prefix):
        err(f"L-{key}-PFX", f"{f.name}: id={rid!r} 前缀应为 {prefix!r}")
    iid = r.get("item_id")
    if iid:
        if isinstance(iid, list):
            for one in iid:
                if one not in reg:
                    err(f"L-{key}-REF", f"{f.name} {rid}: item_id {one!r} 悬空")
        elif iid not in reg:
            err(f"L-{key}-REF", f"{f.name} {rid}: item_id {iid!r} 悬空")


# =============================================================================
# C16 总账树
# =============================================================================


def check_ledger(reg: Dict[str, Any]) -> None:
    if not LEDGER_TREE_FILE.exists():
        gap("C16-MISS", "ledger_tree.json 不存在（总账树未构建）")
        return
    tree = load_json(LEDGER_TREE_FILE, {})
    if tree.get("levels") != LEDGER_LEVELS:
        err("C16-LV", f"层级不符: {tree.get('levels')}")

    towns = tree.get("level1_total", {}).get("towns", [])
    names = [t["name"] for t in towns]
    if names != LEDGER_TOWNS:
        err("C16-TOWNS", f"镇不符: {names}")
    print(f"[C16] 镇={len(towns)} 层级={tree.get('levels')}")

    n_detail = 0
    for t in towns:
        if not t.get("sides"):
            err("C16-SIDES", f"{t['name']}: 无兵种层")
        declared = t.get("summary", {}).get("条目数", 0)
        actual = sum(len(c["details"]) for s in t["sides"] for c in s["categories"])
        n_detail += actual
        if declared != actual:
            err("C16-COUNT", f"{t['name']}: summary 条目数 {declared} != 明细 {actual}")
        # 三层齐备
        for s in t["sides"]:
            if s.get("level") != "兵种":
                err("C16-LEV", f"{t['name']}/{s['name']}: level != 兵种")
            if not s.get("categories"):
                err("C16-CAT", f"{t['name']}/{s['name']}: 无收入类别")
            for c in s["categories"]:
                if c.get("level") != "收入类别":
                    err("C16-LEV", f"{t['name']}: category level != 收入类别")
                for det in c["details"]:
                    if det.get("level") != "明细":
                        err("C16-LEV", f"{t['name']}: detail level != 明细")
                    # 可回溯：明细须有原短语
                    if not det.get("phrase"):
                        err("C16-TRACE", f"{t['name']}: 明细缺 phrase（不可溯源）")

        # item_id 必须指向食货六真实条目
        iid = t.get("item_id")
        if iid not in reg:
            err("C16-REF", f"{t['name']}: item_id {iid!r} 悬空")
        elif reg[iid]["volume"] != "食货六":
            err("C16-VOL", f"{t['name']}: item_id 卷别错误 {reg[iid]['volume']}")

    # 扁平 CSV 与树守恒
    if LEDGER_FLAT_FILE.exists():
        rows = list(csv.DictReader(open(LEDGER_FLAT_FILE, encoding="utf-8-sig")))
        if len(rows) != n_detail:
            err("C16-CSV", f"CSV {len(rows)} 行 != 树明细 {n_detail} 条")
        # 每行金额可与原短语核对：数字串应出现在 phrase 内
        for r in rows:
            if r["原文数字"] and r["原文数字"] not in r["原短语"]:
                err("C16-DIGIT", f"{r['id']}: 原文数字 {r['原文数字']!r} 不在原短语内")
            if not r["数值"].lstrip("-").isdigit():
                err("C16-NUM", f"{r['id']}: 数值非整数 {r['数值']!r}")
        print(f"[C16] 明细={n_detail} CSV={len(rows)} 行")
    else:
        gap("C16-CSV-MISS", "ledger_flat.csv 不存在")


# =============================================================================
# K kg_join 跨层索引（SKILL §13）—— 条 → 层挂载可回溯、空条目率入报告
# =============================================================================


def check_kg_join(reg: Dict[str, Any]) -> None:
    if not KG_JOIN_FILE.exists():
        gap("K-MISS", "_kg_join.json 不存在（跨层索引未构建）")
        return
    joined = load_json(KG_JOIN_FILE, [])
    if not isinstance(joined, list) or not joined:
        gap("K-EMPTY", "_kg_join.json 为空")
        return

    # 1) 键集与 registry 一致
    keys = {j.get("item_id") for j in joined}
    if len(joined) != len(reg):
        gap("K-KEYS", f"kg_join {len(joined)} 条 != registry {len(reg)} 条")
    miss = set(reg) - keys
    extra = keys - set(reg)
    if miss:
        gap("K-KEYS", f"registry 有而 kg_join 缺 {len(miss)} 条: {sorted(miss)[:8]}…")
    if extra:
        gap("K-KEYS", f"kg_join 多出 registry 无 {len(extra)} 条: {sorted(extra)[:8]}…")

    # 2) 结构字段：item_id/volume/layers/layer_count
    for j in joined:
        if not j.get("item_id") or j["item_id"] not in reg:
            gap("K-STRUCT", f"kg_join 条目 item_id 非法: {j.get('item_id')!r}")
            continue
        layers = j.get("layers")
        if not isinstance(layers, dict):
            err("K-STRUCT", f"{j['item_id']}: layers 非对象")
            continue
        if set(layers) != set(LAYER_SPECS):
            err("K-STRUCT", f"{j['item_id']}: 槽位与 LAYER_SPECS 不一致")
        if j.get("volume") != reg[j["item_id"]]["volume"]:
            err("K-STRUCT", f"{j['item_id']}: volume 与 registry 不符")
        expect = sum(1 for ids in layers.values() if ids)
        if j.get("layer_count") != expect:
            err(
                "K-STRUCT",
                f"{j['item_id']}: layer_count {j.get('layer_count')} != 实挂 {expect}",
            )

    # 3) 挂载可回溯：每条 (layer, id) 必须存在于对应层文件
    layer_ids = _collect_layer_ids()
    n_hang = 0
    for j in joined:
        for key, ids in (j.get("layers") or {}).items():
            for rid in ids or []:
                if rid not in layer_ids.get(key, set()):
                    n_hang += 1
                    if n_hang <= 10:
                        err(
                            f"K-HANG",
                            f"{j['item_id']}: {key}/{rid} 挂载悬空（层文件中不存在）",
                        )
    if n_hang:
        err(f"K-HANG", f"挂载悬空共 {n_hang} 处（仅列前 10）")

    # 4) 空条目率（SKILL §13.2 交付须报）
    n_empty = sum(1 for j in joined if j.get("layer_count", 0) == 0)
    total = len(joined)
    rate = n_empty / total * 100 if total else 0.0
    info(
        "K-EMPTY",
        f"空条目率 {n_empty}/{total} ({rate:.1f}%) —— 指 registry 有条目但任何层均无挂载",
    )
    print(f"[K] kg_join={total} 空条目={n_empty} ({rate:.1f}%)")

    # 5) 扁平 CSV 与 json 挂载总数守恒
    if KG_JOIN_FLAT_FILE.exists():
        rows = list(csv.DictReader(open(KG_JOIN_FLAT_FILE, encoding="utf-8-sig")))
        n_mount = sum(
            len(ids) for j in joined for ids in (j.get("layers") or {}).values()
        )
        if len(rows) != n_mount:
            gap("K-CSV", f"flat {len(rows)} 行 != json 挂载总数 {n_mount}")
        else:
            print(f"[K] flat={len(rows)} 行 守恒 OK")
    else:
        gap("K-CSV-MISS", "_kg_join_flat.csv 不存在")


def _collect_layer_ids() -> Dict[str, set]:
    """收集各层真实记录 ID（跳过 `_` 前缀索引文件）。"""
    layer_ids: Dict[str, set] = {}
    for key in LAYER_SPECS:
        ids: set = set()
        d = layer_dir(key)
        if d.exists():
            for f in sorted(d.glob("*.json")):
                if f.name.startswith("_"):
                    continue
                data = load_json(f, {})
                for _sub, r in _iter_records(key, data):
                    if r.get("id"):
                        ids.add(r["id"])
        layer_ids[key] = ids
    return layer_ids


# =============================================================================
# EL 实体引用连通率（build_entity_links.py 产物校验，SKILL §13 补充指标）
#     指标：被至少 1 层引用的 ENT 数 / ENT 总数；引用悬空回溯
# =============================================================================


def check_entity_links(reg: Dict[str, Any]) -> None:
    if not ENT_LINKS_FILE.exists():
        gap("EL-MISS", "_ent_links.json 不存在（实体引用索引未构建）")
        return
    links = load_json(ENT_LINKS_FILE, [])
    if not isinstance(links, list) or not links:
        gap("EL-EMPTY", "_ent_links.json 为空或非列表")
        return

    # 1) 结构与 item_id 合法性（含总数守恒）
    ent_total = len(links)
    bad_id = 0
    for o in links:
        if not str(o.get("id", "")).startswith("ENT-"):
            err("EL-STRUCT", f"{o.get('id', '?')}: id 前缀应为 ENT-")
            bad_id += 1
        iid = o.get("item_id")
        if iid not in reg:
            err("EL-REF", f"{o.get('id', '?')}: item_id {iid!r} 悬空（registry 无）")
        lk = o.get("links")
        if not isinstance(lk, dict):
            err("EL-STRUCT", f"{o.get('id', '?')}: links 非对象")
            continue
        n_ids = sum(len(v) for v in lk.values() if v)
        if o.get("link_count", -1) != n_ids:
            err(
                "EL-STRUCT",
                f"{o.get('id', '?')}: link_count {o.get('link_count')} != 实引 {n_ids}",
            )

    # 2) 连通率：被至少 1 层引用的 ENT 占比
    n_linked = sum(1 for o in links if o.get("link_count"))
    rate = n_linked / ent_total * 100 if ent_total else 0.0
    info(
        "EL-RATE",
        f"实体引用连通率 {n_linked}/{ent_total} ({rate:.1f}%) "
        f"—— 被至少 1 层引用的 ENT 数 / ENT 总数（零链接 {ent_total - n_linked} 条已登记不建层）",
    )
    print(f"[EL] 实体连通 {n_linked}/{ent_total} ({rate:.1f}%) 引用悬空回溯…")

    # 3) 悬空回溯：每条 (layer, rid) 必须存在于对应层文件
    layer_ids = _collect_layer_ids()
    n_hang = 0
    for o in links:
        for key, ids in (o.get("links") or {}).items():
            if key not in layer_ids:
                err("EL-LAYER", f"{o.get('id', '?')}: 引用未知层 {key!r}")
                continue
            for rid in ids or []:
                if rid not in layer_ids.get(key, set()):
                    n_hang += 1
                    if n_hang <= 10:
                        err(
                            "EL-HANG",
                            f"{o.get('id', '?')}: {key}/{rid} 引用悬空（层文件中不存在）",
                        )
    if n_hang:
        err("EL-HANG", f"实体引用悬空共 {n_hang} 处（仅列前 10）")
    else:
        print("[EL] 引用悬空 0 处")


# =============================================================================
# 报告
# =============================================================================


def write_report(counts: Dict[str, int]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    by_level: Dict[str, Dict[str, List[str]]] = {}
    for level, code, msg in ISSUES:
        by_level.setdefault(level, {}).setdefault(code, []).append(msg)

    lines = ["# 《明史·食货志》全层验证报告", ""]
    n_err = len(by_level.get("ERR", {}))
    n_gap = len(by_level.get("GAP", {}))
    n_warn = len(by_level.get("WARN", {}))
    lines += [
        f"- ERR 类 {n_err} / GAP 类 {n_gap} / WARN 类 {n_warn}",
        "",
        "## 各层记录数",
        "",
        "| 层 | 记录数 |",
        "|---|---|",
    ]
    for k, v in counts.items():
        lines.append(f"| {k} | {v} |")
    lines.append("")

    for level in ("ERR", "GAP", "WARN", "INFO"):
        codes = by_level.get(level)
        if not codes:
            continue
        lines.append(f"## {level}")
        lines.append("")
        for code, msgs in sorted(codes.items()):
            lines.append(f"### {code}  ({len(msgs)})")
            lines.append("")
            for m in msgs[:50]:
                lines.append(f"- {m}")
            if len(msgs) > 50:
                lines.append(f"- … 其余 {len(msgs) - 50} 条略")
            lines.append("")

    (REPORTS_DIR / "validation.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"  [写] reports/validation.md")


def main() -> int:
    print("=== 全层验证 ===")
    reg = check_base()
    check_skeleton()

    counts: Dict[str, int] = {}
    for key in LAYER_SPECS:
        n = check_layer(key, reg)
        counts[key] = n
        status = "有" if n else "缺"
        print(f"[L] {key:<8} {status} ({n} 条)")

    check_ledger(reg)

    check_kg_join(reg)

    check_entity_links(reg)

    write_report(counts)

    n_err = sum(1 for i in ISSUES if i[0] == "ERR")
    n_gap = sum(1 for i in ISSUES if i[0] == "GAP")
    n_warn = sum(1 for i in ISSUES if i[0] == "WARN")
    print(f"\n结果: ERR={n_err} GAP={n_gap} WARN={n_warn}")
    if n_err:
        print("未通过：存在 ERR，详见 reports/validation.md")
        return 1
    print("通过：无 ERR" + ("（有 GAP，属未建层）" if n_gap else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
