# -*- coding: utf-8 -*-
"""《五杂俎》知识工程 —— 公共基座（公共地基，所有打包器与验证脚本共用）。

设计口径（照 skill `wuzazu-knowledge` §14 / references/schemas.md §1）：
  * 一律"临时文件 + os.replace 落盘"，防并行半写；
  * 共享汇总文件走"增量合并"语义（--volumes 只重算请求卷，其余卷原样保留）；
  * item_id = NN-NNN，是所有层的共同锚点；
  * original/norm 不手抄，统一由 _item_registry.json 注入；
  * 枚举校验走"收集 - 报告 - 暂存"，未知值入 pending 不中断执行；
  * 业务 ID 全部由打包器分配（源数据只写 item_id + 该层语义键）。

命令行约定（所有 build_/validate_ 脚本一致）：
    python build_event.py                # 全量
    python build_event.py --volumes 01   # 单卷重跑（增量合并）
    python build_event.py --check        # 只校验不写盘
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# --------------------------------------------------------------------------
# 0. 环境与路径
# --------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent

# 源文本：优先环境变量 WZZ_TXT；未设置时默认取 <项目根>/_source/五杂俎.txt
SOURCE_TXT = Path(os.environ.get("WZZ_TXT") or (ROOT / "_source" / "五杂俎.txt"))
EXTRACT_DIR = ROOT / "_extract"
REGISTRY_PATH = ROOT / "_item_registry.json"

LAYER_JSON_DIR = ROOT / "_layers"          # 每层每卷 <layer>_<NN>.json
SRC_DIR = ROOT / "_src"                    # AI 源数据 _<layer>_ai_<NN>.py
BUILD_DIR = ROOT / "_build"                # 打包产物
VALIDATE_DIR = ROOT / "_validate"          # 验证清单
DELIVER_DIR = ROOT / "_deliver"            # 交付聚合

ENCODING = "utf-8"
UNKNOWN = "未明"
BUILD_VERSION = "v1.0"

# --------------------------------------------------------------------------
# 1. 卷表（NN -> 卷名）；序 = 00
# --------------------------------------------------------------------------

VOLUMES: list[tuple[str, str]] = [
    ("00", "版本说明与序"),
    ("01", "天部一"),
    ("02", "天部二"),
    ("03", "地部一"),
    ("04", "地部二"),
    ("05", "人部一"),
    ("06", "人部二"),
    ("07", "人部三"),
    ("08", "人部四"),
    ("09", "物部一"),
    ("10", "物部二"),
    ("11", "物部三"),
    ("12", "物部四"),
    ("13", "事部一"),
    ("14", "事部二"),
    ("15", "事部三"),
    ("16", "事部四"),
]
VOLUME_NAME = dict(VOLUMES)
ALL_VOLUMES = [n for n, _ in VOLUMES]

# 卷阅读模式初判（V1；细判见 references/volume-profile.md，执行时以卷内实际为准回填）
VOLUME_MODE_HINT = {
    "00": "均衡全层",
    "01": "论理优先/灾异优先",
    "02": "论理优先/灾异优先",
    "03": "风土优先",
    "04": "风土优先",
    "05": "人物优先",
    "06": "人物优先",
    "07": "人物优先",
    "08": "人物优先",
    "09": "名物优先",
    "10": "名物优先",
    "11": "名物优先",
    "12": "名物优先",
    "13": "世情优先/轶事优先",
    "14": "世情优先/轶事优先",
    "15": "世情优先/轶事优先",
    "16": "世情优先/轶事优先",
}

# --------------------------------------------------------------------------
# 2. 层配置（写的源数据 / 打包器 / 验证器全部由本表驱动）
# --------------------------------------------------------------------------

COMMON_KEYS = ("volume", "item_id", "original", "norm", "evidence")

LAYERS: dict[str, dict] = {
    "ent": {
        "id_prefix": "ENT-",
        "id_field": "ent_id",
        "source": "entity",              # 独立主键表 builder
        "key_fields": ("text",),
        "enum_fields": ("type",),
        "ref_fields": (),
        "must_fields": ("item_id", "text", "type", "start", "end"),
        "volume_level": False,           # 主键表 + 每卷 records 双产物
    },
    "event": {
        "id_prefix": "WZZ-E-",
        "id_field": "event_id",
        "source": "event",
        "key_fields": ("type", "action"),
        "enum_fields": ("type",),
        "ref_fields": ("who_ent_ids",),
        "must_fields": ("item_id", "type", "who", "action", "what", "when", "where"),
    },
    "rel": {
        "id_prefix": "REL-",
        "id_field": "rel_id",
        "source": "rel",
        "key_fields": ("person_a", "person_b", "relation_type"),
        "enum_fields": ("relation_type", "direction"),
        "ref_fields": ("a_ent_ids", "b_ent_ids"),
        "must_fields": ("item_id", "person_a", "person_b", "relation_type", "direction", "evidence"),
    },
    "nam": {
        "id_prefix": "NAM-",
        "id_field": "nam_id",
        "source": "nam",
        "key_fields": ("name", "category"),
        "enum_fields": ("category",),
        "ref_fields": ("ent_ids",),
        "must_fields": ("item_id", "name", "category", "scope", "entries"),
    },
    "cit": {
        "id_prefix": "CIT-",
        "id_field": "cit_id",
        "source": "cit",
        "key_fields": ("cited_work", "citation_type"),
        "enum_fields": ("citation_type", "context"),
        "ref_fields": ("work_ent_ids",),
        "must_fields": ("item_id", "cited_work", "citation_type", "context"),
    },
    "obj": {
        "id_prefix": "OBJ-",
        "id_field": "obj_id",
        "source": "obj",
        "key_fields": ("name", "category"),
        "enum_fields": ("category",),
        "ref_fields": ("ent_ids",),
        "must_fields": ("item_id", "name", "category", "attributes", "lore"),
    },
    "cus": {
        "id_prefix": "CUS-",
        "id_field": "cus_id",
        "source": "cus",
        "key_fields": ("type", "term"),
        "enum_fields": ("type",),
        "ref_fields": ("region_ent_ids",),
        "must_fields": ("item_id", "type", "region", "term", "description"),
    },
    "opn": {
        "id_prefix": "OPN-",
        "id_field": "opn_id",
        "source": "opn",
        "key_fields": ("topic",),
        "enum_fields": ("stance",),
        "ref_fields": ("evidence_refs",),
        "must_fields": ("item_id", "topic", "stance", "argument"),
    },
    "ming": {
        "id_prefix": "MING-",
        "id_field": "ming_id",
        "source": "ming",
        "key_fields": ("era", "what"),
        "enum_fields": ("category",),
        "ref_fields": ("who_ent_ids", "ref_events"),
        "must_fields": ("item_id", "era", "who", "what", "when", "where", "category", "first_person"),
    },
    "appt": {
        "id_prefix": "APPT-",
        "id_field": "appointment_id",
        "source": "appt",
        "key_fields": ("person", "office"),
        "enum_fields": ("status",),
        "ref_fields": ("person_ent_ids", "official_ent_ids", "inst_ent_ids"),
        "must_fields": ("item_id", "person", "office", "institution", "when", "status", "evidence"),
    },
    "trl": {
        "id_prefix": "TRL-",
        "id_field": "trl_id",
        "source": "trl",
        "key_fields": (),                # 一条目一条译文（覆盖口径：条目数 = 翻译数）
        "enum_fields": ("style",),
        "ref_fields": (),
        "must_fields": ("item_id", "translation", "style", "note", "confidence"),
    },
}

# 跨层索引里的层键 -> 层名（_kg_join 一行贯通）
JOIN_LAYER_KEYS = {
    "event": "events",
    "rel": "rels",
    "nam": "nams",
    "cit": "cits",
    "obj": "objs",
    "cus": "cuss",
    "opn": "opns",
    "ming": "mings",
    "appt": "appts",
    "trl": "trls",
}

# --------------------------------------------------------------------------
# 3. 基础工具：读写（原子落盘）、哈希、时间
# --------------------------------------------------------------------------


def _reconfigure_console() -> None:
    """Windows 控制台常为 GBK：强制 UTF-8 + 替换，中文报告不再因编码中断。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


_reconfigure_console()


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path: str | Path) -> str:
    with open(path, "r", encoding=ENCODING, newline="") as fp:
        return fp.read()


def write_text(path: str | Path, text: str) -> None:
    """临时文件 + os.replace 落盘。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    with open(tmp, "w", encoding=ENCODING, newline="\n") as fp:
        fp.write(text)
    os.replace(tmp, p)


def write_json(path: str | Path, obj, indent: int = 2) -> None:
    write_text(path, json.dumps(obj, ensure_ascii=False, indent=indent))


def read_json(path: str | Path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    with open(p, "r", encoding=ENCODING) as fp:
        return json.load(fp)


def write_csv(path: str | Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        write_text(p, "")
        return
    fields = fieldnames or list(rows[0].keys())
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: _csv_cell(row.get(k)) for k in fields})
    write_text(p, buf.getvalue())


def _csv_cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return " | ".join(_csv_cell(v) for v in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def read_csv(path: str | Path) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    with open(p, "r", encoding=ENCODING, newline="") as fp:
        return list(csv.DictReader(fp))


# --------------------------------------------------------------------------
# 4. 原文归一（norm）
# --------------------------------------------------------------------------

# 占位符/异体字映射表（本书扫描本常见误字 → 通行字）。数据驱动，可继续补。
VARIANT_MAP: dict[str, str] = {}


def normalize_text(text: str) -> str:
    """norm 口径：全角空白归一 + 半角空白压缩 + 异体字映射（保留句读标点）。"""
    out = text.replace("\u3000", " ").replace("\t", " ")
    for src, dst in VARIANT_MAP.items():
        out = out.replace(src, dst)
    out = re.sub(r"[ ]{2,}", " ", out)
    return out.strip()


ITEM_PREFIX_RE = re.compile(r"^[\s\u3000]*")


def strip_indent(line: str) -> str:
    return ITEM_PREFIX_RE.sub("", line).strip()


# --------------------------------------------------------------------------
# 5. 底座读取：条目 / 指纹库
# --------------------------------------------------------------------------


def item_key(volume: str, seq: int) -> str:
    return f"{volume}-{seq:03d}"


def extract_path(volume: str) -> Path:
    return EXTRACT_DIR / f"{volume}_{VOLUME_NAME[volume]}.txt"


def parse_extract(volume: str) -> list[list]:
    """读 _extract/NN_卷名.txt（`条N|正文`），返回 [(item_id, text), ...]。"""
    p = extract_path(volume)
    if not p.exists():
        raise FileNotFoundError(f"未找到切分产物 {p}，请先执行 python build_base.py")
    items: list[list] = []
    for line in read_text(p).split("\n"):
        if not line.strip():
            continue
        seq_s, _, body = line.partition("|")
        seq = int(re.sub(r"\D", "", seq_s) or 0)
        items.append([item_key(volume, seq), body])
    return items


def load_registry() -> dict:
    reg = read_json(REGISTRY_PATH)
    if reg is None:
        raise FileNotFoundError(f"未找到指纹库 {REGISTRY_PATH}，请先执行 python build_base.py")
    return reg


def registry_items(volume: str | None = None) -> list[tuple[str, dict]]:
    reg = load_registry()
    keys = sorted(reg.keys(), key=lambda k: (k.split("-")[0], int(k.split("-")[1])))
    if volume:
        keys = [k for k in keys if k.startswith(f"{volume}-")]
    return [(k, reg[k]) for k in keys]


def inject_original(record: dict, registry: dict) -> dict:
    """把 original/norm 注入记录（源数据不手抄原文）。"""
    item_id = record.get("item_id")
    entry = registry.get(item_id)
    if entry is None:
        record.setdefault("original", "")
        record.setdefault("norm", "")
        return record
    record["original"] = entry["original"]
    record["norm"] = entry["norm"]
    return record


# --------------------------------------------------------------------------
# 6. 源数据装载：_src/_<layer>_ai_<NN>.py
# --------------------------------------------------------------------------


def source_path(layer: str, volume: str) -> Path:
    return SRC_DIR / f"_{layer}_ai_{volume}.py"


def load_source(layer: str, volume: str) -> list[dict]:
    """装载单卷 AI 源数据。约定：模块内定义 RECORDS: list[dict]，只写条号 + 解读字段。"""
    p = source_path(layer, volume)
    if not p.exists():
        return []
    ns: dict = {"__file__": str(p), "__name__": f"_{layer}_ai_{volume}"}
    exec(compile(read_text(p), str(p), "exec"), ns)  # noqa: S102 - 本地可信源数据
    records = None
    for _cand in ("RECORDS", f"{layer.upper()}_RECORDS"):
        _found = ns.get(_cand)
        if isinstance(_found, list):
            if _found or records is None:
                records = _found
    if records is None:
        raise TypeError(
            f"{p} 缺少顶层列表：需要 RECORDS 或 {layer.upper()}_RECORDS"
        )
    if not isinstance(records, list):
        raise TypeError(f"{p} 的源数据顶层变量必须是 list[dict]")
    return [dict(r) for r in records]


def load_sources(layer: str, volumes: list[str]) -> dict[str, list[dict]]:
    return {v: load_source(layer, v) for v in volumes}


# --------------------------------------------------------------------------
# 7. ID 分配（幂等：同卷同序 → 同 ID）
# --------------------------------------------------------------------------


class IdAllocator:
    """业务 ID 顺序分配器。ID 序号在"层全局"递增，扫描顺序 = 卷序 + 源数据顺序。"""

    def __init__(self, prefix: str, start: int = 1, width: int = 3):
        self.prefix = prefix
        self.value = start
        self.width = width

    def next(self) -> str:
        rid = f"{self.prefix}{self.value:0{self.width}d}"
        self.value += 1
        return rid


def make_id(prefix: str, n: int, width: int = 3) -> str:
    return f"{prefix}{n:0{width}d}"


def layer_sort_key(record: dict, cfg: dict) -> tuple:
    """稳定排序键：item_id 优先，再按该层语义键（保证重跑 ID 不变）。"""
    item_id = str(record.get("item_id", ""))
    try:
        vol, seq = item_id.split("-")
        head = (vol, int(seq))
    except ValueError:
        head = ("99", 999)
    tail = tuple(_flat(record.get(k)) for k in cfg.get("key_fields", ()))
    return head + tail


def _flat(value) -> str:
    if isinstance(value, dict):
        return str(value.get("text", ""))
    if isinstance(value, (list, tuple)):
        return "".join(_flat(v) for v in value)
    return "" if value is None else str(value)


# --------------------------------------------------------------------------
# 8. 单卷产物装载 / 增量合并（共享汇总文件防覆盖）
# --------------------------------------------------------------------------


def layer_json_path(layer: str, volume: str) -> Path:
    return LAYER_JSON_DIR / f"{layer}_{volume}.json"


def read_layer_volume(layer: str, volume: str) -> list[dict]:
    obj = read_json(layer_json_path(layer, volume), default=None)
    if not obj:
        return []
    if isinstance(obj, dict):
        return list(obj.get("records", []))
    return list(obj)


def merge_records_by_volume(existing: dict, volume: str, records: list[dict], id_field: str) -> dict:
    """共享汇总文件的增量合并：只替换请求卷的切片，其余卷原样保留。"""
    merged = dict(existing or {})
    merged[f"volume_{volume}"] = {
        "volume": volume,
        "name": VOLUME_NAME.get(volume, ""),
        "count": len(records),
        "ids": [r.get(id_field) for r in records],
    }
    return merged


def write_volume_products(layer: str, cfg: dict, volumes: list[str],
                          per_volume: dict[str, list[dict]]) -> None:
    """写每卷 JSON（顶层键统一 records）。"""
    for vol in volumes:
        payload = {
            "layer": layer,
            "volume": vol,
            "name": VOLUME_NAME.get(vol, ""),
            "count": len(per_volume.get(vol, [])),
            "generated_at": now_stamp(),
            "builder": BUILD_VERSION,
            "records": per_volume.get(vol, []),
        }
        write_json(layer_json_path(layer, vol), payload)


def collect_layer_records(layer: str, cfg: dict, volumes: list[str],
                          per_volume: dict[str, list[dict]] | None = None) -> list[dict]:
    """汇总某层记录：优先用本次计算结果，其次读已落盘单卷 JSON（实现增量）。"""
    out: list[dict] = []
    for vol in volumes:
        if per_volume is not None and vol in per_volume:
            out.extend(per_volume[vol])
        else:
            out.extend(read_layer_volume(layer, vol))
    return out


# --------------------------------------------------------------------------
# 9. CLI 与运行上下文
# --------------------------------------------------------------------------


def build_context(description: str) -> tuple[argparse.Namespace, list[str]]:
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--volumes", nargs="*", default=None,
                    help="只重跑指定卷（增量合并），如 --volumes 01 02；缺省=全量")
    ap.add_argument("--check", action="store_true", help="只校验不写盘")
    ap.add_argument("--rebuild-index", action="store_true",
                    help="先按 _src/_ent_ai_NN.py 重建实体表与索引，再打包本层")
    args = ap.parse_args()
    if args.volumes:
        vols = [v.zfill(2) for v in args.volumes]
        unknown = [v for v in vols if v not in VOLUME_NAME]
        if unknown:
            raise SystemExit(f"未知卷号：{unknown}")
    else:
        vols = list(ALL_VOLUMES)
    return args, vols


def banner(title: str) -> None:
    print("=" * 68)
    print(f"《五杂俎》知识工程 | {title}")
    print("=" * 68)


def report_stats(title: str, stats: dict) -> None:
    print(f"\n[{title}]")
    for k, v in stats.items():
        print(f"  - {k}: {v}")


def ensure_dirs() -> None:
    for d in (EXTRACT_DIR, LAYER_JSON_DIR, SRC_DIR, BUILD_DIR, VALIDATE_DIR, DELIVER_DIR):
        d.mkdir(parents=True, exist_ok=True)


def have_source(layer: str, volume: str) -> bool:
    return source_path(layer, volume).exists()


def main_guard(fn) -> None:
    try:
        fn()
    except KeyboardInterrupt:
        print("\n[中断] 用户取消", file=sys.stderr)
        raise SystemExit(130)


def resolve_entity_index(args=None) -> dict:
    """各层打包前解析实体索引：--rebuild-index 时按源数据重建，否则读已落盘产物。"""
    import _kg_entity

    if args is not None and getattr(args, "rebuild_index", False):
        idx = _kg_entity.rebuild_entity_index(write=True)
        if idx:
            return idx
    return _kg_entity.load_entity_index()
