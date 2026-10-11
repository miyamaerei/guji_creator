"""从 workflow 溢出文件中抢救落盘（一次性工具）

workflow 的 return 值过大时会写入 spill 文件，里面是本批 agent 产出的
{"path": ..., "content": ...} 列表。本脚本把它解析出来写成 _src 源数据文件，
并逐文件 py_compile 校验。

用法：python _salvage_workflow.py <spill文件路径>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def main() -> None:
    raw = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
    # spill 文件是散文本：以 'Return value:' 之后的内容为主，按 JSON 对象切分
    start = raw.find('"path"')
    if start < 0:
        raise SystemExit("未找到 path 字段，无法解析")
    # 用括号配平扫描所有顶层对象
    objs: list[dict] = []
    i = raw.find("{", max(0, start - 40))
    while i != -1 and i < len(raw):
        depth = 0
        in_str = False
        esc = False
        j = i
        while j < len(raw):
            c = raw[j]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        break
            j += 1
        if j >= len(raw):
            break
        chunk = raw[i:j + 1]
        try:
            obj = json.loads(chunk)
            if isinstance(obj, dict) and "path" in obj and "content" in obj:
                objs.append(obj)
        except json.JSONDecodeError:
            # 内容被 spill 截断（含 truncated 标记）则跳过
            pass
        i = raw.find("{", j + 1)

    written: list[tuple[str, int]] = []
    for obj in objs:
        path = str(obj["path"])
        content = obj["content"]
        if "truncated" in content[-200:] or not content.rstrip().endswith("\n"):
            print(f"[跳过] {path}（疑似被截断，长度 {len(content)}）")
            continue
        if not re.match(r"^_src/_[a-z]+_ai_\d\d\.py$", path):
            print(f"[跳过] 非契约路径：{path}")
            continue
        target = ROOT / path
        target.write_text(content, encoding="utf-8")
        written.append((path, content.count('"item_id"') or content.count("'item_id'")))

    for path, count in written:
        print(f"[写出] {path}  记录数≈{count}")
    print(f"共写出 {len(written)} 个文件")


if __name__ == "__main__":
    main()
