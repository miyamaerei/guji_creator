# -*- coding: utf-8 -*-
"""
《焚书》结构化 JSON → 6 类导出产物

  01_目录结构.txt              全书目录树（卷→篇→子篇）
  02_原文txt/                   每卷纯原文
  03_篇txt/卷X/标题.txt         每篇一个 txt（文件名=标题，含题解/原文/注释/译文）
  04_译文txt/卷X_译文.txt       不带注释的译文全文
  05_背景txt/                   全书题解汇总 + 每卷文件夹内每篇一个背景 txt
  06_原文注释md/卷X/标题.md     每篇“原文+注释”Markdown

用法：python export_fenshu.py [输出根目录]
默认输出根目录：脚本所在目录下的“导出”
"""
import io
import json
import os
import re
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE, "焚书_结构化.json")
OUT_ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "导出")

VOL_LABELS = {
    "卷一": ("书答", "卷一_书答"),
    "卷二": ("书答", "卷二_书答"),
    "卷三": ("杂述", "卷三_杂述"),
    "卷四": ("杂述", "卷四_杂述"),
    "卷五": ("读史", "卷五_读史"),
    "卷六": ("诗", "卷六"),
}

ILLEGAL = re.compile(r'[\\/:*?"<>|\r\n\t]')


def sanitize(name):
    """Windows 文件名净化：替换非法字符，去掉尾部点/空格。"""
    name = ILLEGAL.sub("_", name)
    name = name.rstrip(". ")
    return name or "未命名"


def load_doc():
    with io.open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# 节点模型：把卷内正文展平成“可导出节点”（篇/子篇）
# ---------------------------------------------------------------------------
class Node:
    __slots__ = ("vol", "title", "is_sub", "parent", "ti_jie", "units", "order")

    def __init__(self, vol, title, is_sub, parent, ti_jie, units, order):
        self.vol = vol          # 卷 dict
        self.title = title      # 标题（含子篇标题）
        self.is_sub = is_sub
        self.parent = parent    # 父篇标题（子篇时）
        self.ti_jie = ti_jie    # list[str]
        self.units = units      # list[unit dict]
        self.order = order      # 卷内顺序号（篇级）

    @property
    def vol_dir(self):
        return VOL_LABELS.get(self.vol["no"], (self.vol.get("name", ""), self.vol["no"].replace(" ", "_")))[1]


def build_nodes(doc):
    """正文卷 → 节点列表。
    卷六类别(h2)本身无正文，其下每首诗(h3)独立成节点；
    其余卷的篇(h2)与子篇(h3)凡有正文都独立成节点。
    """
    nodes = []
    for vol in doc["volumes"]:
        order = 0
        for art in vol["articles"]:
            order += 1
            art_has_body = bool(art["units"] or art.get("ti_jie"))
            if art_has_body:
                nodes.append(Node(vol, art["title"], False, None, art.get("ti_jie", []), art["units"], order))
            for sub in art["sub_articles"]:
                if sub["units"] or sub.get("ti_jie"):
                    nodes.append(Node(vol, sub["title"], True, art["title"], sub.get("ti_jie", []), sub["units"], order))
    return nodes


# ---------------------------------------------------------------------------
# 唯一文件名（重名消歧），生成命名说明
# ---------------------------------------------------------------------------
# 无区分度的子篇标题：一律用“父篇_标题”命名
GENERIC_TITLES = {"又", "第一段", "第二段", "第三段", "第四段", "小引"}


def make_unique_names(nodes):
    used = {}          # 已占用文件名(不含扩展) -> 节点
    mapping = []       # (node, final_name, 说明)
    for node in nodes:
        base = sanitize(node.title)
        pbase = f"{sanitize(node.parent)}_{base}" if node.parent else None
        cand = None
        note = ""
        if node.parent and node.title in GENERIC_TITLES:
            cand, note = pbase, f"子篇标题无区分度，改用 {pbase}"
            k = 2
            while cand in used:
                cand, note = f"{pbase}_{k}", f"子篇标题无区分度，改用 {pbase}_{k}"
                k += 1
        elif node.parent:
            cand = base
            if cand in used:
                cand, note = pbase, f"标题重名，改用 {pbase}"
                k = 2
                while cand in used:
                    cand, note = f"{pbase}_{k}", f"标题重名，改用 {pbase}_{k}"
                    k += 1
        else:
            cand = base
            if cand in used:
                cand, note = f"{node.vol['no']}_{base}", f"标题重名，改用 {node.vol['no']}_{base}"
                k = 2
                while cand in used:
                    cand = f"{node.vol['no']}_{base}_{k}"
                    note = f"标题重名，改用 {cand}"
                    k += 1
        used[cand] = node
        mapping.append((node, cand, note))
    return mapping


# ---------------------------------------------------------------------------
# 渲染函数
# ---------------------------------------------------------------------------
def render_units_text(units):
    """整篇的 原文/注释/译文 顺序文本（与分卷样式一致）。"""
    out = []
    for u in units:
        if u["原文"]:
            out.append("【原文】")
            out.extend(u["原文"])
            out.append("")
        if u["注释"]:
            out.append("【注释】")
            for n in u["注释"]:
                out.append(f"{n['key'] or ''}{n['text']}")
            out.append("")
        if u["译文"]:
            out.append("【译文】")
            out.extend(u["译文"])
            out.append("")
    return out


def render_origins(units):
    out = []
    for u in units:
        out.extend(u["原文"])
    return out


def strip_anchors(paras, anchors):
    """按“标注”字段移除段内 sup 标注字符（纯原文导出用，标注与段一一对应）。"""
    out = []
    for i, para in enumerate(paras):
        t = para
        if i < len(anchors):
            for a in anchors[i]:
                t = t.replace(a, "")
        out.append(t)
    return out


def render_origins_clean(units):
    """纯原文（无 ①② 等标注序号）。"""
    out = []
    for u in units:
        out.extend(strip_anchors(u["原文"], u["标注"]))
    return out


def render_translations(units):
    out = []
    for u in units:
        out.extend(u["译文"])
    return out


def render_md(node):
    """原文+注释 Markdown：逐单元 原文/注释 相邻排列。"""
    lines = [f"# {node.title}", ""]
    if node.parent:
        lines.append(f"> 属《{node.parent}》　{node.vol['full']}")
    else:
        lines.append(f"> {node.vol['full']}")
    lines.append("")
    if node.ti_jie:
        lines.append("## 题解")
        lines.append("")
        for p in node.ti_jie:
            lines.append(p)
            lines.append("")
    for u in node.units:
        if u["原文"]:
            lines.append("## 原文")
            lines.append("")
            for para in u["原文"]:
                lines.append(para)
                lines.append("")
        if u["注释"]:
            lines.append("## 注释")
            lines.append("")
            for n in u["注释"]:
                lines.append(f"- {n['key'] or ''}{n['text']}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8-sig") as f:
        f.write(text)


# ---------------------------------------------------------------------------
# 6 类产物
# ---------------------------------------------------------------------------
def export_toc(doc, mapping):
    """01 目录结构 txt"""
    lines = ["《焚书》目录结构", "=" * 40, ""]
    lines.append("卷首（书名页／版权页／目录／李贽论／凡例／自序）")
    lines.append("")
    mi = 0
    for vol in doc["volumes"]:
        lines.append(f"【{vol['full']}】")
        for i, art in enumerate(vol["articles"], 1):
            # 收集属于本篇的节点（主篇+子篇，按序），mapping 与卷内篇目同序
            art_nodes = []
            while mi < len(mapping):
                node, final, _ = mapping[mi]
                if node.vol is vol and node.order == i:
                    art_nodes.append((node, final))
                    mi += 1
                else:
                    break
            if not art_nodes:
                lines.append(f"  {i:>2}. {art['title']}（无正文）")
                continue
            mains = [(n, f) for n, f in art_nodes if not n.is_sub]
            subs = [(n, f) for n, f in art_nodes if n.is_sub]
            if mains:
                for node, final in mains:
                    suffix = f"  → {final}.txt" if final != sanitize(node.title) else ""
                    lines.append(f"  {i:>2}. {node.title}{suffix}")
            else:
                lines.append(f"  {i:>2}. {art['title']}（类目）")
            for node, final in subs:
                suffix = f"  → {final}.txt" if final != sanitize(node.title) else ""
                lines.append(f"      └ {node.title}{suffix}")
        lines.append("")
    for app in doc["appendices"]:
        lines.append(f"【{app['title']}】")
        for a in app.get("articles", []):
            lines.append(f"  · {a['title']}")
        lines.append("")
    w(os.path.join(OUT_ROOT, "01_目录结构.txt"), "\n".join(lines))


def export_yuanwen(doc, nodes):
    """02 纯原文 txt（按卷，无标注序号）"""
    for vol in doc["volumes"]:
        prefix = VOL_LABELS.get(vol["no"], (vol.get("name", ""), vol["no"]))[1]
        out = [f"《焚书》原文 · {vol['full']}", "=" * 40, ""]
        vol_nodes = [n for n in nodes if n.vol["no"] == vol["no"]]
        for n in vol_nodes:
            out.append(f"【{n.title}】")
            for p in render_origins_clean(n.units):
                out.append(p)
            out.append("")
        w(os.path.join(OUT_ROOT, "02_原文txt", f"{prefix}_原文.txt"), "\n".join(out))


def export_articles(doc, mapping):
    """03 每篇一个 txt（文件名=标题，含子篇内容的整篇）"""
    for node, fname, note in mapping:
        out = [f"【{node.title}】", f"（{node.vol['full']}）", ""]
        if node.ti_jie:
            out.append("【题解】")
            out.extend(node.ti_jie)
            out.append("")
        out.extend(render_units_text(node.units))
        vol_dir = node.vol_dir
        w(os.path.join(OUT_ROOT, "03_篇txt", vol_dir, f"{fname}.txt"), "\n".join(out).strip() + "\n")


def export_translations(doc, nodes):
    """04 译文全文 txt（不带注释，按卷）"""
    for vol in doc["volumes"]:
        prefix = VOL_LABELS.get(vol["no"], (vol.get("name", ""), vol["no"]))[1]
        out = [f"《焚书》译文 · {vol['full']}", "=" * 40, ""]
        vol_nodes = [n for n in nodes if n.vol["no"] == vol["no"]]
        for n in vol_nodes:
            out.append(f"【{n.title}】")
            for p in render_translations(n.units):
                out.append(p)
            out.append("")
        w(os.path.join(OUT_ROOT, "04_译文txt", f"{prefix}_译文.txt"), "\n".join(out))


def export_split(doc, mapping, subdir, render_fn, label):
    """07/08 按篇拆分：每篇一个文件，文件名与 03 篇txt 一致。
    render_fn(node) -> list[str]；无正文（仅题解）的篇跳过并计数。"""
    skipped = 0
    for node, fname, note in mapping:
        body = render_fn(node.units)
        if not body:
            skipped += 1
            continue
        w(os.path.join(OUT_ROOT, subdir, node.vol_dir, f"{fname}.txt"), "\n".join(body) + "\n")
    return skipped


def export_background(doc, nodes, mapping):
    """05 背景 txt：全书汇总 + 每卷文件夹每篇一个背景 txt"""
    # 全书汇总
    lines = ["《焚书》全书题解（背景）汇总", "=" * 40, ""]
    for node, fname, note in mapping:
        if not node.ti_jie:
            continue
        lines.append(f"【{node.vol['no']}《{node.title}》】")
        lines.extend(node.ti_jie)
        lines.append("")
    w(os.path.join(OUT_ROOT, "05_背景txt", "全书题解汇总.txt"), "\n".join(lines))
    # 每卷文件夹
    for node, fname, note in mapping:
        if not node.ti_jie:
            continue
        out = [f"《{node.title}》写作背景（题解）", "=" * 40, ""]
        out.extend(node.ti_jie)
        vol_dir = node.vol_dir
        w(os.path.join(OUT_ROOT, "05_背景txt", vol_dir, f"{fname}.txt"), "\n".join(out).strip() + "\n")


def export_md(doc, mapping):
    """06 原文+注释 md（每篇一个）"""
    for node, fname, note in mapping:
        md = render_md(node)
        vol_dir = node.vol_dir
        w(os.path.join(OUT_ROOT, "06_原文注释md", vol_dir, f"{fname}.md"), md)


def export_naming_note(mapping):
    """00 命名说明（重名消歧清单，供人工核对）"""
    lines = ["导出命名说明", "=" * 40, ""]
    renamed = 0
    for node, fname, note in mapping:
        base = sanitize(node.title)
        if note:
            renamed += 1
            lines.append(f"{note}\n    原标题《{node.title}》（{node.vol['no']}）")
            lines.append("")
    lines.insert(2, f"共 {len(mapping)} 个正文篇目节点，{renamed} 个因重名/特殊字符调整了文件名。")
    w(os.path.join(OUT_ROOT, "00_命名说明.txt"), "\n".join(lines))
    return renamed


def main():
    doc = load_doc()
    nodes = build_nodes(doc)
    # 先清空输出根目录（本脚本自产目录），避免旧命名文件残留
    if os.path.exists(OUT_ROOT):
        shutil.rmtree(OUT_ROOT)
    os.makedirs(OUT_ROOT)
    mapping = make_unique_names(nodes)
    renamed = export_naming_note(mapping)
    export_toc(doc, mapping)
    export_yuanwen(doc, nodes)
    export_articles(doc, mapping)
    export_translations(doc, nodes)
    export_background(doc, nodes, mapping)
    export_md(doc, mapping)
    skip_o = export_split(doc, mapping, "07_原文拆分txt", render_origins_clean, "原文")
    skip_t = export_split(doc, mapping, "08_译文拆分txt", render_translations, "译文")
    print(f"导出完成 -> {OUT_ROOT}")
    print(f"正文篇目节点：{len(nodes)} 个（含子篇/诗），重名或特殊字符改名：{renamed} 个，详见 00_命名说明.txt")
    print(f"按篇拆分：原文跳过 {skip_o} 个、译文跳过 {skip_t} 个（均无正文、仅题解的篇）")
    print("产物：")
    for d in ["01_目录结构.txt", "02_原文txt", "03_篇txt", "04_译文txt", "05_背景txt", "06_原文注释md", "07_原文拆分txt", "08_译文拆分txt"]:
        print("  -", os.path.join(OUT_ROOT, d))


if __name__ == "__main__":
    main()
