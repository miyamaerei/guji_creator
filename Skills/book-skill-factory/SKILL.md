---
name: book-skill-factory
description: 书籍处理「skills 工厂」：为任意一本书生成专属书实例技能。通过六组启发式问题（目录区/正文起点/卷/条目标题/段落/噪声校验）向用户或 Agent 问询，把答案翻译成该书的 structure.json，再渲染书实例（SKILL.md + 薄壳 extract.py）。实例的解析依赖本工厂 common/ 参考模板引擎，工厂不针对任何具体书写死解析代码。当用户需要对一本书做「识别目录/卷/标题/段落四级结构、每卷单独提取、合并全本」并生成可复用技能时使用本工厂。
---

# book-skill-factory — 书实例生成工厂

本技能是**工厂**，产出物是**书实例技能**，不是某一本书的解析代码。

核心立场：

1. **问询驱动，不写死**：每本书的结构由 `HEURISTICS.md` 六组启发式问题确定，
   答案进入书实例的 `structure.json`；工厂没有任何"某本书专用"的判定逻辑。
2. **代码只是参考/模板**：`generate.py`、`common/*.py`、`templates/` 均为参考实现，
   书的全部差异由配置表达，改书 = 改配置，不碰代码。

## 工作流（三步）

```
问询引导解析结构 -> 组装 structure.json -> 渲染书实例模板
```

### 第一步：观察源书（Agent 先做）
对源书首、尾、中间各抽样约 20 行，识别四种痕迹：
目录区标记、正文起点标记、卷标记形态、条目标题层级、段落分隔方式、导出噪声。

### 第二步：问询（收集答案）
用 `generate.py` 三种方式之一收集六组问题答案：

| 方式 | 命令 | 适用 |
|------|------|------|
| 交互问询 | `python generate.py --book <path>` | 人工逐题确认 |
| 答案文件 | `python generate.py --book <path> --answers a.json` | Agent 观察后填写/回放 |
| 参考答案 | `python generate.py --book <path> --no-interactive` | 快速起步 |
| 已有配置 | `python generate.py --config <structure.json>` | 已生成过，只重建实例 |

答案键与映射见 `HEURISTICS.md`（六组问题表）与 `common/schemas.py`。

### 第三步：渲染与验收
生成 `book-<slug>/`（SKILL.md、structure.json、scripts/extract.py），
工厂会输出**快照统计**（卷/标题/段落/字符数）供人工核验。
实例运行方式：

```bash
cd <技能安装目录>/book-<slug>
python scripts/extract.py --mode volumes   # 每卷单独 txt
python scripts/extract.py --mode full      # 合并全本 txt
python scripts/extract.py --mode toc       # 目录 txt
```

## 目录结构

```
book-skill-factory/
├── SKILL.md              # 本说明
├── HEURISTICS.md         # 六组启发式问题手册（唯一问题源）
├── generate.py           # 问询向导 + 渲染器（参考实现）
├── common/               # 参考模板引擎（读入/清洗/解析/渲染，结构由配置驱动）
│   ├── input_adapter.py
│   ├── cleaner.py
│   ├── parser.py
│   ├── render.py
│   ├── schemas.py
│   └── __init__.py
└── templates/book-skill/ # 书实例模板
    ├── SKILL.md.tpl
    └── extract.py.tpl
```

## 边界与约束

- 不修改书实例里的 extract.py 增加判定逻辑；结构不准改 `structure.json` 或重跑问询。
- 生成书实例后若需作为独立技能使用，按平台规范注册（extension-sync add）。
- `common/` 引擎是参考骨架：若新书有引擎覆盖不了的结构（如多级嵌套标题），
  先考虑用配置表达；确实表达不了才扩展引擎，且扩展必须保持通用（不写死某本书）。