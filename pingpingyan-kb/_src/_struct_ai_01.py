# -*- coding: utf-8 -*-
"""《平平言》结构化四维源数据（卷01 全量）——AI 判定装填。
dim 顶层封闭（ACT/FRD/LGR/TME）；act_type/frd_type/lgr_type/tme_type 命中枚举；
target 引用 ent_id（须已存在于 ent_keys 或本卷源数据）。"""

RECORDS = [
    # 01-001 造福莫如州縣
    {"item_id": "01-001", "dim": "ACT", "act_type": "official", "target": "", "evidence": "造福莫如州縣、造孽莫如州縣", "confidence": "high"},
    # 01-002 造孽莫如州縣
    {"item_id": "01-002", "dim": "FRD", "frd_type": "abuse", "target": "", "evidence": "州縣造孽：社倉保甲等美政轉成害民之政", "confidence": "high"},
    # 01-003 官不易做
    {"item_id": "01-003", "dim": "ACT", "act_type": "official", "target": "", "evidence": "做官是苦事，欲造福先須耐苦", "confidence": "high"},
    # 01-021 正五九月可上官
    {"item_id": "01-021", "dim": "TME", "tme_type": "season", "target": "", "evidence": "正五九月可上官之忌月考辨", "confidence": "high"},
    # 01-025 各房呈須知冊
    {"item_id": "01-025", "dim": "LGR", "lgr_type": "ledger", "target": "", "evidence": "各房各造須知冊呈送新任", "confidence": "high"},
    # 01-026 清查前任命盜各案
    {"item_id": "01-026", "dim": "TME", "tme_type": "deadline", "target": "", "evidence": "清查前任未結命盜各案，嚴定審限參限", "confidence": "high"},
    # 01-027 工房呈輿圖
    {"item_id": "01-027", "dim": "LGR", "lgr_type": "template_form", "target": "", "evidence": "工房呈輿圖，仿開方計里之法", "confidence": "high"},
    # 01-033 大計
    {"item_id": "01-033", "dim": "TME", "tme_type": "assessment", "target": "", "evidence": "三年大計，卓異六法四格考課", "confidence": "high"},
    # 01-035 事不可入廟門者斷不可為
    {"item_id": "01-035", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "發念之端不可入廟門者斷不可為", "confidence": "high"},
    # 01-036 官不可貪
    {"item_id": "01-036", "dim": "FRD", "frd_type": "abuse", "target": "", "evidence": "貪賄六因：壞心術/敗風俗/損聲名/干國法/辱祖宗/毒子孫", "confidence": "high"},
    # 01-037 官不必貪
    {"item_id": "01-037", "dim": "FRD", "frd_type": "abuse", "target": "", "evidence": "貪賄六不必：眾人分肥/家丁挾制/書差恥笑/畏上控/畏同寅/畏上司訪聞", "confidence": "high"},
    # 01-038 貪吏惟恐民之不窮
    {"item_id": "01-038", "dim": "FRD", "frd_type": "abuse", "target": "", "evidence": "貪吏惟恐富民不窮，誣陷富戶詐財", "confidence": "high"},
    # 01-039 官不可與民爭利（正文=義利關論）
    {"item_id": "01-039", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "義利關如酖毒入口即死，萬萬不可嘗試", "confidence": "high"},
    # 01-040 義利關乃人鬼界（正文=崇陽案）
    {"item_id": "01-040", "dim": "FRD", "frd_type": "abuse", "target": "", "evidence": "派差爭掘陰沉木與民爭利被參革", "confidence": "high"},
    # 01-040 義利關乃人鬼界
    {"item_id": "01-040", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "義利關如酖毒入口即死，萬萬不可嘗試", "confidence": "high"},
    # 01-041 退一步想
    {"item_id": "01-041", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "退一步想貪心自息", "confidence": "high"},
    # 01-042 惷氣
    {"item_id": "01-042", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "自安於惷，不用門丁、撲捕蝗、不愛寶", "confidence": "high"},
    # 01-043 官民交財
    {"item_id": "01-043", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "用現銀平買、出示准鋪戶扭稟強賒", "confidence": "high"},
    # 01-044 官價
    {"item_id": "01-044", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "官價累民，量入為出定裁革", "confidence": "high"},
    # 01-045 陋規
    {"item_id": "01-045", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "陋規應裁/不必裁/去太甚之界；汪劉兩說", "confidence": "high"},
    # 01-046 革陋規非易事
    {"item_id": "01-046", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "革陋規密速行之防棍蠹撞騙", "confidence": "high"},
    # 01-047 不儉用必貪贓
    {"item_id": "01-047", "dim": "FRD", "frd_type": "abuse", "target": "", "evidence": "奢華→缺用→借債→貪贓之鏈", "confidence": "high"},
    # 01-048 不儉用必虧空
    {"item_id": "01-048", "dim": "FRD", "frd_type": "abuse", "target": "", "evidence": "不節用必虧空公帑，侵盜那移", "confidence": "high"},
    # 01-049 優缺亦不可奢華
    {"item_id": "01-049", "dim": "FRD", "frd_type": "evil_custom", "target": "", "evidence": "一人奢華一家奢華，罷後立涸", "confidence": "high"},
    # 01-050 儉非吝嗇
    {"item_id": "01-050", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "可省則省，救急大事不可惜費", "confidence": "high"},
    # 01-051 清慎勤
    {"item_id": "01-051", "dim": "ACT", "act_type": "official", "target": "", "evidence": "清慎勤三字訣，清為第一義", "confidence": "high"},
    # 01-052 勤則少暇
    {"item_id": "01-052", "dim": "ACT", "act_type": "official", "target": "", "evidence": "勤則少暇，民傭之說", "confidence": "high"},
    # 01-053 官不可不明
    {"item_id": "01-053", "dim": "ACT", "act_type": "official", "target": "", "evidence": "清慎勤之外尚須明", "confidence": "high"},
    # 01-055 官不可過用其明
    {"item_id": "01-055", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "過用其明則下不能堪，其政察察其民缺缺", "confidence": "high"},
    # 01-056 精明渾厚
    {"item_id": "01-056", "dim": "ACT", "act_type": "official", "target": "", "evidence": "精明渾厚不可離開", "confidence": "high"},
    # 01-057 緩
    {"item_id": "01-057", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "先以暴怒為戒，緩即從容詳處", "confidence": "high"},
    # 01-058 勿喜事
    {"item_id": "01-058", "dim": "ACT", "act_type": "official", "target": "", "evidence": "為政在省事守法安靜寬簡", "confidence": "high"},
    # 01-059 熱腸
    {"item_id": "01-059", "dim": "ACT", "act_type": "official", "target": "", "evidence": "民生休戚腸不可不熱", "confidence": "high"},
    # 01-060 擔當
    {"item_id": "01-060", "dim": "ACT", "act_type": "official", "target": "", "evidence": "辦大事須有擔當，功名置度外", "confidence": "high"},
    # 01-061 淺露
    {"item_id": "01-061", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "淺露最誤事，戒肆口揚言", "confidence": "high"},
    # 01-062 成見
    {"item_id": "01-062", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "不可預存成見，平其心", "confidence": "high"},
    # 01-065 立法求其可行
    {"item_id": "01-065", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "立法先求可行，不冒昧行", "confidence": "high"},
    # 01-066 法立弊生不可因噎廢食
    {"item_id": "01-066", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "法立弊生不可因噎廢食", "confidence": "high"},
    # 01-067 天不為荊棘靳雨露
    {"item_id": "01-067", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "利民之事被阻撓仍舊照行", "confidence": "high"},
    # 01-068 不必親身私訪
    {"item_id": "01-068", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "私訪最誤事，有私訪之名無其實", "confidence": "high"},
    # 01-069 不可派人私訪
    {"item_id": "01-069", "dim": "FRD", "frd_type": "abuse", "target": "", "evidence": "派人私訪易生奸胥假稱奉命招搖訛詐", "confidence": "high"},
    # 01-070 官不可好名
    {"item_id": "01-070", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "好名純盜虛聲必至名裂", "confidence": "high"},
    # 01-073 惡居下流
    {"item_id": "01-073", "dim": "FRD", "frd_type": "guard", "target": "", "evidence": "平日聲名太壞，民不信服", "confidence": "high"},
    # 01-074 官不可不畏民
    {"item_id": "01-074", "dim": "ACT", "act_type": "official", "target": "", "evidence": "官不畏民是謂亂階", "confidence": "high"},
    # 01-077 親民工夫
    {"item_id": "01-077", "dim": "ACT", "act_type": "xiangyue_role", "target": "", "evidence": "下鄉招耆老諮詢勸孝弟力田", "confidence": "high"},
    # 01-080 咨訪風俗
    {"item_id": "01-080", "dim": "ACT", "act_type": "official", "target": "", "evidence": "博訪周咨留心體察民風土俗", "confidence": "high"},
    # 01-083 閱文稿
    {"item_id": "01-083", "dim": "LGR", "lgr_type": "ledger", "target": "", "evidence": "文稿須親閱，不可盡付書吏幕賓", "confidence": "high"},
    # 01-084 拆公文
    {"item_id": "01-084", "dim": "LGR", "lgr_type": "ledger", "target": "", "evidence": "公文必須親拆或家丁當面拆封", "confidence": "high"},
]
