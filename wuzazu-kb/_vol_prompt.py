# -*- coding: utf-8 -*-
"""按卷扇出的装填提示词生成器 —— 从代码自动派生，取代 34K 静态 skill 包。

为什么要自动生成
----------------
旧做法每个 agent 都要完整读 `wuzazu-knowledge/SKILL.md`(12021) +
`references/schemas.md`(11551) + `translation-style.md`(5769) +
`volume-profile.md`(5177) ≈ **34.5K 字符**，而这些内容里真正每次用到的只有：
字段清单与枚举取值。这两样本来就在代码里（`_kg_layers.ENGINE` 与 `_kg_enums`），
**从代码生成提示词 = 永不漂移 + 每次只发该卷需要的部分**。

用法：
    python _vol_prompt.py 01            # 打印卷01 的完整装填提示词（直接喂给 AI）
    python _vol_prompt.py01 --save      # 存到 _build/_prompt_01.md
    python _vol_prompt.py --all --save  # 全部 17 卷批量生成
    python _vol_prompt.py 01 --compact  # 省略枚举明细（极省 token，装填员熟手用）

成本对比（每卷）：
    旧：34.5K skill 包 × 11 层 = 379K 字符/卷
    新：本文件生成 ≈ 6~9K 字符/卷（枚举按需裁剪），且只发 1 次
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

import _kg_enums as E  # noqa: E402
from _kg_pack_base import (  # noqa: E402
    UNKNOWN,
    VOLUME_MODE_HINT,
    VOLUME_NAME,
    extract_path,
    read_text,
    write_text,
)
from _vol_schema import LAYERS, TUPLE_FIELDS  # noqa: E402

# 层 -> 一句话职责（写提示词用，比读 34K 文档省）
LAYER_ROLE: dict[str, str] = {
    "ent": "实体词表：人/地/书/官职/年号/名物等，原文出现的词形逐个登记",
    "event": "事件五元组：类型、主体、动作、事由、时、地",
    "rel": "人物关系：师生/举荐/弹劾/同僚/姻亲/同乡/父子亲属/恩怨等",
    "nam": "名录谱牒：长寿/巨富/异相/科第等表格式罗列",
    "cit": "引书索引：作者引了哪些书、直引转引、暗用考辨（本书最大特征）",
    "obj": "名物考据：物部四卷为主，形制/产地/用途/时节",
    "cus": "方言风俗：各地俗语、禁忌、节令、物产习俗",
    "opn": "作者论说：余谓/予以为/吾郡等主观见解与论证",
    "ming": "明代纪事：涉明条目与作者亲历（与 event 分工：ming 只索引，细节交 event）",
    "appt": "职官任职：授/擢/迁/除/罢/谪/致仕等任职表述",
    "trl": "古今翻译：每条一译，白话要点式，忠实原意、专名保留",
}

# 每层的必填字段（来自 _kg_pack_base.LAYERS.must_fields，去掉自动注入的）
MUST: dict[str, tuple[str, ...]] = {
    "event": ("type", "who", "action", "what", "when", "where"),
    "rel": ("person_a", "person_b", "relation_type", "direction", "evidence"),
    "nam": ("name", "category", "scope", "entries"),
    "cit": ("cited_work", "citation_type", "context"),
    "obj": ("name", "category", "attributes", "lore"),
    "cus": ("type", "region", "term", "description"),
    "opn": ("topic", "stance", "argument"),
    "ming": ("era", "who", "what", "when", "where", "category", "first_person"),
    "appt": ("person", "office", "institution", "when", "status", "evidence"),
    "trl": ("translation", "style"),
}

ENUMS: dict[str, tuple[str, ...]] = {
    "ent": ("entity_type",),
    "event": ("event_type",),
    "rel": ("relation_type", "relation_direction"),
    "nam": ("nam_category",),
    "cit": ("citation_type", "citation_context"),
    "obj": ("obj_category",),
    "cus": ("cus_type",),
    "opn": ("opn_stance",),
    "ming": ("ming_category",),
    "appt": ("appt_status",),
    "trl": ("trl_style",),
}

# 枚举字段 -> 枚举名（从 _kg_layers.ENGINE 派生，避免手写漂移）
FIELD_ENUM: dict[str, dict[str, str]] = {
    "ent": {"type": "entity_type"},
    "event": {"type": "event_type"},
    "rel": {"relation_type": "relation_type", "direction": "relation_direction"},
    "nam": {"category": "nam_category"},
    "cit": {"citation_type": "citation_type", "context": "citation_context"},
    "obj": {"category": "obj_category"},
    "cus": {"type": "cus_type"},
    "opn": {"stance": "opn_stance"},
    "ming": {"category": "ming_category"},
    "appt": {"status": "appt_status"},
    "trl": {"style": "trl_style"},
}


def _enum_line(field: str, enum_name: str) -> str:
    vals = E.canonical_values(enum_name)
    return f"  - {field}（{enum_name}）：{' / '.join(vals)}"


def _tuple_hint(layer: str) -> str:
    fields = TUPLE_FIELDS.get(layer)
    if not fields:
        return ""
    names, optional = fields
    parts = []
    for i, name in enumerate(names):
        mark = "?" if optional == name else ""
        parts.append(f"{name}{mark}")
    return "、".join(parts)


def build_prompt(volume: str, *, compact: bool = False) -> str:
    """生成单卷装填提示词。"""
    name = VOLUME_NAME.get(volume, "")
    mode = VOLUME_MODE_HINT.get(volume, "均衡全层")
    text_file = extract_path(volume)

    out: list[str] = []
    add = out.append

    add(f"# 《五杂俎》卷{volume}（{name}）知识装填")
    add("")
    add(f"## 任务")
    add("")
    add(f"把卷{volume}（{name}）的正文解析为知识图谱的 11 层数据。")
    add(f"**本卷阅读模式**：{mode} —— 优先在该模式下材料更密的层多下功夫，稀疏层宁缺毋滥。")
    add("")
    add("**关键约束（务必遵守，直接影响成本与正确性）**：")
    add("")
    add("1. **一次产全部 11 层**。不要为不同层分别作答，也不要分多轮输出——"
        "整卷只读一次，11 层写在同一个 `SRC` 字典里。")
    add("2. **不写业务 ID**（ENT-/WZZ-E-/REL-… 全由打包器分配）。")
    add("3. **不写原文**：不抄 `original`/`norm`（由指纹库注入），不写 `volume`（由文件名推导）。")
    add("4. **引用字段只写词形**：如 `who: \"汉明帝\"`，**不要**写 `who_ent_ids`——"
        "跨层回填由打包器统一做，这是你能在一次调用里把 11 层写完的前提。")
    add(f"5. **未考处显式写 `\"{UNKNOWN}\"`**，不留空、不省略键。")
    add("6. **没有材料的层整个键省略**，不要写空 list，更不要为凑数造记录。")
    add("7. 枚举字段必须用下面给出的规范值（旧写法如 主从/政事/军务/科第/office/book 会自动归一，但直接写规范值更省事）。")
    add("")
    add("## 输出格式")
    add("")
    add("输出必须是**可执行的 Python 源码**，UTF-8，只含一个代码块：")
    add("")
    add("```python")
    add('"""卷' + volume + f"（{name}）统一卷源 —— 11 层一次装填""")
    add("")
    add("SRC = {")
    add('"NN-001": {')
    add('    "ent": [("汉明帝", "person")],')
    add('    "event": [{"type": "轶事", "who": "汉明帝", "action": "嘲张重",')
    add('               "what": "以日南郡人应北向看日相嘲", "when": "未明", "where": "未明"}],')
    add('    "cit": [("后汉书", "直引", "考源")],')
    add('    "trl": "白话译文……",')
    add("},")
    add("}")
    add("```")
    add("")
    add("约定：外层 key 是条号（`NN-001`），内层 key 是层名。紧凑元组的字段顺序见下表。")
    add("")

    add("## 11 层字段契约")
    add("")
    for layer in LAYERS:
        add(f"### {layer} —— {LAYER_ROLE[layer]}")
        must = MUST.get(layer, ())
        add("")
        if must:
            add(f"必填：{'、'.join(must)}")
        else:
            add("字段：text（原文词形）、type（枚举）")
        hint = _tuple_hint(layer)
        if hint:
            add(f"紧凑元组写法：`{hint}`（省token，推荐）")
        if not compact:
            for field, enum_name in FIELD_ENUM.get(layer, {}).items():
                add(_enum_line(field, enum_name))
        add("")

    add("## 枚举速查（全部规范值）")
    add("")
    if compact:
        add("（--compact 模式省略；需要时查 `_kg_enums.py` 或去掉本参数重新生成）")
    else:
        for enum_name in E.enum_names():
            if enum_name == "volume_mode":
                continue
            add(f"- **{enum_name}**：{' / '.join(E.canonical_values(enum_name))}")
    add("")

    add("## 原文")
    add("")
    add(f"文件：`{text_file}`")
    add("（每行一条：`条号|正文`；按条号顺序逐条解析）")
    add("")
    if text_file.exists():
        text = read_text(text_file)
        n_items = sum(1 for line in text.split("\n")
                      if line.strip() and line.partition("|")[0].strip())
        add(f"共 {n_items} 条。原文较长时分段处理，但**产出必须合并进同一个 SRC 字典**后再落盘。")
    add("")

    add("## 落盘与校验")
    add("")
    add(f"1. 写入 `_src/_vol_{volume}.py`（可用 `_mk_vol.py` 自动校验并摊平）")
    add(f"2. `python _vol_prompt.py {volume} --save` 可重看本提示词")
    add(f"3. `python _vol_schema.py split --volumes {volume}` 摊平成 11 个分层文件")
    add(f"4. `python build_all.py --volumes {volume}` 打包 + 验证")
    add("")
    add("## 自检清单（落盘前逐条确认）")
    add("")
    add("- [ ] 外层 key 全部存在于 `_item_registry.json`（条号不臆造）")
    add("- [ ] 没有任何业务 ID 字段（ENT-/WZZ-E-/REL- 等）")
    add("- [ ] 没有任何 `original` / `norm` / `volume` 键")
    add("- [ ] 没有任何 `*_ent_ids` 键（引用只写词形）")
    add(f"- [ ] 未考处写的是 `\"{UNKNOWN}\"`，不是空串或省略")
    add("- [ ] 枚举值都在速查表里")
    add("- [ ] 空层的键整个省略，没有空 list 占位")
    add("- [ ] 文件是合法 Python（`python -m py_compile` 能过）")
    add("")
    return "\n".join(out)


def main() -> None:
    args = [a for a in sys.argv[1:]]
    compact = "--compact" in args
    save = "--save" in args
    args = [a for a in args if not a.startswith("--")]

    if args and args[0] != "--all":
        vols = [a.zfill(2) for a in args]
    else:
        vols = [v for v in VOLUME_NAME if v != "00"]

    for vol in vols:
        text = build_prompt(vol, compact=compact)
        if save:
            out = ROOT / "_build" / f"_prompt_{vol}.md"
            out.parent.mkdir(parents=True, exist_ok=True)
            write_text(out, text)
            print(f"[写出] {out}（{len(text):,} 字符）")
        else:
            print(text)
            print("\n" + "=" * 68 + "\n")


if __name__ == "__main__":
    main()