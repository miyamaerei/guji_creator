# -*- coding: utf-8 -*-
"""T3 引用侧联动（v3）：
A. {text|name, *_ent_ids} 槽 / nam entries[].person —— 仅当 canonical 能被本卷 ent
   alias 解析（build 同款逻辑）时改写，防引用断裂。
B. 非槽位纯字符串点名叶子（非 ID_REF_KEYS 跳过键、非 nam entries[].person、
   非 nam.names 列表）—— 整串精确命中映射旧词形 → 无条件改 canonical（不回填无风险）。
保守边界：evidence/source/translation/original/scope 等叙述长文本与 nam 旧词形登记保留。
用法: python ref_side_patch.py [--dry-run]
"""

import ast
import io
import json
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = "C:/Users/Administrator/.qianfan/workspace/sessions/5c7aeec1c4044e68bb49a4541b18ed5b/2026-10-10/new-chat-4/kezuozhuiyu"
SRC = ROOT + "/_src"
DRY = "--dry-run" in sys.argv

mp = json.load(open(ROOT + "/_global/merge_map.json", encoding="utf-8"))
TC = {p["text"]: p["canonical"] for p in mp["text_canonical"]}
CLUSTERS = {}
for c in mp["alias_clusters"]:
    CLUSTERS[c["canonical"]] = c["canonical"]
    for a in c["aliases"]:
        CLUSTERS[a] = c["canonical"]
SPECIAL = {p["text"] for p in mp["text_canonical"] if p["canonical"] == "SPECIAL"}

_ENT_LAYERS = (
    "nam",
    "lit",
    "ming",
    "event",
    "rel",
    "obj",
    "cus",
    "appt",
    "geo",
    "opn",
    "cit",
    "trl",
)
# 与 validate_layers.ID_REF_KEYS 对齐：这些键下字符串不参与词形检查，保留原文
SKIP_KEYS = {
    "item_id",
    "volume",
    "volume_name",
    "original",
    "norm",
    "start",
    "end",
    "_layer",
    "source",
    "evidence",
    "translation",
    "ent_id",
    "id",
    "scope",
    "summary",
    "content_location",
    "names",
    "note",
    "lore",
    "details",
    "description",
    "what",
    "history",
    "detail",
}

_PAREN_RE = re.compile(r"[（(][^（()）]*[）)]")
_PLACEHOLDER = {"未明", "不明", "无", ""}


def resolve(text):
    if text in SPECIAL:
        return None
    c = TC.get(text)
    if c:
        return CLUSTERS.get(c, c)
    return CLUSTERS.get(text)


def load_records(p):
    src = open(p, encoding="utf-8").read()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            getattr(t, "id", None) == "RECORDS" for t in node.targets
        ):
            return ast.literal_eval(node.value)
    return []


def build_alias(records):
    alias = {}
    for r in records:
        text = str(r.get("text") or "").strip()
        eid = r.get("item_id") or ""
        if text and eid and text not in alias:
            alias[text] = eid
    return alias


def resolve_ent(text, alias):
    if not text:
        return None
    hit = alias.get(text)
    if hit:
        return hit
    core = _PAREN_RE.sub("", text).strip()
    if core and core != text:
        hit = alias.get(core)
        if hit:
            return hit
        hit = alias.get(
            text.replace("（", "").replace("）", "").replace("(", "").replace(")", "")
        )
        if hit:
            return hit
    for part in re.findall(r"[（(][^（()）]*[）)]", text):
        inner = part[1:-1].strip()
        if inner:
            hit = alias.get(inner)
            if hit:
                return hit
    if len(text) >= 2 and text not in _PLACEHOLDER:
        cands = [k for k in alias if len(k) >= 2 and (k in text or text in k)]
        if cands:
            cands.sort(key=len)
            return alias[cands[0]]
    return None


def collect_replacements(src, alias, layer, is_ent_id_slot_person):
    """返回 [(lineno, seg, old, new, kind)]；seg 为含引号的完整源码片段（get_source_segment）。"""
    tree = ast.parse(src)
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        keys = []
        for k in node.keys:
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                keys.append(k.value)
        has_ref_slot = any(k.endswith("_ent_ids") for k in keys)
        is_nam_person = layer == "nam" and "person" in keys
        for kidx, k in enumerate(node.keys):
            vnode = node.values[kidx]
            if not (
                isinstance(k, ast.Constant)
                and isinstance(vnode, ast.Constant)
                and isinstance(vnode.value, str)
            ):
                continue
            key = k.value
            val = vnode.value
            if key in ("text", "name") and has_ref_slot:
                canon = resolve(val)
                if canon and canon != val and resolve_ent(canon, alias):
                    seg = ast.get_source_segment(src, vnode)
                    if seg:
                        out.append((vnode.lineno, seg, val, canon, "slot"))
            elif key == "person" and is_nam_person:
                canon = resolve(val)
                if canon and canon != val and resolve_ent(canon, alias):
                    seg = ast.get_source_segment(src, vnode)
                    if seg:
                        out.append((vnode.lineno, seg, val, canon, "person"))
            elif key not in SKIP_KEYS and not is_nam_person and not has_ref_slot:
                # 纯字符串点名叶子：整串精确命中才改（复合叙述/含括注不动）
                canon = resolve(val)
                if canon and canon != val and len(val) >= 1:
                    if (
                        val in TC
                        or val in CLUSTERS
                        or val in {c["canonical"] for c in mp["alias_clusters"]}
                    ):
                        seg = ast.get_source_segment(src, vnode)
                        if seg:
                            out.append((vnode.lineno, seg, val, canon, "plain"))
    return out


def patch_file(p, alias, layer):
    src = open(p, encoding="utf-8").read()
    if "RECORDS" not in src:
        return [], []
    repls = collect_replacements(src, alias, layer, False)
    if DRY:
        return repls, []
    lines = src.splitlines(keepends=True)
    from collections import Counter

    by_line = {}
    for ln, seg, old, new, kind in repls:
        by_line.setdefault(ln, []).append((seg, old, new, kind))
    kept = []
    for ln, reps in by_line.items():
        line = lines[ln - 1]
        cnt = Counter(seg for seg, *_ in reps)
        for seg, old, new, kind in reps:
            quote = seg[0]
            newseg = quote + new + quote
            n = cnt[seg]
            # 该行内 seg 出现次数应与收集数一致，按序替换前 n 个
            pos = 0
            for i in range(n):
                j = line.find(seg, pos)
                if j < 0:
                    kept.append((ln, old, seg))
                    break
                line = line[:j] + newseg + line[j + len(seg) :]
                pos = j + len(newseg)
        lines[ln - 1] = line
    open(p, "w", encoding="utf-8").writelines(lines)
    return repls, kept


def main():
    tot = 0
    tot_kept = 0
    for v in range(1, 11):
        alias = build_alias(load_records(f"{SRC}/_ent_ai_{v:02d}.py"))
        c_all = 0
        ex = []
        for layer in _ENT_LAYERS:
            p = f"{SRC}/_{layer}_ai_{v:02d}.py"
            try:
                open(p, encoding="utf-8").close()
            except FileNotFoundError:
                continue
            repls, kept = patch_file(p, alias, layer)
            c_all += len(repls)
            for ln, seg, old, new, kind in repls[:6]:
                ex.append(f"  {layer} 行{ln}: {old} -> {new} [{kind}]")
        tot += c_all
        print(f"卷{v:02d}: 引用侧改写 {c_all}")
        for x in ex[:14]:
            print(x)
    print(f"合计: {tot} 处  [{'dry-run 未写入' if DRY else '已写入'}]")


if __name__ == "__main__":
    main()
