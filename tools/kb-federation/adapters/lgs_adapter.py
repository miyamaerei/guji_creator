"""adapters/lgs_adapter.py —— 吕公实政录（lgs）适配器

层产物形态：_layers/<key>_NN.json（每卷每层一个文件），wrapper = {records:[...]}
- ent：ent_id 全局唯一（ENT-0001..0573）且跨卷复用（同一实体多卷出现）——
  按 ent_id 跨卷去重（保留首条，合并各卷 text 变体进 payload.surfaces），
  local_id = ent_id（无需卷前缀，ID 全局唯一不撞号）。
- rule / struct / trl：rule_id / struct_id / trl_id 全局唯一段位分配（RULE- / ACT- 等），
  local_id 直取记录 ID。
- fingerprints：工程根 _kg_join.json（{"records":[...]}），items 只存指针。

实现要点：与 VolLayerAdapter 同源但解决"ID 全局唯一跨卷复用"的去重问题，
不靠运行时试探；kind/id_prefix 来自 __init__.py 的 LAYER_DECL 登记。
"""

import os
import json

from .base import BookAdapter, LayerSlice
from . import LAYER_DECL

DENY = {
    "ent_alias",
    "ent_normalized",
    "ent_index",
    "ent_keys",
    "ent_normalized_inventory",
}


class LgsAdapter(BookAdapter):
    LAYER_DIR = "_layers"
    JOIN_REL = "_kg_join.json"

    def __init__(self, book_id, source_root, layer_keys, join_rel=JOIN_REL):
        super().__init__(book_id, source_root)
        self.layer_keys = list(layer_keys)
        self.join_rel = join_rel

    def _layer_files(self):
        """扫描 _layers/<key>/<key>_NN.json（每层一个子目录，卷文件在子目录内）。"""
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
            seen_ent = {}  # ent_id -> 首条在 recs 的 index
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
                            # 同一实体跨卷再标注：合并 text 变体（去重），不新增记录
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
                    elif layer == "rule":
                        local = rec.get("rule_id") or (rec.get("item_id") or "?")
                    elif layer == "trl":
                        local = rec.get("trl_id") or (rec.get("item_id") or "?")
                    else:  # struct
                        local = rec.get("struct_id") or (rec.get("item_id") or "?")
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
