# Jupyter AI DataAnalyze - AI Context (Updated 2025-12-21)

**版本：** 2.1  
**最后更新：** 2025-12-21  
**重要更新：** 仪表盘自动化 + Markdown 输出规范 + 工作流澄清

这是 Jupyter AI DataAnalyze 框架的核心 AI Context 文档。复制相关部分给 AI，帮助它理解框架并生成正确的代码。

---

## ⚠️ **重要：工作流澄清**

### 在 Quick Start Notebook 中

如果用户正在使用 `quick_start.ipynb`，**工作已经部分完成**：

**本地已完成**（用户操作）：
- ✅ Step 2: 数据已加载，维度已自动分析
- ✅ Step 4: 用户已选择维度 → `selected_dimensions` 变量
- ✅ Step 5: 仪表盘已创建 → `dashboard` 对象

**AI 的职责**（仅此而已）：
- ✅ 生成 `update_dashboard(controls)` 函数
- ✅ **动态**使用 `selected_dimensions` 变量（不要硬编码字段名！）
- ✅ 使用 `print_markdown_table()` 输出
- ✅ **在代码末端加上 `dashboard.build()`** 启动仪表盘

**AI 不要做**：
- ❌ 不要重新分析维度字段
- ❌ 不要创建 `dashboard` 对象
- ❌ 不要运行 `from_data()`
- ❌ 不要硬编码字段名（如 `controls['业务年度']`）

### 示例：用户请求

**用户说**："帮我生成仪表盘的分析逻辑"

**AI 应该生成（动态方式）**：
```python
def update_dashboard(controls):
    # ✅ 动态获取维度值
    dim_values = {dim: controls[dim] for dim in selected_dimensions}
    
    # 构建过滤条件
    filters = []
    for dim in selected_dimensions:
        value = dim_values[dim]
        if isinstance(value, list):  # multiselect
            if '全选' not in value:  # 排除"全选"选项
                filters.append(pl.col(dim).is_in(value))
        else:  # dropdown
            if value != '全选':  # 排除"全选"
                filters.append(pl.col(dim) == value)
    
    # 应用过滤
    filtered = df_df
    if filters:
        for f in filters:
            filtered = filtered.filter(f)
    
    # 使用第一个维度进行分组（如果有的话）
    if len(selected_dimensions) > 0:
        group_by_dim = selected_dimensions[0]
        result = filtered.group_by(group_by_dim).agg([
            pl.col('总保费').sum().alias('保费'),
            pl.len().alias('保单数')
        ]).sort('保费', descending=True)
        
        print(f"## 按 {group_by_dim} 分析\n")
        print_markdown_table(result.head(10))
        
        fig = px.bar(result.head(10).to_pandas(), x=group_by_dim, y='保费')
    else:
        # 没有维度，显示总体
        result = filtered.select([
            pl.col('总保费').sum().alias('保费'),
            pl.len().alias('保单数')
        ])
        print_markdown_table(result)
        fig = px.bar(x=['总计'], y=[result['保费'][0]])
    
    return fig

dashboard.set_update_function(update_dashboard)

# ⚠️ 重要：最后必须调用 build() 启动仪表盘
dashboard.build()
```

**❌ AI 不要生成（硬编码方式）**：
```python
def update_dashboard(controls):
    # ❌ 错误：硬编码字段名
    year = controls['业务年度']
    products = controls['业务险种']
    # 如果用户选了不同的维度，这会报错！
```

**AI 不应该生成**：
```python
# ❌ 不要重新分析维度
dimensions_info = []
for col in df_df.columns: ...

# ❌ 不要重新创建 dashboard
dashboard = DashboardBuilder.from_data(...)
```

---

## 🆕 重要更新（2025-12-21)

### 1. 仪表盘创建已简化
- ✅ 本地 Notebook 自动分析维度
- ✅ AI 只负责生成分析逻辑
- ✅ 不再需要手动写控件代码

### 2. 输出必须使用 Markdown 格式
- ✅ 所有 DataFrame 输出使用 `print_markdown_table()`
- ✅ 分析摘要使用 Markdown 标题和列表
- ✅ 让输出在 Jupyter 中渲染为漂亮的表格

### 3. ⚠️ Polars API 更新
- ✅ **使用 `pl.len()` 而不是 `pl.count()`**
- ❌ `pl.count()` 已在 Polars 0.20.5 中弃用
- ✅ 正确写法：`pl.len().alias('数量')`

**示例**:
```python
# ❌ 错误（会产生 DeprecationWarning）
result = df.agg([
    pl.col('总保费').sum().alias('保费'),
    pl.count().alias('保单数')  # 已弃用！
])

# ✅ 正确
result = df.agg([
    pl.col('总保费').sum().alias('保费'),
    pl.len().alias('保单数')  # 使用 pl.len()
])
```

### 4. 📊 可视化规范

#### A. 图表尺寸
- ✅ **自适应占满显示空间**
- ✅ 设置合适的高度和宽度
- ✅ 响应式布局
- ✅ **移除 JupyterLab Cell 宽度限制**（重要！）

**移除 Cell 宽度限制**:
```python
from IPython.display import HTML, display

# 在 notebook 开头运行一次
display(HTML("""
<style>
    .jp-Notebook-cell { max-width: none !important; }
    .jp-OutputArea-output { max-width: none !important; }
</style>
"""))
```

**图表自适应设置**:
```python
# ✅ 正确：自适应尺寸
fig.update_layout(
    height=600,                    # 固定高度
    width=None,                    # 自适应宽度
    autosize=True,                 # 自动调整
    margin=dict(l=50, r=50, t=80, b=50)
)
```

#### B. 金额单位自动转换
- ✅ **金额超过 100 万时，自动转换为"万元"**
- ✅ 更新坐标轴标签和标题

```python
# 检查最大值并转换单位
max_value = result['保费'].max()

if max_value > 1_000_000:
    # 转换为万元
    result = result.with_columns([
        (pl.col('保费') / 10000).alias('保费（万元）')
    ])
    y_col = '保费（万元）'
    y_label = '保费（万元）'
else:
    y_col = '保费'
    y_label = '保费（元）'

# 创建图表
fig = px.bar(result.to_pandas(), x='险种', y=y_col, 
             labels={y_col: y_label})
fig.update_layout(
    yaxis_title=y_label,
    height=600,
    autosize=True
)
```

**完整示例**:
```python
# 聚合数据
result = filtered.group_by('业务险种').agg([
    pl.col('总保费').sum().alias('保费'),
    pl.len().alias('保单数')
])

# 检查并转换单位
max_premium = result['保费'].max()
if max_premium > 1_000_000:
    result = result.with_columns([
        (pl.col('保费') / 10000).alias('保费（万元）')
    ])
    y_col = '保费（万元）'
    title_suffix = '（单位: 万元）'
else:
    y_col = '保费'
    title_suffix = '（单位: 元）'

# 创建图表
fig = px.bar(
    result.to_pandas(), 
    x='业务险种', 
    y=y_col,
    title=f'各险种保费排名 {title_suffix}',
    text=y_col
)

# 自适应布局
fig.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
fig.update_layout(
    height=600,
    autosize=True,
    yaxis_title=y_col,
    showlegend=False,
    margin=dict(l=60, r=30, t=80, b=60)
)
```

---

## 📦 框架概述

这是一个专为 AI 协作设计的数据分析框架，基于 Polars + Plotly + Jupyter Lab。

**核心设计理念：**
- 数据一次加载，全局可用（通过 DataSession）
- 仪表盘自动创建，AI 只写业务逻辑
- 输出使用 Markdown 格式，清晰美观

---

## 🔧 核心 API

### 1. 数据会话（src.session.DataSession）

```python
from src.session import DataSession

# 创建会话
session = DataSession()

# 加载数据到全局命名空间
session.load("alldata", alias="df")  # 创建全局变量 df_df

# 现在可以直接使用 df_df，无需重复加载！

# 查看会话摘要
session.summary()

# 生成 AI Context（包含所有已加载数据的详细信息）
print(session.get_ai_context())  # 复制这个给 AI
```

### 2. 交互式仪表盘

---

## 🚨 **重要：必须使用 Panel Dashboard**

**从现在开始，所有交互式仪表盘都必须使用 `PanelDashboardBuilder`，不再使用旧的 `DashboardBuilder`（ipywidgets）。**

**原因**：
- ✅ **支持导出静态 HTML**（控件 + 图表都可交互）
- ✅ 单个文件，离线可用，可邮件分享
- ✅ 图表自动占满宽度
- ❌ 旧的 `DashboardBuilder` **不支持 HTML 导出**，已废弃

---

#### **Panel Dashboard - 标准流程**
- ✅ 图表自动占满宽度
- ✅ 完整文档：`docs/ai_context/PANEL_GUIDE.md`

**⚠️ 关键前置步骤：移除 JupyterLab 宽度限制**

```python
# ========================================
# 必须首先运行：移除 JupyterLab 宽度限制
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

print("✅ JupyterLab 宽度限制已移除")
```

**使用方法**：

```python
from src.dashboard import PanelDashboardBuilder
import panel as pn
import polars as pl
import plotly.express as px

# 初始化 Panel（全局 stretch_width）
pn.extension('plotly', sizing_mode='stretch_width')

# Step 1: 创建仪表盘（自动生成控件）
dashboard = PanelDashboardBuilder.from_data(
    df_df,
    dimensions=['业务年度', '业务险种'],
    title="📊 保费分析仪表盘"
)

# Step 2: 定义更新函数
# ⚠️ 关键：必须使用 @pn.depends 装饰器
@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):  # 参数是 *args
    # A. 获取控件值
    values = {name: widget.value 
              for name, widget in dashboard.widgets.items()}
    
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
        pl.len().alias('保单数')
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
    print("## 分析结果\\n")
    print_markdown_table(result.head(10))
    
    # F. 图表（自适应宽度）
    fig = px.bar(result.to_pandas(), x='业务险种', y=y_col)
    fig.update_layout(
        height=600,
        autosize=True,  # ← 自动占满宽度
        showlegend=False
    )
    
    return fig

# Step 3: 绑定和显示
dashboard.set_update_function(update_dashboard)
dashboard.show()  # Jupyter 中显示

# Step 4: 导出 HTML（可选）
dashboard.save("保费分析.html")
```

**Panel 关键规则**：
1. 使用 `@pn.depends(*dashboard.widgets.values())` 装饰器
2. 函数参数是 `*args`（不是 controls 字典）
3. 通过 `dashboard.widgets` 字典获取控件值
4. 处理"全选"选项
5. 图表设置 `autosize=True`

---

#### **ipywidgets Dashboard（备选 - 仅 Jupyter）**

#### **🆕 新方式：自动创建（推荐）**

```python
from src.dashboard import DashboardBuilder

# Step 1: AI 识别维度字段（见后文指南）
# 用户确认后...

# Step 2: 自动创建仪表盘控件
dashboard = DashboardBuilder.from_data(
    df_df,
    dimensions=['业务年度', '业务险种', '机构名称'],
    title="保费分析仪表盘"
)

# Step 3: AI 生成分析逻辑
def update_dashboard(controls):
    """
    仪表盘更新函数
    
    Args:
        controls: 控件值字典，如 {'业务年度': '2024', '业务险种': [...]}
    
    Returns:
        Plotly 图表对象
    """
    # 获取控件值
    year = controls['业务年度']
    products = controls['业务险种']  # multiselect 返回列表
    
    # 过滤数据
    filtered = df_df.filter(
        (pl.col('业务年度') == year) &
        (pl.col('业务险种').is_in(products))
    )
    
    # 聚合分析
    result = filtered.group_by('业务险种').agg([
        pl.col('总保费').sum().alias('保费'),
        pl.len().alias('保单数')
    ])
    
    # 📊 输出摘要表（使用 Markdown）
    from src.utils import print_markdown_table
    print("## 分析摘要")
    print_markdown_table(result)
    
    # 创建可视化
    import plotly.express as px
    fig = px.bar(result.to_pandas(), x='业务险种', y='保费')
    
    return fig

# Step 4: 绑定并启动
dashboard.set_update_function(update_dashboard)
dashboard.build()
```

#### ⚙️ 旧方式：手动创建（仍然支持）

```python
# 如果需要更精细的控制，可以手动创建
dashboard = DashboardBuilder("自定义仪表盘")
dashboard.add_dropdown('year', '年度', options=[2020, 2021, 2022])
dashboard.add_slider('threshold', '阈值', min_val=0, max_val=100)
# ... 手动添加所有控件
```

### 3. 🆕 Markdown 输出（src.utils.polars_display）

```python
from src.utils import print_markdown_table, enable_polars_markdown_display

# 方式1：手动使用（推荐用于仪表盘）
result = df.group_by('category').agg(pl.col('sales').sum())
print_markdown_table(result)  # 输出为 Markdown 表格

# 方式2：自动启用（Notebook 顶部运行一次）
enable_polars_markdown_display()
# 之后所有 DataFrame 自动以表格格式显示
```

---

## 📊 维度字段识别指南（重要！）

### AI 的职责

在创建仪表盘前，你需要识别哪些字段适合作为维度。

### 识别标准

**维度字段**（用于分组/筛选）：
- ✅ 字符串类型（String）或日期类型（Date）
- ✅ 描述业务对象的属性（"是什么"、"在哪里"、"什么时候"）
- ✅ 有固定的取值范围（即使很大，如机构名称可能有500+个）
- ✅ 用于 `group_by()`, `filter()`, 控件筛选

**度量字段**（用于聚合计算）：
- ✅ 数值类型（Float64, Int64）
- ✅ 描述数量、金额、比率
- ✅ 用于 `sum()`, `mean()`, `count()`等

### 识别流程

```python
# 1. 分析数据结构
print("## 数据结构分析\n")

dimensions = []  # 维度字段
metrics = []     # 度量字段

for col in df_df.columns:
    dtype = str(df_df[col].dtype)
    n_unique = df_df[col].n_unique()
    
    if dtype == 'String' or dtype.startswith('Date'):
        # 潜在维度
        dimensions.append({
            'name': col,
            'type': dtype,
            'unique_values': n_unique
        })
    elif dtype in ['Float64', 'Int64']:
        # 潜在度量
        metrics.append({
            'name': col,
            'type': dtype
        })

# 2. 输出建议
print("### 建议的维度字段:\n")
for dim in dimensions:
    n = dim['unique_values']
    control_type = ""
    warning = ""
    
    if n <= 10:
        control_type = "dropdown"
    elif n <= 50:
        control_type = "multiselect"
    else:
        control_type = "multiselect"
        warning = " ⚠️ 选项较多，Phase 2 建议使用级联"
    
    print(f"- **{dim['name']}** ({n} 个值) → {control_type}{warning}")

print("\n### 建议的度量字段:\n")
for met in metrics:
    print(f"- **{met['name']}** ({met['type']})")

# 3. 让用户确认
print("\n💡 **请确认要使用哪些维度字段创建仪表盘**")
```

### 重要说明

**❌ 错误理解**：
- "唯一值多 = 不是维度" ← 错！

**✅ 正确理解**：
- 唯一值数量**不决定是否为维度**
- 唯一值数量**决定控件类型和体验**
- 县级机构（500+个）依然是维度，只是需要更好的交互（Phase 2 级联）

**控件类型映射**：

| 唯一值数量 | 控件类型 | 默认选择策略 |
|-----------|----------|-------------|
| ≤ 10      | dropdown（单选） | 最新值或第一个 |
| 11-50     | multiselect（多选） | 前3个 |
| 51-500    | multiselect | 前5个 + 提示"选项较多" |
| 500+      | multiselect | 前5个 + 建议 Phase 2 级联 |

---

## 📝 Markdown 输出规范（必须遵守！）

### 规则

1. **DataFrame 输出**：使用 `print_markdown_table()`
2. **摘要标题**：使用 Markdown 标题 `##`
3. **列表**：使用 Markdown 列表格式
4. **不要使用**：纯 `print(df)` - 会显示为纯文本

### 示例

```python
# ✅ 正确：Markdown 格式
from src.utils import print_markdown_table

print("## 分析结果\n")
print("### Top 10 险种\n")
print_markdown_table(top10)

print("\n### 关键指标\n")
print(f"- 总保费: {total:,.0f} 元")
print(f"- 平均成本率: {avg_ratio:.2f}%")

# ❌ 错误：纯文本
print(top10)  # 显示为难看的纯文本
```

### 在仪表盘中使用

```python
def update_dashboard(controls):
    # ... 分析逻辑 ...
    
    # 输出摘要（Markdown 格式）
    print("## 筛选结果摘要\n")
    print(f"- 筛选年度: {controls['业务年度']}")
    print(f"- 筛选险种: {', '.join(controls['业务险种'])}")
    print(f"- 数据量: {filtered.height:,} 行\n")
    
    print("### 汇总数据\n")
    print_markdown_table(summary)
    
    # 返回图表
    return fig
```

---

## 💡 常见分析模式

### 模式 1: 基础数据探索

```python
import polars as pl

# 查看数据概览
df.head()
df.describe()

# 列信息
df.columns
df.dtypes

# 使用 Markdown 输出
from src.utils import print_markdown_table
print("## 数据概览")
print_markdown_table(df.head(10))
```

### 模式 2: 过滤和聚合

```python
# 过滤
filtered = df.filter(
    (pl.col('业务年度') == '2024') &
    (pl.col('总保费') > 10000)
)

# 聚合
result = filtered.group_by('业务险种').agg([
    pl.col('总保费').sum().alias('保费'),
    pl.len().alias('保单数'),
    pl.col('总保费').mean().alias('平均保费')
])

# Markdown 输出
print("## 聚合结果")
print_markdown_table(result)
```

### 模式 3: 可视化

```python
import plotly.express as px

# 创建图表
fig = px.bar(result.to_pandas(), x='业务险种', y='保费',
             title='各险种保费对比')

# 配置
fig.update_layout(height=500)
fig.show()
```

---

## 🎯 完整工作流示例

```python
# ========== Cell 1: 初始化 ==========
from src.session import DataSession
from src.utils import enable_polars_markdown_display
import polars as pl
import plotly.express as px

# 启用 Markdown 显示
enable_polars_markdown_display()

# 加载数据
session = DataSession()
session.load("alldata", alias="df")
session.summary()

# ========== Cell 2: AI 分析维度 ==========
print("## 维度分析\n")

# AI 生成的维度识别代码
for col in df_df.columns:
    if df_df[col].dtype == pl.Utf8:
        n = df_df[col].n_unique()
        if n < 1000:  # 合理的维度范围
            print(f"- {col}: {n} 个值")

# 用户确认：['业务年度', '业务险种', '机构名称']

# ========== Cell 3: 创建仪表盘 ==========
from src.dashboard import DashboardBuilder

dashboard = DashboardBuilder.from_data(
    df_df,
    dimensions=['业务年度', '业务险种'],
    title="保费分析"
)

# ========== Cell 4: AI 生成分析逻辑 ==========
from src.utils import print_markdown_table

def update_dashboard(controls):
    year = controls['业务年度']
    products = controls['业务险种']
    
    # 过滤
    data = df_df.filter(
        (pl.col('业务年度') == year) &
        (pl.col('业务险种').is_in(products))
    )
    
    # 聚合
    summary = data.group_by('业务险种').agg([
        pl.col('总保费').sum().alias('保费'),
        pl.col('总保额').sum().alias('保额')
    ]).sort('保费', descending=True)
    
    # Markdown 输出
    print(f"## {year}年 险种分析\n")
    print(f"- 筛选险种: {len(products)} 个")
    print(f"- 数据量: {data.height:,} 行\n")
    print_markdown_table(summary)
    
    # 可视化
    fig = px.bar(summary.to_pandas(), x='业务险种', y='保费')
    return fig

# ========== Cell 5: 启动 ==========
dashboard.set_update_function(update_dashboard)
dashboard.build()
```

---

## 🔔 重要提示

### 对 AI 的说明

1. **数据已加载**：如果看到 `df_df` 等变量，它们已在 Jupyter 中可用，**无需再次加载**

2. **仪表盘创建**：使用 `from_data()` 自动创建，**不要**手写 `add_dropdown()` 等代码

3. **Markdown 输出**：所有表格必须使用 `print_markdown_table()`

4. **维度识别**：唯一值多≠不是维度，只是需要不同的控件策略

5. **Phase 2 功能**：级联关系、自动维度检测 - 现在不要使用

---

## 📚 API 快速参考

```python
# 数据加载

## 单文件加载
session.load("data", alias="name")  # → 创建 df_name

## 多文件加载（新功能！）

### 场景 1: 合并同构文件（concat）
```python
# 合并多个结构相同的文件
session.load_multiple_concat(
    ['data/2022.parquet', 'data/2023.parquet', 'data/2024.parquet'],
    alias='all_years'
)
# 使用: all_years_df

# 使用 glob 模式
session.load_multiple_concat(
    ['data/year_*.parquet'],
    alias='all_data'
)
```

### 场景 2: 关联异构文件（join）
```python
# 多表 join
session.load_multiple_join(
    files={
        'policy': 'policy.parquet',
        'customer': 'customer.parquet',
        'product': 'product.parquet'
    },
    joins=[
        {'left': 'policy', 'right': 'customer', 'on': '客户ID', 'how': 'left'},
        {'left': 'policy', 'right': 'product', 'on': '产品代码', 'how': 'left'}
    ],
    result_alias='enriched'
)
# 使用: enriched_df
```

### 场景 3: 批量加载独立文件
```python
session.load_multiple_independent({
    'sales': 'sales.parquet',
    'hr': 'hr.parquet',
    'finance': 'finance.parquet'
})
# 使用: sales_df, hr_df, finance_df
```

**详细文档**: docs/MULTIPLE_FILES_GUIDE.md

# 仪表盘（新方式）
DashboardBuilder.from_data(df, dimensions=[...])

# Markdown 输出
print_markdown_table(df)
enable_polars_markdown_display()

# Polars 常用
df.filter(...)
df.group_by(...).agg(...)
df.sort(..., descending=True)
df.head(n)

# Plotly 可视化
px.bar(df.to_pandas(), x=..., y=...)
px.line(...)
px.scatter(...)
```

---

**这个 AI Context 持续更新！**  
当框架添加新功能时，这个文档会更新。

**版本历史**：
- v2.0 (2025-12-21): 仪表盘自动化 + Markdown 输出规范
- v1.0 (2024-12-21): 初始版本
