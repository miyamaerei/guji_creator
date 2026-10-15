# -*- coding: utf-8 -*-
"""
baihua_to_trl.py ──《福惠全书》/《政学录》白话文 → TRL 古今翻译层 转换器
================================================================================
依据《00-book-knowledge-factory/references/layer-library.md》§C5 古今翻译层（TRL）规范：
  - schema: trl_id / item_id / translation / style / note / confidence / original / norm
  - ID 前缀：TRL-（全局唯一，只属本层）
  - 翻译风格枚举：直译 / 意译 / 注释性翻译
  - 产出：_layers/trl_NN.json（按卷切分），全卷式全书记译本（卷为单位 .md）

适用范围
--------
本脚本针对以下两个项目（白话文条目与原条目 1:1 对齐）：
  - fuhuiquanshu-kb（福惠全书）：每条目以 ○<标题> 起始，白话文直接接续
  - xuezhenglu-kb（政学录）：分两种卷型
      * 卷01（"mixed"型）：顶层 header（内阁/六部/科道/吏部/户部/.../工部）
        + △xxx 子条目，○xxx 为嵌套结构（不计条目的 unit 部分）。
        同时首段存在"共享【译文】块"——一段【译文】覆盖多个条目
        （如 4 段 → 内阁/六部/科道 三条目，按段落切分）。
      * 卷02~05（"circle"型）：仅 ○xxx 作为条目边界，每条目独立【译文】。

设计纪律
--------
- 不改 original / norm（来自 _item_registry.json 的指纹库）
- 翻译风格默认「注释性翻译」（两书皆为官箴/政书，余光中风格基准）
- confidence 统一记 "high"（用户既已逐条翻译，默认高置信）
- 覆盖校验：翻译数 ≤ 条目数（xzl 中"六部""科道"等纯结构条目无独立译文，正常）
- 一条目一译文：fqh 直接按 ○ 切分；xzl 按 registry 匹配 section header

用法
----
  python baihua_to_trl.py --project fuhuiquanshu
  python baihua_to_trl.py --project xuezhenglu
  python baihua_to_trl.py --project both          # 两个项目都处理
  python baihua_to_trl.py --project xuezhenglu --volumes 01
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================
# 路径常量
# ============================================================
REPO_ROOT = Path(r"E:/git/ToolBox/guji")

PROJECTS = {
    "fuhuiquanshu": {
        "kb_dir": REPO_ROOT / "fuhuiquanshu-kb",
        "baihua_dir_name": "白话文",
        "layer_subdir": "trl",
        "layer_prefix": "trl_",
        "book_title": "福惠全书",
        "parser": "fqh",
    },
    "xuezhenglu": {
        "kb_dir": REPO_ROOT / "xuezhenglu-kb",
        "baihua_dir_name": "白话文",
        "layer_subdir": "trl",
        "layer_prefix": "trl_",
        "book_title": "政学录",
        "parser": "xzl",
    },
}

DEFAULT_STYLE = "注释性翻译"
DEFAULT_NOTE = "白话文初翻（注释性翻译·余光中风格基准）"
DEFAULT_CONFIDENCE = "high"
BUILDER_VERSION = "v1.0"


# ============================================================
# 中文数字 → int（卷号解析：卷之一→1, 卷之三十二→32）
# ============================================================
_CN_DIGIT = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
              "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def cn2int(s: str) -> int:
    """中文数字串转 int（支持 一/十/百/千/万 简单组合）。"""
    if not s:
        return 0
    if s.isdigit():
        return int(s)
    total = 0
    cur = 0
    for ch in s:
        if ch in _CN_DIGIT:
            cur = _CN_DIGIT[ch]
        elif ch == "十":
            cur = cur if cur else 1
            total += cur * 10
            cur = 0
        elif ch == "百":
            total += cur * 100
            cur = 0
        elif ch == "千":
            total += cur * 1000
            cur = 0
        elif ch == "万":
            total = (total + cur) * 10000
            cur = 0
    return total + cur


def pad2(n: int) -> str:
    return f"{n:02d}"


# ============================================================
# 卷号解析（从文件名取卷号 NN）
# ============================================================
def parse_volume_number(filename: str, project_key: str) -> Optional[int]:
    """从白话文文件名解析卷号 NN；解析失败返回 None（应跳过）。"""
    name = filename.replace("_白话.txt", "").replace(".txt", "")

    if project_key == "fuhuiquanshu":
        if name in {"凡例", "自序", "目录"}:
            return 0  # 归卷 00
        if name == "禀启附":
            return 33  # 禀启附为卷 33
        m = re.match(r"^卷之(.+)$", name)
        if m:
            return cn2int(m.group(1))

    if project_key == "xuezhenglu":
        m = re.match(r"^政学录·卷(.+)$", name)
        if m:
            return cn2int(m.group(1))

    return None


# ============================================================
# fuhuiquanshu 解析：按 ○<标题> 切条目
# ============================================================
_FQH_O_RE = re.compile(r"^○\s*(.+)$")


def parse_fqh_volume(text: str) -> List[Tuple[str, str]]:
    """fqh 白话文 → [(header, body), ...]
    每条目从 ○<标题> 开始，到下一个 ○<标题> 之前结束。
    ◆ / △ 等结构标记不作为条目切分点（属于条目的子结构）。
    """
    items: List[Tuple[str, str]] = []
    cur_header: Optional[str] = None
    cur_body: List[str] = []

    def flush():
        nonlocal cur_header, cur_body
        if cur_header is not None:
            body = "\n".join(cur_body).strip()
            if body:
                items.append((cur_header, body))
        cur_header = None
        cur_body = []

    for line in text.splitlines():
        m = _FQH_O_RE.match(line.strip())
        if m:
            flush()
            cur_header = m.group(1).strip()
            cur_body = []
            continue
        if cur_header is not None:
            cur_body.append(line)

    flush()
    return items


# ============================================================
# xuezhenglu 解析（两种卷型）
# ============================================================
# 卷01（mixed）：内阁 / 六部 / 科道 / 吏部 / 户部 / 礼部 / 兵部 / 刑部 / 工部 / 内阁大学士 / 翰林院 / 国子监 / 都察院
# 卷02~05（circle）：仅以 ○xxx 切分条目
#
# 关键差异：
#   - mixed 模式下 ○xxx 是嵌套结构（不计条目）；circle 模式下 ○xxx 是条目边界
#   - mixed 模式下 △xxx 是条目边界（次级条目）；circle 模式下 △xxx 不出现
#   - mixed 模式下顶层 header 也是条目边界
#
# 卷01 的"共享【译文】块"（出现在文首）：
#   内阁段只有一个【译文】块（4 段），但需覆盖 内阁/六部/科道 三条目。
#   切分算法：当前条目拥有 max(0, N-K) 段（N=总段数, K=后续依赖条目数），
#   每个依赖条目 1 段。本卷此处 N=4, K=2, 故 内阁/六部/科道 = 2/1/1。

XZL_TOP_HEADERS = {
    "内阁", "六部", "科道",
    "吏部", "户部", "礼部", "兵部", "刑部", "工部",
    "内阁大学士", "翰林院", "国子监", "都察院",
}

XZL_TRANSLATION_MARK = "【译文】"
# 用于去掉可能的尾部方括号副标题（形如：△供状式 【俱刊板刷印者备二纸投文选司】）
_BRACKET_TAIL_RE = re.compile(r"\s*【.*】\s*$")


def _strip_bracket_tail(s: str) -> str:
    """去掉形如"xxx【yyy】"中末尾【...】部分。"""
    return _BRACKET_TAIL_RE.sub("", s).strip()


def _xzl_classify_volume(items_in_vol: List[str], registry: Dict[str, dict]) -> str:
    """根据 item_registry 中本卷条目的首行 marker 模式，返回卷型。"""
    o_count = tri_count = plain_count = 0
    for iid in items_in_vol:
        h = registry[iid].get("original", "").split("\n", 1)[0].strip()
        if h.startswith("○"):
            o_count += 1
        elif h.startswith("△"):
            tri_count += 1
        else:
            plain_count += 1
    if tri_count > 0:
        return "mixed"  # 卷01
    if o_count > 0:
        return "circle"  # 卷02-05
    if plain_count > 0:
        return "plain"  # 兜底
    return "empty"


def parse_xzl_volume(text: str, pattern: str) -> List[Tuple[str, str, bool]]:
    """xzl 白话文 → [(header, body, has_own_translation), ...]

    pattern = "mixed"  → 顶层 header + △xxx 为条目边界；○xxx 是嵌套内容
    pattern = "circle" → ○xxx 为条目边界
    pattern = "plain"  → 顶层 header 为条目边界（兜底）
    """
    lines = text.splitlines()
    sections: List[Tuple[str, List[str], bool]] = []
    cur_header: Optional[str] = None
    cur_body: List[str] = []
    cur_has_trl: bool = False

    def flush():
        nonlocal cur_header, cur_body, cur_has_trl
        if cur_header is not None:
            sections.append((cur_header, cur_body[:], cur_has_trl))
        cur_header = None
        cur_body = []
        cur_has_trl = False

    for line in lines:
        s = line.strip()
        if not s:
            if cur_header is not None and cur_body and cur_body[-1] != "":
                cur_body.append("")  # 保留空行作为段落分隔
            continue

        # —— 检测是否为条目边界 ——
        is_boundary = False
        header_text: Optional[str] = None

        if pattern == "circle":
            m = re.match(r"^○(.+)$", s)
            if m:
                is_boundary = True
                header_text = "○" + _strip_bracket_tail(m.group(1))
        elif pattern == "mixed":
            if s in XZL_TOP_HEADERS:
                is_boundary = True
                header_text = s
            else:
                m = re.match(r"^△(.+)$", s)
                if m:
                    is_boundary = True
                    header_text = _strip_bracket_tail(m.group(1))
        else:  # plain
            if s in XZL_TOP_HEADERS:
                is_boundary = True
                header_text = s

        if is_boundary:
            flush()
            cur_header = header_text
            cur_body = []
            cur_has_trl = False
            continue

        if cur_header is None:
            continue

        # —— 【译文】标记 ——
        if s == XZL_TRANSLATION_MARK:
            cur_has_trl = True
            continue

        # —— nested sub-header（mixed 模式下 ○xxx/◆xxx 不切分）——
        if pattern == "mixed" and (s.startswith("○") or s.startswith("◆")):
            if cur_body and cur_body[-1] != "":
                cur_body.append("")
            cur_body.append(line.rstrip())
            continue

        cur_body.append(line.rstrip())

    flush()
    return [(h, "\n".join(b).strip(), t) for h, b, t in sections]


def _split_paragraphs(text: str) -> List[str]:
    """把一段文本按空行切成段落（保留段落顺序）。"""
    paragraphs: List[str] = []
    cur: List[str] = []
    for line in text.splitlines():
        if line.strip() == "":
            if cur:
                paragraphs.append("\n".join(cur).strip())
                cur = []
        else:
            cur.append(line)
    if cur:
        paragraphs.append("\n".join(cur).strip())
    return [p for p in paragraphs if p]


# ============================================================
# 工具：读 registry、收集卷号
# ============================================================
def load_registry(kb_dir: Path) -> Dict[str, dict]:
    with open(kb_dir / "_item_registry.json", "r", encoding="utf-8") as f:
        return json.load(f)


def registry_volumes(registry: Dict[str, dict]) -> List[str]:
    return sorted({k[:2] for k in registry.keys()})


def registry_item_header(registry: Dict[str, dict], item_id: str) -> str:
    """从 item_registry 提取某条目的 section header（original 第一行，去前导符号）。"""
    first_line = registry[item_id].get("original", "").split("\n", 1)[0].strip()
    # 去掉前导 ○/△/◆
    m = re.match(r"^[△○◆]?(.+)$", first_line)
    base = m.group(1).strip() if m else first_line
    # 去掉可能的尾部【...】注释
    return _strip_bracket_tail(base)


# ============================================================
# 主流程
# ============================================================
def build_volume(project_key: str, vol_no: int, registry: Dict[str, dict],
                 verbose: bool = True) -> List[dict]:
    """为指定卷构建 TRL 记录列表。"""
    cfg = PROJECTS[project_key]
    kb_dir = cfg["kb_dir"]
    baihua_dir = kb_dir / cfg["baihua_dir_name"]
    layer_dir = kb_dir / "_layers" / cfg["layer_subdir"]
    layer_dir.mkdir(parents=True, exist_ok=True)

    # 找 baihua 文件
    baihua_file = _find_baihua_file(baihua_dir, vol_no, project_key)
    if baihua_file is None:
        if verbose:
            print(f"  [卷{pad2(vol_no)}] 未找到白话文文件，跳过")
        return []

    text = baihua_file.read_text(encoding="utf-8")

    # 解析
    if cfg["parser"] == "fqh":
        parsed = parse_fqh_volume(text)
        records = _build_records_fqh(parsed, registry, vol_no)
    elif cfg["parser"] == "xzl":
        vol_str = pad2(vol_no)
        items_in_vol = sorted(k for k in registry.keys() if k.startswith(vol_str + "-"))
        pattern = _xzl_classify_volume(items_in_vol, registry)
        if verbose:
            print(f"  [卷{pad2(vol_no)}] xzl 卷型 = {pattern}（条目 {len(items_in_vol)} 个）")
        parsed = parse_xzl_volume(text, pattern)
        records = _build_records_xzl(parsed, registry, vol_no, pattern)
    else:
        raise ValueError(f"unknown parser: {cfg['parser']}")

    # 写 JSON
    layer_path = layer_dir / f"{cfg['layer_prefix']}{pad2(vol_no)}.json"
    payload = {
        "layer": "trl",
        "volume": pad2(vol_no),
        "name": cfg["book_title"],
        "count": len(records),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "builder": BUILDER_VERSION,
        "records": records,
    }
    with open(layer_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    if verbose:
        print(f"  [卷{pad2(vol_no)}] 写出 {len(records)} 条 → {layer_path.name}")

    # 写全卷记译本
    _write_full_translation_md(layer_dir, vol_no, records, project_key, verbose)

    return records


def _find_baihua_file(baihua_dir: Path, vol_no: int, project_key: str) -> Optional[Path]:
    # 卷 00 特殊（fqh 有 自序/凡例/目录）
    if vol_no == 0:
        for name in ["自序_白话.txt", "凡例_白话.txt", "目录_白话.txt"]:
            p = baihua_dir / name
            if p.exists():
                return p
        return None
    for f in sorted(baihua_dir.glob("*_白话.txt")):
        if parse_volume_number(f.name, project_key) == vol_no:
            return f
    return None


def _build_records_fqh(parsed: List[Tuple[str, str]], registry: Dict[str, dict],
                        vol_no: int) -> List[dict]:
    """fqh：parsed 已是 [(○header, body), ...]；按顺序对齐 item_registry。"""
    vol_str = pad2(vol_no)
    item_ids = sorted([k for k in registry.keys() if k.startswith(vol_str + "-")])
    records: List[dict] = []

    for idx, (header, body) in enumerate(parsed):
        if idx >= len(item_ids):
            break
        item_id = item_ids[idx]
        rec = _make_record(item_id, registry[item_id], body, vol_no)
        records.append(rec)
    return records


def _build_records_xzl(parsed: List[Tuple[str, str, bool]], registry: Dict[str, dict],
                        vol_no: int, pattern: str) -> List[dict]:
    """xzl：按 section header 精确匹配 item_registry；共享【译文】块按段落切分。

    切分逻辑（解决"一段【译文】块包含多个相邻条目"的情况）：
      - 顺序遍历 parsed
      - 若当前 section 有 own 【译文】 → 取其 body 作为本 section 译文；
        同时把 body 按空行拆段
      - 若当前 section 无 own 【译文】 → 已被前一个【译文】块"预分配"
      - "预分配"规则：对于有 own 【译文】 的 section S（含 N 段），
        向后扫描 registry 直到下一个 independent 条目（即"有自己的【译文】"
        的条目）；中间的 dependent 条目均参与切分（K 个）
        → S 取前 max(0, N-K) 段，每个 dependent 1 段（按 registry 顺序）
    """
    vol_str = pad2(vol_no)
    items_in_vol = sorted([k for k in registry.keys() if k.startswith(vol_str + "-")])
    item_header: Dict[str, str] = {iid: registry_item_header(registry, iid) for iid in items_in_vol}

    header_to_item: Dict[str, str] = {}
    for iid in items_in_vol:
        header_to_item.setdefault(item_header[iid], iid)

    # 第一遍：把 parsed section 映射到 item_id
    # section_index_to_item[sec_idx] = item_id (or None)
    section_item: Dict[int, Optional[str]] = {}
    used: set = set()
    fallback_ptr = 0
    for idx, (header, _body, _has_trl) in enumerate(parsed):
        item_id = header_to_item.get(header)
        if item_id is not None and item_id in used:
            item_id = None
        if item_id is None:
            while fallback_ptr < len(items_in_vol) and items_in_vol[fallback_ptr] in used:
                fallback_ptr += 1
            if fallback_ptr < len(items_in_vol):
                item_id = items_in_vol[fallback_ptr]
                fallback_ptr += 1
        if item_id is not None:
            used.add(item_id)
        section_item[idx] = item_id

    # 第二遍：对每段有 own 【译文】 的 section，做段落分配
    # translation_of[item_id] = str
    translation_of: Dict[str, str] = {}
    # 当前 section 的 idx 在 registry 中的位置（用于向后扫描）
    item_index: Dict[str, int] = {iid: i for i, iid in enumerate(items_in_vol)}

    for idx, (header, body, has_trl) in enumerate(parsed):
        if not has_trl:
            continue
        item_id = section_item.get(idx)
        if item_id is None:
            continue
        paragraphs = _split_paragraphs(body)
        N = len(paragraphs)
        if N == 0:
            continue

        # 向后扫描找出 dependent items（在遇到 independent 之前的所有"无 own 【译文】"条目）
        # independent = 自身在 parsed 中有 anchor AND 该 anchor 的 section 有 own 【译文】
        # 但实际上对于"下一个有 anchor 且有 own 【译文】 的 section"之前的，都是 dependent
        dependents: List[str] = []
        cur_pos = item_index[item_id] + 1
        while cur_pos < len(items_in_vol):
            next_iid = items_in_vol[cur_pos]
            # 找到 next_iid 在 parsed 中的 section idx
            next_sec_idx = None
            for s_idx, mapped_iid in section_item.items():
                if mapped_iid == next_iid:
                    next_sec_idx = s_idx
                    break
            # 如果 next_iid 不在 parsed 中（无 anchor），视为 dependent
            # 如果 next_iid 在 parsed 中但该 section 无 own 【译文】，也视为 dependent
            # 如果 next_iid 在 parsed 中且该 section 有 own 【译文】，视为 independent（停止）
            if next_sec_idx is not None:
                _, _, n_has_trl = parsed[next_sec_idx]
                if n_has_trl:
                    break  # 独立条目，停止
            dependents.append(next_iid)
            cur_pos += 1

        K = len(dependents)
        # 分配段落
        if N >= K:
            first_count = N - K
            if first_count > 0:
                translation_of[item_id] = "\n\n".join(paragraphs[:first_count])
            for j, dep_iid in enumerate(dependents):
                translation_of[dep_iid] = paragraphs[first_count + j]
        else:
            # 段落不足：每个 dependent 1 段，前面的吃满
            for j in range(N):
                p_iid = items_in_vol[item_index[item_id] + 1 + j]
                translation_of[p_iid] = paragraphs[j]
            # 当前 item 没分到，标记空
            translation_of[item_id] = ""

    # 兜底：未分配的条目（无 own 【译文】 且未被前段预分配）→ 留空
    for iid in items_in_vol:
        translation_of.setdefault(iid, "")

    # 第三遍：构造 records
    records: List[dict] = []
    for iid in items_in_vol:
        trl = translation_of.get(iid, "").strip()
        if not trl:
            continue  # 跳过空翻译
        rec = _make_record(iid, registry[iid], trl, vol_no)
        records.append(rec)

    return records


def _make_record(item_id: str, payload: dict, translation: str, vol_no: int) -> dict:
    original = payload.get("original", "").strip()
    norm = payload.get("norm", "").strip()
    # trl_id 全局顺序：卷号*1000 + 序号
    mm = re.match(r"^(\d{2})-(\d+)$", item_id)
    if mm:
        seq = int(mm.group(1)) * 1000 + int(mm.group(2))
    else:
        seq = 0
    return {
        "trl_id": f"TRL-{seq:04d}",
        "item_id": item_id,
        "volume": pad2(vol_no),
        "translation": translation.strip(),
        "style": DEFAULT_STYLE,
        "note": DEFAULT_NOTE,
        "confidence": DEFAULT_CONFIDENCE,
        "original": original,
        "norm": norm if norm else original,
    }


def _write_full_translation_md(layer_dir: Path, vol_no: int,
                                records: List[dict], project_key: str,
                                verbose: bool = True):
    cfg = PROJECTS[project_key]
    full_dir = layer_dir / "全书记译本"
    full_dir.mkdir(parents=True, exist_ok=True)
    out_path = full_dir / f"{pad2(vol_no)}_全书记译本.md"

    lines: List[str] = [
        f"# 《{cfg['book_title']}》{pad2(vol_no)} 现代文译本",
        "",
        f"> 共 {len(records)} 条（TRL 注释性翻译·余光中风格）",
        "",
    ]
    for r in records:
        lines.append(f"### {r['item_id']}")
        lines.append("")
        lines.append(r["translation"])
        if r.get("note"):
            lines.append("")
            lines.append(f"> 注：{r['note']}")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    if verbose:
        print(f"  [卷{pad2(vol_no)}] 全卷记译本 → 全书记译本/{out_path.name}")


# ============================================================
# CLI
# ============================================================
def main():
    ap = argparse.ArgumentParser(
        description="白话文 → TRL 古今翻译层 转换器（fuhuiquanshu-kb / xuezhenglu-kb）",
    )
    ap.add_argument(
        "--project",
        choices=list(PROJECTS.keys()) + ["both"],
        default="both",
        help="要处理的项目（默认 both）",
    )
    ap.add_argument(
        "--volumes",
        nargs="*",
        default=None,
        help="仅处理指定卷号（NN，如 01 02 33）",
    )
    args = ap.parse_args()

    targets = [args.project] if args.project != "both" else list(PROJECTS.keys())
    for project_key in targets:
        cfg = PROJECTS[project_key]
        registry = load_registry(cfg["kb_dir"])
        vols = registry_volumes(registry)
        if args.volumes:
            vols = [v for v in vols if v in [pad2(int(x)) for x in args.volumes]]
        print(f"\n=== 《{cfg['book_title']}》共 {len(vols)} 卷 ===")
        for v in vols:
            build_volume(project_key, int(v), registry)
    print("\n完成。")


if __name__ == "__main__":
    main()