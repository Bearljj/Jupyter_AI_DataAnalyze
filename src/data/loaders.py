"""数据加载器模块"""

import polars as pl
from pathlib import Path
from typing import Union, List
from config import Config


def load_data(path: Union[str, Path], lazy: bool = False) -> pl.DataFrame:
    """
    加载数据文件
    
    自动识别文件格式：parquet, csv, excel
    
    Args:
        path: 文件路径（相对或绝对）
        lazy: 是否惰性加载（仅parquet支持）
    
    Returns:
        Polars DataFrame
    
    Examples:
        >>> df = load_data("data/processed/2024_01.parquet")
        >>> df = load_data("2024_01")  # 自动补全路径和扩展名
    """
    path = Path(path)
    
    # 如果是相对路径且不存在，尝试在 processed 目录查找
    if not path.is_absolute() and not path.exists():
        # 尝试多个可能的路径
        possible_paths = [
            Config.PROCESSED_DATA_PATH / path,
            Config.PROCESSED_DATA_PATH / f"{path}.parquet",
            Config.RAW_DATA_PATH / path,
        ]
        
        for p in possible_paths:
            if p.exists():
                path = p
                break
        else:
            raise FileNotFoundError(f"找不到数据文件: {path}")
    
    # 根据扩展名加载
    suffix = path.suffix.lower()
    
    if suffix == ".parquet":
        if lazy:
            return pl.scan_parquet(path)
        else:
            return pl.read_parquet(path)
    
    elif suffix == ".csv":
        return pl.read_csv(path)
    
    elif suffix in [".xlsx", ".xls"]:
        return pl.read_excel(path)
    
    else:
        raise ValueError(f"不支持的文件格式: {suffix}")


def load_multiple(
    pattern: str, 
    concat: bool = True,
    lazy: bool = False
) -> Union[pl.DataFrame, List[pl.DataFrame]]:
    """
    加载多个文件
    
    Args:
        pattern: 文件模式（如 "2024_*.parquet" 或 "data/processed/*.parquet"）
        concat: 是否合并为单个 DataFrame
        lazy: 是否惰性加载
    
    Returns:
        单个 DataFrame（如果 concat=True）或 DataFrame 列表
    
    Examples:
        >>> # 加载2024年所有数据并合并
        >>> df = load_multiple("2024_*.parquet")
        >>> 
        >>> # 加载但不合并
        >>> dfs = load_multiple("2024_*.parquet", concat=False)
    """
    pattern_path = Path(pattern)
    
    # 如果pattern不包含目录，默认在processed目录搜索
    if "/" not in pattern and "\\" not in pattern:
        search_path = Config.PROCESSED_DATA_PATH
        pattern_str = pattern
    else:
        search_path = pattern_path.parent
        pattern_str = pattern_path.name
    
    # 查找匹配的文件
    files = sorted(search_path.glob(pattern_str))
    
    if not files:
        raise FileNotFoundError(f"没有找到匹配的文件: {pattern}")
    
    print(f"找到 {len(files)} 个文件")
    
    # 加载所有文件
    dfs = [load_data(f, lazy=lazy) for f in files]
    
    if concat:
        if lazy:
            return pl.concat([pl.scan_parquet(f) for f in files])
        else:
            return pl.concat(dfs)
    else:
        return dfs


def load_excel_to_polars(path: Union[str, Path], **kwargs) -> pl.DataFrame:
    """
    加载 Excel 文件并转换为 Polars DataFrame
    
    Args:
        path: Excel 文件路径
        **kwargs: 传递给 pl.read_excel 的额外参数
    
    Returns:
        Polars DataFrame
    """
    return pl.read_excel(path, **kwargs)


def load_csv_to_polars(path: Union[str, Path], **kwargs) -> pl.DataFrame:
    """
    加载 CSV 文件并转换为 Polars DataFrame
    
    Args:
        path: CSV文件路径
        **kwargs: 传递给 pl.read_csv 的额外参数
    
    Returns:
        Polars DataFrame
    """
    return pl.read_csv(path, **kwargs)
