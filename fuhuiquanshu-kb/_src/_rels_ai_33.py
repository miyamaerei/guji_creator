# -*- coding: utf-8 -*-
"""卷33 禀启附·角色关系 REL（20 条，写信人与收信人书启关系）。"""
RECORDS = [
    {"item_id": "33-001", "person_a": "某（黄六鸿）", "person_b": "协院", "relation_type": "上下级", "direction": "单向", "evidence": "候某协院——某才惭下驷曾趋锦里之尘，望真人于霄汉日远长安，投下吏于海滨风殊闽徼", "confidence": "high"},
    {"item_id": "33-002", "person_a": "某（黄六鸿）", "person_b": "川抚刘公", "relation_type": "上下级", "direction": "单向", "evidence": "候川抚刘公——某仕林樗质宦海萍踪，仰青岱而蒙收久厕亭云之列，饮沧溟而知感难修涓滴之酬，未遑拥篲清尘敢用芹陈上从", "confidence": "high"},
    {"item_id": "33-003", "person_a": "某（黄六鸿）", "person_b": "文宗某", "relation_type": "上下级", "direction": "单向", "evidence": "候文宗某——某腹惭武库当年喜侍清尘，笔谢词锋此日惊瞻焰藻，借文星而照里依光之愿堪酬，媿宦海以羁踪拥篲之情莫展", "confidence": "high"},
    {"item_id": "33-004", "person_a": "某（黄六鸿）", "person_b": "水巡台", "relation_type": "上下级", "direction": "单向", "evidence": "候水巡台——某猥以监儒谬叨俗吏，蚁封盘马果何以回策如萦，鸡邑烹鲜终且惧负乘致寇，旁皇闻命战栗抚躬", "confidence": "high"},
    {"item_id": "33-005", "person_a": "某（黄六鸿）", "person_b": "潘守台", "relation_type": "上下级", "direction": "单向", "evidence": "候潘守台——某朴樕庸材仅枪鷃步，风尘贱吏谬润蜗涎，初领一同踯躅深虞折北，久依万厦命提实籍指南", "confidence": "high"},
    {"item_id": "33-006", "person_a": "某（黄六鸿）", "person_b": "钱太尊", "relation_type": "上下级", "direction": "单向", "evidence": "候钱太尊——某一经未究六翮无成，提封谬领一同县谱无闻三异，幸步清尘矢心效其正笏，窃追芳躅引领欣为执鞭", "confidence": "high"},
    {"item_id": "33-007", "person_a": "某（黄六鸿）", "person_b": "许刑馆", "relation_type": "上下级", "direction": "单向", "evidence": "候许刑馆——某躬惭短羽力借长风，缅记燕台附骥喜分杏籍之余荣，朝夕受事干左右提命渐引于周行", "confidence": "high"},
    {"item_id": "33-008", "person_a": "某（黄六鸿）", "person_b": "张三府", "relation_type": "上下级", "direction": "单向", "evidence": "候张三府——某学惭为长官喜得师，山城驯雉深怀鸣绮之风，幸仪型伊迩可佩服为韦弦，快趋步有规得借熏于兰□【巳上先君文集】", "confidence": "high"},
    {"item_id": "33-009", "person_a": "某（黄六鸿）", "person_b": "守道", "relation_type": "上下级", "direction": "单向", "evidence": "送守道入贺圣寿——某生际昌期躬逢胜事，惭负弩之无由谨贡暄而作颂", "confidence": "high"},
    {"item_id": "33-010", "person_a": "某（黄六鸿）", "person_b": "道尊", "relation_type": "上下级", "direction": "单向", "evidence": "贺道尊寿——某久庇帡幪深沾培植，覩兹悬弧之令节曷胜献曝之微忱，谨效虫吟聊申燕贺", "confidence": "high"},
    {"item_id": "33-011", "person_a": "某（黄六鸿）", "person_b": "兵备道", "relation_type": "上下级", "direction": "单向", "evidence": "上兵备道——某学困雕虫才惭倚马，肉食徒讥于曹刿莫佐一筹，毛锥久掷于班生未能万里，幸托龙门而长价徒瞻虎旅以杨休", "confidence": "high"},
    {"item_id": "33-012", "person_a": "某（黄六鸿）", "person_b": "袁抚台", "relation_type": "上下级", "direction": "单向", "evidence": "谢袁抚台——某质本迂疏才无表见，荆州品题即佳士何期迹混齐竿，欧阳赏识必闻人窃槐质同燕石，心切雀环情陈理素", "confidence": "high"},
    {"item_id": "33-013", "person_a": "某（黄六鸿）", "person_b": "郑郡守", "relation_type": "上下级", "direction": "单向", "evidence": "迎郑郡守——某官惭司理职摄端城，仰瞻台从何异云霓，敬迓文旌聊同竹马，伏冀遄临曷胜宠籍【巳上外父邹匪石先生文集】", "confidence": "high"},
    {"item_id": "33-014", "person_a": "某（黄六鸿）", "person_b": "杨提台", "relation_type": "上下级", "direction": "单向", "evidence": "候杨提台——某江介鲰生边陲末吏，材同下里滥吹齐氏之竿，质比轻萝愿附将军之树，泐布芜词侑将芹献，伏冀台慈俯垂鉴采", "confidence": "high"},
    {"item_id": "33-015", "person_a": "某（黄六鸿）", "person_b": "学台", "relation_type": "上下级", "direction": "单向", "evidence": "贺学台新正——某朴樕微材章缝贱品，绾铜有惧茂弘结绶常惭叔度，高山之仰止弥殷冀无忝于朗鉴", "confidence": "high"},
    {"item_id": "33-019", "person_a": "某（黄六鸿）", "person_b": "济东丹道台", "relation_type": "上下级", "direction": "单向", "evidence": "贺济东丹道台兼理驿传——某荒区末吏江介鲰生，手扳送迎每愧尘沾首蒭茭供峙尤惭职隶虎符，欣瞻一路福星远窃二天恩庇", "confidence": "high"},
    {"item_id": "33-020", "person_a": "弟某（黄六鸿）", "person_b": "张寅翁", "relation_type": "同僚", "direction": "单向", "evidence": "迎新任张寅翁——弟某江表鲰生蠹藂下士，两年作吏深愧糠粃之先，一旦去官犹幸兼葭之倚，抚此疮痍赤子念念惟父母遗惭", "confidence": "high"},
    {"item_id": "33-026", "person_a": "某（黄六鸿）", "person_b": "济南金太尊", "relation_type": "上下级", "direction": "单向", "evidence": "复济南金太尊——某荒区末吏江介迂儒，乃未修禀于鱼笺先志隆施于雀跃，尺函远锡真如十部之荣，敬因宪使之旋薄具曝芹之献", "confidence": "high"},
    {"item_id": "33-030", "person_a": "弟某（黄六鸿）", "person_b": "张寅翁", "relation_type": "同僚", "direction": "单向", "evidence": "迎新任张寅翁——弟某朴樕匪材谬膺民社，十年尘欠两载艰辛，欲纾赋则前令有未竟之局，欲督催则小民有并征之苦，心力交穷垫赔踵累", "confidence": "high"},
    {"item_id": "33-033", "person_a": "弟某（黄六鸿）", "person_b": "宿迁令君", "relation_type": "同僚", "direction": "单向", "evidence": "贺宿迁令君之任——弟某朴樕下材滥竿滋土，而老年台命世弘猷暂为小试，荒郯之与贵治冲剧难治政复相同，敢云葭玉之倚庶几唇齿之依", "confidence": "high"},
]
