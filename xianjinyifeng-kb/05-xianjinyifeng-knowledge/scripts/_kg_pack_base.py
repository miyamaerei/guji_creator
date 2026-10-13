# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - 公共基座（_kg_pack_base.py）

所有打包器/验证脚本共享的基础能力，各层打包器 import 复用（pitfalls.md #1：共享加载抽成
基座，import 替代复制）。对应 SKILL.md §10 的「公共基座 _kg_pack_base.py」约定。

包含：
  * atomic_write_json  临时文件 + rename 原子落盘（#14，防并行半写文件）
  * load_json / save_json
  * load_registry      加载指纹库 _item_registry.json（唯一真源，key=NN-NNN）
  * alloc_id           业务 ID 段位分配（#13/#22：段容量预留，防跨卷撞号）
  * inject_original    从指纹库注入 original/norm，覆盖任何手抄（#3）
  * load_source        加载 AI 源数据（_<layer>_ai_<vol>.py / .json）
  * check_enum_fields  枚举封闭集硬校验（#27：值∈封闭集；#15：未匹配入 pending 不中断；
                       --strict 时阻断）
  * collect_enum_usage 枚举使用分布统计（#27 对策2：值种数/定义数比值 >1.5 判漂移）
  * merge_volumes      共享文件增量合并语义（#12：--volumes 只重算请求卷、合并写回）
"""

from __future__ import annotations

import csv
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

import _kg_config as cfg
import _kg_enums as enums

# ---------------------------------------------------------------------------
# 基础 IO
# ---------------------------------------------------------------------------


def atomic_write_json(path: str, obj: Any) -> None:
    """临时文件 + rename 原子落盘（UTF-8，ensure_ascii=False 保留汉字）。"""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def load_json(path: str, default: Any = None) -> Any:
    """加载 JSON，文件不存在返回 default；损坏报错（不静默吞异常）。"""
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_csv(path: str, header: List[str], rows: List[List[Any]]) -> None:
    """以逻辑行写 CSV（csv.writer 处理含换行单元格，pittfals.md #18）。"""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    os.replace(tmp, path)


def read_csv_rows(path: str) -> List[Dict[str, str]]:
    """以逻辑行读取 CSV（csv.DictReader），返回 list[dict]；不存在返回 []。"""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


# ---------------------------------------------------------------------------
# 指纹库（唯一真源）
# ---------------------------------------------------------------------------


def load_registry() -> Dict[str, Dict[str, str]]:
    """加载指纹库；不存在返回 {}（调用方按 GAP 处理）。"""
    return load_json(cfg.REGISTRY_FILE, {}) or {}


def registry_item_ids(
    registry: Dict[str, Dict[str, str]], volume: Optional[str] = None
) -> List[str]:
    """指纹库全部 item_id（按 卷-序 排序）；volume 给定时只取该卷。"""
    ids = [i for i in registry.keys() if volume is None or i.startswith(volume + "-")]
    return sorted(ids)


# ---------------------------------------------------------------------------
# 业务 ID 段位分配（#13/#22）
# ---------------------------------------------------------------------------


def alloc_id(prefix: str, volume: int, slot: int) -> str:
    """段位分配：ID = prefix + (volume-1)*SEGMENT_CAPACITY + slot（slot 从 1 起，3 位补零）。

    卷1 槽位 1..500 -> ENT-001..ENT-500；卷2 槽位 1..500 -> ENT-501..ENT-1000。
    段容量不足时（#22：容量仍不够则扩段位全量重跑），改 cfg.SEGMENT_CAPACITY 后重跑。
    """
    return f"{prefix}{(volume - 1) * cfg.SEGMENT_CAPACITY + slot:03d}"


def slot_of(record: Dict[str, Any], index: int) -> int:
    """取记录槽位：显式 slot 字段优先，否则按列表顺序（index 从 1 起）。"""
    s = record.get("slot")
    if isinstance(s, int) and s >= 1:
        return s
    return index


# ---------------------------------------------------------------------------
# original/norm 注入（#3：AI 源数据不手抄原文，打包器从指纹库注入）
# ---------------------------------------------------------------------------


def inject_original(
    record: Dict[str, Any], item_id: str, registry: Dict[str, Dict[str, str]]
) -> List[str]:
    """注入 original/norm（强制覆盖源数据中的手抄，修正差异以指纹库为准）。

    返回本记录的问题列表：item_id 不在指纹库 -> GAP。
    """
    problems: List[str] = []
    entry = registry.get(item_id)
    if entry is None:
        record["original"] = ""
        record["norm"] = ""
        record["_gap"] = f"item_id {item_id} 不在指纹库"
        problems.append(f"{item_id}: item_id 不在指纹库，无法注入 original/norm")
        return problems
    record["original"] = entry["original"]
    record["norm"] = entry.get("norm", entry["original"])
    return problems


# ---------------------------------------------------------------------------
# AI 源数据加载（_<layer>_ai_<vol>.py / .json）
# ---------------------------------------------------------------------------


def source_file_paths(layer: str, volume: str) -> List[str]:
    """返回源数据候选路径（.py 优先；若均为存在则取存在的那些）。"""
    key = layer_key(layer)
    py = os.path.join(cfg.SRC_DIR, f"_{key}_ai_{volume}.py")
    js = os.path.join(cfg.SRC_DIR, f"_{key}_ai_{volume}.json")
    out = []
    for p in (py, js):
        if os.path.exists(p):
            out.append(p)
    return out


def load_source(layer: str, volume: str) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    """加载某卷某层的 AI 源数据。

    返回 (顶层 dict 或 None, 问题列表)：
      * 文件不存在               -> (None, ["source file not found"])
      * .py 源数据               -> exec 命名空间后取 src_key（顶层键名映射，见 #23）
      * .json 源数据             -> 顶层取 src_key；若本身就是 list 则包成 {src_key: list}
    """
    problems: List[str] = []
    paths = source_file_paths(layer, volume)
    if not paths:
        problems.append(
            f"{layer} 卷 {volume}: 源数据不存在（_src/_{layer_key(layer)}_ai_{volume}.py|.json）"
        )
        return None, problems
    src_key = cfg.LAYERS[layer]["src_key"]
    path = paths[0]
    try:
        if path.endswith(".py"):
            ns: Dict[str, Any] = {"__file__": path}
            with open(path, "r", encoding="utf-8-sig") as f:
                code = f.read()
            exec(compile(code, path, "exec"), ns)
            top = {src_key: ns.get(src_key, [])}
            if src_key not in ns:
                problems.append(f"{os.path.basename(path)}: 未定义顶层键 {src_key}")
        else:
            data = load_json(path, {})
            if isinstance(data, list):
                top = {src_key: data}
            elif isinstance(data, dict):
                if src_key not in data:
                    problems.append(f"{os.path.basename(path)}: 未定义顶层键 {src_key}")
                top = data
            else:
                problems.append(
                    f"{os.path.basename(path)}: JSON 顶层必须是 list 或 dict"
                )
                return None, problems
        if not isinstance(top.get(src_key), list):
            problems.append(f"{os.path.basename(path)}: 顶层键 {src_key} 必须是 list")
            return None, problems
        return top, problems
    except Exception as e:  # noqa: BLE001 - 源数据文件解析失败须显式暴露
        problems.append(f"{os.path.basename(path)}: 解析失败 {e!r}")
        return None, problems


def layer_key(layer: str) -> str:
    """层短名 -> 源数据文件名键（ent/appt/rel/event/opn/trl）。"""
    return layer


# ---------------------------------------------------------------------------
# 枚举治理（#15 收集-报告-暂存；#27 封闭集硬校验）
# ---------------------------------------------------------------------------


def _pending_path() -> str:
    return os.path.join(cfg.VALIDATE_DIR, "_enum_pending.json")


def load_pending() -> List[Dict[str, Any]]:
    return load_json(_pending_path(), []) or []


def save_pending(rows: List[Dict[str, Any]]) -> None:
    atomic_write_json(_pending_path(), rows)


def _add_pending(
    value: Any, field: str, enum_key: str, item_id: str, layer: str, source: str
) -> None:
    rows = load_pending()
    key = (str(value), field, enum_key, item_id)
    if not any(
        (r.get("value"), r.get("field"), r.get("enum_key"), r.get("item_id")) == key
        for r in rows
    ):
        rows.append(
            {
                "value": value,
                "field": field,
                "enum_key": enum_key,
                "item_id": item_id,
                "layer": layer,
                "source": source,
            }
        )
        save_pending(rows)


def check_enum_fields(
    layer: str, record: Dict[str, Any], item_id: str, strict: bool = False
) -> List[str]:
    """对记录的枚举字段做封闭集硬校验（#27）。

    规则：
      * 值 ∈ 封闭集            -> 通过
      * 值 ∈ 别名映射          -> 回填为规范值（记录就地改写），报告一次「已归并」
      * 值 ∉ 封闭集            -> 写入 pending 表（收集-报告-暂存，#15）；
                                  strict=True 时抛错阻断（不许静默写入，#27）
    返回问题列表（供验证报告归类 ERR/GAP）。
    """
    problems: List[str] = []
    for field, enum_key in enums.ENUM_FIELD_MAP.get(layer, []):
        value = record.get(field)
        if value is None or value == "":
            continue  # 缺字段由 schema/覆盖校验另行报告
        entry = enums.ENUM_REGISTRY[enum_key]
        if value in entry["values"]:
            continue
        alias = entry["aliases"].get(value)
        if alias is not None:
            record[field] = alias
            problems.append(f"{item_id}: {field}={value!r} 已按别名归并 -> {alias}")
            continue
        msg = f"{item_id}: {field}={value!r} 不在 {enum_key} 封闭集（已入 pending 待决议）"
        problems.append(msg)
        _add_pending(value, field, enum_key, item_id, layer, "check_enum_fields")
        if strict:
            raise ValueError(f"[strict] {msg}")
    return problems


def collect_enum_usage(
    layer: str, record: Dict[str, Any], usage: Dict[str, Dict[str, int]]
) -> None:
    """统计枚举字段使用分布（值 -> 计数），供 #27 对策2 的口径漂移告警。"""
    for field, enum_key in enums.ENUM_FIELD_MAP.get(layer, []):
        value = record.get(field)
        if value is None:
            continue
        bucket = usage.setdefault(enum_key, {})
        bucket[str(value)] = bucket.get(str(value), 0) + 1


# ---------------------------------------------------------------------------
# 共享文件增量合并（#12：--volumes 只重算请求卷、合并写回，不覆盖共享文件）
# ---------------------------------------------------------------------------


def parse_volumes(arg: Optional[str]) -> Optional[List[str]]:
    """解析 --volumes "01,02" -> ["01","02"]；未传返回 None（全量重建）。"""
    if not arg:
        return None
    vols = [v.strip() for v in arg.split(",") if v.strip()]
    for v in vols:
        if len(v) != 2 or not v.isdigit():
            raise ValueError(f"--volumes 格式错误：{v!r}（应为两位卷号 NN）")
    return vols


def volumes_to_rebuild(arg: Optional[str]) -> Optional[List[str]]:
    """确定本次需要重算的卷集合：None=全量（从空重建为权威口径）；否则只重算列出的卷。

    入参为 CLI 原始字符串（如 "01,02"），内部解析为卷号列表（parse_volumes 负责格式校验）。
    """
    return parse_volumes(arg)


def merge_layer_all(
    path: str,
    layer: str,
    vol_records: Dict[str, List[Dict[str, Any]]],
    requested: Optional[List[str]],
) -> Dict[str, Any]:
    """增量合并卷产物到全局聚合文件（#12/#24）。

    - requested is None：以 vol_records 为准全量重建（权威口径）。
    - requested 有值：加载既有 *_all.json，仅替换 requested 对应卷，其余卷保留。
    返回合并后的全局聚合 dict（{"layer","volumes":{vol:{count,records}},"total"}）。
    """
    existing: Dict[str, Any] = load_json(path, {}) or {}
    current_vols: Dict[str, Dict[str, Any]] = existing.get("volumes", {})
    rebuild = requested is None
    if rebuild:
        merged_vols: Dict[str, Any] = {}
        for vol, recs in vol_records.items():
            merged_vols[vol] = {"count": len(recs), "records": recs}
        base = {}
    else:
        merged_vols = dict(current_vols)
        base = {k: v for k, v in existing.items() if k not in ("volumes", "total")}
        for vol, recs in vol_records.items():
            merged_vols[vol] = {"count": len(recs), "records": recs}
    total = sum(v["count"] for v in merged_vols.values())
    out = dict(base)
    out["layer"] = layer
    out["volumes"] = merged_vols
    out["total"] = total
    return out


def all_records_of(agg: Dict[str, Any]) -> List[Dict[str, Any]]:
    """从全局聚合展开全部 records（按卷号顺序）。"""
    out: List[Dict[str, Any]] = []
    for vol in sorted(agg.get("volumes", {}).keys()):
        out.extend(agg["volumes"][vol].get("records", []))
    return out


# ---------------------------------------------------------------------------
# 输出与日志（#6：验证脚本写文件输出，不依赖 stdout；此处仅打印进度摘要）
# ---------------------------------------------------------------------------


def print_progress(msg: str) -> None:
    print(msg, flush=True)


def summary_problems(problems: List[str], kind: str) -> Tuple[int, int]:
    """把问题列表归类为（ERR 数, GAP 数）。

    ERR：结构性问题（缺文件/缺键/解析失败/枚举 strict 阻断等），必须修复；
    GAP：执行缺口（条目未建模/枚举待决议/低置信等），如实单列不并入总量（#9）。
    """
    err = 0
    gap = 0
    for p in problems:
        if (
            "strict" in p
            or "解析失败" in p
            or "未定义顶层键" in p
            or "顶层键" in p
            or "源数据不存在" in p
            or "不在指纹库" in p
        ):
            err += 1
        else:
            gap += 1
    return err, gap


def main_guard() -> None:
    """打包器脚本直接运行时确保数据目录存在。"""
    cfg.ensure_dirs()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
