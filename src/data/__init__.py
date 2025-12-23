"""数据处理包"""

from .loaders import load_data, load_multiple, load_excel_to_polars, load_csv_to_polars

__all__ = [
    "load_data",
    "load_multiple",
    "load_excel_to_polars",
    "load_csv_to_polars",
]
