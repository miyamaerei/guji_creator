# -*- coding: utf-8 -*-
"""《平平言》规则源数据（卷02 全量）——AI 判定装填。"""

RECORDS = [
    # 02-001 素位而行
    {"item_id": "02-001", "type": "禁止型", "subject": "在任多年應遷應調而不遷不調者", "action": "切不可生怠惰心，須就現在之位辦現在應辦之事", "modals": ["禁止"], "condition": "此中自有定數", "object": "", "purpose": "不負設官分職之意", "punishment": "", "confidence": "high"},
    # 02-003 勿演戲
    {"item_id": "02-003", "type": "禁止型", "subject": "衙門內外", "action": "勿演戲，官眷出外看戲固屬不可，即在本衙門以內亦不可看戲", "modals": ["禁止"], "condition": "", "object": "", "purpose": "衙門多一日宴樂外間即多一日愁苦；費晝夜費廉俸費物命，火燭堪虞奴婢奸盜易起", "punishment": "", "confidence": "high"},
    # 02-004 勿賭博
    {"item_id": "02-004", "type": "禁止型", "subject": "官衙", "action": "不可賭博", "modals": ["禁止"], "condition": "本官好賭則官親幕友家丁書差無不好賭", "object": "", "purpose": "滿衙皆賭百弊叢生", "punishment": "", "confidence": "high"},
    # 02-005 勿嗜酒
    {"item_id": "02-005", "type": "禁止型", "subject": "官", "action": "酒可飲不可嗜", "modals": ["禁止"], "condition": "", "object": "酒", "purpose": "飲酒不節最易誤事，使酒亦官聲之玷", "punishment": "", "confidence": "high"},
    # 02-006 勿勸客過飲
    {"item_id": "02-006", "type": "义务型", "subject": "讌會", "action": "勸客不過聊示敬客之意，客如不飲不必苦勸", "modals": ["宜"], "condition": "酒量大小不一，過量則醉", "object": "客", "purpose": "酒以合歡，勿令醜態百出", "punishment": "", "confidence": "high"},
    # 02-007 勿講究飲食
    {"item_id": "02-007", "type": "禁止型", "subject": "宦途", "action": "飲食勿講究，勿苛求屬吏", "modals": ["禁止"], "condition": "飢時易為食飽時難為味", "object": "飲食", "purpose": "何曾奢豪致何氏滅亡無遺類", "punishment": "", "confidence": "high"},
    # 02-008 讌會勿太奢
    {"item_id": "02-008", "type": "禁止型", "subject": "州縣讌會", "action": "不可太奢，應在不豐不儉之間", "modals": ["禁止"], "condition": "縱不能如昔人五簋之約", "object": "", "purpose": "豈可過於奢侈致開風氣", "punishment": "", "confidence": "high"},
    # 02-009 勿買骨董
    {"item_id": "02-009", "type": "禁止型", "subject": "官", "action": "勿買骨董，買骨董不如買書", "modals": ["禁止"], "condition": "書有用骨董無用", "object": "骨董", "purpose": "何必以有用之錢購無用之物", "punishment": "", "confidence": "high"},
    # 02-010 勿諂媚上司
    {"item_id": "02-010", "type": "禁止型", "subject": "官", "action": "勿諂媚上司", "modals": ["禁止"], "condition": "上司不可諂媚亦不必諂媚", "object": "上司", "purpose": "諂媚太過不特見惡於君子併且取厭於小人", "punishment": "", "confidence": "high"},
    # 02-011 事上宜誠樸不宜浮華
    {"item_id": "02-011", "type": "义务型", "subject": "事上", "action": "宜誠樸不宜浮華", "modals": ["宜", "禁止"], "condition": "誠樸之吏悃愊無華", "object": "上司", "purpose": "誠樸者久，浮華者底蘊畢露轉為上司所鄙薄", "punishment": "", "confidence": "high"},
    # 02-012 上行公文宜明白
    {"item_id": "02-012", "type": "义务型", "subject": "上行公文", "action": "須明白曉暢，不可率略晦塞", "modals": ["必须", "不可"], "condition": "上司走馬觀花，幕友多不耐煩思索", "object": "上司", "purpose": "須令一目了然", "punishment": "", "confidence": "high"},
    # 02-013 稟陳利害措詞宜委婉
    {"item_id": "02-013", "type": "义务型", "subject": "事有關係民生利害者", "action": "須據實稟陳，不得因上司駁斥便不敢再申前說，但措詞須委婉", "modals": ["必须", "不得"], "condition": "或應行而上司不准行，或不應行而上司必欲行", "object": "上司", "purpose": "致誤地方", "punishment": "", "confidence": "high"},
    # 02-014 上司厲民之政宜變通
    {"item_id": "02-014", "type": "义务型", "subject": "上司厲民之政", "action": "志在必行，州縣既不能挽回便須酌劑而變通之", "modals": ["宜"], "condition": "不能挽回", "object": "", "purpose": "寬一分則民受一分之賜，不致大傷元氣", "punishment": "", "confidence": "high"},
    # 02-015 上司衙門舊例不可省
    {"item_id": "02-015", "type": "义务型", "subject": "上司衙門常規舊例", "action": "必不可省，亦不必格外加多", "modals": ["必须", "不必"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 02-016 前任善政宜實力經理
    {"item_id": "02-016", "type": "义务型", "subject": "前任有益地方之事", "action": "後任須實力經理", "modals": ["必须"], "condition": "", "object": "", "purpose": "事果有益地方原不必功自我出論自我創", "punishment": "", "confidence": "high"},
    # 02-017 原問不實
    {"item_id": "02-017", "type": "义务型", "subject": "發審案件原問不實", "action": "必須據實平反，切勿回護原問致枉民命", "modals": ["必须", "禁止"], "condition": "", "object": "民命", "purpose": "同寅之誼可稟求上司將原問官銜名列入詳內隨同更正", "punishment": "", "confidence": "high"},
    # 02-018 與小人共事勿負氣
    {"item_id": "02-018", "type": "禁止型", "subject": "與小人共事", "action": "切不可負氣，必須委曲求全", "modals": ["禁止", "必须"], "condition": "", "object": "", "purpose": "乃見作用", "punishment": "", "confidence": "high"},
    # 02-019 同寅勿修怨
    {"item_id": "02-019", "type": "禁止型", "subject": "同寅待我設有過當之處", "action": "祇可情恕理遣，不可修怨", "modals": ["禁止"], "condition": "", "object": "", "purpose": "修怨則失和且示人不廣", "punishment": "", "confidence": "high"},
    # 02-020 勿暴人祖父過惡
    {"item_id": "02-020", "type": "禁止型", "subject": "同寅失和雖甚忿怒", "action": "切不可發人陰私，尤不可暴人父祖之惡", "modals": ["禁止"], "condition": "言語傷人甚於矛戟", "object": "", "purpose": "指其所諱尚不免恨入骨髓，何况暴其祖父之過惡", "punishment": "", "confidence": "high"},
    # 02-021 佐雜衙門書差被人控告
    {"item_id": "02-021", "type": "程序型", "subject": "有控告佐雜衙門書差者", "action": "必應批提", "modals": ["必须"], "condition": "", "object": "", "purpose": "外似刻薄實則保全佐雜，緣佐雜禁不起風浪", "punishment": "", "confidence": "high"},
    # 02-022 詞訟勿批佐雜審理
    {"item_id": "02-022", "type": "禁止型", "subject": "印官", "action": "切不可批發詞訟案件與佐雜，應酌量資助其清苦", "modals": ["禁止"], "condition": "佐雜官職分應管之事方准印官批令查勘", "object": "佐雜", "purpose": "", "punishment": "將地方詞訟批發佐雜辦理者降三級調用，釀成人命者革職", "confidence": "high"},
    # 02-024 幕友須常見面
    {"item_id": "02-024", "type": "义务型", "subject": "官與幕友", "action": "須時常見面，不可令家人傳話", "modals": ["必须", "不可"], "condition": "", "object": "", "purpose": "糊塗者傳話不明白，聰明者又高下其語，公事焉得不錯", "punishment": "", "confidence": "high"},
    # 02-025 勿令子弟出宅門
    {"item_id": "02-025", "type": "禁止型", "subject": "官之子弟", "action": "不可出宅門", "modals": ["禁止"], "condition": "", "object": "", "purpose": "恐被人誘入邪徑，恐蠹役劣紳與之交通", "punishment": "", "confidence": "high"},
    # 02-026 勿令子弟主張公事
    {"item_id": "02-026", "type": "禁止型", "subject": "衙門公事", "action": "不可由少爺主張", "modals": ["禁止"], "condition": "", "object": "", "purpose": "攬權作弊，本官之耳愈聾少爺之膽愈大，必至十分決裂", "punishment": "", "confidence": "high"},
    # 02-027 官須自做
    {"item_id": "02-027", "type": "义务型", "subject": "官", "action": "事無鉅細權操在手，官須自做", "modals": ["必须"], "condition": "胸無成見聽人主張則人人有權即人人做官", "object": "", "purpose": "權不下移亦不旁落，官如傀儡勢必尾大不掉", "punishment": "", "confidence": "high"},
    # 02-028 權不下移之法
    {"item_id": "02-028", "type": "义务型", "subject": "官", "action": "與百姓常見面則吏胥無權，與吏胥常見面則家丁無權", "modals": ["宜"], "condition": "", "object": "", "purpose": "權不下移", "punishment": "", "confidence": "high"},
    # 02-029 吩諭丁役須令覆述
    {"item_id": "02-029", "type": "程序型", "subject": "家人書差奉官面諭", "action": "吩諭後須令覆述一遍", "modals": ["必须"], "condition": "滿口答應一個是字，再問以所諭何事則茫然不知", "object": "", "purpose": "防誤事", "punishment": "", "confidence": "high"},
    # 02-030 勿用門丁
    {"item_id": "02-030", "type": "禁止型", "subject": "州縣", "action": "勿用門丁", "modals": ["禁止"], "condition": "州縣為親民之官，任用門丁則官與百姓氣脈不通", "object": "門丁", "purpose": "咽喉之地無故添入梗塞之物；無才者不能辦事，有才者慣於作弊", "punishment": "", "confidence": "high"},
    # 02-031 門丁不可用
    {"item_id": "02-031", "type": "禁止型", "subject": "門丁", "action": "必不可用，其弊有十", "modals": ["禁止"], "condition": "總不外惟利是視四字", "object": "門丁", "purpose": "勾通棍蠹/庇護差役/走漏消息/捺擱公事/私押人証/賣放要犯/迎合本官/污衊本官/盤剝本官/挾制本官", "punishment": "", "confidence": "high"},
    # 02-032 不必用門丁
    {"item_id": "02-032", "type": "禁止型", "subject": "門丁所司之事", "action": "約有五端，經道破半文不值，不必用門丁", "modals": ["不必"], "condition": "傳喚書差/出納稿簽/訪察情形/商量公事/為官代勞皆可自辦", "object": "門丁", "purpose": "代官作孽，殊可不必", "punishment": "", "confidence": "high"},
    # 02-034 勿用稿案簽押
    {"item_id": "02-034", "type": "禁止型", "subject": "稿案簽押", "action": "勿用，其弊與門丁同，惟賄賣差票則簽押所獨", "modals": ["禁止"], "condition": "紅籤上之姓名皆自賄賂中來", "object": "簽押", "purpose": "歸根落葉總是百姓吃虧；卯簿值日名單可聽本官輪流派差，何必設害人之簽押", "punishment": "", "confidence": "high"},
    # 02-035 勿用錢糧稅契門丁
    {"item_id": "02-035", "type": "禁止型", "subject": "錢糧門丁稅契門丁", "action": "勿用，此亦贅物", "modals": ["禁止"], "condition": "百姓不完錢糧不肯稅契門丁亦無能為力", "object": "", "purpose": "錢糧稅契銀兩均歸帳房經理即可", "punishment": "", "confidence": "high"},
    # 02-036 用印值堂不必專派
    {"item_id": "02-036", "type": "程序型", "subject": "用印值堂", "action": "不必專派某人，用印者只須識字即可勝任；恐夾帶偷用印信則派至親密友監視", "modals": ["不必"], "condition": "", "object": "", "purpose": "值堂不過攤放收回案卷，跟班儘可帶辦", "punishment": "", "confidence": "high"},
    # 02-037 應用之人不必多用
    {"item_id": "02-037", "type": "义务型", "subject": "傳帖寫字跟班管廚管監卡", "action": "均係應有之人，然不可多用", "modals": ["不可"], "condition": "衝途州縣尚有差總流差馬號等事亦須派人經理", "object": "", "purpose": "多則互相推諉必不得力", "punishment": "", "confidence": "high"},
    # 02-038 家丁宜少收
    {"item_id": "02-038", "type": "义务型", "subject": "家丁", "action": "以少收為妙", "modals": ["宜"], "condition": "", "object": "", "purpose": "少則約束易周防範易密；多則閒散之徒動生觖望散布謠言", "punishment": "", "confidence": "high"},
    # 02-039 勿借用家丁銀錢
    {"item_id": "02-039", "type": "禁止型", "subject": "官", "action": "勿借用家丁銀錢", "modals": ["禁止"], "condition": "借用長隨銀錢攜之赴署派以重任，俗名帶馱子帶肚子", "object": "家丁", "purpose": "用之則極惡窮凶剝膚入骨，不用則怨誹誣謗毀方為圓", "punishment": "", "confidence": "high"},
    # 02-040 家丁出息概歸公帳
    {"item_id": "02-040", "type": "程序型", "subject": "初到任時", "action": "應將家丁出息詢問明白，應裁者不准私收，應得者亦令繳呈帳房逐一登記，三節結總公分", "modals": ["必须", "不准"], "condition": "", "object": "家丁出息", "purpose": "若輩為利而來，不能贍其身家必不肯供我驅策", "punishment": "", "confidence": "high"},
    # 02-041 家丁以安靜為佳
    {"item_id": "02-041", "type": "禁止型", "subject": "家丁在署", "action": "以安靜為佳，不准相罵/打降/酗酒/賭博/吹彈歌唱/吸食鴉片煙", "modals": ["禁止"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 02-042 勿令家丁穿上色衣服
    {"item_id": "02-042", "type": "禁止型", "subject": "家丁", "action": "不可穿上色衣服", "modals": ["禁止"], "condition": "若輩衣服與本官一樣", "object": "", "purpose": "何以別上下而辨等威", "punishment": "", "confidence": "high"},
    # 02-043 勿令家丁穿華美衣服
    {"item_id": "02-043", "type": "禁止型", "subject": "家人", "action": "不可穿好衣服", "modals": ["禁止"], "condition": "官不要錢則若輩出息有限", "object": "", "purpose": "競尚華麗勢必在外招搖妄冀非分；正本清源則自本官節儉始", "punishment": "", "confidence": "high"},
    # 02-044 勿令家丁出外滋事
    {"item_id": "02-044", "type": "禁止型", "subject": "家丁", "action": "不可出外滋事", "modals": ["禁止"], "condition": "", "object": "", "purpose": "奴驕主敗，霍氏董賢之鑑", "punishment": "", "confidence": "high"},
    # 02-045 勿受書役陋規
    {"item_id": "02-045", "type": "禁止型", "subject": "州縣到任", "action": "書吏按舊章呈繳陋規、官代書領戳差役保正點卯送陋規，萬不可受", "modals": ["禁止"], "condition": "", "object": "陋規", "purpose": "受則玩官於股掌之上矣", "punishment": "", "confidence": "high"},
    # 02-046 書差卯簿
    {"item_id": "02-046", "type": "程序型", "subject": "點卯前三日", "action": "傳諭經承將各書差的名年歲籍貫詳細詢明逐一註載；點卯時年貌不符者即行黜革", "modals": ["必须"], "condition": "卯冊僅載姓名皆卯名並非的名", "object": "卯冊", "purpose": "防冒名頂替", "punishment": "黜革", "confidence": "high"},
    # 02-047 點卯
    {"item_id": "02-047", "type": "程序型", "subject": "點卯時", "action": "須將事無鉅細咸出親裁、家人只供使令並不主張公事等語當堂明白曉諭", "modals": ["必须"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 02-049 書辦送稿須填姓名
    {"item_id": "02-049", "type": "程序型", "subject": "書辦投稿", "action": "應將經承姓名列入稿尾，不得僅載某房兩字；兩人公承即載明某某公承某人敘稿字樣", "modals": ["必须", "不得"], "condition": "", "object": "稿", "purpose": "如有應詢問之處即可查照稿尾姓名指名傳喚", "punishment": "", "confidence": "high"},
    # 02-050 差稟拒捕宜詳察
    {"item_id": "02-050", "type": "程序型", "subject": "差役自毀其票自撕其衣捏報拒捕", "action": "官須詳察，仿汪龍莊辦法將毀票存銷改差承行，拒捕是否屬實另行確訪", "modals": ["必须"], "condition": "需索不遂往往捏造", "object": "", "purpose": "所傳之人見票內並無拒捕字樣放心到案；差役知本官不輕聽亦不復嘗試", "punishment": "提差嚴懲", "confidence": "high"},
    # 02-051 駕馭書差
    {"item_id": "02-051", "type": "义务型", "subject": "駕馭書役", "action": "不外賞罰，書吏勤勞派以承行、差役勤勞賞以符票，但須嚴禁勒索", "modals": ["必须", "须"], "condition": "賚以銀錢可偶而不可常，酒食亦然", "object": "書差", "purpose": "若因書差寒苦任其訛詐鄉愚便是縱蠹殃民", "punishment": "", "confidence": "high"},
    # 02-052 書差被控
    {"item_id": "02-052", "type": "义务型", "subject": "百姓控告書差", "action": "切莫袒護，應責者責應革者革", "modals": ["必须", "禁止"], "condition": "", "object": "書差", "purpose": "懾書差之膽亦平百姓之氣，氣平則不上控", "punishment": "", "confidence": "high"},
    # 02-053 勤見紳士
    {"item_id": "02-053", "type": "义务型", "subject": "地方官", "action": "勤見紳士", "modals": ["宜"], "condition": "不見紳士則地方一切情形無由知悉", "object": "紳士", "purpose": "不可因其賢否不齊遂一概拒絕，因噎廢食", "punishment": "", "confidence": "high"},
    # 02-054 見紳士之法
    {"item_id": "02-054", "type": "程序型", "subject": "接見正紳", "action": "不可令茶房家丁侍側；見劣紳則宜多令家人茶房號房環侍左右", "modals": ["不可", "宜"], "condition": "正紳多避嫌恐招怨", "object": "紳士", "purpose": "正紳盡言無隱，劣紳不敢公然干以私，此不惡而嚴之法", "punishment": "", "confidence": "high"},
    # 02-055 勿令紳士受累
    {"item_id": "02-055", "type": "禁止型", "subject": "紳士密告土棍訟師之事", "action": "密記於冊，無論拏與不拏辦與不辦切不可漏洩", "modals": ["禁止"], "condition": "", "object": "紳士", "purpose": "漏洩則土棍訟師尋隙報復，紳士反因我而受累", "punishment": "", "confidence": "high"},
    # 02-056 門無留客
    {"item_id": "02-056", "type": "义务型", "subject": "紳士進見過客拜謁", "action": "須嚴飭號房及傳帖家丁立時稟明，見與不見聽本官吩咐，總不得片刻留難", "modals": ["必须"], "condition": "", "object": "賓客", "purpose": "武王門銘：敬遇賓客貴賤無二", "punishment": "", "confidence": "high"},
    # 02-057 勿受紳士禮物
    {"item_id": "02-057", "type": "禁止型", "subject": "紳士送禮", "action": "必不可受", "modals": ["禁止"], "condition": "今日受禮明日拒關說不近人情；因其曾送禮而允其關說聲名狼藉", "object": "禮物", "purpose": "官之聲名", "punishment": "", "confidence": "high"},
    # 02-058 勿凌辱秀才
    {"item_id": "02-058", "type": "禁止型", "subject": "粗暴之吏", "action": "勿凌辱秀才，諸生即有一二不肖須為眾人惜體面，切不可窘辱太過波及父兄妻子", "modals": ["禁止"], "condition": "", "object": "秀才", "purpose": "全斯文之體面收一時之人心；諸生之父非大教不可加刑", "punishment": "", "confidence": "high"},
    # 02-059 不接異色人
    {"item_id": "02-059", "type": "禁止型", "subject": "當官", "action": "不接異色人，巫祝尼媼宜疏絕，匠藝之人亦當用之以時不宜久留於家", "modals": ["禁止"], "condition": "", "object": "異色人", "purpose": "皆能變易聽聞簸弄是非；房琯因琴工董庭蘭為相業之玷", "punishment": "", "confidence": "high"},
    # 02-060 得民在聽訟
    {"item_id": "02-060", "type": "义务型", "subject": "聽訟", "action": "隨到隨審可結便結，毌令拖累日久", "modals": ["必须"], "condition": "欲得民心全在聽訟", "object": "兩造", "purpose": "即此便是養民教民，懲一儆百", "punishment": "", "confidence": "high"},
    # 02-061 審案限期
    {"item_id": "02-061", "type": "时限型", "subject": "自理戶婚田土等項案件", "action": "限二十日完結", "modals": ["必须", "时限"], "condition": "", "object": "", "purpose": "", "punishment": "違限不及一月罰俸三個月，一月以上罰俸一年，半年以上罰俸二年，一年以上降一級留任", "confidence": "high"},
    {"item_id": "02-061", "type": "时限型", "subject": "尋常命案", "action": "統限六個月完結：州縣三個月解府州，府州一個月解司，司一個月解督撫，督撫一個月咨題", "modals": ["必须", "时限"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    {"item_id": "02-061", "type": "时限型", "subject": "盜案及斬絞立決命案並一切搶竊雜案", "action": "統限四個月完結：州縣分限兩個月，府州臬司督撫各分限二十日", "modals": ["必须", "时限"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    {"item_id": "02-061", "type": "时限型", "subject": "情重命案（卑幼擅殺期功尊長等）", "action": "州縣限一月內審解，府州臬司督撫各限十日審轉具題", "modals": ["必须", "时限"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    {"item_id": "02-061", "type": "时限型", "subject": "承審逾限", "action": "初參分限之外遲延不及一月罰俸三個月，一月以上罰俸一年；二參統限屆滿再限四個月，如再逾限查參革職", "modals": ["必须", "时限"], "condition": "州縣以人犯到案之日起限", "object": "", "purpose": "", "punishment": "罰俸/降級/革職", "confidence": "high"},
    {"item_id": "02-061", "type": "时限型", "subject": "審案展限", "action": "開棺檢驗另扣審限；查捕蝗蝻勘災監賑勘河防險公出准扣日期；正犯要證患病具報准展限一個月", "modals": ["允许"], "condition": "限內實難完結者於分限內申詳督撫分別題咨展限", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 02-062 為百姓省錢
    {"item_id": "02-062", "type": "禁止型", "subject": "棍蠹", "action": "禁教唆：戶婚田土錢債及一切口角細故，棍蠹從中挑唆包告包准", "modals": ["禁止"], "condition": "", "object": "百姓", "purpose": "教唆之害：借債賣田案猶未結傾家蕩產", "punishment": "", "confidence": "high"},
    {"item_id": "02-062", "type": "禁止型", "subject": "刁民", "action": "杜歧控：今日在縣丞衙門控告，明日在巡檢衙門控告，又明日在典史武弁衙門控告", "modals": ["禁止"], "condition": "", "object": "良民", "purpose": "此處差役甫去彼處差役又來，良民之家安得不破", "punishment": "", "confidence": "high"},
    {"item_id": "02-062", "type": "义务型", "subject": "規費", "action": "裁規費：費在宅門以內者必須裁革淨盡，費在宅門以外者弊去太甚毌令放膽肆行", "modals": ["必须"], "condition": "衙門八字開有理無錢莫進來", "object": "", "purpose": "事事索費人人索費", "punishment": "", "confidence": "high"},
    {"item_id": "02-062", "type": "程序型", "subject": "核稿時", "action": "只應摘傳緊要人証，其無關緊要者概從節刪", "modals": ["必须"], "condition": "原告將素有嫌隙或家道殷實絕不與本案相干者混列詞尾", "object": "", "purpose": "若不節刪便中其拖累訛詐之計", "punishment": "", "confidence": "high"},
    {"item_id": "02-062", "type": "程序型", "subject": "標差", "action": "每案只標差兩名，勿多", "modals": ["宜"], "condition": "湖北州縣竟有一案標差十名八名者", "object": "", "purpose": "少標差則百姓少花錢", "punishment": "", "confidence": "high"},
    {"item_id": "02-062", "type": "义务型", "subject": "詞訟", "action": "快結案：早結一日之案即早釋一日之累，即少花一日之費", "modals": ["必须"], "condition": "拖延日久花錢愈多，富者必窮窮者必死", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 02-063 代書
    {"item_id": "02-063", "type": "程序型", "subject": "到任之初", "action": "嚴諭代書據實書寫，不准增減；狀內每一格眼祇書一字不准雙行疊寫；呈尾註明依口代書字樣", "modals": ["必须", "不准"], "condition": "民閒詞訟以小為大增輕作重，非因訟師教唆即由代書架捏", "object": "代書", "purpose": "防架捏", "punishment": "", "confidence": "high"},
    # 02-064 三八放告
    {"item_id": "02-064", "type": "程序型", "subject": "命盜鬪傷搶親等案", "action": "擇其尤要者酌定條款刋刻宣示准其隨時喊稟，或於大堂懸鑼准告者鳴鑼官聞聲立即訊辦；尋常案件定於三八放告日當堂收呈，此外各日切勿濫收", "modals": ["宜", "必须", "切勿"], "condition": "", "object": "", "purpose": "放告之期外有親隣勸解可息訟；隨時收呈較為快便", "punishment": "", "confidence": "high"},
    # 02-065 傳詞萬不可受
    {"item_id": "02-065", "type": "禁止型", "subject": "傳詞規費", "action": "萬不可受", "modals": ["禁止"], "condition": "傳進之詞有准無駁，即或十分無理亦必一面駁詰一面姑准", "object": "傳詞", "purpose": "開刁民訛詐之風釀良民破家之痛；果負屈可候告期具控或攔輿喊稟", "punishment": "", "confidence": "high"},
    # 02-066 喊冤
    {"item_id": "02-066", "type": "程序型", "subject": "喊冤者", "action": "無論有呈詞與否均應即刻問供，不可令差役驅逐；因打傷喊冤者尤須速問", "modals": ["必须", "不可"], "condition": "", "object": "", "purpose": "恐傷重致死未取生供；如必須呈詞備案則問供之後再令補具", "punishment": "", "confidence": "high"},
    # 02-067 呈詞朦混須駁詰
    {"item_id": "02-067", "type": "程序型", "subject": "呈狀內敘事不詳年月日者、婚姻無媒証錢債無保人者", "action": "數詞時須加駁詰", "modals": ["必须"], "condition": "多係已往之事故隱其月日以圖朦混", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 02-068 不准之詞勿擲還
    {"item_id": "02-068", "type": "程序型", "subject": "不准之呈詞", "action": "不必當堂擲還，收詞時將所以不准之故當堂明白曉諭，仍將駁語明白批示發房備案", "modals": ["不必", "必须"], "condition": "奸民詐偽百出，擲還則衙門內無案可稽", "object": "", "purpose": "息事安民；異日更改情節另作新詞有案可稽", "punishment": "", "confidence": "high"},
    # 02-069 收詞時呈驗印契勿附卷
    {"item_id": "02-069", "type": "程序型", "subject": "收詞時有呈驗印契者", "action": "驗明後即刻發還，諭令臨審時再行呈驗，仍於收詞簿內註明印契幾張當堂發還字樣；審結後契據等項當堂發還", "modals": ["必须"], "condition": "", "object": "印契", "purpose": "一經附卷則內而家人外而經承無人不需索", "punishment": "", "confidence": "high"},
    # 02-070 放告收詞不必當堂批示
    {"item_id": "02-070", "type": "程序型", "subject": "放告收詞", "action": "牧令自應當堂親自收呈即時批示；初試為吏者退堂後與幕友講求再行批示，務於收詞之次日批示", "modals": ["宜", "必须"], "condition": "批發遲則書差棍蠹因緣為奸，甚有賄買批語之說", "object": "", "purpose": "破莠民之膽；批示遲則增原告之冤壯被告之膽", "punishment": "", "confidence": "high"},
    # 02-071 呈詞批語榜示宜速
    {"item_id": "02-071", "type": "程序型", "subject": "呈詞批語", "action": "本官核定批語之後即照副狀填榜，俟榜發後再謄入正狀", "modals": ["宜"], "condition": "輾轉需時累人久候，且恐無心者漏洩有心者賄賣", "object": "", "purpose": "狀榜可期迅速", "punishment": "", "confidence": "high"},
    # 02-072 原告久不呈催
    {"item_id": "02-072", "type": "程序型", "subject": "原告無故兩月不到", "action": "例應註銷；被告人傳未到原告又久不呈催者亦應即註銷", "modals": ["应该"], "condition": "多係兩造不願終訟或已在鄉間私和", "object": "", "purpose": "如有難銷之案原告必定復控，俟復控時再為差喚", "punishment": "", "confidence": "high"},
    # 02-073 和息
    {"item_id": "02-073", "type": "程序型", "subject": "已准之詞", "action": "即應喚來審訊，實則究治虛則坐誣，不許告息；親友調處可歸和睦者聽斷以法調處以情", "modals": ["必须"], "condition": "劉說杜誣告，汪說睦族鄰", "object": "", "purpose": "一准告息則訟棍逆知狀可息銷便敢放心告狀", "punishment": "", "confidence": "high"},
    # 02-075 看卷
    {"item_id": "02-075", "type": "义务型", "subject": "審案", "action": "須看卷不可厭煩：先看原告控詞命意，次看被告訴詞，再看原被催詞；情節煩多即將緊要處摘錄開單臨審照單研訊", "modals": ["必须"], "condition": "案已多年兩造具呈多次自相矛盾者居多", "object": "卷宗", "purpose": "將矛盾處一一摘出即可從此折服，以子之矛刺子之盾", "punishment": "", "confidence": "high"},
    # 02-076 說官話
    {"item_id": "02-076", "type": "义务型", "subject": "審理詞訟", "action": "須說官話", "modals": ["必须"], "condition": "若不說官話則問官雖說得有情有理百姓終茫然莫解", "object": "", "purpose": "官民上下語言不通必致吏胥從中代為傳達，添飾假借百弊叢生", "punishment": "", "confidence": "high"},
    # 02-077 曉土音
    {"item_id": "02-077", "type": "义务型", "subject": "審理詞訟", "action": "須曉土音；到任時雇覓村童專操土音留心體問", "modals": ["必须"], "condition": "各處方言多難猝解", "object": "", "purpose": "下情不能上達是非曲直從何剖斷；勢必令差役傳達，愚者傳錯伶者增減", "punishment": "", "confidence": "high"},
    # 02-078 臨之以莊
    {"item_id": "02-078", "type": "义务型", "subject": "有司問案", "action": "必須臨之以莊，問姦情案語氣尤須莊重", "modals": ["必须"], "condition": "", "object": "", "purpose": "稍涉輕薄則損威失體", "punishment": "", "confidence": "high"},
    # 02-079 勿以穢言罵百姓
    {"item_id": "02-079", "type": "禁止型", "subject": "理訟", "action": "勿以穢言罵百姓；民果有罪敲之撲之，何必以穢言罵其父母", "modals": ["禁止"], "condition": "", "object": "百姓", "purpose": "堂皇之上如村童然尚復成何體統", "punishment": "", "confidence": "high"},
    # 02-080 審案與辦案不同
    {"item_id": "02-080", "type": "义务型", "subject": "辦案", "action": "宜簡淨；審案宜詳細", "modals": ["宜"], "condition": "", "object": "", "purpose": "辦案不簡淨則情節支離引例時必難確切；審案不詳細則情節遺漏斷案後必多翻控", "punishment": "", "confidence": "high"},
    # 02-081 耐煩
    {"item_id": "02-081", "type": "义务型", "subject": "審案", "action": "須耐煩，多問則事之原委曲折皆明", "modals": ["必须"], "condition": "戶婚田土等項案件一堂可結者居多", "object": "", "purpose": "不耐煩則門丁乘機詐索書役乘機指撞訟師乘機播弄，本小事釀成大事", "punishment": "", "confidence": "high"},
    # 02-082 盡其辭而折之
    {"item_id": "02-082", "type": "义务型", "subject": "審案", "action": "須令兩造傾筐倒篋暢所欲言，待其詞畢而駁詰之", "modals": ["必须"], "condition": "不許其開口則有問無答，聽而不聞", "object": "", "purpose": "愚民自以為是者盡言則差處自見；刁民言多必失，真情出矣", "punishment": "", "confidence": "high"},
    # 02-083 不許書差教供
    {"item_id": "02-083", "type": "禁止型", "subject": "審案時書差", "action": "不可多嘴，不許點頭搖頭賣弄眼色", "modals": ["禁止"], "condition": "", "object": "", "purpose": "恐其受賕教供", "punishment": "", "confidence": "high"},
    # 02-084 不許家丁多言
    {"item_id": "02-084", "type": "禁止型", "subject": "值堂家丁", "action": "不許多言亂語，不許公然喝令皁隸責打", "modals": ["禁止"], "condition": "", "object": "", "purpose": "坐者一問官立者又一問官，刁生劣監藉此上控", "punishment": "", "confidence": "high"},
    # 02-085 本案用何律例須考究明白
    {"item_id": "02-085", "type": "义务型", "subject": "自理詞訟", "action": "本案情節應用何律何例必須考究明白，再就本地風俗準情酌理而變通之", "modals": ["必须"], "condition": "原不必事事照例", "object": "", "purpose": "庶不與律例十分相背；否則上控之後奉批錄案無詞可措", "punishment": "", "confidence": "high"},
    # 02-086 從輕擬辦亦應澈底訊明
    {"item_id": "02-086", "type": "程序型", "subject": "情有可原之案", "action": "不妨原情而略法，但必須澈底訊明", "modals": ["必须"], "condition": "因擬從輕便不究問實情", "object": "", "purpose": "否則彼不以為法外之仁，且謂官受其欺，必圖翻異", "punishment": "", "confidence": "high"},
    # 02-087 勿為詐偽所賣
    {"item_id": "02-087", "type": "禁止型", "subject": "官", "action": "勿為詐偽所賣，須識其偽", "modals": ["禁止"], "condition": "人心不古詐偽多端", "object": "", "purpose": "郭純哭母撒飯、王燧猫犬互乳、假活佛絕粒皆工於作偽，不識其偽便為所賣", "punishment": "", "confidence": "high"},
]
