# -*- coding: utf-8 -*-
"""《水东日记》卷 22 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "22-001 | 周礼一书汉以下名儒率有评议然莽用于汉安石用于宋皆不効者虽非其",
    "22-002 | 正统十四年未多事之先五军都督府并锦衣等卫官旗军人等三百二十五",
    "22-003 | 兵科职掌有守衞官军四城官军二揭帖间见正统十三年所藏二本葢予私",
    "22-004 | 右揭帖乃守衞官军自东安门起至玄武门凡若干门各门轮拨官旗旗军",
    "22-005 | 午门", "22-006 | 长安左门", "22-007 | 长安右门", "22-008 | 东华门",
    "22-009 | 西华门", "22-010 | 玄武门", "22-011 | 左顺门", "22-012 | 右顺门",
    "22-013 | 奉天门", "22-014 | 皇极门", "22-015 | 会极门", "22-016 | 归极门",
    "22-017 | 东安门", "22-018 | 西安门", "22-019 | 北安门", "22-020 | 东上南门",
    "22-021 | 西上南门", "22-022 | 右四城官军揭帖自朝阳等门起至德胜等门止",
    "22-023 | 朝阳门", "22-024 | 东直门", "22-025 | 西直门", "22-026 | 德胜门",
    "22-027 | 杨文贞公归田后作满江红词四首录之以识一时朝野景物之概",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 22-001 周礼序 ============
    {"item_id": "22-001", "text": "周礼", "type": "work", "normalized": "周礼（周官）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-001", "text": "叶水心", "type": "person", "normalized": "叶适（号水心）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "22-001", "text": "陈龙川", "type": "person", "normalized": "陈亮（号龙川）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "22-001", "text": "吕成公", "type": "person", "normalized": "吕祖谦（谥成公）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "22-001", "text": "王莽", "type": "person", "normalized": "王莽（新莽）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "22-001", "text": "王安石", "type": "person", "normalized": "王安石（荆公）", "confidence": 0.88, "source": "原文片段"},

    # ============ 22-002 正统官军数目 ============
    {"item_id": "22-002", "text": "正统十四年", "type": "era", "normalized": "正统十四年", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-002", "text": "五军都督府", "type": "institution", "normalized": "五军都督府", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-002", "text": "锦衣卫", "type": "institution", "normalized": "锦衣卫", "confidence": 0.9, "source": "原文片段"},

    # ============ 22-003/004 守卫官军揭帖 ============
    {"item_id": "22-003", "text": "兵科", "type": "institution", "normalized": "兵科（六科之一）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-004", "text": "东安门", "type": "place", "normalized": "东安门", "confidence": 0.9, "source": "原文片段"},

    # ============ 22-005~021 宫城门名 ============
    {"item_id": "22-005", "text": "午门", "type": "place", "normalized": "午门（紫禁城正门）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-006", "text": "长安左门", "type": "place", "normalized": "长安左门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-007", "text": "长安右门", "type": "place", "normalized": "长安右门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-008", "text": "东华门", "type": "place", "normalized": "东华门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-009", "text": "西华门", "type": "place", "normalized": "西华门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-010", "text": "玄武门", "type": "place", "normalized": "玄武门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-011", "text": "左顺门", "type": "place", "normalized": "左顺门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-012", "text": "右顺门", "type": "place", "normalized": "右顺门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-013", "text": "奉天门", "type": "place", "normalized": "奉天门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-014", "text": "皇极门", "type": "place", "normalized": "皇极门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-015", "text": "会极门", "type": "place", "normalized": "会极门", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "22-016", "text": "归极门", "type": "place", "normalized": "归极门", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "22-017", "text": "东安门", "type": "place", "normalized": "东安门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-018", "text": "西安门", "type": "place", "normalized": "西安门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-019", "text": "北安门", "type": "place", "normalized": "北安门", "confidence": 0.9, "source": "原文片段"},

    # ============ 22-022~026 京城九门 ============
    {"item_id": "22-022", "text": "朝阳门", "type": "place", "normalized": "朝阳门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-023", "text": "朝阳门", "type": "place", "normalized": "朝阳门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-024", "text": "东直门", "type": "place", "normalized": "东直门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-025", "text": "西直门", "type": "place", "normalized": "西直门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-026", "text": "德胜门", "type": "place", "normalized": "德胜门", "confidence": 0.9, "source": "原文片段"},

    # ============ 22-027 杨文贞满江红词 ============
    {"item_id": "22-027", "text": "杨文贞公", "type": "person", "normalized": "杨士奇（谥文贞）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "22-027", "text": "满江红", "type": "work", "normalized": "满江红（词牌）", "confidence": 0.85, "source": "原文片段"},
]
