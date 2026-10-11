"""卷阅读模式标注（skill 执行流程第 2 步）

底座切好卷条之后、开始装填各层之前，先给每卷标一个"阅读侧重"：
该卷以论理为主、还是灾异、风土、人物、名物、世情、轶事？
标注结果决定各层的**装填优先级**（例如"名物优先"的卷先密集做 OBJ/CUS 层），
是后续逐卷装填的作业指导，也让交付报告里的"为什么这样读"有据可循。

产物：
    _build/volume_profile.json      机器可读（供 build_all / 报告引用）
    _deliver/卷阅读模式标注.md      人读（含每卷条目数、条号区间、层优先级建议）

用法：
    python build_volume_profile.py
"""

from __future__ import annotations

from _kg_pack_base import (
    BUILD_DIR,
    DELIVER_DIR,
    VOLUMES,
    VOLUME_MODE_HINT,
    banner,
    build_context,
    ensure_dirs,
    now_stamp,
    read_json,
    report_stats,
    write_json,
    write_text,
)

# 模式 → 层装填优先级（先做的层放前面）
MODE_PRIORITY: dict[str, list[str]] = {
    "均衡全层": ["ent", "event", "rel", "nam", "cit", "obj", "cus", "opn", "ming", "appt", "trl"],
    "论理优先": ["ent", "opn", "cit", "event", "rel", "obj", "cus", "ming", "appt", "nam", "trl"],
    "灾异优先": ["ent", "event", "obj", "cus", "opn", "cit", "rel", "ming", "appt", "nam", "trl"],
    "风土优先": ["ent", "cus", "obj", "event", "cit", "opn", "rel", "ming", "appt", "nam", "trl"],
    "人物优先": ["ent", "rel", "appt", "event", "nam", "cit", "opn", "ming", "obj", "cus", "trl"],
    "名物优先": ["ent", "obj", "cus", "cit", "event", "opn", "rel", "ming", "appt", "nam", "trl"],
    "世情优先": ["ent", "event", "cus", "rel", "opn", "obj", "cit", "ming", "appt", "nam", "trl"],
    "轶事优先": ["ent", "event", "rel", "ming", "opn", "obj", "cus", "cit", "appt", "nam", "trl"],
}

LAYER_LABEL = {
    "ent": "实体", "event": "事件", "rel": "关系", "nam": "名录", "cit": "引书",
    "obj": "名物", "cus": "风俗", "opn": "观点", "ming": "明代纪事",
    "appt": "职官", "trl": "翻译",
}


def build() -> dict:
    summary = read_json(BUILD_DIR / "volume_summary.json", default={}) or {}
    raw = summary.get("volumes") or []
    # volume_summary.json 的 volumes 是列表；也容忍 {卷号: {...}} 的字典形态
    by_volume = {item.get("volume"): item for item in raw} if isinstance(raw, list) else dict(raw)
    rows: list[dict] = []
    for volume, name in VOLUMES:
        info = by_volume.get(volume) or {}
        mode = info.get("mode_hint") or VOLUME_MODE_HINT.get(volume, "均衡全层")
        # mode_hint 可能是「论理优先/灾异优先」这类复合标注：取首个作为主模式，
        # 层优先级按主模式排，复合信息保留在 mode_secondary 里供人工参考
        parts = [p.strip() for p in str(mode).split("/") if p.strip()]
        primary = parts[0] if parts else "均衡全层"
        rows.append({
            "volume": volume,
            "name": name,
            "count": info.get("count"),
            "item_range": info.get("item_range"),
            "mode_hint": mode,
            "mode_primary": primary,
            "mode_secondary": parts[1:],
            "layer_priority": MODE_PRIORITY.get(primary, MODE_PRIORITY["均衡全层"]),
            "note": info.get("note", ""),
        })
    report = {
        "generated_at": now_stamp(),
        "base_ready": bool(by_volume),
        "volume_count": len(rows),
        "volumes": rows,
    }
    return report


def render_markdown(report: dict) -> str:
    lines = [
        "# 《五杂俎》卷阅读模式标注",
        "",
        f"- 生成时间：{report['generated_at']}",
        f"- 底座就绪：{'是' if report['base_ready'] else '否（请先跑 build_base.py）'}",
        "",
        "> 阅读模式决定该卷各层的装填优先级；层优先级中靠前者先做、密度要求更高。",
        "",
        "| 卷 | 卷名 | 条目数 | 条号区间 | 阅读模式 | 层装填优先级 |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for row in report["volumes"]:
        rng = row.get("item_range") or []
        rng_text = f"{rng[0]} ~ {rng[1]}" if len(rng) == 2 else "—"
        priority = " > ".join(LAYER_LABEL.get(x, x) for x in row["layer_priority"])
        lines.append(
            f"| {row['volume']} | {row['name']} | {row.get('count') or 0} | {rng_text} "
            f"| {row['mode_hint']} | {priority} |"
        )
    lines += [
        "",
        "## 模式说明",
        "",
        "| 模式 | 判据 | 装填侧重 |",
        "| --- | --- | --- |",
        "| 均衡全层 | 序、总论性质 | 各层均匀覆盖，铺词汇表 |",
        "| 论理优先 | 以天人、象数、义理之辨立论 | 观点层与引书层要密，事件层次之 |",
        "| 灾异优先 | 灾祥、星变、疾疫、物异 | 事件层要密（灾异类） |",
        "| 风土优先 | 山川、方物、节令、土俗 | 风俗层与名物层要密 |",
        "| 人物优先 | 以人物行迹、品评为主 | 关系层与职官层要密 |",
        "| 名物优先 | 器用、草木、鸟兽、饮食 | 名物层要密，风俗层次之 |",
        "| 世情优先 | 世事人情、官场市井 | 事件层与风俗层要密 |",
        "| 轶事优先 | 谐谈、异闻、琐记 | 事件层（轶事类）与明代纪事层 |",
        "",
        "> 翻译层（trl）各卷口径一致：全条覆盖、余光中风格基准，不因卷而变。",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    args, volumes = build_context("卷阅读模式标注 build_volume_profile")
    banner("卷阅读模式标注 build_volume_profile")
    ensure_dirs()
    report = build()
    targets = [r for r in report["volumes"] if not volumes or r["volume"] in volumes]
    report["volumes"] = targets
    write_json(BUILD_DIR / "volume_profile.json", report)
    write_text(DELIVER_DIR / "卷阅读模式标注.md", render_markdown(report))
    report_stats("卷模式标注", {
        "标注卷数": len(targets),
        "底座就绪": report["base_ready"],
        "产物": ["_build/volume_profile.json", "_deliver/卷阅读模式标注.md"],
    })


if __name__ == "__main__":
    main()
