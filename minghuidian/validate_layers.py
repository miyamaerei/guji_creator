# -*- coding: utf-8 -*-
"""校验器：交叉引用 + 密度检测"""
import os, sys, json
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import _kg_enums as enums


def main():
    with open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8") as f:
        reg = json.load(f)

    print("=" * 60)
    print("《明会典》校验报告")
    print("=" * 60)
    print(f"底座总条目: {len(reg)}")

    # 按卷统计
    vol_items = defaultdict(list)
    for iid in reg:
        vol = int(iid.split('-')[0])
        vol_items[vol].append(iid)

    # 各层数据
    layers = {}
    for layer in ["ents", "rules", "nams", "cits"]:
        p = os.path.join(ROOT, "_layers", layer + ".json")
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                layers[layer] = json.load(f)
        else:
            layers[layer] = []

    # ===== 1. 交叉引用校验 =====
    print("\n--- 1. 交叉引用校验 ---")
    errs = []
    covered = set()
    for layer, items in layers.items():
        # 跳过虚拟节点（item_id 以 VIRT- 开头）
        real_items = [r for r in items if not r.get("item_id", "").startswith("VIRT-")]
        missing = [r["item_id"] for r in real_items if r["item_id"] not in reg]
        for r in items:
            covered.add(r["item_id"])
        print(f"  {layer:6s}: {len(items):4d} 条记录, 覆盖 {len(set(r['item_id'] for r in real_items)):4d} 条目")
        if missing:
            errs.append(f"{layer}: {len(missing)} 条引用了不存在的 item_id")

    # ===== 1.5 staff_config 验证（人员配置条目） =====
    print("\n--- 1.5 人员配置（staff_config）验证 ---")
    staff_items = [r for r in layers["nams"] if "staff_config" in r]
    print(f"  含 staff_config 的 NAM: {len(staff_items)} 条")
    for r in staff_items:
        for sc in r["staff_config"]:
            if sc["role"] not in enums.STAFF_ROLE:
                errs.append(f"{r['id']}: staff role 未注册: {sc['role']}")
    staff_err = [e for e in errs if "staff role" in e]
    if staff_err:
        print(f"  ✗ {len(staff_err)} 个 staff_role 枚举错误")
    else:
        print(f"  ✓ staff_role 枚举全命中")

    uncovered = sorted(set(reg.keys()) - covered)
    print(f"\n未被任何层覆盖: {len(uncovered)} / {len(reg)} ({len(uncovered)*100//len(reg)}%)")

    # ===== 2. 密度检测：按卷组 =====
    print("\n--- 2. 卷组密度 ---")
    groups = [
        ("G0 宗人府", [1]),
        ("G1 吏部", list(range(2, 14))),
        ("G2 户部", list(range(14, 42))),
        ("G3 礼部", list(range(42, 106))),
        ("G4 兵部", list(range(106, 130))),
        ("G5 刑部", list(range(130, 144))),
        ("G6 工部", list(range(144, 164))),
        ("G7 诸文职", list(range(164, 179))),
        ("G8 诸武职", [179, 180]),
    ]
    for gname, vols in groups:
        g_items = []
        for v in vols:
            g_items.extend(vol_items.get(v, []))
        g_covered = [i for i in g_items if i in covered]
        pct = len(g_covered)*100//len(g_items) if g_items else 0
        bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
        print(f"  {gname:12s}: {len(g_items):5d} 条, 已覆盖 {len(g_covered):5d} ({pct:3d}%) {bar}")

    # ===== 3. 实体类型分布 =====
    print("\n--- 3. 实体类型分布（ents）---")
    ent_types = Counter(r.get("type", "unknown") for r in layers["ents"])
    for t, c in ent_types.most_common():
        print(f"  {t:14s}: {c:4d}")

    # ===== 4. 规则类型分布 =====
    print("\n--- 4. 规则类型分布（rules）---")
    rul_types = Counter(r.get("type", "unknown") for r in layers["rules"])
    for t, c in rul_types.most_common():
        print(f"  {t:14s}: {c:4d}")

    # ===== 5. 文书标记分布 =====
    print("\n--- 5. 文书标记分布（source_marker）---")
    markers = Counter(r.get("source_marker", "unknown") for r in layers["rules"])
    for t, c in markers.most_common():
        print(f"  {t:14s}: {c:4d}")

    # ===== 6. 未覆盖条目按卷分布 =====
    print("\n--- 6. 未覆盖条目按卷（前20）---")
    unc_vol = Counter(int(iid.split('-')[0]) for iid in uncovered)
    for v, c in sorted(unc_vol.items())[:20]:
        print(f"  卷{v}: {c} 条")

    # ===== 7. 父子节点验证 =====
    print("\n--- 7. 父子节点验证（parent_id）---")
    ents = layers["ents"]
    ent_ids = {e.get("text", ""): e for e in ents}
    has_parent = [e for e in ents if e.get("parent_id")]
    orphan = [e for e in ents if not e.get("parent_id")]

    print(f"  实体总数: {len(ents)}")
    print(f"  有 parent_id 的: {len(has_parent)}")
    print(f"  无 parent_id（根节点/孤儿）: {len(orphan)}")

    # 检查 parent_id 引用是否合法
    parent_errs = []
    for e in has_parent:
        pid = e["parent_id"]
        if pid not in ent_ids:
            parent_errs.append(f"{e.get('text','?')}: parent_id '{pid}' 不存在")

    if parent_errs:
        print(f"  ✗ {len(parent_errs)} 个父节点引用错误")
        for pe in parent_errs[:5]:
            print(f"    - {pe}")
    else:
        print(f"  ✓ parent_id 引用全部合法")

    # 检查层级深度（简单统计）
    if has_parent:
        depth_ok = sum(1 for e in has_parent if e.get("parent_id") in ent_ids)
        print(f"  层级可解析: {depth_ok}/{len(has_parent)}")

    if errs:
        print(f"\nFAIL: {len(errs)} 个错误")
        for e in errs:
            print(f"  ✗ {e}")
        return 1
    print("\nPASS: 交叉引用合法")
    return 0


if __name__ == "__main__":
    sys.exit(main())
