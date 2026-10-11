"""《五杂俎》知识工程 | 引书索引层（CIT）打包器

源数据：_src/_cit_ai_<NN>.py
    RECORDS = [{
        item_id, cited_work, citation_type, context, work_ent_ids?
    }]
    cited_work 可写字符串（自动转 {text, ent_ids}）或字典；
    ent_ids 缺省时按词形在实体表（type=work 的引书实体）里回填，未命中入待核日志；
    citation_type ∈ {直引, 转引, 泛引, 暗用, 考辨}；
    context ∈ {立论, 证俗, 考源, 反驳, 补遗, 其他}。

产物：_layers/cit_<NN>.json、_build/cit__summary.json、_build/_cit_logs.json

重跑：python build_cit.py [--volumes 09] [--check] [--rebuild-index]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_layer_runner import layer_cli  # noqa: E402
from _kg_pack_base import main_guard  # noqa: E402

TITLE = "引书索引层（CIT）"

if __name__ == "__main__":
    main_guard(lambda: layer_cli("cit", TITLE))
