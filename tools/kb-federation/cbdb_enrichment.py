#!/usr/bin/env python3
"""
CBDB Enrichment Script

从CBDB（中国历代人物传记数据库）补全人物ent_slots。

输入：kb_test.sqlite中的person节点
输出：ent_slots表（称谓/生卒/籍贯/职官/亲属等）

用法：
    python cbdb_enrichment.py [--limit N] [--book BOOK_ID] [--dry-run]
    python cbdb_enrichment.py --query "叶向高之妻"  # 关系查询
"""

import sqlite3
import json
import argparse
from pathlib import Path
from typing import Optional, Tuple

# CBDB路径
CBDB_PATH = Path(r"E:\git\cbdb_sqlite\cbdb_20260926.sqlite3")

# CBDB ALTNAME_CODES映射到我们的slot_type
ALTNAME_TYPE_MAP = {
    3: "曾用名",
    4: "字",
    5: "号",
    6: "谥号",
    7: "行第",
    8: "封爵",
    9: "小名",
    11: "赐名",
    14: "庙号",
    15: "尊号",
    19: "法号",
    20: "道号",
}

# CBDB BIOG_ADDR_CODES映射（籍贯相关）
ADDR_TYPE_MAP = {
    1: "籍贯",
    2: "迁住地",
    5: "祖籍",
    6: "落籍",
    7: "本贯",
    8: "出生地",
}


def setup_connection(kb_path: str = "kb_test.sqlite"):
    """建立数据库连接"""
    kb_con = sqlite3.connect(kb_path)
    cbdb_con = sqlite3.connect(CBDB_PATH)
    return kb_con, cbdb_con


def match_person_by_name(cbdb_con, name: str) -> Optional[int]:
    """
    通过中文名匹配CBDB人物。
    
    返回c_personid，如果找不到返回None。
    如果有多个匹配，返回第一个（可能需要人工确认）。
    """
    cur = cbdb_con.cursor()
    
    # 精确匹配
    rows = cur.execute("""
        SELECT c_personid, c_name_chn, c_birthyear, c_deathyear
        FROM BIOG_MAIN
        WHERE c_name_chn = ?
    """, (name,)).fetchall()
    
    if len(rows) == 1:
        return rows[0][0]
    elif len(rows) > 1:
        # 多个匹配，返回第一个（可能需要消歧）
        print(f"  Warning: {len(rows)} matches for '{name}', using first")
        return rows[0][0]
    
    return None


def extract_aliases(cbdb_con, personid: int) -> list[tuple[str, str]]:
    """
    提取人物的所有别名（字/号/谥号等）。
    
    返回 [(slot_type, slot_value), ...]
    """
    cur = cbdb_con.cursor()
    aliases = []
    
    rows = cur.execute("""
        SELECT c_alt_name_chn, c_alt_name_type_code
        FROM ALTNAME_DATA
        WHERE c_personid = ?
    """, (personid,)).fetchall()
    
    for name_chn, type_code in rows:
        if type_code in ALTNAME_TYPE_MAP and name_chn:
            slot_type = ALTNAME_TYPE_MAP[type_code]
            aliases.append((slot_type, name_chn))
    
    return aliases


def extract_birth_death(cbdb_con, personid: int) -> dict:
    """
    提取人物的生卒年。
    
    返回 {birth_year, death_year, birth_era, death_era}
    """
    cur = cbdb_con.cursor()
    row = cur.execute("""
        SELECT c_birthyear, c_deathyear, c_by_nh_code, c_dy_nh_code
        FROM BIOG_MAIN
        WHERE c_personid = ?
    """, (personid,)).fetchone()
    
    if not row:
        return {}
    
    birth_year, death_year, by_nh, dy_nh = row
    
    result = {}
    if birth_year and birth_year > 0:
        result["birth_year"] = birth_year
    if death_year and death_year > 0:
        result["death_year"] = death_year
    
    # 提取年号（需要查NIAN_HAO表）
    if by_nh and by_nh > 0:
        era_row = cur.execute("""
            SELECT c_nianhao_chn FROM NIAN_HAO WHERE c_nianhao_id = ?
        """, (by_nh,)).fetchone()
        if era_row and era_row[0]:
            result["birth_era"] = era_row[0]
    
    if dy_nh and dy_nh > 0:
        era_row = cur.execute("""
            SELECT c_nianhao_chn FROM NIAN_HAO WHERE c_nianhao_id = ?
        """, (dy_nh,)).fetchone()
        if era_row and era_row[0]:
            result["death_era"] = era_row[0]
    
    return result


def extract_native_place(cbdb_con, personid: int) -> list[tuple[str, str]]:
    """
    提取人物的籍贯/出生地。
    
    返回 [(slot_type, slot_value), ...]
    """
    cur = cbdb_con.cursor()
    places = []
    
    # 从BIOG_ADDR_DATA提取籍贯相关地址
    rows = cur.execute("""
        SELECT c_addr_id, c_addr_type
        FROM BIOG_ADDR_DATA
        WHERE c_personid = ? AND c_addr_type IN (1, 5, 6, 7, 8)
    """, (personid,)).fetchall()
    
    seen = set()
    for addr_id, addr_type in rows:
        if addr_id in seen:
            continue
        seen.add(addr_id)
        
        # 查地址名称
        addr_row = cur.execute("""
            SELECT c_name_chn FROM ADDR_CODES WHERE c_addr_id = ?
        """, (addr_id,)).fetchone()
        
        if addr_row and addr_row[0]:
            slot_type = ADDR_TYPE_MAP.get(addr_type, "籍贯")
            places.append((slot_type, addr_row[0]))
    
    return places


def extract_offices(cbdb_con, personid: int) -> list[tuple[str, str]]:
    """
    提取人物担任的职官。
    
    返回 [(slot_type, slot_value), ...]
    """
    cur = cbdb_con.cursor()
    offices = []
    
    rows = cur.execute("""
        SELECT o.c_office_chn, p.c_firstyear, p.c_lastyear
        FROM POSTED_TO_OFFICE_DATA p
        JOIN OFFICE_CODES o ON p.c_office_id = o.c_office_id
        WHERE p.c_personid = ?
        ORDER BY p.c_firstyear
    """, (personid,)).fetchall()
    
    for office_name, first_year, last_year in rows:
        if office_name:
            # 如果有年份，加入年份信息
            if first_year and first_year > 0:
                if last_year and last_year > 0:
                    value = f"{office_name}({first_year}-{last_year})"
                else:
                    value = f"{office_name}({first_year}-)"
            else:
                value = office_name
            offices.append(("主职", value))
    
    return offices


def extract_dynasty(cbdb_con, personid: int) -> Optional[str]:
    """提取人物所属朝代"""
    cur = cbdb_con.cursor()
    row = cur.execute("""
        SELECT d.c_dynasty_chn
        FROM BIOG_MAIN b
        JOIN DYNASTIES d ON b.c_dy = d.c_dy
        WHERE b.c_personid = ?
    """, (personid,)).fetchone()
    
    if row and row[0]:
        return row[0]
    return None


def extract_kinship(cbdb_con, personid: int) -> list[tuple[str, str]]:
    """
    提取人物的亲属关系。
    
    返回 [(slot_type, slot_value), ...]
    例如: [("亲属:父", "叶朝荣"), ("亲属:妻", "陈氏")]
    """
    cur = cbdb_con.cursor()
    relations = []
    
    rows = cur.execute("""
        SELECT k.c_kin_id, kc.c_kinrel_chn
        FROM KIN_DATA k
        JOIN KINSHIP_CODES kc ON k.c_kin_code = kc.c_kincode
        WHERE k.c_personid = ?
    """, (personid,)).fetchall()
    
    seen = set()
    for kin_id, kinship in rows:
        if kin_id in seen:
            continue
        seen.add(kin_id)
        
        # 查亲属名字
        name_row = cur.execute("""
            SELECT c_name_chn FROM BIOG_MAIN WHERE c_personid = ?
        """, (kin_id,)).fetchone()
        
        if name_row and name_row[0]:
            relations.append((f"亲属:{kinship}", name_row[0]))
    
    return relations


def extract_era_range(cbdb_con, personid: int) -> list[tuple[str, str]]:
    """
    提取人物的活动年号区间（从ENTRY_DATA等表的活动年份映射）。
    
    返回 [(slot_type, slot_value), ...]
    例如: [("活动年号", "正统-成化"), ("活动起始", "1436"), ("活动终止", "1487")]
    """
    cur = cbdb_con.cursor()
    slots = []
    
    # 从多个表收集活动年份
    years = []
    
    # 1. ENTRY_DATA（科举/入仕年份）
    for row in cur.execute("""
        SELECT c_year FROM ENTRY_DATA 
        WHERE c_personid = ? AND c_year > 0
    """, (personid,)).fetchall():
        years.append(row[0])
    
    # 2. POSTED_TO_OFFICE_DATA（任职年份）
    for row in cur.execute("""
        SELECT c_firstyear, c_lastyear FROM POSTED_TO_OFFICE_DATA 
        WHERE c_personid = ? AND (c_firstyear > 0 OR c_lastyear > 0)
    """, (personid,)).fetchall():
        if row[0] and row[0] > 0:
            years.append(row[0])
        if row[1] and row[1] > 0:
            years.append(row[1])
    
    # 3. STATUS_DATA（事迹年份）
    for row in cur.execute("""
        SELECT c_firstyear, c_lastyear FROM STATUS_DATA 
        WHERE c_personid = ? AND (c_firstyear > 0 OR c_lastyear > 0)
    """, (personid,)).fetchall():
        if row[0] and row[0] > 0:
            years.append(row[0])
        if row[1] and row[1] > 0:
            years.append(row[1])
    
    if not years:
        return slots
    
    min_year = min(years)
    max_year = max(years)
    
    # 添加活动年份
    slots.append(("活动起始", str(min_year)))
    slots.append(("活动终止", str(max_year)))
    
    # 映射到年号
    era_names = []
    for year in [min_year, max_year]:
        era_row = cur.execute("""
            SELECT c_nianhao_chn FROM NIAN_HAO 
            WHERE c_firstyear <= ? AND c_lastyear >= ?
            LIMIT 1
        """, (year, year)).fetchone()
        if era_row and era_row[0]:
            era_names.append(era_row[0])
    
    if era_names:
        if len(era_names) == 1:
            slots.append(("活动年号", era_names[0]))
        elif era_names[0] != era_names[1]:
            slots.append(("活动年号", f"{era_names[0]}-{era_names[1]}"))
        else:
            slots.append(("活动年号", era_names[0]))
    
    return slots


def extract_exam_entry(cbdb_con, personid: int) -> list[tuple[str, str]]:
    """
    提取人物的科举/入仕数据。
    
    返回 [(slot_type, slot_value), ...]
    例如: [("科举", "进士(正统十年)"), ("科举", "举人(正统七年)")]
    """
    cur = cbdb_con.cursor()
    slots = []
    
    # 查询ENTRY_DATA，关联ENTRY_CODES和NIAN_HAO
    rows = cur.execute("""
        SELECT e.c_entry_code, ec.c_entry_desc_chn, e.c_year, 
               e.c_entry_nh_id, e.c_entry_nh_year, nh.c_nianhao_chn
        FROM ENTRY_DATA e
        LEFT JOIN ENTRY_CODES ec ON e.c_entry_code = ec.c_entry_code
        LEFT JOIN NIAN_HAO nh ON e.c_entry_nh_id = nh.c_nianhao_id
        WHERE e.c_personid = ? AND e.c_entry_code > 0
        ORDER BY e.c_year
    """, (personid,)).fetchall()
    
    seen = set()
    for entry_code, desc_chn, year, nh_id, nh_year, nianhao in rows:
        # 构建描述
        parts = []
        
        # 入仕方式（简化描述）
        if desc_chn and desc_chn not in seen:
            # 提取关键信息（去掉括号内的英文）
            desc_short = desc_chn.split("(")[0].split("（")[0].strip()
            if len(desc_short) > 10:
                desc_short = desc_short[:10] + "..."
            parts.append(desc_short)
        
        # 年份
        if year and year > 0:
            if nianhao and nh_year and nh_year > 0:
                parts.append(f"{nianhao}{nh_year}年({year})")
            else:
                parts.append(f"{year}年")
        
        if parts:
            value = " ".join(parts)
            if value not in seen:
                seen.add(value)
                slots.append(("科举", value))
    
    return slots


def classify_entity_confidence(slots: list[tuple]) -> str:
    """
    根据ent_slots判断人物类型和置信度。
    
    返回: "famous_person" | "documented_person" | "relation_defined" | "generic_reference"
    """
    if not slots:
        return "generic_reference"
    
    slot_types = [s[1] for s in slots]  # slot_type is at index 1
    
    has_offices = "主职" in slot_types
    has_aliases = any(t in slot_types for t in ["字", "号", "谥号"])
    has_birth_death = "生年" in slot_types or "卒年" in slot_types
    has_native_place = "籍贯" in slot_types
    
    office_count = slot_types.count("主职")
    alias_count = sum(1 for t in slot_types if t in ["字", "号", "谥号", "封爵"])
    
    # 名人：多官职 + 多别名 + 生卒年
    if office_count >= 3 and alias_count >= 2 and has_birth_death:
        return "famous_person"
    
    # 有记录的人物：有生卒年或籍贯
    elif has_birth_death or has_native_place:
        return "documented_person"
    
    # 关系定义的人物：有亲属关系
    elif any(t.startswith("亲属:") for t in slot_types):
        return "relation_defined"
    
    # 其他：信息不足
    else:
        return "generic_reference"


def compute_entity_identity(name: str, slots: list[tuple], confidence: str) -> str:
    """
    计算实体的身份标识（用于消歧）。
    
    返回: identity string
    """
    slot_dict = {}
    for _, slot_type, slot_value, _ in slots:
        if slot_type not in slot_dict:
            slot_dict[slot_type] = []
        slot_dict[slot_type].append(slot_value)
    
    dynasty = slot_dict.get("朝代", [""])[0]
    
    if confidence == "famous_person":
        # 名人：名字@朝代
        return f"{name}@{dynasty}"
    
    elif confidence == "relation_defined":
        # 亲属：找锚点人物
        relations = slot_dict.get("亲属:父", []) + slot_dict.get("亲属:夫", [])
        if relations:
            anchor = relations[0]
            return f"{anchor}之亲属@{dynasty}"
        return f"{name}@{dynasty}"
    
    elif confidence == "generic_reference":
        # 泛称：名字@朝代@籍贯
        place = slot_dict.get("籍贯", [""])[0]
        return f"{name}@{dynasty}@{place}"
    
    else:
        return f"{name}@{dynasty}"


def enrich_person(kb_con, cbdb_con, uid: str, dry_run: bool = False) -> dict:
    """
    补全单个人物节点。
    
    返回补全的slots统计。
    """
    # 获取人物信息
    cur = kb_con.cursor()
    row = cur.execute("""
        SELECT label, payload FROM nodes WHERE uid = ?
    """, (uid,)).fetchone()
    
    if not row:
        return {"error": f"Node {uid} not found"}
    
    label, payload_str = row
    payload = json.loads(payload_str) if payload_str else {}
    name = payload.get("normalized", label)
    
    print(f"Processing: {uid} ({name})")
    
    # 匹配CBDB
    personid = match_person_by_name(cbdb_con, name)
    if not personid:
        print(f"  Not found in CBDB")
        return {"matched": False}
    
    print(f"  Matched CBDB personid: {personid}")
    
    # 提取各维度数据
    slots = []
    
    # 1. 别名（字/号/谥号等）
    aliases = extract_aliases(cbdb_con, personid)
    for slot_type, slot_value in aliases:
        slots.append((uid, slot_type, slot_value, "cbdb"))
    print(f"  Aliases: {len(aliases)}")
    
    # 2. 生卒年
    birth_death = extract_birth_death(cbdb_con, personid)
    if "birth_year" in birth_death:
        slots.append((uid, "生年", str(birth_death["birth_year"]), "cbdb"))
    if "death_year" in birth_death:
        slots.append((uid, "卒年", str(birth_death["death_year"]), "cbdb"))
    if "birth_era" in birth_death:
        slots.append((uid, "生年号", birth_death["birth_era"], "cbdb"))
    if "death_era" in birth_death:
        slots.append((uid, "卒年号", birth_death["death_era"], "cbdb"))
    print(f"  Birth/Death: {birth_death}")
    
    # 3. 籍贯
    places = extract_native_place(cbdb_con, personid)
    for slot_type, slot_value in places:
        slots.append((uid, slot_type, slot_value, "cbdb"))
    print(f"  Native places: {len(places)}")
    
    # 4. 职官
    offices = extract_offices(cbdb_con, personid)
    for slot_type, slot_value in offices:
        slots.append((uid, slot_type, slot_value, "cbdb"))
    print(f"  Offices: {len(offices)}")
    
    # 5. 朝代
    dynasty = extract_dynasty(cbdb_con, personid)
    if dynasty:
        slots.append((uid, "朝代", dynasty, "cbdb"))
    print(f"  Dynasty: {dynasty}")
    
    # 6. 亲属关系
    kinship = extract_kinship(cbdb_con, personid)
    for slot_type, slot_value in kinship:
        slots.append((uid, slot_type, slot_value, "cbdb"))
    print(f"  Kinship: {len(kinship)}")
    
    # 7. 活动年号区间
    era_range = extract_era_range(cbdb_con, personid)
    for slot_type, slot_value in era_range:
        slots.append((uid, slot_type, slot_value, "cbdb"))
    print(f"  Era range: {len(era_range)}")
    
    # 8. 科举/入仕
    exam_entry = extract_exam_entry(cbdb_con, personid)
    for slot_type, slot_value in exam_entry:
        slots.append((uid, slot_type, slot_value, "cbdb"))
    print(f"  Exam entry: {len(exam_entry)}")
    
    # 分类和身份标识
    confidence = classify_entity_confidence(slots)
    identity = compute_entity_identity(name, slots, confidence)
    print(f"  Confidence: {confidence}")
    print(f"  Identity: {identity}")
    
    # 写入ent_slots
    if not dry_run and slots:
        cur.executemany("""
            INSERT OR IGNORE INTO ent_slots (uid, slot_type, slot_value, source_field)
            VALUES (?, ?, ?, ?)
        """, slots)
        kb_con.commit()
        print(f"  Written {len(slots)} slots to ent_slots")
    
    return {
        "matched": True,
        "personid": personid,
        "slots_count": len(slots),
        "aliases": len(aliases),
        "birth_death": len(birth_death),
        "places": len(places),
        "offices": len(offices),
        "kinship": len(kinship),
        "era_range": len(era_range),
        "exam_entry": len(exam_entry),
    }


def main():
    parser = argparse.ArgumentParser(description="CBDB Enrichment Script")
    parser.add_argument("--limit", type=int, help="限制处理人数")
    parser.add_argument("--book", type=str, help="只处理指定book_id")
    parser.add_argument("--dry-run", action="store_true", help="只查询不写入")
    parser.add_argument("--kb", type=str, default="kb_test.sqlite", help="知识库路径")
    parser.add_argument("--query", type=str, help="关系查询（如：叶向高之妻）")
    args = parser.parse_args()
    
    # 关系查询模式
    if args.query:
        query_person_by_relation(args.query)
        return
    
    kb_con, cbdb_con = setup_connection(args.kb)
    
    # 获取person节点列表
    query = "SELECT uid FROM nodes WHERE type = 'person'"
    params = []
    
    if args.book:
        query += " AND book_id = ?"
        params.append(args.book)
    
    if args.limit:
        query += " LIMIT ?"
        params.append(args.limit)
    
    cur = kb_con.cursor()
    uids = [row[0] for row in cur.execute(query, params).fetchall()]
    
    print(f"Found {len(uids)} person nodes to enrich")
    print(f"Dry run: {args.dry_run}")
    print()
    
    # 逐个处理
    stats = {
        "total": len(uids),
        "matched": 0,
        "not_matched": 0,
        "total_slots": 0,
    }
    
    for uid in uids:
        result = enrich_person(kb_con, cbdb_con, uid, dry_run=args.dry_run)
        
        if result.get("matched"):
            stats["matched"] += 1
            stats["total_slots"] += result.get("slots_count", 0)
        else:
            stats["not_matched"] += 1
        
        print()
    
    # 输出统计
    print("=" * 60)
    print("Enrichment Summary:")
    print(f"  Total persons: {stats['total']}")
    print(f"  Matched: {stats['matched']}")
    print(f"  Not matched: {stats['not_matched']}")
    print(f"  Match rate: {stats['matched']/stats['total']*100:.1f}%")
    print(f"  Total slots added: {stats['total_slots']}")
    
    kb_con.close()
    cbdb_con.close()


def enrich_all_persons(con):
    """
    对所有person节点运行CBDB富化（供transform pipeline调用）。
    
    返回: dict with enrichment stats
    """
    cbdb_con = sqlite3.connect(CBDB_PATH)
    
    # 确保ent_slots表存在
    con.execute('''
        CREATE TABLE IF NOT EXISTS ent_slots (
            uid TEXT,
            slot_type TEXT,
            slot_value TEXT,
            source_field TEXT
        )
    ''')
    con.execute('CREATE INDEX IF NOT EXISTS idx_ent_slots_uid ON ent_slots(uid)')
    con.execute('CREATE INDEX IF NOT EXISTS idx_ent_slots_type ON ent_slots(slot_type)')
    con.commit()
    
    # 获取所有person节点
    uids = [row[0] for row in con.execute("SELECT uid FROM nodes WHERE type = 'person'").fetchall()]
    
    stats = {
        "total": len(uids),
        "matched": 0,
        "not_matched": 0,
        "total_slots": 0,
    }
    
    for uid in uids:
        result = enrich_person(con, cbdb_con, uid, dry_run=False)
        
        if result.get("matched"):
            stats["matched"] += 1
            stats["total_slots"] += result.get("slots_count", 0)
        else:
            stats["not_matched"] += 1
    
    cbdb_con.close()
    
    return stats


def query_person_by_relation(query: str):
    """
    通过关系查询人物。
    
    支持格式：
    - "叶向高之妻"
    - "叶向高之父"
    - "童氏（xx之妻）"
    - "张居正之子"
    """
    cbdb_con = sqlite3.connect(CBDB_PATH)
    cur = cbdb_con.cursor()
    
    # 解析查询
    # 格式1: "X之Y" (X是锚点人物，Y是关系)
    if "之" in query:
        parts = query.split("之")
        if len(parts) == 2:
            anchor_name = parts[0].strip()
            relation = parts[1].strip()
            
            print(f"Query: {anchor_name} 的 {relation}")
            
            # 1. 找锚点人物
            anchor_row = cur.execute("""
                SELECT c_personid, c_name_chn FROM BIOG_MAIN 
                WHERE c_name_chn = ?
            """, (anchor_name,)).fetchone()
            
            if not anchor_row:
                print(f"Anchor person '{anchor_name}' not found in CBDB")
                cbdb_con.close()
                return
            
            anchor_id, anchor_name_chn = anchor_row
            print(f"Found anchor: {anchor_name_chn} (personid={anchor_id})")
            
            # 2. 映射关系到CBDB的kinship code
            relation_map = {
                "父": 1, "母": 2, "妻": 3, "夫": 3,
                "子": 4, "女": 5, "兄": 6, "弟": 7,
                "姊": 8, "妹": 9
            }
            
            kin_code = relation_map.get(relation)
            if not kin_code:
                print(f"Unknown relation: {relation}")
                print(f"Supported: {list(relation_map.keys())}")
                cbdb_con.close()
                return
            
            # 3. 查KIN_DATA找亲属
            results = cur.execute("""
                SELECT k.c_kin_id, b.c_name_chn, b.c_birthyear, b.c_deathyear
                FROM KIN_DATA k
                JOIN BIOG_MAIN b ON k.c_kin_id = b.c_personid
                WHERE k.c_personid = ? AND k.c_kin_code = ?
            """, (anchor_id, kin_code)).fetchall()
            
            if not results:
                print(f"No {relation} found for {anchor_name}")
                cbdb_con.close()
                return
            
            print(f"\nFound {len(results)} {relation}(s):")
            for kin_id, name, birth, death in results:
                print(f"  - {name} (personid={kin_id}, {birth}-{death})")
                
                # 获取更多信息
                aliases = extract_aliases(cbdb_con, kin_id)
                if aliases:
                    print(f"    Aliases: {', '.join([v for _, v in aliases[:5]])}")
                
                offices = extract_offices(cbdb_con, kin_id)
                if offices:
                    print(f"    Offices: {len(offices)} positions")
    
    # 格式2: "X氏" (姓氏查询)
    elif "氏" in query:
        surname = query.replace("氏", "").strip()
        print(f"Query: {surname}氏 (surname search)")
        
        results = cur.execute("""
            SELECT c_personid, c_name_chn, c_birthyear, c_deathyear
            FROM BIOG_MAIN
            WHERE c_surname_chn = ?
            LIMIT 10
        """, (surname,)).fetchall()
        
        print(f"\nFound {len(results)} persons with surname {surname}:")
        for pid, name, birth, death in results:
            print(f"  - {name} (personid={pid}, {birth}-{death})")
    
    cbdb_con.close()


if __name__ == "__main__":
    main()
