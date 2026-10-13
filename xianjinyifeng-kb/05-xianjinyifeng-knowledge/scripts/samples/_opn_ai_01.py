# -*- coding: utf-8 -*-
"""《先进遗风》OPN 作者论说层源数据样例（_opn_ai_01.py）

说明：
  * 顶层键固定为 opns（列表）
  * 触发词：论曰/愚按/耿子曰/余按/予谓/余以为/余闻/盖尝论
  * 单条字段：
      item_id  必填，指纹库条号
      topic    论说主题（概要不抄原文）
      stance   立场，封闭集 5 值（_kg_enums.OPN_STANCES）
      argument 论点概要（只写要点，不抄原文）
      trigger  触发词（原文）
"""

opns = [
    {
        "item_id": "01-007",
        "topic": "鲁公初第即不忍厉梓里",
        "stance": "肯定",
        "argument": "作者赞鲁公初第即体贴乡里、衷笃识远",
        "trigger": "论曰",
    },
]
