"""refs.py —— F4-1：物化引用边 + 裸 ID 别名索引

**为什么需要这一层（实测得来的硬事实）**

F2 装载时为了消除「ID 按卷重排 / id 按实体复用」造成的碰撞，给 `records.local_id`
加了卷前缀与 `#n` 后缀：

    kzz  records.local_id = '01:ENT-0001'     payload 里却写 'ENT-0001'
    sdr  records.local_id = '01:ENT-001#2'   payload 里却写 'ENT-001'

于是各层 payload 内嵌的 16 类结构化引用（`cit.cited_ent_ids`、`lit.author_ent_ids`、
`obj.name_ent_ids`、`ming.who_ent_ids` …）**直接 join records 几乎全断**——
实测平铺 join 命中率仅 0%，连 xgf/event 也只有 1 条（它恰好没加前缀）。

修法不是回退 F2（那会把 2847 个撞号重新引进来），而是补一张**裸 ID 别名索引**：
`(book_id, 裸 ID) → [uid...]`。裸 ID = local_id 剥掉 `卷:` 前缀与 `#n` 后缀。

    实测：裸 ID 索引让 16 类引用字段解析率 0% → 100%
    （唯一「未命中」的 sdr/nam 404 条是 payload 里 ent_ids 为空数组，非解析失败）

**裸 ID 天然有歧义**：客座/五杂俎的 ENT-0001 在每一卷都存在（10 卷 → 10 个候选）。
故 `record_refs.target_ambiguous=1` 标记未唯一解析的引用，
查询端可用 `records.volume` 与引用方同卷来消歧（见 `disambiguate_by_volume`）。

本模块只做「物化」，不做对齐：对齐归 transform / query。
"""

import json
from collections import defaultdict

# payload 里承载实体引用的字段 → 语义角色。
# role 决定查询端怎么解读这条边（被引者是谁 / 作者是谁 / 施事是谁）。
REF_FIELDS = {
    # 引书
    "cited_ent_ids": "cited",
    # 文献
    "author_ent_ids": "author",
    "title_ent_ids": "title",
    # 纪事 / 事件
    "who_ent_ids": "agent",
    # 流程（新官轨范）
    "agent_ent_ids": "agent",
    # 名物 / 地名 / 方言 / 名录
    "name_ent_ids": "subject",
    "region_ent_ids": "region",
    "location_ent_ids": "location",
    "source_ent_ids": "source",
    # 职官
    "person_ent_ids": "person",
    "official_ent_ids": "official",
    "office_ent_ids": "office",
    "institution_ent_ids": "institution",
    # 关系
    "person_a_ent_ids": "subject",
    "person_b_ent_ids": "object",
    # 规则（吕公实政录 lgs/rule 等政书规则层主体引用）
    "subject_ent_ids": "subject",
    # 结构化（福惠全书 fqh/struct 目标对象引用；regs/docs 同款 target/related_item 可复用）
    "target_ent_ids": "object",
    # 各书通用兜底字段（wzz/nam, sdr/nam, xgf/actor 等大量使用）
    "ent_ids": "subject",
}

# 与 REF_FIELDS 同层的可读名字段（用于 target_text，多数为 {"text":...,"xx_ent_ids":[...]}）
TEXT_FOR_FIELD = {
    "cited_ent_ids": "cited_work",
    "author_ent_ids": "author",
    "title_ent_ids": "title",
    "who_ent_ids": "who",
    "agent_ent_ids": "agent",
    "name_ent_ids": "name",
    "region_ent_ids": "region",
    "location_ent_ids": "location",
    "source_ent_ids": "source",
    "person_ent_ids": "person",
    "official_ent_ids": "official",
    "office_ent_ids": "office",
    "institution_ent_ids": "institution",
    "person_a_ent_ids": "person_a",
    "person_b_ent_ids": "person_b",
    "target_ent_ids": "target",
    "subject_ent_ids": "subject",
}


def bare_id(local_id):
    """剥掉卷前缀与去重后缀：'01:ENT-001#2' → 'ENT-001'。"""
    return str(local_id).split(":", 1)[-1].split("#", 1)[0]


def build_bare_index(con):
    """(book_id, 裸 ID) → [uid, ...]。uid = book_id:local_id。

    这是全库引用解析的地基。len(候选)>1 即天然歧义（跨卷重名）。
    """
    idx = defaultdict(list)
    for book_id, local_id in con.execute(
        "SELECT book_id, local_id FROM records WHERE layer_key='ent'"
    ).fetchall():
        idx[(book_id, bare_id(local_id))].append(f"{book_id}:{local_id}")
    return idx


def _collect_refs(obj, out):
    """递归收集 payload 内所有 *_ent_ids。

    引用字段都嵌在子对象里（如 `{"person":{"text":"李贽","person_ent_ids":["ENT-1"]}}`），
    必须递归。全路径只取字段名——同一字段名在各书语义一致（见 REF_FIELDS）。
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in REF_FIELDS and isinstance(v, list):
                for x in v:
                    if isinstance(x, str):
                        out.setdefault(k, []).append(x)
            elif isinstance(v, (dict, list)):
                _collect_refs(v, out)
    elif isinstance(obj, list):
        for x in obj:
            _collect_refs(x, out)


def _readable_name(obj, field):
    """取与引用字段同层的可读名。两种形态：
        {"cited_work":{"text":"《书》蔡氏传","cited_ent_ids":[...]}}
        {"person":"李贽","person_ent_ids":[...]}   ← 字符串直接给名
    """
    key = TEXT_FOR_FIELD.get(field)
    if not key:
        return None
    v = obj.get(key)
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        return v.get("text")
    return None


def materialize_refs(con, book_id=None):
    """把 payload 内所有 *_ent_ids 展开进 record_refs。返回统计。

    可重跑：整体先删该书（book_id=None 时全库）再重建。
    """
    where = "" if book_id is None else " WHERE book_id=?"
    args = () if book_id is None else (book_id,)
    con.execute(f"DELETE FROM record_refs{where}", args)

    bare = build_bare_index(con)
    sql = (
        "SELECT book_id, layer_key, local_id, item_id, volume, payload "
        "FROM records"
        + ("" if book_id is None else " WHERE book_id=?")
    )
    rows = []
    stats = {"records": 0, "refs": 0, "resolved": 0, "ambiguous": 0}
    for bid, layer, local_id, item_id, volume, payload in con.execute(sql, args).fetchall():
        try:
            obj = json.loads(payload)
        except (ValueError, TypeError):
            continue
        if not isinstance(obj, dict):
            continue
        stats["records"] += 1
        found = {}
        _collect_refs(obj, found)
        for field, ids in found.items():
            role = REF_FIELDS[field]
            text = _readable_name(obj, field)
            for i, raw in enumerate(ids):
                cands = bare.get((bid, raw))
                uid = None
                amb = 0
                if cands and len(cands) == 1:
                    uid = cands[0]
                elif cands:
                    # 跨卷重名：引用方与被引方通常同卷同条，按卷消歧
                    amb = 1
                    uid = disambiguate_by_volume(con, bid, field, raw, volume)
                rows.append((
                    f"{bid}:{layer}:{local_id}:{field}#{i}",
                    bid, layer, local_id, field, role, raw, text, uid, amb,
                    item_id, volume,
                ))
                stats["refs"] += 1
                if uid:
                    stats["resolved"] += 1
                elif amb:
                    stats["ambiguous"] += 1
    if rows:
        con.executemany(
            "INSERT OR REPLACE INTO record_refs"
            " (ref_id, book_id, layer_key, local_id, field, role,"
            "  raw_target, target_text, target_uid, target_ambiguous, item_id, volume)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            rows,
        )
    con.commit()
    return stats


def disambiguate_by_volume(con, book_id, field, raw_target, volume):
    """裸 ID 在同卷内的唯一候选（引用方与被引方通常同卷同条）。

    用于消解跨卷重名歧义：'ENT-0001' 在 10 卷都有，但引用方在第 3 卷时，
    真正的目标几乎必然也在第 3 卷。
    """
    if not volume:
        return None
    cands = con.execute(
        "SELECT local_id FROM records"
        " WHERE book_id=? AND layer_key='ent' AND local_id LIKE ?",
        (book_id, f"{volume}:{raw_target}%"),
    ).fetchall()
    if len(cands) == 1:
        return f"{book_id}:{cands[0][0]}"
    return None