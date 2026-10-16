"""adapters/ppy_adapter.py —— 平平言（ppy）适配器

与 FqhAdapter 同构（_layers/<key>/<key>_NN.json 子目录 + _kg_join.json records 指针），
差异：产物目录与文件名均为**单数**（rule/struct/reg/opn + rule_01.json），无复数映射。
启用六层：ent / rule / struct / reg / opn / trl。
- ent：ent_id 全局唯一跨卷复用 → 按 ent_id 去重合并 surfaces。
- 其余各层：rule_id / struct_id / reg_id / opn_id / trl_id 全局唯一段位分配，local_id 直取记录 ID。
"""

import os

from .base import BookAdapter, LayerSlice
from . import LAYER_DECL


class PpyAdapter(BookAdapter):
    LAYER_DIR = "_layers"
    JOIN_REL = "_kg_join.json"

    ID_KEYS = {
        "rule": "rule_id",
        "struct": "struct_id",
        "reg": "reg_id",
        "opn": "opn_id",
        "trl": "trl_id",
    }

    def __init__(self, book_id, source_root, layer_keys, join_rel=JOIN_REL):
        super().__init__(book_id, source_root)
        self.layer_keys = list(layer_keys)
        self.join_rel = join_rel

    def _layer_files(self):
        """扫描 _layers/<单数key>/<单数key>_NN.json（平平言产物目录与文件名均为单数）。"""
        out = {}
        for key in self.layer_keys:
            d = os.path.join(self.source_root, self.LAYER_DIR, key)
            if not os.path.isdir(d):
                continue
            for f in sorted(os.listdir(d)):
                if not f.endswith(".json"):
                    continue
                base = f[:-5]
                parts = base.rsplit("_", 1)
                if len(parts) != 2:
                    continue
                prefix, vol = parts
                if prefix != key:
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
