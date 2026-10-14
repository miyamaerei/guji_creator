# -*- coding: utf-8 -*-
"""P0-3 清除「未明」假填充

问题：laws / rituals / ents 等层用字符串 "未明" 占位，使记录数虚高、信息量为零。
处理：
  1. 把占位值 "未明" / ["未明"] 一律清空（设为 "" 或 []）。
  2. 在记录上加 "_todo" 字段，登记仍待抽取的字段名。
  3. 对能从 original 原文中廉价、可靠推导的字段（如 laws.punishment_type /
     source_law）做一次保守回填；推导不出则留空 + _todo。
  4. 输出审计报告 _p0_cleared_report.json。
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
LAY = os.path.join(ROOT, "_layers")

PLACEHOLDERS = {"未明", "不详", "未知"}

# laws 处罚类型关键词（保守）
PUNISH_PAT = [
    ("凌迟", "凌迟"), ("绞", "绞"), ("斩", "斩"), ("充军", "充军"),
    ("迁徙", "迁徙"), ("为民", "为民"), ("杖", "杖"), ("笞", "笞"),
    ("徒", "徒"), ("流", "流"), ("罢职", "罢职"), ("罚俸", "罚俸"),
]
LAW_BOOKS = ["大明律", "诸司职掌", "皇明祖训", "大诰", "大明令", "明集礼",
             "洪武礼制", "礼仪定式", "稽古定制", "孝慈录", "教民榜文", "军法定律", "宪纲"]


def is_placeholder(v):
    if isinstance(v, dict):
        return False
    if isinstance(v, list):
        if len(v) == 0:
            return False  # 空列表本身已是空，无需清理
        return all(isinstance(x, str) and x in PLACEHOLDERS for x in v)
    return v in PLACEHOLDERS


def derive_punishment(original):
    """从原文推导处罚类型（可多个，用/连接）。"""
    found = []
    for kw, label in PUNISH_PAT:
        if kw in original and label not in found:
            found.append(label)
    return "/".join(found)


def derive_source_law(original):
    for b in LAW_BOOKS:
        if b in original:
            return b
    return ""


def clean_layer(path, name, report):
    data = json.load(open(path, encoding="utf-8"))
    if not isinstance(data, list):
        return
    cleared = {}
    refilled = {}
    for rec in data:
        if not isinstance(rec, dict):
            continue
        todo = []
        for k, v in list(rec.items()):
            if k.startswith("_"):
                continue
            if is_placeholder(v):
                # 先尝试廉价回填
                refilled_here = False
                if name == "laws" and k == "punishment_type" and rec.get("original"):
                    d = derive_punishment(rec["original"])
                    if d:
                        rec[k] = d
                        refilled.setdefault(k, 0)
                        refilled[k] += 1
                        refilled_here = True
                if name == "laws" and k == "source_law" and rec.get("original"):
                    d = derive_source_law(rec["original"])
                    if d:
                        rec[k] = d
                        refilled.setdefault(k, 0)
                        refilled[k] += 1
                        refilled_here = True
                if not refilled_here:
                    rec[k] = [] if isinstance(v, list) else ""
                    cleared[k] = cleared.get(k, 0) + 1
                    todo.append(k)
        if todo:
            rec["_todo"] = sorted(set(rec.get("_todo", []) + todo))
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if cleared or refilled:
        report[name] = {"cleared": cleared, "refilled": refilled}
        print("%-14s 清空 %s | 回填 %s" % (name, dict(cleared), dict(refilled)))


def main():
    report = {}
    for f in sorted(os.listdir(LAY)):
        if not f.endswith(".json"):
            continue
        clean_layer(os.path.join(LAY, f), f[:-5], report)
    json.dump(report, open(os.path.join(ROOT, "_p0_cleared_report.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("\n审计报告 -> _p0_cleared_report.json")
    # 复核
    import collections
    for f in sorted(os.listdir(LAY)):
        if not f.endswith(".json"): continue
        d = json.load(open(os.path.join(LAY, f), encoding="utf-8"))
        if not isinstance(d, list): continue
        c = collections.Counter()
        for rec in d:
            if not isinstance(rec, dict): continue
            for k, v in rec.items():
                if v == "未明" or v == ["未明"]:
                    c[k] += 1
        if c:
            print("⚠ 仍有未明:", f, dict(c))
    print("复核完成。")


if __name__ == "__main__":
    main()
