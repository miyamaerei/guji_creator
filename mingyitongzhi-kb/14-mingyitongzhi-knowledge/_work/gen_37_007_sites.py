# -*- coding: utf-8 -*-
import json, os

OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol37"

# ===== sites1: 古迹+祠庙+寺观 =====
sites1 = [
 # 古迹
 {"site_id":"SIT-001","item_id":"37-007","geo_id":"GEO-37007","name":"居延城","type":"古迹","location_text":"在甘州卫城东北","description":"本匈奴地，一曰居延塞，汉张掖郡居延县治此，武帝尝使路博德于此筑遮虏障"},
 {"site_id":"SIT-002","item_id":"37-007","geo_id":"GEO-37007","name":"大通城","type":"古迹","location_text":"在西宁卫城东北","description":"旧名达南，地形险要控扼夏境，宋崇宁间收复湟鄯乃筑塞拒守名曰大通，又名米川城"},
 {"site_id":"SIT-003","item_id":"37-007","geo_id":"GEO-37007","name":"永昌城","type":"古迹","location_text":"在凉州卫城北三十里","description":"元永昌路治此"},
 {"site_id":"SIT-004","item_id":"37-007","geo_id":"GEO-37007","name":"额齐讷城","type":"古迹","location_text":"在肃州东北五百里，南至甘州一千五百里","description":"晋为西海郡居延县地，夏国立威福军，元立额齐讷路总管府领山丹西宁二州，今废"},
 {"site_id":"SIT-005","item_id":"37-007","geo_id":"GEO-37007","name":"瓜州城","type":"古迹","location_text":"在肃州卫城西五百二十六里","description":"古西戎地，汉为炖煌郡地，晋分置晋昌郡，后魏属常乐会稽二郡，隋属炖煌郡；唐置瓜州后陷于吐蕃，宋时为西夏所据，元徙居民于肃州但名存而已"},
 {"site_id":"SIT-006","item_id":"37-007","geo_id":"GEO-37007","name":"沙州城","type":"古迹","location_text":"在肃州卫城西八百余里","description":"秦及汉初为月支匈奴境，武帝置炖煌郡领炖煌广至等六县；东晋时张轨据此置商州，其后凉武昭王都此；后魏为炖煌郡，隋初废郡置瓜州，唐改沙州，后张义潮曹义金相继有其地；宋时西夏据之，元置沙州路；本朝初置沙州卫以首领困即来为都督治之，正统中徙其众于内地但名存而已"},
 {"site_id":"SIT-007","item_id":"37-007","geo_id":"GEO-37007","name":"宜禾城","type":"古迹","location_text":"在故瓜州西北界","description":"汉宜禾都尉治此，晋为县，苻坚时徙江汉之人万余户于此，后魏明帝时侨置会稽郡"},
 {"site_id":"SIT-008","item_id":"37-007","geo_id":"GEO-37007","name":"曲尤城","type":"古迹","location_text":"在肃州卫境之西","description":""},
 {"site_id":"SIT-009","item_id":"37-007","geo_id":"GEO-37007","name":"胭脂城","type":"古迹","location_text":"在肃州卫境之北","description":""},
 {"site_id":"SIT-010","item_id":"37-007","geo_id":"GEO-37007","name":"白城子","type":"古迹","location_text":"在肃州卫城东北一百二十里","description":"元志云在黑水河之西，又瓜州北亦有白城子"},
 {"site_id":"SIT-011","item_id":"37-007","geo_id":"GEO-37007","name":"黑城子","type":"古迹","location_text":"在庄浪卫城南二十五里","description":""},
 {"site_id":"SIT-012","item_id":"37-007","geo_id":"GEO-37007","name":"西宁废州","type":"古迹","location_text":"在西宁卫城西南","description":"宋置州，今废"},
 {"site_id":"SIT-013","item_id":"37-007","geo_id":"GEO-37007","name":"姑臧废县","type":"古迹","location_text":"在凉州卫城东北二里","description":"汉置县为武威郡治，晋隋因之，唐凉州治焉，遗址尚存"},
 {"site_id":"SIT-014","item_id":"37-007","geo_id":"GEO-37007","name":"晋昌废县","type":"古迹","location_text":"在故瓜州北","description":"本汉宜安县属炖煌郡，隋改常乐县，唐改曰晋昌"},
 {"site_id":"SIT-015","item_id":"37-007","geo_id":"GEO-37007","name":"广至废县","type":"古迹","location_text":"在故瓜州西北一百余里","description":"汉置属炖煌郡，晋因之后废"},
 {"site_id":"SIT-016","item_id":"37-007","geo_id":"GEO-37007","name":"寿昌废县","type":"古迹","location_text":"在沙州城西南一百五十里","description":"本汉龙勒县地，后魏置寿昌县"},
 # 祠庙
 {"site_id":"SIT-017","item_id":"37-007","geo_id":"GEO-37007","name":"王母祠","type":"祠庙","location_text":"在昆仑山上","description":""},
 {"site_id":"SIT-018","item_id":"37-007","geo_id":"GEO-37007","name":"刘师祠","type":"祠庙","location_text":"在肃州卫治南","description":"寰宇记师姓刘字摩诃，沮渠蒙逊时西求仙死于此，骨化为珠血为丹，其徒为之立祠，相传祷者往往获珠丹焉"},
 {"site_id":"SIT-019","item_id":"37-007","geo_id":"GEO-37007","name":"宁济公祠","type":"祠庙","location_text":"在焉支山南麓","description":"唐建；天宝间封焉支山山神为宁济公"},
 {"site_id":"SIT-020","item_id":"37-007","geo_id":"GEO-37007","name":"苏武庙","type":"祠庙","location_text":"在苏武山侧","description":""},
 {"site_id":"SIT-021","item_id":"37-007","geo_id":"GEO-37007","name":"龙王庙","type":"祠庙","location_text":"在都司城西南八十里张掖河水经流处","description":"旧名河渎神庙"},
 # 寺观
 {"site_id":"SIT-022","item_id":"37-007","geo_id":"GEO-37007","name":"宝觉寺","type":"寺观","location_text":"在都司治西南","description":"旧名卧佛寺，宣德初改今名"},
 {"site_id":"SIT-023","item_id":"37-007","geo_id":"GEO-37007","name":"大云寺","type":"寺观","location_text":"在凉州卫治东北","description":"唐景云中建"},
 {"site_id":"SIT-024","item_id":"37-007","geo_id":"GEO-37007","name":"庄严寺","type":"寺观","location_text":"在庄浪卫治东北","description":"元建"},
 {"site_id":"SIT-025","item_id":"37-007","geo_id":"GEO-37007","name":"宁番寺","type":"寺观","location_text":"在西宁卫治西北","description":"旧名大佛寺，永乐中改建"},
 {"site_id":"SIT-026","item_id":"37-007","geo_id":"GEO-37007","name":"普观寺","type":"寺观","location_text":"在祁连山下","description":"旧名马蹄佛，内有石洞七，洞各有石寺"},
 {"site_id":"SIT-027","item_id":"37-007","geo_id":"GEO-37007","name":"发塔寺","type":"寺观","location_text":"在山丹卫治东南","description":"旧有佛塔，洪武间筑城于塔址下得铁佛五石函一石香炉一，函内有发炉，上刻发塔寺数字"},
 {"site_id":"SIT-028","item_id":"37-007","geo_id":"GEO-37007","name":"佑善观","type":"寺观","location_text":"在都司治西北","description":"宣德中因旧重修，正统初改今名"},
 {"site_id":"SIT-029","item_id":"37-007","geo_id":"GEO-37007","name":"清真观","type":"寺观","location_text":"在凉州卫治南","description":"永乐中因旧重修"},
 {"site_id":"SIT-030","item_id":"37-007","geo_id":"GEO-37007","name":"集福观","type":"寺观","location_text":"在庄浪卫治南","description":"洪熙元年建"},
 {"site_id":"SIT-031","item_id":"37-007","geo_id":"GEO-37007","name":"广福观","type":"寺观","location_text":"在西宁卫治东","description":"宣德初因旧重修"}
]

sites1_file = {
 "item_id":"37-007","volume":"37","source":"陕西行都指挥使司","region":"陕西行都司",
 "layer":"sites","subsection":"古迹+祠庙+寺观",
 "sites":sites1,
 "validation":{"errs":[],"count":len(sites1),"notes":"古迹16+祠庙5+寺观10=31处"}
}
with open(os.path.join(OUT,"37-007_sites1_古迹祠庙寺观.json"),"w",encoding="utf-8") as f:
 json.dump(sites1_file,f,ensure_ascii=False,indent=1)
print("sites1 written:",len(sites1))

# ===== sites2: 学校+公署+宫室+关梁 =====
sites2 = [
 # 学校
 {"site_id":"SIT-032","item_id":"37-007","geo_id":"GEO-37007","name":"陕西行都司学","type":"学校","location_text":"在都司城内东北","description":"洪武二十八年建，正统十二年重修"},
 {"site_id":"SIT-033","item_id":"37-007","geo_id":"GEO-37007","name":"山丹卫学","type":"学校","location_text":"在卫治东南","description":"正统五年建"},
 {"site_id":"SIT-034","item_id":"37-007","geo_id":"GEO-37007","name":"凉州卫学","type":"学校","location_text":"在卫治东南","description":"正统二年建"},
 {"site_id":"SIT-035","item_id":"37-007","geo_id":"GEO-37007","name":"永昌卫学","type":"学校","location_text":"在卫治东北","description":"正统间建"},
 {"site_id":"SIT-036","item_id":"37-007","geo_id":"GEO-37007","name":"西宁卫学","type":"学校","location_text":"在卫治东","description":"宣德二年建"},
 # 公署
 {"site_id":"SIT-037","item_id":"37-007","geo_id":"GEO-37007","name":"行太仆寺","type":"公署","location_text":"在都司城内西北隅","description":""},
 {"site_id":"SIT-038","item_id":"37-007","geo_id":"GEO-37007","name":"西宁茶马司","type":"公署","location_text":"在西宁卫西","description":"洪武中建"},
 # 宫室
 {"site_id":"SIT-039","item_id":"37-007","geo_id":"GEO-37007","name":"灵钧台","type":"宫室","location_text":"在凉州卫治北","description":"晋明帝太宁初张茂立姑臧时所筑，遗址尚存"},
 {"site_id":"SIT-040","item_id":"37-007","geo_id":"GEO-37007","name":"刘林台","type":"宫室","location_text":"在凉州卫治西北五里","description":"相传汉窦融所筑，旧名窦融台；本朝洪武初百户刘林战死，城下人皆重其忠节因改今名"},
 # 关梁
 {"site_id":"SIT-041","item_id":"37-007","geo_id":"GEO-37007","name":"嘉峪关","type":"关梁/关","location_text":"在肃州卫城西六十里","description":"其在城南又有文殊山硫黄山，东南有寒水石山红山观音山凡五口"},
 {"site_id":"SIT-042","item_id":"37-007","geo_id":"GEO-37007","name":"黑山关","type":"关梁/关","location_text":"在镇番卫西南六十里","description":""},
 {"site_id":"SIT-043","item_id":"37-007","geo_id":"GEO-37007","name":"杂木口关","type":"关梁/关","location_text":"在凉州卫城东三十里","description":"又城西南有俺公山，南有倘哥儿山，东山干沟山，东南有黄羊川下古城等口"},
 {"site_id":"SIT-044","item_id":"37-007","geo_id":"GEO-37007","name":"水磨川关","type":"关梁/关","location_text":"在永昌卫城西二十里","description":"又城西有白石崖山，西南有平羌山脑儿都山鸾鸟山，南有一颗树山，东南有土鲁于山长城山凡七口，以上关口各卫分兵防守"},
 {"site_id":"SIT-045","item_id":"37-007","geo_id":"GEO-37007","name":"玉门关","type":"关梁/关","location_text":"在故瓜州西北一十八里","description":"汉霍去病破走月支开玉门关，班超在西域上书愿生入玉门关即此"},
 {"site_id":"SIT-046","item_id":"37-007","geo_id":"GEO-37007","name":"阳关","type":"关梁/关","location_text":"在废寿昌县西六里","description":"唐诗西出阳关无故人谓此"},
 {"site_id":"SIT-047","item_id":"37-007","geo_id":"GEO-37007","name":"人祖山口","type":"关梁/口","location_text":"在都司城东北四十五里","description":"又城西南有大磁窑小磁窑甘浚山凡三口"},
 {"site_id":"SIT-048","item_id":"37-007","geo_id":"GEO-37007","name":"通远口","type":"关梁/口","location_text":"在都司城南八十里","description":"又南有顺化宣政阳化和宁大慕化小慕化洪水山凡七口"},
 {"site_id":"SIT-049","item_id":"37-007","geo_id":"GEO-37007","name":"红寺山口","type":"关梁/口","location_text":"在山丹卫城北二十五里","description":"其在卫南百余里又有静宁山和宁山无虞山宁番山凡四口"},
 {"site_id":"SIT-050","item_id":"37-007","geo_id":"GEO-37007","name":"石峡口","type":"关梁/口","location_text":"在西宁卫城东七十里","description":"其在卫西又有癿铁沟山伯颜川山西番沟山，在卫南有那海川山可可打班山，在卫北有车卜鲁川山黑松林山撒儿山总八口，以上口皆有戌守"},
 {"site_id":"SIT-051","item_id":"37-007","geo_id":"GEO-37007","name":"沙河堡","type":"关梁/堡","location_text":"在都司城西","description":"又西有甘浚高台，南有小满，东南有黑城，共五堡属甘州左卫"},
 {"site_id":"SIT-052","item_id":"37-007","geo_id":"GEO-37007","name":"长乐堡","type":"关梁/堡","location_text":"在都司城西北","description":"又城南有大满顺化，西北有平源，共四堡属甘州右卫"},
 {"site_id":"SIT-053","item_id":"37-007","geo_id":"GEO-37007","name":"镇平堡","type":"关梁/堡","location_text":"在都司城东南","description":"又城南有小慕化，西有抚夷，西北有平川胭脂，共五堡属甘州中卫"},
 {"site_id":"SIT-054","item_id":"37-007","geo_id":"GEO-37007","name":"柳树堡","type":"关梁/堡","location_text":"在都司城西北","description":"又东南有古城洪水东，共三堡属甘州前卫"},
 {"site_id":"SIT-055","item_id":"37-007","geo_id":"GEO-37007","name":"板桥堡","type":"关梁/堡","location_text":"在都司城西北","description":"属甘州后卫"},
 {"site_id":"SIT-056","item_id":"37-007","geo_id":"GEO-37007","name":"永宁堡","type":"关梁/堡","location_text":"在肃州卫城东","description":"又城南有永安永清，东南有永定盐池，共五堡"},
 {"site_id":"SIT-057","item_id":"37-007","geo_id":"GEO-37007","name":"新河堡","type":"关梁/堡","location_text":"在山丹卫城东","description":"又城东南有永兴暖泉大黄山西南有洪水三洪水店，共六堡"},
 {"site_id":"SIT-058","item_id":"37-007","geo_id":"GEO-37007","name":"乐善堡","type":"关梁/堡","location_text":"在永昌卫城东","description":"又城西有水磨川堡"},
 {"site_id":"SIT-059","item_id":"37-007","geo_id":"GEO-37007","name":"怀安堡","type":"关梁/堡","location_text":"在凉州卫城西","description":"又城北有旧永昌，东有杂木口靖边，共四堡"},
 {"site_id":"SIT-060","item_id":"37-007","geo_id":"GEO-37007","name":"西乐堡","type":"关梁/堡","location_text":"在镇番卫城西","description":"又城东有东安堡"},
 {"site_id":"SIT-061","item_id":"37-007","geo_id":"GEO-37007","name":"应理州堡","type":"关梁/堡","location_text":"在庄浪卫城东","description":"又城东有泗水，西有西大通，南有红城子，共四堡"},
 {"site_id":"SIT-062","item_id":"37-007","geo_id":"GEO-37007","name":"伯颜川堡","type":"关梁/堡","location_text":"在西宁卫城西","description":"又城东有石峡平戎，东南有巴州，北有车卜鲁川，共五堡；自永宁堡至此各属本卫，以上堡俱有军屯守"},
 {"site_id":"SIT-063","item_id":"37-007","geo_id":"GEO-37007","name":"防卫堡","type":"关梁/堡","location_text":"有二，俱在镇番卫城西南","description":"旧属甘州中护卫"},
 {"site_id":"SIT-064","item_id":"37-007","geo_id":"GEO-37007","name":"红水塞","type":"关梁/塞","location_text":"在凉州卫城东北","description":""},
 {"site_id":"SIT-065","item_id":"37-007","geo_id":"GEO-37007","name":"暖泉塞","type":"关梁/塞","location_text":"在凉州卫城东","description":""},
 {"site_id":"SIT-066","item_id":"37-007","geo_id":"GEO-37007","name":"清水河桥","type":"关梁/桥","location_text":"在肃州卫城北","description":"跨清水河"},
 {"site_id":"SIT-067","item_id":"37-007","geo_id":"GEO-37007","name":"大通河桥","type":"关梁/桥","location_text":"在庄浪卫城西","description":"跨大通河"},
 {"site_id":"SIT-068","item_id":"37-007","geo_id":"GEO-37007","name":"黑水渡","type":"关梁/渡","location_text":"在镇夷城南五里","description":""}
]

sites2_file = {
 "item_id":"37-007","volume":"37","source":"陕西行都指挥使司","region":"陕西行都司",
 "layer":"sites","subsection":"学校+公署+宫室+关梁",
 "sites":sites2,
 "validation":{"errs":[],"count":len(sites2),"notes":"学校5+公署2+宫室2+关梁29=38处"}
}
with open(os.path.join(OUT,"37-007_sites2_宫室关梁学校公署.json"),"w",encoding="utf-8") as f:
 json.dump(sites2_file,f,ensure_ascii=False,indent=1)
print("sites2 written:",len(sites2))
print("DONE")
