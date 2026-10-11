# -*- coding: utf-8 -*-
"""book-skill-factory common/render.py

渲染参考模板：把统一事件流渲染成每卷 txt / 全本 / 目录。
不关心具体书，只消费 schema 化的事件。
"""

import os


def build_volume_txt(book_title, volume_name, events):
    lines = [book_title, "=" * 24, volume_name, "=" * 24]
    for ev in events:
        if ev["type"] == "heading":
            lines.append(
                ("# " if ev.get("level", 1) <= 1 else "# " * min(ev["level"], 3))
                + ev["text"]
            )
        else:
            lines.append(ev["text"].strip())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_toc_txt(book_title, toc_lines):
    lines = [book_title, "=" * 24, "目录", "=" * 24]
    for vname, headings in toc_lines:
        lines.append(vname)
        for h in headings:
            lines.append("    " + h)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_full_txt(book_title, front_lines, toc_lines, volumes_events):
    lines = [book_title, "=" * 24]
    if toc_lines:
        lines += ["目录", "=" * 24]
        for vname, headings in toc_lines:
            lines.append(vname)
            for h in headings:
                lines.append("    " + h)
            lines.append("")
    for vname, events in volumes_events:
        lines += ["", "=" * 24, vname, "=" * 24, ""]
        for ev in events:
            if ev["type"] == "heading":
                lines.append(
                    ("# " if ev.get("level", 1) <= 1 else "# " * min(ev["level"], 3))
                    + ev["text"]
                )
            else:
                lines.append(ev["text"].strip())
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_files(out_dir, base_name, volumes_txt, full_txt, toc_txt=None):
    """落盘：每卷 txt + 全本（可选目录）。返回路径列表。"""
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for vname, text in volumes_txt:
        safe = vname.replace("/", "_").replace("\\", "_")
        p = os.path.join(out_dir, "%s_%s.txt" % (base_name, safe))
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        paths.append(p)
    if toc_txt:
        p = os.path.join(out_dir, "%s_目录.txt" % base_name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(toc_txt)
        paths.append(p)
    p = os.path.join(out_dir, "%s_全本.txt" % base_name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(full_txt)
    paths.append(p)
    return paths
