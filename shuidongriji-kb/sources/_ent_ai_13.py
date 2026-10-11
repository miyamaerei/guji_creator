# -*- coding: utf-8 -*-
"""《水东日记》卷 13 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "13-001 | 邹奕字道苏州人有文行元季尝守贑国初谪关西与一时知名士若江右",
    "13-002 | 谢员友规者鄞人洪武初以户役起充浙江宪司吏非其志也告指疾求退得",
    "13-003 | 洪武己巳之秋予兵籍都城艮维之姚坊门乃九月八日与其侪输作于公",
    "13-004 | 袭阳武侯家因凿池得唐故幽州衙前【缺】　使乐安郡府君孙公墓志铭",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 13-001 邹弘道与沈诚庄倡和诗、杏林小隐记 ============
    {"item_id": "13-001", "text": "邹奕", "type": "person", "normalized": "邹奕（字弘道，苏州人）", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "13-001", "text": "苏州", "type": "place", "normalized": "苏州", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "13-001", "text": "夹谷希顔", "type": "person", "normalized": "夹谷希颜", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "13-001", "text": "徐兰", "type": "person", "normalized": "徐兰（三衢）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "13-001", "text": "沈绎诚庄", "type": "person", "normalized": "沈绎（字诚庄，又名成章，儒医，居兰州）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "13-001", "text": "陆禧彦吉", "type": "person", "normalized": "陆禧（字彦吉，同郡）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "13-001", "text": "丁晋仲敏", "type": "person", "normalized": "丁晋（字仲敏，昆山人）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "13-001", "text": "董奉", "type": "person", "normalized": "董奉（三国吴神医，杏林典故）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "13-001", "text": "倪瓉", "type": "person", "normalized": "倪瓒（云林）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "13-001", "text": "兰州", "type": "place", "normalized": "兰州（关西）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "13-001", "text": "皋兰", "type": "place", "normalized": "皋兰（兰州）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "13-001", "text": "张掖", "type": "place", "normalized": "张掖", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "13-001", "text": "洪武壬申", "type": "era", "normalized": "洪武（明太祖年号）", "confidence": 0.9, "source": "原文片段"},

    # ============ 13-002 谢员、潘若水、斯隆玛 ============
    {"item_id": "13-002", "text": "谢员", "type": "person", "normalized": "谢员（字友规，鄞人）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "13-002", "text": "潘若水", "type": "person", "normalized": "潘若水（临江人，退庵集）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "13-002", "text": "解学士大绅", "type": "person", "normalized": "解缙（字大绅，谥文毅）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "13-002", "text": "斯隆玛", "type": "person", "normalized": "斯隆玛（西域人，谢员戏称库生）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "13-002", "text": "临洮府", "type": "place", "normalized": "临洮府", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "13-002", "text": "兴州卫", "type": "place", "normalized": "兴州卫", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "13-002", "text": "西宁行太仆寺", "type": "institution", "normalized": "西宁行太仆寺", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "13-002", "text": "永乐大典", "type": "work", "normalized": "永乐大典", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "13-002", "text": "鸣穷集", "type": "work", "normalized": "鸣穷集（谢员著）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "13-002", "text": "退庵集", "type": "work", "normalized": "退庵集（潘若水著）", "confidence": 0.85, "source": "原文片段"},

    # ============ 13-003 口神梦（叶盛自寓） ============
    {"item_id": "13-003", "text": "洪武己巳", "type": "era", "normalized": "洪武（明太祖年号，己巳=洪武二十二年）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "13-003", "text": "姚坊门", "type": "place", "normalized": "姚坊门（京师城东门）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "13-003", "text": "龙江", "type": "place", "normalized": "龙江（京师）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "13-003", "text": "丹朱", "type": "person", "normalized": "口神自托丹朱（神话人物）", "confidence": 0.8, "source": "原文片段"},

    # ============ 13-004 唐孙公墓志铭出土 ============
    {"item_id": "13-004", "text": "阳武侯", "type": "person", "normalized": "阳武侯（明爵，其家凿池得碑）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "13-004", "text": "孙绪", "type": "person", "normalized": "孙绪（字宗绪，唐乐安郡府君）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "13-004", "text": "孙伏伽", "type": "person", "normalized": "孙伏伽（唐大理卿，孙绪五世祖）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "13-004", "text": "黄谏", "type": "person", "normalized": "黄谏（通判，藏碑于其家）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "13-004", "text": "幽州", "type": "place", "normalized": "幽州", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "13-004", "text": "唐", "type": "era", "normalized": "唐", "confidence": 0.9, "source": "原文片段"},
]
