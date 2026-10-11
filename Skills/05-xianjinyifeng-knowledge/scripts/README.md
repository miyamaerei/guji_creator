# scripts/（执行期脚本目录）

本目录用于存放《先进遗风》知识工程执行期的打包器与验证脚本。骨架阶段为空，执行期按本实例 SKILL.md §10（管线与验证）在此生成，命名规范如下：

- **源数据文件**（AI 逐条判定输入）：`_ent_ai_NN.py` / `_appt_ai_NN.py` / `_rel_ai_NN.py` / `_event_ai_NN.py` / `_opn_ai_NN.py` / `_trl_ai_NN.py`（NN = 卷号）
- **打包器**（build_ 前缀、可重跑、幂等）：`annotate` / `build_ent_keys` / `build_appt` / `build_rel` / `build_event` / `build_opn` / `build_trl` / `build_kg_join`
- **公共模块**：`_kg_pack_base.py`（基座，含业务 ID 段位分配与 original 注入）、`_kg_enums.py`（枚举单点文件，registerVersion 模式）
- **验证脚本**：写文件输出，不依赖 stdout；区分结构性错误 ERR 与执行缺口 GAP

执行基准：见 `../SKILL.md` §9.5 治理组件与 §10 管线验证；枚举基准继承工厂 `../../book-knowledge-factory/references/enum-library.md`。