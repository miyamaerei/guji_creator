"""adapters/base.py —— 抽取中间表与 adapter 抽象基类

LayerSlice 是 E 阶段的统一标准中间表：无论某书 join 是 rows / list /
entries / records / fingerprints 哪种形态，discover() 都归一成它。
"""

from dataclasses import dataclass, field


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
        if size_of(p) > 8 * 1024 * 1024:  # >8MB 跳过
            return None
        import json

        with open(p, encoding="utf-8") as f:
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
