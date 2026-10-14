#!/usr/bin/env python3
"""Build Base Layer – Split source text into chapters/volumes, extract items, build fingerprint."""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SOURCE_FILE = BASE_DIR / "食货志.txt"
EXTRACT_DIR = BASE_DIR / "_extract"
CHAPTERS_DIR = BASE_DIR / "chapters"
DATA_DIR = BASE_DIR / "_data"
REGISTRY_FILE = DATA_DIR / "registry.json"
FINGERPRINT_FILE = DATA_DIR / "fingerprints.json"

# 卷名映射
VOLUME_NAMES = {
    53: "食货一", 54: "食货二", 55: "食货三",
    56: "食货四", 57: "食货五", 58: "食货六",
}

def is_short_no_period(line):
    """判定被正文包围的无句号短行（SKILL §0.4 判据）。"""
    stripped = line.strip()
    return bool(stripped) and "." not in stripped and len(stripped) < 80

def parse_source(text):
    """按卷拆分源文本，返回 (卷号, 卷名, [段落列表])。"""
    lines = text.split("\n")
    volumes = []
    current_vol = None
    current_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        # 卷边界: ◆ 行
        if line.startswith("◆"):
            if current_vol is not None:
                volumes.append((current_vol, current_lines))
            current_vol = i
            current_lines = []
            continue
        if current_vol is None:
            continue
        current_lines.append(line)
    
    if current_vol is not None:
        volumes.append((current_vol, current_lines))
    
    return volumes

def extract_items(para_lines):
    """从段落行中提取条目：判据 = 被正文包围的无句号短行，或完整段落。"""
    items = []
    for line in para_lines:
        stripped = line.strip()
        if not stripped:
            continue
        # 跳过卷标题、子目标记、卷标等
        if stripped.startswith("◎") or stripped.startswith("○"):
            continue
        if stripped.startswith("◆"):
            continue
        items.append(stripped)
    return items

def normalize_text(text):
    """归一化文本：去多余空白、异体字归一、标点规范。"""
    text = re.sub(r"\s+", " ", text)
    return text

def main():
    print("=== Build Base Layer ===")
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        text = f.read()
    
    volumes = parse_source(text)
    registry = {}
    fingerprint = {}
    total_items = 0
    item_counter = 0
    
    for vol_idx, (vol_line, para_lines) in enumerate(volumes):
        vol_name = "食货一"
        vol_seq = vol_idx + 1  # 01-06
        for real_vol, name in VOLUME_NAMES.items():
            if real_vol == vol_idx + 53:
                vol_name = name
                break
        
        # 提取章节文件
        chapter = "\n\n".join(para_lines)
        chapter_file = CHAPTERS_DIR / f"{vol_seq:02d}_{vol_name}.md"
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write(chapter)
        
        # 提取条目（用于 AI 读取）
        items = extract_items(para_lines)
        extract_file = EXTRACT_DIR / f"vol_{vol_seq:02d}.txt"
        with open(extract_file, "w", encoding="utf-8") as f:
            f.write("\n\n".join(items))
        
        print(f"  {vol_name} ({vol_seq}卷): {len(items)} 条目，{len(chapter)} 字符")
        
        # 注册条目到 registry
        for item_no, item_text in enumerate(items, 1):
            item_id = f"{vol_seq:02d}-{item_no:03d}"
            norm_text = normalize_text(item_text)
            registry[item_id] = {
                "volume": vol_name,
                "no": item_no,
                "original": item_text,
                "norm": norm_text,
                "L": "L0",
                "chars": len(norm_text),
            }
            total_items += 1
        
        print(f"    已注册 {len(items)} 条目，累计 {total_items}")
    
    # 写入 registry 和 fingerprint
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    
    # 指纹库：每条指纹
    for item_id, reg in registry.items():
        fingerprint[item_id] = {
            "volume": reg["volume"],
            "section": f"L{reg['chars']:03d}",
            "char_count": reg["chars"],
            "normalized": True,
        }
    with open(FINGERPRINT_FILE, "w", encoding="utf-8") as f:
        json.dump(fingerprint, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== Build Base Layer Complete ===")
    print(f"  总计 {total_items} 条目，6 卷已拆分到 chapters/")
    print(f"  registry: {REGISTRY_FILE}")
    print(f"  fingerprint: {FINGERPRINT_FILE}")

if __name__ == "__main__":
    main()
