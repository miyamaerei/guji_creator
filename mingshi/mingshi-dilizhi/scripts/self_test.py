# -*- coding: utf-8 -*-
"""骨架功能自检：确认五项护栏真的会响（不是只会 import）。"""

import io, os, sys, json, tempfile, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as SK

ok, fail = [], []


def chk(name, cond):
    (ok if cond else fail).append(name)


# ========== B 族 1：命名一致性 ==========
# 注意：这里必须用**生产环境的真实形状**（list of 3-tuples）。
# 曾经此处写成 dict，让一个 `LAYER_SPECS.items()` 的错误实现"通过"了自检，
# 而实例里 LAYER_SPECS 是 list → 一接上就 AttributeError（坑 #63）。
SK.LAYER_SPECS = [
    ("ents", "ents", "records"),  # 正确
    ("rule", "rules", "records"),  # 目录名单数 -> 应报错
]
errs = SK.check_naming_consistency()
chk("B: 命名不一致被捕获", any("rule" in e for e in errs))

# 回归用例：生产形状（list）下必须不崩
SK.LAYER_SPECS = [("ents", "ents", "records"), ("rules", "rules", "records")]
try:
    SK.check_naming_consistency()
    chk("B: list 形状下命名检查不崩（#63 回归）", True)
except Exception:
    chk("B: list 形状下命名检查不崩（#63 回归）", False)

# ========== B 族 2：ID 唯一性（ENT 豁免） ==========
recs = [{"id": "RULE-001"}, {"id": "RULE-001"}, {"id": "ENT-001"}, {"id": "ENT-001"}]
dups = SK.assert_unique_ids(recs, exempt_prefixes=("ENT-",))
chk("B: 重复 ID 被捕获且 ENT- 豁免", dups == ["RULE-001"])

# ========== B 族 3：ID 取记录全局序号而非 slot ==========
recs2 = [
    {"slot": 1, "idf": "x"},
    {"slot": 1, "idf": "y"},
    {"slot": 2, "idf": "z"},
    {"slot": 2, "idf": "w"},
]
SK.assign_ids(recs2, prefix="ZG-R-", volume="01", id_field="idf")
ids = [r["idf"] for r in recs2]
chk("B: ID 按全局序号分配（slot 相同不撞号）", len(set(ids)) == 4)

# ========== B 族 4：子节点 ID 保留已有 ==========
node = {"id": "ORG-100", "children": [{"name": "a"}, {"id": "ORG-100#7", "name": "b"}]}
SK.assign_child_ids(node, node["id"])
chk("B: 子节点已有 ID 被保留", node["children"][1]["id"] == "ORG-100#7")
chk("B: 子节点缺 ID 被派生", node["children"][0]["id"].startswith("ORG-100#"))

# ========== A 族：填充率体检 + 零填充失败 ==========
cov = SK.FieldCoverage("structs")
cov.count_record({"grade": "正二品", "salary_ref": ""}, fields=["grade", "salary_ref"])
cov.count_record({"grade": "正三品"}, fields=["grade", "salary_ref"])
text, zero_fields = cov.report()
rates = cov.rates()
chk("A: 填充率表逐字段输出", set(rates.keys()) == {"grade", "salary_ref"})
chk("A: 零填充字段被标记", rates["salary_ref"][0] == 0 and "salary_ref" in zero_fields)

raised = False
try:
    SK.assert_no_silent_zero((text, zero_fields), "structs")
except AssertionError:
    raised = True
chk("A: 零填充触发 assert_no_silent_zero", raised)

# 已解释的零填充应放行
text2, zf2 = cov.report(zero_explanations={"salary_ref": "本书无俸禄记载"})
chk(
    "A: 已登记原因的零填充被放行（归零字段仍列出但报告写明原因）",
    "本书无俸禄记载" in text2,
)

# ========== G 族：增量合并（不截断共享文件） ==========
tmp = tempfile.mkdtemp()
try:
    p = os.path.join(tmp, "fp.json")
    SK.atomic_write_json(p, {"01-001": "甲"})
    SK.merge_shared_json(p, {"01-002": "乙"}, key_field=None)  # 增量，不得抹掉 01-001
    got = json.load(io.open(p, encoding="utf-8"))
    chk("G: 增量合并不截断共享文件", set(got.keys()) == {"01-001", "01-002"})

    SK.atomic_write_json(p, {"z": 1})
    chk("G: 原子写盘可用", json.load(io.open(p, encoding="utf-8")) == {"z": 1})

    # 按卷落盘：两卷互不覆盖
    SK.PATHS["layers"] = tmp
    SK.merge_layer("ents", "01", [{"id": "ENT-001"}])
    SK.merge_layer("ents", "02", [{"id": "ENT-002"}])
    allrecs = []
    for f in SK.layer_files("ents"):
        allrecs += json.load(io.open(f, encoding="utf-8"))["records"]
    chk("G: 按卷增量落盘不互相覆盖", len(allrecs) == 2)

    # 再跑一次 01，替换而非追加（幂等）
    SK.merge_layer("ents", "01", [{"id": "ENT-001b"}])
    allrecs2 = []
    for f in SK.layer_files("ents"):
        allrecs2 += json.load(io.open(f, encoding="utf-8"))["records"]
    chk("G: 同卷重跑幂等（替换不追加）", len(allrecs2) == 2)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ========== P 族 1：语域锚定匹配 ==========
g = SK.SemanticGate(["留守司"], head_chars=20)
scope = "卫指挥使司，设官如京卫。(品秩并同)外卫各统于都司、行都司或留守司。率世官，或有流官。"
chk("P: 范围词锚定开头，正文同形词不污染", g.match("05-051", scope) is False)
chk(
    "P: 锚定开头命中正例",
    g.match("05-046", "留守司。正留守一人，(正二品)副留守一人。") is True,
)

# ========== P 族 2：中文数字量纲 ==========
chk("P: 一千四十四=1044", SK.cn2int("一千四十四") == 1044)
chk("P: 三百=300", SK.cn2int("三百") == 300)
chk("P: 一百一十二=112", SK.cn2int("一百一十二") == 112)
chk("P: 洪武三年=3", SK.cn2int("洪武三年") == 3)

# ========== P 族 2b：约数后缀（#64 回归，样本取自《明史·食货志》真实总账串） ==========
# 史书/政书数额绝大多数带「馀 / 有奇」，不剥离则静默返回 None → 总账树全空。
chk("P: 十三万二千馀石=132000", SK.cn2int("十三万二千馀石") == 132000)
chk("P: 七十八万七千馀两=787000", SK.cn2int("七十八万七千馀两") == 787000)
chk("P: 四百三十馀万束=4300000", SK.cn2int("四百三十馀万束") == 4300000)
chk("P: 十三万五千馀两=135000", SK.cn2int("十三万五千馀两") == 135000)
chk("P: 十六万两有奇=160000", SK.cn2int("十六万两有奇") == 160000)
chk("P: 万两有奇=10000", SK.cn2int("万两有奇") == 10000)
chk(
    "P: 四百三十馀万束=4300000（约数夹在数字中间）",
    SK.cn2int("四百三十馀万束") == 4300000,
)
chk("P: 四百三十馀万束 不被截成 430", SK.cn2int("四百三十馀万束") != 430)
chk("P: 十万=100000（万前有数字不重复计 1）", SK.cn2int("十万") == 100000)
chk("P: 三十馀万=300000", SK.cn2int("三十馀万") == 300000)
chk("P: 纯约数无数字不报假数", SK.cn2int("馀石") is None)

# ========== P 族 3：枚举漂移告警 ==========
# drift_ratio = 库外值种数 / 库内值种数；阈值 > 1.5 判枚举未覆盖本书。
# 这里构造 3 个库内值 + 6 个库外值 → 6/3 = 2.0 > 1.5
allowed = {"初置", "改置", "废置"}
vals = ["初置"] * 10 + ["新造甲", "新造乙", "新造丙", "新造丁", "新造戊", "新造己"]
drift = SK.drift_ratio(vals, allowed)
chk("P: 漂移率被算出且越界可判(>1.5)", drift > 1.5)
sink = {}
bad = SK.check_enum(vals, allowed, "evo", "change_type", pending_sink=sink)
chk(
    "P: 枚举校验不中断且收集越界值",
    bad == sorted(["新造甲", "新造乙", "新造丙", "新造丁", "新造戊", "新造己"])
    and "evo.change_type" in sink,
)

# ========== P 族 4：探查终止 ==========
pt = SK.ProbeTracker(lambda d: d["nodes"])
pt.settle({"nodes": 158})
settled = pt.settle({"nodes": 158})
chk("P: 连续两次结论不变即判可收口", settled is True)
pt2 = SK.ProbeTracker(lambda d: d["n"])
pt2.settle({"n": 1})
chk("P: 结论变化不判收口", pt2.settle({"n": 2}) is False)

# ========== 交付前：查询问句验收表 ==========
qs = [
    {
        "q": "吏部编制几人几品",
        "layer": "RANK/posts",
        "answer": "尚书1正二品",
        "status": "能答",
    },
    {"q": "内阁首辅几品", "layer": "—", "answer": "原文无", "status": "答不了"},
]
tbl, stat = SK.query_acceptance(qs)
chk(
    "A: 问句验收表能产出且统计在表内",
    "目标查询问句验收表" in tbl and stat.get("能答") == 1 and stat.get("答不了") == 1,
)

print("PASS %d / FAIL %d" % (len(ok), len(fail)))
for f in fail:
    print("  FAIL:", f)
for o in ok:
    print("  ok  :", o)
sys.exit(1 if fail else 0)
