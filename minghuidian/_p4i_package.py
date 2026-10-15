# -*- coding: utf-8 -*-
"""P4-I：生成交付包 _deliver/。

交付包结构
----------
_deliver/
├── 00_README.md              交付说明（先读这个）
├── 01_报告/
│   ├── 使用报告_20261014.md
│   ├── 项目总结报告.md
│   └── 阶段报告（P0/P1/P2/P25_P3/字段密度/路线图）
├── 02_数据/                  30 层 JSON + 底座指纹库 + 跨层索引
│   ├── _item_registry.json
│   ├── _kg_join.json
│   ├── _kg_join_flat.csv
│   └── _layers/*.json
├── 03_可视化/                vis_*.html
├── 04_接口/                  minghuidian_kb.py + 示例
├── 05_脚本/                  _p4a/_p4b/_p4c/_p4f + _qa_final
└── 06_校验/                  _p4_orphans.json + _trees.json + 十问自答输出

只复制必需文件，跳过 .bak / clean / 中间态。
"""
import io, sys, os, json, shutil, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
D = "_deliver"
# 可视化源目录（P4-F 产出）与交付目录分开，避免自删
VIS_SRC = "_vis"
if os.path.exists(D):
    shutil.rmtree(D)
for sub in ("01_报告", "02_数据/_layers", "03_可视化", "04_接口", "05_脚本", "06_校验"):
    os.makedirs(os.path.join(D, sub), exist_ok=True)

log = []


def cp(src, dst, must=True):
    if not os.path.exists(src):
        if must:
            log.append(f"  [缺] {src}")
        return False
    shutil.copy2(src, dst)
    log.append(f"  {src} → {dst}  ({os.path.getsize(dst)/1024:.0f} KB)")
    return True


# ---- 01 报告 ----
reports = ["使用报告_20261014.md", "项目总结报告.md",
           "P0完成报告_20261014.md", "P1完成报告_20261014.md",
           "P2完成报告_20261014.md", "P25_P3_P1完成报告_20261014.md",
           "字段密度与QA诊断报告_20261014.md", "产出评估与补全路线图_20261014.md",
           "交付报告_20261013.md"]
for r in reports:
    cp(r, os.path.join(D, "01_报告", r), must=False)

# ---- 02 数据 ----
for f in ["_item_registry.json", "_kg_join.json", "_kg_join_flat.csv"]:
    cp(f, os.path.join(D, "02_数据", f))

SKIP = (".bak", "_clean", "_manual")
layer_keep = []
for p in sorted(glob.glob("_layers/*.json")):
    b = os.path.basename(p)
    if any(s in b for s in SKIP):
        continue
    layer_keep.append(b)
    cp(p, os.path.join(D, "02_数据/_layers", b))
# 树的 md 版
for p in glob.glob("_layers/*.md"):
    cp(p, os.path.join(D, "02_数据/_layers", os.path.basename(p)), must=False)

# ---- 03 可视化 ----
for p in sorted(glob.glob(os.path.join(VIS_SRC, "*.html"))):
    cp(p, os.path.join(D, "03_可视化", os.path.basename(p)), must=False)

# ---- 04 接口 ----
cp("minghuidian_kb.py", os.path.join(D, "04_接口", "minghuidian_kb.py"))

# ---- 05 脚本 ----
for s in ["_p4a_build_trees.py", "_p4b_build_join.py", "_p4c_build_rankseq.py",
          "_p4f_render_vis.py", "_qa_final.py"]:
    cp(s, os.path.join(D, "05_脚本", s), must=False)

# ---- 00 交付说明 ----
SRC_README = "交付说明_模板.md"
if os.path.exists(SRC_README):
    shutil.copy2(SRC_README, os.path.join(D, "00_README.md"))
    log.append(f"  {SRC_README} → {D}/00_README.md")
else:
    log.append(f"  [缺] {SRC_README}（00_README.md 未生成）")

# ---- 06 校验 ----
for s in ["_p4_orphans.json", "_trees.json"]:
    cp(s, os.path.join(D, "06_校验", s), must=False)

print("\n".join(log))
print(f"\n层文件复制 {len(layer_keep)} 个")
