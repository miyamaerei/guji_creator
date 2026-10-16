# -*- coding: utf-8 -*-
r"""
明一统志 逐行覆盖校验（check_line_coverage.py）
循环明一统志.txt 的每一行，与《明一统志.json》对应卷的条目文本比对：
  1) 原书按行标行号（1 起）；重建 卷00 + 卷01~90 卷段（与 build_full_json.py 同逻辑：首标+撰行校验）
  2) 每行找所属卷 → 取 json 该卷 items 拼接文本（去空白）→ 行（去空白）在其中 → 覆盖；否则 miss
  3) 结构行（卷标/钦定四库全书/<史部…>/明 李贤等 撰/页末重复标）跳过，不计漏
  4) miss 按卷汇总 + 明细（行号/卷/内容前 60 字）写 _coverage_report.txt
用法：python check_line_coverage.py [整书json路径]
"""
import io, os, sys, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
TXT = os.path.join(PROJECT, "明一统志.txt")
CN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}


def cn_num(s):
    if "十" not in s:
        return CN.get(s, 0)
    parts = s.split("十")
    return CN.get(parts[0], 1) * 10 + CN.get(parts[1], 0) if len(parts) > 1 and parts[1] else CN.get(parts[0], 1) * 10


def norm(s):
    return re.sub(r"\s", "", s)


whole = os.path.join(HERE, "明一统志.json")
if len(sys.argv) > 1 and sys.argv[1] not in ("reverse", "char"):
    whole = sys.argv[1]
doc = json.load(io.open(whole, encoding="utf-8-sig"))
vol_by_no = {v["no"]: v for v in doc["volumes"]}

txt = io.open(TXT, encoding="utf-8-sig").read()
lines = txt.split("\n")


def line_of(off):
    return txt[:off].count("\n") + 1


# ---- 卷段重建（同 build_full_json.py） ----
marks = list(re.finditer(r"[明眀]一[统統綂]志[卷巻]([一二三四五六七八九十百]+)", txt))
starts, expect = [], 1
for m in marks:
    no = cn_num(m.group(1))
    if no == expect and norm(txt[m.end():m.end() + 80])[:5] in ("明李贤等撰", "眀李贤等撰"):
        starts.append((no, m))
        expect += 1
        if expect > 90:
            break
assert len(starts) == 90, f"首标 {len(starts)} != 90"
tail_end = marks[-1].start() if marks and cn_num(marks[-1].group(1)) == 90 else len(txt)
seg_line = []
for k, (no, m) in enumerate(starts):
    end = starts[k + 1][1].start() if k + 1 < len(starts) else tail_end
    seg_line.append((no, line_of(m.start()), line_of(end) - 1))
vol00_end = line_of(starts[0][1].start()) - 1


def vol_text(no):
    v = vol_by_no.get(f"{no:02d}") or vol_by_no.get(str(no))
    if not v:
        return ""
    return norm("".join(it.get("text", "") for it in v.get("items", [])))


# ---- 结构行判定 ----
struct_lines = set()
for m in marks:  # 首标+末标行
    struct_lines.add(line_of(m.start()))
for i, ln in enumerate(lines, 1):  # 钦定四库全书 / <史部…> / 明 李贤等 撰
    s = ln.strip()
    if not s:
        continue
    if s.startswith("钦定四库全书") or s.startswith("<史部") or norm(s) in ("明李贤等撰", "眀李贤等撰"):
        struct_lines.add(i)

# ---- 逐行检查 ----
miss_by_vol, miss_detail, covered, total = {}, [], 0, 0
for i, ln in enumerate(lines, 1):
    s = norm(ln)
    if not s or i in struct_lines:
        continue
    total += 1
    if i <= vol00_end:
        no, vt = "00", vol_text(0)
    else:
        no = None
        for vno, sline, eline in seg_line:
            if sline <= i <= eline:
                no, vt = vno, vol_text(vno)
                break
        if no is None:  # 卷段外（清一统志尾段等）
            continue
    if s in vt:
        covered += 1
    else:
        miss_by_vol[no] = miss_by_vol.get(no, 0) + 1
        if len(miss_detail) < 500:
            miss_detail.append((i, no, ln.strip()[:60]))

# ---- 报告 ----
lines_out = []
lines_out.append(f"原书总行 {len(lines)} | 内容行(排除结构行) {total} | 覆盖 {covered} | 遗漏 {sum(miss_by_vol.values())} | 覆盖率 {covered / total * 100:.1f}%")
lines_out.append(f"遗漏卷分布（卷号: 遗漏行数）：")
for no in sorted(miss_by_vol, key=lambda x: (len(str(x)), str(x))):
    lines_out.append(f"  卷{no}: {miss_by_vol[no]} 行")
lines_out.append("")
lines_out.append("== 遗漏明细（前 500 条：行号 | 卷 | 内容前60字）==")
for i, no, s in miss_detail:
    lines_out.append(f"  {i:>5} | 卷{no} | {s}")

report = os.path.join(HERE, "_coverage_report.txt")
with io.open(report, "w", encoding="utf-8") as f:
    f.write("\n".join(lines_out))
print("\n".join(lines_out[:60]))


def run_reverse():
    """反向校验：json 每条 item.text（去空白去【】）整条 → 在原书对应卷段（同样去空白去【】）中查找。
    命中 = 该条内容在原书有据可查（无凭空、无摘录丢原文）；用于判定“校对卷不漏”。"""

    def n2(s):
        return re.sub(r"[\s【】]", "", s)

    seg_text = {0: txt[: starts[0][1].start()]}  # 卷00
    for k, (no, m) in enumerate(starts):
        end = starts[k + 1][1].start() if k + 1 < len(starts) else tail_end
        seg_text[no] = txt[m.end():end]
    seg_norm = {no: n2(s) for no, s in seg_text.items()}

    miss, hit = [], 0
    total_items = 0
    with_pref = 0   # 前缀在原书有据（差异仅在尾部：异体/补长）
    no_origin = 0   # 原书无对应（知识工程补全条目，超集）
    for v in doc["volumes"]:
        vno = v["no"]
        key = 0 if vno == "00" else int(vno)
        sn = seg_norm.get(key, "")
        for it in v.get("items", []):
            t = n2(it.get("text", ""))
            if not t:
                continue
            total_items += 1
            if t in sn:
                hit += 1
            elif t[:15] in sn:
                with_pref += 1
                miss.append((vno, it.get("id"), it.get("title"), t[:50], "前缀有据(异体/尾部差异)"))
            else:
                no_origin += 1
                miss.append((vno, it.get("id"), it.get("title"), t[:50], "原书无对应(补全)"))

    out = []
    out.append(f"反向校验：条目总数 {total_items} | 原书可查(整条) {hit} | 前缀有据(异体/尾部差异) {with_pref} | 原书无对应(补全超集) {no_origin} | 整条命中率 {hit / total_items * 100:.1f}% | 有据率(整条+前缀) {(hit + with_pref) / total_items * 100:.1f}%")
    out.append("不可查条目按卷分布：")
    by_vol = {}
    for vno, iid, title, t, cat in miss:
        by_vol[vno] = by_vol.get(vno, 0) + 1
    for vno in sorted(by_vol, key=lambda x: (len(str(x)), str(x))):
        out.append(f"  卷{vno}: {by_vol[vno]} 条")
    out.append("")
    out.append("== 不可查明细（卷 | id | title | text前50字 | 归类）==")
    for vno, iid, title, t, cat in miss:
        out.append(f"  {vno} | {iid} | {title} | {t} | {cat}")
    r = os.path.join(HERE, "_reverse_report.txt")
    with io.open(r, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("\n".join(out[:50]))
    print(f"\n完整明细已写入 {r}")


def run_char():
    """字符级正向覆盖：以原书卷段正文为基准（去空白、排除结构行），
    逐字符在原书顺序上消耗 json 对应卷 items 拼接文本（多集匹配）。
    覆盖率 = 原书字符中被 json 覆盖数 / 原书总字符数；<95% 的卷输出 miss 行明细供逐条验证。"""

    def is_struct(ln):
        s = norm(ln)
        if not s:
            return True
        if re.fullmatch(r"[明眀]一[统統綂]志[卷巻][一二三四五六七八九十百]+", s):
            return True
        if s in ("明李贤等撰", "眀李贤等撰"):
            return True
        if s.startswith("钦定四库全书") or s.startswith("<史部"):
            return True
        return False

    seg_text = {0: txt[: starts[0][1].start()]}  # 卷00
    for k, (no, m) in enumerate(starts):
        end = starts[k + 1][1].start() if k + 1 < len(starts) else tail_end
        seg_text[no] = txt[m.end():end]

    out = []
    total_s = total_hit = 0
    bad_vols = []
    for v in doc["volumes"]:
        vno = v["no"]
        key = 0 if vno == "00" else int(vno)
        seg = seg_text.get(key, "")
        T = norm("".join(it.get("text", "") for it in v.get("items", [])))
        from collections import Counter
        pool = Counter(T)
        lines = seg.split("\n")
        hit = miss = 0
        miss_lines = []  # (行号, miss字符数, 行内容前50)
        base_off = 0
        for ln in lines:
            if is_struct(ln):
                continue
            ln_norm = norm(ln)
            if not ln_norm:
                continue
            row = txt.find(ln_norm, base_off) if ln_norm else -1
            line_no = txt[:row].count("\n") + 1 if row >= 0 else 0
            if row >= 0:
                base_off = row + len(ln_norm)
            m_cnt = 0
            for ch in ln_norm:
                if pool.get(ch, 0) > 0:
                    pool[ch] -= 1
                    hit += 1
                else:
                    miss += 1
                    m_cnt += 1
            if m_cnt:
                miss_lines.append((line_no, m_cnt, ln.strip()[:50]))
        total_s += hit + miss
        total_hit += hit
        rate = hit / (hit + miss) * 100 if hit + miss else 100.0
        out.append(f"卷{vno}: 原书正文字符 {hit + miss} | 覆盖 {hit} | 未覆盖 {miss} | 覆盖率 {rate:.1f}%")
        if rate < 95:
            bad_vols.append(vno)
            out.append(f"  未覆盖行（行号|miss字符数|内容前50字）：")
            for line_no, m_cnt, s in miss_lines[:30]:
                out.append(f"    {line_no:>6} | {m_cnt} | {s}")
            if len(miss_lines) > 30:
                out.append(f"    …… 共 {len(miss_lines)} 行未完全覆盖")
    out.append("")
    out.append(f"全书汇总：原书正文字符 {total_s} | 覆盖 {total_hit} | 未覆盖 {total_s - total_hit} | 覆盖率 {total_hit / total_s * 100:.1f}%")
    out.append(f"覆盖率 <95% 的卷：{bad_vols if bad_vols else '无'}")
    r = os.path.join(HERE, "_char_report.txt")
    with io.open(r, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("\n".join(out))
    print(f"\n完整报告已写入 {r}")


if len(sys.argv) > 1 and sys.argv[1] == "char":
    run_char()
    sys.exit()
if len(sys.argv) > 1 and sys.argv[1] == "reverse":
    run_reverse()
    sys.exit()
print(f"\n完整明细已写入 {report}")
