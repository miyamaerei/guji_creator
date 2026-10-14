# -*- coding: utf-8 -*-
"""P1-B2: TIM 重构为「制度主题」时间线（Q1 制度因革链）。

旧 tim.json 按「事目/衙门/朝贡国」聚合，主题偏机构。新版按**制度主题**
（漕运/盐法/马政/赋役/屯田/科举/驿传/卫所/铨选/祭祀/朝贡/刑罚/宗藩/仓储/水利/钱法…）
聚合 rules，逐主题生成「年号 → 事件」因革链。
旧结构另存 _layers/tim_topics.json。
"""
import json, os, re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
LAY = os.path.join(ROOT, "_layers")
rules = json.load(open(os.path.join(LAY, "rules.json"), encoding="utf-8"))
PUA = {0xE5AB: "隶", 0xEA1F: "弘", 0xF5F6: "封", 0xEB08: "卷"}


def nz(t):
    return "".join(PUA.get(ord(c), c) for c in t)


THEMES = {
    "漕运": ["漕运", "漕粮", "兑运", "改兑", "白粮", "遮洋", "漕河", "运船", "攒运", "浅夫"],
    "盐法": ["盐课", "盐引", "盐法", "灶户", "盐运", "盐场", "余盐", "存积盐", "常股盐", "开中"],
    "马政": ["马政", "种马", "寄养马", "孳生马", "太仆寺", "马价", "马驹", "牧马", "儿马", "骒马"],
    "赋役": ["赋役", "黄册", "里甲", "户口", "税粮", "夏税", "秋粮", "均徭", "均工夫", "鱼鳞", "十年一造"],
    "屯田": ["屯田", "屯种", "子粒", "军屯", "民屯", "商屯", "样田", "牛具"],
    "科举": ["科举", "乡试", "会试", "殿试", "举人", "进士", "贡士", "岁贡", "生员", "学校", "提学"],
    "驿传": ["驿传", "水马驿", "递运所", "驿夫", "站银", "马夫", "铺兵", "急递铺", "驿递"],
    "卫所军伍": ["卫所", "都司", "卫指挥", "千户所", "清军", "勾军", "军籍", "军伍", "屯军", "京操"],
    "铨选考课": ["铨选", "选官", "考满", "考课", "黜陟", "保举", "举用", "选除", "推陞", "行取"],
    "祭祀": ["郊祀", "社稷", "宗庙", "太庙", "陵寝", "祠祭", "坛壝", "祭器", "牺牲", "斋戒"],
    "朝贡": ["朝贡", "朝觐", "贡使", "外夷", "番国", "四夷", "来朝", "入贡"],
    "刑罚": ["刑名", "问拟", "五刑", "充军", "赎罪", "审录", "秋审", "笞", "杖", "徒", "流"],
    "宗藩": ["宗藩", "宗室", "亲王", "郡王", "藩王", "王府", "宗人府", "玉牒", "宗支"],
    "仓储": ["仓廒", "京仓", "预备仓", "常平仓", "军储", "粮仓", "太仓", "仓场"],
    "水利河防": ["河渠", "水利", "河防", "闸坝", "堤", "圩岸", "泉"],
    "钱法": ["宝钞", "钱法", "钞法", "铸钱", "宝源局", "宝泉局", "制钱", "伪钱"],
}
ERA_ORDER = ["国初", "洪武", "建文", "永乐", "洪熙", "宣德", "正统", "景泰", "天顺",
             "成化", "弘治", "正德", "嘉靖", "隆庆", "万历"]
ERA_IDX = {e: i for i, e in enumerate(ERA_ORDER)}

# 归档旧 TIM
old = json.load(open(os.path.join(LAY, "tim.json"), encoding="utf-8"))
if old and old[0].get("topic"):
    json.dump(old, open(os.path.join(LAY, "tim_topics.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

tim = []
for theme, kws in THEMES.items():
    hit = []
    for r in rules:
        t = nz(r.get("original") or "")
        if any(k in t for k in kws):
            hit.append(r)
    if not hit:
        continue
    # 年号 → 事件
    by_era = defaultdict(list)
    for r in hit:
        era = r.get("era_first") or (r.get("era") or [""])[0]
        if not era:
            continue
        by_era[era].append(r)
    chain = []
    for era in sorted(by_era, key=lambda e: ERA_IDX.get(e, 99)):
        rs = by_era[era]
        evs = Counter(e for r in rs for e in (r.get("event_types") or []))
        chain.append({
            "era": era, "count": len(rs),
            "events": [e for e, _ in evs.most_common(6)],
            "samples": [{"item_id": r["item_id"], "volume": r.get("volume"),
                         "detail": nz(r.get("original") or "")[:70]} for r in rs[:3]],
        })
    eras = [c["era"] for c in chain]
    tim.append({
        "tim_id": "", "theme": theme, "group": "制度主题",
        "keywords": kws, "volumes": sorted({r.get("volume") for r in hit if r.get("volume")}),
        "era_span": [eras[0], eras[-1]] if eras else [],
        "rule_count": len(hit), "event_count": len(chain),
        "era_chain": chain,
    })

tim.sort(key=lambda x: -x["rule_count"])
for i, x in enumerate(tim, 1):
    x["tim_id"] = f"TIM-{i:03d}"

json.dump(tim, open(os.path.join(LAY, "tim.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print(f"TIM(制度主题) {len(tim)} 个主题；旧结构已存 tim_topics.json（{len(old)} 条）")
for x in tim:
    print(f"  {x['tim_id']} {x['theme']:6s} 规则{x['rule_count']:5d} 年号{len(x['era_chain']):2d} "
          f"跨度{x['era_span']} 卷{x['volumes'][:6]}")
