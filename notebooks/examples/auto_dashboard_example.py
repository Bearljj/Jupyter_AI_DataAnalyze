# ========================================
# 🎨 自动仪表盘创建示例
# ========================================
# 演示如何使用 DashboardBuilder.from_data() 
# 自动从数据创建交互式仪表盘
# ========================================

from src.session import DataSession
from src.dashboard import DashboardBuilder
from src.utils import enable_polars_markdown_display, print_markdown_table
import polars as pl
import plotly.express as px

print("=" * 80)
print("🚀 自动仪表盘创建示例")
print("=" * 80)
print()

# ========================================
# Step 1: 加载数据
# ========================================

print("📊 Step 1: 加载数据\n")

session = DataSession()
session.load("alldata", alias="df")
session.summary()

# 启用 Markdown 显示
enable_polars_markdown_display()

print()

# ========================================
# Step 2: AI 分析维度字段
# ========================================

print("=" * 80)
print("🤖 Step 2: AI 分析维度字段")
print("=" * 80)
print()

# AI 识别潜在维度
print("分析数据结构，识别维度字段...\n")

dimensions_info = []

for col in df_df.columns:
    dtype = str(df_df[col].dtype)
    
    # 字符串类型 = 潜在维度
    if dtype == 'String' or dtype.startswith('Date'):
        n_unique = df_df[col].n_unique()
        
        # 确定控件类型
        if n_unique <= 10:
            control = "dropdown"
            note = ""
        elif n_unique <= 50:
            control = "multiselect"
            note = ""
        elif n_unique <= 500:
            control = "multiselect"
            note = "⚠️ 选项较多"
        else:
            control = "multiselect"
            note = "⚠️ 建议 Phase 2 使用级联"
        
        dimensions_info.append({
            'field': col,
            'unique_values': n_unique,
            'control': control,
            'note': note
        })

# 显示建议
print("### 建议的维度字段:\n")
for info in dimensions_info:
    print(f"- **{info['field']}** ({info['unique_values']} 个值)")
    print(f"  → 控件类型: {info['control']} {info['note']}")

print("\n" + "=" * 80)
print()

# ========================================
# Step 3: 用户确认维度（这里手动指定）
# ========================================

print("👤 Step 3: 用户确认要使用的维度\n")

# 实际使用时，这些是用户/AI 确认后的维度
selected_dimensions = ['业务年度', '业务险种']

print(f"✅ 已选择维度: {', '.join(selected_dimensions)}\n")
print("=" * 80)
print()

# ========================================
# Step 4: 自动创建仪表盘
# ========================================

print("🎨 Step 4: 自动创建仪表盘\n")

dashboard = DashboardBuilder.from_data(
    df_df,
    dimensions=selected_dimensions,
    title="保费分析仪表盘"
)

print("=" * 80)
print()

# ========================================
# Step 5: AI 生成分析逻辑
# ========================================

print("🤖 Step 5: AI 生成分析逻辑\n")
print("AI 现在只需要生成 update_function，不需要创建控件！\n")

def update_dashboard(controls):
    """
    仪表盘更新逻辑（AI 生成）
    
    Args:
        controls: 控件值字典
            - '业务年度': 单个年度值（dropdown）
            - '业务险种': 险种列表（multiselect）
    """
    # 获取控件值
    year = controls['业务年度']
    products = controls['业务险种']
    
    # 过滤数据
    filtered = df_df.filter(
        (pl.col('业务年度') == year) &
        (pl.col('业务险种').is_in(products))
    )
    
    # 聚合分析
    result = filtered.group_by('业务险种').agg([
        pl.col('总保费').sum().alias('保费'),
        pl.col('总保额').sum().alias('保额'),
        pl.len().alias('保单数'),
        (pl.col('总保费') / pl.len()).alias('平均保单保费')
    ]).sort('保费', descending=True)
    
    # === Markdown 格式输出（重要！）===
    print(f"## {year}年 险种分析报告\n")
    print(f"### 筛选条件\n")
    print(f"- 年度: {year}")
    print(f"- 险种数量: {len(products)} 个")
    print(f"- 险种: {', '.join(products[:5])}{'...' if len(products) > 5 else ''}")
    print(f"- 数据量: {filtered.height:,} 行\n")
    
    print(f"### Top {min(10, result.height)} 险种保费排名\n")
    print_markdown_table(result.head(10))
    
    print("\n### 关键指标\n")
    print(f"- 总保费: {result['保费'].sum():,.0f} 元")
    print(f"- 总保额: {result['保额'].sum():,.0f} 元")
    print(f"- 总保单: {result['保单数'].sum():,} 份")
    print(f"- 险种数: {result.height}\n")
    
    # 创建可视化
    fig = px.bar(
        result.head(10).to_pandas(),
        x='业务险种',
        y='保费',
        title=f'{year}年 Top 10 险种保费',
        text='保费',
        hover_data=['保额', '保单数', '平均保单保费']
    )
    
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(height=500, showlegend=False)
    
    return fig

print("✅ 分析逻辑已定义\n")
print("=" * 80)
print()

# ========================================
# Step 6: 绑定并启动
# ========================================

print("🚀 Step 6: 绑定分析逻辑并启动仪表盘\n")

dashboard.set_update_function(update_dashboard)

print("✅ 准备就绪！运行 dashboard.build() 启动仪表盘\n")
print("=" * 80)
print()
print("💡 提示：")
print("   1. 仪表盘会显示交互控件")
print("   2. 选择不同的年度和险种，图表会自动更新")
print("   3. 输出会以 Markdown 格式显示，表格清晰美观")
print()
print("现在运行下一个单元格：")
print("dashboard.build()")
print()
print("=" * 80)
