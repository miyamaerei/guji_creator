# -*- coding: utf-8 -*-
"""
《新官轨范》结构化层（AI 判定版）打包与验证器（kg-struct-ai v1）
五维度：文簿台账体系（ledgers）/ 县政时间制度（times）/ 公文生命周期（docs）/ 角色-职责网络（actors）/ 防弊机制库（frauds）
- 打包：读取各卷 _struct_ai_NN.py 的 LEDGERS/TIMES/DOCS/ACTORS/FRAUDS → 每卷 JSON（新官轨范_结构_ai/NN_卷名.json）
- original 注入：从 _item_registry.json 按 source 条号注入（不手抄）
- derived_rule 注入：从规则层 归一_汇总.json 按 item_id 映射 rule_id
- 全局归一：ledger_id=LGR-NNN / time_id=TME-NNN / doc_id=DOC-NNN / actor_id=ACT-NNN / fraud_id=FRD-NNN（按卷序重排）
- 验证（只验缺漏，不参与判定）：
  1) source 条号合法、ID 重排后全局唯一、confidence ∈ (0,1]
  2) ledgers：name/purpose/keeper 必填；times：keyword/value/scope 必填；docs：doc_type/stages 非空
     actors：name/role_type 必填且 role_type ∈ 封闭枚举、duties 非空；frauds：fraud/mechanism 必填且 mechanism_type ∈ 封闭枚举
  3) derived_from item_id 合法
- 用法：python build_struct_ai_新官轨范.py [--volumes 01]
- P1：共享 _kg_pack_base/_kg_enums（常量/加载/注入/卷解析/枚举去重）
"""
import os, json
from _kg_pack_base import (BASE, CH_DIR, load_registry, load_rule_map,
                           parse_volumes, find_xhtml, inject_common,
                           load_ent_alias, resolve_ent_ids)
from _kg_enums import ROLE_TYPES, MECH_TYPES, STRUCT_EMPTY_VOLUMES as EMPTY_VOLUMES

STRUCT_DIR = os.path.join(BASE, "新官轨范_结构_ai")
SCHEMA_VER = "kg-struct-ai-json-v1"
STRUCT_VER = "struct-ai-v1"
SECTIONS = {"ledgers": ("LGR", "ledger_id"), "times": ("TME", "time_id"),
            "docs": ("DOC", "doc_id"), "actors": ("ACT", "actor_id"),
            "frauds": ("FRD", "fraud_id")}


def main():
    want = parse_volumes()
    reg = load_registry()
    rule_map = load_rule_map()
    alias = load_ent_alias()
    os.makedirs(STRUCT_DIR, exist_ok=True)
    issues = []
    per_chapter = []
    acc = {"ledgers": [], "times": [], "docs": [], "actors": [], "frauds": []}
    counters = {"ledgers": 0, "times": 0, "docs": 0, "actors": 0, "frauds": 0}
    by_type = {"ledger_by_keeper": {}, "time_by_unit": {}, "doc_by_type": {},
               "actor_by_role": {}, "fraud_by_mech": {}}
    for ch_no in [f"{i:02d}" for i in range(1, 12)]:
        if want and ch_no not in want:
            continue
        if ch_no in EMPTY_VOLUMES:
            continue
        base = find_xhtml(ch_no)
        if not base:
            issues.append(f"[{ch_no}] 未找到 XHTML")
            continue
        ch_name = os.path.splitext(base)[0][3:]
        vf = os.path.join(BASE, f"_struct_ai_{ch_no}.py")
        if not os.path.exists(vf):
            issues.append(f"[{ch_no}] 缺结构源文件 {os.path.basename(vf)}")
            continue
        ns = {}
        exec(compile(open(vf, encoding="utf-8").read(), vf, "exec"), ns)
        vjson = {"schema_version": SCHEMA_VER, "struct_version": STRUCT_VER,
                 "volume": ch_no, "chapter": ch_name, "source_file": base}
        for sec in SECTIONS:
            items = list(ns.get(sec.upper(), []))
            for it in items:
                counters[sec] += 1
                it[SECTIONS[sec][1]] = f"{SECTIONS[sec][0]}-{counters[sec]:03d}"
                src_id, ok = inject_common(ch_no, it, reg, rule_map, issues)
                it["item_id"] = src_id if ok else None
                conf = it.get("confidence")
                if conf is not None and not (0 < conf <= 1):
                    issues.append(f"[{ch_no}] confidence 越界：{conf}")
                if sec == "actors":
                    it["ent_ids"] = resolve_ent_ids(it.get("name"), alias)
            vjson[f"{sec}_count"] = len(items)
            vjson[sec] = items
            acc[sec].extend(items)
        # 分 section 校验必填与枚举
        for it in vjson["ledgers"]:
            for f in ("name", "purpose", "keeper"):
                if not it.get(f):
                    issues.append(f"[{ch_no}] ledger 缺 {f}：{it.get('ledger_id')}")
        for it in vjson["times"]:
            for f in ("keyword", "value", "scope"):
                if not it.get(f):
                    issues.append(f"[{ch_no}] time 缺 {f}：{it.get('time_id')}")
        for it in vjson["docs"]:
            if not it.get("doc_type") or not it.get("stages"):
                issues.append(f"[{ch_no}] doc 缺 doc_type/stages：{it.get('doc_id')}")
            for st in it.get("stages", []):
                if not st.get("stage") or not st.get("action"):
                    issues.append(f"[{ch_no}] doc stages 缺 stage/action：{it.get('doc_id')}")
        for it in vjson["actors"]:
            if not it.get("name"):
                issues.append(f"[{ch_no}] actor 缺 name")
            rt = it.get("role_type", "")
            if rt not in ROLE_TYPES:
                issues.append(f"[{ch_no}] role_type 不在枚举：{rt}（{it.get('name')}）")
            if not it.get("duties"):
                issues.append(f"[{ch_no}] actor 缺 duties：{it.get('name')}")
            for r in it.get("relations", []):
                if not r.get("rel_type") or not r.get("target"):
                    issues.append(f"[{ch_no}] actor relations 缺字段：{it.get('name')}")
        for it in vjson["frauds"]:
            for f in ("fraud", "mechanism"):
                if not it.get(f):
                    issues.append(f"[{ch_no}] fraud 缺 {f}：{it.get('fraud_id')}")
            mt = it.get("mechanism_type", "")
            if mt not in MECH_TYPES:
                issues.append(f"[{ch_no}] mechanism_type 不在枚举：{mt}（{it.get('fraud_id')}）")
        per_chapter.append({"chapter_no": ch_no, "chapter": ch_name,
                            "ledger_count": vjson["ledgers_count"], "time_count": vjson["times_count"],
                            "doc_count": vjson["docs_count"], "actor_count": vjson["actors_count"],
                            "fraud_count": vjson["frauds_count"]})
        with open(os.path.join(STRUCT_DIR, f"{ch_no}_{ch_name}.json"), "w", encoding="utf-8") as f:
            json.dump(vjson, f, ensure_ascii=False, indent=1)
        print(f"{ch_no} {ch_name}: ledgers={vjson['ledgers_count']} times={vjson['times_count']} docs={vjson['docs_count']} actors={vjson['actors_count']} frauds={vjson['frauds_count']}")
    # 统计
    for it in acc["ledgers"]:
        k = it.get("keeper", "未注")
        by_type["ledger_by_keeper"][k] = by_type["ledger_by_keeper"].get(k, 0) + 1
    for it in acc["times"]:
        u = it.get("unit", "未注")
        by_type["time_by_unit"][u] = by_type["time_by_unit"].get(u, 0) + 1
    for it in acc["docs"]:
        t = it.get("doc_type", "未注")
        by_type["doc_by_type"][t] = by_type["doc_by_type"].get(t, 0) + 1
    for it in acc["actors"]:
        r = it.get("role_type", "未注")
        by_type["actor_by_role"][r] = by_type["actor_by_role"].get(r, 0) + 1
    for it in acc["frauds"]:
        m = it.get("mechanism_type", "未注")
        by_type["fraud_by_mech"][m] = by_type["fraud_by_mech"].get(m, 0) + 1
    merge = {"schema_version": SCHEMA_VER, "struct_version": STRUCT_VER,
             "total_ledgers": len(acc["ledgers"]), "total_times": len(acc["times"]),
             "total_docs": len(acc["docs"]), "total_actors": len(acc["actors"]),
             "total_frauds": len(acc["frauds"]),
             "id_ranges": {f"ledger": f"LGR-001..LGR-{len(acc['ledgers']):03d}",
                           "time": f"TME-001..TME-{len(acc['times']):03d}",
                           "doc": f"DOC-001..DOC-{len(acc['docs']):03d}",
                           "actor": f"ACT-001..ACT-{len(acc['actors']):03d}",
                           "fraud": f"FRD-001..FRD-{len(acc['frauds']):03d}"},
             "by_type": by_type, "per_chapter": per_chapter,
             "ledgers": acc["ledgers"], "times": acc["times"], "docs": acc["docs"],
             "actors": acc["actors"], "frauds": acc["frauds"]}
    with open(os.path.join(STRUCT_DIR, "归一_汇总.json"), "w", encoding="utf-8") as f:
        json.dump(merge, f, ensure_ascii=False, indent=1)
    rep = ["# 结构化层（AI 判定版）验证缺漏清单\n"]
    rep.append(f"- 打包卷数：{len(per_chapter)}；文簿：{len(acc['ledgers'])}；时间制度：{len(acc['times'])}；公文：{len(acc['docs'])}；角色：{len(acc['actors'])}；防弊：{len(acc['frauds'])}")
    rep.append(f"- ID 范围：{json.dumps(merge['id_ranges'], ensure_ascii=False)}")
    rep.append(f"- 问题数：{len(issues)}\n")
    for it in issues:
        rep.append("- " + it)
    with open(os.path.join(STRUCT_DIR, "验证缺漏清单.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep))
    print("issues =", len(issues))
    print("by_type:", json.dumps(by_type, ensure_ascii=False))
    for it in issues[:40]:
        print("  -", it)


if __name__ == "__main__":
    main()
