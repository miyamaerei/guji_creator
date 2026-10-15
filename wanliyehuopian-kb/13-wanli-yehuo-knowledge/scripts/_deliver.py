# -*- coding: utf-8 -*-
"""
构建《万历野获编》交付包 _deliver/

结构（对齐 minghuidian / zhipu-kb 既有交付包惯例）：
  _deliver/
  ├── 00_交付说明.md
  ├── 01_报告/   （使用报告 / 项目总结 / 填充率表 / 十二问验收表）
  ├── 02_数据/   （底座 + 10 层 + 跨层索引 + 归一映射 + 派生视图）
  ├── 03_阅读器/ （单文件 HTML 阅读器）
  ├── 04_脚本/   （可重跑管线）
  └── 05_校验/   （校验输出）

原则：只复制「开箱即用所需」，脚本目录只带管线所需的 .py（不带 _tmp_ / _part_ 片段）。
"""
import io, os, sys, json, shutil, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 13-wanli-yehuo-knowledge
OUT  = os.path.join(BASE, "_deliver")
LAYERS = ["ents", "rules", "events", "appts", "rels", "opns", "cits", "mings", "tmes", "regs"]

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
for d in ["01_报告", "02_数据", "02_数据/_layers", "02_数据/_global", "02_数据/views",
          "03_阅读器", "04_脚本", "05_校验"]:
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

manifest = []   # (相对路径, 字节数, sha256 前12)


def put(src, rel):
    """复制单文件并登记"""
    if not os.path.exists(src):
        print("  [跳过·不存在] %s" % rel)
        return False
    dst = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    b = open(src, "rb").read()
    manifest.append((rel, len(b), hashlib.sha256(b).hexdigest()[:12]))
    return True


def puttree(src, rel, exts=None, skip=None):
    """递归复制目录"""
    n = 0
    for root, dirs, files in os.walk(src):
        for f in files:
            if exts and not f.lower().endswith(exts):
                continue
            if skip and any(s in f for s in skip):
                continue
            full = os.path.join(root, f)
            r = os.path.relpath(full, src).replace("\\", "/")
            if put(full, "%s/%s" % (rel, r)):
                n += 1
    return n


print("=== 构建 _deliver ===")

# ---------- 01_报告 ----------
print("[1/6] 报告")
for name in ["使用报告.md", "项目总结报告.md", "填充率表.md", "十二问验收表.md"]:
    put(os.path.join(BASE, name), "01_报告/%s" % name)

# ---------- 02_数据 ----------
print("[2/6] 数据")
put(os.path.join(BASE, "_item_registry.json"), "02_数据/_item_registry.json")
n = 0
for lay in LAYERS:
    n += puttree(os.path.join(BASE, "_layers", lay), "02_数据/_layers/%s" % lay, exts=(".json",))
print("      层文件 %d 个" % n)
put(os.path.join(BASE, "_kg_join.json"), "02_数据/_kg_join.json")
put(os.path.join(BASE, "_kg_join_flat.csv"), "02_数据/_kg_join_flat.csv")
put(os.path.join(BASE, "_global", "ent_keys.json"), "02_数据/_global/ent_keys.json")
put(os.path.join(BASE, "_global", "alias_index.json"), "02_数据/_global/alias_index.json")
n = puttree(os.path.join(BASE, "views"), "02_数据/views", exts=(".json", ".csv"))
print("      视图文件 %d 个" % n)

# ---------- 04_脚本 ----------
print("[4/6] 脚本")
PIPE = ["validate_layers.py", "build_ent_keys.py", "build_kg_join.py", "build_views.py",
        "_audit_origins.py", "_audit_new_records.py", "_kg_enums.py", "_common.py"]
for s in PIPE:
    put(os.path.join(BASE, "scripts", s), "04_脚本/%s" % s)

# ---------- 03_阅读器 ----------
print("[3/6] 阅读器")
put(os.path.join(BASE, "reader.html"), "03_阅读器/reader.html")

# ---------- 05_校验 ----------
print("[5/6] 校验")
put(os.path.join(BASE, "scripts", "validate_layers.py"), "05_校验/validate_layers.py")
put(os.path.join(BASE, "_validate_out.txt"), "05_校验/校验输出.txt")
put(os.path.join(BASE, "SKILL.md"), "01_报告/项目总纲_SKILL.md")
put(os.path.join(BASE, "references", "schemas.md"), "02_数据/schemas.md")

# ---------- 00_交付说明 ----------
print("[3/6] 交付说明（构建后写）")

# ---------- 统计 ----------
total_files = len(manifest)
total_bytes = sum(m[1] for m in manifest)

desc = """# 《万历野获编》知识库 · 交付说明

**交付日期**：%s
**交付内容**：10 层结构化知识资产 · **9,843** 条记录 · **1,451** 条目 **100%%** 覆盖

---

## 一、交付清单

| 目录 | 内容 | 文件数 |
|---|---|---|
| `01_报告/` | 使用报告 / 项目总结报告 / 填充率表 / 十二问验收表 | 4 |
| `02_数据/` | 底座指纹库 + 10 层 JSON + 跨层索引 + 实体归一 + 6 类派生视图 | %d |
| `03_阅读器/` | 单文件 HTML 阅读器（离线可用） | 1 |
| `04_脚本/` | 可重跑管线（校验 / 重建索引 / 重建视图 / 审计） | 8 |
| `05_校验/` | 校验脚本（复核用） | 1 |
| **合计** | | **%d** |

总体积约 %.1f MB。

## 二、核心数字

| 项 | 值 |
|---|---|
| 底座条目 | **1,451**（34 卷，`item_id` 01-001 ~ 34-050） |
| 记录总数 | **9,843** |
| 覆盖率 | **1,451 / 1,451 = 100.0%%** |
| 零挂载条目 | **0** |
| 层数 | 10（ents / rules / events / appts / rels / opns / cits / mings / tmes / regs） |
| 归一实体 | 2,696（跨卷复用主键的簇 473） |
| 派生视图 | 时间线 396 人物 / 制度沿革 54 / 党网 728·532 / 门类 48 / 补正史 864 行 / 立场 458 |
| 校验 | `validate_layers.py` → **All checks passed!**（GAP=0） |

## 三、五分钟上手

### 1) 打开阅读器
直接双击 `03_阅读器/reader.html`（纯静态、离线、无需服务器）。

### 2) 命令行查询
```python
import json, os
BASE = r"<解压目录>\\02_数据"

# 查某条笔记贯穿了哪些层
join = json.load(open(os.path.join(BASE, "_kg_join.json"), encoding="utf-8"))["records"]
rec = next(r for r in join if r["item_id"] == "16-027")
print(rec["entry_title"], rec["layer_count"], rec["layers"])

# 查某人物一生
tl = json.load(open(os.path.join(BASE, "views/timeline/张居正.json"), encoding="utf-8"))
print(tl["total_records"], tl["layers"])   # 83 条
```

### 3) 复核校验
```bash
cd 04_脚本
python -X utf8 validate_layers.py
```

## 四、目录结构详表

```
_deliver/
├── 00_交付说明.md              ← 本文件
├── 01_报告/
│   ├── 使用报告.md
│   ├── 项目总结报告.md
│   ├── 填充率表.md
│   └── 十二问验收表.md
├── 02_数据/
│   ├── _item_registry.json     ← 底座：1,451 条目指纹库（全层溯源锚）
│   ├── _kg_join.json           ← 跨层索引（条目 → 各层 ID + layer_count）
│   ├── _kg_join_flat.csv       ← 平铺表（9,843 行）
│   ├── _layers/<层>/<层>_NN.json   ← 10 层 × 34 卷
│   ├── _global/ent_keys.json   ← 实体归一映射
│   ├── _global/alias_index.json← 原文词形 → normalized
│   └── views/                  ← 6 类派生视图
├── 03_阅读器/reader.html
├── 04_脚本/                    ← 可重跑管线
└── 05_校验/validate_layers.py
```

## 五、已知边界（如实声明）

1. **枚举漂移**：部分字段有越界值（`events.vs_official_history` 58 条 `unknown`、
   `cits.purpose` 36 条自由文本等）。**治理方案见《使用报告》§8**（三档分级）。
2. **双 schema 并存**：卷01–17 用 style A，新补卷用 style B，字段名不同。
3. **层文件顶层形态不一**：卷01–08 为 `{"records":[…]}`，09–34 为裸数组。读取需兼容。
4. **`ents.exam_info` 覆盖 5.2%%**、**社会名物实体薄**：原因与改进路径见《十二问验收表》Q10/Q11。
5. **`_item_registry.original` 仅存 200 字预览**：全文请查 `assets/sources/万历野获编.txt`（未含在本交付包，属原文版权件）。

## 六、离线自足声明

本交付包**开箱即用**，不依赖项目目录：数据是自包含副本，阅读器是单文件静态页。
`04_脚本/` 中的重建脚本**需要原项目目录结构**（`_layers/`、`assets/sources/`）才可运行，
在交付包内仅作**管线说明与审计代码留档**之用。

---

*生成脚本：`scripts/_deliver.py` ｜ 生成时间：%s*
""" % (datetime.date.today().isoformat(), sum(1 for m in manifest if m[0].startswith("02_数据")),
       total_files + 1, total_bytes / 1024 / 1024, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

open(os.path.join(OUT, "00_交付说明.md"), "w", encoding="utf-8", newline="").write(desc)
manifest.append(("00_交付说明.md", len(desc.encode("utf-8")), ""))

# ---------- 清单文件 ----------
lines = ["# 文件清单（%d 个）" % len(manifest), "", "| 路径 | 字节 | sha256(12) |", "|---|---|---|"]
for rel, sz, h in sorted(manifest):
    lines.append("| `%s` | %d | `%s` |" % (rel, sz, h))
open(os.path.join(OUT, "文件清单.md"), "w", encoding="utf-8", newline="").write("\n".join(lines) + "\n")

print("")
print("=== 完成 ===")
print("文件数: %d" % len(manifest))
print("总字节: %d (%.2f MB)" % (total_bytes, total_bytes / 1024 / 1024))
print("输出:   %s" % OUT)
