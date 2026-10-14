# -*- coding: utf-8 -*-
"""穷尽扫描 v4：对 data_part2b 的 77 条抽候选实体，与已录 ents/gar/hyd/res 比对，输出缺漏清单。
方法：定位每个类别后缀字 → 向左扩展到标点/括号（上限12字，方位词不拦）
→ 取最后一个动词/虚字之后作候选 → 元前朝前缀剥离 → 官署计数后缀截断
→ 纯计数类型短语弃 → 最长保留（子串折叠）→ 与已录名双向子串覆盖。
另输出「软覆盖」清单：tme place / evo owner 提过但 ent/gar/hyd/res 层未录的名字。
只做候选抽取，判定由人工逐条完成。"""

import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from data_part1 import PART

reg = json.load(io.open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 类别后缀字（政区/山水/建筑/机构等名词的类型尾）
SUFFIX = set("山峰岭崖矶洞岩石潭洲屿湾澳荡浦泾浜渡桥驿关镇市司县州府卫所堡寨隘口城台楼阁亭寺观庙塔院园林墅村庄墟集店坊江湖河池井泉溪路")

# 截断点：动词/虚词/句式功能字（取 cand 中最后一个之后）。
# 注意：会/等/将/沿/通/源/尽/益/达/望 等不入列——它们会拦腰截断专名
# （会同县、X等处Y司、将军山、沿边溪洞宣抚司、水尽源通塔平长官司、益州）。
LAST_VERB = set("的了为于在之其以与及或又今故旧是曰称名有属置升降改省入至距领自谓出流合移经界境析徙筑连接抵溯汇皆亦复更当治本即源隶支后迁存者凡俱")

# 截断后残留这些字则弃（句式虚字，不出现在实体名中）
INNER_BAD = set("之以为于在与及或其谓曰在皆亦复更者凡俱")

# 官署计数后缀：X二巡检司 / X三所 / X二峒口 / X二峰 / X二县 → 截回 X（截后须 >=2 字）
COUNT_TAIL = re.compile(
    r"[一二两三四五六七八九十数](?:巡检司|千户所|百户所|宣慰司|安抚司|招讨司|长官司|"
    r"宣抚司|万户府|千户府|府|司|所|卫|峒|口|峰|山|岭|岩|洞|寨|堡|关|镇|市|驿|城|寺|观|"
    r"院|园|亭|台|楼|阁|庄|村|墟|集|店|坊|浦|湾|荡|渡|桥|塔|庙|林|墅|洲|矶|崖|石|水|江|溪|河|湖|池|井|泉|县)$"
)

# 纯计数+类型短语（四长官司 / 七十四寨 / 二巡检司）→ 弃
COUNT_PURE = re.compile(
    r"^[一二两三四五六七八九十数]+(?:巡检司|千户所|百户所|宣慰司|宣慰使司|安抚司|招讨司|"
    r"长官司|宣抚司|指挥使司|都司|司|所|卫|府|县|州|寨|峒|堡|关|镇|市|驿|城)$"
)

# 裸类型词（非专名）→ 弃
TYPE_WORDS = set("""长官司 宣抚司 安抚司 宣慰司 宣慰使司 招讨司 指挥使司 巡检司 都司
蛮夷官司 军民宣慰司 军民宣抚司 军民安抚司 军民千户所 守御千户所 千户所 百户所 万户府""".split())

# 方位+政区前缀（县北九龙岩 → 九龙岩；州西安定山 → 安定山）
PLACE_DIR_PREFIX = re.compile(r"^(?:县|州|府|卫|所|路|郡|道)[东南西北](?=[\u4e00-\u9fff]{2})")


def covered_hard(rec):
    """硬覆盖：ent/gar/hyd/res/geo 层的已录名。"""
    cov = set()
    g = rec.get("geo") or {}
    if g.get("name"):
        cov.add(g["name"])
    p = g.get("parent") or {}
    if p.get("text"):
        cov.add(p["text"])
    for bd in g.get("bearing_distance") or []:
        if bd.get("to_anchor"):
            cov.add(bd["to_anchor"])
    for e in rec.get("ents") or []:
        cov.add(e.get("text", ""))
    for h in rec.get("hyd") or []:
        cov.add(h.get("name", ""))
    for ga in rec.get("gar") or []:
        cov.add(ga.get("name", ""))
    for r in rec.get("res") or []:
        cov.add(r.get("name", ""))
    cov.discard("")
    return cov


def covered_soft(rec):
    """软覆盖：tme place / evo owner（句式里提过，但未必已录 ent/gar/hyd/res）。"""
    cov = set()
    for t in rec.get("tme") or []:
        if t.get("place"):
            cov.add(t["place"])
    for x in rec.get("evo") or []:
        if x.get("owner"):
            cov.add(x["owner"])
    cov.discard("")
    return cov


def expand_left(norm, p):
    """后缀字下标 p，向左扩展到非中文字符（标点/括号/数字西文），上限12字。"""
    q = p
    while q > 0 and (p - q + 1) < 13:
        c = norm[q - 1]
        if not ("\u4e00" <= c <= "\u9fff"):
            break
        q -= 1
    return norm[q:p + 1]


def cut_last_verb(cand):
    """取 cand 中最后一个 LAST_VERB 字之后的部分；若无则整体返回。"""
    idx = -1
    for i, ch in enumerate(cand):
        if ch in LAST_VERB:
            idx = i
    if idx >= 0 and idx + 1 < len(cand):
        return cand[idx + 1:]
    return cand


def candidates(norm):
    """返回 [(候选, 次数, 首次出现位置)]。"""
    raw = {}
    for i, ch in enumerate(norm):
        if ch not in SUFFIX:
            continue
        cand = expand_left(norm, i)
        if len(cand) < 2:
            continue
        cand = cut_last_verb(cand)
        if len(cand) < 2:
            continue
        if any(c in INNER_BAD for c in cand):
            continue
        # 元前朝前缀剥离：元永州路 → 永州路；元湖 → 湖（单字则弃）
        if cand.startswith("元") and len(cand) >= 2:
            alt = cand[1:]
            if len(alt) >= 2 and alt[0] not in LAST_VERB and alt[0] not in "一二两三四五六七八九十数":
                cand = alt
            else:
                continue
        # 方位+政区前缀剥离
        m = PLACE_DIR_PREFIX.match(cand)
        if m:
            cand = cand[2:]
            if len(cand) < 2:
                continue
        if cand in TYPE_WORDS:
            continue
        if COUNT_PURE.match(cand):
            continue
        raw[cand] = raw.get(cand, 0) + 1
    # 官署计数后缀截断
    fixed = {}
    for cand, n in raw.items():
        m = COUNT_TAIL.search(cand)
        if m and m.start() >= 2:
            cand = cand[:m.start()]
            if len(cand) < 2:
                continue
        fixed[cand] = fixed.get(cand, 0) + n
    # 最长保留：A 是 B 真子串 → 弃 A
    names = sorted(fixed, key=len, reverse=True)
    keep = []
    for a in names:
        if any(a != b and a in b for b in keep):
            continue
        keep.append(a)
    out = []
    for c in keep:
        pos = norm.find(c)
        out.append((c, fixed[c], pos))
    out.sort(key=lambda t: t[2])
    return out


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    total_gap = 0
    total_soft = 0
    for iid in sorted(PART):
        if only and iid not in only:
            continue
        rec = PART[iid]
        norm = reg[iid]["norm"]
        cov = covered_hard(rec)
        soft = covered_soft(rec)
        gap = []
        for c, n, pos in candidates(norm):
            if c in cov:
                continue
            if any(c in x or x in c for x in cov if len(x) >= 2):
                continue
            ctx = norm[max(0, pos - 14):pos + len(c) + 14].replace("\n", " ")
            gap.append((c, n, ctx))
        # 软覆盖：soft 中的名不在硬覆盖里 → 可能该录 ent/gar/hyd
        soft_gap = []
        for s in sorted(soft):
            if s in cov:
                continue
            if any(s in x or x in s for x in cov if len(x) >= 2):
                continue
            pos = norm.find(s)
            ctx = norm[max(0, pos - 14):pos + len(s) + 14].replace("\n", " ") if pos >= 0 else ""
            soft_gap.append((s, ctx))
        if gap or soft_gap:
            print("=== %s（ent %d / gar %d / hyd %d / res %d → 缺 %d，软覆盖 %d）" % (
                iid, len(rec.get("ents") or []), len(rec.get("gar") or []),
                len(rec.get("hyd") or []), len(rec.get("res") or []), len(gap), len(soft_gap)))
            for c, n, ctx in gap:
                print("    %-14s x%d  …%s…" % (c, n, ctx))
                total_gap += 1
            for s, ctx in soft_gap:
                print("    [软] %-10s …%s…" % (s, ctx))
                total_soft += 1
    print("TOTAL_GAP_CANDIDATES=%d  TOTAL_SOFT=%d" % (total_gap, total_soft))


if __name__ == "__main__":
    main()
