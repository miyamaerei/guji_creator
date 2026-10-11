"""抽卷进度巡检：各层源数据的记录数、条号分布、缺口。

用法：python _scan_src.py
"""

from __future__ import annotations

import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "_src"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ID_RE = re.compile(r"""item_id["'\]\s:=\[]*["'](\d{2}-\d{3})["']""")
LAYERS = ["ent", "event", "rel", "nam", "cit", "obj", "cus", "opn", "ming", "appt", "trl"]


def main() -> None:
    reg = json.loads((ROOT / "_item_registry.json").read_text(encoding="utf-8"))
    counts: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    stray: list[str] = []

    print("=== 源数据文件 ===")
    for path in sorted(SRC.glob("*")):
        if path.is_dir():
            continue
        if path.suffix == ".py" and re.match(r"^_[a-z]+_ai_\d{2}\.py$", path.name):
            layer = path.name[1:].split("_ai_")[0]
            vol = path.stem[-2:]
            ids = ID_RE.findall(path.read_text(encoding="utf-8"))
            counts[layer][vol] = collections.Counter(ids)
            by_vol = dict(collections.Counter(i[:2] for i in ids))
            print(f"  {path.name:<26} n={len(ids):5d}  vol={by_vol}")
        else:
            stray.append(path.name)
    if stray:
        print("  [非契约文件，不参与打包] " + ", ".join(stray))

    print("\n=== 分层汇总（记录数 / 覆盖条数）===")
    for layer in LAYERS:
        if layer not in counts:
            print(f"  {layer:<6} 缺")
            continue
        tot = sum(len(c) for c in counts[layer].values())
        allids = set()
        for c in counts[layer].values():
            allids |= set(c)
        cov = {v: sum(1 for i in allids if i[:2] == v) for v in ("01", "02")}
        print(f"  {layer:<6} 记录={tot:5d}  覆盖条数 01={cov['01']:4d}/125  02={cov['02']:4d}/105")

    print("\n=== 分卷缺层 ===")
    for layer in LAYERS:
        for v in ("01", "02"):
            if layer in counts and v in counts[layer]:
                continue
            if layer in counts:
                print(f"  缺 {layer} 卷{v}")

    print("\n=== 条号越界检查（非 01/02 的 item_id）===")
    for layer, vols in counts.items():
        for v, c in vols.items():
            bad = [i for i in c if i[:2] not in ("01", "02")]
            if bad:
                print(f"  {layer}_{v}: {sorted(set(bad))[:10]}")
    print("  完成")


if __name__ == "__main__":
    main()
