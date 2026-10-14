# -*- coding: utf-8 -*-
"""
P2-B: 建 L3.NJC 两京对照层。

凡例（001-040）："南京在洪武间为京师，自永乐定都于北，因名南京；官署并置在南京者加南京二字……
                  其事例与在京衙门不同者各列于后"
003-001："暨建两京各衙门官职并置，繁简随宜……南京所减员数正佐多寡不一，不复备列"

两类记录：
  A 机构对照：北京衙门 ↔ 南京衙门（南京清单取自卷41「南京机构名录」）
  B 制度差异：原文中"两京/南京"与差异动词（减/并/革/仍旧/同/异）同现的差异陈述
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
orgs = {p["org_name"]: p for p in json.load(open(os.path.join(LAYERS, "org_profiles.json"), encoding="utf-8"))}

VOL41 = "".join((reg[k].get("original") or "") for k in sorted(reg) if reg[k]["volume"] == 41)
VOL41_ITEMS = {k: (reg[k].get("original") or "") for k in sorted(reg) if reg[k]["volume"] == 41}


def find_vol41_item(name):
    """在卷41中定位该南京衙门所在条目。"""
    key = name.replace("南京", "")
    for k, t in VOL41_ITEMS.items():
        if name in t:
            return k
    for k, t in VOL41_ITEMS.items():
        if key and key in t and "南京" in t:
            return k
    return ""


# ---------- A. 机构对照 ----------
PAIRS = [
    ("宗人府", "南京宗人府", "永乐迁都后南京仍置宗人府，加南京二字"),
    ("吏部", "南京吏部", "永乐迁都后北京置行在吏部，南京加南京二字；南京所减员数正佐多寡不一"),
    ("户部", "南京户部", "南京户部掌南直隶及江南钱粮，员数较北京为简"),
    ("礼部", "南京礼部", "南京礼部掌南都礼仪祭祀，员数较北京为简"),
    ("兵部", "南京兵部", "南京兵部掌南都武卫及守备，员数较北京为简"),
    ("刑部", "南京刑部", "南京刑部掌南都刑名，员数较北京为简"),
    ("工部", "南京工部", "南京工部掌南都营造，员数较北京为简"),
    ("都察院", "南京都察院", "南京都察院掌南都纠劾，设右都御史等官"),
    ("通政使司", "南京通政使司", "南京通政使司掌南都章奏"),
    ("大理寺", "南京大理寺", "南京大理寺掌南都审谳"),
    ("太常寺", "南京太常寺", "南京太常寺掌南都祭祀"),
    ("光禄寺", "南京光禄寺", "南京光禄寺掌南都祭享宴劳"),
    ("鸿胪寺", "南京鸿胪寺", "南京鸿胪寺掌南都朝会仪礼"),
    ("太仆寺", "南京太仆寺", "南京太仆寺掌南直隶马政；弘治二年令南京太仆寺少卿一员分往南直隶比较马驹"),
    ("国子监", "南京国子监", "南京国子监掌南都国学，与北京国子监并置"),
    ("翰林院", "南京翰林院", "南京翰林院掌南都文翰"),
    ("尚宝司", "南京尚宝司", "南京尚宝司掌南都宝玺符牌"),
    ("钦天监", "南京钦天监", "南京钦天监掌南都天文历数"),
    ("太医院", "南京太医院", "南京太医院掌南都医疗"),
    ("五军都督府", "南京五军都督府", "南京五军都督府（中/左/右/前/后）掌南都军旅"),
    ("锦衣卫", "南京锦衣卫", "南京锦衣卫掌南都侍卫缉捕"),
    ("六科", "南京六科", "南京户科等六科，掌南都封驳稽察"),
    ("五城兵马司", "南京五城兵马司", "南京五城兵马司掌南都巡捕街道"),
    ("教坊司", "南京教坊司", "南京教坊司掌南都乐舞承应"),
    ("僧录司", "南京僧录司", "两京俱同（178-012 记道录司'两京俱同'，僧录司同例）"),
    ("道录司", "南京道录司", "两京俱同（178-012：道录司置于朝天宫，两京俱同）"),
    ("神乐观", "南京神乐观", "南京神乐观掌南都祭祀乐舞"),
    ("内官监", "南京内官监", "南京内官监（内府二十四衙门于南京并置）"),
    ("司礼监", "南京司礼监", "南京司礼监（内府于南京并置）"),
    ("御马监", "南京御马监", "南京御马监（内府于南京并置）"),
    ("兵仗局", "南京兵仗局", "南京兵仗局（内府八局于南京并置）"),
    ("织染所", "南京织染局", "南京织染局掌南都织造"),
    ("牺牲所", "南京牺牲所", "南京牺牲所掌南都祭祀牺牲"),
]

njc = []
for i, (bj, nj, diff) in enumerate(PAIRS, 1):
    bprof = orgs.get(bj, {})
    njc.append({
        "njc_id": f"NJC-{i:03d}",
        "type": "机构对照",
        "topic": f"{bj}建置",
        "beijing": bj,
        "nanjing": nj,
        "beijing_item": bprof.get("source") or "",
        "nanjing_item": find_vol41_item(nj),
        "difference": diff,
        "original": (reg.get("001-040", {}).get("original") or "")[:200],
        "source_item": "001-040",
    })

# ---------- B. 制度差异 ----------
# 高精度标记：只收「显式比较/建置差异」陈述，避免例行「南京各衙门」事例噪声
DIFF_RE = re.compile(
    r"(两京同|两京俱同|两京并置|两京并建|两京各衙门官职并置|与南京[^，。]{0,12}同|"
    r"南京.{0,6}与.{0,8}同|视南京|较南京|南京所减|南京所加|南京事例|"
    r"各衙门不同|不同者各列|繁简随宜|事例与在京|南京仍旧|南京设|南京旧卫|南京旧所|"
    r"南京亦置|南京加南京二字|南北二馆|与南京各衙门)")
SENT_SPLIT = re.compile(r"[。；　]")
seen = set()
idx = len(njc)
oldwei_sources = []          # 「南京旧卫/旧所 永乐十八年分调」集群，合并为一条
for k, v in sorted(reg.items()):
    if k == "001-040" or v["volume"] == 41:
        continue
    blob = v.get("original") or ""
    if "南京" not in blob and "两京" not in blob:
        continue
    for sent in SENT_SPLIT.split(blob):
        if len(sent) < 8 or len(sent) > 120:
            continue
        if not DIFF_RE.search(sent):
            continue
        if not re.search(r"(两京|南京)", sent):      # 分句内须真出现两京/南京
            continue
        if re.search(r"南京旧[卫所]", sent):       # 归入集群
            if k not in oldwei_sources:
                oldwei_sources.append(k)
            continue
        key = sent[:20]
        if key in seen:
            continue
        seen.add(key)
        idx += 1
        if re.search(r"(两京同|两京俱同|与南京[^，。]{0,12}同|南京.{0,6}与.{0,8}同)", sent):
            sub = "两京同制"
        elif re.search(r"(所减|所加|不同|南北二馆|繁简随宜|视南京|较南京)", sent):
            sub = "两京异制"
        else:
            sub = "南京建置"
        njc.append({
            "njc_id": f"NJC-{idx:03d}",
            "type": "制度差异",
            "subtype": sub,
            "topic": (v.get("section") or v.get("title") or "")[:20],
            "beijing": "",
            "nanjing": "南京",
            "beijing_item": "",
            "nanjing_item": k,
            "difference": sent[:120],
            "original": sent[:200],
            "source_item": k,
        })

# B2. 南京旧卫分调集群（永乐十八年由南京分调北京的卫所）
if oldwei_sources:
    idx += 1
    njc.append({
        "njc_id": f"NJC-{idx:03d}",
        "type": "制度差异",
        "subtype": "南京旧卫分调",
        "topic": "永乐十八年南京旧卫分调",
        "beijing": "北京卫所",
        "nanjing": "南京旧卫/旧所",
        "beijing_item": "",
        "nanjing_item": oldwei_sources[0],
        "difference": "多处卫所注『俱南京旧卫，永乐十八年分调』『南京旧所，永乐二十二年分调』——"
                      "永乐迁都后，原南京卫所分批北调，此为其编制沿革。",
        "original": "；".join(oldwei_sources),
        "source_item": oldwei_sources[0],
        "source_items": oldwei_sources,
    })

# B3. 凡例总述（两京体例原则）
idx += 1
njc.append({
    "njc_id": f"NJC-{idx:03d}",
    "type": "凡例总述",
    "topic": "两京体例总则",
    "beijing": "北京各衙门",
    "nanjing": "南京各衙门",
    "beijing_item": "001-040",
    "nanjing_item": "041-001",
    "difference": "南京在洪武间为京师，永乐定都于北后因名南京；官署并置在南京者加南京二字；"
                  "其事例与在京衙门不同者各列于后；南京所减员数正佐多寡不一",
    "original": (reg.get("001-040", {}).get("original") or "")[:250],
    "source_item": "001-040",
})

json.dump(njc, open(os.path.join(LAYERS, "njc.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

from collections import Counter
print("=" * 60)
print(f"NJC 层：{len(njc)} 条")
print("类型分布:", dict(Counter(x["type"] for x in njc)))
print("=" * 60)
for x in njc[:6]:
    print(f"{x['njc_id']} {x['type']} | {x['topic']}")
    print(f"   {x['difference'][:70]}")
print("...")
for x in [y for y in njc if y["type"] == "制度差异"][:8]:
    print(f"{x['njc_id']} [{x['source_item']}] {x['difference'][:70]}")
