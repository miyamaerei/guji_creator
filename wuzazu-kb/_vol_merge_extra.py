# -*- coding: utf-8 -*-
"""把 _vol_<NN>_extra.py 的补装层合入 _vol_<NN>.py（幂等，可重复跑）。

用法：
    python _vol_merge_extra.py01 02
    python _vol_merge_extra.py            # 全部已存在的 extra

合并规则：
  * 已存在的层 → 追加（同一层同一 item 的新记录接在旧记录之后）；
  * 旧文件里没有的层 → 直接新增；
  * 不覆盖已有记录（避免把已装填的 6 层数据弄丢）；
  * 合完自动跑 split 与 audit。
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

import _vol_schema as V  # noqa: E402
from _kg_pack_base import BUILD_DIR  # noqa: E402


def extra_path(volume: str) -> Path | None:
    """extra 源文件位置：优先 _src/（正在编辑），其次 _build/（已合入，留档溯源）。"""
    for d in (V.SRC_DIR, BUILD_DIR):
        p = d / f"_vol_{volume}_extra.py"
        if p.exists():
            return p
    return None


def load_extra(volume: str) -> dict:
    p = extra_path(volume)
    if p is None:
        return {}
    ns: dict = {"__file__": str(p), "__name__": f"_vol_{volume}_extra"}
    exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), ns)  # noqa: S102
    out = {}
    for key in ("SRC_EXTRA", "SRC", "RECORDS"):
        val = ns.get(key)
        if isinstance(val, dict):
            out = val
            break
    return out


def merge(volume: str) -> dict:
    extra = load_extra(volume)
    if not extra:
        return {"volume": volume, "added": 0, "layers": {}}

    base = V.load_volume(volume)
    stats: dict[str, int] = {}
    for item_id, bucket in extra.items():
        if item_id not in base:
            base[item_id] = {}
        target = base[item_id]
        for layer, payload in bucket.items():
            rows = V._normalize_layer_value(layer, payload)
            if layer == "trl":
                for row in rows:
                    for dk, dv in V.TRL_DEFAULTS.items():
                        row.setdefault(dk, dv)
            if not rows:
                continue
            # 去重：同一层里内容完全相同的只留一条
            existing = target.get(layer, [])
            seen = {V.row_key(r) for r in existing}
            added = 0
            for row in rows:
                row["item_id"] = item_id
                key = V.row_key(row)
                if key in seen:
                    continue
                seen.add(key)
                existing.append(row)
                added += 1
            if existing:
                target[layer] = existing
                stats[layer] = stats.get(layer, 0) + added

    V.SRC_DIR.mkdir(parents=True, exist_ok=True)
    V.write_text(V.volume_source_path(volume),
                 V.render_volume_source(volume, base))
    return {"volume": volume, "added": sum(stats.values()), "layers": stats}


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    vols = ([a.zfill(2) for a in args] if args
            else sorted({p.name[5:7]
                         for d in (V.SRC_DIR, BUILD_DIR)
                         for p in d.glob("_vol_*_extra.py")}))
    for vol in vols:
        r = merge(vol)
        if not r["layers"]:
            print(f"[skip] 卷{vol}：无 extra 文件")
            continue
        print(f"[merge] 卷{vol}：新增 {r['added']} 条 → "
              + " ".join(f"{k}+{n}" for k, n in sorted(r["layers"].items())))
    print()
    for vol in vols:
        counts = V.split(vol)
        print(f"[split] 卷{vol}：" +
              " ".join(f"{k}={n}" for k, n in counts.items() if n))
        audit = V.audit(vol)
        flag = "OK" if audit["consistent"] else "DIFF"
        print(f"[audit] 卷{vol} {audit['name']}：{flag} 覆盖 {audit['coverage']}")


if __name__ == "__main__":
    main()