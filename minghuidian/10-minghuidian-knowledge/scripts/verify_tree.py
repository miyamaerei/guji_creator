#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《明会典》实例 父子层树校验脚本
验证 references/schemas.md §0 节点注册表的父子关系正确性。
规则见 schemas.md §0.3。
"""

import sys
from collections import deque

# === 节点注册表（与 schemas.md §0.2 同步，改一处需同步另一处）===
# node_id: (name, parent, kind, groups, note)
NODES = {
    # root
    "L0":           ("底座",            None,        "root",          ["G0","G1","G2","G3","G4","G5","G6","G7","G8"], ""),
    "L1":           ("实体",            None,        "root",          ["G0","G1","G2","G3","G4","G5","G6","G7","G8"], ""),
    "L2":           ("规则与时间",      None,        "root",          ["G0","G1","G2","G3","G4","G5","G6","G7","G8"], ""),
    "L3":           ("结构关系",        None,        "root",          ["G0","G1","G2","G3","G4","G5","G6","G7","G8"], ""),
    "L4":           ("六部业务域",      None,        "root",          [], "按卷组启用"),
    "L5":           ("数字与名物",      None,        "root",          [], "按卷组启用"),
    "L6":           ("引用与文册",      None,        "root",          [], "按卷组启用"),

    # L1 common_type
    "L1.org":       ("衙门实体",        "L1",        "common_type",   ["G0","G1","G2","G3","G4","G5","G6","G7","G8"], ""),
    "L1.off":       ("官职实体",        "L1",        "common_type",   ["G1","G4","G7","G8"], ""),
    "L1.geo":       ("地名实体",        "L1",        "common_type",   ["G2","G3","G4","G6"], ""),
    "L1.doc":       ("典籍实体",        "L1",        "common_type",   ["G1","G5"], ""),
    "L1.obj":       ("器物实体",        "L1",        "common_type",   ["G3","G6","G8"], ""),
    "L1.era":       ("年号实体",        "L1",        "common_type",   ["G0","G1","G2","G3","G4","G5","G6","G7","G8"], ""),

    # L2 common_child
    "L2.RUL":       ("事例规则",        "L2",        "common_child",  ["G0","G1","G2","G3","G4","G5","G6","G7","G8"], ""),
    "L2.TIM":       ("制度时间线",      "L2",        "common_child",  ["G1","G2","G3","G4","G5","G6"], ""),

    # L3 common_child
    "L3.ORG":       ("部门结构树",      "L3",        "common_child",  ["G0","G1","G7","G8"], ""),
    "L3.GEO":       ("地理管辖树",      "L3",        "common_child",  ["G2","G4"], ""),
    "L3.RANK":      ("品级等级树",      "L3",        "common_child",  ["G1","G3"], ""),
    "L3.NJC":       ("两京对照",        "L3",        "common_child",  ["G3","G7"], ""),
    "L3.XREF":      ("互见索引",        "L3",        "common_child",  ["G1","G2","G7"], ""),

    # L4 business_domain
    "L4.SEL":       ("吏部域",          "L4",        "business_domain", ["G1","G7"], ""),
    "L4.FIN":       ("户部域",          "L4",        "business_domain", ["G2"], ""),
    "L4.RIT":       ("礼部域",          "L4",        "business_domain", ["G3"], ""),
    "L4.MIL":       ("兵部域",          "L4",        "business_domain", ["G4","G8"], ""),
    "L4.LAW":       ("刑部域",          "L4",        "business_domain", ["G5"], ""),
    "L4.ENG":       ("工部域",          "L4",        "business_domain", ["G6"], ""),

    # L4.SEL business_sub
    "L4.SEL.XUAN":  ("铨选",            "L4.SEL",    "business_sub",  ["G1","G7"], ""),
    "L4.SEL.KAO":   ("考满考察",        "L4.SEL",    "business_sub",  ["G1","G7"], ""),
    "L4.SEL.FENG":  ("封赠荫叙",        "L4.SEL",    "business_sub",  ["G1"], ""),
    "L4.SEL.LI":    ("吏员资格",        "L4.SEL",    "business_sub",  ["G1"], ""),
    "L4.SEL.DING":  ("丁忧起复",        "L4.SEL",    "business_sub",  ["G1","G7"], ""),
    "L4.SEL.HUANG": ("贴黄脚色",        "L4.SEL",    "business_sub",  ["G1"], ""),

    # L4.FIN business_sub
    "L4.FIN.TIAN":  ("土田户口",        "L4.FIN",    "business_sub",  ["G2"], ""),
    "L4.FIN.SHUI":  ("税粮则例",        "L4.FIN",    "business_sub",  ["G2"], ""),
    "L4.FIN.CAO":   ("漕运海运",        "L4.FIN",    "business_sub",  ["G2"], ""),
    "L4.FIN.CANG":  ("仓庚库藏",        "L4.FIN",    "business_sub",  ["G2"], ""),
    "L4.FIN.LU":    ("俸禄折色",        "L4.FIN",    "business_sub",  ["G2"], ""),
    "L4.FIN.TU":    ("土贡方物",        "L4.FIN",    "business_sub",  ["G2"], ""),
    "L4.FIN.ZA":    ("盐茶钱法",        "L4.FIN",    "business_sub",  ["G2"], ""),

    # L4.RIT business_sub
    "L4.RIT.CHAO":  ("朝仪班序",        "L4.RIT",    "business_sub",  ["G3"], ""),
    "L4.RIT.SI":    ("郊庙祭祀",        "L4.RIT",    "business_sub",  ["G3"], ""),
    "L4.RIT.JIA":   ("冠婚丧祭",        "L4.RIT",    "business_sub",  ["G3"], ""),
    "L4.RIT.FU":    ("冠服车舆",        "L4.RIT",    "business_sub",  ["G3"], "与 L3.RANK 交叉"),
    "L4.RIT.GONG":  ("朝贡互市",        "L4.RIT",    "business_sub",  ["G3"], ""),
    "L4.RIT.SENG":  ("僧管道录",        "L4.RIT",    "business_sub",  ["G3"], ""),
    "L4.RIT.YUE":   ("乐章乐器",        "L4.RIT",    "business_sub",  ["G3"], ""),
    "L4.RIT.SHEN":  ("神祇地理",        "L4.RIT",    "business_sub",  ["G3"], ""),

    # L4.MIL business_sub
    "L4.MIL.XUAN":  ("武选袭替",        "L4.MIL",    "business_sub",  ["G4","G8"], ""),
    "L4.MIL.WEI":   ("卫所镇守",        "L4.MIL",    "business_sub",  ["G4","G8"], ""),
    "L4.MIL.GUAN":  ("关津巡检",        "L4.MIL",    "business_sub",  ["G4"], ""),
    "L4.MIL.YI":    ("驿传递运",        "L4.MIL",    "business_sub",  ["G4"], ""),
    "L4.MIL.MA":    ("马政牧养",        "L4.MIL",    "business_sub",  ["G4"], ""),
    "L4.MIL.QI":    ("军器军装",        "L4.MIL",    "business_sub",  ["G4"], "与 L4.ENG.JUN 交叉引用（XREF）"),

    # L4.LAW business_sub
    "L4.LAW.LI":    ("明律条款",        "L4.LAW",    "business_sub",  ["G5"], ""),
    "L4.LAW.WU":    ("五刑比例",        "L4.LAW",    "business_sub",  ["G5"], ""),
    "L4.LAW.HUI":   ("会审审录",        "L4.LAW",    "business_sub",  ["G5"], ""),
    "L4.LAW.ZANG":  ("追赃赎罪",        "L4.LAW",    "business_sub",  ["G5"], ""),
    "L4.LAW.TU":    ("土官诉讼",        "L4.LAW",    "business_sub",  ["G5"], ""),

    # L4.ENG business_sub
    "L4.ENG.DIAN":  ("内府宫殿",        "L4.ENG",    "business_sub",  ["G6"], ""),
    "L4.ENG.WANG":  ("亲王府制",        "L4.ENG",    "business_sub",  ["G6"], ""),
    "L4.ENG.LING":  ("陵寝坟茔",        "L4.ENG",    "business_sub",  ["G6"], ""),
    "L4.ENG.YU":    ("舟车仪仗",        "L4.ENG",    "business_sub",  ["G6"], "G8 锦衣卫仪仗经 XREF 引用本节点"),
    "L4.ENG.JUN":   ("军器军装",        "L4.ENG",    "business_sub",  ["G6"], "与 L4.MIL.QI 交叉"),
    "L4.ENG.LIAO":  ("物料工价",        "L4.ENG",    "business_sub",  ["G6"], ""),
    "L4.ENG.HE":    ("河渠水利",        "L4.ENG",    "business_sub",  ["G6"], ""),

    # L5 common_child
    "L5.NUM":       ("数字则例",        "L5",        "common_child",  ["G2","G6"], ""),
    "L5.NAM":       ("名录",            "L5",        "common_child",  ["G0","G2","G3","G4","G8"], ""),
    "L5.OBJ":       ("器物",            "L5",        "common_child",  ["G3","G6","G8"], ""),

    # L6 common_child
    "L6.CIT":       ("典籍直引",        "L6",        "common_child",  ["G1","G3","G5"], ""),
    "L6.REPORT":    ("文册勘合",        "L6",        "common_child",  ["G2"], ""),
}

# kind 允许的 parent kind 映射
KIND_PARENT_RULE = {
    "root":           {None},
    "common_type":    {"root"},          # 只能挂在 L1
    "common_child":   {"root"},          # 挂在对应 root，下面再校验 root 是否对
    "business_domain":{"root"},          # 只能挂在 L4
    "business_sub":   {"business_domain"},
}

# common_child 必须挂在哪个 root 下（前缀匹配）
COMMON_CHILD_ROOT = {
    "L2.": "L2",   # RUL/TIM
    "L3.": "L3",   # ORG/GEO/RANK/NJC/XREF
    "L5.": "L5",   # NUM/NAM/OBJ
    "L6.": "L6",   # CIT/REPORT
}

VALID_GROUPS = {"G0","G1","G2","G3","G4","G5","G6","G7","G8"}


def verify():
    errors = []
    warnings = []

    # 规则 1: root 节点 parent 必为空
    for nid, (name, parent, kind, groups, note) in NODES.items():
        if kind == "root" and parent is not None:
            errors.append(f"[R1] root 节点 {nid} 的 parent 必须为空（当前={parent}）")
        if kind != "root" and parent is None:
            errors.append(f"[R1] 非 root 节点 {nid} 必须有 parent")

    # 规则 2: parent 必须存在
    for nid, (name, parent, kind, groups, note) in NODES.items():
        if parent is not None and parent not in NODES:
            errors.append(f"[R2] {nid} 的 parent={parent} 在注册表中不存在")

    # 规则 3: kind 与 parent kind 匹配
    for nid, (name, parent, kind, groups, note) in NODES.items():
        if parent is None:
            continue
        parent_kind = NODES[parent][2]
        allowed_parents = KIND_PARENT_RULE.get(kind, set())
        if parent_kind not in allowed_parents:
            errors.append(f"[R3] {nid}({kind}) 不能挂在 {parent}({parent_kind}) 下，允许的 parent kind={allowed_parents}")

    # 规则 3.1: common_type 只能挂在 L1
    for nid, (name, parent, kind, groups, note) in NODES.items():
        if kind == "common_type" and parent != "L1":
            errors.append(f"[R3.1] common_type 节点 {nid} 必须挂在 L1 下（当前 parent={parent}）")

    # 规则 3.2: common_child 必须挂在对应 root 下
    for nid, (name, parent, kind, groups, note) in NODES.items():
        if kind == "common_child":
            expected_root = None
            for prefix, root in COMMON_CHILD_ROOT.items():
                if nid.startswith(prefix):
                    expected_root = root
                    break
            if expected_root is None:
                errors.append(f"[R3.2] common_child 节点 {nid} 前缀未在 COMMON_CHILD_ROOT 登记")
            elif parent != expected_root:
                errors.append(f"[R3.2] common_child 节点 {nid} 必须挂在 {expected_root} 下（当前 parent={parent}）")

    # 规则 3.3: business_domain 只能挂在 L4
    for nid, (name, parent, kind, groups, note) in NODES.items():
        if kind == "business_domain" and parent != "L4":
            errors.append(f"[R3.3] business_domain 节点 {nid} 必须挂在 L4 下（当前 parent={parent}）")

    # 规则 4: 禁止跨层挂接（由 R3 覆盖，这里补 business_sub 不能挂在 common_child）
    # 已由 R3 的 KIND_PARENT_RULE 覆盖

    # 规则 5: 无环——沿 parent 上溯必到 root
    for nid in NODES:
        seen = set()
        cur = nid
        while cur is not None:
            if cur in seen:
                errors.append(f"[R5] 检测到环：从 {nid} 上溯再次遇到 {cur}")
                break
            seen.add(cur)
            cur = NODES[cur][1]

    # 规则 6: 卷组合法
    for nid, (name, parent, kind, groups, note) in NODES.items():
        for g in groups:
            if g not in VALID_GROUPS:
                errors.append(f"[R6] {nid} 启用卷组 {g} 不合法（合法={sorted(VALID_GROUPS)}）")

    # 规则 7: 业务子层不越界——business_sub 的启用卷组必须是其父 business_domain 的子集
    for nid, (name, parent, kind, groups, note) in NODES.items():
        if kind == "business_sub":
            parent_groups = set(NODES[parent][3])
            sub_groups = set(groups)
            extra = sub_groups - parent_groups
            if extra:
                errors.append(f"[R7] business_sub {nid} 启用卷组 {extra} 超出父节点 {parent} 的卷组 {parent_groups}")

    # 规则 8: 每个 business_domain 至少有一个 business_sub
    for nid, (name, parent, kind, groups, note) in NODES.items():
        if kind == "business_domain":
            children = [k for k, v in NODES.items() if v[1] == nid and v[2] == "business_sub"]
            if not children:
                errors.append(f"[R8] business_domain {nid} 没有 business_sub 子节点")

    # 统计
    counts = {}
    for nid, (name, parent, kind, groups, note) in NODES.items():
        counts[kind] = counts.get(kind, 0) + 1

    # 每个卷组启用了多少节点
    group_counts = {g: 0 for g in VALID_GROUPS}
    for nid, (name, parent, kind, groups, note) in NODES.items():
        for g in groups:
            group_counts[g] += 1

    return errors, warnings, counts, group_counts


def main():
    errors, warnings, counts, group_counts = verify()

    print("=" * 60)
    print("《明会典》父子层树校验报告")
    print("=" * 60)
    print(f"\n节点总数: {len(NODES)}")
    print(f"节点性质分布:")
    for k, v in sorted(counts.items()):
        print(f"  {k:18s}: {v}")
    print(f"\n各卷组启用节点数:")
    for g in sorted(group_counts):
        print(f"  {g}: {group_counts[g]}")

    print(f"\n--- 校验结果 ---")
    if errors:
        print(f"FAIL: {len(errors)} 个错误")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("PASS: 所有父子关系校验通过")

    if warnings:
        print(f"\n警告 {len(warnings)} 条:")
        for w in warnings:
            print(f"  ⚠ {w}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
