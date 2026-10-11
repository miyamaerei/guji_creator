"""adapters/norm_layer_adapter.py —— 蘧编 适配器

join 形态：归一_<layer>.json（每层一个汇总文件，覆盖全部 20 卷）
- 文件 wrapper：{layer, count, records:[...]}
- records 每条 = 完整层记录（id=ENT-501 / item_id / volume / normalized ...）
- ID 全局唯一（单文件跨卷），VOLUME_PREFIX 置 False
- 层 key 由文件名复数映射到归一单数：ents→ent, evts→event, ...

条目锚点（items）从 _kg_join.json 的 records 字典取（71 条）。
"""

import os

from .base import BookAdapter, LayerSlice, build_local_id, dedup_local_id
from . import LAYER_DECL

# 文件名复数 → 联邦归一层 key
PLURAL_TO_KEY = {
    "ents": "ent",
    "appts": "appt",
    "evts": "event",
    "rels": "rel",
    "lits": "lit",
    "mems": "mem",
    "chrs": "chr",
    "trls": "trl",
}


class NormLayerAdapter(BookAdapter):
    VOLUME_PREFIX = False  # 蘧编 ID 全局唯一

    def discover(self):
        slices = {}
        for fn in sorted(os.listdir(self.source_root)):
            if not fn.startswith("归一_") or not fn.endswith(".json"):
                continue
            plural = fn[len("归一_") : -5]
            layer = PLURAL_TO_KEY.get(plural)
            if not layer:
                continue
            d = self._read_abspath(os.path.join(self.source_root, fn))
            if not d:
                continue
            recs = []
            seen = {}
            for idx, rec in enumerate(d.get("records") or []):
                if not isinstance(rec, dict):
                    continue
                cand = build_local_id(
                    rec, layer, d, idx, volume_prefix=self.VOLUME_PREFIX
                )
                local = dedup_local_id(cand, seen)
                recs.append(
                    {
                        "local_id": str(local),
                        "item_id": rec.get("item_id"),
                        "volume": rec.get("volume"),
                        "payload": rec,
                    }
                )
            if recs:
                decl = LAYER_DECL.get(self.book_id, {}).get(
                    layer, ("annotation", "norm", "")
                )
                slices[layer] = LayerSlice(
                    self.book_id, layer, decl[1], decl[0], decl[2], recs
                )
        return slices

    def fingerprints(self):
        p = os.path.join(self.source_root, "_kg_join.json")
        d = self._read_abspath(p)
        if not d:
            return []
        recs = d.get("records") or {}
        out = []
        for iid, rec in recs.items():
            if not isinstance(rec, dict):
                continue
            out.append(
                {
                    "item_id": rec.get("item_id") or iid,
                    "volume": rec.get("volume"),
                    "title": str(rec.get("title") or iid)[:50],
                    "fingerprint_ref": iid,
                }
            )
        return out
