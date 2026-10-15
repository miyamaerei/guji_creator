# -*- coding: utf-8 -*-
"""
北直隶卷2：保定府(02-001) + 河间府(02-002) 县级文件生成 v2
修复：
- EVO: 用 endswith 匹配（河间府建置沿革与县条目同行）
- MTN/SITE: 用全称县名匹配（避免"河间"匹配"河间府/郡/路"）
- PER: 短名+"人" 或 全称县名匹配
"""
import re, json, os

ROOT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge"
WORK = os.path.join(ROOT, "_work")
OUT = os.path.join(ROOT, "_data", "vol02")

BAODING = [
    ("c01", "清苑县", "GEO-02001", "保定府"),
    ("c02", "满城县", "GEO-02001", "保定府"),
    ("c03", "安肃县", "GEO-02001", "保定府"),
    ("c04", "定兴县", "GEO-02001", "保定府"),
    ("c05", "新城县", "GEO-02001", "保定府"),
    ("c06", "唐县",   "GEO-02001", "保定府"),
    ("c07", "博野县", "GEO-02001", "保定府"),
    ("c08", "庆都县", "GEO-02001", "保定府"),
    ("c09", "容城县", "GEO-02001", "保定府"),
    ("c10", "完县",   "GEO-02001", "保定府"),
    ("c11", "蠡县",   "GEO-02001", "保定府"),
    ("c12", "雄县",   "GEO-02001", "保定府"),
    ("c13", "深泽县", "GEO-02001-s01", "祁州"),
    ("c14", "束鹿县", "GEO-02001-s01", "祁州"),
    ("c15", "高阳县", "GEO-02001-s02", "安州"),
    ("c16", "新安县", "GEO-02001-s02", "安州"),
    ("c17", "涞水县", "GEO-02001-s03", "易州"),
]
HEJIAN = [
    ("c01", "河间县", "GEO-02002", "河间府"),
    ("c02", "献县",   "GEO-02002", "河间府"),
    ("c03", "阜城县", "GEO-02002", "河间府"),
    ("c04", "肃宁县", "GEO-02002", "河间府"),
    ("c05", "任丘县", "GEO-02002", "河间府"),
    ("c06", "交河县", "GEO-02002", "河间府"),
    ("c07", "青县",   "GEO-02002", "河间府"),
    ("c08", "兴济县", "GEO-02002", "河间府"),
    ("c09", "静海县", "GEO-02002", "河间府"),
    ("c10", "宁津县", "GEO-02002", "河间府"),
    ("c11", "吴桥县", "GEO-02002-s01", "景州"),
    ("c12", "东光县", "GEO-02002-s01", "景州"),
    ("c13", "故城县", "GEO-02002-s01", "景州"),
    ("c14", "南皮县", "GEO-02002-s02", "沧州"),
    ("c15", "盐山县", "GEO-02002-s02", "沧州"),
    ("c16", "庆云县", "GEO-02002-s02", "沧州"),
]

OCR_NORM = str.maketrans({
    "寳": "宝", "寜": "宁", "懐": "怀", "宻": "密",
    "徳": "德", "隷": "隶", "夀": "寿", "鳯": "凤",
    "龍": "龙", "雲": "云", "峯": "峰", "嶺": "岭",
    "澗": "涧", "髙": "高", "愽": "博", "闗": "关",
    "綂": "统", "": "隶",
})
def norm(s):
    return s.translate(OCR_NORM)

text = open(os.path.join(WORK, "vol02.txt"), encoding="utf-8").read()
boundary = text.index("河间府【")
baoding_text = text[:boundary]
hejian_text  = text[boundary:]

def split_sections(t):
    parts = re.split(r"\n　　", t)
    return [s.strip() for s in parts if s.strip()]

def find_sec(sections, start_kw, end_kw):
    si = None
    for i, s in enumerate(sections):
        if si is None and s.startswith(start_kw):
            si = i
            break
    if si is None:
        return ""
    ei = len(sections)
    for j in range(si+1, len(sections)):
        if end_kw and sections[j].startswith(end_kw):
            ei = j
            break
    return "\n".join(sections[si:ei])

def split_brackets(sec):
    return [(n.strip(), d.strip()) for n, d in re.findall(r"([^【\n]+?)【([^】]*)】", sec) if n.strip()]

MTN_TYPE_LIST = ["山","岭","峰","冈","岩","洞","泉","溪","河","江","湖","潭","池","堰","关","桥","井","峪","屿","淀","陂","洼","沽","沟","渠"]
def guess_mtn_type(name):
    for t in MTN_TYPE_LIST:
        if name.endswith(t):
            return t
    if "水" in name or "河" in name or "川" in name: return "河"
    return "其他"

SITE_TYPE_MAP = {
    "学校": "学校", "书院": "书院", "宫室": "宫室",
    "关梁": "关梁", "闗梁": "关梁",
    "寺观": "寺观", "祠庙": "祠庙", "陵墓": "陵墓", "古迹": "古迹",
}

def extract_for_prefecture(pref_text, counties, item_id):
    secs = split_sections(pref_text)
    evo_sec = find_sec(secs, "建置沿革", "郡名")
    mtn_sec = find_sec(secs, "山川", "土产")

    site_sec_defs = [
        ("学校", "学校", "书院"),
        ("书院", "书院", "宫室"),
        ("宫室", "宫室", "关梁"),
        ("关梁", "关梁", "寺观"),
        ("闗梁", "闗梁", "寺观"),
        ("寺观", "寺观", "祠庙"),
        ("祠庙", "祠庙", "陵墓"),
        ("陵墓", "陵墓", "古迹"),
        ("古迹", "古迹", "名宦"),
    ]
    per_sec_defs = [
        ("名宦", "名宦", "流寓"),
        ("流寓", "流寓", "人物"),
        ("人物", "人物", "列女"),
        ("列女", "列女", "仙释"),
        ("仙释", "仙释", None),
    ]

    result = {}
    for code, cname, parent, plabel in counties:
        result[cname] = {"code": code, "parent": parent, "plabel": plabel,
                         "evo": "", "mtns": [], "sites": [], "pers": []}

    # ── EVO: endswith 匹配 ──
    for name, detail in split_brackets(evo_sec):
        name_n = norm(name)
        for code, cname, parent, plabel in counties:
            short = cname.replace("县","")
            if name_n.endswith(cname) or name_n.endswith(short):
                result[cname]["evo"] = detail
                break

    # ── MTN: 全称县名匹配 ──
    for name, detail in split_brackets(mtn_sec):
        name_n = norm(name)
        det_n = norm(detail)
        for code, cname, parent, plabel in counties:
            short = cname.replace("县","")
            # entry name 含县全称 (e.g. 唐县学)
            if cname in name_n:
                result[cname]["mtns"].append({
                    "name": name_n, "type": guess_mtn_type(name_n),
                    "location_text": det_n[:80], "description": det_n,
                    "original": f"{name_n}【{detail}】"[:300],
                })
                break
            # detail 前60字含县全称
            if cname in det_n[:60]:
                result[cname]["mtns"].append({
                    "name": name_n, "type": guess_mtn_type(name_n),
                    "location_text": det_n[:80], "description": det_n,
                    "original": f"{name_n}【{detail}】"[:300],
                })
                break

    # ── SITES: 全称县名匹配 ──
    for sec_key, start_kw, end_kw in site_sec_defs:
        sec_text = find_sec(secs, start_kw, end_kw)
        if not sec_text:
            continue
        stype = SITE_TYPE_MAP.get(sec_key, "其他")
        for name, detail in split_brackets(sec_text):
            name_n = norm(name)
            det_n = norm(detail)
            for code, cname, parent, plabel in counties:
                short = cname.replace("县","")
                if cname in name_n:
                    result[cname]["sites"].append({
                        "name": name_n, "type": stype,
                        "location_text": det_n[:80], "history_lore": det_n,
                        "original": f"{name_n}【{detail}】"[:300],
                    })
                    break
                if cname in det_n[:60]:
                    result[cname]["sites"].append({
                        "name": name_n, "type": stype,
                        "location_text": det_n[:80], "history_lore": det_n,
                        "original": f"{name_n}【{detail}】"[:300],
                    })
                    break

    # ── PERS: 短名+人 或 全称县名 ──
    for sec_key, start_kw, end_kw in per_sec_defs:
        sec_text = find_sec(secs, start_kw, end_kw)
        if not sec_text:
            continue
        for name, detail in split_brackets(sec_text):
            name_n = norm(name)
            det_n = norm(detail)
            for code, cname, parent, plabel in counties:
                short = cname.replace("县","")
                # 全称县名 或 短名+人 (本县人)
                if cname in det_n[:80] or short + "人" in det_n[:80]:
                    result[cname]["pers"].append({
                        "name": name_n, "type": sec_key,
                        "summary": det_n[:200],
                        "original": f"{name_n}【{detail}】"[:300],
                    })
                    break

    return result

baoding_data = extract_for_prefecture(baoding_text, BAODING, "02-001")
hejian_data  = extract_for_prefecture(hejian_text, HEJIAN, "02-002")

os.makedirs(OUT, exist_ok=True)
all_summary = []

def gen_files(counties, data, item_id, vol_label):
    for code, cname, parent, plabel in counties:
        d = data[cname]
        geo_id = f"{parent}-{code}"
        evo_text = d["evo"]

        county_node = {
            "geo_id": geo_id, "item_id": item_id, "name": cname,
            "type": "county", "region": "北直隶",
            "parent": parent, "children": [],
            "volume_range": vol_label,
            "attributes": {"evo_summary": evo_text[:200]},
            "original": evo_text[:300],
        }

        evos = []
        if evo_text:
            evos.append({
                "evo_id": f"EVO-{item_id.replace('-','')}-{code}",
                "item_id": item_id, "geo_id": geo_id,
                "dynasty": "未明", "era": None,
                "institution_name": cname, "action": "因之",
                "detail": evo_text, "original": evo_text,
            })

        mtns = []
        for i, m in enumerate(d["mtns"], 1):
            mtns.append({
                "mtn_id": f"MTN-{item_id.replace('-','')}-{code}-{i:02d}",
                "item_id": item_id, "geo_id": geo_id,
                "name": m["name"], "type": m["type"],
                "location_text": m["location_text"],
                "description": m["description"],
                "lore": "", "original": m["original"],
            })

        sites = []
        for i, s in enumerate(d["sites"], 1):
            sites.append({
                "site_id": f"SITE-{item_id.replace('-','')}-{code}-{i:02d}",
                "item_id": item_id, "geo_id": geo_id,
                "name": s["name"], "type": s["type"],
                "location_text": s["location_text"],
                "history_lore": s["history_lore"],
                "original": s["original"],
            })

        pers = []
        for i, p in enumerate(d["pers"], 1):
            pers.append({
                "per_id": f"PER-{item_id.replace('-','')}-{code}-{i:02d}",
                "item_id": item_id, "geo_id": geo_id,
                "name": p["name"], "type": p["type"],
                "dynasty": "未明", "native_place": "", "office": "",
                "summary": p["summary"], "original": p["original"],
            })

        ents = [{"ent_id": f"ENT-{item_id.replace('-','')}-{code}",
                  "name": cname, "type": "geo", "norm": cname,
                  "first_source": item_id}]

        obj = {
            "item_id": item_id, "volume": "02", "source": cname,
            "region": "北直隶", "original": evo_text[:300],
            "layers": {
                "ents": ents, "geos": [county_node], "evos": evos,
                "mtns": mtns, "pers": pers, "sites": sites,
                "prods": [], "cits": [],
            },
            "layer_count": 7,
            "validation": {"errs": [], "gap": 0,
                           "notes": f"parent={plabel}; auto-extracted, pending manual review"},
        }
        fname = f"{item_id}_{code}_{cname}.json"
        fpath = os.path.join(OUT, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        sz = os.path.getsize(fpath)
        all_summary.append(f"{fname}: evo={len(evos)} mtn={len(mtns)} site={len(sites)} per={len(pers)} ({sz}B)")

gen_files(BAODING, baoding_data, "02-001", "卷2")
gen_files(HEJIAN, hejian_data, "02-002", "卷2")

print("\n".join(all_summary))
print(f"\n共 {len(all_summary)} 个县文件 -> {OUT}")
