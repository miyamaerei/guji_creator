# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— 全量重跑入口（run_all）
==================================================
用法：
  python run_all.py                 # 全量：底座 → 实体主键 → 8 层 → 跨层索引 → 验证
  python run_all.py --volumes 01    # 仅重跑卷 01 对应层（幂等，不破坏其他卷）

管线顺序（skill §1.1 十要点：生成器可重跑、幂等、修复并入生成器）：
  build_base → build_ent_keys → build_appt/event/reg/lit/rel/nam/trl → build_kg_join → validate
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run(step, volumes):
    cmd = [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), step)]
    if volumes:
        cmd += ["--volumes"] + volumes
    print(f"\n######## {step} ########")
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"[失败] {step} 退出码 {r.returncode}")
        sys.exit(r.returncode)
    return r


def main():
    ap = argparse.ArgumentParser(description="《水东日记》知识工程全量重跑")
    ap.add_argument("--volumes", nargs="*", help="仅重跑指定卷（如 01 02）")
    args = ap.parse_args()

    run("build_base.py", args.volumes)
    run("build_ent_keys.py", args.volumes)
    for layer in ["appt", "event", "reg", "lit", "rel", "nam", "trl"]:
        run(f"build_{layer}.py", args.volumes)
    run("build_kg_join.py", args.volumes)

    # 验证（写 reports/验证缺漏清单.txt）
    print("\n######## validate.py ########")
    v = subprocess.run([sys.executable,
                        os.path.join(os.path.dirname(os.path.abspath(__file__)), "validate.py")]
                       + (["--volumes"] + args.volumes if args.volumes else []))
    if v.returncode != 0:
        print("\n[验证未通过] 见 reports/验证缺漏清单.txt")
        sys.exit(v.returncode)
    print("\n[全量重跑完成，验证通过（问题数 = 0）]")


if __name__ == "__main__":
    main()
