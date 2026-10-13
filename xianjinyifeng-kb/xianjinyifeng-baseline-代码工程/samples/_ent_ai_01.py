# -*- coding: utf-8 -*-
"""《先进遗风》L1 实体层源数据样例（_ent_ai_01.py）

说明：
  * 文件名规则：_ent_ai_<卷号>.py（卷号来自 _kg_config.VOLUME_MAP 映射后的 NN）
  * 顶层键固定为 annotations（列表，逐条实体提及）
  * 单条字段：
      item_id    必填，指纹库条号（NN-NNN），original 由打包器注入（#3 禁止手抄原文）
      text       原文词形（尽可能原样，宁长勿截）
      type       实体类型，必填，封闭集 18 值（_kg_enums.ENTITY_TYPES）
      normalized 规范化主名（引用侧统一主名；缺省则取 text）
      confidence 0-1 置信度（<0.8 自动入 V2 待核清单）
  * 不写业务 ID（打包器按组级分配 ent_id）、不写 original/norm（自动注入）
"""

annotations = [
    {
        "item_id": "01-001",
        "text": "学士宋文宪公濓",
        "type": "person",
        "normalized": "宋濂",
        "confidence": 0.98,
    },
    {
        "item_id": "01-001",
        "text": "文宪",
        "type": "posthumous",
        "normalized": "文宪",
        "confidence": 0.95,
    },
    {
        "item_id": "01-007",
        "text": "鲁公",
        "type": "person",
        "normalized": "鲁穆",
        "confidence": 0.8,
    },
    {
        "item_id": "01-007",
        "text": "刘忠宣",
        "type": "person",
        "normalized": "刘大夏",
        "confidence": 0.9,
    },
    {
        "item_id": "01-008",
        "text": "杨文定公溥",
        "type": "person",
        "normalized": "杨溥",
        "confidence": 0.98,
    },
    {
        "item_id": "01-008",
        "text": "江陵",
        "type": "place",
        "normalized": "江陵",
        "confidence": 0.95,
    },
    {
        "item_id": "01-039",
        "text": "新建伯文成王先生守仁",
        "type": "person",
        "normalized": "王守仁",
        "confidence": 0.98,
    },
    {
        "item_id": "01-039",
        "text": "刑部",
        "type": "institution",
        "normalized": "刑部",
        "confidence": 0.97,
    },
    {
        "item_id": "01-039",
        "text": "提牢厅",
        "type": "institution",
        "normalized": "提牢厅",
        "confidence": 0.9,
    },
]
