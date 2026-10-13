# -*- coding: utf-8 -*-
"""卷十八 18-001~18-015：实体层 AI 判定。"""
RECORDS = [
    # 18-001 御制碑涉及人物
    {"item_id": "18-001", "text": "周思得", "type": "person", "confidence": "high"},
    {"item_id": "18-001", "text": "周道宁", "type": "person", "confidence": "high"},
    {"item_id": "18-001", "text": "崔文", "type": "person", "confidence": "high"},
    {"item_id": "18-001", "text": "徐知证", "type": "person", "confidence": "high"},
    {"item_id": "18-001", "text": "徐知谔", "type": "person", "confidence": "high"},
    # 18-003 田宅涉及
    {"item_id": "18-003", "text": "张居正", "type": "person", "confidence": "high"},
    {"item_id": "18-003", "text": "赵志皋", "type": "person", "confidence": "high"},
    # 18-011 功臣坟
    {"item_id": "18-011", "text": "张玉", "type": "person", "confidence": "high"},
    {"item_id": "18-011", "text": "张辅", "type": "person", "confidence": "high"},
    {"item_id": "18-011", "text": "谭渊", "type": "person", "confidence": "high"},
    {"item_id": "18-011", "text": "谭佑", "type": "person", "confidence": "high"},
    # 18-012 祀亲/18-013 祀神/18-014 祀功
    {"item_id": "18-013", "text": "刘三吾", "type": "person", "confidence": "high"},
    {"item_id": "18-013", "text": "邹应龙", "type": "person", "confidence": "high"},
    {"item_id": "18-014", "text": "姚广孝", "type": "person", "confidence": "high"},
    {"item_id": "18-014", "text": "焦芳", "type": "person", "confidence": "high"},
    {"item_id": "18-014", "text": "刘健", "type": "person", "confidence": "high"},
    # 寺观祠庙（机构）
    {"item_id": "18-001", "text": "朝天宫", "type": "institution", "confidence": "high"},
    {"item_id": "18-001", "text": "大德观", "type": "institution", "confidence": "high"},
    {"item_id": "18-001", "text": "大德显灵宫", "type": "institution", "confidence": "high"},
    {"item_id": "18-001", "text": "洪恩灵济宫", "type": "institution", "confidence": "high"},
    {"item_id": "18-001", "text": "大隆善护国寺", "type": "institution", "confidence": "high"},
    {"item_id": "18-001", "text": "大觉寺", "type": "institution", "confidence": "high"},
    {"item_id": "18-001", "text": "大圆通寺", "type": "institution", "confidence": "high"},
    {"item_id": "18-001", "text": "三义庙", "type": "institution", "confidence": "high"},
    {"item_id": "18-013", "text": "都城隍庙", "type": "institution", "confidence": "high"},
    {"item_id": "18-013", "text": "汉寿亭侯庙", "type": "institution", "confidence": "high"},
    {"item_id": "18-013", "text": "灵明显佑宫", "type": "institution", "confidence": "high"},
    {"item_id": "18-003", "text": "保明寺", "type": "institution", "confidence": "high"},
    {"item_id": "18-003", "text": "万寿寺", "type": "institution", "confidence": "high"},
    {"item_id": "18-003", "text": "嘉祥观", "type": "institution", "confidence": "high"},
]
