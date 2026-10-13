# -*- coding: utf-8 -*-
"""
《明史·职官志》知识工程 —— 枚举单点治理
版本：V1.0（2026-10-13）
基准库快照：book-knowledge-factory references/enum-library.md v8
新增值必须 VERSION += 1 并回溯存量（registerVersion）。

沿革：
  v1.0 初版
  v1.2 加 tpl 前缀 + ORG_LEVELS 新增 4 值 + GRADE_ORDER「同北京」
  v1.3（v7）移除 ID_PREFIX["tpl"]，机构模板容器取消
  v1.4（v9，2026-10-15）新增 SALARY_TABLE / salary_of / salary_ref_of ——
       原文第 25 行洪武二十五年岁禄表入库，打通 427 条 posts 的 salary_ref。
"""
VERSION = "1.4"

# ============ L1 实体层 ============
# 继承基准库 §1.1（20 值）的本书适用子集；不适用值不写入
ENTITY_TYPES = {
    "person", "official", "institution", "place", "era", "work",
    "system", "posthumous", "time", "quantity", "punishment", "doc",
    "unknown",   # 兜底
}
# 基准库有、本书不适用（不写入快照）：object/animal/plant/food/behavior/star/event
ENTITY_ALIAS = {"office": "official", "org": "institution", "book": "work"}

# ============ L2 规则层（基准库 §1.2 七值，本书用中文键）============
RULE_TYPES = {"义务型", "禁止型", "程序型", "时限型", "处罚型", "允许型", "优先级型"}
RULE_MODALS = {"obligation", "prohibit", "procedure", "deadline",
               "penalty", "allow", "priority"}

# ============ L3 流程层 ============
# 本书四类流程；无独立枚举，name 自由文本
PROC_SCOPES = {"选官", "考察", "封赠荫叙", "朝贡接待", "其他"}

# ============ L4 结构化层：四维 ============
# v4（2026-10-14）：新增 "差遣" —— 总督/巡抚/总理/抚治/赞理等奉敕差遣之职，
#   条目形态为「<职衔>…一员。」+ 沿革叙事，无品级标注（卷02 实测 46 条仅 4 处
#   品级标注且全在括注中），故 level 与 org_type 单列，避免与正式编制混淆。
# v6（2026-10-14）：新增 "南京"/"道"/"杂职"/"虚拟锚点" —— 卷04 实测需要：
#   南京 = 南京官署（条1–26，品级"同北京"，RANK 关联北京节点）；
#   道   = 布政司参政参议/按察司副使佥事分司诸道（条37–42）；
#   杂职 = 巡检司/驿/税课司/仓/织染局/河泊所/批验所/递运所/铁冶所/医学/阴阳学/僧纲司（条64–75）；
#   虚拟锚点 = 条27「南京官」沿革专条的 TME 承载节点（配 is_virtual:True，非实体机构）。
ORG_LEVELS = {"中枢", "部", "院", "寺", "监", "司", "局", "库", "卫", "所",
              "府", "州县", "布政按察", "都司卫所", "王府", "土司", "内府",
              "差遣", "南京", "道", "杂职", "虚拟锚点", "其他"}

# v7（2026-10-14）：org_type 独立为「权力系统」维度，与 level（机构形态）正交。
#   根因：v6 之前 org_type 直接复制 level 值（level=府 ot=府），未承载任何分类信息，
#   导致「中央/地方/军事/内廷」无法查询。v7 起二者语义分离：
#     level    = 机构形态（部/院/寺/监/司/府/州县/…），供层级校验 LEVEL_RANK 使用；
#     org_type = 权力系统归属（中央/地方/军事/内廷/南京/差遣/藩府），供分组查询。
#   用户 2026-10-14 拍板：加「藩府」类（王府长史司/王府护卫/衍圣公府——不受布政司辖、
#   不在京师编制，明制中自成体系，混入「地方」会污染地方行政查询）；
#   僧录司/道录司/教坊司归「中央」（虽附礼部条下，用户裁定按原文结构归属）。
ORG_TYPES = {"中央", "地方", "军事", "内廷", "南京", "差遣", "藩府", "未明"}

# v1.4（v9）：新增 "俸禄" —— 原文第 25 行洪武二十五年岁禄表（品级→石数），
#   原 RANK_TYPES 无承载值，此前整张表未入库导致 salary_ref 全空。
RANK_TYPES = {"品级员额", "散阶", "勋级", "爵位", "符牌印信", "俸禄", "其他"}

LINE_TYPES = {"直属", "分隶", "兼领", "带管", "统辖", "听于", "其他"}

EVO_TYPES = {"初置", "改置", "升秩", "降秩", "革罢", "复设", "改称",
             "裁并", "增置", "移驻", "未明"}

# ============ L4-RANK 员额：v3 置信度机制（基准库 §1.23）============
COUNT_FORMS = {"P1": 0.95, "P2": 0.90, "P3": 0.60, "P4": 1.00, "未明": 0.30}
COUNT_FORM_VERIFY = {"P1": False, "P2": False, "P3": True, "P4": False, "未明": True}
VERIFY_THRESHOLD = 0.8

# ============ L4-RANK 编制字段族（v3，用户确认全 12 项）============
POST_FIELDS = [
    "office", "office_parts", "count", "grade", "grade_order", "note",
    "count_form", "count_confidence", "verify_needed", "verify_reason",
    "count_evidence",
    # v3 扩展 12 项
    "vacancy_type", "is_concurrent", "post_status", "grade_note",
    "selection_route", "succession", "era_validity",
    "original_span", "rank_grade_raw", "salary_ref",
]
VACANCY_TYPES = {"实授", "署职", "试职", "纳职", "未明"}
POST_STATUS = {"现存", "已革", "后设", "未明"}
SELECTION_ROUTES = {"世官", "流官", "廷推", "推升", "传升", "乞升", "举荐", "未明"}

# ============ APPT 职官任职（基准库 §1.10）============
APPT_STATUS = {"现任", "致仕", "升迁", "贬谪", "罢黜", "兼领", "暂代",
               "追赠", "起复", "世袭", "举荐", "未明"}

# ============ TME 时间沿革（本书归纳）============
TME_CATEGORIES = {"初置", "改置", "升秩降秩", "废置", "复设", "改称",
                  "裁并", "增员", "移驻", "职掌变更", "未明"}

# ============ 排序键（基准库 §1.20 / §1.21）============
GRADE_ORDER = {
    "正一品": 1, "从一品": 2, "正二品": 3, "从二品": 4,
    "正三品": 5, "从三品": 6, "正四品": 7, "从四品": 8,
    "正五品": 9, "从五品": 10, "正六品": 11, "从六品": 12,
    "正七品": 13, "从七品": 14, "正八品": 15, "从八品": 16,
    "正九品": 17, "从九品": 18, "未入流": 19,
    # v6：南京官品级随北京。grade 记 "同北京"，grade_order 取**北京实际品级值**
    #     （由打包器从 link_to_bj.grade_ref 派生，非本表值）；本项仅作兜底。
    "同北京": 19,
    "未明": 99,
}

REIGN_ORDER = {
    "吴": 0, "洪武": 1, "建文": 2, "永乐": 3, "洪熙": 4, "宣德": 5,
    "正统": 6, "景泰": 7, "天顺": 8, "成化": 9, "弘治": 10, "正德": 11,
    "嘉靖": 12, "隆庆": 13, "万历": 14, "泰昌": 15, "天启": 16, "崇祯": 17,
    "未明": 99,
}

# ============ 品级→俸禄（v9，卷05 后补）============
# 依据：原文第 25 行「（洪武二十五年，重定内外文武官岁给禄俸之制。…俱米钞本折兼支。）」
# 18 级品级 × 18 个石数，一级不缺。salary_ref 原字段（v3 建）此前 427/427 全"未明"，
# 系字段建而未回填；本表建立后可按下式派生：salary_ref = "洪武二十五年制：<N>石"。
SALARY_TABLE = {
    "正一品": 1044, "从一品": 888,
    "正二品": 732, "从二品": 576,
    "正三品": 420, "从三品": 312,
    "正四品": 288, "从四品": 252,
    "正五品": 192, "从五品": 168,
    "正六品": 120, "从六品": 96,
    "正七品": 90, "从七品": 84,
    "正八品": 78, "从八品": 72,
    "正九品": 66, "从九品": 60,
    "未入流": 36,
}
SALARY_ERA = "洪武二十五年"
SALARY_UNIT = "石"


def salary_of(grade):
    """由品级取岁禄石数；表外品级返回 None。"""
    return SALARY_TABLE.get(grade)


def salary_ref_of(grade):
    """派生 salary_ref 文本；表外品级返回"未明"。"""
    shi = SALARY_TABLE.get(grade)
    if shi is None:
        return "未明"
    return "%s制：%d%s" % (SALARY_ERA, shi, SALARY_UNIT)


# ============ ID 前缀（命名空间唯一归属）============
ID_PREFIX = {
    "ent": "ENT-",
    "rule": "ZG-R-",
    "proc": "ZG-P-",
    "org": "ORG-",
    "rank": "RANK-",
    "line": "LINE-",
    "evo": "EVO-",
    "appt": "ZG-APPT-",
    "tme": "ZG-TME-",
    # v7（2026-10-14）：移除 "tpl"/"TPL-" —— 用户裁定取消机构模板容器，
    #   卷04 条37-75 的 39 条机构全部回归 ORGS 正式节点（占用 ORG- 卷段位）。
}
SEG_CAPACITY = 500   # 段容量 = 卷条数 × 单层最大扩展系数


def grade_order(g):
    """品级 → 排序整数（未识别的返回 99）"""
    return GRADE_ORDER.get(g, 99)


def reign_order(r):
    """年号 → 绝对序（未识别的返回 99）"""
    return REIGN_ORDER.get(r, 99)


def time_key(reign, year):
    """时间链排序键 = (REIGN_ORDER[reign], year)"""
    y = year if isinstance(year, int) else 99
    return (reign_order(reign), y)


def count_confidence(form):
    return COUNT_FORMS.get(form, 0.30)


def need_verify(form, conf):
    return bool(COUNT_FORM_VERIFY.get(form, True)) or conf < VERIFY_THRESHOLD
