# -*- coding: utf-8 -*-
"""book-skill-factory common/input_adapter.py

输入归一化参考模板：把 txt/md/z-library JSON/epub 统一读成纯文本 str。
只做格式归一，不解析结构。
"""

import json
import os
import re


def _detect_encoding(raw):
    for enc in ("utf-8-sig", "utf-8", "gb18030", "gbk"):
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("utf-8", errors="ignore")


def _from_zlib_json(data):
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        parts = [
            item["markdown"]
            for item in data
            if isinstance(item, dict) and item.get("markdown")
        ]
        if parts:
            return "\n\n".join(parts)
    if isinstance(data, dict):
        if data.get("markdown"):
            return data["markdown"]
        chapters = data.get("chapters") or data.get("sections")
        if isinstance(chapters, list):
            out = []
            for ch in chapters:
                if isinstance(ch, dict):
                    t = ch.get("title")
                    c = ch.get("content") or ch.get("text")
                    out.append(("# %s\n\n" % t if t else "") + (c or ""))
            if out:
                return "\n\n".join(out)
    raise ValueError("无法从该 JSON 结构中提取文本")


def load_book(path, kind=None):
    """读取一本书并返回归一化纯文本。kind: auto|txt|md|json|epub"""
    path = str(path)
    kind = (kind or "auto").lower()
    if kind == "auto":
        ext = os.path.splitext(path)[1].lower()
        kind = "json" if ext == ".json" else ("epub" if ext == ".epub" else "txt")

    if kind == "json":
        with open(path, "rb") as f:
            raw = f.read()
        try:
            data = json.loads(raw.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            data = json.loads(_detect_encoding(raw))
        return _from_zlib_json(data)

    if kind == "epub":
        import zipfile
        from xml.etree import ElementTree as ET

        out = []
        with zipfile.ZipFile(path) as zf:
            names = [
                n for n in zf.namelist() if n.endswith((".xhtml", ".html", ".htm"))
            ]
            names.sort()
            for n in names:
                try:
                    root = ET.fromstring(zf.read(n))
                except Exception:
                    continue
                for el in root.iter():
                    if el.tag.split("}")[-1] in ("script", "style"):
                        el.clear()
                text = "".join(root.itertext())
                text = re.sub(r"\s+", " ", text).strip()
                if text:
                    out.append(text)
        if not out:
            raise ValueError("EPUB 中未解析到正文: %s" % path)
        return "\n\n".join(out)

    with open(path, "rb") as f:
        raw = f.read()
    return _detect_encoding(raw)
