"""four_step_matching.py —— 四步匹配策略

实现完整的身份判定流程：
  Step 1: 名字精确匹配
  Step 2: 别名/变体匹配
  Step 3: 关系网络匹配
  Step 4: 上下文相似度匹配
"""

import json
import sqlite3
from collections import defaultdict
from difflib import SequenceMatcher


# ---------------------------------------------------------------------------
# Step 1: 名字精确匹配
# ---------------------------------------------------------------------------
def step1_exact_name_match(con, new_entity):
    """
    跨书同名 → 大概率同一实体
    
    返回: list[(uid, confidence)]
    """
    label = new_entity['label']
    typ = new_entity['type']
    book_id = new_entity['book_id']
    
    # 查询同名实体（排除同书）
    candidates = []
    for uid, lbl, typ2, bid in con.execute('''
        SELECT uid, label, type, book_id FROM nodes
        WHERE label=? AND type=? AND book_id!=?
    ''', (label, typ, book_id)):
        candidates.append((uid, 0.90))
    
    return candidates


# ---------------------------------------------------------------------------
# Step 2: 别名/变体匹配
# ---------------------------------------------------------------------------
def step2_alias_match(con, new_entity, alias_index=None):
    """
    字/号/谥号/官称等变体指向同一人
    
    返回: list[(uid, confidence)]
    """
    if alias_index is None:
        alias_index = build_alias_index(con)
    
    label = new_entity['label']
    book_id = new_entity['book_id']
    
    # 查询别名索引
    candidates = []
    for uid in alias_index.get(label, []):
        # 排除同书
        if uid.split(':')[0] != book_id:
            candidates.append((uid, 0.85))
    
    return candidates


def build_alias_index(con):
    """
    构建别名索引: alias → [uid]
    
    从以下来源提取别名：
    1. nodes.payload.surfaces（已有的表面形式）
    2. records.payload.aliases（如果有）
    """
    alias_index = defaultdict(list)
    
    # 从 nodes.payload.surfaces 提取
    for uid, pl in con.execute('SELECT uid, payload FROM nodes'):
        if not pl:
            continue
        try:
            payload = json.loads(pl)
            surfaces = payload.get('surfaces', [])
            for surface in surfaces:
                if surface and surface != payload.get('normalized'):
                    alias_index[surface].append(uid)
        except:
            continue
    
    # 从 records.payload.aliases 提取（如果有）
    for uid, pl in con.execute('''
        SELECT n.uid, r.payload 
        FROM nodes n 
        JOIN records r ON n.book_id=r.book_id AND n.layer_key=r.layer_key AND n.local_id=r.local_id
        WHERE n.layer_key='ent'
    '''):
        if not pl:
            continue
        try:
            payload = json.loads(pl)
            aliases = payload.get('aliases', [])
            for alias in aliases:
                if isinstance(alias, dict):
                    alias_val = alias.get('value')
                else:
                    alias_val = alias
                if alias_val:
                    alias_index[alias_val].append(uid)
        except:
            continue
    
    return alias_index


# ---------------------------------------------------------------------------
# Step 3: 关系网络匹配
# ---------------------------------------------------------------------------
def step3_relation_match(con, new_entity, relation_graph=None):
    """
    共享相同的关系邻居 → 同一实体
    
    返回: list[(uid, confidence)]
    """
    if relation_graph is None:
        relation_graph = build_relation_graph(con)
    
    new_uid = new_entity['uid']
    new_type = new_entity['type']
    new_relations = relation_graph.get(new_uid, set())
    
    if not new_relations:
        return []
    
    candidates = []
    
    # 对每个同类型的实体，计算关系网络重叠度
    for uid, typ in con.execute('SELECT uid, type FROM nodes WHERE type=?', (new_type,)):
        if uid == new_uid:
            continue
        
        candidate_relations = relation_graph.get(uid, set())
        
        if not candidate_relations:
            continue
        
        # 计算 Jaccard 相似度
        overlap = len(new_relations & candidate_relations)
        total = len(new_relations | candidate_relations)
        
        if total > 0:
            similarity = overlap / total
            if similarity >= 0.7:  # 阈值
                confidence = 0.70 + 0.20 * similarity  # 0.70-0.90
                candidates.append((uid, confidence))
    
    return candidates


def build_relation_graph(con):
    """
    构建关系图: uid → set[(other_uid, predicate)]
    """
    graph = defaultdict(set)
    
    for subj, obj, pred in con.execute('''
        SELECT subject_uid, object_uid, predicate 
        FROM edges 
        WHERE subject_uid IS NOT NULL AND object_uid IS NOT NULL
    '''):
        graph[subj].add((obj, pred))
        graph[obj].add((subj, pred))
    
    return graph


# ---------------------------------------------------------------------------
# Step 4: 上下文相似度匹配
# ---------------------------------------------------------------------------
def step4_context_match(con, new_entity, context_index=None):
    """
    从 original 文本提取特征，计算相似度
    
    返回: list[(uid, confidence)]
    """
    if context_index is None:
        context_index = build_context_index(con)
    
    new_uid = new_entity['uid']
    new_type = new_entity['type']
    new_features = context_index.get(new_uid, {})
    
    if not new_features:
        return []
    
    candidates = []
    
    # 对每个同类型的实体，计算上下文相似度
    for uid, typ in con.execute('SELECT uid, type FROM nodes WHERE type=?', (new_type,)):
        if uid == new_uid:
            continue
        
        entity_features = context_index.get(uid, {})
        
        if not entity_features:
            continue
        
        # 计算特征重叠度
        era_overlap = jaccard(new_features.get('era', set()), entity_features.get('era', set()))
        place_overlap = jaccard(new_features.get('place', set()), entity_features.get('place', set()))
        office_overlap = jaccard(new_features.get('office', set()), entity_features.get('office', set()))
        
        # 加权平均
        similarity = 0.3 * era_overlap + 0.4 * place_overlap + 0.3 * office_overlap
        
        if similarity >= 0.6:  # 阈值
            confidence = 0.60 + 0.20 * similarity  # 0.60-0.80
            candidates.append((uid, confidence))
    
    return candidates


def build_context_index(con):
    """
    构建上下文索引: uid → {era: set, place: set, office: set}
    
    从 records.payload.original 提取特征
    """
    import re
    
    index = {}
    
    # 年号列表
    reigns = ['洪武', '永乐', '宣德', '正统', '景泰', '天顺', '成化', '弘治', '正德', '嘉靖', 
              '隆庆', '万历', '泰昌', '天启', '崇祯']
    
    # 地名列表（部分）
    places = ['南京', '北京', '应天', '顺天', '苏州', '杭州', '福建', '浙江', '广东', '山东', 
              '河南', '陕西', '四川', '湖广', '江西']
    
    # 官职列表（部分）
    offices = ['尚书', '侍郎', '御史', '知府', '巡抚', '内阁', '大学士', '侍郎', '郎中']
    
    for uid, pl in con.execute('''
        SELECT n.uid, r.payload 
        FROM nodes n 
        JOIN records r ON n.book_id=r.book_id AND n.layer_key=r.layer_key AND n.local_id=r.local_id
        WHERE n.layer_key='ent'
    '''):
        if not pl:
            continue
        
        try:
            payload = json.loads(pl)
            original = payload.get('original', '')
            
            if not original:
                continue
            
            # 提取特征
            features = {
                'era': set(re.findall('|'.join(reigns), original)),
                'place': set(re.findall('|'.join(places), original)),
                'office': set(re.findall('|'.join(offices), original))
            }
            
            if any(features.values()):
                index[uid] = features
        except:
            continue
    
    return index


def jaccard(set_a, set_b):
    """计算 Jaccard 相似度"""
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


# ---------------------------------------------------------------------------
# 综合匹配
# ---------------------------------------------------------------------------
def match_new_entity(con, new_entity, indexes=None):
    """
    四步综合匹配
    
    返回: list[(uid, score, step_scores)]
    """
    if indexes is None:
        indexes = {
            'alias': build_alias_index(con),
            'relation': build_relation_graph(con),
            'context': build_context_index(con)
        }
    
    # 四步匹配
    c1 = step1_exact_name_match(con, new_entity)
    c2 = step2_alias_match(con, new_entity, indexes['alias'])
    c3 = step3_relation_match(con, new_entity, indexes['relation'])
    c4 = step4_context_match(con, new_entity, indexes['context'])
    
    # 合并候选集
    all_candidates = {}
    
    for uid, conf in c1:
        if uid not in all_candidates:
            all_candidates[uid] = {'step1': conf, 'step2': None, 'step3': None, 'step4': None}
        else:
            all_candidates[uid]['step1'] = max(all_candidates[uid]['step1'] or 0, conf)
    
    for uid, conf in c2:
        if uid not in all_candidates:
            all_candidates[uid] = {'step1': None, 'step2': conf, 'step3': None, 'step4': None}
        else:
            all_candidates[uid]['step2'] = max(all_candidates[uid]['step2'] or 0, conf)
    
    for uid, conf in c3:
        if uid not in all_candidates:
            all_candidates[uid] = {'step1': None, 'step2': None, 'step3': conf, 'step4': None}
        else:
            all_candidates[uid]['step3'] = max(all_candidates[uid]['step3'] or 0, conf)
    
    for uid, conf in c4:
        if uid not in all_candidates:
            all_candidates[uid] = {'step1': None, 'step2': None, 'step3': None, 'step4': conf}
        else:
            all_candidates[uid]['step4'] = max(all_candidates[uid]['step4'] or 0, conf)
    
    # 计算综合分数
    results = []
    for uid, step_scores in all_candidates.items():
        score = compute_final_score(step_scores)
        results.append((uid, score, step_scores))
    
    # 按分数排序
    results.sort(key=lambda x: -x[1])
    
    return results


def compute_final_score(step_scores):
    """
    计算综合分数
    
    权重：
    - Step 1 (名字精确): 0.4
    - Step 2 (别名): 0.3
    - Step 3 (关系): 0.2
    - Step 4 (上下文): 0.1
    """
    weights = {
        'step1': 0.4,
        'step2': 0.3,
        'step3': 0.2,
        'step4': 0.1
    }
    
    total_weight = 0
    weighted_sum = 0
    
    for step, score in step_scores.items():
        if score is not None:
            weighted_sum += weights[step] * score
            total_weight += weights[step]
    
    return weighted_sum / total_weight if total_weight > 0 else 0.0


# ---------------------------------------------------------------------------
# 批量匹配
# ---------------------------------------------------------------------------
def match_all_entities(con):
    """
    对所有实体进行匹配，生成候选链接
    
    返回: list[(uid_a, uid_b, method, confidence)]
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
    
    print("\n执行匹配...")
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
        
        matches = match_new_entity(con, new_entity, indexes)
        
        for match_uid, score, step_scores in matches:
            # 规范化顺序，避免重复
            pair = tuple(sorted([uid, match_uid]))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            
            # 确定方法
            if step_scores['step1'] is not None:
                method = 'exact_name'
            elif step_scores['step2'] is not None:
                method = 'alias_variant'
            elif step_scores['step3'] is not None:
                method = 'relation_network'
            else:
                method = 'context_similarity'
            
            candidates.append((pair[0], pair[1], method, score))
    
    print(f"\n生成 {len(candidates)} 个候选对")
    
    return candidates
