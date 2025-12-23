# 工作流澄清 - 人工 vs AI 的职责分工

## 🎯 **核心原则**

**本地 Notebook（人工操作）**： 准备数据和仪表盘框架  
**AI 协作**：生成业务分析逻辑

---

## 📋 **Quick Start 工作流详解**

### **Step 1-2: 准备阶段（👤 人工）**

```
👤 人工在 Notebook 中：
  ├─ Step 1: 导入模块，启用 Markdown
  └─ Step 2: 加载数据 + 自动分析维度
         ↓
       输出: available_dimensions = ['业务年度', '业务险种', '机构名称', ...]
             dimensions_info = [{field, unique_values, control}, ...]
```

### **Step 3: 生成 AI Context（👤 人工）**

```
👤 人工：运行 session.get_ai_context()
         复制输出给 AI
```

### **Step 4-5: 选择与创建（👤 人工）**

```
👤 人工在 Notebook 中：
  ├─ Step 4: 选择维度
  │    selected_dimensions = ['业务年度', '业务险种']
  │
  └─ Step 5: 创建仪表盘
       dashboard = DashboardBuilder.from_data(df_df, dimensions=selected_dimensions)
         ↓
       输出: dashboard 对象已创建，等待分析逻辑
```

### **Step 5 (续): 分析逻辑（🤖 AI）**

```
👤 人工：告诉 AI "帮我生成仪表盘的分析逻辑"

🤖 AI 生成：
  def update_dashboard(controls):
      # 1. 获取控件值
      year = controls['业务年度']
      products = controls['业务险种']
      
      # 2. 过滤 + 聚合
      filtered = df_df.filter(...)
      result = filtered.group_by(...).agg(...)
      
      # 3. Markdown 输出
      print_markdown_table(result)
      
      # 4. 可视化
      return fig
  
  dashboard.set_update_function(update_dashboard)

👤 人工：复制 AI 的代码，运行
```

### **Step 5 (完): 启动（👤 人工）**

```
👤 人工：dashboard.build()
```

---

## ⚠️ **关键：AI 不要重复的工作**

### ❌ **AI 不应该做**

```python
# ❌ 错误1：重新分析维度
dimensions_info = []
for col in df_df.columns:
    if df_df[col].dtype == pl.Utf8:
        n = df_df[col].n_unique()
        dimensions_info.append(...)

# ❌ 错误2：重新创建 dashboard
dashboard = DashboardBuilder.from_data(
    df_df,
    dimensions=['业务年度', '业务险种']  # 用户已经做过了！
)

# ❌ 错误3：重新识别维度
available_dimensions = [...]  # 用户已经有了！
```

### ✅ **AI 应该做**

```python
# ✅ 正确：只生成分析函数
def update_dashboard(controls):
    # 直接使用 selected_dimensions 中的字段
    year = controls[selected_dimensions[0]]  # 或直接写 '业务年度'
    products = controls[selected_dimensions[1]]
    
    # 业务逻辑
    filtered = df_df.filter(
        (pl.col(selected_dimensions[0]) == year) &
        (pl.col(selected_dimensions[1]).is_in(products))
    )
    
    result = filtered.group_by(selected_dimensions[1]).agg([
        pl.col('总保费').sum().alias('保费'),
        pl.len().alias('保单数')
    ])
    
    # Markdown 输出
    print(f"## {year}年分析报告\n")
    print_markdown_table(result)
    
    # 可视化
    fig = px.bar(result.to_pandas(), x=selected_dimensions[1], y='保费')
    return fig

# 绑定
dashboard.set_update_function(update_dashboard)
```

---

## 🎭 **职责对比表**

| 任务 | 👤 人工 | 🤖 AI |
|-----|---------|-------|
| 加载数据 | ✅ | ❌ |
| 分析维度 | ✅ 自动 | ❌ 不要重复 |
| 选择维度 | ✅ | ❌ |
| 创建 dashboard | ✅ | ❌ |
| 生成分析逻辑 | ❌ | ✅ **仅此** |
| 绑定函数 | ✅ 复制 AI 代码 | ✅ 提供代码 |
| 启动仪表盘 | ✅ | ❌ |

---

## 💡 **沟通示例**

### **场景 1：用户第一次请求**

**👤 用户**:
```
我已经运行了 Step 1-5，仪表盘已经创建好了。
我选择的维度是：业务年度、业务险种
帮我生成分析逻辑，显示各险种的保费排名。
```

**🤖 AI 应该理解**:
- ✅ dashboard 对象已存在
- ✅ selected_dimensions = ['业务年度', '业务险种']
- ✅ 只需生成 update_dashboard 函数

**🤖 AI 生成**:
```python
def update_dashboard(controls):
    year = controls['业务年度']
    products = controls['业务险种']
    
    filtered = df_df.filter(
        (pl.col('业务年度') == year) &
        (pl.col('业务险种').is_in(products))
    )
    
    result = filtered.group_by('业务险种').agg([
        pl.col('总保费').sum().alias('保费')
    ]).sort('保费', descending=True)
    
    print(f"## {year}年 险种保费排名\n")
    print_markdown_table(result)
    
    fig = px.bar(result.to_pandas(), x='业务险种', y='保费')
    return fig

dashboard.set_update_function(update_dashboard)
```

### **场景 2：用户从头开始（不用 Quick Start）**

**👤 用户**:
```
我有数据 df_df，帮我创建一个仪表盘分析各年度的保费。
```

**🤖 AI 应该做**:
```python
# 这种情况下，AI 需要做完整流程

# 1. 识别维度
dimensions = []
for col in df_df.columns:
    if df_df[col].dtype == pl.Utf8:
        dimensions.append(col)

# 2. 建议用户选择
print("可用维度：", dimensions)

# 3. 创建 dashboard
dashboard = DashboardBuilder.from_data(
    df_df,
    dimensions=['业务年度'],  # 根据用户需求
    title="保费分析"
)

# 4. 生成分析逻辑
def update_dashboard(controls):
    ...

dashboard.set_update_function(update_dashboard)
dashboard.build()
```

---

## 🎯 **总结**

### **在 Quick Start Notebook 中**
```
人工准备 → AI 生成逻辑 → 人工运行
  ↓            ↓              ↓
Step 1-5    update_dashboard  build()
```

### **在其他场景中**
```
AI 帮助完整流程（如果用户从零开始）
```

**关键判断**：
- 用户说"我已经运行了..." → AI 只生成缺少的部分
- 用户说"帮我从头创建..." → AI 做完整流程

---

**这样就不会冲突了！** ✅
