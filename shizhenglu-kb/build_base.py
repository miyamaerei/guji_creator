# -*- coding: utf-8 -*-
"""《吕公实政录》底座（C3）：切卷 → 切条 → 归一 → 指纹库 → 对账报告。

四段式 ①。用法（从工程根 shizhenglu-kb/ 执行）：
    python build_base.py                 # 全量切分
    python build_base.py --expect "01:1,02:1,03:26"   # 可选：按期望条数自校验

输出：
    _extract/NN_卷名.txt      行格式：条N|标题|正文（卷级条目：条1|卷名|正文）
    _item_registry.json      {item_id: {original, norm}}（原文唯一源，只入不出）
    _build/base_report.txt   对账报告（每卷条数 + 标题清单 + 总计）
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
INSTANCE = os.path.join(ROOT, "07-lvgong-shizhenglu-knowledge")

# 源文本查找顺序：环境变量 > 工程根 _source/ > 实例 assets/sources/
SRC_CANDIDATES = [
    os.environ.get("LSZL_TXT", ""),
    os.path.join(ROOT, "_source", "吕公实政录_原文_全卷合并.txt"),
    os.path.join(INSTANCE, "assets", "sources", "吕公实政录_原文_全卷合并.txt"),
]
SRC = next((p for p in SRC_CANDIDATES if p and os.path.isfile(p)), None)
if SRC is None:
    sys.exit("找不到原文：请在工程根建 _source/ 或设置环境变量 LSZL_TXT")

# 卷号→卷名（按原书顺序；与实例 references/schemas.md §1 一致，固定不改）
VOLUME_NAMES = {
    1: "明职·新吾吕先生实政录序", 2: "明职·明职引", 3: "明职·卷一",
    4: "民务·卷之二", 5: "民务·卷之三", 6: "民务·卷之四",
    7: "乡甲约·卷之一", 8: "乡甲约·卷之二", 9: "乡甲约·卷之三",
    10: "乡甲约·卷之四", 11: "乡甲约·卷之五", 12: "乡甲约·卷之六",
    13: "风宪约·重刊风宪约序", 14: "风宪约·卷之一", 15: "风宪约·卷之二",
}

# norm 归一规则（轻归一：只做明确的异体/俗字映射；缺字□等保留原形不臆补）
NORM_MAP = {"廵": "巡", "飬": "养", "枽": "桑", "貯": "贮"}
NORM_MAP = {ord(k): v for k, v in NORM_MAP.items()}


def norm_text(s: str) -> str:
    return s.translate(NORM_MAP)


def parse_source() -> dict:
    """返回 {vol_no: {"name":..., "title_items": [(title, body)], "vol_body": str}}。
    规则：◆=卷标题；○/△=条目标题；篇目列表行（（卷首篇目）后、（正文）前）跳过；
    无 ○/△ 的卷 → 整卷为一条卷级条目。"""
    lines = io.open(SRC, encoding="utf-8").read().splitlines()
    vols = {}          # vol_no -> dict
    cur_vol = None
    cur_item = None
    in_toc = False     # 是否在（卷首篇目）区内
    started = False    # 是否已见第一卷（跳过文件头）

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("===="):
            continue
        if line.startswith("◆"):
            started = True
            name = line[1:].strip()
            vols[len(vols) + 1] = {"name": name, "title_items": [], "vol_body": []}
            cur_vol = len(vols)
            cur_item = None
            in_toc = False
            continue
        if not started:
            continue  # 文件头
        if line == "（卷首篇目）":
            in_toc = True
            continue
        if line == "（正文）":
            in_toc = False
            continue
        if in_toc:
            continue  # 篇目列表行不进入条目
        m = re.match(r"^[○△](.*)$", line)
        if m:
            title = m.group(1).strip()
            vols[cur_vol]["title_items"].append([title, []])
            cur_item = vols[cur_vol]["title_items"][-1]
            continue
        # 正文行：追加到当前条目；无条目时追加到卷体（卷级条目用）
        if cur_item is not None:
            cur_item[1].append(line)
        else:
            vols[cur_vol]["vol_body"].append(line)
    return vols


def build():
    vols = parse_source()
    os.makedirs(os.path.join(ROOT, "_extract"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "_build"), exist_ok=True)

    registry = {}
    report_lines = []
    total = 0
    for no in sorted(vols):
        v = vols[no]
        items = []
        if v["title_items"]:
            for i, (title, body) in enumerate(v["title_items"], 1):
                items.append((i, title, "\n".join(body)))
        else:
            items.append((1, v["name"], "\n".join(v["vol_body"])))
        # _extract
        fname = os.path.join(ROOT, "_extract", "%02d_%s.txt" % (no, v["name"].split("·")[-1]))
        with io.open(fname, "w", encoding="utf-8") as f:
            for seq, title, body in items:
                f.write("条%d|%s|%s\n" % (seq, title, body))
        # 指纹库
        for seq, title, body in items:
            item_id = "%02d-%03d" % (no, seq)
            original = title + "\n" + body if v["title_items"] else body
            registry[item_id] = {"original": original, "norm": norm_text(original)}
        total += len(items)
        report_lines.append("卷%02d %s：%d 条" % (no, v["name"], len(items)))
        for seq, title, _ in items:
            report_lines.append("    %02d-%03d  %s" % (no, seq, title))

    report_lines.append("合计 %d 条" % total)
    with io.open(os.path.join(ROOT, "_build", "base_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    with io.open(os.path.join(ROOT, "_item_registry.json"), "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=1)

    print("\n".join(report_lines))
    # --expect 自校验（可选）
    for arg in sys.argv[1:]:
        if arg.startswith("--expect="):
            expect = {k: int(v) for k, v in
                      (kv.split(":") for kv in arg.split("=", 1)[1].split(","))}
            actual = {}
            for no in vols:
                n = len(vols[no]["title_items"]) or 1
                actual["%02d" % no] = n
            diff = {k: (expect[k], actual.get(k)) for k in expect if expect[k] != actual.get(k)}
            print("自校验:", "OK" if not diff else "MISMATCH %r" % diff)
    return total


if __name__ == "__main__":
    build()
