# -*- coding: utf-8 -*-
"""《平平言》规则源数据（卷01 全量）——AI 判定装填。
C4：type 中文键（RULE_TYPES 7 值）；modals 中文模态；subject/action/object 解读字段。
一条规范句一单元；说理句/亲历句不抽规则。"""

RECORDS = [
    # 01-002 造孽莫如州縣
    {"item_id": "01-002", "type": "禁止型", "subject": "如有命作州縣者", "action": "萬不可造孽", "modals": ["禁止", "不可"], "condition": "凡為州縣", "object": "百姓", "purpose": "免得來世變畜類", "punishment": "", "confidence": "high"},
    # 01-025 各房呈須知冊
    {"item_id": "01-025", "type": "程序型", "subject": "各房書吏", "action": "各造須知冊呈送本官", "modals": ["应该", "可以", "不得"], "condition": "新任到任之日", "object": "須知冊", "purpose": "凡地方情形利弊本官得以周知", "punishment": "", "confidence": "high"},
    # 01-026 清查前任命盜各案
    {"item_id": "01-026", "type": "程序型", "subject": "新任州縣", "action": "清查前任任內未結命盜各案，照例嚴定審限參限", "modals": ["必须", "应该"], "condition": "到任之後", "object": "命盜各案", "purpose": "恐前官廢弛，新任受其牽累", "punishment": "", "confidence": "high"},
    # 01-032 公罪私罪
    {"item_id": "01-032", "type": "禁止型", "subject": "官員", "action": "私罪必不可有", "modals": ["禁止"], "condition": "公罪尚可容，私罪不可", "object": "私罪", "purpose": "名節所關", "punishment": "雖有級紀不准抵銷", "confidence": "high"},
    # 01-033 大計
    {"item_id": "01-033", "type": "程序型", "subject": "三年大計", "action": "舉以卓異、劾以六法，平等以守政才年四格註考", "modals": ["必须"], "condition": "每三年一举", "object": "州縣以上各員", "purpose": "考課官員", "punishment": "", "confidence": "high"},
    {"item_id": "01-033", "type": "禁止型", "subject": "入六法之員", "action": "加級紀錄不准抵銷", "modals": ["不得"], "condition": "不謹罷輭俱革職、年老有疾俱休致、才力不及降二級調用、浮躁降三級調用", "object": "加級紀錄", "purpose": "懲處劣員", "punishment": "革職/休致/降級調用", "confidence": "high"},
    # 01-035 事不可入廟門者斷不可為
    {"item_id": "01-035", "type": "禁止型", "subject": "為吏者", "action": "發念之端不可以入廟門者斷不可為", "modals": ["禁止"], "condition": "勢會所乘容有不得不為之事，但發念近公方可告神明", "object": "", "purpose": "不愧不怍衾影無慚", "punishment": "", "confidence": "high"},
    # 01-036 官不可貪
    {"item_id": "01-036", "type": "禁止型", "subject": "官", "action": "不可貪", "modals": ["禁止"], "condition": "", "object": "賄賂", "purpose": "六因：壞心術/敗風俗/損聲名/干國法/辱祖宗/毒子孫", "punishment": "干國法者計贓定罪", "confidence": "high"},
    # 01-039 官不可與民爭利（正文=義利關論）
    {"item_id": "01-039", "type": "禁止型", "subject": "官", "action": "不可與民爭利", "modals": ["禁止"], "condition": "", "object": "地利", "purpose": "義利之關", "punishment": "參劾革職", "confidence": "high"},
    {"item_id": "01-039", "type": "禁止型", "subject": "自愛者", "action": "當視義利關如酖毒入口即死，萬萬不可嘗試", "modals": ["禁止"], "condition": "義利關乃人鬼界", "object": "不義之利", "purpose": "久則只知有利不知有害", "punishment": "", "confidence": "high"},
    # 01-040 義利關乃人鬼界（正文=官不可與民爭利崇陽案 + 律載）
    {"item_id": "01-040", "type": "程序型", "subject": "官私地內掘得埋藏無主之物", "action": "惟骨董鐘鼎符印等項限三十日內送官，其餘常物聽民收用", "modals": ["必须", "时限"], "condition": "律載", "object": "埋藏之物", "purpose": "異常之物非民間所宜有", "punishment": "", "confidence": "high"},
    # 01-043 官民交財
    {"item_id": "01-043", "type": "义务型", "subject": "署中所需", "action": "一切須用現銀現錢照時價平買", "modals": ["必须"], "condition": "官與民交財乃官聲所繫", "object": "鋪戶", "purpose": "官聲", "punishment": "", "confidence": "high"},
    {"item_id": "01-043", "type": "程序型", "subject": "到任之初", "action": "須大張告示曉諭各鋪戶；如官親家丁買辦恃強賒取或短發價值行使低銀，准該鋪戶據實扭稟", "modals": ["必须"], "condition": "", "object": "各鋪戶", "purpose": "防官親家丁擾民", "punishment": "據實扭稟", "confidence": "high"},
    # 01-044 官價
    {"item_id": "01-044", "type": "程序型", "subject": "到任之初", "action": "須合進項出項通盤計算", "modals": ["必须"], "condition": "官價最為累民", "object": "官價", "purpose": "定官價裁革與否", "punishment": "", "confidence": "high"},
    {"item_id": "01-044", "type": "义务型", "subject": "官價", "action": "入不敷出則姑仍舊貫，特不可漫無限制縱容家丁人等任意取索", "modals": ["宜", "不可"], "condition": "如入數出數不甚懸殊則官價必應裁革", "object": "官價", "purpose": "累民與公費兩全", "punishment": "", "confidence": "high"},
    # 01-045 陋規
    {"item_id": "01-045", "type": "禁止型", "subject": "前官已裁之陋規", "action": "無論應裁不應裁，萬不可自我復舊", "modals": ["禁止"], "condition": "", "object": "陋規", "purpose": "", "punishment": "", "confidence": "high"},
    {"item_id": "01-045", "type": "禁止型", "subject": "前官未有之陋規", "action": "無論可得不可得，萬不可自我作俑", "modals": ["禁止"], "condition": "", "object": "陋規", "purpose": "", "punishment": "", "confidence": "high"},
    {"item_id": "01-045", "type": "禁止型", "subject": "陋規出之民者或牽涉訟案者", "action": "如命案夫馬錢兩造出結錢代書戳記錢坐堂禮之類，分毫不可收受", "modals": ["禁止"], "condition": "劉簾舫觀察之說", "object": "陋規", "purpose": "", "punishment": "", "confidence": "high"},
    {"item_id": "01-045", "type": "禁止型", "subject": "管理錢局之鑪頭人等所出陋規", "action": "關係錢法，亦必不可收受", "modals": ["禁止"], "condition": "", "object": "陋規", "purpose": "錢法", "punishment": "", "confidence": "high"},
    # 01-046 革陋規非易事
    {"item_id": "01-046", "type": "程序型", "subject": "官欲革陋規", "action": "不可令一人知之，密速行之", "modals": ["不可", "必须"], "condition": "恐棍蠹聞之索詐撞騙", "object": "陋規", "purpose": "防棍蠹撞騙", "punishment": "", "confidence": "high"},
    # 01-050 儉非吝嗇
    {"item_id": "01-050", "type": "义务型", "subject": "當官處事", "action": "搶險救火拏要犯辦大差之類均不可惜費", "modals": ["不可"], "condition": "不可省而省謂之吝嗇", "object": "公費", "purpose": "惜費則誤事", "punishment": "", "confidence": "high"},
    # 01-051 清慎勤
    {"item_id": "01-051", "type": "义务型", "subject": "居官者", "action": "以清慎勤三字為訣，清為第一義", "modals": ["必须"], "condition": "廉而不慎多疏略、廉而不勤政廢弛", "object": "", "purpose": "好官", "punishment": "", "confidence": "high"},
    # 01-053 官不可不明
    {"item_id": "01-053", "type": "义务型", "subject": "官", "action": "不可不明", "modals": ["必须"], "condition": "清慎勤之外尚有一明字", "object": "事理", "purpose": "廉而不明有人從中要錢、慎而不明當斷不斷、勤而不明徒勞罔益", "punishment": "", "confidence": "high"},
    # 01-055 官不可過用其明
    {"item_id": "01-055", "type": "禁止型", "subject": "官", "action": "不可過用其明", "modals": ["禁止"], "condition": "過用其明則下不能堪", "object": "", "purpose": "其政察察其民缺缺", "punishment": "", "confidence": "high"},
    # 01-057 緩
    {"item_id": "01-057", "type": "义务型", "subject": "當官者", "action": "先以暴怒為戒，事有不可當詳處之", "modals": ["必须", "宜"], "condition": "", "object": "", "purpose": "世間事多因忙後錯", "punishment": "", "confidence": "high"},
    # 01-058 勿喜事
    {"item_id": "01-058", "type": "禁止型", "subject": "為政", "action": "勿喜事：在省事不在多事、在守法不在變法、在安靜不在紛擾、在寬簡不在煩苛", "modals": ["禁止"], "condition": "非廢弛之謂", "object": "", "purpose": "寬者不為苛急、簡者不為繁碎", "punishment": "", "confidence": "high"},
    # 01-059 熱腸
    {"item_id": "01-059", "type": "禁止型", "subject": "富貴利達", "action": "眼不可熱", "modals": ["不可"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    {"item_id": "01-059", "type": "义务型", "subject": "民生休戚", "action": "腸不可不熱", "modals": ["必须"], "condition": "", "object": "百姓", "purpose": "腸不熱則百姓休戚如秦越肥瘠", "punishment": "", "confidence": "high"},
    # 01-060 擔當
    {"item_id": "01-060", "type": "义务型", "subject": "辦大事者", "action": "須有擔當，須將功名置於度外", "modals": ["必须"], "condition": "", "object": "", "purpose": "無擔當必至誤事；不置功名度外必不肯擔當", "punishment": "", "confidence": "high"},
    # 01-062 成見
    {"item_id": "01-062", "type": "禁止型", "subject": "當官處事", "action": "不可預存成見", "modals": ["禁止"], "condition": "平者輕重適中", "object": "", "purpose": "心有成見則畸輕畸重", "punishment": "", "confidence": "high"},
    # 01-063 有條理
    {"item_id": "01-063", "type": "义务型", "subject": "事不論大小", "action": "總要有條理", "modals": ["必须"], "condition": "", "object": "", "purpose": "無條理則亂次以濟", "punishment": "", "confidence": "high"},
    # 01-065 立法求其可行
    {"item_id": "01-065", "type": "义务型", "subject": "立法", "action": "先求其可行", "modals": ["必须"], "condition": "立法貴乎必行", "object": "", "purpose": "不求可行而冒昧行，格於成例限於才力拂乎人情戾乎土俗，終歸不行", "punishment": "", "confidence": "high"},
    # 01-066 法立弊生不可因噎廢食
    {"item_id": "01-066", "type": "禁止型", "subject": "法立弊生", "action": "不可因噎廢食", "modals": ["禁止"], "condition": "決無百利而無一弊之事", "object": "", "purpose": "朱子：七分利三分害當行之，三分利七分害不當行", "punishment": "", "confidence": "high"},
    # 01-067 天不為荊棘靳雨露
    {"item_id": "01-067", "type": "义务型", "subject": "地方官利民之事被壞人阻撓或加訕謗", "action": "只須問事之應行與否，事如應行切不可嘔氣灰心，仍舊照行", "modals": ["必须", "不可"], "condition": "天不為荊棘靳其雨露", "object": "", "purpose": "不因荊棘連累桑麻", "punishment": "", "confidence": "high"},
    # 01-068 不必親身私訪
    {"item_id": "01-068", "type": "禁止型", "subject": "官", "action": "不可有私訪之實", "modals": ["禁止"], "condition": "可無私訪之名", "object": "", "purpose": "私訪最誤事：所問之人未必公正、得之傳聞未必目擊、本官先入為主必誤事", "punishment": "", "confidence": "high"},
    # 01-069 不可派人私訪
    {"item_id": "01-069", "type": "禁止型", "subject": "官", "action": "不可派人私訪", "modals": ["禁止"], "condition": "所派之人未必可靠", "object": "", "purpose": "奸胥土棍假稱奉命探事招搖訛詐", "punishment": "", "confidence": "high"},
    # 01-070 官不可好名
    {"item_id": "01-070", "type": "禁止型", "subject": "官", "action": "不可好名", "modals": ["禁止"], "condition": "實者名之形名者實之影", "object": "", "purpose": "一味好名純盜虛聲毫無實濟必至名裂", "punishment": "", "confidence": "high"},
    # 01-071 官不可無名
    {"item_id": "01-071", "type": "义务型", "subject": "官", "action": "不可無名", "modals": ["必须"], "condition": "子夏：信而後勞其民", "object": "", "purpose": "誠意之聲名所感，民乃信服", "punishment": "", "confidence": "high"},
    # 01-074 官不可不畏民
    {"item_id": "01-074", "type": "义务型", "subject": "官", "action": "不可不畏民", "modals": ["必须"], "condition": "民不畏官是謂亂象，官不畏民是謂亂階", "object": "民", "purpose": "盤庚恭承民命、祖已王司敬民、文王不敢侮鰥寡", "punishment": "", "confidence": "high"},
    # 01-075 畏民非畏葸之謂
    {"item_id": "01-075", "type": "义务型", "subject": "為政者", "action": "俗之可因者利用因，俗之應革者利用革", "modals": ["宜"], "condition": "畏民非畏葸之謂，不敢肆於民上為所欲為", "object": "民情風俗", "purpose": "毌違俗以拂百姓之欲、毌徇俗以干百姓之譽", "punishment": "", "confidence": "high"},
    # 01-076 鄉愚見官箕踞無禮
    {"item_id": "01-076", "type": "义务型", "subject": "鄉愚無禮太甚者", "action": "不能不薄責示懲，特不必帶至衙門坐堂撲責", "modals": ["宜", "不必"], "condition": "未嘗見官者不足深怪", "object": "", "purpose": "包荒之量、啟迪之殷；怒鞭撲之示人不廣", "punishment": "薄責示懲", "confidence": "high"},
    # 01-077 親民工夫
    {"item_id": "01-077", "type": "义务型", "subject": "地方官下鄉", "action": "招集耆老諮詢慰問，勸以孝弟力田早完國課莫打官司", "modals": ["必须", "宜"], "condition": "男婦老幼環而相視", "object": "耆老百姓", "purpose": "親民工夫", "punishment": "", "confidence": "high"},
    {"item_id": "01-077", "type": "禁止型", "subject": "差役", "action": "毌任耀武揚威執鞭驅逐", "modals": ["禁止"], "condition": "下鄉時", "object": "百姓", "purpose": "", "punishment": "", "confidence": "high"},
    # 01-078 懲治豪橫之後須随時傳諭警戒
    {"item_id": "01-078", "type": "程序型", "subject": "責懲釋放之後", "action": "如因巡厯經過其地，須向紳士耆老詢問某人近況，傳諭警戒", "modals": ["必须"], "condition": "不孝不弟及豪橫之輩已傳案責懲", "object": "豪橫之人", "purpose": "其人聞之必畏懼斂迹", "punishment": "", "confidence": "high"},
    # 01-079 告示
    {"item_id": "01-079", "type": "义务型", "subject": "告示", "action": "須簡明剀切，不可繁瑣通套", "modals": ["必须", "不可"], "condition": "", "object": "百姓", "purpose": "簡則易記、明則易曉、剀切則入情入理", "punishment": "", "confidence": "high"},
    # 01-080 咨訪風俗
    {"item_id": "01-080", "type": "义务型", "subject": "民風土俗", "action": "各處不同，須博訪周咨留心體察", "modals": ["必须"], "condition": "", "object": "風俗", "purpose": "不訪察則行事乖錯、刑罰失中、號令格格不入", "punishment": "", "confidence": "high"},
    # 01-081 看本邑志書
    {"item_id": "01-081", "type": "义务型", "subject": "本邑志書", "action": "不可不看", "modals": ["必须"], "condition": "民情土俗悉載志書之內", "object": "志書", "purpose": "因地制宜", "punishment": "", "confidence": "high"},
    # 01-082 讀有用之書
    {"item_id": "01-082", "type": "义务型", "subject": "公事稍暇", "action": "宜讀有用之書", "modals": ["宜"], "condition": "作詩寫字彈琴下棋無關百姓痛癢", "object": "有用之書", "purpose": "拓心胸增識見", "punishment": "", "confidence": "high"},
    # 01-083 閱文稿
    {"item_id": "01-083", "type": "程序型", "subject": "州縣奉到文書", "action": "務須耐煩閱明，各就地方情形悉行籌畫，應回覆者明白回覆", "modals": ["必须"], "condition": "文書稿案有書吏序送幕賓點改之陋習", "object": "文稿", "purpose": "事得其理民受其益，增長才識", "punishment": "", "confidence": "high"},
    # 01-084 拆公文
    {"item_id": "01-084", "type": "程序型", "subject": "一切公文", "action": "必須親拆，即不親拆亦必令家丁當面拆封", "modals": ["必须"], "condition": "", "object": "公文", "purpose": "防書吏作弊", "punishment": "", "confidence": "high"},
]
