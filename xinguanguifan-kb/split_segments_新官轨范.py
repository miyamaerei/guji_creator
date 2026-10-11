# -*- coding: utf-8 -*-
"""
《新官轨范》段落细拆脚本（kg-seg v1）
- 输入：新官轨范_章节/*.xhtml（每卷 1 个文件，<p class="item"> 为一条目）
- 输出：新官轨范_规则_段落/NN_卷名_段.json 与 .txt
  - 每条目按句读（。！？；）再细拆为「段」，每段唯一 id：{ch}-{item:03d}-{seg:02d}
  - source 绑定到段：{file}#条{item}#段{seg}
  - 同时产出段落 JSON（供规则 JSON 的 source/segments 校验与溯源）
"""
import os, re, json, html as htmllib, glob

OUT_DIR = os.path.dirname(os.path.abspath(__file__))  # 项目根：脚本自身位置推导
CH_DIR = os.path.join(OUT_DIR, "新官轨范_章节")
SEG_DIR = os.path.join(OUT_DIR, "新官轨范_规则_段落")
SCHEMA_VER = "kg-seg-json-v1"

def load_chapters():
    out = []
    for fp in sorted(glob.glob(os.path.join(CH_DIR, "*.xhtml"))):
        base = os.path.basename(fp)
        no = base[:2]
        if no == "00":
            continue
        with open(fp, encoding="utf-8") as f:
            content = f.read()
        items = re.findall(r'<p class="item">(.*?)</p>', content, re.S)
        items = [htmllib.unescape(m).strip() for m in items]
        if not items:
            items = re.findall(r'<p[^>]*>(.*?)</p>', content, re.S)
            items = [htmllib.unescape(m).strip() for m in items]
        out.append((no, base, items))
    return out

def split_item(txt):
    """按句读切段，返回 [(text, seg_start, seg_end)]，seg 偏移相对去√后的条目正文"""
    if txt.startswith("√"):
        txt = txt[1:].lstrip()
    segs = []
    pos = 0
    for m in re.finditer(r"[。！？；]", txt):
        seg = txt[pos:m.end()].strip()
        if seg:
            segs.append((seg, pos, m.end()))
        pos = m.end()
    if pos < len(txt):
        seg = txt[pos:].strip()
        if seg:
            segs.append((seg, pos, len(txt)))
    return segs

def main():
    os.makedirs(SEG_DIR, exist_ok=True)
    chapters = load_chapters()
    total = 0
    for ch_no, base, items in chapters:
        ch_name = os.path.splitext(base)[0][3:]
        seg_list = []
        for i, it in enumerate(items, 1):
            for j, (seg, s, e) in enumerate(split_item(it), 1):
                seg_list.append({
                    "seg_id": f"{ch_no}-{i:03d}-{j:02d}",
                    "chapter_no": ch_no,
                    "chapter": ch_name,
                    "item": i,
                    "seg_no": j,
                    "source": f"{base}#条{i}#段{j}",
                    "text": seg,
                    "offset": {"start": s, "end": e},
                })
        total += len(seg_list)
        vjson = {
            "schema_version": SCHEMA_VER,
            "volume": ch_no, "chapter": ch_name, "source_file": base,
            "item_count": len(items), "segment_count": len(seg_list),
            "segments": seg_list,
        }
        with open(os.path.join(SEG_DIR, f"{ch_no}_{ch_name}_段.json"), "w", encoding="utf-8") as f:
            json.dump(vjson, f, ensure_ascii=False, indent=1)
        with open(os.path.join(SEG_DIR, f"{ch_no}_{ch_name}_段.txt"), "w", encoding="utf-8") as f:
            for sg in seg_list:
                f.write(f"{sg['seg_id']}\t{sg['source']}\t{sg['text']}\n")
        print(f"{ch_no} {ch_name}: items={len(items)} segs={len(seg_list)}")
    print("TOTAL_SEGS =", total)

if __name__ == "__main__":
    main()
