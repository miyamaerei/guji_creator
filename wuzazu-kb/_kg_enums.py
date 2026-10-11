# -*- coding: utf-8 -*-
"""《五杂俎》知识工程 —— 枚举单点文件（enums 唯一权威点）。

口径（skill `wuzazu-knowledge` §13 + references/schemas.md §1）：
  1. 所有枚举 = 基准值继承（工厂 enum-library.md 树状基准库快照）+ 本书归纳增量；
  2. 校验模式 = 收集 - 报告 - 暂存：未知值只入 pending 表，不报错、不中断；
  3. 新增值必须走 register_version()：version+1 → 回溯存量 → 落盘证据；
  4. 值多时按树组织（顶层大类封闭 → 子类 → 叶子，深度 ≤3，父类计数 = 子类求和）。

本文件不 import `_kg_pack_base`，保持"叶子"地位，任何模块都可以安全引用。
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENUM_STATE_PATH = ROOT / "_build" / "_kg_enums_state.json"
PENDING_PATH = ROOT / "_build" / "_enums_pending.json"

ENUM_VERSION = 1

# --------------------------------------------------------------------------
# 1. 基准快照（照 references/schemas.md 逐层固化；权威源 = 工厂 enum-library.md）
#    alias 表用于"别名 → 规范值"归一（如 政事→朝政、office→official）。
# --------------------------------------------------------------------------

BASE_ENUMS: dict[str, dict] = {
    # ── L1 实体类型（§3；词形归一 office→official、book→work）
    "entity_type": {
        "version": 1,
        "tree": {
            "人物": ["person", "人物"],
            "地理": ["place", "地名"],
            "文献": ["work", "书名", "文献"],
            "职官": ["official", "职官"],
            "时间": ["era", "年号朝代", "年号", "朝代"],
            "名物": ["object", "名物"],
            "生物": ["animal", "动物", "plant", "植物"],
            "饮食": ["food", "饮食"],
            "待定": ["unknown", "类型待定"],
        },
        "canonical": ["person", "place", "work", "official", "era",
                      "object", "animal", "plant", "food", "unknown"],
        "alias": {"office": "official", "book": "work",
                  "人物": "person", "地名": "place", "书名": "work",
                  "职官": "official", "年号朝代": "era", "年号": "era",
                  "朝代": "era", "名物": "object", "动物": "animal",
                  "植物": "plant", "饮食": "food", "类型待定": "unknown"},
    },
    # ── 事件类型（§4；跨书动态库规范全集 22 值 + 兜底"其他"）
    "event_type": {
        "version": 1,
        "tree": {
            "政治": ["朝政", "政变", "人事任免", "弹劾", "礼仪", "建言", "巡查监察"],
            "军事": ["军事", "军政", "边事", "缉捕防盗"],
            "文教": ["科举", "文事"],
            "天灾": ["灾异", "疾疫", "御灾赈济"],
            "社会": ["经济", "司法", "祭祀", "轶事", "神异传说"],
            "兜底": ["其他"],
        },
        "canonical": ["朝政", "政变", "军事", "军政", "边事", "人事任免", "弹劾",
                      "礼仪", "科举", "文事", "建言", "灾异", "轶事", "祭祀",
                      "经济", "司法", "神异传说", "疾疫", "御灾赈济",
                      "缉捕防盗", "巡查监察", "其他"],
        "alias": {"政事": "朝政", "军务": "军事", "科第": "科举", "刑罚": "司法"},
    },
    # ── 人物关系（§5；基准库 12 值）
    "relation_type": {
        "version": 1,
        "tree": {
            "血缘": ["父子亲属", "姻亲"],
            "师承": ["师生"],
            "仕宦": ["举荐", "同僚", "上下级", "同科", "弹劾"],
            "地域": ["同乡"],
            "对立": ["恩怨", "敌对"],
            "兜底": ["其他"],
        },
        "canonical": ["师生", "举荐", "弹劾", "同僚", "姻亲", "同乡", "同科",
                      "父子亲属", "恩怨", "敌对", "上下级", "其他"],
        "alias": {"主从": "上下级"},
    },
    "relation_direction": {
        "version": 1,
        "tree": {"方向": ["单向", "双向", "未明"]},
        "canonical": ["单向", "双向", "未明"],
        "alias": {},
    },
    # ── 名录类型（§6；基准库 12 值，本书常用子集）
    "nam_category": {
        "version": 1,
        "tree": {
            "人物": ["长寿名录", "巨富名录", "异相名录", "官员题名", "同僚题名"],
            "事件": ["灾异名录", "迁谪录"],
            "科举": ["科第名录"],
            "名物": ["器物名录"],
            "文献": ["谱牒", "题名记"],
            "兜底": ["其他"],
        },
        "canonical": ["长寿名录", "巨富名录", "异相名录", "灾异名录", "科第名录",
                      "器物名录", "官员题名", "同僚题名", "迁谪录", "谱牒",
                      "题名记", "其他"],
        "alias": {},
    },
    # ── 引用方式 / 引用目的（§7；基准库 §1.15）
    "citation_type": {
        "version": 1,
        "tree": {"引用": ["直引", "转引", "泛引", "暗用", "考辨"]},
        "canonical": ["直引", "转引", "泛引", "暗用", "考辨"],
        "alias": {},
    },
    "citation_context": {
        "version": 1,
        "tree": {"目的": ["立论", "证俗", "考源", "反驳", "补遗", "其他"]},
        "canonical": ["立论", "证俗", "考源", "反驳", "补遗", "其他"],
        "alias": {},
    },
    # ── 名物类别（§8；基准库 §1.6）
    "obj_category": {
        "version": 1,
        "tree": {
            "人造": ["器物", "材料", "建筑", "服饰"],
            "自然": ["动物", "植物", "珍宝"],
            "生活": ["饮食"],
            "兜底": ["其他"],
        },
        "canonical": ["器物", "动物", "植物", "饮食", "珍宝", "材料",
                      "建筑", "服饰", "其他"],
        "alias": {},
    },
    # ── 方言风俗类型（§9；基准库 §1.7）
    "cus_type": {
        "version": 1,
        "tree": {
            "语言": ["方言词", "谚语"],
            "行为": ["民俗", "禁忌", "节令"],
            "物产": ["物产习俗"],
            "兜底": ["其他"],
        },
        "canonical": ["方言词", "民俗", "禁忌", "谚语", "节令", "物产习俗", "其他"],
        "alias": {},
    },
    # ── 作者立场（§10；基准库 §1.8）
    "opn_stance": {
        "version": 1,
        "tree": {"态度": ["肯定", "否定", "怀疑", "讽刺", "中立"]},
        "canonical": ["肯定", "否定", "怀疑", "讽刺", "中立"],
        "alias": {},
    },
    # ── 涉明类型（§11；基准库 §1.9）
    "ming_category": {
        "version": 1,
        "tree": {
            "制度": ["朝政", "科举", "制度"],
            "人事": ["人物"],
            "社会": ["风俗", "灾异"],
            "亲历": ["亲历见闻"],
            "兜底": ["其他"],
        },
        "canonical": ["朝政", "人物", "科举", "风俗", "灾异", "亲历见闻", "制度", "其他"],
        "alias": {},
    },
    # ── 任职状态（§12；基准库 §1.10，12 值，本书固定 9 + 兜底）
    "appt_status": {
        "version": 1,
        "tree": {
            "在任": ["现任", "兼领", "暂代"],
            "变动": ["升迁", "贬谪", "罢黜", "起复"],
            "荣誉": ["追赠"],
            "非任": ["致仕", "世袭", "举荐"],
            "兜底": ["未明"],
        },
        "canonical": ["现任", "致仕", "升迁", "贬谪", "罢黜", "兼领", "暂代",
                      "追赠", "起复", "世袭", "举荐", "未明"],
        "alias": {},
    },
    # ── 翻译风格（§13；基准库 §1.13）
    "trl_style": {
        "version": 1,
        "tree": {"译法": ["直译", "意译", "注释性翻译"]},
        "canonical": ["直译", "意译", "注释性翻译"],
        "alias": {},
    },
    # ── 卷阅读模式（§14；本书定制，基准库 §1.14 可组合复用）
    "volume_mode": {
        "version": 1,
        "tree": {
            "内容主导": ["论理优先", "风土优先", "人物优先", "名物优先",
                         "世情优先", "轶事优先", "灾异优先"],
            "通用": ["均衡全层"],
        },
        "canonical": ["论理优先", "风土优先", "人物优先", "名物优先", "世情优先",
                      "轶事优先", "灾异优先", "均衡全层"],
        "alias": {},
    },
}

# 本实例带别名映射的枚举（本书初版值 → 规范值；用于读旧数据时归一）
INSTANCE_ALIAS: dict[str, dict[str, str]] = {
    "event_type": {"政事": "朝政", "军务": "军事", "科第": "科举", "刑罚": "司法"},
}

# 源数据/产物字段名 -> 枚举名（层配置 enum_fields 通过本表解析）
FIELD_TO_ENUM: dict[str, str] = {
    "entity.type": "entity_type",
    "event.type": "event_type",
    "rel.relation_type": "relation_type",
    "rel.direction": "relation_direction",
    "nam.category": "nam_category",
    "cit.citation_type": "citation_type",
    "cit.context": "citation_context",
    "obj.category": "obj_category",
    "cus.type": "cus_type",
    "opn.stance": "opn_stance",
    "ming.category": "ming_category",
    "appt.status": "appt_status",
    "trl.style": "trl_style",
}

# --------------------------------------------------------------------------
# 2. 运行时状态（version / 新增值 / 待核）
# --------------------------------------------------------------------------

_STATE: dict | None = None
_PENDING: list[dict] = []
_PENDING_SEEN: set[tuple[str, str]] = set()


def _load_state() -> dict:
    global _STATE
    if _STATE is not None:
        return _STATE
    if ENUM_STATE_PATH.exists():
        with open(ENUM_STATE_PATH, "r", encoding="utf-8") as fp:
            _STATE = json.load(fp)
    else:
        _STATE = {"enums": {}, "updated_at": None}
    for name, spec in BASE_ENUMS.items():
        _STATE["enums"].setdefault(name, {"version": spec["version"], "added": []})
    return _STATE


def save_state() -> None:
    state = _load_state()
    state["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ENUM_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = ENUM_STATE_PATH.with_name(ENUM_STATE_PATH.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as fp:
        json.dump(state, fp, ensure_ascii=False, indent=2)
    os.replace(tmp, ENUM_STATE_PATH)


def flush_pending() -> None:
    """暂存表落盘（收集 - 报告 - 暂存中的"暂存"）。"""
    if not _PENDING:
        return
    PENDING_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if PENDING_PATH.exists():
        with open(PENDING_PATH, "r", encoding="utf-8") as fp:
            existing = json.load(fp)
    known = {(p["enum"], p["value"]) for p in existing}
    for item in _PENDING:
        if (item["enum"], item["value"]) not in known:
            existing.append(item)
            known.add((item["enum"], item["value"]))
    tmp = PENDING_PATH.with_name(PENDING_PATH.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as fp:
        json.dump(existing, fp, ensure_ascii=False, indent=2)
    os.replace(tmp, PENDING_PATH)


# --------------------------------------------------------------------------
# 3. 查询 / 归一 / 校验 API
# --------------------------------------------------------------------------


def enum_names() -> list[str]:
    return sorted(BASE_ENUMS.keys())


def canonical_values(name: str) -> list[str]:
    spec = BASE_ENUMS.get(name)
    if spec is None:
        raise KeyError(f"未登记枚举：{name}")
    return list(spec["canonical"])


def alias_map(name: str) -> dict[str, str]:
    merged = dict(BASE_ENUMS.get(name, {}).get("alias", {}))
    merged.update(INSTANCE_ALIAS.get(name, {}))
    merged.update({v: v for v in canonical_values(name)})
    return merged


def normalize_value(name: str, value) -> str:
    """别名/词形归一到规范值；未登记原样返回（由 validate() 决定是否入 pending）。"""
    if value is None:
        return ""
    text = str(value).strip()
    if not text:
        return ""
    return alias_map(name).get(text, text)


def is_valid(name: str, value) -> bool:
    return normalize_value(name, value) in canonical_values(name)


def validate(name: str, value, where: str = "") -> tuple[str, str | None]:
    """返回 (归一值, 未知值或 None)。未知值自动进 pending（不中断执行）。"""
    norm = normalize_value(name, value)
    if norm and norm not in canonical_values(name):
        key = (name, norm)
        if key not in _PENDING_SEEN:
            _PENDING_SEEN.add(key)
            _PENDING.append({
                "enum": name,
                "value": norm,
                "raw": value,
                "where": where,
                "at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
        return norm, norm
    return norm, None


def register_version(name: str, value: str, evidence: str) -> int:
    """新增值回填：version+1 → 记录证据 → 回溯存量（重跑各层即生效）。"""
    state = _load_state()
    spec = state["enums"].setdefault(name, {"version": 1, "added": []})
    spec.setdefault("added", []).append({
        "value": value,
        "evidence": evidence,
        "at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    spec["version"] = int(spec.get("version", 1)) + 1
    BASE_ENUMS.setdefault(name, {"version": 1, "tree": {}, "canonical": [], "alias": {}})
    if value not in BASE_ENUMS[name]["canonical"]:
        BASE_ENUMS[name]["canonical"].append(value)
        BASE_ENUMS[name].setdefault("tree", {}).setdefault("本书新增", []).append(value)
    save_state()
    return spec["version"]


def tree_report() -> list[dict]:
    """树状枚举报告：顶层大类 → 子类 → 叶子（父类计数 = 子类求和）。"""
    rows: list[dict] = []
    for name in enum_names():
        spec = BASE_ENUMS[name]
        for parent, leaves in spec.get("tree", {}).items():
            for leaf in leaves:
                rows.append({
                    "enum": name,
                    "parent": parent,
                    "value": normalize_value(name, leaf),
                    "is_canonical": normalize_value(name, leaf) in spec["canonical"],
                })
    return rows


def dump_summary() -> dict:
    return {
        "enums": len(BASE_ENUMS),
        "values": sum(len(canonical_values(n)) for n in enum_names()),
        "pending": len(_PENDING),
        "version": ENUM_VERSION,
    }


if __name__ == "__main__":
    from _kg_pack_base import write_json, BUILD_DIR  # 本地调试用

    write_json(BUILD_DIR / "_kg_enums_tree.json",
               {"generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "summary": dump_summary(), "tree": tree_report()})
    print(json.dumps(dump_summary(), ensure_ascii=False, indent=2))
