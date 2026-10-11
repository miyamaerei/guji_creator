"""adapters/base.py —— 抽取中间表与 adapter 抽象基类

LayerSlice 是 E 阶段的统一标准中间表：无论某书 join 是 rows / list /
entries / records / fingerprints 哪种形态，discover() 都归一成它。
"""

import os
import re
from dataclasses import dataclass, field


# 兜底 ID 正则：AABB-123 / AB-1 这类「大写字母前缀 + 数字」（区分于普通字段）
_PREFIXED_ID = re.compile(r"^[A-Z]{2,4}(?:-[A-Z0-9]{1,3})?-\d+$")


@dataclass
class LayerSlice:
    book_id: str
    layer_key: str  # 归一 key：ent / appt / evt / ...
    container_kind: str  # rows|list|entries|records|fingerprints
    kind: str  # node|edge|annotation|profile
    id_prefix: str  # 本书实际 ID 前缀；空串表示按 item_id 键控
    records: list = field(default_factory=list)  # 每条 {'local_id','item_id','volume','payload'}


class BookAdapter:
    """每本书一个 adapter：扫描源目录 → 标准 LayerSlice。

    必须填充 kind / container_kind / id_prefix（来自 __init__.py 的 LAYER_DECL
    注册表），不靠运行时试探 —— 这是对 #27（容器键 events/evts 不一）的反制。
    """

    def __init__(self, book_id, source_root):
        self.book_id = book_id
        self.source_root = source_root

    def _read_json(self, rel):
        p = os_path_join(self.source_root, rel)
        if not os_path_exists(p):
            return None
        if size_of(p) > 64 * 1024 * 1024:  # 大文件（如蘧编 ents 11MB）不跳过
            return None
        import json

        with open(p, encoding="utf-8") as f:
            return json.load(f)

    def _read_abspath(self, path):
        """读绝对路径（adapter 自己拼好的层文件用）。>64MB 跳过。"""
        if not os_path_exists(path):
            return None
        if size_of(path) > 64 * 1024 * 1024:
            return None
        import json

        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def discover(self) -> dict:
        """返回 layer_key -> LayerSlice。子类必须实现。"""
        raise NotImplementedError

    def fingerprints(self) -> list:
        """返回条目锚点列表（item_id/volume/norm）。子类必须实现。"""
        raise NotImplementedError


# --- 小工具（避免顶部重复 import os） ---
import os


def os_path_join(a, b):
    return os.path.join(a, b)


def os_path_exists(p):
    return os.path.exists(p)


def size_of(p):
    return os.path.getsize(p)


def pick_id(rec, layer, wrapper):
    """从一条层记录里挑出它的「主键 ID」。

    优先级：
      1. wrapper 声明的 id_field（KZZ 用 ent_id / event_id 等）
      2. 记录自带的 'id'（SDR / QB / XGF）
      3. '<layer>_id'（WZZ 用 ent_id / event_id 等）
      4. 任意以 '_id' 结尾、且值形如大写前缀 ID 的字段
    取不到返回 None —— 调用方改用 item_id#序号 兜底。
    """
    wrapper = wrapper or {}
    idf = wrapper.get("id_field")
    if idf and rec.get(idf):
        return rec[idf]
    if rec.get("id"):
        return rec["id"]
    cand = rec.get(layer + "_id")
    if cand:
        return cand
    for k, v in rec.items():
        if k.endswith("_id") and isinstance(v, str) and _PREFIXED_ID.match(v):
            return v
    return None


def build_local_id(rec, layer, wrapper, idx, *, volume_prefix):
    """生成 local_id 候选（不一定唯一，去重见 dedup_local_id）。

    - 有 ID：默认直接用；volume_prefix=True 时加卷前缀（KZZ/WZZ 等
      ID 按卷重排，必须加卷才能不丢记录）。
    - 无 ID：item_id#序号 兜底（先进遗风 ent 即此情形）。
    """
    vid = pick_id(rec, layer, wrapper)
    rvol = rec.get("volume") or (wrapper or {}).get("volume")
    item_id = rec.get("item_id")
    if vid:
        return (f"{rvol}:{vid}" if (rvol and volume_prefix) else str(vid))
    if item_id:
        return f"{item_id}#{idx}"
    return f"{rvol}#{idx}" if rvol else f"#{idx}"


def dedup_local_id(candidate, seen):
    """保证 local_id 在 (book, layer) 内唯一。

    同名候选追加 #1/#2/... 后缀；首个保持干净（如 '12:ENT-263'），
    后续为 '12:ENT-263#1'。SDR/XGF 的 id 是「按实体」复用标识，
    同一实体在多处出现会撞 local_id，必须在此去重，否则 OR REPLACE 丢记录。
    """
    cand = str(candidate)
    if cand not in seen:
        seen[cand] = 0
        return cand
    seen[cand] += 1
    return f"{cand}#{seen[cand]}"


# --- 小工具（避免顶部重复 import os） ---
