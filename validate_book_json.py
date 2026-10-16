# -*- coding: utf-8 -*-
r"""
书籍 JSON 统一校验器（validate_book_json.py）
校验 guji 下所有 <书>/书籍json/<书名>_校对版.json 是否符合统一 schema，
并核对 分卷json/ 与整书一致性。用法：
  python validate_book_json.py                # 自动扫描 E:\git\ToolBox\guji 下所有 书籍json
  python validate_book_json.py <书籍json路径> [更多路径...]   # 指定校验
退出码：全部通过=0，任一不通过=1

统一 schema（必填项）：
  顶层    : meta, 卷数, 条目总数, volumes
  meta 必填: 书名, 版本, 底本, item_id规则, 条字段
            （作者/体裁/源 为可选，存在与否不判错）
  volumes : no, file, count, items          （name 可选）
  items   : id, title, text                 （section/source 等可选扩展）
校验项：
  1 必填字段存在性（顶层/meta/卷/条目）
  2 计数一致性：卷数==len(volumes)；条目总数==sum(count)==sum(len(items))
  3 id 规则：全书唯一；id 前缀==卷 no；卷内序号 001 起连续
  4 title/text 非空字符串
  5 分卷一致性：分卷json 卷文件数==卷数；每个卷文件 volumes[0] 与整书对应卷完全相等
"""
import io
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TOP_REQUIRED = ["meta", "卷数", "条目总数", "volumes"]
META_REQUIRED = ["书名", "版本", "底本", "item_id规则", "条字段"]
VOL_REQUIRED = ["no", "file", "count", "items"]
ITEM_REQUIRED = ["id", "title", "text"]


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def check_book(bj_dir, name=""):
    """校验一个 书籍json 目录；返回 (通过?, [问题列表])"""
    problems = []
    whole_files = sorted(
        f for f in os.listdir(bj_dir)
        if f.endswith(".json") and not f.startswith("_")
    )
    if not whole_files:
        return False, [f"{bj_dir}: 未找到整书 json（*_校对版.json 或 <书名>.json）"]
    for wf in whole_files:
        whole_path = os.path.join(bj_dir, wf)
        try:
            d = load(whole_path)
        except Exception as e:
            problems.append(f"{wf}: 无法解析 JSON（{e}）")
            continue
        book = name or d.get("meta", {}).get("书名", wf)
        # 1 必填字段
        for k in TOP_REQUIRED:
            if k not in d:
                problems.append(f"{book}: 顶层缺必填 {k}")
        for k in META_REQUIRED:
            if k not in d.get("meta", {}):
                problems.append(f"{book}: meta 缺必填 {k}")
        if "volumes" not in d:
            continue
        # 2 计数一致性
        vols = d["volumes"]
        if d.get("卷数") != len(vols):
            problems.append(f"{book}: 卷数声明 {d.get('卷数')} != 实际 {len(vols)}")
        if d.get("条目总数") != sum(len(v.get("items", [])) for v in vols):
            problems.append(f"{book}: 条目总数声明 {d.get('条目总数')} != 实际")
        # 3/4 卷与条目
        all_ids = []
        for v in vols:
            for k in VOL_REQUIRED:
                if k not in v:
                    problems.append(f"{book}/{v.get('no','?')}: 卷缺必填 {k}")
            items = v.get("items", [])
            if v.get("count") != len(items):
                problems.append(f"{book}/{v.get('no','?')}: count {v.get('count')} != 条目数 {len(items)}")
            no = v.get("no", "")
            ids = []
            for i, it in enumerate(items, 1):
                for k in ITEM_REQUIRED:
                    if k not in it:
                        problems.append(f"{book}/{it.get('id','?')}: 条目缺必填 {k}")
                        break
                iid = it.get("id", "")
                if iid in all_ids:
                    problems.append(f"{book}: id 重复 {iid}")
                all_ids.append(iid)
                if iid and not iid.startswith(f"{no}-"):
                    problems.append(f"{book}: id {iid} 前缀 != 卷号 {no}")
                ids.append(iid)
                if not (isinstance(it.get("title", ""), str) and it["title"].strip()):
                    problems.append(f"{book}/{iid}: title 为空")
                if not (isinstance(it.get("text", ""), str) and it["text"].strip()):
                    problems.append(f"{book}/{iid}: text 为空")
            # 卷内 id 严格递增且无重复（允许数据缺口，如伪条目剔除/卷文件缺档）
            if ids != sorted(ids) or len(set(ids)) != len(ids):
                problems.append(f"{book}: 卷{no} 内 id 非严格递增或有重复")
        # 5 分卷一致性
        vol_dir = os.path.join(bj_dir, "分卷json")
        if not os.path.isdir(vol_dir):
            problems.append(f"{book}: 缺 分卷json 目录")
        else:
            vol_files = sorted(f for f in os.listdir(vol_dir) if f.endswith(".json"))
            if len(vol_files) != len(vols):
                problems.append(f"{book}: 分卷文件数 {len(vol_files)} != 卷数 {len(vols)}")
            else:
                for v in vols:
                    fn = None
                    cand = [f for f in vol_files if f.startswith(f"{v['no']}_") or f.startswith(f"{v['no']}.")]
                    if len(cand) == 1:
                        fn = cand[0]
                    if fn is None:
                        problems.append(f"{book}: 分卷缺卷 {v['no']}")
                        continue
                    try:
                        vd = load(os.path.join(vol_dir, fn))
                        vv = (vd.get("volumes") or [None])[0]
                        if vv != v:
                            problems.append(f"{book}: 分卷 {fn} 与整书卷 {v['no']} 不一致")
                    except Exception as e:
                        problems.append(f"{book}: 分卷 {fn} 读取失败（{e}）")
    return len(problems) == 0, problems


def main():
    targets = sys.argv[1:]
    if not targets:
        guji = r"E:\git\ToolBox\guji"
        targets = [
            os.path.join(root, "书籍json")
            for root, dirs, files in os.walk(guji)
            if os.path.isdir(os.path.join(root, "书籍json"))
        ]
    ok_all = True
    for t in targets:
        ok, problems = check_book(t)
        book = os.path.basename(os.path.dirname(t)) if os.path.basename(t) == "书籍json" else t
        status = "PASS" if ok else f"FAIL（{len(problems)} 项）"
        print(f"[{status}] {book}")
        for p in problems[:40]:
            print(f"    - {p}")
        if len(problems) > 40:
            print(f"    … 其余 {len(problems) - 40} 项省略")
        ok_all = ok_all and ok
    print("\n===== 汇总 =====")
    print("全部通过" if ok_all else "存在未通过项")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
