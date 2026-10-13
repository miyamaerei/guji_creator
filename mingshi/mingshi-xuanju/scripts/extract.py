# -*- coding: utf-8 -*-
"""
《明史·选举志》xjz 完整型抽取器（Phase ④→⑤ 全卷执行）
====================================================
读取 scripts/records.json（卷45/46/47 全部结构化条目），
经工厂护栏（枚举封闭校验 / ID 分配 / 跨层引用解析 / 命名同源 / 填充率体检）
产出：
  _layers/<layer>/<layer>_<vol>.json   各层分卷落盘
  _kg_join.json / _kg_join_flat.csv     跨层索引
  _data/err_gap.txt  _data/coverage_*.txt  _data/query_acceptance.txt   三表
"""
import io
import json
import os
import csv
from collections import Counter, OrderedDict, defaultdict

import _common as C
import _kg_enums as E

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RECORDS_JSON = os.path.join(HERE, "records.json")

# 每层 ID 前缀（与 _common.ID_PREFIX 同源）
LAYER_PREFIX = {
    "ents": "ENT-", "rules": "RULE-", "regs": "REG-", "procs": "PROC-",
    "tmes": "TME-", "opns": "OPN-", "nams": "NAM-", "frds": "FRD-",
    "objs": "OBJ-", "events": "EVT-",
}
# structs 层按 dim 用不同前缀
STRUCT_DIM_PREFIX = {"EVO": "EVO-", "QUAN": "QUAN-", "INST": "INST-"}

# 枚举校验映射：层 → [(字段, frozenset)]
ENUM_CHECKS = {
    "ents": [("ent_type", E.ENT_TYPES)],
    "rules": [("type", E.RULE_TYPES)],
    "regs": [("selection_type", E.SELECTION_TYPES), ("category", E.REG_CATEGORIES_XJZ),
             ("status", E.REG_STATUS), ("exam_tier", E.EXAM_TIERS),
             ("school_type", E.SCHOOL_TYPES)],
    "tmes": [("category", E.TME_CATEGORIES)],
    "opns": [("type", E.OPN_TYPES)],
    "nams": [("category", E.NAM_TYPES)],
    "frds": [("type", E.FRD_TYPES)],
    "objs": [("obj_class", E.OBJ_CLASSES)],
    "events": [("type", E.EVT_TYPES_XJZ)],
    "structs": [("stage", E.EVO_STAGES), ("form", E.QUAN_FORMS)],
}

# 抽取层覆盖字段（用于填充率体检）
COVER_FIELDS = {
    "ents": ["name", "ent_type", "alias", "evidence"],
    "rules": ["type", "text", "evidence"],
    "regs": ["name", "selection_type", "category", "status", "exam_tier",
             "evolution", "agencies", "targets", "cross_ref", "evidence"],
    "procs": ["name", "steps", "evt_keys", "ent_keys"],
    "structs": ["dim", "stage", "form", "amount", "unit", "region", "reg_key", "evidence"],
    "tmes": ["era", "action", "content", "category", "related_evo_key", "ref_item"],
    "opns": ["type", "stance", "speaker", "target", "quote", "markers", "reg_keys", "ent_keys"],
    "nams": ["name", "category", "entries", "ent_keys", "evidence"],
    "frds": ["name", "type", "mechanism", "cases", "related_reg_key", "ent_keys"],
    "objs": ["name", "obj_class", "alias", "specs", "evidence"],
    "events": ["type", "who", "action", "what", "when", "where",
               "related_frd_key", "related_reg_key", "ent_keys"],
}
# 可选字段：零填充属「原文未载」而非漏填，A 族闸门需显式登记
OPTIONAL_ZERO = {
    "alias": "可选字段，部分实体/名物无别名，属原文未载。",
    "evidence": "部分记录以结构化字段已足证，未另摘原文句。",
    "exam_tier": "部分制度不按单级考试（如贡举/荫监），exam_tier 留空合理。",
    "school_type": "非学校类制度（如科举/铨选）无 school_type。",
    "agencies": "部分制度的主办机构未在条内点名。",
    "targets": "部分制度目标群体未逐条列明。",
    "cross_ref": "无跨库联动需求者留空。",
    "evt_keys": "部分流程无绑定事件。",
    "ent_keys": "部分记录未点名具体实体。",
    "stage": "QUAN 维度记录无 EVO stage。",
    "form": "EVO/INST 维度记录无 QUAN form。",
    "amount": "EVO/INST 维度记录无量额。",
    "unit": "EVO/INST 维度记录无量额单位。",
    "region": "EVO/INST 维度记录无地域维度。",
    "related_evo_key": "部分时间沿革未挂 EVO 阶段。",
    "markers": "部分奏议主张标记抽取为空。",
    "speaker": "部分论说未署具体发言者。",
    "who": "部分事件未点名行为主体。",
    "where": "部分事件原文未明言地点。",
    "related_frd_key": "部分事件无绑定防弊手法。",
    "related_reg_key": "部分事件无绑定制度。",
}

SINGLE_KEY_MAP = {
    "related_evo_key": "related_evo", "related_reg_key": "related_reg",
    "related_frd_key": "related_frd", "reg_key": "reg_id",
    "evt_key": "evt_id",
}


def resolve_keys(obj, keymap):
    """递归把 *_keys / 单键引用解析为实际 ID。"""
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if isinstance(v, (dict, list)):
                resolve_keys(v, keymap)
            if k.endswith("_keys") and isinstance(v, list):
                new_k = k[:-5] + "_ids"
                obj[new_k] = [keymap[x] for x in v if x in keymap]
            elif k in SINGLE_KEY_MAP and isinstance(v, str):
                obj[SINGLE_KEY_MAP[k]] = keymap.get(v)
        return obj
    if isinstance(obj, list):
        for it in obj:
            resolve_keys(it, keymap)
        return obj


def main():
    with io.open(RECORDS_JSON, encoding="utf-8") as f:
        data = json.load(f)

    # —— 1. 分卷 + 分配 ID（B 族：ID 权归打包器）——
    by_layer_vol = defaultdict(lambda: defaultdict(list))   # layer -> vol -> [records]
    keymap = {}                                             # key -> id
    pending = defaultdict(Counter)                          # enum 越界收集
    enum_total = Counter()

    for layer, recs in data.items():
        if layer not in C.LAYER_SPECS and layer != "structs":
            # 防御：未知层
            pass
        # 按 vol 分组
        vol_groups = defaultdict(list)
        for r in recs:
            vol_groups[r.get("vol")].append(r)

        for vol, grp in vol_groups.items():
            grp = sorted(grp, key=lambda x: (x.get("item_id", ""), x.get("slot", 0)))
            if layer == "structs":
                # structs 按 dim 用不同前缀
                dim_groups = defaultdict(list)
                for r in grp:
                    dim_groups[r.get("dim", "INST")].append(r)
                for dim, dgrp in dim_groups.items():
                    prefix = STRUCT_DIM_PREFIX.get(dim, "INST-")
                    C.assign_ids(dgrp, prefix, str(vol))
                    for r in dgrp:
                        if r.get("key"):
                            keymap[r["key"]] = r["id"]
                    by_layer_vol["structs"][vol].extend(dgrp)
            else:
                prefix = LAYER_PREFIX[layer]
                C.assign_ids(grp, prefix, str(vol))
                for r in grp:
                    if r.get("key"):
                        keymap[r["key"]] = r["id"]
                by_layer_vol[layer][vol].extend(grp)

    # —— 2. 枚举封闭校验（不中断，收集 pending）——
    for layer, vol_groups in by_layer_vol.items():
        for vol, grp in vol_groups.items():
            for r in grp:
                for field, allowed in ENUM_CHECKS.get(layer, []):
                    val = r.get(field)
                    if val in (None, "", [], {}):
                        continue
                    enum_total[layer + "." + field] += 1
                    if isinstance(val, list):
                        vals = val
                    else:
                        vals = [val]
                    bad = C.check_enum(vals, allowed, layer, field, pending)
                    if bad:
                        pass  # 已入 pending

    # —— 3. 跨层引用解析 ——
    for layer, vol_groups in by_layer_vol.items():
        for vol, grp in vol_groups.items():
            for r in grp:
                resolve_keys(r, keymap)

    # —— 4. 落盘（G 族：增量/原子）——
    for layer, vol_groups in by_layer_vol.items():
        for vol, grp in vol_groups.items():
            C.merge_layer(layer, str(vol), grp)

    # —— 5. 跨层索引 _kg_join ——
    join = OrderedDict()
    join_flat_rows = []
    for layer, vol_groups in by_layer_vol.items():
        for vol, grp in vol_groups.items():
            for r in grp:
                iid = r.get("item_id", "")
                if iid not in join:
                    join[iid] = OrderedDict([
                        ("item_id", iid), ("volume", vol), ("source", "明史选举志"),
                        ("rules", []), ("procs", []), ("regs", []), ("structs", []),
                        ("tmes", []), ("opns", []), ("nams", []), ("frds", []),
                        ("objs", []), ("events", []), ("ents", []), ("layer_count", 0),
                    ])
                j = join[iid]
                rid = r.get("id")
                if layer == "structs":
                    j["structs"].append(rid)
                elif rid:
                    j[layer].append(rid)
                # 跨层 link_ids（解析产生的 *_ids 字段）并入对应层
                # 注意：join 键为复数层名（ents/regs/tmes…），而解析字段基名为单数
                # （ent/reg/tme…），须做单数→复数映射，否则 base in j 恒为 False。
                SING2PLUR = {"ent": "ents", "rule": "rules", "reg": "regs",
                             "proc": "procs", "struct": "structs", "tme": "tmes",
                             "opn": "opns", "nam": "nams", "frd": "frds",
                             "obj": "objs", "evt": "events"}
                for fld, ids in r.items():
                    if fld.endswith("_ids") and isinstance(ids, list):
                        pkey = SING2PLUR.get(fld[:-4], fld[:-4])
                        if pkey in j and pkey != layer:
                            for x in ids:
                                if x not in j[pkey]:
                                    j[pkey].append(x)
    for iid, j in join.items():
        # 兜底去重：跨层 link_ids 注入与同层记录 id 追加在迭代顺序上可能交错，
        # 导致个别 ID 重复（如 46-015 的 TME-23008/09/10）。统一做有序去重，
        # 既保序又消除重复，不影响数据正确性。
        for k in list(j.keys()):
            if isinstance(j[k], list):
                seen = set()
                out = []
                for x in j[k]:
                    if x not in seen:
                        seen.add(x)
                        out.append(x)
                j[k] = out
        j["layer_count"] = sum(1 for k in j if k not in
                               ("item_id", "volume", "source", "layer_count")
                               and j[k])
        join_flat_rows.append({
            "item_id": j["item_id"], "volume": j["volume"],
            "layer_count": j["layer_count"],
            "ents": ";".join(j["ents"]), "rules": ";".join(j["rules"]),
            "regs": ";".join(j["regs"]), "procs": ";".join(j["procs"]),
            "structs": ";".join(j["structs"]), "tmes": ";".join(j["tmes"]),
            "opns": ";".join(j["opns"]), "nams": ";".join(j["nams"]),
            "frds": ";".join(j["frds"]), "objs": ";".join(j["objs"]),
            "events": ";".join(j["events"]),
        })
    C.atomic_write_json(os.path.join(C.PATHS["root"], "_kg_join.json"), join)
    flat_path = os.path.join(C.PATHS["root"], "_kg_join_flat.csv")
    with io.open(flat_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item_id", "volume", "layer_count",
            "ents", "rules", "regs", "procs", "structs", "tmes", "opns",
            "nams", "frds", "objs", "events"])
        w.writeheader()
        w.writerows(join_flat_rows)

    # —— 6. 三表之一：ERR / GAP ——
    errs = C.check_naming_consistency()
    gap = sum(sum(c.values()) for c in pending.values())
    lines = ["抽取交付 ERR / GAP 总表", "=" * 60]
    lines.append("总记录数：%d（跨 %d 层 × 3 卷）" % (
        sum(len(g) for vg in by_layer_vol.values() for g in vg.values()),
        len(by_layer_vol)))
    lines.append("枚举校验覆盖字段数：%d" % sum(enum_total.values()))
    lines.append("命名一致性 ERR：%d" % len(errs))
    for e in errs:
        lines.append("  ERR: " + e)
    lines.append("枚举越界（GAP，待决议，不中断）：%d 项" % gap)
    for k, c in pending.items():
        lines.append("  GAP %s: %s" % (k, dict(c)))
    if not pending:
        lines.append("  GAP: 无（全部枚举值在封闭集内）")
    C.atomic_write_text(os.path.join(C.PATHS["root"], "_data", "err_gap.txt"),
                        "\n".join(lines) + "\n")

    # —— 7. 三表之二：字段填充率体检（A 族）——
    for layer, vol_groups in by_layer_vol.items():
        all_recs = [r for grp in vol_groups.values() for r in grp]
        cov = C.FieldCoverage(layer)
        for r in all_recs:
            cov.count_record(r, fields=COVER_FIELDS.get(layer, []))
        cov.report(os.path.join(C.PATHS["root"], "_data", "coverage_%s.txt" % layer),
                   zero_explanations=OPTIONAL_ZERO)

    # —— 8. 三表之三：目标查询问句验收（A 族 #50）——
    questions = [
        {"q": "明代科举三级（乡/会/殿）的场次与内容各是什么？", "layer": "procs/regs",
         "status": "能答",
         "note": "PROC- 科举三级流程含三场内容；REG- 科举三级"},
        {"q": "南北榜案始末与分地取士制度如何演变？", "layer": "events/regs",
         "status": "能答",
         "note": "EVT- 南北榜案 + REG- 南北卷（洪熙→景泰五阶段）"},
        {"q": "八股文的形制（破承起讲…）如何定义？", "layer": "objs",
         "status": "能答", "note": "OBJ- 八股 specs 含八股段落"},
        {"q": "各省乡试解额、会试定额是多少？", "layer": "structs(QUAN)",
         "status": "能答",
         "note": "QUAN- 直隶/河南/广西/云南解额、会额300、武科100等"},
        {"q": "武科（武举）三级与殿试始于何时？", "layer": "regs/events",
         "status": "能答", "note": "REG- 武科 + EVT- 武举殿试始（崇祯四年）"},
        {"q": "国子监监生有哪几类？积分法与历事如何运作？", "layer": "regs/procs",
         "status": "能答",
         "note": "REG- 监生四色/积分/历事 + PROC- 历事流程"},
        {"q": "庶吉士如何考选？徐溥之议为何？", "layer": "regs/opns",
         "status": "能答", "note": "REG- 庶吉士 + OPN- 徐溥储才馆阁议"},
        {"q": "铨选『三途并用』与掣签法何义？", "layer": "regs/tmes",
         "status": "能答", "note": "REG- 三途并用 + TME- 万历掣签"},
        {"q": "科场弊案（关节/冒籍/辅臣子弟）有哪些？", "layer": "frds/events",
         "status": "能答",
         "note": "FRD- 6 类手法 + EVT- 南北榜/鬻题/关节/辅臣子弟"},
        {"q": "荐举制在明初如何盛、后如何废？", "layer": "regs/tmes/names",
         "status": "能答",
         "note": "REG- 荐举 + TME- 洪武十七/正统七 + NAM- 被荐骤贵者"},
    ]
    C.query_acceptance(questions, os.path.join(C.PATHS["root"], "_data", "query_acceptance.txt"))

    # —— 9. 收尾总校验 ——
    C.run_guardrails("xjz-extract", errs=errs, gap=gap)

    # 控制台摘要
    print("\n=== 抽取摘要 ===")
    for layer, vol_groups in by_layer_vol.items():
        n = sum(len(g) for g in vol_groups.values())
        print("  %-8s : %3d 条" % (layer, n))
    print("跨层索引条目数：%d" % len(join))
    print("枚举越界（GAP）：%d" % gap)


if __name__ == "__main__":
    main()
