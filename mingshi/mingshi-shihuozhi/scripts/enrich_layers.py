#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enrich TME / APPT / procs —— 引用写回与字段补全（缺口三）。

位置：必须在 build_entity_links.py 之后、build_kg_join.py 之前运行；
本轮只写回 _layers/ 下 tmes / appts / procs 的 JSON 文件，不改任何源数据
(_*_ai_XX.py / _tme_ai_XX.py / _appt_ai_XX.py / _proc_ai_XX.py)。

做三件事（字段语义与 schemas §5/§7/§8 一致，实体匹配与 build_entity_links 同源）：
  1) TME  每条补 era{text,dynasty,reign,year} / target{text,ent_ids} /
          action / content / related_evo / related_ledger / ref_item / confidence；
          target.ent_ids 用 match_ents 对 office 名精确匹配（类型不限，同 FIELD_RULES tmes）；
          related_evo 按同 item_id 的 EVO stage 与 category 语义映射唯一匹配才填。
  2) APPT 每条把 person/office 升级为 {text, person_ent_ids / official_ent_ids}，
          ent_ids 用 match_ents 精确匹配（person 限 person 型；office 限
          official/institution/system/doc/object/place 型），并补 when / confidence。
  3) procs steps 每条补 agent{text, agent_ent_ids}——主体词按句中位置最靠前的
          ENT norm（类型受限）优先，预置词表兜底；agent_ent_ids 匹配同主体词。

纪律：不新增/删除记录（id 与条数守恒）；不修改 evidence/item_id 等既有字段；
新增字段不参与 validate 的 required/enum 判定，故不会破坏全绿校验。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    BASE_DIR,
    load_json,
    layer_file,
    save_json,
)
from build_entity_links import (  # noqa: E402
    build_index,
    match_ents,
)

ENT_LINKS_FILE = BASE_DIR / "_layers" / "ents" / "_ent_links.json"

# ---------------------------------------------------------------------------
# 语义映射
# ---------------------------------------------------------------------------

# TME category → EVO stage（同 item 唯一匹配才写回 related_evo）
CAT2EVO: Dict[str, str] = {
    "初置": "初置",
    "改置": "增改",
    "增员": "增改",
    "复设": "复设",
    "废置": "裁革",
    "改称": "增改",
    "裁并": "裁革",
    "移驻": "增改",
    "职掌变更": "增改",
    "升秩降秩": "增改",
    "定额变更": "增改",
    "定制定型": "定制定型",
    "法弊": "弊坏",
    "未明": "未明",
}

# category 兜底动作词（无法从 evidence 提取动词短语时使用，稳定可溯源）
CAT2ACTION: Dict[str, str] = {
    "初置": "初置",
    "改置": "改置",
    "增员": "增员",
    "复设": "复设",
    "废置": "废置",
    "改称": "改称",
    "裁并": "裁并",
    "移驻": "移驻",
    "职掌变更": "职掌变更",
    "升秩降秩": "升秩降秩",
    "定额变更": "定额变更",
    "定制定型": "定制定型",
    "法弊": "法弊",
    "未明": "未明",
}

# evidence 中可能出现的动作起始字（用于截取动词短语）
ACTION_VERBS = "置改增复罢废裁移定行设立编造奏免折输徵颁给令诏命以调遣罢免恤蠲减升降更"

# procs 步骤主体词兜底表（按优先级排序，长词优先）
AGENT_FALLBACK = [
    "户科给事中",
    "户部主事",
    "户部尚书",
    "户部",
    "御史",
    "有司",
    "里长",
    "甲首",
    "官军",
    "卫所",
    "卫军",
    "运军",
    "粮长",
    "车户",
    "商人",
    "盐商",
    "茶商",
    "中官",
    "内官",
    "州县",
    "各仓",
    "仓场",
    "漕卒",
    "漕军",
    "解户",
    "军民",
    "军",
    "民",
    "官",
    "户",
]

# agent / APPT-person 实体允许类型
PERSON_TYPES = {"person"}
OFFICE_TYPES = {"official", "institution", "system", "doc", "object", "place"}
AGENT_TYPES = {"person", "official", "institution", "system", "object"}

# 汉字数字 → 阿拉伯
CN_NUM = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
    "十一": 11,
    "十二": 12,
    "十三": 13,
    "十四": 14,
    "十五": 15,
    "十六": 16,
    "十七": 17,
    "十八": 18,
    "十九": 19,
    "二十": 20,
    "二十一": 21,
    "二十二": 22,
    "二十三": 23,
    "二十四": 24,
    "二十五": 25,
    "二十六": 26,
    "二十七": 27,
    "二十八": 28,
    "二十九": 29,
    "三十": 30,
    "四十": 40,
    "五十": 50,
}


def _cn2num(s: str) -> Optional[int]:
    if s.isdigit():
        return int(s)
    return CN_NUM.get(s)


def _year_num(ev: str, reign: str) -> Optional[int]:
    """抽取年号内年份数字（「洪武十四年」→ 14；「万历九年」→ 9）。"""
    for patt in (
        reign + r"\s*([0-9一二三四五六七八九十]+)\s*年",
        r"\s*([0-9一二三四五六七八九十]+)\s*年",
    ):
        m = re.search(patt, ev)
        if m:
            return _cn2num(m.group(1))
    return None


def _phr_text(ev: str) -> str:
    """取 evidence 中第一个含年份/朝代的时间短语（era.text）。"""
    m = re.search(
        r"(?:洪武|建文|永乐|洪熙|宣德|正统|景泰|天顺|成化|弘治|正德|嘉靖|隆庆|万历|泰昌|天启|崇祯)"
        r"\s*[0-9一二三四五六七八九十]+\s*年",
        ev,
    )
    if m:
        return m.group(0)
    m2 = re.search(r"[0-9一二三四五六七八九十]+\s*年", ev)
    if m2:
        return m2.group(0)
    return ""


def _action_of(ev: str, category: str) -> str:
    """从 evidence 提取动作短语，失败回退 category 动作词。"""
    pattern = r"[%s][^，。；、：0-9年]*(?:第[^，。；]{0,4})?" % ACTION_VERBS
    m = re.search(pattern, ev)
    if m:
        frag = m.group(0)
        frag = re.sub(r"[0-9]+[万千百十]*[石两斤钱贯银米钞疋匹]?$", "", frag)
        frag = frag[:8]
        if len(frag) >= 2:
            return frag
    return CAT2ACTION.get(category, "未明")


def _subject_agent(text: str, by_norm: Dict[str, List[Dict]]) -> Optional[str]:
    """取 step.text 中位置最靠前的 ENT norm（长度≥2 且类型受限）作为主体词。

    与 build_entity_links 的 norm 索引同源；按「先出现优先」贴近句子主语。
    """
    best_pos = len(text) + 1
    best = None
    for norm, ents in by_norm.items():
        if len(norm) < 2:
            continue
        ok_type = any(e["type"] in AGENT_TYPES for e in ents)
        if not ok_type:
            continue
        pos = text.find(norm)
        if 0 <= pos < best_pos:
            best_pos = pos
            best = norm
    return best


def main() -> None:
    print("=== Enrich TME / APPT / procs ===")

    # ---- 1) 实体索引（与 build_entity_links 同源） ----
    ents: List[Dict] = []
    for v in range(1, 7):
        d = load_json(layer_file("ents", v), [])
        ents.extend(d.get("records", []) if isinstance(d, dict) else d)
    by_id, by_norm = build_index(ents)
    print(f"  实体: {len(ents)} 条, norm 索引: {len(by_norm)} 词")
    rec_ids_map = {e["item_id"] for e in ents}

    # ---- 2) TME ----
    evo_by_item: Dict[str, List[Dict]] = {}
    struct_data = load_json(BASE_DIR / "_layers" / "structs" / "structs.json", {})
    for r in struct_data.get("EVO", []):
        evo_by_item.setdefault(r["item_id"], []).append(r)

    tme_file = BASE_DIR / "_layers" / "tmes" / "tmes.json"
    tdata = load_json(tme_file, {})
    trecs = tdata.get("records", [])
    t_has_target = t_has_action = t_has_evo = 0
    for r in trecs:
        rid = r.get("id", "")
        ev = r.get("evidence", "") or ""
        reign = r.get("reign", "") or ""
        office = r.get("office", "") or ""
        item_ids = {r.get("item_id", "")} if r.get("item_id") else set()
        # era
        txt = _phr_text(ev) or reign
        r["era"] = {
            "text": txt,
            "dynasty": "明",
            "reign": reign,
            "year": _year_num(ev, reign),
        }
        # target（office 名精确匹配，类型不限，同 FIELD_RULES tmes.office）
        r["target"] = {
            "text": office,
            "ent_ids": match_ents(by_norm, office, item_ids, None),
        }
        if r["target"]["ent_ids"]:
            t_has_target += 1
        # action / content
        r["action"] = _action_of(ev, r.get("category", "未明"))
        r["content"] = ev
        if r["action"]:
            t_has_action += 1
        # related_evo（同 item 唯一 stage 匹配才填）
        stage = CAT2EVO.get(r.get("category", ""))
        evo_recs = evo_by_item.get(r.get("item_id", ""), [])
        match = [x for x in evo_recs if x.get("stage") == stage] if stage else []
        if len(match) == 1:
            r["related_evo"] = match[0].get("id", "")
            t_has_evo += 1
        else:
            r["related_evo"] = ""
        r["related_ledger"] = ""
        r["ref_item"] = r.get("item_id", "")
        r["confidence"] = 0.9
    save_json(tme_file, tdata)
    print(
        f"  TME {len(trecs)} 条: target.ent_ids 非空 {t_has_target} / "
        f"action 非空 {t_has_action} / related_evo {t_has_evo}"
    )

    # ---- 3) APPT ----
    appt_file = BASE_DIR / "_layers" / "appts" / "appts.json"
    adata = load_json(appt_file, {})
    arecs = adata.get("records", [])
    a_person = a_office = 0
    for r in arecs:
        _p = r.get("person")
        _o = r.get("office")
        person_txt = _p.get("text", "") if isinstance(_p, dict) else (_p or "")
        office_txt = _o.get("text", "") if isinstance(_o, dict) else (_o or "")
        item_ids = {r.get("item_id", "")} if r.get("item_id") else set()
        person_ids = match_ents(by_norm, person_txt, item_ids, PERSON_TYPES)
        office_ids = match_ents(by_norm, office_txt, item_ids, OFFICE_TYPES)
        r["person"] = {"text": person_txt, "person_ent_ids": person_ids}
        r["office"] = {"text": office_txt, "official_ent_ids": office_ids}
        reign = r.get("reign", "") or ""
        r["when"] = {"text": reign, "dynasty": "明", "reign": reign, "year": None}
        r["confidence"] = 0.9
        if person_ids:
            a_person += 1
        if office_ids:
            a_office += 1
    save_json(appt_file, adata)
    print(
        f"  APPT {len(arecs)} 条: person_ent_ids 非空 {a_person} / "
        f"official_ent_ids 非空 {a_office}"
    )

    # ---- 4) procs steps agent ----
    p_total_steps = p_agent = p_agent_ids = 0
    for v in range(1, 7):
        f = layer_file("procs", v)
        pdata = load_json(f, {})
        recs = pdata.get("records", [])
        changed = 0
        for pr in recs:
            item_ids = {pr.get("item_id", "")} if pr.get("item_id") else set()
            for st in pr.get("steps", []):
                p_total_steps += 1
                txt = st.get("text", "") or ""
                best = _subject_agent(txt, by_norm)
                if not best:
                    for w in AGENT_FALLBACK:
                        if w in txt:
                            best = w
                            break
                if best:
                    st["agent"] = {
                        "text": best,
                        "agent_ent_ids": match_ents(
                            by_norm, best, item_ids, AGENT_TYPES
                        ),
                    }
                    p_agent += 1
                    if st["agent"]["agent_ent_ids"]:
                        p_agent_ids += 1
                else:
                    st["agent"] = {"text": "未明", "agent_ent_ids": []}
                changed += 1
        if changed:
            save_json(f, pdata)
    print(
        f"  procs steps {p_total_steps} 步: 有 agent {p_agent} / "
        f"agent_ent_ids 非空 {p_agent_ids}"
    )
    print("=== enrich_layers 完成 ===")


if __name__ == "__main__":
    main()
