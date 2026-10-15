# -*- coding: utf-8 -*-
"""P4-D2：补建「名物词表」层 _layers/vocab.json

问题：objs.json 的 obj_name 只到「器皿/盔甲/印信」这类**类目**，
      查「衮冕」「令旗」「红杖」这类**具体名物**查不到。
      dress.json 有 388 条但只有 category+name；
      materials.json 60 条。
      而卷 66/148/152/153 的仪仗形制清单里全是具体名物，且已成孤立条 → 已被 P4-D 锚定。

做法：从 objs / dress / materials / 仪仗形制条文中抽取**具体名物名**，
      与 item_id 双向绑定，产出可直接查询的词表层。
不编造：只收录在原文中作为**列举项**出现的名词（带量词/数目/形制描述）。
"""
import json, os, sys, io, re
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

reg = json.load(open("_item_registry.json", encoding="utf-8"))
objs = json.load(open("_layers/objs.json", encoding="utf-8"))
dress = json.load(open("_layers/dress.json", encoding="utf-8"))
mats = json.load(open("_layers/materials.json", encoding="utf-8"))
rank = json.load(open("_layers/rank.json", encoding="utf-8"))

# 名物尾缀（明代典制名物高度规律）
TAIL = ("旗", "纛", "旛", "幡", "旌", "幢", "伞", "繖", "扇", "盖", "葢", "障",
        "杖", "棒", "瓜", "骨朵", "殳", "戟", "斧", "鎗", "枪", "戈", "矛", "刀",
        "盾", "弓", "箭", "弩", "甲", "胄", "盔", "劒", "剑", "鐧", "鞭",
        "鼓", "角", "笛", "箫", "笙", "钟", "钲", "磬", "铃", "铙", "笳", "篪", "竽",
        "轿", "辂", "辇", "车", "舆", "鞍", "辔", "鞍辔", "帐", "幕", "帷", "茵",
        "冕", "冠", "巾", "帽", "袍", "裳", "衣", "带", "佩", "圭", "韈", "舄", "履",
        "绦", "缨", "簪", "钗", "牌", "符", "印", "玺", "宝", "节", "榜", "册",
        "匣", "箱", "厨", "柜", "架", "盘", "盆", "碗", "盏", "瓶", "壶", "炉", "鼎",
        "灯", "烛", "香", "案", "几", "座", "席", "褥", "毯", "帕", "巾")
NUM = "一二三四五六七八九十百千万零数"

# 形制条文判定：含量词/尺寸词
def is_spec(text):
    return bool(re.search(r"[对副枝面张把个件只双对条片粒重尺寸分貫贯两钱觔斤]", text))


vocab = defaultdict(lambda: {"name": "", "kind": "", "items": set(), "count": 0,
                             "contexts": []})


def put(name, kind, item_id, ctx=""):
    name = name.strip()
    if len(name) < 2 or len(name) > 12:
        return
    v = vocab[name]
    v["name"] = name
    v["kind"] = v["kind"] or kind
    v["items"].add(item_id)
    v["count"] += 1
    if ctx and len(v["contexts"]) < 4:
        v["contexts"].append(ctx[:160])


# 1) objs：类目 + 上下文里的具体名
for o in objs:
    iid = o.get("item_id") or ""
    nm = o.get("obj_name") or ""
    put(nm, "器用", iid)
    blob = o.get("context") or ""
    for m in re.finditer(r"([\u4e00-\u9fff]{1,6}(?:" + "|".join(TAIL) + r"))", blob):
        put(m.group(1), "名物", iid, blob)

# 2) dress
for d in dress:
    put(d.get("name") or "", "服饰", d.get("item_id") or "")

# 3) materials
for m in mats:
    put(m.get("material") or "", "物料", m.get("item_id") or "")

# 4) rank 章服/房舍/伞盖/鞍辔 字段
for r in rank:
    lv = r.get("level") or ""
    for f in ("chaofu", "gongfu", "changfu", "jifu", "housing", "tableware",
              "umbrella", "carriage", "zhangman", "anpei"):
        v = r.get(f)
        if isinstance(v, str) and 2 <= len(v) <= 30:
            put(v, "品级制度·" + f, "", f"等级 {lv}")

# 5) 仪仗/器物形制条文（这些条已在 P4-D 被锚定，这里补名物词）
SPEC_SEC = re.compile(r"仪仗|卤簿|陈设|器用|冠服|丧服|织造|营缮|营造|窰冶|珠玉|估直")
for iid, it in reg.items():
    body = norm = (it.get("title") or "") + (it.get("original") or "")
    sec = it.get("section") or ""
    if not SPEC_SEC.search(sec):
        continue
    if not is_spec(body):
        continue
    # 抽出 "量词前的名词" 与 "数目+名词"
    for m in re.finditer(r"([\u4e00-\u9fff]{2,7}?)([一二三四五六七八九十百千万零数]*(?:对|副|枝|面|张|把|个|件|只|双|条|片|管|面|柄|乘|疋|斤|两))", body):
        put(m.group(1), "名物·" + sec[:6], iid, body)
    # 段首列举项：`X一对` 这种直接作名
    for m in re.finditer(r"^([\u4e00-\u9fff]{1,8}?)(?:[一二三四五六七八九十]+(?:对|副|枝|面|张|把|个|件|只|双|条|片))", body):
        put(m.group(1), "名物·目", iid, body)

# 过滤：去掉纯数目/明显噪声/材料前缀型误抽
BAD = re.compile(r"^[一二三四五六七八九十百千万零数两]+$|^(?:凡|及|其|今|内|外|上|下|中)$")
MAT_PREFIX = re.compile(r"^(?:硃漆|黑漆|红漆|贴金|抹金|镀金|浑金|金涂|攅竹|攒竹|木质|木匡|"
                        r"铜质|铁质|以木|以铜|以铁|以革|以帛|以竹|以皮|各色|其余|每位|每|"
                        r"制同|与|用|及|俱|并|共|如|若|其|朱漆|硃红|红色|青色|黄色|白色|黑色)")
out = []
for nm, v in vocab.items():
    if BAD.match(nm):
        continue
    if MAT_PREFIX.match(nm):
        continue
    if len(nm) < 2:
        continue
    # 名物必须以"物尾"结尾，否则是误切
    if v["kind"].startswith(("名物", "器用")) and not nm.endswith(TAIL):
        continue
    out.append({
        "name": nm, "kind": v["kind"], "count": v["count"],
        "item_count": len(v["items"]),
        "item_ids": sorted(v["items"])[:40],
        "contexts": v["contexts"],
    })
out.sort(key=lambda x: (-x["item_count"], -x["count"], x["name"]))

json.dump(out, open("_layers/vocab.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print(f"vocab 词条 {len(out)}")
print("[按 item 覆盖 top 20]")
for v in out[:20]:
    print(f"  {v['name']:12s} {v['kind']:14s} items={v['item_count']:4d} hits={v['count']}")
print()
print("[按类别]")
for k, n in Counter(v["kind"] for v in out).most_common(20):
    print(f"  {k:20s} {n}")
print()
for probe in ("衮冕", "令旗", "红杖", "班劒", "白泽旗", "冕", "印信"):
    hit = [v for v in out if probe == v["name"]]
    near = [v for v in out if probe in v["name"]][:3]
    print(f"  probe {probe:8s} exact={bool(hit)} near={[x['name'] for x in near]}")
