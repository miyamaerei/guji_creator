# -*- coding: utf-8 -*-
r"""
古籍全文 JSON 打包器（registry 组装模式 v3，支持三种 registry 形态）
放在 <书>/书籍json/ 下运行：python build_full_json.py
输入（上级=项目根）：_item_registry.json（必需）；_extract/（有则标题回填+对账）；原文/（可选卷名来源）
输出：<书名>_校对版.json（整书 JSON，meta/卷数/条目总数/volumes）

三种形态：
  map2      {id: {original, norm}}                  —— 标题取 original 首行 或 _extract
  records   {records: [{item_id,volume,volume_name,entry_title,original,...}]} —— 标题取 entry_title

统一 schema：meta{书名,版本,底本,item_id规则,条字段} / volumes{no,file,count,items} / items{id,title,text,(可选扩展)}
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

HERE = os.path.dirname(os.path.abspath(__file__))   # <书>/书籍json
PROJECT = os.path.dirname(HERE)                       # 项目根
BOOK = os.path.basename(PROJECT)

CN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}


def cn_num(s):
    """中文数词→数字：一→1 … 三十三→33"""
    if "十" not in s:
        return CN.get(s, 0)
    parts = s.split("十")
    tens = CN.get(parts[0], 1) if parts[0] else 1
    ones = CN.get(parts[1], 0) if len(parts) > 1 and parts[1] else 0
    return tens * 10 + ones


AUTO_CONFIG = {
    "fuhuiquanshu-kb": dict(
        书名="福惠全书",
        形态="map2", 标题来源="original_head", 标题字段="",
        正文剥="head", extract_format=None,
        卷名来源="原文目录", 卷名目录="原文", 卷名正则=r"^卷之(.+)\.txt$",
        registry_dir="", 扩展={}, 底本="fuhuiquanshu-kb 知识工程（_item_registry 指纹库组装，标题取 original 首行）",
    ),
    "yuanshuzaji-kb": dict(
        书名="宛署杂记",
        形态="map2", 标题来源="extract", 标题字段="",
        正文剥="head", extract_format="tiao3",
        卷名来源="_extract", 卷名目录="", 卷名正则=r"^\d{2}_",
        registry_dir="", 扩展={}, 底本="yuanshuzaji-kb 知识工程（_item_registry 指纹库组装，标题取 _extract，正文对账指纹库）",
    ),
    "wanliyehuopian-kb": dict(
        书名="万历野获编",
        形态="records", 标题来源="entry_field", 标题字段="entry_title",
        正文剥="bracket", extract_format="nnn2",
        卷名来源="registry", 卷名目录="", 卷名正则="",
        registry_dir="13-wanli-yehuo-knowledge", 扩展={"subcategory": "subcategory"},
        底本="wanliyehuopian-kb/13-wanli-yehuo-knowledge 知识工程（_item_registry records 组装，标题取 entry_title）",
    ),
    "xuezhenglu-kb": dict(
        书名="政学录",
        形态="map2", 标题来源="extract", 标题字段="",
        正文剥="head", extract_format="tiao3",
        卷名来源="_extract", 卷名目录="", 卷名正则=r"^\d{2}_",
        registry_dir="", 扩展={}, 底本="xuezhenglu-kb 知识工程（_item_registry 指纹库组装，标题取 _extract，正文对账指纹库）",
    ),
    "wuzazu-kb": dict(
        书名="五杂俎",
        形态="map2", 标题来源="first_sentence", 标题字段="",
        正文剥="none", extract_format=None,
        卷名来源="_extract", 卷名目录="", 卷名正则=r"^\d{2}_",
        registry_dir="", 扩展={}, 底本="wuzazu-kb 知识工程（_item_registry 指纹库组装；条目为笔记体无独立标题，title 取正文首句≤24字）",
    ),
    "qubian_kb": dict(
        书名="蘧编",
        形态="map2", 标题来源="title_field", 标题字段="title",
        正文剥="head", extract_format=None,
        卷名来源="registry", 卷名目录="", 卷名正则="",
        registry_dir="", 扩展={}, 底本="qubian_kb 知识工程（_item_registry 指纹库组装，标题取 title 字段；00/21 卷各含两个源文件）",
    ),
    "shuidongriji-kb": dict(
        书名="水东日记",
        形态="map2", 标题来源="first_sentence", 标题字段="",
        正文剥="none", extract_format=None,
        卷名来源="_extract", 卷名目录="", 卷名正则=r"^\d{2}_",
        registry_dir="_extract", extract_dir="_extract/items",
        扩展={}, 底本="shuidongriji-kb 知识工程（_extract/_item_registry 指纹库组装；条目为笔记体无独立标题，title 取正文首句≤24字）",
    ),
    "kezuozhuiyu-kb": dict(
        书名="客座赘语",
        形态="map2", 标题来源="first_sentence", 标题字段="",
        正文剥="none", extract_format=None,
        卷名来源="_extract", 卷名目录="", 卷名正则=r"^\d{2}_",
        registry_dir="", extract_dir="",
        扩展={}, 底本="kezuozhuiyu-kb 知识工程（_item_registry 指纹库组装；条目为笔记体无独立标题，title 取正文首句≤24字）",
    ),
    "mingshi-dilizhi": dict(
        书名="明史·地理志",
        形态="map2", 标题来源="first_sentence", 标题字段="",
        正文剥="none", extract_format=None,
        卷名来源="_extract", 卷名目录="", 卷名正则=r"^\d{2}_",
        registry_dir="", extract_dir="",
        扩展={}, 底本="mingshi/mingshi-dilizhi 知识工程（_item_registry 指纹库组装；志体条目无独立标题，title 取正文首句≤24字）",
    ),
    "mingshi-zhiguanzhi": dict(
        书名="明史·职官志",
        形态="map2", 标题来源="first_sentence", 标题字段="",
        正文剥="none", extract_format=None,
        卷名来源="_extract", 卷名目录="", 卷名正则=r"^\d{2}_",
        registry_dir="", extract_dir="",
        扩展={}, 底本="mingshi/mingshi-zhiguanzhi 知识工程（_item_registry 指纹库组装；志体条目无独立标题，title 取正文首句≤24字）",
    ),
    "mingshi-shihuozhi": dict(
        书名="明史·食货志",
        形态="map2", 标题来源="first_sentence", 标题字段="",
        正文剥="none", extract_format=None,
        卷名来源="_extract", 卷名目录="", 卷名正则=r"^vol_(\d{2})\.txt$",
        registry_dir="_data", registry_file="registry.json",
        vol_name_field="volume", extract_dir="_extract",
        扩展={}, 底本="mingshi/mingshi-shihuozhi 知识工程（_data/registry.json 切条库组装；志体条目无独立标题，title 取正文首句≤24字）",
    ),
    "mingshi-xuanju": dict(
        书名="明史·选举志",
        形态="txt_raw", 标题来源="", 标题字段="",
        正文剥="", extract_format=None,
        卷名来源="", 卷名目录="", 卷名正则="",
        registry_dir="", extract_dir="", txt_path="选举志.txt",
        扩展={}, 底本="mingshi/mingshi-xuanju 原文直解析（选举志.txt：◆ 章边界切卷，◎ 小节为条目；无条目级切条，每卷成 1 条）",
    ),
    "xinguanguifan-kb": dict(
        书名="新官轨范",
        形态="map2", 标题来源="first_sentence", 标题字段="",
        正文剥="none", extract_format=None,
        卷名来源="_extract", 卷名目录="", 卷名正则=r"^\d{2}_",
        registry_dir="", extract_dir="",
        扩展={}, 底本="xinguanguifan-kb 知识工程（_item_registry 指纹库组装；条文无独立标题，title 取正文首句≤24字；卷00为整理说明，缺卷源文件以占位补卷）",
    ),
    "mingyitongzhi-kb": dict(
        书名="明一统志",
        形态="myz_full", 标题来源="", 标题字段="",
        正文剥="", extract_format=None,
        卷名来源="", 卷名目录="", 卷名正则="",
        registry_dir="", extract_dir="", voljson_dir="14-mingyitongzhi-knowledge/_data",
        txt_path="明一统志.txt",
        扩展={}, 底本="mingyitongzhi-kb/明一统志.txt（四库全书本，正文 90 卷按“明一统志卷X”首标切分，卷00卷首=提要/御制序/进表/职名，卷九十后混入《钦定大清一统志》已截除）+ 14-mingyitongzhi-knowledge/_data/volNN 校对条目（卷01-05/19-31/88 共18卷）；校对卷 title 取 source、text 取 original，空缺卷按原书卷直解析每卷成 1 条",
    ),
}


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def parse_extract(extract_dir, fmt):
    """解析 _extract → {id: (标题, 正文)}；fmt: tiao3=条N|标题|正文 | nnn2=NN-NNN|【标题】正文"""
    items = {}
    if not os.path.isdir(extract_dir):
        return items
    for fn in sorted(os.listdir(extract_dir)):
        m = re.match(r"^(\d{2})_", fn)
        if not m or not fn.endswith(".txt"):
            continue
        no = m.group(1)
        for ln in io.open(os.path.join(extract_dir, fn), encoding="utf-8"):
            line = ln.rstrip("\n")
            if fmt == "tiao3":
                mm = re.match(r"^条(\d+)\|([^|]*)\|(.*)$", line)
                if mm:
                    items[f"{no}-{int(mm.group(1)):03d}"] = (mm.group(2).strip(), mm.group(3).strip())
            elif fmt == "nnn2":
                mm = re.match(r"^(\d{2})-(\d{3})\|(.*)$", line)
                if mm:
                    body = mm.group(3).strip()
                    tm = re.match(r"^【(.+?)】", body)
                    title = tm.group(1).strip() if tm else ""
                    body = body[tm.end():].strip() if tm else body
                    items[f"{mm.group(1)}-{mm.group(2)}"] = (title, body)
    return items


def num_cn(n):
    """数字→中文数词：33→三十三；0→〇（用于缺卷文件的占位卷名）"""
    digits = "一二三四五六七八九"
    if n == 0:
        return "〇"
    if n < 10:
        return digits[n - 1]
    if n == 10:
        return "十"
    t, o = divmod(n, 10)
    s = ("十" if t == 1 else digits[t - 1] + "十") if t else ""
    if o:
        s += digits[o - 1]
    return s


def first_sentence_of(text, max_len=24):
    """取正文首句作标题（笔记体无独立标题时），截断至 ≤max_len，去掉引号"""
    t = text.strip()
    s = t
    for i, ch in enumerate(t):
        if ch in "。！？":
            s = t[:i + 1]
            break
    s = s.strip("\u201c\u201d\"' \u3000")
    return s[:max_len]


def build_txt(cfg):
    """原文直解析形态：◆【章-卷】标题 切卷，◎小节 为条目（无 ◎ 则整卷一条）"""
    txt = io.open(os.path.join(PROJECT, cfg["txt_path"]), encoding="utf-8").read()
    vols = list(re.finditer(r"◆【(.+?)】(.+)", txt))
    volumes, total = [], 0
    for k, m in enumerate(vols):
        no = f"{k + 1:02d}"
        vname = m.group(2).strip()
        seg = txt[m.end():vols[k + 1].start() if k + 1 < len(vols) else len(txt)]
        subs = re.split(r"◎([^\n]+)", seg)
        items = []
        j = 0
        if subs[0].strip():
            j += 1
            b = subs[0].strip()
            items.append({"id": f"{no}-{j:03d}", "title": first_sentence_of(b), "text": b})
        for i in range(1, len(subs), 2):
            t = subs[i].strip()
            b = subs[i + 1].strip() if i + 1 < len(subs) else ""
            if not b:
                continue
            j += 1
            items.append({"id": f"{no}-{j:03d}", "title": t or first_sentence_of(b), "text": b})
        if not items:
            j += 1
            items.append({"id": f"{no}-{j:03d}", "title": vname, "text": seg.strip()})
        volumes.append({"no": no, "file": cfg["txt_path"], "name": vname, "count": len(items), "items": items})
        total += len(items)
        print(f"[卷{no}] {vname}: {len(items)} 条")
    print(f"\n条目总数: {total}")
    doc = {
        "meta": {
            "书名": cfg["书名"], "版本": "校对版", "底本": cfg["底本"],
            "item_id规则": "NN-NNN（卷号两位-条号三位，卷内 001 起连续）", "条字段": "id/title/text",
        },
        "卷数": len(volumes), "条目总数": total, "volumes": volumes,
    }
    out = os.path.join(HERE, f"{cfg['书名']}_校对版.json")
    with io.open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(f"整书 JSON: {out}（{os.path.getsize(out) / 1024:.0f} KB）")


def build_voljson(cfg):
    """按卷条目 json 目录组装（_data/volNN/*.json）：title 取 source，text 取 original，
    源 item_id 卷内可能重复，按卷内文件名排序重算 id；卷号按目录名（支持 3 位卷号）"""
    src = os.path.join(PROJECT, cfg["voljson_dir"])
    vols = {}
    for name in os.listdir(src):
        m = re.match(r"^vol(\d+)$", name)
        if m and os.path.isdir(os.path.join(src, name)):
            vols[m.group(1)] = name
    volumes, total = [], 0
    for no in sorted(vols, key=int):
        d = os.path.join(src, vols[no])
        raw = []
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".json"):
                continue
            j = json.load(io.open(os.path.join(d, fn), encoding="utf-8-sig"))
            text = (j.get("original") or "").strip()
            if not text:
                continue
            raw.append((fn, j.get("source") or "", text))
        items = []
        for j, (fn, src_t, text) in enumerate(raw, 1):
            items.append({"id": f"{no}-{j:03d}", "title": src_t or first_sentence_of(text), "text": text})
        if not items:
            print(f"[跳过] {vols[no]} 空卷（知识工程占位目录，无条目化 json），已跳过")
            continue
        vname = items[0]["title"] if items else ""
        volumes.append({
            "no": no, "file": vols[no],
            **({"name": vname} if vname else {}),
            "count": len(items), "items": items,
        })
        total += len(items)
        print(f"[卷{no}] {vols[no]}: {len(items)} 条")
    print(f"\n条目总数: {total} | 卷数: {len(volumes)}")
    doc = {
        "meta": {
            "书名": cfg["书名"], "版本": "校对版", "底本": cfg["底本"],
            "item_id规则": "卷号-条号（卷号按源卷号位数，条号三位，卷内 001 起）", "条字段": "id/title/text",
        },
        "卷数": len(volumes), "条目总数": total, "volumes": volumes,
    }
    out = os.path.join(HERE, f"{cfg['书名']}_校对版.json")
    with io.open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(f"整书 JSON: {out}（{os.path.getsize(out) / 1024:.0f} KB）")


def build_myz_full(cfg):
    """明一统志 90 卷全本混合组装：
    卷00（卷首：提要/御制序/进表/职名）+ 正文卷一~卷九十。
    有知识工程校对条目的卷（_data/volNN 非空）用条目 json（title=source，text=original，卷内重算 id），
    并用条目 source 在原书对应卷段内定位（行号锚定），输出卷内条目行号连续表；
    空缺卷按原书 txt 直解析（“明一[统統綂]志卷X”首标切卷，卷号递增取首标、页末重复标忽略；
    每卷成 1 条，title=卷首条目标题，text=整卷正文；卷九十段尾截在最后一个卷标处，排除混入的《钦定大清一统志》）。
    输出《明一统志.json》（非“校对版”，因含原书直解析卷）。"""
    # 1) 原书卷边界：卷号递增取首标，并用“首标后必跟 明/眀 李贤等 撰”校验（原书“明/眀”“统/統/綂”“卷/巻”异体混用）
    txt_path = os.path.join(PROJECT, cfg["txt_path"])
    txt = io.open(txt_path, encoding="utf-8-sig").read()
    lines = txt.split("\n")
    marks = list(re.finditer(r"[明眀]一[统統綂]志[卷巻]([一二三四五六七八九十百]+)", txt))
    starts, expect = [], 1
    for m in marks:
        no = cn_num(m.group(1))
        if no == expect and re.sub(r"\s", "", txt[m.end():m.end() + 80])[:5] in ("明李贤等撰", "眀李贤等撰"):
            starts.append((no, m))
            expect += 1
            if expect > 90:
                break
    assert len(starts) == 90, f"原书真首标数 {len(starts)} != 90"
    tail_end = len(txt)
    if marks and cn_num(marks[-1].group(1)) == 90:
        tail_end = marks[-1].start()  # 卷九十末标（其后即《钦定大清一统志》提要）
    segs, seg_first_line = {}, {}
    for k, (no, m) in enumerate(starts):
        beg = m.end()
        end = starts[k + 1][1].start() if k + 1 < len(starts) else tail_end
        segs[no] = txt[beg:end]
        seg_first_line[no] = txt[: m.start()].count("\n") + 1
    vol00 = txt[: starts[0][1].start()].strip()

    # 2) _data 数据卷
    src = os.path.join(PROJECT, cfg["voljson_dir"])
    data_vols = {}
    for name in os.listdir(src):
        m = re.match(r"^vol(\d+)$", name)
        if m and os.path.isdir(os.path.join(src, name)):
            data_vols[m.group(1)] = name

    def read_data_vol(no, dirname):
        d = os.path.join(src, dirname)
        raw = []
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".json"):
                continue
            j = json.load(io.open(os.path.join(d, fn), encoding="utf-8-sig"))
            text = (j.get("original") or "").strip()
            if not text:
                continue
            raw.append((fn, j.get("source") or "", text))
        return [{"id": f"{no}-{j:03d}", "title": st or first_sentence_of(t), "text": t}
                for j, (fn, st, t) in enumerate(raw, 1)]

    def anchor_titles(items, seg_lines, seg_global_line):
        """按 items 顺序在原书该卷段各行中定位 title 首次出现（行号锚定）"""
        anchored, cur = [], 0
        for it in items:
            title = it["title"]
            if not title:
                anchored.append(None)
                continue
            found = None
            for i in range(cur, len(seg_lines)):
                if title in seg_lines[i]:
                    found = seg_global_line + i
                    cur = i
                    break
            anchored.append(found)
        return anchored

    # 3) 组装 00 + 01~90
    volumes, total = [], 0
    if vol00:
        volumes.append({"no": "00", "file": cfg["txt_path"], "name": "卷首", "count": 1,
                        "items": [{"id": "00-001", "title": "卷首（提要·御制序·进表·职名）", "text": vol00}]})
        total += 1
        print("[卷00] 卷首（提要/序/进表/职名）: 1 条")
    for no in range(1, 91):
        key = f"{no:02d}"
        items = read_data_vol(key, data_vols[key]) if key in data_vols else []
        if items:
            seg = segs.get(no, "")
            if seg:
                # 卷全文兜底条目（id=NN-000）：覆盖原书该卷完整正文，保证“原书全文不遗漏”
                items = [{"id": f"{key}-000", "title": f"卷{key} 全文", "text": seg.strip()}] + items
            volumes.append({"no": key, "file": data_vols[key],
                            "name": items[1]["title"] if len(items) > 1 else f"卷{key} 全文",
                            "count": len(items), "items": items})
            total += len(items)
            seg = segs.get(no, "")
            seg_lines = seg.split("\n")
            gl = seg_first_line.get(no, 1)
            anchor = anchor_titles(items, seg_lines, gl)
            got = [a for a in anchor if a is not None]
            order_ok = got == sorted(got)
            gaps = [got[i + 1] - got[i] for i in range(len(got) - 1)]
            bad = [g for g in gaps if g < 0 or g > 80]
            print(f"[卷{key}] {data_vols[key]}（校对卷）: {len(items)} 条 | 行号锚定 {len(got)}/{len(items)} "
                  f"覆盖 {got[0] if got else '-'}~{got[-1] if got else '-'}（段 {gl}~{gl + len(seg_lines) - 1}）"
                  f"| 顺序{'OK' if order_ok else '乱序'} | 中断gap{len(bad)}")
        else:
            seg = segs.get(no, "")
            if not seg:
                print(f"[卷{key}] 原书无此卷段，跳过")
                continue
            first = None
            for ln in seg.split("\n"):
                s = ln.strip()
                if s and re.sub(r"\s", "", s) not in ("明李贤等撰", "眀李贤等撰") and not s.startswith("钦定四库全书"):
                    first = s
                    break
            if not first:
                first = f"卷{key}"
            volumes.append({"no": key, "file": cfg["txt_path"], "name": first, "count": 1,
                            "items": [{"id": f"{key}-001", "title": first, "text": seg.strip()}]})
            total += 1
            print(f"[卷{key}] 原书直解析: 1 条（卷名={first[:14]}…）")
    print(f"\n条目总数: {total} | 卷数: {len(volumes)}")
    doc = {
        "meta": {
            "书名": cfg["书名"], "版本": "明一统志 90 卷全本（混合来源）", "底本": cfg["底本"],
            "item_id规则": "卷号-条号（卷号两位 00-90；条号三位：000=卷级全文兜底条目，001 起为条目）", "条字段": "id/title/text",
        },
        "卷数": len(volumes), "条目总数": total, "volumes": volumes,
    }
    out = os.path.join(HERE, f"{cfg['书名']}.json")
    with io.open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(f"整书 JSON: {out}（{os.path.getsize(out) / 1024:.0f} KB）")


def build_book(cfg):
    reg_dir = os.path.join(PROJECT, cfg.get("registry_dir") or "")
    reg_path = os.path.join(reg_dir, cfg.get("registry_file") or "_item_registry.json")
    reg = load(reg_path)
    # 归一为 {id: data}
    if cfg["形态"] == "records":
        data = {r["item_id"]: r for r in reg["records"]}
    else:
        data = reg
    ed = cfg.get("extract_dir")
    extract_dir = os.path.join(PROJECT, ed) if ed else os.path.join(reg_dir, "_extract")
    extract = parse_extract(extract_dir, cfg["extract_format"]) if cfg["extract_format"] else {}

    # 卷名回填（优先：registry 带卷名字段时，如食货 volume='食货一'）
    vnf = cfg.get("vol_name_field")
    if vnf:
        for i, d in data.items():
            no = i.split("-")[0]
            vol_names.setdefault(no, str(d.get(vnf, "") or ""))

    # 卷文件映射
    vol_files = {}  # no -> file
    vol_names = {}  # no -> name
    if cfg["卷名来源"] == "_extract":
        for fn in sorted(os.listdir(extract_dir)):
            if not fn.endswith(".txt"):
                continue
            m = re.match(cfg["卷名正则"], fn)
            if m:
                no = m.group(1) if m.groups() else fn[:2]
                vol_files[no] = fn
                vol_names.setdefault(no, fn[3:-4] if fn.startswith(no + "_") else fn[:-4])
    elif cfg["卷名来源"] == "原文目录":
        src = os.path.join(PROJECT, cfg["卷名目录"])
        for fn in os.listdir(src):
            m = re.match(cfg["卷名正则"], fn)
            if m:
                n = cn_num(m.group(1))
                if n:
                    vol_files[f"{n:02d}"] = fn
                    vol_names[f"{n:02d}"] = f"卷之{m.group(1)}"
    elif cfg["卷名来源"] == "registry":
        for i, d in data.items():
            no = d["volume"]
            vn = d.get("volume_name", "")
            if vn:
                vol_files[no] = f"{no}_{vn}.txt"
                vol_names[no] = vn
            else:
                vol_files.setdefault(no, "")
        # 无 volume_name 的卷：从 extract 目录匹配 {no}_ 前缀文件（一卷多文件时取首个）
        if os.path.isdir(extract_dir):
            for fn in sorted(os.listdir(extract_dir)):
                m = re.match(r"^(\d{2})_", fn)
                if m and fn.endswith(".txt") and m.group(1) in vol_files and not vol_files[m.group(1)]:
                    vol_files[m.group(1)] = fn

    # 补齐指纹库存在但卷文件映射缺失的卷（原卷文件缺档时以占位名补卷，缺口如实保留）
    for no in sorted({k.split("-")[0] for k in data}):
        if no not in vol_files:
            vn = f"卷之{num_cn(int(no))}"
            vol_files[no] = f"{no}_{vn}.txt"
            vol_names[no] = vn
            print(f"  [缺口] 卷 {no} 缺卷源文件，已以占位名 {vol_files[no]} 补卷")

    volumes, total, title_fb, mism = [], 0, 0, []
    for no in sorted(vol_files):
        fn = vol_files[no]
        ids = sorted(i for i in data if i.startswith(no + "-"))
        items = []
        for i in ids:
            d = data[i]
            orig = d.get("original", "")
            if cfg["标题来源"] in ("entry_field", "title_field"):
                title = d.get(cfg["标题字段"], "").strip()
            elif cfg["标题来源"] == "extract":
                title = extract.get(i, ("", ""))[0] or orig.split("\n", 1)[0].strip()
                if extract.get(i):
                    title_fb += 1
            elif cfg["标题来源"] == "first_sentence":
                title = ""
            else:  # original_head
                title = orig.split("\n", 1)[0].strip()
            # 正文
            if cfg["正文剥"] == "bracket":
                text = orig
                if title and text.startswith("【" + title + "】"):
                    text = text[len("【" + title + "】"):].strip()
            elif cfg["正文剥"] == "none":
                text = orig.strip()
            else:  # head
                text = orig
                if title and text.startswith(title):
                    text = text[len(title):].lstrip("\n").strip()
            if cfg["标题来源"] == "first_sentence":
                title = first_sentence_of(text)
            it = {"id": i, "title": title, "text": text}
            if not text.strip():
                print(f"  [剔除] {i} 空正文伪条目（章节标记残留），已跳过")
                continue
            for k, src in cfg["扩展"].items():
                if src in d:
                    it[k] = d[src]
            # 对账（有 extract 时）
            et, eb = extract.get(i, ("", ""))
            if et and title != et:
                mism.append(("标题", i, title[:20], et[:20]))
            if eb and eb.replace("\n", "") != text.replace("\n", ""):
                mism.append(("正文", i, "", ""))
            items.append(it)
        volumes.append({
            "no": no, "file": fn,
            **({"name": vol_names[no]} if no in vol_names else {}),
            "count": len(items), "items": items,
        })
        total += len(items)
        print(f"[卷{no}] {fn}: {len(items)} 条")

    ids = {i["id"] for v in volumes for i in v["items"]}
    gap = []
    for v in volumes:
        exp = [f"{v['no']}-{k:03d}" for k in range(1, len(v["items"]) + 1)]
        gap += [e for e in exp if e not in {i["id"] for i in v["items"]}]
    print(f"\n条目总数: {total} | 指纹库: {len(data)} | 未归卷: {len(set(data) - ids)} | 卷内断号: {len(gap)} | 标题取自extract: {title_fb}")
    if mism:
        print(f"对账: 标题不一致 {len([m for m in mism if m[0]=='标题'])} 条；正文差异 {len([m for m in mism if m[0]=='正文'])} 条（extract 为原始切条，正文以 registry 校对版为准，差异多为校对修正）")
        bad = [m for m in mism if m[0] == "标题"]
        if bad:
            print(f"  标题不一致样例: {bad[:8]}")
    else:
        print("对账: 0 不一致（extract 标题/正文与 registry 完全一致）")

    doc = {
        "meta": {
            "书名": cfg["书名"], "版本": "校对版", "底本": cfg["底本"],
            "item_id规则": "NN-NNN（卷号两位-条号三位，卷内 001 起连续）", "条字段": "id/title/text",
        },
        "卷数": len(volumes), "条目总数": total, "volumes": volumes,
    }
    out = os.path.join(HERE, f"{cfg['书名']}_校对版.json")
    with io.open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(f"整书 JSON: {out}（{os.path.getsize(out) / 1024:.0f} KB）")


if __name__ == "__main__":
    cfg = AUTO_CONFIG.get(BOOK)
    if not cfg:
        print(f"未知项目 {BOOK}，请在 AUTO_CONFIG 中补充配置")
        sys.exit(1)
    print(f"===== {cfg['书名']}（{BOOK}）=====")
    if cfg["形态"] == "txt_raw":
        build_txt(cfg)
    elif cfg["形态"] == "voljson":
        build_voljson(cfg)
    elif cfg["形态"] == "myz_full":
        build_myz_full(cfg)
    else:
        build_book(cfg)
