"""assoc.py —— F4-3：10 个跨书关联查询

设计原则（按用户「有价值」的标准筛）：
 1. **必须有数据支撑**——每个查询都在真实库上跑得出非空结果，不做想象式设计。
    跑不出结果的（如 Q9 无共现实体时）**如实报告缺口**，不用假数据凑。
 2. **必须跨书**——单书内的检索用不上联邦库；这十个都至少跨越 2 本书，
    或连接「书内关系 + 跨书对齐」两侧。
 3. **必须带出处**——每个结论都能回指 (book, layer, local_id)，可回查原文。
 4. **不重造轮子**——名字归一/置信度一律走 name_resolver + canonical/members，
    不在查询层另写一套匹配。

十个查询（括号内为所用层/表）：
  Q1  跨书同一人      identity_bridge     (canonical/members + record_refs)
  Q2  人物关系网      person_network      (edges.rel + record_refs.person_*)
  Q3  官职升迁链      career_chain        (edges.appt)
  Q4  引文互证        citation_network    (record_refs.cited + records.cit/lit)
  Q5  作品-作者网络   work_author         (record_refs.author + records.lit)
  Q6  地名风物        place_culture       (record_refs.region/location + cus/obj/geo)
  Q7  名物流传        object_lineage      (record_refs.name + records.obj/nam)
  Q8  事件-人物-观点   event_opinion       (records.event/opn/ming + record_refs)
  Q9  同条目对读      parallel_reading    (records.trl + record_refs 共现实体)
  Q10 悬空引用待补    dangling_refs       (pending_refs + record_refs 未解析)

**踩过的坑（别重犯）**
- payload 里的 `*_ent_ids` 是**裸 ID**（ENT-0001），而 records.local_id 因 F2
  加了卷前缀/去重后缀（01:ENT-001#2）——直接 join 命中率 0%。必须走 refs.py
  的裸 ID 别名索引（实测解析率 0% → 86.5%）。
- `《礼记》` 与 `礼记`、`礼记正义` 是同一部书：书名号/注本尾缀必须归一，
  否则引文网络查不到。这是 name_rules 的 `wrapping_marks`/`work_tail_suffix` 存在的原因。
- 「科举」是 event.type 的**枚举分类**而非实体，Q8 只走实体引用会返回空，
  必须另加关键词匹配路径。
- Q9 的跨书对读轴：各书 trl 条目**几乎无共现实体**（卷首各讲各的），
  故按共现实体配对常为 0；此时如实返回 `natural_alignment: false`，
  而非用 item_id（各书卷首编号撞号但题材无关）或文本指纹（措辞必不同）硬凑。
"""

import json
from collections import defaultdict

from query import FederationQuery
from name_resolver import load_rules, normalize


def _label_of(con, uid):
    if not uid:
        return None
    r = con.execute("SELECT label, type, book_id FROM nodes WHERE uid=?", (uid,)).fetchone()
    return {"uid": uid, "label": r[0], "type": r[1], "book": r[2]} if r else None


def _rec(con, book, layer, local_id):
    """回指一条记录（出处锚点），带可读摘要。"""
    r = con.execute(
        "SELECT item_id, volume, payload FROM records"
        " WHERE book_id=? AND layer_key=? AND local_id=?",
        (book, layer, local_id),
    ).fetchone()
    if not r:
        return None
    try:
        d = json.loads(r[2])
    except (ValueError, TypeError):
        d = {}
    # 摘要：取最有信息量的几个标量字段
    brief = {}
    for k in ("topic", "term", "name", "title", "action", "what", "type", "stance",
              "category", "office", "relation_type", "cited_work", "region",
              "era", "when", "where", "summary", "person_a", "person_b"):
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            brief[k] = v.strip()[:60]
        elif isinstance(v, dict):
            t = v.get("text")
            if isinstance(t, str) and t.strip():
                brief[k] = t.strip()[:60]
    return {
        "ref": f"{book}/{layer}/{local_id}",
        "book": book, "layer": layer, "local_id": local_id,
        "item_id": r[0], "volume": r[1], "brief": brief,
    }


class AssocQuery:
    """十个关联查询的统一入口。所有查询跨书、带出处。"""

    def __init__(self, con, rules=None):
        self.con = con
        self.rules = rules or load_rules()
        self.fq = FederationQuery(con, self.rules)

    # ------------------------------------------------------------------
    # Q1 跨书同一人：他在各书都被怎么记的
    # ------------------------------------------------------------------
    def identity_bridge(self, name, limit=20):
        """一个人的「跨书身份对照表」：各书怎么说、置信度多少、有何异文。

        这是联邦库最核心的查询——解决「同一人在六书里被写成六个名字」。
        """
        groups = self.fq.cross_search(name, limit=limit)
        out = []
        for g in groups:
            cid = g["canonical_id"]
            rows = []
            for m in g["members"]:
                uid = m["uid"]
                # 该成员在各层被引用的次数（活跃度）
                cited = self.con.execute(
                    "SELECT layer_key, COUNT(*) FROM record_refs"
                    " WHERE target_uid=? GROUP BY layer_key",
                    (uid,),
                ).fetchall()
                rows.append({
                    **m,
                    "referenced_by": {l: c for l, c in cited},
                    "activity": sum(c for _l, c in cited),
                })
            rows.sort(key=lambda r: (-r["confidence"], -r["activity"], r["book"]))
            out.append({
                "query": name,
                "canonical_id": cid,
                "repr_label": g["repr_label"],
                "repr_type": g["repr_type"],
                "best_confidence": g["best_confidence"],
                "books_covered": sorted({r["book"] for r in rows}),
                "variants": rows,
            })
        return out

    # ------------------------------------------------------------------
    # Q2 人物关系网：跨书对齐后的人在各书里的关系
    # ------------------------------------------------------------------
    def person_network(self, name, predicates=None, limit=60):
        """某人的关系网。**关键价值**：A 书说他与 X 是师徒，B 书说他与 X 敌对——
        跨书对齐后才能看出矛盾/补充。

        predicates 过滤关系类型（如 ['师生','同僚','父子']）。
        """
        uids, cid = self._identity_uids(name, type="person")
        if not uids:
            return []

        adj = defaultdict(list)
        ph = ",".join("?" * len(uids))
        # edges 里的关系边
        for subj, obj, pred, b, l, lid in self.con.execute(
            f"SELECT subject_uid, object_uid, predicate, book_id, layer_key, local_id"
            f"  FROM edges WHERE layer_key='rel'"
            f"   AND (subject_uid IN ({ph}) OR object_uid IN ({ph}))",
            uids + uids,
        ).fetchall():
            if not subj or not obj:
                continue
            adj[subj].append((obj, pred, b, l, lid))
            adj[obj].append((subj, pred, b, l, lid))
        # record_refs 里的 person_a/person_b 引用
        for tgt, role, b, l, lid, field in self.con.execute(
            f"SELECT target_uid, role, book_id, layer_key, local_id, field"
            f"  FROM record_refs"
            f" WHERE field IN ('person_a_ent_ids','person_b_ent_ids')"
            f"   AND target_uid IN ({ph})",
            uids,
        ).fetchall():
            if not tgt:
                continue
            adj[tgt].append((None, f"{field}", b, l, lid))

        neighbors = []
        for uid in uids:
            for other, pred, b, l, lid in adj.get(uid, []):
                if predicates and pred and not any(p in pred for p in predicates):
                    continue
                info = _label_of(self.con, other)
                anchor = _rec(self.con, b, l, lid)
                neighbors.append({
                    "from": _label_of(self.con, uid),
                    "predicate": pred,
                    "to": info,
                    "evidence": anchor,
                })
        # 按关系类型聚合：同一关系类别跨书合并呈现
        by_pred = defaultdict(lambda: {"count": 0, "books": set(), "people": {}})
        for nb in neighbors:
            k = (nb["predicate"] or "未明").split("（")[0].strip()
            slot = by_pred[k]
            slot["count"] += 1
            slot["books"].add(nb["evidence"]["book"] if nb["evidence"] else "?")
            if nb["to"]:
                slot["people"][nb["to"]["uid"]] = nb["to"]["label"]
        summary = sorted(
            [{"predicate": k, "count": v["count"], "books": sorted(v["books"]),
              "people": list(v["people"].values())[:8]}
             for k, v in by_pred.items()],
            key=lambda x: -x["count"],
        )
        return {
            "query": name,
            "canonical_id": cid,
            "identity": (self.fq.canon.get(cid, (None, name, None))[1] or name),
            "degree": len(neighbors),
            "relation_kinds": summary,
            "edges": neighbors[:limit],
        }

    # ------------------------------------------------------------------
    # Q3 官职升迁链：一个人在各书的仕宦轨迹
    # ------------------------------------------------------------------
    def career_chain(self, name, limit=50):
        """跨书仕宦履历。appt 的 `when` 字段含年份，可排时间线。

        价值：客座记「万历二十三年状元」，蘧编记「加少傅…」，跨书拼出完整仕途。
        """
        uids, cid = self._identity_uids(name, type="person")
        if not uids:
            return []
        # appt 记录本身不存 ent_id，只能靠 edges.appt 的 person→uid 边连接
        rows = self._appt_by_local(uids)
        chain = []
        for book, layer, lid, payload, person_label in rows:
            try:
                d = json.loads(payload)
            except (ValueError, TypeError):
                continue
            chain.append({
                "book": book, "person": person_label,
                "office": _txt(d.get("office")),
                "institution": _txt(d.get("institution")),
                "when": d.get("when"),
                "status": d.get("status"),
                "evidence": _rec(self.con, book, layer, lid),
            })
        # 无年份的排最后
        chain.sort(key=lambda c: (not bool(c["when"]), str(c["when"] or "")))
        return {
            "query": name, "canonical_id": cid,
            "identity": (self.fq.canon.get(cid, (None, name, None))[1] or name),
            "books": sorted({c["book"] for c in chain}),
            "appointments": chain,
        }

    def _appt_by_local(self, uids):
        """把 uid 集合转成 (book, local_id) 集合，按 appt 记录回捞。
        appt 记录没有 ent_id 字段，只能靠 edges.appt 的 person→uid 边连接。
        """
        out = []
        ph = ",".join("?" * len(uids))
        seen = set()
        for subj, b, layer, lid, payload in self.con.execute(
            f"SELECT subject_uid, book_id, layer_key, local_id, payload"
            f"  FROM edges WHERE layer_key='appt' AND subject_uid IN ({ph})",
            uids,
        ).fetchall():
            key = (b, layer, lid)
            if key in seen:
                continue
            seen.add(key)
            plabel = _label_of(self.con, subj)
            out.append((b, layer, lid, payload, plabel["label"] if plabel else None))
        return out

    # ------------------------------------------------------------------
    # Q4 引文互证：一部书被哪些书引用、在什么语境下
    # ------------------------------------------------------------------
    def citation_network(self, work, limit=60):
        """某部书/某个被引对象的引用网络（跨书）。

        数据源：record_refs.role='cited'（kzz cit 层的 cited_ent_ids）。
        """
        target = self._resolve(work)
        if not target:
            return []
        out = []
        for uid in target:
            for row in self.con.execute(
                "SELECT book_id, layer_key, local_id, target_text, item_id, volume"
                "  FROM record_refs WHERE target_uid=? AND role='cited'",
                (uid,),
            ).fetchall():
                anchor = _rec(self.con, row[0], row[1], row[2])
                if anchor:
                    out.append({
                        "cited_work": work,
                        "cited_uid": uid,
                        "citing_book": row[0],
                        "citing_ref": anchor,
                        "cited_as": row[3],
                    })
        return {
            "query": work,
            "citations": out,
            "books_citing": sorted({c["citing_book"] for c in out}),
        }

    # ------------------------------------------------------------------
    # Q5 作品-作者网络：谁写了什么、跨书互见
    # ------------------------------------------------------------------
    def work_author(self, author, limit=60):
        """某作者的作品，并标出哪些作品也被别的书写到（跨书互见）。"""
        target = self._resolve(author)
        if not target:
            return []
        works = []
        seen = set()
        for uid in target:
            for row in self.con.execute(
                "SELECT book_id, layer_key, local_id, target_text"
                "  FROM record_refs WHERE target_uid=? AND role='author'",
                (uid,),
            ).fetchall():
                key = (row[0], row[1], row[2])
                if key in seen:
                    continue
                seen.add(key)
                anchor = _rec(self.con, row[0], row[1], row[2])
                if anchor:
                    works.append({"book": row[0], "work_ref": anchor,
                                  "work_title": row[3] or anchor["brief"].get("title")})
        # 同名作品跨书聚合（按标题）
        by_title = defaultdict(list)
        for w in works:
            key = w["work_title"] or w["work_ref"]["local_id"]
            by_title[key].append(w)
        shared = {t: ws for t, ws in by_title.items() if len({w["book"] for w in ws}) > 1}
        return {
            "query": author,
            "author_uids": target,
            "works": works,
            "shared_works_cross_book": [
                {"title": t, "books": sorted({w["book"] for w in ws}),
                 "refs": [w["work_ref"] for w in ws]}
                for t, ws in shared.items()
            ],
        }

    # ------------------------------------------------------------------
    # Q6 地名风物：一个地方的风物/习俗/掌故
    # ------------------------------------------------------------------
    def place_culture(self, place, limit=80):
        """某地的地方志式聚合：方言风俗 + 名物 + 地理 + 掌故纪事。

        客座赘语是金陵掌故、五杂俎是南京风物，此查询把两书按**地名 canonical**
        拼起来——单看任一书都不完整。
        """
        target = self._resolve(place)
        if not target:
            return []
        buckets = defaultdict(list)
        ROLE2LAYER = {"region": "cus", "location": "geo", "subject": None, "name": None}
        for uid in target:
            for role, book, layer, lid, text, item in self.con.execute(
                "SELECT role, book_id, layer_key, local_id, target_text, item_id"
                "  FROM record_refs WHERE target_uid=?",
                (uid,),
            ).fetchall():
                anchor = _rec(self.con, book, layer, lid)
                if not anchor:
                    continue
                # 归到语义桶
                if layer == "cus":
                    b = "方言风俗"
                elif layer == "obj":
                    b = "名物"
                elif layer == "geo":
                    b = "地理"
                elif layer == "nam":
                    b = "名录"
                elif layer == "ming" or layer == "event":
                    b = "纪事"
                else:
                    b = f"其他({layer})"
                buckets[b].append({
                    "book": book, "role": role, "as": text, **anchor,
                })
        return {
            "query": place,
            "place_uids": target,
            "sections": [
                {"section": k, "count": len(v),
                 "books": sorted({x["book"] for x in v}),
                 "entries": v[:limit]}
                for k, v in sorted(buckets.items(), key=lambda kv: -len(kv[1]))
            ],
        }

    # ------------------------------------------------------------------
    # Q7 名物流传：某个名物在各书被如何记载
    # ------------------------------------------------------------------
    def object_lineage(self, name, limit=60):
        """一个名物（如「刀鰶鱼」「 assigns」）的跨书记载对照：形制/习性/传说。"""
        target = self._resolve(name)
        if not target:
            return []
        entries = []
        for uid in target:
            for book, layer, lid, text, item, vol in self.con.execute(
                "SELECT book_id, layer_key, local_id, target_text, item_id, volume"
                "  FROM record_refs WHERE target_uid=? AND layer_key IN ('obj','nam','cus')",
                (uid,),
            ).fetchall():
                anchor = _rec(self.con, book, layer, lid)
                if anchor:
                    entries.append({
                        "book": book, "as": text, "volume": vol,
                        "category": anchor["brief"].get("category"),
                        "evidence": anchor,
                    })
        return {
            "query": name,
            "object_uids": target,
            "books": sorted({e["book"] for e in entries}),
            "records": entries,
        }

    # ------------------------------------------------------------------
    # Q8 事件-人物-观点：同一事件各书的叙述与评价
    # ------------------------------------------------------------------
    def event_opinion(self, keyword, limit=60):
        """按关键词/实体串起「事件 + 人物 + 观点 + 纪事」的跨书对照。

        客座与五杂俎对同类事件常有不同立场（opn.stance），此查询并列呈现。

        两条检索路径（缺一不可）：
          A. entity 路径：keyword 解析为实体 → 找引用该实体的 event/opn/ming 记录
          B. keyword 路径：keyword 直接在 event.type / opn.topic / ming.era 等
             **分类字段**里做文本匹配——「科举」是事件分类而非实体，
             只有 B 能找到（实测 A 路径对「科举」返回空）。
        """
        events, opinions, ming = [], [], []

        # B 路径：分类字段文本匹配（跨书）
        like = f"%{keyword}%"
        for book, layer, lid, item in self.con.execute(
            "SELECT book_id, layer_key, local_id, item_id FROM records"
            " WHERE layer_key IN ('event','opn','ming')"
            "   AND (payload LIKE ?)"
            + (" AND book_id=?" if False else ""),
            (like,),
        ).fetchall():
            anchor = _rec(self.con, book, layer, lid)
            if not anchor:
                continue
            b = anchor["brief"]
            if layer == "event":
                events.append({
                    "book": book, "type": b.get("type"), "action": b.get("action"),
                    "what": b.get("what"), "when": b.get("when"),
                    "where": b.get("where"), "via": "keyword",
                    "evidence": anchor,
                })
            elif layer == "opn":
                opinions.append({
                    "book": book, "topic": b.get("topic"), "stance": b.get("stance"),
                    "argument": b.get("argument"), "via": "keyword",
                    "evidence": anchor,
                })
            elif layer == "ming":
                ming.append({
                    "book": book, "era": b.get("era"), "what": b.get("what"),
                    "when": b.get("when"), "via": "keyword", "evidence": anchor,
                })

        # A 路径：实体引用
        target = self._resolve(keyword)
        for uid in target:
            for book, layer, lid, item in self.con.execute(
                "SELECT book_id, layer_key, local_id, item_id"
                "  FROM record_refs WHERE target_uid=?", (uid,)
            ).fetchall():
                anchor = _rec(self.con, book, layer, lid)
                if not anchor:
                    continue
                b = anchor["brief"]
                if layer == "event":
                    events.append({
                        "book": book, "type": b.get("type"), "action": b.get("action"),
                        "what": b.get("what"), "when": b.get("when"),
                        "where": b.get("where"), "via": "entity",
                        "evidence": anchor,
                    })
                elif layer == "opn":
                    opinions.append({
                        "book": book, "topic": b.get("topic"), "stance": b.get("stance"),
                        "argument": b.get("argument"), "via": "entity",
                        "evidence": anchor,
                    })
                elif layer == "ming":
                    ming.append({
                        "book": book, "era": b.get("era"), "what": b.get("what"),
                        "when": b.get("when"), "via": "entity", "evidence": anchor,
                    })

        # 去重（同 ref 只保留一次）
        def dedup(lst):
            seen, out = set(), []
            for x in lst:
                k = x["evidence"]["ref"]
                if k in seen:
                    continue
                seen.add(k)
                out.append(x)
            return out

        events, opinions, ming = dedup(events), dedup(opinions), dedup(ming)
        return {
            "query": keyword,
            "entity_uids": target,
            "counts": {"events": len(events), "opinions": len(opinions),
                       "chronicles": len(ming)},
            "events": events[:limit],
            "opinions": opinions[:limit],
            "chronicles": ming[:limit],
            "cross_book_contrasts": _contrast(events, opinions),
        }

    # ------------------------------------------------------------------
    # Q9 同条目对读：两书讲同一件事时怎么说
    # ------------------------------------------------------------------
    def parallel_reading(self, keyword, limit=40):
        """跨书「对读」：按关键词找各书的同题材条目，并列原文译文。

        这是六书里 trl（古今翻译）层的真正价值所在——同一制度/名物，
        不同书各译一遍，可直接比对。

        分组说明：item_id（如 '01-001'）在多本书里都存在但**题材无关**
        （各自卷一第一条），不能当跨书对齐依据。
        主题键改用**共现实体集**：两书的两条记录若引用了同一批实体
        （nodes.label 归一后），即判为同题材。这比文本指纹可靠——
        措辞可以天差地别，但共引的人/地/物是硬事实。
        """
        kw = str(keyword).strip()
        if not kw:
            return {"query": kw, "cross_book_items": [], "count": 0}

        # 1) 扫 trl，取含关键词的译文；同时收集该记录共引的实体标签
        by_book = defaultdict(list)
        for book, layer, lid, item, vol, payload in self.con.execute(
            "SELECT book_id, layer_key, local_id, item_id, volume, payload"
            "  FROM records WHERE layer_key='trl'"
        ).fetchall():
            if kw not in (payload or ""):
                continue
            try:
                d = json.loads(payload)
            except (ValueError, TypeError):
                continue
            tr = d.get("translation") or ""
            # 关键词可能只在原文里（译文用现代词），故译文优先、原文兜底
            pos = tr.find(kw)
            src = "translation"
            if pos >= 0:
                snippet = tr[max(0, pos - 20): pos + 40].strip()
            else:
                orig = d.get("original") or d.get("norm") or ""
                pos_o = orig.find(kw)
                src = "original" if pos_o >= 0 else "translation_head"
                snippet = (orig[max(0, pos_o - 20): pos_o + 40].strip()
                           if pos_o >= 0 else tr[:60].strip())

            # 同 item 的其他层记录 → 它们引用的实体 = 本条的题材指纹
            co = set(self._item_entities(book, item))
            by_book[book].append({
                "book": book, "volume": vol, "item_id": item,
                "style": d.get("style"),
                "matched_in": src,
                "snippet": snippet,
                "co_entities": sorted(co)[:8],
                "_coset": co,
                "translation": tr[:300],
                "evidence": _rec(self.con, book, layer, lid),
            })

        # 2) 以共现实体集跨书配对（Jaccard 相似度 > 0 者视为同题材）
        entries = [e for lst in by_book.values() for e in lst]
        pairs = []
        for i, a in enumerate(entries):
            for b in entries[i + 1:]:
                if a["book"] == b["book"]:
                    continue
                inter = a["_coset"] & b["_coset"]
                if not inter:
                    continue
                union = a["_coset"] | b["_coset"]
                jac = len(inter) / len(union) if union else 0.0
                pairs.append({
                    "similarity": round(jac, 3),
                    "shared_entities": sorted(inter)[:6],
                    "books": sorted({a["book"], b["book"]}),
                    "readings": [
                        {k: v for k, v in a.items() if k != "_coset"},
                        {k: v for k, v in b.items() if k != "_coset"},
                    ],
                })
        pairs.sort(key=lambda p: (-p["similarity"], p["books"]))
        # 各书的题材指纹一览：即使没有天然对读轴，也让人工看出「各书各讲什么」
        per_book = []
        for b, lst in sorted(by_book.items()):
            co = sorted({e for x in lst for e in x["co_entities"]})
            per_book.append({
                "book": b, "hits": len(lst),
                "top_entities": co[:10],
                "volumes": sorted({str(x["volume"]) for x in lst})[:8],
            })
        return {
            "query": kw,
            "books_with_hits": sorted(by_book.keys()),
            "total_hits": len(entries),
            "cross_book_topics": len(pairs),
            "natural_alignment": bool(pairs),
            "note": (
                None if pairs else
                "无天然对读轴：各书命中条目无共现实体（卷首各讲各的）。"
                "故不硬凑配对，改列各书题材指纹供人工选对读入口。"
            ),
            "per_book": per_book,
            "cross_book_items": pairs[:limit],
            "count": len(pairs),
        }

    def _item_entities(self, book, item):
        """某条 item 的全部层记录引用到的实体 label（归一后）——题材指纹来源。"""
        if not item:
            return []
        rows = self.con.execute(
            "SELECT DISTINCT n.label FROM record_refs r"
            "  JOIN records rc ON rc.book_id=r.book_id AND rc.layer_key=r.layer_key"
            "     AND rc.local_id=r.local_id"
            "  JOIN nodes n ON n.uid = r.target_uid"
            " WHERE r.book_id=? AND rc.item_id=?"
            " LIMIT 40",
            (book, item),
        ).fetchall()
        out = []
        for (label,) in rows:
            if label:
                out.append(_topic_norm(label, self.rules))
        return sorted(set(out))

    # ------------------------------------------------------------------
    # Q10 悬空引用待补：解析失败的名字（数据缺口清单）
    # ------------------------------------------------------------------
    def dangling_refs(self, limit=60, book_id=None):
        """列出未能解析到实体的引用——既是缺口，也是**下一本书的补录清单**。

        两类：pending_refs（名字解析失败）与 record_refs 里 target_uid 为空者。
        """
        pend = self.con.execute(
            "SELECT book_id, layer_key, local_id, field, raw_name"
            "  FROM pending_refs"
            + (" WHERE book_id=?" if book_id else "")
            + " LIMIT ?",
            ((book_id,) if book_id else ()) + (limit,),
        ).fetchall()
        unres = self.con.execute(
            "SELECT book_id, layer_key, local_id, field, raw_target, target_text, target_ambiguous"
            "  FROM record_refs WHERE target_uid IS NULL"
            + (" AND book_id=?" if book_id else "")
            + " LIMIT ?",
            ((book_id,) if book_id else ()) + (limit,),
        ).fetchall()
        return {
            "pending_name_refs": [
                {"ref": f"{b}/{l}/{lid}", "field": f, "name": nm,
                 "book": b, "evidence": _rec(self.con, b, l, lid)}
                for b, l, lid, f, nm in pend
            ],
            "unresolved_id_refs": [
                {"ref": f"{b}/{l}/{lid}", "field": f, "raw_id": rid,
                 "text": txt, "ambiguous": amb, "book": b,
                 "evidence": _rec(self.con, b, l, lid)}
                for b, l, lid, f, rid, txt, amb in unres
            ],
            "counts": {
                "pending_names": self.con.execute(
                    "SELECT COUNT(*) FROM pending_refs").fetchone()[0],
                "unresolved_ids": self.con.execute(
                    "SELECT COUNT(*) FROM record_refs WHERE target_uid IS NULL").fetchone()[0],
            },
        }

    # ------------------------------------------------------------------
    def _identity_uids(self, name, type=None, cap=200):
        """名字 → 该身份的全部 uid（跨书所有写法），按活跃度降序。

        两个必须注意的坑（都实测踩过）：
        1) 不能只用 groups[0] 的 members —— 同一身份可能被拆成多个 group
           （canonical 未对齐时），应取成员最多的组，并把所有 group 的成员合并。
        2) cross_search 的 limit 是「输出条数」，拿它当检索范围会把关键的
           高活跃 uid 截掉（苏轼 35 个 uid，limit=2 时恰好漏掉唯一有关系边的那个）。
        """
        groups = self.fq.cross_search(name, type=type, limit=50)
        if not groups:
            return [], None
        groups = [g for g in groups if g["members"]] or groups
        groups.sort(key=lambda g: (-len(g["members"]), -g["best_confidence"]))
        uids = list(dict.fromkeys(m["uid"] for g in groups for m in g["members"]))
        self._sort_by_activity(uids)
        return uids[:cap], groups[0]["canonical_id"]

    def _sort_by_activity(self, uids):
        """按被引用次数（活跃度）降序。kzz 有 10 个叫「陈沂」的 ent，
        cross_search 前 N 个未必包含真正被 lit 层引用的那个，不重排会漏。"""
        def activity(uid):
            return self.con.execute(
                "SELECT COUNT(*) FROM record_refs WHERE target_uid=?", (uid,)
            ).fetchone()[0]
        uids.sort(key=activity, reverse=True)

    def _resolve(self, name):
        """名字 → uid 列表（跨书、含置信度，活跃度降序）。"""
        uids, _cid = self._identity_uids(name)
        return uids

    # ------------------------------------------------------------------
    def catalog(self):
        """十个查询的自述：名字 / 说明 / 用到哪些层。供 MCP 的 tools/list。"""
        return [
            {"name": "identity_bridge", "cn": "跨书同一人",
             "desc": "一人的跨书身份对照：各书怎么记、置信度、异文、活跃度",
             "params": {"name": "人名（支持尊称/谥号等任意称呼）"}},
            {"name": "person_network", "cn": "人物关系网",
             "desc": "某人在各书的关系，按关系类聚合，跨书可看出矛盾/互补",
             "params": {"name": "人名", "predicates": "关系类型过滤（可选，列表）"}},
            {"name": "career_chain", "cn": "官职升迁链",
             "desc": "跨书仕宦履历时间线（appt 的 when 字段）",
             "params": {"name": "人名"}},
            {"name": "citation_network", "cn": "引文互证",
             "desc": "某部书/对象被哪些书引用、在什么条目",
             "params": {"work": "被引书名/对象名"}},
            {"name": "work_author", "cn": "作品-作者网络",
             "desc": "某作者的作品，并标出跨书共见的同名作品",
             "params": {"author": "作者名"}},
            {"name": "place_culture", "cn": "地名风物",
             "desc": "某地的地方志式聚合：方言风俗+名物+地理+纪事，跨书拼接",
             "params": {"place": "地名"}},
            {"name": "object_lineage", "cn": "名物流传",
             "desc": "某名物在各书的记载对照（形制/习性/传说）",
             "params": {"name": "名物名"}},
            {"name": "event_opinion", "cn": "事件-人物-观点",
             "desc": "同一实体的事件+观点+纪事跨书对照，显出不同立场",
             "params": {"keyword": "人名/地名/事件关键词"}},
            {"name": "parallel_reading", "cn": "跨书对读",
             "desc": "按关键词找各书同题材条目的译文，并列比对",
             "params": {"keyword": "关键词"}},
            {"name": "dangling_refs", "cn": "悬空引用待补",
             "desc": "未解析的名字/ID 引用清单——数据缺口与下一本书补录清单",
             "params": {"book_id": "限定某书（可选）"}},
        ]


def _txt(v):
    if isinstance(v, str):
        return v.strip() or None
    if isinstance(v, dict):
        t = v.get("text")
        return t.strip() if isinstance(t, str) and t.strip() else None
    return None


def _topic_norm(label, rules):
    """题材指纹里的实体名归一：剥装饰词，截断到前4 字以容忍书名号/注本尾缀差异。"""
    base = normalize(label, rules) or label
    base = base.strip()
    return base[:4] if len(base) > 4 else base



def _contrast(events, opinions):
    """并列呈现跨书对同一实体的不同记载/立场。"""
    books_e = sorted({e["book"] for e in events})
    books_o = sorted({o["book"] for o in opinions})
    return {
        "event_books": books_e,
        "opinion_books": books_o,
        "stances": sorted({o.get("stance") for o in opinions if o.get("stance")}),
        "has_cross_book_divergence": len(books_e) > 1 or len(books_o) > 1,
    }