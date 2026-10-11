"""query.py —— F3 跨书查询（带置信度）

对任意名字做跨书检索，返回「所有可能指同一人/物的成员」+ 每个成员的
方法与置信度。名字归一复用 name_rules.json（配置驱动）。

典型用法：
  cross_search("宋濂")            # 查宋濂在各书的全部出现与对齐
  cross_search("王忠毅公")        # 带尊称的写法也能命中（归一后）
  cross_search("苏轼", type="person")
"""

import json
from collections import defaultdict

from name_resolver import normalize, load_rules, capped_confidence


class FederationQuery:
    def __init__(self, con, rules=None):
        self.con = con
        self.rules = rules or load_rules()
        self.conf_map = self.rules.get("match_confidence", {})
        self._load()

    def _load(self):
        con = self.con
        # node 索引：uid → (label, type, surfaces)
        self.node = {}
        surf_idx = defaultdict(list)
        for uid, label, typ, pl in con.execute(
            "SELECT uid, label, type, payload FROM nodes"
        ):
            surfaces = set()
            if pl:
                try:
                    surfaces = set(json.loads(pl).get("surfaces", []))
                except (ValueError, TypeError):
                    surfaces = set()
            if label:
                surfaces.add(label)
            self.node[uid] = (label, typ, surfaces)
            for s in surfaces:
                surf_idx[s].append(uid)
                surf_idx[normalize(s, self.rules)].append(uid)
        self.surf_idx = surf_idx
        # 成员：uid → (canonical_id, method, confidence, status)
        self.member = {}
        self.canon_members = defaultdict(list)
        for cid, uid, method, conf, status in con.execute(
            "SELECT canonical_id, uid, method, confidence, status FROM members"
        ):
            self.member[uid] = (cid, method, conf, status)
            self.canon_members[cid].append(uid)
        # canonical 元信息
        self.canon = {
            r[0]: (r[1], r[2], r[3])
            for r in con.execute(
                "SELECT canonical_id, repr_type, repr_label, status FROM canonical"
            )
        }

    def _match_uid_conf(self, uid, raw):
        """单个 node 对查询词的匹配方法与置信度。"""
        label, typ, surfaces = self.node[uid]
        if raw == label:
            return "exact_label", 1.0
        if raw in surfaces:
            return "surface_alias", self.conf_map.get("surface_alias", 0.90)
        base = normalize(raw, self.rules)
        if base == normalize(label, self.rules):
            return "normalized_stripped", self.conf_map.get("normalized_stripped", 0.65)
        return None, 0.0

    def cross_search(self, raw, type=None, limit=50):
        """跨书检索名字。返回按置信度分组的 canonical / 独立节点。

        每项：{canonical_id, repr_label, type, best_confidence,
               members:[{uid,book,label,method,confidence,status}]}
        命中的 node 若未并入任何 canonical，也作为独立分组返回。
        """
        base = normalize(raw, self.rules)
        # 命中 uid：raw 或 base 出现在任一 surface
        hit_uids = set(self.surf_idx.get(raw, [])) | set(self.surf_idx.get(base, []))
        # 按 method/conf 计算每个命中 uid
        uid_conf = {}
        for uid in hit_uids:
            label, typ, _s = self.node[uid]
            if type and typ != type:
                continue
            m, c = self._match_uid_conf(uid, raw)
            if m:
                uid_conf[uid] = (m, c)

        # 归到 canonical
        groups = defaultdict(list)
        for uid, (m, c) in uid_conf.items():
            cid = self.member.get(uid, (None,))[0]
            groups[cid].append((uid, m, c))

        results = []
        for cid, hits in groups.items():
            # 成员集合 = 该 canonical 的全部成员 ∪ 本组直接命中（standalone 时即命中集）
            all_uids = set(self.canon_members.get(cid, [])) if cid else set()
            all_uids |= {uid for uid, _m, _c in hits}
            members_out = []
            best = 0.0
            for uid in all_uids:
                label, typ, _s = self.node.get(uid, (None, None, set()))
                if uid in uid_conf:
                    m, c = uid_conf[uid]
                    status = self.member.get(uid, (None, None, None, "auto"))[3]
                else:
                    _, m, c, status = self.member[uid]
                best = max(best, c or 0.0)
                members_out.append({
                    "uid": uid,
                    "book": uid.split(":", 1)[0],
                    "label": label,
                    "type": typ,
                    "method": m,
                    "confidence": round(c or 0.0, 3),
                    "status": status,
                })
            members_out.sort(key=lambda x: (-x["confidence"], x["book"]))
            results.append({
                "canonical_id": cid,
                "repr_label": self.canon.get(cid, (None, raw, None))[1] if cid else (self.node.get(hits[0][0], (raw,))[0] or raw),
                "repr_type": self.canon.get(cid, (None, None, None))[0] if cid else self.node.get(hits[0][0], (None, None))[1],
                "best_confidence": round(best, 3),
                "members": members_out[:limit],
            })

        results.sort(key=lambda x: (-x["best_confidence"], x["canonical_id"] or ""))
        return results

    def resolve_across_books(self, raw):
        """逐书解析一个名字（调试 T1 用）：{book_id: [(uid,method,conf)]}。"""
        base = normalize(raw, self.rules)
        out = {}
        hit = set(self.surf_idx.get(raw, [])) | set(self.surf_idx.get(base, []))
        per_book = defaultdict(list)
        for uid in hit:
            label, typ, _s = self.node[uid]
            m, c = self._match_uid_conf(uid, raw)
            if m:
                per_book[uid.split(":", 1)[0]].append((uid, m, round(c, 3)))
        for b, lst in per_book.items():
            out[b] = sorted(lst, key=lambda x: -x[2])
        return out