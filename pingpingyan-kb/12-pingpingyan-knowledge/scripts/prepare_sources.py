# -*- coding: utf-8 -*-
"""《平平言》实例源文件准备脚本（一次性，可重跑）——12-pingpingyan-knowledge

作用：
1. 核验 pingpingyan-kb/原文 与 白话文/ 各 txt 的编码（UTF-8 优先，回退 GBK）；
2. 按原书顺序生成 UTF-8 合并版原文/白话文（唯一权威来源 + 对照引用源）；
3. 将各卷拆分 txt 复制为 UTF-8 到 assets/sources/（切分主源）。

注意：工程根原有 `原文/平平言_原文_全卷合并.txt` 为 GBK 编码（Windows 下直接读会乱码），
本实例内一律使用本脚本生成的 UTF-8 合并版。
"""
import io
import os
import shutil
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 12-pingpingyan-knowledge/
KB = os.path.dirname(BASE)  # pingpingyan-kb/
SRC_DIR = os.path.join(BASE, "assets", "sources")


def decode(path):
    """严格解码：UTF-8 优先，回退 GBK。返回 (text, encoding)。"""
    with open(path, "rb") as f:
        raw = f.read()
    for enc in ("utf-8", "gbk"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    raise ValueError(f"无法解码（非 UTF-8/GBK）：{path}")


def read_lines(path):
    text, enc = decode(path)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln for ln in text.split("\n") if ln.strip()]
    return lines, enc


def write_utf8(path, text):
    tmp = path + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)  # 临时文件 + rename 落盘


def merge(files, header, out):
    parts = [header]
    for f in files:
        lines, enc = read_lines(f)
        parts.append("")
        parts.append("=" * 60)
        parts.append(f)
        parts.append("=" * 60)
        parts.extend(lines)
    write_utf8(out, "\n".join(parts) + "\n")
    return out


def main():
    os.makedirs(SRC_DIR, exist_ok=True)

    yuanwen = os.path.join(KB, "原文")
    baihua = os.path.join(KB, "白话文")

    yw_files = [
        os.path.join(yuanwen, "序.txt"),
        os.path.join(yuanwen, "凡例.txt"),
        os.path.join(yuanwen, "卷一.txt"),
        os.path.join(yuanwen, "卷二.txt"),
        os.path.join(yuanwen, "卷三.txt"),
        os.path.join(yuanwen, "卷四.txt"),
        os.path.join(yuanwen, "跋.txt"),
    ]
    bh_files = [
        os.path.join(baihua, "序_白话.txt"),
        os.path.join(baihua, "凡例_白话.txt"),
        os.path.join(baihua, "卷一_白话.txt"),
        os.path.join(baihua, "卷二_白话.txt"),
        os.path.join(baihua, "卷三_白话.txt"),
        os.path.join(baihua, "卷四_白话.txt"),
        os.path.join(baihua, "跋_白话.txt"),
    ]

    print("== 编码核验 ==")
    for f in yw_files + bh_files:
        if os.path.exists(f):
            text, enc = decode(f)
            print(f"{os.path.basename(f):<24} {enc}  字符数 {len(text)}")
        else:
            print(f"缺失: {f}")

    # 1) UTF-8 合并版原文（唯一权威来源）
    merged_yw = merge(
        yw_files,
        "平平言（原文全卷合并）\n（清·方大湜 撰，官箴书，序、凡例、四卷及跋按原书顺序合并）",
        os.path.join(SRC_DIR, "平平言_原文_全卷合并.txt"),
    )
    # 2) UTF-8 合并版白话文（对照引用源，不参与抽取）
    merged_bh = merge(
        bh_files,
        "平平言（白话文全卷合并）\n（对照引用源，不参与抽取）",
        os.path.join(SRC_DIR, "平平言_白话文_全卷合并.txt"),
    )
    # 3) 卷拆分 txt（切分主源）
    for f in yw_files + bh_files:
        lines, enc = read_lines(f)
        dst = os.path.join(SRC_DIR, os.path.basename(f))
        write_utf8(dst, "\n".join(lines) + "\n")
        print(f"复制为 UTF-8: {dst}")

    print(f"\n合并原文 -> {merged_yw}")
    print(f"合并白话 -> {merged_bh}")
    print("完成。")


if __name__ == "__main__":
    sys.exit(main())
