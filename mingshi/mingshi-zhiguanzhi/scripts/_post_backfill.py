# -*- coding: utf-8 -*-
"""
第 3 项：posts 逐条回填 vacancy_type / post_status / is_concurrent / selection_route / salary_ref。

设计原则（宁缺毋滥，绝不臆造）：
  原文只在**明确列举**或**明确陈述**处给出判定，故采用「规则命中即填，不命中留未明」，
  并逐条记录 `backfill_evidence`（命中的原文依据），使每条回填可溯源、可推翻。

五条回填规则（全部有原文出处）：

R1 世官（原文第 40 行「世官九等」名单 + 第 18-19 行）：
   指挥使 / 指挥同知 / 指挥佥事 / 卫镇抚 / 正千户 / 副千户 / 百户 / 试百户 / 所镇抚
   → selection_route="世官", succession=True

R2 流官（原文第 40 行「流官八等」名单）：
   左都督 / 右都督 / 都督同知 / 都督佥事 / 都指挥使 / 都指挥同知 / 都指挥佥事 /
   正留守 / 副留守
   → selection_route="流官", succession=False

R3 外卫默认（原文 05-051「率世官，或有流官」）：
   外卫指挥使司条目下的卫官 → 沿用 R1/R2 名单判定，名单外留未明。

R4 寄禄（原文「恩荫寄禄无常员」「恩功寄禄，无定员」「以寄禄驭恩幸」）：
   注记含「寄禄」的 post → vacancy_type="纳职"(带俸不莅事), post_status="后设"
   实际处置：寄禄=有职衔无实事，最贴近 VACANCY_TYPES 中的「纳职」（原文自注"带俸，不莅事"）。

R5 试职（原文 05-053「凡千户，一人掌印，一人佥书，曰管军。千户、百户，有试，有实授」）：
   原文仅陈述"有试职、有实授"两种状态，**未指明某具体官职为试职**，故不逐条回填，
   仅在 note 注明该制度存在（避免臆造）。

R6 兼领（原文「兼」138 处，多为机构职掌合并叙事，非官职兼任）：
   仅当 post 的原文邻域出现「兼领/兼掌/兼摄」且主语为该官职时填 is_concurrent=True。
   实测此类极少，宁缺毋滥。

salary_ref：由 grade 查 E.SALARY_TABLE 派生（原文第 25 行岁禄表），不做人工判断。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _kg_enums as E

# ---------- R1 世官九等（原文第 40 行，武选司条）----------
SHIGUAN = ["指挥使", "指挥同知", "指挥佥事", "卫镇抚", "正千户",
           "副千户", "百户", "试百户", "所镇抚"]

# ---------- R2 流官八等（原文第 40 行）----------
LIUGUAN = ["左都督", "右都督", "都督同知", "都督佥事", "都指挥使",
           "都指挥同知", "都指挥佥事", "正留守", "副留守"]

# ---------- R1b 世袭类（原文另处明言"世袭""世职"者，不属武选司世官九等）----------
# 与 SHIGUAN 的区别：SHIGUAN 是"武职世官九等"这一铨选制度的名单；
# 此处为原文在**具体官职**旁明写「世袭／世职」者，属该官职自身的承袭属性。
# 二者都落 selection_route="世官" + succession=True，但依据文本不同（route_evidence 分记）。
SHIXI_OFFICES = {
    "衍圣公": "衍圣公，孔氏世袭（原文 02-073）",
    "龙虎山正一真人": "龙虎山正一真人一人…封为真人，世袭（原文 03-043）",
    "正一真人": "龙虎山正一真人一人…封为真人，世袭（原文 03-043）",
}

# ---------- 作用域闸门 ----------
# 世官九等／流官八等是**兵部武选司**铨选制度，管辖范围为「卫所土官」。
# 但同为「指挥同知」之名，在留守司（05-046 属官）与卫指挥使司（05-051）下语义不同：
#   留守司属官 → 不套用卫所世官名单；卫/都司/都督府 → 套用。
# owner 字段在卷05 多条为空（原文首句即机构名，未单列 owner），故以
# **条目原文首段**（由调用方传入 scope_text）判定语域，而非仅看 owner。
WEISUO_SCOPE_HINTS = ("卫指挥使司", "都指挥使司", "都督府", "京卫",
                      "留守司", "都司", "千户所", "卫镇抚", "世官", "袭替")
# 首句即「留守司。」者（如其属官指挥同知），不套用卫指挥使司名单。
# 注意：必须锚定**原文开头**，不可全串子串匹配 —— 05-051 卫指挥使司条中
# 亦含「或留守司。」字样（"外卫各统于都司、行都司或留守司。"），
# 全串匹配会把卫条误判为留守司条。
FEISHUO_PREFIX = "留守司"


def _is_feishuo(scope):
    """判是否「首句为留守司」的非卫所条目。"""
    return scope.startswith(FEISHUO_PREFIX)

EV_SHIGUAN = "世官九等：指挥使、指挥同知、指挥佥事、卫镇抚、正千户、副千户、百户、试百户、所镇抚（皆有袭职、替职）"
EV_LIUGUAN = "流官八等：左右都督、都督同知、都督佥事、都指挥使、都指挥同知、都指挥佥事、正留守、副留守（皆不得世）"


def _atomic_apply(p, parts):
    """对单个 post 应用回填规则；返回被填字段字典。"""
    filled = {}

    # --- salary_ref：一律按品级查表（原文第 25 行岁禄表）---
    # 南京官 grade=="同北京" 时，grade_order 已由打包器从 link_to_bj.grade_ref 派生，
    # 此处用 link grade_ref 的品级查表；查不到留未明。
    g_for_salary = p.get("grade")
    link = p.get("link_to_bj") or {}
    if g_for_salary in ("同北京", "未明") and link.get("grade_ref"):
        g_for_salary = link["grade_ref"]
    sref = E.salary_ref_of(g_for_salary)
    if sref != "未明":
        filled["salary_ref"] = sref
        filled["salary_evidence"] = "洪武二十五年重定内外文武官岁给禄俸之制（原文岁禄专段）"

    # --- vacancy_type：寄禄（与铨选语域无关，先判）---
    txt = "%s %s" % (p.get("note", ""), p.get("count_evidence", ""))
    if "寄禄" in txt:
        filled["vacancy_type"] = "纳职"
        filled["vacancy_evidence"] = "「恩荫寄禄无常员」「恩功寄禄，无定员」——寄禄为带俸不莅事之虚衔"

    # --- selection_route / succession ---
    # 先判 R1b：原文旁明写「世袭／世职」的官职（不属武选司世官九等）
    hit_shi = next((o for o in parts if o in SHIXI_OFFICES), None)
    if hit_shi:
        filled["selection_route"] = "世官"
        filled["succession"] = True
        filled["route_evidence"] = SHIXI_OFFICES[hit_shi]
        return filled

    # R1/R2 仅在卫所语域内启用（武选司铨选制度的管辖范围）
    scope = p.get("_scope_text", "") or ""
    if _is_feishuo(scope):
        return filled
    if not any(h in scope for h in WEISUO_SCOPE_HINTS):
        return filled

    for o in parts:
        if o in SHIGUAN:
            filled["selection_route"] = "世官"
            filled["succession"] = True
            filled["route_evidence"] = EV_SHIGUAN
            break
        if o in LIUGUAN:
            filled["selection_route"] = "流官"
            filled["succession"] = False
            filled["route_evidence"] = EV_LIUGUAN
            break

    return filled


def backfill(posts, owner="", item_id="", scope_text=""):
    """就地对 posts 列表回填；返回 (填了 selection_route 的条数, 填了 salary 的条数)。

    scope_text: 该 RANK 记录所属**条目原文**（由 build_struct 从 _item_registry 注入），
                用于判定「世官九等／流官八等」是否适用于本条目的官职。
    """
    n_route = n_salary = 0
    for p in posts:
        p["_owner_note"] = owner
        p["_scope_text"] = scope_text
        parts = p.get("office_parts") or [p.get("office", "")]
        filled = _atomic_apply(p, parts)
        p.pop("_owner_note", None)
        p.pop("_scope_text", None)
        for k, v in filled.items():
            p[k] = v
        if "selection_route" in filled:
            n_route += 1
        if "salary_ref" in filled:
            n_salary += 1
    return n_route, n_salary
