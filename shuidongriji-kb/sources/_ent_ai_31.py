# -*- coding: utf-8 -*-
"""《水东日记》卷 31 —— L1 实体标注 源数据（AI 判定逐条填写）

覆盖条目：31-001~31-012（共 12 条）。
"""

ITEM_LIST = [
    "31-001 | 江南并海之河江港汊通潮汐者",
    "31-002 | 戏谈于凡四方人多以其土名",
    "31-003 | 前人所作墓文碑志序称述子妇者甚少",
    "31-004 | 安阳公居政府之五年",
    "31-005 | 别记独不云小臣廉乎",
    "31-006 | 允矣鲁公生而敦厖",
    "31-007 | 翰林侍讲学士通奉大夫知制诰同修国史兼国子祭酒欧阳玄撰",
    "31-008 | 翰林学士承旨荣禄大夫知制诰兼修国史赵孟頫书篆",
    "31-009 | 至元四年岁在戊寅八月吉日建",
    "31-010 | 天顺七年予在广东肇庆军前用旧韵集赵子昂诗五绝句",
    "31-011 | 登州蓬莱县纳布老人言海市",
    "31-012 | 朱子答张仁叔之问曰李悝百亩而收百五十石",
]

DATA = [
    # ---- 31-001 江南潮沙 ----
    {"id": "ENT-15501", "item_id": "31-001", "text": "江南并海", "type": "place", "start": 0, "end": 0, "normalized": "江南并海地区", "confidence": 0.85, "source": "江南并海之河江港汊"},
    # ---- 31-002 四方土名 ----
    {"id": "ENT-15502", "item_id": "31-002", "text": "宋祭酒", "type": "person", "start": 0, "end": 0, "normalized": "宋讷（明初国子监祭酒）", "confidence": 0.82, "source": "宋祭酒尝过洛"},
    {"id": "ENT-15503", "item_id": "31-002", "text": "罗隐", "type": "person", "start": 0, "end": 0, "normalized": "罗隐", "confidence": 0.82, "source": "唐罗隐盗得之"},
    # ---- 31-003~009 许熙载神道碑 ----
    {"id": "ENT-15504", "item_id": "31-003", "text": "圭斋", "type": "person", "start": 0, "end": 0, "normalized": "欧阳玄（号圭斋）", "confidence": 0.9, "source": "圭斋之于圭塘"},
    {"id": "ENT-15505", "item_id": "31-003", "text": "圭塘", "type": "person", "start": 0, "end": 0, "normalized": "许有壬（号圭塘）", "confidence": 0.88, "source": "圭斋之于圭塘"},
    {"id": "ENT-15506", "item_id": "31-004", "text": "安阳公", "type": "person", "start": 0, "end": 0, "normalized": "许有壬（谥文忠，安阳人）", "confidence": 0.88, "source": "安阳公居政府之五年"},
    {"id": "ENT-15507", "item_id": "31-004", "text": "许熙载", "type": "person", "start": 0, "end": 0, "normalized": "许熙载（字献臣，追封鲁郡公）", "confidence": 0.88, "source": "鲁公讳熙载字献臣"},
    {"id": "ENT-15508", "item_id": "31-004", "text": "欧阳玄", "type": "person", "start": 0, "end": 0, "normalized": "欧阳玄（字元，号圭斋）", "confidence": 0.92, "source": "命其友欧阳玄文诸神道之石"},
    {"id": "ENT-15509", "item_id": "31-004", "text": "兖文忠公", "type": "person", "start": 0, "end": 0, "normalized": "兖文忠公", "confidence": 0.78, "source": "援吾宗兖文忠公例"},
    {"id": "ENT-15510", "item_id": "31-005", "text": "张起岩", "type": "person", "start": 0, "end": 0, "normalized": "张起岩", "confidence": 0.85, "source": "南台侍御史济南张公起岩"},
    {"id": "ENT-15511", "item_id": "31-005", "text": "马祖常", "type": "person", "start": 0, "end": 0, "normalized": "马祖常", "confidence": 0.88, "source": "御史中丞浚仪马公祖常"},
    {"id": "ENT-15512", "item_id": "31-007", "text": "国子祭酒", "type": "official", "start": 0, "end": 0, "normalized": "国子祭酒", "confidence": 0.9, "source": "兼国子祭酒"},
    {"id": "ENT-15513", "item_id": "31-008", "text": "赵孟頫", "type": "person", "start": 0, "end": 0, "normalized": "赵孟頫（字子昂，号松雪）", "confidence": 0.92, "source": "赵孟頫书篆"},
    {"id": "ENT-15514", "item_id": "31-008", "text": "茅绍之", "type": "person", "start": 0, "end": 0, "normalized": "茅绍之（能静处士）", "confidence": 0.82, "source": "能静处士茅绍之集勒"},
    # ---- 31-010 集赵诗 ----
    {"id": "ENT-15515", "item_id": "31-010", "text": "赵子昂", "type": "person", "start": 0, "end": 0, "normalized": "赵孟頫", "confidence": 0.9, "source": "集赵子昂诗五绝句"},
    {"id": "ENT-15516", "item_id": "31-010", "text": "永熙", "type": "person", "start": 0, "end": 0, "normalized": "永熙", "confidence": 0.82, "source": "寄永熙致之群公"},
    {"id": "ENT-15517", "item_id": "31-010", "text": "钦谟", "type": "person", "start": 0, "end": 0, "normalized": "钦谟", "confidence": 0.8, "source": "钦谟自史馆集唐诗二首见寄"},
    # ---- 31-011 登州海市 ----
    {"id": "ENT-15518", "item_id": "31-011", "text": "登州蓬莱", "type": "place", "start": 0, "end": 0, "normalized": "登州蓬莱", "confidence": 0.9, "source": "登州蓬莱县"},
    {"id": "ENT-15519", "item_id": "31-011", "text": "苏东坡", "type": "person", "start": 0, "end": 0, "normalized": "苏轼", "confidence": 0.92, "source": "苏东坡有海市诗"},
    # ---- 31-012 朱子答张仁叔 ----
    {"id": "ENT-15520", "item_id": "31-012", "text": "朱子", "type": "person", "start": 0, "end": 0, "normalized": "朱熹", "confidence": 0.92, "source": "朱子答张仁叔之问"},
    {"id": "ENT-15521", "item_id": "31-012", "text": "张仁叔", "type": "person", "start": 0, "end": 0, "normalized": "张仁叔", "confidence": 0.82, "source": "张仁叔之问"},
    {"id": "ENT-15522", "item_id": "31-012", "text": "李悝", "type": "person", "start": 0, "end": 0, "normalized": "李悝", "confidence": 0.88, "source": "李悝百亩而收百五十石"},
    {"id": "ENT-15523", "item_id": "31-012", "text": "晁错", "type": "person", "start": 0, "end": 0, "normalized": "晁错", "confidence": 0.88, "source": "晁错百亩而收不过百石"},
    {"id": "ENT-15524", "item_id": "31-012", "text": "夜不收", "type": "official", "start": 0, "end": 0, "normalized": "夜不收（边军探听）", "confidence": 0.9, "source": "西北极边谓夜不收"},
    {"id": "ENT-15525", "item_id": "31-012", "text": "宣府", "type": "place", "start": 0, "end": 0, "normalized": "宣府", "confidence": 0.92, "source": "宣府官田"},
]
# 缺口登记：31-004~006 碑文长文中的人物（许氏历官、僚属）不单列。
