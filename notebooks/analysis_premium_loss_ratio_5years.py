# ================================================================
# 📊 最近五年保费结构与综合成本率分析
# ================================================================
# 分析师：AI Assistant
# 分析日期：2025-12-21
# ================================================================

import polars as pl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import display, Markdown

print("🔍 开始分析：最近五年保费结构与综合成本率")
print("=" * 80)

# ================================================================
# 获取数据（兼容多种加载方式）
# ================================================================

df_df = None

# 方法1: 尝试从全局变量获取
try:
    import __main__
    if hasattr(__main__, 'df_df'):
        df_df = __main__.df_df
        print("✅ 从全局变量获取数据")
    elif hasattr(__main__, 'session'):
        # 方法2: 从 session 获取
        session = __main__.session
        df_df = session.get('df_df')
        if df_df is not None:
            print("✅ 从 DataSession 获取数据")
except:
    pass

# 方法3: 尝试直接访问（在 notebook 中粘贴代码时）
if df_df is None:
    try:
        df_df = globals()['df_df']
        print("✅ 从当前命名空间获取数据")
    except KeyError:
        pass

# 如果仍然没有数据，给出清晰的错误提示
if df_df is None:
    print("\n" + "=" * 80)
    print("❌ 错误：未找到数据 df_df")
    print("=" * 80)
    print("\n请先在 Notebook 中运行以下代码加载数据：\n")
    print("```python")
    print("from src.session import DataSession")
    print()
    print("session = DataSession()")
    print("session.load('alldata', alias='df')")
    print("session.summary()")
    print("```")
    print("\n然后：")
    print("1. 方法一：将本脚本的全部内容复制到 Notebook 新单元格中运行")
    print("2. 方法二：使用 exec(open('...py').read()) 运行")
    print("\n❌ 不要使用 %run，它无法访问 Notebook 的全局变量")
    print("=" * 80)
    
    # 抛出异常以停止执行
    raise NameError("df_df 未定义。请先使用 session.load() 加载数据。")

# ================================================================
# 验证数据
# ================================================================
print(f"📊 数据概览：{df_df.height:,} 行 × {df_df.width} 列")
print()

# ================================================================
# 1. 数据准备与计算
# ================================================================

print("⏳ 正在处理数据...")

# 按年度汇总关键指标
yearly_analysis = df_df.group_by('业务年度').agg([
    # ===== 保费指标 =====
    pl.col('总保费').sum().alias('毛保费'),
    pl.col('自留保费').sum().alias('自留保费'),
    
    # ===== 赔款指标（已决 + 未决）=====
    # 总赔款
    (pl.col('总已决赔款').sum() + pl.col('总未决赔款').sum()).alias('总赔款'),
    # 自留赔款
    (pl.col('自留已决').sum() + pl.col('自留未决').sum()).alias('自留赔款'),
    # 分出赔款（通过各类分保赔款汇总）
    (
        pl.col('协议已决').sum() + pl.col('协议未决').sum() +
        pl.col('成数已决').sum() + pl.col('成数未决').sum() +
        pl.col('溢额已决').sum() + pl.col('溢额未决').sum() +
        pl.col('临分已决').sum() + pl.col('临分未决').sum()
    ).alias('分出赔款'),
    
    # ===== 保单数量 =====
    pl.len().alias('保单数量'),
    
]).with_columns([
    # 计算分出保费（毛保费 - 自留保费）
    (pl.col('毛保费') - pl.col('自留保费')).alias('分出保费'),
    
]).with_columns([
    # ===== 综合成本率（赔款 / 保费）=====
    (pl.col('总赔款') / pl.col('毛保费') * 100).alias('毛成本率'),
    (pl.col('自留赔款') / pl.col('自留保费') * 100).alias('自留成本率'),
    (pl.col('分出赔款') / pl.col('分出保费') * 100).alias('分出成本率'),
    
    # ===== 自留率（自留保费 / 毛保费）=====
    (pl.col('自留保费') / pl.col('毛保费') * 100).alias('自留率'),
    
    # ===== 平均保单价值 =====
    (pl.col('毛保费') / pl.col('保单数量')).alias('平均保单价值'),
    
]).sort('业务年度')

# 取最近5年数据
yearly_analysis_5y = yearly_analysis.tail(5)

print(f"✅ 数据处理完成")
print(f"📅 分析期间: {yearly_analysis_5y['业务年度'].min()} - {yearly_analysis_5y['业务年度'].max()}")
print()

# ================================================================
# 2. 关键指标总结表
# ================================================================

print("📋 【表1】最近五年保费结构与成本率总览")
print("=" * 80)

# 使用 Markdown 表格格式化输出（如果启用了 polars_display）
try:
    from src.utils import print_markdown_table
    
    display_table = yearly_analysis_5y.select([
        '业务年度',
        '毛保费',
        '自留保费',
        '分出保费',
        '自留率',
        '毛成本率',
        '自留成本率',
        '分出成本率'
    ])
    
    print_markdown_table(display_table)
except:
    # 如果 Markdown 显示不可用，使用传统格式
    print(yearly_analysis_5y.select([
        '业务年度', '毛保费', '自留保费', '分出保费',
        '自留率', '毛成本率', '自留成本率', '分出成本率'
    ]))

print()

# ================================================================
# 3. 详细分析报告
# ================================================================

print("📊 【详细分析】")
print("=" * 80)

for row in yearly_analysis_5y.iter_rows(named=True):
    year = row['业务年度']
    print(f"\n【{year}年度】")
    print(f"  📈 保费结构：")
    print(f"     • 毛保费:    {row['毛保费']:>15,.0f} 元 (100.0%)")
    print(f"     • 自留保费:  {row['自留保费']:>15,.0f} 元 ({row['自留率']:>5.2f}%)")
    print(f"     • 分出保费:  {row['分出保费']:>15,.0f} 元 ({100-row['自留率']:>5.2f}%)")
    print(f"  ")
    print(f"  🎯 综合成本率：")
    print(f"     • 毛成本率:  {row['毛成本率']:>6.2f}%")
    print(f"     • 自留成本率:{row['自留成本率']:>6.2f}%")
    print(f"     • 分出成本率:{row['分出成本率']:>6.2f}%")
    print(f"  ")
    print(f"  📑 业务规模：")
    print(f"     • 保单数量:  {row['保单数量']:>15,} 份")
    print(f"     • 平均保单:  {row['平均保单价值']:>15,.0f} 元/份")

print("\n" + "=" * 80)

# ================================================================
# 4. 趋势分析与关键洞察
# ================================================================

print("\n💡 【关键洞察】")
print("=" * 80)

# 计算同比变化
if yearly_analysis_5y.height >= 2:
    latest = yearly_analysis_5y[-1]
    previous = yearly_analysis_5y[-2]
    
    premium_growth = (latest['毛保费'] - previous['毛保费']) / previous['毛保费'] * 100
    retention_change = latest['自留率'] - previous['自留率']
    loss_ratio_change = latest['毛成本率'] - previous['毛成本率']
    
    print(f"\n📌 最新年度 ({latest['业务年度']}) vs 上一年度 ({previous['业务年度']}):")
    print(f"   • 毛保费同比: {premium_growth:+.2f}%")
    print(f"   • 自留率变化: {retention_change:+.2f} 个百分点")
    print(f"   • 毛成本率变化: {loss_ratio_change:+.2f} 个百分点")

# 五年期间统计
print(f"\n📌 五年期间总体趋势:")
print(f"   • 毛保费范围: {yearly_analysis_5y['毛保费'].min():,.0f} - {yearly_analysis_5y['毛保费'].max():,.0f} 元")
print(f"   • 自留率范围: {yearly_analysis_5y['自留率'].min():.2f}% - {yearly_analysis_5y['自留率'].max():.2f}%")
print(f"   • 毛成本率范围: {yearly_analysis_5y['毛成本率'].min():.2f}% - {yearly_analysis_5y['毛成本率'].max():.2f}%")

# 风险预警
avg_loss_ratio = yearly_analysis_5y['毛成本率'].mean()
latest_loss_ratio = yearly_analysis_5y[-1]['毛成本率']

print(f"\n⚠️  风险评估:")
print(f"   • 五年平均毛成本率: {avg_loss_ratio:.2f}%")
print(f"   • 最新毛成本率: {latest_loss_ratio:.2f}%")

if latest_loss_ratio > 75:
    print(f"   • 【警示】当前成本率较高（>{75}%），建议关注赔付风险")
elif latest_loss_ratio < 50:
    print(f"   • 【优秀】当前成本率良好（<{50}%），盈利能力较强")
else:
    print(f"   • 【正常】当前成本率处于合理区间")

print("\n" + "=" * 80)

# ================================================================
# 5. 可视化图表
# ================================================================

print("\n📈 生成可视化图表...")

# 创建双子图：保费结构 + 成本率趋势
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=(
        '保费结构分析（毛保费、自留保费、分出保费）',
        '综合成本率对比（毛成本率、自留成本率、分出成本率）'
    ),
    vertical_spacing=0.12,
    specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
)

# 转换为 Pandas 用于 Plotly
df_plot = yearly_analysis_5y.to_pandas()

# === 子图1: 保费堆叠柱状图 + 毛保费折线 ===
fig.add_trace(
    go.Bar(
        name='自留保费',
        x=df_plot['业务年度'],
        y=df_plot['自留保费'],
        marker_color='#2E86AB',
        text=df_plot['自留保费'],
        texttemplate='%{text:,.0f}',
        textposition='inside',
        hovertemplate='自留保费: %{y:,.0f}<extra></extra>'
    ),
    row=1, col=1
)

fig.add_trace(
    go.Bar(
        name='分出保费',
        x=df_plot['业务年度'],
        y=df_plot['分出保费'],
        marker_color='#A23B72',
        text=df_plot['分出保费'],
        texttemplate='%{text:,.0f}',
        textposition='inside',
        hovertemplate='分出保费: %{y:,.0f}<extra></extra>'
    ),
    row=1, col=1
)

# 添加毛保费折线
fig.add_trace(
    go.Scatter(
        name='毛保费',
        x=df_plot['业务年度'],
        y=df_plot['毛保费'],
        mode='lines+markers+text',
        line=dict(color='#F18F01', width=3),
        marker=dict(size=12, symbol='diamond'),
        text=df_plot['毛保费'],
        texttemplate='%{text:,.0f}',
        textposition='top center',
        hovertemplate='毛保费: %{y:,.0f}<extra></extra>'
    ),
    row=1, col=1
)

# === 子图2: 成本率折线图 ===
fig.add_trace(
    go.Scatter(
        name='毛成本率',
        x=df_plot['业务年度'],
        y=df_plot['毛成本率'],
        mode='lines+markers+text',
        line=dict(color='#C73E1D', width=3),
        marker=dict(size=10),
        text=df_plot['毛成本率'].apply(lambda x: f'{x:.1f}%'),
        textposition='top center',
        hovertemplate='毛成本率: %{y:.2f}%<extra></extra>'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        name='自留成本率',
        x=df_plot['业务年度'],
        y=df_plot['自留成本率'],
        mode='lines+markers+text',
        line=dict(color='#2E86AB', width=2, dash='dash'),
        marker=dict(size=8),
        text=df_plot['自留成本率'].apply(lambda x: f'{x:.1f}%'),
        textposition='bottom center',
        hovertemplate='自留成本率: %{y:.2f}%<extra></extra>'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        name='分出成本率',
        x=df_plot['业务年度'],
        y=df_plot['分出成本率'],
        mode='lines+markers+text',
        line=dict(color='#A23B72', width=2, dash='dot'),
        marker=dict(size=8),
        text=df_plot['分出成本率'].apply(lambda x: f'{x:.1f}%'),
        textposition='middle right',
        hovertemplate='分出成本率: %{y:.2f}%<extra></extra>'
    ),
    row=2, col=1
)

# 添加成本率预警线
fig.add_hline(
    y=75, line_dash="dash", line_color="red", opacity=0.5,
    annotation_text="预警线 (75%)", annotation_position="right",
    row=2, col=1
)

# 更新布局
fig.update_layout(
    height=900,
    title_text=f"最近五年保费结构与综合成本率分析 ({yearly_analysis_5y['业务年度'].min()}-{yearly_analysis_5y['业务年度'].max()})",
    title_font_size=16,
    showlegend=True,
    barmode='stack',
    hovermode='x unified',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

fig.update_xaxes(title_text="业务年度", row=1, col=1)
fig.update_yaxes(title_text="保费金额（元）", row=1, col=1)

fig.update_xaxes(title_text="业务年度", row=2, col=1)
fig.update_yaxes(title_text="成本率（%）", row=2, col=1)

# 显示图表
fig.show()

print("✅ 分析完成！")
print("=" * 80)
