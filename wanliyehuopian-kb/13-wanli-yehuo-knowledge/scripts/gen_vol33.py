# -*- coding: utf-8 -*-
"""
gen_vol33.py —— 《万历野获编》补遗卷三（vol 33）全量结构化抽取生成器
输出 _layers/{layer}/{layer}_33.json（顶层 JSON 数组，2 空格缩进，ensure_ascii=False）
字段风格对齐已验收样例 ents_24 / events_24 及各卷 *_25/_26 实践格式；
枚举值全部取自 scripts/_kg_enums.py。
"""
import io
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'assets', 'sources', '万历野获编.txt')
LAYERS = os.path.join(BASE, '_layers')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_enums import (  # noqa: E402
    ENTITY_TYPES, ENTRY_ROLES, FACTIONS, CONFIDENCE,
    RULE_TYPES, ACTUAL_PRACTICE,
    EVENT_TYPES, EVENT_SIGNIFICANCE, SOURCE_TYPES, VS_OFFICIAL_HISTORY,
    APPT_STATUS, CONTROVERSY,
    RELATION_TYPES, DIRECTION, EVIDENCE_STRENGTH,
    CITATION_TYPES, CITATION_PURPOSES, COMMENTARY_TYPES, TONES, FIRSTHAND,
    MING_CATEGORIES, REIGN_FOCUS,
    TME_CATEGORIES, REG_CATEGORIES, REIGN_ORDER,
)


# ---------------------------------------------------------------------------
# 卷三原文载入（按 【标题】 切分为条目，条目号与 _extract/33_补遗卷三.txt 一致）
# ---------------------------------------------------------------------------
def load_item_texts():
    with io.open(SRC, encoding='utf-8') as f:
        whole = f.read()
    start = whole.index(u'\u25cf\u8865\u9057\u5377\u4e09')
    end = whole.index(u'\u25cf\u8865\u9057\u5377\u56db')
    sec = whole[start:end]
    marks = list(re.finditer(u'\u3010([^\u3011]+)\u3011', sec))
    texts = {}
    for i, m in enumerate(marks):
        stop = marks[i + 1].start() if i + 1 < len(marks) else len(sec)
        texts['33-%03d' % (i + 1)] = sec[m.start():stop]
    return texts


ITEM_TEXTS = load_item_texts()
assert len(ITEM_TEXTS) == 54, 'vol33 has %d items' % len(ITEM_TEXTS)


def pos(item_id, text):
    """实体词形在条目原文中的字符偏移；找不到回退 (0,0)。"""
    t = ITEM_TEXTS.get(item_id, u'')
    p = t.find(text)
    if p < 0:
        return 0, 0
    return p, p + len(text)


# ---------------------------------------------------------------------------
# L1 实体层 ENT-3200 ~ ENT-3299
# (key, item_id, text, type, normalized, role, faction, exam_info, career_span, confidence)
# ---------------------------------------------------------------------------
ENT = [
    (u"\u6c88\u5fb7\u7b26", "33-007", u"\u6c88\u5fb7\u7b26", "person", u"\u6c88\u5fb7\u7b26", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "low"),
    (u"\u6b66\u6210\u5e99", "33-001", u"\u6b66\u6210\u5e99", "institution", u"\u6b66\u6210\u738b\u5e99\uff08\u6b66\u5e99\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, None, "high"),
    (u"\u960e\u79b9\u9521", "33-001", u"\u960e\u79b9\u9521", "person", u"\u960e\u79b9\u9521", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u6210\u5316", "high"),
    (u"\u6768\u7167", "33-002", u"\u6768\u7167", "person", u"\u6768\u7167", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756", "high"),
    (u"\u6c6a\u76f4", "33-003", u"\u6c6a\u76f4", "person", u"\u6c6a\u76f4", [u"\u4e3b\u4f53"], u"\u5ba6\u5b98", None, u"\u6210\u5316", "high"),
    (u"\u4f59\u8083\u654f", "33-003", u"\u4f59\u8083\u654f", "person", u"\u4f59\u5b50\u4fca\uff08\u8083\u654f\uff09", [u"\u5173\u8054\u4eba\u7269"], u"\u65e0", None, u"\u6210\u5316", "high"),
    (u"\u77f3\u4ea8", "33-004", u"\u77f3\u4ea8", "person", u"\u77f3\u4ea8\uff08\u6b66\u6e05\u4faf\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u6b63\u7edf\u2014\u666f\u6cf0", "high"),
    (u"\u621a\u5143\u656c", "33-005", u"\u621a\u5143\u656c", "person", u"\u621a\u7ee7\u5149\uff08\u5143\u656c\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756\u2014\u4e07\u5386", "high"),
    (u"\u674e\u66a0", "33-006", u"\u674e\u66a0", "person", u"\u674e\u66a0", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u6b63\u7edf", "high"),
    (u"\u5218\u663e", "33-007", u"\u5218\u663e", "person", u"\u5218\u663e", [u"\u5173\u8054\u4eba\u7269"], u"\u65e0", None, u"\u5609\u9756\u2014\u4e07\u5386", "high"),
    (u"\u6731\u5148", "33-007", u"\u6731\u5148", "person", u"\u6731\u5148", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756\u2014\u4e07\u5386", "high"),
    (u"胡襄愍", "33-007", u"胡襄愍", "person", u"胡宗宪（谥襄愍）", [u"关联人物"], u"无", None, u"嘉靖", "high"),
    (u"\u5f90\u6587\u957f", "33-008", u"\u5f90\u6587\u957f", "person", u"\u5f90\u6e2d\uff08\u6587\u957f\uff09", [u"\u5173\u8054\u4eba\u7269"], u"\u65e0", None, u"\u5609\u9756", "high"),
    (u"\u6bd5\u65fa", "33-009", u"\u6bd5\u65fa", "person", u"\u6bd5\u65fa", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u666f\u6cf0", "high"),
    (u"\u5175\u90e8", "33-010", u"\u5175\u90e8", "institution", u"\u5175\u90e8", [u"\u5173\u8054\u4eba\u7269"], u"\u65e0", None, None, "high"),
    (u"\u674e\u5982\u677e", "33-011", u"\u674e\u5982\u677e", "person", u"\u674e\u5982\u677e", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u5e90\u7965", "33-012", u"\u5e90\u7965", "person", u"\u5e90\u7965", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u6210\u5316", "high"),
    (u"\u4e01\u5927\u4f2f", "33-013", u"\u4e01\u5927\u4f2f", "person", u"\u4e01\u5927\u4f2f", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "medium"),
    (u"\u4e50\u65b0\u7089", "33-014", u"\u4e50\u65b0\u7089", "person", u"\u4e50\u65b0\u7089", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u738b\u5efa\u4e2d", "33-014", u"\u738b\u5efa\u4e2d", "person", u"\u738b\u5efa\u4e2d", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u5415\u65b0\u543e", "33-015", u"\u5415\u65b0\u543e", "person", u"\u5415\u6606\uff08\u65b0\u543e\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"闺范", "33-015", u"闺范", "book", u"《闺范》", [u"客体"], u"无", None, None, "high"),
    (u"\u6234\u58eb\u8861", "33-015", u"\u6234\u58eb\u8861", "person", u"\u6234\u58eb\u8861", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u6a0a\u7389\u8861", "33-015", u"\u6a0a\u7389\u8861", "person", u"\u6a0a\u7389\u8861", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u5f20\u65b0\u5efa", "33-015", u"\u5f20\u65b0\u5efa", "person", u"\u5f20\u4f4d\uff08\u65b0\u5efa\uff09", [u"\u5173\u8054\u4eba\u7269"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u7687\u8d35\u5983", "33-015", u"\u7687\u8d35\u5983", "person", u"\u90d1\u8d35\u5983", [u"\u5173\u8054\u4eba\u7269"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u71d5\u5c71\u6731\u4e1c\u5409", "33-017", u"\u71d5\u5c71\u6731\u4e1c\u5409", "person", u"\u6731\u4e1c\u5409\uff08\u8be1\u540d\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "medium"),
    (u"\u90d1\u627f\u6069", "33-016", u"\u90d1\u627f\u6069", "person", u"\u90d1\u627f\u6069", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"俶生光", "33-018", u"俶生光", "person", u"俶生光", [u"关联人物"], u"无", None, u"万历", "medium"),
    (u"郑朴", "33-019", u"锦衣郑朴", "person", u"郑朴（锦衣卫）", [u"关联人物"], u"无", None, u"万历", "medium"),
    (u"\u90d1\u798f\u6210", "33-019", u"\u90d1\u798f\u6210", "person", u"\u90d1\u798f\u6210\uff08\u8be1\u540d\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "medium"),
    (u"\u9648\u77e9", "33-019", u"\u9648\u77e9", "person", u"\u9648\u77e9", [u"\u5173\u8054\u4eba\u7269"], u"\u5ba6\u5b98", None, u"\u4e07\u5386", "high"),
    (u"\u56fd\u672c\u6538\u5173", "33-019", u"\u56fd\u672c\u6538\u5173", "book", u"\u56fd\u672c\u6538\u5173\uff08\u7eed\u5fe7\u5371\u7ac9\u8bae\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, None, "high"),
    (u"\u8463\u5e7c\u6d77", "33-020", u"\u8463\u5e7c\u6d77", "person", u"\u8463\u4f20\u7533\uff08\u5e7c\u6d77\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u6f58\u5b63\u9a6f", "33-021", u"\u6f58\u5b63\u9a6f", "person", u"\u6f58\u5b63\u9a6f", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u674e\u690d", "33-021", u"\u674e\u690d", "person", u"\u674e\u690d", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u6c5f\u9675", "33-021", u"\u6c5f\u9675", "person", u"\u5f20\u5c45\u6b63\uff08\u6c5f\u9675\uff09", [u"\u5173\u8054\u4eba\u7269"], u"\u65e0", None, u"\u5609\u9756\u2014\u4e07\u5386", "high"),
    (u"\u9a6c\u901a", "33-022", u"\u9a6c\u901a", "person", u"\u9a6c\u901a", [u"\u5173\u8054\u4eba\u7269"], u"\u65e0", None, u"\u6b63\u7edf", "high"),
    (u"\u82f1\u5b97", "33-023", u"\u82f1\u5b97", "person", u"\u660e\u82f1\u5b97", [u"\u5173\u8054\u4eba\u7269"], u"\u65e0", None, u"\u6b63\u7edf\u2014\u5929\u987a", "high"),
    (u"\u590f\u7444", "33-023", u"\u590f\u7444", "person", u"\u590f\u7444", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5929\u987a", "high"),
    (u"\u9ec4\u5ef7\u8058", "33-024", u"\u9ec4\u5ef7\u8058", "person", u"\u9ec4\u5ef7\u8058", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756", "high"),
    (u"\u5f20\u6c38\u660e", "33-024", u"\u5f20\u6c38\u660e", "person", u"\u5f20\u6c38\u660e", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756", "high"),
    (u"\u8f9b\u81ea\u4fee", "33-024", u"\u8f9b\u81ea\u4fee", "person", u"\u8f9b\u81ea\u4fee", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u6c88\u6c5d\u6881", "33-024", u"\u6c88\u6c5d\u6881", "person", u"\u6c88\u6c5d\u6881", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u94b1\u4e00\u672c", "33-024", u"\u94b1\u4e00\u672c", "person", u"\u94b1\u4e00\u672c", [u"\u4e3b\u4f53"], u"\u4e1c\u6797", None, u"\u4e07\u5386", "high"),
    (u"\u795d\u5927\u821f", "33-024", u"\u795d\u5927\u821f", "person", u"\u795d\u5927\u821f", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u5e9e\u5c1a\u9e4f", "33-024", u"\u5e9e\u5c1a\u9e4f", "person", u"\u5e9e\u5c1a\u9e4f", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756\u2014\u4e07\u5386", "high"),
    (u"张璁", "33-025", u"张璁", "person", u"张璁", [u"主体"], u"无", None, u"嘉靖", "high"),
    (u"桂萼", "33-025", u"桂萼", "person", u"桂萼", [u"主体"], u"无", None, u"嘉靖", "high"),
    (u"\u6768\u5ef7\u548c", "33-025", u"\u6768\u5ef7\u548c", "person", u"\u6768\u5ef7\u548c", [u"\u5173\u8054\u4eba\u7269"], u"\u65e0", None, u"\u6b63\u5fb7\u2014\u5609\u9756", "high"),
    (u"\u9f50\u4e16\u81e3", "33-026", u"\u9f50\u4e16\u81e3", "person", u"\u9f50\u4e16\u81e3", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"郑颙", "33-027", u"郑颙", "person", u"郑颙", [u"主体"], u"无", None, u"正统", "high"),
    (u"\u738b\u632f", "33-027", u"\u738b\u632f", "person", u"\u738b\u632f", [u"\u5173\u8054\u4eba\u7269"], u"\u5ba6\u5b98", None, u"\u6b63\u7edf", "high"),
    (u"\u6d77\u5fe0\u4ecb", "33-028", u"\u6d77\u5fe0\u4ecb", "person", u"\u6d77\u745e\uff08\u5fe0\u4ecb\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756\u2014\u4e07\u5386", "high"),
    (u"房寰", "33-028", u"房寰", "person", u"房寰", [u"主体"], u"无", None, u"万历", "high"),
    (u"李秉彝", "33-029", u"李秉彝", "person", u"李秉彝", [u"主体"], u"无", None, u"景泰", "high"),
    (u"林聪", "33-029", u"林聪", "person", u"林聪（庄敏）", [u"主体"], u"无", None, u"正统—天顺", "high"),
    (u"\u5218\u6587\u6cf0", "33-030", u"\u5218\u6587\u6cf0", "person", u"\u5218\u6587\u6cf0", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u6210\u5316\u2014\u6d2a\u6cbb", "high"),
    (u"\u9a6c\u4ece\u8c26", "33-031", u"\u9a6c\u4ece\u8c26", "person", u"\u9a6c\u4ece\u8c26", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756", "high"),
    (u"\u675c\u6cf0", "33-031", u"\u675c\u6cf0", "person", u"\u675c\u6cf0", [u"\u4e3b\u4f53"], u"\u5ba6\u5b98", None, u"\u5609\u9756", "high"),
    (u"柰亨", "33-032", u"柰亨", "person", u"柰亨", [u"主体"], u"无", None, u"正统", "high"),
    (u"\u8305\u4e00\u67f1", "33-032", u"\u8305\u4e00\u67f1", "person", u"\u8305\u4e00\u67f1", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u7b97\u5b66", "33-033", u"\u7b97\u5b66", "institution", u"\u7b97\u5b66", [u"\u4e3b\u4f53"], u"\u65e0", None, None, "high"),
    (u"\u5434\u5eb7\u658b", "33-034", u"\u5434\u5eb7\u658b", "person", u"\u5434\u4e0e\uff08\u5eb7\u658b\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u660e\u521d", "high"),
    (u"\u6731\u9686\u79a7", "33-034", u"\u6731\u9686\u79a7", "person", u"\u6731\u9686\u79a7", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756", "high"),
    (u"\u5218\u777f", "33-035", u"\u5218\u777f", "person", u"\u5218\u777f", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u6b63\u7edf\u2014\u6210\u5316", "high"),
    (u"\u674e\u71e7", "33-035", u"\u674e\u71e7", "person", u"\u674e\u71e7", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u6b63\u5fb7\u2014\u5609\u9756", "high"),
    (u"\u6768\u829d", "33-036", u"\u6768\u829d", "person", u"\u6768\u829d\uff08\u7f8a\u8102\u7389\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u6b63\u5fb7", "high"),
    (u"汪鋐", "33-037", u"汪鋐", "person", u"汪鋐", [u"主体"], u"无", None, u"嘉靖", "high"),
    (u"\u5434\u5c71", "33-038", u"\u5c1a\u4e66\u5434\u5c71", "person", u"\u5434\u5c71\uff08\u9ad8\u5b89\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756", "high"),
    (u"\u738b\u91d1", "33-038", u"\u738b\u91d1", "person", u"\u738b\u91d1", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756\u2014\u4e07\u5386", "high"),
    (u"\u5468\u6587\u8944", "33-039", u"\u5468\u6587\u8944", "person", u"\u5468\u5ff1\uff08\u6587\u8944\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u6c38\u4e50\u2014\u6b63\u7edf", "high"),
    (u"\u5b8b\u6ca7", "33-040", u"\u5b8b\u6ca7", "person", u"\u5b8b\u6ca7", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756", "high"),
    (u"\u7f57\u6c5d\u656c", "33-041", u"\u7f57\u6c5d\u656c", "person", u"\u7f57\u6c5d\u656c", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u6c38\u4e50\u2014\u6b63\u7edf", "high"),
    (u"\u9ece\u5229", "33-041", u"\u9ece\u5229", "person", u"\u9ece\u5229", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5ba3\u5fb7", "high"),
    (u"\u8521\u56fd\u7199", "33-042", u"\u8521\u56fd\u7199", "person", u"\u8521\u56fd\u7199", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u5f90\u76f8", "33-042", u"\u5f90\u76f8", "person", u"\u5f90\u76f8", [u"\u5ba2\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u9646\u4e94\u53f0", "33-042", u"\u9646\u4e94\u53f0", "person", u"\u9646\u5149\u4eea\uff08\u4e94\u53f0\uff09", [u"\u5173\u8054\u4eba\u7269"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u5434\u7ecd", "33-042", u"\u5434\u5c11\u53c2\uff08\u7ecd\uff09", "person", u"\u5434\u7ecd", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"周用斋", "33-043", u"周用斋", "person", u"周汝砺（用斋）", [u"主体"], u"无", None, u"万历", "high"),
    (u"\u6c88\u7956\u91cf", "33-044", u"\u6c88\u7956\u91cf", "person", u"\u6c88\u540c\u751f\uff08\u7956\u91cf\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u4e07\u5386", "high"),
    (u"\u6768\u5ba3", "33-045", u"\u6768\u5ba3", "person", u"\u6768\u5ba3", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5929\u987a\u2014\u6d2a\u6cbb", "high"),
    (u"\u5e38\u7407", "33-046", u"\u5e38\u7407", "person", u"\u5e38\u7407", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u6210\u5316", "high"),
    (u"方瑛", "33-046", u"方瑛", "person", u"方瑛（南和伯）", [u"关联人物"], u"无", None, u"天顺—成化", "high"),
    (u"龙闰", "33-046", u"龙闰", "person", u"龙闰", [u"主体"], u"宦官", None, u"成化", "high"),
    (u"\u592a\u5b97\u6587\u7687\u5e1d", "33-047", u"\u592a\u5b97\u6587\u7687\u5e1d", "person", u"\u660e\u6210\u7956", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u6c38\u4e50", "high"),
    (u"\u5f20\u5347", "33-048", u"\u52c7\u58eb\u5f20\u5347", "person", u"\u5f20\u5347", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756", "high"),
    (u"\u5de5\u90e8", "33-049", u"\u5de5\u90e8", "institution", u"\u5de5\u90e8", [u"\u5173\u8054\u4eba\u7269"], u"\u65e0", None, None, "high"),
    (u"\u5357\u5e02\u697c", "33-050", u"\u5357\u5e02\u697c", "place", u"\u5357\u5e02\u697c", [u"\u5ba2\u4f53"], u"\u65e0", None, None, "high"),
    (u"\u5b89\u4e50\u5802", "33-051", u"\u5b89\u4e50\u5802", "institution", u"\u5b89\u4e50\u5802", [u"\u4e3b\u4f53"], u"\u65e0", None, None, "high"),
    (u"翊坤宫", "33-052", u"翊坤宫", "place", u"翊坤宫", [u"主体"], u"无", None, None, "high"),
    (u"\u767d\u4e91\u89c2", "33-053", u"\u767d\u4e91\u89c2", "institution", u"\u767d\u4e91\u89c2", [u"\u4e3b\u4f53"], u"\u65e0", None, None, "high"),
    (u"\u90b1\u5143\u6e05", "33-053", u"\u90b1\u5143\u6e05", "person", u"\u90b1\u5143\u6e05", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u6d2a\u6b66\u521d", "medium"),
    (u"\u70df\u4e5d", "33-053", u"\u70df\u4e5d", "custom", u"\u70df\u4e5d\uff08\u961a\u4e5d\uff09", [u"\u4e3b\u4f53"], u"\u65e0", None, None, "high"),
    (u"\u5951\u5144\u5f1f", "33-054", u"\u5951\u5144\u5f1f", "custom", u"\u5951\u5144\u5f1f", [u"\u4e3b\u4f53"], u"\u65e0", None, None, "high"),
    (u"\u8d75\u5143\u6069", "33-054", u"\u8d75\u5143\u6069", "person", u"\u8d75\u5143\u6069", [u"\u4e3b\u4f53"], u"\u65e0", None, u"\u5609\u9756", "high"),
    (u"\u8d75\u6587\u534e", "33-012", u"\u8d75\u6587\u534e", "person", u"\u8d75\u6587\u534e", [u"\u4e3b\u4f53"], u"\u5f85\u5b9a", None, u"\u5609\u9756", "high"),
    (u"\u5b59\u4ee5\u4ec1", "33-024", u"\u5b59\u4ee5\u4ec1", "person", u"\u5b59\u4ee5\u4ec1", [u"\u5ba2\u4f53"], u"\u65e0", None, u"\u9686\u5e86", "high"),
    (u"\u5f20\u6c38", "33-035", u"\u5f20\u6c38", "person", u"\u5f20\u6c38\uff08\u5b98\u5b98\uff09", [u"\u5173\u8054\u4eba\u7269"], u"\u5ba6\u5b98", None, u"\u6b63\u5fb7", "high"),
    (u"\u5434\u9e4f", "33-042", u"\u5434\u592a\u5bb0", "person", u"\u5434\u9e4f\uff08\u6b66\u6c5f\uff0c\u53f2\u90e8\u5c1a\u4e66\uff09", [u"\u5173\u8054\u4eba\u7269"], u"\u65e0", None, u"\u5609\u9756", "medium"),
]

E = {}
ENTS = []
for i, (k, it, tx, ty, nm, role, fac, exam, span, cf) in enumerate(ENT):
    eid = 'ENT-32%02d' % i if i < 100 else None
    assert eid is not None, 'ENT overflow'
    E[k] = eid
    s, e2 = pos(it, tx)
    if s == 0 and tx not in ITEM_TEXTS.get(it, u'')[:1]:
        cf = 'low' if cf == 'high' and tx != u'\u6c88\u5fb7\u7b26' else cf
    ENTS.append({
        "ent_id": eid,
        "item_id": it,
        "text": tx,
        "type": ty,
        "normalized": nm,
        "start": s,
        "end": e2,
        "confidence": cf,
        "source": it,
        "role_in_entry": role,
        "faction": fac,
        "exam_info": exam,
        "career_span": span,
    })

# ---------------------------------------------------------------------------
# L2 规则层 RULE-33-NNN
# ---------------------------------------------------------------------------
RULES = [
    {"rule_id": "RULE-33-001", "item_id": "33-003", "category": "程序",
     "title": "武举乡会殿试程序",
     "content": "武举设科悉如进士恩例：选武臣嫡子就儒学读书习射，乡试以九月，会试以三月，初场试射、二场试论、三场试策，以四月初一殿试，赐及第出身恩荣次第，刻录立碑一如进士制。",
     "scope": "武臣嫡子及武举考生", "effective_date": "成化十四年议定", "status": "名存实亡",
     "note": "万安密奏缓行，事止；弘治中虽行武举但不殿试",
     "source_text": "选武臣嫡子就儒学读书习射，乡试以九月，会试以三月，初场试射，二场试论，三场试策，以四月初一殿试",
     "confidence": "high"},
    {"rule_id": "RULE-33-002", "item_id": "33-010", "category": "程序",
     "title": "武职比试三等法",
     "content": "应袭舍人年十五以上送学充附，二十应比试者考韬钤策一道转送抚按覆阅：韬钤贯通弓马娴熟为上等候缺管事，中等带俸差操，下等支半俸候再考；二次不中照邦政例仍支半俸，三次不中革发为军、别选子弟袭职。",
     "scope": "天下武职应袭舍人", "effective_date": "隆庆二年二月十四日奉旨依拟", "status": "名存实亡",
     "note": "久而不废此辈必思自奋，竟不知废于何年",
     "source_text": "韬钤贯通，弓马娴熟者为上等；韬钤疏而弓马熟者为次等；韬钤弓马俱不习为下等",
     "confidence": "high"},
    {"rule_id": "RULE-33-003", "item_id": "33-012", "category": "义务",
     "title": "土兵编佥与民壮训练之制",
     "content": "选民兵之壮者编成什伍为土兵，量免户租；民壮招募时器械鞍马俱从官给，地方有司春秋训练，遇警调用。",
     "scope": "边镇有司及民兵", "effective_date": "成化初年—正统以来", "status": "变通",
     "note": "弘治二年复命行之，后照例编佥徒供迎送之用",
     "source_text": "宜选民兵之壮者，编成什伍为土兵，量免户租",
     "confidence": "high"},
    {"rule_id": "RULE-33-004", "item_id": "33-013", "category": "程序",
     "title": "长解防逃追补程序",
     "content": "解军以本图里长充长解；凡遇军犯逃叛，长解必告所在官司追捕，羁留之，然后发卒追讨。",
     "scope": "长解及所在官司", "effective_date": "国初旧例", "status": "名存实亡",
     "note": "近年长解自充军犯雇男女投批到卫，戍长隐匿不敢声言",
     "source_text": "向来长解凡遇逃叛，必告所在官司追捕，即羁留之，然后发卒追讨",
     "confidence": "high"},
    {"rule_id": "RULE-33-005", "item_id": "33-022", "category": "禁止",
     "title": "赌博厉禁",
     "content": "天下赌博盛行，本朝法轻仅杖枷；作者称宋淳化二年太宗令开封府凡坊市赌博者俱行处斩、邻比匿不闻者问罪，谓此法至善。",
     "scope": "坊市民人", "effective_date": "宋淳化二年闰二月（本朝沿用轻法）", "status": "变通",
     "note": "正统间马通建白定犯者运粮口外，今格不行仅从初制拟杖",
     "source_text": "宋时淳化二年闰二月，太宗下令开封府，凡坊市有赌博者，俱行处斩，邻比匿不闻者问罪",
     "confidence": "high"},
    {"rule_id": "RULE-33-006", "item_id": "33-022", "category": "处罚",
     "title": "洪武二十二年游惰肉刑令",
     "content": "学唱的割了舌头，下棋打双陆的断手，蹴圆者卸脚，犯者必如法施行。",
     "scope": "游惰戏玩之人", "effective_date": "洪武二十二年圣旨", "status": "名存实亡",
     "note": "作者主张赌博亦当如太祖初制解腕",
     "source_text": "洪武二十二年圣旨：学唱的割了舌头，下棋打双陆的断手，蹴圆者卸脚",
     "confidence": "high"},
    {"rule_id": "RULE-33-007", "item_id": "33-029", "category": "义务",
     "title": "京官父母丧听终制",
     "content": "凡京官非与机要者，有父母丧，悉听终制，不必夺情；或有以夺情为善事，视父母如路人，子道既亏，臣节安在。",
     "scope": "京官", "effective_date": "景泰五年林聪奏准", "status": "变通",
     "note": "景泰五年止王复夺情，然天顺三年林聪自己以忧归又被行取赴任",
     "source_text": "凡京官非与机要者，有父母丧，悉听终制，不必夺情",
     "confidence": "high"},
    {"rule_id": "RULE-33-008", "item_id": "33-047", "category": "允许",
     "title": "上元节假放灯永为定例",
     "content": "上元节正月十一日至二十日官人每都与节假不奏事，民间放灯从他饮酒作乐快活，兵马司都不禁，夜巡不要搅扰生事，永为定例。",
     "scope": "京师官民", "effective_date": "永乐七年正月十一日圣旨", "status": "遵行",
     "note": "每至年终礼部上疏援引前例请旨，许民间放灯凡十昼夜",
     "source_text": "今年上元节正月十一日至二十日，这几日官人每都与节假",
     "confidence": "high"},
    {"rule_id": "RULE-33-009", "item_id": "33-050", "category": "禁止",
     "title": "朝臣禁狎歌妓",
     "content": "宣德中以百僚日醉狭邪不修职业，左都御史顾佐奏禁，廷臣有犯者至褫职，迄今不改。",
     "scope": "朝臣", "effective_date": "宣德中", "status": "遵行",
     "note": "太祖所建十楼本为歌妓之薮，禁后金陵十四楼仅存商贾游集",
     "source_text": "至宣德中，以百僚日醉狭邪，不修职业，为左都御史顾佐奏禁，廷臣有犯者至褫职",
     "confidence": "high"},
    {"rule_id": "RULE-33-010", "item_id": "33-018", "category": "禁止",
     "title": "造作妖书之禁",
     "content": "借改易东朝为名造作妖书、指实大臣姓名者，立意甚毒、造语甚巧，罪当殊死。",
     "scope": "天下臣民", "effective_date": "万历癸卯", "status": "遵行",
     "note": "仅捕俶生光服上刑塞责，造撰之人终莫能明",
     "source_text": "复借改易东朝为名，而指朱次揆姓名以实之，其立意甚毒，造语甚巧，而其词旨甚不经",
     "confidence": "high"},
    {"rule_id": "RULE-33-011", "item_id": "33-001", "category": "程序",
     "title": "三皇庙祀典规程",
     "content": "诏修太医院三皇庙，厘正祀典：正位伏羲神农黄帝，配位勾芒祝融风后力牧，从祀僦贷季天师等十人拟十哲，复增伊尹、扁鹊至朱彦修十八人从祀两庑；牲用太牢，器用笾豆簠簋，以仲春仲冬上甲日遣大臣行礼，著为令。",
     "scope": "太医院三皇庙有司", "effective_date": "嘉靖间", "status": "遵行",
     "note": "与文宣庙、武成庙鼎立为京师三大祀",
     "source_text": "牲用太牢，器用笾豆簠簋，以仲春仲冬上甲日，遣大臣行礼，著为令",
     "confidence": "high"},
]

# ---------------------------------------------------------------------------
# L5 事件层 EVT-33-NNN（主键 event_id）
# ---------------------------------------------------------------------------
EVENTS = [
    {"event_id": "EVT-33-001", "item_id": "33-001", "title": "洪武废武成庙",
     "description": "本朝洪武间礼部请如前代故事设武学、建武成庙，上谓是歧文武为二矣，但以太公从祀帝王庙而废武成庙，并武学不设。",
     "event_type": "制度变动", "date": "洪武间", "reign": "洪武", "location": "南京",
     "participants": ["太祖", "礼部", "太公"], "outcome": "文武分祀之制暂止，武成庙废",
     "source_text": "上谓是歧文武为二矣，但以太公从祀帝王庙，而废武成庙。并武学不设",
     "event_significance": "制度变动", "political_impact": "明初崇文抑武、文武不分祀的定位",
     "source_type": "文献转引", "vs_official_history": "与正史合"},
    {"event_id": "EVT-33-002", "item_id": "33-001", "title": "成化四年武学改建庙议",
     "description": "成化四年用国子监丞阎禹锡言，古者学必有庙，乞将武学余楹改为庙，使知礼先勇后之义；上许之，而太公不得祀犹故也。",
     "event_type": "制度变动", "date": "成化四年", "reign": "成化", "location": "京师武学",
     "participants": ["阎禹锡"], "outcome": "许改建庙而太公仍不得祀",
     "source_text": "成化四年，用国子监丞阎禹锡言，古者学必有庙，乞将武学余楹改为庙",
     "event_significance": "一般掌故", "political_impact": "武庙之制反复未定",
     "source_type": "文献转引", "vs_official_history": "与正史合"},
    {"event_id": "EVT-33-003", "item_id": "33-001", "title": "嘉靖十五年诏重建武成王庙",
     "description": "嘉靖十五年四月兵部议以武学太窄请拓其制，改建于大兴隆寺故址；会礼工二部皆言宜仿唐制立武成王庙，增徐达常遇春等配享，上允之，于是文武两庙并医王三大祀鼎立于京师。",
     "event_type": "制度变动", "date": "嘉靖十五年四月", "reign": "嘉靖", "location": "京师大兴隆寺故址",
     "participants": ["世宗", "兵部", "徐达", "常遇春"], "outcome": "武成王庙复立，与文宣庙、三皇庙并峙",
     "source_text": "改建于大兴隆寺故址。上命会礼工二部共议，皆言宜仿唐制，立武成王庙",
     "event_significance": "制度变动", "political_impact": "世宗厘正祀典，文武医三大祀格局成立",
     "source_type": "文献转引", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-004", "item_id": "33-002", "title": "杨照刺背战殁",
     "description": "嘉靖末年故将杨照起为辽东总兵，涅尽忠报国四字于背，与巡抚侯汝谅、管饷郎中何东序互讦回卫，复起后誓死与虏角战殁；巡抚王之诰以闻，上命月给米三石复其家。",
     "event_type": "军事", "date": "嘉靖末年", "reign": "嘉靖", "location": "辽东",
     "participants": ["杨照", "侯汝谅", "何东序", "王之诰"], "outcome": "照战殁，朝廷月给米三石复其家，为累朝旷典",
     "source_text": "照感上知遇，涅\u201c尽忠报国\u201d四字于背",
     "event_significance": "重大政治", "political_impact": "以旷典励各边壮士",
     "source_type": "传闻", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-005", "item_id": "33-003", "title": "汪直请设武举殿试科",
     "description": "成化十四年宦官汪直擅权务边功右武人，上疏请武举设科并用乡会殿试悉如进士恩例；兵部余子俊不敢决，廷臣集议条上大略；万安密奏内批缓之，令兵部移文天下教养数年，事方得止。",
     "event_type": "科举", "date": "成化十四年", "reign": "成化", "location": "京师",
     "participants": ["汪直", "余肃敏", "万文康", "张辅"], "outcome": "武举殿试之议暂缓；至弘治中毕竟行之但不殿试",
     "source_text": "乃上疏请武举设科，亦用乡试、会试、殿试，悉如进士恩例",
     "event_significance": "制度变动", "political_impact": "阉人干政而士大夫以缓字诀调停",
     "source_type": "文献转引", "vs_official_history": "与正史合"},
    {"event_id": "EVT-33-006", "item_id": "33-004", "title": "石亨请刺军人臂字被驳",
     "description": "景泰中武清侯石亨为总兵请征剿也先，军人四胜五胜者左右臂各刺赤心报国四字；景帝以刺字是刑罚加于无罪不近情，不许。",
     "event_type": "军事", "date": "景泰中", "reign": "景泰", "location": "京师",
     "participants": ["石亨", "景帝"], "outcome": "请竟被驳，本朝极重黥刺而不可妄加",
     "source_text": "四胜五胜者，左右臂各刺\u201c赤心报国\u201d四字",
     "event_significance": "一般掌故", "political_impact": "武人不学妄议之典型",
     "source_type": "文献转引", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-007", "item_id": "33-006", "title": "李暠杖祁州知州李玉",
     "description": "正统十三年大宁都指挥佥事李暠道遇祁州知州李玉不避道，杖之，为巡按御史段信所劾，其时都司之横如此。",
     "event_type": "司法", "date": "正统十三年", "reign": "正统", "location": "大宁—祁州",
     "participants": ["李暠", "李玉", "段信"], "outcome": "为巡按所劾，见武弁之横",
     "source_text": "大宁都指挥佥事李暠，道遇祁州知州李玉不避道，杖之，为巡按御史段信所劾",
     "event_significance": "一般掌故", "political_impact": "缙绅道丧之一端",
     "source_type": "文献转引", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-008", "item_id": "33-006", "title": "杨峻杖死都指挥佥事陶忠",
     "description": "景泰元年万全参将杨峻挟私杖死都指挥佥事陶忠，初拟斩，未几景帝宥之，令随父昌平侯杨洪立功而已。",
     "event_type": "司法", "date": "景泰元年", "reign": "景泰", "location": "万全",
     "participants": ["杨峻", "陶忠", "杨洪", "景帝"], "outcome": "免死随父立功，都司之贱又如此",
     "source_text": "万全参将杨峻，以挟私杖死都指挥佥事陶忠，初拟斩，未几景帝宥之",
     "event_significance": "一般掌故", "political_impact": "五品刺史反见挞于健儿",
     "source_type": "文献转引", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-009", "item_id": "33-007", "title": "嘉靖癸亥倭伪官军据兴化府",
     "description": "嘉靖癸亥十一月倭至兴化府伪为官军赴救，城中开门纳之，倭遂入据其城逾岁方去；立功大将刘显军掠夺逃出妇人，原任参政王凤台新继妻亦为显所纳。",
     "event_type": "军事", "date": "嘉靖癸亥十一月", "reign": "嘉靖", "location": "兴化府",
     "participants": ["刘显", "王凤台"], "outcome": "城陷逾岁，官军之蹂践更倍于倭",
     "source_text": "倭至兴化府伪为官军赴救，城中开门纳之，倭遂入据其城，逾岁方去",
     "event_significance": "重大政治", "political_impact": "东南倭患与大帅无纪之实态",
     "source_type": "传闻", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-010", "item_id": "33-007", "title": "朱先募前锋破倭起家",
     "description": "倭事起时吾乡朱先以贩盐拒捕伤官兵论斩，会募壮士为前锋应募，一日馘倭十三人，胡宗宪以便宜拜守备，逾年至参将，后终为福建大帅，以年老归。",
     "event_type": "军事", "date": "嘉靖间", "reign": "嘉靖", "location": "东南",
     "participants": ["朱先", "胡襄敏"], "outcome": "由罪囚致位大帅，廉勇善战而没没无闻",
     "source_text": "一日馘倭十三人，胡襄愍为督府，即以便宜拜守备",
     "event_significance": "人物转折", "political_impact": "非常之功须非常之人之一例",
     "source_type": "传闻", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-011", "item_id": "33-008", "title": "胡宗宪从徐渭言剖卒验鲊",
     "description": "胡襄敏提兵在吾郡，健儿买酒肉鲊不偿值且殴酤者，徐文长在坐谓当剖腹验之，胡立命剖之，鲊尚在，遂释酤者倍偿之，军中股栗不复敢肆。",
     "event_type": "军事", "date": "嘉靖间", "reign": "嘉靖", "location": "浙江行台",
     "participants": ["胡襄敏", "徐文长"], "outcome": "军令肃然，书生胆决如此",
     "source_text": "时徐文长在坐，谓当剖腹以验之",
     "event_significance": "轶闻", "political_impact": "军中股栗，不复敢肆",
     "source_type": "传闻", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-012", "item_id": "33-009", "title": "毕旺援例请许锦衣麟服",
     "description": "武弁绣胸不循钦定品级概服狮子，人皆谓起嘉靖间，后乃知事在景泰四年：锦衣指挥同知毕旺疏援永乐旧例，谓环卫近臣不比他官，概许麟服。",
     "event_type": "制度变动", "date": "景泰四年", "reign": "景泰", "location": "京师",
     "participants": ["毕旺"], "outcome": "一品采章下逮皂隶，僭服之端实始此",
     "source_text": "后乃知事在景泰四年：锦衣指挥同知毕旺，疏援永乐旧例",
     "event_significance": "一般掌故", "political_impact": "服制名器之滥",
     "source_type": "文献转引", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-013", "item_id": "33-010", "title": "隆庆二年申武职比试之法",
     "description": "隆庆二年二月十四日兵部题浙江巡抚赵都御史陈将材一节而申明之：应袭舍人送学充附，比试分三等，三次不中革发为军别选子弟袭职，奉旨依拟行。",
     "event_type": "制度变动", "date": "隆庆二年二月十四日", "reign": "隆庆", "location": "京师—天下卫所",
     "participants": ["兵部"], "outcome": "法久竟废，穆宗史亦不载",
     "source_text": "偶检得隆庆二年二月十四日，兵部题浙江巡抚赵都御史陈将材一节而申明之",
     "event_significance": "制度变动", "political_impact": "武弁考核最严亦最恕之法",
     "source_type": "亲历", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-014", "item_id": "33-011", "title": "碧蹄馆家丁遇伏战殁",
     "description": "癸巳朝鲜之役平壤大捷后，李如松不欲他兵分功，潜率家丁二千人夜至碧蹄馆遇伏一举歼焉；家丁李友升只身殿后战殁，如松始得脱。",
     "event_type": "军事", "date": "万历癸巳（二十年）", "reign": "万历", "location": "朝鲜碧蹄馆",
     "participants": ["李如松", "李友升"], "outcome": "家丁歼焉，如松仅以身免",
     "source_text": "潜率家丁二千人夜至碧蹄馆，遇伏一举歼焉",
     "event_significance": "重大政治", "political_impact": "将帅专仗家丁之害见端",
     "source_type": "传闻", "vs_official_history": "异于正史"},
    {"event_id": "EVT-33-015", "item_id": "33-012", "title": "庐祥建议编设土兵",
     "description": "成化初年巡抚延绥都御史庐祥以营伍兵少而延安庆阳边民骁勇，建议选民兵之壮者编成什伍为土兵量免户租，凡得五千人训练之；毛里孩入寇为之退却，祥去而此法遂废。",
     "event_type": "军事", "date": "成化初年", "reign": "成化", "location": "延绥",
     "participants": ["庐祥", "毛里孩"], "outcome": "土兵始此，祥去法废",
     "source_text": "巡抚延绥都御史庐祥建议，以营伍兵少，而延安庆阳边民骁勇",
     "event_significance": "制度变动", "political_impact": "明边兵土兵制度之始",
     "source_type": "文献转引", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-016", "item_id": "33-012", "title": "赵文华乡官领兵议寝",
     "description": "倭警时赵文华誓师浙江，故令乡官领兵团结出战，又查籍间田百万亩以赡新兵；蒲坂杨襄毅新从蓟辽召领中枢，覆疏谓乡绅为帅督责未便且间田出于何所，事遂得已。",
     "event_type": "军事", "date": "嘉靖间", "reign": "嘉靖", "location": "浙江",
     "participants": ["赵文华", "杨襄毅"], "outcome": "乡官领兵之议得寝",
     "source_text": "赵文华誓师浙江，故令乡官领兵，团结出战，又查籍间田百万亩，以赡新兵",
     "event_significance": "一般掌故", "political_impact": "文华欲笼桑梓张威福，尤舛谬之谈",
     "source_type": "文献转引", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-017", "item_id": "33-013", "title": "丁大伯解军遁归反早还",
     "description": "作者幼年侍先人邸中，吴江叟丁大伯为捕役妄指平民发遣辽东三万卫充军作长解；王姓军犯到伍先从间道遁归不由山海关，反早还。近年长解自充军犯雇男女投批到卫，荷戈之人优游闾里。",
     "event_type": "社会", "date": "万历间（作者幼年）", "reign": "万历", "location": "京师—辽东三万卫",
     "participants": ["丁大伯"], "outcome": "解军之弊日深，逃者百中不得一二追获",
     "source_text": "曾记幼年侍先人邸之，有吴江一叟，号丁大伯者",
     "event_significance": "一般掌故", "political_impact": "明代发遣充军制度崩坏之侧影",
     "source_type": "传闻", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-018", "item_id": "33-014", "title": "王建中纠山人乐新炉",
     "description": "今上辛卯冬，刑科给事中王建中特疏纠山人乐新炉捏造飞语，以邹元标等为十君子、赵卿等为八狗、杨四知等为三羊；上命逮新炉诏狱鞫之，具伏，荷立枷戍之寻死。",
     "event_type": "司法", "date": "万历辛卯冬", "reign": "万历", "location": "京师",
     "participants": ["乐新炉", "王建中", "邹元标"], "outcome": "新炉死于戍，张鼎思自白亦见嘲为张换狗",
     "source_text": "刑科给事中王建中，特疏纠之，内云新炉捏造飞语",
     "event_significance": "一般掌故", "political_impact": "山人蜚语与言路波连",
     "source_type": "传闻", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-019", "item_id": "33-015", "title": "戊戌谤书：戴士衡樊玉衡参吕坤",
     "description": "吕新吾刻《闺范》而皇贵妃重刻为序，吏科给事中戴士衡首发大难参吕包藏祸心，全椒知县樊玉衡继之，举朝骇愕；有为图说跋者专攻吕司寇，标名忧危竑议以讥切之，诡名燕山朱东吉，竟不知何人所造。",
     "event_type": "朝政", "date": "万历戊戌", "reign": "万历", "location": "京师",
     "participants": ["吕新吾", "戴士衡", "樊玉衡", "皇贵妃", "张新建"], "outcome": "两家聚讼，张位借东事被逐之案根于此",
     "source_text": "吏科给事中戴士衡首发大难，参吕包藏祸心",
     "event_significance": "重大政治", "political_impact": "国本之争中闺范一书成攻讦之具",
     "source_type": "传闻", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-020", "item_id": "33-016", "title": "皇贵妃重刊闺范自序",
     "description": "万历二十三年乙未七月望日，皇贵妃以近得吕氏坤《闺范》一书，原出宫赀命官重梓颁布中外，且为之序，光艳照一时，朝士争购置案头。",
     "event_type": "文化", "date": "万历二十三年乙未七月望日", "reign": "万历", "location": "内廷",
     "participants": ["皇贵妃", "吕新吾", "郑承恩"], "outcome": "图说第一段明德马后今已删去不存",
     "source_text": "原出宫赀，命官重梓，颁布中外，永作法程",
     "event_significance": "一般掌故", "political_impact": "戚畹与见任大臣刻书破格之恩",
     "source_type": "亲历", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-021", "item_id": "33-017", "title": "闺鉴图说跋伪作",
     "description": "戊戌有图说跋专攻吕司寇，其语深文杂引在事知名大臣，以或问或难之体曲庇易储之谋，署燕山朱东吉顿首跋，诡名也，竟不知何人所造。",
     "event_type": "其他", "date": "万历戊戌", "reign": "万历", "location": "京师",
     "participants": ["燕山朱东吉", "吕新吾"], "outcome": "跋语标名忧危竑议，为张位被逐案之张本",
     "source_text": "因援笔记之。燕山朱东吉顿首跋",
     "event_significance": "重大政治", "political_impact": "妖书案之始作俑",
     "source_type": "传闻", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-022", "item_id": "33-018", "title": "癸卯妖书起举朝鼎沸",
     "description": "至癸卯岁震方久安已历三年，妖书陡起复借改易东朝为名而指朱次揆姓名以实之，上怒莫测举朝鼎沸，仅捕俶生光服上刑塞责，造撰之人终莫能明；都下或云锦衣郑朴为之，或云出自中书赵士桢手。",
     "event_type": "朝政", "date": "万历癸卯", "reign": "万历", "location": "京师",
     "participants": ["俶生光", "朱次揆", "郑朴"], "outcome": "生光冤死，真造者不可知",
     "source_text": "捕俶生光服上刑，聊以塞责完局耳",
     "event_significance": "重大政治", "political_impact": "郭江夏沈归德诸公俱几不保首领",
     "source_type": "传闻", "vs_official_history": "与正史合"},
    {"event_id": "EVT-33-023", "item_id": "33-019", "title": "陈矩封进《续忧危竑议》",
     "description": "万历三十一年十一月十二日，提督东厂太监陈矩奏称办事蒋臣等访得《国本攸关》刊书一本封进圣览；皮面签国本攸关四字，本书第一行则续忧危竑议五字，借郑福成诡名极言东宫可摇。",
     "event_type": "朝政", "date": "万历三十一年十一月十二日", "reign": "万历", "location": "京师东厂",
     "participants": ["陈矩", "郑福成", "项应祥", "乔应甲"], "outcome": "妖书案正式爆发，捕狱纷纭",
     "source_text": "万历三十一年十一月十二日，提督东厂太监陈矩奏称",
     "event_significance": "重大政治", "political_impact": "署名项应祥乔应甲之伪撰转成党狱",
     "source_type": "传闻", "vs_official_history": "与正史合"},
    {"event_id": "EVT-33-024", "item_id": "33-020", "title": "董幼海陆二顽为仆所杀",
     "description": "往年松江董幼海少宰以御下过苛为群仆所脔割；近年嘉兴平湖陆生号二顽者酷遇诸奴，奴辈共手刃之俱自首正法；又万历十七年南监生潘文锡为爱婢春桃与嬖奴朱廷所杀。",
     "event_type": "社会", "date": "万历间", "reign": "万历", "location": "松江—嘉兴—金陵",
     "participants": ["董幼海", "潘文锡", "春桃"], "outcome": "怨毒之极甘心抵偿，可戒可戒",
     "source_text": "以御下过苛，为群仆所脔割",
     "event_significance": "轶闻", "political_impact": "主仆恩仇之变见于三吴一方",
     "source_type": "传闻", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-025", "item_id": "33-021", "title": "李植劾潘季驯并及其家",
     "description": "甲申刑部尚书潘季驯请宽故相江陵子孙，御史李植劾其自叙河工以发踪人功推江陵，又云父访察充军兄人命拟死，父子兄弟济恶；弹章诬及家门自此始。",
     "event_type": "朝政", "date": "万历甲申", "reign": "万历", "location": "京师",
     "participants": ["潘季驯", "李植", "江陵"], "outcome": "弹章所指蔓延闺阁，其秽令人掩耳",
     "source_text": "御史李植劾其往年自叙河工，以发踪人功推江陵",
     "event_significance": "一般掌故", "political_impact": "株连父兄之政体败坏",
     "source_type": "传闻", "vs_official_history": "与正史合"},
    {"event_id": "EVT-33-026", "item_id": "33-023", "title": "天顺议罚倒置",
     "description": "英宗复辟后刑赏失平：天顺二年常德卫指挥使夏瑄杀寄居者妻子三人焚之，本论凌迟，因其子代刑之疏竟得复职，按察司冯诚反以失入人死下锦衣狱；沂川卫王有忠杀人嗾部杀之仅遣戍；御史何楚英笞厨役朱辛致死，枷都察院前三月降平南典史。",
     "event_type": "司法", "date": "天顺二年—三年", "reign": "天顺", "location": "京师—湖广—山东",
     "participants": ["英宗", "夏瑄", "何楚英"], "outcome": "曹石擅权专右武人，台臣僇辱至此",
     "source_text": "夫杀人至三人七人，此宇宙大变，一得复官，一仅遣戍，此何律也",
     "event_significance": "重大政治", "political_impact": "复辟后刑章倒置之实录",
     "source_type": "文献转引", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-027", "item_id": "33-024", "title": "御史墨败相绳系列案",
     "description": "嘉靖四十四年巡按御史黄廷聘归籍过衡山被知县发箧，左都御史张永明发其状，冠带闲住；四十五年何起鸣追论陈志先；穆宗初庞尚鹏劾孙以仁；万历丙戌辛自修劾沈汝梁追赃遣戍；辛卯钱一本追论祝大舟逮京诏狱遣戍；壬辰李天麟劾苏酂以贪斥。",
     "event_type": "司法", "date": "嘉靖四十四年—万历壬辰", "reign": "嘉靖—万历", "location": "京师—南京",
     "participants": ["黄廷聘", "张永明", "辛自修", "钱一本", "祝大舟"], "outcome": "处分渐加重，兰台体面扫地尽矣",
     "source_text": "奉旨追赃遣戌，此以堂官参治台臣，正与张永明同",
     "event_significance": "重大政治", "political_impact": "台省风气与处分轻重之变迁",
     "source_type": "传闻", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-028", "item_id": "33-025", "title": "桂萼请科道互纠丁亥考察",
     "description": "嘉靖六年丁亥大计，张璁桂萼分被南北科道所纠，萼疏谓杨廷和私党犹在言路，引例请拾遗后互相纠察；上命吏部勒科道互纠，科道先劾储良材等，最后惟良材罢而又降又留，内批反谪二科臣报私怨。",
     "event_type": "人事", "date": "嘉靖六年", "reign": "嘉靖", "location": "京师",
     "participants": ["张璁", "桂萼", "杨廷和", "储良材"], "outcome": "内计颠倒披猖，书之史册令人戟手追詈权奸",
     "source_text": "萼乃疏谓杨廷和私党犹在言路，引宪宗初年例，于拾遗后，互相纠察",
     "event_significance": "重大政治", "political_impact": "大礼议后阁臣控言路之实例",
     "source_type": "文献转引", "vs_official_history": "异于正史"},
    {"event_id": "EVT-33-029", "item_id": "33-026", "title": "齐世臣以姓名见目标",
     "description": "科臣齐世臣初保张居正再保大峪山，则目之为齐人齐保山；言官惯以串合名字陷人登之章疏，最后癸卯妖书云上起朱山阴于田间，专以易储示意。",
     "event_type": "社会", "date": "万历间", "reign": "万历", "location": "京师",
     "participants": ["齐世臣", "张居正"], "outcome": "穿凿矫诬惑乱远近，儇薄成俗",
     "source_text": "初保张居正，再保大峪山，则目之为齐人齐保山",
     "event_significance": "轶闻", "political_impact": "姓名之祸与文字之祸相寻",
     "source_type": "传闻", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-030", "item_id": "33-027", "title": "郑颙请以内官领张家湾抽分",
     "description": "正统二年五月御史郑颙奏张家湾宣课司宜专委内官抽分，时王振初窃柄，顾佐甫去位；上曰不必专委内官，事竟不行。成化六年郭瑞奏保镇守太监钱能，戴缙谀汪直皆其端。",
     "event_type": "宫廷", "date": "正统二年五月", "reign": "正统", "location": "京师",
     "participants": ["郑颙", "王振", "顾佐"], "outcome": "三杨在内阁尚能杜祸萌",
     "source_text": "张家湾宜专委内官抽分，崇文门宜令本门收钞内官兼管",
     "event_significance": "一般掌故", "political_impact": "台臣阿内侍之渐",
     "source_type": "文献转引", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-031", "item_id": "33-028", "title": "房寰再以讥谑疏攻海瑞",
     "description": "海忠介为房寰所论列愤极上疏辩析，房再疏攻之，专录笑谑之语：锺宇淳批牍尾海外奇谈、黄凤翔批令祭酒讲解素位一章、诸臣座中诮其读程策、抱石投江诸怪说；万历十四年七月疏至举朝骇惑，三进士合疏攻房保海不胜见逐。",
     "event_type": "朝政", "date": "万历十四年七月", "reign": "万历", "location": "京师",
     "participants": ["海忠介", "房寰", "锺宇淳", "黄凤翔"], "outcome": "房亦外转副使以去，忠介之清冠绝一时",
     "source_text": "惟其矢口笑谑者，最堪捧腹，今节录于后",
     "event_significance": "重大政治", "political_impact": "海瑞案之谑化与言路风气的标本",
     "source_type": "传闻", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-032", "item_id": "33-030", "title": "弘治十六年命刘文泰改修本草",
     "description": "弘治十六年上因《本草》讹误命官改修，以刘文泰等充其役；文泰等实懵然乃请用翰林官校正，阁臣刘健争之，上命翰林专修而其太医官不预。文泰因得与太监张瑜相表里，援引直入禁中。",
     "event_type": "文化", "date": "弘治十六年", "reign": "弘治", "location": "京师太医院",
     "participants": ["刘文泰", "刘健", "邱濬"], "outcome": "文泰欲窃邱濬医书为己功之计败",
     "source_text": "至弘治十六年，上因《本草》讹误，命官改修，以刘文泰等充其役",
     "event_significance": "一般掌故", "political_impact": "词臣校书之争议",
     "source_type": "文献转引", "vs_official_history": "与正史合"},
    {"event_id": "EVT-33-033", "item_id": "33-030", "title": "刘文泰误药弑两朝帝",
     "description": "刘文泰先以投剂乖方致损宪宗，孝宗命降为院判；乙丑之夏上（孝宗）本患热得疾，文泰误投大热之剂以至上宾；武宗登极后法司会奏文泰与张瑜交结作弊各斩，久之俱免死遗戍。",
     "event_type": "宫廷", "date": "成化二十三年—弘治十八年", "reign": "成化—弘治", "location": "京师",
     "participants": ["刘文泰", "韩重", "陈谷"], "outcome": "庸医致促两朝圣寿，竟免于死",
     "source_text": "文泰误投大热之剂，烦躁不堪，以至上宾",
     "event_significance": "重大政治", "political_impact": "医官与内臣交结为孝宗之死一大公案",
     "source_type": "文献转引", "vs_official_history": "异于正史"},
    {"event_id": "EVT-33-034", "item_id": "33-031", "title": "马从谦杖毙于劾杜泰",
     "description": "光禄少卿马从谦嘉靖间劾提督光禄太监杜泰干没内帑数万，泰诬其诽谤不忠，诏杖八十即毙杖下；严嵩因前疏下石。穆宗登极言官屡为请恩典而中官阻之，至今上辛卯从其子马有骅之请始与祭葬。",
     "event_type": "司法", "date": "嘉靖—万历辛卯", "reign": "嘉靖—万历", "location": "京师",
     "participants": ["马从谦", "杜泰"], "outcome": "死可谓至冤，恤典迟三十年",
     "source_text": "泰亦诬从谦诽谤不忠，上信而怒之，诏杖八十",
     "event_significance": "人物转折", "political_impact": "内侍报复与言路噤声",
     "source_type": "传闻", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-035", "item_id": "33-032", "title": "正统六年柰亨盗祀物获宥",
     "description": "光禄寺大官署丞张冕奏本寺卿柰亨借供祀盗取猪鹅肉面食为私用，上命对状，姑宥之；亨后两以户侍郎充廷试读卷官又荫子为中书舍人，恩宠之滥亦甚。万历十八年署丞茅一柱盗火腿，问徒为民。",
     "event_type": "司法", "date": "正统六年", "reign": "正统", "location": "光禄寺",
     "participants": ["柰亨", "茅一柱"], "outcome": "两事略同处分略异，亨之厚颜不足责",
     "source_text": "奏本寺卿柰亨借供祀，盗取猪鹅肉及面食为私用",
     "event_significance": "轶闻", "political_impact": "法外施恩流弊可见",
     "source_type": "文献转引", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-036", "item_id": "33-034", "title": "朱隆禧作太极衣献世宗",
     "description": "太极本无极而迂儒铸图如圈；本朝吴康斋每以两手作圈势自云无时不见太极，浮薄者以芦菔投其中；世宗朝罢任府丞朱隆禧作太极衣以献盖房中术，上大喜，进卿进侍郎。",
     "event_type": "宗教", "date": "嘉靖间", "reign": "嘉靖", "location": "京师",
     "participants": ["朱隆禧", "吴康斋", "世宗"], "outcome": "圣贤道理受人亵慢至此",
     "source_text": "至世宗朝，罢任府丞朱隆禧。作太极衣以献，盖房中术也",
     "event_significance": "轶闻", "political_impact": "佞幸以玄修进，可痛可恨",
     "source_type": "传闻", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-037", "item_id": "33-035", "title": "刘睿李燧媒进于权阉",
     "description": "河南鄢陵刘睿为吏科都给事中，路遇王振跪于道旁，振大喜升户部左侍郎后升尚书；汤阴李燧致仕归，张永西征还过汤阴，燧敝衣破冠束赐玉带跪迎于路，永至京师荐之召复故官再长冬曹。",
     "event_type": "人事", "date": "正统—嘉靖", "reign": "正统—嘉靖", "location": "河南—京师",
     "participants": ["刘睿", "李燧", "王振", "张永"], "outcome": "二人俱功名始终老死林下，然媒进之术如此",
     "source_text": "路遇王振，跪于道旁，振大喜，升为户部左侍郎",
     "event_significance": "一般掌故", "political_impact": "甲科六卿逢迎内竖之丑",
     "source_type": "文献转引", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-038", "item_id": "33-036", "title": "武宗赐歌童杨芝名羊脂玉",
     "description": "武宗南幸至杨文襄家，悦歌童杨芝白皙，赐名羊脂玉命从驾北上；其妻父宋闵以人命系常州府狱，巡按御史李东急命知府李嵩唤出免罪取女送府从上至京师。先是有歌者头上白，几被召而竟阉。",
     "event_type": "宫廷", "date": "正德间", "reign": "正德", "location": "南京—京师",
     "participants": ["杨芝", "武宗"], "outcome": "同为歌童而幸不幸至此",
     "source_text": "上悦其白皙，问何名，曰杨芝，赐名曰羊脂玉",
     "event_significance": "轶闻", "political_impact": "武宗南巡宠幸伶人之实态",
     "source_type": "传闻", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-039", "item_id": "33-037", "title": "汪鋐独主迁显陵之议",
     "description": "嘉靖大礼之议自张桂倡之，至奉迁显陵，下至厨役王福随全亦效之；士君子无一人以为可，惟汪鋐独主迁移一说，则章圣太后尚无恙也。魏恭简托桂萼密进种子秘方，高文瑞撰玄文叩坛求媚。",
     "event_type": "朝政", "date": "嘉靖间", "reign": "嘉靖", "location": "京师—显陵",
     "participants": ["汪鋐", "桂萼", "魏恭简", "高文瑞"], "outcome": "阿谄成风即一时号为正人亦献谀希宠",
     "source_text": "然士君子无一人以为可者，惟汪鋐独主迁移一说",
     "event_significance": "一般掌故", "political_impact": "大礼议腐蚀士风之实证",
     "source_type": "传闻", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-040", "item_id": "33-038", "title": "嘉靖帝采芝献瑞与王金祸",
     "description": "嘉靖丙辰八月上问礼臣古用芝草入药当求之何所，尚书吴山以《本草》、《论衡》诸书条对；诏采芝于元岳龙虎诸山，臣民献芝接踵，采芝使四出。末年王金献芝得圣眷召为御医，炼芝为药杂进不经之剂致损圣躬，上仙后坐子杀父律论剐。",
     "event_type": "宫廷", "date": "嘉靖丙辰—万历初", "reign": "嘉靖—万历", "location": "京师—诸名山",
     "participants": ["吴山", "王金", "陶仲文", "顾可学"], "outcome": "主事王健以采龙涎出，左通政王槐以开矿出，所至采办遍天下",
     "source_text": "上问礼臣：\u201c古用芝草入药，当求之何所，今可得否？\u201d",
     "event_significance": "重大政治", "political_impact": "玄修风气下服食之祸上及君躬",
     "source_type": "文献转引", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-041", "item_id": "33-039", "title": "周忱织绒地毯馈王振",
     "description": "周文襄抚江南最久功最大，然正谲兼用：王振新建私第，文襄密令人规度其厅事内室广狭长短，命松江府织绒地衣以馈，振铺之不爽分寸，凡有奏请批答无不如意。振死籍家得金观音背镂孝孙周忱进。",
     "event_type": "朝政", "date": "正统间", "reign": "正统", "location": "江南—京师",
     "participants": ["周文襄", "王振", "钱昕"], "outcome": "以此得便宜展布，委曲从事亦豪杰作用",
     "source_text": "命松江府织绒地衣以馈，振铺之不爽分寸，因大喜",
     "event_significance": "一般掌故", "political_impact": "能臣事权阉以行其政之策略",
     "source_type": "文献转引", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-042", "item_id": "33-040", "title": "宋沧献白兔开瑞物之端",
     "description": "嘉靖十一年四川巡按御史宋沧获白兔于梁山县以献，礼部请贺，献于太庙世庙呈两宫太后，百官表贺，汪鋐献诗夏言献颂郭维藩以献赋忤旨革职闲住。嗣后吴山得白鹿、陈轼献白兔，进瑞物者接踵。",
     "event_type": "朝政", "date": "嘉靖十一年", "reign": "嘉靖", "location": "京师—梁山",
     "participants": ["宋沧", "汪鋐", "夏言", "郭维藩"], "outcome": "抚镇重臣贡瑞取媚自此始，宗室诸王效尤皆不令终",
     "source_text": "嘉靖十一年四川巡按御史宋沧，获白兔于梁山县以献，礼部请贺",
     "event_significance": "一般掌故", "political_impact": "祥瑞政治与言官失职",
     "source_type": "文献转引", "vs_official_history": "与正史合"},
    {"event_id": "EVT-33-043", "item_id": "33-041", "title": "罗汝敬谕交址碎器服黎利",
     "description": "罗汝敬受宣宗知超为工部右侍郎，往谕交址黎利，以利设女乐不悦尽碎其饮器，黎惧遣使驰谢；寻提督陕西屯田受赃论绞，蒙宥再往，遇诉讼重则付都司布政按察及巡按御史究问。",
     "event_type": "边政", "date": "宣德间", "reign": "宣德", "location": "交址—陕西",
     "participants": ["罗汝敬", "黎利", "宣宗"], "outcome": "甫脱死囚遽膺重任，亦可废祖宗时制度",
     "source_text": "以利设女乐不悦，尽碎其饮器，黎惧，遣使驰谢",
     "event_significance": "重大政治", "political_impact": "宣德处置交址之一幕",
     "source_type": "文献转引", "vs_official_history": "补正史之阙"},
    {"event_id": "EVT-33-044", "item_id": "33-042", "title": "蔡国熙张子仁创势家",
     "description": "苏松兵备广平蔡国熙本华亭徐相讲学高足，既应高新郑幕，百方窘华亭没其产戍其子；嘉湖兵备无锡张子仁法绳吴太宰舍人子，长公太守日扶服顿颡于邑令，禾郡有太守跪知县之谚。",
     "event_type": "社会", "date": "万历间", "reign": "万历", "location": "松江—嘉兴",
     "participants": ["蔡国熙", "徐相", "陆五台", "吴绍"], "outcome": "华亭几欲投缳，吴太宰父子相继死，蔡斥张调方解",
     "source_text": "既应高新郑幕，百方窘华亭，没其产，戍其子",
     "event_significance": "一般掌故", "political_impact": "监司与绅宦相抗两败俱伤",
     "source_type": "传闻", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-045", "item_id": "33-043", "title": "周汝砺龙阳解后好外而殁",
     "description": "周用斋汝砺文名藉甚举南畿解元，馆于湖州南浔董宗伯家，性朴茂未解男色；主人令童子乘醉纳其茎，乃大呼龙山真圣人，自是遂溺于男宠不问妍媸老幼，后举丁丑进士竟以好外羸惫而殁。",
     "event_type": "社会", "date": "万历丁丑前后", "reign": "万历", "location": "湖州南浔",
     "participants": ["周用斋"], "outcome": "远近怪笑，竟以是殒身",
     "source_text": "举南畿解元，久未第，馆于湖州南浔董宗伯家",
     "event_significance": "轶闻", "political_impact": "名士性情之变一例",
     "source_type": "传闻", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-046", "item_id": "33-045", "title": "杨宣妻王氏以妒受杖",
     "description": "礼部致仕左侍郎杨宣妻王氏素妒悍杖杀侍婢十余人，东厂上其事，刑部拟赎如律；上以肆意残酷仍命杖之五十使知所儆。此成化末年事；弘治十一年泗州知州许弼妻孙氏妒妾事发，亦命杖八十离异。",
     "event_type": "司法", "date": "成化末年", "reign": "成化", "location": "京师",
     "participants": ["杨宣"], "outcome": "命妇不纳赎受杖，别开一例",
     "source_text": "上曰：王氏虽命妇，例应纳赎，但肆意残酷，仍命刑部杖之五十",
     "event_significance": "一般掌故", "political_impact": "妒悍之妇稍戢之一端",
     "source_type": "文献转引", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-047", "item_id": "33-046", "title": "常琇通义父妾龙闰娶方瑛妾",
     "description": "僧官常琇拜故南和伯方瑛为父，又通瑛妾，为其徒所告，以奸义父之妾杖一百充铁岭卫军；御马监左监丞龙闰娶方瑛妾许氏为妻，事发命离异，闰送司礼监治之。俱成化年间事。",
     "event_type": "司法", "date": "成化间", "reign": "成化", "location": "京师",
     "participants": ["常琇", "方瑛", "龙闰"], "outcome": "瑛身后姬侍或耦妖秃或配淫阉，俱彻圣听",
     "source_text": "以琇奸义父之妾，杖一百充铁岭卫军",
     "event_significance": "轶闻", "political_impact": "僧宦秽闻关圣听",
     "source_type": "文献转引", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-048", "item_id": "33-048", "title": "嘉靖十年裁西苑豹房勇士",
     "description": "嘉靖十年兵部覆勇士张升奏：西苑豹房畜土豹一只至役勇士二百四十名，岁廪二千八百石占地十顷岁租七百金，实皆典守内臣侵牟；请量留四十人余还营差操，上从之。",
     "event_type": "制度变动", "date": "嘉靖十年", "reign": "嘉靖", "location": "西苑豹房",
     "participants": ["张升"], "outcome": "内廷畜费少纾，然举一豹而他物可知",
     "source_text": "西苑豹房畜土豹一只，至役勇士二百四十名，岁廪二千八百石",
     "event_significance": "一般掌故", "political_impact": "内府滥费之真相",
     "source_type": "亲历", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-049", "item_id": "33-049", "title": "洪武二十七年建十六楼于江东门外",
     "description": "洪武二十七年上以海内太平思与民偕乐，命工部建十酒楼于江东门外，有鹤鸣醉仙讴歌鼓腹来宾重译等名，又增作五楼；诏赐文武百官钞命宴于醉仙楼，五楼专处侑酒歌妓，又命宴博士钱宰等于新成酒楼各献诗谢。",
     "event_type": "社会", "date": "洪武二十七年", "reign": "洪武", "location": "南京江东门外",
     "participants": ["工部", "钱宰"], "outcome": "不设官酝以收榷课，最为清朝佳事",
     "source_text": "命工部建十酒楼于江东门外，有鹤鸣、醉仙、讴歌、鼓腹、来宾、重译等名",
     "event_significance": "制度变动", "political_impact": "国初与民同乐之政",
     "source_type": "文献转引", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-050", "item_id": "33-051", "title": "永乐十五年建安乐堂",
     "description": "禁城北安门外有安乐堂，为永乐十五年所建，以处工匠之疾病者；近来惟内臣卑秩无私宅可依遇疾且殆者徙入以待其殒，槥送净乐堂焚化。",
     "event_type": "宫廷", "date": "永乐十五年", "reign": "永乐", "location": "禁城北安门外",
     "participants": ["安乐堂"], "outcome": "宫人病故转停尸房易朱棺火葬",
     "source_text": "有安乐堂，为永乐十五年所建，以处工匠之疾病者",
     "event_significance": "一般掌故", "political_impact": "内廷生死之惨状",
     "source_type": "传闻", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-051", "item_id": "33-052", "title": "厚载门翊坤宫不避庙讳御名",
     "description": "禁城北门名厚载即玄武门，二字俱犯世宗穆宗庙讳上一字，上下通称不避；今上皇贵妃郑氏所居宫名翊坤宫，上一字即今上御名，公然直呼无一人议及。",
     "event_type": "宫廷", "date": "万历间", "reign": "万历", "location": "禁城",
     "participants": ["穆宗"], "outcome": "此等事俱不可解",
     "source_text": "二字俱犯世宗、穆宗庙讳上一字，上下通称不避",
     "event_significance": "一般掌故", "political_impact": "讳典之弛",
     "source_type": "传闻", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-052", "item_id": "33-053", "title": "都城正月十八耍烟九",
     "description": "京师正月灯市例以十八日收灯，次日都中士女倾国出城西白云观联袂嬉游，名为耍烟九；都下耆旧云全真道人邱元清以是日就阉故名阉九，四方全真道人不期而集者不下数万。",
     "event_type": "社会", "date": "每年正月十八", "reign": "万历", "location": "京师白云观",
     "participants": ["邱元清", "张三丰"], "outcome": "阉九之说亦似不妄",
     "source_text": "都中士女，倾国出城西郊所谓白云观者，联袂嬉游",
     "event_significance": "轶闻", "political_impact": "京师风物之掌故学",
     "source_type": "亲历", "vs_official_history": "正史不载"},
    {"event_id": "EVT-33-053", "item_id": "33-054", "title": "闽俗契兄弟契儿",
     "description": "闽人酷重男色，长者为契兄少者为契弟，兄入弟家父母抚爱如婿；近乃有称契儿者，壮夫聚姿首韶秀者以父自居，最为逆乱之尤。又嘉靖间广西上冻州土知州赵元恩呼私通其母之太平陆监生为契父。",
     "event_type": "社会", "date": "万历间", "reign": "万历", "location": "福建—广西",
     "participants": ["赵元恩"], "outcome": "契父之称亦有所本",
     "source_text": "闽人酷重男色，无论贵贱妍媸，各以其类相结",
     "event_significance": "一般掌故", "political_impact": "方俗之奇与海寇渊源",
     "source_type": "传闻", "vs_official_history": "正史不载"},
]

# ---------------------------------------------------------------------------
# C1 任职层 APPT-33-NNN
# ---------------------------------------------------------------------------
APPTS = [
    {"appt_id": "APPT-33-001", "item_id": "33-002", "person": E["杨照"], "person_text": "杨照",
     "position": "辽东总兵官", "reign": "嘉靖", "date": "嘉靖末年", "type": "现任",
     "source": "用故将杨照为辽东总兵官，照感上知遇", "controversy": "遭弹劾",
     "note": "与巡抚侯汝谅、户部管饷郎中何东序互讦回卫，久之复起战殁"},
    {"appt_id": "APPT-33-002", "item_id": "33-003", "person": E["余肃敏"], "person_text": "余肃敏",
     "position": "兵部尚书（大司马）", "reign": "成化", "date": "成化十四年", "type": "现任",
     "source": "时余肃敏为大司马，不敢决，请廷臣集议", "controversy": "有争议",
     "note": "汪直请武举设科，不敢决请廷议"},
    {"appt_id": "APPT-33-003", "item_id": "33-004", "person": E["石亨"], "person_text": "石亨",
     "position": "总兵官", "reign": "景泰", "date": "景泰中", "type": "现任",
     "source": "武清侯石亨为总兵，请征剿也先", "controversy": "有争议",
     "note": "请刺军人臂字为景帝所驳"},
    {"appt_id": "APPT-33-004", "item_id": "33-006", "person": E["李暠"], "person_text": "李暠",
     "position": "大宁都指挥佥事", "reign": "正统", "date": "正统十三年", "type": "现任",
     "source": "大宁都指挥佥事李暠，道遇祁州知州李玉不避道，杖之", "controversy": "遭弹劾",
     "note": "为巡按御史段信所劾"},
    {"appt_id": "APPT-33-005", "item_id": "33-007", "person": E["朱先"], "person_text": "朱先",
     "position": "福建总兵（大帅）", "reign": "嘉靖—万历", "date": "嘉靖—万历", "type": "升迁",
     "source": "即以便宜拜守备，逾年至参将", "controversy": "遭弹劾",
     "note": "胡宗宪便宜拜守备，再进再谪，终为福建大帅"},
    {"appt_id": "APPT-33-006", "item_id": "33-009", "person": E["毕旺"], "person_text": "毕旺",
     "position": "锦衣指挥同知", "reign": "景泰", "date": "景泰四年", "type": "现任",
     "source": "锦衣指挥同知毕旺，疏援永乐旧例", "controversy": "有争议",
     "note": "疏请环卫近臣概许麟服，开武弁僭服之端"},
    {"appt_id": "APPT-33-007", "item_id": "33-011", "person": E["李如松"], "person_text": "李如松",
     "position": "提督（平壤之役统帅）", "reign": "万历", "date": "万历癸巳", "type": "现任",
     "source": "李如松以平殄在迩，不欲他兵分其功，潜率家丁二千人", "controversy": "有争议",
     "note": "专仗家丁树勋，碧蹄馆之败几以身殉"},
    {"appt_id": "APPT-33-008", "item_id": "33-012", "person": E["庐祥"], "person_text": "庐祥",
     "position": "巡抚延绥都御史", "reign": "成化", "date": "成化初年", "type": "现任",
     "source": "巡抚延绥都御史庐祥建议，以营伍兵少", "controversy": "无争议",
     "note": "土兵之设始于祥之建议"},
    {"appt_id": "APPT-33-009", "item_id": "33-014", "person": E["王建中"], "person_text": "王建中",
     "position": "刑科给事中", "reign": "万历", "date": "万历辛卯冬", "type": "现任",
     "source": "刑科给事中王建中，特疏纠之", "controversy": "无争议",
     "note": "纠山人乐新炉捏造飞语"},
    {"appt_id": "APPT-33-010", "item_id": "33-015", "person": E["戴士衡"], "person_text": "戴士衡",
     "position": "吏科给事中", "reign": "万历", "date": "万历戊戌", "type": "现任",
     "source": "吏科给事中戴士衡首发大难", "controversy": "无争议",
     "note": "曾为张新建知县"},
    {"appt_id": "APPT-33-011", "item_id": "33-015", "person": E["樊玉衡"], "person_text": "樊玉衡",
     "position": "全椒知县（原任御史）", "reign": "万历", "date": "万历戊戌", "type": "贬谪",
     "source": "前任御史今全椒知县樊玉衡者继之", "controversy": "无争议",
     "note": "由御史出为县令，继戴士衡参吕坤"},
    {"appt_id": "APPT-33-012", "item_id": "33-023", "person": E["夏瑄"], "person_text": "夏瑄",
     "position": "湖广常德卫指挥使", "reign": "天顺", "date": "天顺二年九月", "type": "罢黜",
     "source": "有湖广常德卫指挥使夏瑄，杀依己以居者妻子三人", "controversy": "有争议",
     "note": "本论凌迟，因子疏代刑且翻雇工人之辨，竟得复职"},
    {"appt_id": "APPT-33-013", "item_id": "33-024", "person": E["黄廷聘"], "person_text": "黄廷聘",
     "position": "巡按浙江御史", "reign": "嘉靖", "date": "嘉靖四十四年", "type": "罢黜",
     "source": "上命廷聘冠带闲住", "controversy": "遭弹劾",
     "note": "回籍过衡山被知县陈安志发箧得金银，张永明发其状"},
    {"appt_id": "APPT-33-014", "item_id": "33-024", "person": E["钱一本"], "person_text": "钱一本",
     "position": "试御史（原任庐陵知县）", "reign": "万历", "date": "万历辛卯", "type": "现任",
     "source": "原任江西庐陵知县新任试御史钱一本，追论巡按江西丁忧御史祝大舟", "controversy": "无争议",
     "note": "以旧属吏发同官秽状"},
    {"appt_id": "APPT-33-015", "item_id": "33-025", "person": E["张璁"], "person_text": "张璁",
     "position": "兵部左侍郎", "reign": "嘉靖", "date": "嘉靖六年", "type": "现任",
     "source": "张璁以兵部左侍郎，为北科道所纠", "controversy": "遭弹劾",
     "note": "丁亥大计被纠，奉旨留用而心恨甚"},
    {"appt_id": "APPT-33-016", "item_id": "33-025", "person": E["桂萼"], "person_text": "桂萼",
     "position": "礼部右侍郎", "reign": "嘉靖", "date": "嘉靖六年", "type": "现任",
     "source": "桂萼以礼部右侍郎，为南科道所纠", "controversy": "遭弹劾",
     "note": "疏请科道互相纠察以报私怨"},
    {"appt_id": "APPT-33-017", "item_id": "33-029", "person": E["林聪"], "person_text": "林聪",
     "position": "吏科都给事中→右副都御史", "reign": "景泰—天顺", "date": "景泰四年—天顺三年", "type": "现任",
     "source": "至天顺三年，则林聪已为右副都御史，以忧归里，奉旨行取来京", "controversy": "有争议",
     "note": "自奏京官听终制，及己以忧归却一辞不允即赴任"},
    {"appt_id": "APPT-33-018", "item_id": "33-030", "person": E["刘文泰"], "person_text": "刘文泰",
     "position": "右通政管太医院使→院判", "reign": "成化—弘治", "date": "成化末", "type": "贬谪",
     "source": "刘文泰先任右通政，管太医院使，以投剂乖方，致损宪宗", "controversy": "遭弹劾",
     "note": "给事中韩重、御史陈谷交章参劾，孝宗命降为院判"},
    {"appt_id": "APPT-33-019", "item_id": "33-031", "person": E["马从谦"], "person_text": "马从谦",
     "position": "光禄少卿", "reign": "嘉靖", "date": "嘉靖间", "type": "现任",
     "source": "光禄少卿马从谦，嘉靖间劾提督光禄太监杜泰", "controversy": "遭弹劾",
     "note": "反被诬诽谤不忠，诏杖八十毙杖下"},
    {"appt_id": "APPT-33-020", "item_id": "33-032", "person": E["柰亨"], "person_text": "柰亨",
     "position": "光禄寺卿", "reign": "正统", "date": "正统六年", "type": "现任",
     "source": "光禄寺大官署丞张冕，奏本寺卿柰亨借供祀，盗取猪鹅肉", "controversy": "遭弹劾",
     "note": "论法难容姑宥之，后两充廷试读卷官又荫子"},
    {"appt_id": "APPT-33-021", "item_id": "33-034", "person": E["朱隆禧"], "person_text": "朱隆禧",
     "position": "太仆寺卿→礼部右侍郎", "reign": "嘉靖", "date": "嘉靖间", "type": "升迁",
     "source": "作太极衣以献，盖房中术也", "controversy": "无争议",
     "note": "以方技登九列"},
    {"appt_id": "APPT-33-022", "item_id": "33-035", "person": E["刘睿"], "person_text": "刘睿",
     "position": "吏科都给事中→户部尚书", "reign": "正统—成化", "date": "正统间", "type": "升迁",
     "source": "路遇王振，跪于道旁，振大喜，升为户部左侍郎", "controversy": "有争议",
     "note": "逢迎内竖致位六卿，成化七年始卒"},
    {"appt_id": "APPT-33-023", "item_id": "33-035", "person": E["李燧"], "person_text": "李燧",
     "position": "工部尚书（致仕复起）", "reign": "正德—嘉靖", "date": "正德间", "type": "升迁",
     "source": "永至京师，吏部荐之，召复故官，再长冬曹", "controversy": "有争议",
     "note": "敝衣破冠束赐玉带跪迎张永乞怜复官"},
    {"appt_id": "APPT-33-024", "item_id": "33-038", "person": E["吴山"], "person_text": "吴山",
     "position": "礼部尚书", "reign": "嘉靖", "date": "嘉靖辛酉", "type": "罢黜",
     "source": "吴山为礼部尚书时，值辛酉年正旦，以日食不及分数当免救，上欲臣下称贺，山不从，遂罢归", "controversy": "有争议",
     "note": "高安人，后谥文端；罢归盖借以饰昔日之逢迎"},
    {"appt_id": "APPT-33-025", "item_id": "33-038", "person": E["王金"], "person_text": "王金",
     "position": "御医", "reign": "嘉靖", "date": "嘉靖末年", "type": "现任",
     "source": "王金献芝，大得圣眷，召为御医", "controversy": "无争议",
     "note": "炼芝杂进不经之剂致损圣躬，坐子杀父律论剐"},
    {"appt_id": "APPT-33-026", "item_id": "33-040", "person": E["宋沧"], "person_text": "宋沧",
     "position": "巡按四川御史", "reign": "嘉靖", "date": "嘉靖十一年", "type": "现任",
     "source": "嘉靖十一年四川巡按御史宋沧，获白兔于梁山县以献", "controversy": "有争议",
     "note": "贡瑞取媚，可呼为白兔都御史"},
    {"appt_id": "APPT-33-027", "item_id": "33-040", "person": E["汪鋐"], "person_text": "汪鋐",
     "position": "吏部尚书", "reign": "嘉靖", "date": "嘉靖十一年", "type": "现任",
     "source": "于是吏部尚书汪鋐、侍讲学士葵昂献诗", "controversy": "无争议",
     "note": "献诗颂瑞，自献甘露后贡媚不辍"},
    {"appt_id": "APPT-33-028", "item_id": "33-041", "person": E["罗汝敬"], "person_text": "罗汝敬",
     "position": "工部右侍郎总督陕西屯田", "reign": "宣德—正统", "date": "宣德间", "type": "升迁",
     "source": "受宣宗知，超为工部右侍郎，往谕交址黎利", "controversy": "有争议",
     "note": "论绞蒙宥充为事官仍往总督，甫脱死囚遽膺重任"},
    {"appt_id": "APPT-33-029", "item_id": "33-045", "person": E["杨宣"], "person_text": "杨宣",
     "position": "礼部左侍郎（致仕）", "reign": "天顺—弘治", "date": "成化末", "type": "致仕",
     "source": "礼部致仕左侍郎杨宣妻王氏，素妒悍", "controversy": "无争议",
     "note": "进士起家天顺初为御史，立拜鸿胪少卿历宪宗朝甚被眷注"},
    {"appt_id": "APPT-33-030", "item_id": "33-046", "person": E["常琇"], "person_text": "常琇",
     "position": "僧官", "reign": "成化", "date": "成化间", "type": "罢黜",
     "source": "以琇奸义父之妾，杖一百充铁岭卫军", "controversy": "遭弹劾",
     "note": "为其徒所告，下锦衣卫狱"},
    {"appt_id": "APPT-33-031", "item_id": "33-046", "person": E["龙闰"], "person_text": "龙闰",
     "position": "御马监左监丞", "reign": "成化", "date": "成化间", "type": "贬谪",
     "source": "御马监左监丞龙闰，娶方瑛妾许氏为妻，事发", "controversy": "有争议",
     "note": "命离异，送司礼监治之"},
    {"appt_id": "APPT-33-032", "item_id": "33-012", "person": E["赵文华"], "person_text": "赵文华",
     "position": "督察浙江军务", "reign": "嘉靖", "date": "嘉靖间", "type": "现任",
     "source": "赵文华誓师浙江，故令乡官领兵", "controversy": "有争议",
     "note": "乡官领兵间田赡兵之议为杨博所覆而寝"},
]

# ---------------------------------------------------------------------------
# C3 关系层 REL-33-NNN
# ---------------------------------------------------------------------------
RELS = [
    {"rel_id": "REL-33-001", "item_id": "33-007", "source": E["胡襄愍"], "source_text": "胡襄愍（胡宗宪）",
     "target": E["朱先"], "target_text": "朱先", "relation": "举荐", "direction": "单向",
     "evidence": "胡襄愍为督府，即以便宜拜守备", "detail": "朱先应募为前锋一日馘倭十三人，胡宗宪便宜授职，由守备至参将",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-002", "item_id": "33-003", "source": E["汪直"], "source_text": "汪直",
     "target": E["余肃敏"], "target_text": "余肃敏", "relation": "上下级", "direction": "单向",
     "evidence": "时余肃敏为大司马，不敢决", "detail": "汪直擅权请武举设科，兵部尚书余子俊畏不敢决，请廷臣集议",
     "evidence_strength": "推断", "confidence": "medium"},
    {"rel_id": "REL-33-003", "item_id": "33-015", "source": E["戴士衡"], "source_text": "戴士衡",
     "target": E["吕新吾"], "target_text": "吕新吾（吕坤）", "relation": "弹劾", "direction": "单向",
     "evidence": "吏科给事中戴士衡首发大难，参吕包藏祸心", "detail": "戴以吕刻闺范得贵妃之序，劾其有敬宗林甫之谋",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-004", "item_id": "33-015", "source": E["樊玉衡"], "source_text": "樊玉衡",
     "target": E["吕新吾"], "target_text": "吕新吾", "relation": "弹劾", "direction": "单向",
     "evidence": "而前任御史今全椒知县樊玉衡者继之，举朝骇愕", "detail": "樊继戴士衡之后继续攻讦吕坤",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-005", "item_id": "33-015", "source": E["吕新吾"], "source_text": "吕新吾",
     "target": E["张新建"], "target_text": "张新建（张位）", "relation": "敌对", "direction": "双向",
     "evidence": "吕与秀水沈继山争为少宰，俱不得，而沈独见逐，沈与新建素厚，吕遂疑新建为沈报复矣",
     "detail": "争铨不遂转疑张位主使谤书，戊戌之案两家相攻，张位卒借东事被逐",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-006", "item_id": "33-016", "source": E["皇贵妃"], "source_text": "皇贵妃郑氏",
     "target": E["郑承恩"], "target_text": "郑承恩", "relation": "父子亲属", "direction": "双向",
     "evidence": "此贵妃旧序，妃兄郑国泰之伯郑承恩重刻", "detail": "郑氏外戚，承恩为贵妃兄辈，重刊闺范并上辨疏",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-007", "item_id": "33-021", "source": E["潘季驯"], "source_text": "潘季驯",
     "target": E["江陵"], "target_text": "张居正（江陵）", "relation": "其他", "direction": "单向",
     "evidence": "刑部尚书潘季驯请宽故相江陵子孙", "detail": "潘受江陵恩，江陵殁后独请宽其子孙，河工自叙推江陵发踪之功",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-008", "item_id": "33-021", "source": E["李植"], "source_text": "李植",
     "target": E["潘季驯"], "target_text": "潘季驯", "relation": "弹劾", "direction": "单向",
     "evidence": "御史李植劾其往年自叙河工", "detail": "李植劾潘并诬及家门，父访察充军兄人命拟死，开弹章及父兄之恶例",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-009", "item_id": "33-024", "source": E["张永明"], "source_text": "张永明（台长）",
     "target": E["黄廷聘"], "target_text": "黄廷聘", "relation": "弹劾", "direction": "单向",
     "evidence": "掌院左都御史张永明发其状", "detail": "以堂官发台臣赃状，命冠带闲住，台长可谓能举其职",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-010", "item_id": "33-024", "source": E["辛自修"], "source_text": "辛自修",
     "target": E["沈汝梁"], "target_text": "沈汝梁", "relation": "弹劾", "direction": "单向",
     "evidence": "南京掌院右都御史辛自修，疏劾巡视下江御史沈汝梁", "detail": "丙戌年以堂官参治台臣，赃贿数万，追赃遣戍",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-011", "item_id": "33-024", "source": E["庞尚鹏"], "source_text": "庞尚鹏",
     "target": E["孙以仁"], "target_text": "孙以仁", "relation": "弹劾", "direction": "单向",
     "evidence": "屯盐都御史庞尚鹏，疏劾淮扬巡盐御史孙以仁", "detail": "同事宪臣相纠侵匿盐银千余两，先革职听勘",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-012", "item_id": "33-024", "source": E["钱一本"], "source_text": "钱一本",
     "target": E["祝大舟"], "target_text": "祝大舟", "relation": "弹劾", "direction": "单向",
     "evidence": "新任试御史钱一本，追论巡按江西丁忧御史祝大舟", "detail": "以旧属吏发同官秽状，缇骑逮京下诏狱遣戍追赃",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-013", "item_id": "33-025", "source": E["桂萼"], "source_text": "桂萼",
     "target": E["杨廷和"], "target_text": "杨廷和", "relation": "敌对", "direction": "单向",
     "evidence": "萼乃疏谓杨廷和私党犹在言路", "detail": "大礼议之余恨，借丁亥考察排廷和之党",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-014", "item_id": "33-025", "source": E["张璁"], "source_text": "张璁",
     "target": E["杨廷和"], "target_text": "杨廷和", "relation": "敌对", "direction": "双向",
     "evidence": "张璁以兵部左侍郎，为北科道所纠", "detail": "张桂与杨廷和议礼相左，及第互纠皆缘大礼恩怨",
     "evidence_strength": "推断", "confidence": "medium"},
    {"rel_id": "REL-33-015", "item_id": "33-027", "source": E["郑颙"], "source_text": "郑颙",
     "target": E["王振"], "target_text": "王振", "relation": "其他", "direction": "单向",
     "evidence": "时王振初窃柄，颙奏非结交近侍而何", "detail": "御史建白请以内官抽分税课，实阿附近侍",
     "evidence_strength": "推断", "confidence": "medium"},
    {"rel_id": "REL-33-016", "item_id": "33-028", "source": E["房寰"], "source_text": "房寰",
     "target": E["海忠介"], "target_text": "海瑞（忠介）", "relation": "弹劾", "direction": "单向",
     "evidence": "海忠介为房寰所论列，愤极上疏辩析", "detail": "房再疏攻海，专录笑谑之语，泼皮无赖之称自此而始",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-017", "item_id": "33-029", "source": E["李秉彝"], "source_text": "李秉彝",
     "target": E["林聪"], "target_text": "林聪", "relation": "其他", "direction": "单向",
     "evidence": "曩者吏科都给事林聪奏，凡京官非与机要者", "detail": "李秉彝引林聪前疏为据请止王复夺情；林后自处以机要，前后矛盾",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-018", "item_id": "33-031", "source": E["马从谦"], "source_text": "马从谦",
     "target": E["杜泰"], "target_text": "杜泰", "relation": "弹劾", "direction": "单向",
     "evidence": "劾提督光禄太监杜泰，干没内帑数万", "detail": "马劾杜泰反被诬诽谤不忠，诏杖八十毙杖下",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-019", "item_id": "33-035", "source": E["刘睿"], "source_text": "刘睿",
     "target": E["王振"], "target_text": "王振", "relation": "其他", "direction": "单向",
     "evidence": "路遇王振，跪于道旁，振大喜", "detail": "甲科给事中跪逢内竖，由是致位六卿",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-020", "item_id": "33-035", "source": E["李燧"], "source_text": "李燧",
     "target": E["张永"], "target_text": "张永", "relation": "举荐", "direction": "单向",
     "evidence": "永至京师，吏部荐之，召复故官", "detail": "致仕尚书跪迎张永乞怜，因是复官再长冬曹",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-021", "item_id": "33-037", "source": E["汪鋐"], "source_text": "汪鋐",
     "target": E["桂萼"], "target_text": "桂萼", "relation": "党派", "direction": "双向",
     "evidence": "惟汪鋐独主迁移一说", "detail": "大礼议中张桂集团，汪鋐附其议并主迁显陵",
     "evidence_strength": "推断", "confidence": "medium"},
    {"rel_id": "REL-33-022", "item_id": "33-040", "source": E["宋沧"], "source_text": "宋沧",
     "target": E["汪鋐"], "target_text": "汪鋐", "relation": "同僚", "direction": "双向",
     "evidence": "抚镇重臣贡瑞取媚，自嘉靖八年汪鋐献甘露后所仅见", "detail": "宋沧献白兔与汪鋐献甘露同科谄风，百官表贺成例",
     "evidence_strength": "推断", "confidence": "medium"},
    {"rel_id": "REL-33-023", "item_id": "33-041", "source": E["罗汝敬"], "source_text": "罗汝敬",
     "target": E["黎利"], "target_text": "黎利", "relation": "其他", "direction": "单向",
     "evidence": "往谕交址黎利，以利设女乐不悦，尽碎其饮器", "detail": "奉使谕意，碎器立威，黎惧遣使驰谢",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-024", "item_id": "33-042", "source": E["蔡国熙"], "source_text": "蔡国熙",
     "target": E["徐相"], "target_text": "徐相", "relation": "恩怨", "direction": "单向",
     "evidence": "既应高新郑幕，百方窘华亭，没其产，戍其子", "detail": "蔡本徐相讲学高足，反为权势百方酷治其师之门",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-025", "item_id": "33-042", "source": E["陆五台"], "source_text": "陆五台",
     "target": E["蔡国熙"], "target_text": "蔡国熙", "relation": "其他", "direction": "双向",
     "evidence": "时陆五台太宰以卿士居家，与蔡同侍讲席者，曲为排解", "detail": "同侍讲席，陆以门墙谊为徐氏排解，蔡不受",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-026", "item_id": "33-042", "source": E["吴绍"], "source_text": "吴绍",
     "target": E["吴鹏"], "target_text": "吴鹏", "relation": "父子亲属", "direction": "双向",
     "evidence": "绍为太宰鹏仲子", "detail": "吴鹏家居纵舍人子不法，兵备张子仁法绳之，吴氏父子不胜忿相继死",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-027", "item_id": "33-046", "source": E["常琇"], "source_text": "常琇",
     "target": E["方瑛"], "target_text": "方瑛（南和伯）", "relation": "父子亲属", "direction": "双向",
     "evidence": "僧官常琇者，拜故南和伯方瑛为父", "detail": "义父子而通其妾，杖一百充铁岭卫军",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-028", "item_id": "33-014", "source": E["王建中"], "source_text": "王建中",
     "target": E["乐新炉"], "target_text": "乐新炉", "relation": "弹劾", "direction": "单向",
     "evidence": "刑科给事中王建中，特疏纠之", "detail": "王疏纠山人捏造飞语，新炉逮诏狱荷立枷戍之寻死",
     "evidence_strength": "直接表述", "confidence": "high"},
    {"rel_id": "REL-33-029", "item_id": "33-019", "source": E["陈矩"], "source_text": "陈矩",
     "target": E["俶生光"], "target_text": "俶生光", "relation": "其他", "direction": "单向",
     "evidence": "提督东厂太监陈矩奏称", "detail": "陈矩提督东厂访得妖书封进，狱成仅捕俶生光服上刑塞责，真造撰之人终莫能明",
     "evidence_strength": "推断", "confidence": "medium"},
]

# ---------------------------------------------------------------------------
# L6 引书层 CIT-33-NNN
# ---------------------------------------------------------------------------
CITS = [
    {"cit_id": "CIT-33-001", "item_id": "33-038", "cited_work": u"《论衡》", "author": u"王充",
     "cite_context": u"直引", "source_text": u"王充《论衡》云：芝生于土，土气和，故芝草生",
     "quoted_text": u"芝生于土，土气和，故芝草生", "reign": u"汉", "confidence": "high"},
    {"cit_id": "CIT-33-002", "item_id": "33-038", "cited_work": u"《瑞命记》", "author": u"佚名",
     "cite_context": u"直引", "source_text": u"《瑞命记》云：王者德仁，则芝草生",
     "quoted_text": u"王者德仁，则芝草生", "reign": u"不详", "confidence": "medium"},
    {"cit_id": "CIT-33-003", "item_id": "33-038", "cited_work": u"《文选》", "author": u"萧统",
     "cite_context": u"直引", "source_text": u"《文选》云：煌煌灵芝，一年三秀",
     "quoted_text": u"煌煌灵芝，一年三秀", "reign": u"梁", "confidence": "high"},
    {"cit_id": "CIT-33-004", "item_id": "33-038", "cited_work": u"《汉旧仪》", "author": u"卫宏",
     "cite_context": u"直引", "source_text": u"《汉旧仪》云：芝有九茎，金色绿叶朱实，夜有光",
     "quoted_text": u"芝有九茎，金色绿叶朱实，夜有光", "reign": u"汉", "confidence": "high"},
    {"cit_id": "CIT-33-005", "item_id": "33-038", "cited_work": u"《黄帝内传》", "author": u"佚名",
     "cite_context": u"直引", "source_text": u"《黄帝内传》云：王母遣仙人歌万年长生之曲，授帝以石函玉笈之书",
     "quoted_text": u"王母遣仙人歌万年长生之曲", "reign": u"上古", "confidence": "medium"},
    {"cit_id": "CIT-33-006", "item_id": "33-033", "cited_work": u"《广典故》", "author": u"佚名",
     "cite_context": u"考辨", "source_text": u"按《广典故》云：以赀为郎，非赀财也",
     "quoted_text": u"以赀为郎，非赀财也", "reign": u"不详", "confidence": "medium"},
    {"cit_id": "CIT-33-007", "item_id": "33-033", "cited_work": u"《九章周髀》", "author": u"佚名",
     "cite_context": u"泛引", "source_text": u"其业以《九章周髀》，及假设疑数为算问",
     "quoted_text": None, "reign": u"周—汉", "confidence": "high"},
    {"cit_id": "CIT-33-008", "item_id": "33-033", "cited_work": u"《太初历》", "author": u"佚名",
     "cite_context": u"泛引", "source_text": u"又洛下闳与鲜于妄人俱同定《太初历》者",
     "quoted_text": None, "reign": u"汉", "confidence": "high"},
    {"cit_id": "CIT-33-009", "item_id": "33-048", "cited_work": u"《大明会典》", "author": u"徐溥等敕修",
     "cite_context": u"考辨", "source_text": u"载在《会典》，掌之太常",
     "quoted_text": None, "reign": u"明", "confidence": "high"},
    {"cit_id": "CIT-33-010", "item_id": "33-016", "cited_work": u"《女诫》", "author": u"班昭",
     "cite_context": u"泛引", "source_text": u"虽不敢上拟仁孝之《女诫》，章圣之《女训》",
     "quoted_text": None, "reign": u"汉", "confidence": "high"},
    {"cit_id": "CIT-33-011", "item_id": "33-015", "cited_work": u"《辨冤录》", "author": u"郑承恩",
     "cite_context": u"泛引", "source_text": u"郑畹《辨冤录》，世已不多见矣",
     "quoted_text": None, "reign": u"万历", "confidence": "high"},
    {"cit_id": "CIT-33-012", "item_id": "33-041", "cited_work": u"《弇州奇事》", "author": u"王世贞",
     "cite_context": u"直引", "source_text": u"弇州奇事云：汝敬为吉士时，曾充刑部吏",
     "quoted_text": u"汝敬为吉士时，曾充刑部吏", "reign": u"万历", "confidence": "high"},
    {"cit_id": "CIT-33-013", "item_id": "33-053", "cited_work": u"《典论》", "author": u"曹丕",
     "cite_context": u"直引", "source_text": u"魏文帝《典论》云：左慈到，人竞受其补导之术，至寺人严竣往从问受",
     "quoted_text": u"左慈到，人竞受其补导之术，至寺人严竣往从问受", "reign": u"魏", "confidence": "high"},
    {"cit_id": "CIT-33-014", "item_id": "33-050", "cited_work": u"《宴南市楼诗》", "author": u"揭轨",
     "cite_context": u"直引", "source_text": u"诏出金钱送酒垆，绮楼胜会集文儒",
     "quoted_text": u"诏出金钱送酒垆，绮楼胜会集文儒", "reign": u"明初", "confidence": "high"},
    {"cit_id": "CIT-33-015", "item_id": "33-044", "cited_work": u"《赠妓词》", "author": u"沈祖量",
     "cite_context": u"直引", "source_text": u"末句云：任他百般打骂百般羞，也只是书生薄福难消受",
     "quoted_text": u"任他百般打骂百般羞，也只是书生薄福难消受", "reign": u"万历", "confidence": "high"},
    {"cit_id": "CIT-33-016", "item_id": "33-049", "cited_work": u"蔡沈《书传》", "author": u"蔡沈",
     "cite_context": u"考辨", "source_text": u"上初观蔡氏书传，日月星辰运行与朱子诗传不同",
     "quoted_text": None, "reign": u"宋", "confidence": "high"},
    {"cit_id": "CIT-33-017", "item_id": "33-047", "cited_work": u"宋人诗", "author": u"佚名",
     "cite_context": u"泛引", "source_text": u"正如宋汴京“春如红锦堆中过，人似青罗幙里行”，真太平佳话也",
     "quoted_text": u"春如红锦堆中过，人似青罗幙里行", "reign": u"宋", "confidence": "high"},
    {"cit_id": "CIT-33-018", "item_id": "33-028", "cited_work": u"《中庸》", "author": u"子思",
     "cite_context": u"泛引", "source_text": u"且将《中庸》君子素位而行一章，与他讲解",
     "quoted_text": u"君子素位而行一章", "reign": u"先秦", "confidence": "high"},
]

# ---------------------------------------------------------------------------
# L7 论说层 OPN-33-NNN（评论者皆为作者沈德符）
# ---------------------------------------------------------------------------
OPNS = [
    {"opn_id": "OPN-33-001", "item_id": "33-002", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"讽刺", "target": u"武臣刺背效颦之风",
     "content": u"评嘉靖末杨照等刺背尽忠报国之事：割股剖肝本为美事，然相效不已即成套数，黄绾杨照惜其见不及此。",
     "source_text": u"割股剖肝，固尽孝美事，然效颦不已，亦成故套",
     "reign": u"嘉靖", "faction": u"无", "tone": u"嘲讽", "firsthand_witness": u"传闻", "confidence": "high"},
    {"opn_id": "OPN-33-002", "item_id": "33-003", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"感慨", "target": u"武举殿试破格之渐",
     "content": u"评汪直请武举殿试事：孝宗朝四方清晏犹不免为武弁破格，今南北多事武夫有跃冶之心，或议及殿试未可知。",
     "source_text": u"以孝宗亲礼儒臣，四方清晏，犹不免为缨弁破格",
     "reign": u"成化—万历", "faction": u"无", "tone": u"严肃", "firsthand_witness": u"文献转引", "confidence": "high"},
    {"opn_id": "OPN-33-003", "item_id": "33-005", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"讽刺", "target": u"汪道昆怕妇与戚继光相伯仲",
     "content": u"引汪道昆志戚继光墓述其为妻所困，而汪之长君为其妇所阉，蝙蝠笑梁上燕，自蹈其讥。",
     "source_text": u"蝙蝠不自见，笑他梁上燕。自古然矣",
     "reign": u"嘉靖—万历", "faction": u"无", "tone": u"嘲讽", "firsthand_witness": u"传闻", "confidence": "high"},
    {"opn_id": "OPN-33-004", "item_id": "33-007", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"感慨", "target": u"朱先功高没没无闻",
     "content": u"评故乡盐贩出身的朱先：廉勇善战终为福建大帅而四壁萧然，有古人风，竟没没无闻，深以为惜。",
     "source_text": u"朱先为将军，有古人风，似不在诸弁下，竟没没无闻，惜哉",
     "reign": u"嘉靖—万历", "faction": u"无", "tone": u"惋惜", "firsthand_witness": u"亲历", "confidence": "high"},
    {"opn_id": "OPN-33-005", "item_id": "33-008", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"褒扬", "target": u"徐渭书生胆决",
     "content": u"记胡宗宪军士饮酒不偿一案，徐文长建议剖腹验鲊，军中股栗，赞其书生而有胆决。",
     "source_text": u"徐以书生而有胆决乃尔",
     "reign": u"嘉靖", "faction": u"无", "tone": u"客观", "firsthand_witness": u"传闻", "confidence": "high"},
    {"opn_id": "OPN-33-006", "item_id": "33-009", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"贬斥", "target": u"健儿滥服一二品狮补",
     "content": u"评武弁绣胸不循品级概服狮子，至健儿荷刀戟者亦以为常服，一二品采章辱亵至此。",
     "source_text": u"孰知一二品采章，辱亵至此",
     "reign": u"景泰—万历", "faction": u"无", "tone": u"愤慨", "firsthand_witness": u"传闻", "confidence": "high"},
    {"opn_id": "OPN-33-007", "item_id": "33-010", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"褒扬", "target": u"隆庆二年武职比试三等之法",
     "content": u"检得隆庆二年兵部申明应袭舍人比试韬钤弓马三等之法，评其于武弁考核最严亦最恕，久而不废此辈必思自奋。",
     "source_text": u"此法于武弁考核最严，亦最恕，久而不废，此辈必思自奋",
     "reign": u"隆庆", "faction": u"无", "tone": u"客观", "firsthand_witness": u"文献转引", "confidence": "high"},
    {"opn_id": "OPN-33-008", "item_id": "33-013", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"讽刺", "target": u"长解卖放逃逸之弊",
     "content": u"记丁大伯解军中途纵犯自归故事，评近来长解自充军犯雇人代役，向来的遇逃叛必告官追捕，自蹈重典者比比，抑可拙也。",
     "source_text": u"自蹈重典者比比，抑可拙也",
     "reign": u"万历", "faction": u"无", "tone": u"嘲讽", "firsthand_witness": u"亲历", "confidence": "high"},
    {"opn_id": "OPN-33-009", "item_id": "33-014", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"讽刺", "target": u"张鼎思改供称冤",
     "content": u"评乐新炉案中张鼎思上疏自白而招词改入其名，吴吻儇薄遂嘲为张换狗。",
     "source_text": u"而吴吻儇薄，遂嘲为“张换狗”",
     "reign": u"万历", "faction": u"无", "tone": u"嘲讽", "firsthand_witness": u"传闻", "confidence": "medium"},
    {"opn_id": "OPN-33-010", "item_id": "33-015", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"中立评述", "target": u"吕张闺范案聚讼",
     "content": u"评戊戌谤书案吕坤张位两家聚讼，谓刻书成心与否预闻与否鬼神察之，两党之争如妇女勃溪俱不足凭。",
     "source_text": u"两家聚讼，正如妇女勃溪，俱不足凭也",
     "reign": u"万历", "faction": u"无", "tone": u"嘲讽", "firsthand_witness": u"传闻", "confidence": "high"},
    {"opn_id": "OPN-33-011", "item_id": "33-018", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"感慨", "target": u"癸卯妖书造撰之人",
     "content": u"评癸卯妖书狱成仅捕俶生光塞责完局，至于造撰之人终莫能明。",
     "source_text": u"至于造撰之人，终莫能明也",
     "reign": u"万历", "faction": u"无", "tone": u"严肃", "firsthand_witness": u"传闻", "confidence": "high"},
    {"opn_id": "OPN-33-012", "item_id": "33-020", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"劝诫", "target": u"奴婢弑逆之变",
     "content": u"记董幼海为群仆脔割、潘文锡为婢奴所杀诸事，评淫虐得祸如此而潘事更奇，俱在三吴可戒可戒。",
     "source_text": u"盖淫虐之得祸如此，而潘事则更奇矣",
     "reign": u"万历", "faction": u"无", "tone": u"严肃", "firsthand_witness": u"传闻", "confidence": "high"},
    {"opn_id": "OPN-33-013", "item_id": "33-021", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"贬斥", "target": u"弹章诬及家门之习",
     "content": u"评李植劾潘季驯并及其父兄，自是而后弹章所指诬及家门蔓延闺阁，其秽令人掩耳。",
     "source_text": u"弹章所指，诬及家门，蔓延闺阁，其秽令人掩耳矣",
     "reign": u"万历", "faction": u"无", "tone": u"愤慨", "firsthand_witness": u"传闻", "confidence": "high"},
    {"opn_id": "OPN-33-014", "item_id": "33-022", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"褒扬", "target": u"宋淳化赌博处斩之法",
     "content": u"评宋太宗坊市赌博处斩之令为至善，人情畏死自然衰止；又引洪武圣旨主张今赌搏者解腕。",
     "source_text": u"此法至善，盖人情畏死，自然衰止",
     "reign": u"宋—明", "faction": u"无", "tone": u"客观", "firsthand_witness": u"文献转引", "confidence": "high"},
    {"opn_id": "OPN-33-015", "item_id": "33-023", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"贬斥", "target": u"天顺刑赏倒置",
     "content": u"记夏瑄杀多人得复职而御史何楚英杖厨役至荷三木三月，评曹石擅权专右武人以至台臣僇辱至此。",
     "source_text": u"盖是时曹石擅权，专右武人，以至台臣僇辱至此",
     "reign": u"天顺", "faction": u"无", "tone": u"愤慨", "firsthand_witness": u"文献转引", "confidence": "high"},
    {"opn_id": "OPN-33-016", "item_id": "33-024", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"中立评述", "target": u"台省相讦之风",
     "content": u"历数嘉靖末至万历台臣赃败诸案与国初台臣相讦之事，评近日有台不攻台之说虽非国体亦近于厚。",
     "source_text": u"近日有台不攻台之说，虽非国体，亦近于厚",
     "reign": u"永乐—万历", "faction": u"无", "tone": u"客观", "firsthand_witness": u"亲闻", "confidence": "high"},
    {"opn_id": "OPN-33-017", "item_id": "33-025", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"贬斥", "target": u"桂萼倡互纠颠倒内计",
     "content": u"评嘉靖六年科道互纠一案桂萼妄引宪宗成化弘治例以报私怨，内计大典颠倒披猖，书之史册令人戟手追詈权奸。",
     "source_text": u"内计大典，似此颠倒披猖，书之史册，令人戟手追詈权奸",
     "reign": u"嘉靖", "faction": u"无", "tone": u"愤慨", "firsthand_witness": u"文献转引", "confidence": "high"},
    {"opn_id": "OPN-33-018", "item_id": "33-026", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"贬斥", "target": u"以姓名穿凿陷人之科臣",
     "content": u"评齐世臣陈陈相因徐申去嫌名附同姓及癸卯妖书以朱为国姓赓者更也，穿凿矫诬惑乱远近其罪殊死固宜。",
     "source_text": u"穿凿矫诬，惑乱远近，其罪殊死固宜",
     "reign": u"万历", "faction": u"无", "tone": u"愤慨", "firsthand_witness": u"传闻", "confidence": "high"},
    {"opn_id": "OPN-33-019", "item_id": "33-029", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"中立评述", "target": u"林聪夺情前后矛盾",
     "content": u"评林聪先奏京官听终制不必夺情，后天顺三年自己以忧归一辞不允即赴任，完璧之瑕云。",
     "source_text": u"此事亦完璧之瑕云",
     "reign": u"景泰—天顺", "faction": u"无", "tone": u"惋惜", "firsthand_witness": u"文献转引", "confidence": "high"},
    {"opn_id": "OPN-33-020", "item_id": "33-032", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"贬斥", "target": u"柰亨蒙宥恩宠之滥",
     "content": u"评光禄寺卿柰亨借供祀盗猪鹅肉仅见宥，后以户侍郎充读卷官荫子中书舍人，亨之厚颜不足责而恩宠之滥亦甚。",
     "source_text": u"亨之厚颜不足责，而恩宠之滥亦甚矣",
     "reign": u"正统", "faction": u"无", "tone": u"愤慨", "firsthand_witness": u"文献转引", "confidence": "high"},
    {"opn_id": "OPN-33-021", "item_id": "33-033", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"感慨", "target": u"本朝算学不讲",
     "content": u"记宋崇宁立算学绘像从祀封五等之爵之制，叹今日钦天监世学诸生无能通九章周髀者，宋人识见固非今世所及。",
     "source_text": u"宋人识见，固非今世所及",
     "reign": u"宋—万历", "faction": u"无", "tone": u"惋惜", "firsthand_witness": u"文献转引", "confidence": "high"},
    {"opn_id": "OPN-33-022", "item_id": "33-034", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"贬斥", "target": u"亵慢太极侮圣之俗",
     "content": u"记吴康斋作圈势受以芦菔之嘲、显官以冲破太极治隶人、朱隆禧献太极衣、缅铃称太极丸诸事，侮圣至此可痛可恨。",
     "source_text": u"侮圣至此，可痛可恨",
     "reign": u"嘉靖—万历", "faction": u"无", "tone": u"愤慨", "firsthand_witness": u"传闻", "confidence": "high"},
    {"opn_id": "OPN-33-023", "item_id": "33-037", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"贬斥", "target": u"嘉靖阿谄献谀士风",
     "content": u"评大礼议后汪鋐独主迁显陵、魏庄渠进种子秘方、高南宇撰玄文叩坛，奈何阿谄成风即一时号为正人亦献谀希宠。",
     "source_text": u"奈何阿谄成风，即一时号为正人，亦献谀希宠",
     "reign": u"嘉靖", "faction": u"无", "tone": u"愤慨", "firsthand_witness": u"文献转引", "confidence": "high"},
    {"opn_id": "OPN-33-024", "item_id": "33-039", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"褒扬", "target": u"周忱委曲结王振",
     "content": u"记周文襄规度王振新第广狭织绒地衣以馈得便宜展布，籍没时金观音背镂孝孙周忱进，评盖委曲以从事亦豪杰作用。",
     "source_text": u"盖委曲以从事，亦豪杰作用",
     "reign": u"正统—景泰", "faction": u"无", "tone": u"客观", "firsthand_witness": u"文献转引", "confidence": "high"},
    {"opn_id": "OPN-33-025", "item_id": "33-042", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"感慨", "target": u"吴鹏父子势极祸发",
     "content": u"述先人往候病中的吴鹏，闻其以久雨为乡村图赖租债之地，大骇谓身一品富一郡何出此语，未几祸发逾年谢世。",
     "source_text": u"先人大骇，谓身一品，富一郡，何出此语",
     "reign": u"嘉靖—隆庆", "faction": u"无", "tone": u"严肃", "firsthand_witness": u"亲闻", "confidence": "high"},
    {"opn_id": "OPN-33-026", "item_id": "33-044", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"贬斥", "target": u"沈祖量词气卑靡",
     "content": u"评友人沈祖量赠妓词末句任他百般打骂百般羞，柔情亦吾辈佳事何至卑下委媟乃尔，才名虽著风云气短。",
     "source_text": u"此君虽有才名，其如风云气短何",
     "reign": u"万历", "faction": u"无", "tone": u"惋惜", "firsthand_witness": u"亲历", "confidence": "high"},
    {"opn_id": "OPN-33-027", "item_id": "33-047", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"感慨", "target": u"辇下灯市盛衰",
     "content": u"记永乐七年宣德二年元夕放灯永为定例，一百九十九年四海承平辇下繁富，儿时目睹繁华至今入梦，闻近年亦稍稍减旧观。",
     "source_text": u"余儿时目睹繁华，至今入梦",
     "reign": u"永乐—万历", "faction": u"无", "tone": u"惋惜", "firsthand_witness": u"亲历", "confidence": "high"},
    {"opn_id": "OPN-33-028", "item_id": "33-048", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"感慨", "target": u"内府鸟兽之畜靡费",
     "content": u"记张升奏西苑豹房一豹役勇士二百四十名岁廪二千八百石，余近得游苑中见虎豹之槛不可枚举，举一豹而他物可知矣。",
     "source_text": u"举一豹而他物可知矣",
     "reign": u"嘉靖—万历", "faction": u"无", "tone": u"严肃", "firsthand_witness": u"亲历", "confidence": "high"},
    {"opn_id": "OPN-33-029", "item_id": "33-052", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"讽刺", "target": u"门宫公然犯庙讳御名",
     "content": u"评厚载门犯世宗穆宗庙讳上一字、翊坤宫犯今上御名而银榜高悬章疏直呼无一人议及，此等事俱不可解。",
     "source_text": u"此等事俱不可解",
     "reign": u"万历", "faction": u"无", "tone": u"嘲讽", "firsthand_witness": u"亲历", "confidence": "high"},
    {"opn_id": "OPN-33-030", "item_id": "33-054", "author": E[u"沈德符"], "author_text": u"沈德符",
     "opinion_type": u"贬斥", "target": u"闽俗契兄弟之忍",
     "content": u"评南宋王僧达欲逼留族子确设坑杀之事，男色之嗜至不避族属尊卑且行凶忍如此，亦闽俗之祖。",
     "source_text": u"男色之嗜，至不避族属尊卑，且行凶忍如此",
     "reign": u"嘉靖—万历", "faction": u"无", "tone": u"愤慨", "firsthand_witness": u"传闻", "confidence": "high"},
]

# ---------------------------------------------------------------------------
# L8 明代纪事层 MING-33-NNN
# ---------------------------------------------------------------------------
MINGS = [
    {"ming_id": "MING-33-001", "item_id": "33-001", "person": E[u"阎禹锡"], "person_text": u"阎禹锡",
     "event": u"成化四年以国子监丞言古者学必有庙，请改武学余楹为武成庙，上许之",
     "reign": u"成化", "date": u"成化四年",
     "source_text": u"成化四年，用国子监丞阎禹锡言，古者学必有庙，乞将武学余楹改为庙", "confidence": "high"},
    {"ming_id": "MING-33-002", "item_id": "33-002", "person": E[u"杨照"], "person_text": u"杨照",
     "event": u"嘉靖末起为辽东总兵，涅尽忠报国四字于背，战殁后贫母月给米三石",
     "reign": u"嘉靖", "date": u"嘉靖末年",
     "source_text": u"照感上知遇，涅“尽忠报国”四字于背", "confidence": "high"},
    {"ming_id": "MING-33-003", "item_id": "33-003", "person": E[u"汪直"], "person_text": u"汪直",
     "event": u"成化十四年擅权右武，上疏请武举设科用乡会殿试悉如进士恩例",
     "reign": u"成化", "date": u"成化十四年",
     "source_text": u"成化十四年，宦官汪直擅权，方务边功，右武人，乃上疏请武举设科", "confidence": "high"},
    {"ming_id": "MING-33-004", "item_id": "33-004", "person": E[u"石亨"], "person_text": u"石亨",
     "event": u"景泰中以总兵请征也先，议军士四胜五胜刺赤心报国于臂，景帝不许",
     "reign": u"景泰", "date": u"景泰中",
     "source_text": u"武清侯石亨为总兵，请征剿也先", "confidence": "high"},
    {"ming_id": "MING-33-005", "item_id": "33-005", "person": E[u"戚元敬"], "person_text": u"戚元敬",
     "event": u"汪道昆志其墓述为妻所困几至绝祀，其惧内与汪相伯仲",
     "reign": u"万历", "date": u"戚殁之后",
     "source_text": u"然汪之怕妇，亦与戚相伯仲", "confidence": "high"},
    {"ming_id": "MING-33-006", "item_id": "33-006", "person": E[u"李暠"], "person_text": u"李暠",
     "event": u"正统十三年以大宁都指挥佥事道遇祁州知州李玉不避道杖之，为巡按御史段信所劾",
     "reign": u"正统", "date": u"正统十三年",
     "source_text": u"大宁都指挥佥事李暠，道遇祁州知州李玉不避道，杖之", "confidence": "high"},
    {"ming_id": "MING-33-007", "item_id": "33-007", "person": E[u"刘显"], "person_text": u"刘显",
     "event": u"嘉靖癸亥倭据兴化，显御军全无纪律，掠夺逃出妇人，又纳王凤台继妻",
     "reign": u"嘉靖", "date": u"嘉靖癸亥",
     "source_text": u"兴化城逃出妇人，显军即掠夺之", "confidence": "high"},
    {"ming_id": "MING-33-008", "item_id": "33-007", "person": E[u"朱先"], "person_text": u"朱先",
     "event": u"贩盐拒捕应募为前锋，一日馘倭十三人，胡宗宪便宜拜守备，终为福建大帅",
     "reign": u"嘉靖", "date": u"嘉靖癸亥后",
     "source_text": u"一日馘倭十三人，胡襄愍为督府，即以便宜拜守备", "confidence": "high"},
    {"ming_id": "MING-33-009", "item_id": "33-009", "person": E[u"毕旺"], "person_text": u"毕旺",
     "event": u"景泰四年以锦衣指挥同知疏援永乐旧例，环卫近臣概许麟服，武弁僭服之始",
     "reign": u"景泰", "date": u"景泰四年",
     "source_text": u"事在景泰四年：锦衣指挥同知毕旺，疏援永乐旧例", "confidence": "high"},
    {"ming_id": "MING-33-010", "item_id": "33-011", "person": E[u"李如松"], "person_text": u"李如松",
     "event": u"万历癸巳平壤大捷后不欲他兵分功，潜率家丁二千夜至碧蹄馆遇伏，家丁李友升战殁",
     "reign": u"万历", "date": u"万历癸巳",
     "source_text": u"李如松以平殄在迩，不欲他兵分其功，潜率家丁二千人夜至碧蹄馆", "confidence": "high"},
    {"ming_id": "MING-33-011", "item_id": "33-012", "person": E[u"庐祥"], "person_text": u"庐祥",
     "event": u"成化初巡抚延绥，建议选延安庆阳民兵壮者编什伍为土兵五千人，祥去法废",
     "reign": u"成化", "date": u"成化初年",
     "source_text": u"巡抚延绥都御史庐祥建议，以营伍兵少", "confidence": "high"},
    {"ming_id": "MING-33-012", "item_id": "33-015", "person": E[u"戴士衡"], "person_text": u"戴士衡",
     "event": u"万历戊戌以吏科给事中首发闺范之案，参吕坤包藏祸心有敬宗林甫之谋",
     "reign": u"万历", "date": u"万历戊戌",
     "source_text": u"吏科给事中戴士衡首发大难，参吕包藏祸心", "confidence": "high"},
    {"ming_id": "MING-33-013", "item_id": "33-015", "person": E[u"樊玉衡"], "person_text": u"樊玉衡",
     "event": u"继戴士衡之后，以前御史今全椒知县疏攻吕坤，举朝骇愕",
     "reign": u"万历", "date": u"万历戊戌",
     "source_text": u"前任御史今全椒知县樊玉衡者继之，举朝骇愕", "confidence": "high"},
    {"ming_id": "MING-33-014", "item_id": "33-015", "person": E[u"吕新吾"], "person_text": u"吕新吾",
     "event": u"司寇刻《闺范》一书行京师，皇贵妃重刻为序，遂启戊戌癸卯两案聚讼",
     "reign": u"万历", "date": u"万历戊戌前后",
     "source_text": u"吕新吾司寇，初刻《闺范》一书，行京师未久", "confidence": "high"},
    {"ming_id": "MING-33-015", "item_id": "33-019", "person": E[u"陈矩"], "person_text": u"陈矩",
     "event": u"万历三十一年十一月十二日以提督东厂太监奏称访得《国本攸关》妖书封进圣览",
     "reign": u"万历", "date": u"万历三十一年十一月十二日",
     "source_text": u"提督东厂太监陈矩奏称", "confidence": "high"},
    {"ming_id": "MING-33-016", "item_id": "33-023", "person": E[u"夏瑄"], "person_text": u"夏瑄",
     "event": u"天顺二年常德卫指挥使杀寄居妻子三人论死，其子虎上疏愿代父刑，瑄竟得复职",
     "reign": u"天顺", "date": u"天顺二年九月",
     "source_text": u"瑄子虎上疏，原代父刑", "confidence": "high"},
    {"ming_id": "MING-33-017", "item_id": "33-024", "person": E[u"黄廷聘"], "person_text": u"黄廷聘",
     "event": u"嘉靖四十四年巡按御史回籍过衡山不礼知县，发箧得金银诸物，冠带闲住",
     "reign": u"嘉靖", "date": u"嘉靖四十四年",
     "source_text": u"巡按御史浙江黄廷聘回籍，过衡山县，不礼知县陈安志", "confidence": "high"},
    {"ming_id": "MING-33-018", "item_id": "33-024", "person": E[u"钱一本"], "person_text": u"钱一本",
     "event": u"万历辛卯以原任庐陵知县新任试御史追论丁忧巡按祝大舟临行票取多赃",
     "reign": u"万历", "date": u"万历辛卯",
     "source_text": u"原任江西庐陵知县新任试御史钱一本，追论巡按江西丁忧御史祝大舟", "confidence": "high"},
    {"ming_id": "MING-33-019", "item_id": "33-025", "person": E[u"桂萼"], "person_text": u"桂萼",
     "event": u"嘉靖六年大计为南科道所纠，疏请科道互相纠察，妄引宪宗初年例以报私怨",
     "reign": u"嘉靖", "date": u"嘉靖六年丁亥",
     "source_text": u"引宪宗初年例，于拾遗后，互相纠察", "confidence": "high"},
    {"ming_id": "MING-33-020", "item_id": "33-026", "person": E[u"齐世臣"], "person_text": u"齐世臣",
     "event": u"科臣初保张居正再保大峪山，被串名目为齐人齐保山，开以姓名嘲讦之渐",
     "reign": u"万历", "date": u"万历间",
     "source_text": u"则目之为齐人齐保山", "confidence": "high"},
    {"ming_id": "MING-33-021", "item_id": "33-029", "person": E[u"林聪"], "person_text": u"林聪",
     "event": u"先奏京官听终制不必夺情，天顺三年己以右副都御史忧归，一辞不允即赴任",
     "reign": u"天顺", "date": u"天顺三年",
     "source_text": u"至天顺三年，则林聪已为右副都御史，以忧归里", "confidence": "high"},
    {"ming_id": "MING-33-022", "item_id": "33-030", "person": E[u"刘文泰"], "person_text": u"刘文泰",
     "event": u"庸医误药促两朝圣寿，荐纂《本草》实懵然请用翰林校正，交结中官张瑜竟免死",
     "reign": u"弘治", "date": u"弘治十六年—正德",
     "source_text": u"而文泰等于《本草》实懵然，乃请用翰林官任校正", "confidence": "high"},
    {"ming_id": "MING-33-023", "item_id": "33-031", "person": E[u"马从谦"], "person_text": u"马从谦",
     "event": u"嘉靖间光禄少卿劾提督太监杜泰干没内帑，被诬诽谤诏杖八十毙杖下",
     "reign": u"嘉靖", "date": u"嘉靖间",
     "source_text": u"诏杖八十，即毙杖下", "confidence": "high"},
    {"ming_id": "MING-33-024", "item_id": "33-032", "person": E[u"柰亨"], "person_text": u"柰亨",
     "event": u"正统六年光禄寺卿借供祀盗猪鹅肉，上仅姑宥之，后两充廷试读卷官又荫子",
     "reign": u"正统", "date": u"正统六年",
     "source_text": u"贪饕如此，论法难容，姑宥之", "confidence": "high"},
    {"ming_id": "MING-33-025", "item_id": "33-034", "person": E[u"朱隆禧"], "person_text": u"朱隆禧",
     "event": u"嘉靖世宗朝罢任府丞作太极衣以献，实房中术，上大喜进卿进侍郎",
     "reign": u"嘉靖", "date": u"嘉靖间",
     "source_text": u"作太极衣以献，盖房中术也", "confidence": "high"},
    {"ming_id": "MING-33-026", "item_id": "33-035", "person": E[u"刘睿"], "person_text": u"刘睿",
     "event": u"吏科都给事中路遇王振跪道旁，振大喜升户部左侍郎，后升尚书致仕",
     "reign": u"正统", "date": u"正统间",
     "source_text": u"路遇王振，跪于道旁，振大喜，升为户部左侍郎", "confidence": "high"},
    {"ming_id": "MING-33-027", "item_id": "33-035", "person": E[u"李燧"], "person_text": u"李燧",
     "event": u"致仕后敝衣破冠束玉带跪迎张永于路乞怜，召复故官再长冬曹",
     "reign": u"正德", "date": u"正德间",
     "source_text": u"燧敝衣破冠，而束上所赐玉带，跪迎于路", "confidence": "high"},
    {"ming_id": "MING-33-028", "item_id": "33-037", "person": E[u"汪鋐"], "person_text": u"汪鋐",
     "event": u"大礼议中士君子无一人以为可，惟汪鋐独主奉迁显陵之说",
     "reign": u"嘉靖", "date": u"嘉靖间",
     "source_text": u"惟汪鋐独主迁移一说", "confidence": "high"},
    {"ming_id": "MING-33-029", "item_id": "33-038", "person": E[u"吴山"], "person_text": u"吴山",
     "event": u"嘉靖间礼部尚书条对芝草逢迎，至辛酉正旦以日食不当免救、上欲称贺不从罢归",
     "reign": u"嘉靖", "date": u"嘉靖辛酉",
     "source_text": u"值辛酉年正旦，以日食不及分数当免救", "confidence": "high"},
    {"ming_id": "MING-33-030", "item_id": "33-039", "person": E[u"周文襄"], "person_text": u"周文襄",
     "event": u"抚江南密令人规度王振新第广狭，命松江府织绒地衣以馈，得便宜展布",
     "reign": u"正统", "date": u"正统间",
     "source_text": u"文襄密令人规度其厅事内室，广狭长短，命松江府织绒地衣以馈", "confidence": "high"},
]

# ---------------------------------------------------------------------------
# C9 论说层修正：firsthand_witness 枚举严格取自 FIRSTHAND（无「文献转引」项）
# ---------------------------------------------------------------------------
_FW_FIX = {u"\u6587\u732e\u8f6c\u5f15": u"\u4f20\u95fb"}
for _r in OPNS:
    _v = _r.get("firsthand_witness")
    if _v in _FW_FIX:
        _r["firsthand_witness"] = _FW_FIX[_v]

# ---------------------------------------------------------------------------
# C14 时间沿革层 YHB-TME-33-NNN（era 由 reign 取自 REIGN_ORDER，tme_id 顺序生成）
# ---------------------------------------------------------------------------
TMES_RAW = [
    {"item_id": "33-001", "date": u"洪武间", "reign": u"洪武", "category": u"废置",
     "event": u"礼部请如前代故事设武学、建武成庙，太祖谓是歧文武为二，但以太公从祀帝王庙，废武成庙并武学不设",
     "source_text": u"礼部请如前代故事，设武学，仍建武成庙，上谓是歧文武为二矣", "confidence": "high"},
    {"item_id": "33-001", "date": u"建文四年正月", "reign": u"建文", "category": u"初置",
     "event": u"始建京卫武学，并置教授等官，武学复立于本朝",
     "source_text": u"至建文四年正月，始建京卫武学，及教授等官", "confidence": "high"},
    {"item_id": "33-001", "date": u"景泰三年", "reign": u"景泰", "category": u"废置",
     "event": u"废武学", "source_text": u"景泰三年废武学", "confidence": "high"},
    {"item_id": "33-001", "date": u"天顺二年", "reign": u"天顺", "category": u"复设",
     "event": u"复设武学", "source_text": u"景泰三年废武学，天顺二年复设", "confidence": "high"},
    {"item_id": "33-001", "date": u"成化四年", "reign": u"成化", "category": u"改置",
     "event": u"用国子监丞阎禹锡言，乞将武学余楹改为庙，使知礼先勇后之义，上许之而太公不得祀犹故",
     "source_text": u"乞将武学余楹改为庙，使知礼先勇后之义", "confidence": "high"},
    {"item_id": "33-001", "date": u"嘉靖十五年四月", "reign": u"嘉靖", "category": u"移驻",
     "event": u"兵部议以武学太窄请拓其制，改建于大兴隆寺故址，会礼工二部议仿唐制立武成王庙",
     "source_text": u"兵部议以武学太窄，请拓其制，改建于大兴隆寺故址", "confidence": "high"},
    {"item_id": "33-001", "date": u"嘉靖间", "reign": u"嘉靖", "category": u"初置",
     "event": u"世宗诏修太医院三皇庙仍厘正祀典，正位伏羲神农黄帝，从祀十八人，遂成文武两庙并医王三大祀",
     "source_text": u"仍厘正祀典，正位以伏羲、神农、黄帝", "confidence": "high"},
    {"item_id": "33-003", "date": u"成化十四年", "reign": u"成化", "category": u"初置",
     "event": u"汪直请武举设科，廷臣条上选武臣嫡子就儒学、乡试九月会试三月三场试以策、四月初一殿试之大略",
     "source_text": u"选武臣嫡子就儒学读书习射，乡试以九月，会试以三月", "confidence": "high"},
    {"item_id": "33-003", "date": u"弘治中", "reign": u"弘治", "category": u"职掌变更",
     "event": u"武举之科至弘治中毕竟行之，特不殿试，恩例较进士为杀",
     "source_text": u"然至弘治中，毕竟行之，但不殿试耳", "confidence": "high"},
    {"item_id": "33-003", "date": u"嘉靖十九年", "reign": u"嘉靖", "category": u"废置",
     "event": u"兵部请武举乡试，上以累科未见得人命已之",
     "source_text": u"嘉靖十九年，兵部请武举乡试，上以累科未见得人，命已之", "confidence": "high"},
    {"item_id": "33-003", "date": u"嘉靖十九年后未久", "reign": u"嘉靖", "category": u"复设",
     "event": u"给事中王梦弼请六年一举不许，未久武举乡试复行之",
     "source_text": u"给事中王梦弼请六年一举，亦不许。未久复行之", "confidence": "medium"},
    {"item_id": "33-009", "date": u"景泰四年", "reign": u"景泰", "category": u"职掌变更",
     "event": u"锦衣指挥同知毕旺疏援永乐旧例，谓环卫近臣不比他官概许麟服，武弁服色自是逾品级",
     "source_text": u"后乃知事在景泰四年：锦衣指挥同知毕旺，疏援永乐旧例", "confidence": "high"},
    {"item_id": "33-010", "date": u"隆庆二年二月十四日", "reign": u"隆庆", "category": u"初置",
     "event": u"兵部题浙江巡抚赵都御史陈将材而申明之，应袭舍人送学充附，以韬钤弓马分三等，三次不中革发为军，奉旨依拟行",
     "source_text": u"偶检得隆庆二年二月十四日，兵部题浙江巡抚赵都御史陈将材一节而申明之", "confidence": "high"},
    {"item_id": "33-010", "date": u"隆庆二年后，年月不可考", "reign": u"万历", "category": u"废置",
     "event": u"武职比试三等考核之法久而不废此辈必思自奋，然竟不知废于何年，穆宗实录亦不载",
     "source_text": u"竟不知废于何年，而穆宗史亦不载何也", "confidence": "medium"},
    {"item_id": "33-012", "date": u"成化初年", "reign": u"成化", "category": u"初置",
     "event": u"巡抚延绥都御史卢祥建议选延安庆阳边民之壮者编成什伍为土兵，量免户租，得五千人训练之",
     "source_text": u"土兵之设，始于成化初年，巡抚延绥都御史庐祥建议", "confidence": "high"},
    {"item_id": "33-012", "date": u"卢祥去职后", "reign": u"成化", "category": u"废置",
     "event": u"土兵强盛时毛里孩入寇为之退却，祥去而此法遂废",
     "source_text": u"祥去而此法遂废", "confidence": "high"},
    {"item_id": "33-012", "date": u"正统己巳之变", "reign": u"正统", "category": u"初置",
     "event": u"内地民壮之设始于正统己巳之变，招募时器械鞍马官给，地方有司春秋训练遇警调用，然非祖制",
     "source_text": u"今内地所谓民壮者，始于正统己巳之变，亦非祖制", "confidence": "high"},
    {"item_id": "33-012", "date": u"弘治二年", "reign": u"弘治", "category": u"复设",
     "event": u"复命编佥民壮，此后照例编佥，徒供迎送之用",
     "source_text": u"弘治二年，复命行之，此后照例编佥，徒供迎送之用", "confidence": "high"},
    {"item_id": "33-022", "date": u"正统间", "reign": u"正统", "category": u"改置",
     "event": u"大兴知县马通建白治赌博之法，法司覆议定犯者运粮口外",
     "source_text": u"正统间，大兴知县马通建白治赌博之法，法司覆议，已定犯者运粮口外矣", "confidence": "high"},
    {"item_id": "33-022", "date": u"万历时（作者自称「今」）", "reign": u"万历", "category": u"废置",
     "event": u"运粮口外之法格不行，赌博仅从初制拟杖，加重者不过枷示",
     "source_text": u"今此法何以格不行，仅从初制拟杖，即加重者不过枷示", "confidence": "high"},
    {"item_id": "33-033", "date": u"万历时", "reign": u"万历", "category": u"未明",
     "event": u"宋崇宁三年特立算学、大观中命算学如庠序之制，本朝算学不设，钦天监世学诸生无能通九章周髀者",
     "source_text": u"今日钦天监世学诸生，有能通《九章周髀》者乎", "confidence": "medium"},
    {"item_id": "33-047", "date": u"永乐七年正月十一日", "reign": u"永乐", "category": u"初置",
     "event": u"太宗圣旨：上元节正月十一日至二十日官人每与节假不奏事，民间放灯从他饮酒作乐，兵马司都不禁，永为定例",
     "source_text": u"今年上元节正月十一日至二十日，这几日官人每都与节假", "confidence": "high"},
    {"item_id": "33-047", "date": u"宣德二年正月十二日", "reign": u"宣德", "category": u"职掌变更",
     "event": u"宣宗敕谕：特赐百官假十日，在京军民如故事张灯饮酒为乐，五城兵马弛夜禁，永为定例",
     "source_text": u"特赐百官假十日，凡有机务重事，封进来闻", "confidence": "high"},
    {"item_id": "33-047", "date": u"宣德四年正月朔（五年、八年亦然）", "reign": u"宣德", "category": u"增员",
     "event": u"特赐文武节假二十日，元宵夜召群臣悉赴御苑观灯，属特恩非常例",
     "source_text": u"宣德四年正月朔，特赐文武节假二十日，元宵夜，召群臣悉赴御苑观灯", "confidence": "high"},
    {"item_id": "33-047", "date": u"每岁年终（沿永乐七年例）", "reign": u"万历", "category": u"职掌变更",
     "event": u"永乐七年、宣德二年二例载在令甲，每至年终礼部上疏援引前例请旨，许来年新正民间放灯凡十昼夜，至万历三十五年恰一百九十九年",
     "source_text": u"以上二例，皆载在令甲，每至年终，礼部上疏援引前例请旨", "confidence": "high"},
    {"item_id": "33-048", "date": u"嘉靖初年", "reign": u"嘉靖", "category": u"废置",
     "event": u"世宗初年革内府鹰房诸鹰犬，令放纵几尽",
     "source_text": u"世宗初年，革内府鹰房诸鹰犬，令放纵几尽矣", "confidence": "high"},
    {"item_id": "33-048", "date": u"嘉靖八年", "reign": u"嘉靖", "category": u"废置",
     "event": u"鹰房内臣以祖庙献新奏请存留，上严旨不许，礼部言非会典之例请一切罢之，遂依会典罢去",
     "source_text": u"上纳其言，遂依《会典》罢去", "confidence": "high"},
    {"item_id": "33-048", "date": u"嘉靖十年", "reign": u"嘉靖", "category": u"裁并",
     "event": u"兵部覆勇士张升奏，西苑豹房畜土豹一只役勇士二百四十名，请量留四十人余还营差操，仍令该监核其奸利",
     "source_text": u"请量留勇士四十人，余还营差操，仍令该监核其奸利以报", "confidence": "high"},
    {"item_id": "33-049", "date": u"洪武二十七年", "reign": u"洪武", "category": u"初置",
     "event": u"太祖以海内太平思与民偕乐，命工部建十酒楼于江东门外，有鹤鸣、醉仙、讴歌、鼓腹、来宾、重译等名",
     "source_text": u"命工部建十酒楼于江东门外，有鹤鸣、醉仙、讴歌、鼓腹、来宾、重译等名", "confidence": "high"},
    {"item_id": "33-049", "date": u"洪武二十七年继增", "reign": u"洪武", "category": u"增员",
     "event": u"既而又增作五楼至是皆成，五楼专以处侑酒歌妓，仿宋世故事但不设官酝收榷课",
     "source_text": u"既而又增作五楼，至是皆成", "confidence": "high"},
    {"item_id": "33-050", "date": u"宣德中", "reign": u"宣德", "category": u"废置",
     "event": u"以百僚日醉狭邪不修职业，左都御史顾佐奏禁歌妓，廷臣有犯者至褫职，迄今不改",
     "source_text": u"至宣德中，以百僚日醉狭邪，不修职业，为左都御史顾佐奏禁，廷臣有犯者至褫职", "confidence": "high"},
    {"item_id": "33-051", "date": u"永乐十五年", "reign": u"永乐", "category": u"初置",
     "event": u"禁城北安门外建安乐堂，本以处工匠之疾病者",
     "source_text": u"有安乐堂，为永乐十五年所建，以处工匠之疾病者", "confidence": "high"},
    {"item_id": "33-051", "date": u"万历时（作者自称「近来」）", "reign": u"万历", "category": u"职掌变更",
     "event": u"安乐堂与工匠无涉，惟内臣卑秩无私宅无名下官可依者遇疾且殆徙入待殒，槥送净乐堂焚化",
     "source_text": u"近来则与工匠无涉，惟内臣卑秩无私宅可住，无名下官可依者，遇疾且殆，即徙入此中", "confidence": "high"},
]

# ---------------------------------------------------------------------------
# REG 制度层 REG-33-NNN（reg_id 顺序生成）
# ---------------------------------------------------------------------------
REGS_RAW = [
    {"item_id": "33-001", "name": u"武成王庙祀典沿革", "type": u"礼制", "reign": u"嘉靖",
     "description": u"唐封太公为武成王立庙，宋置十哲七十二弟子从祀。洪武废武成庙并武学不设，建文始建京卫武学，景泰废、天顺复设，成化四年改武学余楹为庙。嘉靖十五年兵部请拓改制，改建于大兴隆寺故址，仿唐制立武成王庙，益以尉缭子、黄石公、李广、赵充国，宋增韩世忠、岳飞，本朝以徐达、常遇春、张玉、汤和配享，夏秋致祭、仲冬车驾幸讲武殿大阅，与文宣庙并峙。",
     "source_text": u"于是文武两庙并医王凡三大祀，鼎立于京师矣", "confidence": "high"},
    {"item_id": "33-001", "name": u"三皇庙医王从祀之典", "type": u"礼制", "reign": u"嘉靖",
     "description": u"世宗诏修太医院三皇庙厘正祀典：正位伏羲、神农、黄帝，配位勾芒、祝融、风后、力牧，从祀僦贷季天师至李杲、朱彦修十八人拟十哲之列，殿曰景惠、门曰咸济，牲用太牢、器用笾豆簠簋，以仲春仲冬上甲日遣大臣行礼，著为令。",
     "source_text": u"牲用太牢，器用笾豆簠簋，以仲春仲冬上甲日，遣大臣行礼，著为令", "confidence": "high"},
    {"item_id": "33-003", "name": u"武举设科取士之制", "type": u"科举", "reign": u"成化",
     "description": u"成化十四年汪直请武举设科用乡试会试殿试悉如进士恩例，廷臣条上：选武臣嫡子就儒学读书习射，乡试以九月、会试以三月，初场试射、二场试论、三场试策，四月初一殿试，赐第恩荣刻录立碑一如进士制；万安密奏内批缓之。弘治中行之但不殿试，嘉靖十九年尝命已之未久复行。",
     "source_text": u"选武臣嫡子就儒学读书习射，乡试以九月，会试以三月，初场试射，二场试论，三场试策", "confidence": "high"},
    {"item_id": "33-004", "name": u"军士刺字之禁", "type": u"军事", "reign": u"洪武",
     "description": u"本朝极重黔刺，太祖厉禁不许；景泰中石亨为总兵请以四胜五胜者左右臂各刺「赤心报国」四字，帝以刺字是刑罚加于无罪不近情，不许。宋健儿刺面防逃逸、八字军自刺其面，本朝则无刺臂之制。",
     "source_text": u"本朝极重黔刺，太祖厉禁不许", "confidence": "high"},
    {"item_id": "33-009", "name": u"武弁品级服色之制", "type": u"官制", "reign": u"景泰",
     "description": u"武弁绣胸当循钦定品级，然自锦衣至指挥佥事而上无不服麒麟，健儿荷刀戟者以狮子补为常服。其源在景泰四年锦衣指挥同知毕旺疏援永乐旧例，谓环卫近臣不比他官概许麟服，遂开僭越之渐。",
     "source_text": u"疏援永乐旧例，谓环卫近臣，不比他官，概许麟服", "confidence": "high"},
    {"item_id": "33-010", "name": u"武职袭替比试三等考第之法", "type": u"官制", "reign": u"隆庆",
     "description": u"隆庆二年兵部申明：应袭舍人年十五以上资质可造者送学充附作养，遇袭替年及二十应比试者学臣考韬钤策一道转送抚按覆阅，韬钤贯通弓马娴熟为上等候缺管事，中等带俸差操，下等支半俸候再考；二次不中照邦政例支半俸，三次不中革发为军别选子弟袭职，奉旨依拟行。",
     "source_text": u"韬钤贯通，弓马娴熟者为上等；韬钤疏而弓马熟者为次等；韬钤弓马俱不习为下等", "confidence": "high"},
    {"item_id": "33-011", "name": u"将帅蓄养家丁之制", "type": u"军事", "reign": u"万历",
     "description": u"家丁昉于唐季藩镇（田承嗣魏府牙兵、杨行密黑云都之属），今西北将帅所蓄家丁廪饩衣械过额兵十倍，每大敌用以陷阵，善战者多以首功自奋间至登坛，辽左李成梁、李如松专仗之以树勋，碧蹄馆之战潜率家丁二千人。",
     "source_text": u"今西北将帅所蓄家丁，其廪饩衣械，过额兵十倍", "confidence": "high"},
    {"item_id": "33-012", "name": u"土兵与民壮之制", "type": u"军事", "reign": u"成化",
     "description": u"土兵始于成化初年卢祥抚延绥，选延安庆阳边民之壮者编成什伍、量免户租，得五千人训练之，祥去遂废。内地民壮始于正统己巳之变，器械鞍马官给、有司春秋训练遇警调用，弘治二年复命行之，后照例编佥徒供迎送，非祖制也。",
     "source_text": u"宜选民兵之壮者，编成什伍为土兵，量免户租，凡得五千人训练之", "confidence": "high"},
    {"item_id": "33-013", "name": u"解军长解之制", "type": u"司法", "reign": u"万历",
     "description": u"解军一役以本图里长充长解，官司先为娶妻备赀装，事之如严父防之如大敌，犹虞中途逃逸相累；践更获遣者举家震怖，甚至有抵罪破家者。近年长解自充军犯、雇男女代投批到卫，戍长利其遗下口粮不敢声言，荷戈之人优游闾里。",
     "source_text": u"解军一役，以本图里长充长解，先为娶妻，备赀装，事之如严父，防之如大敌", "confidence": "high"},
    {"item_id": "33-022", "name": u"赌博厉禁之令", "type": u"司法", "reign": u"洪武",
     "description": u"洪武二十二年圣旨：学唱的割了舌头，下棋打双陆的断手，蹴圆者卸脚，犯者必如法施行；正统间马通建白定犯赌博者运粮口外。今此法格不行，仅从初制拟杖，加重者不过枷示，故赌博盛行浸成劫贼。宋淳化二年令坊市赌博者俱行处斩，邻比匿不闻者问罪。",
     "source_text": u"洪武二十二年圣旨：学唱的割了舌头，下棋打双陆的断手，蹴圆者卸脚", "confidence": "high"},
    {"item_id": "33-024", "name": u"台省纠赃相讦之例", "type": u"官制", "reign": u"万历",
     "description": u"巡方御史坐赃，或由知县发其箧、掌院左都御史举其状（张永明之于黄廷聘），或由同省垣纠西台（何起鸣之论陈志先），或同事宪臣相纠（庞尚鹏之劾孙以仁），或堂官参治台臣（辛自修之劾沈汝梁），旧属吏新台臣发同官秽状（钱一本之论祝大舟）。处分自万历朝较世宗朝加重，国初台臣相讦已如此。",
     "source_text": u"此以堂官参治台臣，正与张永明同", "confidence": "high"},
    {"item_id": "33-025", "name": u"科道互纠拾遗之制", "type": u"官制", "reign": u"嘉靖",
     "description": u"嘉靖六年丁亥大计，张璁、桂萼为南北科道所纠，萼疏引宪宗初年例谓拾遗后互相纠察，上以萼言为然命吏部勒科道互相纠拾；桂萼又引成化三年宪纲，吏部谓是弘治十七年事而宪宗无之，所引二例皆不然，考察之内反成报私怨之具。",
     "source_text": u"上以萼言为然，命吏部勒科道互相纠拾", "confidence": "high"},
    {"item_id": "33-029", "name": u"京官夺情终制之例", "type": u"礼制", "reign": u"景泰",
     "description": u"吏科都给事中林聪奏：凡京官非与机要者有父母丧，悉听终制不必夺情，已蒙俞允；景泰五年李秉彝上疏止左通政王复夺情，上不允其所引。天顺三年林聪本人为右副都御史以忧归里，奉旨行取即赴任，一辞不允，前所持论遂为完璧之瑕。",
     "source_text": u"凡京官非与机要者，有父母丧，悉听终制，不必夺情", "confidence": "high"},
    {"item_id": "33-032", "name": u"光禄寺堂官盗祀品之处分", "type": u"司法", "reign": u"正统",
     "description": u"正统六年光禄寺大官署丞张冕奏本寺卿柰亨借供祀盗取猪鹅肉面食为私用，上命对状，以堂官贪饕论法难容而姑宥之，后两充廷试读卷官又荫子中书舍人；万历十八年署丞茅一柱盗署中火腿为堂官所奏，命送刑部追原物问徒为民。两事略同而处分略异。",
     "source_text": u"尔为堂官，贪饕如此，论法难容，姑宥之", "confidence": "high"},
    {"item_id": "33-045", "name": u"命妇犯妒杀之处断", "type": u"司法", "reign": u"成化",
     "description": u"成化末年礼部致仕左侍郎杨宣妻王氏素妒悍杖杀侍婢十余人，东厂上其事，刑部拟赎如律、宣赎杖仍致仕，上以肆意残酷仍命杖五十使知所儆。弘治十一年泗州知州许弼妻孙氏妒妾自缢事觉，命杖八十离异；宣德六年御史傅敬妻殴妾致死，有司以曾受封为疑，上命罪之如律。",
     "source_text": u"王氏虽命妇，例应纳赎，但肆意残酷，仍命刑部杖之五十，使知所儆", "confidence": "high"},
    {"item_id": "33-047", "name": u"上元节假放灯永为定例", "type": u"礼制", "reign": u"永乐",
     "description": u"永乐七年正月十一日圣旨：上元节正月十一日至二十日官人每与节假不奏事，民间放灯听其饮酒作乐，兵马司不禁、夜巡勿扰，永为定例。宣德二年敕赐百官假十日、五城兵马弛夜禁。二例载在令甲，每岁年终礼部援引请旨，许民间放灯凡十昼夜，较宋初钱俶买宴增三日之外又展二日。",
     "source_text": u"民间放灯，从他饮酒作乐快活，兵马司都不禁，夜巡著不要搅扰生事，永为定例", "confidence": "high"},
    {"item_id": "33-048", "name": u"宗庙献新品味之制", "type": u"礼制", "reign": u"嘉靖",
     "description": u"宗庙献新及奉先殿岁荐品味，不过鹿、雁、兔、猪、鹅、鸭、鸡等物，载在《会典》、掌之太常；后因内畜鹰犬或间以奉荐，然非例也，嘉靖八年礼部请一切罢之，上纳其言遂依会典罢去。",
     "source_text": u"宗庙献新，及奉先殿岁荐品味，不过鹿、雁、兔、猪、鹅、鸭、鸡等物，载在《会典》，掌之太常", "confidence": "high"},
    {"item_id": "33-048", "name": u"内府鹰房豹房廪饩之费", "type": u"财政", "reign": u"嘉靖",
     "description": u"西苑豹房畜土豹一只，役勇士二百四十名，岁廪二千八百石，占地十顷，岁租七百金，其实皆典守内臣侵牟；嘉靖十年兵部议量留勇士四十人，余还营差操，仍令该监核其奸利以报。内廷鸟兽之畜所费不赀，举一豹而他物可知。",
     "source_text": u"至役勇士二百四十名，岁廪二千八百石，占地十顷，岁租七百金", "confidence": "high"},
    {"item_id": "33-049", "name": u"江东门外十五楼之设", "type": u"其他", "reign": u"洪武",
     "description": u"洪武二十七年命工部建十酒楼于江东门外（鹤鸣、醉仙、讴歌、鼓腹、来宾、重译等名），又增作五楼专处侑酒歌妓，盖仿宋世故事但不设官酝以收榷课。十楼尚有清江、石城、乐民、集贤四名，五楼云轻烟、淡粉、梅妍、柳翠而遗其一，今金陵人称十四楼而不知有十五。诏赐百官宴于醉仙楼，博士钱宰等亦赐宴新楼。",
     "source_text": u"盖仿宋世故事，但不设官酝，以收榷课，最为清朝佳事", "confidence": "high"},
    {"item_id": "33-050", "name": u"百僚禁游狭邪之令", "type": u"官制", "reign": u"宣德",
     "description": u"宣德中左都御史顾佐以百僚日醉狭邪不修职业奏禁歌妓，廷臣有犯者至褫职，迄今不改；好事者以为太平缺陷。作者谓唐宜春、教坊非士大夫所得游，宋官妓不过州郡应奉过客，与之狎者仍有厉禁，故顾佐一疏保全士人实多。",
     "source_text": u"为左都御史顾佐奏禁，廷臣有犯者至褫职，迄今不改", "confidence": "high"},
    {"item_id": "33-051", "name": u"安乐堂处内臣疾病之制", "type": u"宦官", "reign": u"永乐",
     "description": u"永乐十五年于禁城北安门外建安乐堂，本以处工匠之疾病者；近来惟内臣卑秩无私宅可住、无名下官可依者遇疾且殆即徙入以待其殒，槥送净乐堂焚化，不欲以遗骼污禁掖。宫人无位号名秩病故或谴责死者，其尸亦传达安乐堂转停尸房，易朱棺再送火葬。",
     "source_text": u"有安乐堂，为永乐十五年所建，以处工匠之疾病者", "confidence": "high"},
    {"item_id": "33-052", "name": u"庙讳御名通称不避之例", "type": u"礼制", "reign": u"万历",
     "description": u"禁城北门名厚载即玄武门，二字俱犯世宗、穆宗庙讳上一字，上下通称不避；皇贵妃郑氏所居宫名翊坤宫，上一字即今上御名，银榜高悬而内外所称、章疏所列俱公然直呼，恬不为怪，无一人议及。",
     "source_text": u"但二字俱犯世宗、穆宗庙讳上一字，上下通称不避", "confidence": "high"},
    {"item_id": "33-054", "name": u"闽人契兄弟契儿之俗", "type": u"其他", "reign": u"万历",
     "description": u"闽人酷重男色，各以其类相结，长者为契兄、少者为契弟，兄入弟家弟之父母抚爱之如婿，弟娶妻诸费取办于契兄；近有称契儿者，壮夫以多赀聚姿首韶秀者，以父自居列诸少年于子舍。闻其事肇于海寇（舟中禁妇人），酋豪遂称契父；嘉靖间广西上冻州土知州赵元恩呼母之私夫陆监生为契父，其尊称同而故大不侔。",
     "source_text": u"长者为契兄，少者为契弟", "confidence": "high"},
]

# ---------------------------------------------------------------------------
# 输出与自检
# ---------------------------------------------------------------------------
def _build_tmes():
    out = []
    for i, t in enumerate(TMES_RAW):
        r = {"tme_id": "YHB-TME-33-%03d" % (i + 1)}
        r["item_id"] = t["item_id"]
        r["date"] = t["date"]
        r["reign"] = t["reign"]
        r["era"] = REIGN_ORDER[t["reign"]]
        r["category"] = t["category"]
        r["event"] = t["event"]
        r["source_text"] = t["source_text"]
        r["confidence"] = t["confidence"]
        out.append(r)
    return out


def _build_regs():
    out = []
    for i, t in enumerate(REGS_RAW):
        out.append({
            "reg_id": "REG-33-%03d" % (i + 1),
            "item_id": t["item_id"],
            "name": t["name"],
            "type": t["type"],
            "description": t["description"],
            "reign": t["reign"],
            "source_text": t["source_text"],
            "confidence": t["confidence"],
        })
    return out


def _quote_ok(rec, field):
    """引文核验：source_text / source 须在所属条目原文中逐字出现。"""
    v = rec.get(field)
    if not isinstance(v, str):
        return True
    return v in ITEM_TEXTS.get(rec["item_id"], u"")


def _ensure_confidence(rec, field):
    """缺失 confidence 的记录按引文可核验程度补 default。"""
    if "confidence" not in rec:
        rec["confidence"] = "high" if _quote_ok(rec, field) else "medium"


def _derive_confidence_for_events():
    for r in EVENTS:
        _ensure_confidence(r, "source_text")
    for r in APPTS:
        _ensure_confidence(r, "source")


TMES = _build_tmes()
REGS = _build_regs()
_derive_confidence_for_events()

LAYER_SPECS = [
    ("ents", "ent_id", ENTS),
    ("rules", "rule_id", RULES),
    ("events", "event_id", EVENTS),
    ("appts", "appt_id", APPTS),
    ("rels", "rel_id", RELS),
    ("opns", "opn_id", OPNS),
    ("cits", "cit_id", CITS),
    ("mings", "ming_id", MINGS),
    ("tmes", "tme_id", TMES),
    ("regs", "reg_id", REGS),
]


def write_layers():
    for layer, idkey, data in LAYER_SPECS:
        d = os.path.join(LAYERS, layer)
        if not os.path.isdir(d):
            os.makedirs(d)
        p = os.path.join(d, "%s_33.json" % layer)
        txt = json.dumps(data, ensure_ascii=False, indent=2)
        with io.open(p, "w", encoding="utf-8") as f:
            f.write(txt + u"\n")
        print(u"wrote %s_33.json  %3d records" % (layer, len(data)))


def selfcheck():
    errs = []
    warns = []
    # 枚举域
    E_TYPE, E_ROLE, E_FAC, E_CONF = set(ENTITY_TYPES), set(ENTRY_ROLES), set(FACTIONS), set(CONFIDENCE)
    R_CAT, R_ST = set(RULE_TYPES), set(ACTUAL_PRACTICE)
    V_TYPE, V_SIG, V_SRC, V_VOH = set(EVENT_TYPES), set(EVENT_SIGNIFICANCE), set(SOURCE_TYPES), set(VS_OFFICIAL_HISTORY)
    A_ST, A_CV = set(APPT_STATUS), set(CONTROVERSY)
    L_REL, L_DIR, L_EV = set(RELATION_TYPES), set(DIRECTION), set(EVIDENCE_STRENGTH)
    C_CTX = set(CITATION_TYPES) | set(CITATION_PURPOSES)
    O_TYPE, O_TONE, O_FW = set(COMMENTARY_TYPES), set(TONES), set(FIRSTHAND)
    M_CAT, M_REIGN = set(MING_CATEGORIES), set(REIGN_FOCUS)
    T_CAT, G_TYPE = set(TME_CATEGORIES), set(REG_CATEGORIES)
    REIGNS = set(REIGN_ORDER) | {u"跨朝"}
    ALL_ITEMS = set(ITEM_TEXTS)
    ENT_IDS = set(r["ent_id"] for r in ENTS)
    ids = set()

    def chk(cond, msg):
        if not cond:
            errs.append(msg)

    for layer, idkey, data in LAYER_SPECS:
        seen = set()
        for r in data:
            rid = r.get(idkey)
            chk(isinstance(rid, str), u"%s: 缺 %s" % (layer, idkey))
            chk(rid not in seen, u"%s: 重复 ID %s" % (layer, rid))
            seen.add(rid)
            ids.add(rid)
            it = r.get("item_id")
            chk(it in ALL_ITEMS, u"%s %s: item_id 非法 %s" % (layer, rid, it))
            conf = r.get("confidence", "high")
            chk(conf in E_CONF, u"%s %s: confidence 越界 %s" % (layer, rid, conf))
            # 引文核验（不入 err，只作 warn，避免古籍异体字误伤）
            if layer == "rels":
                _qfields = ["evidence"]
            else:
                _qfields = ["source_text"] + (["source"] if layer == "appts" else [])
            for fld in _qfields:
                v = r.get(fld)
                if isinstance(v, str) and not v.startswith("ENT-") and not _quote_ok(r, fld):
                    warns.append(u"%s %s: %s 未在条目原文中逐字命中（%s）" % (layer, rid, fld, it))
            if layer == "ents":
                chk(r["type"] in E_TYPE, u"ents %s: type 越界 %s" % (rid, r["type"]))
                chk(r["faction"] in E_FAC, u"ents %s: faction 越界 %s" % (rid, r["faction"]))
                for x in r["role_in_entry"]:
                    chk(x in E_ROLE, u"ents %s: role 越界 %s" % (rid, x))
            elif layer == "rules":
                chk(r["category"] in R_CAT, u"rules %s: category 越界 %s" % (rid, r["category"]))
                chk(r["status"] in R_ST, u"rules %s: status 越界 %s" % (rid, r["status"]))
            elif layer == "events":
                chk(r["event_type"] in V_TYPE, u"events %s: event_type 越界" % rid)
                for k in ("event_significance", "source_type", "vs_official_history"):
                    if k in r:
                        pool = {"event_significance": V_SIG, "source_type": V_SRC, "vs_official_history": V_VOH}[k]
                        chk(r[k] in pool, u"events %s: %s 越界 %s" % (rid, k, r[k]))
            elif layer == "appts":
                chk(r["type"] in A_ST, u"appts %s: type 越界 %s" % (rid, r["type"]))
                if "controversy" in r:
                    chk(r["controversy"] in A_CV, u"appts %s: controversy 越界" % rid)
                chk(r["person"] in ENT_IDS, u"appts %s: person 悬空 %s" % (rid, r["person"]))
            elif layer == "rels":
                chk(r["relation"] in L_REL, u"rels %s: relation 越界 %s" % (rid, r["relation"]))
                chk(r["direction"] in L_DIR, u"rels %s: direction 越界 %s" % (rid, r["direction"]))
                chk(r["evidence_strength"] in L_EV, u"rels %s: evidence_strength 越界" % rid)
                for k in ("source", "target"):
                    chk(r[k] in ENT_IDS, u"rels %s: %s 悬空 %s" % (rid, k, r[k]))
            elif layer == "cits":
                chk(r["cite_context"] in C_CTX, u"cits %s: cite_context 越界 %s" % (rid, r["cite_context"]))
            elif layer == "opns":
                chk(r["opinion_type"] in O_TYPE, u"opns %s: opinion_type 越界 %s" % (rid, r["opinion_type"]))
                if "tone" in r:
                    chk(r["tone"] in O_TONE, u"opns %s: tone 越界 %s" % (rid, r["tone"]))
                if "firsthand_witness" in r:
                    chk(r["firsthand_witness"] in O_FW, u"opns %s: firsthand 越界 %s" % (rid, r["firsthand_witness"]))
                if "faction" in r:
                    chk(r["faction"] in E_FAC, u"opns %s: faction 越界" % rid)
                chk(r["author"] in ENT_IDS, u"opns %s: author 悬空 %s" % (rid, r["author"]))
            elif layer == "mings":
                chk(r["reign"] in M_REIGN, u"mings %s: reign 越界 %s" % (rid, r["reign"]))
                if "category" in r:
                    chk(r["category"] in M_CAT, u"mings %s: category 越界" % rid)
                chk(r["person"] in ENT_IDS, u"mings %s: person 悬空 %s" % (rid, r["person"]))
            elif layer == "tmes":
                chk(r["category"] in T_CAT, u"tmes %s: category 越界 %s" % (rid, r["category"]))
                chk(r["reign"] in REIGN_ORDER, u"tmes %s: reign 越界 %s" % (rid, r["reign"]))
                chk(r["era"] == REIGN_ORDER[r["reign"]], u"tmes %s: era 与 reign 不符" % rid)
            elif layer == "regs":
                chk(r["type"] in G_TYPE, u"regs %s: type 越界 %s" % (rid, r["type"]))
                chk(r["reign"] in REIGNS, u"regs %s: reign 越界 %s" % (rid, r["reign"]))
        chk(len(seen) == len(data), u"%s: ID 计数不符" % layer)

    # ENT 段与 ID 上限
    ent_ids = [r["ent_id"] for r in ENTS]
    chk(len(ent_ids) <= 100, u"ents 超过 100 条")
    for e in ent_ids:
        n = int(e.split("-")[1])
        chk(3200 <= n <= 3299, u"ents ID 越段 %s" % e)
    # 覆盖
    covered = set()
    for _, _, data in LAYER_SPECS:
        for r in data:
            covered.add(r["item_id"])
    missing = sorted(ALL_ITEMS - covered)
    chk(not missing, u"条目未覆盖: %s" % missing)
    print(u"条目覆盖: %d/54" % len(covered & ALL_ITEMS))
    # registry 校验
    reg = os.path.join(BASE, "_item_registry.json")
    if os.path.exists(reg):
        with io.open(reg, encoding="utf-8") as f:
            rr = json.load(f)
        regset = {x["item_id"] for x in rr.get("records", [])}
        bad = sorted(covered - regset)
        chk(not bad, u"item_id 不在 registry: %s" % bad)
    return errs, warns


def main():
    write_layers()
    errs, warns = selfcheck()
    print(u"--- 自检 ---")
    for e in errs:
        print(u"[ERR] " + e)
    for w in warns:
        print(u"[WARN] " + w)
    print(u"errors=%d warnings=%d" % (len(errs), len(warns)))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())

