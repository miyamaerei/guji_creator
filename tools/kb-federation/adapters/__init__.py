"""adapters/__init__.py —— 注册表 + 每书 catalog 声明

BOOK_ROOTS：六书相对仓库根的路径（撞号扫描用，不依赖 adapter 类）。
BOOK_REGISTRY：现已实现 adapter 的书（F2 补全其余 5 本）。
LAYER_DECL：层 key ↔ 形态 ↔ 前缀 ↔ kind 显式登记。取代运行时试探，
            正是契约线 C4/C5 在联邦线侧的兑现 —— 新书/新层只在此加几行，
            loader 逻辑不改。

注意：LAYER_DECL 等数据定义必须在 import LayersAdapter 之前完成，
否则 layers_adapter 里的 `from . import LAYER_DECL` 会因尚未定义而环形失败。
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
}
BOOK_NAMES = {
    "kzz": "客座赘语",
    "wzz": "五杂俎",
    "sdr": "水东日记",
    "xgf": "新官轨范",
    "qb": "蘧编",
    "xyf": "先进遗风",
}

# adapter 注册（F1 仅 xyf；F2 补全其余 4 个 adapter 类）
BOOK_REGISTRY = {
    "xyf": {
        "class": None,  # 占位，下面赋值
        "root": BOOK_ROOTS["xyf"],
        "join": "data/_layers/kg_join.json",
    },
}

# 层声明：层 key -> (kind, container_kind, id_prefix)
#   kind: node | edge | annotation | profile
#   container_kind: 来源形态（layers/rows/list/entries/records/fingerprints）
#   id_prefix: 本书实际 ID 前缀；空串表示按 item_id 键控
LAYER_DECL = {
    "xyf": {
        "ent": ("node", "layers", ""),
        "appt": ("edge", "layers", ""),
        "rel": ("edge", "layers", "REL-"),
        "event": ("edge", "layers", "XJF-E-"),
        "opn": ("annotation", "layers", ""),
        "trl": ("annotation", "layers", ""),
    },
}

from .layers_adapter import LayersAdapter  # noqa: E402

BOOK_REGISTRY["xyf"]["class"] = LayersAdapter


def book_source_root(book_id):
    return os.path.join(REPO_ROOT, BOOK_REGISTRY[book_id]["root"])


def make_adapter(book_id):
    reg = BOOK_REGISTRY[book_id]
    root = os.path.join(REPO_ROOT, reg["root"])
    if reg["class"] is LayersAdapter:
        return LayersAdapter(book_id, root, reg["join"])
    return reg["class"](book_id, root)


__all__ = [
    "BookAdapter",
    "LayerSlice",
    "LayersAdapter",
    "BOOK_ROOTS",
    "BOOK_NAMES",
    "BOOK_REGISTRY",
    "LAYER_DECL",
    "REPO_ROOT",
    "make_adapter",
    "book_source_root",
]
