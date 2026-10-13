# -*- coding: utf-8 -*-
"""补充L4关键词后重新分类"""
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
    ("G5 刑部", list(range(130, 146)), "LAW"),
    ("G6 工部", list(range(146, 164)), "ENG"),
    ("G7 诸文职", list(range(164, 179)), "ORG"),
    ("G8 诸武职", [179, 180], "ORG"),
]

# ===== 补充后的L4子层关键词 =====
SUBLAYER_KEYWORDS = {
    # SEL 吏部（补充：回避/选官/考满/教官）
    "SEL-XUAN": ["文选", "铨选", "选官", "除授", "升调", "回避", "注拟", "进士", "监生", "庶吉士", "御史选", "教官", "除", "选"],
    "SEL-KAO": ["考满", "考察", "拾遗", "大计", "给由", "考覈", "称职", "不称职"],
    "SEL-FENG": ["封赠", "荫叙", "诰敕", "封爵", "廕"],
    "SEL-LI": ["吏员", "掾史", "令史", "典吏", "司吏", "攒典", "书吏"],
    "SEL-DING": ["丁忧", "致仕", "起复", "终养", "养亲"],
    "SEL-HUANG": ["贴黄", "脚色", "履历"],
    # FIN 户部（补充：俸禄/户口/仓场/盐茶）
    "FIN-TIAN": ["土田", "户口", "田土", "田赋", "黄册", "人户", "民户"],
    "FIN-SHUI": ["税粮", "赋税", "夏税", "秋粮", "则例", "田赋"],
    "FIN-CAO": ["漕运", "海运", "运粮", "漕粮", "运军"],
    "FIN-CANG": ["仓庾", "库藏", "仓库", "太仓", "京仓", "粮储"],
    "FIN-LU": ["俸禄", "俸给", "折色", "折银", "俸米", "月粮"],
    "FIN-TU": ["土贡", "方物", "贡物", "贡品"],
    "FIN-ZA": ["盐法", "茶法", "钱法", "钞法", "盐课"],
    # RIT 礼部（补充：乐章/朝仪/祭祀/冠服）
    "RIT-CHAO": ["朝仪", "班序", "朝贺", "正旦", "冬至", "万寿", "百官行礼", "升殿", "还宫"],
    "RIT-SI": ["郊祀", "太庙", "宗庙", "社稷", "时享", "祫祭", "祭祀", "祭"],
    "RIT-JIA": ["冠礼", "婚礼", "丧礼", "冠婚", "丧祭", "丧仪"],
    "RIT-FU": ["冠服", "车舆", "冕旒", "服色", "仪仗", "服饰"],
    "RIT-GONG": ["朝贡", "互市", "遣使", "外国", "夷"],
    "RIT-SENG": ["僧道", "僧录", "道录", "寺观", "僧", "道"],
    "RIT-YUE": ["乐章", "乐器", "大乐", "韶乐", "曲", "杖鼓", "搏拊", "歌"],
    "RIT-SHEN": ["神祇", "山川", "坛壝", "神"],
    # MIL 兵部（补充：军职/卫所/土官/驿递）
    "MIL-XUAN": ["武选", "袭替", "世官", "武官", "军职", "都督", "留守司", "都指挥", "土官", "宣慰使", "宣抚司"],
    "MIL-WEI": ["卫所", "镇守", "防御", "城守", "卫", "千户所"],
    "MIL-GUAN": ["关津", "巡检", "巡检司", "关"],
    "MIL-YI": ["驿传", "驿递", "驿站", "递运", "驿"],
    "MIL-MA": ["马政", "牧养", "牧马", "草场", "马"],
    "MIL-QI": ["军器", "军装", "盔甲", "军资", "军"],
    # LAW 刑部（补充：斗殴/保辜/五刑/诉讼）
    "LAW-LI": ["明律", "律条", "律例", "斗殴", "保辜", "忿争", "殴人", "人命", "贼盗"],
    "LAW-WU": ["五刑", "比例", "赎刑", "赎罪", "笞", "杖", "徒", "流", "死"],
    "LAW-HUI": ["会审", "审录", "朝审", "大审"],
    "LAW-ZANG": ["追赃", "赃物", "没官", "赃"],
    "LAW-TU": ["土官", "诉讼", "原告", "被告", "告状"],
    # ENG 工部（补充：物料/宫殿/陵寝/河渠）
    "ENG-DIAN": ["宫殿", "内府", "皇极", "中极", "建极", "乾清", "坤宁", "宫"],
    "ENG-WANG": ["王府", "亲王府", "郡王府", "王府制"],
    "ENG-LING": ["陵寝", "坟茔", "山陵", "献陵", "景陵", "陵"],
    "ENG-YU": ["舟车", "大辂", "步辇", "仪仗", "车"],
    "ENG-JUN": ["军器", "军装", "盔甲", "军资"],
    "ENG-LIAO": ["物料", "工价", "木料", "砖瓦", "石灰", "颜料", "油漆", "工"],
    "ENG-HE": ["河渠", "水利", "黄河", "运河", "堤坝", "河"],
}

def classify_sublayer(domain, title, original):
    """根据域和内容判断子层"""
    text = title + original
    prefix = domain + "-"
    # 优先匹配长关键词（更具体的）
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

# 保存
outpath = os.path.join(ROOT, "_layers", "domain_tags.json")
with open(outpath, "w", encoding="utf-8") as f:
    json.dump(all_tags, f, ensure_ascii=False, indent=1)

# 统计
other_count = sum(1 for t in all_tags if t["sublayer"].endswith("OTHER"))
classified = len(all_tags) - other_count
print(f"\n{'='*60}")
print(f"总计: {len(all_tags)}条")
print(f"已分类: {classified}条 ({classified*100//len(all_tags)}%)")
print(f"未分类: {other_count}条 ({other_count*100//len(all_tags)}%)")
