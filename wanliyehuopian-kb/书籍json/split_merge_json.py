# -*- coding: utf-8 -*-
"""
书籍 JSON 分卷拆分 / 拼接工具（通用，单书场景）
用法：
  python split_merge_json.py <整书json>   → 拆到 脚本同目录/分卷json/ 下，每卷一个 json
  python split_merge_json.py merge <书名> → 从 分卷json/ 拼回整书 json（<书名>_拼合.json）

整书 JSON 约定结构：
  { "meta": {...}, "卷数": N, "条目总数": M,
    "volumes": [ {"no": "...", "name": "...(可无)", "file": "...", "count": n, "items": [...]} ] }
每卷 JSON 结构（与整书中该卷一致，供拼接）：
  { "meta": {...}, "volumes": [ {no,name,file,count,items} ] }
分卷存放：单书场景直接放 <脚本目录>/分卷json/ 根（卷文件即 <no>_<name>.json）。
"""
import io
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
SPLIT_DIR = os.path.join(BASE, "分卷json")


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, doc):
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)


def safe_name(s):
    return re.sub(r'[\\/:*?"<>|]', "_", s)


def split_book(json_path):
    doc = load(json_path)
    meta = doc.get("meta", {})
    book = meta.get("书名") or os.path.splitext(os.path.basename(json_path))[0]
    book = safe_name(book)
    outdir = SPLIT_DIR
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for v in doc.get("volumes", []):
        name = safe_name(v.get("name") or "")
        if name:
            fn = f"{v.get('no')}_{name}.json"
        else:
            fn = v.get("file", "").replace(".txt", ".json") or f"{v.get('no')}.json"
        save(os.path.join(outdir, fn), {"meta": meta, "volumes": [v]})
        n += 1
    print(f"拆分 {book}: {n} 卷 → {outdir}")


def merge_book(book, out_path=None):
    book = safe_name(book)
    indir = SPLIT_DIR
    if not os.path.isdir(indir):
        raise FileNotFoundError(f"未找到分卷目录: {indir}")
    files = sorted(f for f in os.listdir(indir) if f.endswith(".json"))
    if not files:
        raise FileNotFoundError(f"分卷目录为空: {indir}")
    volumes, meta = [], None
    for fn in files:
        doc = load(os.path.join(indir, fn))
        if meta is None:
            meta = doc.get("meta", {})
        vs = doc.get("volumes") or []
        if vs:
            volumes.append(vs[0])
    total = sum(len(v.get("items", [])) for v in volumes)
    doc = {"meta": meta, "卷数": len(volumes), "条目总数": total, "volumes": volumes}
    out = out_path or os.path.join(BASE, f"{book}_拼合.json")
    save(out, doc)
    print(f"拼接 {book}: {len(volumes)} 卷 / {total} 条 → {out}")
    return out


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "merge":
        merge_book(sys.argv[2])
    elif len(sys.argv) == 2:
        split_book(sys.argv[1])
    else:
        print(__doc__)
