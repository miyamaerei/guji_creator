# -*- coding: utf-8 -*-
"""治谱 TRL 层：把 白话文/ 现成白话按篇目顺序对位入层。
不另译、不切条——白话条目直接按顺序对应 registry 里该卷第 N 条。
输出 _layers/trl/trl_NN.json + trl_summary.json。"""
import json, os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_base as bb

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "白话文")
OUT = os.path.join(ROOT, "_layers", "trl")
REG = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 文件名 → 卷号
VOL_MAP = {
    "卷之一_白话.txt": "01", "卷之二_白话.txt": "02", "卷之三_白话.txt": "03",
    "卷之四_白话.txt": "04", "卷之五_白话.txt": "05", "卷之六_白话.txt": "06",
    "卷之七_白话.txt": "07", "卷之八_白话.txt": "08", "卷之九_白话.txt": "09",
    "卷之十_白话.txt": "10", "卷之十补遗_白话.txt": "11",
}

# 该卷在 registry 里的所有 item_id（按序）
def vol_items(vol):
    return [k for k in sorted(REG.keys()) if k.startswith(vol + "-")]

os.makedirs(OUT, exist_ok=True)
summary = []
total = 0
for fname, vol in VOL_MAP.items():
    text = open(os.path.join(SRC, fname), encoding="utf-8").read()
    sections = bb.split_sections(text)
    baihua_items = []
    for titles, body in sections:
        baihua_items.extend(bb.parse_body(body, titles))
    expected = vol_items(vol)
    # 对账
    n_bh = len(baihua_items)
    n_reg = len(expected)
    if n_bh != n_reg:
        print(f"⚠ {vol}: 白话 {n_bh} 条 vs registry {n_reg} 条 —— 仅对位前 min(n_bh,n_reg) 条，差 {n_reg-n_bh}")
    # 对位
    records = []
    for i, (iid, (bh_title, bh_text)) in enumerate(zip(expected, baihua_items)):
        records.append({
            "trl_id": f"TRL-{iid.replace('-','')}",
            "item_id": iid,
            "style": "注释性翻译",
            "translation": bh_text,
            "original": REG[iid]["original"],
            "confidence": 1.0,
        })
    out = os.path.join(OUT, f"trl_{vol}.json")
    json.dump({"records": records}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    total += len(records)
    summary.append({"vol": vol, "registry": n_reg, "baihua": n_bh, "aligned": len(records)})

json.dump({"summary": summary, "total": total},
          open(os.path.join(OUT, "trl_summary.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print(f"\nTRL 完成：{total} 条 → {OUT}")
for s in summary:
    flag = "✓" if s["registry"] == s["baihua"] else "⚠"
    print(f"  {flag} 卷{s['vol']}: registry {s['registry']} / 白话 {s['baihua']} / 对位 {s['aligned']}")
