# -*- coding: utf-8 -*-
"""
C15 官职层（OFFICIALS）构建器 —— 由 ORG 树 + RANK posts + 原文证据派生官职节点。

用户裁定（2026-10-15）：
  ① 建立官职层；
  ② 覆盖**全部官职**（不限有原文上下级证据者）；
  ③ 平级 = 同机构同品级 / 同层级，**不跨机构**。

设计要点
--------
1. **官职来源**（三条合流，去重后建节点）：
   a. ORG 树每个节点的 `posts[]`（含 v7 转正的 218 个节点）；
   b. RANK 记录的 `posts[]`（品级员额 97 条 / 427 posts）；
   c. 实体层 `type=="official"` 的 1109 条标注（此前标了却无主键可索引）。
2. **节点键** = (org_id, office_name)。同名官职挂在不同机构下 → 不同节点
   （「吏部郎中」≠「户部郎中」）。这正是"平级不跨机构"的前提。
3. **平级**（用户第 3 项定义，写死）：`peers` 仅当**同 org_id 且同 grade_order**
   时互连。绝不退化为"同品级列表"。
4. **官职关系**只建有原文依据的三种：副贰(贰之/佐之) / 首领(为首领官) / 兼领(兼领之)。
   同机构内的其余上下级不建 relation 边（组织包含已由 ORG 树表达）。
5. **俸禄**：`salary.grade_based` = 按品级保底（岁禄表）；`salary.actual` =
   该官职的实际俸禄（有原文依据才填，否则 null）。
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C
import _kg_enums as E

# ---------- 原文证据（关系表述 → 类型）----------
REL_PATTERNS = [
    # (正则, 关系类型, 说明)
    (r"贰之", "副贰", "侍郎贰之"),
    (r"佐之", "副贰", "少詹事佐之 / 司历、监候佐之 / 训导佐之"),
    (r"为首领官", "首领", "主事、司务各四人，为首领官，有主事印"),
    (r"兼领之", "兼领", "以礼部尚书、侍郎由翰林出身者兼掌之 等"),
]

# ---------- 实俸证据（原文表述 → salary.actual 形态）----------
# 作用域：仅当该官职所属**条目原文**命中判定句时回填，宁缺毋滥。
ACTUAL_SALARY_RULES = [
    # (条目原文命中串, form, note, duty)
    ("非真授者曰署职", "不支俸", "署职，递加本职一级作半级，不支俸，非军功，毋得实授", "署职"),
    ("曰试职", "半俸", "试职作一级，支半俸，不给诰", "试职"),
    ("曰纳职", "带俸", "纳职带俸，不莅事", "纳职"),
    ("设官不给禄", "不给禄", "设官不给禄", "不给禄"),
    ("皆无岁禄", "无岁禄", "凡土司之官九级，自从三品至从七品，皆无岁禄", "土司"),
    ("岁禄以功为差", "以功为差", "公、侯、伯…岁禄以功为差", "勋爵"),
    ("岁禄各有差", "各有差", "驸马都尉…岁禄各有差，皆不得与政事", "驸马仪宾"),
    ("曰见任管事", "本色", "分理诸杂务，曰见任管事", "见任管事"),
    ("曰带俸差操", "带俸", "不任事入队，曰带俸差操", "带俸差操"),
]

# 哪些条目原文的「不给禄」只作用于该条的一些官职（而非全部）
# 04-073 医学：正科(府,从九品)不给禄，但州典科/县训科原文未注品级
# 原文「医学。府，正科一人。(从九品)州，典科一人。县，训科一人。洪武十七年置，设官不给禄。」
# → 「设官不给禄」修饰的是**该条全部官职**，故全填。


def load_vol_json(container, vol):
    p = os.path.join(C.LAYERS, container, "%s_%s.json" % (container, vol))
    if not os.path.isfile(p):
        return []
    with open(p, "r", encoding="utf-8") as f:
        obj = json.load(f)
    return obj.get("records", []) if isinstance(obj, dict) else obj


def is_rank(rec):
    """structs 层的维度分派（pitfalls #38 定死顺序：children → change_type → line_type → posts）"""
    if "children" in rec:
        return False
    if "change_type" in rec:
        return False
    if "line_type" in rec:
        return False
    return "posts" in rec


def is_org(rec):
    return "children" in rec


# ---------- org_binding：无机构归属官职的分类（v12 缺口1）----------
# 背景（可用性审计 缺口1）：387 个官职节点 org_id="" 占 1241 的 31%。
# 样本显示这**不是数据缺失**，而是真实判定难点：
#   · OFF-1087 总督京营戎政 / OFF-1106 把总 / OFF-942 参将 / OFF-929 千总
#     ——全来自 05-006 京营条「设副、参、游、佐、坐营、号头、中军、千把总等官」
#     属**差遣性军职**，不属任一固定机构，不给 org 是对的；
#   · 但 `org_name=''` 与「归属未明」混在一起，查询时无法区分。
# 故新增 org_binding 区分「有意留空」与「尚未判定」。
#
# 取值（OFFICIAL_BINDINGS 枚举）：
#   机构   —— 有 org_id（正常挂载）
#   差遣军职 —— 京营/镇戍等临时增设的武职，原文无固定机构
#   散官加官 —— 加官/赠官/兼官，非常设编制（三公三孤、东宫大臣）
#   封爵   —— 公侯伯/驸马都尉等爵位性官职
#   土官   —— 土司所辖，隶属宣慰/宣抚/安抚/长官等司
#   未明   —— 真未判定（须复核者，进 verify 清单）
ORG_BINDING_ONLY = "机构"
_ORG_BINDING_RULES = [
    # (取值, 官职名或来源条目判据, 说明)
    ("差遣军职", ("把总", "千总", "把司", "把牌", "参将", "游击", "守备",
                  "副总兵", "总兵官", "号头", "中军", "坐营", "副将", "佐击",
                  "总督京营戎政", "协理京营戎政", "提督", "巡视", "备御",
                  "领班", "备倭", "镇守", "分守", "协守", "提调"),
     "差遣性武职（京营/镇戍），原文无固定机构"),
    ("散官加官", ("太师", "太傅", "太保", "少师", "少傅", "少保",
                  "太子太师", "太子太傅", "太子太保", "太子少师", "太子少傅",
                  "太子少保", "太子宾客", "三公", "三孤"),
     "加官/赠官/兼官，非常设编制"),
    ("封爵", ("公", "侯", "伯", "驸马都尉", "仪宾", "郡主", "县主"),
     "爵位性官职，非机构编制"),
]


def classify_binding(office, sources, item_id=None):
    """无机构归属时的分类（v12 缺口1）。返回 (binding, reason)。"""
    nm = office or ""
    if not nm:
        return "未明", ""
    for binding, keys, reason in _ORG_BINDING_RULES:
        for k in keys:
            if nm == k or nm.endswith(k):
                return binding, reason
    # 土官：item_id 落在卷05 条54–60（土司段）
    if item_id and item_id.startswith("05-") and item_id[3:] >= "054":
        return "土官", "土司所辖官职，隶宣慰/宣抚/安抚/长官等司"
    if item_id and item_id[:2] in ("02",) and "总督" in nm:
        return "差遣军职", "督抚类差遣，原文无固定机构"
    if item_id and item_id[:2] in ("02",) and "巡抚" in nm:
        return "差遣军职", "督抚类差遣，原文无固定机构"
    return "未明", ""


def walk_org(node, out, parent_id=None, parent_name=None, path=None,
             parent_item_id=None):
    """递归展平 ORG 树；返回 [(id, name, level, parent_name, posts, org_path)]

    ⚠ 关键历史（v10 已修）：
    打包器 `assign_ids` 只对**顶层记录**分 ID，`children[]` 子节点长期无名。
    v10 起 `build_struct.py` 会为子节点派生稳定 ID（`<父ID>#<序号>`）并回填
    `posts[].org_id`；此函数**优先沿用**记录里已有的 `id`，仅在缺失时才合成，
    以免覆盖真实 ID 造成两处 ID 空间不一致（曾致 446/869 条官职无机构归属）。

    ⚠ 子节点的 `item_id` 沿树继承根节点：职掌条回溯（owning_item）依赖
    「同机构的所有层都属同一编制条」这一事实，子节点自身不带 item_id。
    """
    if path is None:
        path = []
    nid = node.get("id")
    if not nid:
        # 合成 ID（仅在 build_struct 未派生时兜底）
        nid = "%s#%s" % (parent_id or "ROOT", "/".join(path + [node.get("name") or ""]))
    my_path = path + [node.get("name")]
    my_item = node.get("item_id") or parent_item_id
    out.append({
        "id": nid,
        "name": node.get("name"),
        "level": node.get("level"),
        "parent_name": parent_name,
        "parent_id": parent_id,
        "posts": node.get("posts") or [],
        "org_type": node.get("org_type"),
        "is_virtual": bool(node.get("is_virtual", False)),
        "item_id": my_item,
        "path": my_path,
    })
    for c in (node.get("children") or []):
        walk_org(c, out, nid, node.get("name"), my_path, my_item)


# ---------- 官职名归一 ----------
# 官职名前缀噪音：并列分割后的单名、括注残留等
OFFICE_CLEAN = [
    (re.compile(r"^《(.+)》$"), r"\1"),        # 《五经》博士 → 五经博士
    (re.compile(r"^(左|右)、?(左|右)"), r"\1"),  # 左、右宗人 → 左宗人（office_parts 已拆）
]


def clean_office(name):
    n = (name or "").strip()
    n = n.replace("《", "").replace("》", "")
    return n


def build_officials(vols):
    """主构建：返回 (officials, errs, stats)"""
    errs = []
    stats = {}

    # ---------- 1. 收集 ORG 树 ----------
    org_nodes = []
    org_by_id = {}
    for v in vols:
        for rec in load_vol_json("structs", v):
            if is_org(rec):
                walk_org(rec, org_nodes)
    for n in org_nodes:
        if n["id"]:
            org_by_id[n["id"]] = n

    # ---------- 2. 收集 RANK（含卷00 专表）----------
    rank_recs = []
    for v in sorted(set(vols) | {"00"}):
        for rec in load_vol_json("structs", v):
            if is_rank(rec):
                rank_recs.append(rec)

    # ---------- 3. 收集 ENT official 标注 ----------
    ent_official = {}     # normalized_name -> [item_id...]
    for v in vols:
        for rec in load_vol_json("ents", v):
            if rec.get("type") == "official":
                nm = rec.get("normalized") or rec.get("text") or ""
                ent_official.setdefault(nm, []).append(rec.get("item_id", ""))

    # ---------- 4. 合流建节点 ----------
    # key = (org_id, office_name)
    nodes = {}

    def add(org_id, org_name, org_path, office, grade, grade_order,
            count, note, item_id, src, rank_id=None, link_to_bj=None):
        office = clean_office(office)
        if not office:
            return
        key = (org_id or "", office)
        if key not in nodes:
            nodes[key] = {
                "org_id": org_id or "",
                "org_name": org_name or "",
                "org_path": org_path,
                "office": office,
                "grade": grade or "未明",
                "grade_order": grade_order if grade_order is not None else E.grade_order(grade),
                "count": count,
                "note": note or "未明",
                "item_ids": [],
                "rank_ids": [],
                "sources": set(),
                "link_to_bj": link_to_bj or {},
                "org_binding": ORG_BINDING_ONLY if org_id else "",
                "org_binding_reason": "" if org_id else "",
            }
        n = nodes[key]
        if item_id and item_id not in n["item_ids"]:
            n["item_ids"].append(item_id)
        if rank_id and rank_id not in n["rank_ids"]:
            n["rank_ids"].append(rank_id)
        n["sources"].add(src)
        # 品级取更具体者（"未明" 让位于具体品级）
        if n["grade"] == "未明" and grade and grade != "未明":
            n["grade"] = grade
            n["grade_order"] = grade_order if grade_order is not None else E.grade_order(grade)
        if n["count"] == 0 and count:
            n["count"] = count

    # 4a. ORG 节点自带 posts（v10：post 已由 build_struct 回填 org_id，直接用）
    for n in org_nodes:
        if not n["id"] or n["is_virtual"]:
            continue
        path = n.get("path") or [n["name"]]
        for p_ in (n["posts"] or []):
            parts = p_.get("office_parts") or [p_.get("office")]
            for part in parts:
                add(p_.get("org_id") or n["id"], n["name"], path, part,
                    p_.get("grade"), p_.get("grade_order"),
                    p_.get("count", 0), p_.get("note"),
                    n.get("item_id"), "ORG", link_to_bj=p_.get("link_to_bj"))

    # 4b. RANK posts（v10：优先用 build_struct 回填的 owner_org_id）
    for r in rank_recs:
        rtype = r.get("rank_type")
        if rtype != "品级员额":
            continue          # 散阶/勋级/俸禄/爵位为专表，不进官职层（属品级制度非官职编制）
        iid = r.get("item_id") or ""
        rid = r.get("id")
        org_id = r.get("owner_org_id") or ""
        org_name = r.get("owner_org_name") or r.get("owner") or ""
        pick = org_by_id.get(org_id) or {}
        org_path = pick.get("path") or ([org_name] if org_name else [])
        for p_ in (r.get("posts") or []):
            parts = p_.get("office_parts") or [p_.get("office")]
            for part in parts:
                add(org_id, org_name, org_path, part,
                    p_.get("grade"), p_.get("grade_order"),
                    p_.get("count", 0), p_.get("note"),
                    iid, "RANK", rank_id=rid,
                    link_to_bj=p_.get("link_to_bj"))

    # 4c. ENT official 标注（未被 ORG/RANK 覆盖的官职也建节点，org_id=""）
    for nm, iids in ent_official.items():
        nm2 = clean_office(nm)
        if not nm2:
            continue
        # 若该官职名已在某机构下存在，不重复建 org_id="" 的孤立节点
        if any(k[1] == nm2 for k in nodes):
            continue
        for iid in iids[:1]:
            nodes[("", nm2)] = {
                "org_id": "", "org_name": "", "org_path": [],
                "office": nm2, "grade": "未明", "grade_order": 99,
                "count": 0, "note": "仅实体层标注，未见于编制行",
                "item_ids": [iid], "rank_ids": [], "sources": {"ENT"},
                "link_to_bj": {},
            }

    stats["org_nodes"] = len(org_nodes)
    stats["rank_recs"] = len(rank_recs)
    stats["ent_official"] = len(ent_official)
    stats["node_total"] = len(nodes)

    # ---------- 5. 关系：只建有原文依据的三种 ----------
    # ⚠ 关系表述所在的条目**往往不是编制条目**：
    #   · 01-001「明官制…侍郎贰之」是卷首总述；
    #   · 01-034「尚书，掌天下武卫官军选授…侍郎佐之」是**职掌条**，
    #     其编制在同机构的前一条 01-033（兵部编制条），本条自身不带 posts；
    #   · 01-011「为首领官」是主事/司务的职掌条。
    #   故不能用「该条目 own 的官职」定位关系双方，必须**从关系句本身解析官职名**，
    #   并且把「关系条 → 编制条」的归属**沿条目序回溯**（职掌条紧跟其编制条）。
    #
    #   回溯纪律：只在**同卷、序号更小、且确有 ORG 节点**的条目中找最近者；
    #   跨卷不回（卷首条目无前驱时留 unmatched，不臆测）。
    reg_all = C.load_registry()
    item_order = {iid: (v[0], int(v[1])) for iid, v in
                  ((k, k.split("-")) for k in reg_all)
                  if len(v) == 2 and v[1].isdigit()}
    org_items = set()
    for n in org_nodes:
        if n.get("item_id"):
            org_items.add(n["item_id"])

    def owning_item(iid):
        """返回该条目语域所属的「编制条」item_id（优先自身，否则同卷回溯）。"""
        if iid in org_items:
            return iid
        v, k = item_order.get(iid, (None, None))
        if v is None:
            return iid
        cands = [i for i in org_items
                 if item_order.get(i, (None, None))[0] == v
                 and item_order[i][1] < k]
        if not cands:
            return iid
        return max(cands, key=lambda i: item_order[i][1])

    rel_hits = {}     # item_id -> [(type, pat, context, pos, owning_item)]
    for iid, v in reg_all.items():
        if iid.split("-")[0] not in vols:
            continue
        txt = v.get("original") or ""
        for pat, rtype, _ex in REL_PATTERNS:
            for m in re.finditer(pat, txt):
                # 关系句窗口：标记词前 60 字 / 后 20 字
                a = max(0, m.start() - 60)
                b = min(len(txt), m.end() + 20)
                rel_hits.setdefault(iid, []).append(
                    (rtype, pat, txt[a:b], m.start(), owning_item(iid)))

    stats["rel_entries"] = len(rel_hits)
    stats["rel_mentions"] = sum(len(v) for v in rel_hits.values())

    # ---------- 6. 落 ID + peers + salary ----------
    # 排序：机构序（org_id）→ 品级（高→低）→ 官职名
    ordered = sorted(nodes.values(),
                     key=lambda n: (n["org_id"] or "zzz", n["grade_order"], n["office"]))
    for i, n in enumerate(ordered, 1):
        n["official_id"] = "%s%03d" % (E.ID_PREFIX["off"], i)
        n["id"] = n["official_id"]
        n["sources"] = sorted(n["sources"])

    # org_binding（v12 缺口1）：无机构归属者分类，区分「有意留空」与「尚未判定」
    binding_stat = {}
    for n in ordered:
        if n["org_id"]:
            n["org_binding"] = ORG_BINDING_ONLY
            n["org_binding_reason"] = ""
        else:
            b, why = classify_binding(n["office"], n["sources"],
                                      n["item_ids"][0] if n["item_ids"] else None)
            n["org_binding"] = b
            n["org_binding_reason"] = why
        binding_stat[n["org_binding"]] = binding_stat.get(n["org_binding"], 0) + 1
    stats["org_binding"] = binding_stat

    # peers：同 org_id 且同 grade_order（用户定义，写死）
    by_org_grade = {}
    for n in ordered:
        if not n["org_id"]:
            continue          # 无机构归属者不参与平级判定
        by_org_grade.setdefault((n["org_id"], n["grade_order"]), []).append(n)
    peer_n = 0
    for n in ordered:
        key = (n["org_id"], n["grade_order"])
        grp = by_org_grade.get(key, [])
        if not n["org_id"] or len(grp) < 2:
            n["peers"] = []
            continue
        n["peers"] = [m["official_id"] for m in grp if m is not n]
        peer_n += 1

    # salary：grade_based（保底）+ actual（实俸，有据才填）
    for n in ordered:
        g = n["grade"]
        if g == "同北京" and n.get("link_to_bj", {}).get("grade_ref"):
            g_ref = n["link_to_bj"]["grade_ref"]
        else:
            g_ref = g
        gb = E.salary_obj(g_ref, form="本色", source="岁禄表",
                          note="洪武二十五年重定内外文武官岁给禄俸之制")
        if gb["amount"] is None:
            gb = None
        n["salary"] = {"grade_based": gb, "actual": None}

    # actual：由所属条目原文命中判定句
    actual_n = 0
    for n in ordered:
        for iid in n["item_ids"]:
            txt = (reg_all.get(iid, {}).get("original") or "")
            hit = None
            for needle, form, note, duty in ACTUAL_SALARY_RULES:
                if needle in txt:
                    hit = (needle, form, note, duty)
                    break
            if not hit:
                continue
            needle, form, note, duty = hit
            # 「见任管事 / 带俸差操」为同一条目内的**两种对立状态**，
            # 不能整条套用：仅当官职为卫所武官（grade 属卫官品级）时按条填「见任管事」，
            # 并注记「不任事则为带俸差操」（原文对照关系保留）。
            if needle == "曰见任管事":
                obj = E.salary_obj(n["grade"], form="本色",
                                   source=iid + "（见任管事）", note=note)
                obj["note"] = "分理屯田、验军、营操…曰见任管事；不任事入队，曰带俸差操"
                obj["duty"] = "见任管事"
            elif needle == "岁禄以功为差" or needle == "岁禄各有差":
                obj = {"item": "米", "amount": None, "unit": "石", "form": form,
                       "era_text": "未明", "era": None, "source": iid,
                       "note": note, "duty": duty}
            else:
                obj = E.salary_obj(n["grade"], form=form, source=iid, note=note)
                obj["duty"] = duty
            n["salary"]["actual"] = obj
            actual_n += 1
            break

    stats["official_total"] = len(ordered)
    stats["peers"] = peer_n
    stats["actual_salary"] = actual_n
    stats["org_items"] = org_items
    return ordered, rel_hits, stats, errs


# ---------- 关系配对（依赖 ordered）----------
LEADER_HINTS = ("尚书", "都御史", "卿", "寺卿", "太仆寺卿", "大理寺卿", "通政使",
                "詹事", "祭酒", "总督", "巡抚", "留守", "郎中")


def build_official_relations(officials, rel_hits, org_by_id, org_items=None):
    """把原文关系表述配对为官职→官职边。

    方法（关键：关系句自身解析官职名，不依赖条目是否携带 posts）：
      以关系标记词（贰之/佐之/为首领官/兼领之）为锚点，在其**前导窗口**内
      做官职名**最长匹配**。

    ⚠ 语义方向（v10 首跑曾判反，务必守）：
      原文句式一律是「**A，职掌…。B佐之**」——B 是佐者（副贰），A 是被佐者（主官）；
      「以尚书任天下事，**侍郎贰之**」同：侍郎佐尚书。
      故**主官 = 窗口内首个官职名，佐者 = 标记词紧邻的那个**（中文语序：佐者紧贴动词）。
      反取会把方向整个转 180°（实测把「侍郎佐尚书」配成「尚书佐侍郎」）。

    配对纪律（宁缺毋滥）：
      · 前导窗口内至少要解析出**两个**官职名，否则不配对（只记 evidence）；
      · 主官 = 窗口内**第一个**官职名（句首主语，被佐者）；
      · 佐者 = 窗口内**其余**官职名（通常为紧邻标记词的那个）。
    """
    # 官职词表：全部官职名（按长度降序，做最长匹配）
    vocab = sorted({n["office"] for n in officials}, key=len, reverse=True)

    def sub_base_match(office, name):
        """合称/拆名互认：`左侍郎`≡`侍郎`、`右侍郎`≡`侍郎`（去左右前缀后同名）。"""
        if office == name:
            return True
        return re.sub(r"^(左|右)", "", office) == re.sub(r"^(左|右)", "", name)

    def parse_offices(window):
        """在窗口文本中解析官职名（不重叠最长匹配，按出现位置排序）。"""
        found = []
        i = 0
        while i < len(window):
            hit = None
            for w in vocab:
                if len(w) >= 2 and window.startswith(w, i):
                    hit = w
                    break
            if hit:
                found.append((i, hit))
                i += len(hit)
            else:
                i += 1
        return found

    out, unmatched = [], []
    for iid, hits in rel_hits.items():
        for (rtype, pat, window, pos, owner_item) in hits:
            # ⚠ 纪律零：关系条必须有**可定位的机构语域**。
            #   卷首总述（01-001「明官制…侍郎贰之」）讲的是全书通则，
            #   其自身无 ORG 节点、回溯也落回自己 → owner_item 无对应官职，
            #   此时**不得**退化为「按名字取首个」，否则会随机挂到南京某部。
            #   判据：owner_item 不在 org_items 内即视为无语域，只记 evidence。
            if org_items and owner_item not in org_items:
                unmatched.append({"item_id": iid, "type": rtype, "evidence": pat,
                                  "window": window,
                                  "reason": "关系条无可定位机构语域（卷首总述类），"
                                            "不配对"})
                continue
            # 标记词本身要去掉，避免把「贰」「佐」当官职片段
            widow_before = window[:window.find(pat)] if pat in window else window
            parsed = parse_offices(widow_before)
            if len(parsed) < 2:
                unmatched.append({"item_id": iid, "type": rtype, "evidence": pat,
                                  "window": window, "reason": "窗口内官职名不足 2 个"})
                continue
            # 主官 = 窗口内**第一个**官职名（句首主语＝被佐者）；
            # 佐者 = 其余（通常紧邻标记词，即「佐之」的执行者）。
            #
            # ⚠ 例外：「首领官」不适用句首主语规则。
            #   原文「明初，设主事、司务各四人，**为首领官**」＝ 主事、司务**二者皆是**
            #   首领官（并列同位），并非「主事为首、司务为领」。此时**不成对**
            #   （两条边方向语义都不成立），只记 evidence 待人工判。
            if rtype == "首领":
                unmatched.append({"item_id": iid, "type": rtype, "evidence": pat,
                                  "window": window,
                                  "reason": "首领官为并列同位（A、B 皆为首领官），"
                                            "无上下级方向，不成边"})
                continue
            # ⚠ 例外二：「兼领之」的主语可以是**人**而非官职。
            #   原文「命兵部尚书于谦兼领之」——兼领者是「于谦」（人），
            #   「兵部尚书」只是其本职。故本句不能解为官职边，须跳过。
            #   判据：标记词前 14 字内出现「命/以…」施动句式。
            if rtype == "兼领" and re.search(r"[命以][^，。]{0,16}$",
                                            widow_before):
                unmatched.append({"item_id": iid, "type": rtype, "evidence": pat,
                                  "window": window,
                                  "reason": "兼领主语为人（「命X兼领之」），非官职边"})
                continue
            leader_name = parsed[0][1]
            sub_names = [nm for _i, nm in parsed[1:]]
            # 主官必须是一个**真实在编的官职节点**，且不能是机构名误匹配。
            # ⚠ 同名官职跨机构多义（尚书/侍郎/郎中 等 113 个名字被多机构共用），
            #   故**优先按 owning_item 定位**（职掌条回溯到同机构编制条 = 同一语域），
            #   而非按名字取首个 —— 否则「兵部侍郎佐之」会错挂到「南京吏部」。
            # ⚠ 其次：「左、右侍郎」在 packages 里已拆为 office_parts=[左侍郎,右侍郎]，
            #   节点名是**拆后**的；而原文关系句里写的是**合称**「侍郎」。
            #   故匹配须**同时接受**精确名、拆后部件名、以及「合称去掉左右前缀」的基名
            #   （否则「侍郎佐之」永远找不到节点，6 条尚书/侍郎边全丢）。
            def _cands(name):
                base = re.sub(r"^(左|右)", "", name)
                return {name, base}

            lc = []
            for n in officials:
                if owner_item in n["item_ids"] and (
                        n["office"] in _cands(leader_name)
                        or sub_base_match(n["office"], leader_name)):
                    lc.append(n)
            if not lc:
                lc = [n for n in officials
                      if n["office"] == leader_name and iid in n["item_ids"]]
            if not lc:
                lc = [n for n in officials if n["office"] == leader_name]
            # 优先取有机构归属者，其次品级较高者
            lc.sort(key=lambda n: (not bool(n["org_id"]), n["grade_order"]))
            leader = lc[0]
            # 纪律：主官不得是纯机构名误匹配（如「兼领之」窗口抓到的「副使各一人」）
            if "各" in leader_name or "一人" in leader_name:
                unmatched.append({"item_id": iid, "type": rtype, "evidence": pat,
                                  "window": window,
                                  "reason": "主官名疑似非官职: %s" % leader_name})
                continue
            for sn in sub_names:
                # 佐者同样不得是含「各/一人」的短语片段
                if "各" in sn or "一人" in sn:
                    unmatched.append({"item_id": iid, "type": rtype, "evidence": pat,
                                      "window": window,
                                      "reason": "佐者名疑似非官职: %s" % sn})
                    continue
                # 副贰/首领关系的被佐者必须与主官**同机构**（用户定义：不跨机构）。
                # 同样接受合称/拆名互认（原文「侍郎」↔ 节点「左侍郎/右侍郎」）。
                sc = [n for n in officials
                      if sub_base_match(n["office"], sn)
                      and n["org_id"] == leader["org_id"]]
                if not sc and not leader["org_id"]:
                    sc = [n for n in officials if sub_base_match(n["office"], sn)]
                if not sc:
                    unmatched.append({"item_id": iid, "type": rtype, "evidence": pat,
                                      "window": window,
                                      "reason": "被佐者 %s 与主官 %s 非同机构或无节点"
                                                % (sn, leader_name)})
                    continue
                sc.sort(key=lambda n: n["grade_order"])
                subj = sc[0]
                if subj["official_id"] == leader["official_id"]:
                    continue
                out.append({
                    "official_id": subj["official_id"],
                    "type": rtype,
                    "target": leader["official_id"],
                    "target_office": leader["office"],
                    "org_id": leader["org_id"],
                    "evidence": "%s（原文：%s）" % (pat, window.strip()[:80]),
                    "item_id": iid,
                })

    # 回填到 officials
    by_id = {n["official_id"]: n for n in officials}
    for n in officials:
        n["relations"] = []
        n["subordinates"] = []
    for e in out:
        t = by_id.get(e["official_id"])
        if t is not None:
            t["relations"].append({k: e[k] for k in
                                   ("type", "target", "target_office", "org_id",
                                    "evidence", "item_id")})
    for e in out:
        t = by_id.get(e["target"])
        if t is not None:
            t["subordinates"].append(e["official_id"])
    return out, unmatched
