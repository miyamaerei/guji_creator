# -*- coding: utf-8 -*-
"""P1-A2: rules 补 condition / punishment（Q2「一条事例的完整要素」）。

condition：以「若/如/遇/倘」条件连词与「凡…者/有…者」者-小句为主，抽适用条件。
punishment：抽处罚语并归入 五刑/降黜/罚俸/财产/问拟 等档，填 punishment_level。
"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
LAY = os.path.join(ROOT, "_layers")
rules = json.load(open(os.path.join(LAY, "rules.json"), encoding="utf-8"))
PUA = {0xE5AB: "隶", 0xEA1F: "弘", 0xF5F6: "封", 0xEB08: "卷"}


def nz(t):
    return "".join(PUA.get(ord(c), c) for c in t)


COND_PATS = [re.compile(p) for p in (
    r"若(.{2,24}?)[，。；　]",
    r"如(.{2,24}?)[，。；　]",
    r"遇(.{2,24}?)[，。；　]",
    r"倘(.{2,24}?)[，。；　]",
    r"有(.{2,20}?)者",
    r"凡(.{2,26}?)者",
)]
# 处罚（有序：先具体刑名，后泛称）
PUN_LEVELS = [
    ("死刑", r"(凌迟|斩|绞)"),
    ("流刑", r"(充军|发充军|流[一二三四五六七八九十百千]+里|发配|编管)"),
    ("徒刑", r"(徒[一二三四五六七八九十]+年)"),
    ("杖刑", r"(杖[一二三四五六七八九十百]+十?)"),
    ("笞刑", r"(笞[一二三四五六七八九十百]+十?)"),
    ("降黜", r"(降[一二三四五六七八九十]+级|罢职|黜为[^，。；]{0,6}|黜|削籍|除名|为民|发为民)"),
    ("罚俸", r"(罚俸[一二三四五六七八九十]+个月?|罚俸一年|停俸)"),
    ("财产", r"(籍没[^，。；]{0,8}|追[^，。；]{0,6}还官|追赃|追征|收赎|纳赎|运炭|纳米赎罪)"),
    ("问拟", r"(问罪|治罪|论罪|拟罪|依律[^，。；]{0,10}|照律[^，。；]{0,10}|减等|加等|免罪|免罚|免究)"),
]
PUN_PATS = [(lvl, re.compile(rx)) for lvl, rx in PUN_LEVELS]

c_fill = p_fill = 0
lvl_counter = Counter()
for x in rules:
    t = nz(x.get("original") or "")
    # condition（优先高精度连词；已有则保留）
    if not x.get("condition"):
        cond = None
        for rx in COND_PATS:
            m = rx.search(t)
            if m:
                cond = m.group(1)
                break
        if cond and 2 <= len(cond) <= 30:
            x["condition"] = cond
            c_fill += 1
    else:
        c_fill += 1
    # punishment
    if not x.get("punishment"):
        for lvl, rx in PUN_PATS:
            m = rx.search(t)
            if m:
                x["punishment"] = m.group(1)
                x["punishment_level"] = lvl
                lvl_counter[lvl] += 1
                p_fill += 1
                break
    else:
        p_fill += 1

json.dump(rules, open(os.path.join(LAY, "rules.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

n = len(rules)
print(f"rules {n} 条")
print(f"  condition        : {sum(1 for x in rules if x.get('condition'))} ({sum(1 for x in rules if x.get('condition'))/n*100:.1f}%)")
print(f"  punishment       : {sum(1 for x in rules if x.get('punishment'))} ({sum(1 for x in rules if x.get('punishment'))/n*100:.1f}%)")
print(f"  punishment_level : {dict(lvl_counter)}")
print("--- 抽样 ---")
shown = 0
for x in rules:
    if x.get("condition") and x.get("punishment") and shown < 10:
        print(f"  [{x['item_id']}] 条件={x['condition'][:24]} | 罚={x['punishment']}({x.get('punishment_level')})")
        shown += 1
