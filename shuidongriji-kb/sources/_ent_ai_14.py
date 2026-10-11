# -*- coding: utf-8 -*-
"""《水东日记》卷 14 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "14-001 | 皇祐四年夏五月邕獠刦库兵称乱陈船顺江絶数郡郡之守臣狃于承平弛",
    "14-002 | 王抑庵先生还政归泰和日有叹落花一首最爱东园桃李花可堪飘荡委泥",
    "14-003 | 王贞妇淸风岭事昭然在金石灿然在简册可征也夏宪使言昔有一人以为",
    "14-004 | 东广人言其地有宋坟无唐坟盖自宋南渡后衣冠家多流落至此始变其族",
    "14-005 | 庐陵李祯字昌祺河南左布政使为人耿介亷洁自始仕至归老始终一致人",
    "14-006 | 广州府学教授长乐郑万奎藏其父躭犁手卷有洪武甲戌国子博士临安钱宰",
    "14-007 | 右程子遗书二十五篇二先生门人记其所见闻荅问之书也始诸公各自为",
    "14-008 | 杭州西湖傍近编竹节水可专菱芡之利而惟时有势力者可得之故杭人有",
    "14-009 | 韩都御史雍坐事被收西江术者周季龙曰此都御史官也及左迁按察司",
    "14-010 | 李景瓒占命闻京师至山东谓陆布政瑜曰刑部刘尚书休矣公宜促装代之",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 14-001 赵师旦闵忠诗碑 ============
    {"item_id": "14-001", "text": "皇祐四年", "type": "era", "normalized": "皇祐（宋仁宗年号）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "14-001", "text": "赵师旦", "type": "person", "normalized": "赵师旦（康州知州，谥赞）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "14-001", "text": "曹觐", "type": "person", "normalized": "曹觐（封州知州）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "14-001", "text": "元绛", "type": "person", "normalized": "元绛（字原，广南东路转运使）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "14-001", "text": "康州", "type": "place", "normalized": "康州（三洲洞）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "14-001", "text": "封州", "type": "place", "normalized": "封州", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "14-001", "text": "广南东路", "type": "place", "normalized": "广南东路", "confidence": 0.88, "source": "原文片段"},

    # ============ 14-002 王抑庵归田诗 ============
    {"item_id": "14-002", "text": "王抑庵", "type": "person", "normalized": "王直（号抑庵，谥文端）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "14-002", "text": "泰和", "type": "place", "normalized": "泰和", "confidence": 0.9, "source": "原文片段"},

    # ============ 14-003 王贞妇清风岭 ============
    {"item_id": "14-003", "text": "王贞妇", "type": "person", "normalized": "王贞妇（清风岭节妇）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "14-003", "text": "清风岭", "type": "place", "normalized": "清风岭", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "14-003", "text": "夏宪使", "type": "person", "normalized": "夏宪使（姓名未明）", "confidence": 0.8, "source": "原文片段"},

    # ============ 14-004 东广宋坟 赖布衣 ============
    {"item_id": "14-004", "text": "厉布衣", "type": "person", "normalized": "厉伯韶（俗称赖布衣，堪舆家）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "14-004", "text": "嘉定", "type": "era", "normalized": "嘉定（南宋宁宗年号）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "14-004", "text": "广州", "type": "place", "normalized": "广州", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "14-004", "text": "林弁", "type": "person", "normalized": "林弁（庚午举人）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "14-004", "text": "林汝思", "type": "person", "normalized": "林汝思（癸酉举人）", "confidence": 0.8, "source": "原文片段"},

    # ============ 14-005 李祯昌祺 ============
    {"item_id": "14-005", "text": "李祯", "type": "person", "normalized": "李祯（字昌祺，庐陵人，剪灯余话作者）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "14-005", "text": "河南左布政使", "type": "official", "normalized": "河南左布政使", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "14-005", "text": "韩雍", "type": "person", "normalized": "韩雍（都御史）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "14-005", "text": "剪灯余话", "type": "work", "normalized": "剪灯余话（李祯著）", "confidence": 0.9, "source": "原文片段"},

    # ============ 14-006 躭犁生传 ============
    {"item_id": "14-006", "text": "郑琳", "type": "person", "normalized": "郑琳（号躭犁生，闽人）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "14-006", "text": "郑万奎", "type": "person", "normalized": "郑万奎（郑琳子，广州府学教授）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "14-006", "text": "钱宰", "type": "person", "normalized": "钱宰（字子予，国子博士，躭犁生传作者）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "14-006", "text": "胡靖", "type": "person", "normalized": "胡靖（字光大，读躭犁生传）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "14-006", "text": "练子宁", "type": "person", "normalized": "练子宁（洪武三年作躭犁赋）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "14-006", "text": "张显宗", "type": "person", "normalized": "张显宗（状元及第，建文二年跋）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "14-006", "text": "钱习礼", "type": "person", "normalized": "钱习礼（钱吉水，翰林）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "14-006", "text": "杨荣", "type": "person", "normalized": "杨荣（建安，东里）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "14-006", "text": "躭犁生传", "type": "work", "normalized": "躭犁生传（钱宰撰）", "confidence": 0.85, "source": "原文片段"},

    # ============ 14-007 程子遗书 ============
    {"item_id": "14-007", "text": "朱熹", "type": "person", "normalized": "朱熹（晦庵，编次程氏遗书）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "14-007", "text": "程颢", "type": "person", "normalized": "程颢（明道先生）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "14-007", "text": "程颐", "type": "person", "normalized": "程颐（伊川先生）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "14-007", "text": "张栻", "type": "person", "normalized": "张栻（南轩，乾道九年跋）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "14-007", "text": "尹焞", "type": "person", "normalized": "尹焞（程门弟子）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "14-007", "text": "程氏遗书", "type": "work", "normalized": "程氏遗书（二先生遗书二十五篇）", "confidence": 0.88, "source": "原文片段"},

    # ============ 14-008 西湖谣 相术 ============
    {"item_id": "14-008", "text": "西湖", "type": "place", "normalized": "杭州西湖", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "14-008", "text": "袁忠彻", "type": "person", "normalized": "袁忠彻（四明，相士）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "14-008", "text": "白圭", "type": "person", "normalized": "白圭（布政，浙藩）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "14-008", "text": "王竑", "type": "person", "normalized": "王竑（都御史）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "14-008", "text": "于谦", "type": "person", "normalized": "于谦（兵部尚书）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "14-008", "text": "梁瑶", "type": "person", "normalized": "梁瑶（保定伯）", "confidence": 0.8, "source": "原文片段"},

    # ============ 14-009 韩雍坐事 ============
    {"item_id": "14-009", "text": "韩雍", "type": "person", "normalized": "韩雍（都御史）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "14-009", "text": "周季龙", "type": "person", "normalized": "周季龙（西江术者）", "confidence": 0.82, "source": "原文片段"},

    # ============ 14-010 李景瓒占命 ============
    {"item_id": "14-010", "text": "李景瓒", "type": "person", "normalized": "李景瓒（占命术者）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "14-010", "text": "陆瑜", "type": "person", "normalized": "陆瑜（布政）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "14-010", "text": "钱原溥", "type": "person", "normalized": "钱溥（字原溥，翰林）", "confidence": 0.85, "source": "原文片段"},
]
