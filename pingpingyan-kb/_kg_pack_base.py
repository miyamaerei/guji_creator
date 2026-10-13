# -*- coding: utf-8 -*-
"""《平平言》打包公共基座：路径推导 / 指纹库 / 枚举 / 段位 ID / 卷参数。"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
INSTANCE = os.path.join(ROOT, "12-pingpingyan-knowledge")
SRC_DIR = os.path.join(ROOT, "_src")
LAYER_DIR = os.path.join(ROOT, "_layers")
BUILD_DIR = os.path.join(ROOT, "_build")
GLOBAL_DIR = os.path.join(ROOT, "_global")
REGISTRY_PATH = os.path.join(ROOT, "_item_registry.json")
ENUMS_PATH = os.path.join(ROOT, "_kg_enums.py")
SOURCE_DIR = os.path.join(INSTANCE, "assets", "sources")  # 切分主源（卷拆分 txt，UTF-8）

# 契约登记表（C4，与实例 references/schemas.md §2 一致：ent/rule/struct/reg/opn 5 层）
LAYER_SCHEMA = {
    "ent": {"prefix": "ENT-", "dir": "ent",
            "schema_fields": ["ent_id", "item_id", "text", "type", "start", "end",
                              "normalized", "confidence", "source", "original"],
            "enum_fields": ["type"]},
    "rule": {"prefix": "RULE-", "dir": "rule",
             "schema_fields": ["rule_id", "item_id", "type", "modals", "condition",
                               "subject", "subject_ent_ids", "action", "object",
                               "purpose", "punishment", "original", "confidence"],
             "enum_fields": ["type"]},
    "struct": {"prefix": "", "dir": "struct",
               "schema_fields": ["struct_id", "item_id", "dim", "target", "evidence",
                                 "original", "confidence"],
               "enum_fields": ["dim"]},
    "reg": {"prefix": "REG-", "dir": "reg",
            "schema_fields": ["reg_id", "item_id", "name", "type", "content",
                              "evolution", "target", "original", "confidence"],
            "enum_fields": ["type"]},
    "opn": {"prefix": "OPN-", "dir": "opn",
            "schema_fields": ["opn_id", "item_id", "topic", "stance", "argument",
                              "evidence_refs", "original", "confidence"],
            "enum_fields": ["stance"]},
}
DIM_PREFIX = {"ACT": "ACT-", "FRD": "FRD-", "LGR": "LGR-", "TME": "TME-"}
DIM_TYPE_FIELD = {"ACT": "act_type", "FRD": "frd_type", "LGR": "lgr_type", "TME": "tme_type"}


def load_registry():
    with io.open(REGISTRY_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_enums():
    ns = {}
    with io.open(ENUMS_PATH, encoding="utf-8") as f:
        code = f.read()
    exec(compile(code, ENUMS_PATH, "exec"), ns)
    return ns


def parse_volumes():
    """--volumes 01,03 或 --volumes 03；缺省 None=全部已装填卷。"""
    for arg in sys.argv[1:]:
        if arg.startswith("--volumes"):
            val = arg.split("=", 1)[1] if "=" in arg else sys.argv[sys.argv.index(arg) + 1]
            vols = [v.strip() for v in val.split(",") if v.strip()]
            return vols
    # 缺省：扫描 _src 已装填的实体源文件推导卷号（升序）
    vols = set()
    if os.path.isdir(SRC_DIR):
        for fn in os.listdir(SRC_DIR):
            m = re.match(r"^_ents_ai_(\d+)\.py$", fn)
            if m:
                vols.add(m.group(1))
    return sorted(vols, key=int) if vols else []


def alloc_id(prefix, vol, seq):
    """段位 ID：卷号 × 500 + 卷内序（C2，杜绝跨卷撞号）。"""
    return "%s%04d" % (prefix, int(vol) * 500 + seq)


def find_span(original, text):
    i = original.find(text)
    if i < 0:
        return None
    return {"start": i, "end": i + len(text)}


def load_src(vol, layer):
    """读 _src/_<layer>_ai_<vol>.py 的 RECORDS；缺文件返回 None。"""
    p = os.path.join(SRC_DIR, "_%s_ai_%s.py" % (layer, vol))
    if not os.path.isfile(p):
        return None
    ns = {}
    with io.open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    return ns.get("RECORDS") or []


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with io.open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def read_json(path, default):
    if not os.path.isfile(path):
        return default
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)
