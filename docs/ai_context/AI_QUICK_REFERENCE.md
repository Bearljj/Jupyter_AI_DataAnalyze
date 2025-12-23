# 🤖 AI 生成代码 - 完整上下文

**给 AI 的提示**：请完整阅读此文档，然后生成符合规范的 Panel Dashboard 代码。

---

## 🚨 **关键规则（必须遵守）**

### **1. 必须使用 PanelDashboardBuilder**

```python
# ✅ 正确
from src.dashboard import PanelDashboardBuilder
import panel as pn

# ❌ 错误 - 不要使用这个！
from src.dashboard import DashboardBuilder  # 已废弃
```

### **2. 必须添加 CSS 宽度修复**

**在所有代码开头添加**：

```python
from IPython.display import HTML, display

display(HTML("""
<style>
    .jp-Notebook { --jp-notebook-max-width: 100% !important; }
    .jp-Notebook-cell, .jp-Cell-outputWrapper, 
    .jp-OutputArea-output, .jp-OutputArea-child { 
        max-width: none !important; 
        width: 100% !important; 
    }
    .bk-root, .bk-root > .bk { 
        width: 100% !important; 
        max-width: none !important; 
    }
</style>
"""))

print("✅ JupyterLab 宽度限制已移除")
```

### **3. Panel 初始化**

```python
import panel as pn
pn.extension('plotly', sizing_mode='stretch_width')
```

---

## 📋 **完整代码模板**

```python
# ========================================
# Step 1: CSS 修复 + 导入
# ========================================
from IPython.display import HTML, display

display(HTML("""
<style>
    .jp-Notebook { --jp-notebook-max-width: 100% !important; }
    .jp-Notebook-cell, .jp-Cell-outputWrapper, 
    .jp-OutputArea-output, .jp-OutputArea-child { 
        max-width: none !important; 
        width: 100% !important; 
    }
    .bk-root, .bk-root > .bk { 
        width: 100% !important; 
        max-width: none !important; 
    }
</style>
"""))

import panel as pn
import polars as pl
import plotly.express as px
from src.dashboard import PanelDashboardBuilder
from src.utils import print_markdown_table

# 初始化 Panel
pn.extension('plotly', sizing_mode='stretch_width')

print("✅ 环境初始化完成")

# ========================================
# Step 2: 创建仪表盘
# ========================================
dashboard = PanelDashboardBuilder.from_data(
    df_df,
    dimensions=['业务年度', '业务险种'],  # 你的维度
    title="📊 数据分析仪表盘"
)

# ========================================
# Step 3: 定义更新函数
# ========================================
@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    """
    ⚠️ 关键点：
    1. 使用 @pn.depends(*dashboard.widgets.values())
    2. 参数是 *args
    3. 通过 dashboard.widgets 获取控件值
    """
    
    # A. 获取控件值
    values = {
        name: widget.value 
        for name, widget in dashboard.widgets.items()
    }
    
    # B. 动态过滤数据（处理"全选"）
    filters = []
    for dim, val in values.items():
        if isinstance(val, list):  # MultiChoice
            if '全选' not in val:
                filters.append(pl.col(dim).is_in(val))
        else:  # Select
            if val != '全选':
                filters.append(pl.col(dim) == val)
    
    filtered = df_df
    for f in filters:
        filtered = filtered.filter(f)
    
    # C. 聚合分析
    result = filtered.group_by('业务险种').agg([
        pl.col('总保费').sum().alias('保费'),
        pl.len().alias('保单数')  # ← 使用 pl.len()
    ]).sort('保费', descending=True)
    
    # D. 单位转换（>100万转为万元）
    max_premium = result['保费'].max()
    if max_premium > 1_000_000:
        result = result.with_columns([
            (pl.col('保费') / 10000).alias('保费（万元）')
        ])
        y_col = '保费（万元）'
    else:
        y_col = '保费'
    
    # E. Markdown 输出
    print("## 📊 分析结果\\n")
    print(f"数据量: {filtered.height:,} 行\\n")
    print("### Top 10\\n")
    print_markdown_table(result.head(10))
    
    # F. 图表（自适应宽度）
    fig = px.bar(
        result.head(10).to_pandas(),
        x='业务险种',
        y=y_col,
        title='险种保费排名',
        text=y_col
    )
    
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(
        height=600,
        autosize=True,  # ← 关键
        showlegend=False
    )
    
    return fig

# ========================================
# Step 4: 绑定和显示
# ========================================
dashboard.set_update_function(update_dashboard)
dashboard.show()

# ========================================
# Step 5: 导出 HTML（可选）
# ========================================
dashboard.save("分析结果.html")
print("✅ 已导出到 分析结果.html")
```

---

## 🎯 **关键规则清单**

### **必须遵守**：

- [ ] 使用 `from src.dashboard import PanelDashboardBuilder`
- [ ] **不要**使用 `DashboardBuilder`（已废弃）
- [ ] 开头添加 CSS 宽度修复
- [ ] 使用 `pn.extension('plotly', sizing_mode='stretch_width')`
- [ ] 使用 `@pn.depends(*dashboard.widgets.values())` 装饰器
- [ ] 函数参数是 `*args`
- [ ] 通过 `dashboard.widgets` 获取控件值
- [ ] 处理"全选"选项
- [ ] 使用 `pl.len()` 而不是 `pl.count()`
- [ ] 金额超过 100 万时转换为"万元"
- [ ] 图表设置 `autosize=True`
- [ ] 末尾有 `dashboard.show()`

### **处理"全选"示例**：

```python
for dim, val in values.items():
    if isinstance(val, list):  # MultiChoice（多选）
        if '全选' not in val:
            filters.append(pl.col(dim).is_in(val))
    else:  # Select（单选）
        if val != '全选':
            filters.append(pl.col(dim) == val)
```

---

## ⚠️ **常见错误**

### **错误 1: 使用旧的 DashboardBuilder**

```python
# ❌ 错误
from src.dashboard import DashboardBuilder
dashboard = DashboardBuilder.from_data(...)

# ✅ 正确
from src.dashboard import PanelDashboardBuilder
dashboard = PanelDashboardBuilder.from_data(...)
```

### **错误 2: 忘记 CSS 修复**

```python
# ❌ 错误 - 没有 CSS 修复
import panel as pn
pn.extension('plotly')

# ✅ 正确 - 有 CSS 修复
from IPython.display import HTML, display
display(HTML("""<style>..."""))
pn.extension('plotly', sizing_mode='stretch_width')
```

### **错误 3: 装饰器错误**

```python
# ❌ 错误
def update_dashboard(controls):  # ipywidgets 方式
    ...

# ✅ 正确
@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):  # Panel 方式
    values = {name: widget.value for name, widget in dashboard.widgets.items()}
    ...
```

### **错误 4: 使用 pl.count()**

```python
# ❌ 错误（已弃用）
pl.count().alias('保单数')

# ✅ 正确
pl.len().alias('保单数')
```

---

## 📚 **详细文档**

完整的 Panel 使用指南请参考：`docs/ai_context/PANEL_GUIDE.md`

---

**按照这个模板生成代码，Dashboard 将完美运行并可导出 HTML！** ✨
