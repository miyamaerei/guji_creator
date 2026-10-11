---
name: book-先进遗风
description: 「先进遗风」书实例技能（由 book-skill-factory 问询生成）。按 structure.json 的四级结构规则（目录/卷/标题/段落）提取每卷、全本与目录正文；结构不合预期时改 structure.json 或重跑工厂问询，不修改本实例代码。
---

# 先进遗风 书实例

本实例由 book-skill-factory 的启发式问询生成，结构规则唯一真源是同目录 `structure.json`；
解析引擎复用工厂参考模板 `book-skill-factory/common`，本实例不包含任何写死的解析代码。

## 结构配置

`structure.json` 由六组启发式问题的答案翻译而来：

| 组 | 问题 | 对应字段 |
|----|------|---------|
| Q1 | 目录区起点/终点 | `toc_anchor` |
| Q2 | 正文起点 | `body_anchor` |
| Q3 | 是否分卷、卷标记形态 | `volume_pattern` |
| Q4 | 条目标题层级 | `heading_kind` / `heading_pattern` |
| Q5 | 页码是否保留 | `keep_pages` |
| Q6 | 噪声行与清洗开关 | `omit_lines` / `strip_artifacts` |

## 用法

```bash
python scripts/extract.py --mode volumes   # 每卷单独一个 txt
python scripts/extract.py --mode full      # 合并全本 txt（含目录 + 正文）
python scripts/extract.py --mode toc       # 输出目录 txt
python scripts/extract.py --out <目录>     # 指定输出目录（默认实例目录）
```

## 结构调整

结构识别不准时（卷数/标题数/段落数与预期不符），优先改 `structure.json`
（参考 `book-skill-factory/HEURISTICS.md` 的字段说明），或带 `--answers` 重新运行
工厂 `generate.py` 问询。不要在本实例内写死新逻辑。