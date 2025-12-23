# 🔧 Quick Start Notebook 仪表盘数据问题修复指南

## 📋 问题描述

在 `notebooks/templates/quick_start.ipynb` 中：
- **Cell 3-6**: 使用了硬编码的示例数据（`df_example`）
- **Cell 7**: AI 生成的代码使用了真实数据（`df_df`）
- **Cell 8**: 启动仪表盘时，仍然引用的是示例数据的变量

导致仪表盘显示的是随机生成的示例数据，而不是你上传的真实数据。

## ✅ 解决方案

### 方法 1: 快速修复（推荐）

1. **打开 `quick_start.ipynb`**

2. **在 Cell 7（AI 生成的分析代码）之后，添加一个新的单元格**，粘贴以下代码：

```python
# ================================================================
# 📊 使用真实数据创建仪表盘
# ================================================================

from src.dashboard import DashboardBuilder
import polars as pl
import plotly.express as px

# 从真实数据中提取选项
product_column = '业务险种'  # 👈 根据你的数据字段修改
year_options = df_df.select(pl.col('业务年度').unique()).to_series().sort().to_list()

# 创建仪表盘
dashboard_real = DashboardBuilder("真实数据分析仪表盘")

dashboard_real.add_dropdown(
    name='year',
    label='选择年度',
    options=year_options,
    default=year_options[-1]  # 默认最新年度
)

# 定义更新函数
def update_dashboard(controls):
    year = controls['year']
    
    # 过滤数据
    filtered = df_df.filter(pl.col('业务年度') == year)
    
    # 按险种汇总
    summary = filtered.group_by(product_column).agg([
        pl.col('总保费').sum().alias('保费'),
        pl.col('总已决赔款').sum().alias('赔款'),
        pl.len().alias('保单数')
    ]).sort('保费', descending=True).head(10)
    
    # 创建图表
    fig = px.bar(
        summary.to_pandas(),
        x=product_column,
        y='保费',
        title=f'{year}年 Top 10 险种保费',
        text='保费'
    )
    
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(height=500)
    
    return fig

# 绑定函数
dashboard_real.set_update_function(update_dashboard)

# 构建并显示
dashboard_real.build()
```

3. **运行这个新单元格**，你就会看到基于真实数据的仪表盘！

### 方法 2: 使用预制的单元格代码

我已经为你创建了一个更智能的版本：

1. **打开文件**：`notebooks/templates/real_data_dashboard_cell.py`

2. **复制全部内容**

3. **在 Notebook 中创建新单元格**，粘贴并运行

4. **再创建一个单元格**，运行：
   ```python
   # 启动真实数据仪表盘
   dashboard_real.build()
   ```

这个版本会自动检测你的数据字段并创建相应的控件。

### 方法 3: 删除示例数据单元格

如果你不需要示例数据：

1. **打开 `quick_start.ipynb`**
2. **删除或注释掉 Cell 3-6**（示例数据相关的单元格）
3. **保留 Cell 7**（AI 生成的真实数据分析）
4. **按照方法1添加新的仪表盘代码**

## 📊 字段名称对照

根据你的数据（从 Cell 7 输出可以看到），以下是可用的字段：

### 常用维度字段：
- `业务年度` - 年份
- `业务险种` - 产品/险种类型
- `机构名称` - 分支机构
- `机构代码` - 机构编码
- `业务来源` - 业务渠道
- `风险等级` - 风险分类
- `占用性质名称` - 占用类型
- `行业类别名称` - 行业分类
- `境内境外` - 地域分类

### 常用度量字段：
- `总保费` - 总保费金额
- `自留保费` - 自留保费
- `总保额` - 保额
- `总已决赔款` - 已决赔款
- `总未决赔款` - 未决赔款
- `手续费` - 手续费

## 🎨 仪表盘进阶示例

### 示例1: 多维度分析仪表盘

```python
from src.dashboard import DashboardBuilder

dashboard = DashboardBuilder("多维度保费分析")

# 添加多个控件
dashboard.add_dropdown(
    'year', '业务年度',
    options=df_df.select(pl.col('业务年度').unique()).to_series().to_list()
).add_dropdown(
    '险种', '业务险种',
    options=df_df.select(pl.col('业务险种').unique()).to_series().to_list()[:20]
).add_multiselect(
    'regions', '选择机构',
    options=df_df.select(pl.col('机构名称').unique()).to_series().to_list()[:15],
    default=[]
)

def update(controls):
    # 逐步过滤
    data = df_df.filter(pl.col('业务年度') == controls['year'])
    data = data.filter(pl.col('业务险种') == controls['险种'])
    
    if controls['regions']:
        data = data.filter(pl.col('机构名称').is_in(controls['regions']))
    
    # 创建月度趋势
    monthly = data.group_by('保险起期').agg([
        pl.col('总保费').sum().alias('保费'),
        pl.len().alias('保单数')
    ]).sort('保险起期')
    
    fig = px.line(monthly.to_pandas(), x='保险起期', y='保费', markers=True)
    return fig

dashboard.set_update_function(update).build()
```

### 示例2: 成本率分析仪表盘

```python
dashboard_loss = DashboardBuilder("成本率分析")

dashboard_loss.add_slider(
    'years', '年份数量',
    min_val=1, max_val=10, step=1, default=5
)

def update_loss(controls):
    n_years = int(controls['years'])
    
    # 取最近N年数据
    recent = df_df.group_by('业务年度').agg([
        pl.col('总保费').sum().alias('保费'),
        (pl.col('总已决赔款').sum() + pl.col('总未决赔款').sum()).alias('赔款')
    ]).with_columns(
        (pl.col('赔款') / pl.col('保费') * 100).alias('成本率')
    ).sort('业务年度').tail(n_years)
    
    fig = px.bar(recent.to_pandas(), x='业务年度', y='成本率', text='成本率')
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="警戒线")
    return fig

dashboard_loss.set_update_function(update_loss).build()
```

## 🚀 最佳实践

### 1. 先探索数据
在创建仪表盘前，先了解你的数据：
```python
# 查看所有字段
df_df.columns

# 查看某字段的唯一值数量
df_df.select(pl.col('业务险种').n_unique())

# 查看某字段的所有唯一值
df_df.select(pl.col('业务险种').unique()).to_series().to_list()
```

### 2. 限制选项数量
避免在下拉菜单中显示过多选项：
```python
options = df_df.select(pl.col('字段').unique()).to_series().to_list()
options = options[:20]  # 限制最多20个
```

### 3. 使用默认值
为控件设置合理的默认值：
```python
years = sorted(df_df.select(pl.col('业务年度').unique()).to_series().to_list())
dashboard.add_dropdown('year', '年度', options=years, default=years[-1])  # 默认最新年
```

### 4. 性能优化
对于大数据集，在更新函数中进行聚合：
```python
def update(controls):
    # 先过滤再聚合，避免处理全量数据
    filtered = df_df.filter(pl.col('年度') == controls['year'])
    summary = filtered.group_by('类别').agg(...)
    return create_chart(summary)
```

## 📚 相关文档

- [DashboardBuilder API 文档](../../docs/api/dashboard.md)
- [Polars 数据处理](https://pola-rs.github.io/polars/)
- [Plotly 可视化](https://plotly.com/python/)

---

## 🆘 需要帮助？

如果仍然看到示例数据，检查：

1. ✅ 数据是否已加载：`'df_df' in globals()`
2. ✅ 更新函数是否使用了 `df_df` 而不是 `df_example`
3. ✅ dashboard.set_update_function() 是否已调用
4. ✅ dashboard.build() 是否在设置函数之后

**调试技巧**：
```python
# 在更新函数中添加打印
def update(controls):
    print(f"控件值: {controls}")
    print(f"数据量: {df_df.height} 行")
    ...
```

---

**现在你可以创建完全基于真实数据的交互式仪表盘了！** 🎉
