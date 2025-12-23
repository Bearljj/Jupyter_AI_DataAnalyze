# 🚀 Panel 架构迁移指南

**日期**: 2025-12-21  
**版本**: Phase 2.0 - Panel Integration  
**状态**: 📋 实施中

---

## 🎯 **迁移目标**

将项目从 **ipywidgets** 迁移到 **Panel**，以支持：
- ✅ 导出静态 HTML（包含交互控件）
- ✅ 图表自适应占满宽度
- ✅ 更好的部署选项
- ✅ 保持向下兼容

---

## 📋 **迁移检查清单**

### **Phase 1: 核心组件** ✅
- [x] 创建 `PanelDashboardBuilder` (src/dashboard/panel_builder.py)
- [ ] 更新 `src/dashboard/__init__.py`
- [ ] 添加 Panel 到依赖
- [ ] 测试基本功能

### **Phase 2: 文档更新**
- [ ] 更新 AI Context (docs/ai_context/main.md)
- [ ] 创建 Panel 使用指南
- [ ] 更新 Quick Start
- [ ] 创建迁移示例

### **Phase 3: 示例和模板**
- [ ] 创建 Panel 版本示例
- [ ] 更新 notebook 模板
- [ ] 创建导出脚本

---

## 🔧 **手动更新步骤**

### **步骤 1: 更新 `src/dashboard/__init__.py`**

```python
"""交互式仪表盘包"""

from .builder import DashboardBuilder
from .panel_builder import PanelDashboardBuilder

__all__ = ["DashboardBuilder", "PanelDashboardBuilder"]
```

### **步骤 2: 安装 Panel**

```bash
pip install panel bokeh param
```

或更新 `requirements.txt`:
```
polars>=0.20.0
plotly>=5.18.0
ipywidgets>=8.0.0
panel>=1.3.0  # 新增
bokeh>=3.3.0  # Panel 依赖
param>=2.0.0  # Panel 依赖
```

### **步骤 3: 测试 Panel 版本**

```python
# 在 Jupyter 中测试
from src.dashboard import PanelDashboardBuilder
from src.session import DataSession
import polars as pl

# 加载数据
session = DataSession()
session.load("alldata", alias="df")

# 创建仪表盘
dashboard = PanelDashboardBuilder.from_data(
    df_df,
    dimensions=['业务年度', '业务险种'],
    title="Panel 测试仪表盘"
)

# 定义更新函数
import panel as pn
import plotly.express as px

@pn.depends(*dashboard.widgets.values())
def update(*args):
    # 获取控件值
    values = {name: widget.value 
              for name, widget in dashboard.widgets.items()}
    
    # 过滤数据
    filtered = df_df
    for dim, val in values.items():
        if isinstance(val, list):
            if '全选' not in val:
                filtered = filtered.filter(pl.col(dim).is_in(val))
        else:
            if val != '全选':
                filtered = filtered.filter(pl.col(dim) == val)
    
    # 聚合
    result = filtered.group_by('业务险种').agg([
        pl.col('总保费').sum().alias('保费'),
        pl.len().alias('保单数')
    ]).sort('保费', descending=True)
    
    # 图表
    fig = px.bar(result.to_pandas(), x='业务险种', y='保费')
    fig.update_layout(height=600, autosize=True)
    
    return fig

dashboard.set_update_function(update)

# 显示
dashboard.show()

# 导出 HTML
dashboard.save("test_panel.html")
```

---

## 📝 **AI Context 更新**

### **新增章节：Panel Dashboard (推荐)**

在 `docs/ai_context/main.md` 中添加：

```markdown
## 🆕 交互式仪表盘（Panel - 推荐）

### 为什么选择 Panel？

- ✅ **支持导出静态 HTML**（包含交互控件）
- ✅ 图表自动占满宽度
- ✅ 单个文件，可离线使用
- ✅ 可邮件分享

### 使用方法

#### Step 1: 自动创建仪表盘

\`\`\`python
from src.dashboard import PanelDashboardBuilder
import panel as pn

# 从数据创建仪表盘
dashboard = PanelDashboardBuilder.from_data(
    df_df,
    dimensions=['业务年度', '业务险种', '机构名称'],
    title="保费分析仪表盘"
)
\`\`\`

#### Step 2: AI 生成分析逻辑

\`\`\`python
import plotly.express as px

# ⚠️ 关键：使用 @pn.depends 装饰器
@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    # 1. 获取控件值
    values = {name: widget.value 
              for name, widget in dashboard.widgets.items()}
    
    # 2. 动态过滤数据
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
    
    # 3. 聚合分析
    result = filtered.group_by('业务险种').agg([
        pl.col('总保费').sum().alias('保费'),
        pl.len().alias('保单数')
    ])
    
    # 4. 单位转换（100万+转为万元）
    max_premium = result['保费'].max()
    if max_premium > 1_000_000:
        result = result.with_columns([
            (pl.col('保费') / 10000).alias('保费（万元）')
        ])
        y_col = '保费（万元）'
    else:
        y_col = '保费'
    
    # 5. Markdown 输出
    print("## 分析结果\\n")
    print_markdown_table(result.head(10))
    
    # 6. 图表（自适应宽度）
    fig = px.bar(result.to_pandas(), x='业务险种', y=y_col)
    fig.update_layout(
        height=600,
        autosize=True,  # 自动占满宽度
        showlegend=False
    )
    
    return fig

# 绑定更新函数
dashboard.set_update_function(update_dashboard)
\`\`\`

#### Step 3: 显示和导出

\`\`\`python
# 在 Jupyter 中显示
dashboard.show()

# 导出为静态 HTML
dashboard.save("analysis.html")
\`\`\`

### AI 注意事项

1. **必须使用 `@pn.depends` 装饰器**
   ```python
   @pn.depends(*dashboard.widgets.values())
   def update_dashboard(*args):
       ...
   ```

2. **函数参数是 `*args`**（不需要具体命名）

3. **在函数内部通过 `dashboard.widgets` 获取值**
   ```python
   values = {name: widget.value for name, widget in dashboard.widgets.items()}
   ```

4. **不要硬编码字段名**，使用 `values` 字典动态访问

5. **处理"全选"选项**
   ```python
   if isinstance(val, list):
       if '全选' not in val:
           filters.append(...)
   else:
       if val != '全选':
           filters.append(...)
   ```

### 完整代码模板

见 `docs/ai_context/PANEL_TEMPLATE.md`
```

---

## 🎨 **代码对比**

### **ipywidgets 版本（旧）**

```python
from src.dashboard import DashboardBuilder

dashboard = DashboardBuilder.from_data(df_df, dimensions=[...])

def update_dashboard(controls):
    # controls 是字典 {'年度': '2024', ...}
    year = controls['业务年度']
    ...
    return fig

dashboard.set_update_function(update_dashboard)
dashboard.build()
```

### **Panel 版本（新）**

```python
from src.dashboard import PanelDashboardBuilder
import panel as pn

dashboard = PanelDashboardBuilder.from_data(df_df, dimensions=[...])

@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    # 通过 dashboard.widgets 获取值
    values = {name: w.value for name, w in dashboard.widgets.items()}
    year = values['业务年度']
    ...
    return fig

dashboard.set_update_function(update_dashboard)
dashboard.show()

# ⭐ 新功能：导出 HTML
dashboard.save("output.html")
```

### **关键差异**

| 特性 | ipywidgets | Panel |
|------|-----------|-------|
| 装饰器 | 不需要 | **@pn.depends** |
| 函数参数 | `controls` 字典 | `*args` |
| 获取值 | 直接从参数 | `dashboard.widgets[name].value` |
| 显示 | `build()` | `show()` |
| 导出 HTML | ❌ 需要 Voila | ✅ `save()` |

---

## 📚 **文档位置**

- ✅ Panel Builder: `src/dashboard/panel_builder.py`
- ⏳ AI Context 更新: `docs/ai_context/main.md`（待更新）
- ⏳ Panel 模板: `docs/ai_context/PANEL_TEMPLATE.md`（待创建）
- ⏳ 迁移示例: `notebooks/examples/panel_dashboard_example.ipynb`（待创建）

---

## ⚠️ **注意事项**

1. **保持向下兼容**：旧的 `DashboardBuilder` 仍然可用
2. **推荐新项目使用 Panel**
3. **旧项目可逐步迁移**
4. **Panel 需要额外依赖**：确保安装

---

## 🚀 **下一步**

1. [ ] 完成依赖安装
2. [ ] 测试 Panel 版本
3. [ ] 更新 AI Context
4. [ ] 创建示例 notebook
5. [ ] 更新 Quick Start

---

**迁移进行中...** 🏗️
