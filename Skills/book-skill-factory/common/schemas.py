# -*- coding: utf-8 -*-
"""book-skill-factory common/schemas.py

structure.json 数据契约（唯一真源）与校验。

结构配置承载「目录 -> 卷 -> 标题 -> 段落」四级识别所需的全部规则，
由 HEURISTICS.md 六组启发式问题的答案翻译而来；参考模板代码不写死任何判定。
"""

DEFAULT_VOLUME_PATTERN = {
    # kind:
    #   "regex_match" -> 卷标记形态有规律（如 "# 卷一" / "<!-- **卷X** -->" / "卷一"），
    #                    pattern 给正则列表（正文区只启用严格整行形态，防误伤）
    #   "fixed_list"  -> 卷名无规律，按 names 顺序出现的位置切分
    #   "none"        -> 不分卷（整本单卷）
    "kind": "regex_match",
    "pattern": [
        r"^\s*#\s*卷[一二三四五六七八九十百零〇0-9]+\s*$",
        r"<!--\s*\*\*卷[一二三四五六七八九十百零〇0-9]+\*\*\s*-->",
    ],
    "names": [],
}


def default_layout():
    """与客座赘语形态一致的默认布局（作为新书起点，等待问询答案覆盖）。"""
    return {
        "toc_anchor": {
            "pattern": r"<!--\s*\*\*目录\*\*\s*-->",
            "end_exclusive": r"<!--\s*\*\*卷一\*\*\s*-->",
        },
        "body_anchor": {"pattern": r"<!--\s*\*\*卷一\*\*\s*-->"},
        "volume_pattern": {
            k: (list(v) if isinstance(v, list) else v)
            for k, v in DEFAULT_VOLUME_PATTERN.items()
        },
        "heading_kind": "h2",  # h1|h2|h3|plain|none（none=整卷无标题）
        "heading_pattern": r"^##+(?!#)\s*(.+?)\s*$",
        "keep_pages": False,
        "omit_lines": [],
        "strip_artifacts": True,
    }


REQUIRED_KEYS = ["toc_anchor", "body_anchor", "volume_pattern", "heading_kind"]


def validate_structure(cfg):
    """校验结构配置是否满足解析运行所需。返回 (ok: bool, errors: [str])。"""
    errors = []
    if not isinstance(cfg, dict):
        return False, ["structure.json 顶层必须是对象"]
    for key in REQUIRED_KEYS:
        if key not in cfg:
            errors.append("缺少必需配置: %s" % key)
    vp = cfg.get("volume_pattern") or {}
    kind = vp.get("kind")
    if kind == "fixed_list" and not vp.get("names"):
        errors.append("volume_pattern.kind=fixed_list 时 names 不能为空")
    if kind == "regex_match" and not vp.get("pattern"):
        errors.append("volume_pattern.kind=regex_match 时 pattern 不能为空")
    hk = cfg.get("heading_kind")
    if hk not in (None, "h1", "h2", "h3", "plain", "none"):
        errors.append("heading_kind 应为 h1|h2|h3|plain|none，当前: %r" % hk)
    return (len(errors) == 0), errors
