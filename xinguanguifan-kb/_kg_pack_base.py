# -*- coding: utf-8 -*-
"""《新官轨范》打包公共基座（P1 合并产物）。
四层打包器共享：常量 / 指纹库加载 / 规则映射 / --volumes 解析 / original+derived_rule 注入 / 实体别名解析。
行为与既有打包器完全一致，仅去重。
"""
import os, sys, json, re

BASE = r"C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat"
CH_DIR = os.path.join(BASE, "新官轨范_章节")
REG_FILE = os.path.join(BASE, "_item_registry.json")
RULE_MERGE = os.path.join(BASE, "新官轨范_规则_ai", "归一_汇总.json")
ENT_KEY = os.path.join(BASE, "新官轨范_实体_主键表.json")
VOL_NUMS = [f"{i:02d}" for i in range(1, 12)]


def load_registry():
    with open(REG_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_rule_map():
    try:
        with open(RULE_MERGE, encoding="utf-8") as f:
            m = json.load(f)
        return {r["item_id"]: r["rule_id"] for r in m.get("rules", [])}
    except Exception:
        return {}


def parse_volumes(argv=None):
    """--volumes 03 04 → {'03','04'}；省略 → None（全量）。"""
    argv = sys.argv if argv is None else argv
    if "--volumes" not in argv:
        return None
    i = argv.index("--volumes")
    parts = []
    for tok in argv[i + 1:]:
        if tok.startswith("--"):
            break
        parts.extend(tok.replace(",", " ").split())
    return set(parts)


def find_xhtml(ch_no):
    hits = [os.path.basename(p) for p in os.listdir(CH_DIR)
            if p.startswith(ch_no + "_") and p.endswith(".xhtml")]
    return hits[0] if hits else None


def resolve_src_id(ch_no, source):
    """source='01_卷上...xhtml#条5' → '01-005'；无法解析返回 None。"""
    try:
        iid = source.split("#条")[-1]
        return "%s-%03d" % (ch_no, int(iid))
    except Exception:
        return None


def inject_common(ch_no, item, reg, rule_map, issues=None):
    """original + derived_rule 注入（rule 层不调用）。返回 (src_id, ok)。"""
    src_id = resolve_src_id(ch_no, item.get("source", ""))
    if not src_id or src_id not in reg:
        if issues is not None:
            issues.append(f"[{ch_no}] source 条号不在指纹库：{item.get('source')}")
        return None, False
    item["original"] = reg[src_id]["original"]
    item["derived_rule"] = rule_map.get(src_id, "")
    return src_id, True


def exec_source(rel_py):
    """执行卷源数据 py，返回命名空间 dict。"""
    vf = os.path.join(BASE, rel_py)
    ns = {}
    exec(compile(open(vf, encoding="utf-8").read(), vf, "exec"), ns)
    return ns


def load_ent_alias():
    """实体主键表 alias_index：surface(text) → [ent_id]。失败返回 {}。"""
    try:
        with open(ENT_KEY, encoding="utf-8") as f:
            d = json.load(f)
        return d.get("alias_index", {})
    except Exception:
        return {}


def resolve_ent_ids(names, alias):
    """文本名 → 实体 ID 列表（机械映射，非判定）。
    - names: str 或 [str]；剥离（解读）括号后按 alias_index 精确匹配。
    - 未命中返回 []（如实，不猜测）。
    """
    if isinstance(names, str):
        names = [names]
    out = []
    for n in names:
        n = (n or "").strip()
        if not n:
            continue
        cand = re.sub(r"（.*?）", "", n).strip()
        if cand and cand in alias:
            out.extend(alias[cand])
    return sorted(set(out))
