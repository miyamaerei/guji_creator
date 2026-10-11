# -*- coding: utf-8 -*-
"""书注册表：一本书 = 一个「枚举后端」+ 一组「层产物扫描规格」。

P0 只读阶段，本表是唯一需要人工维护的地方。新增一本书只需在此加一项。

字段说明
--------
book            目录名（相对仓库根）
title           书名，用于报告可读化
enum_backend    枚举定义来源，见 adapters.EnumBackend
                 - "spec"     : 单注册表变量，值为 {枚举名: spec}，spec 内含 tree/canonical/alias
                 - "flat"     : 若干平铺的 *_TYPES / *_STYLES 等大写常量（dict 或 set）
                 - "none"     : 无单点枚举（值内嵌在打包器里）→ drift 只能报「无基准」
enum_path       枚举文件相对路径（相对书目录）
enum_var        spec 形态下的注册表名
enum_names      flat 形态下要抓取的变量名（不填则按 ENUM_VAR_PATTERNS 自动发现）
layers          层产物扫描规格，见 adapters.scan_layers
                 globs     : 文件通配，{layer} 占位符会被替换为 *（用于按层归类）
                 container : 记录列表所在的顶层/嵌套键（按序尝试）
                 nested    : "dict_of_layers" 表示 container 取到的是 {层名: [记录]}
schemas         实例 schemas.md 快照路径（相对仓库根），用于 enum_sync 三处比对
"""

import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

FACTORY_DIR = os.path.join(REPO_ROOT, "Skills", "00-book-knowledge-factory")
FACTORY_ENUM_LIB = os.path.join(FACTORY_DIR, "references", "enum-library.md")
FACTORY_CHANGELOG = os.path.join(FACTORY_DIR, "references", "enum-changelog.md")
FACTORY_PENDING = os.path.join(FACTORY_DIR, "references", "pending-review.md")

# flat 形态自动发现变量名时的后缀模式
ENUM_VAR_PATTERNS = (
    "_TYPES", "_STYLES", "_STATUS", "_STANCES", "_MODALS",
    "_CATEGORIES", "_CATEGORY", "_KINDS", "_LEVELS", "_CLASSES",
    "_MODE", "_TYPE", "_STANCE",
)
# 这些大写常量不是枚举，自动发现时排除
NON_ENUM_VAR_SUFFIX = (
    "_VERSION", "_PATTERN", "_FIELDS", "_EMPTY_VOLUMES", "_PREFIXES",
    "_PREFIX_VERSION", "_ORDER", "_ALIAS", "_INDEX",
)

BOOKS = {
    "kezuozhuiyu-kb": {
        "title": "《客座赘语》",
        "enum_backend": "none",
        "enum_path": None,
        "layers": {
            "globs": ["_layers/*.json"],
            "container": ["records"],
            "nested": None,
        },
        "schemas": "Skills/04-kezuozhuiyu-knowledge/references/schemas.md",
    },
    "wuzazu-kb": {
        "title": "《五杂俎》",
        "enum_backend": "spec",
        "enum_path": "_kg_enums.py",
        "enum_var": "BASE_ENUMS",
        "layers": {
            "globs": ["_layers/*.json"],
            "container": ["records"],
            "nested": None,
        },
        "schemas": "Skills/03-wuzazu-knowledge/references/schemas.md",
    },
    "shuidongriji-kb": {
        "title": "《水东日记》",
        "enum_backend": "flat",
        "enum_path": "_kg_enums.py",
        "enum_names": None,
        "layers": {
            "globs": ["data/*/*.json"],
            "container": ["records", "annotations"],
            "nested": None,
        },
        "schemas": "Skills/01-shuidong-riji-knowledge/references/schemas.md",
    },
    "xinguanguifan-kb": {
        "title": "《新官轨范》",
        "enum_backend": "flat",
        "enum_path": "_kg_enums.py",
        "enum_names": None,
        "layers": {
            "globs": [
                "新官轨范_标注/*.json",
                "新官轨范_事件_ai/*.json",
                "新官轨范_规则_ai/*.json",
                "新官轨范_流程_ai/*.json",
                "新官轨范_结构_ai/*.json",
            ],
            "container": ["entities", "records", "items", "annotations"],
            "nested": None,
            # 新官的层产物按「中文目录」分装，文件名不含层名 → 需显式映射
            "dir_layer_map": {
                "新官轨范_标注": "ent",
                "新官轨范_事件_ai": "evt",
                "新官轨范_规则_ai": "rule",
                "新官轨范_流程_ai": "proc",
                "新官轨范_结构_ai": "struct",
            },
        },
        "schemas": None,
    },
    "qubian_kb": {
        "title": "《蘧编》",
        "enum_backend": "none",
        "enum_path": None,
        "layers": {
            "globs": ["_kg_*.json"],
            "container": ["records"],
            "nested": "dict_of_layers",
        },
        "schemas": "Skills/02-qubian-knowledge/references/schemas.md",
    },
    "xianjinyifeng-kb": {
        "title": "《先进遗风》",
        "enum_backend": "spec",
        "enum_path": "05-xianjinyifeng-knowledge/scripts/_kg_enums.py",
        "enum_var": "ENUM_REGISTRY",
        "layers": {
            "globs": ["05-xianjinyifeng-knowledge/data/_layers/*.json"],
            "container": ["records"],
            "nested": None,
        },
        "schemas": "xianjinyifeng-kb/05-xianjinyifeng-knowledge/references/schemas.md",
    },
}

# 层名 → 工厂库枚举名的归一映射。
# 目的：drift 时能拿「层实际取值」去比对「工厂定义的枚举」，即便两边命名不同。
# 左侧是层名（文件名前缀或嵌套子键），右侧是工厂库 §1.x 的枚举名（去 _TYPES 后缀后的主干）。
LAYER_TO_ENUM = {
    "ent": "ENTITY",
    "evt": "EVENT",
    "event": "EVENT",
    "appt": "APPT",
    "obj": "OBJ",
    "cus": "CUS",
    "nam": "NAM",
    "lit": "LIT",
    "ming": "MING",
    "geo": "GEO",
    "rel": "REL",
    "opn": "OPN",
    "trl": "TRL",
    "cit": "CIT",
    "reg": "REG",
    "ents": "ENTITY",
    "evts": "EVENT",
    "appts": "APPT",
    "rels": "REL",
    "lits": "LIT",
    "mems": "MING",
    "chrs": "CHR",
    "trls": "TRL",
    "rule": "RULE",
    "proc": "PROC",
    "struct": "STRUCT",
    "official": "ENTITY",
}

# 同一语义在工厂库与实例里可能叫不同名字，做一张别名表（双向归一到左侧主干）
ENUM_KEY_ALIASES = {
    "ENTITY": ("ENTITY", "ENT", "ENTITIE"),
    "EVENT": ("EVENT", "EVT"),
    "APPT": ("APPT", "APPOINTMENT", "APPT_STATUS"),
    "OBJ": ("OBJ", "OBJECT", "ARTIFACT"),
    "CUS": ("CUS", "CUSTOM"),
    "NAM": ("NAM", "NAME"),
    "LIT": ("LIT", "LITERATURE"),
    "MING": ("MING",),
    "GEO": ("GEO", "GEOGRAPHY"),
    "REL": ("REL", "RELATION"),
    "OPN": ("OPN", "OPINION"),
    "TRL": ("TRL", "TRANSLATION"),
    "CIT": ("CIT", "CITATION"),
    "REG": ("REG", "REGULATION"),
    "RULE": ("RULE",),
    "CHR": ("CHR", "CHRONICLE"),
    "PROC": ("PROC", "PROCESS"),
    "STRUCT": ("STRUCT", "STRUCTURE"),
    "VOL": ("VOL", "VOLUME"),
    "ROLE": ("ROLE",),
    "MECH": ("MECH", "MECHANISM"),
    "MODAL": ("MODAL", "RULE_MODAL"),
}

# 兜底值：枚举里必须有「无法归入时」的出口，否则执行期必然自造值（pitfalls #27）
FALLBACK_VALUES = {"其他", "unknown", "待定", "杂项", "未详"}

# 只对「归类型」枚举检查兜底值。
# 封闭分类型枚举（任职状态、论说立场、关系类型、翻译风格、卷阅读模式…）取值天然穷举，
# 不存在「无法归类」的情形，要求它们带兜底值只会制造假警报。
NEEDS_FALLBACK = {
    "ENTITY", "EVENT", "OBJ", "CUS", "NAM", "LIT", "MING", "GEO",
    "REG", "CHR", "CIT", "STRUCT", "PROC",
}


def canon_key(name):
    """把任意枚举名归一到主干：ENTITY_TYPES→ENTITY、EVT_TYPES→EVENT、ent→ENTITY。"""
    if not name:
        return None
    s = str(name).strip().upper()
    # 注意：长后缀必须在前（_TYPES 先于 _TYPE），否则只剥掉一半
    # 刻意**不**剥 _CONTEXT / _DIRECTION：`citation_type` 与 `citation_context`
    # 是两个不同枚举，都剥成 CITATION 会互相覆盖
    for suffix in ("_TYPES", "_TYPE", "_ENUMS", "_ENUM", "_STYLES", "_STATUS",
                   "_STANCES", "_STANCE", "_MODALS", "_CATEGORIES", "_CATEGORY",
                   "_KINDS", "_LEVELS", "_CLASSES", "_MODE", "_SET", "_VALUES"):
        if s.endswith(suffix):
            s = s[: -len(suffix)]
            break
    for main, aliases in ENUM_KEY_ALIASES.items():
        if s == main or s in aliases:
            return main
    return s


def enum_key_for_layer(layer):
    """层名 → 工厂库枚举主干名。"""
    if not layer:
        return None
    key = str(layer).strip().lower().rstrip("s") or str(layer).strip().lower()
    if str(layer).lower() in LAYER_TO_ENUM:
        return LAYER_TO_ENUM[str(layer).lower()]
    if key in LAYER_TO_ENUM:
        return LAYER_TO_ENUM[key]
    return canon_key(layer)


def book_dir(book):
    return os.path.join(REPO_ROOT, book)


def list_books():
    return sorted(BOOKS)
