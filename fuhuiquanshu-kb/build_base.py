# -*- coding: utf-8 -*-
"""福惠全书底座切分 v2：条目=卷首列表标题（权威，含总论/余论/说）；正文 ○段 匹配列表标题则开新条、否则并入；
△款目（文书式/分节）不独立成条（DOC/流程层建模）；禀启附=卷33（按篇成条）。"""
import io, os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "原文")
OUT = os.path.join(ROOT, "_item_registry.json")

VOL_FILES = {}
for f in sorted(os.listdir(SRC)):
    m = re.match(r"卷之([一二三四五六七八九十]+)\.txt$", f)
    if m:
        num = m.group(1)
        cn = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
              "十": 10, "十一": 11, "十二": 12, "十三": 13, "十四": 14, "十五": 15, "十六": 16,
              "十七": 17, "十八": 18, "十九": 19, "二十": 20, "二十一": 21, "二十二": 22,
              "二十三": 23, "二十四": 24, "二十五": 25, "二十六": 26, "二十七": 27, "二十八": 28,
              "二十九": 29, "三十": 30, "三十一": 31, "三十二": 32}[num]
        VOL_FILES[cn] = os.path.join(SRC, f)
# 禀启附 = 卷33
FULU = os.path.join(SRC, "禀启附.txt")

DEPT_RE = re.compile(r"^(筮仕|莅任|钱谷|杂课|编审|清丈|刑名|保甲|典礼|教养|荒政|邮政|庶政|升迁)部[一二三四五六七八九十]?$")
AUTHOR_RE = re.compile(r"黄六鸿")

def clean(s):
    return re.sub(r"\s+", "", s)

def parse_volume(cn, path, is_fu=False):
    s = io.open(path, encoding="utf-8").read()
    if not is_fu:
        s = re.sub(r"【福惠全书卷之[^】]+】", "", s, count=1)
    else:
        s = re.sub(r"【禀启附】", "", s, count=1)
    first_o = s.find("○")
    head = s[:first_o] if first_o >= 0 else s
    body = s[first_o:] if first_o >= 0 else ""
    list_titles = []
    for line in head.splitlines():
        t = clean(line)
        if not t or t.startswith("◆"):
            continue
        if AUTHOR_RE.search(t):
            continue
        if DEPT_RE.match(t):
            continue
        list_titles.append(t)
    # 一卷两部的补列表：正文区中 ◆部名 后紧跟的连续列表行（如卷08 ◆杂课部 后 总论/颜料匠班…杂征余论）
    # 只收无符号行；遇 ○/△/◆/部名/作者行即止。
    body_lines = body.splitlines()
    for i, ln in enumerate(body_lines):
        if clean(ln).startswith("◆"):
            j = i + 1
            while j < len(body_lines):
                t = clean(body_lines[j])
                if not t or t.startswith(("◆", "○", "△")):
                    break
                if DEPT_RE.match(t) or AUTHOR_RE.search(t):
                    break
                if t not in list_titles:
                    list_titles.append(t)
                j += 1
    if not body:
        return list_titles, []
    segs = re.split(r"(○)", body)
    segments = []
    cur = ""
    for part in segs:
        if part == "○":
            if cur.strip():
                segments.append(cur)
            cur = part
        else:
            cur += part
    if cur.strip():
        segments.append(cur)
    items = []
    for seg in segments:
        if not seg.startswith("○"):
            continue
        t = seg[1:]
        m = re.match(r"^([\u4e00-\u9fff·]{2,12})", t)
        items.append({"title": m.group(1) if m else "", "seg": seg})
    # 条目：○段标题 == 列表标题 或 列表标题以段首标题开头（如 出堂规 ⊂ 出堂规式附）→ 开新条；
    # 段首标题是列表标题的超集（逃人不宜有窝 ⊃ 逃人）= 条内肯綮小节 → 并入
    final = []
    for it in items:
        t = it["title"]
        hit = False
        if t:
            for x in list_titles:
                if t == x or (x.startswith(t) and len(t) >= 2):
                    hit = True
                    break
        if hit:
            final.append({"title": t, "text": it["seg"][1 + len(t):]})
        else:
            if final:
                final[-1]["text"] += it["seg"]
            else:
                final.append({"title": t or "(首)", "text": it["seg"]})
    return list_titles, final

def main():
    registry = {}
    diag = []
    total = 0
    vols = sorted(VOL_FILES)
    for cn in vols:
        lt, items = parse_volume(cn, VOL_FILES[cn])
        for seq, it in enumerate(items, 1):
            item_id = "%02d-%03d" % (cn, seq)
            registry[item_id] = {"original": it["title"] + it["text"], "norm": it["title"]}
        total += len(items)
        flag = "" if len(lt) == len(items) else "  << 差异!"
        diag.append("卷%02d: 列表 %d / 条目 %d%s" % (cn, len(lt), len(items), flag))
        if len(lt) != len(items):
            diag.append("  列表=%s" % "|".join(lt))
            diag.append("  条目=%s" % "|".join(x["title"] for x in items))
    lt, items = parse_volume(33, FULU, is_fu=True)
    for seq, it in enumerate(items, 1):
        item_id = "33-%03d" % seq
        registry[item_id] = {"original": it["title"] + it["text"], "norm": it["title"]}
    total += len(items)
    diag.append("卷33(禀启附): 列表 %d / 条目 %d%s" % (len(lt), len(items), "" if len(lt) == len(items) else "  << 差异!"))
    if len(lt) != len(items):
        diag.append("  列表=%s" % "|".join(lt[:30]))
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(registry, ensure_ascii=False, indent=1))
    if not os.path.isdir(os.path.join(ROOT, "_build")):
        os.makedirs(os.path.join(ROOT, "_build"))
    io.open(os.path.join(ROOT, "_build", "base_diag.txt"), "w", encoding="utf-8").write("\n".join(diag))
    print("\n".join(diag))
    print("TOTAL:", total)

if __name__ == "__main__":
    main()
