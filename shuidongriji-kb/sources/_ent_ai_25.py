# -*- coding: utf-8 -*-
"""《水东日记》卷 25 —— L1 实体标注 源数据（AI 判定逐条填写）

覆盖条目：25-001~25-029（共 29 条）。
"""

ITEM_LIST = [
    "25-001 | 歌风台诗多矣宋张安道云",
    "25-002 | 下诗曰",
    "25-003 | 蔡京以章惇入相",
    "25-004 | 太清楼特晏记",
    "25-005 | 为君难为臣不易尚矣",
    "25-006 | 右一",
    "25-007 | 右二",
    "25-008 | 右二",
    "25-009 | 奋于百世之下",
    "25-010 | 政和甲午六月朔日记",
    "25-011 | 翰林书艺局镌字艺学臣严竒",
    "25-012 | 睿思殿御前文字外库镌字艺学臣徐珣",
    "25-013 | 臣张士亨",
    "25-014 | 待诏臣朱章",
    "25-015 | 臣邢肃",
    "25-016 | 臣张仲文",
    "25-017 | 书待诏臣王公琬待诏赐绯臣倪士宣",
    "25-018 | 臣封士宁",
    "25-019 | 从义郎臣张士永模刊",
    "25-020 | 胡忠安公尝属先公遗事卷",
    "25-021 | 清江俞行之在永乐中有能诗盛名",
    "25-022 | 文衡之任亦难矣",
    "25-023 | 欧阳公丰乐亭记",
    "25-024 | 毘陵谢子兰氏辨惑编",
    "25-025 | 四明袁桷伯长元翰林大手笔也",
    "25-026 | 颇记一纪闻云文丞相一子",
    "25-027 | 苏天爵为右司都事时所类元诗文名曰国朝文类",
    "25-028 | 宋元祐中防师雄为陕府转运判官",
    "25-029 | 左坟制故事起冢象铁山积石山",
]

DATA = [
    # ---- 25-001 歌风台诗评 ----
    {"id": "ENT-12501", "item_id": "25-001", "text": "歌风台", "type": "place", "start": 0, "end": 0, "normalized": "歌风台", "confidence": 0.9, "source": "歌风台诗多矣"},
    {"id": "ENT-12502", "item_id": "25-001", "text": "张安道", "type": "person", "start": 0, "end": 0, "normalized": "张方平（字安道）", "confidence": 0.9, "source": "宋张安道"},
    {"id": "ENT-12503", "item_id": "25-001", "text": "张光弼", "type": "person", "start": 0, "end": 0, "normalized": "张光弼", "confidence": 0.85, "source": "近时张光弼"},
    {"id": "ENT-12504", "item_id": "25-001", "text": "刘郎", "type": "person", "start": 0, "end": 0, "normalized": "刘邦（汉高祖）", "confidence": 0.85, "source": "落魄刘郎作帝归"},
    {"id": "ENT-12505", "item_id": "25-001", "text": "信越", "type": "person", "start": 0, "end": 0, "normalized": "韩信、彭越", "confidence": 0.85, "source": "才如信越犹葅醢"},
    # ---- 25-003 蔡京论 ----
    {"id": "ENT-12506", "item_id": "25-003", "text": "蔡京", "type": "person", "start": 0, "end": 0, "normalized": "蔡京", "confidence": 0.95, "source": "蔡京以章惇入相"},
    {"id": "ENT-12507", "item_id": "25-003", "text": "章惇", "type": "person", "start": 0, "end": 0, "normalized": "章惇", "confidence": 0.9, "source": "以章惇入相"},
    {"id": "ENT-12508", "item_id": "25-003", "text": "蔡卞", "type": "person", "start": 0, "end": 0, "normalized": "蔡卞", "confidence": 0.88, "source": "卞等左右之"},
    {"id": "ENT-12509", "item_id": "25-003", "text": "王觌", "type": "person", "start": 0, "end": 0, "normalized": "王觌", "confidence": 0.88, "source": "善乎王觌之言曰"},
    {"id": "ENT-12510", "item_id": "25-003", "text": "常安民", "type": "person", "start": 0, "end": 0, "normalized": "常安民", "confidence": 0.88, "source": "莫切乎常安民之言曰"},
    {"id": "ENT-12511", "item_id": "25-003", "text": "徽宗", "type": "person", "start": 0, "end": 0, "normalized": "宋徽宗", "confidence": 0.92, "source": "如徽宗者"},
    {"id": "ENT-12512", "item_id": "25-003", "text": "绍圣", "type": "era", "start": 0, "end": 0, "normalized": "绍圣", "confidence": 0.9, "source": "绍圣元年"},
    {"id": "ENT-12513", "item_id": "25-003", "text": "靖康", "type": "era", "start": 0, "end": 0, "normalized": "靖康", "confidence": 0.9, "source": "靖康元年"},
    {"id": "ENT-12514", "item_id": "25-003", "text": "政和", "type": "era", "start": 0, "end": 0, "normalized": "政和", "confidence": 0.9, "source": "政和壬辰"},
    {"id": "ENT-12515", "item_id": "25-003", "text": "太清楼特宴记", "type": "work", "start": 0, "end": 0, "normalized": "太清楼特宴记", "confidence": 0.9, "source": "徽宗亲书太清楼特宴记"},
    {"id": "ENT-12516", "item_id": "25-003", "text": "开封府学", "type": "place", "start": 0, "end": 0, "normalized": "开封府学", "confidence": 0.85, "source": "多在今开封府学墙壁间"},
    # ---- 25-005~019 太清楼特宴记（徽宗文+题衔） ----
    {"id": "ENT-12517", "item_id": "25-005", "text": "王安石", "type": "person", "start": 0, "end": 0, "normalized": "王安石", "confidence": 0.92, "source": "追述三代相王安石"},
    {"id": "ENT-12518", "item_id": "25-007", "text": "蔡鞗", "type": "person", "start": 0, "end": 0, "normalized": "蔡鞗（京子）", "confidence": 0.85, "source": "许其子鞗尚朕女"},
    {"id": "ENT-12519", "item_id": "25-011", "text": "翰林书艺局", "type": "institution", "start": 0, "end": 0, "normalized": "翰林书艺局", "confidence": 0.85, "source": "翰林书艺局镌字艺学"},
    {"id": "ENT-12520", "item_id": "25-012", "text": "睿思殿御前文字外库", "type": "institution", "start": 0, "end": 0, "normalized": "睿思殿御前文字外库", "confidence": 0.85, "source": "睿思殿御前文字外库"},
    {"id": "ENT-12521", "item_id": "25-019", "text": "梁师成", "type": "person", "start": 0, "end": 0, "normalized": "梁师成", "confidence": 0.85, "source": "通侍大夫臣梁师成"},
    # ---- 25-020 胡忠安公图书 ----
    {"id": "ENT-12522", "item_id": "25-020", "text": "胡忠安公", "type": "person", "start": 0, "end": 0, "normalized": "胡濙（谥忠安）", "confidence": 0.92, "source": "胡忠安公"},
    {"id": "ENT-12523", "item_id": "25-020", "text": "蹇公", "type": "person", "start": 0, "end": 0, "normalized": "蹇义（谥忠定）", "confidence": 0.85, "source": "蜀蹇公"},
    {"id": "ENT-12524", "item_id": "25-020", "text": "夏忠靖", "type": "person", "start": 0, "end": 0, "normalized": "夏原吉（谥忠靖）", "confidence": 0.88, "source": "夏忠靖"},
    {"id": "ENT-12525", "item_id": "25-020", "text": "吴少师", "type": "person", "start": 0, "end": 0, "normalized": "吴少师", "confidence": 0.8, "source": "吴少师则和敏详达"},
    {"id": "ENT-12526", "item_id": "25-020", "text": "夏仲昭", "type": "person", "start": 0, "end": 0, "normalized": "夏昶（字仲昭）", "confidence": 0.82, "source": "夏主事仲昭"},
    # ---- 25-021 俞行之诗 ----
    {"id": "ENT-12527", "item_id": "25-021", "text": "俞行之", "type": "person", "start": 0, "end": 0, "normalized": "俞行之（清江）", "confidence": 0.85, "source": "清江俞行之"},
    {"id": "ENT-12528", "item_id": "25-021", "text": "顾师颜", "type": "person", "start": 0, "end": 0, "normalized": "顾师颜", "confidence": 0.82, "source": "题顾师颜西湖画"},
    # ---- 25-022 文衡 ----
    {"id": "ENT-12529", "item_id": "25-022", "text": "王抑庵", "type": "person", "start": 0, "end": 0, "normalized": "王直（号抑庵）", "confidence": 0.9, "source": "王抑庵先生主考"},
    {"id": "ENT-12530", "item_id": "25-022", "text": "张穆", "type": "person", "start": 0, "end": 0, "normalized": "张穆", "confidence": 0.85, "source": "第二名张穆兵马策"},
    {"id": "ENT-12531", "item_id": "25-022", "text": "宁王", "type": "person", "start": 0, "end": 0, "normalized": "宁王", "confidence": 0.8, "source": "前序尝为宁王所许"},
    # ---- 25-023 欧阳公 ----
    {"id": "ENT-12532", "item_id": "25-023", "text": "欧阳公", "type": "person", "start": 0, "end": 0, "normalized": "欧阳修", "confidence": 0.92, "source": "欧阳公丰乐亭记"},
    {"id": "ENT-12533", "item_id": "25-023", "text": "白乐天", "type": "person", "start": 0, "end": 0, "normalized": "白居易", "confidence": 0.92, "source": "用白乐天庐山草堂记"},
    {"id": "ENT-12534", "item_id": "25-023", "text": "张子野", "type": "person", "start": 0, "end": 0, "normalized": "张先（字子野）", "confidence": 0.88, "source": "张子野云破月来花弄影"},
    {"id": "ENT-12535", "item_id": "25-023", "text": "丰乐亭记", "type": "work", "start": 0, "end": 0, "normalized": "丰乐亭记", "confidence": 0.9, "source": "丰乐亭记"},
    # ---- 25-024 谢子兰辨惑编 ----
    {"id": "ENT-12536", "item_id": "25-024", "text": "谢子兰", "type": "person", "start": 0, "end": 0, "normalized": "谢子兰（毘陵）", "confidence": 0.85, "source": "毘陵谢子兰氏辨惑编"},
    {"id": "ENT-12537", "item_id": "25-024", "text": "辨惑编", "type": "work", "start": 0, "end": 0, "normalized": "辨惑编", "confidence": 0.9, "source": "辨惑编一书"},
    # ---- 25-025 袁桷 ----
    {"id": "ENT-12538", "item_id": "25-025", "text": "袁桷", "type": "person", "start": 0, "end": 0, "normalized": "袁桷（字伯长，号清容）", "confidence": 0.92, "source": "四明袁桷伯长"},
    {"id": "ENT-12539", "item_id": "25-025", "text": "虞文靖公", "type": "person", "start": 0, "end": 0, "normalized": "虞集", "confidence": 0.9, "source": "虞文靖公与伯长最厚"},
    {"id": "ENT-12540", "item_id": "25-025", "text": "元明善", "type": "person", "start": 0, "end": 0, "normalized": "元明善", "confidence": 0.85, "source": "乃元明善之文"},
    {"id": "ENT-12541", "item_id": "25-025", "text": "袁忠彻", "type": "person", "start": 0, "end": 0, "normalized": "袁忠彻", "confidence": 0.82, "source": "袁忠彻家进士忠义录"},
    # ---- 25-026 文丞相子 ----
    {"id": "ENT-12542", "item_id": "25-026", "text": "文丞相", "type": "person", "start": 0, "end": 0, "normalized": "文天祥", "confidence": 0.95, "source": "文丞相一子"},
    {"id": "ENT-12543", "item_id": "25-026", "text": "文陞", "type": "person", "start": 0, "end": 0, "normalized": "文陞（文丞相子）", "confidence": 0.85, "source": "丞相之子即元仁宗皇庆中集贤直学士陞"},
    # ---- 25-027 国朝文类 ----
    {"id": "ENT-12544", "item_id": "25-027", "text": "苏天爵", "type": "person", "start": 0, "end": 0, "normalized": "苏天爵", "confidence": 0.92, "source": "苏天爵为右司都事"},
    {"id": "ENT-12545", "item_id": "25-027", "text": "国朝文类", "type": "work", "start": 0, "end": 0, "normalized": "国朝文类", "confidence": 0.92, "source": "所类元诗文名曰国朝文类"},
    {"id": "ENT-12546", "item_id": "25-027", "text": "姚牧庵", "type": "person", "start": 0, "end": 0, "normalized": "姚燧（号牧庵）", "confidence": 0.88, "source": "姚牧庵"},
    {"id": "ENT-12547", "item_id": "25-027", "text": "马祖常", "type": "person", "start": 0, "end": 0, "normalized": "马祖常", "confidence": 0.85, "source": "马祖常"},
    {"id": "ENT-12548", "item_id": "25-027", "text": "元好问", "type": "person", "start": 0, "end": 0, "normalized": "元好问", "confidence": 0.88, "source": "元好问"},
    {"id": "ENT-12549", "item_id": "25-027", "text": "陈旅", "type": "person", "start": 0, "end": 0, "normalized": "陈旅", "confidence": 0.82, "source": "有陈旅序"},
    {"id": "ENT-12550", "item_id": "25-027", "text": "吴思庵", "type": "person", "start": 0, "end": 0, "normalized": "吴思庵", "confidence": 0.85, "source": "吴思庵惩乡人伪作"},
    # ---- 25-028~029 唐二公坟 ----
    {"id": "ENT-12551", "item_id": "25-028", "text": "防师雄", "type": "person", "start": 0, "end": 0, "normalized": "防师雄", "confidence": 0.82, "source": "防师雄为陕府转运判官"},
    {"id": "ENT-12552", "item_id": "25-028", "text": "李英公", "type": "person", "start": 0, "end": 0, "normalized": "李勣（封英国公）", "confidence": 0.88, "source": "唐李英卫二公坟"},
    {"id": "ENT-12553", "item_id": "25-028", "text": "卫公", "type": "person", "start": 0, "end": 0, "normalized": "李靖（封卫国公）", "confidence": 0.88, "source": "卫公云赠司徒并州都督"},
    {"id": "ENT-12554", "item_id": "25-029", "text": "昭陵", "type": "place", "start": 0, "end": 0, "normalized": "昭陵（唐太宗陵）", "confidence": 0.9, "source": "陪葬昭陵"},
    {"id": "ENT-12555", "item_id": "25-029", "text": "韩世忠", "type": "person", "start": 0, "end": 0, "normalized": "韩世忠", "confidence": 0.88, "source": "姑苏灵岩山下韩世忠墓"},
    {"id": "ENT-12556", "item_id": "25-029", "text": "钱武肃", "type": "person", "start": 0, "end": 0, "normalized": "钱镠（谥武肃）", "confidence": 0.9, "source": "吴思庵题钱武肃画像卷"},
    {"id": "ENT-12557", "item_id": "25-029", "text": "钱惟演", "type": "person", "start": 0, "end": 0, "normalized": "钱惟演", "confidence": 0.82, "source": "彭城郡公惟演"},
    {"id": "ENT-12558", "item_id": "25-029", "text": "太祖高皇帝", "type": "person", "start": 0, "end": 0, "normalized": "明太祖朱元璋", "confidence": 0.92, "source": "我太祖高皇帝"},
    {"id": "ENT-12559", "item_id": "25-029", "text": "寰宇通志", "type": "work", "start": 0, "end": 0, "normalized": "寰宇通志", "confidence": 0.92, "source": "初修寰宇通志"},
    {"id": "ENT-12560", "item_id": "25-029", "text": "祝穆", "type": "person", "start": 0, "end": 0, "normalized": "祝穆", "confidence": 0.85, "source": "一准祝穆方舆胜览"},
    {"id": "ENT-12561", "item_id": "25-029", "text": "方舆胜览", "type": "work", "start": 0, "end": 0, "normalized": "方舆胜览", "confidence": 0.9, "source": "祝穆方舆胜览"},
]
# 缺口登记：25-013~018 碑刻题衔（张士亨/朱章/邢肃/张仲文/倪士宣/封士宁等）为碑工，不单列。
