# 🚀 快速参考 - 仪表盘自动化

## 📋 新工作流（3步）

```python
# Step 1: 加载数据
from src.session import DataSession
session = DataSession()
session.load("alldata", alias="df")

# Step 2: 创建仪表盘（AI识别维度后）
from src.dashboard import DashboardBuilder
dashboard = DashboardBuilder.from_data(
    df_df,
    dimensions=['业务年度', '业务险种']  # AI建议+用户确认
)

# Step 3: 绑定分析逻辑（AI生成）
from src.utils import print_markdown_table

def update(controls):
    # 获取控件值
    year = controls['业务年度']
    products = controls['业务险种']
    
    # 分析逻辑
    result = df_df.filter(...).group_by(...).agg(...)
    
    # Markdown输出
    print("## 分析结果")
    print_markdown_table(result)
    
    # 返回图表
    return fig

dashboard.set_update_function(update)
dashboard.build()
```

## 🎨 控件类型自动选择

| 唯一值数量 | 控件类型 | 默认选择 |
|-----------|----------|---------|
| ≤ 10      | dropdown | 最新值 |
| 11-50     | multiselect | 前3个 |
| 50+       | multiselect⚠️ | 前5个 |

## 📊 Markdown 输出

```python
# ✅ 正确
from src.utils import print_markdown_table
print_markdown_table(result)

# ❌ 错误
print(result)  # 纯文本
```

## 🤖 AI 识别维度模板

```python
for col in df_df.columns:
    if df_df[col].dtype == pl.Utf8:
        n = df_df[col].n_unique()
        print(f"- {col}: {n} 个值")
```

## 📚 文档

- **AI Context**: `docs/ai_context/main.md`
- **完整示例**: `notebooks/examples/auto_dashboard_example.py`
- **总结**: `PHASE1_SUMMARY.md`
