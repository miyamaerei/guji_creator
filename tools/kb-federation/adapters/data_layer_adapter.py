"""adapters/data_layer_adapter.py —— 水东日记 适配器

join 形态：data/<layer>/*.json（每层一个目录，每卷一个文件）
- 文件 wrapper：{volume, annotations:[...]}
- 每条 annotation = 完整层记录（id=ENT-001 / item_id / volume / normalized ...）
- 顶层还有 data/join/_kg_join.json（条目锚点，用于 items 表）

注意：SDR 的 ID 是全局唯一（不按卷重排），但加卷前缀无害，保持与其他
书一致；VOLUME_PREFIX 仍置 True（同一卷内 id 是主键，前缀后整体仍唯一）。
"""

import os

from .base import BookAdapter, LayerSlice, build_local_id, dedup_local_id
from . import LAYER_DECL


class DataLayerAdapter(BookAdapter):
    LAYER_DIR = "data"
    VOLUME_PREFIX = True

    def discover(self):
        slices = {}
        d = os.path.join(self.source_root, self.LAYER_DIR)
        if not os.path.isdir(d):
            return slices
        for layer in sorted(os.listdir(d)):
            ld = os.path.join(d, layer)
            if not os.path.isdir(ld):
                continue
            recs = []
            seen = {}
            for f in sorted(os.listdir(ld)):
                if not f.endswith(".json"):
                    continue
                fp = os.path.join(ld, f)
                dd = self._read_abspath(fp)
                if not isinstance(dd, dict):  # 跳过 ent_keys 等非 wrapper 文件
                    continue
                wvol = dd.get("volume")
                container = dd.get("annotations") or dd.get("records") or []
                for idx, rec in enumerate(container):
                    if not isinstance(rec, dict):
                        continue
                    cand = build_local_id(
                        rec, layer, dd, idx, volume_prefix=self.VOLUME_PREFIX
                    )
                    local = dedup_local_id(cand, seen)
                    recs.append(
                        {
                            "local_id": str(local),
                            "item_id": rec.get("item_id"),
                            "volume": rec.get("volume") or wvol,
                            "payload": rec,
                        }
                    )
            if recs:
                decl = LAYER_DECL.get(self.book_id, {}).get(
                    layer, ("annotation", "data", "")
                )
                slices[layer] = LayerSlice(
                    self.book_id, layer, decl[1], decl[0], decl[2], recs
                )
        return slices

    def fingerprints(self):
        p = os.path.join(self.source_root, "data/join/_kg_join.json")
        d = self._read_abspath(p)
        if not d:
            return []
        rows = d if isinstance(d, list) else (d.get("rows") or [])
        out = []
        for r in rows:
            if not isinstance(r, dict):
                continue
            iid = r.get("item_id")
            if not iid:
                continue
            title = r.get("source") or f"{r.get('volume')}/{iid}"
            out.append(
                {
                    "item_id": iid,
                    "volume": r.get("volume"),
                    "title": str(title)[:50],
                    "fingerprint_ref": iid,
                }
            )
        return out
