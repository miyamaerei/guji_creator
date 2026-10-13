# -*- coding: utf-8 -*-
"""
《明史·职官志》知识工程 —— 公共基座（供 build_* 与 validate 复用）
提供：路径常量、源读取、卷映射、切分、指纹库读写、原子写盘、ID 段位分配。
"""
import json
import os
import re
import tempfile

# ---------- 路径 ----------
SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
SRC = os.path.join(ROOT, "assets", "sources", "明史职官志.txt")
EXTRACT = os.path.join(ROOT, "_extract")
CHAPTERS = os.path.join(ROOT, "chapters")
LAYERS = os.path.join(ROOT, "_layers")
VIEWS = os.path.join(ROOT, "_views")
REGISTRY = os.path.join(ROOT, "_item_registry.json")

# ---------- 卷映射：汉字卷名直接映射，不按读取顺序（pitfalls #24）----------
VOL_MAP = {"职官一": "01", "职官二": "02", "职官三": "03",
           "职官四": "04", "职官五": "05"}
VOL_NAMES = {"01": "职官一", "02": "职官二", "03": "职官三",
             "04": "职官四", "05": "职官五"}

# ---------- 标记 ----------
MARK_CHAPTER = "◆"   # 章标记（不计条）
MARK_VOL = "◎"       # 卷标记（不计条）
MARK_TOC = "○"       # 卷目录行（不计条）


def read_source_lines():
    """读源文件，返回 [(原行号, 原始行)]（1-based 行号）"""
    with open(SRC, "r", encoding="utf-8") as f:
        return [(i, ln.rstrip("\n")) for i, ln in enumerate(f, 1)]


def split_entries(lines=None):
    """
    切分机构条目：一行非空段落 = 一条；◆/◎/○ 行与空行不计条。

    特例（源文本缺陷，2026-10-13 修正）：卷01 的卷目录行无 `○` 标记且**跨两行**
    （L5「宗人府三公三孤…礼部」+ L6「兵部(附协理京营戎政)刑部…」），与正文条目
    形态相同无法按标记识别。其余 4 卷目录行均有 `○` 标记且单行。
    处置：**卷目录块 = 从正文首条之后、第一个以机构名开头且不含 `。` 的连续短行块**；
    本书判据 = 位于卷首 `◎` 行之后、正文长段（≥100 字）之前、且不含句号 `。` 的行。
    """
    if lines is None:
        lines = read_source_lines()

    # 先按标记收集候选，并记录卷序
    cand, cur = [], None
    for lineno, text in lines:
        s = text.strip()
        if s.startswith(MARK_CHAPTER):
            m = re.search(r"职官([一二三四五])", s)
            if m:
                cur = VOL_MAP["职官" + m.group(1)]
            continue
        if s.startswith(MARK_VOL) or s.startswith(MARK_TOC) or s == "":
            continue
        cand.append({"volume": cur, "lineno": lineno, "text": s})

    # 逐卷识别「卷目录块」（源文本缺陷，2026-10-13 修正）
    # ------------------------------------------------------------------
    # 卷02~05 目录行有 `○` 标记且单行，已被上面的标记过滤剔除。
    # **仅卷01** 的目录行无 `○` 标记且跨两行（L5「宗人府三公三孤…礼部」+
    # L6「兵部(附协理京营戎政)刑部…」），形态与正文条目相同，标记法无法识别。
    # 位置特征（实测）：◎职官一(L3) → 卷序论(L4,含句号) → 目录(L5-L6,不含句号)
    #                   → 首个机构条目(L7,含句号)
    # 判据 = **紧邻首个含句号的正文条之前、连续不含句号的行** = 目录块。
    # ------------------------------------------------------------------
    toc_linenos = set()
    by_vol = {}
    for c in cand:
        by_vol.setdefault(c["volume"], []).append(c)
    for v, cs in by_vol.items():
        # 找「被正文包围的无句号段」：前一行为含句号正文、后一行亦为含句号正文，
        # 中间连续的若干无句号行 = 目录块。
        n = len(cs)
        for i in range(1, n):
            if "。" in cs[i]["text"]:
                continue
            # 无句号行：检查其前一行是否含句号（即紧跟在正文之后）
            if "。" in cs[i - 1]["text"]:
                j = i
                while j < n and "。" not in cs[j]["text"]:
                    toc_linenos.add(cs[j]["lineno"])
                    j += 1

    entries = [c for c in cand if c["lineno"] not in toc_linenos]
    cnt = {}
    for e in entries:
        v = e["volume"]
        cnt[v] = cnt.get(v, 0) + 1
        e["item_id"] = "%s-%03d" % (v, cnt[v])
    return entries


def norm_text(s):
    """
    norm 归一：繁体→简体（本书源已是简体）、异体字归一、标点归一、空格清理。
    全角括号（）保留（沿革括注是重要语义）。
    """
    t = s
    # 异体字归一（按实际出现的最小集）
    for a, b in (("適", "嫡"), ("讎", "仇"), ("倂", "并"), ("幷", "并"),
                 ("甯", "宁"), ("傑", "杰")):
        t = t.replace(a, b)
    # 标点统一为全角中文标点
    t = t.replace(",", "，").replace(";", "；").replace(":", "：")
    t = t.replace("(", "（").replace(")", "）")
    # 空白清理（保留正文，无空格则无操作）
    t = re.sub(r"[ \t\u3000]+", "", t)
    return t


def build_registry(entries):
    """指纹库：key=NN-NNN, value={original, norm}"""
    reg = {}
    for e in entries:
        reg[e["item_id"]] = {"original": e["text"], "norm": norm_text(e["text"])}
    return reg


def load_registry():
    with open(REGISTRY, "r", encoding="utf-8") as f:
        return json.load(f)


def atomic_write_json(path, obj):
    """临时文件 + rename 落盘（pitfalls #14）"""
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d or ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def atomic_write_text(path, text):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d or ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def seg_start(volume):
    """业务 ID 段位起点 = 卷号 × 段容量（pitfalls #13/#22）"""
    return int(volume) * 500
def assign_ids(records, prefix, volume, id_field):
    """
    按**全局记录序号**自动分配业务 ID（AI 源数据只写 slot 表示卷内语义顺序，
    不写 ID）。段位 = 卷号 × 段容量；卷内序号 = 记录在列表中的位置 + 1。

    ⚠ 关键纪律（pitfalls 实例：ZG-R 撞号）：**ID 序号必须取自记录在列表中的
    序号，不能取自 `slot`** —— slot 是"条目内语义顺序"，每个 item_id 都从 1
    重启，直接用 slot 会让所有条目的第 1 条规则都撞成 ZG-R-501。
    调用方须保证 records 已按 (item_id, slot) 排序。
    """
    base = seg_start(volume)
    for i, r in enumerate(records, 1):
        r[id_field] = "%s%03d" % (prefix, base + i)
    return records


def load_layer(container, volume):
    """读单卷层产物 _layers/<container>/<container>_NN.json"""
    p = os.path.join(LAYERS, container, "%s_%s.json" % (container, volume))
    if not os.path.isfile(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save_layer(container, volume, records):
    """写单卷层产物，顶层键统一 records（pitfalls #19）"""
    p = os.path.join(LAYERS, container, "%s_%s.json" % (container, volume))
    atomic_write_json(p, {"volume": volume, "records": records})
    return p


def iter_volumes(arg=None):
    """--volumes 01,02 支持；空则全部 5 卷"""
    if not arg:
        return ["01", "02", "03", "04", "05"]
    if isinstance(arg, (list, tuple)):
        return list(arg)
    return [v.strip() for v in str(arg).split(",") if v.strip()]
