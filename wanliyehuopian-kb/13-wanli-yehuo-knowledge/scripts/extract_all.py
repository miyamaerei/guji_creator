# -*- coding: utf-8 -*-
"""
《万历野获编》全量条目提取器
============================
从源文本自动切分全部条目，生成：
  _extract/NN_卷名.txt    每卷提取文件（item_id|original）
  _item_registry.json     全局条目注册表
  _layers/*/              各层骨架文件（空 records）

用法：python scripts/extract_all.py
"""

import json
import os
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "assets" / "sources" / "万历野获编.txt"
OUT = BASE

# === 卷号映射 ===
VOL_MAP = {
    "序": ("00", "前言"),
    "续编小引": ("00", "前言"),
    "补遗序": ("00", "前言"),
    "补遗跋": ("00", "前言"),
    "分类凡例": ("00", "前言"),
}

def vol_num(name: str) -> tuple:
    """返回 (卷号str, 卷类型, 卷名)"""
    if name in VOL_MAP:
        return VOL_MAP[name] + (name,)
    m = re.match(r'卷([一二三四五六七八九十]+)', name)
    if m:
        cn = m.group(1)
        cn2num = {
            "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
            "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
            "十一": 11, "十二": 12, "十三": 13, "十四": 14, "十五": 15,
            "十六": 16, "十七": 17, "十八": 18, "十九": 19, "二十": 20,
            "二十一": 21, "二十二": 22, "二十三": 23, "二十四": 24, "二十五": 25,
            "二十六": 26, "二十七": 27, "二十八": 28, "二十九": 29, "三十": 30,
        }
        n = cn2num.get(cn, 0)
        return (f"{n:02d}", "正卷", name)
    m = re.match(r'补遗卷([一二三四])', name)
    if m:
        cn = m.group(1)
        cn2num = {"一": 1, "二": 2, "三": 3, "四": 4}
        n = cn2num.get(cn, 0)
        return (f"{30 + n:02d}", "补遗", name)
    return ("00", "前言", name)


def parse_source(text: str):
    """解析源文本，返回 [(vol_info, entries)] 列表"""
    # 找所有 ● 卷标记
    vol_markers = list(re.finditer(r'[ \s]*●([^\n]+)', text))
    
    all_vols = []
    
    for i, m in enumerate(vol_markers):
        vol_name = m.group(1).strip()
        vol_start = m.end()
        vol_end = vol_markers[i+1].start() if i+1 < len(vol_markers) else len(text)
        vol_text = text[vol_start:vol_end]
        
        vnum, vtype, vname = vol_num(vol_name)
        vol_info = {"num": vnum, "type": vtype, "name": vname}
        
        # 前言不入条目库
        if vnum == "00":
            all_vols.append((vol_info, []))
            continue
        
        # 提取条目：【标题】... 到下一个 【标题】 或 ○ 或 ● 之前
        entries = []
        # 用正则找所有 【标题】 位置
        entry_starts = list(re.finditer(r'【([^】]+)】', vol_text))
        
        for j, em in enumerate(entry_starts):
            title = em.group(1)
            entry_start = em.start()
            # 结束位置：下一个 【 或 ○ 或文本结尾
            next_entry = entry_starts[j+1].start() if j+1 < len(entry_starts) else len(vol_text)
            # 也检查 ○ 标记
            o_match = re.search(r'\n[ \s]*○', vol_text[entry_start+1:next_entry])
            if o_match:
                entry_end = entry_start + 1 + o_match.start()
            else:
                entry_end = next_entry
            
            original = vol_text[entry_start:entry_end].strip()
            # 去掉尾部的 ○ 行
            original = re.sub(r'\n[ \s]*○[^\n]*$', '', original).strip()
            
            # 找二级分类（○ 标记）
            # 在 entry 之前找最近的 ○
            pre_text = vol_text[:entry_start]
            o_matches = list(re.finditer(r'○([^\n]+)', pre_text))
            subcategory = o_matches[-1].group(1).strip() if o_matches else ""
            
            entry_id = f"{vnum}-{j+1:03d}"
            entries.append({
                "item_id": entry_id,
                "volume": vnum,
                "volume_name": vname,
                "volume_type": vtype,
                "subcategory": subcategory,
                "entry_title": title,
                "original": original,
            })
        
        all_vols.append((vol_info, entries))
    
    return all_vols


def write_extract(vol_info, entries):
    """写 _extract/NN_卷名.txt"""
    vnum = vol_info["num"]
    if vnum == "00":
        return
    vname = vol_info["name"]
    fname = f"{vnum}_{vname}.txt"
    fpath = OUT / "_extract" / fname
    fpath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(fpath, "w", encoding="utf-8") as f:
        for e in entries:
            # 原文取第一行（避免多行问题）
            first_line = e["original"].split("\n")[0]
            f.write(f'{e["item_id"]}|{first_line}\n')
    
    print(f"  _extract/{fname}: {len(entries)} 条")


def write_registry(all_vols):
    """写 _item_registry.json"""
    records = []
    for vol_info, entries in all_vols:
        for e in entries:
            records.append({
                "item_id": e["item_id"],
                "volume": e["volume"],
                "volume_name": e["volume_name"],
                "volume_type": e["volume_type"],
                "subcategory": e["subcategory"],
                "entry_title": e["entry_title"],
                "original": e["original"][:200],  # 截断避免过大
                "norm": e["original"][:200],
            })
    
    fpath = OUT / "_item_registry.json"
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump({"records": records, "total": len(records)}, f, ensure_ascii=False, indent=2)
    
    print(f"  _item_registry.json: {len(records)} 条")


def write_skeleton_layers(all_vols):
    """为每卷写各层骨架文件（空 records）"""
    layer_dirs = ["ents", "rules", "events", "appts", "rels", "opns", "cits", "mings", "tmes", "regs"]
    
    for vol_info, entries in all_vols:
        vnum = vol_info["num"]
        if vnum == "00":
            continue
        
        for layer in layer_dirs:
            d = OUT / "_layers" / layer
            d.mkdir(parents=True, exist_ok=True)
            fpath = d / f"{layer}_{vnum}.json"
            if not fpath.exists():  # 不覆盖已有文件（如试点的卷一）
                with open(fpath, "w", encoding="utf-8") as f:
                    json.dump({"records": []}, f, ensure_ascii=False, indent=2)


def main():
    print(f"读取源文本: {SRC}")
    text = SRC.read_text(encoding="utf-8")
    
    print("解析卷结构...")
    all_vols = parse_source(text)
    
    total = sum(len(e) for _, e in all_vols)
    print(f"全书共 {total} 条（不含前言）\n")
    
    print("写 _extract/ 文件...")
    for vol_info, entries in all_vols:
        write_extract(vol_info, entries)
    
    print("\n写 _item_registry.json...")
    write_registry(all_vols)
    
    print("\n写各层骨架文件...")
    write_skeleton_layers(all_vols)
    
    print("\n=== 统计 ===")
    for vol_info, entries in all_vols:
        if vol_info["num"] != "00":
            print(f"  {vol_info['name']}: {len(entries)} 条")
    
    print(f"\n总计: {total} 条")
    print("提取完成。")


if __name__ == "__main__":
    main()
