# -*- coding: utf-8 -*-
"""对照原文，看为什么找不到上下级关系"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 找吏部相关的条目
print("=" * 70)
print("【吏部相关条目】看原文怎么写的")
print("=" * 70)

libu_items = [(iid, item) for iid, item in reg.items() if "吏部" in item["title"] or "文选司" in item["title"]]
for iid, item in libu_items[:5]:
    print(f"\n{iid}: {item['title'][:50]}")
    print(f"  原文: {item['original'][:100]}...")

# 找都察院相关的条目
print("\n\n" + "=" * 70)
print("【都察院相关条目】看原文怎么写的")
print("=" * 70)

dcy_items = [(iid, item) for iid, item in reg.items() if "都察院" in item["title"] or "监察御史" in item["title"]]
for iid, item in dcy_items[:5]:
    print(f"\n{iid}: {item['title'][:50]}")
    print(f"  原文: {item['original'][:100]}...")

# 分析为什么找不到
print("\n\n" + "=" * 70)
print("【分析】为什么找不到上下级关系？")
print("=" * 70)
print("""
互联网知识：
- 吏部下属：文选司、验封司、稽勋司、考功司（4个清吏司）
- 都察院下属：十三道监察御史（13个道）

原文写法：
- 原文是按"部门"分卷的，吏部一卷、都察院一卷
- 每个部门下面直接列"尚书、侍郎、郎中、员外郎、主事"
- 然后列"文选司、验封司..."作为子条目

为什么我们提取不到？
1. 原文没有明确说"吏部下属有XX司"这样的句子
2. 而是用"层级结构"排版：吏部 → 文选司 → 郎中...
3. 我们的提取是按条目切的，把层级结构打散了
4. 正则只能匹配文字，识别不了排版层级

结论：
- 原文里有上下级关系，但不是用句子写的
- 是用排版层级表示的（缩进、子标题）
- 我们的文本提取把层级信息丢了
- 所以正则匹配不到"吏部下属有XX司"这样的文字
""")
