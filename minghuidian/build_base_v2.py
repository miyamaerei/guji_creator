# -*- coding: utf-8 -*-
"""《明会典》底座重建 v2（P0 修复版，位置法 ID 映射）

修复 v1 缺陷：
  A. 卷标题 OCR 变体：首字"眀"(U+7700)、"卷"字被 OCR 成私用区字形 U+EB08
     （影响卷 33 / 128 / 129 / 130）→ 放宽 VOL_MARK 正则。
  B. 卷122 源文本本身无内容（标题紧邻卷123）→ 保留为空卷并标注。
  C. 器物/仪仗/礼仪内容被丢弃（卷 60/149/150/152/153 产出 0 条）
     → 新增两条起始规则，只把"原本会被丢弃"的行变成条目。

ID 映射：用「起始行号」把旧条目一一对应到新条目（旧起始行集合是新起始行集合的子集），
输出 _id_map.json（old_id -> new_id），供下游层重映射。
"""

import json, os, re, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "明会典.txt")
OUT_DIR = os.path.join(ROOT, "_extract")
os.makedirs(OUT_DIR, exist_ok=True)

OCR_FIX = {
    "明防典": "明会典", "知防": "知会", "中防": "中门", "正防": "正门",
    "直防": "直厅", "资防直": "资廉直", "复防通": "复会通", "臯防": "臯夔",
    "孝防": "孝廉", "特防": "特旨", "防选": "选除", "防同": "会同",
    "照防": "照会", "圣防": "圣旨", "以防": "以会试",
    "钦定四库全书": "",
}

ERA_RE = re.compile(
    r"^(洪武|永乐|洪熈|洪熙|宣徳|宣德|正统|景泰|天顺|成化|弘治|正德|嘉靖|隆庆|万厯|万历)"
)
VOL_STRICT = re.compile(r"^明(?:会|防)典卷([一二三四五六七八九十百零]+)\s*$")
VOL_RELAX = re.compile(
    r"^[明眀朙][会防㑹]典[卷\uE000-\uF8FF]\s*([一二三四五六七八九十百零]+)\s*$"
)

CLASSIC_TITLES = {"诸司职掌", "皇明祖训", "大明令", "大诰", "大明集礼", "洪武礼制",
                  "礼仪定式", "稽古定制", "孝慈录", "教民榜文", "大明律", "军法定律", "宪纲"}
GROUP_HEADS = {"事例", "南京事例"}
ORG_SUBHEADS = {"正官", "首领官", "属官", "承差", "知印", "使臣"}

QTY = ("一对|二对|三对|四对|五对|六对|七对|八对|九对|十对|"
       "一乘|二乘|一面|二面|一把|二把|一副|二副|一件|二件|一张|二张|"
       "一管|二管|四管|一顶|二顶|一叶|二叶|一个|二个|一枝|二枝|一套|二套|"
       "一座|二座|一双|二双|一只|二只|一盘|二盘|一串|二串|一条|二条|一根|二根|"
       "一十|二十|三十|四十|五十|六十|七十|八十|九十|一百|二百|三百|四百|五百")
OBJ_ITEM_RE = re.compile(r"^[^\s，。；：、凡奏诏敕令国洪永宣正景天成弘嘉隆万]{2,14}(?:%s)" % QTY)
NOISE_SUB = ("史部,政书类", "史部，政书类", "<史部", "〈史部", "＜史部", "钦定四库全书")


def cn2int(s):
    s = s.strip()
    if not s: return 0
    if s == "一百八十": return 180
    if s.startswith("一百"):
        rest = s[2:]; return 100 + (cn2int(rest) if rest else 0)
    if s.startswith("十"):
        rest = s[1:]
        return 10 + {"":0,"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}.get(rest, 0)
    if "十" in s:
        a, b = s.split("十")
        HI = {"":1,"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}
        LO = {"":0,"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}
        return HI.get(a,1)*10 + LO.get(b,0)
    return {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}.get(s,0)


def ocr_fix(s):
    for k, v in OCR_FIX.items():
        s = s.replace(k, v)
    return s


def is_noise(s):
    return any(k in s for k in NOISE_SUB)


def is_yamen_line(s):
    if not (2 <= len(s) <= 6): return False
    if any(p in s for p in ["。","，","；","：","、","一员","二员","三员","令","凡","奏"]): return False
    if ERA_RE.match(s): return False
    if s in {"官制","衙门","事例","事例附录","在外","在京","吏部","户部","礼部","兵部","刑部","工部"}: return False
    return True


def is_geo_line(s):
    if not (2 <= len(s) <= 15): return False
    if any(p in s for p in ["。","，","；","：","、","界","抵"]): return False
    return s.endswith(("承宣布政使司","都司","布政司","府","州","县","卫","所"))


def classify_kind(s):
    """条目性质分类（启发式）：事例 / 沿革 / 事目 / 名录行 / 长文。
    用于把 v1 混在一起的事目标题、名录行与真正的「凡…」事例区分开。
    ⚠ 启发式字段，非人工校订结果。"""
    if not s:
        return "长文"
    if s.startswith("凡") or (s.startswith("一") and len(s) > 15):
        return "事例"
    if ERA_RE.match(s):
        return "事例"
    if s.startswith(("国初", "南京在")):
        return "沿革"
    if "国初" in s and any(k in s for k in ("改", "置", "罢", "革", "设")):
        return "沿革"
    punct = any(p in s for p in "。，；：、")
    ORG_SUFFIX = ("库", "司", "局", "院", "寺", "监", "仓", "驿", "卫", "所",
                  "门", "殿", "坛", "庙", "制", "仪", "礼", "事例")
    # 名录行：极短碎片（非事目类词）/ 含计数 / 地理机构后缀
    if len(s) <= 6 and not punct and not s.endswith(ORG_SUFFIX):
        return "名录行"
    if len(s) <= 30 and (any(k in s for k in ("一员", "二员", "三名", "一对", "二对", "一把", "一乘", "一面"))
                         or s.endswith(("府", "州", "县", "卫", "所", "仓", "驿"))):
        return "名录行"
    # 事目/标题：中短行且无句读
    if len(s) <= 12 and not punct:
        return "事目"
    return "长文"


def split_volume(vno, lines, base_line, mode):
    """mode='v1' 复刻旧切分；mode='v2' 修复切分。返回 [(start_line, sec, src, title, body)]"""
    items = []
    cur_section = None
    cur_source = None
    seq = 0
    cur_title = None
    cur_body = []
    cur_start = None

    def flush():
        nonlocal cur_title, cur_body, cur_start
        if cur_title is not None:
            body = "".join(cur_body).strip()
            if body:
                items.append((cur_start, cur_section, cur_source, cur_title, body))
        cur_title = None; cur_body = []; cur_start = None

    def start(ln, title, body):
        nonlocal seq, cur_title, cur_body, cur_start
        seq += 1; cur_title = title; cur_body = [body]; cur_start = ln

    for off, raw in enumerate(lines):
        ln = base_line + off
        s = raw.strip()
        if not s: continue
        s = ocr_fix(s)
        if not s: continue
        if mode == "v2" and is_noise(s): continue
        if (VOL_STRICT if mode == "v1" else VOL_RELAX).match(s): continue
        if s in CLASSIC_TITLES:
            flush(); cur_source = s; continue
        if s in GROUP_HEADS:
            flush(); continue
        if s in ORG_SUBHEADS:
            if cur_title is not None: cur_body.append("【%s】" % s)
            continue

        if s.startswith("凡"): flush(); start(ln, s[:30], s); continue
        if ERA_RE.match(s): flush(); start(ln, s[:30], s); continue
        if s.startswith(("国初","南京在")): flush(); start(ln, s[:30], s); continue
        if s.startswith("一") and len(s) > 15: flush(); start(ln, s[:30], s); continue

        if mode == "v2" and len(s) > 22 and OBJ_ITEM_RE.match(s):
            flush(); start(ln, s[:30], s); continue

        if is_yamen_line(s) and cur_title is None:
            if cur_section in ("官制","衙门","吏部三","吏部四","吏部五"):
                flush(); start(ln, s, s)
            else:
                cur_section = s
            continue
        if is_yamen_line(s) and not s.startswith("凡"):
            flush(); start(ln, s, s); continue
        if is_geo_line(s) and not s.startswith("凡"):
            flush(); start(ln, s, s); continue

        if mode == "v2" and cur_title is None and len(s) > 15:
            start(ln, s[:30], s); continue

        if cur_title is not None:
            cur_body.append(s)

    flush()
    return items


def _is_footer(i, all_lines, regex):
    """页脚判定：其后 1-2 行是「钦定四库全书」或另一卷标题。"""
    for j in (i + 1, i + 2):
        if j < len(all_lines):
            s = all_lines[j].strip()
            if "钦定四库全书" in s or regex.match(s):
                return True
    return False


def collect_bounds(all_lines, regex, fix_missing_header=False):
    """取每卷首次出现为卷首。fix_missing_header=True 时，对"仅出现一次且为页脚"
    的卷（如卷122 天头缺失），用前一卷的页脚作为其卷首。"""
    occ = collections.defaultdict(list)
    for i, l in enumerate(all_lines):
        m = regex.match(l.strip())
        if m:
            v = cn2int(m.group(1))
            if v and 1 <= v <= 180:
                occ[v].append(i)
    first = {}
    for v, lst in occ.items():
        if fix_missing_header and len(lst) == 1 and _is_footer(lst[0], all_lines, regex) and (v - 1) in occ:
            first[v] = occ[v - 1][-1]
        else:
            first[v] = lst[0]
    return sorted(first.items(), key=lambda x: x[1])


def run(all_lines, bounds, mode):
    out = {}   # (vol, start_line) -> (sec,src,title,body)
    for idx, (vno, st) in enumerate(bounds):
        end = bounds[idx+1][1] if idx+1 < len(bounds) else len(all_lines)
        for (ln, sec, src, t, b) in split_volume(vno, all_lines[st:end], st, mode):
            out[(vno, ln)] = (sec, src, t, b)
    return out


def main():
    all_lines = [l.rstrip("\n").rstrip("\r") for l in open(SRC, encoding="utf-8")]

    # 旧底座（优先读 v1 备份，保证可重跑）
    old_path = os.path.join(ROOT, "_backup_p0", "_item_registry.v1.json")
    if not os.path.exists(old_path):
        old_path = os.path.join(ROOT, "_item_registry.json")
    old_reg = json.load(open(old_path, encoding="utf-8"))
    print("旧底座来源：%s（%d 条）" % (os.path.basename(old_path), len(old_reg)))

    # 1) 复刻 v1，建立 old_id -> 起始行号
    v1_bounds = collect_bounds(all_lines, VOL_STRICT)
    v1_items = run(all_lines, v1_bounds, "v1")
    # v1 内部按 (vol, start_line) 排序，与原 seq 顺序一致
    v1_sorted = sorted(v1_items.keys(), key=lambda x: (x[0], x[1]))
    # 按卷分组，赋 old_id（复刻 %03d-%03d）
    old_line_of_id = {}
    per_vol = collections.defaultdict(list)
    for (vno, ln) in v1_sorted:
        per_vol[vno].append(ln)
    for vno, lns in per_vol.items():
        for i, ln in enumerate(lns):
            old_line_of_id["%03d-%03d" % (vno, i+1)] = ln

    # 校验：复刻条数是否与旧底座一致
    match = sum(1 for k in old_line_of_id if k in old_reg)
    print("v1 复刻条目 %d，与旧底座 ID 交集 %d" % (len(old_line_of_id), match))

    # 2) 新切分 v2
    v2_bounds = collect_bounds(all_lines, VOL_RELAX, fix_missing_header=True)
    print("v2 检测卷数：%d" % len(v2_bounds))
    v2_items = run(all_lines, v2_bounds, "v2")
    print("v2 条目数：%d" % len(v2_items))

    # 3) 分配 new_id：优先复用旧 ID（同卷同起始行）；否则分配新号
    old_id_at_line = {ln: oid for oid, ln in old_line_of_id.items()}
    line_to_new = {}
    registry = {}
    id_map = {}
    per_vol2 = collections.defaultdict(list)
    for (vno, ln) in v2_items:
        per_vol2[vno].append(ln)
    for vno, lns in per_vol2.items():
        lns.sort()
        used = set()
        assigned = {}
        # 第一轮：复用（旧 ID 卷前缀须一致）
        for ln in lns:
            oid = old_id_at_line.get(ln)
            if oid and oid.split("-")[0] == "%03d" % vno and oid not in used:
                assigned[ln] = oid
                used.add(oid)
        # 第二轮：新号
        counter = 1
        for ln in lns:
            if ln in assigned:
                continue
            while True:
                cand = "%03d-%03d" % (vno, counter)
                counter += 1
                if cand not in used:
                    break
            assigned[ln] = cand
            used.add(cand)
        # 落盘 + 记录 old->new
        for ln in lns:
            nid = assigned[ln]
            line_to_new[(vno, ln)] = nid
            sec, src, t, b = v2_items[(vno, ln)]
            registry[nid] = {"volume": vno, "node_kind": classify_kind(b),
                             "section": sec or "", "source": src or "", "title": t,
                             "original": b, "norm": ocr_fix(b)}
            oid = old_id_at_line.get(ln)
            if oid and oid != nid:
                id_map[oid] = nid
    print("ID 映射条目（卷前缀变动）：%d" % len(id_map))
    # 安全检查：是否有旧 ID 未映射且未复用
    unmapped = [oid for oid in old_reg if oid not in registry and oid not in id_map]
    print("未覆盖的旧 ID：%d %s" % (len(unmapped), unmapped[:12]))
    # 兜底：v1 误切的卷/事目标题（如「刑部四」「兵部十七」）无对应新条目，
    # 映射到其所在行之后最近的 v2 条目，保证下游引用不悬空。
    line_to_nid = {ln: nid for (v, ln), nid in line_to_new.items()}
    new_starts = sorted(line_to_nid)
    import bisect
    for oid in unmapped:
        ln = old_line_of_id.get(oid)
        if ln is None:
            continue
        idx = bisect.bisect_left(new_starts, ln)
        if idx < len(new_starts):
            id_map[oid] = line_to_nid[new_starts[idx]]
    print("补映射后 ID 映射总条目：%d" % len(id_map))

    # 写盘
    json.dump(registry, open(os.path.join(ROOT, "_item_registry.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    json.dump(id_map, open(os.path.join(ROOT, "_id_map.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # 统计
    vc = collections.Counter(k.split("-")[0] for k in registry)
    empty = [v for v in range(1, 181) if vc.get("%03d" % v, 0) == 0]
    print("卷覆盖：%d/180，空卷：%s" % (len([v for v in range(1,181) if vc.get('%03d'%v,0)>0]), empty))

    # 卷文件
    for vno, lns in per_vol2.items():
        lns.sort()
        with open(os.path.join(OUT_DIR, "%03d_卷.txt" % vno), "w", encoding="utf-8") as f:
            for ln in lns:
                nid = line_to_new[(vno, ln)]
                sec, src, t, b = v2_items[(vno, ln)]
                f.write("%s|%s|%s|%s|%s\n" % (nid, sec or "", src or "", t, b))


if __name__ == "__main__":
    main()
