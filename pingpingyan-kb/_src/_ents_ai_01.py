# -*- coding: utf-8 -*-
"""《平平言》实体源数据（卷01 全量 84 条）——AI 判定装填。
C3：只写条号 + 解读字段；text 逐字命中原文词形（GAP 纪律）；original 由打包器注入。"""

RECORDS = [
    # 01-001 造福莫如州縣
    {"item_id": "01-001", "text": "州縣", "type": "official", "confidence": "high"},
    {"item_id": "01-001", "text": "章楓山", "type": "person", "confidence": "high"},
    {"item_id": "01-001", "text": "督撫", "type": "official", "confidence": "high"},
    {"item_id": "01-001", "text": "臨武知縣", "type": "official", "confidence": "high"},
    {"item_id": "01-001", "text": "南京大理寺丞", "type": "official", "confidence": "high"},
    # 01-002 造孽莫如州縣
    {"item_id": "01-002", "text": "州縣", "type": "official", "confidence": "high"},
    {"item_id": "01-002", "text": "社倉", "type": "system", "confidence": "high"},
    {"item_id": "01-002", "text": "保甲", "type": "system", "confidence": "high"},
    {"item_id": "01-002", "text": "奸胥蠹役", "type": "unknown", "confidence": "medium"},
    # 01-003 官不易做
    {"item_id": "01-003", "text": "呂新吾先生", "type": "person", "confidence": "high"},
    {"item_id": "01-003", "text": "王朗川先生", "type": "person", "confidence": "high"},
    {"item_id": "01-003", "text": "州縣", "type": "official", "confidence": "high"},
    # 01-006 候補宜讀書（应读之书目录成体系：work 实体密集）
    {"item_id": "01-006", "text": "福惠全書", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "圖民錄", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "牧令書", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "佐治藥言", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "學治臆說", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "庸吏庸言", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "折獄龜鑑", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "大清會典", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "大清律例", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "洗冤錄", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "處分則例", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "邸鈔", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "海國圖志", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "農政全書", "type": "work", "confidence": "high"},
    {"item_id": "01-006", "text": "汪輝祖", "type": "person", "confidence": "high"},
    {"item_id": "01-006", "text": "劉衡", "type": "person", "confidence": "high"},
    {"item_id": "01-006", "text": "胡林翼", "type": "person", "confidence": "high"},
    # 01-011 候補人員見上司
    {"item_id": "01-011", "text": "首府首縣", "type": "official", "confidence": "medium"},
    # 01-012 君相不能造命
    {"item_id": "01-012", "text": "能改齋漫錄", "type": "work", "confidence": "high"},
    {"item_id": "01-012", "text": "朝野僉載", "type": "work", "confidence": "high"},
    {"item_id": "01-012", "text": "元魏徵", "type": "person", "confidence": "high"},
    # 01-014 無恥
    {"item_id": "01-014", "text": "嚴分宜", "type": "person", "confidence": "high"},
    {"item_id": "01-014", "text": "張江陵", "type": "person", "confidence": "high"},
    {"item_id": "01-014", "text": "顧亭林先生", "type": "person", "confidence": "high"},
    # 01-015 候補當差
    {"item_id": "01-015", "text": "湖北", "type": "place", "confidence": "high"},
    {"item_id": "01-015", "text": "元微之", "type": "person", "confidence": "high"},
    # 01-018 候補時宜訪求幕友
    {"item_id": "01-018", "text": "刑錢幕友", "type": "official", "confidence": "high"},
    # 01-021 正五九月可上官
    {"item_id": "01-021", "text": "雲溪漫鈔", "type": "work", "confidence": "high"},
    {"item_id": "01-021", "text": "菽園雜記", "type": "work", "confidence": "high"},
    {"item_id": "01-021", "text": "南齊書", "type": "work", "confidence": "high"},
    {"item_id": "01-021", "text": "北齊書", "type": "work", "confidence": "high"},
    {"item_id": "01-021", "text": "左傳", "type": "work", "confidence": "high"},
    {"item_id": "01-021", "text": "漢書", "type": "work", "confidence": "high"},
    {"item_id": "01-021", "text": "顧亭林先生", "type": "person", "confidence": "high"},
    {"item_id": "01-021", "text": "唐高祖", "type": "person", "confidence": "high"},
    # 01-022 四絕四離四不祥月忌不足信
    {"item_id": "01-022", "text": "襄陽", "type": "place", "confidence": "high"},
    # 01-023 到任可進南門
    {"item_id": "01-023", "text": "襄陽", "type": "place", "confidence": "high"},
    {"item_id": "01-023", "text": "荊州", "type": "place", "confidence": "high"},
    # 01-025 各房呈須知冊
    {"item_id": "01-025", "text": "須知冊", "type": "doc", "confidence": "high"},
    {"item_id": "01-025", "text": "各房", "type": "institution", "confidence": "medium"},
    # 01-026 清查前任命盜各案
    {"item_id": "01-026", "text": "刑房", "type": "institution", "confidence": "high"},
    {"item_id": "01-026", "text": "審限", "type": "system", "confidence": "high"},
    {"item_id": "01-026", "text": "參限", "type": "system", "confidence": "high"},
    {"item_id": "01-026", "text": "命盜各案", "type": "unknown", "confidence": "medium"},
    # 01-027 工房呈輿圖
    {"item_id": "01-027", "text": "輿圖", "type": "doc", "confidence": "high"},
    {"item_id": "01-027", "text": "工房", "type": "institution", "confidence": "high"},
    # 01-030 下馬風
    {"item_id": "01-030", "text": "袁易齋", "type": "person", "confidence": "high"},
    # 01-031 初任宜簡僻缺
    {"item_id": "01-031", "text": "衝繁疲難", "type": "system", "confidence": "high"},
    # 01-032 公罪私罪
    {"item_id": "01-032", "text": "公罪", "type": "system", "confidence": "high"},
    {"item_id": "01-032", "text": "私罪", "type": "system", "confidence": "high"},
    {"item_id": "01-032", "text": "級紀", "type": "system", "confidence": "high"},
    # 01-033 大計
    {"item_id": "01-033", "text": "大計", "type": "system", "confidence": "high"},
    {"item_id": "01-033", "text": "卓異", "type": "system", "confidence": "high"},
    {"item_id": "01-033", "text": "六法", "type": "system", "confidence": "high"},
    {"item_id": "01-033", "text": "四格", "type": "system", "confidence": "high"},
    # 01-034 吏不可俗
    {"item_id": "01-034", "text": "呂叔簡先生", "type": "person", "confidence": "high"},
    # 01-035 事不可入廟門者斷不可為
    {"item_id": "01-035", "text": "汪龍莊明府", "type": "person", "confidence": "high"},
    # 01-036 官不可貪
    {"item_id": "01-036", "text": "官", "type": "official", "confidence": "high"},
    {"item_id": "01-036", "text": "受贓", "type": "system", "confidence": "high"},
    {"item_id": "01-036", "text": "枉法贓", "type": "system", "confidence": "high"},
    {"item_id": "01-036", "text": "不枉法贓", "type": "system", "confidence": "high"},
    # 01-037 官不必貪
    {"item_id": "01-037", "text": "官", "type": "official", "confidence": "high"},
    # 01-038 貪吏惟恐民之不窮
    {"item_id": "01-038", "text": "胡文忠公", "type": "person", "confidence": "high"},
    {"item_id": "01-038", "text": "循吏", "type": "official", "confidence": "medium"},
    {"item_id": "01-038", "text": "貪吏", "type": "unknown", "confidence": "medium"},
    # 01-039 官不可與民爭利（正文=義利關乃人鬼界论：雙題連排，正文錯位，按原文裝填）
    {"item_id": "01-039", "text": "義利關", "type": "unknown", "confidence": "medium"},
    {"item_id": "01-039", "text": "酖毒", "type": "object", "confidence": "medium"},
    # 01-040 義利關乃人鬼界（正文=官不可與民爭利崇陽案）
    {"item_id": "01-040", "text": "崇陽縣", "type": "place", "confidence": "high"},
    {"item_id": "01-040", "text": "陰沉木", "type": "object", "confidence": "high"},
    {"item_id": "01-040", "text": "高皇帝實錄", "type": "work", "confidence": "high"},
    # 01-041 退一步想
    {"item_id": "01-041", "text": "胡文忠公", "type": "person", "confidence": "high"},
    {"item_id": "01-041", "text": "廣濟", "type": "place", "confidence": "high"},
    # 01-042 惷氣
    {"item_id": "01-042", "text": "襄陽", "type": "place", "confidence": "high"},
    # 01-044 官價
    {"item_id": "01-044", "text": "官價", "type": "system", "confidence": "high"},
    # 01-045 陋規
    {"item_id": "01-045", "text": "陋規", "type": "system", "confidence": "high"},
    {"item_id": "01-045", "text": "汪龍莊明府", "type": "person", "confidence": "high"},
    {"item_id": "01-045", "text": "劉簾舫觀察", "type": "person", "confidence": "high"},
    # 01-046 革陋規非易事
    {"item_id": "01-046", "text": "劉簾舫觀察", "type": "person", "confidence": "high"},
    {"item_id": "01-046", "text": "樊城", "type": "place", "confidence": "high"},
    {"item_id": "01-046", "text": "襄陽府", "type": "institution", "confidence": "high"},
    {"item_id": "01-046", "text": "老河口", "type": "place", "confidence": "high"},
    # 01-048 不儉用必虧空
    {"item_id": "01-048", "text": "侵盜", "type": "system", "confidence": "high"},
    {"item_id": "01-048", "text": "那移", "type": "system", "confidence": "high"},
    {"item_id": "01-048", "text": "倉穀", "type": "system", "confidence": "high"},
    # 01-050 儉非吝嗇
    {"item_id": "01-050", "text": "汪龍莊明府", "type": "person", "confidence": "high"},
    # 01-051 清慎勤
    {"item_id": "01-051", "text": "司馬炎", "type": "person", "confidence": "high"},
    {"item_id": "01-051", "text": "真西山先生", "type": "person", "confidence": "high"},
    # 01-052 勤則少暇
    {"item_id": "01-052", "text": "荀子脩身篇", "type": "work", "confidence": "high"},
    {"item_id": "01-052", "text": "石瑤辰郡丞", "type": "person", "confidence": "high"},
    # 01-054 曉事
    {"item_id": "01-054", "text": "吳厯", "type": "work", "confidence": "high"},
    {"item_id": "01-054", "text": "廢帝亮", "type": "person", "confidence": "high"},
    {"item_id": "01-054", "text": "裴松之", "type": "person", "confidence": "high"},
    {"item_id": "01-054", "text": "鄭克", "type": "person", "confidence": "high"},
    # 01-055 官不可過用其明
    {"item_id": "01-055", "text": "老子", "type": "work", "confidence": "high"},
    # 01-056 精明渾厚
    {"item_id": "01-056", "text": "武昌", "type": "place", "confidence": "high"},
    # 01-057 緩
    {"item_id": "01-057", "text": "劉忠定公安世", "type": "person", "confidence": "high"},
    {"item_id": "01-057", "text": "張仲賓", "type": "person", "confidence": "high"},
    {"item_id": "01-057", "text": "呂居仁", "type": "person", "confidence": "high"},
    # 01-058 勿喜事
    {"item_id": "01-058", "text": "楊文襄公", "type": "person", "confidence": "high"},
    {"item_id": "01-058", "text": "歐陽文忠公", "type": "person", "confidence": "high"},
    # 01-059 熱腸
    {"item_id": "01-059", "text": "陳文恭公", "type": "person", "confidence": "high"},
    # 01-060 擔當
    {"item_id": "01-060", "text": "洪忠宣公", "type": "person", "confidence": "high"},
    {"item_id": "01-060", "text": "范忠宣公", "type": "person", "confidence": "high"},
    {"item_id": "01-060", "text": "王竑", "type": "person", "confidence": "high"},
    {"item_id": "01-060", "text": "雲軒公", "type": "person", "confidence": "high"},
    {"item_id": "01-060", "text": "巴陵", "type": "place", "confidence": "high"},
    # 01-061 淺露
    {"item_id": "01-061", "text": "李懷光", "type": "person", "confidence": "high"},
    {"item_id": "01-061", "text": "王彥章", "type": "person", "confidence": "high"},
    {"item_id": "01-061", "text": "宋濟王", "type": "person", "confidence": "high"},
    # 01-062 成見
    {"item_id": "01-062", "text": "孟子", "type": "person", "confidence": "high"},
    {"item_id": "01-062", "text": "張子", "type": "person", "confidence": "high"},
    # 01-063 有條理
    {"item_id": "01-063", "text": "韓信", "type": "person", "confidence": "high"},
    # 01-065 立法求其可行
    {"item_id": "01-065", "text": "王安石", "type": "person", "confidence": "high"},
    {"item_id": "01-065", "text": "商鞅", "type": "person", "confidence": "high"},
    # 01-066 法立弊生不可因噎廢食
    {"item_id": "01-066", "text": "朱子", "type": "person", "confidence": "high"},
    {"item_id": "01-066", "text": "呂新吾先生", "type": "person", "confidence": "high"},
    # 01-067 天不為荊棘靳雨露
    {"item_id": "01-067", "text": "陸宣公", "type": "person", "confidence": "high"},
    # 01-068 不必親身私訪
    {"item_id": "01-068", "text": "襄陽", "type": "place", "confidence": "high"},
    # 01-071 官不可無名
    {"item_id": "01-071", "text": "子夏", "type": "person", "confidence": "high"},
    # 01-073 惡居下流
    {"item_id": "01-073", "text": "來瞿塘先生", "type": "person", "confidence": "high"},
    # 01-074 官不可不畏民
    {"item_id": "01-074", "text": "盤庚", "type": "person", "confidence": "high"},
    {"item_id": "01-074", "text": "祖已", "type": "person", "confidence": "high"},
    {"item_id": "01-074", "text": "文王", "type": "person", "confidence": "high"},
    # 01-079 告示
    {"item_id": "01-079", "text": "告示", "type": "doc", "confidence": "high"},
    # 01-080 咨訪風俗
    {"item_id": "01-080", "text": "劉忠宣公", "type": "person", "confidence": "high"},
    {"item_id": "01-080", "text": "周文襄公", "type": "person", "confidence": "high"},
    # 01-081 看本邑志書
    {"item_id": "01-081", "text": "志書", "type": "work", "confidence": "high"},
    # 01-083 閱文稿
    {"item_id": "01-083", "text": "陳文恭公", "type": "person", "confidence": "high"},
    # 01-084 拆公文
    {"item_id": "01-084", "text": "公文", "type": "doc", "confidence": "high"},
]
