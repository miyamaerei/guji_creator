# -*- coding: utf-8 -*-
"""
P2-D: 建 L3.GEO 地理管辖树（省→府→州→县，都司→卫→所）。

数据源：
  卷17-18 图志：省头「X府N　州M县K…（尾部/另项为第一府「X府领州a县b」）」
                → 府头「X府领[州a]县b」 → 名录行 = 州/县/土司 名
  卷108 都司卫所：事目/长文 = 都司/都督府/留守司/亲军/南京 头 → 卫/所 名

要点：
  · OCR PUA 字形还原（隶=U+E5AB 等）
  · 府名 = 「府」前 2 字（明府名皆为二字+府；「军民府」取前 2 字+军民府）；
    府头常嵌在上一府属名之后（如「…平谷县保定府领州三县十七」）
  · 段内以全角空格 U+3000 分词；属名可为 县/州/府/军民府/长官司 等
  · 父子关系在生成时以 geo_id 绑定，避免「太平府」等同名府跨省串接
"""
import json, os, re
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ---------------- PUA 归一化 ----------------
PUA_MAP = {
    0xE5AB: "隶", 0xEA1F: "弘", 0xEB91: "发", 0xEE70: "赃", 0xE7B5: "候", 0xECDE: "点",
    0xE898: "瓜", 0xEA92: "敕", 0xEF6E: "扬", 0xEA20: "玄", 0xE638: "葬", 0xE6A2: "雨",
    0xEF33: "类", 0xEA77: "帖", 0xE880: "派", 0xF848: "帘", 0xE3E7: "弊", 0xEB64: "带",
    0xEEA3: "递", 0xE3BD: "再", 0xE645: "紧", 0xE205: "笙", 0xE177: "引", 0xEDAB: "弦",
    0xEE60: "赓", 0xECEA: "瓜", 0xE730: "龟", 0xEF6C: "场", 0xECB9: "兰", 0xECD5: "羹",
    0xEB07: "参", 0xE3C8: "伞", 0xEF3D: "团", 0xECFB: "牦", 0xECB5: "泥", 0xED36: "献",
    0xED88: "房", 0xECC9: "丝", 0xEB8E: "弦", 0xEEB7: "烟", 0xEC68: "瓜", 0xE4BF: "碎",
    0xEDD5: "顶", 0xEC6A: "沔", 0xEBF1: "攒", 0xE4BE: "珊", 0xEA5B: "传", 0xEE1D: "廪",
    0xF5F6: "封", 0xEEE5: "侵", 0xF5B4: "钗", 0xEAA3: "廨", 0xEB34: "密", 0xEED7: "隐",
    0xE109: "高", 0xEBCA: "懒", 0xEF07: "馔", 0xEECC: "钺", 0xEE10: "蔬", 0xEF67: "参",
    0xECCA: "烽", 0xEE9A: "回", 0xE620: "夏", 0xEDBE: "报", 0xE621: "朔", 0xEDFB: "葅",
    0xEB3F: "呈", 0xECF0: "状", 0xEAFA: "丞", 0xEECD: "铅", 0xEA60: "拨", 0xEE25: "亏",
    0xF539: "贝", 0xED30: "诚", 0xE6D9: "诓", 0xEDB6: "绑", 0xED3C: "盥", 0xEA9F: "郎",
    0xF662: "襕", 0xED68: "襕", 0xEA1A: "鸂", 0xEC6E: "膊", 0xEA65: "伞", 0xF52A: "匕",
    0xEE18: "喷", 0xEF2D: "面", 0xE982: "糗", 0xEF11: "辈", 0xEA40: "凶", 0xE8FF: "升",
    0xED00: "硝", 0xE9E8: "煠", 0xED8E: "篪", 0xF866: "姚", 0xEDB4: "缅", 0xED21: "瘗",
    0xEBF2: "搀", 0xED7B: "秽", 0xE5D6: "窗", 0xEAA5: "厅", 0xEA35: "盂", 0xEB3C: "将",
    0xEBB3: "员", 0xEC1B: "尾", 0xEADD: "木", 0xE187: "兴", 0xED6A: "复", 0xEF2A: "剑",
    0xEAAC: "谷", 0xE6BF: "每", 0xE166: "苎", 0xEC74: "晋", 0xED94: "试", 0xED20: "刁",
    0xEEC7: "沙", 0xE172: "积", 0xEB45: "履", 0xED3F: "眩", 0xE220: "捧", 0xEBC0: "欣",
    0xEE7E: "蹈", 0xEAA4: "升", 0xEB12: "彝", 0xEE19: "藻", 0xE900: "网", 0xE313: "袜",
    0xE580: "抹", 0xEC42: "毕", 0xEA57: "奏", 0xEC64: "戟", 0xEB5F: "毕", 0xE699: "馔",
    0xEA59: "侍", 0xE6AF: "仰", 0xEE06: "蓬", 0xEC78: "卫", 0xEDA3: "黍", 0xEDA2: "笾",
    0xE9D5: "旴", 0xEDE3: "芒", 0xEA32: "牧", 0xE596: "幡", 0xED7A: "祯", 0xF65D: "括",
    0xEA39: "悬", 0xEA79: "敛", 0xF65E: "撒", 0xEE29: "蔗", 0xEB2C: "边", 0xEEA6: "蓬",
    0xE064: "奇", 0xE80F: "沐", 0xEB68: "弩", 0xEDB8: "痊", 0xECA9: "龙", 0xE11E: "溪",
    0xE443: "峨", 0xEC55: "郁", 0xEA91: "敕", 0xEB2F: "谋", 0xEB4E: "峰", 0xEB99: "养",
    0xED73: "社", 0xED3B: "盐", 0xEB81: "舶", 0xEABF: "詹", 0xEB37: "叛", 0xED92: "垛",
    0xEBF4: "侵", 0xEB86: "缴", 0xEBB7: "刻", 0xECD9: "铜", 0xEC50: "辐", 0xE60A: "焊",
    0xEC70: "泖", 0xF8A8: "壁", 0xE189: "硼", 0xE3D0: "兔", 0xEBE8: "点", 0xEF6D: "旸",
    0xEB08: "卷",
}


def nz(t):
    return "".join(PUA_MAP.get(ord(c), c) for c in t)


# ---------------- 中文数字 ----------------
CN_D = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def cn2i(s):
    if not s:
        return None
    if "百" in s:
        a, b = s.split("百", 1)
        return (CN_D.get(a, 1) * 100) + (cn2i(b) or 0)
    if s == "十":
        return 10
    if "十" in s:
        a, b = s.split("十", 1)
        return (CN_D.get(a, 1) * 10) + (CN_D.get(b, 0) if b else 0)
    return CN_D.get(s)


# ---------------- 行政单位抽取 ----------------
SUFFIXES = ("守御千户所", "千户所", "百户所", "军民府", "府", "县", "州")
UNIT_RE = re.compile(r"[\u4e00-\u9fff]{1,4}?(?:" + "|".join(SUFFIXES) + ")")
TU_SI = ("长官司", "宣慰司", "宣抚司", "安抚司", "招讨司")
# 土司常以「X州」为名（播州宣慰使司/真州长官司/平州陆洞长官司），须优先整体识别
TU_SUF = ("宣慰使司", "宣抚使司", "安抚使司", "招讨使司", "宣慰司", "宣抚司",
          "安抚司", "招讨司", "长官司")
TU_RE = re.compile(r"[\u4e00-\u9fff]{1,4}?(?:" + "|".join(TU_SUF) + ")")
ALL_SUF = sorted(set(SUFFIXES) | set(TU_SUF), key=len, reverse=True)
MAX_SUF = max(len(s) for s in ALL_SUF)
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
BAD_PRE = set("属俱领等诸其所有以及凡数处内外附隶")
BAD_TU = set("领属等其凡数处内外附")
NUMCH = "一二三四五六七八九十百"


def strip_note(t):
    return re.sub(r"[【（(][^】）)]*[】）)]", "", t)


def extract_units(text):
    """左→右最长匹配切分行政单位（府/军民府/州/县/土司），避免跨名误切。

    要点：名长 1–4 字；民职名不含「县/府」（故「兖州府」之名「兖州」合法，
    而「陵县泰安」非法）；土司名可含「州」（播州宣慰使司 / 平州陆洞长官司）。
    """
    clean = strip_note(text)
    found = []
    pos, n = 0, len(clean)
    while pos < n:
        hit = None
        for L in range(min(6 + MAX_SUF, n - pos), 1, -1):
            cand = clean[pos:pos + L]
            suf = next((s for s in ALL_SUF if cand.endswith(s)), None)
            if not suf:
                continue
            nm = cand[:-len(suf)]
            maxn = 6 if suf in TU_SUF else 4     # 土司名可长（洪州泊里蛮夷长官司）
            if not (1 <= len(nm) <= maxn):
                continue
            if not all(CJK_RE.match(c) for c in nm):
                continue
            if any(c in BAD_PRE or c in NUMCH for c in nm):
                continue
            if suf == "县" and any(c in "州府" for c in nm):    # 「邠州淳化县」须切成 邠州+淳化县
                continue
            if suf == "州" and any(c in "县府" for c in nm):
                continue
            if suf in ("府", "军民府") and "县" in nm:           # 府名可含州（兖州府）
                continue
            if suf in TU_SUF and any(c in BAD_TU for c in nm):
                continue
            hit = (cand, suf)
            break
        if hit:
            found.append(hit)
            pos += len(hit[0])
        else:
            pos += 1
    return found


PROV_HEAD = re.compile(r"^(北直隶|南直隶|([\u4e00-\u9fff]{2,3})等处承宣布政使司)府[一二三四五六七八九十百]+")
CNT_RE = re.compile(r"府([一二三四五六七八九十百]+)[\u3000\s]*"
                    r"(?:州([一二三四五六七八九十百]+))?[\u3000\s]*"
                    r"县([一二三四五六七八九十百]+)")
JUNMIN_RE = re.compile(r"军民府([一二三四五六七八九十百]+)")
FU_QUOTA = re.compile(r"府领州([一二三四五六七八九十百]+)")   # 府声明属州数
DUSI_A = re.compile(r"([\u4e00-\u9fff]{2})都指挥使司")          # 图志内都司段
COUNT_SEG = re.compile(r"(?:宣慰司|宣抚司|安抚司|招讨司|长官司|军民府|都司|留守司|"
                       r"都督府|盐运司|盐课提举司|市舶提举司|河渠提举司|州|县|府|司)"
                       r"[一二三四五六七八九十百]")               # 计数段特征


def norm_prov(raw):
    if raw in ("北直隶", "南直隶"):
        return raw
    core = raw.replace("等处", "").replace("承宣布政使司", "").strip()
    m = re.match(r"([\u4e00-\u9fff]{2,3})", core)
    return (m.group(1) if m else core) + "布政使司"


def split_fu(seg):
    """返回 (府名, 前缀文本, 头后余文) 或 None。府名 = 后缀前 2 字。"""
    for tail, extra in (("军民府领", "军民府"), ("府领", "府")):
        i = seg.find(tail)
        if i < 0:
            continue
        before = seg[:i]
        j = max(0, len(before) - 2)
        return before[j:] + extra, before[:j], seg[i + len(tail):]
    return None


ZHILI_RE = re.compile(r"([\u4e00-\u9fff]{2,3}州)[^【]{0,8}【[^】]*直隶")


# ---------------- 节点 ----------------
nodes = []
gidx = 0


def add(name, ntype, parent_name, parent_id, level, item_id, original, extra=None):
    global gidx
    gidx += 1
    rec = {
        "geo_id": f"GEO-{gidx:04d}", "name": name, "type": ntype,
        "parent": parent_name or "", "parent_id": parent_id or "",
        "children": [], "level": level, "administered_by": parent_name or "",
        "garrisons": [], "post_stations": [], "granaries": [],
        "volume": reg[item_id]["volume"], "item_id": item_id,
        "original": (original or "")[:120],
    }
    if extra:
        rec.update(extra)
    nodes.append(rec)
    return rec


class ProvState:
    """图志解析游标：省 / 府（含属州配额）/ 属州。"""
    def __init__(self):
        self.prov_name = self.fu_name = self.zhou_name = None
        self.prov_id = self.fu_id = self.zhou_id = ""
        self.fu_quota = 0          # 本府声明属州数
        self.fu_used = 0           # 已归本府之属州数


def emit_units(text, raw, item_id, st, as_prov=None):
    """抽取并挂靠行政单位（省→府→属州→县）。

    图志格式：`X府领州a县b` → 先列府直辖县 → 遇 `X州` 则其后县归该属州，
    直至下一属州或下一府头；超出府声明州数者判为直隶州（隶布政司）。
    """
    as_prov = as_prov or set()
    for name, suf in extract_units(text):
        if suf in TU_SI:
            add(name, "土司", st.fu_name or st.prov_name, st.fu_id or st.prov_id,
                "土司", item_id, raw)
        elif suf in ("府", "军民府"):
            add(name, "府", st.prov_name, st.prov_id, "府", item_id, raw)
        elif suf == "州":
            if name in as_prov or st.fu_used >= st.fu_quota:   # 直隶布政司之州
                node = add(name, "州", st.prov_name, st.prov_id, "州/县", item_id, raw,
                           {"note": "直隶布政司"})
            else:                                              # 府之属州
                node = add(name, "州", st.fu_name, st.fu_id, "州/县", item_id, raw)
                st.fu_used += 1
            st.zhou_name, st.zhou_id = name, node["geo_id"]
        elif suf == "县":
            if st.zhou_id:                                     # 属州之县（二级展开）
                add(name, "县", st.zhou_name, st.zhou_id, "州/县", item_id, raw)
            else:                                              # 府之直辖县
                add(name, "县", st.fu_name or st.prov_name, st.fu_id or st.prov_id,
                    "州/县", item_id, raw)


# ============ A. 省→府→州→县（卷17-18） ============
seq = [(k, nz(v.get("original") or "")) for k, v in sorted(reg.items())
       if v["volume"] in (17, 18)]
seq = [(k, t) for k, t in seq if t]

st = ProvState()
prov_decl = {}

for idx, (k, t) in enumerate(seq):
    nxt = seq[idx + 1][1] if idx + 1 < len(seq) else ""
    for raw in t.split("\u3000"):
        raw = raw.strip()
        if not raw:
            continue
        seg = strip_note(raw)
        if not seg:
            continue
        pm = PROV_HEAD.match(seg)
        if pm:
            st.prov_name = norm_prov(pm.group(1))
            st.fu_name = st.zhou_name = None
            st.fu_id = st.zhou_id = ""
            cm = CNT_RE.search(t + "\u3000" + nxt)
            jm = JUNMIN_RE.search(t + "\u3000" + nxt)
            prov_decl[st.prov_name] = {
                "府": cn2i(cm.group(1)) if cm else None,
                "州": (cn2i(cm.group(2)) or 0) if cm else None,
                "县": cn2i(cm.group(3)) if cm else None,
                "军民府": cn2i(jm.group(1)) if jm else 0,
            }
            node = add(st.prov_name,
                       "直隶" if st.prov_name in ("北直隶", "南直隶") else "布政司",
                       "", "", "省", k, t, {"declared": prov_decl[st.prov_name]})
            st.prov_id = node["geo_id"]
            continue
        if st.prov_name is None:
            continue
        dm = DUSI_A.search(seg)                     # 图志内「X都指挥使司」段（如辽东）
        if dm:
            emit_units(seg[:dm.start()], raw, k, st, set(ZHILI_RE.findall(raw)))
            nm = dm.group(1) + "都司"
            node = add(nm, "都司", "", "", "都司", k, raw)   # 都司独立，非布政司属
            st.fu_name, st.fu_id = nm, node["geo_id"]
            st.fu_quota, st.fu_used = 99, 0
            st.zhou_name, st.zhou_id = None, ""
            continue
        fs = split_fu(seg)
        if fs:
            fu_name, prefix, tail = fs
            as_prov = set(ZHILI_RE.findall(raw))
            # 前缀属上一府/属州（如「蒲台县兖州府领…」中蒲台县归上一属州）；
            # 若为省界描述（含「抵」）则丢弃（如「东北抵贵州界云南府领…」）
            if "抵" not in prefix:
                emit_units(prefix, raw, k, st, as_prov)
            st.fu_name = fu_name
            node = add(fu_name, "府", st.prov_name, st.prov_id, "府", k, seg)
            st.fu_id = node["geo_id"]
            qm = FU_QUOTA.search(seg)
            st.fu_quota = cn2i(qm.group(1)) if qm else 0
            st.fu_used = 0
            st.zhou_name, st.zhou_id = None, ""     # 新府 → 属州游标复位
            if tail:                                # 头后余文（如「马湖府领长官司四泥溪长官司」）
                emit_units(tail, raw, k, st, as_prov)
            continue
        if "抵" in seg:                            # 省界描述段，跳过（避免「贵州界」误抽）
            continue
        if COUNT_SEG.search(seg) and "领" not in seg:   # 计数段（宣抚司四/长官司二十七）
            continue
        emit_units(seg, raw, k, st, set(ZHILI_RE.findall(raw)))

# ============ B. 都司→卫→所（卷108） ============
SKIP108 = re.compile(r"^(计天下|后定天下|都司[一二三四五六七八九十]+处|留守司[一二三四五六七八九十]+处)")
DUSI_OK = {"浙江", "辽东", "山东", "云南", "贵州", "四川", "陜西", "广西", "河南", "湖广",
           "福建", "江西", "广东", "北平", "山西", "大宁", "万全",
           "四川行", "湖广行", "福建行", "山西行"}
DUDU_OK = {"五军", "左军", "右军", "中军", "前军", "后军"}
LS_OK = {"中都"}
_alt = lambda s: "|".join(sorted(s, key=len, reverse=True))
HDR = re.compile(r"(南京见设卫所|(%s)都督府|(%s)都司|(%s)留守司|亲军卫|上十二卫)"
                 % (_alt(DUDU_OK), _alt(DUSI_OK), _alt(LS_OK)))
WEI_RE = re.compile(r"[\u4e00-\u9fff]{2,4}(?:守御千户所|千户所|百户所|护卫|卫)")
WEI_BAD_CHARS = set("属等诸各其凡处数内外京司")
WEI_BAD = {"卫所", "都司", "都督府", "留守司", "五军都督府", "护卫"}
WEI_CLEAN = re.compile(r"(?:所属|在京属|在外属|内外|在京|在外)卫所|[一二三四五六七八九十百]+处")

region = "北京"
cur_sec = cur_sec_id = None
nanking_id = ""
sec_names = set()


def wei_in(text, item_id):
    for nm in WEI_RE.findall(text):
        if nm in WEI_BAD or nm.endswith("卫所") or "处" in nm:
            continue
        if any(c in WEI_BAD_CHARS for c in nm):
            continue
        ntype = "所" if nm.endswith("所") else ("护卫" if nm.endswith("护卫") else "卫")
        add(nm, ntype, cur_sec, cur_sec_id, "卫/所", item_id, text)


def new_sec(name, ntype, item_id, original):
    global cur_sec, cur_sec_id
    cur_sec = name
    # 复用图志已建之同名根节点（如辽东都司），避免重复与悬挂
    for g in nodes:
        if g["name"] == name and g["parent"] == "" and g["type"] == ntype:
            cur_sec_id = g["geo_id"]
            sec_names.add(name)
            return
    if name not in sec_names:
        sec_names.add(name)
        # 南京各衙门挂到「南京见设卫所」之下
        pn, pid = ("南京见设卫所", nanking_id) if (region == "南京" and name != "南京见设卫所") else ("", "")
        cur_sec_id = add(name, ntype, pn, pid, ntype, item_id, original)["geo_id"]
    else:
        cur_sec_id = next(g["geo_id"] for g in nodes if g["name"] == name)


for k, v in sorted(reg.items()):
    if v["volume"] != 108:
        continue
    if v.get("node_kind") in ("沿革", "事例"):   # 卷首叙论，非卫所名录
        continue
    t = nz(v.get("original") or "")
    if not t or SKIP108.match(t):
        continue
    clean = WEI_CLEAN.sub("", strip_note(t))
    marks = list(HDR.finditer(clean))
    if not marks:
        if cur_sec:
            wei_in(clean, k)
        continue
    prev_end = 0
    for m in marks:
        if cur_sec:
            wei_in(clean[prev_end:m.start()], k)
        tok = m.group(0)
        if tok == "南京见设卫所":
            region = "南京"
            new_sec("南京见设卫所", "南京", k, t)
            nanking_id = cur_sec_id
        elif tok in ("亲军卫", "上十二卫"):
            new_sec(("南京" if region == "南京" else "") + "亲军卫", "亲军", k, t)
        else:
            if m.group(2):
                base, ntype = m.group(2) + "都督府", "都督府"
            elif m.group(3):
                base, ntype = m.group(3) + "都司", "都司"
            else:
                base, ntype = m.group(4) + "留守司", "留守司"
            new_sec(("南京" if region == "南京" else "") + base, ntype, k, t)
        prev_end = m.end()
    if cur_sec:
        wei_in(clean[prev_end:], k)

# ============ 去重 & children（按 geo_id 建树） ============
seen = set()
dedup = []
for g in nodes:
    key = (g["name"], g["parent"])
    if key in seen:
        continue
    seen.add(key)
    dedup.append(g)
by_id = {g["geo_id"]: g for g in dedup}
kids = defaultdict(list)
for g in dedup:
    if g.get("parent_id") and g["parent_id"] in by_id:
        kids[g["parent_id"]].append(g["geo_id"])
for g in dedup:
    g["children"] = [by_id[c]["name"] for c in kids.get(g["geo_id"], [])]

json.dump(dedup, open(os.path.join(LAYERS, "geo.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ============ 可读树 ============
lines = ["# 明会典·地理管辖树", "", f"共 {len(dedup)} 个地理节点。", ""]
out = []


def dump(gid, depth):
    if depth > 6:
        return
    g = by_id[gid]
    out.append("  " * depth + f"- {g['name']}（{g['type']}）〔卷{g['volume']}〕")
    for c in kids.get(gid, []):
        dump(c, depth + 1)


for g in dedup:
    if g["level"] in ("省", "都司", "都督府", "留守司", "亲军", "南京"):
        out.append(f"## {g['name']}（{g['type']}）")
        for c in kids.get(g["geo_id"], []):
            dump(c, 0)
        out.append("")
open(os.path.join(LAYERS, "geo_tree.md"), "w", encoding="utf-8").write("\n".join(lines + out))


# ============ 统计 ============
def descendants(gid):
    d = defaultdict(int)
    stack = list(kids.get(gid, []))
    seen_n = set()
    while stack:
        n = stack.pop()
        if n in seen_n:
            continue
        seen_n.add(n)
        d[by_id[n]["type"]] += 1
        stack.extend(kids.get(n, []))
    return d


print("=" * 60)
print(f"GEO 层：{len(dedup)} 条（去重前 {len(nodes)}）")
cnt = defaultdict(int)
for g in dedup:
    cnt[g["type"]] += 1
print("类型分布:", dict(cnt))

print("\n--- 各省 声明 vs 实际 ---")
ok = 0
for g in dedup:
    if g["level"] != "省":
        continue
    d = g.get("declared", {})
    r = descendants(g["geo_id"])
    decl_fu = (d.get("府") or 0) + (d.get("军民府") or 0)
    if decl_fu == r["府"]:
        ok += 1
        flag = ""
    else:
        flag = f"  <<< 差{r['府'] - decl_fu:+d}"
    print(f"  {g['name']:10s} 声明 府{decl_fu}(军{d.get('军民府')})/州{d.get('州')}/县{d.get('县')}"
          f" | 实际 府{r['府']}/州{r['州']}/县{r['县']}/土司{r['土司']}{flag}")
print(f"府数吻合省: {ok}/15")

print("\n都司:", [g["name"] for g in dedup if g["type"] == "都司"])
print("都督府/留守司/亲军/南京:", [g["name"] for g in dedup
                                  if g["type"] in ("都督府", "留守司", "亲军", "南京")])
for tp in ("府", "州", "县", "卫", "所", "护卫", "土司"):
    names = [g["name"] for g in dedup if g["type"] == tp]
    print(f"{tp}: {len(names)} (唯一名 {len(set(names))})  示例 {names[:8]}")
