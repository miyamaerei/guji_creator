# -*- coding: utf-8 -*-
"""
北直隶卷3-5 县级独立文件提取。
真定府(卷3) / 顺德府+广平府+大名府(卷4) / 永平府+延庆州(卷5)。
"""
import re, os, json

BASE = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge"
WORK = os.path.join(BASE, "_work")
DATA = os.path.join(BASE, "_data")

# OCR 归一（仅用于匹配，输出保留原文）
OCR_NORM = str.maketrans({
    "寳": "宝", "寜": "宁", "懐": "怀", "宻": "密", "徳": "德",
    "隷": "隶", "夀": "寿", "鳯": "凤", "龍": "龙", "雲": "云",
    "峯": "峰", "嶺": "岭", "澗": "涧", "綂": "统", "防": "坊",
    "髙": "高", "栢": "柏", "賛": "赞", "彊": "强", "豊": "丰",
    "寕": "宁", "眞": "真", "": "隶",
})
def norm(s):
    return s.translate(OCR_NORM)

SECTION_KEYS = ["建置沿革","郡名","形胜","风俗","土产","山川","公署",
                "学校","书院","宫室","关梁","寺观","祠庙","陵墓","古迹",
                "名宦","流寓","人物","列女","仙释"]

# ---------- 县规格 ----------
# (code, canonical_name, [aliases for matching], parent_geo_id, parent_label)
ZHENDING = {  # 03-001 真定府 GEO-03001
    "item_id":"03-001","volume":"03","vr":"卷3","pfx":"GEO-03001",
    "counties":[
        ("c01","真定县",["真定"],"GEO-03001","真定府"),
        ("c02","井陉县",["井陉"],"GEO-03001","真定府"),
        ("c03","获鹿县",["获鹿"],"GEO-03001","真定府"),
        ("c04","元氏县",["元氏"],"GEO-03001","真定府"),
        ("c05","灵寿县",["灵寿","灵夀"],"GEO-03001","真定府"),
        ("c06","藁城县",["藁城"],"GEO-03001","真定府"),
        ("c07","栾城县",["栾城"],"GEO-03001","真定府"),
        ("c08","无极县",["无极"],"GEO-03001","真定府"),
        ("c09","平山县",["平山"],"GEO-03001","真定府"),
        ("c10","阜平县",["阜平"],"GEO-03001","真定府"),
        ("c11","新乐县",["新乐"],"GEO-03001-s01","定州"),
        ("c12","曲阳县",["曲阳"],"GEO-03001-s01","定州"),
        ("c13","行唐县",["行唐"],"GEO-03001-s01","定州"),
        ("c14","南宫县",["南宫"],"GEO-03001-s02","冀州"),
        ("c15","新河县",["新河"],"GEO-03001-s02","冀州"),
        ("c16","枣强县",["枣强","枣彊"],"GEO-03001-s02","冀州"),
        ("c17","武邑县",["武邑"],"GEO-03001-s02","冀州"),
        ("c18","安平县",["安平"],"GEO-03001-s03","晋州"),
        ("c19","饶阳县",["饶阳"],"GEO-03001-s03","晋州"),
        ("c20","武强县",["武强","武彊"],"GEO-03001-s03","晋州"),
        ("c21","柏乡县",["柏乡","栢乡"],"GEO-03001-s04","赵州"),
        ("c22","隆平县",["隆平"],"GEO-03001-s04","赵州"),
        ("c23","高邑县",["高邑","髙邑"],"GEO-03001-s04","赵州"),
        ("c24","临城县",["临城"],"GEO-03001-s04","赵州"),
        ("c25","赞皇县",["赞皇","賛皇"],"GEO-03001-s04","赵州"),
        ("c26","宁晋县",["宁晋","寜晋"],"GEO-03001-s04","赵州"),
        ("c27","衡水县",["衡水"],"GEO-03001-s05","深州"),
    ]
}

SHUNDE = {  # 04-001 顺德府 GEO-04001
    "item_id":"04-001","volume":"04","vr":"卷4","pfx":"GEO-04001",
    "counties":[
        ("c01","邢台县",["邢台"],"GEO-04001","顺德府"),
        ("c02","沙河县",["沙河"],"GEO-04001","顺德府"),
        ("c03","南和县",["南和"],"GEO-04001","顺德府"),
        ("c04","平乡县",["平乡"],"GEO-04001","顺德府"),
        ("c05","广宗县",["广宗"],"GEO-04001","顺德府"),
        ("c06","巨鹿县",["巨鹿","钜鹿"],"GEO-04001","顺德府"),
        ("c07","唐山县",["唐山"],"GEO-04001","顺德府"),
        ("c08","内丘县",["内丘"],"GEO-04001","顺德府"),
        ("c09","任县",["任县"],"GEO-04001","顺德府"),
    ]
}

GUANGPING = {  # 04-002 广平府 GEO-04002
    "item_id":"04-002","volume":"04","vr":"卷4","pfx":"GEO-04002",
    "counties":[
        ("c01","永年县",["永年"],"GEO-04002","广平府"),
        ("c02","曲周县",["曲周"],"GEO-04002","广平府"),
        ("c03","肥乡县",["肥乡","肥郷"],"GEO-04002","广平府"),
        ("c04","鸡泽县",["鸡泽"],"GEO-04002","广平府"),
        ("c05","广平县",["广平"],"GEO-04002","广平府"),
        ("c06","邯郸县",["邯郸"],"GEO-04002","广平府"),
        ("c07","成安县",["成安"],"GEO-04002","广平府"),
        ("c08","威县",["威县"],"GEO-04002","广平府"),
        ("c09","清河县",["清河"],"GEO-04002","广平府"),
    ]
}

DAMING = {  # 04-003 大名府 GEO-04003
    "item_id":"04-003","volume":"04","vr":"卷4","pfx":"GEO-04003",
    "counties":[
        ("c01","元城县",["元城"],"GEO-04003","大名府"),
        ("c02","大名县",["大名"],"GEO-04003","大名府"),
        ("c03","南乐县",["南乐"],"GEO-04003","大名府"),
        ("c04","魏县",["魏县"],"GEO-04003","大名府"),
        ("c05","清丰县",["清丰","清豊"],"GEO-04003","大名府"),
        ("c06","内黄县",["内黄"],"GEO-04003","大名府"),
        ("c07","濬县",["濬县"],"GEO-04003","大名府"),
        ("c08","滑县",["滑县"],"GEO-04003","大名府"),
        ("c09","东明县",["东明"],"GEO-04003","大名府"),
        ("c10","长垣县",["长垣"],"GEO-04003-s01","开州"),
    ]
}

YONGPING = {  # 05-001 永平府 GEO-05001
    "item_id":"05-001","volume":"05","vr":"卷5","pfx":"GEO-05001",
    "counties":[
        ("c01","卢龙县",["卢龙"],"GEO-05001","永平府"),
        ("c02","迁安县",["迁安"],"GEO-05001","永平府"),
        ("c03","抚宁县",["抚宁","抚寕"],"GEO-05001","永平府"),
        ("c04","昌黎县",["昌黎"],"GEO-05001","永平府"),
        ("c05","乐亭县",["乐亭"],"GEO-05001-s01","滦州"),
    ]
}

YANQING = {  # 05-002 延庆州 GEO-05002
    "item_id":"05-002","volume":"05","vr":"卷5","pfx":"GEO-05002",
    "counties":[
        ("c01","永宁县",["永宁","永寕"],"GEO-05002","延庆州"),
    ]
}

# 短别名（需严格匹配，避免误命中）—— 这些县的别名在 detail 中要求后跟"人/县/令"
SHORT_ALIASES = {"任县","威县","魏县","濬县","滑县","唐山","邯郸","广平","大名","新河","南宫"}

def read_vol(fn):
    return open(os.path.join(WORK, fn), encoding="utf-8").read()

def split_prefecture_blocks(text, headers):
    """按府/州标题切段。headers = 标题字符串列表（出现在行首）。"""
    lines = text.split("\n")
    blocks = {h: [] for h in headers}
    cur = None
    for ln in lines:
        s = ln.strip().lstrip("　").strip()
        sn = norm(s)  # OCR 归一后匹配（顺徳府->顺德府）
        hit = None
        for h in headers:
            hn = norm(h)
            if sn.startswith(hn + "【") or sn.startswith(hn):
                # 避免 "顺德府" 误中 "顺德府学" 等：要求标题后紧跟【或为完整府名
                if sn.startswith(hn + "【") or sn == hn or re.match(r"^"+re.escape(hn)+r"[^学]", sn):
                    hit = h; break
        if hit:
            cur = hit
        if cur:
            blocks[cur].append(ln)
    return {h: "\n".join(lines) for h, lines in blocks.items()}

def parse_sections(block_text):
    """把一个府块切成 {section_key: text}。"""
    secs = {}
    cur = None
    for ln in block_text.split("\n"):
        s = ln.strip().lstrip("　").strip()
        if not s:
            continue
        matched = None
        for k in SECTION_KEYS:
            if s.startswith(k):
                matched = k; break
        if matched:
            cur = matched
            secs.setdefault(cur, [])
            # 去掉 section 关键字本身
            secs[cur].append(s[len(k):])
        else:
            if cur:
                secs[cur].append(s)
    return {k: "".join(v) for k, v in secs.items()}

def split_bracket(sec):
    parts = re.findall(r"([^【\n]{1,40}?)【([^】]*)】", sec)
    out = []
    for n, d in parts:
        n = n.strip()
        # 去掉前一个条目残余（含 】 或太长的尾巴）
        if not n or n.endswith("】") or "】" in n:
            continue
        out.append((n, d.strip()))
    return out

def alias_in_detail(aliases, d, window):
    """检查别名是否在 detail 前 window 字内。短别名要求后缀。"""
    head = d[:window]
    for a in aliases:
        if a in SHORT_ALIASES:
            # 要求 a 后接 人/县/令
            for suf in ["人","县","令"]:
                if (a+suf) in head:
                    return True
        else:
            if a in head:
                return True
    return False

def guess_mtn_type(name):
    for t in ["山","岭","峰","冈","岩","洞","泉","溪","江","河","湖","潭","池","堰","关","桥","井","峪","泊","淀","陂"]:
        if name.endswith(t):
            return t
    if "水" in name or "河" in name or "川" in name: return "河"
    return "山"

def loc_county_match(aliases, head):
    """山川/古迹：要求明确出现'X县'，避免'真定府/真定路'误命中附郭。"""
    for a in aliases:
        if (a + "县") in head:
            return True
    return False

SITE_SECTION_TYPE = {"学校":"学校","书院":"书院","宫室":"宫室","关梁":"关梁",
                     "寺观":"寺观","祠庙":"祠庙","陵墓":"陵墓","古迹":"古迹"}

def build_prefecture(spec, block_text):
    secs = parse_sections(block_text)
    counties = spec["counties"]
    # county name -> spec
    by_canon = {}
    for code, cname, aliases, parent, plabel in counties:
        by_canon[cname] = dict(code=code,cname=cname,aliases=aliases,parent=parent,plabel=plabel)
    # evo: 建置沿革中按精确名匹配
    evo_sec = secs.get("建置沿革","")
    evo_map = {}
    for code,cname,aliases,parent,plabel in counties:
        shorts = [cname.replace("县","")] + list(aliases)
        for a in shorts:
            m = re.search(re.escape(a) + r"县【([^】]*)】", evo_sec)
            if m:
                evo_map[cname] = m.group(1).strip()
                break
    # mtns
    mtn_sec = secs.get("山川","")
    mtn_assign = {c[1]: [] for c in counties}
    for n, d in split_bracket(mtn_sec):
        dn = norm(d)
        placed = False
        for code,cname,aliases,parent,plabel in counties:
            if loc_county_match(aliases, dn[:50]):
                mtn_assign[cname].append((n,d)); placed=True; break
    # sites
    site_assign = {c[1]: [] for c in counties}
    for sec_name, stype in SITE_SECTION_TYPE.items():
        sec = secs.get(sec_name,"")
        for n, d in split_bracket(sec):
            dn = norm(d)
            # 学校：按名匹配
            if sec_name in ("学校","书院"):
                nn = norm(n)
                if "府学" in nn or "州学" in nn or "卫学" in nn:
                    continue
                placed = False
                for code,cname,aliases,parent,plabel in counties:
                    if any(a in nn for a in aliases):
                        site_assign[cname].append((n,d,stype)); placed=True; break
                continue
            placed = False
            for code,cname,aliases,parent,plabel in counties:
                if loc_county_match(aliases, dn[:50]):
                    site_assign[cname].append((n,d,stype)); placed=True; break
    # pers
    per_secs = {}
    for k in ["名宦","流寓","人物","列女","仙释"]:
        if k in secs: per_secs[k] = secs[k]
    per_assign = {c[1]: [] for c in counties}
    for sec_name, sec in per_secs.items():
        for n, d in split_bracket(sec):
            dn = norm(d)
            head = dn[:35]
            placed = False
            for code,cname,aliases,parent,plabel in counties:
                # 人物按籍贯"X人"归属（本县人），不按任职地
                if any((a + "人") in head for a in aliases):
                    per_assign[cname].append((n,d,sec_name)); placed=True; break
    return evo_map, mtn_assign, site_assign, per_assign

def write_county(spec, cname, evo, mtns, sites, pers):
    code = None; parent=None; plabel=None
    for c in spec["counties"]:
        if c[1]==cname: code,_,ali,parent,plabel = c; break
    pfx = spec["pfx"]
    geo_id = f"{pfx}-{code}"
    item_id = spec["item_id"]
    evos = []
    if evo:
        evos.append({
            "evo_id": f"EVO-{item_id}-{code}",
            "item_id": item_id, "geo_id": geo_id,
            "dynasty": "未明","era": None,
            "institution_name": cname, "action": "因之",
            "detail": evo, "original": evo,
        })
    mtn_list=[]
    for i,(n,d) in enumerate(mtns,1):
        mtn_list.append({
            "mtn_id": f"MTN-{item_id}-{code}-{i:02d}",
            "item_id": item_id,"geo_id":geo_id,
            "name":n,"type":guess_mtn_type(n),
            "location_text":d[:80],"description":d,"lore":"",
            "original":f"{n}【{d}】"[:300],
        })
    site_list=[]
    for i,(n,d,st) in enumerate(sites,1):
        site_list.append({
            "site_id": f"SITE-{item_id}-{code}-{i:02d}",
            "item_id": item_id,"geo_id":geo_id,
            "name":n,"type":st,
            "location_text":d[:80],"history_lore":d,
            "original":f"{n}【{d}】"[:300],
        })
    per_list=[]
    for i,(n,d,pt) in enumerate(pers,1):
        per_list.append({
            "per_id": f"PER-{item_id}-{code}-{i:02d}",
            "item_id": item_id,"geo_id":geo_id,
            "name":n,"type":pt,"dynasty":"未明",
            "native_place":"","office":"",
            "summary":d[:200],"original":f"{n}【{d}】"[:300],
        })
    obj = {
        "item_id": item_id,
        "volume": spec["volume"],
        "source": cname,
        "region": "北直隶",
        "original": evo[:300],
        "layers": {
            "ents":[{"ent_id":f"ENT-{item_id}-{code}","name":cname,"type":"geo","norm":cname,"first_source":item_id}],
            "geos":[{
                "geo_id":geo_id,"item_id":item_id,"name":cname,
                "type":"county","region":"北直隶","parent":parent,
                "children":[],"volume_range":spec["vr"],
                "attributes":{"evo_summary":evo[:200]},
                "original":evo[:300],
            }],
            "evos":evos,"mtns":mtn_list,"pers":per_list,
            "sites":site_list,"prods":[],"cits":[],
        },
        "layer_count":7,
        "validation":{"errs":[],"gap":0,
                      "notes":f"parent={plabel}; auto-extracted, pending manual review"},
    }
    outdir = os.path.join(DATA, f"vol{spec['volume']}")
    os.makedirs(outdir, exist_ok=True)
    fn = f"{item_id}_{code}_{cname}.json"
    with open(os.path.join(outdir,fn),"w",encoding="utf-8") as f:
        json.dump(obj,f,ensure_ascii=False,indent=1)
    return fn, len(evos), len(mtn_list), len(site_list), len(per_list)

def run_prefecture(spec, block_text):
    evo_map,mtn_as,site_as,per_as = build_prefecture(spec, block_text)
    rows=[]
    for code,cname,ali,parent,plabel in spec["counties"]:
        fn,ne,nm,ns,np = write_county(spec,cname,
            evo_map.get(cname,""),
            mtn_as.get(cname,[]),
            site_as.get(cname,[]),
            per_as.get(cname,[]))
        rows.append((fn,nm,ns,np, "evo" if evo_map.get(cname) else "NO-EVO"))
    return rows

# ============ 执行 ============
report = {}

# vol03 真定府
v3 = read_vol("vol03.txt")
b3 = split_prefecture_blocks(v3, ["真定府"])
report["真定府"] = run_prefecture(ZHENDING, b3["真定府"])

# vol04 顺德/广平/大名
v4 = read_vol("vol04.txt")
b4 = split_prefecture_blocks(v4, ["顺德府","广平府","大名府"])
report["顺德府"] = run_prefecture(SHUNDE, b4["顺德府"])
report["广平府"] = run_prefecture(GUANGPING, b4["广平府"])
report["大名府"] = run_prefecture(DAMING, b4["大名府"])

# vol05 永平/延庆
v5 = read_vol("vol05.txt")
b5 = split_prefecture_blocks(v5, ["永平府","延庆府"])
report["永平府"] = run_prefecture(YONGPING, b5["永平府"])
report["延庆州"] = run_prefecture(YANQING, b5["延庆府"])

for pf, rows in report.items():
    print(f"\n===== {pf} =====")
    for fn,nm,ns,np,evo in rows:
        print(f"  {fn:34s} mtn={nm:2d} site={ns:2d} per={np:2d}  [{evo}]")
