# -*- coding: utf-8 -*-
"""AI 源数据加载与 ID 分配 —— 所有打包器的公共入口。

源数据文件名约定（SKILL §14.2）：`scripts/_<prefix>_ai_<NN>.py`，例如：
  _ents_ai_01.py / _rules_ai_02.py / _regs_ai_06.py
每个文件必须定义顶层变量 `AI_RECORDS`（list[dict]）。

ID 分配纪律（references/schemas.md §0.3）：
  · 源数据只写 `slot`，**绝不手写 ID**（ENT 除外：同一实体多条记录可显式
    给出相同 `id` 以共享主键，打包器保留不覆盖）；
  · 打包器按 `<前缀><卷段位><序号>` 分配：如 ENT-01001 = 卷01 第1条；
  · 段容量 SEG_CAPACITY=500（超过会告警，不阻断）。
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List

from _kg_enums import SEG_CAPACITY

AI_DIR = Path(__file__).resolve().parent


def load_ai(prefix: str, vol: int) -> Any:
    """加载 `scripts/_<prefix>_ai_<NN>.py` 的 AI_RECORDS；文件缺失返回 []。

    返回类型：L1-L3/L5-C14 层为 list[dict]；L4 (prefix="struct") 为
    dict[str, list[dict]]（子类 → 记录）。文件缺失统一返回 []。
    """
    path = AI_DIR / f"_{prefix}_ai_{vol:02d}.py"
    if not path.exists():
        return []
    mod_name = f"_ai_{prefix}_{vol:02d}"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载源数据模块: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    recs = getattr(mod, "AI_RECORDS", [])
    if prefix == "struct":
        if not isinstance(recs, dict):
            raise RuntimeError(
                f"{path.name}: AI_RECORDS 必须是 dict（子类→记录），实为 {type(recs).__name__}"
            )
        return recs
    if not isinstance(recs, list):
        raise RuntimeError(
            f"{path.name}: AI_RECORDS 必须是 list，实为 {type(recs).__name__}"
        )
    return recs


def assign_ids(
    recs: List[Dict[str, Any]], prefix: str, vol: int
) -> List[Dict[str, Any]]:
    """为记录分配 ID：`<prefix><vol:02d><seq:03d>`；显式 id 保留（ENT 共享主键）。"""
    used = set()
    for r in recs:
        if r.get("id"):
            used.add(str(r["id"]))
    seq = 0
    out: List[Dict[str, Any]] = []
    for r in recs:
        rec = dict(r)
        if not rec.get("id"):
            seq += 1
            while f"{prefix}{vol:02d}{seq:03d}" in used:
                seq += 1
                if seq > SEG_CAPACITY:
                    raise RuntimeError(
                        f"{prefix} 卷 {vol:02d} 段容量 {SEG_CAPACITY} 已耗尽（坑 #28 段位设计）"
                    )
            rec["id"] = f"{prefix}{vol:02d}{seq:03d}"
        out.append(rec)
    return out


def check_item_ids(recs: List[Dict[str, Any]], reg: Dict[str, Any]) -> None:
    """每条记录的 item_id 必须命中 registry（单值或列表）。"""
    for r in recs:
        iid = r.get("item_id")
        if iid is None:
            continue
        if isinstance(iid, list):
            for one in iid:
                if one not in reg:
                    raise RuntimeError(f"{r.get('id', '?')}: item_id {one!r} 悬空")
        elif iid not in reg:
            raise RuntimeError(f"{r.get('id', '?')}: item_id {iid!r} 悬空")


def volumes_arg(argv: List[str]) -> List[int]:
    """--volumes NN 参数：缺省跑 01-06 全量（SKILL §16.8：勿用逗号多卷，须逐卷或缺省全量）。"""
    if "--volumes" in argv:
        i = argv.index("--volumes")
        if i + 1 < len(argv):
            raw = argv[i + 1].strip()
            if "," in raw:
                raise SystemExit(
                    "--volumes 不接受逗号多卷（SKILL §16.8），请逐卷运行或缺省全量"
                )
            vol = int(raw)
            if not 1 <= vol <= 6:
                raise SystemExit(f"卷号越界: {vol}")
            return [vol]
        raise SystemExit("--volumes 缺参数")
    return list(range(1, 7))
