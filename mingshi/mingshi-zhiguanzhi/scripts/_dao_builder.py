# -*- coding: utf-8 -*-
"""道制节点构建器（v12）—— 原文卷04 条37–41 的 200+ 道名 → ORG 子节点。

原文形态（决定性）：
    布政司参政、参议分司诸道。督粮道，(十三布政司各一员，俱驻省城。)督册道，…
    分守道：浙江杭嘉湖道，宁绍台道，金衢严道，温处道。(俱驻省)江西南瑞道，(驻省)…
    按察司副使、佥事分司诸道。提督学道，清军道，驿传道，…
    分巡道：浙江杭严道，宁绍道，嘉湖道，金衢道。江西饶南九江道，(驻饶州)…
    整饬兵备道：浙江宁绍道，嘉兴道，温处道，台海道。…
    其外又有协堂道，(副使，河南、浙江间设。)水利道，(浙江)…其北直隶之道寄衔于山东者，
    则为密云道，大名道，天津道，霸州道；寄衔于山西者，则为易州道，…

解析要点（实测校准）：
  1. **省份切分**：段内以省名起头（浙江/江西/山东/山西/陕西/河南/湖广/福建/广东/
     四川/广西/贵州/云南），作省前缀继承，直到下一个省名出现。
     实测省名出现数：条37=17 / 条39=14 / 条40=13。
  2. **驻点括注紧跟道名**：`<道名>，(驻X)` —— 括注只修饰其前的道名。
     `(俱驻省)` 修饰**本句之前**的全部道名（实测：「浙江杭嘉湖道，宁绍台道，
     金衢严道，温处道。(俱驻省)」四道俱驻省）。
  3. **「寄衔」组**：`其北直隶之道寄衔于山东者，则为密云道，…；寄衔于山西者，…`
     形态是「则为」后列道名，寄衔对象写在前面。寄衔道本身无驻地。
  4. **组标题词剔除**：分守道/分巡道/整饬兵备道/提督学道 等是组名不是道名。

落盘：作为 `道` 节点（ORG-2031）的 children[] + 同步 LINE 边 + 驻点视图。
"""

import re

import _common as C
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C
import _kg_enums as E

# ---------- 原文常量 ----------
DAO_ITEM_GROUPS = {
    "04-037": "分守道",
    "04-038": "专职道",
    "04-039": "分巡道",
    "04-040": "兵备道",
    "04-041": "其他道",
}

PROVS = ["浙江", "江西", "山东", "山西", "陕西", "河南", "湖广", "福建",
         "广东", "四川", "广西", "贵州", "云南", "北平", "北直隶", "南直隶"]

# 组标题词（**只含以「：」引出清单的组名**，它们本身不是道）
GROUP_WORDS = {
    "分守道", "分巡道", "整饬兵备道",
}

# 段首引导句（不是道名，须整句剔除）
HEAD_SENTENCES = [
    "布政司参政、参议分司诸道",
    "按察司副使、佥事分司诸道",
]

# 专职道（条38 三条 + 条37 首两条）—— 十三布政司俱各一员，非省属
# 注意：这些是**真实道名**，不可放进 GROUP_WORDS
ZHIZHUAN = ["督粮道", "督册道", "提督学道", "清军道", "驿传道"]

# 其他道（条41 前半，独立成道，多为一省专设）
QITA = ["协堂道", "水利道", "屯田道", "管河道", "盐法道", "抚治道",
        "监军道", "招练道"]

# 裸写为「X道」但实为**设置说明/官职称谓**的噪声词（长度过滤器 + 白名单双保险）
NOISE_WORDS = {
    "守巡道", "兵巡道", "道", "分司诸道", "诸道", "其道", "之道",
    "道者", "兵道",
}


def _is_dao_name(s):
    """判定是否为真实道名"""
    return (s.endswith("道") and 2 <= len(s) < 14
            and s not in GROUP_WORDS and s not in NOISE_WORDS)


# 寄衔道（条41 末）—— 南北直隶之道寄衔于邻省
JIXIAN = {
    "山东": ["密云道", "大名道", "天津道", "霸州道"],
    "山西": ["易州道", "口北道", "昌平道", "井陉道", "蓟州道", "永平等道"],
    "南直隶—山东": ["太仓道", "颍州道", "徐州道"],
    "南直隶—浙江江西湖广": ["苏松道", "漕储道", "常镇道", "庐凤道",
                             "徽宁池太道", "淮扬道"],
}

# 驻点括注形态判定
STATION_RE = re.compile(r"[（(]([^）)]{1,32})[）)]")


def _station_form(body):
    """括注文本 → (form, station_text)"""
    b = body.strip()
    if b.startswith("俱驻"):
        return "prov", b[2:]
    if b.startswith("或驻"):
        return "multi", b[2:]
    if b.startswith("驻"):
        rest = b[1:]
        if rest in ("省", "省城"):
            return "prov", rest
        return "exact", rest
    if b.startswith("移"):
        return "move", b[1:]
    return None, None


def parse_dao_section(text, group):
    """解析一个条目里的道名与其驻地。

    返回 [{name, province, group, station, station_form, evidence}]
    """
    if group == "专职道":
        return _parse_zhizhuan(text)
    if group == "其他道":
        out = _parse_qita(text)
        out.extend(_parse_jixian(text))
        return out
    return _parse_plain(text, group)


def _parse_plain(text, group):
    """常规段：省名切分 + 道名 + 紧跟括注。

    算法（实测校准）：
      0. 先摘出段首「专职诸道」（督粮道 / 督册道 —— 十三布政司各一员，非省属）；
      1. 把括注替换为占位符 \\x00N\\x00，按 [，,。；;：:] 切 token 串；
      2. 逐个 token 判定：是省名（含省名+道名）→ 记 cur_prov 并可能出 1 道名；
         是道名（以「道」结尾、非组名、长度合理）→ 入 pending（**连同伴随省名入队**）；
         是占位符 → 判定驻点形态：
            (俱驻X)  回填**本句内**（自分隔符后）所有 pending
            (驻X)    只回填 pending 最后一个
      3. 每遇句末分隔符结算 pending 为「无驻点」。
    """
    out = []
    holds = []

    def _hold(m):
        holds.append(m.group(1))
        return "\x00%d\x00" % (len(holds) - 1)

    masked = STATION_RE.sub(_hold, text)

    # 剔除段首引导句
    for h in HEAD_SENTENCES:
        masked = masked.replace(h, "")

    # 段首专职诸道（督粮道/督册道）：十三布政司各一员，省属=多省
    for nm in ("督粮道", "督册道"):
        # 形如「督粮道，(十三布政司各一员，俱驻省城。)」
        mm = re.search(re.escape(nm) + r"[，,]?", masked)
        if mm:
            out.append({"name": nm, "province": "多省", "group": group,
                        "station": "省城", "station_form": "prov",
                        "note": "十三布政司各一员", "evidence": nm})
            masked = masked[:mm.start()] + "\x01" * len(nm) + masked[mm.end():]

    cur_prov = None
    sent_pending = []      # [(道名, evidence, 入队时省名)]

    def _emit(name, station, form, ev, prov=None):
        """prov=None 时取当前 cur_prov（调用点须保证时效性）"""
        out.append({"name": name, "province": prov if prov is not None else cur_prov,
                    "group": group, "station": station,
                    "station_form": form, "evidence": ev})

    def _flush_sentence():
        """本句结束：把仍待定的道名按「无驻点」结算（用各自入队时的省名）"""
        for nm, ev, pv in sent_pending:
            _emit(nm, None, "none", ev, prov=pv)
        sent_pending.clear()

    token = re.compile(r"\x00(\d+)\x00|([，,。；;：:])")
    pos = 0

    def _consume_chunk(chunk):
        nonlocal cur_prov
        # 可能形如「浙江杭嘉湖道」或纯省名「浙江」或道名
        p = _match_prov(chunk)
        if p:
            rest = chunk[len(p):]
            # 例：「浙江」→ 只切省；「浙江杭嘉湖道」→ 省 + 道名
            # 例：「河南道，(驻河南)」→「河南」既是省名又是道名，此时整串作道名
            if not rest:
                cur_prov = p
                return
            if _is_dao_name(rest):
                cur_prov = p
                sent_pending.append((rest, chunk, p))
                return
            # 「福建兵备道」：rest 是组名（兵备道）—— 视为该省的通名道，整串作名
            if rest in GROUP_WORDS:
                cur_prov = p
                sent_pending.append((rest, chunk, p))
                return
            # 「河南道」：省名 == 道名前缀，整串是道名
            if _is_dao_name(chunk):
                sent_pending.append((chunk, chunk, cur_prov))
                return
            cur_prov = p
            return
        if _is_dao_name(chunk):
            sent_pending.append((chunk, chunk, cur_prov))

    for m in token.finditer(masked):
        chunk = masked[pos:m.start()].strip()
        pos = m.end()

        if chunk:
            _consume_chunk(chunk)
            continue

        if m.group(1) is not None:
            # 括注
            body = holds[int(m.group(1))]
            form, station = _station_form(body)
            if station is None:
                continue
            if body.strip().startswith("俱驻"):
                # 回填本句内全部 pending
                for nm, ev, pv in sent_pending:
                    _emit(nm, station, form, ev, prov=pv)
                sent_pending.clear()
            else:
                # 只回填最后一个
                if sent_pending:
                    nm, ev, pv = sent_pending.pop()
                    _emit(nm, station, form, ev, prov=pv)
                elif out:
                    # 括注紧跟在上一个已结算道名之后
                    prev = out[-1]
                    prev["station"] = station
                    prev["station_form"] = form
            continue

        # 分隔符
        if m.group(2) in ("。", "；", ";"):
            _flush_sentence()
        # 逗号/分号不结算（(俱驻X) 覆盖范围是整句）

    _flush_sentence()
    return out


def _match_prov(s):
    for p in PROVS:
        if s.startswith(p):
            return p
    return None


def _strip_prov(nm):
    p = _match_prov(nm)
    if p and len(nm) > len(p):
        return nm[len(p):]
    return nm


def _parse_jixian(text):
    """寄衔段（条41 后半）。两种句式：

      北直隶：其北直隶之道寄衔于山东者，则为密云道，大名道，…；
              寄衔于山西者，则为易州道，…，蓟州、永平等道。
      南直隶：南直隶之道寄衔于山东者，太仓道，颍州道，徐州道；
              寄衔浙江、江西、湖广者，苏松道，…
    """
    out = []
    seen = set()
    idx_bj = text.find("其北直隶之道")
    idx_nj = text.find("南直隶之道")
    segs = []
    if idx_bj >= 0 and idx_nj > idx_bj:
        segs.append(("北直隶", text[idx_bj:idx_nj]))
        segs.append(("南直隶", text[idx_nj:]))
    elif idx_nj >= 0:
        segs.append(("南直隶", text[idx_nj:]))

    for region, seg in segs:
        # 「寄衔(X)者，[则]为(Y)」；南直隶省略「则为」
        for m in re.finditer(
                r"寄衔([^，,。；;]{1,20}?)者[，,]?则?为?([^；;。]+)", seg):
            host = m.group(1).strip()
            body = m.group(2)
            # 顿号并列体：「蓟州、永平等道」→ 前项补足「道」后缀
            body = re.sub(r"([\u4e00-\u9fa5]{2,6})、([\u4e00-\u9fa5]{2,6}道)",
                          lambda x: x.group(1) + "道，" + x.group(2), body)
            for nm in re.split(r"[，,、]", body):
                nm = nm.strip()
                if _is_dao_name(nm) and nm not in seen:
                    seen.add(nm)
                    out.append({"name": nm, "province": region,
                                "group": "寄衔道", "station": None,
                                "station_form": "none",
                                "jixian_to": host,
                                "evidence": "寄衔于%s" % host})
    return out


def _parse_qita(text):
    """其他道（条41 前半）：三种括注形态混合，须分别处理。

      A `协堂道，(副使，河南、浙江间设。)`  → 括注=设置说明，非驻点
      B `水利道，(浙江)`                    → 同上（省份）
      C `抚治道，(陕西抚治商洛道，湖广又有抚民、抚苗道。)` → 括注内**另含道名**
    """
    head = text.split("其北直隶之道", 1)[0]
    head = head.replace("其外又有", "")
    out = []
    seen = set()

    # 逐「道名 + 可选括注」抓取
    pat = re.compile(r"([\u4e00-\u9fa5]{2,12}道)[，,]?[（(]([^）)]{0,60})[）)]")
    for m in pat.finditer(head):
        nm, note = m.group(1), m.group(2)
        if nm in GROUP_WORDS or nm in seen:
            continue
        seen.add(nm)
        out.append({"name": nm, "province": None, "group": "其他道",
                    "station": None, "station_form": "none",
                    "note": note, "evidence": m.group(0)})
        # 形态 C：括注内另含道名（抚治商洛道 / 抚民道 / 抚苗道）
        for sub in re.finditer(r"([\u4e00-\u9fa5]{2,12}道)", note):
            s = sub.group(1)
            if _is_dao_name(s) and s not in seen:
                seen.add(s)
                out.append({"name": s, "province": None, "group": "其他道",
                            "station": None, "station_form": "none",
                            "note": "见括注：%s" % note, "evidence": note})

    # 段内无括注的裸道名（盐法道 等），以「道」后接分隔符为界
    for m in re.finditer(r"([\u4e00-\u9fa5]{2,12}道)(?=[，,。；;）)]|$)", head):
        nm = m.group(1)
        if nm in GROUP_WORDS or nm in seen:
            continue
        seen.add(nm)
        out.append({"name": nm, "province": None, "group": "其他道",
                    "station": None, "station_form": "none", "evidence": nm})
    return out


def _parse_zhizhuan(text):
    """专职道（条38）：按察司副使、佥事分司诸道。提督学道，清军道，驿传道，(...)"""
    # 先删全部括注（设置说明，非驻点）
    head = re.sub(r"[（(][^）)]*[）)]", "", text)
    head = head.replace("按察司副使、佥事分司诸道。", "")
    head = head.replace("按察司副使、佥事分司诸道", "")
    out = []
    for nm in re.split(r"[，,。]", head):
        nm = nm.strip()
        if _is_dao_name(nm):
            out.append({"name": nm, "province": None, "group": "专职道",
                        "station": None, "station_form": "none",
                        "evidence": nm})
    return out


def build(vols, errs):
    """由 `_dao_builder` 解析出的 206 条道记录生成结构化增量。

    输出（dict）：
      dao_nodes    道子节点列表（挂到 ORG-2031 children[]，level="道"）
      dao_lines    LINE 边（道 → 道 汇总节点，跨树边）
      dao_stations 驻点表（供 `_views/dao_stations.json`）
      dao_parent   汇总节点 id
    """
    import json
    import os

    if "04" not in ([str(v) for v in vols] or ["04"]):
        return {"dao_nodes": [], "dao_lines": [], "dao_stations": [],
                "dao_parent": None}

    reg = C.load_registry()
    parent_id = "ORG-2031"          # 卷04 条37 的「道」汇总节点

    rows = []
    for iid, group in DAO_ITEM_GROUPS.items():
        if iid not in reg:
            errs.append("道制：条目 %s 不在注册表" % iid)
            continue
        rows.extend(parse_dao_section(reg[iid]["original"], group))

    # 唯一键：道名 + 组 + 省（同名可跨组/跨省，属真实重复）
    seen = set()
    nodes = []
    n = 0
    for r in rows:
        key = (r["name"], r["group"], r.get("province"))
        if key in seen:
            continue
        seen.add(key)
        n += 1
        node = {
            "id": "%s#%d" % (parent_id, n),
            "name": r["name"],
            "level": "道",
            "parent": "道",
            "dao_group": r["group"],
            "province": r.get("province"),
            "station": r.get("station"),
            "station_form": r.get("station_form", "none"),
            "is_concurrent": False,
            "note": r.get("note") or "",
            "evidence": r.get("evidence", ""),
            "item_id": None,
            "children": [],
        }
        if r.get("jixian_to"):
            node["jixian_to"] = r["jixian_to"]
        nodes.append(node)

    # 驻点表（只含有明确驻点者）
    stations = [{"dao": x["name"], "group": x["dao_group"],
                 "province": x["province"], "station": x["station"],
                 "station_form": x["station_form"], "id": x["id"]}
                for x in nodes if x["station"]]

    # LINE 边：每条道 → 道汇总节点（**跨树边**）
    # 依据 pitfall #44：道节点挂在汇总节点「道」之下，但 LINE 边的 superior
    # 记「道」会造成 (道, 道) 自重边，与树内边口径不符。
    # 处置：树内 parent 置「道」（承载 children 结构），LINE 边记 superior="天子"
    #   以示跨树，并在 note 中保留真实归属；`cross_tree=True` 供校验器识别。
    lines = []
    for i, x in enumerate(nodes, 1):
        lines.append({
            "slot": 200 + i,
            "item_id": "04-037",
            "subordinate": x["name"],
            "superior": "天子",
            "line_type": "分隶",
            "level_gap": 1,
            "note": "道制驻点：%s（隶道统）" % (x["station"] or "无载"),
            "ent_ids": [],
            "confidence": 0.9,
            "_vol": "04",
            "cross_tree": True,
        })

    return {"dao_nodes": nodes, "dao_lines": lines,
            "dao_stations": stations, "dao_parent": parent_id,
            "dao_summary": "道制：解析 %d 条记录 → %d 节点"
                           % (len(rows), len(nodes))}
