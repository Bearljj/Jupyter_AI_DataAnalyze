"""Polars DataFrame Markdown 输出增强

自动将 Polars DataFrame 在 Jupyter 中以 Markdown 表格格式显示
"""

import polars as pl
from IPython.display import Markdown, display
from typing import Optional


def df_to_markdown(
    df: pl.DataFrame, 
    max_rows: int = 100,
    index: bool = False
) -> Markdown:
    """
    将 Polars DataFrame 转换为 Markdown 表格并显示
    
    Args:
        df: Polars DataFrame
        max_rows: 最大显示行数
        index: 是否显示索引
        
    Returns:
        IPython Markdown 对象
        
    Examples:
        >>> result = df.group_by('category').agg(pl.col('sales').sum())
        >>> df_to_markdown(result)
    """
    # 限制行数
    if df.height > max_rows:
        display_df = df.head(max_rows)
        note = f"\n\n*注：仅显示前 {max_rows} 行，共 {df.height:,} 行*"
    else:
        display_df = df
        note = ""
    
    # 转换为 pandas 然后生成 Markdown
    pandas_df = display_df.to_pandas()
    markdown_table = pandas_df.to_markdown(index=index)
    
    return Markdown(markdown_table + note)


def enable_polars_markdown_display():
    """
    启用 Polars DataFrame 的 Markdown 表格自动显示
    
    在 Jupyter Notebook 中调用此函数后，所有 Polars DataFrame 
    将自动以 Markdown 表格格式显示
    
    Examples:
        >>> from src.utils.polars_display import enable_polars_markdown_display
        >>> enable_polars_markdown_display()
        >>> 
        >>> # 现在所有 DataFrame 输出都是 Markdown 格式
        >>> df.head()  
    """
    def _polars_to_html_(df_self, max_rows=100):
        """自定义 Polars DataFrame 的 HTML 表示"""
        # 生成 Markdown
        pandas_df = df_self.head(max_rows).to_pandas()
        markdown = pandas_df.to_markdown(index=False)
        
        # 转换为 HTML (Jupyter 会自动渲染)
        html_table = pandas_df.to_html(index=False, border=1, classes='dataframe')
        
        if df_self.height > max_rows:
            html_table += f'<p style="color: gray; font-size:0.9em;"><em>仅显示前 {max_rows} 行，共 {df_self.height:,} 行</em></p>'
            
        return html_table
    
    # Monkey patch Polars DataFrame
    pl.DataFrame._repr_html_ = _polars_to_html_
    
    print("✅ Polars Markdown 显示已启用")
    print("💡 现在所有 DataFrame 将以表格格式自动显示")


def print_markdown_table(df: pl.DataFrame, max_rows: int = 100):
    """
    打印 DataFrame 为 Markdown 表格（适用于 AI 生成的代码）
    
    Args:
        df: Polars DataFrame
        max_rows: 最大显示行数
        
    Examples:
        >>> # AI 可以生成这样的代码:
        >>> result = df.group_by('product').agg(pl.col('sales').sum())
        >>> print_markdown_table(result)
    """
    display(df_to_markdown(df, max_rows=max_rows))
