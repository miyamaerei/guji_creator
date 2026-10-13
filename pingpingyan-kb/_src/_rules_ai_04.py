# -*- coding: utf-8 -*-
"""《平平言》规则源数据（卷04 全量）——AI 判定装填。"""

RECORDS = [
    # 04-001 路弊命案
    {"item_id": "04-001", "type": "程序型", "subject": "路斃命案相驗無傷者", "action": "儘可在屍場了結，地鄰地主屍場問供之後即可省釋無庸到城候訊；報案之後先著地保傳諭地主地鄰，夫馬飯食由官給發斷不騷擾", "modals": ["宜"], "condition": "愚民最怕命案官未下鄉之先往往避匿", "object": "", "purpose": "案係路斃一訊即結斷不牽連，民必信從", "punishment": "", "confidence": "high"},
    # 04-002 傷痕分別真偽
    {"item_id": "04-002", "type": "程序型", "subject": "相驗之法", "action": "莫確於比：肉傷以此之色比彼之色，骨傷以左比右以上比下，以今日乍見之形痕比前此經見之形痕", "modals": ["必须"], "condition": "初登仕版認傷必不的確", "object": "屍傷", "purpose": "比則易見比則難欺", "punishment": "", "confidence": "high"},
    {"item_id": "04-002", "type": "程序型", "subject": "分辨真傷假傷", "action": "真傷色活有癊腳暈痕顏色自深而淺，假傷色呆紅紫堆積；真傷堅硬假傷虛輭；真服毒以足色銀釵試探作青黑色皁角水揩洗不變，死後假作中毒皮肉骨只作黃白色；活人被殺皮肉緊縮四畔有血癊，死後加刃皮不緊縮血不灌癊；自刎者執刀之手必輭，別人執刀戳殺者手直不能彎曲；自縊痕色紫赤或黑淤色，被人勒死假作自縊痕色必白且無血癊；生前溺死口鼻有水沫肚腹脹腳底皺白，死後掉水內口鼻無水沫肚腹不脹", "modals": ["必须"], "condition": "", "object": "", "purpose": "洗冤錄分別真傷偽傷生前死後不外兩相比對", "punishment": "", "confidence": "high"},
    # 04-003 落水情形不一
    {"item_id": "04-003", "type": "义务型", "subject": "落水命案", "action": "全靠細心推鞫四面印證，不可執一而論", "modals": ["必须"], "condition": "投水手握眼合落水手開眼微開乃至當不易之理，然失足/被推/被趕逼情形不一，頭下腳下均不得而知", "object": "", "purpose": "分別自行失足/被人推入/被人趕逼入水", "punishment": "", "confidence": "high"},
    # 04-004 命案七殺
    {"item_id": "04-004", "type": "义务型", "subject": "審理命案", "action": "須將七殺分別清楚乃有把握：謀殺/故殺/鬬殺/戲殺/誤殺/擅殺/過失殺", "modals": ["必须"], "condition": "今人作吏多年問以七殺茫然不解", "object": "", "purpose": "謀殺先設殺人之計；故殺臨時有意欲殺非人所知；鬬殺兩人相對而毆本無殺人之意；戲殺以堪殺人之事彼此言明和同相戲；誤殺差錯失手誤中在旁之人；擅殺有罪之人不送官而自殺之；過失殺耳目所不到思慮所不及", "punishment": "", "confidence": "high"},
    # 04-005 防命犯翻異
    {"item_id": "04-005", "type": "义务型", "subject": "命案犯雖供認殺人", "action": "須將下手情形逐細推敲以防翻異", "modals": ["必须"], "condition": "刁民譸張為幻命案尤甚", "object": "", "purpose": "若不得實情則後必翻異而姦人計得矣；推覈之際戒在疏略", "punishment": "", "confidence": "high"},
    # 04-006 疑獄勿遽定爰書
    {"item_id": "04-006", "type": "义务型", "subject": "獄苟可疑", "action": "雖囚無冤詞亦未可遽定爰書", "modals": ["禁止"], "condition": "易曰君子以議獄緩死", "object": "", "purpose": "慎重民命之意", "punishment": "", "confidence": "high"},
    # 04-007 勿出人罪以求福報
    {"item_id": "04-007", "type": "禁止型", "subject": "法家", "action": "勿惑於罪福報應之說喜出人罪以求福報", "modals": ["禁止"], "condition": "死者不可復生，爰書不遽定乃慎重民命非故出人罪救生不救死", "object": "", "purpose": "使無罪者不得直有罪倖免是乃所以為惡耳，何福報之有", "punishment": "", "confidence": "high"},
    # 04-008 冤鬼附體報仇（说理叙事，不抽规则）
    # 04-009 捕役之弊
    {"item_id": "04-009", "type": "禁止型", "subject": "捕役", "action": "不得豢賊分肥/縱賊殃民/需索事主/妄拏平民/私刑弔拷/囑賊誣扳/私起贓物/侵剝盜贓", "modals": ["禁止"], "condition": "賊以捕為護身之符捕以賊為養身之具，捕賊一氣", "object": "", "purpose": "開花誣扳之害，無辜之民憑空枉陷", "punishment": "", "confidence": "high"},
    # 04-010 馭捕之法
    {"item_id": "04-010", "type": "义务型", "subject": "養捕", "action": "明定章程捐資養捕：每捕按月給錢米、每緝一案給購線費、每破一案按罪名輕重給賞項、每解一案按人數多寡給解費", "modals": ["必须"], "condition": "捕役家無恆產額定工食無多，欲其不豢賊不誣良難矣", "object": "", "purpose": "服捕之心杜捕之口袪捕之弊得捕之力", "punishment": "", "confidence": "high"},
    {"item_id": "04-010", "type": "程序型", "subject": "比捕", "action": "遇有強竊案件立限緝拏逾限則比；捕役畏比妄拏無辜或拏獲正賊審有私刑誣扳等弊立即重處切勿稍寬", "modals": ["必须"], "condition": "平時既給養贍解案又不賠累仍不認真緝盜", "object": "", "purpose": "", "punishment": "重處", "confidence": "high"},
    # 04-011 以盜捕盜
    {"item_id": "04-011", "type": "程序型", "subject": "緝盜", "action": "以捕捕盜不如以盜捕盜：得偷盜酋長貰其罪令致諸盜以自贖", "modals": ["宜"], "condition": "張敞/段幻然/黃思湖皆以此法收效", "object": "", "purpose": "宥故盜以嚴新盜，令近盜以遏遠盜", "punishment": "", "confidence": "high"},
    # 04-012 夥盜姓名
    {"item_id": "04-012", "type": "程序型", "subject": "夥盜姓名", "action": "必須細鞫不可草率：逸盜年歲籍貫住處面貌記認逐一問明，詳載差票關文內；賊黨排行名目（趙老一錢老二等）須將的名訊問確實", "modals": ["必须"], "condition": "賊黨相呼多以排行最易影射", "object": "", "purpose": "庶同姓同名之人不至無辜受累", "punishment": "", "confidence": "high"},
    # 04-013 盜憑贓定
    {"item_id": "04-013", "type": "义务型", "subject": "盜案", "action": "盜憑贓定指其獲之真贓而言，眾盜到案後供指同夥分得某物殊難憑信", "modals": ["必须"], "condition": "事隔多日自己所分或能記憶眾人所分斷難備記", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-014 贓真賊不真
    {"item_id": "04-014", "type": "义务型", "subject": "贓經主認之案", "action": "正賊無疑然閒有贓真而賊不真者，若不留心便成冤獄", "modals": ["必须"], "condition": "京師遺冊一案：起獲贓物既係本案之贓埋贓處所又出自諸少之口，旁人與諸少自以為不冤，實則大謬不然", "object": "", "purpose": "鞫獄者如之何弗慎", "punishment": "", "confidence": "high"},
    # 04-015 誤買賊贓
    {"item_id": "04-015", "type": "程序型", "subject": "誤買賊贓者", "action": "只令保甲查起，票尾硃書只將誤買贓物全數呈繳買贓之人不必到案", "modals": ["宜"], "condition": "誤買賊贓情本可原，一經差拘家立破矣", "object": "", "purpose": "杜嚇詐而安良善", "punishment": "", "confidence": "high"},
    # 04-016 盜窩
    {"item_id": "04-016", "type": "义务型", "subject": "緝盜", "action": "辦十盜不如辦一窩，以窩者盜之源無窩則盜不能託足也；窩家必在附近（與被盜處所相去不過五里十里至遠二三十里）", "modals": ["宜"], "condition": "行刦於三十里外一來一去便是七八十里天已明追者至矣", "object": "盜窩", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-017 審部駁案
    {"item_id": "04-017", "type": "义务型", "subject": "部駁之案", "action": "可頂則頂不可頂則遵駁改正，不必遷就亦不必固執", "modals": ["应该"], "condition": "恩施捉姦殺死案頂覆照准、蘄水罷考案半頂半遵照准", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-018 退堂不可草率
    {"item_id": "04-018", "type": "程序型", "subject": "退堂時", "action": "不可草率：案如未結須將字據等項一一檢點；案如已結須將某人因何而勝某人因何而負明白曉諭諄諄誥誡", "modals": ["必须"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-019 招房錯漏情節
    {"item_id": "04-019", "type": "程序型", "subject": "審理案件緊要口供", "action": "全賴自己記憶；招房謄清送閱如有遺漏用硃筆添載、錯誤用硃筆塗改，遺漏錯誤太多即令另寫或逐一添入更正再令招房在內署謄正", "modals": ["必须"], "condition": "招房明白者不可多得且恐受賄徇情將情節故意錯漏", "object": "", "purpose": "犯證本已供明而招房錯漏本官自應更正，與改易供招之例不同", "punishment": "", "confidence": "high"},
    # 04-020 審結案件不必當堂書判
    {"item_id": "04-020", "type": "程序型", "subject": "審結案件", "action": "宜當堂硃書判語令兩造自讀或房書宣讀照硃判具遵結；問官筆下敏鈍不一者退堂後斟酌判語較為周妥", "modals": ["宜"], "condition": "若令差人帶兩造在外間出結則棍蠹挑撥書役高下其手", "object": "", "purpose": "供與結不至兩歧，將來翻異展卷瞭如指掌", "punishment": "", "confidence": "high"},
    # 04-021 判語須列榜
    {"item_id": "04-021", "type": "程序型", "subject": "斷案之後", "action": "將堂諭榜示頭門，其有關兩造永遠者鈔錄蓋印給兩造收執（但須防家丁索錢）", "modals": ["宜"], "condition": "兩造向承行書辦鈔錄堂諭往往任意需索", "object": "", "purpose": "需索之弊不禁自止", "punishment": "", "confidence": "high"},
    # 04-022 斷案錯誤須覆訊
    {"item_id": "04-022", "type": "义务型", "subject": "斷案之後訟者心未輸服懇請覆訊", "action": "即須細意推求虛心再鞫，如果錯誤便應改正並將所以錯誤之故明白曉諭", "modals": ["必须"], "condition": "人非聖賢孰能無過", "object": "", "purpose": "官果無私民自相諒，切不可迴護前非致負百姓", "punishment": "", "confidence": "high"},
    # 04-023 公事錯誤須改正
    {"item_id": "04-023", "type": "义务型", "subject": "公事錯誤", "action": "必須改正，自行檢舉處分亦可從減，切不可迴護前非致干重譴", "modals": ["必须", "禁止"], "condition": "自行檢舉例應革職者減為革留等", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-024 勿濫用非刑
    {"item_id": "04-024", "type": "禁止型", "subject": "問刑衙門", "action": "不得濫用非刑：例載刑具只有夾棍桚指枷號竹板鐵鎖杻鐐七項，擰耳跪鍊壓膝掌責亦准行用，此外小夾棍木棒棰聯枷大鎖竹板木架撐執懸弔敲踝針刺手指荊條擊背等皆非刑", "modals": ["禁止"], "condition": "問刑衙門原准用刑但不得濫用", "object": "", "purpose": "", "punishment": "私設非刑照違制例革職", "confidence": "high"},
    # 04-025 勿輕用夾棍
    {"item_id": "04-025", "type": "程序型", "subject": "夾棍", "action": "強盜竊盜人命及情罪重大案件例准夾訊，別項小事概不准濫用；非萬不得已不得輕用夾棍", "modals": ["禁止"], "condition": "", "object": "", "purpose": "", "punishment": "不應夾而夾及雖應夾而因夾致死並恣意疊夾致死者題參治罪", "confidence": "high"},
    # 04-026 枷號
    {"item_id": "04-026", "type": "程序型", "subject": "枷號", "action": "枷有輕重，輕罪人犯不得用重枷；罪應枷杖者應先枷後打不得先打後枷", "modals": ["禁止"], "condition": "", "object": "", "purpose": "", "punishment": "用重枷致死輕罪人犯本官應問滿徒不止革職", "confidence": "high"},
    # 04-027 掌嘴須護住耳門
    {"item_id": "04-027", "type": "程序型", "subject": "掌責時", "action": "須令皁隸以手護住耳門", "modals": ["必须"], "condition": "耳根係致命處所一擊即斃", "object": "", "purpose": "", "punishment": "漢陽令因掌打死一人致被參劾", "confidence": "high"},
    # 04-028 行杖須子細
    {"item_id": "04-028", "type": "程序型", "subject": "用刑時", "action": "須用皁隸搜檢恐腰帶褲帶擊有堅硬物件墊傷小腹；又須定睛細視恐皁役受囑以重刑毒打或不打腿而打腿彎或專用板頭或一板一拖", "modals": ["必须"], "condition": "竹杖有一定之制受刑有一定之處所謂法也", "object": "", "purpose": "", "punishment": "決不如法而致死者官應革職；於人虛怯處非法毆打致死者官問滿徒", "confidence": "high"},
    # 04-029 勿輕用笞杖
    {"item_id": "04-029", "type": "义务型", "subject": "治民", "action": "當養其廉恥，事至為之剖其曲直諭以理法；刑非甚不得已未可輕動", "modals": ["必须"], "condition": "不論事犯輕重平素良頑一概予杖，有終身含羞/不復顧惜/仇恨愈深子孫數代不能解釋者", "object": "", "purpose": "彼此之氣易平，不愧父母斯民之義", "punishment": "", "confidence": "high"},
    # 04-030 刑戒
    {"item_id": "04-030", "type": "义务型", "subject": "有用刑之責者", "action": "允宜熟讀深思呂新吾刑戒八章：五不打（老幼病衣食不繼人打我不打）/五不輕打（宗室官生員上司差人婦人）/五勿就打（人急人忿人醉遠路跑來喘氣）/五且緩打（我怒我醉我病不見真不能處分）/三莫又打（已桚已夾已枷）/三憐不打（盛寒酷暑佳辰令節人方傷心）/三應打不打（尊長與卑幼訟、百姓與衙門人訟、工役鋪行為修私衙或買辦自己物）/三禁打（禁重杖、禁從下打、禁佐貳非刑打）", "modals": ["必须"], "condition": "慈祥惻怛藹然仁者之言，思周慮密則仁而且智", "object": "", "purpose": "以平矜躁", "punishment": "", "confidence": "high"},
    # 04-031 寬待百姓嚴待書差
    {"item_id": "04-031", "type": "义务型", "subject": "有司", "action": "待百姓宜寬待書差宜嚴；書差作弊慣技有犯必懲（五必打：經承壓擱稿案/衙役捺延差票/仵作捏報傷痕/皁役行杖不如法/代書敘事不以實）", "modals": ["宜"], "condition": "刑戒八章仁者之言然亦有不可姑息者", "object": "", "purpose": "書差或者稍知斂迹", "punishment": "", "confidence": "high"},
    # 04-032 寬待良民嚴待莠民
    {"item_id": "04-032", "type": "义务型", "subject": "有司", "action": "待良民宜寬待莠民宜嚴，安良必先除莠", "modals": ["宜"], "condition": "刑戒八章勿就打且緩打非一概不打；若一味慈祥漫無區別則莠民玩法過甚", "object": "", "purpose": "國之有法如家有不肖子弟必須嚴加約束，愛之適以害之", "punishment": "", "confidence": "high"},
    # 04-033 避刑邪術
    {"item_id": "04-033", "type": "程序型", "subject": "避刑邪術（運氣符籙）", "action": "用小竹條數根去葉留枝令數人分持齊擊其肩背腿足必得實供；服藥架刑者俟其藥力過後再行刑訊", "modals": ["宜"], "condition": "符籙與運氣刑不能傷者以其心志專一，竹枝叢雜著膚不止一處則神氣散亂其術不靈", "object": "", "purpose": "屢試屢驗", "punishment": "", "confidence": "high"},
    # 04-034 班房內用活地板
    {"item_id": "04-034", "type": "程序型", "subject": "班房收押", "action": "良民賊犯必須分押不可漫無區別；應將四圍溝渠開濬深通、看役打掃潔淨、草薦時常晒、貫仲蒼朮浸水辟穢惡；卡房內鋪墊活地板（板離地尺許對面開鋪中留空地，板下臨空透氣可取起打掃）", "modals": ["必须"], "condition": "班房久干例禁然有不應收監者（命案要證尋常枷犯追比錢糧等）及應收監不便遽收者（命盜姦拐應擬死罪等）收押公所為便", "object": "", "purpose": "活地板之議創於粵東朱杏生法良意美且所費不多，必可保全人命", "punishment": "", "confidence": "high"},
    # 04-035 稽查班房
    {"item_id": "04-035", "type": "程序型", "subject": "稽查班房", "action": "必須出其不意或早或晚或二三更或四五更親到班房察看有無凌虐情形並詢問所押之人曾否被差凌虐", "modals": ["必须"], "condition": "看役凌虐押犯無惡不作其弊較監獄為尤甚；經管班房之家丁須心地慈祥否則串同看役任意需索", "object": "", "purpose": "家丁看役稍知斂迹", "punishment": "", "confidence": "high"},
    # 04-036 祀典各廟必須修葺
    {"item_id": "04-036", "type": "义务型", "subject": "廟宇之載在祀典者", "action": "均應以時修葺不得聽其攲頹，文廟尤宜加意", "modals": ["必须"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-037 一切典禮必須敬謹
    {"item_id": "04-037", "type": "义务型", "subject": "朔望行香春秋二祭及朝賀拜牌等事", "action": "必須早起早到以昭敬謹", "modals": ["必须"], "condition": "皆典禮所關", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-038 敬恭先哲
    {"item_id": "04-038", "type": "义务型", "subject": "境內先賢祠墓", "action": "須隨時修理；先賢子孫式微須加意培植", "modals": ["必须"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-039 旌揚節烈
    {"item_id": "04-039", "type": "义务型", "subject": "節烈旌表", "action": "必須加意搜訪嚴禁需索，單寒之戶無由上達者為之舉報", "modals": ["必须"], "condition": "節烈者正氣所鍾風化所繫，富家巨族尚不難於舉報單寒之戶往往湮滅不彰", "object": "", "purpose": "扶正氣而端風化", "punishment": "", "confidence": "high"},
    # 04-040 表章孝義
    {"item_id": "04-040", "type": "义务型", "subject": "孝友義行", "action": "若不表揚何以勸善，應照例旌表", "modals": ["应该"], "condition": "孝友義行皆難能而可貴者", "object": "", "purpose": "勸善", "punishment": "", "confidence": "high"},
    # 04-041 保甲
    {"item_id": "04-041", "type": "义务型", "subject": "保甲", "action": "果能逐細清編認真稽察，不特外來宵小無托足之地即本地匪徒不法之事亦有所憚；惟力行保甲甚不容易（得人/籌費/連坐/改換牌冊四難）", "modals": ["必须"], "condition": "某戶某名居住某鄉某甲年歲生理土著流寓房屋田地錢漕男丁婦女大口小口雇工夥計寄居親戚無一不載明保甲冊十家牌內", "object": "", "purpose": "平日弭盜安良線索在手，遇催科捕亡辦緩辦賑亦不難按冊而稽", "punishment": "", "confidence": "high"},
    # 04-042 發門牌須防需索
    {"item_id": "04-042", "type": "禁止型", "subject": "查保甲發門牌", "action": "須嚴防需索，門丁書差惟利是視必不為本官聲名計，本官奈何不自為計耶", "modals": ["必须"], "condition": "鶴峰州牧散發門牌每張索錢一千文闔州怨恨卒以上登白簡，所索之錢皆門丁書差瓜分本官並未染指", "object": "", "purpose": "散發門牌係闔邑之事按戶勒索則人人怨恨家家怨恨", "punishment": "", "confidence": "high"},
    # 04-043 倉穀
    {"item_id": "04-043", "type": "义务型", "subject": "倉穀", "action": "必須實貯庶緩急足恃，須防偷竊防霉爛", "modals": ["必须"], "condition": "此事頗為有司之累", "object": "", "purpose": "", "punishment": "因循怠玩致米穀霉爛者革職動帑買補勒限一年照數追賠", "confidence": "high"},
    # 04-044 米貴時須因地制宜
    {"item_id": "04-044", "type": "义务型", "subject": "米貴措置", "action": "須因地制宜：本地米足不藉客米則減價，地近水次仰藉客米則不應驟減", "modals": ["必须"], "condition": "潞公成都減價平糶/趙清獻越州榜令增價糶之，行之各有效", "object": "", "purpose": "減價則富民居奇而民食艱，驟減則米商裹足而民食愈艱", "punishment": "", "confidence": "high"},
    {"item_id": "04-044", "type": "禁止型", "subject": "平糶", "action": "官府減價平糶不是抑勒富戶減價出糶；若勒令富戶減價則富戶愈不肯糶價何由平", "modals": ["禁止"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-045 賑饑先查戶口
    {"item_id": "04-045", "type": "义务型", "subject": "賑濟飢民", "action": "莫要於查戶口：某戶應賑某戶不應賑、大口小口若干、極貧次貧稍貧層級等差，須查得的確", "modals": ["必须"], "condition": "任之書差保正則索錢冒領，任之紳衿耆老則徇情礙面，本官親身徧查勢難周厯", "object": "", "purpose": "戶口不清則賑錢賑米賑粥均無從下手，實需經費亦無從核計", "punishment": "", "confidence": "high"},
    # 04-046 賑鄉村飢民難於城市（说理，不抽规则）
    # 04-047 外來流民
    {"item_id": "04-047", "type": "程序型", "subject": "外來流民", "action": "宜散不宜聚", "modals": ["宜"], "condition": "富鄭公在青州活流民數十萬其訣竅在不令聚於一處", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-048 開礦
    {"item_id": "04-048", "type": "义务型", "subject": "礦利", "action": "尤為因民美利，不能因噎廢食；聚集多人奸良不一全在彈壓稽查之得人", "modals": ["必须"], "condition": "地方官只求於己無事倡為礦不可開之說，多一事不如少一事之議塞養民者之口", "object": "", "purpose": "生齒日繁農田所入止有此數，苟有可以資生者自當竭力圖之", "punishment": "", "confidence": "high"},
    # 04-049 孤貧口糧
    {"item_id": "04-049", "type": "禁止型", "subject": "孤貧口糧", "action": "不可剋扣", "modals": ["禁止"], "condition": "鰥寡孤獨殘廢之人皆窮民之無告者，國家經費有常例每名每日僅給錢數文", "object": "", "purpose": "天理昭彰，剋扣者之子孫求為鰥寡孤獨殘廢而不可得矣", "punishment": "", "confidence": "high"},
    {"item_id": "04-049", "type": "程序型", "subject": "給發孤貧口糧", "action": "先囑帳房將每人應得之數交錢店發票，屆期坐大堂點名每名給錢票一紙不給現錢", "modals": ["宜"], "condition": "", "object": "", "purpose": "以免剋扣之弊", "punishment": "", "confidence": "high"},
    # 04-050 恤孤幼
    {"item_id": "04-050", "type": "义务型", "subject": "孤幼", "action": "鰥寡孤獨皆窮而無告之人而孤幼為尤甚，必須加意撫恤", "modals": ["必须"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-051 禁溺女
    {"item_id": "04-051", "type": "禁止型", "subject": "溺女", "action": "最干天地之和，必須禁止；不貧之戶力能養而溺女者量罰錢米給養別女", "modals": ["禁止"], "condition": "", "object": "", "purpose": "", "punishment": "量罰錢米", "confidence": "high"},
    {"item_id": "04-051", "type": "程序型", "subject": "禁溺女之法", "action": "育嬰建堂不如酌給錢米令其自育：查實係貧乏小戶生女者按月酌給衣米聽其自己撫養，不時登門查驗病亡者停給；來厯不明暗地送堂之子女另選附近貧婦良慈者領養給以衣糧；育嬰總局必須設立遴派總首事經理", "modals": ["宜"], "condition": "育嬰堂所雇乳媼非其親生痛癢不關常致疾疫不能生全", "object": "", "purpose": "母女天性痛癢相關自多生全，較之收入堂內撫養者事半功倍", "punishment": "", "confidence": "high"},
    # 04-052 禁私宰
    {"item_id": "04-052", "type": "禁止型", "subject": "私宰", "action": "必須嚴禁以絕盜源；官禁不如私禁，勸諭正紳公議禁約每鄉派總首事散首事隨時稽查，違禁私宰公同處罰不遵罰者送官究治", "modals": ["必须"], "condition": "私宰者盜牛之窩家；印官衙門書役佐雜弓兵營汛兵丁鄉約保正無一人不抽收規費包庇縱容", "object": "", "purpose": "官禁乃具文私禁乃實事", "punishment": "公同處罰/送官究治", "confidence": "high"},
    # 04-053 禁婦女入廟燒香
    {"item_id": "04-053", "type": "禁止型", "subject": "婦女入廟燒香", "action": "不特褻瀆神明亦且敗壞風化必須嚴禁以挽頹風，責成住持認真阻攔，住持不攔即傳案責懲並勒令還俗", "modals": ["必须"], "condition": "律載縱令妻女於寺觀神廟燒香者笞四十罪坐夫男", "object": "", "purpose": "", "punishment": "住持責懲勒令還俗；再犯提男夫責懲", "confidence": "high"},
    {"item_id": "04-053", "type": "程序型", "subject": "婦女初犯入廟燒香", "action": "只傳夫男赴案詳細教訓一番免其責處，若再犯則應提男夫責懲不得一味姑息", "modals": ["宜"], "condition": "婦女不聽約束入廟燒香不必皆由縱令，負氣男兒受責歸家吵鬧恐家道失和甚至婦女短見輕生", "object": "", "purpose": "就律意而變通之體恤人情", "punishment": "", "confidence": "high"},
    # 04-054 禁修建寺廟
    {"item_id": "04-054", "type": "禁止型", "subject": "建修廟宇", "action": "必須嚴禁以省耗費而戢亂階：律載寺觀庵院除現在處所不許私自創建增置", "modals": ["禁止"], "condition": "建修廟宇無非耗費民財且廟宇太多往往藏垢", "object": "", "purpose": "", "punishment": "違者僧道充軍尼僧女冠入官為奴；民間擅行興造以違制論；州縣官不行查禁反給告示者罰俸一年", "confidence": "high"},
    # 04-055 禁幼女出家為尼
    {"item_id": "04-055", "type": "禁止型", "subject": "出家為僧道尼僧", "action": "出家為僧道必須在十六歲以下，出家為尼必須在四十歲以上；尼僧不得招受少年女徒；幼女出家由父母作主並非本人情願，應召其父母領回還俗", "modals": ["禁止"], "condition": "例載民閒子弟年在十六以上不准出家；禮部則例尼僧一項不得招受少年女徒", "object": "", "purpose": "定例具有深意；論天理論國法論人情均應如此", "punishment": "地方官嚴行禁止", "confidence": "high"},
    # 04-056 禁燒香聚眾
    {"item_id": "04-056", "type": "禁止型", "subject": "燒香聚眾", "action": "必須嚴行禁止：狡黠僧道及無賴之徒捏稱某廟某神非常靈異，愚民一人傳十十人傳百燒香聚眾舉國若狂，倘不嚴行禁止必致釀成事端", "modals": ["必须"], "condition": "愚民惑於禍福最信鬼神", "object": "", "purpose": "不止男女混雜有傷風化已也", "punishment": "", "confidence": "high"},
    {"item_id": "04-056", "type": "程序型", "subject": "禁妖異靈異", "action": "防微杜漸：趙鳳舉斧碎佛牙/程珦投祠具/林俊焚活佛/蓮浦公鎚碎石獅/楊令暗砍關刀神，皆以權變處置", "modals": ["宜"], "condition": "愚民易惑難曉不必以口舌爭", "object": "", "purpose": "即無事矣", "punishment": "", "confidence": "high"},
    # 04-057 不禁之禁
    {"item_id": "04-057", "type": "程序型", "subject": "淫祀妖術", "action": "不禁而自禁尤為善處之方：宋均令山娶者皆娶巫家女、李德裕以豬肉驗聖水、程明道詰石佛放光，皆不禁自禁", "modals": ["宜"], "condition": "為政者畏其神莫敢禁止", "object": "", "purpose": "民其害遂絕/妖亦尋敗", "punishment": "", "confidence": "high"},
    # 04-058 鄉民求雨擡神像至縣堂
    {"item_id": "04-058", "type": "禁止型", "subject": "民間祈雨擡神像至縣請官叩禱", "action": "乾隆十二年欽奉上諭嚴行禁止，此風斷不可長；地方官遇水旱當竭誠致禱為民請命，棍徒藉名聚眾擡神挾持官長照律治罪", "modals": ["禁止"], "condition": "閩省風俗尚信鬼巫，無藉之徒意在斂錢肥已詭稱神佛靈應聚眾迎賽", "object": "", "purpose": "甚為風俗人心之害", "punishment": "違犯照律治罪；地方官悠忽姑息養姦該督撫參處", "confidence": "high"},
    {"item_id": "04-058", "type": "程序型", "subject": "革除擡神之習", "action": "欲革此習全在平日見信於民；官民尚未相信則照舊行禮，或乘民甫經祈雨尚未轝神來縣之時多張告示剴切曉諭祇准祈雨不准斂錢，恭錄上諭於告示之內", "modals": ["宜"], "condition": "若俟其來而後爭以口舌，民不信便不免滋生事端", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-059 錢糧底冊
    {"item_id": "04-059", "type": "程序型", "subject": "州縣徵收錢糧", "action": "先造實徵底冊；令各里各甲戶書另造一冊上列戶名某某應完錢糧若干下註的名某某住某鄉某處，遇有拖欠便不難指名催追", "modals": ["必须"], "condition": "冊內所載名目是戶名不是的名亦無住址可考；戶書以此為奇貨往往不肯開造", "object": "", "purpose": "若非恩威並用未必惟命是聽", "punishment": "", "confidence": "high"},
    # 04-060 銀錢兼收
    {"item_id": "04-060", "type": "程序型", "subject": "州縣徵收錢糧", "action": "銀錢兼收：鄉村僻陋無銀可換且小戶數目零星必令完銀多窒礙，一概收錢易啟櫃書掯勒之弊，銀照時價計算於民較便", "modals": ["宜"], "condition": "本應照例收銀", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-061 不惡而嚴
    {"item_id": "04-061", "type": "程序型", "subject": "徵收錢糧刁抗者", "action": "鎖於錢糧櫃側令其看他人完納錢糧以激發羞惡之心，一俟完清即行開釋", "modals": ["宜"], "condition": "開徵之後周厯四鄉沿村諄勸", "object": "", "purpose": "不惡而嚴之法，從未以抗欠刑責一人", "punishment": "", "confidence": "high"},
    # 04-062 禁催差擾累
    {"item_id": "04-062", "type": "禁止型", "subject": "催差下鄉", "action": "百姓拖欠錢糧自不能不用差催但須嚴防擾累：催差下鄉兇橫似虎稍拂其慾即擲票毆差為詞，或私囑櫃書多方掯勒，或慫恿門丁多人拘鎖", "modals": ["必须"], "condition": "需索之浮費數倍於應完之錢糧", "object": "", "purpose": "恐蚩蚩者不免賣兒鬻女", "punishment": "", "confidence": "high"},
    # 04-063 契約勿用官紙
    {"item_id": "04-063", "type": "禁止型", "subject": "官紙寫契", "action": "昔有創為官紙者發交約保收存凡買賣田地必須向約保買取官紙書立契約，雖杜匿稅之一法，但權在約保不免藉端掯勒，便於官不便於民殊非體恤之道", "modals": ["禁止"], "condition": "鄉民省錢往往匿契不稅", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-064 杜漏稅之弊
    {"item_id": "04-064", "type": "程序型", "subject": "民閒買田推收過割", "action": "應令經管推收之書辦於每年推收時將某鄉某人買某人田若干價若干造冊送核；有投稅者於冊內註銷不投稅者即可指名催稅", "modals": ["必须"], "condition": "應稅之契或多或少無不一目了然", "object": "", "purpose": "較之用官紙寫契尚少流弊", "punishment": "", "confidence": "high"},
    # 04-065 接收交代
    {"item_id": "04-065", "type": "程序型", "subject": "接收交代", "action": "須先將前任交抵二摺發給書辦逐細查核並令書辦出結，結內聲敘某項額征若干前任已征若干民欠若干已解若干征存未解若干已支若干未支若干，如有應交未交不應抵而抵情弊願甘著賠；再請幕友查券根查迴批查領狀（已征未征以券根為憑已解未解以迴批為憑已支未支以領狀為憑）", "modals": ["必须"], "condition": "", "object": "", "purpose": "書辦各顧身家恐干著賠必不代前任朦混，自不難水落石出", "punishment": "", "confidence": "high"},
    # 04-066 受代須從忠厚
    {"item_id": "04-066", "type": "义务型", "subject": "接收交代", "action": "須從忠厚，今日之後任即異日之前任", "modals": ["必须"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-067 銀錢出入簿
    {"item_id": "04-067", "type": "程序型", "subject": "州縣銀錢出入", "action": "囑司筦鑰者分列正入正出雜入雜出四簿：正入簿記銀米應征之數及稅契雜稅耗羨，正出簿記銀米應解應支應放應墊及廉俸幕脩，雜入簿記銀之平餘米之斛面及每歲額有之陋規，雜出簿記應捐應贈及日月應費；四簿之外另置驛站簿，另備收銀用銀流水總簿收錢用錢流水總簿逐日結總滾算", "modals": ["必须"], "condition": "州縣身兼庶事萬不能瑣屑理財然出納之數斷不可不知，盡委經手之人而己不與聞則有挪移侵盜者至交代時噬臍無及", "object": "", "purpose": "正入稍虧即以雜入補之而用自不敢不節；設遇去官交代冊籍頃刻可成雖猾吏無能為弊", "punishment": "", "confidence": "high"},
    # 04-068 為後任留餘地
    {"item_id": "04-068", "type": "义务型", "subject": "交卸時", "action": "須為後任留餘地，便宜處不可打撈淨盡", "modals": ["必须"], "condition": "", "object": "", "purpose": "", "punishment": "", "confidence": "high"},
    # 04-069 去之日如始至
    {"item_id": "04-069", "type": "义务型", "subject": "將卸事時", "action": "須嚴約家丁不許損壞門扇等項，臨時須親自檢點；叔孫所館者雖一日必葺其牆屋去之如始至", "modals": ["必须"], "condition": "", "object": "", "purpose": "即此便是物我無閒氣象", "punishment": "", "confidence": "high"},
    # 04-070 將卸事時即令眷屬出署
    {"item_id": "04-070", "type": "程序型", "subject": "官員卸任", "action": "於交代限內即出署另居不得久佔衙署：道府交代定限一月舊任分限只十日，州縣交代定限兩月舊任分限只二十日；交卸前一二日即令眷屬搬移本官交印時搬移", "modals": ["必须"], "condition": "向有新任催舊任出署而舊任以例限一月為辭不肯即出因而新舊失和", "object": "", "purpose": "新舊任共居一署家丁混雜不清，不特新任難於稽查防範即舊任亦有許多窒礙；人己兩便", "punishment": "", "confidence": "high"},
]
