"""
从卷1顺天府原文中，按县名提取：
- 建置沿革段（XX县【...】）
- 山川段中带"在XX县"的条目
- 寺观/祠庙/陵墓/古迹/学校/关梁中带"在XX县"的条目
- 人物中明确标注该县的
输出为 JSON 草稿，供人工审核后落盘。
"""
import re, json, os, sys

VOL_DIR = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_work"
OUT_DIR = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol01"

# 顺天府属县清单（按原文顺序，c01..c22）
SHUNTIAN_COUNTIES = [
    ("c01", "大兴县"),
    ("c02", "宛平县"),
    ("c03", "良乡县"),
    ("c04", "固安县"),
    ("c05", "永清县"),
    ("c06", "东安县"),
    ("c07", "香河县"),
    # 通州 s01 领县四
    ("c08", "三河县"),
    ("c09", "武清县"),
    ("c10", "漷县"),
    ("c11", "宝坻县"),
    # 昌平州 s02 领县三
    ("c12", "顺义县"),
    ("c13", "密云县"),
    ("c14", "怀柔县"),
    # 涿州 s03 领县一
    ("c15", "房山县"),
    # 霸州 s04 领县三
    ("c16", "文安县"),
    ("c17", "大城县"),
    ("c18", "保定县"),
    # 蓟州 s05 领县四
    ("c19", "玉田县"),
    ("c20", "丰润县"),
    ("c21", "遵化县"),
    ("c22", "平谷县"),
]

# 属州清单
SHUNTIAN_SUBS = [
    ("s01", "通州"),
    ("s02", "昌平州"),
    ("s03", "涿州"),
    ("s04", "霸州"),
    ("s05", "蓟州"),
]

text = open(os.path.join(VOL_DIR, "vol01.txt"), encoding="utf-8").read()

# 提取大段落：以　　段首（两个全角空格）切分
# 每段以 "门" 开头（建置沿革/郡名/形胜/风俗/山川/土产/公署/学校/书院/宫室/关梁/寺观/祠庙/陵墓/古迹/名宦/流寓/人物/列女/仙释）
sections = re.split(r"\n　　", text)
sections = [s.strip() for s in sections if s.strip()]

def find_section_range(start_kw, end_kw):
    """从 start_kw 开头的段开始，到 end_kw 开头的段之前结束，合并所有段"""
    start_idx = None
    end_idx = None
    for i, s in enumerate(sections):
        if start_idx is None and s.startswith(start_kw):
            start_idx = i
        elif start_idx is not None and s.startswith(end_kw):
            end_idx = i
            break
    if start_idx is None:
        return ""
    if end_idx is None:
        end_idx = len(sections)
    return "\n".join(sections[start_idx:end_idx])

evo_sec = find_section_range("建置沿革", "郡名")
mtn_sec = find_section_range("山川", "土产")
site_secs = {
    "学校": find_section_range("学校", "书院"),
    "书院": find_section_range("书院", "宫室"),
    "宫室": find_section_range("宫室", "关梁"),
    "关梁": find_section_range("关梁", "寺观"),
    "寺观": find_section_range("寺观", "祠庙"),
    "祠庙": find_section_range("祠庙", "陵墓"),
    "陵墓": find_section_range("陵墓", "古迹"),
    "古迹": find_section_range("古迹", "名宦"),
}
per_secs = {
    "名宦": find_section_range("名宦", "流寓"),
    "流寓": find_section_range("流寓", "人物"),
    "人物": find_section_range("人物", "列女"),
    "列女": find_section_range("列女", "仙释"),
    "仙释": find_section_range("仙释", "等恐"),
}

def split_bracket_entries(sec):
    """把 '建置沿革禹贡...大兴县【...】宛平县【...】...' 切成 [(name, detail), ...]"""
    parts = re.findall(r"([^【\n]+?)【([^】]*)】", sec)
    return [(n.strip(), d.strip()) for n, d in parts if n.strip()]

# 提取每个县的建置沿革
county_data = {}
for code, cname in SHUNTIAN_COUNTIES:
    county_data[cname] = {
        "code": code,
        "evo": "",
        "mtns": [],
        "sites": [],
        "pers": [],
    }

# OCR 异体字归一
OCR_NORM = str.maketrans({
    "寳": "宝", "寜": "宁", "懐": "怀", "密": "密", "宻": "密", "漷": "漷",
    "徳": "德", "隷": "隶", "綂": "统", "防": "坊", "夀": "寿",
    "鳯": "凤", "龍": "龙", "雲": "云", "風": "风", "氣": "气",
    "寜": "宁", "寳": "宝", "澗": "涧", "峯": "峰", "嶺": "岭",
})
def norm(s):
    return s.translate(OCR_NORM)

# 建置沿革：从 evo_sec 里找 "XX县【...】"——name 必须正好是县名
evo_entries = split_bracket_entries(evo_sec)
for name, detail in evo_entries:
    name_clean = re.sub(r"[【\s].*$", "", name).strip()
    name_norm = norm(name_clean)
    for code, cname in SHUNTIAN_COUNTIES:
        if name_norm == cname or name_norm == cname.replace("县", ""):
            county_data[cname]["evo"] = detail
            break

# 山川：在 mtn_sec 里找条目，location_text 含县名
mtn_entries = split_bracket_entries(mtn_sec)
MTN_TYPES = ["山","岭","峰","冈","岩","洞","泉","溪","江","河","湖","潭","池","堰","关","桥","井"]
def guess_mtn_type(name):
    for t in MTN_TYPES:
        if name.endswith(t):
            return t
    if "岭" in name: return "岭"
    if "水" in name or "河" in name or "川" in name: return "河"
    return "山"

for name, detail in mtn_entries:
    name_clean = re.sub(r"[【\s].*$", "", name).strip()
    detail_norm = norm(detail)
    for code, cname in SHUNTIAN_COUNTIES:
        short = cname.replace("县", "")
        if short in detail_norm[:30] or cname in detail_norm[:30]:
            county_data[cname]["mtns"].append({
                "name": name_clean,
                "type": guess_mtn_type(name_clean),
                "location_text": detail[:60],
                "description": detail,
                "original": f"{name_clean}【{detail}】"[:200],
            })
            break

# 古迹类（寺观/祠庙/陵墓/学校/书院/宫室/关梁）
SITE_TYPE_MAP = {
    "学校": "学校", "书院": "书院", "宫室": "宫室", "关梁": "关梁",
    "寺观": "寺观", "祠庙": "祠庙", "陵墓": "陵墓", "古迹": "古迹",
}
for sec_name, sec_text in site_secs.items():
    entries = split_bracket_entries(sec_text)
    for name, detail in entries:
        name_clean = re.sub(r"[【\s].*$", "", name).strip()
        detail_norm = norm(detail)
        for code, cname in SHUNTIAN_COUNTIES:
            short = cname.replace("县", "")
            if short in detail_norm[:30] or cname in detail_norm[:30]:
                county_data[cname]["sites"].append({
                    "name": name_clean,
                    "type": SITE_TYPE_MAP[sec_name],
                    "location_text": detail[:60],
                    "history_lore": detail,
                    "original": f"{name_clean}【{detail}】"[:200],
                })
                break

# 人物：名宦/流寓/人物/列女/仙释
for sec_name, sec_text in per_secs.items():
    entries = split_bracket_entries(sec_text)
    for name, detail in entries:
        name_clean = re.sub(r"[【\s].*$", "", name).strip()
        detail_norm = norm(detail)
        for code, cname in SHUNTIAN_COUNTIES:
            short = cname.replace("县", "")
            if short in detail_norm[:40] or cname in detail_norm[:40]:
                county_data[cname]["pers"].append({
                    "name": name_clean,
                    "type": sec_name,
                    "summary": detail[:120],
                    "original": f"{name_clean}【{detail}】"[:200],
                })
                break

# 输出草稿
os.makedirs(OUT_DIR, exist_ok=True)
draft = {}
for code, cname in SHUNTIAN_COUNTIES:
    d = county_data[cname]
    draft[cname] = {
        "code": code,
        "evo_len": len(d["evo"]),
        "mtns_count": len(d["mtns"]),
        "sites_count": len(d["sites"]),
        "pers_count": len(d["pers"]),
    }
    print(f"{code} {cname}: evo={len(d['evo'])}字  mtn={len(d['mtns'])}  site={len(d['sites'])}  per={len(d['pers'])}")

# 保存完整草稿
with open(os.path.join(VOL_DIR, "shuntian_counties_draft.json"), "w", encoding="utf-8") as f:
    json.dump(county_data, f, ensure_ascii=False, indent=2)
print("\n草稿已存:", os.path.join(VOL_DIR, "shuntian_counties_draft.json"))
