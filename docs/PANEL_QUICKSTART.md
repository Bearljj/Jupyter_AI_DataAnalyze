# 🚀 Panel 快速上手

## 📦 **安装**

```bash
# 安装 Panel 和依赖
pip install panel bokeh param

# 或添加到 requirements.txt
echo "panel>=1.3.0" >> requirements.txt
echo "bokeh>=3.3.0" >> requirements.txt
pip install -r requirements.txt
```

## ⚡ **5 分钟快速开始**

```python
# 1. 导入
from src.dashboard import PanelDashboardBuilder
from src.session import DataSession
import panel as pn
import polars as pl
import plotly.express as px

pn.extension('plotly')

# 2. 加载数据
session = DataSession()
session.load("alldata", alias="df")

# 3. 创建仪表盘（自动生成控件）
dashboard = PanelDashboardBuilder.from_data(
    df_df,
    dimensions=['业务年度', '业务险种'],
    title="📊 快速测试"
)

# 4. 定义分析逻辑
@pn.depends(*dashboard.widgets.values())
def update(*args):
    values = {n: w.value for n, w in dashboard.widgets.items()}
    
    # 简单聚合
    result = df_df.group_by('业务险种').agg([
        pl.col('总保费').sum().alias('保费')
    ]).head(10)
    
    # 图表
    fig = px.bar(result.to_pandas(), x='业务险种', y='保费')
    fig.update_layout(autosize=True, height=500)
    return fig

# 5. 显示
dashboard.set_update_function(update)
dashboard.show()

# 6. 导出
dashboard.save("test.html")
```

## ✅ **验证**

运行后应该看到：
1. 控件（下拉框/多选框）
2. 图表（可交互）
3. 文件 `test.html` 已创建

用浏览器打开 `test.html`，所有功能都可用！

## 📚 **完整指南**

- 详细文档：`docs/ai_context/PANEL_GUIDE.md`
- 迁移指南：`PANEL_MIGRATION.md`
- AI Context：即将更新

## 🆘 **问题排查**

**问题**: 控件不响应  
**解决**: 确保使用 `@pn.depends(*dashboard.widgets.values())`

**问题**: 图表不占满宽度  
**解决**: 设置 `fig.update_layout(autosize=True)`

**问题**: 导出 HTML 失败  
**解决**: 确保 `embed=True`: `dashboard.save("file.html", embed=True)`

---

**开始使用 Panel！** 🎉
