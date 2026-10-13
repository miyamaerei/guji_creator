"""adapters/__init__.py —— 注册表 + 每书 catalog 声明

BOOK_ROOTS：六书相对仓库根的路径（撞号扫描用，不依赖 adapter 类）。
BOOK_REGISTRY：现已实现 6 本书的 adapter（F2 补全其余 5 本）。
LAYER_DECL：层 key ↔ 形态 ↔ 前缀 ↔ kind 显式登记。取代运行时试探，
            正是契约线 C4/C5 在联邦线侧的兑现 —— 新书/新层只在此加几行，
            loader 逻辑不改。

注意：LAYER_DECL 等数据定义必须在 import 各 adapter 类之前完成，
否则 adapter 里的 `from . import LAYER_DECL` 会因尚未定义而环形失败。
"""

import os

from .base import BookAdapter, LayerSlice

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))  # guji/

# 全部六书根目录（撞号扫描用）
BOOK_ROOTS = {
    "kzz": "kezuozhuiyu-kb",
    "wzz": "wuzazu-kb",
    "sdr": "shuidongriji-kb",
    "xgf": "xinguanguifan-kb",
    "qb": "qubian_kb",
    "xyf": "xianjinyifeng-kb/05-xianjinyifeng-knowledge",
    "lgs": "shizhenglu-kb",
    "xzl": "xuezhenglu-kb",
    "ysz": "yuanshuzaji-kb",
    "fqh": "fuhuiquanshu-kb",
    "ppy": "pingpingyan-kb",
}
BOOK_NAMES = {
    "kzz": "客座赘语",
    "wzz": "五杂俎",
    "sdr": "水东日记",
    "xgf": "新官轨范",
    "qb": "蘧编",
    "xyf": "先进遗风",
    "lgs": "吕公实政录",
    "xzl": "政学录",
    "ysz": "宛署杂记",
    "fqh": "福惠全书",
    "ppy": "平平言",
}

# 每书实际要装的层（白名单；同时是 LAYER_DECL 的 key 全集）
BOOK_LAYERS = {
    "kzz": ["ent", "event", "cit", "obj", "cus", "ming", "geo", "appt",
            "nam", "lit", "opn", "rel", "trl"],
    "wzz": ["ent", "event", "cit", "cus", "appt", "nam", "obj", "opn",
            "ming", "rel", "trl"],
    "sdr": ["ent", "appt", "event", "reg", "lit", "rel", "nam", "trl"],
    "xgf": ["ent", "rule", "proc", "event", "ledger", "time", "doc",
            "actor", "fraud"],
    "qb": ["ent", "appt", "event", "rel", "lit", "mem", "chr", "trl"],
    "xyf": ["ent", "appt", "rel", "event", "opn", "trl"],
    "lgs": ["ent", "rule", "struct"],
    "xzl": ["ent", "rule", "struct", "reg", "evt"],
    "ysz": ["ent", "appt", "evt", "lit", "reg", "nam", "opn", "cus", "geo"],
    "fqh": ["ent", "rule", "struct", "reg", "opn", "proc", "doc", "rel"],
    "ppy": ["ent", "rule", "struct", "reg", "opn"],
}

# 层声明：层 key -> (kind, container_kind, id_prefix)
#   kind: node | edge | annotation | profile
#   container_kind: 来源形态（layers/data/norm/summary/fingerprints）
#   id_prefix: 本书实际 ID 前缀；空串表示按 item_id 键控
LAYER_DECL = {
    # 客座赘语：13 层
    "kzz": {
        "ent": ("node", "layers", "ENT-"), "event": ("edge", "layers", "EVENT-"),
        "cit": ("annotation", "layers", "CIT-"), "obj": ("annotation", "layers", "OBJ-"),
        "cus": ("annotation", "layers", "CUS-"), "ming": ("annotation", "layers", "MING-"),
        "geo": ("node", "layers", "GEO-"), "appt": ("edge", "layers", "APPT-"),
        "nam": ("annotation", "layers", "NAM-"), "lit": ("annotation", "layers", "LIT-"),
        "opn": ("annotation", "layers", "OPN-"), "rel": ("edge", "layers", "REL-"),
        "trl": ("annotation", "layers", "TRL-"),
    },
    # 五杂俎：11 层（无 geo）
    "wzz": {
        "ent": ("node", "layers", "ENT-"), "event": ("edge", "layers", "EVENT-"),
        "cit": ("annotation", "layers", "CIT-"), "cus": ("annotation", "layers", "CUS-"),
        "appt": ("edge", "layers", "APPT-"), "nam": ("annotation", "layers", "NAM-"),
        "obj": ("annotation", "layers", "OBJ-"), "opn": ("annotation", "layers", "OPN-"),
        "ming": ("annotation", "layers", "MING-"), "rel": ("edge", "layers", "REL-"),
        "trl": ("annotation", "layers", "TRL-"),
    },
    # 水东日记：8 层
    "sdr": {
        "ent": ("node", "data", "ENT-"), "appt": ("edge", "data", "APPT-"),
        "event": ("edge", "data", "EVENT-"), "reg": ("annotation", "data", "REG-"),
        "lit": ("annotation", "data", "LIT-"), "rel": ("edge", "data", "REL-"),
        "nam": ("annotation", "data", "NAM-"), "trl": ("annotation", "data", "TRL-"),
    },
    # 新官轨范：9 层（结构拆 5 子层）
    "xgf": {
        "ent": ("node", "summary", "ENT-"), "rule": ("annotation", "summary", "XGF-R-"),
        "proc": ("annotation", "summary", "XGF-P-"), "event": ("edge", "summary", "XGF-E-"),
        "ledger": ("annotation", "summary", "LED-"), "time": ("annotation", "summary", "TME-"),
        "doc": ("annotation", "summary", "DOC-"), "actor": ("annotation", "summary", "ACT-"),
        "fraud": ("annotation", "summary", "FRD-"),
    },
    # 蘧编：8 层
    "qb": {
        "ent": ("node", "norm", "ENT-"), "appt": ("edge", "norm", "APPT-"),
        "event": ("edge", "norm", "EVENT-"), "rel": ("edge", "norm", "REL-"),
        "lit": ("annotation", "norm", "LIT-"), "mem": ("annotation", "norm", "MEM-"),
        "chr": ("edge", "norm", "CHR-"), "trl": ("annotation", "norm", "TRL-"),
    },
    # 先进遗风：6 层
    "xyf": {
        "ent": ("node", "layers", ""), "appt": ("edge", "layers", ""),
        "rel": ("edge", "layers", "REL-"), "event": ("edge", "layers", "XJF-E-"),
        "opn": ("annotation", "layers", ""), "trl": ("annotation", "layers", ""),
    },
    # 吕公实政录：3 层（struct 内 ACT-/FRD-/LGR-/TME- 四维前缀混用，登记 ACT- 为代表）
    "lgs": {
        "ent": ("node", "layers", "ENT-"), "rule": ("annotation", "layers", "RULE-"),
        "struct": ("annotation", "layers", "ACT-"),
    },
    # 政学录：5 层（reg REG-/evt EVT-）
    "xzl": {
        "ent": ("node", "layers", "ENT-"), "rule": ("annotation", "layers", "RULE-"),
        "struct": ("annotation", "layers", "ACT-"),
        "reg": ("annotation", "layers", "REG-"), "evt": ("edge", "layers", "EVT-"),
    },
    # 宛署杂记：9 层（appt APPT-/evt EVT-/lit LIT-/reg REG-/nam NAM-/opn OPN-/cus CUS-/geo GEO-）
    "ysz": {
        "ent": ("node", "layers", "ENT-"), "appt": ("edge", "layers", "APPT-"),
        "evt": ("edge", "layers", "EVT-"), "lit": ("annotation", "layers", "LIT-"),
        "reg": ("annotation", "layers", "REG-"), "nam": ("annotation", "layers", "NAM-"),
        "opn": ("annotation", "layers", "OPN-"), "cus": ("annotation", "layers", "CUS-"),
        "geo": ("node", "layers", "GEO-"),
    },
    # 福惠全书：8 层（rule RULE-/struct STRUCT-（四维前缀混用，登记 ACT- 为代表）
    # /reg REG-/opn OPN-/proc PROC-/doc DOC-/rel REL-）
    "fqh": {
        "ent": ("node", "layers", "ENT-"), "rule": ("annotation", "layers", "RULE-"),
        "struct": ("annotation", "layers", "ACT-"),
        "reg": ("annotation", "layers", "REG-"), "opn": ("annotation", "layers", "OPN-"),
        "proc": ("annotation", "layers", "PROC-"), "doc": ("annotation", "layers", "DOC-"),
        "rel": ("edge", "layers", "REL-"),
    },
    # 平平言：5 层（rule RULE-/struct ACT-（四维前缀混用，登记 ACT- 为代表）
    # /reg REG-/opn OPN-）
    "ppy": {
        "ent": ("node", "layers", "ENT-"), "rule": ("annotation", "layers", "RULE-"),
        "struct": ("annotation", "layers", "ACT-"),
        "reg": ("annotation", "layers", "REG-"), "opn": ("annotation", "layers", "OPN-"),
    },
}

# adapter 注册（F2 已补全全部 6 本；lgs 为第 7 本契约线交付后并入）
from .vol_layer_adapter import VolLayerAdapter  # noqa: E402
from .data_layer_adapter import DataLayerAdapter  # noqa: E402
from .norm_layer_adapter import NormLayerAdapter  # noqa: E402
from .xgf_adapter import XgfAdapter  # noqa: E402
from .layers_adapter import LayersAdapter  # noqa: E402
from .lgs_adapter import LgsAdapter  # noqa: E402
from .xzl_adapter import XzlAdapter  # noqa: E402
from .ysz_adapter import YszAdapter  # noqa: E402
from .fqh_adapter import FqhAdapter  # noqa: E402
from .ppy_adapter import PpyAdapter  # noqa: E402

BOOK_REGISTRY = {
    "kzz": {"class": VolLayerAdapter, "root": BOOK_ROOTS["kzz"],
            "layer_keys": BOOK_LAYERS["kzz"]},
    "wzz": {"class": VolLayerAdapter, "root": BOOK_ROOTS["wzz"],
            "layer_keys": BOOK_LAYERS["wzz"]},
    "sdr": {"class": DataLayerAdapter, "root": BOOK_ROOTS["sdr"]},
    "xgf": {"class": XgfAdapter, "root": BOOK_ROOTS["xgf"]},
    "qb": {"class": NormLayerAdapter, "root": BOOK_ROOTS["qb"]},
    "xyf": {"class": LayersAdapter, "root": BOOK_ROOTS["xyf"],
            "join": "data/_layers/kg_join.json"},
    "lgs": {"class": LgsAdapter, "root": BOOK_ROOTS["lgs"],
            "layer_keys": BOOK_LAYERS["lgs"], "join": "_kg_join.json"},
    "xzl": {"class": XzlAdapter, "root": BOOK_ROOTS["xzl"],
            "layer_keys": BOOK_LAYERS["xzl"], "join": "_kg_join.json"},
    "ysz": {"class": YszAdapter, "root": BOOK_ROOTS["ysz"],
            "layer_keys": BOOK_LAYERS["ysz"], "join": "_kg_join.json"},
    "fqh": {"class": FqhAdapter, "root": BOOK_ROOTS["fqh"],
            "layer_keys": BOOK_LAYERS["fqh"], "join": "_kg_join.json"},
    "ppy": {"class": PpyAdapter, "root": BOOK_ROOTS["ppy"],
            "layer_keys": BOOK_LAYERS["ppy"], "join": "_kg_join.json"},
}


def book_source_root(book_id):
    return os.path.join(REPO_ROOT, BOOK_REGISTRY[book_id]["root"])


def make_adapter(book_id):
    reg = BOOK_REGISTRY[book_id]
    root = os.path.join(REPO_ROOT, reg["root"])
    cls = reg["class"]
    if cls is VolLayerAdapter:
        return cls(book_id, root, reg["layer_keys"])
    if cls is LayersAdapter:
        return cls(book_id, root, reg["join"])
    if cls in (LgsAdapter, XzlAdapter, YszAdapter, FqhAdapter, PpyAdapter):
        return cls(book_id, root, reg["layer_keys"], reg.get("join", "_kg_join.json"))
    return cls(book_id, root)


__all__ = [
    "BookAdapter",
    "LayerSlice",
    "VolLayerAdapter",
    "DataLayerAdapter",
    "NormLayerAdapter",
    "XgfAdapter",
    "LayersAdapter",
    "LgsAdapter",
    "XzlAdapter",
    "YszAdapter",
    "FqhAdapter",
    "PpyAdapter",
    "BOOK_ROOTS",
    "BOOK_NAMES",
    "BOOK_LAYERS",
    "BOOK_REGISTRY",
    "LAYER_DECL",
    "REPO_ROOT",
    "make_adapter",
    "book_source_root",
]
