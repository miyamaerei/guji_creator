import io, json, os, collections
os.chdir(r"E:\git\ToolBox\guji\mingshi\mingshi-zhiguanzhi")
off = json.load(io.open("_layers/structs/officials.json", encoding="utf-8"))
offs = off["officials"] if isinstance(off, dict) and "officials" in off else off.get("records", off)

print("=== 缺口1: org_binding ===")
c = collections.Counter(n.get("org_binding") for n in offs)
for k, v in c.most_common():
    print("  %-8s %d" % (k, v))

print()
print("=== 缺口1 样例（非「机构」者）===")
seen = set()
for n in offs:
    b = n.get("org_binding")
    if b != "机构" and b not in seen:
        seen.add(b)
        print("  %-8s %-18s org=%-8s reason=%s" % (n["id"], n["office"], n["org_id"], n.get("org_binding_reason", "")[:40]))

print()
print("=== 缺口2: 内阁 ===")
for n in offs:
    if "内阁" in (n.get("org_name") or "") or n["office"] in (
            "中极殿大学士", "建极殿大学士", "文华殿大学士", "武英殿大学士",
            "文渊阁大学士", "东阁大学士"):
        print("  %-9s %-14s org_id=%-10s org_name=%-8s grade=%s" % (
            n["id"], n["office"], n["org_id"], n.get("org_name"), n["grade"]))

print()
print("=== 缺口2: ORG 树 翰林院->内阁 ===")
for v in ("01", "02"):
    d = json.load(io.open("_layers/structs/structs_%s.json" % v, encoding="utf-8"))
    for r in d["records"]:
        if r.get("name") in ("翰林院", "内阁"):
            print("  %-9s %-8s parent=%-8s children=%s" % (
                r["id"], r["name"], r.get("parent"),
                [c["name"] for c in (r.get("children") or [])][:4]))

print()
print("=== 缺口3: EVO owner_orgs ===")
tot = own = multi = 0
for v in ("01", "02", "03", "04", "05"):
    try:
        d = json.load(io.open("_layers/structs/structs_%s.json" % v, encoding="utf-8"))
    except Exception:
        continue
    for r in d["records"]:
        if r.get("change_type"):
            tot += 1
            oo = r.get("owner_orgs") or []
            if oo:
                own += 1
            if len(oo) > 1:
                multi += 1
print("  EVO 共 %d, 有 owner %d (%.1f%%), 多 owner %d" % (tot, own, 100.0 * own / tot, multi))

print()
print("=== 缺口3 样例：吏部沿革（按 owner_orgs 反查）===")
for v in ("01",):
    d = json.load(io.open("_layers/structs/structs_%s.json" % v, encoding="utf-8"))
    for r in d["records"]:
        if r.get("change_type") and any(o["name"] == "吏部" for o in (r.get("owner_orgs") or [])):
            print("  %-9s %-14s %-8s %s" % (r["id"], r["change_type"], r["era"], r["content"][:60]))

print()
print("=== 缺口3 样例：六部共用沿革（多 owner）===")
d = json.load(io.open("_layers/structs/structs_01.json", encoding="utf-8"))
for r in d["records"]:
    if r.get("change_type") and len(r.get("owner_orgs") or []) > 1:
        print("  %-9s owners=%s | %s" % (
            r["id"], [o["name"] for o in r["owner_orgs"]], r["content"][:40]))
