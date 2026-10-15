"""place_office_matching.py —— 地名和官职的匹配策略

基于CBDB富化的ent_slots进行跨书匹配。

地名匹配：
  - 名字相同 + 隶属链相同 → 高置信度
  - 名字相同 + 行政级别相同 → 中置信度
  - 名字相同（无其他信息）→ 低置信度

官职匹配：
  - 名字相同 + 朝代相同 → 高置信度
  - 名字相同（无朝代）→ 中置信度
"""

import sqlite3
from collections import defaultdict


def match_places(con):
    """
    地名匹配：基于名字+隶属链+行政级别
    
    返回: list[(uid_a, uid_b, method, confidence)]
    """
    candidates = []
    
    # 获取所有place节点及其ent_slots
    places = {}
    for uid, label in con.execute('''
        SELECT uid, label FROM nodes WHERE type = 'place'
    ''').fetchall():
        slots = con.execute('''
            SELECT slot_type, slot_value FROM ent_slots WHERE uid = ?
        ''', (uid,)).fetchall()
        places[uid] = {
            'label': label,
            'slots': {t: v for t, v in slots}
        }
    
    # 按名字分组
    by_name = defaultdict(list)
    for uid, data in places.items():
        by_name[data['label']].append(uid)
    
    # 对每个同名组，检查隶属链和行政级别
    for name, uids in by_name.items():
        if len(uids) < 2:
            continue
        
        # 两两比较
        for i in range(len(uids)):
            for j in range(i + 1, len(uids)):
                uid_a, uid_b = uids[i], uids[j]
                
                # 同书不匹配
                book_a = uid_a.split(':')[0]
                book_b = uid_b.split(':')[0]
                if book_a == book_b:
                    continue
                
                slots_a = places[uid_a]['slots']
                slots_b = places[uid_b]['slots']
                
                # 检查隶属链
                hierarchy_a = slots_a.get('隶属链')
                hierarchy_b = slots_b.get('隶属链')
                
                # 检查行政级别
                admin_a = slots_a.get('行政级别')
                admin_b = slots_b.get('行政级别')
                
                # 判定
                if hierarchy_a and hierarchy_b and hierarchy_a == hierarchy_b:
                    # 隶属链完全相同 → 高置信度
                    candidates.append((uid_a, uid_b, 'place_hierarchy_match', 0.95))
                elif admin_a and admin_b and admin_a == admin_b:
                    # 行政级别相同 → 中置信度
                    candidates.append((uid_a, uid_b, 'place_admin_match', 0.80))
                else:
                    # 只有名字相同 → 低置信度
                    candidates.append((uid_a, uid_b, 'place_name_match', 0.60))
    
    return candidates


def match_offices(con):
    """
    官职匹配：基于名字+朝代
    
    返回: list[(uid_a, uid_b, method, confidence)]
    """
    candidates = []
    
    # 获取所有official节点及其ent_slots
    offices = {}
    for uid, label in con.execute('''
        SELECT uid, label FROM nodes WHERE type = 'official'
    ''').fetchall():
        slots = con.execute('''
            SELECT slot_type, slot_value FROM ent_slots WHERE uid = ?
        ''', (uid,)).fetchall()
        offices[uid] = {
            'label': label,
            'slots': {t: v for t, v in slots}
        }
    
    # 按名字分组
    by_name = defaultdict(list)
    for uid, data in offices.items():
        by_name[data['label']].append(uid)
    
    # 对每个同名组，检查朝代
    for name, uids in by_name.items():
        if len(uids) < 2:
            continue
        
        # 两两比较
        for i in range(len(uids)):
            for j in range(i + 1, len(uids)):
                uid_a, uid_b = uids[i], uids[j]
                
                # 同书不匹配
                book_a = uid_a.split(':')[0]
                book_b = uid_b.split(':')[0]
                if book_a == book_b:
                    continue
                
                slots_a = offices[uid_a]['slots']
                slots_b = offices[uid_b]['slots']
                
                # 检查朝代
                dynasty_a = slots_a.get('朝代')
                dynasty_b = slots_b.get('朝代')
                
                # 判定
                if dynasty_a and dynasty_b and dynasty_a == dynasty_b:
                    # 朝代相同 → 高置信度
                    candidates.append((uid_a, uid_b, 'office_dynasty_match', 0.90))
                else:
                    # 只有名字相同 → 中置信度
                    candidates.append((uid_a, uid_b, 'office_name_match', 0.70))
    
    return candidates


def match_all_places_offices(con):
    """对所有地名和官职进行匹配"""
    print("Matching places...")
    place_candidates = match_places(con)
    print(f"  Place candidates: {len(place_candidates)}")
    
    print("Matching offices...")
    office_candidates = match_offices(con)
    print(f"  Office candidates: {len(office_candidates)}")
    
    return place_candidates + office_candidates


if __name__ == "__main__":
    con = sqlite3.connect("kb.sqlite")
    candidates = match_all_places_offices(con)
    
    print(f"\nTotal candidates: {len(candidates)}")
    
    # By method
    by_method = defaultdict(int)
    for a, b, method, conf in candidates:
        by_method[method] += 1
    
    print("\nBy method:")
    for method, count in sorted(by_method.items()):
        print(f"  {method}: {count}")
    
    # Sample
    print("\nSample candidates:")
    for a, b, method, conf in candidates[:10]:
        label_a = con.execute('SELECT label FROM nodes WHERE uid=?', (a,)).fetchone()[0]
        label_b = con.execute('SELECT label FROM nodes WHERE uid=?', (b,)).fetchone()[0]
        print(f"  {label_a} <-> {label_b} ({method}, {conf:.2f})")
    
    con.close()
