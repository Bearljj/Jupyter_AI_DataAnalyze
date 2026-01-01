"""
📊 数据分析标准模版 (v3.0 - 物理隔离版)
用法：复制此文件并重命名，修改数据路径和业务逻辑即可。
"""

import polars as pl
import plotly.express as px
import panel as pn
from IPython.display import HTML, display

from src.session import DataSession
from src.dashboard import PanelDashboardBuilder
from src.utils import print_markdown_table

# ========================================
# 1. 环境初始化
# ========================================
def init_env():
    # 移除 Jupyter 宽度限制
    display(HTML("<style>.jp-Notebook { --jp-notebook-max-width: 100% !important; }</style>"))
    # 初始化 Panel
    pn.extension('plotly', sizing_mode='stretch_width')
    print("✅ 环境初始化完成")

# ========================================
# 2. 核心分析函数 (AI 逻辑区)
# ========================================
def build_analysis(df: pl.DataFrame, dimensions: list, title: str):
    # 创建仪表盘容器
    dashboard = PanelDashboardBuilder.from_data(
        df, 
        dimensions=dimensions, 
        title=title
    )

    @pn.depends(*dashboard.widgets.values())
    def update_plot(*args):
        # --- [A] 物理隔离获取参数 ---
        # 只获取业务过滤器的值（已自动排除聚合维度等系统控件）
        filters = dashboard.data_values
        # 获取当前的动态聚合轴
        agg_axis = dashboard.widgets['_aggregation_dimension'].value
        
        # --- [B] 动态数据过滤 ---
        tmp_df = df
        for col, val in filters.items():
            if isinstance(val, list):
                if '全选' not in val:
                    tmp_df = tmp_df.filter(pl.col(col).is_in(val))
            elif val != '全选':
                tmp_df = tmp_df.filter(pl.col(col) == val)
        
        # --- [C] 业务聚合逻辑 ---
        # 示例：计算总额和计数
        result = (
            tmp_df.group_by(agg_axis)
            .agg([
                pl.col('总保费').sum().alias('指标总额'), # 替换为实际列名
                pl.len().alias('单数')
            ])
            .sort('指标总额', descending=True)
            .head(15)
        )
        
        # --- [D] 可视化输出 ---
        fig = px.bar(
            result.to_pandas(), 
            x=agg_axis, 
            y='指标总额', 
            title=f"按 {agg_axis} 统计分析"
        )
        fig.update_layout(autosize=True, height=500)
        
        # 打印表格（Jupyter 中可见）
        print_markdown_table(result)
        
        return fig

    # 绑定并返回布局
    dashboard.set_update_function(update_plot)
    return dashboard

# ========================================
# 3. 执行入口
# ========================================
if __name__ == "__main__":
    init_env()
    
    # 加载数据
    session = DataSession()
    session.load("alldata", alias="df") # 修改为你的文件名
    
    # 启动分析
    # 这里的维度和标题可以根据需求动态修改
    app = build_analysis(
        df=session.get_data("df"),
        dimensions=['业务年度', '业务险种', '机构名称'],
        title="测试分析仪表盘"
    )
    
    # 在 Jupyter 中显示
    app.show()
