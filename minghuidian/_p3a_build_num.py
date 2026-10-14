# -*- coding: utf-8 -*-
"""P3-A: 建 L5.NUM 数字则例层（Q8「夏税/秋粮/盐引…具体数额」）。

从全库抽取「主体 + 数额 + 单位」键值对。主体锚定于经济/军事/编制类关键词，
避免「六部」「一员」等结构计数噪声。单位含 石/斗/升/两/钱/分/贯/文/锭/斤/引/匹/顷/亩/户/丁/名…
"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

PUA = {0xE5AB: "隶", 0xEA1F: "弘", 0xF5F6: "封", 0xEB08: "卷", 0xE205: "笙"}


def nz(t):
    return "".join(PUA.get(ord(c), c) for c in t)


# 主体（按语义分类）
SUBJ = {
    "税粮": r"(税粮|夏税|秋粮|秋粮米|夏税麦|税粮米|兑运|改兑|漕粮|白粮|南粮|北粮|本色|折色)",
    "盐课": r"(盐课|盐引|盐斤|户口盐|盐钞|引盐|余盐|存积盐|常股盐)",
    "银钞": r"(赃罚银|马价银|工食银|料价银|驿站银|站银|柴薪银|课银|税银|折银|宝钞|寳钞|钞|银)",
    "屯田": r"(屯田|屯粮|子粒|屯种|样田|牛具|屯地)",
    "马政": r"(种马|寄养马|孳生马|备养马|马驹|儿马|骒马|马)",
    "户口": r"(户口|人户|户|口|丁|成丁|壮丁|军丁|灶丁|盐丁)",
    "军伍": r"(军士|屯军|舍余|军余|操军|备倭军|京军|班军|募军|民壮|弓兵|机兵|军)",
    "钱粮": r"(月粮|俸粮|廪米|禄米|俸银|口粮|行粮|粮米|米|麦|豆|草|谷|谷)",
    "编制": r"(典吏|令史|承差|知印|监生|生员|举人|贡生|斗级|库子|马夫|铺兵|驿夫|皂隶)",
}
NUM = r"([0-9]{1,10}|[一二三四五六七八九十百千万亿零两]{1,15})"
UNIT = (r"(石|斗|升|合|勺|两|钱|分|厘|毫|贯|文|锭|錠|斤|匹|疋|引|束|"
        r"顷|畒|亩|户|口|丁|名|颗|隻|只|艘|领)")
UNIT2 = r"(斤|两|钱|分|石|斗|升|匹|疋|引|顷|亩|畒)"   # 「每X Y」折算率

# 单字主体的上下文字校验（排除 清吏司/司马/户部/甲乙丙丁 等词内误切）
BAD_PRE = {"吏": "清司官文书", "户": "民", "丁": "甲乙丙", "马": "司兵御仓攅",
           "军": "器", "银": "金", "钞": "宝寳", "米": "稻", "谷": "黍",
           "草": "甘", "口": "户", "名": "姓"}
BAD_NXT = {"户": "部科", "军": "器", "银": "矿", "名": "字", "马": "百千"}


def ok_subject(t, s, e, subj):
    if len(subj) >= 2:
        return True
    if subj in BAD_PRE and s > 0 and t[s - 1] in BAD_PRE[subj]:
        return False
    if subj in BAD_NXT and e < len(t) and t[e] in BAD_NXT[subj]:
        return False
    return True

# 主体+（≤6字）+数字+单位
RULES = []
for cat, rx in SUBJ.items():
    RULES.append((cat, re.compile(rx + r"[^\u3000，。；：、（）【】]{0,3}?" + NUM + UNIT)))
    # 折算率：每 + 单位 + 数字 + 单位2
    RULES.append((cat + "·折算", re.compile(rx + r".{0,4}?每" + UNIT + NUM + UNIT2)))

records = []
seen = set()
for k, v in sorted(reg.items()):
    t = nz(v.get("original") or "")
    for cat, rx in RULES:
        for m in rx.finditer(t):
            g = m.groups()
            subj, q, unit = g[0], g[-2], g[-1]
            if q in ("", "零"):
                continue
            if unit == "户" and q in ("千", "万"):     # 千户/万户 系官称，非户口数
                continue
            # 主体词内误切校验：找到主体在整段中的位置
            sj = t.rfind(subj, max(0, m.start() - 4), m.end())
            if sj < 0 or not ok_subject(t, sj, sj + len(subj), subj):
                continue
            key = (k, cat, subj, q, unit)
            if key in seen:
                continue
            seen.add(key)
            records.append({
                "num_id": "", "item_id": k, "volume": v.get("volume"),
                "category": cat.split("·")[0], "kind": "折算率" if cat.endswith("折算") else "数额",
                "subject": subj, "quantity": q, "unit": unit,
                "context": t[max(0, m.start() - 6):m.end() + 6],
                "original": t[:160],
            })

records.sort(key=lambda x: x["item_id"])
for i, r in enumerate(records, 1):
    r["num_id"] = f"NUM-{i:05d}"

os.makedirs(os.path.join(ROOT, "_layers"), exist_ok=True)
json.dump(records, open(os.path.join(ROOT, "_layers/num.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print(f"NUM 层：{len(records)} 条")
print("类别:", dict(Counter(r["category"] for r in records)))
print("单位 Top15:", dict(Counter(r["unit"] for r in records).most_common(15)))
print("卷 Top10:", dict(Counter(r["volume"] for r in records).most_common(10)))
print("--- 抽样 ---")
for r in records[:20]:
    print(f"  [{r['item_id']}|{r['category']}] {r['subject']} {r['quantity']}{r['unit']}  «{r['context'][:26]}»")
