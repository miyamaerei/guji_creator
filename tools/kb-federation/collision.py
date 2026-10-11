"""collision.py —— F0-a 撞号体检

把「六书 ID 跨书撞号」固化为可重复脚本，作为 E 阶段前置断言：
撞号必须被复合主键 (book_id, ...) 消解，否则联邦库无法安全合并。

扫描所有书的所有 .json 文本，正则抽取 `前缀-数字` 型 ID，统计：
- 总 ID 数
- 出现在 ≥2 本书的 ID 数（跨书撞号）
- 撞号按前缀分布
- 样例（供人工核对）

零第三方依赖，仅 os / re / collections。
"""

import os
import re
import collections

# 例：ENT-001 / APPT-012 / XJF-E-001 / REL-003
ID = re.compile(r"\b([A-Z]{2,4}(?:-[A-Z])?)-\d+\b")

# walk 时跳过的目录（这些不是层产物，或会污染扫描）
SKIP_DIRS = {
    "_backup",
    "_tmp",
    "_validate",
    "_build",
    "交付物",
    "阅读器",
    "node_modules",
    ".git",
}


def iter_json_files(root):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if not f.endswith(".json"):
                continue
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 64 * 1024 * 1024:  # 大文件（如蘧编 ents 11MB）不跳过
                    continue
            except OSError:
                continue
            yield p


def scan_ids(roots):
    """书 -> {id}。"""
    out = {}
    for b, root in roots.items():
        ids = set()
        if not os.path.isdir(root):
            continue
        for p in iter_json_files(root):
            try:
                t = open(p, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for m in ID.finditer(t):
                ids.add(m.group(0))
        out[b] = ids
    return out


def check_collision(roots):
    owner = collections.defaultdict(set)  # id -> {书}
    for b, ids in scan_ids(roots).items():
        for k in ids:
            owner[k].add(b)
    multi = {k: sorted(v) for k, v in owner.items() if len(v) > 1}
    byp = collections.Counter()
    for k in multi:
        byp[k.split("-")[0]] += 1
    return {
        "total_ids": len(owner),
        "books": len(roots),
        "collisions": len(multi),
        "by_prefix": dict(byp.most_common()),
        "multi": multi,
    }


def format_report(rep, samples=10):
    lines = []
    lines.append(f"扫描书数：{rep['books']}")
    lines.append(f"总 ID 数：{rep['total_ids']}")
    lines.append(
        f"跨书撞号数：{rep['collisions']}"
        f"（占 {rep['collisions'] / max(rep['total_ids'], 1) * 100:.1f}%）"
    )
    lines.append("撞号按前缀分布：")
    for p, c in rep["by_prefix"].items():
        lines.append(f"    {p:<6} {c}")
    lines.append(f"撞号样例（最多 {samples}）：")
    for k in sorted(rep["multi"])[:samples]:
        lines.append(f"    {k}  →  {', '.join(rep['multi'][k])}")
    return "\n".join(lines)
