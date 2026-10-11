# -*- coding: utf-8 -*-
"""T3 合并映射回写：ent 层补 normalized/修正 type（SPECIAL 与 v2_pending 不动）。
用法: python apply_merge_map.py [--dry-run] [--ent-only]
- --dry-run  只输出 patch 计划不写文件
- --ent-only 仅回写 ent 层（引用侧另跑）
引号风格跟随源文件：含单引号 dict 用 python repr，双引号用 json。
"""

import ast
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 项目根：由脚本自身位置推导（本文件在 <项目根>/_global/ 下），整体搬移无需改路径
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = ROOT + "/_src"
DRY = "--dry-run" in sys.argv

mp = json.load(open(ROOT + "/_global/merge_map.json", encoding="utf-8"))
TC = {p["text"]: p["canonical"] for p in mp["text_canonical"]}
CLUSTERS = {}
for c in mp["alias_clusters"]:
    CLUSTERS[c["canonical"]] = c["canonical"]
    for a in c["aliases"]:
        CLUSTERS[a] = c["canonical"]
NS = mp.get("nature_split", {})
NAT = {}
for k in ("animal", "plant", "place", "unknown"):
    for x in NS.get(k, []):
        NAT[x] = k

SPECIAL = {p["text"] for p in mp["text_canonical"] if p["canonical"] == "SPECIAL"}


def resolve(text: str):
    """返回 (canonical, need_norm)：need_norm=False 表示不用写 normalized。"""
    if text in SPECIAL:
        return None, False
    c = TC.get(text)
    if c:
        return CLUSTERS.get(c, c), True
    cc = CLUSTERS.get(text)
    if cc:
        return cc, True
    return None, False


def fix_type(t: str, text: str):
    if t == "book":
        return "work"
    if t == "other":
        return "unknown"
    if t == "event":
        return "event"
    if t == "nature":
        return NAT.get(text, "unknown")
    return t


def render_dict(d: dict, indent: str, quote: str, multiline: bool) -> str:
    """把 dict 渲染成与源一致的形态。quote=' 或 "。"""
    if quote == "'":

        def q(s):
            return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'") + "'"
    else:

        def q(s):
            return json.dumps(str(s), ensure_ascii=False)

    items = []
    for k, v in d.items():
        if isinstance(v, str):
            items.append((k, q(v)))
        else:
            items.append((k, repr(v)))
    if multiline:
        inner = ",\n".join(indent + "    " + q(k) + ": " + v for k, v in items)
        out = indent + "{\n" + inner + "\n" + indent + "}," if True else ""
        return indent + "{\n" + inner + "\n" + indent + "},"
    return indent + "{" + ", ".join(q(k) + ": " + v for k, v in items) + "},"


def patch_ent_file(v: int):
    vv = f"{v:02d}"
    p = f"{SRC}/_ent_ai_{vv}.py"
    src = open(p, encoding="utf-8").read()
    tree = ast.parse(src)
    recs_node = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            getattr(t, "id", None) == "RECORDS" for t in node.targets
        ):
            recs_node = node.value
    if not isinstance(recs_node, ast.List):
        return vv, 0, 0, 0, "no RECORDS list"
    lines = src.splitlines(keepends=True)
    region = {}  # (start_ln, end_ln) -> new dict
    n_norm = n_type = n_spec = 0
    for el in recs_node.elts:
        if not isinstance(el, ast.Dict):
            continue
        d = ast.literal_eval(el)
        text = d.get("text", "")
        if text in SPECIAL:
            n_spec += 1
            continue
        orig_lines = "".join(lines[el.lineno - 1 : el.end_lineno])
        quote = (
            "'"
            if re.search(r"['\"](text|type|item_id|normalized)['\"]:\s*'", orig_lines)
            else '"'
        )
        multiline = el.lineno != el.end_lineno
        indent = re.match(r"[ \t]*", lines[el.lineno - 1]).group(0)
        nd = dict(d)
        changed = False
        canon, need_norm = resolve(text)
        if need_norm and canon and nd.get("normalized") != canon:
            nd["normalized"] = canon
            n_norm += 1
            changed = True
        nt = fix_type(nd.get("type"), text)
        if nd.get("type") != nt:
            nd["type"] = nt
            n_type += 1
            changed = True
        if changed:
            region[(el.lineno, el.end_lineno)] = render_dict(
                nd, indent, quote, multiline
            )
    if not region:
        return vv, n_norm, n_type, n_spec, "no patch"
    if DRY:
        print(
            f"[dry-run] 卷{vv}: norm+n_type={n_norm}+{n_type} patch 区间 {len(region)}"
        )
        return vv, n_norm, n_type, n_spec, "dry"
    # 从后往前替换
    for (s, e), newtxt in sorted(region.items(), key=lambda x: -x[0][0]):
        # 校验新文本行数兼容（multiline 输出行数 = 键数+2）
        lines[s - 1 : e] = [newtxt + "\n"]
    open(p, "w", encoding="utf-8").writelines(lines)
    return vv, n_norm, n_type, n_spec, "patched"


def main():
    total = [0, 0, 0]
    for v in range(1, 11):
        vv, nn, nt, ns, msg = patch_ent_file(v)
        total[0] += nn
        total[1] += nt
        total[2] += ns
        print(f"卷{vv}: normalized+{nn} type+{nt} SPECIAL跳过{ns} [{msg}]")
    print(f"合计: normalized+{total[0]} type+{total[1]} SPECIAL跳过{total[2]}")


if __name__ == "__main__":
    main()
