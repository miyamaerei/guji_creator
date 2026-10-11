# -*- coding: utf-8 -*-
"""《水东日记》卷 02 —— REL 人物关系 源数据（AI 判定逐条填写）

说明：关系记录：person_a/person_b(含各自 ent_ids)/relation_type/direction(单向/双向/未明)/evidence；只建文本有直接证据的关系，宁缺毋滥
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "02-001 | 景泰元年太上皇万寿圣节礼部请羣臣朝诏免朝二年盛与季聪约当草疏",
    "02-002 | 居庸以北俗择塟地以验蛇盘兎为上昌平侯杨洪赤城塟母处亦然意者地",
    "02-003 | 景泰二年予为殿试弥封官知读卷事第一甲盖閤老预属意于受卷官已得",
    "02-004 | 独石城堡今治开平卫初阳武侯薛禄奏筑城迁卫于此有僧庆西堂者号精",
    "02-005 | 尹鳯岐先生在翰林好作诗讽切时事节之最能记予仅记其一首时应诏举",
    "02-006 | 真定逻卒获一人为敌语甚习以为先被掳见留敌酋额森将窥临清使我等",
    "02-007 | 【阙】　　　　　　　以贸易习敌语不事作业被捶楚潜匿于外妄为此",
    "02-008 | 吴思庵先生谈及浅学后进曰此韵府羣玉秀才好趁航船尔航船吴中所谓",
    "02-009 | 弋谦代州人累任显官有声仁庙时歳己巳布衣走阙下疏前成山侯王通龙",
    "02-010 | 古人制作名集编次多出于己各有深意存焉或身后出于门生故吏子孙学",
    "02-011 | 景泰二年冬文渊阁办事中书舍人何观言大臣旧老少保兼吏部尚书王直",
    "02-012 | 祭酒安成李先生初以言事得罪系狱宣庙登极后一日御别殿以其激怒先",
    "02-013 | 景泰元年八月十一日朝退禁门侧尚书胡公手一揭帖文武重臣羣立传观",
    "02-014 | 南都数年前一时人物之盛勲旧之贤如襄城伯李公通材重望如少保黄公",
    "02-015 | 题秋胡图诗二首其一曰郎恩叶薄妾氷清郎说黄金妾不譍若使偶然通一",
]

# 字段键（打包器校验用）：rel_id, item_id, person_a, person_b, relation_type, direction, evidence, confidence
DATA = [
    # ---- 02-001 叶盛与季聪议疏 ----
    {"rel_id": "REL-1001", "item_id": "02-001",
     "person_a": {"text": "叶盛", "person_a_ent_ids": []},
     "person_b": {"text": "季聪", "person_b_ent_ids": []},
     "relation_type": "同僚", "direction": "双向",
     "evidence": "二年盛与季聪约当草疏偕科道与礼部同上",
     "confidence": 0.9},
    # ---- 02-002 于节庵为董镛婿 ----
    {"rel_id": "REL-1002", "item_id": "02-002",
     "person_a": {"text": "于节庵", "person_a_ent_ids": []},
     "person_b": {"text": "董镛", "person_b_ent_ids": []},
     "relation_type": "姻亲", "direction": "双向",
     "evidence": "节庵既长为董镛先生壻先生藏书有元黄文献公溍集",
     "confidence": 0.85},
    # ---- 02-008 季聪劾善增 ----
    {"rel_id": "REL-1003", "item_id": "02-008",
     "person_a": {"text": "季聪", "person_a_ent_ids": []},
     "person_b": {"text": "善增（内官）", "person_b_ent_ids": []},
     "relation_type": "弹劾", "direction": "单向",
     "evidence": "季聪偕六科十三道上言尽暴其罪恶乞急治之",
     "confidence": 0.88},
    # ---- 02-009 弋谦举荐王通 ----
    {"rel_id": "REL-1004", "item_id": "02-009",
     "person_a": {"text": "弋谦", "person_a_ent_ids": []},
     "person_b": {"text": "王通", "person_b_ent_ids": []},
     "relation_type": "举荐", "direction": "单向",
     "evidence": "谦则力言宜专用通众导之再四",
     "confidence": 0.82},
    {"rel_id": "REL-1005", "item_id": "02-009",
     "person_a": {"text": "石亨", "person_a_ent_ids": []},
     "person_b": {"text": "于谦", "person_b_ent_ids": []},
     "relation_type": "同僚", "direction": "双向",
     "evidence": "石亨为时倚重偕于尚书治兵土城外",
     "confidence": 0.85},
    # ---- 02-011 何观劾王直等 ----
    {"rel_id": "REL-1006", "item_id": "02-011",
     "person_a": {"text": "何观", "person_a_ent_ids": []},
     "person_b": {"text": "王直", "person_b_ent_ids": []},
     "relation_type": "弹劾", "direction": "单向",
     "evidence": "言大臣旧老少保兼吏部尚书王直等正统中皆阿附权奸今此辈老猾不宜在左右",
     "confidence": 0.85},
    {"rel_id": "REL-1007", "item_id": "02-011",
     "person_a": {"text": "叶盛", "person_a_ent_ids": []},
     "person_b": {"text": "毛玉", "person_b_ent_ids": []},
     "relation_type": "同僚", "direction": "双向",
     "evidence": "玉素于盛厚因附耳喻此意……盛因抹去冒头",
     "confidence": 0.85},
    # ---- 02-012 解缙与胡祭酒契好 ----
    {"rel_id": "REL-1008", "item_id": "02-012",
     "person_a": {"text": "解缙", "person_a_ent_ids": []},
     "person_b": {"text": "胡祭酒", "person_b_ent_ids": []},
     "relation_type": "同僚", "direction": "双向",
     "evidence": "解学士胡祭酒契好甚密一日同观放进士榜",
     "confidence": 0.85},
    # ---- 02-013 王文与于谦持两端 ----
    {"rel_id": "REL-1009", "item_id": "02-013",
     "person_a": {"text": "王文", "person_a_ent_ids": []},
     "person_b": {"text": "于谦", "person_b_ent_ids": []},
     "relation_type": "其他", "direction": "单向",
     "evidence": "都御史王文曰匿名文书不得言……以告于少保第言使封进亦无妨盖其意亦持两端",
     "confidence": 0.78},
    {"rel_id": "REL-1010", "item_id": "02-013",
     "person_a": {"text": "胡濙", "person_a_ent_ids": []},
     "person_b": {"text": "王直", "person_b_ent_ids": []},
     "relation_type": "其他", "direction": "单向",
     "evidence": "王公有忧色曰诸公勿累小子吃牢饭也两人之量不同如此",
     "confidence": 0.78},
    # 缺口登记：其余条目人物间或无直接文本证据（推测不建），如
    # 02-004 杨洪与都御史李公、02-005 尹鳯岐与鸿胪杨公，均属泛记，不强行建关系。
]
