"""layered_matching.py —— 分层匹配策略

在four_step_matching基础上，集成CBDB富化数据：
  - 人物分层识别（famous/documented/relation/generic）
  - 身份标识计算（用于消歧）
  - 关系匹配（亲属关系作为身份的一部分）
  - 泛称保护（generic_reference永不合并）
"""

import json
import sqlite3
from collections import defaultdict
from four_step_matching import (
    build_alias_index, build_relation_graph, build_context_index,
    jaccard
)


# ---------------------------------------------------------------------------
# 人物分层识别
# ---------------------------------------------------------------------------
def classify_entity(con, uid):
    """
    根据ent_slots判断人物类型。
    
    返回: "famous_person" | "documented_person" | "relation_defined" | "generic_reference"
    """
    slots = con.execute('''
        SELECT slot_type, slot_value FROM ent_slots WHERE uid = ?
    ''', (uid,)).fetchall()
    
    if not slots:
        return "generic_reference"
    
    slot_types = [s[0] for s in slots]
    
    has_offices = "主职" in slot_types
    has_aliases = any(t in slot_types for t in ["字", "号", "谥号"])
    has_birth_death = "生年" in slot_types or "卒年" in slot_types
    has_native_place = "籍贯" in slot_types
    has_kinship = any(t.startswith("亲属:") for t in slot_types)
    
    office_count = slot_types.count("主职")
    alias_count = sum(1 for t in slot_types if t in ["字", "号", "谥号", "封爵"])
    
    # 名人：多官职 + 多别名 + 生卒年
    if office_count >= 3 and alias_count >= 2 and has_birth_death:
        return "famous_person"
    
    # 有记录的人物：有生卒年或籍贯
    elif has_birth_death or has_native_place:
        return "documented_person"
    
    # 关系定义的人物：有亲属关系
    elif has_kinship:
        return "relation_defined"
    
    # 其他：信息不足
    else:
        return "generic_reference"


def get_entity_identity(con, uid):
    """
    计算实体的身份标识（用于消歧）。
    
    返回: identity string
    """
    slots = con.execute('''
        SELECT slot_type, slot_value FROM ent_slots WHERE uid = ?
    ''', (uid,)).fetchall()
    
    if not slots:
        label = con.execute('SELECT label FROM nodes WHERE uid = ?', (uid,)).fetchone()
        return label[0] if label else uid
    
    slot_dict = defaultdict(list)
    for slot_type, slot_value in slots:
        slot_dict[slot_type].append(slot_value)
    
    dynasty = slot_dict.get("朝代", [""])[0]
    label = con.execute('SELECT label FROM nodes WHERE uid = ?', (uid,)).fetchone()
    name = label[0] if label else uid
    
    confidence = classify_entity(con, uid)
    
    if confidence == "famous_person":
        return f"{name}@{dynasty}"
    
    elif confidence == "relation_defined":
        # 找锚点人物（父/夫/子）
        anchors = (slot_dict.get("亲属:父", []) + 
                   slot_dict.get("亲属:夫", []) + 
                   slot_dict.get("亲属:子", []))
        if anchors:
            return f"{anchors[0]}之亲属@{dynasty}"
        return f"{name}@{dynasty}"
    
    elif confidence == "generic_reference":
        place = slot_dict.get("籍贯", [""])[0]
        return f"{name}@{dynasty}@{place}"
    
    else:
        return f"{name}@{dynasty}"


# ---------------------------------------------------------------------------
# Step 5: 关系匹配（基于ent_slots的亲属关系）
# ---------------------------------------------------------------------------
def step5_kinship_match(con, new_entity):
    """
    基于ent_slots中的亲属关系匹配。
    
    如果两个实体有相同的锚点人物+相同的关系类型 → 同一人
    
    返回: list[(uid, confidence)]
    """
    new_uid = new_entity['uid']
    new_type = new_entity['type']
    
    if new_type != 'person':
        return []
    
    # 获取新实体的亲属关系
    new_kinship = con.execute('''
        SELECT slot_type, slot_value FROM ent_slots 
        WHERE uid = ? AND slot_type LIKE '亲属:%'
    ''', (new_uid,)).fetchall()
    
    if not new_kinship:
        return []
    
    candidates = []
    
    # 对每个同类型实体，检查亲属关系是否匹配
    for uid, in con.execute('SELECT uid FROM nodes WHERE type=? AND uid!=?', (new_type, new_uid)):
        candidate_kinship = con.execute('''
            SELECT slot_type, slot_value FROM ent_slots 
            WHERE uid = ? AND slot_type LIKE '亲属:%'
        ''', (uid,)).fetchall()
        
        if not candidate_kinship:
            continue
        
        # 检查是否有相同的锚点+关系
        new_kin_dict = {(t, v) for t, v in new_kinship}
        cand_kin_dict = {(t, v) for t, v in candidate_kinship}
        
        overlap = new_kin_dict & cand_kin_dict
        
        if overlap:
            # 有相同的亲属关系
            confidence = 0.85 + 0.10 * len(overlap) / max(len(new_kin_dict), len(cand_kin_dict))
            candidates.append((uid, min(confidence, 0.95)))
    
    return candidates


# ---------------------------------------------------------------------------
# 分层匹配逻辑
# ---------------------------------------------------------------------------
def should_merge(con, uid_a, uid_b):
    """
    判断两个实体是否应该合并（考虑分层）。
    
    返回: (should_merge: bool, confidence: float, reason: str)
    """
    conf_a = classify_entity(con, uid_a)
    conf_b = classify_entity(con, uid_b)
    
    # 规则1：泛称永不合并
    if conf_a == "generic_reference" or conf_b == "generic_reference":
        return False, 0.0, "generic_reference_no_merge"
    
    # 规则2：名人精确匹配
    if conf_a == "famous_person" and conf_b == "famous_person":
        id_a = get_entity_identity(con, uid_a)
        id_b = get_entity_identity(con, uid_b)
        if id_a == id_b:
            return True, 0.95, "famous_person_identity_match"
    
    # 规则3：亲属关系匹配
    if conf_a == "relation_defined" or conf_b == "relation_defined":
        id_a = get_entity_identity(con, uid_a)
        id_b = get_entity_identity(con, uid_b)
        if id_a == id_b:
            return True, 0.85, "relation_identity_match"
    
    # 规则4：其他情况（documented_person）
    # 需要名字+朝代+籍贯都匹配
    id_a = get_entity_identity(con, uid_a)
    id_b = get_entity_identity(con, uid_b)
    
    if id_a == id_b:
        return True, 0.75, "documented_person_identity_match"
    
    return False, 0.0, "no_match"


# ---------------------------------------------------------------------------
# 综合匹配（集成四步+分层）
# ---------------------------------------------------------------------------
def match_with_layers(con, new_entity, indexes=None):
    """
    分层综合匹配。
    
    返回: list[(uid, score, step_scores, merge_decision)]
    """
    from four_step_matching import (
        step1_exact_name_match, step2_alias_match, 
        step3_relation_match, step4_context_match,
        compute_final_score
    )
    
    if indexes is None:
        indexes = {
            'alias': build_alias_index(con),
            'relation': build_relation_graph(con),
            'context': build_context_index(con)
        }
    
    # 五步匹配
    c1 = step1_exact_name_match(con, new_entity)
    c2 = step2_alias_match(con, new_entity, indexes['alias'])
    c3 = step3_relation_match(con, new_entity, indexes['relation'])
    c4 = step4_context_match(con, new_entity, indexes['context'])
    c5 = step5_kinship_match(con, new_entity)
    
    # 合并候选集
    all_candidates = {}
    
    for uid, conf in c1:
        if uid not in all_candidates:
            all_candidates[uid] = {'step1': conf, 'step2': None, 'step3': None, 'step4': None, 'step5': None}
        else:
            all_candidates[uid]['step1'] = max(all_candidates[uid]['step1'] or 0, conf)
    
    for uid, conf in c2:
        if uid not in all_candidates:
            all_candidates[uid] = {'step1': None, 'step2': conf, 'step3': None, 'step4': None, 'step5': None}
        else:
            all_candidates[uid]['step2'] = max(all_candidates[uid]['step2'] or 0, conf)
    
    for uid, conf in c3:
        if uid not in all_candidates:
            all_candidates[uid] = {'step1': None, 'step2': None, 'step3': conf, 'step4': None, 'step5': None}
        else:
            all_candidates[uid]['step3'] = max(all_candidates[uid]['step3'] or 0, conf)
    
    for uid, conf in c4:
        if uid not in all_candidates:
            all_candidates[uid] = {'step1': None, 'step2': None, 'step3': None, 'step4': conf, 'step5': None}
        else:
            all_candidates[uid]['step4'] = max(all_candidates[uid]['step4'] or 0, conf)
    
    for uid, conf in c5:
        if uid not in all_candidates:
            all_candidates[uid] = {'step1': None, 'step2': None, 'step3': None, 'step4': None, 'step5': conf}
        else:
            all_candidates[uid]['step5'] = max(all_candidates[uid]['step5'] or 0, conf)
    
    # 计算综合分数 + 分层判断
    results = []
    for uid, step_scores in all_candidates.items():
        score = compute_final_score({
            'step1': step_scores['step1'],
            'step2': step_scores['step2'],
            'step3': step_scores['step3'],
            'step4': step_scores['step4']
        })
        
        # 分层合并判断
        merge, merge_conf, reason = should_merge(con, new_entity['uid'], uid)
        
        results.append((uid, score, step_scores, merge, merge_conf, reason))
    
    # 按分数排序
    results.sort(key=lambda x: -x[1])
    
    return results


# ---------------------------------------------------------------------------
# 批量匹配
# ---------------------------------------------------------------------------
def match_all_with_layers(con):
    """
    对所有实体进行分层匹配。
    
    返回: list[(uid_a, uid_b, method, confidence, merge, reason)]
    """
    print("构建索引...")
    indexes = {
        'alias': build_alias_index(con),
        'relation': build_relation_graph(con),
        'context': build_context_index(con)
    }
    
    print(f"  别名索引: {len(indexes['alias'])} 个别名")
    print(f"  关系图: {len(indexes['relation'])} 个节点")
    print(f"  上下文索引: {len(indexes['context'])} 个节点")
    
    # 统计分层
    print("\n统计人物分层...")
    layer_counts = defaultdict(int)
    for uid, in con.execute("SELECT uid FROM nodes WHERE type='person'"):
        conf = classify_entity(con, uid)
        layer_counts[conf] += 1
    
    for layer, count in sorted(layer_counts.items()):
        print(f"  {layer}: {count}")
    
    print("\n执行分层匹配...")
    candidates = []
    seen_pairs = set()
    
    for uid, label, typ, book_id, pl in con.execute('''
        SELECT uid, label, type, book_id, payload FROM nodes
    '''):
        new_entity = {
            'uid': uid,
            'label': label,
            'type': typ,
            'book_id': book_id,
            'payload': pl
        }
        
        matches = match_with_layers(con, new_entity, indexes)
        
        for match_uid, score, step_scores, merge, merge_conf, reason in matches:
            pair = tuple(sorted([uid, match_uid]))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            
            # 确定方法
            if step_scores.get('step5') is not None:
                method = 'kinship_relation'
            elif step_scores.get('step1') is not None:
                method = 'exact_name'
            elif step_scores.get('step2') is not None:
                method = 'alias_variant'
            elif step_scores.get('step3') is not None:
                method = 'relation_network'
            else:
                method = 'context_similarity'
            
            candidates.append((pair[0], pair[1], method, score, merge, reason))
    
    print(f"\n生成 {len(candidates)} 个候选对")
    
    # 统计
    merge_count = sum(1 for c in candidates if c[4])
    print(f"  可合并: {merge_count}")
    print(f"  不合并: {len(candidates) - merge_count}")
    
    return candidates


if __name__ == "__main__":
    con = sqlite3.connect("kb_test.sqlite")
    candidates = match_all_with_layers(con)
    
    print("\nTop 20 candidates:")
    for a, b, method, score, merge, reason in candidates[:20]:
        label_a = con.execute('SELECT label FROM nodes WHERE uid=?', (a,)).fetchone()[0]
        label_b = con.execute('SELECT label FROM nodes WHERE uid=?', (b,)).fetchone()[0]
        merge_str = "MERGE" if merge else "NO_MERGE"
        print(f"  [{merge_str}] {label_a} <-> {label_b} ({method}, {score:.2f}, {reason})")
    
    con.close()
