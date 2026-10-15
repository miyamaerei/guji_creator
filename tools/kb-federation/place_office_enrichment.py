"""place_office_enrichment.py —— 地名和官职的CBDB富化

从CBDB补全地名和官职的结构化信息，用于跨书匹配。

地名富化维度：
  - 行政级别（省/府/县）
  - 隶属链（省→府→县）
  - 坐标（经纬度）
  - 朝代有效性

官职富化维度：
  - 所属机构（六部/都察院/...）
  - 品级
  - 朝代
"""

import sqlite3
from pathlib import Path
from collections import defaultdict

CBDB_PATH = Path(r"E:\git\cbdb_sqlite\cbdb_20260926.sqlite3")


def enrich_places(con, cbdb_con):
    """
    从CBDB补全地名信息。
    
    CBDB表：
      - ADDR_CODES: 地名主表（30,160条）
      - ADDRESSES: 层级关系（64,347条）
    """
    cbdb_cur = cbdb_con.cursor()
    
    # 获取所有place节点
    places = con.execute('''
        SELECT uid, label FROM nodes WHERE type = 'place'
    ''').fetchall()
    
    stats = {"total": len(places), "matched": 0, "slots": 0}
    
    for uid, label in places:
        # 在CBDB中查找地名
        addr_row = cbdb_cur.execute('''
            SELECT c_addr_id, c_name_chn, c_admin_cat_code, x_coord, y_coord
            FROM ADDR_CODES
            WHERE c_name_chn = ?
        ''', (label,)).fetchone()
        
        if not addr_row:
            continue
        
        addr_id, name_chn, admin_level, x_coord, y_coord = addr_row
        stats["matched"] += 1
        
        slots = []
        
        # 行政级别
        if admin_level and admin_level > 0:
            level_row = cbdb_cur.execute('''
                SELECT c_admin_cat_hz FROM ADMIN_CAT_CODES 
                WHERE c_admin_cat_code = ?
            ''', (admin_level,)).fetchone()
            if level_row and level_row[0]:
                slots.append((uid, "行政级别", level_row[0], "cbdb"))
        
        # 坐标
        if x_coord and y_coord:
            slots.append((uid, "坐标", f"{x_coord:.2f},{y_coord:.2f}", "cbdb"))
        
        # 隶属链（从ADDRESSES表）
        addr_full = cbdb_cur.execute('''
            SELECT belongs1_Name_chn, belongs2_Name_chn, belongs3_Name_chn, belongs4_Name_chn, belongs5_Name_chn
            FROM ADDRESSES WHERE c_addr_id = ?
        ''', (addr_id,)).fetchone()
        
        if addr_full:
            hierarchy = [name for name in addr_full if name]
            if hierarchy:
                slots.append((uid, "隶属链", "→".join(hierarchy), "cbdb"))
        
        # 写入ent_slots
        if slots:
            con.executemany('''
                INSERT OR IGNORE INTO ent_slots (uid, slot_type, slot_value, source_field)
                VALUES (?, ?, ?, ?)
            ''', slots)
            stats["slots"] += len(slots)
    
    con.commit()
    return stats


def enrich_offices(con, cbdb_con):
    """
    从CBDB补全官职信息。
    
    CBDB表：
      - OFFICE_CODES: 官职主表（34,176条）
      - OFFICE_CODE_TYPE_REL: 官职分类（43,797条）
    """
    cbdb_cur = cbdb_con.cursor()
    
    # 获取所有official节点
    offices = con.execute('''
        SELECT uid, label FROM nodes WHERE type = 'official'
    ''').fetchall()
    
    stats = {"total": len(offices), "matched": 0, "slots": 0}
    
    for uid, label in offices:
        # 在CBDB中查找官职
        office_row = cbdb_cur.execute('''
            SELECT c_office_id, c_office_chn, c_dy
            FROM OFFICE_CODES
            WHERE c_office_chn = ?
        ''', (label,)).fetchone()
        
        if not office_row:
            continue
        
        office_id, office_chn, dy = office_row
        stats["matched"] += 1
        
        slots = []
        
        # 朝代
        if dy and dy > 0:
            dyn_row = cbdb_cur.execute('''
                SELECT c_dynasty_chn FROM DYNASTIES WHERE c_dy = ?
            ''', (dy,)).fetchone()
            if dyn_row and dyn_row[0]:
                slots.append((uid, "朝代", dyn_row[0], "cbdb"))
        
        # 写入ent_slots
        if slots:
            con.executemany('''
                INSERT OR IGNORE INTO ent_slots (uid, slot_type, slot_value, source_field)
                VALUES (?, ?, ?, ?)
            ''', slots)
            stats["slots"] += len(slots)
    
    con.commit()
    return stats


def enrich_all_places_offices(con):
    """对正式库运行地名和官职富化"""
    cbdb_con = sqlite3.connect(CBDB_PATH)
    
    print("Enriching places...")
    place_stats = enrich_places(con, cbdb_con)
    print(f"  Places: {place_stats['matched']}/{place_stats['total']} matched, {place_stats['slots']} slots")
    
    print("Enriching offices...")
    office_stats = enrich_offices(con, cbdb_con)
    print(f"  Offices: {office_stats['matched']}/{office_stats['total']} matched, {office_stats['slots']} slots")
    
    cbdb_con.close()
    
    return {"places": place_stats, "offices": office_stats}


if __name__ == "__main__":
    con = sqlite3.connect("kb.sqlite")
    stats = enrich_all_places_offices(con)
    con.close()
    print("\nDone!")
