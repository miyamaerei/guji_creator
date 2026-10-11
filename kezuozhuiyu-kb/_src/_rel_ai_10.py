# -*- coding: utf-8 -*-
# _rel_ai_10.py  卷十 人物关系层源数据
# 字段: item_id / person_a / person_b / relation_type / evidence

RECORDS = [
    # ===== 10-001 官军粮赏则例（含议谥二则） =====
    {
        "item_id": "10-001",
        "person_a": "京兆公",
        "person_b": "陈遇",
        "relation_type": "举荐",
        "evidence": "京兆公举陈遇等应谥，骆公骎酌而疏请下部。",
    },
    {
        "item_id": "10-001",
        "person_a": "骆骎",
        "person_b": "顾璘",
        "relation_type": "疏请",
        "evidence": "部使者骆公骎酌顾璘诸公上疏请谥。",
    },
    # ===== 10-005 宁国公主墨杯 =====
    {
        "item_id": "10-005",
        "person_a": "宁国公主",
        "person_b": "梅殷",
        "relation_type": "夫妻",
        "evidence": "太祖十六女宁国公主下嫁梅殷，遗墨与酒杯世藏梅氏家。",
    },
    # ===== 10-006 文士二则 =====
    {
        "item_id": "10-006",
        "person_a": "顾起元",
        "person_b": "李佺",
        "relation_type": "序集",
        "evidence": "顾起元尝为李象先诗集作序，颇极推挹。",
    },
    {
        "item_id": "10-006",
        "person_a": "顾起元",
        "person_b": "胡宗仁",
        "relation_type": "序集",
        "evidence": "顾起元序胡彭举《知载斋稿》板而行之。",
    },
    {
        "item_id": "10-006",
        "person_a": "周晖",
        "person_b": "胡宗仁",
        "relation_type": "品评",
        "evidence": "周吉甫称胡诗句中有画类王右丞。",
    },
    {
        "item_id": "10-006",
        "person_a": "叶遵",
        "person_b": "焦竑",
        "relation_type": "校讐",
        "evidence": "焦弱侯《升庵外集》校讐编次皆叶循甫笔。",
    },
    # ===== 10-007 书法 =====
    {
        "item_id": "10-007",
        "person_a": "顾起元",
        "person_b": "黄复儒",
        "relation_type": "戏谑评书",
        "evidence": "顾起元戏谓黄叔遁举体充悦当号笨伯而作字秀羸。",
    },
    # ===== 10-009 王梅溪研 =====
    {
        "item_id": "10-009",
        "person_a": "盛时泰",
        "person_b": "盛敏耕",
        "relation_type": "父子",
        "evidence": "王梅溪研藏于盛仲交，后其子伯年尝以见示。",
    },
    {
        "item_id": "10-009",
        "person_a": "盛时泰",
        "person_b": "顾起元",
        "relation_type": "交游",
        "evidence": "顾起元亲见苍润轩中王梅溪研之藏。",
    },
    # ===== 10-013 两谢公墩 =====
    {
        "item_id": "10-013",
        "person_a": "谢安",
        "person_b": "王羲之",
        "relation_type": "同游",
        "evidence": "谢安石与王羲之登冶城西园，有悠然远想之谈。",
    },
    {
        "item_id": "10-013",
        "person_a": "谢玄",
        "person_b": "谢灵运",
        "relation_type": "祖孙",
        "evidence": "半山寺后谢公墩为谢玄与其兄子灵运所居。",
    },
    {
        "item_id": "10-013",
        "person_a": "王安石",
        "person_b": "谢安",
        "relation_type": "误认古迹（诗咏）",
        "evidence": "荆公“我屋公墩”之诗误以太傅当半山之墩。",
    },
    # ===== 10-017 东坡先生金陵诗 =====
    {
        "item_id": "10-017",
        "person_a": "苏轼",
        "person_b": "王安石",
        "relation_type": "诗酬",
        "evidence": "东坡次荆公韵四绝句。",
    },
    {
        "item_id": "10-017",
        "person_a": "苏轼",
        "person_b": "王胜之",
        "relation_type": "同游",
        "evidence": "东坡同王胜之游蒋山。",
    },
    {
        "item_id": "10-017",
        "person_a": "苏轼",
        "person_b": "苏遁",
        "relation_type": "父子",
        "evidence": "小子遁病亡，东坡作二诗哭之。",
    },
    # ===== 10-019 八功德水 =====
    {
        "item_id": "10-019",
        "person_a": "昙隐",
        "person_b": "山龙",
        "relation_type": "授水",
        "evidence": "山龙自陈知师渴，指功德池饮之，语毕人与口灭，一沼沸成。",
    },
    # ===== 10-020 沿江开河议 =====
    {
        "item_id": "10-020",
        "person_a": "卢公",
        "person_b": "李思聪",
        "relation_type": "同论开河",
        "evidence": "宋卢公访古漕河以避江险，与明李君思聪开内河之议先后相合。",
    },
    # ===== 10-028 幕府直渎诸山 =====
    {
        "item_id": "10-028",
        "person_a": "王导",
        "person_b": "晋元帝",
        "relation_type": "君臣建幕府",
        "evidence": "晋元帝渡江，王导建幕府于山，因名幕府山。",
    },
    {
        "item_id": "10-028",
        "person_a": "孙皓",
        "person_b": "竺瑶",
        "relation_type": "凿墓（相恶）",
        "evidence": "吴将竺瑶墓有王气，孙皓恶之凿其后为直渎。",
    },
    # ===== 10-032 王荆公疏湖田 =====
    {
        "item_id": "10-032",
        "person_a": "王安石",
        "person_b": "赵善湘",
        "relation_type": "后任增租（良法之弊）",
        "evidence": "荆公疏湖田岁收水面钱，绍兴二年赵善湘增收田租遂以为例。",
    },
    # ===== 10-036 中书左丞一人 =====
    {
        "item_id": "10-036",
        "person_a": "杨宪",
        "person_b": "陈轻",
        "relation_type": "擢拔",
        "evidence": "陈轻解一统山河花押之意，杨宪大喜即擢轻为编修。",
    },
    # ===== 10-042 移囚 =====
    {
        "item_id": "10-042",
        "person_a": "庞嵩",
        "person_b": "南京刑部",
        "relation_type": "建言",
        "evidence": "庞嵩郎中建议增筑湖北岸城以护法司与陵寝。",
    },
    # ===== 10-043 国初榜文 =====
    {
        "item_id": "10-043",
        "person_a": "虞让",
        "person_b": "虞端",
        "relation_type": "父子",
        "evidence": "府军卫千户虞让男虞端故违禁令吹箫唱曲被割唇鼻。",
    },
    {
        "item_id": "10-043",
        "person_a": "伏颙",
        "person_b": "姚晏保",
        "relation_type": "同罪受罚",
        "evidence": "龙江卫指挥伏颙与小旗姚晏保蹴圆卸脚全家发云南。",
    },
    # ===== 10-045 前乙酉举人见后乙酉 =====
    {
        "item_id": "10-045",
        "person_a": "石城先生",
        "person_b": "万历乙酉举人",
        "relation_type": "谒见",
        "evidence": "万历乙酉中式举人谒先生，时年八十余，方矍铄无老态。",
    },
]
