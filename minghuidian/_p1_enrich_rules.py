# -*- coding: utf-8 -*-
"""P1-A 重抽 rules 层

现状：rules 3,594 条已有 subject/action/condition/purpose，但缺
  - original（原文，无法溯源）
  - era（年号/纪年，无法做时间线）
  - section / volume（事目与卷，无法按门类检索）
  - subject_ent_ids（与实体/衙门不互链）

本脚本从底座 _item_registry.json 回填 original/section/volume/node_kind，
并从原文抽取年号，规范化 subject，链接到全局衙门索引（若存在）。
"""
import json, os, re, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
LAY = os.path.join(ROOT, "_layers")

ERA_CANON = {
    "洪武": "洪武", "永乐": "永乐", "洪熙": "洪熙", "洪熈": "洪熙",
    "宣德": "宣德", "宣徳": "宣德", "正统": "正统", "景泰": "景泰",
    "天顺": "天顺", "成化": "成化", "弘治": "弘治", "正德": "正德",
    "嘉靖": "嘉靖", "隆庆": "隆庆", "万历": "万历", "万厯": "万历",
}
ERA_RE = re.compile(r"(洪武|永乐|洪熙|洪熈|宣德|宣徳|正统|景泰|天顺|成化|弘治|正德|嘉靖|隆庆|万历|万厯)([元一二三四五六七八九十百零]{0,6}年)?")
# 事件动词（演变链用）
EVENT_KW = [("置", "立"), ("设立", "立"), ("设", "立"), ("定", "定"),
            ("改", "改"), ("罢", "罢"), ("革", "革"), ("复", "复"),
            ("增", "增"), ("减", "减"), ("添设", "增"), ("裁", "减"),
            ("并", "并"), ("归", "并"), ("废", "罢")]


def extract_era(orig):
    """抽取年号与纪年原文。返回 (era_list, era_raw_list, era_first)"""
    eras, raws = [], []
    for m in ERA_RE.finditer(orig or ""):
        e = ERA_CANON.get(m.group(1), m.group(1))
        raw = m.group(0)
        if e not in eras:
            eras.append(e)
        if raw not in raws:
            raws.append(raw)
    first = ""
    if orig:
        if orig.startswith("国初") or "国初" in orig[:6]:
            first = "国初"
        elif eras:
            first = eras[0]
    return eras, raws, first


def extract_event(orig):
    """从原文识别沿革事件（立/改/罢/复/增/减/并）。"""
    evs = []
    for kw, label in EVENT_KW:
        if kw in (orig or "") and label not in evs:
            evs.append(label)
    return evs


def main():
    reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
    rules = json.load(open(os.path.join(LAY, "rules.json"), encoding="utf-8"))

    # 全局衙门索引（若 P1-D 已生成）
    org_index = {}
    op = os.path.join(LAY, "org_profiles.json")
    if os.path.exists(op):
        for o in json.load(open(op, encoding="utf-8")):
            nm = o.get("org_name")
            if nm:
                org_index[nm] = o.get("org_id") or nm

    filled = collections.Counter()
    for x in rules:
        iid = x.get("item_id")
        base = reg.get(iid, {})
        orig = base.get("original", "")
        # 1) original / 门类 / 卷
        x["original"] = orig
        x["section"] = base.get("section", "")
        x["volume"] = base.get("volume")
        x["node_kind"] = base.get("node_kind", "")
        if orig:
            filled["original"] += 1
        # 2) era
        eras, raws, first = extract_era(orig)
        x["era"] = eras
        x["era_raw"] = raws
        x["era_first"] = first
        if eras or first:
            filled["era"] += 1
        # 3) 沿革事件
        evs = extract_event(orig)
        if evs:
            x["event_types"] = evs
            filled["event_types"] += 1
        # 4) subject 规范化 + 实体链接
        subj = x.get("subject", "")
        x["subject_norm"] = subj
        if subj in org_index:
            x["subject_org_id"] = org_index[subj]
            filled["subject_org_id"] += 1
        # 5) 行文标记来源（凡例枚举）
        sm = x.get("source_marker", "")
        if sm and sm not in ("凡",):
            filled["source_marker_nonfan"] += 1

    json.dump(rules, open(os.path.join(LAY, "rules.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    n = len(rules)
    print("rules 增强完成：%d 条" % n)
    for k in ["original", "era", "event_types", "subject_org_id", "source_marker_nonfan"]:
        print("  %-22s %5d/%d (%.0f%%)" % (k, filled[k], n, 100 * filled[k] / n))
    print("  era 分布:", collections.Counter(x.get("era_first") for x in rules).most_common(12))


if __name__ == "__main__":
    main()
