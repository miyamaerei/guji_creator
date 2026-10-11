"""adapters/layers_adapter.py —— 先进遗风（xyf）适配器

join 形态：{meta, fingerprints:[...], layers:{key:{records:[...],total}}}
- 层记录来自 layers[key].records
- 层内键：rel/event 有 'id'（REL-001 / XJF-E-001），其余（ent/appt/opn/trl）
  只用 item_id 键控（如 01-001）
- fingerprints 即本书的「条目指纹库」（item_id → 原文），items 只存指针
"""

from .base import BookAdapter, LayerSlice
from . import LAYER_DECL


class LayersAdapter(BookAdapter):
    def __init__(self, book_id, source_root, join_rel):
        super().__init__(book_id, source_root)
        self.join_rel = join_rel

    def _load_join(self):
        return self._read_json(self.join_rel) or {}

    def discover(self):
        d = self._load_join()
        layers = d.get("layers", {}) or {}
        out = {}
        for key, blob in layers.items():
            recs = blob.get("records", []) if isinstance(blob, dict) else []
            slices = []
            for idx, rec in enumerate(recs):
                if not isinstance(rec, dict):
                    continue
                local = rec.get("id")
                if local is None:
                    # 无显式层内 id（ent/appt/opn/trl 用 item_id 键控）：
                    # item_id 在同层内可能重复（同一条目提到多实体），
                    # 故追加层内序号保证 (book_id,layer_key,local_id) 唯一且稳定。
                    local = "%s#%d" % (rec.get("item_id") or "?", idx)
                slices.append(
                    {
                        "local_id": str(local),
                        "item_id": rec.get("item_id"),
                        "volume": rec.get("volume"),
                        "payload": rec,
                    }
                )
            decl = LAYER_DECL.get(self.book_id, {}).get(
                key, ("annotation", "layers", "")
            )
            out[key] = LayerSlice(
                self.book_id, key, decl[1], decl[0], decl[2], slices
            )
        return out

    def fingerprints(self):
        d = self._load_join()
        fps = d.get("fingerprints", []) or []
        return [f for f in fps if isinstance(f, dict) and f.get("item_id")]
