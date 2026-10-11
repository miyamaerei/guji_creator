"""《五杂俎》知识工程 | 名物层（OBJ）打包器

源数据：_src/_obj_ai_<NN>.py
    RECORDS = [{
        item_id, name, category, attributes, lore, ent_ids?
    }]
    name 可写字符串（自动转 {text, ent_ids}）或字典；
    attributes 为随类别而异的自由键字典（如 {形制, 材质, 产地, 用法}）；
    lore 记掌故/考据补充；category 走 obj_category 枚举。

产物：_layers/obj_<NN>.json、_build/obj__summary.json、_build/_obj_logs.json

重跑：python build_obj.py [--volumes 09] [--check] [--rebuild-index]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_layer_runner import layer_cli  # noqa: E402
from _kg_pack_base import main_guard  # noqa: E402

TITLE = "名物层（OBJ）"

if __name__ == "__main__":
    main_guard(lambda: layer_cli("obj", TITLE))
