# -*- coding: utf-8 -*-
"""《宛署杂记》打包公共基座：路径推导 / 指纹库 / 枚举 / 段位 ID / 卷参数（9 层）。"""
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

# 模块加载即预建产物目录（write_json 会自建层目录，但 errors/global 需显式）
for _d in (BUILD_DIR, GLOBAL_DIR):
    os.makedirs(_d, exist_ok=True)

# 契约登记表（C4，与实例 references/schemas.md §2 一致；9 层）
LAYER_SCHEMA = {
    "ent": {"prefix": "ENT-", "dir": "ent", "id_key": "ent_id",
            "schema_fields": ["ent_id", "item_id", "text", "type", "start", "end",
                              "normalized", "confidence", "source", "original"],
            "enum_fields": ["type"]},
    "appt": {"prefix": "APPT-", "dir": "appt", "id_key": "appointment_id",
             "schema_fields": ["appointment_id", "item_id", "person", "person_ent_ids",
                               "office", "official_ent_ids", "institution",
                               "institution_ent_ids", "when", "status", "evidence",
                               "original", "confidence"],
             "enum_fields": ["status"]},
    "evt": {"prefix": "EVT-", "dir": "evt", "id_key": "event_id",
            "schema_fields": ["event_id", "item_id", "type", "who", "who_ent_ids",
                              "action", "what", "when", "where", "original", "confidence"],
            "enum_fields": ["type"]},
    "lit": {"prefix": "LIT-", "dir": "lit", "id_key": "lit_id",
            "schema_fields": ["lit_id", "item_id", "title", "author", "author_ent_ids",
                              "type", "content_location", "original", "confidence"],
            "enum_fields": ["type"]},
    "reg": {"prefix": "REG-", "dir": "reg", "id_key": "reg_id",
            "schema_fields": ["reg_id", "item_id", "name", "type", "content",
                              "evolution", "target", "original", "confidence"],
            "enum_fields": ["type"]},
    "nam": {"prefix": "NAM-", "dir": "nam", "id_key": "nam_id",
            "schema_fields": ["nam_id", "item_id", "name", "category", "scope",
                              "entries", "ent_ids", "original", "confidence"],
            "enum_fields": ["category"]},
    "opn": {"prefix": "OPN-", "dir": "opn", "id_key": "opn_id",
            "schema_fields": ["opn_id", "item_id", "topic", "stance", "argument",
                              "evidence_refs", "original", "confidence"],
            "enum_fields": ["stance"]},
    "cus": {"prefix": "CUS-", "dir": "cus", "id_key": "cus_id",
            "schema_fields": ["cus_id", "item_id", "type", "region", "term",
                              "description", "original", "confidence"],
            "enum_fields": ["type"]},
    "geo": {"prefix": "GEO-", "dir": "geo", "id_key": "geo_id",
            "schema_fields": ["geo_id", "item_id", "name", "category", "attributes",
                              "lore", "ent_ids", "original", "confidence"],
            "enum_fields": ["category"]},
}
# 各层枚举字段 → 枚举组名（_kg_enums.py）
LAYER_ENUM_GROUP = {
    "ent": "ENTITY", "appt": "APPT", "evt": "EVENT", "lit": "LIT",
    "reg": "REG", "nam": "NAM", "opn": "OPN", "cus": "CUS", "geo": "GEO",
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
    """--volumes 01,03 或 --volumes 03；缺省 None=全部已装填卷。"""
    for arg in sys.argv[1:]:
        if arg.startswith("--volumes"):
            val = arg.split("=", 1)[1] if "=" in arg else sys.argv[sys.argv.index(arg) + 1]
            vols = [v.strip() for v in val.split(",") if v.strip()]
            return vols
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
