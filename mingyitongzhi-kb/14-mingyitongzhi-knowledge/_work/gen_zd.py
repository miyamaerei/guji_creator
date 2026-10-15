# -*- coding: utf-8 -*-
"""Generate 彰德府 (27-002) JSON files."""
import json, os

OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol27"
IID = "27-002"
GID = "GEO-27002"

def per(pid, name, typ, dyn, np, off, summ):
    return {"per_id":pid,"item_id":IID,"geo_id":GID,"name":name,"type":typ,"dynasty":dyn,"native_place":np,"office":off,"summary":summ}
def site(sid,name,typ,loc,hist):
    return {"site_id":sid,"item_id":IID,"geo_id":GID,"name":name,"type":typ,"location_text":loc,"history_lore":hist}
def mtn(mid,name,typ,loc,desc,lore=""):
    return {"mtn_id":mid,"item_id":IID,"geo_id":GID,"name":name,"type":typ,"location_text":loc,"description":desc,"lore":lore}

# ===== MAIN FILE =====
main = {
  "item_id": IID, "volume": "27", "source": "彰德府", "region": "河南", "type": "prefecture",
  "original": "彰徳府【东至直隶大名府内黄县界七十里南至大名府濬县界七十里西至山西潞州壶闗县界一百七十里北至直隶广平府邯郸县界一百二十里自府治至京师一千二百里至南京一千七百里】【粮二十五万二千石零】",
  "layers": {
    "ents": [
      {"ent_id":"ENT-001","name":"彰德府","type":"geo","norm":"彰德府","first_source":IID},
      {"ent_id":"ENT-002","name":"安阳县","type":"geo","norm":"安阳县","first_source":IID},
      {"ent_id":"ENT-003","name":"汤阴县","type":"geo","norm":"汤阴县","first_source":IID},
      {"ent_id":"ENT-004","name":"临漳县","type":"geo","norm":"临漳县","first_source":IID},
      {"ent_id":"ENT-005","name":"林县","type":"geo","norm":"林县","first_source":IID},
      {"ent_id":"ENT-006","name":"磁州","type":"geo","norm":"磁州","first_source":IID},
      {"ent_id":"ENT-007","name":"武安县","type":"geo","norm":"武安县","first_source":IID},
      {"ent_id":"ENT-008","name":"涉县","type":"geo","norm":"涉县","first_source":IID},
      {"ent_id":"ENT-009","name":"魏郡","type":"geo","norm":"魏郡","first_source":IID},
      {"ent_id":"ENT-010","name":"相州","type":"geo","norm":"相州","first_source":IID},
      {"ent_id":"ENT-011","name":"邺郡","type":"geo","norm":"邺郡","first_source":IID},
      {"ent_id":"ENT-012","name":"彰德卫","type":"geo","norm":"彰德卫","first_source":IID},
      {"ent_id":"ENT-013","name":"太行山","type":"mtn","norm":"太行山","first_source":IID},
      {"ent_id":"ENT-014","name":"漳河","type":"mtn","norm":"漳河","first_source":IID},
      {"ent_id":"ENT-015","name":"图经","type":"book","norm":"图经","first_source":IID},
      {"ent_id":"ENT-016","name":"隋志","type":"book","norm":"隋志","first_source":IID},
      {"ent_id":"ENT-017","name":"郡志","type":"book","norm":"郡志","first_source":IID},
      {"ent_id":"ENT-018","name":"相台志","type":"book","norm":"相台志","first_source":IID},
      {"ent_id":"ENT-019","name":"赵王府","type":"geo","norm":"赵王府","first_source":IID}
    ],
    "geos": [
      {
        "geo_id": GID, "item_id": IID, "name": "彰德府", "type": "prefecture",
        "region": "河南", "parent": "GEO-000",
        "children": ["GEO-27002c01","GEO-27002c02","GEO-27002c03","GEO-27002c04","GEO-27002s01","GEO-27002w01","GEO-27002w02"],
        "volume_range": "卷27",
        "attributes": {
          "borders": [
            {"direction":"东","to_place":"直隶大名府内黄县界","distance_li":70},
            {"direction":"南","to_place":"大名府濬县界","distance_li":70},
            {"direction":"西","to_place":"山西潞州壶关县界","distance_li":170},
            {"direction":"北","to_place":"直隶广平府邯郸县界","distance_li":120}
          ],
          "to_capital": [
            {"capital":"京师","distance_li":1200},
            {"capital":"南京","distance_li":1700}
          ],
          "grain_tax": {"amount":252000,"unit":"石","note":"二十五万二千石零"},
          "jun_name": "魏郡邺郡",
          "topography": "旁极齐秦跨蹑燕赵【晋左思魏都赋】；西泽潞东大名南卫辉北洺磁【图经】；其地平广为天下要【相台志】",
          "customs": "得京洛之风【隋志】邺都所在浮巧成俗雕刻之工特云精巧；俗陶淳古人尚英雄【图经】自殷王河亶甲所都而俗已陶为淳古；勤于营生俭于费用【图经】；雅重儒术【郡志】土狭人稀习尚淳厚雅重儒术",
          "garrisons": [
            {"name":"彰德卫","type":"卫","location_text":"在府城内东南隅洪武七年建"},
            {"name":"守御林县中千户所","type":"千户所","location_text":"在林县治东南洪武二十八年建隶彰德卫"},
            {"name":"守御磁州千户所","type":"千户所","location_text":"在州治东北洪武中建隶山西潞州卫"}
          ],
          "fiefs": [
            {"name":"赵王府","location":"在府治东洪熙元年以彰德府治改建"},
            {"name":"临漳王府","location":"在府治南景泰三年建"},
            {"name":"汤阴王府","location":"俱同城"},
            {"name":"襄邑王府","location":"俱同城"},
            {"name":"洛川王府","location":"俱同城"},
            {"name":"南乐王府","location":"俱同城"},
            {"name":"平乡王府","location":"俱同城"},
            {"name":"广安王府","location":"俱同城"},
            {"name":"江宁王府","location":"俱同城"},
            {"name":"获嘉王府","location":"俱同城"},
            {"name":"成皋王府","location":"俱同城"},
            {"name":"光山王府","location":"俱同城"}
          ]
        },
        "cit_ids": ["CIT-001","CIT-002","CIT-003","CIT-004","CIT-005"]
      },
      {"geo_id":"GEO-27002w01","item_id":IID,"name":"守御林县中千户所","type":"weisuo","region":"河南","parent":GID,"children":[],"volume_range":"卷27","attributes":{"location_text":"在林县治东南洪武二十八年建隶彰德卫"},"cit_ids":[]},
      {"geo_id":"GEO-27002w02","item_id":IID,"name":"守御磁州千户所","type":"weisuo","region":"河南","parent":GID,"children":[],"volume_range":"卷27","attributes":{"location_text":"在州治东北洪武中建隶山西潞州卫"},"cit_ids":[]}
    ],
    "evos": [
      {"evo_id":"EVO-001","item_id":IID,"geo_id":GID,"dynasty":"商","era":None,"institution_name":"相","action":"置","detail":"禹贡冀州之域，天文室壁分野，商河亶甲居相即此"},
      {"evo_id":"EVO-002","item_id":IID,"geo_id":GID,"dynasty":"春秋","era":None,"institution_name":"晋东阳地","action":"因之","detail":"春秋为晋之东阳地，战国为魏之邺地"},
      {"evo_id":"EVO-003","item_id":IID,"geo_id":GID,"dynasty":"秦","era":None,"institution_name":"上党邯郸二郡地","action":"置","detail":"秦为上党邯郸二郡地"},
      {"evo_id":"EVO-004","item_id":IID,"geo_id":GID,"dynasty":"汉","era":None,"institution_name":"魏郡","action":"置","detail":"汉置魏郡治邺，东汉末冀州徙治邺，魏曹操受封于此称为邺都"},
      {"evo_id":"EVO-005","item_id":IID,"geo_id":GID,"dynasty":"南北朝","era":"东魏","institution_name":"司州","action":"改","detail":"后魏于此置相州，东魏静帝徙都之改曰司州，北齐改清都尹"},
      {"evo_id":"EVO-006","item_id":IID,"geo_id":GID,"dynasty":"北周","era":None,"institution_name":"相州","action":"改","detail":"后周复改为相州及魏郡治安阳"},
      {"evo_id":"EVO-007","item_id":IID,"geo_id":GID,"dynasty":"唐","era":"天宝","institution_name":"邺郡","action":"改","detail":"隋初罢郡为相州，大业初复改魏郡，唐为相州，天宝初改邺郡乾元初复为相州"},
      {"evo_id":"EVO-008","item_id":IID,"geo_id":GID,"dynasty":"五代","era":None,"institution_name":"昭德军","action":"置","detail":"五代梁置昭德军节度，晋改彰德军"},
      {"evo_id":"EVO-009","item_id":IID,"geo_id":GID,"dynasty":"宋","era":None,"institution_name":"相州","action":"因之","detail":"宋复为相州属河北道"},
      {"evo_id":"EVO-010","item_id":IID,"geo_id":GID,"dynasty":"金","era":None,"institution_name":"彰德府","action":"升","detail":"金升彰德府，元改彰德路"},
      {"evo_id":"EVO-011","item_id":IID,"geo_id":GID,"dynasty":"明","era":None,"institution_name":"彰德府","action":"因之","detail":"本朝改彰德府，领州一县六"}
    ],
    "mtns": [
      mtn("MTN-001","韩陵山","山","在府城东北一十七里","曹魏刘桢诗朝发白马暮宿韩陵即此，东魏高欢破尔朱荣于此","陈徐陵谓北朝人物惟韩陵一片石耳"),
      mtn("MTN-002","宝山","山","在府城西南四十里","多产白石陶人取以为器",""),
      mtn("MTN-003","龙山","山","在府城西四十里","魏都赋虎涧龙山即此",""),
      mtn("MTN-004","安阳河","河","一名洹水","源自故洹水县东至林安阳二县，东经永和镇入卫河",""),
      mtn("MTN-005","漳河","河","其源有二一出山西潞州长子县名浊漳一出平定州乐平县名清漳","俱东至林县合流经临漳馆陶县界入卫河",""),
      mtn("MTN-006","万金渠","渠","源出宝山经府城西分注东南溉田","其利可抵万金",""),
      mtn("MTN-007","高平渠","渠","在安阳县东南二十里","唐刺史李景所凿引安阳水东流溉田，宋韩琦判相州疏之",""),
    ],
    "pers": [], "sites": [],
    "prods": [
      {"prod_id":"PROD-001","item_id":IID,"geo_id":GID,"name":"艾","category":"药材","note":"汤阴县扁鹊墓旁出"},
      {"prod_id":"PROD-002","item_id":IID,"geo_id":GID,"name":"磁石","category":"矿物","note":"磁州出"},
      {"prod_id":"PROD-003","item_id":IID,"geo_id":GID,"name":"锡","category":"矿物","note":"武安县出"},
      {"prod_id":"PROD-004","item_id":IID,"geo_id":GID,"name":"铁","category":"矿物","note":"俱涉县出"},
      {"prod_id":"PROD-005","item_id":IID,"geo_id":GID,"name":"自然铜","category":"矿物","note":"俱涉县出"},
      {"prod_id":"PROD-006","item_id":IID,"geo_id":GID,"name":"知母","category":"药材","note":"府境出"},
    ],
    "cits": [
      {"cit_id":"CIT-001","item_id":IID,"cited_work":"隋志","cited_work_ent_id":"ENT-016","context":"证俗","original":"【隋志】"},
      {"cit_id":"CIT-002","item_id":IID,"cited_work":"图经","cited_work_ent_id":"ENT-015","context":"证俗","original":"【图经】"},
      {"cit_id":"CIT-003","item_id":IID,"cited_work":"郡志","cited_work_ent_id":"ENT-017","context":"证俗","original":"【郡志】"},
      {"cit_id":"CIT-004","item_id":IID,"cited_work":"相台志","cited_work_ent_id":"ENT-018","context":"立论","original":"【相台志序】"},
      {"cit_id":"CIT-005","item_id":IID,"cited_work":"魏都赋","cited_work_ent_id":None,"context":"立论","original":"【晋左思魏都赋】"}
    ]
  },
  "layer_count": 7,
  "validation": {"errs":[],"gap":0,"notes":"pers拆至pers1/pers2；sites拆至sites.json；府级山川只留府城附近"}
}

with open(os.path.join(OUT,"27-002_彰德府.json"),"w",encoding="utf-8") as f:
    json.dump(main,f,ensure_ascii=False,indent=2)
print("彰德府 main done")

# ===== pers1: 名宦 =====
pers1_data = [
  per("PER-001","西门豹","名宦","周","","邺令","邺俗素信巫觋岁为河伯娶妇，豹投巫止之，因开河为十二渠以溉田"),
  per("PER-002","史起","名宦","周","","邺令","引漳水灌田，民歌曰邺有贤令兮为史公决漳水兮灌邺旁"),
  per("PER-003","京房","名宦","汉","","魏郡太守","得以考功法治郡，在郡尝上书极言灾异"),
  per("PER-004","铫期","名宦","汉","","魏郡太守","平五校贼郡界清平，人尤服其威信"),
  per("PER-005","黄香","名宦","汉","","魏郡太守","郡旧有内外园田与人分种，香曰食禄之人不与民争利乃悉以赋人"),
  per("PER-006","王脩","名宦","三国","","魏郡太守","为治抑强扶弱明信赏罚，百姓称之"),
  per("PER-007","尉迟迥","名宦","北周","","相州总管","持正守法恩泽下流，隋攻相城迥坚守之伏剑奋忠以保相民"),
  per("PER-008","梁彦光","名宦","隋","","相州刺史","发擿奸伏若神豪滑潜窜，招致儒师立乡校以德化人"),
  per("PER-009","樊叔略","名宦","隋","","相州刺史","政为第一玺书褒美并赐粟帛"),
  per("PER-010","宋璟","名宦","唐","","相州刺史","政尚清毅吏民无敢犯者"),
  per("PER-011","张说","名宦","唐","","相州刺史","河北道观察使勤恤民隐有惠政"),
  per("PER-012","李景","名宦","唐","","相州刺史","于州西开万金高平二渠引洹水东流以灌田，民获其利"),
  per("PER-013","寇准","名宦","宋","","知相州","初为成安令百姓便之，后以宰相出知相州"),
  per("PER-014","程珦","名宦","宋","","知磁州","慈恕而刚断，熙宁法行为守令者奉命惟恐后，珦独抗议指其未便"),
  per("PER-015","王猎","名宦","宋","","知林虑县","县依山俗以搜田为生不知学，猎立孔子庙择秀民诲之"),
  per("PER-016","宗泽","名宦","宋","","知磁州","靖康中太原失守，泽就道至磁缮城浚隍治器械募义，金人来攻泽遣兵击败之"),
  per("PER-017","赵不试","名宦","宋","","知相州","建炎初金人来攻，不试固守不下，外援不至与敌约勿杀城中人，既启门遂与阖家赴井死"),
  per("PER-018","詹俊","名宦","明","","磁州同知","洪武初民有掘故址得藏金纳半于官，俊不许而归之，遇飞蝗呼天哀告蝗遂出境"),
  per("PER-019","陈文通","名宦","明","","彰德知府","洪武末廉介有为门无私谒，岁饥尝劝富民出粟人争输米以赈"),
  per("PER-020","应琚","名宦","明","","彰德知府","永乐初府俗富民子弟多投肄兵以隐役，琚乃谕以教条限以额数"),
  per("PER-021","杨缙","名宦","明","","彰德知府","永乐间淫雨河水涌溢为患，缙乃率寮属自责以祷，未几果天霁水复故道"),
]
pers1 = {"item_id":IID,"volume":"27","source":"彰德府-名宦","region":"河南",
  "layers":{"ents":[],"geos":[],"evos":[],"mtns":[],"pers":pers1_data,"sites":[],"prods":[],"cits":[]},
  "layer_count":7,"validation":{"errs":[],"gap":0,"notes":"名宦层拆分"}}
with open(os.path.join(OUT,"27-002_彰德府_pers1_名宦.json"),"w",encoding="utf-8") as f:
    json.dump(pers1,f,ensure_ascii=False,indent=2)
print("pers1 done")

# ===== pers2: 人物+流寓+列女+仙释 =====
pers2_data = [
  per("PER-001","盖宽饶","人物","汉","魏郡","司隶校尉","举贤良对策高第，为卫司马遇士卒甚有恩，后擢司隶校尉刺举无所避"),
  per("PER-002","霍谞","人物","汉","邺县","尚书仆射","大将军梁冀秉权，谞因陛见陈其罪，及冀诛封邺都亭侯"),
  per("PER-003","郭巨","人物","汉","林虑","孝子","家贫养母尽孝，乃埋其子掘地三尺得黄金一釜，上有丹书曰天赐孝子郭巨"),
  per("PER-004","杜乔","人物","汉","林虑","大司空","少为诸生举孝廉，梁冀专权乔正色不挠，卒为所害"),
  per("PER-005","邵续","人物","晋","安阳","冀州刺史","素朴有志博览经史妙解天文，绥怀有方散亡归附"),
  per("PER-006","尧君素","人物","隋","汤阴","鹰击郎将","大业末从屈突通拒唐师，通军败左右请降君素不从，后死节"),
  per("PER-007","傅奕","人物","唐","邺县","太史丞","仕为太史丞，尝上疏诋浮图法，贞观时召赐食谓曰向所奏何防败我"),
  per("PER-008","戴胄","人物","唐","安阳","尚书右仆射","仕为秦王府参军迁大理少卿，犯颜谏诤累辨冤狱，子至德亦为右仆射"),
  per("PER-009","李延寿","人物","唐","相州","崇文馆学士","尝追述父志作南北史一百八十篇，又撰太宗政典"),
  per("PER-010","源乾曜","人物","唐","临漳","相","第进士，开元中拜相，帝东幸以京兆尹留守京师，治尚宽简"),
  per("PER-011","韩琦","人物","宋","安阳","魏国公","天圣中弱冠举进士，嘉祐中拜相，其后拥英立神不动声色措天下于泰山之安，封魏国公谥忠献"),
  per("PER-012","韩忠彦","人物","宋","安阳","左仆射","琦子举进士，徽宗时拜右仆射，进左仆射封仪国公"),
  per("PER-013","岳飞","人物","宋","汤阴","鄂王","少负气节好左氏春秋孙吴兵法，用兵能以寡敌众屡破强敌，为秦桧所害，追封鄂王谥武穆"),
  per("PER-014","韩浩","人物","宋","安阳","奉直大夫","琦孙靖康中守潍州，建炎二年金人攻城浩率众死守城陷力战死之"),
  per("PER-015","姚兴","人物","宋","相州","容州观察使","金兵渡淮兴以四百骑当金人十数万，自辰至午战数十合援兵不至父子俱死"),
  per("PER-016","赵秉文","人物","金","滏阳","礼部尚书","举进士累官礼部尚书翰林学士，有才藻工书翰，所著有滏水文集"),
  per("PER-017","许有壬","人物","元","汤阴","中书左丞","延祐中进士累官集贤大学士，历事七朝垂五十年，所著有至正集谥文忠"),
  per("PER-018","郭资","人物","明","武安","太子太师","洪武乙丑进士，永乐初擢北京刑部尚书改户部，居官清介士林重之"),
  per("PER-019","崔铣","人物","明","安阳","国子监祭酒","弘治乙丑进士，累官国子监祭酒究心理学，与王湛相友善"),
  per("PER-020","王庭筠","流寓","金","河东","翰林修撰","罢归卜居彰德买田隆虑读书黄华山寺，因号黄华山主，工诗能文书学米元章"),
  per("PER-021","许氏","列女","元","安阳","赵洙妻","大学士有壬侄女，元末贼陷辽阳洙以叱贼死，贼诱许氏复以刃胁之，许氏骂不绝口遂遇害"),
  per("PER-022","马氏","列女","明","汤阴","薛鷇妻","幼读孝经列女传通大义，生一女鷇拙于家事妇翁怒责遂离去，逾三年父母欲令适人，乃投井而死"),
  per("PER-023","萧綦","仙释","汉末","","碧霄真人","修道天平山延寿宫善吹箫能致鸾凤翔集，号碧霄真人，道成白日冲举"),
  per("PER-024","李志方","仙释","金","安阳","重玄子","初名益，弃官隐隆虑山坐炼久之，谒邱处机锡号重玄子，尝主天庆宫有万鹤绕坛之异"),
]
pers2 = {"item_id":IID,"volume":"27","source":"彰德府-人物流寓列女仙释","region":"河南",
  "layers":{"ents":[],"geos":[],"evos":[],"mtns":[],"pers":pers2_data,"sites":[],"prods":[],"cits":[]},
  "layer_count":7,"validation":{"errs":[],"gap":0,"notes":"人物流寓列女仙释层拆分"}}
with open(os.path.join(OUT,"27-002_彰德府_pers2_人物列女仙释.json"),"w",encoding="utf-8") as f:
    json.dump(pers2,f,ensure_ascii=False,indent=2)
print("pers2 done")

# ===== sites =====
sites_data = [
  site("SITE-001","彰德府学","学校","在府治西","宋至和间建，本朝洪武三年重建"),
  site("SITE-002","昼锦堂","宫室","在府治北","宋韩琦以宰相判乡郡建于居第，欧阳修记蔡襄书碑刻尚存"),
  site("SITE-003","醉白堂","宫室","在府治北","韩琦建于居第池上，名曰醉白取白乐天池上之诗，苏轼为记"),
  site("SITE-004","清风楼","宫室","在府城内","宋相韩琦建"),
  site("SITE-005","铜雀台","古迹","在临漳县治西","魏曹操筑，并金虎冰井三台相去各六十步，上铸大铜雀高一五尺置之楼顶"),
  site("SITE-006","邺城","古迹","在临漳县西二十里","本战国魏之邺邑，三国魏后赵前燕东魏皆都于此"),
  site("SITE-007","羑里","古迹","在汤阴县北九里","一名牖城又名安阳城，即纣囚文王处"),
  site("SITE-008","岳飞庙","祠庙","在汤阴县治西南","飞宋将，本朝建赐额精忠，敕有司春秋致祭"),
  site("SITE-009","扁鹊庙","祠庙","在汤阴县东南一十五里伏道村","扁鹊古名医为同辈所嫉刺杀于此，祠堂碑刻尚存"),
  site("SITE-010","西门豹庙","祠庙","在府城北大夫村","北齐天保间建碑刻尚存"),
  site("SITE-011","韩琦庙","祠庙","在府治东南昼锦坊","琦宋相封魏国忠献王"),
  site("SITE-012","曹操疑冢","陵墓","在讲武城外凡七十二处","森然弥望高者如小山布列直至磁州而止"),
  site("SITE-013","韩琦墓","陵墓","在安阳县旧辅岩县城","琦卒之前一夕大星陨治所，神宗命发两河卒为治冢，篆其碑曰两朝顾命定策元勋"),
  site("SITE-014","安阳桥","关梁","在府城北四里跨洹水","旧名鲸背"),
  site("SITE-015","天宁寺","寺观","在府治西北","周广顺初建"),
]
sites = {"item_id":IID,"volume":"27","source":"彰德府-寺观祠庙古迹","region":"河南",
  "layers":{"ents":[],"geos":[],"evos":[],"mtns":[],"pers":[],"sites":sites_data,"prods":[],"cits":[]},
  "layer_count":7,"validation":{"errs":[],"gap":0,"notes":"sites层拆分"}}
with open(os.path.join(OUT,"27-002_彰德府_sites.json"),"w",encoding="utf-8") as f:
    json.dump(sites,f,ensure_ascii=False,indent=2)
print("sites done")

print("彰德府 main files done!")

