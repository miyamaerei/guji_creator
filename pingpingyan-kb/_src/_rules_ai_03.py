# -*- coding: utf-8 -*-
"""《平平言》规则源数据（卷03 全量）——AI 判定装填。"""

RECORDS = [
    # 03-001 據筆跡涉訟須處處留神
    {"item_id": "03-001", "type": "义务型", "subject": "據筆跡斷案", "action": "必須處處留神切勿稍涉大意，察弊之法大略有九", "modals": ["必须", "禁止"], "condition": "券約等項無一不可詐偽", "object": "券約", "purpose": "防挖補/驗紙色/對筆跡/查印信/考年月/辨界址/稽價值/核姓名/察情理", "punishment": "", "confidence": "high"},
    {"item_id": "03-001", "type": "程序型", "subject": "黏呈契據借約", "action": "須於緊要處紙背蓋用圖記，並於詞內明白批示以杜訟源", "modals": ["必须"], "condition": "蠹吏挖補之計更毒", "object": "契據", "purpose": "杜訟源", "punishment": "", "confidence": "high"},
    # 03-002 鄉愚不通文理須逐細分剖
    {"item_id": "03-002", "type": "义务型", "subject": "鄉愚不通文理據筆迹涉訟者", "action": "須為之講解明晰，講解時越淺越好越俗越好，就其所執之據逐細分剖務令明白", "modals": ["必须"], "condition": "往往誤會錯解自以為是，若不講解明晰雖死不服", "object": "鄉愚", "purpose": "務令明白而後已", "punishment": "", "confidence": "high"},
    # 03-003 據譜涉訟須細核
    {"item_id": "03-003", "type": "义务型", "subject": "據族譜涉訟", "action": "必須細心查核，不特核其所載控爭之處而且從頭至尾細閱數過", "modals": ["必须"], "condition": "譜係家藏不難假造", "object": "族譜", "purpose": "得其瑕處就其瑕而攻之", "punishment": "", "confidence": "high"},
    # 03-004 隔別研記
    {"item_id": "03-004", "type": "程序型", "subject": "詞訟聽審者（原告被告干證鄉約保正）", "action": "每項不止一人必須隔別審訊，此人所供勿令彼人聞知", "modals": ["必须"], "condition": "即或在外串通亦必有串通不到之處", "object": "", "purpose": "所供情節不至依樣葫蘆", "punishment": "", "confidence": "high"},
    # 03-005 據證
    {"item_id": "03-005", "type": "义务型", "subject": "案情有證佐者", "action": "須心入其中詳細研求，以事物為證便是鐵板註腳", "modals": ["必须"], "condition": "證以人尚恐有串通之弊", "object": "證佐", "purpose": "明明有事物可證不致熟視無覩", "punishment": "", "confidence": "high"},
    # 03-006 無證之中尋出確證
    {"item_id": "03-006", "type": "义务型", "subject": "疑難案件本無證據者", "action": "須於無證之中尋一確證", "modals": ["必须"], "condition": "刁民恃其無證任意爭執嘵嘵不休", "object": "", "purpose": "服其心而關其口", "punishment": "", "confidence": "high"},
    # 03-007 察情
    {"item_id": "03-007", "type": "义务型", "subject": "凡事", "action": "細心體察情理", "modals": ["必须"], "condition": "作偽者往往出乎情理之外", "object": "", "purpose": "雖不中必不遠", "punishment": "", "confidence": "high"},
    # 03-008 用譎
    {"item_id": "03-008", "type": "程序型", "subject": "證難憑情難見之案", "action": "發奸摘伏莫妙於用譎，因譎而得真情", "modals": ["宜"], "condition": "譎雖非正", "object": "", "purpose": "懾服奸慝又免累及無辜，仍不失為正道", "punishment": "", "confidence": "high"},
    # 03-009 用譎宜密
    {"item_id": "03-009", "type": "义务型", "subject": "用譎", "action": "宜密不可漏洩", "modals": ["必须", "禁止"], "condition": "趙廣鉤距之妙在鉤尤在距", "object": "", "purpose": "若可窺則可遁矣", "punishment": "", "confidence": "high"},
    # 03-010 兩全之法
    {"item_id": "03-010", "type": "程序型", "subject": "兩造皆是未可偏非之案", "action": "須得兩全之法", "modals": ["必须"], "condition": "是非本不容並立然亦有兩造皆是者", "object": "", "purpose": "息訟端", "punishment": "", "confidence": "high"},
    # 03-011 彼此換易
    {"item_id": "03-011", "type": "程序型", "subject": "爭分財田產不均之案", "action": "取具兩造切實供狀，令其彼此掉換所爭之產", "modals": ["宜"], "condition": "兩造供狀既已結實", "object": "", "purpose": "如願相償自不能再生枝節", "punishment": "", "confidence": "high"},
    # 03-012 富民與貧民搆訟
    {"item_id": "03-012", "type": "义务型", "subject": "富民與貧民搆訟", "action": "不可偏袒富民亦不可故抑富民，但當問其枉不枉不當問其富不富", "modals": ["不可", "禁止"], "condition": "偏袒與故抑皆矯枉過正", "object": "", "purpose": "果不枉夷齊無生理，果枉陶朱無死法", "punishment": "", "confidence": "high"},
    # 03-013 錢債
    {"item_id": "03-013", "type": "义务型", "subject": "錢債券約分明者", "action": "自應照律追償", "modals": ["必须"], "condition": "告貸之手札不足為憑，以券約為憑", "object": "", "purpose": "若不追償則富民不敢放債，一遇歲饑小民束手", "punishment": "", "confidence": "high"},
    {"item_id": "03-013", "type": "禁止型", "subject": "私放錢債", "action": "每月不得過三分，年月雖多不過一本一利", "modals": ["禁止"], "condition": "年年納利本錢未還者不得統計已還之利而算一本一利", "object": "錢債", "purpose": "", "punishment": "", "confidence": "high"},
    {"item_id": "03-013", "type": "义务型", "subject": "利息過多或負者實係無力", "action": "斷令酌減利息，或勸借主減本歸結", "modals": ["应该"], "condition": "所納之利已經子過其母", "object": "", "purpose": "取息過多未免不公", "punishment": "", "confidence": "high"},
    # 03-014 勿忽細故
    {"item_id": "03-014", "type": "义务型", "subject": "戶婚田土錢債偷竊等細故之案", "action": "須經心辦理，不可因細故而不經心", "modals": ["必须"], "condition": "一州一縣之中重案少細故多", "object": "", "purpose": "百姓視之則利害切己", "punishment": "", "confidence": "high"},
    # 03-015 踏勘
    {"item_id": "03-015", "type": "义务型", "subject": "踏勘山場田地墳墓等事", "action": "不可草率，如遇途路崎嶇亦必親身履勘形勢界址", "modals": ["必须"], "condition": "", "object": "", "purpose": "踏勘時了然於心庶堂審時了然於口", "punishment": "", "confidence": "high"},
    # 03-016 棠陰聽訟
    {"item_id": "03-016", "type": "程序型", "subject": "州縣因公下鄉遇有兩造控籲無甚轇轕者", "action": "就近剖斷", "modals": ["宜"], "condition": "", "object": "", "purpose": "最為省事，胥役何緣為姦訟師何所措手", "punishment": "", "confidence": "high"},
    # 03-017 鬬毆先下手者宜重治
    {"item_id": "03-017", "type": "处罚型", "subject": "民有鬬毆者", "action": "本罪之外別令先下手者出錢以與後應者", "modals": ["应该"], "condition": "無賴之徒不畏杖責", "object": "", "purpose": "靳財不甘輸錢終日紛爭相視無敢先下手者", "punishment": "", "confidence": "high"},
    # 03-018 原告審虛加倍懲治
    {"item_id": "03-018", "type": "处罚型", "subject": "原告審虛", "action": "加倍懲治", "modals": ["必须"], "condition": "原告捏詞陷害非挾嫌即圖詐", "object": "", "purpose": "挽回刁風，誣告加三等律有明文", "punishment": "加倍懲治", "confidence": "high"},
    # 03-019 二競同卡
    {"item_id": "03-019", "type": "程序型", "subject": "二競俱禁者", "action": "令競主與之同匣", "modals": ["宜"], "condition": "若令別牢則獄吏受賂傳狀遞信息", "object": "", "purpose": "互相譏察猶有忌憚，同匣日久解讎為和", "punishment": "", "confidence": "high"},
    # 03-020 證佐受賄
    {"item_id": "03-020", "type": "禁止型", "subject": "證佐受賄幫話或供詞含糊者", "action": "必須嚴懲，證佐不言實情照律本應懲治何况受賄", "modals": ["必须"], "condition": "受原告之賄則幫原告說話受被告之賄則幫被告說話", "object": "證佐", "purpose": "", "punishment": "嚴懲", "confidence": "high"},
    # 03-021 訟師可畏（说理示范，不抽规则）
    # 03-022 訟師未獲須恐以虛聲
    {"item_id": "03-022", "type": "义务型", "subject": "唆訟訟師", "action": "須問明姓名年貌住址嚴拏究懲；拏不到案者遇因公下鄉直言某人唆訟拏到必應嚴懲", "modals": ["必须"], "condition": "兩造均不願終訟而訟師慾壑未盈不肯罷手", "object": "訟師", "purpose": "該訟師聞之必畏懼必斂迹必不敢再入城", "punishment": "嚴懲", "confidence": "high"},
    # 03-023 訟師已獲須傷其顏面
    {"item_id": "03-023", "type": "程序型", "subject": "拏到之訟師", "action": "責懲管押，遇審案時提出鎖柱示眾令其鵠立看審", "modals": ["宜"], "condition": "訟師在外每以手段自矜", "object": "訟師", "purpose": "傷其顏面則人不信服", "punishment": "責懲管押", "confidence": "high"},
    # 03-024 審狂人
    {"item_id": "03-024", "type": "义务型", "subject": "狂人訴事", "action": "須耐煩細問", "modals": ["必须"], "condition": "狂者語無倫次最討人厭惡", "object": "", "purpose": "雖語言雜亂無次然時有可曉者", "punishment": "", "confidence": "high"},
    # 03-025 審啞子
    {"item_id": "03-025", "type": "程序型", "subject": "病瘖不能言者", "action": "取顙叫子令作聲以辨其一二，乃獲伸", "modals": ["宜"], "condition": "啞子本不能言有無冤枉無從審訊", "object": "", "purpose": "啞子亦可取供", "punishment": "", "confidence": "high"},
    # 03-026 禁婦女出頭告狀
    {"item_id": "03-026", "type": "禁止型", "subject": "家有夫男不親身具控而令婦女出頭告狀者", "action": "無論有理無理一概不准，仍將婦女掌責", "modals": ["禁止"], "condition": "明係捏詞圖詐為將來審虛地步", "object": "", "purpose": "凡有夫男之家自不敢令婦女輕於嘗試", "punishment": "掌責", "confidence": "high"},
    # 03-027 勿輕易傳訊婦女
    {"item_id": "03-027", "type": "禁止型", "subject": "案內牽涉婦女", "action": "非萬不得已不可輕易傳訊，寡婦閨女尤不可令其出頭露面對簿公堂", "modals": ["禁止"], "condition": "", "object": "婦女", "purpose": "人之顏面所繫即己之陰騭所關", "punishment": "", "confidence": "high"},
    # 03-028 審訊婦女宜莊重
    {"item_id": "03-028", "type": "义务型", "subject": "審訊婦女", "action": "不得喚近案前低聲悄問，退去時不得定睛目送", "modals": ["不得"], "condition": "公堂之上為士民觀瞻所繫", "object": "婦女", "purpose": "恐觀者竊笑傳作話柄", "punishment": "", "confidence": "high"},
    # 03-029 為政有體
    {"item_id": "03-029", "type": "义务型", "subject": "為政", "action": "須有體統，不可任意妄為", "modals": ["必须"], "condition": "以意為之輕薄難膺民社", "object": "", "purpose": "犯姦者枷律也兩人共荷之非政體也", "punishment": "撤委勒令告病", "confidence": "high"},
    # 03-030 婦女勿輕交官媒
    {"item_id": "03-030", "type": "禁止型", "subject": "婦女", "action": "非犯姦非犯命案不可輕易交官媒看管", "modals": ["禁止"], "condition": "官媒需索凌虐與班房看役同", "object": "官媒", "purpose": "引誘賣姦逼勒賣姦則官媒所獨也", "punishment": "", "confidence": "high"},
    # 03-031 勿掌責閨女
    {"item_id": "03-031", "type": "程序型", "subject": "牽涉閨女必須責懲之案", "action": "以手板授其父兄飭令當堂責打手心，不令差役掌嘴捉手", "modals": ["必须"], "condition": "閨女被官責打已許字者辱及夫家未許字者誰為聘問", "object": "閨女", "purpose": "顏面所繫即性命所關", "punishment": "", "confidence": "high"},
    # 03-032 強姦
    {"item_id": "03-032", "type": "义务型", "subject": "強姦案件", "action": "必須照律嚴辦", "modals": ["必须"], "condition": "州縣有維持風化之責", "object": "", "purpose": "挽回惡俗", "punishment": "絞監候", "confidence": "high"},
    {"item_id": "03-032", "type": "义务型", "subject": "審理強姦案件", "action": "存不得一毫成見著不得一毫粗心，防串捏，傷痕衣服只可用作印證不能據為鐵憑", "modals": ["不得"], "condition": "強姦罪名甚重真偽難分，飾強為和與諱和為強並存", "object": "", "purpose": "以真為偽無以懾姦匪之心，以偽為真未免中刁徒之計", "punishment": "", "confidence": "high"},
    # 03-033 調姦未成宜速拘
    {"item_id": "03-033", "type": "程序型", "subject": "報調姦未成圖姦未成強姦未成者", "action": "必須即刻差拘嚴懲，切不可因其未成便視為無關緊要任意延擱", "modals": ["必须", "禁止"], "condition": "", "object": "", "purpose": "以快貞婦之心，恐延擱日久本婦懷忿自盡", "punishment": "嚴懲", "confidence": "high"},
    # 03-034 因姦致死人命
    {"item_id": "03-034", "type": "义务型", "subject": "因姦致死人命", "action": "必應擬抵，切不可聽救生不救死之邪說", "modals": ["必须", "禁止"], "condition": "", "object": "", "purpose": "致死者含冤地下", "punishment": "擬抵", "confidence": "high"},
    # 03-035 以姦為盜勿深究
    {"item_id": "03-035", "type": "允许型", "subject": "豐厚之家涉曖昧不得已以所獲作為竊賊送官者", "action": "雖知其情勿發其隱，如犯者逞刁供詞挾制切勿輕聽速為責釋完案", "modals": ["允许", "禁止"], "condition": "雖以姦為盜罪應滿杖", "object": "", "purpose": "律設大法禮順人情，彼既自惜其顏面官何苦一定傷其顏面", "punishment": "", "confidence": "high"},
    # 03-036 婦人誕育不可概論常理（知识说理，不抽规则）
    # 03-037 男化女女化男（知识说理，不抽规则）
    # 03-038 老人之子（说理示范，不抽规则）
    # 03-039 命盜不必諱
    {"item_id": "03-039", "type": "义务型", "subject": "命盜", "action": "不可諱亦不必諱，不如據實詳報", "modals": ["禁止", "必须"], "condition": "諱命諱盜例應革職且係私罪不准抵銷", "object": "", "purpose": "諱命則兇徒漏網死者含冤，諱盜則匪徒得志良民受害；兩害相形取其輕", "punishment": "革職", "confidence": "high"},
    # 03-040 相驗命案勿多帶人役
    {"item_id": "03-040", "type": "程序型", "subject": "相驗命案", "action": "例止許隨帶仵作一名刑書一名皁隸二名，多帶人役便是違例", "modals": ["必须", "禁止"], "condition": "人役過多約束難周搔擾愈甚", "object": "", "purpose": "", "punishment": "違例", "confidence": "high"},
    # 03-041 因公下鄉勿帶家人
    {"item_id": "03-041", "type": "程序型", "subject": "因公下鄉", "action": "帶茶房一名伺候足矣，跟班家人可以不帶；勘驗強竊盜案帶招房一名，相驗命案帶仵作一名招房一名", "modals": ["宜"], "condition": "茶房需索不過草鞋錢跟班家人則需索靴子錢", "object": "", "purpose": "省擾累", "punishment": "", "confidence": "high"},
    # 03-042 驗案夫馬費
    {"item_id": "03-042", "type": "程序型", "subject": "相驗命案僕從胥役夫馬伙食等費", "action": "由紳商捐資文善堂生息作為經費，名數日給工飯錢數一一酌定通稟立案泐石，由縣給印諭飭堂照發，不准向屍親兇手地鄰人等需索分文", "modals": ["必须", "禁止"], "condition": "向均取給於差役展轉株連肆行訛詐，一案可破數十家中人之產", "object": "夫馬費", "purpose": "例意重在恤民，以免藉口詐索", "punishment": "", "confidence": "high"},
    # 03-043 初驗不可草率
    {"item_id": "03-043", "type": "义务型", "subject": "相驗屍傷", "action": "務須親驗不可遠立，務須細驗不可草率", "modals": ["必须"], "condition": "命案全憑初驗，初驗不實屍親刁控兇手狡賴", "object": "屍傷", "purpose": "稟請開驗屍遭蒸刷之慘", "punishment": "", "confidence": "high"},
    {"item_id": "03-043", "type": "程序型", "subject": "相驗時掩穢氣", "action": "站立上風，或用新布小手巾醮燒酒掩鼻，麝香切不可用", "modals": ["宜", "禁止"], "condition": "恐穢氣薰觸", "object": "", "purpose": "穢氣自不能入", "punishment": "", "confidence": "high"},
]
