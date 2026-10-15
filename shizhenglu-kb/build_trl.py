# -*- coding: utf-8 -*-
"""《吕公实政录》古今翻译层（TRL）打包器：白话文分册译本 → 对齐指纹库 → TRL 记录。

依据 Skills/00-book-knowledge-factory 层库 C5 古今翻译层（TRL）：
    记录 schema：trl_id / item_id / translation / style / note / confidence / original / norm
    ID 前缀：TRL-（本工程内全局唯一，trl_id = TRL-<册NN><条NNN>，可由 item_id 直接还原）
    风格枚举：直译/意译/注释性翻译（本书取"注释性翻译"——白话正文 + 专名/职官/年代括注，
              与 assets/sources/吕公实政录_白话文_全卷合并.txt 同源的翻译口径）

输入（对照引用源，非抽取依据；原 SKILL.md §0"按条目对应引用"口径的落地即本层）：
    白话文/<册名>_白话.txt      15 册分册白话译本（◆ 册名与卷号表见 VOLUME_NAMES）
    _item_registry.json        指纹库（original/norm 唯一源，打包器注入，不手抄）
硬校验（不过即报错，退出码 1）：
    * 册头【册名】/（正文）结构完整；卷级册（无 ○/△ 条目）整册为一条
    * 每册 白话条数 = 指纹库条数（C5 覆盖校验：条目数=翻译数）
    * 标题按序逐一相等（剥 ○/△ 前缀与首尾空白后比对；卷级册以册名代标题）
    * 译文非空；original 注入后与指纹库逐条一致
产出：
    _layers/trl/trl_NN.json             {"records": [...]}（与 ent/rule/struct 等层同构）
    _layers/trl/trl_summary.json        层级汇总
    _layers/trl/全书白话译本/NN_册名.md  可读译本（条号 + 标题 + 译文）

用法（从工程根 shizhenglu-kb/ 执行）：
    python build_trl.py                  # 全量 15 册
    python build_trl.py --volumes 03 14  # 指定册
"""
import argparse
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(ROOT, "_item_registry.json")
BAIHUA_DIR = os.path.join(ROOT, "白话文")
OUT_DIR = os.path.join(ROOT, "_layers", "trl")
MD_DIR = os.path.join(OUT_DIR, "全书白话译本")

STYLE = "注释性翻译"

# 册号→册名（与 build_base.py VOLUME_NAMES 一致，固定不改）
VOLUME_NAMES = {
    1: "明职·新吾吕先生实政录序", 2: "明职·明职引", 3: "明职·卷一",
    4: "民务·卷之二", 5: "民务·卷之三", 6: "民务·卷之四",
    7: "乡甲约·卷之一", 8: "乡甲约·卷之二", 9: "乡甲约·卷之三",
    10: "乡甲约·卷之四", 11: "乡甲约·卷之五", 12: "乡甲约·卷之六",
    13: "风宪约·重刊风宪约序", 14: "风宪约·卷之一", 15: "风宪约·卷之二",
}


def read_lines(path):
    return [ln.strip() for ln in io.open(path, encoding="utf-8").read().splitlines() if ln.strip()]


def extract_titles(vol_no):
    """从 _extract/NN_*.txt 取册内条目标题（指纹库构建时的同源切分，标题字段显式）。
    卷级册的条目标题即册名。返回标题列表；extract 缺失返回 None。"""
    import glob as _glob
    hits = sorted(_glob.glob(os.path.join(ROOT, "_extract", "%02d_*.txt" % vol_no)))
    if not hits:
        return None
    titles = []
    for ln in io.open(hits[0], encoding="utf-8").read().splitlines():
        m = re.match(r"^条\d+\|([^|]+)\|", ln)
        if m:
            titles.append(m.group(1).strip())
    return titles


def parse_baihua(path, vol_name):
    """解析分册白话文件：返回 [(title|None, body_lines)]。
    ○/△ 行 = 新条目标题（照抄原文）；无条目标记的册 → 整册为一条（title=None，卷级条目）。"""
    lines = read_lines(path)
    issues = []
    expect_head = "【%s】" % vol_name
    if not lines or lines[0] != expect_head:
        issues.append("%s：册头应为 %r，实际 %r" % (os.path.basename(path), expect_head,
                                                  lines[0] if lines else "<空文件>"))
    if "（正文）" not in lines:
        issues.append("%s：缺（正文）分节标记" % os.path.basename(path))
    items, cur, in_toc = [], None, False
    for ln in lines[1:]:
        if ln == "（卷首篇目）":
            in_toc = True
            continue
        if ln == "（正文）":
            in_toc = False
            continue
        if in_toc:
            continue
        m = re.match(r"^[○△](.+)$", ln)
        if m:
            cur = [m.group(1).strip(), []]
            items.append(cur)
            continue
        if cur is not None:
            cur[1].append(ln)
        elif not items:
            cur = [None, [ln]]  # 卷级册：（正文）后直接是整册译文
            items.append(cur)
        else:
            issues.append("%s：条目区出现游离行 %r" % (os.path.basename(path), ln[:40]))
    return items, issues


def build(volumes=None, verbose=True):
    with io.open(REGISTRY_PATH, encoding="utf-8") as f:
        registry = json.load(f)
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(MD_DIR, exist_ok=True)

    issues = []
    total_records = 0
    covered = []
    nos = sorted(VOLUME_NAMES) if not volumes else [n for n in sorted(VOLUME_NAMES)
                                                    if "%02d" % n in volumes]

    for no in nos:
        vol_no = "%02d" % no
        vol_name = VOLUME_NAMES[no]
        src = os.path.join(BAIHUA_DIR, vol_name + "_白话.txt")
        if not os.path.isfile(src):
            issues.append("册 %s：缺白话文件 %s" % (vol_no, src))
            continue
        items, iss = parse_baihua(src, vol_name)
        issues.extend(iss)

        reg_ids = sorted(k for k in registry if k.startswith(vol_no + "-"))
        reg_titles = extract_titles(no)
        if reg_titles is None:
            issues.append("册 %s：缺 _extract/NN_*.txt，无法取条目标题，本册不产出" % vol_no)
            continue
        if len(reg_titles) != len(reg_ids):
            issues.append("册 %s：_extract 条数 %d ≠ 指纹库条数 %d，本册不产出"
                          % (vol_no, len(reg_titles), len(reg_ids)))
            continue

        if len(reg_ids) != len(items):
            issues.append("册 %s：条目数≠翻译数（指纹库 %d / 白话 %d），本册不产出"
                          % (vol_no, len(reg_ids), len(items)))
            continue
        mism = [(i, a, b) for i, (a, b) in enumerate(zip(reg_titles, items))
                if a != (b[0] if b[0] is not None else vol_name)]
        if mism:
            for i, a, b in mism[:5]:
                issues.append("册 %s 第 %d 条标题不齐：extract %r ≠ 白话 %r"
                              % (vol_no, i + 1, a, b[0] if b[0] is not None else "<卷级>"))
            issues.append("册 %s：标题对齐失败（共 %d 处），本册不产出" % (vol_no, len(mism)))
            continue

        records = []
        for seq, (item_id, (title, body)) in enumerate(zip(reg_ids, items), 1):
            translation = "\n".join(body).strip()
            if not translation:
                issues.append("册 %s %s：译文为空" % (vol_no, item_id))
                continue
            records.append({
                "trl_id": "TRL-%s%03d" % (vol_no, seq),
                "item_id": item_id,
                "translation": translation,
                "style": STYLE,
                "note": "整段取自白话文对照源：白话文/%s_白话.txt（○/△标题照抄原文，正文白话）" % vol_name,
                "confidence": 1.0,
                "original": registry[item_id]["original"],
                "norm": registry[item_id]["norm"],
            })
        # original 注入一致性复核
        for r in records:
            if r["original"] != registry[r["item_id"]]["original"]:
                issues.append("册 %s %s：original 与指纹库不一致" % (vol_no, r["item_id"]))

        with io.open(os.path.join(OUT_DIR, "trl_%s.json" % vol_no), "w", encoding="utf-8",
                     newline="\n") as f:
            json.dump({"records": records}, f, ensure_ascii=False, indent=2)
            f.write("\n")
        write_md(vol_no, vol_name, records, reg_titles)
        total_records += len(records)
        covered.append(vol_no)
        if verbose:
            print("册 %s %s: %d 条 TRL 记录" % (vol_no, vol_name, len(records)))

    summary = {
        "layer": "trl",
        "record_count": total_records,
        "volumes_covered": covered,
        "style": STYLE,
        "id_rule": "trl_id = TRL-<册NN><条NNN>，可由 item_id 还原",
        "source": "白话文/<册名>_白话.txt（对照引用源，整段截取，不参与抽取；"
                  "合并版见 assets/sources/吕公实政录_白话文_全卷合并.txt）",
    }
    with io.open(os.path.join(OUT_DIR, "trl_summary.json"), "w", encoding="utf-8",
                 newline="\n") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        f.write("\n")

    if issues:
        print("\n[TRL 校验问题 %d 条]" % len(issues))
        for i in issues[:20]:
            print("  -", i)
        if len(issues) > 20:
            print("  ...（其余 %d 条略）" % (len(issues) - 20))
        return 1
    print("\nTRL 校验通过（条目数=翻译数=%d，标题全对齐，问题数=0）" % total_records)
    return 0


def write_md(vol_no, vol_name, records, titles):
    """可读译本：### 条号 标题 + 译文（源文件一行一段，空行分段）。"""
    parts = ["# 《吕公实政录》%s 白话译本" % vol_name,
             "", "> 共 %d 条（TRL · 注释性翻译 · 白话文对照源整段截取）" % len(records), ""]
    for r, title in zip(records, titles):
        parts.append("### %s %s" % (r["item_id"], title))
        parts.append("")
        for para in r["translation"].split("\n"):
            parts.append(para)
            parts.append("")
        parts.append("")
    with io.open(os.path.join(MD_DIR, "%s_%s_白话译本.md" % (vol_no, vol_name)), "w",
                 encoding="utf-8", newline="\n") as f:
        f.write("\n".join(parts))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="《吕公实政录》TRL 古今翻译层打包器")
    ap.add_argument("--volumes", nargs="*", help="册号（01~15），缺省全量")
    args = ap.parse_args()
    sys.exit(build(volumes=args.volumes))
