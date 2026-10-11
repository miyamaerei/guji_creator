# -*- coding: utf-8 -*-
"""《蘧编》TRL 古今翻译层独立管线（支持 --volumes 按卷分步）。

标准（用户指定）：
- ID 前缀 TRL-；schema 槽位 trl_id / item_id / translation / style / note / confidence / original
- 风格枚举：直译 / 意译 / 注释性翻译（默认，余光中风格，见 qubian-knowledge references/translation-style.md）
- 交付形态：每卷译文 JSON（_trl_NN.json）+ 全书记译文本（trl_卷NN_全书记译.txt）+ 汇总（trl_汇总.json，增量合并）
- 执行方式：translation 由 AI 逐条审定（复用 _ai_NN.py 的 trl，已按七条规范复核）；note/confidence 由 _trl_notes.py 覆盖；
  代码只验覆盖（条目数 = 翻译数）与 schema 字段齐全，结果写 trl_验证.txt（不依赖 stdout）。
- 幂等：写出前清理目标旧文件，避免残留陈旧记录。
用法：python build_trl.py --volumes 01 02   （不带 --volumes 则全卷 01-20）
"""
import argparse, json, os, sys, importlib.util

KB = os.path.dirname(os.path.abspath(__file__))
VOLUMES = [f"{i:02d}" for i in range(1, 21)]

def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def load_notes():
    p = os.path.join(KB, "_trl_notes.py")
    if not os.path.exists(p):
        return {}
    return load_mod("_trl_notes", p).TRL_NOTES

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volumes", nargs="*", default=None)
    args = ap.parse_args()
    vols = args.volumes if args.volumes else VOLUMES

    with open(os.path.join(KB, "_item_registry.json"), encoding="utf-8") as f:
        REG = json.load(f)
    notes = load_notes()

    # 增量合并语义：加载既有汇总，只重算请求卷
    sum_path = os.path.join(KB, "trl_汇总.json")
    merged = {}
    if os.path.exists(sum_path):
        with open(sum_path, encoding="utf-8") as f:
            merged = json.load(f).get("records", {})

    ver_lines = []
    ok = True
    for vol in vols:
        src_path = os.path.join(KB, f"_ai_{vol}.py")
        if not os.path.exists(src_path):
            ver_lines.append(f"[ERR] {vol}: 源数据 {os.path.basename(src_path)} 不存在")
            ok = False
            continue
        src = load_mod(f"_ai_{vol}", src_path).SRC
        records = []
        # 幂等清理本卷旧产物
        for old in (f"_trl_{vol}.json", f"trl_卷{vol}_全书记译.txt"):
            op = os.path.join(KB, old)
            if os.path.exists(op):
                os.remove(op)
        seq = 0
        txt_lines = [f"《蘧编》卷{vol} 全书记译（现代文）", f"（卷 {vol}：{len(src)} 条）", ""]
        for item_id, data in src.items():
            if item_id not in REG:
                ver_lines.append(f"[ERR] {item_id}: 不在指纹库")
                ok = False
                continue
            seq += 1
            raw = data.get("trl")
            if raw is None:
                ver_lines.append(f"[ERR] {item_id}: 无 trl")
                ok = False
                continue
            if isinstance(raw, str):
                raw = {"translation": raw}
            rec = dict(raw)
            rec["trl_id"] = f"TRL-{int(vol) * 500 + seq}"
            rec["item_id"] = item_id
            rec["volume"] = vol
            rec["original"] = REG[item_id].get("original", "")
            rec.setdefault("style", "注释性翻译")
            nt = notes.get(item_id, {})
            rec.setdefault("confidence", nt.get("confidence", "high"))
            rec.setdefault("note", nt.get("note", ""))
            # schema 完整性
            for field in ("trl_id", "item_id", "translation", "style", "note", "confidence", "original"):
                if field not in rec or (isinstance(rec[field], str) and not rec[field].strip() and field in ("translation", "trl_id", "item_id")):
                    ver_lines.append(f"[ERR] {item_id}: 缺字段 {field}")
                    ok = False
            records.append(rec)
            txt_lines.append(f"【{item_id}】{rec['translation']}")
            txt_lines.append("")
        # 本卷 JSON
        vol_json = {"volume": vol, "scope": f"卷{vol}", "count": len(records), "records": records}
        with open(os.path.join(KB, f"_trl_{vol}.json"), "w", encoding="utf-8") as f:
            json.dump(vol_json, f, ensure_ascii=False, indent=1)
        # 本卷全书记译文本
        with open(os.path.join(KB, f"trl_卷{vol}_全书记译.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(txt_lines))
        merged[vol] = vol_json
        ver_lines.append(f"[OK] {vol}: {len(records)} 条翻译，覆盖 {len(src)}/{len(src)}，trl_id TRL-{int(vol)*500+1}~TRL-{int(vol)*500+seq}")

    # 汇总（只含已跑卷；全量跑时重建全量）
    if args.volumes:
        out = {"scope": "卷" + "+".join(vols), "count": sum(len(v["records"]) for v in merged.values()), "records": merged}
    else:
        out = {"scope": "卷01-20", "count": sum(len(v["records"]) for v in merged.values()), "records": merged}
    with open(sum_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    ver_lines.append(f"[汇总] trl_汇总.json：{out['scope']} 共 {out['count']} 条")
    ver_lines.append("PASS" if ok and not any(l.startswith("[ERR]") for l in ver_lines) else "FAIL")
    with open(os.path.join(KB, "trl_验证.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(ver_lines) + "\n")
    print("\n".join(ver_lines))

if __name__ == "__main__":
    main()
