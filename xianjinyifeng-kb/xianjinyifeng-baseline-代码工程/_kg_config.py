# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - 配置单点（_kg_config.py）

所有路径、卷映射、段容量、层注册等参数集中在此文件，打包器/验证脚本只从这里取参，
避免同类参数散落各脚本造成口径漂移（pitfalls.md #4/#24）。

数据目录约定（相对本文件父目录 SKILL 实例根，即 05-xianjinyifeng-knowledge/）：
    data/_extract/     分卷条目 TXT（格式 条N|正文）
    data/_item_registry.json  指纹库（key=NN-NNN, value={original, norm}）
    data/_src/         AI 源数据（_<layer>_ai_<NN>.py / .json）
    data/_layers/      层产物（*_<NN>.json 卷产物、*_all.json 全局聚合、kg_join.*）
    data/_validate/    验证输出（缺漏清单、枚举分布、pending 表、待核清单）
    data/_deliver/     交付打包目录
    scripts/samples/   源数据样例（AI 写源数据的参照模板）
"""

from __future__ import annotations

import os

# ---------------------------------------------------------------------------
# 路径（以本文件所在目录为锚点计算，换机/换目录无需改绝对路径）
# ---------------------------------------------------------------------------
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))  # .../scripts
INSTANCE_DIR = os.path.dirname(SCRIPTS_DIR)  # .../05-xianjinyifeng-knowledge
DATA_DIR = os.path.join(INSTANCE_DIR, "data")

SOURCE_FILE = os.path.join(
    INSTANCE_DIR, "assets", "sources", "先进遗风_全本.txt"
)  # 唯一权威来源
EXTRACT_DIR = os.path.join(DATA_DIR, "_extract")
REGISTRY_FILE = os.path.join(DATA_DIR, "_item_registry.json")
SRC_DIR = os.path.join(DATA_DIR, "_src")
LAYERS_DIR = os.path.join(DATA_DIR, "_layers")
VALIDATE_DIR = os.path.join(DATA_DIR, "_validate")
DELIVER_DIR = os.path.join(DATA_DIR, "_deliver")
SAMPLES_DIR = os.path.join(SCRIPTS_DIR, "samples")

# ---------------------------------------------------------------------------
# 卷映射（pitfalls.md #24：汉字卷名直接映射，不依赖文件读取顺序）
# ---------------------------------------------------------------------------
VOLUME_MAP = {
    "先进遗风卷上": "01",  # 卷上 = 01
    "先进遗风卷下": "02",  # 卷下 = 02
}
# 书名行/卷标记行之外的装饰分隔线（全行 = 开头），不入条目
SEPARATOR_PREFIX = "="

# ---------------------------------------------------------------------------
# 业务 ID 段位（pitfalls.md #13/#22：AI 源数据不手写业务 ID，打包器按段位分配）
#   ID = f"{prefix}{(volume - 1) * SEGMENT_CAPACITY + slot:03d}"
#   段容量 = 卷条数 × 单层最大扩展系数预留，本项目卷均约 50-58 条且单层记录数
#   远超条数（多实体/多任职/多事件），预留 500 段位（全卷 100 条 0 撞号实测）。
# ---------------------------------------------------------------------------
SEGMENT_CAPACITY = 500

# annotate 底座提取的卷-条数期望（实验分区，与 .dumate/试点_条目切分.txt 一致）
DEFAULT_EXPECT_ITEMS = "01:58,02:42"
EXPECT_TOTAL_ITEMS = 100

# ---------------------------------------------------------------------------
# 启用层注册（与 SKILL.md §0 锁定的六数据层一一对应）
#   id_prefix : 业务 ID 前缀（ID 命名空间唯一归属，禁止跨层占用）
#   src_key   : AI 源数据文件顶层键名（源数据键名 → 打包容器键 records 的映射，
#               pitfalls.md #23：打包器内建显式 SRC_KEY 映射表）
#   builder   : 对应打包器模块名（scripts/build_<builder>.py）
# ---------------------------------------------------------------------------
LAYERS = {
    "ent": {"id_prefix": "ENT-", "src_key": "annotations", "builder": "build_ent_keys"},
    "appt": {"id_prefix": "APPT-", "src_key": "appointments", "builder": "build_appt"},
    "rel": {"id_prefix": "REL-", "src_key": "relations", "builder": "build_rel"},
    "event": {"id_prefix": "XJF-E-", "src_key": "events", "builder": "build_event"},
    "opn": {"id_prefix": "OPN-", "src_key": "opns", "builder": "build_opn"},
    "trl": {"id_prefix": "TRL-", "src_key": "trls", "builder": "build_trl"},
}
LAYER_ORDER = ["ent", "appt", "rel", "event", "opn", "trl"]  # 构建与验证顺序

# 各层源数据文件的 AI 侧键名（用于生成源数据模板与加载；单键为 AI 顶层键名）
# 源数据单条记录内只写 条号(item_id) + 解读字段，不手写业务 ID、不手抄 original。

# ---------------------------------------------------------------------------
# 低置信阈值（V2 人工校验闭环：confidence < 该值自动入待核清单）
# ---------------------------------------------------------------------------
CONFIDENCE_WARN = 0.8


def ensure_dirs() -> None:
    """确保执行期数据目录存在（幂等，可反复调用）。"""
    for d in (EXTRACT_DIR, SRC_DIR, LAYERS_DIR, VALIDATE_DIR, DELIVER_DIR):
        os.makedirs(d, exist_ok=True)
