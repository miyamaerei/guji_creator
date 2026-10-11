# -*- coding: utf-8 -*-
"""book-skill-factory common/parser.py

四级结构解析参考模板：按 structure.json 配置把正文切分为
目录区 -> 卷 -> 标题条目 -> 段落（事件流）。

所有判定依赖配置：
  toc_anchor / body_anchor / volume_pattern(kind/pattern/names) /
  heading_kind / heading_pattern / keep_pages / omit_lines / strip_artifacts

事件流元素：{"type":"heading","level":1,"text":…} / {"type":"para","text":…}
           / {"type":"table","text":…} / {"type":"page","text":…}
不针对任何书；书的差异全部由配置表达。
"""

import re

from .cleaner import clean_text, clean_table, should_drop_line, strip_export_artifacts


def _compile_heading_matcher(heading_kind, heading_pattern):
    """按 heading_kind 编译标题行匹配器。plain=用 heading_pattern；h1/h2/h3=井号层数。"""
    if heading_kind in (None, "none"):
        return (lambda s: False), (lambda s: s.strip())
    if heading_kind == "plain":
        rx = re.compile(heading_pattern, re.M)
    else:
        weight = {"h1": 1, "h2": 2, "h3": 3}.get(heading_kind, 2)
        rx = re.compile(r"^%s(?!%s)\s*(.+?)\s*$" % ("#" * weight, "#" * weight), re.M)

    def is_heading(line):
        return bool(rx.match(line))

    def get_heading(line):
        m = rx.match(line)
        return m.group(1).strip() if m else line.strip()

    return is_heading, get_heading


_CN_NUM_OR_DIGIT = re.compile(r"卷[一二三四五六七八九十百零〇0-9]+")


def _extract_volume_name(m_text, m):
    if m.groupdict() and m.groupdict().get("name"):
        return m.groupdict()["name"].strip()
    hit = _CN_NUM_OR_DIGIT.search(m_text)
    if hit:
        return hit.group(0)
    return m_text.strip()


def _compile_volume_patterns(vp):
    pat = vp.get("pattern") or []
    if isinstance(pat, str):
        pat = [pat]
    rxs = []
    for p in pat:
        try:
            rxs.append(re.compile(p, re.M))
        except re.error:
            continue
    return rxs


def split_volumes(body, volume_pattern):
    """按配置把正文切成 [(卷名, 卷内文本块), ...]。

    kind:
      regex_match -> 多形态候选正则扫描全部卷标记，按出现位置排序切分；
                     第一个标记前的文本单独成段（无名，由上层注入首卷名）。
      fixed_list  -> 按 names 顺序出现的位次切分。
      none/缺省   -> 整本单卷 ("", body)。
    """
    if not volume_pattern or volume_pattern.get("kind") in ("none", None):
        return [("", body)]
    if volume_pattern.get("kind") == "fixed_list":
        return _split_by_fixed_list(body, volume_pattern.get("names") or [])
    return _split_by_regex(body, _compile_volume_patterns(volume_pattern))


def _split_by_regex(body, rxs):
    if not rxs:
        return [("", body)]
    marks = []
    for rx in rxs:
        for m in rx.finditer(body):
            marks.append((m.start(), m.end(), _extract_volume_name(m.group(0), m)))
    if not marks:
        return [("", body)]
    marks.sort(key=lambda t: t[0])
    uniq = []
    for pos, end, name in marks:
        if uniq and uniq[-1][0] == pos:
            continue
        uniq.append((pos, end, name))
    volumes = []
    if uniq[0][0] > 0:
        volumes.append(("", body[: uniq[0][0]]))
    for i, (pos, end, name) in enumerate(uniq):
        chunk_end = uniq[i + 1][0] if i + 1 < len(uniq) else len(body)
        volumes.append((name, body[end:chunk_end]))
    return volumes


def _split_by_fixed_list(body, names):
    if not names:
        return [("", body)]
    positions = [body.find(n) for n in names]
    volumes = []
    for i, name in enumerate(names):
        start = positions[i]
        end = (
            positions[i + 1]
            if i + 1 < len(positions) and positions[i + 1] > start
            else len(body)
        )
        chunk = body[start:end]
        if chunk.startswith(name):
            chunk = chunk[len(name) :]
        volumes.append((name, chunk))
    return volumes


def parse_volume(block, layout, keep_pages=False):
    """把一个卷的文本块解析成事件流。"""
    heading_kind = layout.get("heading_kind")
    heading_pattern = layout.get("heading_pattern") or r"^##+(?!#)\s*(.+?)\s*$"
    is_heading, get_heading = _compile_heading_matcher(heading_kind, heading_pattern)
    omit = layout.get("omit_lines") or []

    rx_page = re.compile(
        r"^\s*(?:第\s*[一二三四五六七八九十百千0-9]+\s*页|[-—]?\s*\d+\s*[-—]?)\s*$"
    )

    events = []
    buf = []

    def flush_para():
        nonlocal buf
        t = "\n".join(buf).strip()
        buf = []
        if t:
            events.append(_classify(t))

    for raw in block.split("\n"):
        line = raw.strip()
        if should_drop_line(raw, omit):
            continue
        if not line:
            flush_para()
            continue
        if rx_page.match(line):
            flush_para()
            if keep_pages:
                events.append({"type": "page", "text": line})
            continue
        if is_heading(line):
            flush_para()
            events.append({"type": "heading", "level": 1, "text": get_heading(line)})
            continue
        buf.append(line)

    flush_para()
    return events


def _classify(text):
    if "\n" not in text and "|" in text:
        return {"type": "table", "text": clean_table(text)}
    return {"type": "para", "text": clean_text(text)}


def get_headings(events):
    return [e for e in events if e["type"] == "heading"]


def get_paras(events):
    return [e for e in events if e["type"] == "para"]


def count_paras(events):
    return sum(1 for e in events if e["type"] == "para")


def count_chars(events):
    total = 0
    for e in events:
        t = e["text"]
        if e["type"] == "table":
            t = re.sub(r"<TABLE>|</TABLE>|\|", "", t)
        elif e["type"] == "heading":
            continue
        total += len(re.sub(r"\s", "", t))
    return total


def _infer_first_volume_name(layout):
    ba = layout.get("body_anchor") or {}
    hit = _CN_NUM_OR_DIGIT.search(ba.get("pattern") or "")
    if hit:
        return hit.group(0)
    vp = layout.get("volume_pattern") or {}
    if vp.get("kind") == "fixed_list" and vp.get("names"):
        return vp["names"][0]
    return None


def _parse_toc(toc_lines, layout):
    """把目录区文本解析为 [(卷名, [标题, ...]), ...]。"""
    vp = layout.get("volume_pattern") or {}
    vrx = None
    if vp.get("kind") == "fixed_list" and vp.get("names"):
        vrx = re.compile("|".join(re.escape(n) for n in vp["names"] if n))
    elif vp.get("kind") != "none":
        rxs = _compile_volume_patterns(vp)
        if rxs:
            vrx = re.compile("|".join(rx.pattern for rx in rxs))

    heading_kind = layout.get("heading_kind")
    heading_pattern = layout.get("heading_pattern") or r"^##+(?!#)\s*(.+?)\s*$"
    is_heading, get_heading = _compile_heading_matcher(heading_kind, heading_pattern)

    result = []
    current = None
    bare = re.compile(r"卷[一二三四五六七八九十百零〇0-9]+")

    def find_vol_marker(line):
        if vrx:
            m = vrx.search(line)
            if m:
                hit = bare.search(m.group(0)) or bare.search(line)
                return (hit.group(0) if hit else m.group(0).strip(), m)
        m = bare.search(line)
        if m:
            return (m.group(0), m)
        return None

    for raw in toc_lines.split("\n"):
        line = raw.strip()
        if not line:
            continue
        marker = find_vol_marker(line)
        if marker:
            name, m = marker
            rest = (line[: m.start()] + line[m.end() :]).strip(" #|:")
            if rest and is_heading(rest):
                rest = get_heading(rest)
            result.append([name, [rest] if rest else []])
            current = name
            continue
        t = get_heading(line) if is_heading(line) else line
        if current is not None:
            result[-1][1].append(t)
        else:
            result.append(["", [t]])
    return [(v, hs) for v, hs in result]


def parse_book(text, layout):
    """整书解析：目录区 + 正文区 + 每卷事件流。返回 dict(front/toc/toc_raw/volumes)。"""
    if layout.get("strip_artifacts", True):
        text = strip_export_artifacts(text)

    body_anchor = layout.get("body_anchor") or {}
    toc_anchor = layout.get("toc_anchor") or {}

    body_start = len(text)
    if body_anchor.get("pattern"):
        m = re.search(body_anchor["pattern"], text)
        if m:
            body_start = m.end()

    toc_raw = ""
    if toc_anchor.get("pattern"):
        m = re.search(toc_anchor["pattern"], text)
        if m:
            toc_start = m.end()
            toc_end = body_start
            if toc_anchor.get("end_exclusive"):
                m2 = re.search(toc_anchor["end_exclusive"], text[toc_start:])
                if m2:
                    toc_end = toc_start + m2.start()
            toc_raw = text[toc_start:toc_end]

    body = text[body_start:]
    volumes = split_volumes(body, layout.get("volume_pattern"))
    inferred = _infer_first_volume_name(layout)
    if inferred and volumes and volumes[0][0] == "":
        volumes = [(inferred, volumes[0][1])] + volumes[1:]
    volumes_events = []
    for name, block in volumes:
        volumes_events.append(
            (name, parse_volume(block, layout, layout.get("keep_pages", False)))
        )

    return {
        "front": text[:body_start],
        "toc": _parse_toc(toc_raw, layout) if toc_raw.strip() else [],
        "toc_raw": toc_raw,
        "volumes": volumes_events,
    }
