"""配置管理模块"""

from pathlib import Path
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()


class Config:
    """全局配置"""
    
    # 项目根目录
    ROOT_DIR = Path(__file__).parent.parent
    
    # 数据路径
    RAW_DATA_PATH = ROOT_DIR / os.getenv("RAW_DATA_PATH", "data/raw")
    PROCESSED_DATA_PATH = ROOT_DIR / os.getenv("PROCESSED_DATA_PATH", "data/processed")
    CACHE_PATH = ROOT_DIR / "data/cache"
    OUTPUT_PATH = ROOT_DIR / os.getenv("OUTPUT_PATH", "data/outputs")
    CATALOG_PATH = ROOT_DIR / "data/catalog"
    
    # Polars 配置
    POLARS_MAX_THREADS = int(os.getenv("POLARS_MAX_THREADS", "8"))
    POLARS_STRING_CACHE = os.getenv("POLARS_STRING_CACHE", "true").lower() == "true"
    
    # 缓存配置
    ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))
    
    # Jupyter 配置
    JUPYTER_PORT = int(os.getenv("JUPYTER_PORT", "8888"))
    
    # 项目信息
    PROJECT_NAME = os.getenv("PROJECT_NAME", "数据分析项目")
    ANALYST_NAME = os.getenv("ANALYST_NAME", "分析师")
    
    @classmethod
    def ensure_directories(cls):
        """确保所有必要的目录存在"""
        for path in [
            cls.RAW_DATA_PATH,
            cls.PROCESSED_DATA_PATH,
            cls.CACHE_PATH,
            cls.OUTPUT_PATH,
            cls.OUTPUT_PATH / "reports",
            cls.OUTPUT_PATH / "charts",
            cls.OUTPUT_PATH / "exports",
            cls.CATALOG_PATH,
            cls.CATALOG_PATH / "profiles",
        ]:
            path.mkdir(parents=True, exist_ok=True)


# 初始化时确保目录存在
Config.ensure_directories()

# 配置 Polars
import polars as pl

pl.Config.set_tbl_rows(20)
pl.Config.set_tbl_cols(20)

if Config.POLARS_STRING_CACHE:
    pl.enable_string_cache()
