# -*- coding: utf-8 -*-
"""《平平言》古今翻译层（TRL）打包器：白话文分卷译本 → 对齐指纹库 → TRL 记录。

依据 Skills/00-book-knowledge-factory 层库 C5 古今翻译层（TRL）：
    记录 schema：trl_id / item_id / translation / style / note / confidence / original / norm
    ID 前缀：TRL-（本工程内全局唯一，trl_id = TRL-<卷NN><条NNN>，可由 item_id 直接还原）
    风格枚举：直译/意译/注释性翻译（本书取"注释性翻译"——白话正文 + 专名/年代括注，
              见 白话文/_翻译规格.md §二.3/§二.4）

输入（对照引用源，非抽取依据）：
    白话文/卷一~卷四_白话.txt   分卷白话译本（○标题照抄原文、正文白话）
    _item_registry.json        指纹库（original/norm 唯一源，打包器注入，不手抄）
硬校验（不过即报错，退出码 1）：
    * 卷头【平平言卷X】/（卷首篇目）/（正文）结构完整
    * 每册 白话条数 = 指纹库条数（C5 覆盖校验：条目数=翻译数）
    * 标题按序逐一相等（剥 ○ 前缀与首尾空白后比对）
    * 译文非空；original 注入后与指纹库逐条一致
产出：
    _layers/trl/trl_NN.json             {"records": [...]}（与 ent/rule/struct 等层同构）
    _layers/trl/trl_summary.json        层级汇总
    _layers/trl/全书白话译本/NN_卷名.md  可读译本（条号 + 标题 + 译文）

用法（从工程根 pingpingyan-kb/ 执行）：
    python build_trl.py                  # 全量 4 卷
    python build_trl.py --volumes 01 03  # 指定卷
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
CN_VOL = {"一": "01", "二": "02", "三": "03", "四": "04"}
VOL_FILES = {"01": "卷一_白话.txt", "02": "卷二_白话.txt",
             "03": "卷三_白话.txt", "04": "卷四_白话.txt"}


def read_lines(path):
    return [ln.strip() for ln in io.open(path, encoding="utf-8").read().splitlines() if ln.strip()]


def parse_baihua(path, vol_no):
    """解析分卷白话文件：返回 [(title, body_lines)]。跳过（卷首篇目）区；
    ○ 行 = 新条目标题（照抄原文），其余行为当前条目译文续行。"""
    lines = read_lines(path)
    issues = []
    expect_head = "【平平言卷%s】" % next(k for k, v in CN_VOL.items() if v == vol_no)
    if not lines or lines[0] != expect_head:
        issues.append("%s：卷头应为 %r，实际 %r" % (os.path.basename(path), expect_head,
                                                  lines[0] if lines else "<空文件>"))
    if "（卷首篇目）" not in lines or "（正文）" not in lines:
        issues.append("%s：缺（卷首篇目）/（正文）分节标记" % os.path.basename(path))
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
        else:
            issues.append("%s：（正文）后、首条 ○ 前出现游离行 %r" % (os.path.basename(path), ln[:40]))
    return items, issues


def build(volumes=None, verbose=True):
    with io.open(REGISTRY_PATH, encoding="utf-8") as f:
        registry = json.load(f)
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(MD_DIR, exist_ok=True)

    issues = []
    total_records = 0
    covered = []
    vols = sorted(VOL_FILES) if not volumes else [v for v in sorted(VOL_FILES) if v in volumes]

    for vol_no in vols:
        src = os.path.join(BAIHUA_DIR, VOL_FILES[vol_no])
        if not os.path.isfile(src):
            issues.append("卷 %s：缺白话文件 %s" % (vol_no, src))
            continue
        items, iss = parse_baihua(src, vol_no)
        issues.extend(iss)

        reg_ids = sorted(k for k in registry if k.startswith(vol_no + "-"))
        reg_titles = [registry[k]["original"].split("\n")[0].lstrip("○△").strip() for k in reg_ids]
        bai_titles = [t for t, _ in items]

        if len(reg_ids) != len(items):
            issues.append("卷 %s：条目数≠翻译数（指纹库 %d / 白话 %d），本卷不产出"
                          % (vol_no, len(reg_ids), len(items)))
            continue
        mism = [(i, a, b) for i, (a, b) in enumerate(zip(reg_titles, bai_titles)) if a != b]
        if mism:
            for i, a, b in mism[:5]:
                issues.append("卷 %s 第 %d 条标题不齐：指纹库 %r ≠ 白话 %r" % (vol_no, i + 1, a, b))
            issues.append("卷 %s：标题对齐失败（共 %d 处），本卷不产出" % (vol_no, len(mism)))
            continue

        records = []
        for seq, (item_id, (title, body)) in enumerate(zip(reg_ids, items), 1):
            translation = "\n".join(body).strip()
            if not translation:
                issues.append("卷 %s %s：译文为空" % (vol_no, item_id))
                continue
            records.append({
                "trl_id": "TRL-%s%03d" % (vol_no, seq),
                "item_id": item_id,
                "translation": translation,
                "style": STYLE,
                "note": "整段取自白话文对照源：白话文/%s（○标题照抄原文，正文白话）" % VOL_FILES[vol_no],
                "confidence": 1.0,
                "original": registry[item_id]["original"],
                "norm": registry[item_id]["norm"],
            })
        # original 注入一致性复核
        for r in records:
            if r["original"] != registry[r["item_id"]]["original"]:
                issues.append("卷 %s %s：original 与指纹库不一致" % (vol_no, r["item_id"]))

        with io.open(os.path.join(OUT_DIR, "trl_%s.json" % vol_no), "w", encoding="utf-8",
                     newline="\n") as f:
            json.dump({"records": records}, f, ensure_ascii=False, indent=2)
            f.write("\n")
        write_md(vol_no, records, reg_titles)
        total_records += len(records)
        covered.append(vol_no)
        if verbose:
            print("卷 %s: %d 条 TRL 记录" % (vol_no, len(records)))

    summary = {
        "layer": "trl",
        "record_count": total_records,
        "volumes_covered": covered,
        "style": STYLE,
        "id_rule": "trl_id = TRL-<卷NN><条NNN>，可由 item_id 还原",
        "source": "白话文/卷一~卷四_白话.txt（对照引用源，整段截取，不参与抽取）",
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


def write_md(vol_no, records, titles):
    """可读译本：### 条号 标题 + 译文（源文件一行一段，空行分段）。"""
    vol_cn = {v: k for k, v in CN_VOL.items()}[vol_no]
    parts = ["# 《平平言》卷%s 白话译本" % vol_cn,
             "", "> 共 %d 条（TRL · 注释性翻译 · 白话文对照源整段截取）" % len(records), ""]
    for r, title in zip(records, titles):
        parts.append("### %s %s" % (r["item_id"], title))
        parts.append("")
        for para in r["translation"].split("\n"):
            parts.append(para)
            parts.append("")
        parts.append("")
    with io.open(os.path.join(MD_DIR, "%s_卷%s_白话译本.md" % (vol_no, vol_cn)), "w",
                 encoding="utf-8", newline="\n") as f:
        f.write("\n".join(parts))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="《平平言》TRL 古今翻译层打包器")
    ap.add_argument("--volumes", nargs="*", help="卷号（01 02 03 04），缺省全量")
    args = ap.parse_args()
    sys.exit(build(volumes=args.volumes))
