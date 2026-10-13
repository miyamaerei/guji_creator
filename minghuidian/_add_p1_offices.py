# -*- coding: utf-8 -*-
"""补全：女官系统 + 武散官 + 勋官"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
offices = json.load(open(os.path.join(ROOT, "_layers", "office_profiles.json"), encoding="utf-8"))

# ============================================================
# 一、女官系统（六局二十四司）
# ============================================================
# 来源：《明史·职官志》女官
# 六局：尚宫局、尚仪局、尚服局、尚食局、尚寝局、尚功局
# 每局有：尚宫/尚仪等（正五品）→ 司记/司言等（正六品）→ 典/掌（七品/八品）

def add(name, rank, type_="实职", system="女官", headcount=1, duties="", parent="", location="内府"):
    offices.append({
        "office_name": name,
        "rank": rank,
        "type": type_,
        "system": system,
        "headcount": headcount,
        "duties": duties,
        "parent_org": parent,
        "child_offices": [],
        "location": location,
        "history": [],
        "note": "",
    })

# 尚宫局（掌导引中宫）
add("尚宫", "正五品", duties="掌导引中宫，总司记司言司簿司闱", parent="皇后")
add("尚宫局司记", "正六品", duties="掌宫内文书录目记审", parent="尚宫")
add("尚宫局司言", "正六品", duties="掌宣传启奏", parent="尚宫")
add("尚宫局司簿", "正六品", duties="掌宫人名廪赐记录", parent="尚宫")
add("尚宫局司闱", "正六品", duties="掌宫闱管钥", parent="尚宫")

# 尚仪局（掌礼仪起居）
add("尚仪", "正五品", duties="掌礼仪起居，总司籍司乐司宾司赞", parent="皇后")
add("尚仪局司籍", "正六品", duties="掌经籍教学纸笔几案", parent="尚仪")
add("尚仪局司乐", "正六品", duties="掌音乐音律", parent="尚仪")
add("尚仪局司宾", "正六品", duties="掌宾客朝见接待", parent="尚仪")
add("尚仪局司赞", "正六品", duties="掌赞相礼仪", parent="尚仪")

# 尚服局（掌服章宝藏）
add("尚服", "正五品", duties="掌服章宝藏，总司宝司衣司饰司仗", parent="皇后")
add("尚服局司宝", "正六品", duties="掌宝玺符契", parent="尚服")
add("尚服局司衣", "正六品", duties="掌衣服服用", parent="尚服")
add("尚服局司饰", "正六品", duties="掌巾栉膏沐", parent="尚服")
add("尚服局司仗", "正六品", duties="掌仗卫器械", parent="尚服")

# 尚食局（掌膳馐品齐）
add("尚食", "正五品", duties="掌膳馐品齐，总司膳司酝司药司饎", parent="皇后")
add("尚食局司膳", "正六品", duties="掌食膳烹调", parent="尚食")
add("尚食局司酝", "正六品", duties="掌酒醴酏饮", parent="尚食")
add("尚食局司药", "正六品", duties="掌医药方饵", parent="尚食")
add("尚食局司饎", "正六品", duties="掌廪饩柴炭", parent="尚食")

# 尚寝局（掌帏帐床寝）
add("尚寝", "正五品", duties="掌帏帐床寝，总司设司舆司苑司灯", parent="皇后")
add("尚寝局司设", "正六品", duties="掌床帷茵席洒扫张设", parent="尚寝")
add("尚寝局司舆", "正六品", duties="掌舆辇伞扇", parent="尚寝")
add("尚寝局司苑", "正六品", duties="掌苑园种植蔬果", parent="尚寝")
add("尚寝局司灯", "正六品", duties="掌灯烛膏火", parent="尚寝")

# 尚功局（女工功课）
add("尚功", "正五品", duties="掌女工功课，总司制司彩司计司正", parent="皇后")
add("尚功局司制", "正六品", duties="掌衣服裁制缝纫", parent="尚功")
add("尚功局司彩", "正六品", duties="掌彩锦缯丝", parent="尚功")
add("尚功局司计", "正六品", duties="掌衣服饮食柴炭物料", parent="尚功")
add("宫正", "正五品", duties="掌戒令谪罚纠察", parent="皇后", location="内府")

print(f"女官系统: 新增{len([o for o in offices if o['system']=='女官'])}个")

# ============================================================
# 二、武散官（30阶）
# ============================================================
# 来源：《明史·职官志》武散官
wu_san_guan = [
    ("特进光禄大夫", "正一品", "升授"),
    ("特进荣禄大夫", "正一品", "初授"),
    ("光禄大夫", "从一品", "升授"),
    ("荣禄大夫", "从一品", "初授"),
    ("骠骑将军", "正二品", "升授"),
    ("镇国将军", "正二品", "初授"),
    ("护军将军", "从二品", "升授"),
    ("护国将军", "从二品", "初授"),
    ("昭勇将军", "正三品", "升授"),
    ("昭毅将军", "正三品", "初授"),
    ("昭武将军", "从三品", "升授"),
    ("怀远将军", "从三品", "初授"),
    ("定远将军", "从四品", "升授"),
    ("明威将军", "从四品", "初授"),
    ("宣武将军", "正四品", "升授"),
    ("武德将军", "正四品", "初授"),
    ("武略将军", "从四品", "升授"),
    ("武毅将军", "从四品", "初授"),
    ("骑将军", "正五品", "升授"),
    ("步将军", "正五品", "初授"),
    ("武骑将军", "从五品", "升授"),
    ("骁骑将军", "从五品", "初授"),
    ("飞骑尉", "正六品", "升授"),
    ("云骑尉", "正六品", "初授"),
    ("武骑尉", "从六品", "升授"),
    ("忠显校尉", "从六品", "初授"),
    ("忠武校尉", "正七品", "升授"),
    ("忠显校尉", "正七品", "初授"),
    ("忠翊校尉", "从七品", "升授"),
    ("修武校尉", "从七品", "初授"),
]

existing = {o["office_name"] for o in offices}
for name, rank, stage in wu_san_guan:
    if name not in existing:
        offices.append({
            "office_name": name,
            "rank": rank,
            "type": "散官",
            "system": "武职",
            "headcount": 0,
            "duties": f"武散官（{stage}）",
            "parent_org": "",
            "child_offices": [],
            "location": "中央",
            "history": [],
            "note": "武职散官，品级称号，按实职支俸",
            "salary": None,
            "salary_note": "散官是品级称号，按实际职务支俸",
        })

print(f"武散官: 新增{len(wu_san_guan)}个")

# ============================================================
# 三、勋官（12阶）
# ============================================================
# 来源：《明史·职官志》文勋五阶、武勋六阶、合计12阶
xun_guan = [
    # 文勋
    ("左柱国", "正一品", "文勋"),
    ("右柱国", "从一品", "文勋"),
    ("柱国", "正二品", "文勋"),
    ("护军", "从二品", "文勋"),
    ("轻车都尉", "正三品", "文勋"),
    # 武勋
    ("上柱国", "正一品", "武勋"),
    ("柱国", "从一品", "武勋"),
    ("上护军", "正二品", "武勋"),
    ("护军", "从二品", "武勋"),
    ("上轻车都尉", "正三品", "武勋"),
    ("轻车都尉", "从三品", "武勋"),
    ("骁骑尉", "正四品", "武勋"),
]

existing = {o["office_name"] for o in offices}
for name, rank, xun_type in xun_guan:
    if name not in existing:
        offices.append({
            "office_name": name,
            "rank": rank,
            "type": "勋官",
            "system": "文职" if "文" in xun_type else "武职",
            "headcount": 0,
            "duties": f"{xun_type}称号",
            "parent_org": "",
            "child_offices": [],
            "location": "中央",
            "history": [],
            "note": f"{xun_type}，功勋称号，非实职",
            "salary": None,
            "salary_note": "勋官，功勋称号，按实职支俸",
        })

print(f"勋官: 新增{len(xun_guan)}个")

# ============================================================
# 保存
# ============================================================
with open(os.path.join(ROOT, "_layers", "office_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(offices, f, ensure_ascii=False, indent=2)

print(f"\n===== 补全完成 =====")
print(f"总官职数: {len(offices)}")

# 统计
type_count = {}
for o in offices:
    t = o.get("type", "未知")
    type_count[t] = type_count.get(t, 0) + 1
print(f"\n类型分布:")
for t, cnt in sorted(type_count.items(), key=lambda x: -x[1]):
    print(f"  {t}: {cnt}个")

sys_count = {}
for o in offices:
    s = o.get("system", "未知")
    sys_count[s] = sys_count.get(s, 0) + 1
print(f"\n系统分布:")
for s, cnt in sorted(sys_count.items(), key=lambda x: -x[1]):
    print(f"  {s}: {cnt}个")
