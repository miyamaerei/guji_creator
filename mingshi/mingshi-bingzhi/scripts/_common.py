# -*- coding: utf-8 -*-
"""
打包器公共基座（兵志实例 `scripts/_common.py`）
=============================================

由工厂 `assets/skeletons/packer_skeleton.py` 复制而来（Phase ③ 实例化）。
职责与工厂版一致：把 references/error-taxonomy.md 中 A / B / G / P 四族
（全部工程侧、与书内容无关的错误）在骨架层面一次性消除。

四条纪律（继承工厂，勿删护栏）：
1. 没有报错 ≠ 有数据：任何「填充率 0 / 某层 0 条 / 覆盖率异常偏低」必须给出解释。
2. 命名四处同源：目录名 / 文件名前缀 / 索引槽位名 / schema 键名共用 LAYER_SPECS。
3. ID 分配权归打包器：AI 源数据只写槽位，永不手写业务 ID（子节点同样走分配器）。
4. 写盘一律「临时文件 + rename」；共享文件增量合并，绝不从空字典重建。

兵志实例定制（相对工厂版）：
- LAYER_SPECS 只列 8 个启用层（ents/regs/weis/tmes/opns/rules/objs/structs），
  与 SKILL.md §1.1 及 references/schemas/bz_schemas.json 严格同源。
- ID_PREFIX 扩展至 10 个（含兵志专属 REG-/WEI-/OPN-/OBJ-/EVO-/QUAN-/REW-）。
- assert_unique_ids 增加 WEI- 豁免：C17 卫所树节点（_layers/weis/）与 L4 卫所编制
  记录（_layers/structs/）共用 WEI- 前缀是**设计如此**（SKILL.md §6.4/§11.3），
  跨层以 (layer, wei_id) 二元组消歧，不做撞号误报。
- cn2int 自检样本改用兵志实测串（含约数后缀），覆盖坑 #48/#64。
"""

from __future__ import annotations

import io
import json
import os
import re
import sys
import tempfile
from collections import Counter, OrderedDict

# =============================================================================
# 0. 路径配置
# =============================================================================

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PATHS = {
    "root": ROOT,
    "source": os.path.join(ROOT, "assets", "sources"),  # 源文件（唯一权威来源）
    "extract": os.path.join(ROOT, "_extract"),  # 条目切分产物
    "chapters": os.path.join(ROOT, "chapters"),  # 章节文件
    "layers": os.path.join(ROOT, "_layers"),  # 各层落盘目录（复数）
    "views": os.path.join(ROOT, "_views"),  # 查询视图
    "data": os.path.join(ROOT, "_data"),  # 报表/待核清单
    "registry": os.path.join(ROOT, "_item_registry.json"),
    "join": os.path.join(ROOT, "_kg_join.json"),
}

# =============================================================================
# 1. 命名单点治理（B 族：目录名 / 文件名前缀 / 索引槽位名 / schema 键名四处同源）
# =============================================================================
#
# 只在这里声明一次，所有地方都引用它。三元组 (dir_name, slot_key, list_key)
# 三者同源，全部用复数，与 _layers/<dir>/ 物理目录一致。
# 兵志实例：8 个启用层（SKILL.md §1.1；不建 L3/L5/NAM/C1/C16）。

LAYER_SPECS = [
    ("ents", "ents", "ents"),  # L1 实体层
    ("regs", "regs", "regs"),  # REG 制度层
    ("weis", "weis", "weis"),  # C17 卫所树层（bz 型核心）
    ("tmes", "tmes", "tmes"),  # C14 时间沿革层
    ("opns", "opns", "opns"),  # C9 论说层
    ("rules", "rules", "rules"),  # L2 规则层
    ("objs", "objs", "objs"),  # OBJ 名物层（薄层）
    ("structs", "structs", "structs"),  # L4 四维（EVO/QUAN/WEI/REW 同目录分文件）
]

# 源数据模块名模板：scripts/_<kind>_ai_<NN>.py（NN = 卷号，可带 b/c 后缀分片）
SRC_MODULE_PATTERN = "_{kind}_ai_{vol}{suffix}"

# ID 前缀（与实例 scripts/_kg_enums.py 中的 ID_PREFIX 保持同源；此处为兜底示例）
ID_PREFIX = {
    "ent": "ENT-",
    "rule": "RULE-",
    "reg": "REG-",
    "wei": "WEI-",
    "tme": "TME-",
    "opn": "OPN-",
    "obj": "OBJ-",
    "evo": "EVO-",
    "quan": "QUAN-",
    "rew": "REW-",
}

# 段容量：按「卷条数 × 单层最大扩展系数」预留（卷66 卫列树节点量级大，沿用 500）
SEG_CAPACITY = 500

# 每层记录顶层键**必须是** `records`
RECORDS_KEY = "records"


def layer_dir(name: str) -> str:
    """返回某层的物理目录路径——目录名一律取 LAYER_SPECS 的复数形。"""
    return os.path.join(PATHS["layers"], name)


def layer_files(name: str):
    """返回某层全部已落盘文件（按卷号排序）。"""
    d = layer_dir(name)
    if not os.path.isdir(d):
        return []
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".json"))


def check_naming_consistency() -> list:
    """B 族护栏：校验命名四处同源。

    检查项：
      1. 每个 slot_key 与 dir_name 一致（索引槽位名 == 目录名）
      2. 每个层目录下文件名前缀 == 目录名
      3. 每层记录顶层键 == `records`
    """
    errs = []
    for dir_name, slot_key, _list_key in LAYER_SPECS:
        name = dir_name
        if dir_name != slot_key:
            errs.append(
                "命名漂移（B 族）：层 %r 的目录名 %r != 索引槽位名 %r —— "
                "四处同源要求二者一致" % (name, dir_name, slot_key)
            )
        d = layer_dir(dir_name)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if not fn.endswith(".json"):
                continue
            stem = fn.split("_")[0]
            if stem != dir_name:
                errs.append(
                    "命名漂移（B 族）：%s/%s 文件名前缀 %r != 目录名 %r"
                    % (dir_name, fn, stem, dir_name)
                )
        for path in layer_files(dir_name):
            try:
                obj = json.load(io.open(path, encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001
                errs.append("读盘失败 %s: %s" % (path, exc))
                continue
            if RECORDS_KEY not in obj:
                errs.append(
                    "顶层键漂移（B 族）：%s 无 %r 键（实际键：%s）"
                    % (path, RECORDS_KEY, sorted(obj.keys()))
                )
    return errs


# =============================================================================
# 2. ID 分配（B 族：分配权唯一归打包器；源头 #13 / #39 / #54）
# =============================================================================
#
# 三条铁律：
#   ① 源数据只写槽位（slot），绝不手写 ID
#   ② 序号取记录全局序号 `enumerate(records, 1)`，不取 slot
#   ③ 子节点同样走本分配器（用 `<父ID>#<序号>` 派生），不得自行合成


def assign_ids(records, prefix: str, volume: str, id_field: str = "id"):
    """按「卷号 × 段容量 + 全局序号」分配业务 ID（幂等）。

    volume 取卷号字符串（"65"/"66"/"67"/"68"）；全书性专表用虚拟卷位 "00"。
    """
    try:
        base = int(volume) * SEG_CAPACITY
    except ValueError:
        base = (abs(hash(volume)) % 900 + 100) * SEG_CAPACITY
    for i, rec in enumerate(records, 1):
        rec[id_field] = "%s%0*d" % (prefix, 4, base + i)
    return records


def assign_child_ids(node, parent_id: str, id_field: str = "id"):
    """递归为**子节点**分配 ID（修 #54：分配器只作用顶层记录）。

    派生形式 `<父ID>#<序号>`。优先沿用已有 id，仅在缺失时派生——
    否则会覆盖已在别处（如 build_struct 分派的 L4-WEI 编制）派生的 ID。
    """
    children = node.get("children") or []
    for i, child in enumerate(children, 1):
        if not child.get(id_field):
            child[id_field] = "%s#%d" % (parent_id, i)
        assign_child_ids(child, child[id_field], id_field)
    return node


def assert_unique_ids(records, id_field: str = "id", exempt_prefixes=("ENT-", "WEI-")):
    """B 族护栏：ID 唯一性校验。

    - ENT- 豁免：实体层 id 是**实体主键**，同实体多条目复用同一 ID 是设计如此。
    - WEI- 豁免（兵志定制）：C17 卫所树节点（_layers/weis/）与 L4 卫所编制
      记录（_layers/structs/）共用 WEI- 前缀是设计如此（SKILL.md §6.4/§11.3），
      跨层以 (layer, wei_id) 二元组消歧，不做撞号误报。

    返回重复 ID 的列表（去重后），空列表 = 通过。
    """
    seen, dups = set(), []
    for rec in records:
        rid = rec.get(id_field)
        if not rid:
            continue
        if any(rid.startswith(p) for p in exempt_prefixes):
            continue
        if rid in seen and rid not in dups:
            dups.append(rid)
        seen.add(rid)
    return dups


# =============================================================================
# 3. 原子写盘与增量合并（G 族：幂等性 / 原子性）
# =============================================================================


def atomic_write_json(path: str, obj) -> None:
    """原子写 JSON（临时文件 + rename）。"""
    d = os.path.dirname(os.path.abspath(path)) or "."
    if not os.path.isdir(d):
        os.makedirs(d)
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    try:
        with io.open(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=1)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def atomic_write_text(path: str, text: str) -> None:
    """原子写文本（临时文件 + rename）。"""
    d = os.path.dirname(os.path.abspath(path)) or "."
    if not os.path.isdir(d):
        os.makedirs(d)
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    try:
        with io.open(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def merge_layer(name: str, volume: str, records, records_key: str = RECORDS_KEY):
    """**增量**写回某层某卷（G 族核心装置）。

    语义：只替换该卷的记录，其余卷原样保留——`--volumes 66` 重跑不会
    影响 65/67/68 的数据，更不会截断共享文件。
    """
    path = os.path.join(layer_dir(name), "%s_%s.json" % (name, volume))
    payload = OrderedDict()
    payload["volume"] = volume
    payload[records_key] = list(records)
    atomic_write_json(path, payload)
    return path


def merge_shared_json(path: str, new_items, key_field=None, sort_key=None):
    """增量合并**共享** JSON（如指纹库、跨层索引）。

    先读已有文件 → 用 `key_field` 做键增量更新 → 原子写回。绝不从空字典重建。
    """
    old = {}
    if os.path.exists(path):
        try:
            obj = json.load(io.open(path, encoding="utf-8"))
            if isinstance(obj, dict):
                old = obj
            elif isinstance(obj, list):
                if not key_field:
                    raise ValueError(
                        "merge_shared_json：已有文件是列表，必须提供 key_field 才能合并"
                    )
                old = {
                    it.get(key_field): it
                    for it in obj
                    if isinstance(it, dict) and it.get(key_field)
                }
        except Exception:  # noqa: BLE001
            old = {}

    if isinstance(new_items, dict):
        old.update(new_items)
    else:
        if not key_field:
            raise ValueError("merge_shared_json：new_items 是序列时必须提供 key_field")
        for it in new_items:
            if not isinstance(it, dict):
                continue
            k = it.get(key_field)
            if k:
                old[k] = it

    if sort_key:
        out = OrderedDict((k, old[k]) for k in sorted(old.keys(), key=sort_key))
    else:
        out = OrderedDict(sorted(old.items()))
    atomic_write_json(path, out)
    return out


# =============================================================================
# 4. 字段填充率体检（A 族核心装置——本骨架最重要的一段）
# =============================================================================


class FieldCoverage:
    """字段填充率统计器（A 族装置）。

    兵志用法::

        cov = FieldCoverage("regs")
        for rec in records:
            cov.count_record(rec, fields=["geo_ref", "num_value", "num_semantic",
                                          "src_loc", "cross_ref", "mil_class"])
        cov.report("_data/regs/coverage_regs.txt",
                   zero_explanations={"mil_class": "该条制度无军事类别归属"})

    交付要求：填充率为 0 的字段**必须逐条给出解释**。
    """

    def __init__(self, layer_name: str):
        self.layer = layer_name
        self.total = 0
        self.filled = Counter()
        self.fields = []

    def count_record(self, rec, fields=None, nested=None):
        """统计单条记录的字段填充情况。

        nested : str | None —— 字段藏在嵌套键下时指定（如 spec 内的 material）。
        """
        self.total += 1
        if fields:
            for f in fields:
                if f not in self.fields:
                    self.fields.append(f)
                if nested:
                    items = rec.get(nested) or []
                    if any(
                        (it.get(f) not in (None, "", [], {}))
                        for it in items
                        if isinstance(it, dict)
                    ):
                        self.filled[f] += 1
                else:
                    if rec.get(f) not in (None, "", [], {}):
                        self.filled[f] += 1

    def rates(self):
        """返回 {字段: (已填, 总数, 百分比)}。"""
        out = {}
        for f in self.fields:
            n = self.filled[f]
            pct = (n / self.total * 100) if self.total else 0.0
            out[f] = (n, self.total, pct)
        return out

    def report(self, path=None, zero_explanations=None):
        """产出填充率表。`zero_explanations` 为 {字段: 零值原因} 时必须提供。"""
        lines = [
            "字段填充率体检 —— 层：%s（共 %d 条记录）" % (self.layer, self.total),
            "=" * 64,
            "%-28s %8s %8s %8s" % ("字段", "已填", "总数", "填充率"),
            "-" * 64,
        ]
        zero_fields = []
        for f, (n, tot, pct) in self.rates().items():
            flag = ""
            if n == 0:
                flag = "  <- 零填充，须解释"
                zero_fields.append(f)
            lines.append("%-28s %8d %8d %7.1f%%%s" % (f, n, tot, pct, flag))
        if zero_fields:
            lines.append("")
            lines.append("零填充字段解释（A 族要求：0 值必须给出原因，不允许沉默）：")
            for f in zero_fields:
                why = (zero_explanations or {}).get(f)
                if why:
                    lines.append("  - %s：%s" % (f, why))
                else:
                    lines.append(
                        "  - %s：**未解释** —— 排查顺序："
                        "① 回填器是否被 build 脚本真正调用 → "
                        "② 解析覆盖面是否漏组（复合句/超长行）→ "
                        "③ 最后才接受「原文没有」" % f
                    )
        text = "\n".join(lines) + "\n"
        if path:
            atomic_write_text(path, text)
        return text, zero_fields


def assert_no_silent_zero(coverage_report, layer_name: str):
    """A 族护栏：任何零填充字段都必须有解释，否则报 ERR。"""
    _text, zero_fields = coverage_report
    if zero_fields:
        raise AssertionError(
            "A 族静默失败：层 %s 有 %d 个字段零填充且未解释：%s\n"
            "排查顺序：① 回填器是否被调用 → ② 解析覆盖面 → ③ 原文是否真没有。\n"
            "若确属「原文没有」，请在 FieldCoverage.report(zero_explanations=...) "
            "中显式登记原因。" % (layer_name, len(zero_fields), zero_fields)
        )


# =============================================================================
# 5. 语义闸门（P 族：锚定位置，不用全串匹配）
# =============================================================================


class SemanticGate:
    """语域闸门：判断某条目是否属于指定语域（P 族装置）。

    只在**原文开头**（前 `head_chars` 字）匹配关键词，避免正文同形词污染。
    兵志重点应用：判「卫列行走」/「都司行」锚定行首。
    """

    def __init__(self, keywords, head_chars: int = 60):
        self.keywords = tuple(keywords)
        self.head_chars = head_chars
        self.hits, self.misses = [], []

    def match(self, item_id: str, original: str) -> bool:
        head = (original or "")[: self.head_chars]
        ok = any(k in head for k in self.keywords)
        (self.hits if ok else self.misses).append(item_id)
        return ok

    def report(self):
        return "语域闸门：命中 %d 条 / 未命中 %d 条（关键词 %s，匹配窗口=前 %d 字）" % (
            len(self.hits),
            len(self.misses),
            self.keywords,
            self.head_chars,
        )


# =============================================================================
# 6. 探查终止条件（P 族 #1：最高频的坑）
# =============================================================================


class ProbeTracker:
    """探查跟踪器：给定「设计结论指纹」的函数，自动判定是否应收口。"""

    def __init__(self, fingerprint_fn, stage_name: str = "探查"):
        self.fp = fingerprint_fn
        self.stage = stage_name
        self.history = []

    def settle(self, design) -> bool:
        """登记一次设计结论；返回 True 表示**应收口**（连续两次未变）。"""
        cur = self.fp(design)
        self.history.append(cur)
        if len(self.history) >= 2 and self.history[-1] == self.history[-2]:
            print(
                "[%s] 连续两次读取未改变设计结论 → 达终止条件，停止探查（P 族 #1）"
                % self.stage
            )
            return True
        return False


# =============================================================================
# 7. 枚举单点治理（P 族 / D 族：封闭枚举不得就地吸收）
# =============================================================================


def check_enum(values, allowed, layer: str, field: str, pending_sink=None) -> list:
    """枚举值校验（**不中断**，收集未匹配值）。

    pending_sink : dict | None —— {layer.field: Counter(未匹配值)}，
    收集后由主流程统一输出 pending 表（收集-报告-暂存模式，坑 #15）。
    """
    bad = Counter(v for v in values if v not in allowed)
    if bad and pending_sink is not None:
        pending_sink.setdefault("%s.%s" % (layer, field), Counter()).update(bad)
    return sorted(bad)


def drift_ratio(values, allowed) -> float:
    """枚举漂移率 = 库外值种数 / 库内值种数；> 1.5 判漂移（坑 #27）。"""
    used_out = set(v for v in values if v not in allowed)
    denom = len(allowed) or 1
    return len(used_out) / denom


# =============================================================================
# 8. 收尾总校验（所有 build_* 的最后一步调用）
# =============================================================================


def run_guardrails(name: str, errs=None, gap=0):
    """统一收尾：命名一致性 + 打印统计 + 非零退出。"""
    errs = list(errs or [])
    errs.extend(check_naming_consistency())
    print("OK %s ERR=%d GAP=%d" % (name, len(errs), gap))
    for e in errs:
        print("  ERR:", e)
    if errs:
        sys.exit(1)
    return 0


# =============================================================================
# 9. 交付前：目标查询问句逐问验收（A 族根治手段 #50）
# =============================================================================


def query_acceptance(questions, path=None):
    """目标查询问句验收表。

    questions : list[dict]
        [{"q": "某卫隶属沿革", "layer": "weis", "answer": "...",
          "status": "能答"|"半答"|"答不了", "note": "..."}]
    """
    lines = [
        "目标查询问句验收表（A 族 #50：先有问句清单，才有字段设计）",
        "=" * 72,
        "%-4s %-34s %-16s %-8s" % ("#", "问句", "承载层", "结果"),
        "-" * 72,
    ]
    stat = Counter()
    for i, item in enumerate(questions, 1):
        st = item.get("status", "未测")
        stat[st] += 1
        lines.append(
            "%-4d %-34s %-16s %-8s"
            % (i, item.get("q", "")[:34], item.get("layer", "")[:16], st)
        )
        if item.get("note"):
            lines.append("     注：%s" % item["note"])
    lines.append("-" * 72)
    total = sum(stat.values()) or 1
    lines.append(
        "合计 %d 问：%s（答不出比例 %.0f%%）"
        % (
            total,
            " / ".join("%s %d" % (k, v) for k, v in stat.most_common()),
            stat.get("答不了", 0) / total * 100,
        )
    )
    lines.append("")
    lines.append(
        "凡「答不了」须分类：① 原文确无（属正常，须写明）／"
        "② 结构缺陷（字段/关联缺失，须回填修复）。"
    )
    text = "\n".join(lines) + "\n"
    if path:
        atomic_write_text(path, text)
    return text, stat


# =============================================================================
# 10. 文本工具（小工具，多书通用）
# =============================================================================


def norm_text(s: str) -> str:
    """归一化原文：去空白、统一标点（按实例需要扩展）。"""
    if not s:
        return ""
    s = s.replace("\u3000", " ").replace("\r", "").replace("\n", "")
    s = re.sub(r"\s+", "", s)
    return s.strip()


CN_DIGITS = {
    "〇": 0,
    "零": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}
CN_UNITS = {"十": 10, "百": 100, "千": 1000, "万": 10000}


def cn2int(s: str):
    """中文数字转整数（P 族 #48/#64：量纲前缀、约数后缀、纪年兼容）。

    兵志实测入参：
        「一千四十四」→ 1044（量纲前缀：千 作用于 四十四）
        「十六万」    → 160000
        「七万七百余」→ 70700（约数标记 余 剔除）
        「四百三十馀万束」→ 4300000（夹在数字中间的 馀 剔除）
        「卫三百八十四」→ 384（尾部单位 卫 剥离）
        「洪武三年」  → 3（年号前缀跳过，尾锚定 三年 → 3）
    返回 None 一律当**错误**处理，不得静默当 0（坑 #48/#64）。
    """
    if not s:
        return None
    s = s.strip()
    if re.fullmatch(r"\d+", s):
        return int(s)
    # ① 先剥「有奇 / 有馀 / 有余」——整体是约数标记，不参与数值
    core = re.sub(r"(有奇|有馀|有余)$", "", s)
    # ② 剔除夹在数字中间的约数标记（位置不固定）：馀/余/奇/众/许/数 不贡献量值
    core = re.sub(r"[馀余奇众许数]", "", core)
    # ③ 再剥尾部量词与单位（可重复剥离）
    tail_re = re.compile(
        r"(年|月|日|石|斗|升|合|勺|人|员|名|匹|疋|端|两|斤|钱|分|厘"
        r"|贯|文|锭|顷|亩|引|束|间|所|个|卫|等)$"
    )
    for _ in range(4):
        new = tail_re.sub("", core)
        if new == core:
            break
        core = new
    core = core.strip()
    if not core:
        return None
    # ④ 尾部向前截取连续中文数字串，跳过「洪武」「永乐」这类年号前缀
    m = re.search(r"[〇零一二三四五六七八九十百千万]+$", core)
    if not m:
        return int(core) if re.fullmatch(r"\d+", core) else None
    s = m.group(0)
    if not s:
        return None
    total, section, number = 0, 0, 0
    for ch in s:
        if ch in CN_DIGITS:
            number = CN_DIGITS[ch]
        elif ch in CN_UNITS:
            unit = CN_UNITS[ch]
            if unit == 10000:
                coeff = number if (number or section) else 1
                section = (section + coeff) * unit
                total += section
                section, number = 0, 0
            else:
                section += (number or 1) * unit
                number = 0
        else:
            break
    return total + section + number


# =============================================================================
# 自检：直接运行本文件时打印骨架状态（样本用兵志实测串）
# =============================================================================

if __name__ == "__main__":
    print("兵志实例打包器基座 scripts/_common.py")
    print("=" * 64)
    print("启用层 LAYER_SPECS:", [t[0] for t in LAYER_SPECS])
    print("命名一致性:", check_naming_consistency() or "通过")
    print("cn2int 自检（样本须含约数后缀，坑 #64）：")
    for probe in [
        "一千四十四",
        "十六万",
        "七万七百余",
        "四百三十馀万束",
        "卫三百八十四",
        "洪武三年",
        "十三万二千馀石",
        "万",
    ]:
        print("  %-12s -> %s" % (probe, cn2int(probe)))
