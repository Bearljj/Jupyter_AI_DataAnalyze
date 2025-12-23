# 给 AI 的提示模板

当你在 **Quick Start Notebook** 运行到 **Step 5** 后，需要让 AI 生成仪表盘的分析逻辑。

---

## 📋 **标准提示模板**

复制以下内容粘贴给 AI：

```
【框架说明】
我正在使用 Jupyter AI DataAnalyze 框架进行数据分析。
这是一个基于 Polars + Plotly + Jupyter 的 AI 辅助分析框架。

【重要文档】
请阅读 AI Context 文档：/Users/harold/working/Jupyter_AI_DataAnalyze/docs/ai_context/main.md

【当前状态】
✅ 已完成：
- Step 1: 环境已初始化
- Step 2: 数据已加载（df_df 变量可用）
- Step 3: AI Context 已生成
- Step 4: 维度已选择
- Step 5: 仪表盘对象已创建（dashboard 变量可用）

【我选择的维度】
selected_dimensions = ['业务年度', '业务险种']

【数据概览】
[从 Step 3 复制 session.get_ai_context() 的输出]

【需要你做的】
请生成仪表盘的分析逻辑代码，要求：

1. 动态使用 selected_dimensions（不要硬编码字段名）
2. 处理"全选"选项（dropdown 和 multiselect 都有"全选"）
3. 使用 print_markdown_table() 输出表格
4. 使用 pl.len() 而不是 pl.count()
5. 代码末尾必须加上 dashboard.build()

【分析需求】
我想分析 [描述你的分析需求，例如：]
- 各年度各险种的保费排名
- 显示 Top 10
- 包含保费、保单数等指标
```

---

## 🎯 **精简版（推荐）**

如果 AI 已经熟悉框架，可以用精简版：

```
【Quick Start - Step 5】
我已完成：
- df_df: 数据已加载
- selected_dimensions = ['业务年度', '业务险种'] 
- dashboard: 仪表盘已创建

请生成 update_dashboard 函数，要求：
✅ 动态使用 selected_dimensions
✅ 处理"全选"选项
✅ 使用 print_markdown_table() 和 pl.len()
✅ 末尾加 dashboard.build()

分析需求：按年度和险种分析保费，显示 Top 10
```

---

## 📝 **详细版（首次使用）**

第一次使用时，提供完整信息：

```
【项目】Jupyter AI DataAnalyze 框架

【AI Context】
请先阅读：/Users/harold/working/Jupyter_AI_DataAnalyze/docs/ai_context/main.md

核心要点：
1. 这是一个 AI 辅助数据分析框架
2. 数据通过 DataSession 加载，全局可用（df_df）
3. 仪表盘通过 DashboardBuilder.from_data() 自动创建
4. AI 只需生成分析逻辑（update_dashboard 函数）

【当前 Notebook 状态】
我在 quick_start.ipynb 中，已完成：

Step 1-2: 数据加载完成
- df_df 变量可用
- 776,739 行 × 68 列数据
- 已自动分析维度字段

Step 3: AI Context
[粘贴 session.get_ai_context() 输出]

Step 4: 维度选择
selected_dimensions = ['业务年度', '业务险种']

Step 5: 仪表盘创建
dashboard 对象已创建，包含：
- "业务年度" 控件（dropdown，10 个选项 + 全选）
- "业务险种" 控件（multiselect，35 个选项 + 全选）

【你的任务】
生成完整的分析逻辑代码，包括：

1. update_dashboard(controls) 函数
   - 动态获取维度值：dim_values = {dim: controls[dim] for dim in selected_dimensions}
   - 处理"全选"：if value != '全选' (dropdown), if '全选' not in value (multiselect)
   - 过滤数据 + 聚合分析
   - Markdown 输出：print_markdown_table(result)
   - 返回 Plotly 图表

2. 绑定函数
   dashboard.set_update_function(update_dashboard)

3. 启动仪表盘
   dashboard.build()

【重要提醒】
- ✅ 使用 pl.len() 而不是 pl.count()（已弃用）
- ✅ 动态处理 selected_dimensions，不要硬编码字段名
- ❌ 不要重新创建 dashboard
- ❌ 不要重新分析维度

【分析需求】
我想要：
- 按选择的年度和险种进行分析
- 显示各险种的保费排名（Top 10）
- 包含保费、保单数等核心指标
- 使用柱状图可视化
```

---

## 💡 **最佳实践**

### 1️⃣ **第一次交互**
使用**详细版**，让 AI 充分理解框架

### 2️⃣ **后续交互**
使用**精简版**，快速说明需求

### 3️⃣ **复杂需求**
在精简版基础上，详细描述分析逻辑

---

## 🎨 **示例对话**

### **你说**:
```
【Quick Start - Step 5】
已完成数据加载和仪表盘创建。
selected_dimensions = ['业务年度', '业务险种', '机构名称']

请生成分析逻辑：
- 按年度、险种、机构三个维度进行筛选
- 使用第一个维度（年度）进行分组
- 显示各年度的总保费和保单数
- Top 10 + 柱状图
- 记得处理"全选"，使用 pl.len()，末尾加 dashboard.build()
```

### **AI 会生成**:
```python
def update_dashboard(controls):
    # 动态获取维度值
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
    
    # 分组聚合
    result = filtered.group_by(selected_dimensions[0]).agg([
        pl.col('总保费').sum().alias('保费'),
        pl.len().alias('保单数')
    ]).sort('保费', descending=True)
    
    # Markdown 输出
    print(f"## 按 {selected_dimensions[0]} 分析\n")
    print_markdown_table(result.head(10))
    
    # 可视化
    fig = px.bar(result.head(10).to_pandas(), 
                 x=selected_dimensions[0], y='保费')
    return fig

dashboard.set_update_function(update_dashboard)
dashboard.build()
```

---

## 📚 **快速参考**

| 情况 | 使用模板 | 关键信息 |
|-----|---------|---------|
| **第一次** | 详细版 | AI Context + 完整说明 |
| **已熟悉** | 精简版 | 维度 + 需求 |
| **复杂分析** | 精简版 + 详细需求 | 具体分析逻辑 |

---

## ✅ **检查清单**

发送给 AI 前，确保包含：

- [ ] 说明是 Quick Start Notebook
- [ ] 当前完成到 Step 5
- [ ] 提供 selected_dimensions
- [ ] 说明分析需求
- [ ] 提醒关键要点（全选、pl.len()、dashboard.build()）
- [ ] （首次）提供 AI Context 路径

---

**使用这些模板，AI 就能生成正确的代码！** ✅
