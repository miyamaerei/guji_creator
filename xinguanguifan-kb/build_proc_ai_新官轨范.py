# -*- coding: utf-8 -*-
"""
《新官轨范》流程层（AI 判定版）打包与验证器（kg-proc-ai v1，全卷版）
- 打包：读取各卷 _proc_ai_NN.py 的 PROCESSES → 每卷 JSON（新官轨范_流程_ai/NN_卷名.json）
- original 注入：AI 源数据不手抄原文；original 从 _item_registry.json 按 source 条号注入
- derived_rule 注入：从规则层 归一_汇总.json 按 item_id 映射 rule_id
- 事件引用（P0-2 修复并入）：process.events 显式引用事件层 XGF-E ID（按 derived_from 从事件层归一映射）；XGF-E 命名空间归事件层
- 全局归一：process_id 重排 = XGF-P-NNN（按卷序）
- 验证（只验缺漏，不参与判定）：
  1) source 绑定合法（条号存在）、process_id 重排后全局唯一
  2) steps 非空、step_id 格式 {ch}-{item}-s{n} 且唯一、next 引用存在（同 process 内或 END）
  3) event_type 在封闭枚举内（_kg_enums.EVENT_TYPES）
  4) confidence ∈ (0,1]；必填字段：title/source/每步 action
  5) derived_from item_id 合法；events 引用均为事件层真实 ID
- 用法：python build_proc_ai_新官轨范.py [--volumes 03 04]
- P1：共享 _kg_pack_base/_kg_enums；源数据 EVENTS 槽位已废弃（事件由事件层单独维护）
"""
import os, re, json
from _kg_pack_base import (BASE, CH_DIR, load_registry, load_rule_map,
                           parse_volumes, find_xhtml, inject_common,
                           load_ent_alias, resolve_ent_ids)
from _kg_enums import EVENT_TYPES, STRUCT_EMPTY_VOLUMES as EMPTY_VOLUMES

PROC_DIR = os.path.join(BASE, "新官轨范_流程_ai")
EV_MERGE = os.path.join(BASE, "新官轨范_事件_ai", "归一_汇总.json")
SCHEMA_VER = "kg-proc-ai-json-v1"
PROC_VER = "proc-ai-v1"


def load_event_ref():
    """item_id → [XGF-E ids]（事件层归一）。"""
    try:
        with open(EV_MERGE, encoding="utf-8") as f:
            m = json.load(f)
    except Exception:
        return {}
    ref = {}
    for ev in m.get("events", []):
        for it in ev.get("derived_from", []):
            ref.setdefault(it, []).append(ev["event_id"])
    for k in ref:
        ref[k] = sorted(set(ref[k]))
    return ref


def main():
    want = parse_volumes()
    reg = load_registry()
    rule_map = load_rule_map()
    ev_ref = load_event_ref()
    alias = load_ent_alias()
    os.makedirs(PROC_DIR, exist_ok=True)
    issues = []
    per_chapter = []
    all_proc = []
    gp = 0
    by_type = {}
    total_steps = 0
    total_ref = 0
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
        vf = os.path.join(BASE, f"_proc_ai_{ch_no}.py")
        if not os.path.exists(vf):
            issues.append(f"[{ch_no}] 缺流程源文件 {os.path.basename(vf)}")
            continue
        ns = {}
        exec(compile(open(vf, encoding="utf-8").read(), vf, "exec"), ns)
        procs = list(ns.get("PROCESSES", []))
        legacy_evs = list(ns.get("EVENTS", []))
        if legacy_evs:
            issues.append(f"[{ch_no}] 源数据 EVENTS 槽位已废弃，请迁至事件层：{len(legacy_evs)} 条")
        ch_ref = 0
        for p in procs:
            gp += 1
            p["process_id"] = f"XGF-P-{gp:03d}"
            src_id, ok = inject_common(ch_no, p, reg, rule_map, issues)
            et = p.get("event_type", "")
            if et not in EVENT_TYPES:
                issues.append(f"[{ch_no}] event_type 不在枚举：{et}（{p.get('title')}）")
            by_type[et] = by_type.get(et, 0) + 1
            steps = p.get("steps", [])
            if not steps:
                issues.append(f"[{ch_no}] steps 为空：{p.get('title')}")
            ids = set()
            for s in steps:
                sid = s.get("step_id", "")
                if not re.fullmatch(rf"{ch_no}-\d{{3}}-s\d+", sid):
                    issues.append(f"[{ch_no}] step_id 格式非法：{sid}")
                if sid in ids:
                    issues.append(f"[{ch_no}] step_id 重复：{sid}")
                ids.add(sid)
                if not s.get("action"):
                    issues.append(f"[{ch_no}] step 缺 action：{sid}")
                s["agent_ent_ids"] = resolve_ent_ids(s.get("agent"), alias)
            for s in steps:
                nx = s.get("next")
                if nx and nx != "END" and nx not in ids:
                    issues.append(f"[{ch_no}] next 引用不存在：{nx}（{p.get('title')}）")
            for d in p.get("derived_from", []):
                if d not in reg:
                    issues.append(f"[{ch_no}] derived_from 非法：{d}")
            # 事件引用（P0-2）
            evs = []
            for d in (p.get("derived_from", []) or []):
                evs.extend(ev_ref.get(d, []))
            evs = sorted(set(evs))
            p["events"] = evs
            ch_ref += len(evs)
            conf = p.get("confidence")
            if conf is not None and not (0 < conf <= 1):
                issues.append(f"[{ch_no}] confidence 越界：{conf}（{p.get('title')}）")
            if not p.get("title") or not p.get("source"):
                issues.append(f"[{ch_no}] 缺 title/source")
            total_steps += len(steps)
        vjson = {"schema_version": SCHEMA_VER, "process_version": PROC_VER,
                 "volume": ch_no, "chapter": ch_name, "source_file": base,
                 "process_count": len(procs), "event_count": ch_ref,
                 "events_note": "events 字段为事件层引用（XGF-E 命名空间归事件层维护）",
                 "processes": procs}
        with open(os.path.join(PROC_DIR, f"{ch_no}_{ch_name}.json"), "w", encoding="utf-8") as f:
            json.dump(vjson, f, ensure_ascii=False, indent=1)
        per_chapter.append({"chapter_no": ch_no, "chapter": ch_name,
                            "process_count": len(procs), "event_count": ch_ref,
                            "total_steps": sum(len(p["steps"]) for p in procs)})
        all_proc.extend(procs)
        total_ref += ch_ref
        print(f"{ch_no} {ch_name}: proc={len(procs)} events_ref={ch_ref} steps={sum(len(p['steps']) for p in procs)}")
    merge = {"schema_version": SCHEMA_VER, "process_version": PROC_VER,
             "total_processes": len(all_proc), "total_events": total_ref,
             "total_steps": total_steps,
             "process_id_range": f"XGF-P-001..XGF-P-{len(all_proc):03d}",
             "event_id_range": "XGF-E-001..XGF-E-229（由事件层归一维护，流程层仅引用）",
             "by_event_type": by_type, "per_chapter": per_chapter,
             "events": sorted({x for v in ev_ref.values() for x in v}),
             "events_note": "流程层 events 槽位显式引用事件层 XGF-E ID；命名空间归事件层。",
             "processes": all_proc}
    with open(os.path.join(PROC_DIR, "归一_汇总.json"), "w", encoding="utf-8") as f:
        json.dump(merge, f, ensure_ascii=False, indent=1)
    rep = ["# 流程层（AI 判定版）验证缺漏清单\n"]
    rep.append(f"- 打包卷数：{len(per_chapter)}；流程总数：{len(all_proc)}；事件引用总数：{total_ref}；步骤总数：{total_steps}")
    rep.append(f"- process_id 范围：{merge['process_id_range']}；事件引用范围见事件层归一")
    rep.append(f"- 问题数：{len(issues)}\n")
    for it in issues:
        rep.append("- " + it)
    with open(os.path.join(PROC_DIR, "验证缺漏清单.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep))
    print("issues =", len(issues))
    print("by_event_type:", by_type)
    for it in issues[:40]:
        print("  -", it)


if __name__ == "__main__":
    main()
