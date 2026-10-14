# -*- coding: utf-8 -*-
"""《明史·食货志》知识工程 —— 公共骨架（唯一来源）。

所有 build_*.py / validate_*.py 必须 `from _common import ...`，
不得再各自 `BASE = Path(__file__).parent.parent` 并硬编码 `layers/`（复数）路径。

口径统一（2026-10-16）：
  · 层目录 = `_layers/`（下划线复数），由 LAYER_SPECS 单点定义；
  · `layers/`（无下划线）为历史遗留，已废弃，见 FROZEN_DIRS；
  · 实体层 = `_layers/ents/`，`entities/`（项目根）为历史遗留。

@ 2026-10-16 骨架首次落地
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from _kg_enums import (  # noqa: F401  (re-export for builders)
    ENTITY_TYPES,
    ENTITY_TYPE_ALIASES,
    RULE_TYPES,
    RULE_MODALS,
    INST_TYPES,
    REG_STATUS,
    REG_QUOTA_TYPES,
    REG_SCOPES,
    REG_LEVIED_FORMS,
    REG_DOCS,
    REG_AGENT_KINDS,
    REG_PURPOSES,
    REG_SOURCES,
    REG_EXT_KEYS,
    QUAN_FORMS,
    QUAN_UNITS,
    QUAN_UNIT_DIMENSIONS,
    QUAN_ORIGINS,
    QUAN_SIDES,
    EVO_STAGES,
    FISC_STAGES,
    LEDGER_LEVELS,
    LEDGER_TOWNS,
    TRANS_MODES,
    TRANS_STEPS,
    HK_CATEGORIES,
    HK_CLASSES,
    LAND_TYPES,
    LAND_ASPECTS,
    REIGN_ORDER,
    TME_CATEGORIES,
    APPT_STATUS,
    OPN_TYPES,
    OPN_STANCES,
    OPN_CLAIM_MARKERS,
    OPN_MIN_LEN,
    ID_PREFIX,
    STRUCT_PREFIX,
    SEG_CAPACITY,
)

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_FILE = BASE_DIR / "食货志.txt"
CHAPTERS_DIR = BASE_DIR / "chapters"
EXTRACT_DIR = BASE_DIR / "_extract"
DATA_DIR = BASE_DIR / "_data"
LAYERS_DIR = BASE_DIR / "_layers"
VIEWS_DIR = BASE_DIR / "_views"
REPORTS_DIR = BASE_DIR / "reports"

REGISTRY_FILE = DATA_DIR / "registry.json"
FINGERPRINT_FILE = DATA_DIR / "fingerprints.json"

FROZEN_DIRS = [BASE_DIR / "layers", BASE_DIR / "entities"]

VOLUME_NAMES = {
    1: "食货一",
    2: "食货二",
    3: "食货三",
    4: "食货四",
    5: "食货五",
    6: "食货六",
}
VOLUME_MAX_NO = {1: 53, 2: 54, 3: 55, 4: 56, 5: 57, 6: 58}

# =============================================================================
# LAYER_SPECS —— 8 层 + 结构层 8 子类的唯一定义
# 字段：dir / id_prefix / kind(ents|list|registry) / per(卷文件 or 全局) / required
# =============================================================================

LAYER_SPECS: Dict[str, Dict[str, Any]] = {
    # ---- L1 实体层 ----
    "ents": {
        "dir": "_layers/ents",
        "id_prefix": "ENT-",
        "kind": "list",
        "per": "volume",
        "name": "L1 实体层",
        "required": ["id", "item_id", "type", "text", "norm"],
        "enum_fields": {"type": ENTITY_TYPES},
    },
    # ---- L2 规则层 ----
    "rules": {
        "dir": "_layers/rules",
        "id_prefix": "RULE-",
        "kind": "list",
        "per": "volume",
        "name": "L2 规则层",
        "required": [
            "id",
            "item_id",
            "rule_type",
            "modal",
            "subject",
            "predicate",
            "object",
            "condition",
            "exception",
            "penalty",
        ],
        "enum_fields": {"rule_type": RULE_TYPES, "modal": RULE_MODALS},
    },
    # ---- L3 过程层 ----
    "procs": {
        "dir": "_layers/procs",
        "id_prefix": "PROC-",
        "kind": "list",
        "per": "volume",
        "name": "L3 过程层",
        "required": ["id", "item_id", "scope", "name", "steps"],
        "enum_fields": {"mode": TRANS_MODES},
        "step_enum_field": "step",
        "step_enum": TRANS_STEPS,
    },
    # ---- REG 制度层（本书骨架，13 属性）----
    "regs": {
        "dir": "_layers/regs",
        "id_prefix": "REG-",
        "kind": "list",
        "per": "global",
        "name": "REG 制度层",
        "required": [
            "id",
            "item_id",
            "inst_type",
            "name",
            "主体",
            "对象",
            "标准",
            "存续",
            "文书载体",
            "执行者",
            "目的",
            "沿革",
            "史料来源",
        ],
        "enum_fields": {
            "inst_type": INST_TYPES,
            "status": REG_STATUS,
            "quota_type": REG_QUOTA_TYPES,
            "scope": REG_SCOPES,
            "levied_form": REG_LEVIED_FORMS,
            "docs": REG_DOCS,
            "agent_kinds": REG_AGENT_KINDS,
            "purpose": REG_PURPOSES,
            "source": REG_SOURCES,
        },
    },
    # ---- L4 结构层（8 子类共目录）----
    "structs": {
        "dir": "_layers/structs",
        "id_prefix": "",
        "kind": "registry",
        "per": "global",
        "name": "L4 结构层",
        "subtypes": {
            "QUAN": {
                "prefix": "QUAN-",
                "required": [
                    "id",
                    "item_id",
                    "item",
                    "form",
                    "amount",
                    "unit",
                    "dimension",
                ],
                "enum_fields": {
                    "form": QUAN_FORMS,
                    "unit": QUAN_UNITS,
                    "origin": QUAN_ORIGINS,
                    "side": QUAN_SIDES,
                },
            },
            "INST": {
                "prefix": "INST-",
                "required": ["id", "item_id", "label"],
                "enum_fields": {"inst_type": INST_TYPES},
            },
            "EVO": {
                "prefix": "EVO-",
                "required": ["id", "item_id", "stage", "description"],
                "enum_fields": {"stage": EVO_STAGES},
            },
            "FISC": {
                "prefix": "FISC-",
                "required": ["id", "item_id", "step", "object"],
                "enum_fields": {"step": FISC_STAGES},
            },
            "LED": {
                "prefix": "LED-",
                "required": ["id", "item_id", "level", "label"],
                "enum_fields": {"level": LEDGER_LEVELS},
            },
            "TRANS": {
                "prefix": "TRANS-",
                "required": ["id", "item_id", "mode"],
                "enum_fields": {"mode": TRANS_MODES},
            },
            "HK": {
                "prefix": "HK-",
                "required": ["id", "item_id", "category"],
                "enum_fields": {"category": HK_CATEGORIES, "class": HK_CLASSES},
            },
            "LAND": {
                "prefix": "LAND-",
                "required": ["id", "item_id", "land_type", "aspect"],
                "enum_fields": {"land_type": LAND_TYPES, "aspect": LAND_ASPECTS},
            },
        },
    },
    # ---- C1 任职层 ----
    "appts": {
        "dir": "_layers/appts",
        "id_prefix": "APPT-",
        "kind": "list",
        "per": "global",
        "name": "C1 任职层",
        "required": ["id", "item_id", "office", "person", "reign", "status"],
        "enum_fields": {"status": APPT_STATUS, "reign": list(REIGN_ORDER)},
    },
    # ---- TME 沿革层 ----
    "tmes": {
        "dir": "_layers/tmes",
        "id_prefix": "TME-",
        "kind": "list",
        "per": "global",
        "name": "TME 沿革层",
        "required": ["id", "item_id", "office", "category", "reign"],
        "enum_fields": {"category": TME_CATEGORIES, "reign": list(REIGN_ORDER)},
    },
    # ---- C9 论说层 ----
    "opns": {
        "dir": "_layers/opns",
        "id_prefix": "OPN-",
        "kind": "list",
        "per": "global",
        "name": "C9 论说层",
        "required": ["id", "item_id", "text", "opn_type", "stance"],
        "enum_fields": {"opn_type": OPN_TYPES, "stance": OPN_STANCES},
    },
}

# C16 总账树是 LAYER_SPECS["structs"].subtypes["LED"] 的派生视图，另存
LEDGER_TREE_FILE = DATA_DIR / "ledger_tree.json"
LEDGER_FLAT_FILE = DATA_DIR / "ledger_flat.csv"

# 跨层索引（SKILL §13.1：项目根 `_kg_join.json` + `_kg_join_flat.csv`）
KG_JOIN_FILE = BASE_DIR / "_kg_join.json"
KG_JOIN_FLAT_FILE = BASE_DIR / "_kg_join_flat.csv"

# 实体引用索引（build_entity_links.py 产物：ENT → 各层记录 ID 引用）
ENT_LINKS_FILE = LAYERS_DIR / "ents" / "_ent_links.json"

# =============================================================================
# cn2int —— 中文数字 → int（坑 #64：必须锚定最长数字串，禁止逐字翻译）
# =============================================================================

_CN_DIGIT = {
    "零": 0,
    "〇": 0,
    "○": 0,
    "一": 1,
    "壹": 1,
    "二": 2,
    "贰": 2,
    "貳": 2,
    "两": 2,
    "兩": 2,
    "三": 3,
    "叁": 3,
    "參": 3,
    "四": 4,
    "肆": 4,
    "五": 5,
    "伍": 5,
    "六": 6,
    "陆": 6,
    "陸": 6,
    "七": 7,
    "柒": 7,
    "八": 8,
    "捌": 8,
    "九": 9,
    "玖": 9,
}
_CN_UNIT = {
    "十": 10,
    "拾": 10,
    "百": 100,
    "佰": 100,
    "千": 1000,
    "仟": 1000,
    "万": 10000,
    "萬": 10000,
    "亿": 100000000,
}

# 贪婪匹配最长的中文数字串（含 万/亿/千/百/十 及 有奇/馀 前的量）
# ★ 关键排除：`两` 既是数词 2 又是重量单位「两」。在食货志账目中，`两` 几乎总是
#   货币单位（…万两 / …馀两），故此处 **不把 `两` 当数词**，避免「万两」→10002。
#   数词 2 一律写作 二/贰，可安全收录。
_CN_DIGIT_NUM = {k: v for k, v in _CN_DIGIT.items() if k not in ("两", "兩")}
_CN_CHARS = "".join(_CN_DIGIT_NUM) + "".join(_CN_UNIT)

_CN_NUM_RE = re.compile(
    r"[零〇○一壹二贰貳三叁參四肆五伍六陆陸七柒八捌九玖十拾百佰千仟万萬亿]+"
)

_CN_CHARS = "".join(_CN_DIGIT) + "".join(_CN_UNIT)


class Cn2IntError(ValueError):
    """中文数字解析失败。"""


def cn2int(s: str) -> int:
    """单个中文数字串 → int。必须整串消费，否则抛错（不静默返回 0）。

    >>> cn2int("一千"); cn2int("万"); cn2int("四百三十万"); cn2int("十八万九千")
    1000 10000 4300000 189000
    """
    if isinstance(s, int):
        return s
    t = (s or "").strip()
    if not t:
        raise Cn2IntError("空串")
    if t.isdigit():
        return int(t)
    if any(c not in _CN_CHARS for c in t):
        raise Cn2IntError(f"含非中文数字字符: {t!r}")

    total, section, number = 0, 0, 0
    for ch in t:
        if ch in _CN_DIGIT:
            number = _CN_DIGIT[ch]
        elif ch in ("十", "拾"):
            section += (number or 1) * 10
            number = 0
        elif ch in ("百", "佰"):
            section += (number or 1) * 100
            number = 0
        elif ch in ("千", "仟"):
            section += (number or 1) * 1000
            number = 0
        elif ch in ("万", "萬"):
            # 「万」单独出现（如「京运年例银万两」）系数为 1，非 0
            section = (section + number or 1) * 10000
            total += section
            section, number = 0, 0
        elif ch in ("亿",):
            section = (section + number or 1) * 100000000
            total += section
            section, number = 0, 0
        else:  # 零/〇
            number = 0
    return total + section + number


def cn2int_in_text(text: str) -> List[int]:
    """按最长数字串抽取文本中全部中文数字（顺序返回）。"""
    return [cn2int(m.group(0)) for m in _CN_NUM_RE.finditer(text)]


# =============================================================================
# 数量解析（食货志钱粮专用）
# =============================================================================

# 数字：阿拉伯 或 中文数字串；后缀：馀/有奇/余
_NUM_PART = r"(?:\d+(?:\.\d+)?|[" + _CN_CHARS + r"]+)"
_QM = r"(?:馀|余|有奇|有餘|有馀)?"
_PAREN = r"(?:\（[^）]*\）|\（[^）]*\）)?"
# 单位表（长单位优先，防「石」吃掉「万石」类误切）
_UNIT_ALT = "|".join(sorted(set(QUAN_UNITS), key=len, reverse=True))

_QUAN_RE = re.compile(
    r"(?P<num>" + _NUM_PART + r")"
    r"(?P<qi>馀|余|有奇)?"
    r"(?P<unit>" + _UNIT_ALT + r")"
    r"(?P<tail>有奇|馀|余)?"
    r"(?P<paren>" + _PAREN + r")?"
)


def parse_amount(num_s: str) -> Tuple[int, bool]:
    """数字串 → (数值, 是否约数)。'馀'/'有奇' 由调用方标 approx。"""
    if num_s.isdigit():
        return int(num_s), False
    return cn2int(num_s), False


def unit_dimension(unit: str) -> str:
    for dim, units in QUAN_UNIT_DIMENSIONS.items():
        if unit in units:
            return dim
    return "未明"


# =============================================================================
# 术语归一（食货志专有）
# =============================================================================

# 屯粮 / 屯粮料 / 民运粮料 / 折色粮料草银 … 需映射到 (origin, form, 品类)
# 顺序敏感：长词优先。
LEDGER_TERM_RULES: List[Tuple[str, Dict[str, Any]]] = [
    # —— 屯田系 ——
    # 「屯田及民运草」双源合并：origin 记 屯田，origin_alt 记 民运（不臆断比例）
    (
        "屯田及民运本色草",
        {
            "origin": "屯田",
            "origin_alt": "民运",
            "form": "本色",
            "object": "草",
            "combined": True,
        },
    ),
    (
        "屯田及民运草",
        {
            "origin": "屯田",
            "origin_alt": "民运",
            "form": "本色",
            "object": "草",
            "combined": True,
        },
    ),
    ("屯粮料", {"origin": "屯田", "form": "本色", "object": "粮料"}),
    ("屯粮本色", {"origin": "屯田", "form": "本色", "object": "粮"}),
    ("屯粮折色银", {"origin": "屯田", "form": "折色", "object": "粮"}),
    ("屯粮", {"origin": "屯田", "form": "本色", "object": "粮"}),
    ("屯草折银", {"origin": "屯田", "form": "折色", "object": "草"}),
    # 裸「草」（山西：草九万五千馀束）——承 屯田 本色草
    ("草", {"origin": "屯田", "form": "本色", "object": "草"}),
    ("荒田粮", {"origin": "荒田", "form": "本色", "object": "粮"}),
    # —— 民运系 ——
    ("民运本色米麦", {"origin": "民运", "form": "本色", "object": "米麦"}),
    ("民运本色米豆", {"origin": "民运", "form": "本色", "object": "米豆"}),
    ("民运本色粮料", {"origin": "民运", "form": "本色", "object": "粮料"}),
    ("民运本色米", {"origin": "民运", "form": "本色", "object": "米"}),
    # 宁夏：民运本色粮千馀石（无「料」字）
    ("民运本色粮", {"origin": "民运", "form": "本色", "object": "粮"}),
    ("民运粮布折银", {"origin": "民运", "form": "折色", "object": "粮布"}),
    (
        "民运折色粮料草布花银",
        {"origin": "民运", "form": "折色", "object": "粮料草布花"},
    ),
    ("民运折色银", {"origin": "民运", "form": "折色", "object": "银"}),
    ("民运粮料", {"origin": "民运", "form": "本色", "object": "粮料"}),
    ("民运银", {"origin": "民运", "form": "折色", "object": "银"}),
    ("民运草", {"origin": "民运", "form": "本色", "object": "草"}),
    ("民壮工食银", {"origin": "工食", "form": "折色", "object": "银"}),
    # —— 盐系 ——
    ("两淮、长芦、河东盐引银", {"origin": "盐引", "form": "折色", "object": "银"}),
    ("淮、芦盐引银", {"origin": "盐引", "form": "折色", "object": "银"}),
    ("淮、芦盐", {"origin": "盐引", "form": "本色", "object": "盐"}),
    ("淮、浙、山东盐引银", {"origin": "盐引", "form": "折色", "object": "银"}),
    ("淮、浙盐引银", {"origin": "盐引", "form": "折色", "object": "银"}),
    # 辽东：两淮、山东盐引银三万九千馀两
    ("两淮、山东盐引银", {"origin": "盐引", "form": "折色", "object": "银"}),
    ("两淮盐引银", {"origin": "盐引", "form": "折色", "object": "银"}),
    ("盐引银", {"origin": "盐引", "form": "折色", "object": "银"}),
    ("河东盐课银", {"origin": "盐课", "form": "折色", "object": "银"}),
    ("盐钞银", {"origin": "盐钞", "form": "折色", "object": "银"}),
    # —— 京运系 ——
    ("京运年例银", {"origin": "京运", "form": "折色", "object": "银"}),
    ("京运银", {"origin": "京运", "form": "折色", "object": "银"}),
    ("漕粮", {"origin": "漕粮", "form": "本色", "object": "粮"}),
    # —— 地亩系 ——
    ("地亩马草折色银", {"origin": "地亩", "form": "折色", "object": "马草"}),
    ("地亩牛具银", {"origin": "地亩", "form": "折色", "object": "银"}),
    ("地亩银", {"origin": "地亩", "form": "折色", "object": "银"}),
    ("牛具银", {"origin": "牛具", "form": "折色", "object": "银"}),
    ("折草银", {"origin": "屯田", "form": "折色", "object": "草"}),
    ("折色粮料草银", {"origin": "民运", "form": "折色", "object": "粮料草"}),
    # —— 赏恤系 ——
    ("抚赏银", {"origin": "抚赏", "form": "折色", "object": "银"}),
    ("犒军银", {"origin": "犒军", "form": "折色", "object": "银"}),
    ("犒赏银", {"origin": "犒赏", "form": "折色", "object": "银"}),
    ("山东民兵工食银", {"origin": "工食", "form": "折色", "object": "银"}),
    ("遵化营民壮工食银", {"origin": "工食", "form": "折色", "object": "银"}),
    # ★ 裸「折色银」：原文承前省略主语，无法从短语本身判定属 屯田 还是 民运。
    #   保守归 未明 并标 ambiguous=True（由 build_ledger 依上下文补 note），
    #   禁止臆断为 其他（会污染 收入类别 汇总）。
    ("折色银", {"origin": "未明", "form": "折色", "object": "银", "ambiguous": True}),
    (
        "折色粮料草布花银",
        {"origin": "未明", "form": "折色", "object": "银", "ambiguous": True},
    ),
]


def match_ledger_term(label: str) -> Optional[Dict[str, Any]]:
    """把账目短语归类为 (origin, form, object)。长词优先。"""
    for key, val in LEDGER_TERM_RULES:
        if label.startswith(key):
            return dict(val, matched_key=key)
    return None


# =============================================================================
# 读写与护栏
# =============================================================================


def load_json(path: Path, default: Any = None) -> Any:
    if not Path(path).exists():
        if default is not None:
            return default
        raise FileNotFoundError(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  [写] {p.relative_to(BASE_DIR)}  ({_size_of(data)})")


def save_csv(path: Path, rows: Iterable[Dict[str, Any]], fields: List[str]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"  [写] {p.relative_to(BASE_DIR)}  ({len(rows)} 行 × {len(fields)} 列)")


def _size_of(data: Any) -> str:
    if isinstance(data, (list, dict)):
        return f"{len(data)} 条"
    return f"{type(data).__name__}"


def layer_dir(key: str) -> Path:
    return BASE_DIR / LAYER_SPECS[key]["dir"]


def layer_file(
    key: str, vol_seq: Optional[int] = None, subtype: Optional[str] = None
) -> Path:
    spec = LAYER_SPECS[key]
    d = layer_dir(key)
    if spec["kind"] == "registry":
        return d / (f"{subtype}.json" if subtype else "structs.json")
    if spec["per"] == "volume":
        return d / f"{vol_seq:02d}_{key}.json"
    return d / f"{key}.json"


def vol_items(volume: str, registry: Optional[Dict[str, Any]] = None) -> List[str]:
    """返回某卷全部 item_id，按 no 排序。"""
    reg = registry if registry is not None else load_json(REGISTRY_FILE)
    return sorted(
        (k for k, v in reg.items() if v["volume"] == volume), key=lambda k: reg[k]["no"]
    )


def guard_no_legacy_dirs() -> None:
    """护栏：禁止任何层输出再落到 `layers/`（无下划线）与 `entities/`。

    `layers/` 的 6 个遗留文件已被 `_layers/` 取代；`entities/entities.json`
    已被 `_layers/ents/` 取代。本护栏只警告，不删除（保留追溯）。
    """
    for d in FROZEN_DIRS:
        if not d.exists():
            continue
        files = [p for p in d.rglob("*") if p.is_file()]
        if files:
            print(
                f"  [护栏] 历史目录仍存在且非空：{d.relative_to(BASE_DIR)}"
                f"（{len(files)} 文件）—— 层输出请写 _layers/，勿再引用此处",
                file=sys.stderr,
            )


def check_enum(value: Any, allowed: Iterable[str]) -> bool:
    """枚举校验：允许 list（多值）或单值。"""
    allowed = set(allowed)
    if value is None or value == "":
        return True
    if isinstance(value, (list, tuple, set)):
        return all(v in allowed for v in value)
    return value in allowed


def normalize_entity_type(t: str) -> str:
    return ENTITY_TYPE_ALIASES.get(t, t)


def vol_seq_of(volume: str) -> int:
    for k, v in VOLUME_NAMES.items():
        if v == volume:
            return k
    raise KeyError(volume)
