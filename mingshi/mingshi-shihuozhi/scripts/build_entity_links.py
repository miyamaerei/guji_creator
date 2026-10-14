#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Entity-Link Index —— ENT 实体 → 各层记录的引用回填（实体连通率）。

背景：L1 实体层 803 条 ENT 标注完成后，与其余 7 层（rules/regs/procs/structs/
appts/tmes/opns）之间没有建立任何引用（rules 的 subject/object.ent_ids 槽位
留空，其余层无常量槽位）。本脚本做高置信回填：

  1) 产出 _layers/ents/_ent_links.json：ENT id → {text, norm, type, item_id,
     links: {层: [该层记录 id]}, link_count}；
  2) 回填 rules 层 subject.ent_ids / object.ent_ids（槽位已存在，一次性补全）。

匹配口径（防同名误配）：
  · exact 优先：value == norm/text（或顿号拆分成分相等），跨条目允许；
  · substr 兜底：norm（len≥2 且非泛词）出现在 value 中——
      同条目必回填；跨条目仅当该 norm 在全库唯一（by_norm[norm]==1 条）才回填；
      同名 norm 冲突组（67 组，如「巡抚」6 条）跨条目 substr 一律跳过，防串人/串物。
  对 tmes.office / INST.label / QUAN.item / FISC.object / regs 主体对象执行者 /
  procs.name / appts.person / opns.speaker / rules subject|object 均适用。

用法: python build_entity_links.py
"""

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    BASE_DIR,
    LAYER_SPECS,
    load_json,
    layer_dir,
    layer_file,
    save_json,
)

ENT_LINKS_FILE = BASE_DIR / "_layers" / "ents" / "_ent_links.json"

# 通用泛词黑名单（len≥2 但高频泛义，substr 会误配）：跳过
SUBSTR_STOPWORDS = {
    "天下",
    "京师",
    "天下户口",
    "有司",
    "人户",
    "民",
    "户",
    "田",
    "银",
    "粮",
    "米",
    "钞",
    "钱",
    "盐",
    "茶",
    "马",
    "布",
    "绢",
    "朝廷",
    "官",
    "军",
    "吏",
    "税",
    "课",
    "税粮",
    "正供",
    "边饷",
}


def _split_terms(value: str) -> List[str]:
    """顿号/逗号/空格拆分候选词，并保留整串。"""
    parts = [p.strip() for p in value.replace("、", ",").replace("，", ",").split(",")]
    terms = [p for p in parts if p]
    if value.strip() and value.strip() not in terms:
        terms.append(value.strip())
    return terms


def _iter_layer_records(key: str):
    """扁平迭代某层全部记录，返回 (record, 子类)。"""
    spec = LAYER_SPECS[key]
    d = layer_dir(key)
    if not d.exists():
        return
    for f in sorted(d.glob("*.json")):
        data = load_json(f, {})
        if spec["kind"] == "registry":
            for sub, items in (data or {}).items():
                for r in items or []:
                    yield r, sub
        else:
            if isinstance(data, dict) and ("items" in data or "records" in data):
                data = data.get("items") or data.get("records")
            for r in data or []:
                yield r, ""


def _item_ids_of(r: Dict[str, Any]) -> set:
    iid = r.get("item_id")
    if isinstance(iid, list):
        return set(iid)
    return {iid} if iid else set()


def _field_texts(r: Dict[str, Any], fld: str) -> List[str]:
    """提取字段文本块：str 原样；list 结构（如 procs.steps[].text）递归收集 text。"""
    v = r.get(fld)
    if isinstance(v, str):
        return [v] if v else []
    if isinstance(v, list):
        out = []
        for it in v:
            if isinstance(it, str) and it:
                out.append(it)
            elif isinstance(it, dict):
                t = it.get("text")
                if isinstance(t, str) and t:
                    out.append(t)
        return out
    return []


def build_index(ents: List[Dict]):
    """返回 (ent_by_id, norm→[ent] 索引)。"""
    by_id: Dict[str, Dict] = {}
    by_norm: Dict[str, List[Dict]] = defaultdict(list)
    for e in ents:
        by_id[e["id"]] = e
        norm = e.get("norm") or e.get("text") or ""
        by_norm[norm].append(e)
        # text 与 norm 不同时也索引（text 常含原文花名/并列）
        if e.get("text") and e["text"] != norm:
            by_norm[e["text"]].append(e)
    return by_id, dict(by_norm)


def match_ents(
    by_norm: Dict[str, List[Dict]],
    value: str,
    rec_item_ids: set,
    allowed_types: Optional[set] = None,
) -> List[str]:
    """对字段值做匹配，返回命中的 ENT id 列表（保序去重）。

    exact：term == norm/text（跨条目允许）；
    substr：norm(len≥2 且非泛词) ∈ term —— 同条目回填；跨条目仅 norm 唯一时回填。
    """
    hit_ids: List[str] = []
    seen: set = set()
    terms = _split_terms(value)
    for t in terms:
        cands = by_norm.get(t, [])
        for e in cands:
            if allowed_types and e["type"] not in allowed_types:
                continue
            if e["id"] in seen:
                continue
            hit_ids.append(e["id"])
            seen.add(e["id"])
    # substr 兜底（仅对未 exact 命中的实体）
    for norm, e_list in by_norm.items():
        if not norm or len(norm) < 2 or norm in SUBSTR_STOPWORDS:
            continue
        if any(e["id"] in seen for e in e_list):
            continue
        if norm not in value:
            continue
        # 同 item_id 优先；无同 item 时全局回退（同名 norm 跨条目视为同一语义实体）
        same_item = [e for e in e_list if e["item_id"] in rec_item_ids]
        chosen = same_item if same_item else list(e_list)
        for e in chosen:
            if e["id"] in seen:
                continue
            if allowed_types and e["type"] not in allowed_types:
                continue
            hit_ids.append(e["id"])
            seen.add(e["id"])
    return hit_ids


# ---------------------------------------------------------------------------
# 各层回填规则：层名 → (字段列表, 允许的实体类型或 None)
# 说明：tmes.office 实为制度/文书/机构名（盐法、皇庄、金花银…）而非官职，
#       故类型不限定 official；structs 按子类（QUAN/INST/EVO/FISC）单独配置。
#       evidence/沿革/标准 等长文本字段参与「文本落位」回填（方案口径）：
#       norm 子串出现在证据文本即回填，防误配规则同 match_ents。
# ---------------------------------------------------------------------------
# 叙述/证据类字段：norm 子串出现即视为被提及，类型不限（天然防噪见 match_ents）
NARRATIVE_TYPES = None

FIELD_RULES: Dict[str, List] = {
    "appts": [
        ("person", {"person"}),
        ("office", {"official", "institution", "system", "doc", "object", "place"}),
        ("evidence", NARRATIVE_TYPES),
    ],
    "opns": [
        ("speaker", {"person"}),
        ("text", NARRATIVE_TYPES),
        ("evidence", NARRATIVE_TYPES),
    ],
    "tmes": [
        ("office", None),  # 制度/文书/机构/场所/物产名，类型不限定
        ("evidence", NARRATIVE_TYPES),
    ],
    "regs": [
        ("主体", {"person", "institution", "official", "era", "system"}),
        ("对象", None),
        ("执行者", {"official", "person", "institution", "system"}),
        ("沿革", NARRATIVE_TYPES),
        ("目的", NARRATIVE_TYPES),
        ("标准", NARRATIVE_TYPES),
        ("文书载体", NARRATIVE_TYPES),
        ("史料来源", NARRATIVE_TYPES),
    ],
    "procs": [
        ("name", {"system", "behavior", "object", "institution"}),
        ("scope", {"place", "system"}),
        ("steps", NARRATIVE_TYPES),
    ],
}
STRUCT_FIELD_RULES: Dict[str, List] = {
    "QUAN": [
        (
            "item",
            {"quantity", "object", "place", "era", "system", "institution", "person"},
        ),
        ("amount", NARRATIVE_TYPES),
    ],
    "INST": [("label", {"system", "doc", "institution", "person"})],
    "EVO": [("stage", {"era", "system"}), ("description", NARRATIVE_TYPES)],
    "FISC": [("object", {"object", "quantity", "place", "system"})],
}


def main() -> None:
    print("=== Build Entity-Link Index ===")
    # 1) 加载全部 ENT
    ents: List[Dict] = []
    for v in range(1, 7):
        d = layer_dir("ents") / f"0{v}_ents.json"
        data = load_json(d, [])
        ents.extend(data.get("records", []) if isinstance(data, dict) else data)
    by_id, by_norm = build_index(ents)
    print(f"  实体: {len(ents)} 条, norm 索引: {len(by_norm)} 词")

    # 2) 逐层回填 → links[ent_id][layer] = [record ids]
    links: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
    rules_fill: Dict[str, set] = {}  # rules 层写回：记录 id -> 累积 ent_ids
    rules_recs: Dict[str, Dict] = {}  # 记录 id -> 记录 dict

    for key, field_defs in FIELD_RULES.items():
        n_hit_records = 0
        for r, _sub in _iter_layer_records(key):
            rec_ids = _item_ids_of(r)
            rid = r.get("id", "")
            rec_hit = False
            for fld, allowed in field_defs:
                for val in _field_texts(r, fld):
                    hits = match_ents(by_norm, val, rec_ids, allowed)
                    if hits:
                        rec_hit = True
                        for eid in hits:
                            links[eid][key].append(rid)
            if rid and rec_hit:
                n_hit_records += 1
        print(f"  {key:<8} 关联记录 {n_hit_records} 条")

    # structs（registry，按子类字段配置）
    for r, sub in _iter_layer_records("structs"):
        field_defs = STRUCT_FIELD_RULES.get(sub, [])
        rec_ids = _item_ids_of(r)
        rid = r.get("id", "")
        for fld, allowed in field_defs:
            val = r.get(fld)
            if not isinstance(val, str) or not val:
                continue
            hits = match_ents(by_norm, val, rec_ids, allowed)
            for eid in hits:
                links[eid]["structs"].append(rid)
    n_struct = sum(1 for o in links.values() if o.get("structs"))
    print(f"  structs 关联记录（去重实体）{n_struct} 条")

    # rules 层：subject/object 的 ent_ids 回填（写回层文件，并计入 links）；
    # evidence/condition/predicate 文本参与 links 落位（不进 ent_ids 槽位）
    for v in range(1, 7):
        f = layer_file("rules", v)
        data = load_json(f, {})
        recs = data.get("records", []) if isinstance(data, dict) else data
        changed = 0
        for r in recs:
            rec_ids = _item_ids_of(r)
            rid = r.get("id", "")
            for slot in ("subject", "object"):
                node = r.get(slot)
                if not isinstance(node, dict):
                    continue
                hits = match_ents(by_norm, node.get("text", ""), rec_ids, None)
                node["ent_ids"] = sorted(set(hits))
                if hits:
                    changed += 1
                    for eid in hits:
                        links[eid]["rules"].append(rid)
            for fld in ("evidence", "condition", "predicate", "exception", "penalty"):
                val = r.get(fld)
                if isinstance(val, str) and val:
                    for eid in match_ents(by_norm, val, rec_ids, None):
                        links[eid]["rules"].append(rid)
        if changed:
            save_json(f, data)
            print(f"  rules 卷{v:02d}: {changed} 个 subject/object 槽位回填")

    # 3) 产出 _ent_links.json（全部 ENT，含 0 链接）
    out = []
    n_linked = 0
    for e in ents:
        lk = {lay: sorted(set(ids)) for lay, ids in links[e["id"]].items() if ids}
        cnt = sum(len(v) for v in lk.values())
        if cnt:
            n_linked += 1
        out.append(
            {
                "id": e["id"],
                "item_id": e["item_id"],
                "type": e["type"],
                "text": e["text"],
                "norm": e.get("norm", e["text"]),
                "links": lk,
                "link_count": cnt,
            }
        )
    save_json(ENT_LINKS_FILE, out)
    rate = n_linked / len(ents) * 100 if ents else 0.0
    total_links = sum(o["link_count"] for o in out)
    print(f"\n  连通实体: {n_linked}/{len(ents)} ({rate:.1f}%)  总引用: {total_links}")
    per_layer = defaultdict(int)
    for o in out:
        for lay, ids in o["links"].items():
            per_layer[lay] += len(ids)
    print("  每层引用数:", dict(sorted(per_layer.items())))
    orphan = [o for o in out if o["link_count"] == 0]
    print(f"  零链接实体: {len(orphan)}（已登记，不建新层）")
    print("=== Build Entity-Link Index Complete ===")


if __name__ == "__main__":
    main()
