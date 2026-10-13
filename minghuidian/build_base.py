# -*- coding: utf-8 -*-
"""《明会典》底座切分器 v3：全 180 卷 + 官制名录识别

切分规则：
A. 规则条目（凡.../年号.../国初.../一...）
B. 官制名录：衙门名短行 + 其下连续短行（<30字）= 一条 NAM
C. 事目/司名短行作为 section 上下文
D. 典籍标题作为 source
"""

import json, os, re

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
VOL_MARK = re.compile(r"^明(?:会|防)典卷([一二三四五六七八九十百零]+)\s*$")

CLASSIC_TITLES = {"诸司职掌", "皇明祖训", "大明令", "大诰", "大明集礼", "洪武礼制",
                  "礼仪定式", "稽古定制", "孝慈录", "教民榜文", "大明律", "军法定律", "宪纲"}
GROUP_HEADS = {"事例", "南京事例"}
# 官制分组标记（不单独成条）
ORG_SUBHEADS = {"正官", "首领官", "属官", "承差", "知印", "使臣"}


def cn2int(s):
    s = s.strip()
    if not s: return 0
    if s == "一百八十": return 180
    if s.startswith("一百"):
        rest = s[2:]
        return 100 + (cn2int(rest) if rest else 0)
    if s.startswith("十"):
        rest = s[1:]
        return 10 + ({"":0,"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}.get(rest, 0))
    if "十" in s:
        a, b = s.split("十")
        return {"":1,"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}.get(a,1)*10 + \
               {"":0,"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}.get(b,0)
    return {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}.get(s, 0)


def ocr_fix(s):
    for k, v in OCR_FIX.items():
        s = s.replace(k, v)
    return s


def is_yamen_line(s):
    """衙门名短行：2-6字，无动词，无标点，结尾不是一员/二员。"""
    if not (2 <= len(s) <= 6):
        return False
    if any(p in s for p in ["。", "，", "；", "：", "、", "一员", "二员", "三员", "令", "凡", "奏"]):
        return False
    if ERA_RE.match(s):
        return False
    # 排除事目关键词
    if s in {"官制", "衙门", "事例", "事例附录", "在外", "在京", "吏部", "户部", "礼部", "兵部", "刑部", "工部"}:
        return False
    return True


def is_geo_line(s):
    """地理单元短行：X等处承宣布政使司 / X府 / X州 / X县，2-15字。"""
    if not (2 <= len(s) <= 15):
        return False
    if any(p in s for p in ["。", "，", "；", "：", "、", "界", "抵"]):
        return False
    # 布政使司 / 都司 / 府 / 州 / 县
    if s.endswith(("承宣布政使司", "都司", "布政司", "府", "州", "县", "卫", "所")):
        return True
    return False


def is_compact_line(s):
    """名录内容短行：<30字，含'员'/'名'或纯官职罗列。"""
    if len(s) > 40:
        return False
    return True


def split_volume(vno, lines):
    items = []
    cur_section = None
    cur_source = None
    seq = 0
    cur_title = None
    cur_body = []
    in_minglu = False  # 是否在官制名录模式

    def flush():
        nonlocal cur_title, cur_body, seq
        if cur_title is not None:
            body = "".join(cur_body).strip()
            if body:
                items.append((seq, cur_section, cur_source, cur_title, body))
            cur_title = None
            cur_body = []

    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        s = ocr_fix(s)
        if not s:
            continue
        if VOL_MARK.match(s):
            continue
        if s in CLASSIC_TITLES:
            flush()
            cur_source = s
            continue
        if s in GROUP_HEADS:
            flush()
            continue
        if s in ORG_SUBHEADS:
            # 官制子分组（正官/首领官），作为上下文，不切条
            if cur_title is not None:
                cur_body.append("【%s】" % s)
            continue

        # 条目起点：凡...
        if s.startswith("凡"):
            flush()
            seq += 1
            cur_title = s[:30]
            cur_body = [s]
            in_minglu = False
            continue
        # 年号开头
        if ERA_RE.match(s):
            flush()
            seq += 1
            cur_title = s[:30]
            cur_body = [s]
            in_minglu = False
            continue
        # 国初/南京沿革
        if s.startswith(("国初", "南京在")):
            flush()
            seq += 1
            cur_title = s[:30]
            cur_body = [s]
            in_minglu = False
            continue
        # "一自古以来..."
        if s.startswith("一") and len(s) > 15:
            flush()
            seq += 1
            cur_title = s[:30]
            cur_body = [s]
            in_minglu = False
            continue
        # 官制名录：衙门名短行
        if is_yamen_line(s) and cur_title is None:
            # 在"官制"section下，衙门名切条；否则作为 section
            if cur_section in ("官制", "衙门", "吏部三", "吏部四", "吏部五"):
                flush()
                seq += 1
                cur_title = s
                cur_body = [s]
            else:
                cur_section = s
            continue
        if is_yamen_line(s) and not s.startswith("凡"):
            flush()
            seq += 1
            cur_title = s
            cur_body = [s]
            in_minglu = True
            continue
        # 地理名录：布政使司/府/州县
        if is_geo_line(s) and not s.startswith("凡"):
            flush()
            seq += 1
            cur_title = s
            cur_body = [s]
            continue
        # 续行
        if cur_title is not None:
            cur_body.append(s)

    flush()
    return [("%03d-%03d" % (vno, i+1), sec, src, t, b)
            for i, (_, sec, src, t, b) in enumerate(items)]


def main():
    with open(SRC, encoding="utf-8") as f:
        all_lines = [l.rstrip("\n").rstrip("\r") for l in f]

    # 找所有卷边界（去重）
    vol_bounds = []
    seen_vols = set()
    for i, l in enumerate(all_lines):
        s = l.strip()
        m = re.match(r"^明(?:会|防)典卷([一二三四五六七八九十百零]+)\s*$", s)
        if m:
            v = cn2int(m.group(1))
            if v and v not in seen_vols and 1 <= v <= 180:
                vol_bounds.append((v, i))
                seen_vols.add(v)

    print("检测到卷标记：%d 卷" % len(vol_bounds))

    registry = {}
    total = 0
    for idx, (vno, start) in enumerate(vol_bounds):
        end = vol_bounds[idx+1][1] if idx+1 < len(vol_bounds) else len(all_lines)
        items = split_volume(vno, all_lines[start:end])
        total += len(items)
        if vno <= 13 or vno % 20 == 0:  # 打印前13卷和每20卷
            print("卷%3d: %4d 条" % (vno, len(items)))

        with open(os.path.join(OUT_DIR, "%03d_卷.txt" % vno), "w", encoding="utf-8") as f:
            for iid, sec, src, title, body in items:
                f.write("%s|%s|%s|%s|%s\n" % (iid, sec or "", src or "", title, body))
                registry[iid] = {
                    "section": sec or "", "source": src or "", "title": title,
                    "original": body, "norm": ocr_fix(body),
                }
    with open(os.path.join(ROOT, "_item_registry.json"), "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=1)
    print("\n全 180 卷切分完成：总计 %d 条" % total)


if __name__ == "__main__":
    main()
