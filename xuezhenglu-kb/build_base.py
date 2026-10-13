# -*- coding: utf-8 -*-
"""《政学录》底座：卷拆分切分 → _extract/ + _item_registry.json

切分规则（schemas.md §1/§3）：
- 卷级条目：卷一"内阁/六部/科道"3 个无符号标题（各带正文）→ 01-001..01-003
- △ 标题条目：`^△...` 行 + 其后正文 → 01-004..01-023（六部则例条）
- ○ 标题条目：`^○...` 行 + 其后正文（卷一 6 个 ○ 分组标题无正文，跳过）
- 跳过行：卷首署名（畿辅丛书/枣强郑端辑）、卷一 6 行部名总目、卷二卷首官职目录行、空行
- 缺字 □/■〈…〉 保留原形；norm 异体归一（厯→历、廵→巡、覈→核、曡→叠、賸→剩、悞→误、紏→纠）

输出：_extract/NN_卷名.txt（条N|○标题|正文）+ _item_registry.json
预计 183 条：卷1=23 / 卷2=15 / 卷3=111 / 卷4=2 / 卷5=32
"""

import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT, "原文")
OUT_DIR = os.path.join(ROOT, "_extract")
os.makedirs(OUT_DIR, exist_ok=True)

CN = ["一", "二", "三", "四", "五"]
VOL_EXPECT = {"1": 23, "2": 15, "3": 111, "4": 2, "5": 32}

# 异体/繁体 → 规范简体（与 schemas.md §3.2 一致）
NORM_MAP = {
    "厯": "历", "厶": "私", "廵": "巡", "覈": "核", "曡": "叠", "賸": "剩",
    "悞": "误", "紏": "纠", "咨": "咨", "罽": "罽", "儹": "攒", "兠": "兜",
    "閧": "哄", "幇": "帮", "麕": "麇", "勦": "剿", "誼": "谊", "闘": "斗",
    "壻": "婿", "舖": "铺", "踈": "疏", "襍": "杂", "稜": "棱", "闗": "关",
    "缷": "卸", "彽": "低", "秌": "秋", "瘉": "愈", "隷": "隶", "麤": "粗",
    "輭": "软", "覔": "觅", "拏": "拿", "竈": "灶", "廪": "廪", "鉅": "巨",
    "勑": "敕", "菑": "灾", "稲": "稻", "矦": "侯", "暦": "历", "儘": "尽",
    "樁": "桩", "撿": "捡", "摃": "扛", "皁": "皂", "胥": "胥",
}
# 常用繁体替换（政学录高频字）
TRAD_MAP = {
    "與": "与", "為": "为", "書": "书", "後": "后", "時": "时", "門": "门",
    "問": "问", "聞": "闻", "開": "开", "關": "关", "間": "间", "閣": "阁",
    "條": "条", "務": "务", "須": "须", "許": "许", "責": "责", "罰": "罚",
    "罰": "罚", "獄": "狱", "錢": "钱", "糧": "粮", "銀": "银", "兩": "两",
    "縣": "县", "州": "州", "府": "府", "官": "官", "職": "职", "選": "选",
    "禮": "礼", "儀": "仪", "樂": "乐", "歲": "岁", "萬": "万", "興": "兴",
    "國": "国", "體": "体", "號": "号", "數": "数", "發": "发", "單": "单",
    "應": "应", "當": "当", "總": "总", "監": "监", "縣": "县", "學": "学",
    "教": "教", "報": "报", "執": "执", "臺": "台", "準": "准", "參": "参",
    "照": "照", "歸": "归", "獨": "独", "斷": "断", "聽": "听", "審": "审",
    "訟": "讼", "訴": "诉", "詞": "词", "誣": "诬", "許": "许", "馬": "马",
    "驛": "驿", "隸": "隶", "撲": "扑", "撥": "拨", "賣": "卖", "買": "买",
    "貨": "货", "稅": "税", "課": "课", "額": "额", "數": "数", "冊": "册",
    "録": "录", "紀": "纪", "綱": "纲", "經": "经", "歷": "历", "設": "设",
    "議": "议", "講": "讲", "證": "证", "據": "据", "辯": "辩", "變": "变",
    "遷": "迁", "邊": "边", "衛": "卫", "營": "营", "軍": "军", "軍": "军",
    "統": "统", "績": "绩", "給": "给", "約": "约", "網": "网", "紙": "纸",
    "冊": "册", "門": "门", "開": "开", "關": "关", "請": "请", "謹": "谨",
    "誠": "诚", "讓": "让", "贊": "赞", "頌": "颂", "風": "风", "額": "额",
    "項": "项", "銀": "银", "鈔": "钞", "銷": "销", "鐘": "钟", "鍾": "钟",
    "鑰": "钥", "鐵": "铁", "銅": "铜", "銀": "银", "價": "价", "倉": "仓",
    "庫": "库", "廒": "廒", "貯": "贮", "撻": "挞", "拏": "拿", "廩": "廪",
    "賑": "赈", "貸": "贷", "賬": "账", "貧": "贫", "窮": "穷", "餓": "饿",
    "飽": "饱", "飲": "饮", "飯": "饭", "餉": "饷", "餓": "饿", "飽": "饱",
}


def norm_text(s):
    out = []
    for ch in s:
        if ch in NORM_MAP:
            out.append(NORM_MAP[ch])
        elif ch in TRAD_MAP:
            out.append(TRAD_MAP[ch])
        else:
            out.append(ch)
    return "".join(out)


# 卷级条目白名单（卷一无符号标题）
VOL_HEADERS = {"内阁", "六部", "科道"}
# 卷一 6 行部名总目（跳过）
PART_GROUPS = {"吏部", "户部", "礼部", "兵部", "刑部", "工部"}
# ○ 分组标题（无正文，跳过，仅卷一）
GROUP_O = {"○吏部", "○户部", "○礼部", "○兵部", "○刑部", "○工部"}
# 卷首署名 / 卷二卷首官职目录行（跳过）
SKIP_LINES = {"畿辅丛书", "枣强郑端辑", "直省", "督抚", "布政司", "按察司", "提学道",
              "守巡道", "盐运司", "知府", "同知通判推官", "知州知县", "州县佐贰", "教官",
              "弟子", "科甲", "贡士", "官恩例贡", "库官", "司狱司", "司狱"}


def split_volume(vno):
    """切分一卷，返回 [(item_id, title, body)]"""
    fn = os.path.join(SRC_DIR, "政学录·卷%s.txt" % CN[vno - 1])
    with open(fn, encoding="utf-8") as f:
        lines = [l.rstrip("\n").rstrip("\r") for l in f]

    items = []
    seq = 0
    cur_title = None      # 当前条目标题（含符号或卷级名）
    cur_body = []
    vol_pending = []      # 卷一头部连续卷级标题（内阁/六部/科道）
    vol_body = []         # 卷级正文累积（按 督臣/台臣 分界拆三条）

    def flush():
        nonlocal cur_title, cur_body, vol_pending, vol_body, seq
        if cur_title is not None:
            items.append((seq, cur_title, "".join(cur_body)))
            cur_title = None
            cur_body = []
        if vol_pending:
            vol_text = "".join(vol_body)
            # 按分界拆三段：内阁（至督臣前）/六部（督臣至台臣前）/科道（台臣起）
            i1 = vol_text.find("督臣")
            i2 = vol_text.find("台臣")
            segs = []
            if i1 >= 0 and i2 >= 0:
                segs = [vol_text[:i1], vol_text[i1:i2], vol_text[i2:]]
            elif i1 >= 0:
                segs = [vol_text[:i1], vol_text[i1:]]
            elif vol_text:
                segs = [vol_text]
            for k, t in enumerate(vol_pending):
                items.append((seq + k, t, segs[k] if k < len(segs) else ""))
            seq += len(vol_pending)
            vol_pending = []
            vol_body = []

    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if s in SKIP_LINES:
            continue
        if s in PART_GROUPS:
            continue
        if s in GROUP_O:
            flush()
            continue
        m = re.match(r"^[○△](.+)$", s)
        if m:
            flush()
            seq += 1
            cur_title = s
            cur_body = []
            continue
        if s in VOL_HEADERS and vno == 1:
            if cur_title is None and not vol_pending:
                vol_pending = [s]
            elif cur_title is None:
                vol_pending.append(s)
            else:
                # 理论不可达（卷级头必在正文前）
                flush()
                seq += 1
                cur_title = s
                cur_body = []
            continue
        if vol_pending:
            vol_body.append(s)
            continue
        if cur_title is None:
            continue
        cur_body.append(s)
    flush()

    # item_id 分配：NN-NNN
    return [(vno, "%02d-%03d" % (vno, i + 1), t, b) for i, (_, t, b) in enumerate(items)]


def main():
    registry = {}
    total = 0
    for vno in range(1, 6):
        items = split_volume(vno)
        vol_total = len(items)
        exp = VOL_EXPECT[str(vno)]
        print("卷%d：切出 %d 条（期望 %d）%s" % (vno, vol_total, exp, "OK" if vol_total == exp else "!! MISMATCH"))
        total += vol_total
        with open(os.path.join(OUT_DIR, "%02d_卷%s.txt" % (vno, CN[vno - 1])), "w", encoding="utf-8") as f:
            for i, (v, iid, title, body) in enumerate(items):
                f.write("条%d|%s|%s\n" % (i + 1, title, body))
                registry[iid] = {"original": ("%s\n%s" % (title, body)), "norm": norm_text(body)}
    with open(os.path.join(ROOT, "_item_registry.json"), "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=1)
    print("总计：%d 条（期望 183）" % total)
    # 空正文检查
    empties = [k for k, v in registry.items() if not v["norm"].strip()]
    print("空正文条目：%d %s" % (len(empties), empties))


if __name__ == "__main__":
    main()
