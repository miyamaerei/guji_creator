# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— 卷脚手架（scaffold_volume）
=====================================================
为指定卷生成 8 层 AI 源数据模板（sources/_<layer>_ai_NN.py）：
- 从指纹库提取该卷全部条目清单（条号+原文），供 AI 逐条填写
- 每层模板含：字段结构 + 示例记录 + 填写说明
- 幂等：已存在不覆盖（--force 可覆盖重建）

用法：
  python scaffold_volume.py --volumes 01
  python scaffold_volume.py --volumes 17 --force
"""
import argparse
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from _kg_enums import (APPT_STATUS, ENTITY_TYPES, EVENT_TYPES, LIT_TYPES,
                       NAM_TYPES, REG_TYPES, REL_DIRECTIONS, REL_TYPES,
                       TRL_STYLES)

LAYER_META = {
    "ent": {
        "title": "L1 实体标注",
        "doc": "实体标注：每条记录标注该条目中的实体（text=原文字面，type=实体类型，normalized=归一词形，confidence=置信度）",
        "keys": ["text", "type", "normalized", "confidence", "source"],
        "example": '{"item_id": "01-001", "text": "礼部尚书", "type": "official", "normalized": "礼部尚书", "confidence": 0.97, "source": "原文片段"}',
        "enums": ENTITY_TYPES,
    },
    "appt": {
        "title": "APPT 职官任职",
        "doc": "任职记录：person(人物含 person_ent_ids)/office(官职含 official_ent_ids)/institution(机构含 ent_ids)/when(时间，未明写'未明')/status(任职状态)/evidence(证据)",
        "keys": ["appointment_id", "item_id", "person", "office", "institution", "when", "status", "evidence", "confidence"],
        "example": '{"appointment_id": "APPT-001", "item_id": "01-004", "person": {"text": "汪澄", "person_ent_ids": ["ENT-xxx"]}, "office": {"text": "巡按御史", "official_ent_ids": ["ENT-xxx"]}, "institution": {"text": "福建（巡按）", "ent_ids": ["ENT-xxx"]}, "when": "正统十三年", "status": "现任", "evidence": "巡按御史汪澄将至延平", "confidence": 0.92}',
        "enums": APPT_STATUS,
    },
    "event": {
        "title": "L5 事件",
        "doc": "事件五元组：who(含 who_ent_ids)/action/what/when/where；未明字段显式写'未明'",
        "keys": ["event_id", "item_id", "type", "who", "action", "what", "when", "where"],
        "example": '{"event_id": "SDJ-E-001", "item_id": "01-001", "type": "礼仪", "who": {"text": "礼部鸿胪寺及科道导驾等官", "who_ent_ids": ["ENT-xxx"]}, "action": "导驾陞奉天殿受朝", "what": "冬至正旦节早朝仪节", "when": "冬至正旦节早", "where": "左掖门→中左门→华盖殿→奉天殿"}',
        "enums": EVENT_TYPES,
    },
    "reg": {
        "title": "REG 典章制度",
        "doc": "制度记录：name/type/content(摘要)/institutions(机构 ent_ids)/officials(职官 official_ent_ids)；一条目多项制度拆多条共享 item_id",
        "keys": ["reg_id", "item_id", "name", "type", "content", "institutions", "officials", "confidence"],
        "example": '{"reg_id": "REG-001", "item_id": "01-001", "name": "冬至正旦节早朝仪节", "type": "朝仪", "content": "礼部鸿胪寺及科道导驾等官先入左掖门……", "institutions": ["ENT-xxx"], "officials": ["ENT-xxx"], "confidence": 0.95}',
        "enums": REG_TYPES,
    },
    "lit": {
        "title": "LIT 文献资产",
        "doc": "文献记录：title(篇名，无则取首句)/author(含 author_ent_ids；佚名写'未明')/type/content_location(所在卷条目定位)",
        "keys": ["lit_id", "item_id", "title", "author", "type", "content_location", "confidence"],
        "example": '{"lit_id": "LIT-001", "item_id": "19-001", "title": "洪武元年戒谕衍圣公孔克坚圣旨", "author": {"text": "朱元璋", "author_ent_ids": ["ENT-xxx"]}, "type": "诏敕圣旨", "content_location": "卷十九首条", "confidence": 0.97}',
        "enums": LIT_TYPES,
    },
    "rel": {
        "title": "REL 人物关系",
        "doc": "关系记录：person_a/person_b(含各自 ent_ids)/relation_type/direction(单向/双向/未明)/evidence；只建文本有直接证据的关系，宁缺毋滥",
        "keys": ["rel_id", "item_id", "person_a", "person_b", "relation_type", "direction", "evidence", "confidence"],
        "example": '{"rel_id": "REL-001", "item_id": "01-004", "person_a": {"text": "姚铣", "person_a_ent_ids": ["ENT-xxx"]}, "person_b": {"text": "汪澄", "person_b_ent_ids": ["ENT-xxx"]}, "relation_type": "弹劾", "direction": "单向", "evidence": "兵科给事中姚铣等以为澄畏避且忌嫉当言之", "confidence": 0.9}',
        "enums": REL_TYPES,
    },
    "nam": {
        "title": "NAM 名录谱牒（结构分类）",
        "doc": "名录记录：name/category/scope/entries(四元组数组 {seq,person,courtesy_name,hometown,office})/ent_ids；书信中仅提及族谱者 entries 空数组+evidence 注明",
        "keys": ["nam_id", "item_id", "name", "category", "scope", "entries", "ent_ids", "confidence"],
        "example": '{"nam_id": "NAM-001", "item_id": "17-002", "name": "都御史题名（天顺、景泰末年）", "category": "官员题名", "scope": "都察院·都御史（左/右/副/佥都御史）", "entries": [{"seq": 1, "person": "杨善", "courtesy_name": "未明", "hometown": "未明", "office": "左都御史（天顺）"}], "ent_ids": ["ENT-xxx"], "confidence": 0.95}',
        "enums": NAM_TYPES,
    },
    "trl": {
        "title": "TRL 古今翻译",
        "doc": "翻译记录：translation(现代译文)/style(默认'注释性翻译'·余光中风格)/note(难点/异文/专名处理)；全量逐条（条目数=翻译数）",
        "keys": ["trl_id", "item_id", "translation", "style", "note", "confidence"],
        "example": '{"trl_id": "TRL-001", "item_id": "01-001", "translation": "冬至、正旦两节清晨……", "style": "注释性翻译", "note": "长句拆并联短句；专名括注", "confidence": 0.93}',
        "enums": TRL_STYLES,
    },
}


def enum_doc(enums):
    return " / ".join(f"{k}={v}" for k, v in enums.items())


def gen_template(layer, vol_no, items, force=False):
    meta = LAYER_META[layer]
    path = os.path.join(common.SOURCES_DIR, f"_{layer}_ai_{vol_no}.py")
    if os.path.exists(path) and not force:
        return False, path
    lines = [
        "# -*- coding: utf-8 -*-",
        f'"""《水东日记》卷 {vol_no} —— {meta["title"]} 源数据（AI 判定逐条填写）',
        "",
        f'说明：{meta["doc"]}',
        "",
        "字段说明：",
        "  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）",
        "  * 枚举（封闭+兜底）：" + enum_doc(meta["enums"]),
        "  * 未建模条目在下方注释中如实单列，不强行编造",
        "",
        "填写方式：把 DATA 中的示例记录替换为本卷实际判定结果；",
        "         每条记录为一个 dict；未判定条目保留注释占位。",
        '"""',
        "",
        "ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）",
    ]
    for item_id, body in items:
        lines.append(f'    "{item_id} | {body[:30]}",')
    lines += [
        "]",
        "",
        "# 字段键（打包器校验用）：" + ", ".join(meta["keys"]),
        "# 示例记录（保留作格式对照）：",
        f"# {meta['example']}",
        "",
        "DATA = [",
        "    # 在此逐条填写判定结果，例如：",
        "    # {",
        f"    #     {meta['example']}",
        "    # },",
        "    # 未判定的条目请在此处注释登记缺口，例如：",
        '    # "缺口": "XX-XXX 未建模（原因）",',
        "]",
        "",
    ]
    common.write_text(path, "\n".join(lines))
    return True, path


def main():
    ap = argparse.ArgumentParser(description="卷脚手架：生成某卷 8 层源数据模板")
    ap.add_argument("--volumes", nargs="+", required=True, help="卷号，如 01 17")
    ap.add_argument("--force", action="store_true", help="覆盖已存在模板")
    args = ap.parse_args()

    reg = common.load_registry()
    created, skipped = 0, 0
    for vol_no in args.volumes:
        if vol_no not in [f"{i:02d}" for i in range(0, 39)]:
            print(f"[跳过] 非法卷号 {vol_no}")
            continue
        items = [(i, reg[i]["original"]) for i in sorted(reg) if i.startswith(vol_no + "-")]
        for layer in LAYER_META:
            ok, path = gen_template(layer, vol_no, items, force=args.force)
            if ok:
                created += 1
                print(f"[创建] {os.path.basename(path)}（{len(items)} 条条目清单）")
            else:
                skipped += 1
                print(f"[跳过] {os.path.basename(path)} 已存在（--force 覆盖）")
    print(f"\n完成：创建 {created} 个模板，跳过 {skipped} 个。")


if __name__ == "__main__":
    main()
