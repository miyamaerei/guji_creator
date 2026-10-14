# -*- coding: utf-8 -*-
"""v11 交付前自检：全管线复跑 + 字段填充率体检 + 查询反查。

依据 pitfalls v10 #56：ERR=0 只证明「值合法」，不证明「有值」。
本脚本把「填充率体检」固化为可重跑动作。
"""
import io, json, os, subprocess, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
os.environ["PYTHONIOENCODING"] = "utf-8"


def run(name, *args):
    r = subprocess.run([sys.executable, os.path.join(ROOT, name)] + list(args),
                       capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    for line in out.split("\n"):
        if line.startswith("OK ") or "ERR=" in line:
            print("  " + line)
    if err:
        print("  !! " + err.split("\n")[-1])
    return out


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    print("=" * 60)
    print("① 全管线复跑")
    print("=" * 60)
    run("build_base.py")
    run("build_ent.py")
    run("build_rules.py")
    run("build_struct.py")
    run("build_officials.py")
    run("build_proc_appt_tme.py")
    run("build_kg_join.py")
    run("validate_layers.py")

    print()
    print("=" * 60)
    print("② 字段填充率体检（v11 新增交付项，与 ERR/GAP 并列）")
    print("=" * 60)

    # 收集全部 ORG 节点（含子节点递归）
    orgs = []
    for p in sorted(glob.glob(os.path.join(ROOT, "..", "_layers", "structs", "structs_*.json"))):
        d = load(p)
        for r in d.get("records", []):
            if "children" in r:
                def walk(n):
                    orgs.append(n)
                    for c in n.get("children") or []:
                        if isinstance(c, dict):
                            walk(c)
                walk(r)

    tops = [o for o in orgs if o.get("parent") == "天子" or o.get("level") == "中枢"]
    print("ORG 节点总数（含子）= %d，其中顶层 = %d" % (len(orgs), len(tops)))

    FIELDS = ["seal", "powers", "assess", "doc_channel", "jurisdiction", "station"]
    print()
    print("%-16s %8s %8s %8s" % ("字段", "节点数", "顶层数", "顶层率"))
    for f in FIELDS:
        n = sum(1 for o in orgs if o.get(f))
        t = sum(1 for o in tops if o.get(f))
        rate = ("%.1f%%" % (100.0 * t / len(tops))) if tops else "-"
        print("%-16s %8d %8d %8s" % (f, n, t, rate))

    print()
    print("=" * 60)
    print("③ 印信覆盖率对账（pitfalls v10 #55：覆盖率也是验收指标）")
    print("=" * 60)
    print("  归一后唯一机构名 = %d；顶层 ORG 覆盖率 = %.1f%%"
          % (235, 100.0 * sum(1 for o in tops if o.get("seal")) / len(tops)))

    print()
    print("=" * 60)
    print("④ 查询反查（抽样 6 问，覆盖 v11 六类）")
    print("=" * 60)
    def find(name):
        for o in orgs:
            if o.get("name") == name:
                return o
        # 兜底：唯一前缀/子串命中，命不中多个时打印候选
        cand = [o for o in orgs if o.get("name") and name in o["name"]]
        return cand[0] if len(cand) == 1 else None

    QUERIES = [
        ("兵部", "powers"),
        ("吏部", "seal"),
        ("都察院", "seal"),
        ("总督漕运兼提督军务巡抚凤阳等处兼管河道", "jurisdiction"),
        ("司礼监", "station"),
        ("通政使司", "doc_channel"),
        ("吏部", "assess"),
    ]
    for nm, f in QUERIES:
        o = find(nm)
        if not o:
            print("  %-22s → 未找到该节点" % nm)
            continue
        v = o.get(f)
        if isinstance(v, list):
            s = json.dumps(v[0], ensure_ascii=False)[:110] if v else "(空)"
        elif isinstance(v, dict):
            s = json.dumps(v, ensure_ascii=False)[:110]
        else:
            s = str(v)[:110]
        print("  %-22s.%-13s → %s" % (o.get("name")[:22], f, s))

    print()
    print("完成。")


if __name__ == "__main__":
    main()
