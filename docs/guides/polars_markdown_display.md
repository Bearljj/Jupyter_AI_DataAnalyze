# 🎨 Polars Markdown 表格显示 - 使用指南

## ✨ 功能说明

默认情况下，Polars DataFrame 在 Jupyter 中以纯文本格式显示：
```
shape: (3, 2)
┌──────────┬────────┐
│ product  ┆ sales  │
│ ---      ┆ ---    │
│ str      ┆ i64    │
╞══════════╪════════╡
│ A        ┆ 1000   │
│ B        ┆ 2000   │
│ C        ┆ 1500   │
└──────────┴────────┘
```

启用 Markdown 显示后，DataFrame 会以美观的 HTML 表格格式显示。

## 🚀 使用方法

### 方法 1: 自动显示（推荐）

在 Notebook 顶部添加以下代码，所有 DataFrame 将自动以表格格式显示：

```python
from src.utils import enable_polars_markdown_display

# 启用自动 Markdown 显示
enable_polars_markdown_display()

# 现在所有 DataFrame 都会以表格格式显示
df.head()
result = df.group_by('product').agg(pl.col('sales').sum())
result  # 自动显示为表格
```

### 方法 2: 手动显示

如果你想手动控制哪些 DataFrame 以表格格式显示：

```python
from src.utils import print_markdown_table

# 普通显示
df.head()  # 纯文本格式

# Markdown 表格显示
result = df.group_by('product').agg(pl.col('sales').sum())
print_markdown_table(result)  # 表格格式
```

### 方法 3: 作为 Markdown 对象

返回 IPython Markdown 对象，适合在其他地方使用：

```python
from src.utils import df_to_markdown

result = df.group_by('product').agg(pl.col('sales').sum())
md_table = df_to_markdown(result, max_rows=50)
display(md_table)
```

## 🤖 AI 协作建议

### 在 AI Context 中添加

当与 AI 协作时，在你的 AI Context 中添加以下说明：

```markdown
## 📊 输出格式规范

本项目已启用 Polars Markdown 显示。

**AI 生成代码时的要求：**
1. 对于最终结果 DataFrame，使用 `print_markdown_table(result)` 显示
2. 示例：
   ```python
   from src.utils import print_markdown_table
   
   result = df.group_by('category').agg(pl.col('amount').sum())
   print_markdown_table(result)
   ```

3. 或者，如果启用了自动显示模式，直接返回 DataFrame 即可。
```

### Quick Start 模板

在 Notebook 开头使用：

```python
# === 标准设置 ===
from src.session import DataSession
from src.utils import enable_polars_markdown_display
import polars as pl

# 启用 Markdown 表格显示
enable_polars_markdown_display()

# 初始化数据会话
session = DataSession()
session.load("your_data", alias="df")

# 现在开始分析，所有输出都会是漂亮的表格！
```

## ⚙️ 高级配置

### 限制显示行数

```python
# 显示前 50 行
print_markdown_table(df, max_rows=50)

# 或修改默认行数
df_to_markdown(df, max_rows=200)
```

### 显示索引

```python
from src.utils.polars_display import df_to_markdown

md_table = df_to_markdown(df, index=True)
display(md_table)
```

## 📝 示例对比

### Before (纯文本)
```
shape: (1000, 5)
┌───────────┬──────────┬──────────┬──────────┬──────────┐
│ date      ┆ product  ┆ sales    ┆ quantity ┆ region   │
│ ---       ┆ ---      ┆ ---      ┆ ---      ┆ ---      │
│ date      ┆ str      ┆ f64      ┆ i64      ┆ str      │
╞═══════════╪══════════╪══════════╪══════════╪══════════╡
│ 2024-01-01┆ Widget A ┆ 12500.50 ┆ 125      ┆ North    │
│ ...       ┆ ...      ┆ ...      ┆ ...      ┆ ...      │
└───────────┴──────────┴──────────┴──────────┴──────────┘
```

### After (Markdown 表格)

| date       | product  | sales    | quantity | region |
|:-----------|:---------|:---------|:---------|:-------|
| 2024-01-01 | Widget A | 12500.50 | 125      | North  |
| 2024-01-02 | Widget B | 8900.25  | 89       | South  |
| 2024-01-03 | Widget C | 15600.75 | 156      | East   |

*显示为可排序、可选择的 HTML 表格，支持鼠标操作*

## 🔧 故障排除

### 问题：表格不显示

**解决方案：**
1. 确保安装了 `tabulate` 库：
   ```bash
   uv add tabulate
   # 或
   pip install tabulate
   ```

2. 重新加载模块：
   ```python
   %reload_ext autoreload
   %autoreload 2
   ```

### 问题：显示为纯文本

**解决方案：**
确保调用了 `enable_polars_markdown_display()`，且在 DataFrame 输出之前。

### 问题：显示行数过多

**解决方案：**
使用 `max_rows` 参数限制显示行数：
```python
print_markdown_table(large_df, max_rows=20)
```

## 📚 相关文档

- [Polars 官方文档](https://pola-rs.github.io/polars/)
- [pandas.to_markdown()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
- [IPython Display](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html)

---

**享受更美观的数据展示！** ✨
