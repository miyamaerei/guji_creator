# -*- coding: utf-8 -*-
"""卷07 钱谷部二·结构化四维（8 条）。"""
RECORDS = [
    {"item_id": "07-001", "dim": "TME", "tme_type": "deadline",
     "target": "征比限期", "target_ent_ids": [], "content": "夏税不逾六月秋粮不逾十月开征早必得仲春；每月上下二限共一分十个月二十限共十分，二月找征正月二限、五月止征上半月、六月止征下半月，五月下半月并于七月六月上半月并于八月，十月十分止作十六限", "confidence": "high"},
    {"item_id": "07-001", "dim": "LGR", "lgr_type": "ledger",
     "target": "比簿限单体系", "target_ent_ids": [], "content": "比簿（每里一本每本十一张，前一张登里总注现年姓名后造本里十限该银；里经慛查算总书、本年实征条银内搭征钱粮房经承）+ 里甲限单 + 花户实征限单（里一本首造里总一页各甲造甲总一页）；各里完欠一目了然", "confidence": "high"},
    {"item_id": "07-001", "dim": "LGR", "lgr_type": "template_form",
     "target": "连二截票", "target_ent_ids": [], "content": "连二免比票：一截票存算、一归农免比，合缝用印；如本限透完下限者每限截给归农票一张须作两限填明截粘下限总内；不足限数者不准截止于限簿挂浮签俟下限完数总算；每里二十页以十限上下为率仍装钉护页数明张数用印登票号发总书仍取领票领状", "confidence": "high"},
    {"item_id": "07-001", "dim": "LGR", "lgr_type": "template_form",
     "target": "三比单", "target_ent_ids": [], "content": "里长排年分限比单/甲长经催分限比单/各甲花户分限比单——分则以之查比合则以之考数；排年完欠务要里结里总甲结甲总使开册便知某里尚欠应比某里巳完不必摘比", "confidence": "high"},
    {"item_id": "07-001", "dim": "FRD", "frd_type": "guard",
     "target": "比册防弊", "target_ent_ids": [], "content": "防总书粮房受贿通同：比册土粘揭重页庇护全里、水贴膏药庇护欠多之人、抽簿逃卯捏登完数——内衙勤敏精详逐限完结，查拏之日自寅至酉务必查尽；假票避比以对同小印封之仍行揭去", "confidence": "high"},
    {"item_id": "07-002", "dim": "FRD", "frd_type": "guard",
     "target": "拆封防弊", "target_ent_ids": [], "content": "晚间不可拆封（本官倦盹灯下易作弊）；拆时官不可分心别视，防奸胥在拆手箝封角搓块掷地、在兑指夹零银轻丢入袖；拆完柜吏另具拆单，库吏查前次拆单亲填连前共拆银若干逓粘成卷存查", "confidence": "high"},
    {"item_id": "07-003", "dim": "FRD", "frd_type": "guard",
     "target": "解银防弊", "target_ent_ids": [], "content": "防批回洗补（印发后以多改少、实收领出后以少改多）；防小批侵匿（非上司颁发无号可稽，按限严查掣批清项）；防管解侵吞（佥解选差取保+移营拨兵+亲信内丁协解，银鞘外蒙生牛皮铁篐密钉）；官役过支预借断不可开", "confidence": "high"},
    {"item_id": "07-003", "dim": "LGR", "lgr_type": "ledger",
     "target": "解支账册", "target_ent_ids": [], "content": "解支库簿（每年一总册，解支一次扣算开写一次拆封一次连前结总一次）+ 解支两截册（上截原额应解应给下截陆续填批注给，相符印完讫二字）+ 比批簿（奉某衙门发号批若干张，获到填批已收）+ 批收粘案橱（全欵解完挨序夹入实收粘连成卷骑缝斜印）", "confidence": "high"},
]
