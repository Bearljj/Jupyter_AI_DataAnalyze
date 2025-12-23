# 🎯 Panel Dashboard - AI 使用指南

**最新架构**: Phase 2.0 - Panel Integration  
**推荐度**: ⭐⭐⭐⭐⭐ (强烈推荐)

---

## ✨ **为什么使用 Panel？**

Panel 是**唯一**能导出包含交互控件的静态 HTML 的方案！

**优势**:
- ✅ 导出静态 HTML（控件 + 图表都可交互）
- ✅ 单个文件，可离线使用
- ✅ 可邮件分享
- ✅ 图表自动占满宽度
- ✅ 支持 Jupyter 和独立部署

---

## 🚨 **关键：必须移除 JupyterLab 宽度限制**

**为什么图表会挤在左边？**

JupyterLab 4 默认限制 notebook 最大宽度为 1140px，即使 Panel 设置了 `stretch_width`，图表也会被父容器限制。

**解决方案（每个 notebook 开头必须运行）：**

```python
# ========================================
# ⚠️ 必须运行：移除 JupyterLab 宽度限制
# ========================================
from IPython.display import HTML, display

display(HTML("""
<style>
    /* 核心：解除 JupyterLab 4 的宽度限制 */
    .jp-Notebook { 
        --jp-notebook-max-width: 100% !important; 
    }
    
    /* 确保所有输出容器占满宽度 */
    .jp-Notebook-cell, 
    .jp-Cell-outputWrapper, 
    .jp-OutputArea-output, 
    .jp-OutputArea-child { 
        max-width: none !important; 
        width: 100% !important; 
    }
    
    /* Panel 根容器强制铺满 */
    .bk-root, .bk-root > .bk { 
        width: 100% !important; 
        max-width: none !important; 
    }
</style>
"""))

print("✅ JupyterLab 宽度限制已移除")

# 然后初始化 Panel（全局 stretch_width）
import panel as pn
pn.extension('plotly', sizing_mode='stretch_width')
```

**这段代码做了什么？**
1. 覆盖 JupyterLab 的 `--jp-notebook-max-width` CSS 变量
2. 确保所有输出容器不受宽度限制
3. 强制 Panel/Bokeh 容器占满宽度
4. 设置 Panel 全局 `sizing_mode='stretch_width'`

**不运行会怎样？**
- ❌ 图表挤在左边
- ❌ 控件布局窄
- ❌ 导出的 HTML 也会很窄

---

## 📋 **完整代码模板**

### **标准工作流**

```python
# ========================================
# Panel 仪表盘 - 标准模板
# ========================================

# Step 1: 导入
from src.dashboard import PanelDashboardBuilder
from src.utils import print_markdown_table
import panel as pn
import polars as pl
import plotly.express as px

# Step 2: 初始化 Panel
pn.extension('plotly')

# Step 3: 创建仪表盘
dashboard = PanelDashboardBuilder.from_data(
    df_df,
    dimensions=['业务年度', '业务险种', '机构名称'],
   title="📊 保费分析仪表盘"
)

# Step 4: 定义更新函数（AI 生成）
@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    """
    仪表盘更新函数
    
    ⚠️ 关键点：
    1. 必须使用 @pn.depends(*dashboard.widgets.values())
    2. 参数是 *args（不需要具体命名）
    3. 通过 dashboard.widgets 获取控件值
    """
    
    # A. 获取控件值
    values = {
        name: widget.value 
        for name, widget in dashboard.widgets.items()
    }
    
    # B. 动态过滤数据
    filters = []
    for dim, val in values.items():
        if isinstance(val, list):  # MultiChoice（多选）
            if '全选' not in val:
                filters.append(pl.col(dim).is_in(val))
        else:  # Select（单选）
            if val != '全选':
                filters.append(pl.col(dim) == val)
    
    filtered = df_df
    for f in filters:
        filtered = filtered.filter(f)
    
    # C. 聚合分析
    result = filtered.group_by('业务险种').agg([
        pl.col('总保费').sum().alias('保费'),
        pl.len().alias('保单数')
    ]).sort('保费', descending=True)
    
    # D. 单位转换（>100万转为万元）
    max_premium = result['保费'].max()
    if max_premium > 1_000_000:
        result = result.with_columns([
            (pl.col('保费') / 10000).alias('保费（万元）')
        ])
        y_col = '保费（万元）'
        title_suffix = '（单位: 万元）'
    else:
        y_col = '保费'
        title_suffix = ''
    
    # E. Markdown 输出
    print("## 📊 分析结果\\n")
    print(f"数据量: {filtered.height:,} 行\\n")
    print("### Top 10 险种\\n")
    print_markdown_table(result.head(10))
    
    # F. 图表（自适应宽度）
    fig = px.bar(
        result.head(10).to_pandas(),
        x='业务险种',
        y=y_col,
        title=f'险种保费排名 {title_suffix}',
        text=y_col
    )
    
    fig.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
    fig.update_layout(
        height=600,
        autosize=True,  # ← 关键：自动占满宽度
        showlegend=False
    )
    
    return fig

# Step 5: 绑定更新函数
dashboard.set_update_function(update_dashboard)

# Step 6: 显示
dashboard.show()

# Step 7: 导出 HTML（可选）
dashboard.save("保费分析.html")
print("\\n✅ 已导出到 保费分析.html")
print("💡 用浏览器打开，所有控件和图表都可交互！")
```

---

## 🎯 **AI 必须遵循的规则**

### **Rule 1: 装饰器**
```python
# ✅ 正确
@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    ...

# ❌ 错误（缺少装饰器）
def update_dashboard(*args):
    ...
```

### **Rule 2: 函数参数**
```python
# ✅ 正确
def update_dashboard(*args):  # 参数是 *args
    values = {name: widget.value for name, widget in dashboard.widgets.items()}
    
# ❌ 错误（参数名错误）
def update_dashboard(controls):  # 这是 ipywidgets 的方式
    ...
```

### **Rule 3: 获取控件值**
```python
# ✅ 正确（动态获取）
values = {name: widget.value for name, widget in dashboard.widgets.items()}
year = values['业务年度']

# ❌ 错误（无法直接获取）
year = controls['业务年度']  # controls 不存在
```

### **Rule 4: 处理"全选"**
```python
# ✅ 正确
for dim, val in values.items():
    if isinstance(val, list):
        if '全选' not in val:  # 排除"全选"
            filters.append(pl.col(dim).is_in(val))
    else:
        if val != '全选':
            filters.append(pl.col(dim) == val)

# ❌ 错误（忘记处理"全选"）
filters.append(pl.col(dim) == val)  # "全选"会导致错误
```

### **Rule 5: 图表自适应**
```python
# ✅ 正确
fig.update_layout(
    height=600,
    autosize=True,  # ← 必须
    showlegend=False
)

# ❌ 错误（固定宽度）
fig.update_layout(width=1000, height=600)
```

### **Rule 6: 使用 pl.len()**
```python
# ✅ 正确
pl.len().alias('保单数')

# ❌ 错误（已弃用）
pl.count().alias('保单数')
```

### **Rule 7: 末尾调用**
```python
# ✅ 正确
dashboard.set_update_function(update_dashboard)
dashboard.show()  # Jupyter 中显示
dashboard.save("output.html")  # 导出 HTML

# ❌ 错误（缺少 show/save）
dashboard.set_update_function(update_dashboard)
# 没有显示或导出
```

---

## 📝 **常见场景示例**

### **场景 1: 单维度分析**

```python
@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    values = {name: widget.value for name, widget in dashboard.widgets.items()}
    
    year = values.get('业务年度', '全选')
    
    if year == '全选':
        result = df_df.group_by('业务年度').agg([...])
    else:
        result = df_df.filter(pl.col('业务年度') == year).agg([...])
    
    fig = px.line(result.to_pandas(), x='业务年度', y='保费')
    fig.update_layout(autosize=True, height=600)
    return fig
```

### **场景 2: 多维度交叉分析**

```python
@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    values = {name: widget.value for name, widget in dashboard.widgets.items()}
    
    # 应用所有过滤
    filtered = df_df
    for dim, val in values.items():
        if isinstance(val, list):
            if '全选' not in val:
                filtered = filtered.filter(pl.col(dim).is_in(val))
        else:
            if val != '全选':
                filtered = filtered.filter(pl.col(dim) == val)
    
    # 使用第一个维度分组
    dims = list(values.keys())
    if dims:
        group_by_dim = dims[0]
        result = filtered.group_by(group_by_dim).agg([...])
        fig = px.bar(result.to_pandas(), x=group_by_dim, y='保费')
    else:
        result = filtered.select([...])
        fig = px.bar(x=['总计'], y=[result['保费'][0]])
    
    fig.update_layout(autosize=True, height=600)
    return fig
```

### **场景 3: 带多个子图**

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    values = {name: widget.value for name, widget in dashboard.widgets.items()}
    
    # 过滤...
    
    # 创建子图
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("保费趋势", "险种分布", "地区对比", "综合指标")
    )
    
    # 添加图表...
    fig.add_trace(go.Bar(...), row=1, col=1)
    fig.add_trace(go.Pie(...), row=1, col=2)
    
    fig.update_layout(
        height=1000,
        autosize=True,  # ← 关键
        showlegend=True
    )
    
    return fig
```

---

## ✅ **检查清单**

AI 生成代码前，确保：

- [ ] 使用 `@pn.depends(*dashboard.widgets.values())`
- [ ] 函数参数是 `*args`
- [ ] 通过 `dashboard.widgets` 获取控件值
- [ ] 处理"全选"选项
- [ ] 使用 `pl.len()` 而不是 `pl.count()`
- [ ] 金额超过 100 万时转换为"万元"
- [ ] 图表设置 `autosize=True`
- [ ] 末尾有 `dashboard.show()` 或 `dashboard.save()`
- [ ] 使用 `print_markdown_table()` 输出表格

---

## 🎉 **完整流程**

```
1. 用户选择维度 → PanelDashboardBuilder.from_data()
2. AI 生成更新函数 → @pn.depends 装饰器 + 动态过滤
3. 绑定函数 → dashboard.set_update_function()
4. 显示 → dashboard.show()
5. 导出 → dashboard.save("output.html")
6. 分享 → 发送 HTML 文件
```

---

**按照这个模板，生成的仪表盘将完美运行！** ✨
