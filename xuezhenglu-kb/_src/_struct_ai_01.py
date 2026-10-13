# -*- coding: utf-8 -*-
"""《政学录》卷一 结构化层源数据（四维 ACT/FRD/LGR/TME，AI 逐条判定，2026-10-12）。
纪律：dim 必填 + 维度类型字段必填且命中枚举；target 用 ID 引用（暂可空，打包后回填 ENT id）；evidence 写要点不抄长文。"""

RECORDS = [
    # ---- 01-001 内阁 ----
    {"item_id": "01-001", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "内阁职掌：启奏票拟面赐裁决/东宫讲读/总裁实录/会试廷试贡士总领/郊祀巡狩扈行"},
    {"item_id": "01-001", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "机密文书防漏泄稽缓遗失妄误皆有罚"},
    # ---- 01-002 六部 ----
    {"item_id": "01-002", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "法令烦多滋弊，救弊在减法：止治贪暴奸私明知故犯，因功获过概免琐议"},
    {"item_id": "01-002", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "六部职掌：逐件讲求见行事例减法，大官易于综核"},
    # ---- 01-003 科道 ----
    {"item_id": "01-003", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "例之弊：例既无所不有弊故无所不为，可重可轻可上可下"},
    {"item_id": "01-003", "dim": "LGR", "lgr_type": "ledger",
     "target": "", "evidence": "汇集从前诸例一册（请旨定者/部院科道条陈准行者），堂官一览可悉"},
    # ---- 01-004 选法 ----
    {"item_id": "01-004", "dim": "TME", "tme_type": "deadline",
     "target": "", "evidence": "选法日期：大选单月十五投供双月二十三封签二十五除选；急选双月十五投供单月二十三封签二十五补授"},
    {"item_id": "01-004", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "吏部选法职掌：投供点卯/对缺封缺签/除选补授/截取数目"},
    {"item_id": "01-004", "dim": "LGR", "lgr_type": "voucher",
     "target": "", "evidence": "候选官员丁忧患病取甘结报部以凭注册扣选"},
    # ---- 01-005 考课 ----
    {"item_id": "01-005", "dim": "TME", "tme_type": "assessment",
     "target": "", "evidence": "考课年限：六年京察三年大计五年军政；康熙改三年一次汇考；复六年考察"},
    {"item_id": "01-005", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "考满职责：部院大臣自陈/堂官斟酌等第/督抚保奏/在外一省文武官五等分疏具题"},
    {"item_id": "01-005", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "考满积弊：营求徇庇/奔竞钻刺如夜蛾投火/层层剥削县官"},
    {"item_id": "01-005", "dim": "LGR", "lgr_type": "ledger",
     "target": "", "evidence": "考满造册：办过事件功过造册与题疏一同移送部院"},
    # ---- 01-006 钱粮总归户部 ----
    {"item_id": "01-006", "dim": "LGR", "lgr_type": "ledger",
     "target": "", "evidence": "赋役全书+简明赋役之书+易知由单（止开丁地银米名色）"},
    {"item_id": "01-006", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "户部总理钱粮职掌：正月全拨兵饷/部寺应用钱粮年终核报"},
    {"item_id": "01-006", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "防钱粮名色混杂：诸凡催提征解俱称丁地钱粮，别项名色槩行停止"},
    # ---- 01-007 钱粮出入数目 ----
    {"item_id": "01-007", "dim": "LGR", "lgr_type": "ledger",
     "target": "", "evidence": "钱粮出入通盘核算：入数（丁地/盐课/关税/当税）+出数（兵饷/俸饷/织造）"},
    {"item_id": "01-007", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "宂兵宂费之弊：明季禄俸出多入少王府缺禄米卫所缺月粮"},
    # ---- 01-008 安限催征 ----
    {"item_id": "01-008", "dim": "TME", "tme_type": "deadline",
     "target": "", "evidence": "开征月份：夏税五六两月秋粮九十两月照全书款项纳完其余月分不许征收"},
    {"item_id": "01-008", "dim": "TME", "tme_type": "season",
     "target": "", "evidence": "农忙停催：明季万历前农忙停催科以养民力"},
    {"item_id": "01-008", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "催征积弊：明末预征/正项之外杂项勒索/兵马经临派夫"},
    {"item_id": "01-008", "dim": "LGR", "lgr_type": "ledger",
     "target": "", "evidence": "赋役全书夏税秋粮项款正项杂费皆在其中"},
    # ---- 01-009 漕粮 ----
    {"item_id": "01-009", "dim": "LGR", "lgr_type": "ledger",
     "target": "", "evidence": "循环册籍查廒贮：每廒收米若干注明经管官某人吏某人"},
    {"item_id": "01-009", "dim": "TME", "tme_type": "deadline",
     "target": "", "evidence": "漕限：冬兑冬开五月尽数过淮；北地十一月结冰二月开，一岁八月工夫"},
    {"item_id": "01-009", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "漕储职责：经纪运米大通桥监督查验/车户运米各仓监督查验/闸督催趱"},
    {"item_id": "01-009", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "仓粮土湿防弊：三晒三扬之例/一廒清一廒之数/一官清一官之事"},
    # ---- 01-010 盐课 ----
    {"item_id": "01-010", "dim": "LGR", "lgr_type": "ledger",
     "target": "", "evidence": "盐课额账：四盐差长芦兼辖山东/河东兼辖山陕/两淮/两浙兼辖江南四府/广东广西福建"},
    # ---- 01-011 关税 ----
    {"item_id": "01-011", "dim": "LGR", "lgr_type": "ledger",
     "target": "", "evidence": "康熙八年关税额账：崇文门/张家口/杀虎口/浒墅关/芜湖关/北新关/九江关等额税"},
    # ---- 01-012 钱法 ----
    {"item_id": "01-012", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "钱多壅滞之弊：贮之者少运之者少用之者少（三少），多则必滞"},
    # ---- 01-013 祀典 ----
    {"item_id": "01-013", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "有司祭祀之责：修葺坛壝庙宇/斋戒执事告戒/牲帛粢盛亲省"},
    {"item_id": "01-013", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "祭祀虚文之弊：坛壝宿莽积尘/斋戒视为虚文/供陈尽托仆隶"},
    # ---- 01-014 士额 ----
    {"item_id": "01-014", "dim": "TME", "tme_type": "assessment",
     "target": "", "evidence": "入学额数沿革：顺治四年大学四十中学二十五小学十二；顺治十五年照万历大府二十人大州县十五人；康熙八年乡试编字号"},
    {"item_id": "01-014", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "士数充塞之弊：额少则跃冶之民舞文健讼窝盗蓄奸"},
    # ---- 01-015 风俗 ----
    {"item_id": "01-015", "dim": "FRD", "frd_type": "evil_custom",
     "target": "", "evidence": "奢侈之风：衣服华美僭比公卿/饮食珍错/器具奇技淫巧/屋宇装饰过分/婚嫁称贷葬竭中产"},
    {"item_id": "01-015", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "乡饮乡贤之弊：不论有德无德惟爵位是尊/不论公是公非惟体面是重"},
    # ---- 01-016 兵制 ----
    {"item_id": "01-016", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "五府三营职掌不相侵：在内营操官止管操练无衙门印信；五府有衙门印信理常行政务"},
    {"item_id": "01-016", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "兵柄防弊：兵柄不宜轻假武臣/出征必选二三人名位谋勇相等者参用/事平将归于府军归于营印归于朝"},
    # ---- 01-017 屯田 ----
    {"item_id": "01-017", "dim": "TME", "tme_type": "deadline",
     "target": "", "evidence": "屯田起科期限：自拨给之日俸饷预支为牛种，三年之后照民例起科"},
    {"item_id": "01-017", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "州县官劝垦职责：诚能劝垦照民例加级纪录，调剂无能听督抚参奏"},
    {"item_id": "01-017", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "防投诚垦荒兵脱逃：督抚稽察给饷无侵扣"},
    # ---- 01-018 纤夫 ----
    {"item_id": "01-018", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "纤夫之害：借名加派以一派十/闭寺断出入/鞭扑勒索勒常例/倒毙殆尽"},
    {"item_id": "01-018", "dim": "TME", "tme_type": "deadline",
     "target": "", "evidence": "纤夫定限：自京起程者臣部定限自外起行者该督抚定限报部"},
    {"item_id": "01-018", "dim": "LGR", "lgr_type": "voucher",
     "target": "", "evidence": "勘合火牌填给船数"},
    # ---- 01-019 逃人 ----
    {"item_id": "01-019", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "假逃人诈害：奸恶光棍充作逃人展转诈害夺人妻子/地方光棍犯罪冒称旗人逃人"},
    {"item_id": "01-019", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "辨逃情真伪防弊：迫于情而逃/迫于有所为而故逃/假逃人名色诈害 七项分判"},
    # ---- 01-020 失出 ----
    {"item_id": "01-020", "dim": "FRD", "frd_type": "abuse",
     "target": "", "evidence": "宁从重拟之弊：承问官惕于功令宁从重拟以作自全之计"},
    {"item_id": "01-020", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "失出免究防冤：拟罪稍轻引律未协查明免究即行改正；徇私枉法故出故入指名参处"},
    # ---- 01-021 秋审 ----
    {"item_id": "01-021", "dim": "TME", "tme_type": "deadline",
     "target": "", "evidence": "朝审日期例应霜降后十日举行"},
    {"item_id": "01-021", "dim": "ACT", "act_type": "justice_role",
     "target": "", "evidence": "秋审职责：吏部尚书主笔会审/三法司覆奏/刑科三覆具奏候御笔勾除"},
    {"item_id": "01-021", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "重惜民命：情真之中委曲分别轻重/求其生而不得然后死之"},
    # ---- 01-022 结案 ----
    {"item_id": "01-022", "dim": "TME", "tme_type": "deadline",
     "target": "", "evidence": "审案定限：强盗人命重情首告到官定限一年结案；府州县自理限一月；提人行查再限二十日"},
    {"item_id": "01-022", "dim": "ACT", "act_type": "justice_role",
     "target": "", "evidence": "审级职责：州县详审招解推官/推官审明招解臬司/臬司详报督抚/督抚细核"},
    {"item_id": "01-022", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "防草率：草率游移引律不合开列承问职名题参；徇庇贿托另行纠参"},
    # ---- 01-023 河道 ----
    {"item_id": "01-023", "dim": "TME", "tme_type": "deadline",
     "target": "", "evidence": "筑坝限期：水发六月下旬旧例筑坝至九月霜降三个月，余时去坝用闸启闭如常；漕运限期六月前尽报过淮"},
    {"item_id": "01-023", "dim": "ACT", "act_type": "official",
     "target": "", "evidence": "河工职责：总河总漕勘议/河官按境修理/印官量起民夫农忙散归"},
    {"item_id": "01-023", "dim": "FRD", "frd_type": "guard",
     "target": "", "evidence": "堤坝水柜修防：岁修顶冲/缕堤月堤遥堤大行堤护城堤格堤减水石坝/水柜潴蓄防豪民侵占"},
]
