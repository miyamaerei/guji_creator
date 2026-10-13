# -*- coding: utf-8 -*-
"""修正卷组边界 + 按L4六部业务域层设计，给各卷组打子层标签"""
import json, os, re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ===== 修正后的卷组边界 =====
GROUPS = [
    ("G0 宗人府", [1], "ORG"),
    ("G1 吏部", list(range(2, 14)), "SEL"),
    ("G2 户部", list(range(14, 42)), "FIN"),
    ("G3 礼部", list(range(42, 106)), "RIT"),
    ("G4 兵部", list(range(106, 130)), "MIL"),
    ("G5 刑部", list(range(130, 146)), "LAW"),  # 修正：130-145
    ("G6 工部", list(range(146, 164)), "ENG"),   # 修正：146-163
    ("G7 诸文职", list(range(164, 179)), "ORG"),
    ("G8 诸武职", [179, 180], "ORG"),
]

# ===== L4 子层关键词映射 =====
SUBLAYER_KEYWORDS = {
    # SEL 吏部
    "SEL-XUAN": ["文选", "铨选", "选官", "除授", "升调"],
    "SEL-KAO": ["考满", "考察", "拾遗", "大计"],
    "SEL-FENG": ["封赠", "荫叙", "诰敕", "封爵"],
    "SEL-LI": ["吏员", "掾史", "令史", "典吏", "司吏"],
    "SEL-DING": ["丁忧", "致仕", "起复", "终养"],
    "SEL-HUANG": ["贴黄", "脚色", "履历"],
    # FIN 户部
    "FIN-TIAN": ["土田", "户口", "田土", "田赋", "黄册"],
    "FIN-SHUI": ["税粮", "赋税", "夏税", "秋粮", "则例"],
    "FIN-CAO": ["漕运", "海运", "运粮", "漕粮"],
    "FIN-CANG": ["仓庾", "库藏", "仓库", "太仓", "京仓"],
    "FIN-LU": ["俸禄", "俸给", "折色", "折银"],
    "FIN-TU": ["土贡", "方物", "贡物"],
    "FIN-ZA": ["盐法", "茶法", "钱法", "钞法"],
    # RIT 礼部
    "RIT-CHAO": ["朝仪", "班序", "朝贺", "正旦", "冬至", "万寿"],
    "RIT-SI": ["郊祀", "太庙", "宗庙", "社稷", "时享", "祫祭"],
    "RIT-JIA": ["冠礼", "婚礼", "丧礼", "冠婚", "丧祭"],
    "RIT-FU": ["冠服", "车舆", "冕旒", "服色", "仪仗"],
    "RIT-GONG": ["朝贡", "互市", "遣使", "外国"],
    "RIT-SENG": ["僧道", "僧录", "道录", "寺观"],
    "RIT-YUE": ["乐章", "乐器", "大乐", "韶乐"],
    "RIT-SHEN": ["神祇", "山川", "坛壝"],
    # MIL 兵部
    "MIL-XUAN": ["武选", "袭替", "世官", "武官"],
    "MIL-WEI": ["卫所", "镇守", "防御", "城守"],
    "MIL-GUAN": ["关津", "巡检", "巡检司"],
    "MIL-YI": ["驿传", "驿递", "驿站", "递运"],
    "MIL-MA": ["马政", "牧养", "牧马", "草场"],
    "MIL-QI": ["军器", "军装", "盔甲", "军资"],
    # LAW 刑部
    "LAW-LI": ["明律", "律条", "律例", "笞杖", "徒流"],
    "LAW-WU": ["五刑", "比例", "赎刑", "赎罪"],
    "LAW-HUI": ["会审", "审录", "朝审", "大审"],
    "LAW-ZANG": ["追赃", "赃物", "没官"],
    "LAW-TU": ["土官", "诉讼", "原告", "被告"],
    # ENG 工部
    "ENG-DIAN": ["宫殿", "内府", "皇极", "中极", "建极", "乾清", "坤宁"],
    "ENG-WANG": ["王府", "亲王府", "郡王府"],
    "ENG-LING": ["陵寝", "坟茔", "山陵", "献陵", "景陵"],
    "ENG-YU": ["舟车", "大辂", "步辇", "仪仗"],
    "ENG-JUN": ["军器", "军装", "盔甲", "军资"],
    "ENG-LIAO": ["物料", "工价", "木料", "砖瓦", "石灰", "颜料"],
    "ENG-HE": ["河渠", "水利", "黄河", "运河", "堤坝"],
}

def classify_sublayer(domain, title, original):
    """根据域和内容判断子层"""
    text = title + original
    prefix = domain + "-"
    for sublayer, keywords in SUBLAYER_KEYWORDS.items():
        if not sublayer.startswith(prefix):
            continue
        for kw in keywords:
            if kw in text:
                return sublayer
    return prefix + "OTHER"

# ===== 执行分类 =====
all_tags = []
for gname, vols, domain in GROUPS:
    g_items = [(iid, item) for iid, item in reg.items() if int(iid.split("-")[0]) in vols]

    sublayer_dist = Counter()
    for iid, item in g_items:
        sl = classify_sublayer(domain, item["title"], item["original"])
        sublayer_dist[sl] += 1
        all_tags.append({
            "item_id": iid,
            "volume": int(iid.split("-")[0]),
            "group": gname,
            "domain": domain,
            "sublayer": sl,
            "title": item["title"][:40],
        })

    print(f"\n【{gname}】({domain}) 共{len(g_items)}条")
    print(f"  {'子层':15s} {'数量':>5s} {'占比':>6s}")
    print("  " + "-" * 35)
    for sl, cnt in sublayer_dist.most_common():
        pct = cnt * 100 // len(g_items)
        bar = "█" * (pct // 2)
        print(f"  {sl:15s} {cnt:5d} ({pct:3d}%) {bar}")

# 保存所有标签
outpath = os.path.join(ROOT, "_layers", "domain_tags.json")
with open(outpath, "w", encoding="utf-8") as f:
    json.dump(all_tags, f, ensure_ascii=False, indent=1)
print(f"\n已保存所有标签: {outpath} ({len(all_tags)}条)")

# 统计有多少OTHER
other_count = sum(1 for t in all_tags if t["sublayer"].endswith("OTHER"))
print(f"\n未分类(OTHER): {other_count} 条 ({other_count*100//len(all_tags)}%)")
