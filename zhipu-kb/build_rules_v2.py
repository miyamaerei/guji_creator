# -*- coding: utf-8 -*-
"""治谱 rule 二次加工：剔错判 + 补 subject + 去重。
输入：_layers/rule/rule_auto.json（1108 条候选）
输出：_layers/rule/rule_v2.json（清洗后候选）
口径：剔掉说理/后果论述句；保留直接规范句；confidence 提到 0.6 仍标 pending。"""
import json, os, re
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(ROOT, "_layers", "rule", "rule_auto.json")
OUT = os.path.join(ROOT, "_layers", "rule", "rule_v2.json")

raw = json.load(open(IN, encoding="utf-8"))["records"]

# 说理/后果论述标志（句尾或句中）
ARG_MARKS = [
    "最苦莫大于", "可为戒", "可为鉴", "无益之", "可谓", "可笑",
    "此盖", "盖", "夫然后", "然后能", "晚矣", "此之谓", "此言",
]
# 真规范句必须含的强命令/模态词
STRONG_MODAL = re.compile(r"(不可|不得|不许|勿|切勿|必须|务要|务须|须要|须|宜|应|当|许|听|不必|毋庸|止可|只可|切不可)")

def is_arg(sent):
    """说理句判定：含明显论述标志，且句尾是感叹/判断"""
    tail = sent.rstrip("。；，、")[-3:]
    if any(m in sent for m in ARG_MARKS) and not sent.startswith(("一、","一.")):
        return True
    # 举例批评句："有等少年…""有一选官…"
    if re.match(r"^(有等|有一|或有|曾有)", sent) and tail.endswith(("矣","也")):
        return True
    # 句尾"矣/也/此"且句长>40 且无直接命令词
    if tail.endswith(("矣","也","此","哉")) and len(sent) > 40 and not re.search(r"(不可|不得|须|宜|应|当|勿|切)", sent):
        return True
    return False

def guess_subject(sent):
    """从句首抽 subject"""
    for pat in ["州县","有司","知州","知县","凡","一、","选官后","赴任后","到任后","新官","我辈","凡州县"]:
        if sent.startswith(pat):
            return pat.rstrip("、.")
    return ""

cleaned = []
seen = set()
dropped_arg = 0
dropped_dup = 0

for r in raw:
    sent = r["action"]
    # 剔说理句
    if is_arg(sent):
        dropped_arg += 1
        continue
    # 去重：同 item_id 下前 30 字相同
    key = (r["item_id"], sent[:30])
    if key in seen:
        dropped_dup += 1
        continue
    seen.add(key)
    # 补 subject
    r["subject"] = guess_subject(sent)
    r["confidence"] = 0.6
    r["review_status"] = "auto_v2"
    cleaned.append(r)

# 重排 rule_id（按 item_id 顺序）
for i, r in enumerate(cleaned, 1):
    vol = int(r["item_id"].split("-")[0])
    r["rule_id"] = f"RULE-{vol*500+i:04d}"

json.dump({"records": cleaned}, open(OUT, "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

from collections import Counter
by_type = Counter(r["type"] for r in cleaned)
print(f"输入: {len(raw)} 条")
print(f"剔说理: {dropped_arg}")
print(f"去重: {dropped_dup}")
print(f"输出: {len(cleaned)} 条 → {OUT}")
print(f"按类型: {dict(by_type)}")
print(f"覆盖条目: {len(set(r['item_id'] for r in cleaned))} / 401")
