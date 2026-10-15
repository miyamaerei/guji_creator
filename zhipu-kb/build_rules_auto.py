# -*- coding: utf-8 -*-
"""治谱 rule 层启发式提取器（词典+规则先行，AI 复核后转正）。
扫 401 条 original，按触发词切规则候选句，type 按模态猜，confidence=0.5 标 pending_review。
产出 _layers/rule/rule_auto.json；与探针 pilot.json 不冲突。"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REG = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 触发词 → (rule_type, modal)
TRIGGERS = [
    (r"不得|不可|不许|勿|切勿|切不可|断不可|万不可", "禁止型", "禁止"),
    (r"必须|务要|务须|须要|当须", "义务型", "必须"),
    (r"须|宜|应|当", "义务型", "应该"),
    (r"许|听其|听自", "允许型", "可以"),
    (r"不必|毋庸|不用", "允许型", "不必"),
]

def split_sentences(text):
    """按句读切句：。！；换行"""
    parts = re.split(r"(?<=[。！；\n])", text)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) >= 8]

def guess_type(sent):
    for pat, rtype, modal in TRIGGERS:
        if re.search(pat, sent):
            return rtype, modal
    return None, None

records = []
rid_seq = {}
for iid in sorted(REG.keys()):
    orig = REG[iid]["original"]
    vol = int(iid.split("-")[0])
    for sent in split_sentences(orig):
        rtype, modal = guess_type(sent)
        if not rtype:
            continue
        # ID 段位
        rid_seq.setdefault(vol, 0)
        rid_seq[vol] += 1
        rid = f"RULE-{vol*500+rid_seq[vol]:04d}"
        records.append({
            "rule_id": rid,
            "item_id": iid,
            "type": rtype,
            "modals": [modal],
            "condition": "",
            "subject": "",
            "action": sent[:60],
            "object": "",
            "purpose": "",
            "punishment": "",
            "original": orig,
            "confidence": 0.5,
            "review_status": "pending",
        })

out = os.path.join(ROOT, "_layers", "rule", "rule_auto.json")
json.dump({"records": records}, open(out, "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
# 统计
from collections import Counter
by_type = Counter(r["type"] for r in records)
by_vol = Counter(int(r["item_id"].split("-")[0]) for r in records)
print(f"rule 候选：{len(records)} 条 → {out}")
print(f"按类型: {dict(by_type)}")
print(f"按卷: {dict(sorted(by_vol.items()))}")
print(f"涉及条目: {len(set(r['item_id'] for r in records))} / 401")
