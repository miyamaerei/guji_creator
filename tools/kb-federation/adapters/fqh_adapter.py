"""adapters/fqh_adapter.py —— 福惠全书（fqh）适配器

与 YszAdapter/LgsAdapter 同构（_layers/<key>/<key>_NN.json 子目录 + _kg_join.json records 指针），
启用九层：ent / rule / struct / reg / opn / proc / doc / rel / trl。
- ent：ent_id 全局唯一跨卷复用 → 按 ent_id 去重合并 surfaces。
- 其余各层：rule_id / struct_id / reg_id / opn_id / process_id / doc_id / rel_id / trl_id
  全局唯一段位分配，local_id 直取记录 ID。
注意：id_key 必须对实际字段名（xzl 曾误用 evt_id 实为 event_id 致 50 折叠；proc 为 process_id 非 proc_id）。
"""

import os

from .base import BookAdapter, LayerSlice
from . import LAYER_DECL


class FqhAdapter(BookAdapter):
    LAYER_DIR = "_layers"
    JOIN_REL = "_kg_join.json"

    # 福惠产物目录为复数（rules/structs/regs/opns/procs/docs/rels），ent 单复同形
    LAYER_DIR_NAMES = {
        "ent": "ent",
        "rule": "rules",
        "struct": "structs",
        "reg": "regs",
        "opn": "opns",
        "proc": "procs",
        "doc": "docs",
        "rel": "rels",
    }

    ID_KEYS = {
        "rule": "rule_id",
        "struct": "struct_id",
        "reg": "reg_id",
        "opn": "opn_id",
        "proc": "process_id",
        "doc": "doc_id",
        "rel": "rel_id",
        "trl": "trl_id",
    }

    def __init__(self, book_id, source_root, layer_keys, join_rel=JOIN_REL):
        super().__init__(book_id, source_root)
        self.layer_keys = list(layer_keys)
        self.join_rel = join_rel

    def _layer_files(self):
        """扫描 _layers/<复数目录>/<复数key>_NN.json（福惠产物目录与文件名均为复数）。"""
        out = {}
        for key in self.layer_keys:
            d = os.path.join(self.source_root, self.LAYER_DIR,
                             self.LAYER_DIR_NAMES.get(key, key))
            if not os.path.isdir(d):
                continue
            name_prefix = self.LAYER_DIR_NAMES.get(key, key)
            for f in sorted(os.listdir(d)):
                if not f.endswith(".json"):
                    continue
                base = f[:-5]
                parts = base.rsplit("_", 1)
                if len(parts) != 2:
                    continue
                prefix, vol = parts
                if prefix != name_prefix:
                    continue
                out.setdefault(key, []).append((vol, os.path.join(d, f)))
        return out

    def discover(self):
        slices = {}
        for layer, files in self._layer_files().items():
            recs = []
            seen_ent = {}
            for vol, path in files:
                d = self._read_abspath(path)
                if not d:
                    continue
                for rec in d.get("records") or []:
                    if not isinstance(rec, dict):
                        continue
                    if layer == "ent":
                        eid = rec.get("ent_id")
                        if not eid:
                            continue
                        if eid in seen_ent:
                            i = seen_ent[eid]
                            prev = recs[i]["payload"]
                            texts = set()
                            for t in (prev.get("text"), rec.get("text")):
                                if isinstance(t, str) and t.strip():
                                    texts.add(t.strip())
                            if len(texts) > 1:
                                prev["surfaces"] = sorted(texts)
                            continue
                        seen_ent[eid] = len(recs)
                        local = eid
                    else:
                        id_key = self.ID_KEYS.get(layer)
                        local = rec.get(id_key) or rec.get("item_id") or "?"
                    recs.append(
                        {
                            "local_id": str(local),
                            "item_id": rec.get("item_id"),
                            "volume": rec.get("volume") or d.get("volume") or vol,
                            "payload": rec,
                        }
                    )
            if recs:
                decl = LAYER_DECL.get(self.book_id, {}).get(
                    layer, ("annotation", "layers", "")
                )
                slices[layer] = LayerSlice(
                    self.book_id, layer, decl[1], decl[0], decl[2], recs
                )
        return slices

    def fingerprints(self):
        d = self._read_json(self.join_rel)
        if not d:
            return []
        rows = d.get("records") or []
        out = []
        for r in rows:
            if not isinstance(r, dict):
                continue
            iid = r.get("item_id")
            if not iid:
                continue
            title = r.get("source") or r.get("norm") or r.get("original") or ""
            out.append(
                {
                    "item_id": iid,
                    "volume": r.get("volume"),
                    "title": str(title)[:50],
                    "fingerprint_ref": iid,
                }
            )
        return out
