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
print("## 📚 Panel Dashboard 完整使用指南")
print("=" * 80)
print()

print("""
🚨 关键规则（必须遵守）

⚠️ 规则 0: 仪表盘已经定义，不要重复创建！

**Step 6 已经运行了：**
```python
dashboard = PanelDashboardBuilder.from_data(
    df_df,
    dimensions=['业务年度', '业务险种', '机构名称'],
    title="📊 分析"
)
```

**你只需要生成：**
- ✅ update_dashboard 函数（用 @pn.depends 装饰）
- ✅ dashboard.set_update_function(update_dashboard)
- ✅ dashboard.show()

**不要生成：**
- ❌ 不要重复创建 dashboard
- ❌ 不要重复导入库
- ❌ 不要重复 CSS 修复
- ❌ 不要重复 pn.extension()

---

⚠️ 规则 1: 禁止硬编码任何维度名称！

**这是最重要的规则！**

❌❌❌ 绝对禁止：
```python
ANALYSIS_DIMENSION = '机构名称'  # ← 禁止定义这种常量！
group_col = '业务险种'  # ← 禁止写死！
result = filtered.group_by('机构名称').agg([...])  # ← 禁止硬编码！
fig = px.bar(..., x='业务年度', ...)  # ← 禁止硬编码！
```

✅✅✅ 正确：
```python
# 从控件获取聚合维度
group_col = values.get('_aggregation_dimension', '业务险种')
result = filtered.group_by(group_col).agg([...])  # ← 用变量
fig = px.bar(..., x=group_col, ...)  # ← 用变量
```

⚡️ 正确使用聚合维度的 3 个步骤

步骤 1: 获取聚合维度（放在函数开头）

```python
@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    values = {name: widget.value for name, widget in dashboard.widgets.items()}
    
    # ⚡️ 第一步：获取聚合维度
    group_col = values.get('_aggregation_dimension', '业务险种')  # ← 必须！
```

步骤 2: 过滤时跳过聚合维度（必须！）

```python
    filters = []
    for dim, val in values.items():
        # ⚠️ 关键：必须跳过聚合维度控件
        if dim == '_aggregation_dimension':  # ← 这 2 行必须有！
            continue  # ← 跳过！
        
        if isinstance(val, list):
            if '全选' not in val:
                filters.append(pl.col(dim).is_in(val))
        else:
            if val != '全选':
                filters.append(pl.col(dim) == val)
```

**为什么必须跳过？**
- _aggregation_dimension 只是控件，不是数据列
- 如果不跳过会报错：ColumnNotFoundError
- 它的值已保存在 group_col 中

步骤 3: 使用聚合维度变量（所有分组的地方）

```python
    # 按聚合维度分组
    result = filtered.group_by(group_col).agg([  # ← 用 group_col
        pl.col('总保费').sum().alias('保费'),
        pl.len().alias('保单数')
    ])
    
    # 输出标题
    print(f"## {group_col}分析结果")  # ← 用 group_col
    
    # 表格
    print_markdown_table(result.select([group_col, '保费', ...]))  # ← 用 group_col
    
    # 图表 X 轴
    fig = px.bar(result.to_pandas(), x=group_col, y='保费')  # ← 用 group_col
    
    # 图表标题
    fig.update_layout(title=f'{group_col}保费排名')  # ← 用 group_col
```

🎯 重要提示：仪表盘已经定义！

**Step 6 已经运行了这段代码：**
```python
dashboard = PanelDashboardBuilder.from_data(
    df_df,
    dimensions=['业务年度', '业务险种', '机构名称'],  # 用户已选择的维度
    title="📊 数据分析仪表盘"
)
```

**你只需要生成：**
1. ❌ 不要重复创建 dashboard
2. ❌ 不要重复导入和 CSS 修复
3. ✅ 只生成 update_dashboard 函数
4. ✅ 只生成 dashboard.set_update_function() 和 dashboard.show()

完整代码模板

**⚠️ 重要说明：**
1. 用户的 notebook 已经有基础初始化（Cell 1）
2. **但你需要自己添加必要的 import！**
3. 只生成更新函数部分（不要重复创建 dashboard）

```python
# ========================================
# Step 7: 生成分析代码
# ========================================

# 1️⃣ 导入必要的库（根据实际需要添加！）
import plotly.express as px
import plotly.graph_objects as go  # 如果需要
import polars as pl
# from datetime import datetime, timedelta  # 如果需要

# 2️⃣ 定义更新函数
@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    \"\"\"
    根据控件值更新仪表盘
    
    Args:
        *args: 控件值变化触发的参数
    
    Returns:
        plotly figure 对象
    \"\"\"
    # 第 1 步：获取所有控件的值
    values = {name: widget.value for name, widget in dashboard.widgets.items()}
    
    # 第 2 步：获取聚合维度（关键！）
    group_col = values.get('_aggregation_dimension', '业务险种')
    
    # 第 3 步：构建过滤条件
    filters = []
    for dim, val in values.items():
        # ⚠️ 必须跳过聚合维度控件！
        if dim == '_aggregation_dimension':
            continue
        
        if isinstance(val, list):
            if '全选' not in val:
                filters.append(pl.col(dim).is_in(val))
        else:
            if val != '全选':
                filters.append(pl.col(dim) == val)
    
    # 第 4 步：应用过滤
    filtered = df_df  # 使用实际的数据变量名
    for f in filters:
        filtered = filtered.filter(f)
    
    # 第 5 步：使用 group_col 进行聚合
    result = filtered.group_by(group_col).agg([
        pl.col('总保费').sum().alias('总保费'),
        pl.len().alias('保单数')
    ]).sort('总保费', descending=True)
    
    # 第 6 步：创建图表（使用 group_col）
    fig = px.bar(
        result.to_pandas(),
        x=group_col,  # ← 使用 group_col
        y='总保费',
        title=f'{group_col}保费分析',  # ← 使用 group_col
        labels={group_col: group_col, '总保费': '总保费（元）'}
    )
    
    # 第 7 步：配置图表
    fig.update_layout(
        autosize=True,
        height=600,
        font=dict(family=\"Microsoft YaHei, SimHei, Arial\")  # 中文字体
    )
    
    return fig

# 3️⃣ 绑定更新函数
dashboard.set_update_function(update_dashboard)

# 4️⃣ 显示仪表盘
dashboard.show()
```
# from src.dashboard import PanelDashboardBuilder
# from src.utils import print_markdown_table
# 
# display(HTML('''<style>...</style>'''))
# pn.extension('plotly', sizing_mode='stretch_width')
# 
# dashboard = PanelDashboardBuilder.from_data(
#     df_df,
#     dimensions=[...],  # 用户已定义
#     title="..."
# )

# ========================================
# 你需要生成的代码从这里开始 ⬇️
# ========================================

@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    values = {name: widget.value for name, widget in dashboard.widgets.items()}
    
    # ⚡️ 步骤 1：获取聚合维度
    group_col = values.get('_aggregation_dimension', '业务险种')
    
    # ⚡️ 步骤 2：过滤（跳过聚合维度）
    filters = []
    for dim, val in values.items():
        if dim == '_aggregation_dimension':  # ← 必须跳过
            continue
        
        if isinstance(val, list):
            if '全选' not in val:
                filters.append(pl.col(dim).is_in(val))
        else:
            if val != '全选':
                filters.append(pl.col(dim) == val)
    
    filtered = df_df
    for f in filters:
        filtered = filtered.filter(f)
    
    # ⚡️ 步骤 3：使用聚合维度进行分组分析
    # 这里写你的业务逻辑，例如：
    result = filtered.group_by(group_col).agg([
        pl.col('总保费').sum().alias('保费'),
        pl.len().alias('保单数')
    ]).sort('保费', descending=True)
    
    # 单位转换
    if result['保费'].max() > 1_000_000:
        result = result.with_columns([
            (pl.col('保费') / 10000).alias('保费（万元）')
        ])
        y_col = '保费（万元）'
    else:
        y_col = '保费'
    
    # 输出
    print(f"## {group_col}分析结果")
    print_markdown_table(result.head(10))
    
    # 图表
    fig = px.bar(result.head(10).to_pandas(), x=group_col, y=y_col,
                 title=f'{group_col}保费排名')
    fig.update_layout(height=600, autosize=True)
    
    return fig

dashboard.set_update_function(update_dashboard)
dashboard.show()
```

✅ 检查清单（生成代码后必须检查）

第 0 步：检查是否有必要的导入
□ 代码开头有 `import plotly.express as px` (如果用 px.bar/line 等)
□ 代码开头有 `import polars as pl` (如果用 pl.col/pl.when 等)
□ 代码开头有 `import plotly.graph_objects as go` (如果用 go.Figure)
□ 不要遗漏任何需要的 import！

第 1 步：检查是否重复定义
□ 代码中没有 `dashboard = PanelDashboardBuilder.from_data(...)` 
□ 代码中没有 `from IPython.display import HTML, display`
□ 代码中没有 `pn.extension()`
□ 代码只包含：import语句 + update_dashboard 函数 + set_update_function + show


第 2 步：检查函数开头
□ 有 group_col = values.get('_aggregation_dimension') 吗？

第 3 步：检查过滤循环
□ 有 if dim == '_aggregation_dimension': continue 吗？

第 4 步：检查所有用到维度的地方
□ group_by('机构名称') → 改为 group_by(group_col)
□ x='业务年度' → 改为 x=group_col
□ title='险种分析' → 改为 title=f'{group_col}分析'
□ select(['机构名称', ...]) → 改为 select([group_col, ...])

第 5 步：快速验证
□ 代码开头有必要的 import
□ 函数开头定义了 group_col
□ 过滤循环跳过了 _aggregation_dimension
□ group_by() 使用 group_col
□ 图表 X 轴使用 group_col
□ 标题包含 group_col
□ 使用 pl.len()
□ 图表有 autosize=True

⚠️ 常见错误

错误 1: 定义 ANALYSIS_DIMENSION = '机构名称'  # ← 禁止！
错误 2: 忘记 if dim == '_aggregation_dimension': continue
错误 3: group_by('业务险种')  # ← 硬编码！

规则：
1. 使用 PanelDashboardBuilder
2. 不要自己创建控件
3. 获取聚合维度
4. 跳过聚合维度
5. 使用聚合维度变量
6. 使用 @pn.depends
7. 参数是 *args
8. 使用 pl.len()
9. autosize=True
""")

print()
print("=" * 80)
print("💡 使用方法")
print("=" * 80)
print("1. 复制上面的所有内容给 AI")
print("2. 告诉 AI 你的需求")
print("3. 强调：不要硬编码任何维度！")
print("=" * 80)
