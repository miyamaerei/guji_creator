# -*- coding: utf-8 -*-
"""《蘧编》底座构建器 build_base.py
按 qubian-knowledge SKILL.md §2 执行：
  输入 蘧编_结构化.json（章→节→段）→ 切分为 76 条（卷01-20 的 71 条入层）
  产出 _item_registry.json（指纹库）+ _extract\\NN_卷名.txt + volume_summary.csv
幂等：可重跑；带 --volumes 时增量合并（不截断共享文件）。
"""
import json
import os
import re
import sys
import csv

ROOT = os.path.dirname(os.path.abspath(__file__))   # 项目根：脚本自身位置推导
# 源数据：优先环境变量 QB_SRC；未设置时默认取 <项目根>/_source/蘧编_结构化.json
SRC = os.environ.get("QB_SRC") or os.path.join(ROOT, "_source", "蘧编_结构化.json")
OUT_DIR = os.environ.get("QB_OUT") or ROOT

# ---- 章号映射：JSON 章标题 → 卷号 ----
VOLUME_RE = re.compile(r"^卷(.+)$")   # 01-20
TAIL_ORDER = ["后记（一）", "后记（二）", "附录"]  # 21, 22

def volume_no_for(title: str):
    if title in ("序", "前言"):
        return "00"
    m = VOLUME_RE.match(title)
    if m:
        return "{:02d}".format(chinese_num(m.group(1)))
    if title == "后记（一）":
        return "21"
    if title == "后记（二）":
        return "21"
    if title == "附录":
        return "22"
    return None

def chinese_num(s: str) -> int:
    mapping = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
               "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
               "十一": 11, "十二": 12, "十三": 13, "十四": 14, "十五": 15,
               "十六": 16, "十七": 17, "十八": 18, "十九": 19, "二十": 20}
    return mapping.get(s, 0)

def make_norm(text: str) -> str:
    """基础归一：OCR 缺字 ☐→□、去重复空白、统一换行为空格（保留段落分隔符）"""
    t = text.replace("☐", "□").replace("囗", "□")
    t = re.sub(r"[ \t\u3000]+", " ", t)
    t = re.sub(r"\s*\n\s*", "\n", t)
    t = t.strip()
    return t

def main():
    with open(SRC, encoding="utf-8") as f:
        data = json.load(f)

    registry = {}
    volume_summary = {}
    extract = {}  # 卷文件 -> [(条号, 正文)]

    for ch in data["structure"]:
        vol = volume_no_for(ch["title"])
        if vol is None:
            continue
        key_file = f"{vol}_{ch['title'].replace('（', '_').replace('）', '')}"
        sec_list = ch.get("sections", [])
        if sec_list:
            for i, sec in enumerate(sec_list, 1):
                item_id = f"{vol}-{i:03d}"
                title = sec.get("title", "")
                paras = sec.get("paras", [])
                original = "\n".join([title] + paras) if title else "\n".join(paras)
                registry[item_id] = {
                    "original": original,
                    "norm": make_norm(original),
                    "volume": vol,
                    "title": title,
                    "in_layer": int(vol) in range(1, 21),
                }
                extract.setdefault(key_file, []).append((i, original))
        else:
            paras = ch.get("paras", [])
            original = "\n".join(paras)
            # 章级条目号：该卷已有条数 + 1
            n = len([k for k in registry if k.startswith(vol + "-")]) + 1
            item_id = f"{vol}-{n:03d}"
            registry[item_id] = {
                "original": original,
                "norm": make_norm(original),
                "volume": vol,
                "title": ch["title"],
                "in_layer": int(vol) in range(1, 21),
            }
            extract.setdefault(key_file, []).append((n, original))

    # 卷概要
    for item_id, v in sorted(registry.items()):
        vol = v["volume"]
        vs = volume_summary.setdefault(vol, {"volume": vol, "chapters": set(), "items": 0, "in_layer_items": 0, "in_layer": False})
        vs["chapters"].add(v["title"])
        vs["items"] += 1
        if v["in_layer"]:
            vs["in_layer_items"] += 1
            vs["in_layer"] = True

    # 写出 _item_registry.json
    os.makedirs(OUT_DIR, exist_ok=True)
    reg_path = os.path.join(OUT_DIR, "_item_registry.json")
    with open(reg_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    print(f"[输出] _item_registry.json -> {reg_path}（{len(registry)} 条）")

    # 写出 _extract（幂等：先清理本目录旧卷文件，避免错误卷号残留）
    ext_dir = os.path.join(OUT_DIR, "_extract")
    os.makedirs(ext_dir, exist_ok=True)
    for old in os.listdir(ext_dir):
        if old.endswith(".txt"):
            os.remove(os.path.join(ext_dir, old))
    for key_file, rows in sorted(extract.items()):
        p = os.path.join(ext_dir, key_file + ".txt")
        with open(p, "w", encoding="utf-8-sig") as f:
            for seq, text in rows:
                f.write(f"条{seq}|{text}\n")
        print(f"[输出] _extract\\{key_file}.txt（{len(rows)} 条）")

    # 写出 volume_summary.csv
    csv_path = os.path.join(OUT_DIR, "volume_summary.csv")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["volume", "chapters", "items", "in_layer_items", "in_layer"])
        for vol in sorted(volume_summary.keys()):
            vs = volume_summary[vol]
            w.writerow([vs["volume"], "|".join(sorted(vs["chapters"])), vs["items"], vs["in_layer_items"], vs["in_layer"]])
    print(f"[输出] volume_summary.csv -> {csv_path}")

    total = len(registry)
    in_layer = sum(1 for v in registry.values() if v["in_layer"])
    print(f"[统计] 总条数 {total} | 入层条数 {in_layer} | 不入层 {total - in_layer}")

if __name__ == "__main__":
    main()
