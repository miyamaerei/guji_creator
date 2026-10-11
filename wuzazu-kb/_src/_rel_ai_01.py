"""（自动摊平，勿手改）由 _vol_01.py 拆出。
层：rel　卷：01 天部一　记录数：22
要改内容请改 _vol_01.py 后重新 python _vol_sync.py split。
"""

RECORDS = [
    {
        "person_a": "汉文帝",
        "person_b": "邓通",
        "relation_type": "其他",
        "direction": "双向",
        "evidence": "即汉文帝之于邓通，哀帝之于董贤，同卧起者数矣，未闻帝座之有犯也",
        "item_id": "01-017"
    },
    {
        "person_a": "哀帝",
        "person_b": "董贤",
        "relation_type": "其他",
        "direction": "双向",
        "evidence": "即汉文帝之于邓通，哀帝之于董贤，同卧起者数矣，未闻帝座之有犯也",
        "item_id": "01-017"
    },
    {
        "person_a": "刘健",
        "person_b": "谢迁",
        "relation_type": "同僚",
        "direction": "双向",
        "evidence": "未几，逆瑾出首，逐内阁刘健、谢迁，而后九卿台谏无不被祸",
        "item_id": "01-023"
    },
    {
        "person_a": "张居正",
        "person_b": "赵用贤",
        "relation_type": "恩怨",
        "direction": "单向",
        "evidence": "无何，而张居正以夺情事杖，赵用贤、吴中行、艾穆、邹元标等，编管远方",
        "item_id": "01-023"
    },
    {
        "person_a": "张居正",
        "person_b": "王锡爵",
        "relation_type": "敌对",
        "direction": "单向",
        "evidence": "逐王锡爵、张位等。朝中正人为之一空",
        "item_id": "01-023"
    },
    {
        "person_a": "张居正",
        "person_b": "赵用贤",
        "relation_type": "同僚",
        "direction": "单向",
        "evidence": "夺情之争，赵用贤等抗争被杖编管",
        "item_id": "01-023"
    },
    {
        "person_a": "张居正",
        "person_b": "邹元标",
        "relation_type": "同僚",
        "direction": "单向",
        "evidence": "夺情之争，邹元标被编管远方",
        "item_id": "01-023"
    },
    {
        "person_a": "刘健",
        "person_b": "谢迁",
        "relation_type": "同僚",
        "direction": "双向",
        "evidence": "同为逆瑾所逐之内阁",
        "item_id": "01-023"
    },
    {
        "person_a": "孔子",
        "person_b": "曾子",
        "relation_type": "师生",
        "direction": "单向",
        "evidence": "孔子答曾子：“诸侯见天子入门，不得终礼者，太庙火，日食是也。”",
        "item_id": "01-065"
    },
    {
        "person_a": "永乐帝",
        "person_b": "夏原吉",
        "relation_type": "上下级",
        "direction": "双向",
        "evidence": "上惊异，欲从之。独夏原吉曰：“此幻术也……”上语廷臣，原吉终不以为然",
        "item_id": "01-073"
    },
    {
        "person_a": "夏原吉",
        "person_b": "明成祖（永乐帝）",
        "relation_type": "同僚",
        "direction": "单向",
        "evidence": "力谏帝勿信道士幻术，帝不听，后果悟",
        "item_id": "01-073"
    },
    {
        "person_a": "王氏",
        "person_b": "天女",
        "relation_type": "姻亲",
        "direction": "双向",
        "evidence": "遂为夫妇。今王氏百年科名，贵盛无比，皆天女之后也",
        "item_id": "01-076"
    },
    {
        "person_a": "习凿齿",
        "person_b": "星人",
        "relation_type": "其他",
        "direction": "单向",
        "evidence": "习凿齿谓星人曰：“君尝闻知星宿有不覆之义乎？”",
        "item_id": "01-078"
    },
    {
        "person_a": "狄仁杰",
        "person_b": "叶迁招",
        "relation_type": "其他",
        "direction": "双向",
        "evidence": "又叶迁招曾避雨，亦救雷公于夹树间。翌日，雷公授以墨篆，与仁杰事政同",
        "item_id": "01-089"
    },
    {
        "person_a": "马生尔骐",
        "person_b": "马生尔骐之母",
        "relation_type": "父子亲属",
        "direction": "单向",
        "evidence": "东郡马生尔骐言其母，一日，雷绕户外，念东室漏，趋视之，大震一声，有龙自其枕下出",
        "item_id": "01-090"
    },
    {
        "person_a": "张熹",
        "person_b": "主簿",
        "relation_type": "上下级",
        "direction": "单向",
        "evidence": "临武张熹为平舆令，乃卒焚死。有主簿小吏皆从焚",
        "item_id": "01-098"
    },
    {
        "person_a": "元稹",
        "person_b": "石虎",
        "relation_type": "其他",
        "direction": "单向",
        "evidence": "南安王元稹为相州刺史，祷雨不效，鞭石虎像一百，未几，疽发背死",
        "item_id": "01-100"
    },
    {
        "person_a": "奚康生",
        "person_b": "西门豹",
        "relation_type": "其他",
        "direction": "单向",
        "evidence": "奚康生在相，亦以祷雨取西门豹舌，三儿暴丧，身亦遇疾",
        "item_id": "01-100"
    },
    {
        "person_a": "江公铎",
        "person_b": "城隍",
        "relation_type": "同僚",
        "direction": "单向",
        "evidence": "大旱与城隍约，不雨则暴之枷之",
        "item_id": "01-100"
    },
    {
        "person_a": "谢肇淛",
        "person_b": "徐兴公",
        "relation_type": "其他",
        "direction": "双向",
        "evidence": "余一日与徐兴公集法海寺，至暮而别。余西行数十步，即遇大雨如注，衣巾淋漓；兴公东行，点滴而已",
        "item_id": "01-103"
    },
    {
        "person_a": "谢肇淛",
        "person_b": "陈后山",
        "relation_type": "其他",
        "direction": "单向",
        "evidence": "陈后山云：“中秋，阴晴天下如一。”此语未试，然亦恐不尽然也",
        "item_id": "01-103"
    },
    {
        "person_a": "石氏女",
        "person_b": "尤郎",
        "relation_type": "姻亲",
        "direction": "双向",
        "evidence": "相传石氏女嫁为尤郎妇，尤出贾石思忆之至死曰：“吾当作大风，为天下妇人阻商旅也。”故名“石尤”云",
        "item_id": "01-118"
    }
]
