# -*- coding: utf-8 -*-
"""《客座赘语》知识工程 —— 公共基座（公共地基，所有打包器与验证脚本共用）。

设计口径（照 skill `kezuo-zhuiyu-knowledge` §2 / §18 / references/schemas.md）：
  * 一律"临时文件 + os.replace 落盘"，防并行半写；
  * 共享汇总文件走"增量合并"语义（--volumes 只重算请求卷，其余卷原样保留）；
  * item_id = NN-NNN，是所有层的共同锚点；
  * original/norm 不手抄，统一由 _item_registry.json 注入；
  * 枚举校验走"收集 - 报告 - 暂存"，未知值入 pending 不中断执行；
  * 业务 ID 全部由打包器分配（源数据只写 item_id + 该层语义键）。

命令行约定（所有 build_ 脚本一致）：
    python build_base.py              # 底座打包（章节切分 + 指纹库）
    python build_base.py --check      # 只自检不写盘
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

DEFAULT_SRC = r"C:\Users\Administrator\.qianfan\workspace\sessions\5c7aeec1c4044e68bb49a4541b18ed5b\2026-10-10\new-chat-2\客座赘语_txt"
SOURCE_DIR = Path(os.environ.get("KZZ_SRC", DEFAULT_SRC))

EXTRACT_DIR = ROOT / "_extract"
REGISTRY_PATH = ROOT / "_item_registry.json"

LAYER_JSON_DIR = ROOT / "_layers"  # 每层每卷 <layer>_<NN>.json
SRC_DIR = ROOT / "_src"  # AI 源数据 _<layer>_ai_<NN>.py
BUILD_DIR = ROOT / "_build"  # 打包产物
VALIDATE_DIR = ROOT / "_validate"  # 验证清单
DELIVER_DIR = ROOT / "_deliver"  # 交付聚合

ENCODING = "utf-8"
UNKNOWN = "未明"
BUILD_VERSION = "v1.0"

# --------------------------------------------------------------------------
# 1. 卷表（NN -> 卷名）；00 = 版本说明与序（丛书总序/导读/点校说明/原序/四库提要）
# --------------------------------------------------------------------------

VOLUMES: list[tuple[str, str]] = [
    ("00", "版本说明与序"),
    ("01", "卷一"),
    ("02", "卷二"),
    ("03", "卷三"),
    ("04", "卷四"),
    ("05", "卷五"),
    ("06", "卷六"),
    ("07", "卷七"),
    ("08", "卷八"),
    ("09", "卷九"),
    ("10", "卷十"),
]
VOLUME_NAME = dict(VOLUMES)
ALL_VOLUMES = [n for n, _ in VOLUMES]

# 卷阅读模式初判（V1；细判见 references/volume-profile.md，执行时以卷内实际为准回填）
# 依据 skill §16：卷四/卷五古迹异闻→风土优先；卷七/卷九/卷十制度名物→制度优先/名物优先；
# 卷一/卷二人物轶事→人物优先/轶事优先；未预判卷（三/六/八）按均衡全层。
VOLUME_MODE_HINT = {
    "00": "均衡全层",
    "01": "人物优先/轶事优先",
    "02": "人物优先/轶事优先",
    "03": "均衡全层",
    "04": "风土优先",
    "05": "风土优先",
    "06": "均衡全层",
    "07": "制度优先/名物优先",
    "08": "均衡全层",
    "09": "制度优先/名物优先",
    "10": "制度优先/名物优先/名录优先",
}

# --------------------------------------------------------------------------
# 2. 层配置（写的源数据 / 打包器 / 验证器全部由本表驱动）
# --------------------------------------------------------------------------

COMMON_KEYS = ("volume", "item_id", "original", "norm", "evidence")

LAYERS: dict[str, dict] = {
    "ent": {
        "id_prefix": "ENT-",
        "id_field": "ent_id",
        "source": "entity",
        "key_fields": ("text",),
        "enum_fields": ("type",),
        "ref_fields": (),
        "must_fields": ("item_id", "text", "type", "start", "end"),
        "volume_level": False,
    },
    "event": {
        "id_prefix": "EVT-",
        "id_field": "event_id",
        "source": "event",
        "key_fields": ("type", "action"),
        "enum_fields": ("type",),
        "ref_fields": (),
        "must_fields": ("item_id", "type", "action", "who", "where", "when", "what"),
        "volume_level": False,
    },
    "cit": {
        "id_prefix": "CIT-",
        "id_field": "cit_id",
        "source": "cit",
        "key_fields": ("cited_work", "citation_type"),
        "enum_fields": ("citation_type", "purpose"),
        "ref_fields": (),
        "must_fields": (
            "item_id",
            "cited_work",
            "citation_type",
            "context",
            "original",
        ),
        "volume_level": False,
    },
    "obj": {
        "id_prefix": "OBJ-",
        "id_field": "obj_id",
        "source": "obj",
        "key_fields": ("name",),
        "enum_fields": ("category",),
        "ref_fields": (),
        "must_fields": ("item_id", "name", "category"),
        "volume_level": False,
    },
    "cus": {
        "id_prefix": "CUS-",
        "id_field": "cus_id",
        "source": "cus",
        "key_fields": ("term", "type"),
        "enum_fields": ("type",),
        "ref_fields": (),
        "must_fields": ("item_id", "type", "term", "description"),
        "volume_level": False,
    },
    "ming": {
        "id_prefix": "MING-",
        "id_field": "ming_id",
        "source": "ming",
        "key_fields": ("category",),
        "enum_fields": ("category",),
        "ref_fields": ("ref_events",),
        "must_fields": ("item_id", "category", "what"),
        "volume_level": False,
    },
    "geo": {
        "id_prefix": "GEO-",
        "id_field": "geo_id",
        "source": "geo",
        "key_fields": ("name",),
        "enum_fields": ("category",),
        "ref_fields": (),
        "must_fields": ("item_id", "name", "category"),
        "volume_level": False,
    },
    "appt": {
        "id_prefix": "APPT-",
        "id_field": "appointment_id",
        "source": "appt",
        "key_fields": ("office",),
        "enum_fields": ("status",),
        "ref_fields": (),
        "must_fields": ("item_id", "person", "office"),
        "volume_level": False,
    },
    "nam": {
        "id_prefix": "NAM-",
        "id_field": "nam_id",
        "source": "nam",
        "key_fields": ("category",),
        "enum_fields": ("category",),
        "ref_fields": (),
        "must_fields": ("item_id", "name", "category"),
        "volume_level": False,
    },
    "lit": {
        "id_prefix": "LIT-",
        "id_field": "lit_id",
        "source": "lit",
        "key_fields": ("title",),
        "enum_fields": ("type",),
        "ref_fields": (),
        "must_fields": ("item_id", "title", "type"),
        "volume_level": False,
    },
    "opn": {
        "id_prefix": "OPN-",
        "id_field": "opn_id",
        "source": "opn",
        "key_fields": ("topic",),
        "enum_fields": ("stance",),
        "ref_fields": ("evidence_refs",),
        "must_fields": ("item_id", "topic", "stance"),
        "volume_level": False,
    },
    "rel": {
        "id_prefix": "REL-",
        "id_field": "rel_id",
        "source": "rel",
        "key_fields": ("relation_type",),
        "enum_fields": ("relation_type",),
        "ref_fields": (),
        "must_fields": ("item_id", "person_a", "person_b", "relation_type"),
        "volume_level": False,
    },
    "trl": {
        "id_prefix": "TRL-",
        "id_field": "trl_id",
        "source": "trl",
        "key_fields": ("style",),
        "enum_fields": ("style",),
        "ref_fields": (),
        "must_fields": ("item_id", "translation", "style"),
        "volume_level": False,
    },
}

# 卷帙级 task 的任务链（一卷一个里程碑：通读 → 写入 → 三连自检 → build → 复核）
TASK_STEPS = ["通读", "写入", "三连自检", "build", "复核"]

# --------------------------------------------------------------------------
# 3. 文本 IO 工具（UTF-8，临时文件 + os.replace 原子落盘）
# --------------------------------------------------------------------------


def _reconfigure_console() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
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


def write_csv(
    path: str | Path, rows: list[dict], fieldnames: list[str] | None = None
) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        write_text(p, "")
        return
    fields = fieldnames or list(rows[0].keys())
    buf = io.StringIO()
    writer = csv.DictWriter(
        buf, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
    )
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

# 占位符/异体字映射表（扫描本缺字/常见异体字 → 通行字）。数据驱动，可继续补。
# 缺字：原文用 ☐（U+2610）占位，norm 统一为 □（U+25A1）。
VARIANT_MAP: dict[str, str] = {
    "\u2610": "\u25a1",  # ☐ -> □
}


def normalize_text(text: str) -> str:
    """norm 口径：全角空白归一 + 半角空白压缩 + 异体字/缺字映射（保留句读标点）。"""
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
    """读 _extract/NN_卷名.txt（`条N|正文`），返回 [(item_id, text), ...]。

    条目正文允许跨多行（段落以 \n 分隔）；以"条N|"前缀行作为新条目起点，
    后续非"条"前缀行续接到上一条目正文（接 \n）。
    """
    p = extract_path(volume)
    if not p.exists():
        raise FileNotFoundError(f"未找到切分产物 {p}，请先执行 python build_base.py")
    type(volume)
    items: list[list] = []
    seq_s = ""
    body_parts: list[str] = []
    for line in read_text(p).split("\n"):
        if not line.strip():
            continue
        m = re.match(r"^条(\d+)\|", line)
        if m:
            if body_parts:
                items.append([item_key(volume, int(seq_s)), "\n".join(body_parts)])
            seq_s = m.group(1)
            body_parts = [line[m.end() :]]
        else:
            body_parts.append(line)
    if body_parts:
        items.append([item_key(volume, int(seq_s)), "\n".join(body_parts)])
    return items


def load_registry() -> dict:
    reg = read_json(REGISTRY_PATH)
    if reg is None:
        raise FileNotFoundError(
            f"未找到指纹库 {REGISTRY_PATH}，请先执行 python build_base.py"
        )
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
# 6. 源数据加载（_src/_<layer>_ai_<NN>.py 的 RECORDS）
# --------------------------------------------------------------------------


def source_path(layer: str, volume: str) -> Path:
    return SRC_DIR / f"_{layer}_ai_{volume}.py"


def load_source(layer: str, volume: str) -> list[dict]:
    """importlib 动态加载 _src/_<layer>_ai_<NN>.py，返回 RECORDS。"""
    import importlib.util

    p = source_path(layer, volume)
    if not p.exists():
        return []
    spec = importlib.util.spec_from_file_location(f"_src_{layer}_{volume}", p)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载源数据模块：{p}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    records = list(getattr(mod, "RECORDS", []))
    for r in records:
        if not isinstance(r, dict):
            raise TypeError(f"{p.name} 的 RECORDS 非 dict 记录：{r!r}")
    return records


def load_sources(layer: str, volumes: list[str]) -> dict[str, list[dict]]:
    return {vol: load_source(layer, vol) for vol in volumes}


# --------------------------------------------------------------------------
# 7. ID 分配（幂等：同卷同序 → 同 ID）
# --------------------------------------------------------------------------


class IdAllocator:
    """业务 ID 顺序分配器。ID 序号在"层全局"递增，扫描顺序 = 卷序 + 源数据顺序。"""

    def __init__(self, prefix: str, start: int = 1, width: int = 4):
        self.prefix = prefix
        self.value = start
        self.width = width

    def next(self) -> str:
        rid = f"{self.prefix}{self.value:0{self.width}d}"
        self.value += 1
        return rid


def make_id(prefix: str, n: int, width: int = 4) -> str:
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
# 8. 单卷产物装载 / 增量合并 / 共享汇总
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


def write_volume_products(
    layer: str, cfg: dict, volumes: list[str], per_volume: dict[str, list[dict]]
) -> None:
    """写每卷 JSON（顶层键统一 records；元信息 header 键）。"""
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


def collect_layer_records(
    layer: str,
    cfg: dict,
    volumes: list[str],
    per_volume: dict[str, list[dict]] | None = None,
) -> list[dict]:
    """汇总某层记录：优先用本次计算结果，其次读已落盘单卷 JSON（实现增量）。"""
    out: list[dict] = []
    for vol in volumes:
        if per_volume is not None and vol in per_volume:
            out.extend(per_volume[vol])
        else:
            out.extend(read_layer_volume(layer, vol))
    return out


JOIN_LAYER_KEYS: dict[str, str] = {
    "ent": "ents",
    "event": "events",
    "cit": "cits",
    "obj": "objs",
    "cus": "cuss",
    "ming": "mings",
    "geo": "geos",
    "appt": "appts",
    "nam": "nams",
    "lit": "lits",
    "opn": "opns",
    "rel": "rels",
    "trl": "trls",
}


# --------------------------------------------------------------------------
# 9. CLI 与运行上下文
# --------------------------------------------------------------------------


def build_context(description: str) -> tuple[argparse.Namespace, list[str]]:
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument(
        "--volumes",
        nargs="*",
        default=None,
        help="只重跑指定卷（增量合并），如 --volumes 01 02；缺省=全量",
    )
    ap.add_argument("--check", action="store_true", help="只校验不写盘")
    ap.add_argument(
        "--zip",
        action="store_true",
        help="构建完成后生成统一打包 zip（build_layers 使用）",
    )
    args = ap.parse_args()
    if args.volumes:
        vols = [v.zfill(2) for v in args.volumes]
        unknown = [v for v in vols if v not in VOLUME_NAME]
        if unknown:
            raise SystemExit(f"未知卷号：{unknown}")
    else:
        vols = list(ALL_VOLUMES)
    return args, vols


def ensure_dirs() -> None:
    for d in (
        EXTRACT_DIR,
        LAYER_JSON_DIR,
        SRC_DIR,
        BUILD_DIR,
        VALIDATE_DIR,
        DELIVER_DIR,
    ):
        d.mkdir(parents=True, exist_ok=True)


def have_source(layer: str, volume: str) -> bool:
    return source_path(layer, volume).exists()
