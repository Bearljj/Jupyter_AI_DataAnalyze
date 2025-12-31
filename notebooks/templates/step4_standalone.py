# ========================================
# 📋 给 AI 的完整信息（复制全部输出给 AI）
# ========================================

print("=" * 80)
print("📋 **复制以下所有内容给 AI**")
print("=" * 80)
print()

# 1. 数据结构
print("## 📊 数据结构")
print()

# 检查 session 是否存在
try:
    if 'session' in dir():
        print(session.get_ai_context())
    else:
        print("⚠️ 警告: session 未初始化")
        print("请先运行 Step 2 加载数据")
        print()
        print("提示数据结构:")
        print("- df_xxx: 已加载的 DataFrame")
        print("- 使用 session.summary() 查看详情")
except Exception as e:
    print(f"⚠️ 无法获取数据上下文: {e}")
    print("请确保已运行 Step 2 加载数据")

print()

print("=" * 80)
print("## 🎯 工作流程（重要！请严格遵守）")
print("=" * 80)
print()

print("""
📌 **第一步：理解需求，不要急着写代码！**

在生成任何代码之前，你必须：

1. ✅ **仔细阅读用户需求**
   - 理解用户想分析什么
   - 确认需要什么样的可视化
   - 明确数据的聚合方式

2. ✅ **向用户确认理解**
   用自然语言回复：
   \"我理解你的需求是：
   - [总结需求]
   - [确认分析逻辑]
   - [确认可视化类型]
   
   请确认我的理解是否正确？\"

3. ✅ **等待用户明确指令**
   只有在用户回复 \"是的，开始吧\" 或类似明确指令后，才开始写代码

4. ❌ **不要上来就写代码**
   这会浪费 token，而且可能理解错需求

---

📌 **第二步：处理导入语句**

⚠️ **重要：你需要自己添加必要的 import！**

在生成的代码开头（update_dashboard 函数之前），必须包含：

```python
# 必需的导入（根据实际使用情况添加）
import plotly.express as px
import plotly.graph_objects as go
import polars as pl
import panel as pn
from datetime import datetime, timedelta
```

**为什么？**
- Cell 1 只有基础导入
- 你的分析代码可能需要额外的库
- 不要假设所有库都已导入

**检查清单：**
□ plotly.express (如果用 px.bar, px.line 等)
□ plotly.graph_objects (如果用 go.Figure)
□ polars as pl (如果直接用 pl.col, pl.when 等)
□ datetime/timedelta (如果处理日期)

---

📌 **第三步：询问确认后再优化**

生成代码后：
1. 先给出初版代码
2. 等用户测试
3. 根据反馈再优化
4. 不要一次性给出多个版本

---

""")

print("=" * 80)
print("## 🛡️ **AI 核心指令：物理隔离规范 (v3.0)**")
print("=" * 80)
print("""
⚠️ **请严格遵守以下开发原则：**

1. ✅ **必须使用 PanelDashboardBuilder** 进行开发。
2. ✅ **规范等级**：请严格遵守 `main.md` 中的 v3.0 规范。
3. ⚡️ **核心原则（物理隔离）**：
   - ❌ **严禁遍历 `.widgets` 进行数据过滤**。
   - ✅ **必须使用 `.data_values` 获取数据维度值**。
   这样做能自动排除系统功能控件（如 `_aggregation_dimension`），防止在数据过滤时因引用非数据列名而导致崩溃。
""")

print("=" * 80)
print("## 📚 Panel Dashboard 完整使用指南 (v3.0)")
print("=" * 80)
print()

print("""
🚨 关键规则 (AI 必须严格遵守)

⚠️ 规则 0: 仪表盘已由框架自动创建，禁止重复创建！
只需生成 `update_dashboard` 函数、绑定并显示即可。

⚠️ 规则 1: 禁止硬编码维度名称！
❌ 绝对禁止：`group_by('业务险种')` 或 `x='业务年度'`。
✅ 必须使用：从系统控件动态获取聚合维度标识。

⚡️ **核心：v3.0 物理隔离开发流程**

步骤 1: 获取数据值与业务维度
```python
@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    # ✅ 物理隔离：只获取业务数据列的值
    data_filters = dashboard.data_values  
    
    # ✅ 动态维度：从系统控件获取当前的聚合/分组轴
    group_col = dashboard.widgets['_aggregation_dimension'].value
```

步骤 2: 极简动态过滤
```python
    filtered = df_df
    for dim, val in data_filters.items():
        if isinstance(val, list):
            if '全选' not in val:
                filtered = filtered.filter(pl.col(dim).is_in(val))
        elif val != '全选':
            filtered = filtered.filter(pl.col(dim) == val)
```

步骤 3: 聚合分析与可视化 (使用变量)
```python
    result = filtered.group_by(group_col).agg([
        pl.col('总保费').sum().alias('保费')
    ])
    
    fig = px.bar(result.to_pandas(), x=group_col, y='保费')
    fig.update_layout(autosize=True)
```

---

📝 **完整代码模板**

```python
import plotly.express as px
import polars as pl

@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    # 1. 物理隔离获取业务过滤值
    filters = dashboard.data_values
    # 2. 获取当前的动态聚合轴
    agg_axis = dashboard.widgets['_aggregation_dimension'].value
    
    # 3. 执行动态过滤
    df_filtered = df_df
    for col, val in filters.items():
        if isinstance(val, list):
            if '全选' not in val:
                df_filtered = df_filtered.filter(pl.col(col).is_in(val))
        elif val != '全选':
            df_filtered = df_filtered.filter(pl.col(col) == val)
            
    # 4. 业务逻辑 (示例：Top 10 排名)
    analysis = df_filtered.group_by(agg_axis).agg([
        pl.col('总保费').sum().alias('总额'),
        pl.len().alias('条数')
    ]).sort('总额', descending=True).head(10)
    
    # 5. 可视化
    fig = px.bar(analysis.to_pandas(), x=agg_axis, y='总额', title=f'按{agg_axis}统计结果')
    fig.update_layout(autosize=True, height=600)
    
    # 6. 辅助表格输出
    print_markdown_table(analysis)
    
    return fig

dashboard.set_update_function(update_dashboard)
dashboard.show()
```

✅ **AI 生成后自检清单**
□ 是否使用了 `dashboard.data_values`？ (必须使用，严禁直接遍历 .widgets)
□ 是否通过 `dashboard.widgets['_aggregation_dimension'].value` 获取轴？
□ 过滤循环中是否不再需要 `if dim == '_aggregation_dimension': continue`？ (是的，data_values 已自动过滤)
□ 图表是否设置了 `autosize=True`？
□ 是否使用了 `pl.len()`？
□ 是否在函数内部包含了必要的 `import`？

⚠️ **高频错误告诫**
❌ 严禁在过滤逻辑中涉及 `_aggregation_dimension`。
❌ 严禁硬编码任何具体的列名（如 '业务年度'）作为坐标轴或分组键。
""")

print()
print("=" * 80)
print("💡 使用方法")
print("=" * 80)
print("1. 复制上面的所有内容给 AI")
print("2. 告诉 AI 你的需求")
print("3. 强调：请严格遵守 v3.0 物理隔离规范")
print("=" * 80)
