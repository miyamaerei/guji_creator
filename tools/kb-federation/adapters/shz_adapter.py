"""adapters/shz_adapter.py —— 《明史·食货志》（shz）适配器

层产物形态（E:\\git\\ToolBox\\guji\\mingshi\\mingshi-shihuozhi\\_layers\\）：
- 目录名与文件名均为**复数**（ents/rules/procs/appts/opns/regs/tmes/structs），
  归一 layer key 为单数（ent/rule/proc/appt/opn/reg/tme/struct）。
- 多卷层（卷号在文件名**前**）：_layers/{dir}/NN_{dir}.json，wrapper={volume,records}
    ents（六卷）/ procs（六卷）/ rules（六卷）
- 单文件层：_layers/{dir}/{dir}.json，wrapper={records}（无 volume）
    appts（n=244，APPT-01001，person+office 两字段**无 institution**）
    opns（n=66，OPN-01001）/ regs（n=122，REG-01001）/ tmes（n=227，TME-01001）
- structs：_layers/structs/structs.json 是 **7 维 dict**（非 records 包装），
    QUAN 271 / INST 120 / EVO 172 / FISC 107 / HK 14 / LAND 17 / TRANS 11 = 712，
    各维记录自备 id（QUAN-01001 / INST-01001 / ...），须摊平后逐条装载。

ID 命名空间：所有层 id 全局唯一（ENT-01001.. 含卷号段），local_id 直取 id；
shz appts 无 institution 字段，edge 解析须 per-book override object=office
（见 transform.py EDGE_SPEC_BOOK，本 adapter 只负责把 appts 原样载入 records）。

fingerprints：_kg_join.json 是 **list 形态**（254 条），元素 {item_id,volume,layers,layer_count}，
无 source/norm/original → title 用 volume 兜底。

零第三方依赖，幂等（装载由 load.py 的 wipe+INSERT 保证，本 adapter 无副作用）。
"""

import os

from .base import BookAdapter, LayerSlice, dedup_local_id
from . import LAYER_DECL


def _norm_item_id(v):
    """item_id 归一：可能为 str / list（多条目引用，如 regs）→ 存字符串主值。"""
    if isinstance(v, list):
        return v[0] if v and isinstance(v[0], str) else (str(v[0]) if v else None)
    return v


# 归一 key（单数，LAYER_DECL 用）→ 源目录/文件名（复数）
_DIR_MAP = {
    "ent": "ents",
    "rule": "rules",
    "proc": "procs",
    "appt": "appts",
    "tme": "tmes",
    "opn": "opns",
    "reg": "regs",
    "struct": "structs",
}

DENY = {
    "ent_alias",
    "ent_normalized",
    "ent_index",
    "ent_keys",
    "ent_normalized_inventory",
}


class ShzAdapter(BookAdapter):
    LAYER_DIR = "_layers"
    JOIN_REL = "_kg_join.json"

    def __init__(self, book_id, source_root, layer_keys, join_rel=JOIN_REL):
        super().__init__(book_id, source_root)
        self.layer_keys = list(layer_keys)
        self.join_rel = join_rel

    def _layer_files(self):
        """扫描 _layers/{dir}/（复数目录名），返回 key -> [(tag, abspath)]。

        多卷层匹配 NN_{dir}.json（卷号在前，如 01_ents.json）；
        单文件层匹配 {dir}.json（如 appts.json）；
        structs 特殊处理（dict 摊平），其余（_ 前缀等）跳过。
        """
        out = {}
        for key in self.layer_keys:
            dname = _DIR_MAP[key] if key in _DIR_MAP else key
            d = os.path.join(self.source_root, self.LAYER_DIR, dname)
            if not os.path.isdir(d):
                continue
            files = []
            for f in sorted(os.listdir(d)):
                if not f.endswith(".json") or f.startswith("_"):
                    continue
                base = f[:-5]
                if "_" in base:
                    head, _, tail = base.partition("_")
                    if head.isdigit() and tail == dname:  # 01_ents
                        files.append(("vol", os.path.join(d, f)))
                elif base == dname:  # 单文件层：appts/opns/regs/tmes
                    files.append(("single", os.path.join(d, f)))
            if files:
                out[key] = files
        return out

    def _structs_flat(self):
        """structs.json 是 7 维 dict（{QUAN:[...], INST:[...], ...}），摊平为统一 records 列表。"""
        d = os.path.join(self.source_root, self.LAYER_DIR, "structs", "structs.json")
        if not os.path.exists(d):
            return []
        data = self._read_abspath(d)
        if not isinstance(data, dict):
            return []
        out = []
        seen = {}
        for dim, recs in data.items():
            if not isinstance(recs, list):
                continue
            for rec in recs:
                if not isinstance(rec, dict):
                    continue
                local = rec.get("id")
                if not local:
                    continue
                item_id = _norm_item_id(rec.get("item_id"))
                vol = None
                if isinstance(item_id, str) and "-" in item_id:
                    vol = item_id.split("-", 1)[0]
                out.append(
                    {
                        "local_id": dedup_local_id(local, seen),
                        "item_id": item_id,
                        "volume": vol,
                        "payload": rec,
                    }
                )
        return out

    def discover(self):
        slices = {}
        for layer, files in self._layer_files().items():
            if layer == "struct":
                recs = self._structs_flat()
            else:
                recs = []
                seen = {}
                for tag, path in files:
                    d = self._read_abspath(path)
                    if not d:
                        continue
                    for rec in d.get("records") or []:
                        if not isinstance(rec, dict):
                            continue
                        local = rec.get("id") or (
                            _norm_item_id(rec.get("item_id")) or "?"
                        )
                        item_id = _norm_item_id(rec.get("item_id"))
                        vol = rec.get("volume") or d.get("volume")
                        if tag == "single":  # 单文件层无 volume
                            vol = None
                        recs.append(
                            {
                                "local_id": dedup_local_id(local, seen),
                                "item_id": item_id,
                                "volume": vol,
                                "payload": rec,
                            }
                        )
            if recs and layer in self.layer_keys:
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
        # shz kg_join 是 list 形态（254 条），无 source/norm/original
        rows = d if isinstance(d, list) else (d.get("records") or [])
        out = []
        for r in rows:
            if not isinstance(r, dict):
                continue
            iid = _norm_item_id(r.get("item_id"))
            if not iid:
                continue
            title = (
                r.get("source")
                or r.get("norm")
                or r.get("original")
                or r.get("volume")
                or ""
            )
            out.append(
                {
                    "item_id": iid,
                    "volume": r.get("volume"),
                    "title": str(title)[:50],
                    "fingerprint_ref": iid,
                }
            )
        return out
