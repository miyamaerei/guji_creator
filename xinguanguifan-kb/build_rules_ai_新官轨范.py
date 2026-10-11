# -*- coding: utf-8 -*-
"""
《新官轨范》规则层（AI 判定版）打包与验证器（kg-rule-ai v1，全卷版）
- 打包：读取各卷 _rules_ai_NN.py 的 RULES → 每卷 JSON（新官轨范_规则_ai/NN_卷名.json）
- 全局归一：按卷序+条序重排 rule_id = XGF-R-001..N（02 卷注语无规则，跳过）
- 验证（只验缺漏，不参与判定）：
  1) rule_id 全局唯一、item_id 格式合法
  2) 条目全覆盖：每卷 XHTML 每一条目都有且仅有 1 条规则（02 卷注语除外）
  3) source 绑定：source 与 item_id 对应文件#条N 一致
  4) original 一致性：original 与 XHTML 对应条文本（去√）一致（容忍空白差异）
  5) 必填字段：rule_id/item_id/type/modals/source/original/confidence 非空；type∈合法枚举；confidence∈(0,1]
  6) modals 合法值
- 输出：每卷 JSON + 归一_汇总.json + 验证缺漏清单.txt
- P1：共享 _kg_pack_base/_kg_enums（常量/枚举去重）
"""
import os, re, json, glob, html as htmllib
from collections import Counter
from _kg_pack_base import BASE, CH_DIR, find_xhtml, load_ent_alias, resolve_ent_ids
from _kg_enums import VALID_RULE_TYPES as VALID_TYPES, VALID_RULE_MODALS as VALID_MODALS, RULE_EMPTY_VOLUMES as EMPTY_VOLUMES

AI_DIR = os.path.join(BASE, "新官轨范_规则_ai")
SCHEMA_VER = "kg-rule-ai-json-v1"
RULE_VER = "rule-ai-v1"


def load_xhtml_items(base):
    content = open(os.path.join(CH_DIR, base), encoding="utf-8").read()
    items = re.findall(r'<p class="item">(.*?)</p>', content, re.S)
    items = [htmllib.unescape(m).strip() for m in items]
    if not items:
        items = re.findall(r'<p[^>]*>(.*?)</p>', content, re.S)
        items = [htmllib.unescape(m).strip() for m in items]
    return items


def norm(s):
    return re.sub(r"\s+", "", s)


def main():
    os.makedirs(AI_DIR, exist_ok=True)
    alias = load_ent_alias()
    vol_nums = [f"{i:02d}" for i in range(1, 12)]
    per_chapter = []
    all_rules = []
    issues = []
    by_type = Counter()
    by_modal = Counter()
    combo = 0
    gid = 0
    for ch_no in vol_nums:
        vf = os.path.join(BASE, f"_rules_ai_{ch_no}.py")
        base = find_xhtml(ch_no)
        if not base:
            issues.append(f"[{ch_no}] 未找到 XHTML")
            continue
        items = load_xhtml_items(base)
        ch_name = os.path.splitext(base)[0][3:]
        if ch_no in EMPTY_VOLUMES:
            vjson = {"schema_version": SCHEMA_VER, "rule_version": RULE_VER,
                     "volume": ch_no, "chapter": ch_name, "source_file": base,
                     "item_count": len(items), "rule_count": 0, "note": "卷首注语，无规范句，规则数为0",
                     "rules": []}
            with open(os.path.join(AI_DIR, f"{ch_no}_{ch_name}.json"), "w", encoding="utf-8") as f:
                json.dump(vjson, f, ensure_ascii=False, indent=1)
            per_chapter.append({"chapter_no": ch_no, "chapter": ch_name,
                                "item_count": len(items), "rule_count": 0})
            print(f"{ch_no} {ch_name}: items={len(items)} rules=0（注语）")
            continue
        if not os.path.exists(vf):
            issues.append(f"[{ch_no}] 缺规则源文件 {os.path.basename(vf)}")
            continue
        ns = {}
        exec(compile(open(vf, encoding="utf-8").read(), vf, "exec"), ns)
        rules = list(ns["RULES"])
        rules.sort(key=lambda r: int(r["item_id"].split("-")[1]))
        item_ids = {f"{ch_no}-{i:03d}" for i in range(1, len(items) + 1)}
        rule_items = {r["item_id"] for r in rules}
        missing = sorted(item_ids - rule_items)
        dup = [i for i, c in Counter(r["item_id"] for r in rules).items() if c > 1]
        extra = sorted(rule_items - item_ids)
        if missing:
            issues.append(f"[{ch_no}] 缺规则条目：{','.join(missing)}（{len(missing)}条）")
        if dup:
            issues.append(f"[{ch_no}] 重复 item_id：{','.join(dup)}")
        if extra:
            issues.append(f"[{ch_no}] 超出条目范围 item_id：{','.join(extra)}")
        seen_items = set()
        for r in rules:
            iid = r["item_id"]
            if iid in seen_items:
                continue
            seen_items.add(iid)
            gid += 1
            r["rule_id"] = f"XGF-R-{gid:03d}"
            m = re.fullmatch(r"\d{2}-\d{3}", iid or "")
            if not m:
                issues.append(f"[{ch_no}] item_id 格式非法：{iid}")
            expect_source = f"{base}#条{int(iid.split('-')[1])}"
            if r.get("source") != expect_source:
                issues.append(f"[{ch_no}] source 与 item_id 不符：{r.get('source')} != {expect_source}")
            for fld in ("type", "modals", "original", "confidence"):
                if not r.get(fld):
                    issues.append(f"[{ch_no}] 缺必填字段 {fld}：{iid}")
            if r.get("type") and r["type"] not in VALID_TYPES and "+" not in r["type"]:
                issues.append(f"[{ch_no}] type 非法：{r['type']}（{iid}）")
            bad_modals = [x for x in r.get("modals", []) if x not in VALID_MODALS]
            if bad_modals:
                issues.append(f"[{ch_no}] modals 非法值：{bad_modals}（{iid}）")
            conf = r.get("confidence")
            if conf is not None and not (0 < conf <= 1):
                issues.append(f"[{ch_no}] confidence 越界：{conf}（{iid}）")
            if iid in item_ids:
                idx = int(iid.split("-")[1])
                src_item = items[idx - 1]
                if src_item.startswith("√"):
                    src_item = src_item[1:].lstrip()
                if norm(r.get("original", "")) != norm(src_item):
                    issues.append(f"[{ch_no}] original 与条文本不一致：{iid}")
            primary = r["type"].split("+")[0]
            by_type[primary] += 1
            if "+" in r["type"]:
                combo += 1
            for m_ in r["modals"]:
                by_modal[m_] += 1
            r["subject_ent_ids"] = resolve_ent_ids(r.get("subject"), alias)
        vjson = {"schema_version": SCHEMA_VER, "rule_version": RULE_VER,
                 "volume": ch_no, "chapter": ch_name, "source_file": base,
                 "item_count": len(items), "rule_count": len(rules), "rules": rules}
        with open(os.path.join(AI_DIR, f"{ch_no}_{ch_name}.json"), "w", encoding="utf-8") as f:
            json.dump(vjson, f, ensure_ascii=False, indent=1)
        per_chapter.append({"chapter_no": ch_no, "chapter": ch_name,
                            "item_count": len(items), "rule_count": len(rules)})
        all_rules.extend(rules)
        print(f"{ch_no} {ch_name}: items={len(items)} rules={len(rules)}")
    merge = {
        "schema_version": SCHEMA_VER, "rule_version": RULE_VER,
        "total_items": sum(c["item_count"] for c in per_chapter),
        "total_rules": len(all_rules), "combo_rule_count": combo,
        "by_type": dict(by_type), "by_modal": dict(by_modal),
        "per_chapter": per_chapter,
        "rule_id_range": f"XGF-R-001..XGF-R-{len(all_rules):03d}",
        "rules": all_rules,
    }
    with open(os.path.join(AI_DIR, "归一_汇总.json"), "w", encoding="utf-8") as f:
        json.dump(merge, f, ensure_ascii=False, indent=1)
    rep = ["# 规则层（AI 判定版）验证缺漏清单\n"]
    rep.append(f"- 已打包卷数：{len(per_chapter)}；条目总数：{merge['total_items']}；规则总数：{len(all_rules)}；组合规则：{combo}")
    rep.append(f"- rule_id 全局范围：{merge['rule_id_range']}")
    rep.append(f"- 问题数：{len(issues)}\n")
    for it in issues:
        rep.append("- " + it)
    with open(os.path.join(AI_DIR, "验证缺漏清单.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep))
    print("issues =", len(issues))
    print("total_rules =", len(all_rules), "combo =", combo)
    print("by_type:", dict(by_type))
    print("by_modal:", dict(by_modal))
    for it in issues[:40]:
        print("  -", it)


if __name__ == "__main__":
    main()
