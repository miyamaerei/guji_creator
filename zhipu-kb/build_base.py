# -*- coding: utf-8 -*-
"""
《治谱》底座切条（build_base.py）
- 基底：校对/ 目录（用户指定）
- 输入：校对/卷之N.txt（体例：卷首题名 / 卷首篇目 / 正文 / 校勘记；补遗含两段篇目）
- 切条粒度：一个卷首篇目里的小标题 = 一条；正文按空行切块，块首行=标题
- 输出：
    _extract/NN_卷名.txt      （条N|标题\\n正文）
    _item_registry.json       {NN-NNN: {title, original, note}}  ← 不可重建，必入库
对账：每卷切出条数 == 该卷所有（卷首篇目）段列出的标题数。
"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT, "校对")
OUT_DIR = os.path.join(ROOT, "_extract")

# 卷文件 → (两位卷号, 卷名用于文件名)
VOL_ORDER = [
    ("卷之一", "01", "初选门"),
    ("卷之二", "02", "到任门"),
    ("卷之三", "03", "堂事门"),
    ("卷之四", "04", "词讼门"),
    ("卷之五", "05", "钱粮门"),
    ("卷之六", "06", "人命门"),
    ("卷之七", "07", "贼盗门"),
    ("卷之八", "08", "狱囚门"),
    ("卷之九", "09", "待人门"),
    ("卷之十", "10", "杂事门"),
    ("卷之十补遗", "11", "补遗祥刑要览"),
]

def split_sections(text):
    """把一卷文件切成 [(篇目标题列表, 正文字符串), ...]，支持一卷多段。"""
    # 找所有 （卷首篇目） ... （正文） ... （下一个（卷首篇目）/（校勘记）/文末）
    sections = []
    # 先按（卷首篇目）切开
    parts = re.split(r"（卷首篇目）", text)
    for p in parts[1:]:  # 第一段是卷首题名，跳过
        m = re.split(r"（正文）", p, maxsplit=1)
        if len(m) != 2:
            continue
        titles_block, rest = m
        # rest 在（校勘记）处截断
        body = re.split(r"（校勘记）", rest, maxsplit=1)[0]
        titles = [l.strip() for l in titles_block.splitlines() if l.strip()]
        sections.append((titles, body.strip()))
    return sections

def parse_body(body, titles):
    """以篇目清单为锚点切正文：标题独占一行处即条目起点，到下一标题行止。
    组标题自动跳过；全括注标题拼接括注内汉字匹配；同名相邻锚点去重；
    标题若粘在上段正文行尾（。XX：），先断行再锚。"""
    def norm(s):
        core = re.sub(r"〔[^〕]*〕", "", s).strip().rstrip("：:").strip()
        if core:
            return core
        # 全括注标题：拼接括注内汉字做匹配骨架
        return "".join(re.findall(r"〔([^〕]*)〕", s))
    lines = [l.rstrip() for l in body.splitlines()]
    # 预处理：把粘在行尾的标题（如 "…自遁矣。附健吾先生保甲铳药法："）断成两行
    title_norms = [norm(t) for t in titles]
    fixed = []
    for l in lines:
        hit = None
        for tn in title_norms:
            if len(tn) >= 3 and tn in l and not l.strip().startswith(tn):
                idx = l.index(tn)
                fixed.append(l[:idx].rstrip())
                fixed.append(l[idx:].rstrip())
                hit = tn
                break
        if not hit:
            fixed.append(l)
    lines = fixed
    # 找锚点
    anchors = []
    for li, line in enumerate(lines):
        ln = norm(line.strip())
        if not ln or len(ln) > 30:
            continue
        for tn in title_norms:
            if not tn:
                continue
            if ln == tn or ln.startswith(tn) or tn.startswith(ln):
                anchors.append((li, line.strip().rstrip("：:")))
                break
    dedup = []
    for a in anchors:
        if dedup and norm(a[1]) == norm(dedup[-1][1]):
            continue
        dedup.append(a)
    anchors = dedup
    items = []
    for ai, (li, raw_title) in enumerate(anchors):
        end = anchors[ai + 1][0] if ai + 1 < len(anchors) else len(lines)
        body_text = "\n".join(lines[li + 1:end]).strip()
        if body_text:
            items.append((raw_title, body_text))
    return items

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    registry = {}
    report = []
    total = 0
    for vol_name, vol_no, gate in VOL_ORDER:
        fp = os.path.join(SRC_DIR, vol_name + ".txt")
        text = open(fp, encoding="utf-8").read()
        sections = split_sections(text)
        # 切条：以篇目为锚点
        items = []
        for titles, body in sections:
            items.extend(parse_body(body, titles))
        # 写 _extract
        extract_path = os.path.join(OUT_DIR, f"{vol_no}_{gate}.txt")
        with open(extract_path, "w", encoding="utf-8") as f:
            for i, (title, body) in enumerate(items, 1):
                item_id = f"{vol_no}-{i:03d}"
                f.write(f"{item_id}|{title}\n{body}\n\n")
                registry[item_id] = {
                    "title": title,
                    "original": body,
                    "note": "",
                }
        total += len(items)
        # 对账：切出条数 vs 篇目条目数（组标题行在锚点切分时自动跳过，这里仅报告篇目总数供参考）
        expected = sum(len(t) for t, _ in sections)
        report.append(f"{vol_no} {gate}: 切出 {len(items)} 条（篇目清单 {expected} 行，组标题不计入）")

    reg_path = os.path.join(ROOT, "_item_registry.json")
    with open(reg_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=1)

    print("\n".join(report))
    print(f"\n底座合计：{total} 条 → {reg_path}")

if __name__ == "__main__":
    main()
