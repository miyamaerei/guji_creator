"""L1 实体层源数据样例（卷一）

形状约定：
  item_id  必填，条粒度主键 NN-NNN（序卷 = 00）
  text     必填，原文中出现的实体词形（照抄原文，不加书名号等符号）
  type     必填，枚举 entity_type 的取值：
           person / place / work / official / era / object / animal / plant / food / unknown
           写 office→official、book→work 等旧写法也会被自动归一

不必写：id（ENT- 由打包器分配）、normalized（由 canon_surface 归一）、
        start/end（缺省时用 text 在 original 中的位置推算）、original/norm（指纹库注入）
"""

RECORDS = [
    {"item_id": "01-001", "text": "老子", "type": "person"},
    {"item_id": "01-003", "text": "释氏", "type": "person"},
    {"item_id": "01-004", "text": "朱晦翁", "type": "person"},
    {"item_id": "01-004", "text": "天", "type": "object"},
    {"item_id": "01-005", "text": "天变不足畏", "type": "work"},
    {"item_id": "01-006", "text": "璇玑玉衡", "type": "object"},
    {"item_id": "01-006", "text": "洛下闳", "type": "person"},
    {"item_id": "01-006", "text": "僧一行", "type": "person"},
    {"item_id": "01-006", "text": "舜", "type": "person"},
    {"item_id": "01-007", "text": "汉明帝", "type": "person"},
    {"item_id": "01-007", "text": "张重", "type": "person"},
    {"item_id": "01-007", "text": "日南郡", "type": "place"},
]
