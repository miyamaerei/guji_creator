# -*- coding: utf-8 -*-
"""《水东日记》卷 23 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "23-001 | 太师平章军国重事潞国文忠烈公生真宗景徳三年仁宗天圣五年二十二",
    "23-002 | 相台许可用中丞元延祐初科进士文章亦表着一时有盛名今世所见者可",
    "23-003 | 欧阳文忠公云汉以来有银青金紫之号青紫绶也金银其所佩印章绶所以",
    "23-004 | 内府所藏对类书有巧对甚多姑记其一二如云",
    "23-005 | 王交山先生尝著论谓寇准之亲征李纲之固守京师皆非也其说似是",
    "23-006 | 李性学古今文章精义一编皆录先儒论文字语今其书行于世",
    "23-007 | 曲阜孔林有孟氏祖庭图记碑岁久磨泐其文可考者今録于左",
    "23-008 | 宦防录所载方药多有验者今录薏苡一方云",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 23-001 文彦博翼城庙记 ============
    {"item_id": "23-001", "text": "文彦博", "type": "person", "normalized": "文彦博（封潞国公，谥忠烈）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "23-001", "text": "翼城县", "type": "place", "normalized": "翼城县", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "23-001", "text": "夏忠靖", "type": "person", "normalized": "夏原吉（谥忠靖）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "23-001", "text": "景德", "type": "era", "normalized": "景德（北宋真宗年号）", "confidence": 0.85, "source": "原文片段"},

    # ============ 23-002 许可用晋宁乡贤祠记 ============
    {"item_id": "23-002", "text": "许可用", "type": "person", "normalized": "许可用（相台，中丞，延祐初进士）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "23-002", "text": "晋宁路", "type": "place", "normalized": "晋宁路", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "23-002", "text": "延祐", "type": "era", "normalized": "延祐（元仁宗年号）", "confidence": 0.85, "source": "原文片段"},

    # ============ 23-003 欧阳文忠公论鱼袋 ============
    {"item_id": "23-003", "text": "欧阳文忠公", "type": "person", "normalized": "欧阳修（谥文忠）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "23-003", "text": "银青金紫", "type": "official", "normalized": "银青金紫（官阶章服）", "confidence": 0.82, "source": "原文片段"},

    # ============ 23-005 王交山论寇准李纲 ============
    {"item_id": "23-005", "text": "王交山", "type": "person", "normalized": "王交山（林州隐者）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "23-005", "text": "寇准", "type": "person", "normalized": "寇准（莱公）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "23-005", "text": "李纲", "type": "person", "normalized": "李纲（忠定）", "confidence": 0.88, "source": "原文片段"},

    # ============ 23-006 古今文章精义 ============
    {"item_id": "23-006", "text": "李性学", "type": "person", "normalized": "李性学（编古今文章精义）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "23-006", "text": "古今文章精义", "type": "work", "normalized": "古今文章精义（李性学编）", "confidence": 0.85, "source": "原文片段"},

    # ============ 23-007 孟氏祖庭图记碑 ============
    {"item_id": "23-007", "text": "孟氏祖庭图记", "type": "work", "normalized": "孟氏祖庭图记碑", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "23-007", "text": "孔林", "type": "place", "normalized": "曲阜孔林", "confidence": 0.85, "source": "原文片段"},

    # ============ 23-008 宦防录薏苡方 ============
    {"item_id": "23-008", "text": "宦防录", "type": "work", "normalized": "宦防录（药方书）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "23-008", "text": "辛稼轩", "type": "person", "normalized": "辛弃疾（号稼轩）", "confidence": 0.82, "source": "原文片段"},
]
