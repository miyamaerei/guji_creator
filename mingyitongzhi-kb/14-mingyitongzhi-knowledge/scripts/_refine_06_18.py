# -*- coding: utf-8 -*-
"""
_refine_06_18.py  —  南直隶(卷6-18) AI精修粗抽取
工作流: 程序粗切(本脚本) → 产出可复原 JSON → AI 精修补录/校验
设计原则(用户要求):
  - 代码只做"大概": 分节 + 机械字段(GEO/EVO/MTN/PER/SITE/CIT)粗抽
  - 精修记录落盘为 _data/refined_south_zhili.json, 重试可整体复原
  - 另出 _data/refine_check_06_18.csv 密度/质量报告, 决定结构是否需重定
"""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_data")
SRC_SLICE = os.path.join(DATA, "cut_slices_06_18.json")
OUT_REFINED = os.path.join(DATA, "refined_south_zhili.json")
OUT_CHECK = os.path.join(DATA, "refine_check_06_18.csv")

CN_NUM = "[一二三四五六七八九十百千万零]+"

# ---- 20 节固定顺序 ----
SECT_ORDER = ["建置沿革", "郡名", "形胜", "风俗", "山川", "土产", "公署",
              "学校", "书院", "宫室", "关梁", "寺观", "祠庙", "陵墓",
              "古迹", "名宦", "流寓", "人物", "列女", "仙释"]
PROSE_SECTS = {"建置沿革", "郡名", "形胜", "风俗"}
SITE_SECT_TYPE = {"寺观": "temple", "祠庙": "shrine", "陵墓": "tomb",
                  "古迹": "historic_site", "公署": "office", "学校": "school",
                  "书院": "academy", "宫室": "palace", "关梁": "bridge_pass"}
PER_SECT_TYPE = {"名宦": "名宦", "流寓": "流寓", "人物": "人物",
                 "列女": "列女", "仙释": "仙释"}

# 朝代/年号 字典(长优先)
DYNS = ["东汉", "西汉", "蜀汉", "曹魏", "北魏", "东魏", "北齐", "北周",
        "后梁", "后唐", "后晋", "后汉", "后周", "南唐", "吴越", "北宋",
        "南宋", "国朝", "本朝", "夲朝", "皇明", "大明", "三国", "两汉",
        "先秦", "虞", "夏", "商", "周", "秦", "汉", "魏", "呉", "吴", "蜀",
        "晋", "宋", "齐", "梁", "陈", "隋", "唐", "元", "明", "五"]
ERAS = ["洪武", "永乐", "洪熙", "宣徳", "正统", "景泰", "天顺", "成化",
        "弘治", "正徳", "嘉靖", "隆庆", "万历", "泰昌", "天启", "崇祯"]
# EVO 朝代切分标记(按历史顺序)
EVO_MARKS = ["禹贡", "虞", "夏", "商", "周", "春秋", "战国", "楚", "秦",
             "西汉", "东汉", "三国", "蜀汉", "曹魏", "呉", "晋", "东晋",
             "宋", "齐", "梁", "陈", "隋", "唐", "五代", "十国", "北宋",
             "南宋", "金", "元", "明", "国朝", "本朝", "夲朝"]
# 引书词典
CIT_WORKS = ["汉书", "后汉书", "三国志", "晋书", "宋书", "南齐书", "梁书",
             "陈书", "魏书", "北齐书", "周书", "隋书", "南史", "北史",
             "旧唐书", "新唐书", "旧五代史", "新五代史", "宋史", "辽史",
             "金史", "元史", "明史", "资治通鉴", "通典", "通志", "文献通考",
             "艺文类聚", "初学记", "太平御览", "太平寰宇记", "元丰九域志",
             "舆地志", "郡国志", "水经注", "史记", "说文解字", "玉海",
             "册府元龟", "元和郡县志", "寰宇记", "一统志"]
CIT_WORKS.sort(key=len, reverse=True)


# 全局 OCR 异体字归一(仅映射已确认安全的变体)
OCR_FIX = {"\uef6e": "扬", "\ue5ab": "隶", "綂": "统"}

def clean_text(t):
    t = "".join(OCR_FIX.get(c, c) for c in t)
    lines = [ln.strip() for ln in t.split("\n")]
    out = []
    for ln in lines:
        if not ln:
            continue
        if re.match(r"^<.*>$", ln):          # <史部,...>
            continue
        if ln == "钦定四库全书":
            continue
        if re.match(r"^明一统志卷[统綂]?[一二三四五六七八九十百]+$", ln):
            continue
        out.append(ln)
    return "".join(out)


def split_sections(t, head_end):
    """顺序扫描 20 节，返回 {节名: (start,end)} ; 通过 min-gap 与 '之' 前缀排除正文误匹配。
    节内容 = 本节点文本 至 下一有序节点开始。"""
    pos = head_end
    spans = {}
    for s in SECT_ORDER:
        idx = t.find(s, pos)
        while idx != -1:
            # 正文误匹配排除: 前一字符为 之/其/以/于 (如 山川之王气)
            prev = t[idx-1] if idx > 0 else ""
            if prev in "之其以于而" and s in ("山川", "古迹", "寺观", "学校",
                                              "陵墓", "土产", "宫室", "关梁", "祠庙"):
                idx = t.find(s, idx + len(s))
                continue
            # 条目型节需紧跟 名称【 ; 散文型节直接接受
            if s in PROSE_SECTS:
                spans[s] = idx
                pos = idx + len(s)
                break
            else:
                nxt = t[idx + len(s): idx + len(s) + 40]
                if "【" in nxt:
                    spans[s] = idx
                    pos = idx + len(s)
                    break
                idx = t.find(s, idx + len(s))
                continue
        # 未找到则该节缺失
    # 计算每节内容区间
    keys = SECT_ORDER
    found = [(k, spans[k]) for k in keys if k in spans]
    found.sort(key=lambda x: x[1])
    sections = {}
    for i, (k, st) in enumerate(found):
        end = found[i+1][1] if i + 1 < len(found) else len(t)
        sections[k] = t[st + len(k): end]
    return sections


def parse_brackets(text):
    """从文本抽取 ['名称','内容'] 条目对(【】分隔)"""
    recs = []
    # 名称 = 紧邻【前的 1-6 个汉字
    for m in re.finditer(r"([\u4e00-\u9fff]{1,6})【([^【】]*)】", text):
        recs.append((m.group(1), m.group(2)))
    return recs


def parse_geo_head(head):
    geo = {"borders": [], "to_capital": [], "households": None,
           "grain_tax": None, "counties": []}
    # OCR 异体字归一: 束->东 (淮安府「束至海岸」)
    head = head.replace("束", "东")
    # 四至八到 (东/西/南/北 + 东南/东北/西南/西北) + OCR 束=东
    # 地名可能含方向字(如「山东」), 故允许中间任意字, 以 数字+里 为锚
    dirs = ["东南", "东北", "西南", "西北", "东", "西", "南", "北"]
    for d in dirs:
        for m in re.finditer(rf"{d}[至到]((?:[^【】]{{1,30}}?))({CN_NUM})里", head):
            place = m.group(1).strip("。，、")
            dist = m.group(2)
            if place:
                geo["borders"].append({"direction": d, "to_place": place,
                                       "distance_li": dist})
    # 至京师/南京/北京
    for m in re.finditer(rf"自(?:府治|州治)至(京师|南京|北京)({CN_NUM})里", head):
        geo["to_capital"].append({"capital": m.group(1), "distance_li": m.group(2)})
    m = re.search(rf"编户({CN_NUM})里", head)
    if m:
        geo["households"] = {"count_str": m.group(1), "unit": "里"}
    m = re.search(rf"粮({CN_NUM})石", head)
    if m:
        geo["grain_tax"] = {"amount_str": m.group(1), "unit": "石"}
    return geo


def split_dynasty(raw):
    """人物名 = 朝代前缀 + 姓名 ; 返回 (dynasty, era, name)"""
    s = raw
    dyn = None
    era = None
    for e in ERAS:
        if s.startswith(e):
            era = e
            dyn = "明"
            s = s[len(e):]
            break
    if dyn is None:
        for d in DYNS:
            if s.startswith(d):
                dyn = d
                s = s[len(d):]
                break
    return dyn, era, s.strip("。，、】 ")


# EVO 边界判据:
#  - 多字朝代标记(战国/东晋/五代/夲朝...)无歧义, 直接接受
#  - 单字朝代标记需满足: 位于段首 | 前导字为承接词 | 后1-3字为朝代承接词/动词
EVO_MULTI = {"禹贡", "战国", "三国", "蜀汉", "曹魏", "东晋", "北宋", "南宋",
             "五代", "十国", "国朝", "本朝", "夲朝", "西汉", "东汉"}
EVO_CUE_BEFORE = set("之後后初至寻又改复平自于属为仍因降罢立迁析割省入领筑营建更曰升徙分废都置")
EVO_NEXT = set("始高太武文孝世元肃代德顺昭哀献少中宣景炀庄烈废简敬僖懿"
               "置改属徙分废都仍因為复升平更曰降罢立迁析割省入筑营建名号徙治"
               "自以居乃遂至既寻后又")
# 内嵌保护: 朝代单字 + 后一字 构成常见地名/专名时拒绝 (金->陵 金陵, 夏->同 同夏)
EMBED_GUARD = {"金": "陵川山华沙台汤泉", "夏": "同诸", "楚": "苦",
               "周": "武公", "唐": "山僧", "宋": "公"}


def _evo_mark_ok(prose, mk, i):
    if i == 0:
        return True
    if mk in EVO_MULTI:
        return True
    if mk in EMBED_GUARD and prose[i + len(mk): i + len(mk) + 1] in EMBED_GUARD[mk]:
        return False
    if prose[i - 1] in EVO_CUE_BEFORE:
        return True
    nxt = prose[i + len(mk): i + len(mk) + 3]
    if any(c in EVO_NEXT for c in nxt):
        return True
    return False


def parse_evo(prose):
    """建置沿革 朝代切分 —— 按历史顺序取每个朝代的【首次有效出现】作为分界。"""
    pos = 0
    segs = []
    last = None
    for mk in EVO_MARKS:  # 已按历史顺序排列
        i = prose.find(mk, pos)
        if i == -1:
            continue
        if not _evo_mark_ok(prose, mk, i):
            continue
        if last is not None:
            segs.append((last, prose[pos:i]))
        pos = i + len(mk)
        last = mk
    if last is not None:
        segs.append((last, prose[pos:]))
    # 合并极小碎片段(如「宋齐梁陈因之」)到前一段, 避免朝代列举被切碎
    merged = []
    for dn, txt in segs:
        txt = txt.strip()
        if merged and len(txt) < 8:
            merged[-1] = (merged[-1][0], merged[-1][1] + txt)
        else:
            merged.append((dn, txt))
    evos = []
    for dn, txt in merged:
        txt = txt.strip()
        if len(txt) < 3:
            continue
        evos.append({"dynasty": dn, "detail": txt,
                     "action": _evo_action(txt), "era": None,
                     "institution_name": ""})
    return evos


def _mark_dyn(txt):
    for d in EVO_MARKS:
        if txt.startswith(d):
            return d
    return "沿革"


def _evo_action(t):
    if re.search(r"置(?:县|郡|府|州|军|路|城)", t):
        return "置"
    if re.search(r"改(?:名|曰|为)", t) or "更为" in t:
        return "改名/改为"
    if "废" in t:
        return "废"
    if re.search(r"徙(?:都|治)", t):
        return "徙都/徙治"
    if "分" in t:
        return "分置"
    if "省" in t or "省入" in t:
        return "省入"
    if "升" in t or "陞" in t:
        return "升"
    if "因之" in t or "仍旧" in t or "仍" in t:
        return "因之/仍旧"
    if "属" in t:
        return "属"
    if "都" in t:
        return "定都"
    if "治" in t:
        return "置治"
    return "沿革"


def classify_mtn(name, desc):
    n = name + desc
    if "江" in n or "河" in n:
        return "river"
    if "湖" in n or "池" in n or "潭" in n:
        return "lake"
    if "井" in n or "泉" in n:
        return "spring"
    if "洲" in n or "屿" in n:
        return "island"
    if "溪" in n or "涧" in n or "川" in n:
        return "stream"
    if "山" in n:
        return "mountain"
    return "landform"


def parse_citations(text):
    cits = []
    seen = set()
    for w in CIT_WORKS:
        for m in re.finditer(re.escape(w), text):
            ctx = text[max(0, m.start()-18): m.end()+18]
            key = (w, m.start())
            if key in seen:
                continue
            seen.add(key)
            cits.append({"cited_work": w, "context": ctx})
            if len(cits) > 200:
                return cits
    return cits


def refine_entry(e):
    raw = clean_text(e["text"])
    base = e["item_id"].replace("-", "")
    name = e["name"]
    is_metro = name in ("京城", "南京") or e.get("type") == "metro"

    item = {"item_id": e["item_id"], "volume": str(e["volume"]),
            "region": e["region"], "source": name + "【…】",
            "type": "metro" if is_metro else "prefecture",
            "layers": {"ents": [], "geos": [], "evos": [], "mtns": [],
                       "pers": [], "sites": [], "prods": [], "cits": []},
            "validation": {"errs": [], "gap": 0, "notes": ""}}

    # 头括号
    hb = raw.find("【")
    he = raw.find("】")
    head = raw[hb: he+1] if hb != -1 and he != -1 and he > hb else ""

    if is_metro:
        geo = {"name": name, "type": "metro", "region": e["region"],
               "city_walls": [{"name": "城池", "desc": head[1:-1] if head else ""}],
               "gates": parse_gates(head)}
        item["layers"]["geos"].append(_geo_rec(base, e, geo))
        item["sections_found"] = 1
        # 其余 【】 条目按内容归类
        for nm, ds in parse_brackets(raw[he+1:]):
            cls = _metro_classify(nm + ds)
            item["layers"][cls["layer"]].append(cls["rec"])
        item["layers"]["evos"] = parse_evo_section(raw)
    else:
        geo = parse_geo_head(head[1:-1] if head else "")
        geo["name"] = name
        geo["type"] = "prefecture"
        geo["region"] = e["region"]
        sections = split_sections(raw, he+1 if he != -1 else 0)
        item["sections_found"] = len(sections)

        # counties from 建置沿革 (领县 + 附郭县【…编户…】)
        evo_txt = sections.get("建置沿革", "")
        # 主府沿革 与 属县小史 以「领县/领州」为界, EVO 只取主府部分
        evo_main = re.split(r"领[州县][一二三四五六七八九十百]+", evo_txt)[0]
        geo["counties"] = parse_counties(evo_txt)
        item["layers"]["evos"] = parse_evo(evo_main)
        item["layers"]["geos"].append(_geo_rec(base, e, geo))

        # MTN
        n = 0
        for nm, ds in parse_brackets(sections.get("山川", "")):
            n += 1
            item["layers"]["mtns"].append({
                "mtn_id": f"MTN-{base}-{n:02d}", "item_id": e["item_id"],
                "geo_id": f"GEO-{base}", "name": nm,
                "type": classify_mtn(nm, ds),
                "location_text": _loc(ds), "description": ds, "lore": ""})
        # PER  (同朝代连续人名无前缀 -> 继承上一位的朝代)
        p = 0
        for sect, typ in PER_SECT_TYPE.items():
            cur_dyn = None
            for nm, ds in parse_brackets(sections.get(sect, "")):
                p += 1
                dyn, era, realname = split_dynasty(nm)
                if dyn is None and cur_dyn is not None:
                    dyn = cur_dyn
                else:
                    cur_dyn = dyn
                item["layers"]["pers"].append({
                    "per_id": f"PER-{base}-{p:02d}", "item_id": e["item_id"],
                    "geo_id": f"GEO-{base}", "name": realname or nm,
                    "type": typ, "dynasty": dyn, "era": era,
                    "native_place": _native(ds), "office": _office(ds),
                    "summary": ds})
        # SITE
        s = 0
        for sect, typ in SITE_SECT_TYPE.items():
            for nm, ds in parse_brackets(sections.get(sect, "")):
                s += 1
                item["layers"]["sites"].append({
                    "site_id": f"SITE-{base}-{s:02d}", "item_id": e["item_id"],
                    "geo_id": f"GEO-{base}", "name": nm, "type": typ,
                    "location_text": _loc(ds), "history_lore": ds})
        # PROD 跳过(府级不用, 仅外夷卷)

    # CIT (全篇)
    cits = parse_citations(raw)
    for i, c in enumerate(cits, 1):
        item["layers"]["cits"].append({
            "cit_id": f"CIT-{base}-{i:03d}", "item_id": e["item_id"],
            "cited_work": c["cited_work"], "cited_work_ent_id": None,
            "context": c["context"], "original": ""})

    # ents: geo + 引书去重
    item["layers"]["ents"].append({"ent_id": f"ENT-{base}-GEO",
                                   "name": name, "type": "geo", "norm": name,
                                   "first_source": e["item_id"]})
    books = sorted({c["cited_work"] for c in item["layers"]["cits"]})
    for i, b in enumerate(books, 1):
        item["layers"]["ents"].append({"ent_id": f"ENT-{base}-B{i:02d}",
                                       "name": b, "type": "book", "norm": b,
                                       "first_source": e["item_id"]})

    # 验证/缺口
    L = item["layers"]
    notes = []
    if not is_metro and not L["geos"][0]["attributes"].get("borders"):
        notes.append("无四至")
    if not L["evos"]:
        notes.append("无建置沿革切分")
    if "sections_found" not in item:
        item["sections_found"] = 0
    item["validation"]["notes"] = ";".join(notes)
    item["validation"]["gap"] = len(notes)
    item["layer_count"] = sum(1 for k in ("ents", "geos", "evos", "mtns",
                                          "pers", "sites", "cits") if L[k])
    return item


def parse_gates(head):
    gates = []
    # 立门X 南曰.. 北曰.. 等
    for m in re.finditer(r"(?:曰|为)([\u4e00-\u9fff]{1,4})(?:门)?", head):
        g = m.group(1)
        if g in ("正阳", "通济", "聚寳", "三山", "石城", "太平", "神防",
                 "金川", "钟阜", "朝阳") or "门" in g:
            gates.append(g)
    return gates


def parse_counties(evo_txt):
    cs = []
    m = re.search(rf"领(?:州|县)({CN_NUM})", evo_txt)
    # 先剥离「领县N」标记, 避免吞入属县名
    txt2 = re.sub(r"领[州县][一二三四五六七八九十百]+", "", evo_txt)
    # 县/州 条目: X县【(附郭)?…编户N里】
    for mm in re.finditer(r"([\u4e00-\u9fff]{1,5}[州县])【([^】]*)】", txt2):
        nm = mm.group(1)
        ds = mm.group(2)
        if nm in ("州县",) or nm.startswith("领"):
            continue
        hb = re.search(rf"编户({CN_NUM})里", ds)
        fu = "附郭" in ds
        cs.append({"name": nm, "is_capital_county": fu,
                   "households": hb.group(1) if hb else None})
    return cs


def parse_evo_section(raw):
    # metro 若有建置沿革则切分
    idx = raw.find("建置沿革")
    if idx == -1:
        return []
    return parse_evo(raw[idx+4: idx+4+600])


def _geo_rec(base, e, geo):
    return {"geo_id": f"GEO-{base}", "item_id": e["item_id"], "name": geo["name"],
            "type": geo["type"], "region": e["region"], "parent": e["region"],
            "children": [], "volume_range": str(e["volume"]),
            "attributes": geo, "cit_ids": []}


def _loc(ds):
    m = re.search(r"在[府州县郡东西南北内外上下]{0,6}?(?:[一二三四五六七八九十百千]+\s*里|[\u4e00-\u9fff]{1,4}界|[\u4e00-\u9fff]{1,4}侧|[\u4e00-\u9fff]{1,4}南|[\u4e00-\u9fff]{1,4}北)", ds)
    return m.group(0) if m else ""


def _native(ds):
    m = re.search(r"([\u4e00-\u9fff]{2,6}?(?:人|郡|县|州|邑|里))", ds)
    # 取首个 籍贯标记
    for kw in ("人", "郡人", "县人", "州人", "邑人", "里人", "之孙", "之子"):
        if kw in ds:
            i = ds.find(kw)
            seg = ds[max(0, i-6): i+1]
            return seg
    return ""


def _office(ds):
    m = re.search(r"(?:官至|为|拜|任|累官|擢|迁|除)([\u4e00-\u9fff]{1,8}?(?:令|长|守|尹|刺史|尚书|侍郎|丞相|相|公|卿|大夫|郎|将军|使|提举|判|知|留守|都督|中书))", ds)
    return m.group(1) if m else ""


def _metro_classify(nm_ds):
    n = nm_ds
    layer = "sites"
    typ = "site"
    if "坛" in n:
        typ = "altar"
    elif "庙" in n:
        typ = "temple"
    elif "陵" in n:
        typ = "tomb"
    elif "山" in n:
        layer, typ = "mtns", "mountain"
    elif "城" in n or "门" in n:
        typ = "wall"
    rec = {"site_id": "", "item_id": "", "geo_id": "", "name": "",
           "type": typ, "location_text": _loc(nm_ds), "history_lore": nm_ds}
    if layer == "mtns":
        rec = {"mtn_id": "", "item_id": "", "geo_id": "", "name": "",
               "type": "mountain", "location_text": _loc(nm_ds),
               "description": nm_ds, "lore": ""}
    return {"layer": layer, "rec": rec, "name": nm_ds, "desc": nm_ds}


def main():
    cut = json.load(open(SRC_SLICE, encoding="utf-8"))
    out = []
    rows = []
    for e in cut:
        item = refine_entry(e)
        L = item["layers"]
        flags = item["validation"]["notes"]
        rows.append({
            "item_id": item["item_id"], "name": e["name"],
            "vol": e["volume"], "type": item["type"],
            "sects": item.get("sections_found", 0),
            "evo_n": len(L["evos"]), "mtn_n": len(L["mtns"]),
            "per_n": len(L["pers"]), "site_n": len(L["sites"]),
            "cit_n": len(L["cits"]), "county_n": len(L["geos"][0]["attributes"].get("counties", [])),
            "flags": flags,
        })
        out.append(item)

    json.dump(out, open(OUT_REFINED, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    with open(OUT_CHECK, "w", encoding="utf-8") as f:
        f.write("item_id,name,vol,type,sects,evo_n,mtn_n,per_n,site_n,cit_n,county_n,flags\n")
        for r in rows:
            f.write(f"{r['item_id']},{r['name']},{r['vol']},{r['type']},"
                    f"{r['sects']},{r['evo_n']},{r['mtn_n']},{r['per_n']},"
                    f"{r['site_n']},{r['cit_n']},{r['county_n']},{r['flags']}\n")

    print(f"refined entries: {len(out)}")
    tot = {"evo": 0, "mtn": 0, "per": 0, "site": 0, "cit": 0, "county": 0}
    for o in out:
        tot["evo"] += len(o["layers"]["evos"])
        tot["mtn"] += len(o["layers"]["mtns"])
        tot["per"] += len(o["layers"]["pers"])
        tot["site"] += len(o["layers"]["sites"])
        tot["cit"] += len(o["layers"]["cits"])
        tot["county"] += len(o["layers"]["geos"][0]["attributes"].get("counties", []))
    print("totals:", tot)
    print("check csv ->", OUT_CHECK)


if __name__ == "__main__":
    main()
