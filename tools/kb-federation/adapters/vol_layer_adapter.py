"""adapters/vol_layer_adapter.py —— 客座赘语 / 五杂俎 适配器

join 形态：_layers/<layer>_<vol>.json（每卷每层一个文件）
- 文件 wrapper：{layer, volume, name, id_prefix, id_field, count, records:[...]}
  （WZZ 无 id_prefix/id_field，ID 键为 <layer>_id）
- records 内每条 = 完整层记录（ent_id / item_id / volume / text / normalized ...）
- ID 按卷重排（vol02 又从 ENT-0001 起），故 local_id 加卷前缀隔离

实现要点：LAYER_DECL 显式登记层 key↔形态↔前缀，不靠运行时试探。
"""

import os

from .base import BookAdapter, LayerSlice, build_local_id, dedup_local_id
from . import LAYER_DECL


class VolLayerAdapter(BookAdapter):
    LAYER_DIR = "_layers"
    # 非层产物（主键表 / 别名表 / 索引 / 库存清单）一律跳过
    DENY = {
        "ent_alias",
        "ent_normalized",
        "ent_index",
        "ent_keys",
        "ent_normalized_inventory",
    }
    VOLUME_PREFIX = True  # KZZ/WZZ ID 按卷重排，必须加卷前缀

    def __init__(self, book_id, source_root, layer_keys):
        super().__init__(book_id, source_root)
        self.layer_keys = list(layer_keys)  # 该书实际要装的层（白名单）

    def _layer_files(self):
        d = os.path.join(self.source_root, self.LAYER_DIR)
        out = {}
        if not os.path.isdir(d):
            return out
        for f in sorted(os.listdir(d)):
            if not f.endswith(".json") or f.startswith("_kg_join"):
                continue
            base = f[:-5]
            parts = base.rsplit("_", 1)
            if len(parts) != 2:
                continue
            prefix, vol = parts
            if prefix in self.DENY:
                continue
            if prefix not in self.layer_keys:
                continue
            out.setdefault(prefix, []).append((vol, os.path.join(d, f)))
        return out

    def discover(self):
        slices = {}
        for layer, files in self._layer_files().items():
            recs = []
            seen = {}
            for vol, path in files:
                d = self._read_abspath(path)
                if not d:
                    continue
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
        p = os.path.join(self.source_root, self.LAYER_DIR, "_kg_join.json")
        d = self._read_abspath(p)
        if not d:
            return []
        rows = d.get("rows") or []
        out = []
        for r in rows:
            if not isinstance(r, dict):
                continue
            iid = r.get("item_id")
            if not iid:
                continue
            title = r.get("norm") or r.get("original") or r.get("volume_name") or ""
            out.append(
                {
                    "item_id": iid,
                    "volume": r.get("volume"),
                    "title": str(title)[:50],
                    "fingerprint_ref": iid,
                }
            )
        return out
