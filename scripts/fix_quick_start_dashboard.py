#!/usr/bin/env python3
"""
修复 quick_start.ipynb - 将示例数据替换为真实数据
"""
import json
import sys

NOTEBOOK_PATH = '/Users/harold/working/Jupyter_AI_DataAnalyze/notebooks/templates/quick_start.ipynb'

# 真实数据仪表盘代码
REAL_DASHBOARD_CODE = """# ================================================================
# 📊 创建基于真实数据的交互式仪表盘
# ================================================================

from src.dashboard import DashboardBuilder
import polars as pl
import plotly.express as px

# 检查是否有真实数据
if 'df_df' in globals():
    # 从真实数据中提取选项
    year_options = df_df.select(pl.col('业务年度').unique()).to_series().sort().to_list()
    
    # 创建仪表盘
    dashboard = DashboardBuilder("真实数据分析仪表盘")
    
    dashboard.add_dropdown(
        name='year',
        label='选择年度',
        options=year_options,
        default=year_options[-1]  # 默认最新年度
    )
    
    # 定义更新函数（使用真实数据）
    def update_dashboard(controls):
        year = controls['year']
        
        # 过滤真实数据
        filtered = df_df.filter(pl.col('业务年度') == year)
        
        # 按险种汇总 Top 10
        summary = filtered.group_by('业务险种').agg([
            pl.col('总保费').sum().alias('保费'),
            pl.col('总保额').sum().alias('保额'),
            pl.len().alias('保单数')
        ]).sort('保费', descending=True).head(10)
        
        # 创建图表
        fig = px.bar(
            summary.to_pandas(),
            x='业务险种',
            y='保费',
            title=f'{year}年 Top 10 险种保费分析',
            text='保费',
            hover_data=['保额', '保单数']
        )
        
        fig.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside'
        )
        fig.update_layout(height=500, showlegend=False)
        
        return fig
    
    # 绑定更新函数
    dashboard.set_update_function(update_dashboard)
    
    print("✅ 仪表盘已创建（基于真实数据）")
    print(f"📊 年度选项: {year_options}")
    
else:
    print("❌ 错误：未找到数据 df_df")
    print("💡 请先运行前面的单元格加载数据")
"""

BUILD_CODE = """# 启动仪表盘
if 'dashboard' in globals():
    dashboard.build()
    print("\\n🎉 仪表盘已启动！使用上方的控件进行交互分析")
else:
    print("❌ 请先运行上一个单元格创建仪表盘")
"""

def main():
    # 读取 notebook
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    modified = False
    
    # 修改仪表盘创建 cell
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source_text = ''.join(cell.get('source', []))
            
            # 找到创建仪表盘的 cell (包含 DashboardBuilder 和 products)
            if 'DashboardBuilder' in source_text and ('products' in source_text or 'regions' in source_text):
                print(f"Found dashboard cell at index {i}, updating...")
                cell['source'] = REAL_DASHBOARD_CODE.split('\n')
                # 确保每行都以换行符结尾
                cell['source'] = [line + '\n' if not line.endswith('\n') else line for line in cell['source']]
                modified = True
            
            # 找到 build() cell
            elif 'dashboard.build()' in source_text and len(source_text) < 200:  # 简单的 build cell
                print(f"Found build cell at index {i}, updating...")
                cell['source'] = BUILD_CODE.split('\n')
                cell['source'] = [line + '\n' if not line.endswith('\n') else line for line in cell['source']]
                modified = True
    
    if modified:
        # 保存修改后的 notebook
        with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        
        print("\n✅ quick_start.ipynb 已成功更新！")
        print("📝 主要修改：")
        print("   - 仪表盘现在使用真实数据 (df_df)")
        print("   - 从数据中动态提取年度选项")
        print("   - 显示 Top 10 险种的保费分析")
        print("\n🔄 建议：在 Jupyter 中重新加载 Notebook 以查看更改")
    else:
        print("⚠️  未找到需要修改的单元格")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
