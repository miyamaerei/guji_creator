# -*- coding: utf-8 -*-
"""
《新官轨范》事件五元组 Registry（AI 判定版）打包与验证器（kg-event-ai v1）
- 打包：读取各卷 _event_ai_NN.py 的 EVENTS（五元组实例）→ 每卷 JSON（新官轨范_事件_ai/NN_卷名.json）
- 五元组：who（主体）→ action（动作）→ what（对象/客体）→ when（时间/时序）→ where（地点/空间）
- original 注入：AI 源数据不手抄原文；original 从 _item_registry.json 按 source 条号注入
- derived_rule 注入：从规则层 归一_汇总.json 按 item_id 映射 rule_id
- 全局归一：event_id 重排 = XGF-E-NNN（按卷序）
- 验证（只验缺漏，不参与判定）：
  1) source 绑定合法（条号存在）、event_id 重排后全局唯一
  2) 五元组必填：who 非空数组、action 非空、what 非空数组、when 非空、where 非空（未明须显式标注"未明"）
  3) event_type 在封闭枚举内（新增类型需先扩展 _kg_enums.EVENT_TYPES）
  4) confidence ∈ (0,1]；必填字段：title/source/analysis
  5) derived_from item_id 合法
- 用法：python build_event_ai_新官轨范.py [--volumes 03 04]
- P1：共享 _kg_pack_base/_kg_enums（常量/加载/注入/卷解析去重）
"""
import os, json
from _kg_pack_base import (BASE, CH_DIR, load_registry, load_rule_map,
                           parse_volumes, find_xhtml, inject_common,
                           load_ent_alias, resolve_ent_ids)
from _kg_enums import EVENT_TYPES, STRUCT_EMPTY_VOLUMES as EMPTY_VOLUMES

EV_DIR = os.path.join(BASE, "新官轨范_事件_ai")
SCHEMA_VER = "kg-event-ai-json-v1"
EV_VER = "event-ai-v1"
SLOTS = ["who", "action", "what", "when", "where"]


def main():
    want = parse_volumes()
    reg = load_registry()
    rule_map = load_rule_map()
    alias = load_ent_alias()
    os.makedirs(EV_DIR, exist_ok=True)
    issues = []
    per_chapter = []
    all_ev = []
    ge = 0
    by_type = {}
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
        vf = os.path.join(BASE, f"_event_ai_{ch_no}.py")
        if not os.path.exists(vf):
            issues.append(f"[{ch_no}] 缺事件源文件 {os.path.basename(vf)}")
            continue
        ns = {}
        exec(compile(open(vf, encoding="utf-8").read(), vf, "exec"), ns)
        evs = list(ns.get("EVENTS", []))
        for e in evs:
            ge += 1
            e["event_id"] = f"XGF-E-{ge:03d}"
            inject_common(ch_no, e, reg, rule_map, issues)
            e["who_ent_ids"] = resolve_ent_ids(e.get("who"), alias)
            et = e.get("type", "")
            if et not in EVENT_TYPES:
                issues.append(f"[{ch_no}] type 不在枚举：{et}（{e.get('title')}）")
            by_type[et] = by_type.get(et, 0) + 1
            for slot in SLOTS:
                v = e.get(slot)
                if slot in ("who", "what"):
                    if not isinstance(v, list) or not v:
                        issues.append(f"[{ch_no}] 五元组缺 {slot}：{e.get('title')}")
                else:
                    if not v or not str(v).strip():
                        issues.append(f"[{ch_no}] 五元组缺 {slot}：{e.get('title')}")
            if not e.get("title") or not e.get("source") or not e.get("analysis"):
                issues.append(f"[{ch_no}] 缺 title/source/analysis")
            conf = e.get("confidence")
            if conf is not None and not (0 < conf <= 1):
                issues.append(f"[{ch_no}] confidence 越界：{conf}（{e.get('title')}）")
            for d in e.get("derived_from", []):
                if d not in reg:
                    issues.append(f"[{ch_no}] derived_from 非法：{d}")
        vjson = {"schema_version": SCHEMA_VER, "event_version": EV_VER,
                 "volume": ch_no, "chapter": ch_name, "source_file": base,
                 "event_count": len(evs), "events": evs}
        with open(os.path.join(EV_DIR, f"{ch_no}_{ch_name}.json"), "w", encoding="utf-8") as f:
            json.dump(vjson, f, ensure_ascii=False, indent=1)
        per_chapter.append({"chapter_no": ch_no, "chapter": ch_name,
                            "event_count": len(evs)})
        all_ev.extend(evs)
        print(f"{ch_no} {ch_name}: events={len(evs)}")
    merge = {"schema_version": SCHEMA_VER, "event_version": EV_VER,
             "total_events": len(all_ev),
             "event_id_range": f"XGF-E-001..XGF-E-{len(all_ev):03d}",
             "by_event_type": by_type, "per_chapter": per_chapter,
             "events": all_ev}
    with open(os.path.join(EV_DIR, "归一_汇总.json"), "w", encoding="utf-8") as f:
        json.dump(merge, f, ensure_ascii=False, indent=1)
    rep = ["# 事件五元组 Registry（AI 判定版）验证缺漏清单\n"]
    rep.append(f"- 打包卷数：{len(per_chapter)}；事件总数：{len(all_ev)}")
    rep.append(f"- event_id 范围：{merge['event_id_range']}")
    rep.append(f"- 问题数：{len(issues)}\n")
    for it in issues:
        rep.append("- " + it)
    with open(os.path.join(EV_DIR, "验证缺漏清单.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep))
    print("issues =", len(issues))
    print("by_event_type:", by_type)
    for it in issues[:40]:
        print("  -", it)


if __name__ == "__main__":
    main()
