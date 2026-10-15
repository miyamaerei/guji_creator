"""harvest.py —— 从现有数据收割 ent_slots（称谓槽）

对应《跨书身份判定方法论》§3.2：
  每个实体记录 → 一组 (slot_type, slot_value) 对，用于 slot-ladder 身份判定。

槽位类型（按方法论 §3.2 的 slot-ladder）：
  - person:   era, reign, place, role, relation (与其他人的关系)
  - official: dynasty, ministry, rank, function
  - place:    era, admin_level, parent_place
  - event:    year, place, participants, outcome
  - anecdote: source, participants, theme
  - work:     author, era, genre
  - era:      start_year, end_year, founder
  - system:   dynasty, domain (如科举、军事)

收割逻辑：
  1. 从 ent 记录的 payload 提取直接字段（如 person.era, official.dynasty）
  2. 从 edges 提取关系字段（如 person 的 relation edges → relation slot）
  3. 从 refs 提取引用字段（如 event 引用的 place → place slot）

输出：
  ent_slots 表：(uid, slot_type, slot_value, source_field)
  - uid: 实体 uid（如 kzz:01:ENT-0465）
  - slot_type: 槽位类型（如 era, reign, place）
  - slot_value: 槽位值（如 "洪武", "应天"）
  - source_field: 来源字段（如 "payload.era", "edge.relation"）
"""

import json
from collections import defaultdict


# 每类实体的槽位提取规则（配置驱动，可扩展）
SLOT_RULES = {
    "person": {
        "direct": [
            ("era", "era"),
            ("reign", "reign"),
            ("place", "birth_place"),
            ("place", "death_place"),
            ("role", "role"),
        ],
        "relation": [
            ("relation", "relation_type", "person_b"),  # edge: person_a --[relation_type]--> person_b
        ],
    },
    "official": {
        "direct": [
            ("dynasty", "dynasty"),
            ("ministry", "ministry"),
            ("rank", "rank"),
            ("function", "function"),
        ],
    },
    "place": {
        "direct": [
            ("era", "era"),
            ("admin_level", "admin_level"),
            ("parent_place", "parent_place"),
        ],
    },
    "event": {
        "direct": [
            ("year", "year"),
            ("place", "place"),
            ("outcome", "outcome"),
        ],
        "ref": [
            ("participant", "participants"),  # payload.participants 数组
        ],
    },
    "anecdote": {
        "direct": [
            ("source", "source"),
            ("theme", "theme"),
        ],
        "ref": [
            ("participant", "participants"),
        ],
    },
    "work": {
        "direct": [
            ("author", "author"),
            ("era", "era"),
            ("genre", "genre"),
        ],
    },
    "era": {
        "direct": [
            ("start_year", "start_year"),
            ("end_year", "end_year"),
            ("founder", "founder"),
        ],
    },
    "system": {
        "direct": [
            ("dynasty", "dynasty"),
            ("domain", "domain"),
        ],
    },
}


def _extract_direct_slots(payload, rules):
    """从 payload 直接字段提取槽位。"""
    slots = []
    for slot_type, field in rules:
        val = payload.get(field)
        if val is None:
            continue
        if isinstance(val, (str, int, float)):
            slots.append((slot_type, str(val), f"payload.{field}"))
        elif isinstance(val, dict):
            text = val.get("text")
            if text:
                slots.append((slot_type, text, f"payload.{field}.text"))
    return slots


def _extract_ref_slots(payload, rules):
    """从 payload 的引用字段提取槽位（如 participants 数组）。"""
    slots = []
    for slot_type, field in rules:
        val = payload.get(field)
        if val is None:
            continue
        if isinstance(val, list):
            for item in val[:10]:  # 限制数量，避免爆炸
                if isinstance(item, str):
                    slots.append((slot_type, item, f"payload.{field}[]"))
                elif isinstance(item, dict):
                    text = item.get("text")
                    if text:
                        slots.append((slot_type, text, f"payload.{field}[].text"))
        elif isinstance(val, str):
            slots.append((slot_type, val, f"payload.{field}"))
    return slots


def harvest_ent_slots(con, commit=True):
    """从 ent 记录收割 ent_slots。返回 (slot_count, entity_count)。"""
    cur = con.cursor()
    cur.execute("DELETE FROM ent_slots")

    rows = []
    entity_count = 0

    # 从 records 表读取原始 ent 数据（不是 nodes 表）
    for uid, typ, pl in cur.execute(
        "SELECT n.uid, n.type, r.payload FROM nodes n"
        " JOIN records r ON n.book_id=r.book_id AND n.layer_key=r.layer_key AND n.local_id=r.local_id"
        " WHERE n.layer_key='ent'"
    ):
        if not pl:
            continue
        try:
            payload = json.loads(pl)
        except (ValueError, TypeError):
            continue

        rules = SLOT_RULES.get(typ, {})
        slots = []

        # 直接字段
        if "direct" in rules:
            slots.extend(_extract_direct_slots(payload, rules["direct"]))

        # 引用字段（如 participants）
        if "ref" in rules:
            slots.extend(_extract_ref_slots(payload, rules["ref"]))

        if slots:
            entity_count += 1
            for slot_type, slot_value, source_field in slots:
                rows.append((uid, slot_type, slot_value, source_field))

    cur.executemany(
        "INSERT OR IGNORE INTO ent_slots(uid, slot_type, slot_value, source_field)"
        " VALUES (?,?,?,?)",
        rows,
    )

    if commit:
        con.commit()

    return len(rows), entity_count


def harvest_relation_slots(con, commit=True):
    """从 edges 收割关系槽位（person 的 relation edges）。"""
    cur = con.cursor()

    rows = []
    seen = set()
    for subj_uid, obj_uid, pred in cur.execute(
        "SELECT subject_uid, object_uid, predicate FROM edges"
        " WHERE subject_uid IS NOT NULL AND object_uid IS NOT NULL"
        " AND layer_key='rel'"
    ):
        # person_a --[relation_type]--> person_b
        key = (subj_uid, "relation", f"{pred}:{obj_uid}")
        if key not in seen:
            seen.add(key)
            rows.append((subj_uid, "relation", f"{pred}:{obj_uid}", "edge.rel"))

    cur.executemany(
        "INSERT OR IGNORE INTO ent_slots(uid, slot_type, slot_value, source_field)"
        " VALUES (?,?,?,?)",
        rows,
    )

    if commit:
        con.commit()

    return len(rows)


def harvest_all(con, commit=True):
    """收割所有 ent_slots。返回统计 dict。"""
    ent_slots, ent_count = harvest_ent_slots(con, commit=False)
    rel_slots = harvest_relation_slots(con, commit=commit)
    return {
        "ent_slots": ent_slots,
        "rel_slots": rel_slots,
        "total_slots": ent_slots + rel_slots,
        "entities_with_slots": ent_count,
    }
