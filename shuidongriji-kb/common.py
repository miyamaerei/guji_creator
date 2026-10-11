# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— 公共基座（common）
============================================
- 项目根目录自动定位（以本文件所在目录为根）
- 路径常量（_extract / sources / data / reports）
- 指纹库加载 / 源数据加载（AI 只写条号+解读，original 由打包器注入）
- norm 归一化规则（skill §2.4）
- 写入 JSON 的辅助（UTF-8、ensure_ascii=False、幂等重建）
"""
import io
import json
import os
import re
import sys

# ---- 路径 ----------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
EXTRACT_DIR = os.path.join(PROJECT_ROOT, "_extract")
VOLUMES_DIR = os.path.join(EXTRACT_DIR, "volumes")
ITEMS_DIR = os.path.join(EXTRACT_DIR, "items")
REGISTRY_PATH = os.path.join(EXTRACT_DIR, "_item_registry.json")
SOURCES_DIR = os.path.join(PROJECT_ROOT, "sources")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

INPUT_TXT = r"C:\Users\Administrator\Downloads\水东日记.txt"

# 卷名映射（阿拉伯卷号 → 原文卷名行）
CN_NUM = "一二三四五六七八九十"
VOL_CN = {str(i): "水东日记卷" + cn for i, cn in enumerate([
    "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
    "二十一", "二十二", "二十三", "二十四", "二十五", "二十六", "二十七", "二十八", "二十九", "三十",
    "三十一", "三十二", "三十三", "三十四", "三十五", "三十六", "三十七", "三十八"], start=1)}

VOL_CN_REV = {v: k for k, v in VOL_CN.items()}

# ---- norm 归一化（skill §2.4）--------------------------------------
# 规则：全角空格/制表符/连续半角空格折叠为单半角空格；去首尾空白；
#      缺字方括号【】注音保留原样（异体字按 norm 归一再检索比对）。
def normalize_text(s):
    """条目正文归一化：折叠空白、去首尾。异体/缺字保留原样。"""
    s = re.sub(r"[\u3000\t\u00a0 ]+", " ", s)
    return s.strip()


# ---- 指纹库 --------------------------------------------------------
def load_registry():
    """加载 _item_registry.json；缺失返回空 dict。"""
    if not os.path.exists(REGISTRY_PATH):
        return {}
    with io.open(REGISTRY_PATH, encoding="utf-8") as f:
        return json.load(f)


def registry_item(item_id):
    """按 item_id 取指纹库条目（original/norm）；缺失返回 None。"""
    reg = load_registry()
    return reg.get(item_id)


def iter_volumes():
    """按卷号升序遍历全部卷：返回 (卷号字符串, 卷名) 列表。"""
    vols = []
    for name in os.listdir(VOLUMES_DIR):
        m = re.match(r"^(\d{2})_.+\.xhtml$", name)
        if m:
            vols.append((m.group(1), name))
    vols.sort(key=lambda x: x[0])
    return vols


def list_item_ids(volume=None):
    """列出指纹库全部 item_id（可按卷过滤，卷号 '01'）。"""
    reg = load_registry()
    ids = list(reg.keys())
    if volume:
        ids = [i for i in ids if i.startswith(volume + "-")]
    ids.sort()
    return ids


# ---- 源数据加载（AI 判定逐条写入，sources/_<layer>_ai_NN.py）--------
def load_source(layer, volume):
    """动态加载 sources/_<layer>_ai_<NN>.py，返回其 DATA 列表或 None。

    layer: ent/appt/event/reg/lit/rel/nam/trl
    文件缺失（尚未执行该卷）→ 返回 None（由打包器/验证脚本报缺漏）。
    """
    import importlib.util

    path = os.path.join(SOURCES_DIR, f"_{layer}_ai_{volume}.py")
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location(f"_kg_src_{layer}_{volume}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    data = getattr(mod, "DATA", None)
    if data is None:
        raise ValueError(f"源数据 {path} 缺少 DATA 变量")
    return data


# ---- JSON 辅助 -----------------------------------------------------
def load_json(path):
    """读取 JSON；文件缺失返回 None。"""
    if not os.path.exists(path):
        return None
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    """幂等写入：UTF-8、ensure_ascii=False、indent=2、末尾换行。"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def write_text(path, text):
    """幂等写入 UTF-8 文本。"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def read_text(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


# ---- 通用层打包骨架（build_appt/event/reg/lit/rel/nam/trl 共用）----
def layer_build(layer, volumes, key_fields, enum_checker, out_dir,
                id_field="id", verbose=True):
    """遍历卷跑一层打包器。

    layer:      appt/event/reg/lit/rel/nam/trl
    key_fields: 每条记录必填字段列表
    enum_checker: 函数(rec, issues, item_id) 做枚举校验（就地 append 问题）
    out_dir:    data/<layer> 输出目录
    id_field:   主键字段名（各层不同：appointment_id/event_id/...）
    返回 issues 列表。
    """
    import re as _re

    os.makedirs(out_dir, exist_ok=True)
    reg = load_registry()
    issues = []
    all_records = []

    vols = iter_volumes()
    if volumes:
        vols = [v for v in vols if v[0] in volumes]

    for vol_no, _vol_file in vols:
        data = load_source(layer, vol_no)
        if data is None:
            msg = f"卷 {vol_no}：缺 {layer} 源数据 sources/_{layer}_ai_{vol_no}.py"
            issues.append(msg)
            if verbose:
                print("[缺漏]", msg)
            continue
        records = data if isinstance(data, list) else data.get("records", [])
        vol_out = {"volume": vol_no, "records": []}
        seen_ids = set()
        for rec in records:
            item_id = rec.get("item_id")
            if not _re.match(r"^\d{2}-\d{3}$", str(item_id or "")):
                issues.append(f"卷 {vol_no}：非法 item_id {item_id!r}")
                continue
            item = reg.get(item_id)
            if item is None:
                issues.append(f"卷 {vol_no} {item_id}：不在指纹库")
                continue
            for kf in key_fields:
                if rec.get(kf) in (None, ""):
                    issues.append(f"卷 {vol_no} {item_id}：缺必填字段 {kf}")
            rid = rec.get(id_field)
            if rid in seen_ids:
                issues.append(f"卷 {vol_no} {item_id}：{id_field} 重复 {rid!r}")
            if rid:
                seen_ids.add(rid)
            enum_checker(rec, issues, item_id)
            out_rec = dict(rec)
            out_rec["original"] = item["original"]
            out_rec["norm"] = item["norm"]
            vol_out["records"].append(out_rec)
            all_records.append(out_rec)
        write_json(os.path.join(out_dir, f"{layer}_{vol_no}.json"), vol_out)
        if verbose:
            print(f"卷 {vol_no}: {len(vol_out['records'])} 条 {layer} 记录")

    summary = {
        "layer": layer,
        "record_count": len(all_records),
        "volumes_covered": sorted({r["item_id"][:2] for r in all_records}),
    }
    write_json(os.path.join(out_dir, f"{layer}_summary.json"), summary)
    return issues


if __name__ == "__main__":
    print("PROJECT_ROOT:", PROJECT_ROOT)
    print("VOL_CN 卷数:", len(VOL_CN))
    print("归一化测试:", normalize_text("　杨善　　　萧维祯　　马昻　") == "杨善 萧维祯 马昻")
