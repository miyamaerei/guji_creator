# -*- coding: utf-8 -*-
"""
打包器公共骨架（Packer Skeleton）—— 工厂 v13 起随实例复制
=========================================================

本文件是「书实例 skill」在 Phase ③ 实例化时**应当复制进实例 `scripts/` 目录**的
公共基座。它把 `references/error-taxonomy.md` 中 **A / B / G / P 四族**（= 65 条坑里
的 29 条，约 46%）——也就是**全部工程侧、与书内容无关的错误**——在骨架层面一次性消除。

四族与本骨架的对应关系
----------------------
| 族 | 错误模式 | 本骨架的消除装置 |
|---|---|---|
| A | 「校验通过」≠「数据可用」（静默失败） | `FieldCoverage` 填充率表 / `assert_no_silent_zero()` / 问句验收表 |
| B | 键名·ID·编号没有单一来源 | `NAMING` 单点命名表 / `assign_ids()` 唯一分配权 / `LAYER_SPECS` 三元组同源 |
| G | 写盘幂等性与原子性缺失 | `atomic_write_json()` / `merge_layer()` 增量合并 / `idempotent()` 校验 |
| P | 流程与语境失配 | `probe()` 终止条件 / `enums.py` 单点枚举 / `SemanticGate` 锚定匹配 |

使用方式（实例化时）
--------------------
1. 复制本文件为实例 `scripts/_common.py`（可改名），按实例情况填 `PATHS`。
2. **不要删除任何护栏函数**——它们的存在就是为了让错误「出声」。
   如某护栏确实不适用，须在实例 SKILL.md 写明理由，而不是静默删掉。
3. 每个 `build_*.py` 打包器最后一行调用 `run_guardrails()`。

设计原则（三句话）
------------------
1. **没有报错 ≠ 有数据**：任何「填充率 0 / 某层 0 条 / 覆盖率异常偏低」都必须给出解释。
2. **命名四处同源**：目录名 / 文件名前缀 / 索引槽位名 / schema 键名共用一个常量表。
3. **ID 分配权归打包器**：源数据只写槽位，永不手写业务 ID。
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
# 0. 路径配置——实例化时按实际情况修改
# =============================================================================

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PATHS = {
    "root": ROOT,
    "source": os.path.join(ROOT, "assets", "sources"),   # 源文件（唯一权威来源）
    "extract": os.path.join(ROOT, "_extract"),           # 条目切分产物
    "chapters": os.path.join(ROOT, "chapters"),          # 章节文件
    "layers": os.path.join(ROOT, "_layers"),             # 各层落盘目录（复数！见 B 族）
    "views": os.path.join(ROOT, "_views"),               # 查询视图
    "data": os.path.join(ROOT, "_data"),                 # 报表/待核清单
    "registry": os.path.join(ROOT, "_item_registry.json"),
    "join": os.path.join(ROOT, "_kg_join.json"),
}

# =============================================================================
# 1. 命名单点治理（B 族：目录名 / 文件名前缀 / 索引槽位名 / schema 键名四处同源）
# =============================================================================
#
# B 族的根因是「同一个名字在 4 个地方各写一份」，单复数/前缀一旦漂移就静默失配
# （#28 跨层索引 7 层静默空回填、#29 adapter 漏扫 7 层、#19 annotations vs records、
#  #23 源 chr vs 容器 chrs）。
#
# 对策：**只在这里声明一次**，所有地方都引用它。
# LAYER_SPECS 是三元组（目录名, 索引槽位名, 记录列表键名）——三者同源，永不手写字符串。

# (dir_name, slot_key, list_key) —— 全部用**复数**，与 _layers/<dir>/ 物理目录一致
# (dir_name, slot_key, list_key) —— 全部用**复数**，与 _layers/<dir>/ 物理目录一致
# 《明史·选举志》xjz 完整型（11 层 + L5 事件层），2026-10-14 锁定方案：
#   L1 实体 / L2 规则 / REG 制度(★骨架) / L3 流程(科举三级) /
#   L4 四维(EVO·QUAN·INST) / C14 时间沿革 / C9 论说 /
#   NAM 名录 / FRD 防弊(科场弊案) / OBJ 名物(薄层) / L5 事件
# APPT 任职不单列层，以 REG.cross_kb 跨库联动《明史·职官志》；底座与跨层索引非 LAYER_SPECS 项。
LAYER_SPECS = [
    ("ents",    "ents",    "records"),   # L1 实体层（person/institution/school/place/era…）
    ("rules",   "rules",   "records"),   # L2 规则层（22 处"著为令/凡/不许/禁"规范性语句）
    ("regs",    "regs",    "records"),   # REG 制度层（★本书骨架，13 属性 + 选举 token）
    ("procs",   "procs",   "records"),   # L3 流程层（乡试→会试→殿试 三级 + 场次/考官）
    ("structs", "structs", "records"),   # L4 四维（EVO 沿革 / QUAN 数额 / INST 制度类型；多维同目录）
    ("tmes",    "tmes",    "records"),   # C14 时间沿革（洪武→万历 变革链）
    ("opns",    "opns",    "records"),   # C9 论说（科举利弊/掣签之议等奏议引语）
    ("nams",    "nams",    "records"),   # NAM 名录（一甲题名/考官题名/进士题名）
    ("frds",    "frds",    "records"),   # FRD 防弊·科场弊案（冒籍/倩代/关节/通榜）
    ("objs",    "objs",    "records"),   # OBJ 名物（薄层：八股/贡院/武科器械/题名碑）
    ("events",  "events",  "records"),   # L5 事件层（科场弊案始末、制度争议等叙事事件）
]

# 源数据模块名模板：scripts/_<kind>_ai_<NN>.py（NN = 卷号，可带 b/c 后缀分片）
SRC_MODULE_PATTERN = "_{kind}_ai_{vol}{suffix}"

# ID 前缀（与实例 _kg_enums.py 中的 ID_PREFIX 保持同源；此处为兜底示例）
ID_PREFIX = {
    "ent": "ENT-", "rule": "RULE-", "proc": "PROC-", "reg": "REG-",
    "tme": "TME-", "opn": "OPN-", "nam": "NAM-", "frd": "FRD-",
    "obj": "OBJ-", "evo": "EVO-", "quan": "QUAN-", "inst": "INST-",
    "evt": "EVT-",
}

# 段容量：按「卷条数 × 单层最大扩展系数」预留，不按条目数估（#22）
SEG_CAPACITY = 500

# 每层记录顶层键**必须是** `records`（#19：ent 曾用 `annotations`，与其余层不一致）
RECORDS_KEY = "records"


def layer_dir(name: str) -> str:
    """返回某层的物理目录路径——目录名一律取 LAYER_SPECS 的复数形。"""
    return os.path.join(PATHS["layers"], name)


def layer_files(name: str):
    """返回某层全部已落盘文件（按卷号排序）。"""
    d = layer_dir(name)
    if not os.path.isdir(d):
        return []
    return sorted(
        os.path.join(d, f) for f in os.listdir(d) if f.endswith(".json")
    )


def check_naming_consistency() -> list:
    """B 族护栏：校验命名四处同源。

    检查项：
      1. 每个 slot_key 与 dir_name 一致（索引槽位名 == 目录名）
      2. 每个层目录下文件名前缀 == 目录名（防 fuhuiquanshu 的 `ents/ent_01.json`）
      3. 每层记录顶层键 == `records`
    """
    errs = []
    # LAYER_SPECS 是**列表**，元素为三元组 (dir_name, slot_key, list_key)。
    # 直接 `for x in LAYER_SPECS` 拿到的是元组而非 key 字符串，故按元组解包。
    #
    # 历史教训（坑 #63）：本函数曾被改成 `for name, spec in LAYER_SPECS.items()`
    # ——那是把「遍历 dict 只得 key」的修法套在了列表上，`list` 无 `.items()`，
    # 于是从「解包崩」变成「AttributeError 崩」，**B 族核心装置依然全坏**。
    # 而自检当时把 LAYER_SPECS 替换成了 dict（self_test 里 `SK.LAYER_SPECS = {...}`），
    # 恰好喂给它一个生产环境不存在的形状 → 自检**通过**、缺陷照旧出厂。
    # 纪律：自检的数据形状必须与生产声明完全一致；不得为让测试通过而换形状。
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
            # 文件名前缀必须是目录名（复数），不允许单数
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
# 2. ID 分配（B 族：分配权唯一归打包器；源头是 #13 / #39 / #54）
# =============================================================================
#
# 血的教训：
#   #13 - AI 手写业务 ID，试点两卷即互撞（50 条规则只有 9 个唯一 ID，全撞 ZG-R-501）
#   #39 - 用 `slot`（条目内语义顺序）当全局序号，每个 item 从 1 重启 → 撞号
#   #54 - 分配器只作用顶层记录，子节点从未拿到 ID，2 个遍历器各自合成 ID 互相覆盖
#
# 三条铁律：
#   ① 源数据**只写槽位**（slot），绝不手写 ID
#   ② 序号取**记录全局序号** `enumerate(records, 1)`，不取 slot
#   ③ 子节点同样走本分配器（用 `<父ID>#<序号>` 派生），不得自行合成


def assign_ids(records, prefix: str, volume: str, id_field: str = "id"):
    """按「卷号 × 段容量 + 全局序号」分配业务 ID（幂等）。

    Parameters
    ----------
    records : list[dict]
        本卷记录。**调用前须排序**（通常按 (item_id, slot)），否则序号不稳定。
    prefix : str
        ID 前缀，如 "ENT-"。
    volume : str
        卷号字符串，如 "01" / "00"（全书性专表用虚拟卷位 "00"）。
    id_field : str
        写入哪个键（默认 "id"；部分层用 "template_id"/"official_id" 等）。

    Returns
    -------
    list[dict]
        原地写入 ID 后的同一列表（便于链式调用）。

    Notes
    -----
    - 卷位 "00" 用于**与单条无关的全书性表**（#46），段位独立不与正文卷冲突。
    - 段容量取 `SEG_CAPACITY`（按「卷条数 × 单层最大扩展系数」预留）。
    """
    try:
        base = int(volume) * SEG_CAPACITY
    except ValueError:
        # 非数字卷位（如 "00" 之外的自定义卷名）→ 取哈希兜底，保证不撞
        base = (abs(hash(volume)) % 900 + 100) * SEG_CAPACITY
    for i, rec in enumerate(records, 1):
        rec[id_field] = "%s%0*d" % (prefix, 4, base + i)
    return records


def assign_child_ids(node, parent_id: str, id_field: str = "id"):
    """递归为**子节点**分配 ID（修 #54：分配器只作用顶层记录）。

    派生形式 `<父ID>#<序号>`。

    关键：**优先沿用记录里已有的 id**，仅在缺失时才派生——否则会覆盖
    已在别处（如 build_struct）派生的 ID，造成两个遍历器 ID 空间互相覆盖。
    """
    children = node.get("children") or []
    for i, child in enumerate(children, 1):
        if not child.get(id_field):
            child[id_field] = "%s#%d" % (parent_id, i)
        assign_child_ids(child, child[id_field], id_field)
    return node


def assert_unique_ids(records, id_field: str = "id", exempt_prefixes=("ENT-",)):
    """B 族护栏：ID 唯一性校验。

    **ENT- 前缀必须豁免**：实体层的 id 是**实体主键**，同一实体在多个条目中
    复用同一个 ID 是设计如此（不是撞号）。其余层一律不得重复。

    返回重复 ID 的列表（去重后的 ID 值），空列表 = 通过。
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
#
# 血的教训：
#   #12 - build_base.py --volumes NN 从空字典重建指纹库并按卷过滤，
#         把共享指纹库从 1197 条抹成该卷条数（**单卷复跑截断共享文件**）
#   #14 - 并行子代理半写文件与汇总竞态（瞬时 ValueError）
#   #2  - 一次性修复脚本落在正式生成器之外，重跑即丢
#
# 两条纪律：
#   ① 写文件一律「临时文件 + rename 落盘」（同盘 rename 是原子操作）
#   ② 所有 build_* 脚本统一**增量语义**：`--volumes NN` 只重算该卷，
#      合并写回，**绝不覆盖**共享文件


def atomic_write_json(path: str, obj) -> None:
    """原子写 JSON（临时文件 + rename）。"""
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.isdir(d):
        os.makedirs(d)
    fd, tmp = tempfile.mkstemp(dir=d or ".", suffix=".tmp")
    try:
        with io.open(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=1)
        os.replace(tmp, path)   # 原子替换
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def atomic_write_text(path: str, text: str) -> None:
    """原子写文本（临时文件 + rename）。"""
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.isdir(d):
        os.makedirs(d)
    fd, tmp = tempfile.mkstemp(dir=d or ".", suffix=".tmp")
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

    语义：只替换该卷的记录，其余卷原样保留——`--volumes 01` 重跑不会
    影响 02..05 的数据，更不会截断共享文件。

    同时顺带修 #46：写盘循环必须覆盖**所有**已存在的卷位，
    不能只遍历本次 `vols`（否则卷 00 的记录只计数不落盘）。
    """
    path = os.path.join(layer_dir(name), "%s_%s.json" % (name, volume))
    payload = OrderedDict()
    payload["volume"] = volume
    payload[records_key] = list(records)
    atomic_write_json(path, payload)
    return path


def merge_shared_json(path: str, new_items, key_field: str = None, sort_key=None):
    """增量合并**共享** JSON（如指纹库、跨层索引）。

    先读已有文件 → 用 `key_field` 做键做增量更新 → 再原子写回。
    绝不从空字典重建。

    Parameters
    ----------
    new_items : dict | iterable
        - dict：直接按键合并（`key_field` 可为 None）
        - iterable[dict]：按 `key_field` 取值合并（此时 `key_field` 必填）
    key_field : str | None
        记录内作主键的字段名；传入 dict 时可省略。
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
            raise ValueError(
                "merge_shared_json：new_items 是序列时必须提供 key_field"
            )
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
#
# 血的教训：
#   #45 - 新增 salary_ref 字段，431/431 全空，ERR=0
#   #56 - _seal_backfill.py 写完且 import 了，但 build_struct.py **从未调用**
#         → seal 填充 0 而 ERR=0（同坑第 2 次复发 = 检查单缺失）
#   #55 - 印信表复合句解析器只取首组，覆盖 57% 不报错
#
# 核心结论：**ERR=0 只证明「值合法」，不证明「有值」。**
# 因此填充率表必须与 ERR/GAP **并列交付**。


class FieldCoverage:
    """字段填充率统计器（A 族装置）。

    用法::

        cov = FieldCoverage("structs")
        for rec in records:
            cov.count_record(rec, fields=["seal", "powers", "assess", "jurisdiction"])
        cov.report("_data/struct/coverage_structs.txt")

    交付要求：填充率为 0 的字段**必须逐条给出解释**（原文没有？还是没接线？）。
    """

    def __init__(self, layer_name: str):
        self.layer = layer_name
        self.total = 0
        self.filled = Counter()
        self.fields = []

    def count_record(self, rec, fields=None, nested=None):
        """统计单条记录的字段填充情况。

        Parameters
        ----------
        rec : dict
        fields : list[str] | None
            顶层字段名列表。
        nested : str | None
            若字段藏在某个嵌套键下（如 posts 内的 grade），在此指定，
            此时 fields 各项按 `rec[nested][i][field]` 取值。
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
                        for it in items if isinstance(it, dict)
                    ):
                        self.filled[f] += 1
                else:
                    if rec.get(f) not in (None, "", [], {}):
                        self.filled[f] += 1

    def rates(self):
        """返回 {字段: (已填, 总数, 百分比)}。"""
        out = OrderedDict()
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
                flag = "  ← 零填充，须解释"
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
                        "② 解析覆盖面是否漏组（复合句）→ "
                        "③ 最后才接受「原文没有」"
                        % f
                    )
        text = "\n".join(lines) + "\n"
        if path:
            atomic_write_text(path, text)
        return text, zero_fields


def assert_no_silent_zero(coverage_report, layer_name: str):
    """A 族护栏：任何零填充字段都必须有解释，否则报 ERR。

    这是把「静默失败」变成「出声失败」的关键闸门。
    """
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
#
# 血的教训（#47）：
#   用 `"留守司。" in scope_text` 判语域，结果 05-051（卫指挥使司条）的正文
#   含「外卫各统于都司、行都司或**留守司**。」——被误判为留守司条，漏填 3 条世官。
#
# 修法：**判语域一律锚定原文开头（startswith），不做全串子串匹配**。
# 因为「同一个词在正文里被顺带提到」与「这条讲的就是这个对象」是两回事。


class SemanticGate:
    """语域闸门：判断某条目是否属于指定语域（P 族装置）。

    只在**原文开头**（前 `head_chars` 字）匹配关键词，避免正文同形词污染。
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
        return (
            "语域闸门：命中 %d 条 / 未命中 %d 条（关键词 %s，匹配窗口=前 %d 字）"
            % (len(self.hits), len(self.misses), self.keywords, self.head_chars)
        )


# =============================================================================
# 6. 探查终止条件（P 族 #1：最高频的坑）
# =============================================================================
#
# #1「重复读取 / 反复探查」是**最高频**的坑：同一文件反复读、探查久不收口。
# 对策：**连续两次读取不再改变设计结论时立即停止**。


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
#
# #27 实测：《客座赘语》事件类型 23→111 种、文献 11→114 种、名录 **100% 库外** ——
#       封闭枚举名存实亡，因为校验器只校验「是否有值」不校验「值是否在封闭集内」。
# #15 实测：《水东日记》5 次中断（枚举校验遇未匹配值直接抛错）。
#
# 对策：**收集-报告-暂存**模式 + `check_enum()` 硬校验。
# 校验器在**打包前**阻断，未匹配值入 pending 表（不中断），收尾统一决议。


def check_enum(values, allowed, layer: str, field: str, pending_sink=None) -> list:
    """枚举值校验（**不中断**，收集未匹配值）。

    Parameters
    ----------
    values : iterable
        待校验的实际值。
    allowed : set | frozenset
        封闭枚举的合法值集合。
    pending_sink : dict | None
        {layer.field: Counter(未匹配值)}——收集后由主流程统一输出 pending 表。

    Returns
    -------
    list
        越界值列表（去重后排序）。
    """
    bad = Counter(v for v in values if v not in allowed)
    if bad and pending_sink is not None:
        pending_sink.setdefault("%s.%s" % (layer, field), Counter()).update(bad)
    return sorted(bad)


def drift_ratio(values, allowed) -> float:
    """枚举漂移率 = 库外值种数 / 库内值种数。

    #27 的告警阈值：**比值 > 1.5 判漂移**（意味着枚举定义基本没覆盖这本书）。
    """
    used_out = set(v for v in values if v not in allowed)
    denom = len(allowed) or 1
    return len(used_out) / denom


# =============================================================================
# 8. 收尾总校验（所有 build_* 的最后一步调用）
# =============================================================================


def run_guardrails(name: str, errs=None, gap=0):
    """统一收尾：命名一致性 + 打印统计 + 非零退出。

    每个 `build_*.py` 结尾都应调用本函数。
    """
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
#
# 「验收指标全绿 ≠ 能回答用户的问题」。
# ERR=0 / GAP=0 / 0 空条目测的是**层内自洽**；用户的验收是「我想知道 X 能不能查到」。
#
# 对策：**Phase ② 就产出「目标查询问句清单」并逐问标注承载层**，交付时逐问实测作答。
# 本函数提供最小装置：把问句清单与作答结果落成表，2 能答 / 3 半答 / 3 答不了
# 这类结论**必须出现在交付报告里**。


def query_acceptance(questions, path=None):
    """目标查询问句验收表。

    Parameters
    ----------
    questions : list[dict]
        [{"q": "吏部编制几人几品", "layer": "RANK/posts", "answer": "...",
          "status": "能答" | "半答" | "答不了", "note": "..."}]
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
    "〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
    "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
}
CN_UNITS = {"十": 10, "百": 100, "千": 1000, "万": 10000}


def cn2int(s: str):
    """中文数字转整数（P 族 #48：量纲前缀不得误读）。

    「一千四十四」→ 1044（**不是** 1+44，也不是 1444）。
    「一千」「一百」中的「千」「百」是**量纲前缀**，作用于其后的数字。

    **纪年兼容**：本函数常被用来解析「洪武三年」「永乐二十二年」这类纪年串。
    此时须**跳过朝代/年号前缀**（年号本身是汉字且首字多为数字字，如「洪武」
    的「洪」不是、「正德」的「正」不是，但「**永**乐」「**二**十**二**年」中
    若从头解析会因「永」非数字字而立即 break → 得 0）。
    故先剥离尾部单位字，再从后向前取连续的中文数字串解析。

    本函数是**单点实现**——数值解析一律走这里，散落实现必然漂移。

    **约数后缀兼容（坑 #64）**：史书/政书的数额**绝大多数带约数后缀**——
    「十三万二千**馀**石」「七十八万七千**馀**两」「四百三十**馀**万束」
    「十六万两**有奇**」。此类后缀若不先剥离，尾部锚定的数字串取不到
    （`馀` 非数字字，`re.search(r"[…]+$", core)` 因串尾是 `馀` 而失配）
    → **静默返回 `None`**，调用方多半把 `None` 当 0 或跳过 → 整棵总账树解析为空。
    这与 #48 是同一函数上的**第 2 次复发**：都是「数值解析的单点实现没覆盖
    真实主要入参」。故自检样本须含**带约数后缀**的实测串（见 self_test P 族）。
    """
    if not s:
        return None
    s = s.strip()
    if re.fullmatch(r"\d+", s):
        return int(s)
    # ① 先剥「有奇 / 有馀 / 有余」——它们整体是约数标记，不参与数值
    core = re.sub(r"(有奇|有馀|有余)$", "", s)
    # ② 剔除**夹在数字中间的约数标记**（位置不固定）：
    #    「三十**馀**万束」= 三十余万 = 30×10000；「万**许**」= 约一万。
    #    约数标记（馀/余/奇/众/许/数）在数值中**从不贡献量值**，一律删除。
    core = re.sub(r"[馀余奇众许数]", "", core)
    # ③ 再剥尾部量词与单位（可重复剥离，如「二千馀石」先「石」后无）
    tail_re = re.compile(
        r"(年|月|日|石|斗|升|合|勺|人|员|名|匹|疋|端|两|斤|钱|分|厘"
        r"|贯|文|锭|顷|亩|引|束|间|所|个|等)$"
    )
    for _ in range(4):
        new = tail_re.sub("", core)
        if new == core:
            break
        core = new
    core = core.strip()
    if not core:
        return None
    # ④ 从尾部向前截取**连续的中文数字串**，跳过「洪武」「永乐」这类年号前缀
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
                # 「万」的默认系数 1 只在**本段尚无任何数字**时生效
                #   「万两有奇」→ 1×10000 = 10000   （段内空）
                #   「十万」   → 10×10000 = 100000  （段内已有 10）
                #   「四百三十馀万」→ 430×10000 = 4300000
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
# 自检：直接运行本文件时打印骨架状态
# =============================================================================

if __name__ == "__main__":
    print(__doc__.split("使用方式")[0].strip()[:400])
    print()
    print("LAYER_SPECS:", LAYER_SPECS or "（未配置——实例化时按启用层填写）")
    print("命名一致性:", check_naming_consistency() or "通过")
    print("cn2int 自检：", cn2int("一千四十四"), cn2int("四十二"), cn2int("十"))
