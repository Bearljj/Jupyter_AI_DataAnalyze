"""
Jupyter AI DataAnalyze - AI-Assisted Data Analysis Framework

主要模块：
- session: 数据会话管理
- data: 数据加载和处理
- dashboard: 交互式仪表盘
- catalog: 数据目录系统
- visualization: 可视化工具
- analysis: 分析工具
- reporting: 报告生成
"""

__version__ = "1.0.0"

from .session import DataSession
from .data import load_data, load_multiple

__all__ = [
    "DataSession",
    "load_data",
    "load_multiple",
]
