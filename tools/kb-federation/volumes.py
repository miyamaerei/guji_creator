"""volumes.py —— 稀疏表填充（二）：volumes 目录表

背景（见 docs/联邦库原表增量与稀疏诊断.md §2.6）：schema 声明了 volumes 目录表作「扩展点」，
但实际 0 行；卷信息散在 records.volume / items.volume 自由文本（'01'..'12' 裸数字）。
本模块从 records 派生填充 volumes：每 (book_id, volume) 取该卷内记录最多的层为
dominant_type、次多为 secondary_type（reading_mode/basis 暂留 NULL，待后续阅读模式归纳）。

幂等：先 DELETE 再 INSERT。卷维在数仓侧已能由 records 派生，本填充让联邦库侧也有规范目录。

用法：
  python federation.py volumes
零第三方依赖。
"""

import os
import sqlite3
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))


def populate_volumes(con):
    """从 records 派生填充 volumes 目录表。"""
    con.execute("DELETE FROM volumes")
    rows = []
    # 每 (book, volume) 统计各 layer_key 出现次数
    stats = {}
    for book, vol, layer in con.execute(
        "SELECT book_id, volume, layer_key FROM records "
        "WHERE volume IS NOT NULL AND volume <> ''"
    ):
        stats.setdefault((book, vol), Counter())[layer] += 1
    for (book, vol), cnt in stats.items():
        most = cnt.most_common(2)
        dominant = most[0][0] if most else None
        secondary = most[1][0] if len(most) > 1 else None
        rows.append((book, vol, dominant, secondary, None, None))
    con.executemany(
        "INSERT OR REPLACE INTO volumes"
        "(book_id,volume,dominant_type,secondary_type,reading_mode,basis) "
        "VALUES(?,?,?,?,?,?)",
        rows,
    )
    con.commit()
    return {"volumes": len(rows)}


if __name__ == "__main__":
    con = sqlite3.connect(os.path.join(HERE, "kb.sqlite"))
    con.execute("PRAGMA foreign_keys=OFF")
    out = populate_volumes(con)
    print("volumes 填充：%d 行" % out["volumes"])
    con.close()
