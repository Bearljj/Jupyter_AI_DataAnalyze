# Windows 图表显示问题诊断

import sys
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("📊 图表显示问题诊断")
print("=" * 70)
print()

# 1. Python 版本
print("1️⃣ Python 版本")
print(f"   {sys.version}")
print()

# 2. 关键库版本
print("2️⃣ 关键库版本")
try:
    import panel as pn
    print(f"   ✅ Panel: {pn.__version__}")
except ImportError as e:
    print(f"   ❌ Panel: 未安装 ({e})")

try:
    import plotly
    print(f"   ✅ Plotly: {plotly.__version__}")
except ImportError as e:
    print(f"   ❌ Plotly: 未安装 ({e})")

try:
    import polars as pl
    print(f"   ✅ Polars: {pl.__version__}")
except ImportError as e:
    print(f"   ❌ Polars: 未安装 ({e})")

print()

# 3. Panel 扩展检查
print("3️⃣ Panel 扩展状态")
try:
    import panel as pn
    pn.extension('plotly')
    print("   ✅ Plotly 扩展已加载")
except Exception as e:
    print(f"   ❌ 扩展加载失败: {e}")

print()

# 4. 测试简单图表
print("4️⃣ 测试 Plotly 图表")
try:
    import plotly.express as px
    import pandas as pd
    
    # 创建测试数据
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [1, 4, 2, 5, 3],
        'category': ['A', 'B', 'A', 'B', 'A']
    })
    
    # 创建图表
    fig = px.line(df, x='x', y='y', title='测试图表')
    
    print("   ✅ Plotly 图表创建成功")
    print("   💡 如果下面显示图表，说明 Plotly 正常")
    print()
    
    # 显示图表
    fig.show()
    
except Exception as e:
    print(f"   ❌ 创建失败: {e}")
    import traceback
    print()
    print("详细错误:")
    print(traceback.format_exc())

print()

# 5. 测试 Panel
print("5️⃣ 测试 Panel Dashboard")
try:
    import panel as pn
    pn.extension('plotly')
    
    # 创建简单 Panel
    widget = pn.widgets.IntSlider(name='测试', start=0, end=10, value=5)
    pane = pn.pane.Markdown(f"## 测试 Panel\n\n值: {widget.value}")
    
    print("   ✅ Panel 组件创建成功")
    print("   💡 如果下面显示组件，说明 Panel 正常")
    print()
    
    # 显示
    panel_obj = pn.Column(widget, pane)
    panel_obj
    
except Exception as e:
    print(f"   ❌ Panel 失败: {e}")
    import traceback
    print()
    print("详细错误:")
    print(traceback.format_exc())

print()

# 6. 中文显示测试
print("6️⃣ 测试中文显示")
try:
    import plotly.express as px
    import pandas as pd
    
    df = pd.DataFrame({
        '年份': ['2022', '2023', '2024'],
        '保费': [100, 150, 200]
    })
    
    fig = px.bar(df, x='年份', y='保费', title='中文测试')
    
    print("   ✅ 中文图表创建成功")
    print("   💡 如果下面中文显示正常，说明字体正常")
    print()
    
    fig.show()
    
except Exception as e:
    print(f"   ❌ 中文测试失败: {e}")

print()

# 7. Jupyter 环境检查
print("7️⃣ Jupyter 环境")
try:
    from IPython import get_ipython
    ipython = get_ipython()
    
    if ipython is not None:
        print(f"   ✅ 运行在 Jupyter 中")
        print(f"   类型: {type(ipython).__name__}")
    else:
        print("   ⚠️  不在 Jupyter 环境中")
        
except Exception as e:
    print(f"   ❌ 检查失败: {e}")

print()

# 8. 浏览器信息
print("8️⃣ 建议")
print("   如果图表不显示:")
print("   1. 检查浏览器控制台（F12）是否有错误")
print("   2. 尝试刷新页面 (Ctrl+R)")
print("   3. 清除浏览器缓存")
print("   4. 尝试不同浏览器（Chrome/Edge/Firefox)")
print("   5. 检查是否有代理或防火墙阻止 CDN")

print()
print("=" * 70)
print("诊断完成！")
print("=" * 70)
