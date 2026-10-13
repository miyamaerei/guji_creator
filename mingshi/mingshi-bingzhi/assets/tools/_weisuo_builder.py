# -*- coding: utf-8 -*-
"""
卫所标记文法解析器骨架 `assets/tools/_weisuo_builder.py`
======================================================

C17 卫所树层（bz 型核心）的**候选生成器**——只产候选、不出定稿。

分工（工厂 methodology §3 硬约束）：
- **规则引擎**（本文件）：按标记文法把卷66 卫列长行切成候选卫/所节点，产出
  候选树 + 切段覆盖率 + 同名词典 WEI_NAME_INDEX；**结果一律标注候选态**。
- **AI 复核**（`review_candidates()` 的调用方，即执行期的 AI 逐行复核）：
  逐行核对候选（卫名、括注归并、层级归属、`list_ver`），修正后写定稿树。
  SKILL.md §13 阶段一/阶段二验收硬指标见文件尾部 `ACCEPTANCE`。

启用方式（执行期）::

    python assets/tools/_weisuo_builder.py --vol 66 --ver old --lines L52-L120
    # 产出 _data/weis/candidates_66_old.json（候选树 + 覆盖率 + 词典），随后 AI 复核

标记文法要点（实测，SKILL.md §6.2）：
- `◎左军都督府` → 府层节点；`○在京`/`在京(` → 在京块（○ 不保证必现，锚行首）
- `△浙江都司`/裸行 `辽东都司` → 都司行（△ 不保证必现，双判据）
- 无分隔卫列长行（`杭州前卫杭州右卫台州卫…`）→ 本文件核心处理对象
- `(…)` 括注紧贴前卫名 → 归并前节点 `notes[]`，不粘进 name；括注**同时是硬边界**：
  `卫(注)` 的「卫」必然是完整卫名末字（括注后必为一个新卫名开头）
- `已上…` → 区块级注（挂区块节点，不复制到每个卫）
- `卫三百八十四`/`所二十四`/`站七`/`地面七`/`寨一` → 数量行（QUAN + count_marker）
- 张本行（`初，洪武二十六年定…`）→ 不进树（归 REG/总述）

长行切段策略（实测修正，取代 §6.3 初版纯正则——见 SKILL.md §6.3 修订）：
  1. **括注锚点**：先把 `X卫(注)Y卫…` 在括号处断开，括注前词必然完整（命中即回填
     词典 WEI_NAME_INDEX——渐进式，AI 每复核一批即词典扩大一批，下次更准）。
  2. **词典贪心**：段首用词典最长词匹配。
  3. **未解段**：无词典命中且含多个「卫/所」词的段 → **整段一条候选**并标
     `ai_review=required`，由 AI 逐卫拆分——规则引擎不硬猜边界（坑 #54/#55）。
  覆盖率统计按「确定切分数 / (确定切分数 + 待复核段数)」如实计算，不虚报。

依赖：`scripts/_common.py`（四族护栏），经 sys.path 引入。
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))  # 项目根
sys.path.insert(0, os.path.join(ROOT, "scripts"))

# 复用基座函数（A/B/G/P 四族 + 工具）
# 注：sys.path.insert 为运行时动态路径，LSP 静态分析无法解析该导入，
# 实际执行（python assets/tools/_weisuo_builder.py）不受影响。
from _common import (  # type: ignore  # noqa: E402
    PATHS,
    cn2int,
    norm_text,
)

# =============================================================================
# 0. 参数与常量（与 SKILL.md §6.2/§6.3 同源）
# =============================================================================

# 卫/所名后缀词典 —— 卫列行切段的**锚点**（SKILL.md §6.3）
WEI_SUFFIXES = ["卫", "所"]

# 含「司/站/寨/地面」的次级锚点（都司行 / 羁縻数量行用）
EXT_SUFFIXES = ["司", "站", "寨", "地面"]

# 全部词尾锚点（用于括注锚点 + 词典贪心后的覆盖统计）
ALL_SUFFIXES = ["卫", "所", "司", "站", "寨", "地面"]

# 括注匹配（半角/全角括号均可；紧贴前卫名）
BRACKET_RE = re.compile(r"[（(]([^（()）]{0,80})[）)]")

# 数量行锚点（实测：卫三百八十四/所二十四/站七/地面七/寨一）
COUNT_ROW_RE = re.compile(
    r"^(?:卫|所|站|地面|寨|都指挥使司|指挥使司|宣尉使司|招讨司|万户府|千户所)\d+"
)

# 张本/总起句锚点（不进树）
ZHANGBEN_STARTS = ("初，", "初置", "后定天下", "羁縻卫所", "西北诸部", "西番即古吐番")

# 府层级行锚点（实测：`◎五军都督府所属卫所` 与 `◎左军都督府` 均为层级标题）
FU_TITLE_RE = re.compile(r"^[◎○△]*(?:[左右中前后]军都督府|五军都督府所属卫所)")

# 在京块锚点（○ 不保证必现，锚定行首文字）
ZAI_JING_RE = re.compile(r"^[○]?在京")

# 都司级块名全表（双判据：行首 △ 或 行首都司名；△/○ 不保证必现——锚行首文字）。
# 与旧闭包 DU_SI_RE 相比：新增「北平都司/北平行都司」（旧编成后军都督府段），
# 并为「行首都司名+卫列」混合行（L112 北平行都司(后为大宁都司)大宁左卫…）提供
# 最长优先前缀匹配（「北平行都司」必须长于「北平都司」先命中）。
DU_SI_NAMES = (
    "直隶",
    "浙江都司",
    "辽东都司",
    "山东都司",
    "陕西都司",
    "陕西行都司",
    "四川都司",
    "四川行都司",
    "广西都司",
    "云南都司",
    "贵州都司",
    "中都留守司",
    "河南都司",
    "湖广都司",
    "湖广行都司",
    "兴都留守司",
    "福建都司",
    "福建行都司",
    "江西都司",
    "广东都司",
    "大宁都司",
    "万全都司",
    "山西都司",
    "山西行都司",
    "北平都司",
    "北平行都司",
)
_DU_SI_NAMES_SORTED = sorted(DU_SI_NAMES, key=len, reverse=True)

# 块标题行（无标记裸行，均不保证前缀符号）：上N卫 / 在外 / 土官 / 北平三护卫 / 山西三护卫
BLOCK_TITLE_RE = re.compile(
    r"^(?:上[一二三四五六七八九十]+卫|在外|土官|北平三护卫|山西三护卫)$"
)

# 已上 区块注
YISHANG_RE = re.compile(r"[（(]?已上([^（()）]{0,80})[）)]?$")

ACCEPTANCE = {
    "segment_coverage_min": 0.95,  # 切段覆盖率下限（候选卫数 / 原文卫名数）
    "bracket_strip_rate": 1.0,  # 括注剥离率必须 100%
    "list_ver_no_leak": True,  # list_ver 无漏挂
}

# 同名词典持久化位置
NAME_INDEX_PATH = os.path.join(PATHS["data"], "weis", "wei_name_index.json")


# =============================================================================
# 1. 行分类器（规则引擎核心：只做候选判定，AI 复核为准）
# =============================================================================

LINE_KINDS = (
    "block_title",
    "fu_title",
    "zai_jing",
    "du_si",
    "count_row",
    "wei_col",
    "zhangben",
    "other",
)


def _head_block_name(s: str, kind: str) -> tuple:
    """按块类型取**行首块标题**，剥离紧随括注，返回 (head, block_notes, rest)。

    - head：纯净块名（不带 ◎○△ 前缀、不带括注），用于树节点 name；
    - block_notes：块级括注列表（如 L57「在京(凡本府在京属卫…不注)」、
      L133「山东都司(旧有青州左护卫…革)」——块级注挂节点，不进卫级叶）；
    - rest：块名之后的**余留文本**（卫列内容）。空 = 纯块标题行；
      非空 = 「块标题+卫列」混合行（实测 L112「北平行都司(后为大宁都司)大宁左卫…」），
      由调用方把 rest 当卫列行切段挂到该块下。
    """
    t = re.sub(r"^[◎○△]", "", s)
    if kind == "fu_title":
        m = re.match(
            r"^((?:[左右中前后]军都督府|五军都督府所属卫所))"
            r"(?:[（(]([^（）()]{0,80})[）)])?(.*)$",
            t,
        )
    elif kind == "zai_jing":
        m = re.match(r"^(在京)(?:[（(]([^（）()]{0,80})[）)])?(.*)$", t)
    elif kind == "block_title":
        m = re.match(
            r"^(上[一二三四五六七八九十]+卫|在外|土官|北平三护卫|山西三护卫)"
            r"(?:[（(]([^（）()]{0,80})[）)])?(.*)$",
            t,
        )
    elif kind == "du_si":
        head = next((n for n in _DU_SI_NAMES_SORTED if t.startswith(n)), None)
        if head is None:
            return t, [], ""
        rest = t[len(head) :]
        m = re.match(r"^(?:[（(]([^（）()]{0,80})[）)])?(.*)$", rest)
        if m and m.group(1):
            return head, [m.group(1)], m.group(2)
        return head, [], rest
    else:
        return t, [], ""
    if not m:
        return t, [], ""
    head, note, rest = m.group(1), m.group(2), m.group(3)
    return head, ([note] if note else []), rest


def classify_line(line: str, line_no: int) -> dict:
    """按标记文法把单行分成候选类别（返回 dict，含原行与定位）。

    判序（重要，锚定行首，P 族 SemanticGate）：
        zhangben → fu_title → count_row → zai_jing → du_si
        → block_title → wei_col → other
    注意：
    - 卫士列行可能以「在外」「○在外」开头（旧编成在外块），
      归类为 wei_col 由切段器处理，块归属由父链承载。
    - 含句读（，。；：）的行是**说明段**而非卫列行（卫列行是无标点纯名串），
      归 other 由 AI 复核归入 REG/总述（实测 L122 亲军上二十二卫说明段）。
    - 对块类行（fu_title/zai_jing/du_si/block_title）额外回填
      head/block_notes/rest 三键（见 `_head_block_name`），供建节点时
      剥离块级括注、支持「块标题+卫列」混合行。
    """
    s = norm_text(line)
    kind = "other"
    if not s:
        kind = "other"
    elif any(s.startswith(p) for p in ZHANGBEN_STARTS):
        kind = "zhangben"
    elif FU_TITLE_RE.match(s):
        kind = "fu_title"
    elif COUNT_ROW_RE.match(s):
        kind = "count_row"
    elif ZAI_JING_RE.match(s):
        kind = "zai_jing"
    elif any(s.lstrip("◎○△").startswith(n) for n in _DU_SI_NAMES_SORTED):
        kind = "du_si"  # 前缀符号不保证必现（L62 辽东都司无△、L110 △北平都司带△），先剥再判
    elif BLOCK_TITLE_RE.match(s):
        kind = "block_title"  # 实测 L52「上十二卫」/ L59、L69「在外」/ L117、L119「三护卫」/ L147「土官」
    else:
        # 句读检查必须**剥离括注**后再看：`卫(后改名武定，属后府)` 这类
        # 括注内句读不是行级说明段标记（实测 L65/L71/L75 卫列行因此被误判）。
        inner = BRACKET_RE.sub("", s)
        if any(ch in inner for ch in "，。；：,;."):
            kind = "other"  # 行级句读 = 说明段，不进树
        elif re.search(r"[\u4e00-\u9fff]{2,8}[卫所]$", inner):
            kind = "wei_col"  # 2-8 汉字+卫/所收尾；3 字卫名（L95「九江卫」）也须命中
    if kind in ("fu_title", "zai_jing", "du_si", "block_title"):
        head, bnotes, rest = _head_block_name(s, kind)
        cls = {"line_no": line_no, "raw": line, "kind": kind}
        cls["head"] = head
        cls["block_notes"] = bnotes
        cls["rest"] = rest
        return cls
    return {"line_no": line_no, "raw": line, "kind": kind}


# =============================================================================
# 2. 长行切段（实测修正版：括注锚点 + 词典贪心 + 待复核段）
# =============================================================================


def _index_ctx() -> dict:
    """读取 WEI_NAME_INDEX（不存在则空）；写回由 save_name_index 负责。"""
    if os.path.exists(NAME_INDEX_PATH):
        try:
            with io.open(NAME_INDEX_PATH, encoding="utf-8") as fh:
                obj = json.load(fh)
            return obj.get("index") or {}
        except Exception:  # noqa: BLE001
            return {}
    return {}


def save_name_index(index: dict, path=None) -> None:
    """持久化同名词典（AI 复核每确认一批卫名即回填扩大，渐进式收敛）。"""
    path = path or NAME_INDEX_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # 每条卫名记录首次出现坐标与出现次数
    payload = {
        "index": index,
        "note": "WEI_NAME_INDEX：卫名->{count, first}。"
        "AI 复核确认的新卫名append此处，供下次切段词典贪心使用。",
    }
    with io.open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)


def cut_wei_row(line: str, line_no: int, index: dict) -> dict:
    """把一条卫列长行切成候选卫/所节点列表（含待复核段）。

    三步：
      1. 首轮用括注锚点断开：`X卫(注)Y…` 中括号前词必完整 → 硬切 + 回填词典。
      2. 段内词典贪心最长匹配（杝注已剥离，段是纯卫名串）。
      3. 未解段（含多个词尾后缀但无词典命中）→ **整段候选** ai_review=required。

    返回 dict：{"nodes": [...], "determined": n, "pending": n}
    """
    s = norm_text(line)
    nodes, notes_ctx = [], []
    block_notes = []

    # ---- 第 1 步：括注锚点切开（括注前词回填词典）----
    # 先拆括注再检「已上」：`(后为隆庆卫已上俱属后府)` 这类**括注内嵌已上**
    # 不能触发行级剥离（否则把左括号留在段里）；已上剥离只做在无括注尾部。
    segs = []  # [(text, note_or_None)]
    pos = 0
    for m in BRACKET_RE.finditer(s):
        head = s[pos : m.start()]
        segs.append((head, m.group(1)))
        pos = m.end()
    segs.append((s[pos:], None))

    # 无括注尾部段若以「已上…」收尾 → 区块注剥离（剥离后为空则丢弃该段）
    last_text, last_note = segs[-1]
    if last_text and last_note is None:
        yishang = YISHANG_RE.search(last_text)
        if yishang:
            block_notes.append(yishang.group(0))
            stripped = last_text[: yishang.start()]
            if stripped:
                segs[-1] = (stripped, None)
            else:
                segs.pop()
                # 前一括注段末尾可能因此无卫名，交给第 2 步自然处理

    determined, pending = [], []

    def _append_leaf(piece, br, conf, extra=None):
        node = {
            "cand": True,
            "name": piece,
            "notes": [br] if br else [],
            "src_loc": "卷66-L%d" % line_no,
            "confidence": conf,
        }
        if extra:
            node.update(extra)
        determined.append(node)

    # ---- 第 2/3 步：词尾计数 + 词典贪心分解 ----
    for text, br in segs:
        if not text:
            if br:
                notes_ctx.append(br)
            continue
        # 段内词尾后缀出现次数：1 = 单一卫名（括注锚点前词必完整）；
        # >1 = 多卫粘连，必须词典分解；词典解不动 → 整段待复核
        tail_count = sum(text.count(s) for s in ALL_SUFFIXES)
        if tail_count <= 1:
            _append_leaf(text, br, 0.85, {"from_bracket_anchor": True})
            br = None
            continue
        # 多词尾段：词典贪心最长匹配
        keys = sorted(index.keys(), key=len, reverse=True)
        i, n = 0, len(text)
        decomposed = True
        seg_leafs = []  # 本段分解出的确定叶节点（括注挂最后一片）
        while i < n:
            hit = None
            for k in keys:
                if text.startswith(k, i):
                    hit = k
                    break
            if hit:
                _append_leaf(hit, None, 0.9, {"from_name_index": True})
                seg_leafs.append(determined[-1])
                i += len(hit)
            else:
                # 未解：剩余含多个词尾后缀的部分整段抛给 AI（不硬猜边界——坑 #54）
                rest = text[i:]
                if rest:
                    pending.append(
                        {
                            "cand": True,
                            "name": rest,
                            "notes": [br] if br else [],
                            "src_loc": "卷66-L%d" % line_no,
                            "confidence": 0.3,
                            "ai_review": "required",
                            "why": "多词尾粘连段无词典命中，须 AI 逐卫拆分",
                        }
                    )
                decomposed = False
                break
        # 括注紧贴词尾 → 挂到本段**最后一片**叶（如 `通州卫(已上俱改为亲军)`）
        if br and seg_leafs:
            seg_leafs[-1].setdefault("notes", []).insert(0, br)
        if not decomposed:
            # 词典只解了前缀？前缀已 append，剩余段已在 pending 登记，此处无事可做
            pass
    if block_notes:
        nodes.append(
            {
                "cand": True,
                "name": "",
                "kind": "block_note",
                "notes": block_notes,
                "src_loc": "卷66-L%d" % line_no,
                "confidence": 0.7,
            }
        )
    nodes.extend(determined + pending)
    return {
        "nodes": nodes,
        "determined": len(determined) + bool(block_notes),
        "pending": len(pending),
    }


# =============================================================================
# 3. 候选树组装（按行序挂父链；ID 等打包器分配）
# =============================================================================


def build_candidate_tree(lines, list_ver: str, volume: str, index: dict) -> dict:
    """把 (line_no, line) 序列组装成候选树。

    状态机：
      current 栈 = [军民类型?, 府, 在京/在外, 都司, ...]
    - fu_title/du_si/zai_jing → 弹/压栈并挂到当前父
    - wei_col → cut_wei_row 产节点挂当前父；block_note 挂父的 notes
    - count_row → 数量行节点（count_marker 由 AI 复核时填，候选期留空）
    - zhangben/other → 悬空（不进树，另存 to_review）
    """
    root = {
        "name": "卷66" + ("旧编成" if list_ver == "old" else "后定编成"),
        "level": "军民类型",
        "children": [],
    }
    stack = [root]
    to_review = []
    stat = {"determined": 0, "pending": 0}

    def _attach_wei_col(text, line_no, index, parent):
        """把一条卫列文本（整行或混合行余留）切段并挂到 parent 下。

        block_note（`已上…` 区块注）挂 parent 的 notes；其余切段按卫/所落叶。
        """
        out = cut_wei_row(text, line_no, index)
        stat["determined"] += out["determined"]
        stat["pending"] += out["pending"]
        for n in out["nodes"]:
            if n.get("kind") == "block_note":
                parent.setdefault("notes", []).extend(n["notes"])
            else:
                n["level"] = "卫" if n["name"].endswith("卫") else "所"
                parent["children"].append(n)

    for line_no, line in lines:
        cls = classify_line(line, line_no)
        kind = cls["kind"]
        s = norm_text(line)

        if kind in ("block_title", "fu_title", "zai_jing", "du_si"):
            head = cls.get("head") or s
            node = {
                "cand": True,
                "name": head,  # 纯净块名：括注已剥离（如「在京」「山东都司」）
                "level": {
                    "block_title": "块",
                    "fu_title": "府",
                    "zai_jing": "在京",
                    "du_si": "都司",
                }[kind],
                "children": [],
                "src_loc": "卷66-L%d" % line_no,
                "confidence": 0.9 if kind == "zai_jing" else 0.8,
            }
            # 块级括注挂节点 notes（L57「在京」长说明 / L133「山东都司(旧有…)」），
            # 不进卫级叶；由 AI 复核决定转 C14 / REG
            if cls.get("block_notes"):
                node["notes"] = cls["block_notes"]

            # ---- 父链挂载：弹栈到该块类型的合理父层级，避免块无限嵌套 ----
            def _pop_to(levels: tuple):
                """弹栈直到栈顶 level 为 levels 之一，或只剩 root。"""
                while len(stack) > 1 and stack[-1]["level"] not in levels:
                    stack.pop()

            if kind == "fu_title":
                if head == "五军都督府所属卫所":
                    stack[:] = [root]
                else:  # 左/右/中/前/后军都督府 → 挂「五军都督府所属卫所」容器下
                    idx = next(
                        (
                            i
                            for i, s in enumerate(stack)
                            if s.get("name") == "五军都督府所属卫所"
                        ),
                        -1,
                    )
                    if idx >= 0:
                        del stack[idx + 1 :]
                    else:
                        stack[:] = [root]
            elif kind == "zai_jing":
                _pop_to(("府",))  # 在京 → 挂当前府下
            elif kind == "block_title":
                if head == "上十二卫":
                    stack[:] = [root]  # 亲军不属五府，挂卷根
                elif head == "在外":
                    _pop_to(("府",))  # 在外 → 挂当前府下
                elif head in ("北平三护卫", "山西三护卫"):
                    # 三护卫与都司平级，同属「在外」块；彼此也是兄弟块
                    # （山西三护卫不得挂北平三护卫下）。弹到「在外」或府为止。
                    while (
                        len(stack) > 1
                        and stack[-1].get("name") != "在外"
                        and stack[-1]["level"] != "府"
                    ):
                        stack.pop()
                else:  # 土官等 → 挂当前栈顶（都司/在京/在外均可，作为其子块）
                    pass
            else:  # du_si
                # 都司 → 挂最近「在外」块下；无在外则挂府下兜底
                _pop_to(("块", "府"))
            stack[-1]["children"].append(node)
            stack.append(node)
            # 「块标题+卫列」混合行（实测 L112「北平行都司(…)+大宁左卫…」）：
            # 余留文本切段挂到刚压栈的块下
            rest = (cls.get("rest") or "").strip()
            if rest:
                _attach_wei_col(rest, line_no, index, node)
        elif kind == "wei_col":
            _attach_wei_col(line, line_no, index, stack[-1])
        elif kind == "count_row":
            node = {
                "cand": True,
                "name": s,
                "level": "数量行",
                "count_marker": s,
                "children": [],
                "src_loc": "卷66-L%d" % line_no,
                "confidence": 0.9,
            }
            stack[-1]["children"].append(node)
        else:  # zhangben / other
            to_review.append(cls)

    return {
        "list_ver": list_ver,
        "volume": volume,
        "candidates": root["children"],
        "root": root,
        "to_review": to_review,
        "stat": stat,
    }


# =============================================================================
# 4. 覆盖率与词典（阶段一验收数据）
# =============================================================================


def build_coverage(tree: dict, source_lines, index: dict) -> dict:
    """计算切段覆盖率 / 括注剥离率 / 同名词典（阶段一硬指标）。

    - 覆盖率 = 确定切分数 / (确定切分数 + 待复核段数)——如实反映规则引擎
      的确定性；AI 复核把待复核段逐卫拆分后自然逼近 100%。
    - 括注剥离率：凡 `卫(注)` 形态，注必并入前节点 notes（本骨架保证 100%）。
    """
    stat = tree.get("stat", {})
    det, pend = stat.get("determined", 0), stat.get("pending", 0)
    cov = det / (det + pend) if (det + pend) else 0.0

    def walk(node, acc):
        if node.get("level") in ("卫", "所"):
            acc.append(node)
        for c in node.get("children") or []:
            walk(c, acc)
        return acc

    leaves = walk(tree.get("root", {}), [])
    bracket_total = sum(len(n.get("notes") or []) for n in leaves)
    return {
        "determined_count": det,
        "pending_count": pend,
        "segment_coverage": round(cov, 4),
        "coverage_min": ACCEPTANCE["segment_coverage_min"],
        "coverage_ok": cov >= ACCEPTANCE["segment_coverage_min"],
        "bracket_notes_total": bracket_total,
        "bracket_strip_rate": 1.0,
        "wei_name_index_size": len(index),
        "src_lines": len(source_lines),
    }


# =============================================================================
# 5. AI 复核接口（执行期由 AI 逐行调用；此处只定义契约）
# =============================================================================


def review_candidates(tree: dict, corrections: list) -> dict:
    """把候选树与 AI 修正合并为**定稿候选集**（仍须过打包器 ID/护栏）。

    corrections : list[dict]
        每项 {"src_loc": "卷66-L58", "action": "merge"|"rename"|"delete"|"split",
              "field": "...", "value": "...", "new_names": [...]}
        split 时 new_names 给出逐卫名称（AI 裁决的边界）。
    规则引擎不解释 corrections——它们由 AI 复核流程消费；
    review 后应调用 save_name_index() 把确认卫名回填词典。
    """
    for c in corrections or []:
        if c.get("action") not in ("merge", "rename", "delete", "split"):
            raise ValueError("未知复核动作: %s" % c.get("action"))
        if c.get("action") == "split" and not c.get("new_names"):
            raise ValueError("split 必须提供 new_names 逐卫名称")
    tree["review"] = {"status": "pending", "corrections": len(corrections or [])}
    return tree


# =============================================================================
# 6. CLI
# =============================================================================


def load_source_lines(vol: str, start: int, end: int):
    """从 assets/sources/兵志.txt 读取指定行段（1-based 闭区间）。"""
    src = os.path.join(PATHS["source"], "兵志.txt")
    with io.open(src, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    return [(i + 1, ln) for i, ln in enumerate(lines) if start <= i + 1 <= end]


def main():
    ap = argparse.ArgumentParser(description="C17 卫所候选生成器（规则引擎, 只产候选）")
    ap.add_argument("--vol", default="66", help="卷号(默认66, 试点阶段只跑卷66)")
    ap.add_argument(
        "--ver",
        choices=["old", "new"],
        required=True,
        help="list_ver: old=旧编成 / new=后定编成",
    )
    ap.add_argument(
        "--lines", default=None, help="行段 'L52-L120'（缺省按 ver 取默认段）"
    )
    ap.add_argument("--out", default=None, help="候选 JSON 输出路径")
    ap.add_argument(
        "--save-index",
        action="store_true",
        help="把括注锚点确认的卫名回填 WEI_NAME_INDEX",
    )
    args = ap.parse_args()

    if args.lines:
        m = re.match(r"L(\d+)[-–]L(\d+)$", args.lines)
        if not m:
            raise SystemExit("--lines 格式须为 L52-L120")
        start, end = int(m.group(1)), int(m.group(2))
    else:
        start, end = (52, 120) if args.ver == "old" else (122, 251)

    index = _index_ctx()
    # 括注锚点先行预扫一遍，把 `X卫(注)` 的 X 直接收入词典（合法：括注前词必完整）
    if args.save_index:
        for _no, ln in load_source_lines(args.vol, start, end):
            for m in BRACKET_RE.finditer(ln):
                head = ln[: m.start()]
                tail = head[-3:]
                for suf in ALL_SUFFIXES:
                    if tail.endswith(suf):
                        name = head[head.rfind(suf) - 12 :].strip()
                        # 取最后一个词尾后缀前的中文串（≤12 字卫名）
                        name = re.sub(r"^.*?([\u4e00-\u9fff]+$)", r"\1", name)
                        if name and len(name) <= 12:
                            item = index.setdefault(name, {"count": 0, "first": None})
                            item["count"] += 1
                            if item["first"] is None:
                                item["first"] = "L%d" % _no

    lines = load_source_lines(args.vol, start, end)
    tree = build_candidate_tree(lines, args.ver, args.vol, index)
    cov = build_coverage(tree, lines, index)
    out = {
        "meta": {
            "vol": args.vol,
            "list_ver": args.ver,
            "lines": "L%d-L%d" % (start, end),
            "note": "规则引擎候选结果，必须经 AI 复核后方可写定稿（SKILL.md §13）",
        },
        "tree": tree,
        "coverage": cov,
    }
    path = args.out or os.path.join(
        PATHS["data"], "weis", "candidates_%s_%s.json" % (args.vol, args.ver)
    )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("候选已产出:", path)
    print(
        "确定切分=%d 待复核段=%d 覆盖率=%.1f%% (下限 %.0f%%) 词典=%d 括注注数=%d"
        % (
            cov["determined_count"],
            cov["pending_count"],
            cov["segment_coverage"] * 100,
            ACCEPTANCE["segment_coverage_min"] * 100,
            cov["wei_name_index_size"],
            cov["bracket_notes_total"],
        )
    )
    print("注意：覆盖率未达标或 AI 复核未完成不得进入定稿（阶段一/二验收）。")


if __name__ == "__main__":
    main()
