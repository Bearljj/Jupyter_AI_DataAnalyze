# ================================================================
# 📋 使用真实数据的仪表盘示例
# ================================================================
# 这个单元格展示如何使用你的真实数据创建交互式仪表盘
# 替代了原来的硬编码示例数据

from src.dashboard import DashboardBuilder
import polars as pl
import plotly.express as px

# 从已加载的数据中提取真实的选项值
# 假设你的数据已经通过 session.load() 加载为 df_df

# 提取真实的产品列表（根据你的数据字段调整）
if 'df_df' in globals():
    # 方法1: 如果你的数据有"产品"相关字段
    # 根据实际字段名调整，例如：'业务险种', '产品类型' 等
    product_column = '业务险种'  # 👈 根据实际字段名修改
    
    if product_column in df_df.columns:
        products_real = df_df.select(pl.col(product_column).unique()).to_series().to_list()
        products_real = [p for p in products_real if p is not None][:20]  # 最多20个，避免太多
    else:
        # 如果没有产品字段，使用业务年度作为示例
        products_real = df_df.select(pl.col('业务年度').unique()).to_series().to_list()
        product_column = '业务年度'
    
    # 提取真实的地区列表（如果有）
    region_column = '机构名称'  # 👈 根据实际字段名修改
    if region_column in df_df.columns:
        regions_real = df_df.select(pl.col(region_column).unique()).to_series().to_list()
        regions_real = [r for r in regions_real if r is not None][:10]  # 最多10个
    else:
        regions_real = ['全部']
    
    print(f"✅ 已提取真实数据选项：")
    print(f"   - {product_column}: {len(products_real)} 个选项")
    print(f"   - {region_column}: {len(regions_real)} 个选项")
    print()
    
    # 创建基于真实数据的仪表盘
    dashboard_real = DashboardBuilder("基于真实数据的分析仪表盘")
    
    # 添加控件（使用真实数据的值）
    dashboard_real.add_dropdown(
        name='filter_value',
        label=f'选择{product_column}',
        options=products_real,
        default=products_real[0]
    ).add_multiselect(
        name='regions',
        label=f'选择{region_column}',
        options=regions_real,
        default=regions_real[:3] if len(regions_real) >= 3 else regions_real
    )
    
    # 定义更新函数（使用真实数据）
    def update_real_dashboard(controls):
        selected_value = controls['filter_value']
        selected_regions = controls['regions']
        
        # 过滤数据
        filtered = df_df.filter(pl.col(product_column) == selected_value)
        
        if region_column in df_df.columns and '全部' not in selected_regions:
            filtered = filtered.filter(pl.col(region_column).is_in(selected_regions))
        
        # 汇总数据
        summary = filtered.group_by('业务年度').agg([
            pl.col('总保费').sum().alias('总保费'),
            pl.col('自留保费').sum().alias('自留保费'),
            pl.len().alias('保单数')
        ]).sort('业务年度')
        
        # 创建图表
        fig = px.bar(
            summary.to_pandas(),
            x='业务年度',
            y='总保费',
            title=f'{selected_value} - 按年度保费分析',
            labels={'总保费': '保费金额（元）', '业务年度': '年度'},
            text='总保费'
        )
        
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(height=500, showlegend=True)
        
        return fig
    
    # 绑定更新函数
    dashboard_real.set_update_function(update_real_dashboard)
    
    print("📊 仪表盘已准备好！运行下一个单元格启动仪表盘。")
    
else:
    print("❌ 错误：未找到数据 df_df")
    print("💡 请先运行前面的单元格加载数据：session.load('alldata', alias='df')")
