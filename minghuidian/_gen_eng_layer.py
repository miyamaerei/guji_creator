# -*- coding: utf-8 -*-
"""按L4六部业务域层设计，给G6工部补ENG子层标签"""
import json, os, re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))

# ENG 工部域子层关键词映射
ENG_SUBLAYERS = {
    "ENG-DIAN": ["宫殿", "内府", "皇极", "中极", "建极", "奉天殿", "华盖殿", "谨身殿", "乾清宫", "坤宁宫"],
    "ENG-WANG": ["王府", "亲王府", "郡王府", "王府制"],
    "ENG-LING": ["陵寝", "坟茔", "陵", "山陵", "献陵", "景陵", "裕陵"],
    "ENG-YU": ["舟车", "仪仗", "大辂", "步辇", "仪仗", "车驾"],
    "ENG-JUN": ["军器", "军装", "盔甲", "刀枪", "弓箭"],
    "ENG-LIAO": ["物料", "工价", "木料", "砖瓦", "石灰", "颜料", "油漆"],
    "ENG-HE": ["河渠", "水利", "黄河", "运河", "堤坝", "闸坝"],
}

def classify_eng(title, original):
    """根据内容判断属于哪个ENG子层"""
    text = title + original
    for sublayer, keywords in ENG_SUBLAYERS.items():
        for kw in keywords:
            if kw in text:
                return sublayer
    return "ENG-OTHER"

# 给G6工部（卷144-163）的条目打ENG子层标签
eng_tags = []
seq = 0

for iid, item in reg.items():
    vol = int(iid.split("-")[0])
    if not (144 <= vol <= 163):
        continue

    seq += 1
    sublayer = classify_eng(item["title"], item["original"])
    eng_tags.append({
        "tag_id": f"ENG-TAG-{seq:03d}",
        "item_id": iid,
        "sublayer": sublayer,
        "title": item["title"][:40],
    })

print(f"G6工部条目: {len(eng_tags)} 条")
print(f"\nENG子层分布:")
sublayer_dist = Counter(t["sublayer"] for t in eng_tags)
for s, c in sublayer_dist.most_common():
    print(f"  {s:12s}: {c:3d}")

# 保存
outpath = os.path.join(ROOT, "_layers", "eng_tags.json")
with open(outpath, "w", encoding="utf-8") as f:
    json.dump(eng_tags, f, ensure_ascii=False, indent=1)
print(f"\n已保存: {outpath}")

# 抽样看ENG-OTHER是什么
print("\n=== ENG-OTHER 抽样（未分类的） ===")
others = [t for t in eng_tags if t["sublayer"] == "ENG-OTHER"]
for t in others[:10]:
    print(f"  {t['item_id']}: {t['title']}")
