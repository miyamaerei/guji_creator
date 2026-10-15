# -*- coding: utf-8 -*-
"""治谱 rule v3 终修：type 重判 + 残留错判剔 + object 抽取 + 终态标记。
输入: rule_v2.json (1065 条 auto_v2)
输出: rule_final.json (人工校验闭环后的候选)
口径：
  - type 按模态词优先级重判（禁止 > 义务 > 允许）
  - 剔纯问句/短感叹/举例残留
  - object 从句末关键词抽（词状/钱粮/保甲/衙役/里甲/文书…）
  - review_status=auto_v3，confidence 0.7
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(ROOT,"_layers","rule","rule_v2.json"),encoding="utf-8"))["records"]

# 模态词 → (type, modal) 按优先级
PATTERNS = [
    (re.compile(r"切不可|断不可|万不可|切勿|不得|不许|不可|勿"), "禁止型", "禁止"),
    (re.compile(r"必须|务要|务须|须要"), "义务型", "必须"),
    (re.compile(r"须|宜|应|当"), "义务型", "应该"),
    (re.compile(r"许|听其|听自|听"), "允许型", "可以"),
    (re.compile(r"不必|毋庸|不用|止可|只可"), "允许型", "不必"),
]
# object 关键词
OBJ_KW = ["词状","状","钱粮","银","谷","仓","保甲","里甲","牌票","文书","礼物","下程",
          "酒宴","犯人","盗贼","贼","人命","尸","狱","囚","衙役","书役","吏书","门子",
          "长随","夫马","驿","邮递","考试","学校","生员","绅士","士夫","佐贰","上司",
          "绅士","火耗","陋规","溺女","烧香","僧道","保长","甲长","地方"]

def retype(sent):
    """按模态词优先级重判 type 和 modals"""
    hits = []
    for pat, rtype, modal in PATTERNS:
        if pat.search(sent):
            hits.append((rtype, modal))
    if not hits:
        return None, []
    # 去重保序
    seen=set(); uniq=[]
    for t,m in hits:
        if (t,m) not in seen:
            seen.add((t,m)); uniq.append((t,m))
    # 主 type：禁止 > 义务 > 允许
    order = {"禁止型":0, "义务型":1, "允许型":2}
    main = sorted(uniq, key=lambda x: order[x[0]])[0][0]
    return main, list({m for _,m in uniq})

def drop(sent):
    """残留错判剔"""
    # 纯问句
    if sent.strip().endswith(("？","?")) and len(sent) < 50:
        return True
    # 短感叹句尾"矣/也"
    tail = sent.rstrip("。；，、")[-2:]
    if tail in ("矣。","也。") and len(sent) < 25:
        return True
    # 纯举例残留"有等/有一"
    if re.match(r"^(有等|有一|或有|曾有)", sent):
        return True
    return False

def guess_object(sent):
    for kw in OBJ_KW:
        if kw in sent:
            return kw
    return ""

final = []
dropped = 0
retiped = 0
for r in raw:
    sent = r["action"]
    if drop(sent):
        dropped += 1
        continue
    new_type, new_modals = retype(sent)
    if not new_type:
        dropped += 1
        continue
    if new_type != r["type"] or new_modals != r["modals"]:
        retiped += 1
        r["type"] = new_type
        r["modals"] = new_modals
    r["object"] = guess_object(sent)
    r["confidence"] = 0.7
    r["review_status"] = "auto_v3"
    final.append(r)

# 重排 id
for i, r in enumerate(final, 1):
    vol = int(r["item_id"].split("-")[0])
    r["rule_id"] = f"RULE-{vol*500+i:04d}"

out = os.path.join(ROOT,"_layers","rule","rule_final.json")
json.dump({"records": final}, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

from collections import Counter
print(f"输入 v2: {len(raw)}")
print(f"再剔: {dropped}")
print(f"type 重判: {retiped}")
print(f"输出 final: {len(final)} → {out}")
print(f"按 type: {dict(Counter(r['type'] for r in final))}")
print(f"按 object: {dict(Counter(r['object'] or '(空)' for r in final).most_common(15))}")
print(f"覆盖条目: {len(set(r['item_id'] for r in final))} / 401")
