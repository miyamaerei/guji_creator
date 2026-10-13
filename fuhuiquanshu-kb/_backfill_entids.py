# -*- coding: utf-8 -*-
"""福惠 *_ent_ids 引用回填器（确定性匹配，可复现）。

范围：产物 _layers 中实际存在的 *_ent_ids 字段——
  rules.subject_ent_ids   ← subject 文本
  structs.target_ent_ids  ← target 文本
  rels.person_a_ent_ids   ← person_a 文本
  rels.person_b_ent_ids   ← person_b 文本

匹配策略（宁缺毋滥，只写确定性命中）：
  exact 全等（字段值 == ent_keys 词形）> contains 最长词形（≥2 字出现在字段值中）> split 标点拆分全等
不强行映射泛称角色（士君子/官/皇帝/绅衿 等未标实体），如实留空。

幂等：已有 *_ent_ids 非空的不覆盖；重跑结果稳定。
"""
import json, glob, os, re, shutil

ROOT = r'E:\git\ToolBox\guji\fuhuiquanshu-kb'
LAYERS = ["rules", "structs", "rels"]
BACKUP = os.path.join(ROOT, "_build", "backfill_backup")
PLAN = [
    ("rules", "subject", "subject_ent_ids"),
    ("structs", "target", "target_ent_ids"),
    ("rels", "person_a", "person_a_ent_ids"),
    ("rels", "person_b", "person_b_ent_ids"),
]

ent = json.load(open(os.path.join(ROOT, "_global", "ent_keys.json"), encoding="utf-8"))
norm = {}
for k, v in ent.items():
    norm.setdefault(re.sub(r"\s+", "", k), v)

def match_field(val):
    if not isinstance(val, str) or not val.strip():
        return None
    v = re.sub(r"\s+", "", val.strip())
    if v in norm:
        return norm[v], "exact"
    cands = [(nk, eid) for nk, eid in norm.items() if nk and len(nk) >= 2 and nk in v]
    if cands:
        best = max(cands, key=lambda t: len(t[0]))
        return best[1], "contains(%d)" % len(best[0])
    for part in re.split(r"[、，。；：,;:及与和/／\s]+", val):
        p = re.sub(r"\s+", "", part)
        if p and p in norm:
            return norm[p], "split"
    return None

os.makedirs(BACKUP, exist_ok=True)
total_filled = 0
total_hit = 0
stats = {}

for ly in LAYERS:
    files = sorted(glob.glob(os.path.join(ROOT, "_layers", ly, "*.json")))
    if not files:
        continue
    # 备份整卷文件（首次）
    for f in files:
        b = os.path.join(BACKUP, os.path.basename(f))
        if not os.path.exists(b):
            shutil.copy2(f, b)
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        changed = False
        for r in d.get("records") or []:
            if not isinstance(r, dict):
                continue
            for layer, field, idf in PLAN:
                if layer != ly:
                    continue
                cur = r.get(idf)
                if isinstance(cur, list) and cur:
                    continue  # 已回填不覆盖
                m = match_field(r.get(field))
                if m:
                    r[idf] = [m[0]]
                    total_filled += 1
                    total_hit += 1
                    stats.setdefault(idf, {}).setdefault(m[1], 0)
                    stats[idf][m[1]] += 1
                    changed = True
        if changed:
            with open(f, "w", encoding="utf-8") as fo:
                json.dump(d, fo, ensure_ascii=False, indent=1)

print("回填完成：填充字段值 %d 处" % total_filled)
for idf, s in stats.items():
    print(f"  {idf}: {sum(s.values())} 处 策略={s}")
