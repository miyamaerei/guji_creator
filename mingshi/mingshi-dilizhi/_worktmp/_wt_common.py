# -*- coding: utf-8 -*-
"""卷01 生成器公共模块：registry 加载 + 子串断言 + 中文数字转换 + 文件写出。"""

import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, "scripts")

with io.open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8") as f:
    REG = json.load(f)


def norm(iid):
    return REG[iid]["norm"]


def need(iid, s, what):
    if s and s not in norm(iid):
        raise AssertionError("%s %s 未命中: %r" % (iid, what, s))


def need_all(iid, pairs):
    for s, what in pairs:
        need(iid, s, what)


_DIGITS = "零一二三四五六七八九"
_UNITS = {"十": 10, "百": 100, "千": 1000}


def cn2int(s):
    """中文数字 → int：三十三万四千七百九十二→334792；支持 万/亿 分段。"""
    result = 0
    section = 0
    num = 0
    for ch in s:
        if ch in _DIGITS:
            num = _DIGITS.index(ch)
        elif ch in _UNITS:
            section += (num if num else 1) * _UNITS[ch]
            num = 0
        elif ch == "万":
            result += (section + num) * 10000
            section = 0
            num = 0
        elif ch == "亿":
            result += (section + num) * 100000000
            section = 0
            num = 0
    return result + section + num


def check_number(iid, phrase, raw):
    """校验：phrase 是 raw 的核心数字短语，且 raw 命中 norm。返回 int。"""
    if phrase not in raw:
        raise AssertionError("%s 数字短语 %r 不在 raw %r 中" % (iid, phrase, raw))
    need(iid, raw, "raw")
    return cn2int(phrase)


HEAD = "# -*- coding: utf-8 -*-\n"
ATTR = getattr


def write_layer(varname, docs, header_note, transform):
    """docs：无 slot 的记录列表；transform(r) 返回无 slot dict；按顺序编 slot 并写文件。"""
    recs = []
    for i, doc in enumerate(docs, 1):
        r = transform(doc)
        r = dict(r)
        r["slot"] = i
        recs.append(r)
    body = "\n".join("    %r," % r for r in recs)
    text = HEAD + header_note + "\n" + varname + " = [\n" + body + "\n]\n"
    # 序列化用 repr 会产生单引号 dict；改用 pprint 保留字段顺序
    import pprint

    buf = io.StringIO()
    buf.write(HEAD)
    buf.write(header_note)
    buf.write("\n")
    buf.write(varname)
    buf.write(" = ")
    pprint.pprint(recs, stream=buf, width=120, sort_dicts=False)
    buf.write("\n")
    with io.open(os.path.join(SCRIPTS, filename(varname)), "w", encoding="utf-8") as f:
        f.write(buf.getvalue())
    print("%s -> %d 条" % (varname, len(recs)))
    return recs


def filename(varname):
    return {
        "ENTITIES": "_ents_ai_01.py",
        "TME_AI": "_tme_ai_01.py",
        "GEO_AI": "_geo_ai_01.py",
        "EVO_AI": "_evo_ai_01.py",
        "HYD_AI": "_hyd_ai_01.py",
        "GAR_AI": "_gar_ai_01.py",
        "RES_AI": "_res_ai_01.py",
    }[varname]
