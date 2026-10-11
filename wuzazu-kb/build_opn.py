"""《五杂俎》知识工程 | 作者观点论说层（OPN）打包器

源数据：_src/_opn_ai_<NN>.py
    RECORDS = [{
        item_id, topic, stance, argument, evidence_refs?
    }]
    stance 走 opn_stance 枚举（论理优先卷 01/02 为重点产地）；
    evidence_refs 写条号（01-012）或本层 ID（WZZ-E-004），只索引不改写原文。

产物：_layers/opn_<NN>.json、_build/opn__summary.json、_build/_opn_logs.json

重跑：python build_opn.py [--volumes 01 02] [--check] [--rebuild-index]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_layer_runner import layer_cli  # noqa: E402
from _kg_pack_base import main_guard  # noqa: E402

TITLE = "作者观点论说层（OPN）"

if __name__ == "__main__":
    main_guard(lambda: layer_cli("opn", TITLE))
