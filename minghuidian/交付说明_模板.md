# 《明会典》知识库 · 交付包

> 交付日期：2026-10-14 ｜ 版本：P4「打通与交付」完成版
> 源书：《大明会典》（正德本）180 卷 / 854,118 字 / 13,364 条

---

## 先读这个

本包是《明会典》数字化知识工程的**完整可交付成果**。三条使用路径，按你的目的选：

| 我想… | 打开 |
|---|---|
| **查一条制度/官职/地名** | `04_接口/minghuidian_kb.py`（推荐）或 `02_数据/_kg_join_flat.csv` |
| **看结构与演变** | `03_可视化/vis_org_tree.html`、`vis_timeline.html`、`vis_geo_tree.html`（双击即开） |
| **了解这套东西怎么做的** | `01_报告/使用报告_20261014.md`（怎么用），`01_报告/项目总结报告.md`（为什么这么做） |

---

## 目录结构

```
_deliver/
├── 00_README.md              本文件
├── 01_报告/                   8 份报告
│   ├── 使用报告_20261014.md        ★ 完整使用说明（查询/溯源/重跑/扩展）
│   ├── 项目总结报告.md             ★ 全流程回顾（10 阶段 + 反思 + 方法论）
│   ├── 产出评估与补全路线图_20261014.md   P0–P4 路线图
│   ├── P0完成报告_20261014.md      地基：补 9 缺卷 / 清假填充 / 类型归一
│   ├── P1完成报告_20261014.md      核心层：rules 五要素 / TIM 16 主题 / history
│   ├── P2完成报告_20261014.md      结构层：RANK/NJC/XREF/GEO
│   ├── P25_P3_P1完成报告_20261014.md  驿站并层 + P3 数字文册器物
│   ├── 字段密度与QA诊断报告_20261014.md 树密度诊断与修复
│   └── 交付报告_20261013.md
├── 02_数据/
│   ├── _item_registry.json    13,364 条指纹库（全部层的原文锚点）
│   ├── _kg_join.json          13,364 行 × 23 桶跨层索引
│   ├── _kg_join_flat.csv      1.6 MB 平铺表（utf-8-sig，Excel 直开）
│   └── _layers/               34 个层文件（JSON，indent=1）
├── 03_可视化/
│   ├── vis_org_tree.html      官制树（衙门 329 + 官职 566）
│   ├── vis_timeline.html      制度演变图（16 主题 × 11 朝）
│   └── vis_geo_tree.html      地理管辖图（3,883 节点）
├── 04_接口/
│   └── minghuidian_kb.py      统一查询接口（15 方法 + CLI）
├── 05_脚本/
│   ├── _p4a_build_trees.py    三棵树构建
│   ├── _p4b_build_join.py     跨层索引
│   ├── _p4c_build_rankseq.py  品级序列层
│   ├── _p4f_render_vis.py     可视化渲染
│   └── _qa_final.py           十问自检
└── 06_校验/
    ├── _p4_orphans.json       曾孤立条审计（921，现已全挂载）
    └── _trees.json            三树汇总指标
```

---

## 三分钟上手

### 1. 查询（最快）

```powershell
cd 04_接口
python -X utf8 minghuidian_kb.py profile 苏州府
python -X utf8 minghuidian_kb.py office 吏部尚书
python -X utf8 minghuidian_kb.py ask "漕运怎么运到北京"
python -X utf8 minghuidian_kb.py stats
python -X utf8 minghuidian_kb.py check
```

> **Windows 提示**：控制台若乱码，务必加 `-X utf8`（脚本内已做 UTF-8 重定向，一般无需 `chcp`）。

### 2. 当 Python 库用

```python
import sys; sys.path.insert(0, r"…\04_接口")
from minghuidian_kb import MingHuidianKB
kb = MingHuidianKB()          # 自动定位同包内的 02_数据/_layers

kb.office("吏部尚书")   # 品级/职掌/沿革/下属/出处
kb.org("户部")          # 编制/沿革/属官/下辖
kb.geo("苏州府")        # 层级/隶属/卫所/驿站/仓场/辖县
kb.rule("漕运")         # 历代事例 + 年代链
kb.profile("苏州府")    # 全景档案（一网打尽）
kb.children("户部")     # 父子树展开
kb.path("苏州府")       # 从根到叶路径
kb.check()              # 自检
```

接口会**自动发现**数据目录（依次尝试 `./_layers`、`./02_数据/_layers`、上级目录），项目根与交付包两种布局都直接可用。也可显式指定：`MingHuidianKB(r"…\02_数据\_layers")`。

### 3. 看可视化

双击 `03_可视化/` 下任意 `.html`。**单文件、无 CDN、无网络依赖**，可直接邮件转发或拷 U 盘。树节点可折叠、支持搜索框过滤。

---

## 数据规模（全部经校验）

| 层 | 量 | 层 | 量 |
|---|---|---|---|
| 底座条目 | **13,364** | 地理节点 | **3,883** |
| 归属实体 | 3,681 | 衙门档案 | 329 |
| 人名 / 人物档案 | 7,467 / 157 | 官职档案 / 官名词表 | 566 / 1,512 |
| 规则事例 | 3,594 | 品级章服 / 品级序列 | 24 / 19 级·287 段 |
| 制度主题 | 16（152 标签） | 数字文册 | 2,813 |
| 器物 | 758（66 类） | 报告奏议 / 引书 | 942 / 99 |
| 律例／礼仪／冠服／考核 | 326 / 410 / 388 / 394 | 两京对照 / 互见 | 47 / 198 |
| **跨层索引** | 13,364 条 × 23 桶，多层贯通 **9,106（68%）**，**孤立 0** | | |

---

## 可信度与边界（如实报告）

**可信度高**：底座条目、地理树（0 悬空，children 与 parent_id 完全一致）、衙门树（100% 可达）、跨层索引（0 孤立）、品级/章服。

**已知边界**：
1. **制度纪年不全** — 原书大量条目不标年号，timeline 只统计可判定者。
2. **官职档案 566 只收有独立档案的官**（主要京官）；土司/盐运/杂职官靠 `02_数据/_layers/offices.json`（1,512 词表）覆盖，未升格为完整档案。
3. **50 例跨省同名卫所弃权不猜**（见 `02_数据/_layers/geo_station_dropped.json`），需专家核后手工指定。
4. **官职沿革部分为空** — 原文未载，未从外部史源补入。
5. **器物层未展开工艺参数** — 仅 758 条 / 66 类。

详见 `01_报告/使用报告_20261014.md` §7「人工校验闭环」。

---

## 溯源原则

**每一条记录都可回溯到刻本原文。** 任何记录都带 `item_id`（形如 `077-001`）：
在 `02_数据/_item_registry.json` 取 `original` = 刻本原文。

> 本交付包**不含** `_extract/`（按卷切分的抽取文本，约 3 MB）。需要按卷通读原文时，请在完整项目目录 `E:\git\ToolBox\guji\minghuidian\` 下操作。

---

## 重跑与扩展

```powershell
cd <项目根>
python -X utf8 _p4a_build_trees.py    # 三棵树
python -X utf8 _p4b_build_join.py     # 跨层索引
python -X utf8 _p4c_build_rankseq.py  # 品级序列
python -X utf8 _p4f_render_vis.py     # 可视化（输出到 _vis/）
python -X utf8 _p4i_package.py        # 重新打包 _deliver/
python -X utf8 _qa_final.py           # 十问自检（应 10/10 通过）
```

改了 `_layers/*.json` 后按上述顺序重跑即可。扩展指南见 `01_报告/使用报告_20261014.md` §4.5。
