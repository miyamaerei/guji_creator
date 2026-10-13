# -*- coding: utf-8 -*-
"""《福惠全书》打包公共基座：路径推导 / 指纹库 / 枚举 / 段位 ID / 卷参数（8 层：ent/rule/struct/reg/opn/proc/doc/rel）。"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT, "_src")
LAYER_DIR = os.path.join(ROOT, "_layers")
BUILD_DIR = os.path.join(ROOT, "_build")
GLOBAL_DIR = os.path.join(ROOT, "_global")
REGISTRY_PATH = os.path.join(ROOT, "_item_registry.json")
ENUMS_PATH = os.path.join(ROOT, "_kg_enums.py")

for _d in (BUILD_DIR, GLOBAL_DIR):
    os.makedirs(_d, exist_ok=True)

# 契约登记表（C4，与实例 references/schemas.md §2 一致；8 层）
LAYER_SCHEMA = {
    "ent": {"prefix": "ENT-", "dir": "ent", "id_key": "ent_id",
            "schema_fields": ["ent_id", "item_id", "text", "type", "start", "end",
                              "normalized", "confidence", "source", "original"],
            "enum_fields": ["type"]},
    "rule": {"prefix": "RULE-", "dir": "rule", "id_key": "rule_id",
             "schema_fields": ["rule_id", "item_id", "type", "modals", "condition",
                               "subject", "subject_ent_ids", "action", "object",
                               "purpose", "punishment", "original", "confidence"],
             "enum_fields": ["type"]},
    "struct": {"prefix": "STRUCT-", "dir": "struct", "id_key": "struct_id",
               "schema_fields": ["struct_id", "item_id", "dim",
                                 "act_type", "frd_type", "lgr_type", "tme_type",
                                 "target", "target_ent_ids", "content", "original", "confidence"],
               "enum_fields": ["dim", "act_type", "frd_type", "lgr_type", "tme_type"]},
    "reg": {"prefix": "REG-", "dir": "reg", "id_key": "reg_id",
            "schema_fields": ["reg_id", "item_id", "name", "type", "content",
                              "evolution", "target", "original", "confidence"],
            "enum_fields": ["type"]},
    "opn": {"prefix": "OPN-", "dir": "opn", "id_key": "opn_id",
            "schema_fields": ["opn_id", "item_id", "topic", "stance", "argument",
                              "evidence_refs", "original", "confidence"],
            "enum_fields": ["stance"]},
    "proc": {"prefix": "PROC-", "dir": "proc", "id_key": "process_id",
             "schema_fields": ["process_id", "item_id", "name", "steps",
                               "state_machine", "events", "original", "confidence"],
             "enum_fields": []},
    "doc": {"prefix": "DOC-", "dir": "doc", "id_key": "doc_id",
            "schema_fields": ["doc_id", "item_id", "name", "category", "format",
                              "purpose", "flow", "related_item", "original", "confidence"],
            "enum_fields": ["category"]},
    "rel": {"prefix": "REL-", "dir": "rel", "id_key": "rel_id",
            "schema_fields": ["rel_id", "item_id", "person_a", "person_a_ent_ids",
                              "person_b", "person_b_ent_ids", "relation_type",
                              "direction", "evidence", "original", "confidence"],
            "enum_fields": ["relation_type"]},
}
LAYER_ENUM_GROUP = {
    "ent": "ENTITY", "rule": "RULE", "reg": "REG", "opn": "OPN",
    "doc": "DOC", "rel": "REL",
}


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
    """--volumes 01,03 或 --volumes 03；缺省 None=全部已装填卷（扫描 _src 推导）。"""
    for arg in sys.argv[1:]:
        if arg.startswith("--volumes"):
            val = arg.split("=", 1)[1] if "=" in arg else sys.argv[sys.argv.index(arg) + 1]
            vols = [v.strip() for v in val.split(",") if v.strip()]
            return vols
    vols = set()
    if os.path.isdir(SRC_DIR):
        for fn in os.listdir(SRC_DIR):
            m = re.match(r"^_([a-z]+)_ai_(\d+)\.py$", fn)
            if m and m.group(1) == "ents":
                vols.add(m.group(2))
    return sorted(vols, key=int) if vols else []


def alloc_id(prefix, vol, seq):
    """段位 ID：卷号 × 500 + 卷内序（C2，杜绝跨卷撞号）。struct 四维前缀 ACT-/FRD-/LGR-/TME- 由打包器传入。"""
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
