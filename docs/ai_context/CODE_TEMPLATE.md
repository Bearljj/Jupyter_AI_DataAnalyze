# AI 生成代码标准模板

## ✅ **完整代码结构**

当用户说"帮我生成仪表盘的分析逻辑"时，AI 应该生成以下完整代码：

```python
# ========================================
# 仪表盘分析逻辑
# ========================================

def update_dashboard(controls):
    """
    仪表盘更新函数
    
    Args:
        controls: 控件值字典，key 是维度字段名
    
    Returns:
        Plotly 图表对象
    """
    # 1. 动态获取所有维度的值
    dim_values = {dim: controls[dim] for dim in selected_dimensions}
    
    # 2. 构建过滤条件（处理"全选"）
    filters = []
    for dim in selected_dimensions:
        value = dim_values[dim]
        if isinstance(value, list):  # multiselect
            if '全选' not in value:
                filters.append(pl.col(dim).is_in(value))
        else:  # dropdown
            if value != '全选':
                filters.append(pl.col(dim) == value)
    
    # 3. 应用过滤
    filtered = df_df
    if filters:
        for f in filters:
            filtered = filtered.filter(f)
    
    # 4. 数据分析（根据业务需求）
    if len(selected_dimensions) > 0:
        group_by_dim = selected_dimensions[0]
        
        # 聚合分析
        result = filtered.group_by(group_by_dim).agg([
            pl.col('总保费').sum().alias('保费'),
            pl.col('总保额').sum().alias('保额'),
            pl.len().alias('保单数')
        ]).sort('保费', descending=True)
        
        # 5. Markdown 输出
        print(f"## 按 {group_by_dim} 分析\\n")
        print(f"### 筛选条件\\n")
        for dim in selected_dimensions:
            val = dim_values[dim]
            if isinstance(val, list):
                print(f"- {dim}: {len(val)} 个选项")
            else:
                print(f"- {dim}: {val}")
        print(f"\\n数据量: {filtered.height:,} 行\\n")
        
        print(f"### Top {min(10, result.height)} {group_by_dim}\\n")
        print_markdown_table(result.head(10))
        
        # 6. 可视化（带单位转换）
        # 检查是否需要转换为万元
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
        
        fig = px.bar(
            result.head(10).to_pandas(),
            x=group_by_dim,
            y=y_col,
            title=f'Top 10 {group_by_dim} 保费排名 {title_suffix}',
            text=y_col
        )
        fig.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
        fig.update_layout(
            height=600,
            autosize=True,
            yaxis_title=y_col,
            showlegend=False
        )
    else:
        # 没有维度，显示总体
        result = filtered.select([
            pl.col('总保费').sum().alias('总保费'),
            pl.col('总保额').sum().alias('总保额'),
            pl.len().alias('保单数')
        ])
        
        print("## 总体分析\\n")
        print_markdown_table(result)
        
        fig = px.bar(x=['总计'], y=[result['总保费'][0]], title='总保费')
    
    return fig

# 绑定分析逻辑
dashboard.set_update_function(update_dashboard)

# ⚠️ 重要：启动仪表盘
dashboard.build()

print("\\n🎉 仪表盘已启动！使用上方的控件进行交互分析")
```

---

## 📋 **关键要点**

### ✅ **必须包含**

1. **动态维度处理**
   ```python
   dim_values = {dim: controls[dim] for dim in selected_dimensions}
   ```

2. **"全选"处理**
   ```python
   if value != '全选':  # dropdown
   if '全选' not in value:  # multiselect
   ```

3. **Markdown 输出**
   ```python
   print_markdown_table(result)
   ```

4. **末尾启动**
   ```python
   dashboard.build()
   ```

### ❌ **不要包含**

1. **不要重新分析维度**
   ```python
   # ❌ 不要
   for col in df_df.columns:
       if df_df[col].dtype == pl.Utf8: ...
   ```

2. **不要重新创建 dashboard**
   ```python
   # ❌ 不要
   dashboard = DashboardBuilder.from_data(...)
   ```

3. **不要硬编码字段名**
   ```python
   # ❌ 不要
   year = controls['业务年度']
   
   # ✅ 应该
   dim_values[selected_dimensions[0]]
   ```

---

## 🎨 **代码结构模板**

```python
def update_dashboard(controls):
    # 1. 动态获取维度值
    dim_values = {dim: controls[dim] for dim in selected_dimensions}
    
    # 2. 构建过滤（处理"全选"）
    filters = []
    for dim in selected_dimensions:
        value = dim_values[dim]
        if isinstance(value, list):
            if '全选' not in value:
                filters.append(pl.col(dim).is_in(value))
        else:
            if value != '全选':
                filters.append(pl.col(dim) == value)
    
    # 3. 应用过滤
    filtered = df_df
    for f in filters:
        filtered = filtered.filter(f)
    
    # 4. 业务分析（根据需求定制）
    # ... 聚合、计算、派生指标等
    
    # 5. Markdown 输出
    print("## 分析报告\\n")
    print_markdown_table(result)
    
    # 6. 可视化
    fig = px...
    return fig

dashboard.set_update_function(update_dashboard)
dashboard.build()  # ← 必须
```

---

## 💡 **变体示例**

### 示例 1: 单维度分析

```python
selected_dimensions = ['业务年度']

def update_dashboard(controls):
    year = controls['业务年度']
    
    if year == '全选':
        # 所有年度汇总
        result = df_df.group_by('业务年度').agg([...])
    else:
        # 单个年度
        result = df_df.filter(pl.col('业务年度') == year).agg([...])
    
    print_markdown_table(result)
    return fig

dashboard.set_update_function(update_dashboard)
dashboard.build()
```

### 示例 2: 多维度分析

```python
selected_dimensions = ['业务年度', '业务险种', '机构名称']

def update_dashboard(controls):
    # 动态处理
    dim_values = {dim: controls[dim] for dim in selected_dimensions}
    
    # 构建过滤
    filters = []
    for dim in selected_dimensions:
        value = dim_values[dim]
        if isinstance(value, list):
            if '全选' not in value:
                filters.append(pl.col(dim).is_in(value))
        else:
            if value != '全选':
                filters.append(pl.col(dim) == value)
    
    # 应用过滤
    filtered = df_df
    for f in filters:
        filtered = filtered.filter(f)
    
    # 使用第一个维度分组
    result = filtered.group_by(selected_dimensions[0]).agg([...])
    
    print_markdown_table(result)
    return px.bar(result.to_pandas(), x=selected_dimensions[0], y='保费')

dashboard.set_update_function(update_dashboard)
dashboard.build()
```

---

## 🎯 **检查清单**

在生成代码前，确保：

- [ ] 使用 `selected_dimensions` 动态处理
- [ ] 处理"全选"选项
- [ ] 使用 `print_markdown_table()` 输出
- [ ] 使用 `pl.len()` 而不是 `pl.count()` ← ⚠️ 重要
- [ ] 金额超过 100 万时转换为"万元" ← ⚠️ 新增
- [ ] 图表自适应占满空间 (autosize=True, height=600) ← ⚠️ 新增
- [ ] 末尾有 `dashboard.build()`
- [ ] 没有硬编码字段名
- [ ] 没有重新分析维度
- [ ] 没有重新创建 dashboard

---

**按照这个模板，AI 生成的代码将完整、正确、可直接运行！** ✅
