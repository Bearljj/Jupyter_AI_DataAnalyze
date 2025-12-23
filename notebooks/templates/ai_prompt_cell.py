# ========================================
# 给 AI 的完整提示（复制所有内容给 AI）
# ========================================

print("📋 复制以下所有内容给 AI:\n")
print("=" * 80)

# 1. 数据结构
print("\n## 📊 数据结构\n")
print(session.get_ai_context())

print("\n" + "=" * 80)

# 2. 必读文档
print("\n## 📚 必读文档（AI 必须完整阅读）\n")
print("1. **主要指南**: `docs/ai_context/main.md`")
print("2. **Panel 完整指南**: `docs/ai_context/PANEL_GUIDE.md`")
print("3. **快速参考**: `docs/ai_context/AI_QUICK_REFERENCE.md`")

# 3. 关键提醒
print("\n## 🚨 关键提醒\n")
print("- ✅ **必须使用** `PanelDashboardBuilder`（可导出 HTML）")
print("- ❌ **禁止使用** `DashboardBuilder`（已废弃，不支持导出）")
print("- ✅ **必须添加** CSS 宽度修复（代码开头）")
print("- ✅ **必须使用** `@pn.depends(*dashboard.widgets.values())` 装饰器")
print("- ✅ **必须使用** `pl.len()` 而不是 `pl.count()`")
print("- ✅ 图表设置 `autosize=True`")

# 4. 代码模板要点
print("\n## 📝 代码结构要点\n")
print("""
正确的导入：
```python
from IPython.display import HTML, display  # ← 必须
from src.dashboard import PanelDashboardBuilder  # ← 不是 DashboardBuilder!
import panel as pn
import polars as pl
import plotly.express as px
```

必须的CSS修复：
```python
display(HTML('''
<style>
    .jp-Notebook { --jp-notebook-max-width: 100% !important; }
    .bk-root, .bk-root > .bk { width: 100% !important; }
</style>
'''))
```

Panel 初始化：
```python
pn.extension('plotly', sizing_mode='stretch_width')  # ← 有 sizing_mode
```

更新函数：
```python
@pn.depends(*dashboard.widgets.values())  # ← 必须有装饰器
def update_dashboard(*args):  # ← 参数是 *args
    values = {name: widget.value for name, widget in dashboard.widgets.items()}
    # ... 分析逻辑
    return fig
```
""")

print("=" * 80)

print("\n💡 将上面的所有内容复制给 AI")
print("💡 然后说: '请使用 Panel Dashboard 生成分析代码'")
