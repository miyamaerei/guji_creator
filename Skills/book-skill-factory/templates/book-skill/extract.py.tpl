# -*- coding: utf-8 -*-
"""「{{title}}」提取薄壳（由 book-skill-factory 模板生成）。

本脚本不含任何书结构判定逻辑，只做三件事：
  1. 从 structure.json 读取工厂引擎位置（source.factory_dir，配置驱动）；
  2. 加载工厂 book-skill-factory/common 参考引擎；
  3. 按 --mode 输出 volumes / full / toc。

用法:
  python scripts/extract.py --mode volumes|full|toc [--out 目录]
"""

import argparse
import json
import os
import sys

INSTANCE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRUCTURE_PATH = os.path.join(INSTANCE_DIR, "structure.json")
BOOK_FILE = r"{{book_path}}"
BOOK_KIND = "{{book_kind}}"


def _load_structure():
    with open(STRUCTURE_PATH, encoding="utf-8") as f:
        return json.load(f)


def _factory_dir():
    """工厂根目录：优先取 structure.json 的 source.factory_dir（生成时记录），
    缺省回退到实例同级目录下的 book-skill-factory。"""
    cfg = _load_structure()
    fd = (cfg.get("source") or {}).get("factory_dir")
    if fd and os.path.isdir(os.path.join(fd, "common")):
        return fd
    return os.path.join(os.path.dirname(INSTANCE_DIR), "book-skill-factory")


sys.path.insert(0, _factory_dir())

from common.input_adapter import load_book  # noqa: E402
from common.parser import parse_book  # noqa: E402
from common.render import (  # noqa: E402
    build_volume_txt,
    build_full_txt,
    build_toc_txt,
    write_files,
)
from common.schemas import validate_structure  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="{{title}} 提取")
    ap.add_argument("--mode", choices=["volumes", "full", "toc"], default="full")
    ap.add_argument("--out", default=INSTANCE_DIR, help="输出目录")
    args = ap.parse_args()

    cfg = _load_structure()
    ok, errors = validate_structure(cfg)
    if not ok:
        sys.exit("structure.json 校验失败: %s" % "; ".join(errors))

    book = cfg.get("source", {}).get("book_path") or BOOK_FILE
    kind = cfg.get("source", {}).get("kind") or BOOK_KIND
    text = load_book(book, kind)

    result = parse_book(text, cfg)
    title = cfg.get("source", {}).get("title", "{{title}}")

    volume_txts = []
    for vname, events in result["volumes"]:
        volume_txts.append((vname, build_volume_txt(title, vname, events)))

    full_txt = build_full_txt(
        title, result["front"], result["toc"], result["volumes"]
    )
    toc_txt = build_toc_txt(title, result["toc"]) if result["toc"] else None

    paths = write_files(args.out, title, volume_txts, full_txt, toc_txt)
    print("写入: %s" % "; ".join(paths))
    print(
        "统计: 卷=%d 标题=%d 段落=%d 字符=%s"
        % (
            len(result["volumes"]),
            sum(1 for _, es in result["volumes"] for e in es if e["type"] == "heading"),
            sum(1 for _, es in result["volumes"] for e in es if e["type"] == "para"),
            cfg.get("stats", {}).get("chars", "?"),
        )
    )


if __name__ == "__main__":
    main()