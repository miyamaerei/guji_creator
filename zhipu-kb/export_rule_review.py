# -*- coding: utf-8 -*-
"""把 rule_v2 按 10 条一组导出人工校验 markdown 清单。
输出 _validate/rule_review/groups.md + 每组一个独立小文件。
"""
import json, os, math

ROOT = os.path.dirname(os.path.abspath(__file__))
src = json.load(open(os.path.join(ROOT, "_layers", "rule", "rule_v2.json"), encoding="utf-8"))["records"]
out_dir = os.path.join(ROOT, "_validate", "rule_review")
os.makedirs(out_dir, exist_ok=True)

groups = [src[i:i+10] for i in range(0, len(src), 10)]
print(f"共 {len(src)} 条，分 {len(groups)} 组（每组 10 条）")

# 总览 index
index = ["# 治谱 rule 人工校验清单\n",
         f"- 总数：{len(src)} 条\n- 分组：{len(groups)} 组\n- 状态：待校验（review_status=auto_v2）\n",
         "| 组号 | 条数 | 条目范围 | 状态 |\n|---|---|---|---|"]
for gi, g in enumerate(groups, 1):
    rng = f"{g[0]['item_id']} ~ {g[-1]['item_id']}"
    index.append(f"| 第 {gi:03d} 组 | {len(g)} | {rng} | ☐ 待校 |\n")

open(os.path.join(out_dir, "00_index.md"), "w", encoding="utf-8").write("".join(index))

# 每组一个文件
for gi, g in enumerate(groups, 1):
    lines = [f"## 第 {gi:03d} 组（{g[0]['item_id']} ~ {g[-1]['item_id']}）\n\n"]
    lines.append("| # | rule_id | item_id | type | modals | action（待校） | 判定 |\n")
    lines.append("|---|---|---|---|---|---|---|\n")
    for i, r in enumerate(g, 1):
        action = r["action"].replace("|","/").replace("\n"," ")
        if len(action) > 80: action = action[:80]+"…"
        lines.append(f"| {i} | {r['rule_id']} | {r['item_id']} | {r['type']} | {','.join(r['modals'])} | {action} | ☐ 保留/删/改 |\n")
    open(os.path.join(out_dir, f"group_{gi:03d}.md"), "w", encoding="utf-8").write("".join(lines))

print(f"清单已导出 → {out_dir}")
print(f"  00_index.md（总览）")
print(f"  group_001.md ~ group_{len(groups):03d}.md")
