"""adapters/zgz_adapter.py —— 《明史·职官志》（zgz）适配器

层产物形态（E:\\git\\ToolBox\\guji\\mingshi\\mingshi-zhiguanzhi\\_layers\\）：
- 目录名与多卷文件名均为**复数**（ents/rules/procs/appts/tmes/structs），
  归一 layer key 为单数（ent/rule/proc/appt/tme/struct/org）。
- 多卷层（卷号在文件名**后**）：_layers/{dir}/{dir}_NN.json，wrapper={volume,records}
    ents（五卷）/ rules / procs / appts / tmes
- structs 目录（special）：
    officials.json（n=1246，OFF-001..，双 ID：official_id 与 id 均 OFF-xxx，
      payload 含 salary/peers/subordinates/org_id，org_id 唯一 303 个）→ struct 层
    structs_00..05.json（RANK-001 俸禄表 + ORG-501 机构树，children 嵌套
      子节点 id 如 ORG-501#1 含 #n 后缀）→ org 层 flatten_tree 递归展开

ID 命名空间（关键差异）：
- **ents 的 id 会跨卷复用（3261 条仅 2154 唯一）且卷内亦复用**（ENT-0013 卷内
  9 处"尚书"）→ local_id 必须「卷前缀 + 卷内序号」：01:ENT-0013、01:ENT-0013#1...
- rules（ZG-R-）/ procs（ZG-P-）/ appts（ZG-APPT-）/ tmes（ZG-TME-）跨卷全局唯一，
  local_id 直取 id（仍走 dedup_local_id 兜底卷内重复）。
- structs（OFF-xxx 全局唯一）直取 id。
- org 层：flatten_tree 展开嵌套 children，local_id 保留 #n 后缀（ORG-501#1），
  payload 保留节点原 JSON（含 parent/children 嵌套，树形查询走 payload 递归）。
- zgz appts 有 person/office/**institution** 三字段 → edge 解析用默认
  EDGE_SPEC（object=institution），无需 override。

fingerprints：_kg_join.json 是 dict.records 形态（n=317，source="原文"），标准读取；
title 用 source 兜底（原文）。

零第三方依赖，幂等（装载由 load.py 的 wipe+INSERT 保证，本 adapter 无副作用）。
"""

import os

from .base import BookAdapter, LayerSlice, dedup_local_id
from . import LAYER_DECL


def _norm_item_id(v):
    """item_id 归一：可能为 str / list（多条目引用）→ 存字符串主值。"""
    if isinstance(v, list):
        return v[0] if v and isinstance(v[0], str) else None
    return v


# 归一 key → 源目录名（复数）
_DIR_MAP = {
    "ent": "ents",
    "rule": "rules",
    "proc": "procs",
    "appt": "appts",
    "tme": "tmes",
    "struct": "structs",
    "org": "structs",
}

DENY = {
    "ent_alias",
    "ent_normalized",
    "ent_index",
    "ent_keys",
    "ent_normalized_inventory",
}

# structs 目录内机构树/俸禄表文件：structs_00..05.json
_ORG_FILES = [f"structs_{i:02d}.json" for i in range(6)]


def normalize_local_id(rec, idx, wrapper):
    """org 节点 local_id 归一：直取 id（保留 #n 后缀），无 id 用 item_id#idx 兜底。"""
    vid = rec.get("id")
    if vid:
        return str(vid)
    iid = _norm_item_id(rec.get("item_id"))
    if iid:
        return f"{iid}#{idx}"
    vol = (wrapper or {}).get("volume")
    return f"{vol or 'x'}#{idx}"


def flatten_tree(top_records):
    """递归展开嵌套 children → 独立节点列表（每条一条 record）。

    - 每个节点（含最深层机构，如 structs_04 里 ORG-xxx#n）都成为独立记录，
      local_id 保留 #n 后缀，不再埋没在父 JSON 的 children 里当孤儿；
    - payload 保留该节点**原 JSON 完整字段**（含 children 嵌套、parent 名），
      父子关系由 payload.parent（名）与 id 前缀（ORG-501 → ORG-501#1）天然保存，
      树形查询在 L3 用 WITH RECURSIVE / payload 递归，不加新表 —— 正好兑现
      方案文档"树形不加表、最深层可寻址"的承诺。
    """
    out = []
    seen = {}
    stack = [(top_idx, rec, None) for top_idx, rec in enumerate(top_records or [])]
    while stack:
        idx, rec, parent_id = stack.pop(0)
        if not isinstance(rec, dict):
            continue
        item_id = _norm_item_id(rec.get("item_id"))
        vol = rec.get("volume") or rec.get("_vol")
        local = normalize_local_id(rec, idx, {"volume": vol})
        local = dedup_local_id(local, seen)
        out.append(
            {
                "local_id": local,
                "item_id": item_id,
                "volume": vol,
                "payload": rec,
            }
        )
        kids = rec.get("children")
        if isinstance(kids, list) and kids:
            for k in kids:
                if isinstance(k, dict):
                    stack.append((idx, k, rec.get("id")))
    return out


class ZgzAdapter(BookAdapter):
    LAYER_DIR = "_layers"
    JOIN_REL = "_kg_join.json"

    def __init__(self, book_id, source_root, layer_keys, join_rel=JOIN_REL):
        super().__init__(book_id, source_root)
        self.layer_keys = list(layer_keys)
        self.join_rel = join_rel

    def _layer_files(self):
        """扫描 _layers/{dir}/（复数目录名），返回 key -> [(tag, abspath)]。

        多卷层匹配 {dir}_NN.json（卷号在后，如 ents_01.json）；
        structs 目录 special：officials.json → struct 层；structs_NN.json → org 层。
        """
        out = {}
        for key in self.layer_keys:
            dname = _DIR_MAP[key] if key in _DIR_MAP else key
            d = os.path.join(self.source_root, self.LAYER_DIR, dname)
            if not os.path.isdir(d):
                continue
            if key == "struct":
                p = os.path.join(d, "officials.json")
                if os.path.exists(p):
                    out[key] = [("single", p)]
                continue
            if key == "org":
                files = []
                for f in sorted(os.listdir(d)):
                    if f in _ORG_FILES:
                        files.append(("org", os.path.join(d, f)))
                if files:
                    out[key] = files
                continue
            files = []
            for f in sorted(os.listdir(d)):
                if not f.endswith(".json") or f.startswith("_"):
                    continue
                base = f[:-5]
                if "_" in base:
                    head, _, tail = base.partition("_")
                    if head == dname and tail.isdigit():  # ents_01
                        files.append(("vol", os.path.join(d, f)))
            if files:
                out[key] = files
        return out

    def discover(self):
        slices = {}
        for layer, files in self._layer_files().items():
            recs = []
            if layer == "org":
                top = []
                for tag, path in files:
                    d = self._read_abspath(path)
                    if not d:
                        continue
                    vol = d.get("volume")
                    for rec in d.get("records") or []:
                        if not isinstance(rec, dict):
                            continue
                        rec.setdefault("_vol", vol)
                        top.append(rec)
                recs.extend(flatten_tree(top))
            else:
                seen = {}
                for tag, path in files:
                    d = self._read_abspath(path)
                    if not d:
                        continue
                    vol = d.get("volume")
                    for rec in d.get("records") or []:
                        if not isinstance(rec, dict):
                            continue
                        if layer == "ent":
                            # 卷前缀 + 卷内序号去重：01:ENT-0013、01:ENT-0013#1...
                            cand = (
                                f"{vol}:{rec.get('id')}"
                                if vol
                                else (rec.get("id") or (rec.get("item_id") or "?"))
                            )
                            local = dedup_local_id(cand, seen)
                        else:
                            local = dedup_local_id(
                                rec.get("id")
                                or (_norm_item_id(rec.get("item_id")) or "?"),
                                seen,
                            )
                        recs.append(
                            {
                                "local_id": local,
                                "item_id": _norm_item_id(rec.get("item_id")),
                                "volume": rec.get("volume") or vol,
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
        rows = d.get("records") or []  # zgz 是 dict.records 形态（317 条）
        out = []
        for r in rows:
            if not isinstance(r, dict):
                continue
            iid = _norm_item_id(r.get("item_id"))
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
