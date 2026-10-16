# -*- coding: utf-8 -*-
"""
书籍json 精简契约回填器（book-json/1.1）

用法：
    python tools/book_json_augment.py            # 全部书（跳过 EXCLUDE）
    python tools/book_json_augment.py 客座赘语 治谱   # 只处理指定书名
    python tools/book_json_augment.py --check    # 只跑校验+打印将要写的 meta，不落盘

处理对象：每本 `<书>/书籍json/<书>_校对版.json`（明一统志为 `<书>.json`，本轮跳过）。

meta 补 7 项（全部机采，其余字段一律不动）：
    契约 / book_id / 著者 / 朝代 / 体裁 / 成书年 / 底本版本(+_来源) / 数字化 / 条字段(实测键名)
    身份三列取自 Summary/html/data.js books[]（唯一真相源）
    底本版本取自 registry.md「底本=」，无则退到本书实例 SKILL.md/README.md 的「底本=」声明
    数字化取自实测：条 text 前 60 字（去空白）对书目录内 txt 候选求包含率，单文件≥90% 记单文件，
      否则同目录 txt 合并≥90% 记分卷目录（含 文件数），再否则填 null + candidates
item 补 1 项：level = item | volume-fallback（id 尾号 000 者）；预留 sections 字段位（有则校验，无则不建）
三条校验：
    V1 id 全局唯一 + 卷内条号连续（跳号记 WARN）
    V2 卷级兜底条（-000）不计入 条目总数（只取 level=item）
    V3 sections 区间必须落在本条 text 内、不重叠
原则：测不出来的填 null 并写 `*_依据` / `*_来源`（lookedFor / candidates），不猜。
"""
import io
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
CONTRACT = "book-json/1.1"

# 明一统志按用户指示本轮跳过（体量大，另议）
EXCLUDE = {"明一统志"}

DATA_JS = os.path.join(ROOT, "Summary", "html", "data.js")
REGISTRY_MD = os.path.join(ROOT, "Skills", "00-book-knowledge-factory", "references", "registry.md")


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, doc):
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)


def read_text(path):
    with io.open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


# ---------- ① 身份来源：Summary/html/data.js（单点真相，不另存） ----------

def load_identities():
    if not os.path.isfile(DATA_JS):
        return {}
    t = read_text(DATA_JS)
    out = {}
    pat = re.compile(
        r'\{\s*id:"([A-Za-z_]+)",\s*dir:"([^"]+)",\s*title:"([^"]*)",\s*author:"([^"]*)",\s*genre:"([^"]*)"')
    for m in pat.finditer(t):
        bid, d, title, author, genre = m.groups()
        out[d] = {"book_id": bid, "title": title, "author": author, "genre": genre}
    return out


# ---------- ② 版本来源：工厂实例台账 registry.md 的「底本=」 ----------

def load_base_editions():
    if not os.path.isfile(REGISTRY_MD):
        return {}
    out = {}
    for line in read_text(REGISTRY_MD).splitlines():
        if not line.startswith("|"):
            continue
        hits = re.findall(r"底本\s*=\s*([^；)）|】]+)", line)
        if not hits:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        book = cells[1].split("（")[0].strip()
        cur = out.get(book)
        joined = _clean_base(hits[0])
        if joined and (cur is None or len(joined) > len(cur)):
            out[book] = joined
    return out


def _clean_base(v):
    if not v:
        return None
    v = re.sub(r"\]\([^)]*\)", "", v)          # markdown 链接尾巴
    v = re.sub(r"[*`#|]+", "", v)
    v = re.split(r"(?:，|\s)?来源\s|UTF-?8|\d{4,}\s*字节", v)[0]
    v = v.strip().strip("，,、；;：: /）)】]")
    while v and v[-1] in "（(":
        v = v[:-1]
    return v.strip("，,、；; ") or None


BASE_DEC = re.compile(r"底本\s*[=为：:]\s*([^\n]{2,140})")


def declared_base(book_dir):
    """书目录（含 NN-*-knowledge 实例目录）里 SKILL.md/README.md 的「底本=」声明 → (值, 来源相对路径)"""
    docs = []
    for root, dirs, files in os.walk(book_dir):
        dirs[:] = [d for d in dirs if not d.startswith(("_", ".")) and d not in ("书籍json", "分卷json", "node_modules")]
        for fn in ("SKILL.md", "README.md"):
            if fn in files:
                docs.append(os.path.join(root, fn))
    for p in sorted(docs, key=lambda x: (0 if x.endswith("SKILL.md") else 1, len(x))):
        for line in read_text(p).splitlines():
            m = BASE_DEC.search(line)
            if not m:
                continue
            v = re.sub(r"[*`]+", "", m.group(1)).strip().strip("，,、 ")
            v = re.split(r"[。；]", v)[0].strip()
            if len(v) >= 2:
                return _clean_base(v), os.path.relpath(p, ROOT).replace("\\", "/") + " 行内「底本=」声明"
    return None, None


# ---------- ③ 数字化：按"文本包含率"选底座文件/分卷目录（不靠猜路径） ----------

SKIP_SRC = re.compile(r"(白话|译文|翻译|对照|报告|说明|校记|勘误|记译|清单)")
# 同等命中时优先「随实例存放的源文件」，其次校对/原文，最后中间切条产物
RANK_SRC = [
    ("assets/sources", 0),
    ("/原文", 1),
    ("/校对", 1),
    ("_extract", 3),
    ("_backup", 9),
]


def rank_of(rel):
    best = 5
    for pat, r in RANK_SRC:
        if pat in rel:
            best = min(best, r)
    return best


def find_txt_candidates(book_dir, limit_bytes=24 * 1024 * 1024):
    out = []
    for root, dirs, files in os.walk(book_dir):
        dirs[:] = [d for d in dirs
                   if d not in ("书籍json", "分卷json", "node_modules", ".git") and not SKIP_SRC.search(d)]
        for fn in files:
            if not fn.lower().endswith(".txt") or SKIP_SRC.search(fn):
                continue
            p = os.path.join(root, fn)
            try:
                if os.path.getsize(p) > limit_bytes:
                    continue
            except OSError:
                continue
            out.append(p)
    return out


def _probes(items, n=60, least=30):
    ps = []
    for it in items:
        t = re.sub(r"\s+", "", it.get("text") or "")
        if len(t) >= least:
            ps.append(t[:n])
    return ps


def digitize(book_dir, items):
    ps = _probes(items)
    total = len(ps)
    cands = find_txt_candidates(book_dir)
    hay = {}
    scored = []
    for p in cands:
        try:
            txt = read_text(p)
        except Exception:
            continue
        hay[p] = re.sub(r"\s+", "", txt)
        hit = sum(1 for q in ps if q in hay[p])
        scored.append((hit, -rank_of(os.path.relpath(p, ROOT).replace("\\", "/")), p))

    groups = {}
    for p in cands:
        groups.setdefault(os.path.dirname(p), []).append(p)
    bundles = []
    for d, fl in groups.items():
        h = "".join(hay.get(p) or re.sub(r"\s+", "", read_text(p)) for p in fl)
        bundles.append((sum(1 for q in ps if q in h), rank_of(os.path.relpath(d, ROOT).replace("\\", "/")), d, fl))

    scored.sort(key=lambda x: (-x[0], x[1]))
    bundles.sort(key=lambda x: (-x[0], x[1]))
    pick = None
    if scored and scored[0][0] >= 0.9 * total:
        hit, _, p = scored[0]
        pick = (hit, [p], "单文件")
    elif bundles and bundles[0][0] >= 0.9 * total:
        hit, _, d, fl = bundles[0]
        pick = (hit, fl, "分卷目录")
    if pick is None:
        cand_txt = "; ".join(
            ["%s 单文件%d/%d" % (os.path.relpath(p, ROOT).replace("\\", "/"), h, total) for h, _, p in scored[:2]] +
            ["%s 目录合并%d/%d(%d txt)" % (os.path.relpath(d, ROOT).replace("\\", "/"), hb, total, len(fl))
             for hb, _, d, fl in bundles[:2]])
        return {
            "文件": None, "字节": None, "行数": None, "全角标点": None,
            "探针数": total,
            "依据": "无候选达 90% 包含率，不猜。lookedFor=书目录内 .txt（排除白话/对照/记译/清单与 书籍json、分卷json）；"
                    "探针=条 text 前 60 字去空白；candidates=" + (cand_txt or "无 txt 候选"),
        }
    hit, files, kind = pick
    txts = [read_text(p) for p in files]
    punc = sum(len(re.findall(r"[。，、；：？！]", t)) for t in txts)
    rel = [os.path.relpath(p, ROOT).replace("\\", "/") for p in files]
    out = {
        "文件": rel[0] if kind == "单文件" else os.path.dirname(rel[0]) or ".",
        "形态": kind,
        "字节": sum(os.path.getsize(p) for p in files),
        "行数": sum(t.count("\n") + 1 for t in txts),
        "全角标点": punc,
        "标点形态": "原本无" if punc == 0 else "有标点",
        "探针数": total,
        "依据": "实测包含率 %d/%d（条 text 前 60 字去空白后整段命中；探针少于条数=短条不足 30 字）" % (hit, total),
    }
    if kind == "分卷目录":
        out["文件数"] = len(files)
    return out


# ---------- ④ 三条校验 ----------

def validate(doc):
    errs, warns, infos = [], [], []
    ids = {}
    for v in doc.get("volumes", []):
        nums = []
        for it in v.get("items", []):
            i = it.get("id")
            if i in ids:
                errs.append("V1 重复 id %s（卷 %s 与 %s）" % (i, ids[i], v.get("no")))
            ids[i] = v.get("no")
            m = re.search(r"-(\d{3})$", i or "")
            if m:
                nums.append(int(m.group(1)))
            # V3 sections 区间
            for s in (it.get("sections") or []):
                st, en = s.get("start"), s.get("end")
                if not isinstance(st, int) or not isinstance(en, int) or st < 0 or en > len(it.get("text") or "") or st >= en:
                    errs.append("V3 %s 的 section %r 区间非法 [ %s, %s ) / len=%d"
                                % (i, s.get("name"), st, en, len(it.get("text") or "")))
            if it.get("sections"):
                pr = [(s["start"], s["end"]) for s in it["sections"]
                      if isinstance(s.get("start"), int) and isinstance(s.get("end"), int)]
                pr.sort()
                for a, b in zip(pr, pr[1:]):
                    if a[1] > b[0]:
                        errs.append("V3 %s 的 sections 重叠 %s %s" % (i, a, b))
        if nums:
            for a, b in zip(nums, nums[1:]):
                if b - a > 1:
                    warns.append("V1 卷 %s 条号跳号 %03d→%03d" % (v.get("no"), a, b))
                    break
    fb = [i for i in ids if i.endswith("-000")]
    if fb:
        infos.append("V2 本有卷级兜底条 %d 个（装载与计数须排除，只取 level=item）" % len(fb))
    return errs, warns, infos, ids, fb


# ---------- ⑤ 主流程 ----------

def book_json_files(which):
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "分卷json")]
        if os.path.basename(root) != "书籍json":
            continue
        for fn in files:
            if fn.endswith(".json") and "_拼合" not in fn:
                yield os.path.join(root, fn)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check_only = "--check" in sys.argv
    ident = load_identities()
    editions = load_base_editions()
    rows = []
    for path in sorted(book_json_files(args)):
        doc = load(path)
        meta = doc.setdefault("meta", {})
        book = meta.get("书名") or os.path.splitext(os.path.dirname(path))[0]
        if book in EXCLUDE and not args:
            rows.append((book, "跳过（EXCLUDE）", ""))
            continue
        if args and book not in args:
            continue
        items = [it for v in doc.get("volumes", []) for it in v.get("items", [])]
        book_dir = os.path.dirname(os.path.dirname(path))
        rec = ident.get(os.path.relpath(book_dir, ROOT).replace("\\", "/")) or \
            ident.get(os.path.basename(book_dir))

        # --- meta 6 项 ---
        meta["契约"] = CONTRACT
        meta["book_id"] = (rec or {}).get("book_id")
        if meta["book_id"] is None:
            meta["book_id_依据"] = "Summary/html/data.js books[] 无此 dir；dir=" + os.path.basename(book_dir)
        au = (rec or {}).get("author") or ""
        seg = au.split("·")
        if len(seg) > 1 and re.match(r"^(先秦|秦|汉|晋|唐|宋|辽|金|元|明|清|民国)$", seg[0]):
            dynasty, author = seg[0], "·".join(seg[1:])
        else:
            dynasty, author = None, au or None
        # 书上已有声明优先，盘面值只作对照标注（annotate 不 replace；已有键名沿用，不建同义键）
        au_key = "作者" if "作者" in meta else "著者"
        own_au = meta.get(au_key)
        if au_key == "著者":
            own_au = own_au or meta.get("作者")
        meta[au_key] = own_au or author
        if own_au and author and own_au != author:
            meta["著者_盘面"] = author
        meta["朝代"] = meta.get("朝代") or dynasty
        if au and not meta["朝代"]:
            meta["朝代_依据"] = "data.js author=%r 首段不是朝代名，不猜" % au
        ge = (rec or {}).get("genre")
        own_ge = meta.get("体裁")
        meta["体裁"] = own_ge or ge
        if own_ge and ge and own_ge != ge:
            meta["体裁_盘面"] = ge
        if meta.get("体裁") is None:
            meta["体裁_依据"] = "book 内无声明且 data.js books[] 无该 dir"

        meta["成书年"] = None
        meta["成书年_依据"] = "盘面无可机采来源（序跋年号需逐本读，本轮不做）"
        be, src = editions.get(book), None
        if be is not None:
            src = "Skills/00-book-knowledge-factory/references/registry.md 行内 底本="
        if be is None:
            be, src = declared_base(book_dir)
        meta["底本版本"] = be
        if be is None and meta.get("底本"):
            src = ("lookedFor=registry.md 底本= 行 + 书目录内 SKILL.md/README.md 的「底本=」声明，均无命中；不猜。"
                   "书 meta.底本=%r 是构建来源说明（讲怎么切的），不是版次，故不上录" % meta["底本"])
        meta["底本版本_来源"] = src or "lookedFor=registry.md 底本= 行 + 书目录内 SKILL.md/README.md 的「底本=」声明，均无命中；不猜"
        meta["数字化"] = digitize(book_dir, items)

        # --- item 2 项 ---
        for it in items:
            it["level"] = "volume-fallback" if re.search(r"-000$", it.get("id") or "") else "item"
            if "sections" in it and it["sections"] is None:
                del it["sections"]
        keys = {k for it in items for k in it.keys()}
        head = [k for k in ("id", "title", "text") if k in keys]
        meta["条字段"] = "/".join(head + sorted(keys - set(head)))

        errs, warns, infos, ids, fb = validate(doc)
        real = sum(1 for it in items if it["level"] == "item")
        doc["条目总数"] = real
        if fb:
            meta["兜底条数"] = len(fb)
        rows.append((book, "ERR=%d WARN=%d INFO=%d" % (len(errs), len(warns), len(infos)),
                     "条=%d(item %d/fallback %d) 标点=%s 文件=%s" % (
                         len(items), real, len(fb),
                         meta["数字化"].get("全角标点"), meta["数字化"].get("文件") or "null")))
        for e in errs:
            rows.append(("", "  " + e, ""))
        for w in warns[:5]:
            rows.append(("", "  " + w, ""))
        if not check_only:
            save(path, doc)
        else:
            rows.append(("", "  meta新字段: " + json.dumps(
                {k: meta[k] for k in ("book_id", "著者", "朝代", "体裁", "成书年", "底本版本", "底本版本_来源")
                 if k in meta}, ensure_ascii=False), ""))
            rows.append(("", "  数字化: " + json.dumps(meta["数字化"], ensure_ascii=False), ""))

    w = max(len(r[0]) for r in rows) if rows else 4
    print("== 书籍json 精简契约回填 %s%s ==" % (CONTRACT, "（--check 未写文件）" if check_only else ""))
    for book, st, detail in rows:
        print(("%-" + str(w) + "s  %s  %s") % (book, st, detail))


if __name__ == "__main__":
    main()
