"""adapters/xgf_adapter.py —— 新官轨范 适配器

join 形态：多份「归一_汇总」文件，各自装一种层：
- 实体：新官轨范_实体_主键表.json  → entities   (ent_id)
- 规则：新官轨范_规则_归一_汇总.json → rules      (rule_id)
- 流程：新官轨范_流程_ai/归一_汇总.json → processes (process_id)
- 事件：新官轨范_事件_ai/归一_汇总.json → events    (event_id, derived_from→item_id)
- 结构：新官轨范_结构_ai/归一_汇总.json → ledgers/times/docs/actors/frauds
  （ledger_id / time_id / doc_id / actor_id / fraud_id）

ID 全部全局唯一，VOLUME_PREFIX 置 False；事件可借 derived_from 反推 item_id，
其余层 item_id 留空（F3 再补）。条目锚点（items）取 _kg_join.json 的 entries。
"""

import os
import re

from .base import BookAdapter, LayerSlice, build_local_id, dedup_local_id
from . import LAYER_DECL

# (文件相对根目录, 容器内键, 主键字段, 归一 layer_key)
LAYER_FILES = [
    ("新官轨范_实体_主键表.json", "entities", "ent_id", "ent"),
    ("新官轨范_规则_归一_汇总.json", "rules", "rule_id", "rule"),
    ("新官轨范_流程_ai/归一_汇总.json", "processes", "process_id", "proc"),
    ("新官轨范_事件_ai/归一_汇总.json", "events", "event_id", "event"),
    ("新官轨范_结构_ai/归一_汇总.json", "ledgers", "ledger_id", "ledger"),
    ("新官轨范_结构_ai/归一_汇总.json", "times", "time_id", "time"),
    ("新官轨范_结构_ai/归一_汇总.json", "docs", "doc_id", "doc"),
    ("新官轨范_结构_ai/归一_汇总.json", "actors", "actor_id", "actor"),
    ("新官轨范_结构_ai/归一_汇总.json", "frauds", "fraud_id", "fraud"),
]

_VOL_RE = re.compile(r"^(\d{2})_")


class XgfAdapter(BookAdapter):
    VOLUME_PREFIX = False  # 新官 ID 全局唯一

    def discover(self):
        slices = {}
        for fname, container, idfield, layer in LAYER_FILES:
            p = os.path.join(self.source_root, fname)
            d = self._read_abspath(p)
            if not d:
                continue
            recs = []
            seen = {}
            for idx, rec in enumerate(d.get(container) or []):
                if not isinstance(rec, dict):
                    continue
                vid = rec.get(idfield) or rec.get("id")
                # item_id：优先 derived_from，其次 item_id
                df = rec.get("derived_from")
                if isinstance(df, list) and df:
                    item_id = df[0]
                elif isinstance(df, str):
                    item_id = df
                else:
                    item_id = rec.get("item_id")
                # volume：记录自带 → 否则从 source/first_source 的文件名解析章号
                rvol = rec.get("volume")
                if not rvol:
                    src = rec.get("source") or rec.get("first_source") or ""
                    m = _VOL_RE.match(os.path.basename(src))
                    if m:
                        rvol = m.group(1)
                # XGF 主键本身已是全局唯一，但 build_local_id 会按需加卷前缀
                cand = build_local_id(
                    dict(rec, **{"volume": rvol}),
                    layer,
                    d,
                    idx,
                    volume_prefix=self.VOLUME_PREFIX,
                )
                local = dedup_local_id(cand, seen)
                recs.append(
                    {
                        "local_id": str(local),
                        "item_id": item_id,
                        "volume": rvol,
                        "payload": rec,
                    }
                )
            if recs:
                decl = LAYER_DECL.get(self.book_id, {}).get(
                    layer, ("annotation", "summary", "")
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
        entries = d.get("entries") or []
        out = []
        for e in entries:
            if not isinstance(e, dict):
                continue
            iid = e.get("item_id")
            if not iid:
                continue
            vol = iid.split("-")[0] if "-" in iid else None
            out.append(
                {
                    "item_id": iid,
                    "volume": vol,
                    "title": str(e.get("source") or iid)[:50],
                    "fingerprint_ref": iid,
                }
            )
        return out
