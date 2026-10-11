# -*- coding: utf-8 -*-
"""guji-kb-enum MCP 内核（P0 只读）。

零第三方依赖，只用标准库。分层：
    registry.py  书注册表（唯一需人工维护的配置）
    adapters.py  五种枚举载体的读取适配（工厂 Markdown / 四种 Python 后端 / 层产物）
    tools.py     只读工具实现
"""

__version__ = "0.1.0-p0"
