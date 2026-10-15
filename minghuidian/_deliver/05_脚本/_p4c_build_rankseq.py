# -*- coding: utf-8 -*-
"""P4-C 品级序列（rank_sequence）：把卷12 文职品级名录解析成
   {品级 -> [官职名]} 的结构，并把每个官职行反向挂到对应 item_id。

   卷12 行文规律：
     - 品级标记「正一品」「从二品」「正三品」…「未入流」作为**段首内嵌标记**
     - 其后跟随若干官职名，以全角空格（　）/【注】分隔
     - 【…】为朝代的 "后添设/后革/后为寺" 等沿革小注，不是官名
   产出：_layers/rank_sequence.json + 每行的 item_id 归属，供 join 挂载。
"""
import json, os, re, sys, io
from collections import defaultdict, OrderedDict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

LEVELS = ["正一品", "从一品", "正二品", "从二品", "正三品", "从三品",
          "正四品", "从四品", "正五品", "从五品", "正六品", "从六品",
          "正七品", "从七品", "正八品", "从八品", "正九品", "从九品", "未入流"]
LV_RE = re.compile("(" + "|".join(LEVELS) + ")")

# 沿革小注 / 非官名片段
NOTE_RE = re.compile(r"【[^】]*】")
JUNK = {"已上增", "后添设", "后革", "后为寺", "旧正八品", "旧从八品", "旧正九品",
        "旧从九品", "旧未入流", "后陞正七品", "后陞从七品", "后陞正八品", "后陞从九品",
        "回回监正后革", "回回监副后革", "回回监五官正后革", "回回监主簿五官保章正后革",
        "回回监五官灵台郎后革", "回回监五官挈壶正后革", "回回监五官司厯后革",
        "回回监五官司晨后革", "寳泉局大使后革", "寳泉局副使后革"}

# 非品级名录的说明性条目（沿革/勋级前言），逐条排除
SKIP_ITEMS = {"012-004"}


def clean(txt):
    """去注、去空格、还原 PUA。"""
    t = NOTE_RE.sub("　", txt or "")
    t = t.replace("　", "\n")
    return [x.strip() for x in t.split("\n") if x.strip()]


def parse_volume(vol, system):
    """把某卷解析为 [(level, office_text, item_id)]。

    关键：会典卷12 把「品级标记」与「官职名」混排，
      有时同一 item 内（`从一品少保　少傅`），
      有时品级独占一个 item（`012-011 名录行 从二品`），其后若干 item 都属该品级。
    故 cur_level 必须**跨 item 延续**，不能每个 item 重置。

    另：卷12 首段（太师/太傅/太保…）无显式「正一品」标记——会典以文职衙门之首开篇，
    按明制这三公即正一品，故**初值设为「正一品」**而非 None。
    """
    out = []
    markers = []                  # 纯品级标记行，单独记账（供 join 挂 rank 层）
    cur_level = "正一品"          # 卷12 首段隐式正一品（太师/太傅/太保）
    for k in sorted(k for k in reg if k.startswith(f"{vol:03d}-")):
        it = reg[k]
        # 012-001~004 是「勋级/散官」事例与沿革说明，不是品级名录，跳过
        if it.get("node_kind") == "事例" or k in SKIP_ITEMS:
            continue
        for seg in clean(it.get("original") or ""):
            # 纯品级标记行（如「从二品」独占一条）→ 记为 marker，并更新游标
            if seg in LEVELS:
                cur_level = seg
                markers.append({"level": seg, "item_id": k})
                continue
            parts = LV_RE.split(seg)
            pre = parts[0].strip()
            if pre and pre not in JUNK:
                out.append((cur_level, pre, k))
            for i in range(1, len(parts), 2):
                cur_level = parts[i]
                post = parts[i + 1].strip() if i + 1 < len(parts) else ""
                if post and post not in JUNK:
                    out.append((cur_level, post, k))
    return out, markers


rows, markers = parse_volume(12, "文职")
print("卷12 解析行数:", len(rows), "｜ 品级标记行:", len(markers))

# 归并：每行按全角空格已是单段；再按 "　" 已拆过。下面做细分：
# 段内若仍含多个官名（无空格分隔，如「六部尚书都察院左右都御史」），保留整段，
# 但另存拆分候选，便于查询时模糊命中。
seq = OrderedDict((lv, []) for lv in LEVELS)
for lv, text, iid in rows:
    if not lv:
        continue
    if text in JUNK:
        continue
    seq.setdefault(lv, [])
    seq[lv].append({"text": text, "item_id": iid})

# 汇总统计
marker_by_level = defaultdict(list)
for m in markers:
    marker_by_level[m["level"]].append(m["item_id"])

result = []
for lv in LEVELS:
    segs = seq.get(lv, [])
    if not segs:
        continue
    item_ids = sorted({s["item_id"] for s in segs} | set(marker_by_level.get(lv, [])))
    result.append({"level": lv, "order": LEVELS.index(lv) + 1,
                   "segment_count": len(segs),
                   "marker_item": sorted(set(marker_by_level.get(lv, []))),
                   "item_ids": item_ids,
                   "segments": [s["text"] for s in segs]})

json.dump(result, open(os.path.join(LAYERS, "rank_sequence.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print()
for r in result:
    print(f"  {r['level']:5s} 段 {r['segment_count']:3d} 条 | item {len(r['item_ids']):3d} | "
          f"{' ｜ '.join(r['segments'][:3])[:80]}")
total_seg = sum(r["segment_count"] for r in result)
all_items = set()
for r in result:
    all_items |= set(r["item_ids"])
print(f"\n合计段落 {total_seg}，品级 {len(result)} 级，覆盖 item {len(all_items)}")
print("写出 _layers/rank_sequence.json")
