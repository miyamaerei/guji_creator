# -*- coding: utf-8 -*-
"""《平平言》论说源数据（卷01 全量）——AI 判定装填。
stance ∈ OPN_STANCES；argument 为作者论说立场概括；说理句抽论说、规范句抽规则（分工）。"""

RECORDS = [
    # 01-001 造福莫如州縣
    {"item_id": "01-001", "topic": "造福莫如州縣", "stance": "肯定", "argument": "州縣親民造福最易，士君子心存利濟當自州縣始；章楓山歷官所至有惠政可證", "evidence_refs": [], "confidence": "high"},
    # 01-002 造孽莫如州縣
    {"item_id": "01-002", "topic": "造孽莫如州縣", "stance": "否定", "argument": "同是州縣，造福易造孽亦易；社倉保甲等美政行之不善反成害民之政", "evidence_refs": [], "confidence": "high"},
    # 01-003 官不易做
    {"item_id": "01-003", "topic": "官不易做", "stance": "肯定", "argument": "做官是苦事：欲造福不造孽，先須耐得苦；歷官如苦人處苦事方能成就", "evidence_refs": ["呂新吾先生"], "confidence": "high"},
    # 01-004 立志
    {"item_id": "01-004", "topic": "立志", "stance": "肯定", "argument": "立志第一義：志在造福，則一切貪求自息", "evidence_refs": [], "confidence": "high"},
    # 01-005 立志在候補時
    {"item_id": "01-005", "topic": "立志在候補時", "stance": "肯定", "argument": "候補時即須立定主意，臨事方有把持", "evidence_refs": [], "confidence": "high"},
    # 01-006 候補宜讀書
    {"item_id": "01-006", "topic": "候補宜讀書", "stance": "肯定", "argument": "候補時宜讀吏治書與本朝吏治書：律例、則例、官箴、治譜、輿地、荒政、兵事皆為牧令所必需", "evidence_refs": ["福惠全書"], "confidence": "high"},
    # 01-007 候補宜擇交
    {"item_id": "01-007", "topic": "候補宜擇交", "stance": "肯定", "argument": "擇交為候補第一義，友必勝己", "evidence_refs": [], "confidence": "high"},
    # 01-008 候補宜虛心
    {"item_id": "01-008", "topic": "候補宜虛心", "stance": "肯定", "argument": "虛心訪問同官，即受委曲亦是學問", "evidence_refs": [], "confidence": "high"},
    # 01-009 官場換帖太容易
    {"item_id": "01-009", "topic": "官場換帖太容易", "stance": "中立", "argument": "官場換帖太容易，交誼反不堅固，當慎之", "evidence_refs": [], "confidence": "high"},
    # 01-010 候補宜謹言
    {"item_id": "01-010", "topic": "候補宜謹言", "stance": "肯定", "argument": "禍從口出，衙參言語最宜謹慎", "evidence_refs": [], "confidence": "high"},
    # 01-011 候補人員見上司
    {"item_id": "01-011", "topic": "候補人員見上司", "stance": "肯定", "argument": "見上司應讓首府首縣對答，不可僭越攙說", "evidence_refs": [], "confidence": "high"},
    # 01-012 君相不能造命
    {"item_id": "01-012", "topic": "君相不能造命", "stance": "肯定", "argument": "富貴自有定數，君相不能造命，非分之求無益", "evidence_refs": ["能改齋漫錄"], "confidence": "high"},
    # 01-013 小人枉為小人
    {"item_id": "01-013", "topic": "小人枉為小人", "stance": "肯定", "argument": "小人算計徒自勞，枉為小人", "evidence_refs": [], "confidence": "high"},
    # 01-014 無恥
    {"item_id": "01-014", "topic": "無恥", "stance": "否定", "argument": "無恥之甚莫如權貴家奴與丐官者；顧亭林論亡國之君恥不及家人奴婢", "evidence_refs": ["顧亭林先生"], "confidence": "high"},
    # 01-015 候補當差
    {"item_id": "01-015", "topic": "候補當差", "stance": "肯定", "argument": "當差須盡心，不計勞怨；元微之詩可證公事之難", "evidence_refs": ["元微之"], "confidence": "high"},
    # 01-016 候補出差請教首府縣
    {"item_id": "01-016", "topic": "候補出差請教首府縣", "stance": "肯定", "argument": "出差宜請教首府縣以知地方情形，免誤事", "evidence_refs": [], "confidence": "high"},
    # 01-017 出差勿計較供應程儀
    {"item_id": "01-017", "topic": "出差勿計較供應程儀", "stance": "肯定", "argument": "出差供應程儀厚薄不計較，事辦為要", "evidence_refs": [], "confidence": "high"},
    # 01-018 候補時宜訪求幕友
    {"item_id": "01-018", "topic": "候補時宜訪求幕友", "stance": "肯定", "argument": "刑錢幕友最關緊要，候補時即宜訪求，臨事不致倉猝", "evidence_refs": [], "confidence": "high"},
    # 01-019 候補宜儉用
    {"item_id": "01-019", "topic": "候補宜儉用", "stance": "肯定", "argument": "候補時儉用，到任後方能自立，不致因缺用而貪", "evidence_refs": [], "confidence": "high"},
    # 01-020 候補時同寅女眷不宜往來
    {"item_id": "01-020", "topic": "候補時同寅女眷不宜往來", "stance": "否定", "argument": "同寅女眷往來易生是非，於候補聲名有損", "evidence_refs": [], "confidence": "high"},
    # 01-021 正五九月可上官
    {"item_id": "01-021", "topic": "正五九月可上官", "stance": "怀疑", "argument": "正五九月不宜上官之忌月說，作者以經史考辨其不足據，親歷驗之", "evidence_refs": ["雲溪漫鈔", "菽園雜記", "南齊書", "北齊書"], "confidence": "high"},
    # 01-022 四絕四離四不祥月忌不足信
    {"item_id": "01-022", "topic": "四絕四離四不祥月忌不足信", "stance": "怀疑", "argument": "四絕四離四不祥諸忌日不足信，作者篆襄陽縣事驗之無驗", "evidence_refs": [], "confidence": "high"},
    # 01-023 到任可進南門
    {"item_id": "01-023", "topic": "到任可進南門", "stance": "怀疑", "argument": "到任忌進南門之說不足信，作者親歷兩地驗之", "evidence_refs": [], "confidence": "high"},
    # 01-024 到任時借貸
    {"item_id": "01-024", "topic": "到任時借貸", "stance": "否定", "argument": "到任借貸易受部民挾制，貽害無窮，寧儉毋借", "evidence_refs": [], "confidence": "high"},
    # 01-027 工房呈輿圖
    {"item_id": "01-027", "topic": "工房呈輿圖", "stance": "肯定", "argument": "輿圖須開方計里，方可量地知遠近，非徒具文", "evidence_refs": [], "confidence": "high"},
    # 01-028 新官到任須抖擻精神
    {"item_id": "01-028", "topic": "新官到任須抖擻精神", "stance": "肯定", "argument": "到任初精神最要緊，百事賴以振作", "evidence_refs": [], "confidence": "high"},
    # 01-029 大利大弊須徐徐興革
    {"item_id": "01-029", "topic": "大利大弊須徐徐興革", "stance": "肯定", "argument": "興革大政須徐徐圖之，不可操切", "evidence_refs": [], "confidence": "high"},
    # 01-030 下馬風
    {"item_id": "01-030", "topic": "下馬風", "stance": "否定", "argument": "新任到任即張揚興革之風最可厭，非實心任事者所為", "evidence_refs": ["袁易齋"], "confidence": "high"},
    # 01-031 初任宜簡僻缺
    {"item_id": "01-031", "topic": "初任宜簡僻缺", "stance": "肯定", "argument": "初任宜簡僻之缺，事簡民淳可學習；衝繁疲難兼全之最要缺非初任所宜", "evidence_refs": [], "confidence": "high"},
    # 01-032 公罪私罪
    {"item_id": "01-032", "topic": "公罪可容、私罪必不可有", "stance": "肯定", "argument": "公罪出於無心尚可容，私罪出於有心必不可有；抵銷則例森嚴，官員當知畏", "evidence_refs": [], "confidence": "high"},
    # 01-034 吏不可俗
    {"item_id": "01-034", "topic": "吏不可俗", "stance": "肯定", "argument": "用三代以前見識而不迂、就三代以後家數而不俗；家數非必不可就，但不可俗耳", "evidence_refs": ["呂叔簡先生"], "confidence": "high"},
    # 01-035 事不可入廟門者斷不可為
    {"item_id": "01-035", "topic": "不可入廟門者斷不可為", "stance": "肯定", "argument": "發念之端不可告神明者斷不可為；此說不求不愧衾影但求可入廟門，平正而不強人以難", "evidence_refs": ["汪龍莊明府"], "confidence": "high"},
    # 01-036 官不可貪
    {"item_id": "01-036", "topic": "官不可貪", "stance": "否定", "argument": "貪之害有六：壞心術、敗風俗、損聲名、干國法、辱祖宗、毒子孫；受贓罪名森嚴", "evidence_refs": ["劉簾舫觀察", "任杏農學博"], "confidence": "high"},
    # 01-037 官不必貪
    {"item_id": "01-037", "topic": "官不必貪", "stance": "否定", "argument": "貪賄六不必：眾人分肥、家丁挾制、書差恥笑、畏百姓上控、畏同寅多言、畏上司訪聞", "evidence_refs": [], "confidence": "high"},
    # 01-038 貪吏惟恐民之不窮
    {"item_id": "01-038", "topic": "貪吏惟恐民之不窮", "stance": "否定", "argument": "循吏惟恐窮民不富、貪吏惟恐富民不窮；胡文忠所述官吏誣富詐財故事為證", "evidence_refs": ["胡文忠公"], "confidence": "high"},
    # 01-039 官不可與民爭利（正文=義利關論）
    {"item_id": "01-039", "topic": "官不可與民爭利", "stance": "肯定", "argument": "義利關乃人鬼界，一失足即入鬼界；初在可取不可取之間，久則只知利不知害，當視如酖毒萬萬不可嘗試", "evidence_refs": [], "confidence": "high"},
    # 01-040 義利關乃人鬼界（正文=崇陽案 + 律載）
    {"item_id": "01-040", "topic": "與民爭利之害", "stance": "否定", "argument": "崇陽令派差爭掘陰沉木被參革；明高皇帝以民金歸民；律載常物聽民收用，陰沉木不應入官", "evidence_refs": ["高皇帝實錄"], "confidence": "high"},
    # 01-040 義利關乃人鬼界
    {"item_id": "01-040", "topic": "義利關乃人鬼界", "stance": "肯定", "argument": "義利關乃人鬼界，一失足即入鬼界；初在可取不可取之間，久則只知利不知害，當視如酖毒", "evidence_refs": [], "confidence": "high"},
    # 01-041 退一步想
    {"item_id": "01-041", "topic": "退一步想", "stance": "肯定", "argument": "退一步想貪心自息；胡文忠批語：立志不求溫飽，官何負於我", "evidence_refs": ["胡文忠公"], "confidence": "high"},
    # 01-042 惷氣
    {"item_id": "01-042", "topic": "惷氣", "stance": "肯定", "argument": "大賢以下做好人行好事皆帶惷氣，自安於惷；襄人作歌謠稱其不用門丁、撲捕蝗、不愛寶", "evidence_refs": [], "confidence": "high"},
    # 01-043 官民交財
    {"item_id": "01-043", "topic": "官民交財最宜留意", "stance": "肯定", "argument": "官與民交財乃官聲所繫，須用現銀平買、出示曉諭、准鋪戶扭稟強賒", "evidence_refs": [], "confidence": "high"},
    # 01-044 官價
    {"item_id": "01-044", "topic": "官價裁革須量入為出", "stance": "中立", "argument": "官價累民宜裁，然須通盤計算：入不敷出姑仍舊貫但不可漫無限制，出入不甚懸殊則必應裁革", "evidence_refs": [], "confidence": "high"},
    # 01-046 革陋規非易事
    {"item_id": "01-046", "topic": "革陋規非易事", "stance": "肯定", "argument": "革陋規不可令人知，恐棍蠹撞騙；一切興除可藉以撞騙者均應密速行之；樊城減稅親歷為證", "evidence_refs": ["劉簾舫觀察", "庸吏庸言"], "confidence": "high"},
    # 01-047 不儉用必貪贓
    {"item_id": "01-047", "topic": "不儉用必貪贓", "stance": "肯定", "argument": "廉俸有限、陋規只此數，奢華則缺用、缺用則借債、借債不已則貪贓", "evidence_refs": [], "confidence": "high"},
    # 01-048 不儉用必虧空
    {"item_id": "01-048", "topic": "不儉用必虧空", "stance": "肯定", "argument": "不節用不貪贓者必虧空公帑；虧空分侵盜那移，律例森嚴，累己累上", "evidence_refs": [], "confidence": "high"},
    # 01-049 優缺亦不可奢華
    {"item_id": "01-049", "topic": "優缺亦不可奢華", "stance": "否定", "argument": "優缺不可多得，應用之余可與鄰里鄉黨，勿習奢華；一人奢華一家奢華，罷後立涸", "evidence_refs": [], "confidence": "high"},
    # 01-050 儉非吝嗇
    {"item_id": "01-050", "topic": "儉非吝嗇", "stance": "肯定", "argument": "可省則省為儉、不可省而省為吝嗇；救急大事不可惜費，應酬須循舊", "evidence_refs": ["汪龍莊明府"], "confidence": "high"},
    # 01-051 清慎勤
    {"item_id": "01-051", "topic": "清慎勤", "stance": "肯定", "argument": "清慎勤三字訣，清為第一義；廉而不慎多疏略、廉而不勤政廢弛；貞節婦女之喻", "evidence_refs": ["司馬炎", "真西山先生"], "confidence": "high"},
    # 01-052 勤則少暇
    {"item_id": "01-052", "topic": "勤則少暇", "stance": "肯定", "argument": "治人者不可多暇日；懶故多暇、勤則少暇；石瑤辰自號民傭，父母之于子亦只是不懶", "evidence_refs": ["石瑤辰郡丞"], "confidence": "high"},
    # 01-053 官不可不明
    {"item_id": "01-053", "topic": "官不可不明", "stance": "肯定", "argument": "廉慎勤之外尚須明：廉而不明有人從中要錢、慎而不明當斷不斷、勤而不明徒勞罔益", "evidence_refs": [], "confidence": "high"},
    # 01-054 曉事
    {"item_id": "01-054", "topic": "曉事尤難", "stance": "肯定", "argument": "當官明理難、曉事尤難；蜜中鼠矢案：理雖決定事或偶合，執理御事有時不通，窮理之人反為曉事者所笑", "evidence_refs": ["吳厯", "鄭克", "裴松之"], "confidence": "high"},
    # 01-055 官不可過用其明
    {"item_id": "01-055", "topic": "官不可過用其明", "stance": "肯定", "argument": "不可不明亦不可過用其明；其政察察其民缺缺", "evidence_refs": ["老子"], "confidence": "high"},
    # 01-056 精明渾厚
    {"item_id": "01-056", "topic": "精明渾厚", "stance": "肯定", "argument": "精明欠渾厚便是刻薄、渾厚欠精明便是糊塗；移守武昌蒙大府奏稱精明渾厚", "evidence_refs": [], "confidence": "high"},
    # 01-057 緩
    {"item_id": "01-057", "topic": "緩", "stance": "肯定", "argument": "勤謹和緩四字訣；世間事多因忙後錯，緩即從容詳處，非怠緩", "evidence_refs": ["劉忠定公安世", "呂居仁"], "confidence": "high"},
    # 01-058 勿喜事
    {"item_id": "01-058", "topic": "勿喜事", "stance": "肯定", "argument": "為政在省事不在多事、守法不在變法、安靜不在紛擾、寬簡不在煩苛；寬者不為苛急、簡者不為繁碎", "evidence_refs": ["楊文襄公", "歐陽文忠公"], "confidence": "high"},
    # 01-059 熱腸
    {"item_id": "01-059", "topic": "熱腸", "stance": "肯定", "argument": "富貴利達眼不可熱、民生休戚腸不可不熱；得百自了漢不如得一熱腸人；有治人無治法", "evidence_refs": ["陳文恭公"], "confidence": "high"},
    # 01-060 擔當
    {"item_id": "01-060", "topic": "擔當", "stance": "肯定", "argument": "辦大事須有擔當、功名置度外；洪皓截留常平米、范純仁擅發常平、王竑發廣運倉、雲軒公截留城工銀救災，皆以一身任專擅之咎", "evidence_refs": ["洪忠宣公", "范忠宣公", "王竑", "雲軒公"], "confidence": "high"},
    # 01-061 淺露
    {"item_id": "01-061", "topic": "淺露", "stance": "否定", "argument": "淺露最誤事；李懷光、王彥章、宋濟王皆肆口揚言犯小人之忌而敗", "evidence_refs": ["李懷光", "王彥章", "宋濟王"], "confidence": "high"},
    # 01-062 成見
    {"item_id": "01-062", "topic": "成見", "stance": "否定", "argument": "當官不可預存成見；平者輕重適中，心有成見則畸輕畸重", "evidence_refs": ["孟子", "張子"], "confidence": "high"},
    # 01-063 有條理
    {"item_id": "01-063", "topic": "有條理", "stance": "肯定", "argument": "事不論大小總要有條理；韓信將兵多多益善不外分數明", "evidence_refs": ["韓信"], "confidence": "high"},
    # 01-064 學問閱厯
    {"item_id": "01-064", "topic": "學問閱厯", "stance": "肯定", "argument": "血性聰明需學問閱歷輔之：無學問血性僨事、無閱歷聰明誤事", "evidence_refs": [], "confidence": "high"},
    # 01-065 立法求其可行
    {"item_id": "01-065", "topic": "立法求其可行", "stance": "肯定", "argument": "立法貴乎必行、先求可行；新法之禍在效商鞅必行而不問可行與否", "evidence_refs": ["王安石", "商鞅"], "confidence": "high"},
    # 01-066 法立弊生不可因噎廢食
    {"item_id": "01-066", "topic": "法立弊生不可因噎廢食", "stance": "肯定", "argument": "決無百利無一弊之法；設官設兵皆有弊，不可因害廢設；朱子七分利三分害當行；呂新吾毌執偶然之弊訾常然之法", "evidence_refs": ["朱子", "呂新吾先生"], "confidence": "high"},
    # 01-067 天不為荊棘靳雨露
    {"item_id": "01-067", "topic": "天不為荊棘靳雨露", "stance": "肯定", "argument": "利民之事被壞人阻撓訕謗，只問應行與否，應行仍舊照行；陸宣公語為慰", "evidence_refs": ["陸宣公"], "confidence": "high"},
    # 01-068 不必親身私訪
    {"item_id": "01-068", "topic": "不必親身私訪", "stance": "否定", "argument": "私訪所問之人未必公正、得之傳聞未必目擊、本官先入為主必誤事；有私訪之名無其實最善", "evidence_refs": [], "confidence": "high"},
    # 01-069 不可派人私訪
    {"item_id": "01-069", "topic": "不可派人私訪", "stance": "否定", "argument": "派人私訪所派未必可靠，奸胥土棍假稱奉命招搖訛詐", "evidence_refs": [], "confidence": "high"},
    # 01-070 官不可好名
    {"item_id": "01-070", "topic": "官不可好名", "stance": "否定", "argument": "實者名之形名者實之影；一味好名純盜虛聲毫無實濟必至名裂", "evidence_refs": [], "confidence": "high"},
    # 01-071 官不可無名
    {"item_id": "01-071", "topic": "官不可無名", "stance": "肯定", "argument": "官民隔塞不通，誠意需聲名以達；受惠者信是誠意所感，未受惠者亦信是聲名所感", "evidence_refs": ["子夏"], "confidence": "high"},
    # 01-072 官聲卓著最省事
    {"item_id": "01-072", "topic": "官聲卓著最省事", "stance": "肯定", "argument": "廉名不敢賄進、正名不敢情託、精明果決名不敢輕試，斷卻葛藤省卻心力", "evidence_refs": [], "confidence": "high"},
    # 01-073 惡居下流
    {"item_id": "01-073", "topic": "惡居下流", "stance": "肯定", "argument": "平日聲名太壞，偶出一令一行亦被疑染指；仁富格言出孟子口則為格言、出陽虎口則為勦說", "evidence_refs": ["來瞿塘先生"], "confidence": "high"},
    # 01-074 官不可不畏民
    {"item_id": "01-074", "topic": "官不可不畏民", "stance": "肯定", "argument": "民不畏官是謂亂象、官不畏民是謂亂階；盤庚恭承民命、祖已王司敬民、文王不敢侮鰥寡", "evidence_refs": ["盤庚", "祖已", "文王"], "confidence": "high"},
    # 01-075 畏民非畏葸之謂
    {"item_id": "01-075", "topic": "畏民非畏葸之謂", "stance": "肯定", "argument": "畏民者不敢肆於民上為所欲為；民好民惡指公好公惡，偏好偏惡當別論；俗可因者因、應革者革", "evidence_refs": [], "confidence": "high"},
    # 01-076 鄉愚見官箕踞無禮
    {"item_id": "01-076", "topic": "鄉愚見官箕踞無禮", "stance": "中立", "argument": "鄉愚無禮不足深怪，寬之訓之見包荒啟迪之量；無禮太甚者薄責示懲，不必帶至衙門坐堂撲責", "evidence_refs": [], "confidence": "high"},
    # 01-077 親民工夫
    {"item_id": "01-077", "topic": "親民工夫", "stance": "肯定", "argument": "下鄉招集耆老諮詢慰問，勸以孝弟力田早完國課莫打官司；毋任差役耀武揚威執鞭驅逐", "evidence_refs": [], "confidence": "high"},
    # 01-080 咨訪風俗
    {"item_id": "01-080", "topic": "咨訪風俗", "stance": "肯定", "argument": "民風土俗各處不同，須博訪周咨；劉大夏召邊上父老講究、周忱沿村詢訪老農，故得領要", "evidence_refs": ["劉忠宣公", "周文襄公"], "confidence": "high"},
    # 01-082 讀有用之書
    {"item_id": "01-082", "topic": "讀有用之書", "stance": "肯定", "argument": "朝廷設官原為百姓，作詩寫字彈琴下棋無關百姓痛癢；公事稍暇宜讀有用之書拓心胸增識見", "evidence_refs": [], "confidence": "high"},
    # 01-083 閱文稿
    {"item_id": "01-083", "topic": "閱文稿", "stance": "肯定", "argument": "文稿案牘不可盡付書吏幕賓；奉到文書須耐煩閱明、各就地方情形籌畫，方能事得其理民受其益", "evidence_refs": ["陳文恭公"], "confidence": "high"},
]
