# -*- coding: utf-8 -*-
"""《蘧编》全卷各层验证 validate_layers.py —— 独立回读（写文件输出）
校验：item_id 归属 / ID 全局唯一 / CHR·TRL 覆盖 / ent 定位 / 枚举值（收集-报告，不中断）
"""
import json, os, re

KB = os.path.dirname(os.path.abspath(__file__))     # 项目根：脚本自身位置推导
REPORT = os.path.join(KB, "layers_验证缺漏清单.txt")
errors, gaps, pending, stats = [], [], [], {}

with open(os.path.join(KB, "_item_registry.json"), encoding="utf-8") as f:
    REG = json.load(f)

VOLUMES = [f"{i:02d}" for i in range(1, 21)]
LAYERS = ["ents", "appts", "evts", "rels", "lits", "mems", "chrs", "trls"]

# 允许枚举（基准库规范值 + 本书已决议增量；未匹配值入 pending）
ALLOW = {
    "ents": {"person","place","official","institution","work","era","object","animal","plant",
             "food","doc","system","behavior","punishment","time","quantity","posthumous","unknown"},
    "evts": {"朝政","政变","军事","军政","边事","人事任免","弹劾","礼仪","科举","文事","建言",
             "灾异","轶事","祭祀","经济","司法","神异传说","疾疫","御灾赈济","缉捕防盗","巡查监察","其他","家事"},
    "rels": {"同僚","师生","姻亲","同乡","同科","举荐","弹劾","恩怨","上下级","父子亲属","敌对","其他","同窗"},
    "appts": {"现任","致仕","升迁","贬谪","罢黜","兼领","暂代","追赠","未明","起复","世袭","举荐"},
    "chrs": {"幼年行迹","科举应试","宦途任职","朝政事务","乞休辞官","家居闲适","营建修造","家事姻亲","病逝后事","其他","家事","家事居乡","家事边事","家事朝政","朝政家事"},
    "mems_t": {"上疏","具揭","条陈","谕旨","批答","传谕","面奏","其他"},
    "mems_r": {"允准","不准","不允","留中","改拟","慰留","未报","其他"},
    "lits": {"诏敕圣旨","碑文","奏议","书启","诗","记","题跋","序","祭文","其他","集"},
    "trls": {"直译","意译","注释性翻译"},
}

def load_vol(vol):
    with open(os.path.join(KB, f"_kg_{vol}.json"), encoding="utf-8") as f:
        return json.load(f)

seen_ids = {k: set() for k in LAYERS}
used_enums = {k: set() for k in ALLOW}
ent_span_miss = []

total = {k: 0 for k in LAYERS}
for vol in VOLUMES:
    vj = load_vol(vol)
    for layer in LAYERS:
        recs = vj["records"][layer]
        total[layer] += len(recs)
        for r in recs:
            # item_id 归属
            iid = r.get("item_id", "")
            if iid not in REG:
                errors.append(f"[{layer}] {r.get('id')} item_id 不在指纹库: {iid}")
            elif not REG[iid].get("in_layer"):
                errors.append(f"[{layer}] {r.get('id')} item_id 不入层: {iid}")
            elif iid[:2] not in VOLUMES:
                errors.append(f"[{layer}] {r.get('id')} 越出卷01-20: {iid}")
            # ID 唯一
            rid = r.get("id", "")
            if rid in seen_ids[layer]:
                errors.append(f"[{layer}] ID 重复: {rid}")
            seen_ids[layer].add(rid)
            # 枚举收集
            if layer == "ents":
                used_enums["ents"].add(r.get("type",""))
            elif layer == "evts":
                used_enums["evts"].add(r.get("type",""))
            elif layer == "rels":
                used_enums["rels"].add(r.get("type",""))
            elif layer == "appts":
                used_enums["appts"].add(r.get("status",""))
            elif layer == "chrs":
                used_enums["chrs"].add(r.get("category",""))
            elif layer == "mems":
                used_enums["mems_t"].add(r.get("type",""))
                used_enums["mems_r"].add(r.get("result",""))
            elif layer == "lits":
                used_enums["lits"].add(r.get("type",""))
            elif layer == "trls":
                used_enums["trls"].add(r.get("style",""))
            # ent 定位
            if layer == "ents":
                if r.get("start") is None:
                    ent_span_miss.append(f"{rid}({r.get('text','')[:12]}) in {iid}")

# 枚举报告：未匹配值 → pending（收集-报告，不中断）
for k, vals in used_enums.items():
    allow = ALLOW[k]
    stats[k] = sorted(vals)
    for v in vals:
        if v and v not in allow:
            pending.append(f"{k}: '{v}'（不在规范值内，需决议：新增或归并）")

# CHR/TRL 覆盖：卷 01-20 共 71 条入层，应各有 chr 与 trl
chr_items = set(r["item_id"] for r in [x for vol in VOLUMES for x in load_vol(vol)["records"]["chrs"]])
trl_items = set(r["item_id"] for r in [x for vol in VOLUMES for x in load_vol(vol)["records"]["trls"]])
exp = {iid for iid in REG if REG[iid]["in_layer"] and iid[:2] in VOLUMES}
for iid in sorted(exp - chr_items):
    errors.append(f"CHR 缺失: {iid}")
for iid in sorted(exp - trl_items):
    errors.append(f"TRL 缺失: {iid}")

# 跨层索引
with open(os.path.join(KB, "_kg_join.json"), encoding="utf-8") as f:
    join = json.load(f)["records"]
exp_join = len(exp)
if len(join) != exp_join:
    errors.append(f"跨层索引条数={len(join)}，应为 {exp_join}")
zero_layer = [iid for iid, e in join.items() if e["layer_count"] == 0]
if zero_layer:
    gaps.append(f"跨层 layer_count=0 的条目: {zero_layer}")

with open(REPORT, "w", encoding="utf-8") as f:
    f.write(f"《蘧编》全卷（卷01-20）各层验证缺漏清单\n{'='*46}\n")
    f.write(f"各层总量: {total}\n")
    f.write(f"跨层索引: {len(join)} 条（卷01-20）\n")
    f.write(f"ent 定位未命中: {len(ent_span_miss)} 处\n")
    for m in ent_span_miss[:40]:
        f.write(f"  - {m}\n")
    f.write(f"\n[ERROR] {len(errors)} 项\n")
    for e in errors:
        f.write(f"  - {e}\n")
    f.write(f"\n[GAP/执行缺口] {len(gaps)} 项\n")
    for g in gaps:
        f.write(f"  - {g}\n")
    f.write(f"\n[PENDING 枚举待决议] {len(pending)} 项（收集-报告，不中断）\n")
    for p in pending:
        f.write(f"  - {p}\n")
    f.write(f"\n[枚举使用分布]\n")
    for k in sorted(stats):
        f.write(f"  {k}: {stats[k]}\n")
    f.write(f"\n结论: {'PASS' if not errors else 'FAIL'}（GAP/PENDING 为执行缺口与枚举待决议，不计入结构错误）\n")

print(f"[验证] {REPORT}")
print(f"[验证] errors={len(errors)} gaps={len(gaps)} pending={len(pending)}")
print(f"[验证] 各层总量: {total}")
for e in errors[:10]:
    print("  ERR:", e)
