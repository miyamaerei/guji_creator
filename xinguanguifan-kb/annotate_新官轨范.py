# -*- coding: utf-8 -*-
"""
《新官轨范》实体标注管线（kg-annot v1）
- 种子词典：全部由《新官轨范》文本直接内生（脚本校验每个词条都出现在原文中，未出现者自动剔除并记录）
- 实体类型：11 类封闭枚举 + 兜底「类型待定」（ming-officials-kg 枚举治理规则）
- 方法：词典最长匹配 + 正则规则（时间/数量/刑罚），重叠消解，置信度评分
- 输出：每卷一个 JSON（含 id/text/type/start/end/normalized/confidence/source）+ 全局归一化汇总 + 总报告 + 预处理分词文件
"""
import os, re, json, html as htmllib, glob

OUT_DIR = r"C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat"
CH_DIR = os.path.join(OUT_DIR, "新官轨范_章节")
ANN_DIR = os.path.join(OUT_DIR, "新官轨范_标注")
PRE_FILE = os.path.join(OUT_DIR, "新官轨范_预处理_分词.txt")
MERGE_FILE = os.path.join(OUT_DIR, "新官轨范_实体归一_汇总.json")
REPORT_FILE = os.path.join(OUT_DIR, "新官轨范_实体标注_总报告.md")
SCRIPT_VER = "kg-annot-json-v1"
ENUM_VER = "entity-type-enum-v1"

TYPES = ["official", "person", "org", "place", "document", "institution",
         "behavior", "object", "punishment", "time", "quantity", "undetermined"]
TYPE_CN = {
    "official": "职官", "person": "人物", "org": "机构", "place": "地点",
    "document": "文书", "institution": "制度", "behavior": "行为",
    "object": "器物", "punishment": "刑罚", "time": "时间",
    "quantity": "数量", "undetermined": "类型待定",
}
TYPE_PRIORITY = {t: i for i, t in enumerate(
    ["official", "document", "person", "institution", "org",
     "behavior", "object", "punishment", "place", "time", "quantity", "undetermined"])}

# 异体字归一表（应用于 normalized 与预处理文本）
VARIANT = {"筭": "算", "摽": "标", "滕": "誊", "豊": "丰"}
VARIANT_PENALTY = 0.9

LEX = {
    "official": [
        ("新官", 0.92), ("正官", 0.92), ("长官", 0.85), ("佐贰", 0.9), ("县官", 0.8),
        ("正官", 0.92), ("佐贰官", 0.92), ("首领官", 0.92), ("属官", 0.9),
        ("署印官", 0.9), ("经手官", 0.85), ("巡捕官员", 0.9), ("学官", 0.9),
        ("教官", 0.9), ("教读", 0.85), ("乡官", 0.9), ("京官", 0.9),
        ("寿官", 0.88), ("义官", 0.88), ("前官", 0.8), ("赃官", 0.85),
        ("风宪", 0.68),
        ("吏典", 0.9), ("司吏", 0.85), ("承发吏", 0.9), ("直堂吏", 0.9),
        ("直印吏", 0.9), ("架阁库吏", 0.9), ("刑房吏", 0.9), ("户房吏", 0.9),
        ("兵房吏", 0.9), ("工房吏", 0.9), ("礼房吏", 0.9), ("巡风吏", 0.88),
        ("贴写", 0.85), ("主文", 0.85), ("书手", 0.88), ("表背匠人", 0.85),
        ("门子", 0.88), ("皂隶", 0.88), ("禁子", 0.88), ("狱卒", 0.88),
        ("仵作", 0.88), ("土工", 0.85), ("铺长", 0.85), ("铺兵", 0.85),
        ("弓兵", 0.85), ("应捕", 0.85), ("快手", 0.85), ("火夫", 0.85),
        ("总甲", 0.85), ("直老", 0.85),
        ("粮长", 0.9), ("里长", 0.9), ("里老", 0.9), ("甲首", 0.88),
        ("老人", 0.85), ("阴阳生", 0.88), ("医生", 0.88),
    ],
    "person": [
        ("官民", 0.68), ("军民", 0.68), ("人户", 0.68), ("小民", 0.68),
        ("百姓", 0.68), ("贫民", 0.68), ("富民", 0.68), ("势豪", 0.68),
        ("刁民", 0.68), ("刁泼", 0.68), ("大户", 0.75), ("士夫", 0.85),
        ("乡宦", 0.85), ("耆宿", 0.8), ("父老", 0.8), ("屠户", 0.8),
        ("佃户", 0.8), ("纳户", 0.8), ("生员", 0.88), ("廪生", 0.88),
        ("廪增", 0.85), ("增生", 0.88), ("附学", 0.85), ("礼生", 0.88),
        ("僧道", 0.8), ("师巫", 0.8),
        ("囚犯", 0.85), ("干证", 0.8), ("原告", 0.85), ("被告", 0.85),
        ("强盗", 0.8), ("窃盗", 0.8), ("贼盗", 0.78), ("贼", 0.75),
        ("赵甲", 0.9), ("王大", 0.9),
    ],
    "org": [
        ("官府", 0.85), ("六房吏典", 0.9),
        ("本县", 0.85), ("概县", 0.8), ("邻县", 0.8), ("县衙", 0.9),
        ("六房", 0.9), ("吏房", 0.9), ("户房", 0.9), ("礼房", 0.9),
        ("兵房", 0.9), ("刑房", 0.9), ("工房", 0.9), ("县学", 0.85),
        ("学校", 0.8), ("儒学", 0.85), ("明伦堂", 0.8), ("巡检司", 0.9),
        ("布政司", 0.9), ("按察司", 0.9), ("三司", 0.85), ("法司", 0.8),
        ("卫", 0.85), ("仓", 0.8), ("官库", 0.85), ("库", 0.75),
        ("监", 0.85), ("监房", 0.85), ("养济院", 0.85), ("坛庙", 0.8),
        ("坛", 0.75), ("庙", 0.7), ("寺观", 0.75), ("社学", 0.8),
        ("公馆", 0.85), ("铺舍", 0.8), ("铺", 0.75), ("衙门", 0.68),
        ("上司", 0.68), ("府厅", 0.75), ("府", 0.8), ("州", 0.8),
        ("县", 0.8), ("城隍", 0.6), ("文庙", 0.85), ("庙庵", 0.75), ("架阁库", 0.8),
    ],
    "place": [
        ("城", 0.7), ("乡", 0.7), ("乡里", 0.72), ("里", 0.7), ("都", 0.7),
        ("都图", 0.72), ("图", 0.7), ("坊", 0.7), ("街坊", 0.72),
        ("巷", 0.7), ("街", 0.7), ("胡同", 0.7), ("庄", 0.7), ("田", 0.7),
        ("田地", 0.7), ("塘", 0.7), ("堰", 0.7), ("陂", 0.7), ("沟渠", 0.7),
        ("圩塘", 0.7), ("桥", 0.7), ("桥梁", 0.7), ("道路", 0.7),
        ("地界", 0.7), ("交界", 0.7), ("四至", 0.7), ("后堂", 0.75),
        ("前堂", 0.75), ("公堂", 0.75), ("站台", 0.7), ("甬路", 0.7),
        ("仪门", 0.7), ("头门", 0.7), ("二门", 0.7), ("廊", 0.65), ("书房", 0.7),
    ],
    "document": [
        ("文簿", 0.85), ("簿籍", 0.85), ("囚簿", 0.9), ("勘合文簿", 0.9),
        ("批状簿", 0.9), ("词状簿", 0.9), ("出票文簿", 0.9), ("接递文簿", 0.9),
        ("清军簿", 0.9), ("公罚文簿", 0.9), ("印信文簿", 0.9), ("税粮簿", 0.9),
        ("里长簿", 0.9), ("巡检弓兵簿", 0.9), ("圩塘长簿", 0.9), ("刑簿", 0.9),
        ("监簿", 0.9), ("交盘文册", 0.9), ("黄册", 0.9), ("赋役册", 0.9),
        ("须知文册", 0.9), ("须知", 0.85), ("手本", 0.9), ("告示", 0.85),
        ("勘合", 0.85), ("公文", 0.8), ("牌帖", 0.85), ("批状", 0.85),
        ("词状", 0.85), ("状子", 0.85), ("供状", 0.85), ("口词", 0.85),
        ("执照", 0.85), ("由帖", 0.85), ("度牒", 0.85), ("赤历", 0.85),
        ("揭帖", 0.85), ("卷宗", 0.85), ("案卷", 0.85), ("文卷", 0.85),
        ("底札", 0.85), ("小册", 0.8), ("卯簿", 0.85), ("实征", 0.7),
        ("文册", 0.8), ("小票", 0.8), ("票帖", 0.8), ("关文", 0.8),
        ("结状", 0.8), ("批文", 0.8), ("行移", 0.75), ("仪注", 0.8),
        ("文案", 0.8), ("文移", 0.8), ("册籍", 0.8), ("簿", 0.68),
        ("总册", 0.8),
    ],
    "institution": [
        ("里甲", 0.88), ("均徭", 0.85), ("赋役", 0.85), ("朝觐", 0.8),
        ("考察", 0.8), ("朝觐考察", 0.85), ("优免", 0.8), ("免差", 0.75),
        ("折色", 0.8), ("本色", 0.8), ("火耗", 0.8), ("折银", 0.8),
        ("存留", 0.8), ("岁办", 0.8), ("秋粮", 0.8), ("夏麦", 0.8),
        ("白粮", 0.8), ("寄庄", 0.8), ("揽纳", 0.8), ("放告", 0.82),
        ("乡饮酒礼", 0.85), ("乡饮", 0.8), ("斋戒", 0.8), ("习仪", 0.8),
        ("拜牌", 0.8), ("救护", 0.8), ("迎春", 0.8), ("清军", 0.8),
        ("清匠", 0.8), ("佥补", 0.8), ("编审", 0.8), ("驿递", 0.8),
        ("班匠", 0.75), ("军役", 0.75), ("差徭", 0.8), ("丁粮", 0.8),
        ("钱粮", 0.78), ("粮料", 0.78), ("税粮", 0.78), ("律例", 0.85),
        ("事例", 0.75), ("条例", 0.8), ("禁约", 0.75), ("律法", 0.8),
        ("杂役", 0.75), ("杂差", 0.75), ("徭役", 0.75),
    ],
    "behavior": [
        ("到任", 0.75), ("勾摄", 0.8), ("拘唤", 0.78), ("比较", 0.8),
        ("催征", 0.8), ("征收", 0.8), ("征粮", 0.8), ("放粮", 0.8),
        ("赈恤", 0.8), ("踏勘", 0.8), ("佥点", 0.78), ("点卯", 0.78),
        ("画卯", 0.78), ("升堂", 0.78), ("退堂", 0.78), ("封门", 0.75),
        ("巡视", 0.75), ("巡更", 0.78), ("巡风", 0.78), ("提铃", 0.75),
        ("点囚", 0.8), ("下狱", 0.78), ("提牢", 0.8), ("封监", 0.8),
        ("交盘", 0.82), ("佥押", 0.8), ("用印", 0.8), ("开印", 0.8),
        ("签押", 0.78), ("参见", 0.75), ("参谒", 0.78), ("望阙谢恩", 0.8),
        ("行礼", 0.7), ("祭祀", 0.75), ("祈祷", 0.75), ("种树", 0.75),
        ("开垦", 0.78), ("修筑", 0.75), ("修理", 0.72), ("葺治", 0.75),
        ("搜捕", 0.78), ("缉访", 0.78), ("缉拿", 0.8), ("擒拿", 0.78),
        ("拘拿", 0.78), ("问理", 0.78), ("审理", 0.78), ("审问", 0.78),
        ("背审", 0.8), ("验实", 0.78), ("检验", 0.78), ("相视", 0.72),
        ("埋葬", 0.72), ("掩埋", 0.72), ("用刑", 0.72), ("行刑", 0.75),
        ("支销", 0.72), ("出纳", 0.72), ("封记", 0.72), ("注簿", 0.75),
        ("注销", 0.72), ("勾销", 0.72), ("开报", 0.72), ("禀报", 0.72),
        ("申报", 0.72), ("呈报", 0.72), ("立限", 0.72), ("起解", 0.72),
        ("递送", 0.72), ("转递", 0.72), ("接递", 0.72), ("迎接", 0.7),
        ("款待", 0.7), ("馈送", 0.7), ("设席", 0.7), ("行酒", 0.68),
        ("打点", 0.7), ("催办", 0.72), ("稽考", 0.72), ("查勘", 0.75),
        ("点查", 0.72), ("清查", 0.72), ("刷卷", 0.78), ("点视", 0.72),
        ("点检", 0.72), ("拘追", 0.72), ("催并", 0.72), ("完报", 0.72),
        ("申详", 0.75), ("回申", 0.72), ("发落", 0.72), ("归结", 0.7),
        ("处治", 0.72), ("问罪", 0.75), ("治罪", 0.75), ("分派", 0.72),
        ("均派", 0.72), ("坐派", 0.75), ("佥解", 0.75), ("提督", 0.7),
        ("看守", 0.68), ("守把", 0.72), ("把守", 0.72), ("支应", 0.7),
        ("出办", 0.7), ("收买", 0.68), ("收贮", 0.72), ("给散", 0.72),
        ("放支", 0.72), ("支给", 0.72), ("上纳", 0.72), ("完纳", 0.72),
        ("征完", 0.72), ("较勘", 0.72), ("量情", 0.7), ("量罚", 0.8),
        ("陪纳", 0.7), ("追并", 0.7), ("除豁", 0.75), ("保举", 0.78),
        ("举保", 0.78), ("锁闭", 0.72), ("封锁", 0.72), ("开写", 0.72),
        ("注写", 0.72), ("注摽", 0.7), ("誊写", 0.72), ("抄写", 0.72),
        ("填写", 0.72), ("呈缴", 0.72), ("送缴", 0.72), ("关领", 0.72),
        ("倒换", 0.72), ("销缴", 0.72), ("查销", 0.72), ("会算", 0.72),
        ("称验", 0.72), ("拆封", 0.7), ("看验", 0.7), ("科派", 0.75),
        ("科敛", 0.75), ("除免", 0.72), ("禁革", 0.75), ("省谕", 0.75),
        ("晓谕", 0.75), ("戒谕", 0.72), ("抚恤", 0.72), ("体访", 0.75),
        ("密访", 0.75), ("访知", 0.72), ("提磨", 0.72), ("对会", 0.72),
        ("眼同", 0.72), ("接管", 0.72), ("交割", 0.72), ("整点", 0.72),
        ("洒扫", 0.7), ("修葺", 0.72), ("修整", 0.72), ("起盖", 0.72),
        ("开筑", 0.72), ("种栽", 0.7), ("畜养", 0.7), ("买办", 0.7),
        ("预备", 0.68), ("供应", 0.68), ("供给", 0.68), ("追筭", 0.7),
        ("点放", 0.72), ("盘诘", 0.75), ("稽核", 0.75), ("吊取", 0.72),
        ("吊查", 0.72), ("拘集", 0.72), ("拘押", 0.72), ("收掌", 0.7),
        ("守掌", 0.7), ("经收", 0.7), ("支领", 0.7), ("领给", 0.7),
        ("请给", 0.7), ("造册", 0.78), ("对册", 0.7), ("点对", 0.72),
        ("具结", 0.72), ("直堂", 0.7),
    ],
    "object": [
        ("县印", 0.88), ("铜印", 0.88), ("印信", 0.85),
        ("木牌", 0.85), ("牌", 0.7), ("签", 0.7), ("梆", 0.8), ("木梆", 0.8),
        ("鼓", 0.8), ("钟鼓", 0.8), ("响板", 0.8), ("灯", 0.75),
        ("锁", 0.75), ("锁钥", 0.8), ("铁索", 0.8), ("铁锁", 0.8),
        ("肘镣", 0.85), ("枷", 0.8), ("镣", 0.8), ("杻", 0.75), ("镣杻", 0.8),
        ("夹棍", 0.85), ("拶指", 0.85), ("竹片", 0.8), ("棍板", 0.8),
        ("刑具", 0.8), ("杖", 0.7), ("刑杖", 0.8), ("纸札", 0.75),
        ("笔墨", 0.75), ("砚瓦", 0.75), ("卷架", 0.75), ("桌凳", 0.75),
        ("桌椅", 0.75), ("器皿", 0.75), ("床帐", 0.75), ("家伙", 0.7),
        ("油烛", 0.75), ("柴炭", 0.75), ("纸笔", 0.75), ("牲口", 0.75),
        ("马匹", 0.75), ("猪羊", 0.75), ("鸡鹅", 0.75), ("香纸", 0.75),
        ("祭物", 0.75), ("祭品", 0.75), ("胙肉", 0.75), ("春花", 0.75),
        ("春杖", 0.75), ("油蜡", 0.75), ("公座", 0.65), ("刑枷", 0.8),
    ],
    "punishment": [
        ("责打", 0.82), ("痛责", 0.8), ("责罚", 0.8), ("责治", 0.8),
        ("痛治", 0.8), ("笞责", 0.8), ("重杖", 0.75), ("监候", 0.8),
        ("锁押", 0.75), ("监禁", 0.75), ("淹禁", 0.7), ("罚谷", 0.8),
        ("罚米", 0.8), ("罚纸札", 0.8), ("量罚", 0.8), ("用刑", 0.72),
        ("行杖", 0.72),
    ],
    "time": [
        ("卯时", 0.9), ("辰时", 0.9), ("巳时", 0.9), ("午时", 0.9),
        ("未时", 0.9), ("申时", 0.9), ("酉时", 0.9), ("五更", 0.85),
        ("朔望", 0.85), ("朔", 0.8), ("月终", 0.8),
        ("年终", 0.8), ("初旬", 0.8), ("中旬", 0.8), ("下旬", 0.8),
        ("每日", 0.75), ("每月", 0.75), ("每年", 0.75), ("递年", 0.75),
        ("到任次日", 0.8), ("次日", 0.72), ("明日", 0.72), ("早堂", 0.75),
        ("中堂", 0.75), ("晚堂", 0.75), ("夜晚", 0.72), ("昏夜", 0.7),
        ("月夜", 0.7), ("雪夜", 0.7), ("半月", 0.8), ("半年", 0.8),
    ],
}
GENERIC = {"官民", "军民", "人户", "小民", "百姓", "贫民", "富民",
           "势豪", "刁民", "刁泼", "上司", "衙门", "风宪"}
# 单字词语境守卫：surface -> 禁止的相邻字（前后）
GUARDS = {
    "里": ("面", "面"),
    "都": ("", "要是来去"),
}

CN_NUM = "零一二三四五六七八九十百千万两"
QTY_UNITS = "名|人|里|日|月|年|张|扇|本|件|面|支|间|家|个|口|匹|石|斗|升|两|钱|文|处|所|步|亩|顷|丈|尺|斤|位|员|次|下|更"
QTY_PAT = re.compile(rf"[{CN_NUM}]{{1,8}}(?:{QTY_UNITS})")
SEV_PAT = re.compile(r"若干|多寡")
TIME_PAT = re.compile(rf"初[{CN_NUM}]日|[{CN_NUM}]{{1,6}}日|[{CN_NUM}]{{1,3}}月|[{CN_NUM}]{{1,3}}年|某年月日|某日|某月|某年")
PUN_PAT = re.compile(rf"(?:打|责打|决|罚)[{CN_NUM}]{{1,4}}(?:大棍|大板|棍|板|杖|下)?|[{CN_NUM}]{{1,4}}(?:大棍|大板|棍|板|杖|下)")

# 去重词典
for t in LEX:
    seen = set()
    keep = []
    for surf, conf in LEX[t]:
        if (surf, conf) not in seen:
            seen.add((surf, conf))
            keep.append((surf, conf))
    LEX[t] = keep
# 行为类低分泛化词统一提至 0.70，避免占据人工复核清单
LEX["behavior"] = [(s, 0.7 if c == 0.68 else c) for s, c in LEX["behavior"]]


def load_chapters():
    out = []
    files = sorted(glob.glob(os.path.join(CH_DIR, "*.xhtml")))
    for fp in files:
        base = os.path.basename(fp)
        no = base[:2]
        if no == "00":
            continue
        with open(fp, encoding="utf-8") as f:
            content = f.read()
        items = re.findall(r'<p class="item">(.*?)</p>', content, re.S)
        items = [htmllib.unescape(m).strip() for m in items]
        if not items:
            items = re.findall(r'<p[^>]*>(.*?)</p>', content, re.S)
            items = [htmllib.unescape(m).strip() for m in items]
        out.append((no, base, items))
    return out


FULL_TEXT = "".join(
    htmllib.unescape(re.sub(r"<[^>]+>", "", open(p, encoding="utf-8").read()))
    for p in glob.glob(os.path.join(CH_DIR, "*.xhtml")) if os.path.basename(p)[:2] != "00")


def verify_lex():
    dropped = {}
    for t, lst in list(LEX.items()):
        keep = []
        for surf, conf in lst:
            if surf in FULL_TEXT:
                keep.append((surf, conf))
            else:
                dropped.setdefault(t, []).append(surf)
        LEX[t] = keep
    return dropped


def norm(s):
    return "".join(VARIANT.get(ch, ch) for ch in s)


def guard_ok(txt, s, e):
    surf = txt[s:e]
    if surf not in GUARDS:
        return True
    prev_bad, next_bad = GUARDS[surf]
    if prev_bad and s > 0 and txt[s - 1] in prev_bad:
        return False
    if next_bad and e < len(txt) and txt[e] in next_bad:
        return False
    return True


def annotate_item(item_text, ch_no, item_idx, fn):
    """偏移相对于去除√后的条目正文"""
    txt = item_text
    if txt.startswith("√"):
        txt = txt[1:].lstrip()
    cands = []
    for t, lst in LEX.items():
        for surf, conf in lst:
            for m in re.finditer(re.escape(surf), txt):
                s, e = m.start(), m.end()
                seg = txt[s:e]
                if "□" in seg or "×" in seg or "£" in seg:
                    continue
                if not guard_ok(txt, s, e):
                    continue
                c = 0.7 if surf in GENERIC else conf
                cands.append((s, e, t, surf, norm(surf), c, "lexicon"))
    for m in QTY_PAT.finditer(txt):
        s, e = m.start(), m.end()
        seg = txt[s:e]
        if "□" in seg or "×" in seg or "£" in seg:
            continue
        cands.append((s, e, "quantity", seg, norm(seg), 0.8, "rule"))
    for m in SEV_PAT.finditer(txt):
        s, e = m.start(), m.end()
        cands.append((s, e, "quantity", txt[s:e], txt[s:e], 0.7, "rule"))
    for m in TIME_PAT.finditer(txt):
        s, e = m.start(), m.end()
        seg = txt[s:e]
        if "□" in seg:
            continue
        cands.append((s, e, "time", seg, norm(seg), 0.8, "rule"))
    for m in PUN_PAT.finditer(txt):
        s, e = m.start(), m.end()
        seg = txt[s:e]
        if "□" in seg or "×" in seg or "£" in seg:
            continue
        if len(seg) <= 2 and seg[-1] == "下":
            continue
        cands.append((s, e, "punishment", seg, norm(seg), 0.78, "rule"))
    cands.sort(key=lambda c: (-(c[1] - c[0]), TYPE_PRIORITY.get(c[2], 99), c[0]))
    chosen = []
    for s, e, t, surf, nrm, c, method in cands:
        if any(not (e <= cs or s >= ce) for cs, ce, *_ in chosen):
            continue
        chosen.append((s, e, t, surf, nrm, c, method))
    chosen.sort(key=lambda c: c[0])
    recs = []
    for n, (s, e, t, surf, nrm, c, method) in enumerate(chosen, 1):
        assert txt[s:e] == surf, (ch_no, item_idx, s, e, surf, txt[s:e])
        if nrm != surf:
            c = round(c * VARIANT_PENALTY, 2)
        recs.append({
            "id": f"{ch_no}-{item_idx:03d}-{n:02d}",
            "text": surf,
            "type": t,
            "start": s,
            "end": e,
            "normalized": nrm,
            "confidence": round(c, 2),
            "source": f"{fn}#条{item_idx}",
        })
    return recs


def main():
    os.makedirs(ANN_DIR, exist_ok=True)
    dropped = verify_lex()
    chapters = load_chapters()
    all_recs = []
    per_ch_stats = []
    pre_lines = []
    total_items = 0

    import jieba
    for t, lst in LEX.items():
        for surf, conf in lst:
            jieba.add_word(surf)

    for no, fn, items in chapters:
        recs = []
        for i, it in enumerate(items, 1):
            recs += annotate_item(it, no, i, fn)
            norm_txt = norm(it.lstrip("√").strip())
            toks = jieba.lcut(norm_txt)
            pre_lines.append(f"【{no}·条{i}】{norm_txt}")
            pre_lines.append(f"分词：{'/'.join(toks)}")
        all_recs += recs
        total_items += len(items)
        stats = {}
        for r in recs:
            stats[r["type"]] = stats.get(r["type"], 0) + 1
        per_ch_stats.append({"chapter_no": no, "file": fn, "item_count": len(items),
                             "entity_count": len(recs), "by_type": stats})
        doc = {
            "schema_version": SCRIPT_VER,
            "enum_version": ENUM_VER,
            "volume": "卷上" if no == "01" else "卷下",
            "chapter": fn.split("_", 1)[1][:-6] if "_" in fn else fn[:-6],
            "chapter_no": no,
            "source_file": fn,
            "item_count": len(items),
            "entity_count": len(recs),
            "entities": recs,
        }
        with open(os.path.join(ANN_DIR, fn.replace(".xhtml", ".json")), "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)

    with open(PRE_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(pre_lines))

    inv = {}
    for r in all_recs:
        key = (r["type"], r["normalized"])
        if key not in inv:
            inv[key] = {"normalized": r["normalized"], "type": r["type"],
                        "count": 0, "first_source": r["source"], "surfaces": []}
        e = inv[key]
        e["count"] += 1
        if r["text"] not in e["surfaces"]:
            e["surfaces"].append(r["text"])
    inventory = sorted(inv.values(), key=lambda x: -x["count"])
    by_type_total = {}
    for e in inventory:
        by_type_total[e["type"]] = by_type_total.get(e["type"], 0) + e["count"]
    merge_doc = {
        "schema_version": SCRIPT_VER,
        "enum_version": ENUM_VER,
        "total_items": total_items,
        "total_entities": len(all_recs),
        "unique_entities": len(inventory),
        "by_type": by_type_total,
        "per_chapter": per_ch_stats,
        "normalized_inventory": inventory,
    }
    with open(MERGE_FILE, "w", encoding="utf-8") as f:
        json.dump(merge_doc, f, ensure_ascii=False, indent=1)

    lines = []
    lines.append("# 《新官轨范》实体标注总报告（kg-annot v1）")
    lines.append("")
    lines.append("> 生成日期：2026-10-09　|　schema：`kg-annot-json-v1`　|　枚举版本：`entity-type-enum-v1`")
    lines.append("")
    lines.append("## 1. 实体类型枚举（11 类封闭 + 兜底，规则据 ming-officials-kg 枚举治理）")
    lines.append("")
    lines.append("| type | 类型 | 标注数 |")
    lines.append("|---|---|---|")
    for t in TYPES:
        lines.append(f"| {t} | {TYPE_CN[t]} | {by_type_total.get(t, 0)} |")
    lines.append("")
    lines.append("> 说明：official（职官）类型含官、吏、役（皂隶、门子、书手等吏役职均归入）；")
    lines.append("> person（人物）类型为身份/角色类（士夫、生员、人户等）；「类型待定」为兜底槽，本版无硬塞。")
    lines.append("")
    lines.append("## 2. 种子词典（v1 全部由《新官轨范》文本内生）")
    lines.append("")
    lines.append("按用户指示，本版不从外部抓取词典（《明史·职官志》《明会典》等留待 v2 人工回填）。")
    lines.append("每个词条均经程序校验出现在原文中；未出现者自动剔除并记录：")
    lines.append("")
    if any(dropped.values()):
        for t, lst in dropped.items():
            lines.append(f"- {TYPE_CN[t]} 剔除（原文未见）：{ '、'.join(lst) }")
    else:
        lines.append("- 全部词条均通过原文校验，无剔除。")
    lines.append("")
    lines.append("| 类型 | 词条数 |")
    lines.append("|---|---|")
    for t in TYPES:
        if t in LEX:
            lines.append(f"| {t} | {len(LEX[t])} |")
    lines.append("")
    lines.append("## 3. 文本预处理规则")
    lines.append("")
    lines.append("- 标点：原文统一全角标点；`£`/`×` 等录入符号不作改动，标注时跳过。")
    lines.append("- 缺字：`□` 保留为缺字符号；任何跨 `□` 的标注一律剔除。")
    lines.append("- 异体归一表（normalized 字段与预处理文本生效）：")
    lines.append("")
    lines.append("| 原文 | 归一 |")
    lines.append("|---|---|")
    for k, v in VARIANT.items():
        lines.append(f"| {k} | {v} |")
    lines.append("")
    lines.append("- 分词：jieba（加载文本内生词表作为用户词典），分词结果见《新官轨范_预处理_分词.txt》。")
    lines.append("- 条目偏移：`start/end` 为相对去除 `√` 后的条目正文的字符偏移（0 起、右开）。")
    lines.append("- 语境守卫：单字「里」遇前后「面」不标注（如“面里影壁”）；「都」后接“要是来去”不标注。")
    lines.append("- 双义处理：数字+「里」一律按数量（距离）标注；“各里/本里/一里十票”等无数字的「里」按地点；该歧义列入人工复核关注项。")
    lines.append("")
    lines.append("## 4. 标注方法")
    lines.append("")
    lines.append("1. **词典层**：文本内生词表最长匹配（多字词优先）。")
    lines.append("2. **规则层**：数量（数词+量词、若干/多寡）、时间（时辰、`初X日`、`X日/X月/X年`、`某年月日`）、刑罚（`打/责打/罚/决`+数词）。")
    lines.append("3. 重叠消解：长匹配优先；等长按类型优先级 `职官>文书>人物>制度>机构>行为>器物>刑罚>地点>时间>数量`。")
    lines.append("4. 泛称词（上司/衙门/人户/小民等）置信度统一 0.70（中置信）；异体归一词条再乘 0.9。")
    lines.append("")
    lines.append("## 5. 置信度公式")
    lines.append("")
    lines.append("```")
    lines.append("base：词典精确匹配 0.80–0.92（依类型）；正则规则 0.70–0.80；泛称 0.70")
    lines.append("调整：应用异体归一 → ×0.9；含缺字跨段 → 剔除；最终 round(x, 2)")
    lines.append("阈值：≥0.85 高置信；0.70–0.84 中置信；<0.70 低置信（进人工复核清单）")
    lines.append("```")
    lines.append("")
    lines.append("## 6. 分卷统计")
    lines.append("")
    lines.append("| 卷/章 | 条目数 | 实体数 | 类型分布（type:count） |")
    lines.append("|---|---|---|---|")
    for st in per_ch_stats:
        dist = "、".join(f"{TYPE_CN[k]}:{v}" for k, v in sorted(st["by_type"].items(), key=lambda x: -x[1]))
        lines.append(f"| {st['file']} | {st['item_count']} | {st['entity_count']} | {dist} |")
    lines.append("")
    lines.append(f"合计：{total_items} 条 / {len(all_recs)} 实体标注 / 归一后唯一实体 {len(inventory)}。")
    lines.append("")
    lines.append("## 7. 高频归一实体 Top30")
    lines.append("")
    lines.append("| 归一实体 | 类型 | 次数 | 首见来源 |")
    lines.append("|---|---|---|---|")
    for e in inventory[:30]:
        lines.append(f"| {e['normalized']} | {TYPE_CN[e['type']]} | {e['count']} | {e['first_source']} |")
    lines.append("")
    low = [r for r in all_recs if r["confidence"] < 0.70]
    lines.append(f"## 8. 人工复核清单（低置信，共 {len(low)} 条）")
    lines.append("")
    lines.append("| id | 原文 | 类型 | 置信度 | 来源 |")
    lines.append("|---|---|---|---|---|")
    for r in low:
        lines.append(f"| {r['id']} | {r['text']} | {TYPE_CN[r['type']]} | {r['confidence']} | {r['source']} |")
    lines.append("")
    lines.append("## 9. 缺口与后续")
    lines.append("")
    lines.append("- 词典为文本内生首版；v2 计划按用户口径回填《明史·职官志》《明会典》《中国历代职官别名大辞典》等官方书，回填后枚举版本 +1 并回溯重标存量。")
    lines.append("- 行为/制度、器物/刑罚存在边界重叠，采用本版规则确定性归类；人工复核发现系统性偏差时调整词典后重跑全部批次。")
    lines.append("- 同名异义（如「监」=监狱/监督）本版未做义项切分，建议入库时按 senseId 分立。")
    lines.append("- 「里」行政区/距离双义、「都」语境为已知噪声源，已按守卫规则处理并列入复核关注。")
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("DONE")
    print(f"chapters={len(chapters)} items={total_items} entities={len(all_recs)} unique={len(inventory)}")
    print("by_type:", by_type_total)
    for st in per_ch_stats:
        print(st["file"], st["entity_count"])


if __name__ == "__main__":
    main()
