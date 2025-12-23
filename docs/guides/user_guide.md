# 用户指南 - Jupyter AI DataAnalyze

## 目录

1. [安装和启动](#安装和启动)
2. [核心概念](#核心概念)
3. [日常工作流](#日常工作流)
4. [高级功能](#高级功能)
5. [最佳实践](#最佳实践)
6. [故障排查](#故障排查)

---

## 安装和启动

### 快速启动

```bash
cd Jupyter_AI_DataAnalyze
./start.sh
```

这个脚本会自动：
- 安装 uv（如果未安装）
- 安装所有依赖
- 创建环境变量文件
- 启动 Jupyter Lab

### 手动安装

如果你想手动控制每个步骤：

```bash
# 1. 安装依赖
uv sync

# 2. 创建环境变量文件
cp .env.example .env

# 3. 启动 Jupyter Lab
uv run jupyter lab
```

---

## 核心概念

### 1. 数据会话（DataSession）

**问题：** 每次分析都要重复写数据加载代码

**解决：** 使用 DataSession，数据加载一次，全局可用

```python
from src.session import DataSession

# 创建会话
session = DataSession()

# 加载数据（自动注入到全局命名空间）
session.load("2024_01", alias="jan")  # 创建全局变量 df_jan

# 现在可以直接使用 df_jan
result = df_jan.group_by('product').agg(...)
```

**优势：**
- ✅ 避免重复代码
- ✅ AI 可以直接使用变量
- ✅ 统一的数据管理

### 2. 交互式仪表盘（Dashboard）

**问题：** 创建交互组件需要大量 ipywidgets 代码

**解决：** 使用 DashboardBuilder，组件由框架提供

```python
from src.dashboard import DashboardBuilder

# 创建仪表盘
dashboard = DashboardBuilder("分析仪表盘")

# 添加控件（链式调用）
dashboard.add_dropdown('product', '产品', options=[...])
dashboard.add_slider('threshold', '阈值', min_val=0, max_val=100)

# AI 只需要生成这个函数
def update(controls):
    product = controls['product']
    # ... 业务逻辑 ...
    return fig

dashboard.set_update_function(update)
dashboard.build()
```

**优势：**
- ✅ AI 只关注业务逻辑
- ✅ 组件自动管理
- ✅ 预制模板可用

### 3. AI Context

**问题：** AI 不了解你的数据结构

**解决：** 自动生成 AI-Friendly 的数据概览

```python
# 生成 AI Context
ai_context = session.get_ai_context()
print(ai_context)

# 或者直接保存
with open("ai_context.txt", "w") as f:
    f.write(ai_context)
```

**包含内容：**
- 已加载的数据集
- 每个数据集的列名和类型
- 数据量统计
- 使用示例

---

## 日常工作流

### 典型的一天

#### 早上：启动环境

```bash
cd Jupyter_AI_DataAnalyze
./start.sh
```

#### 开始分析：初始化会话

```python
# Cell 1: 初始化
from src.session import DataSession
import polars as pl
import plotly.express as px

session = DataSession()
session.load("latest_data", alias="df")
session.summary()
```

#### 准备 AI 协作：生成 Context

```python
# Cell 2: 生成 AI Context
print("🤖 复制以下内容给 AI：")
print("="*60)

# 框架工具
with open("docs/ai_context/main.md") as f:
    print(f.read())

# 当前数据
print(session.get_ai_context())
print("="*60)
```

#### 与 AI 协作：分析任务

```
你（给 AI 的 Prompt）：
---
【AI Context】
... （粘贴上面的 AI Context）

【任务】
分析各产品的保费增长趋势，
找出增长最快的 Top 10 产品
---

AI 生成代码 → 你复制到 Cell 3 → 执行
```

#### 迭代优化

```
你：只显示增长率 > 20% 的产品
AI：修改代码...
你：执行新代码
```

#### 固化结果：创建仪表盘

如果这个分析需要重复使用，创建交互式仪表盘：

```python
dashboard = DashboardBuilder("产品增长分析")
dashboard.add_dropdown('year', '年份', options=['2023', '2024'])
dashboard.set_update_function(ai_generated_function)
dashboard.build()
```

---

## 高级功能

### 1. 惰性加载（Lazy Loading）

处理大数据集时使用：

```python
# 惰性加载（不立即读入内存）
session.load("huge_data.parquet", alias="df", lazy=True)

# 数据处理会被优化
result = (
    df_huge
    .filter(...)
    .group_by(...)
    .agg(...)
    .collect()  # 只在这里才真正执行
)
```

### 2. 批量加载

加载多个数据集：

```python
from src.data import load_multiple

# 加载并合并
df_all = load_multiple("2024_*.parquet")

# 或者不合并
dfs = load_multiple("2024_*.parquet", concat=False)
```

### 3. 自定义仪表盘组件

除了基础组件，还可以组合使用：

```python
dashboard = DashboardBuilder("高级分析")

# 多个控件组合
dashboard.add_dropdown('dimension1', '维度1', options=[...])
dashboard.add_dropdown('dimension2', '维度2', options=[...])
dashboard.add_slider('top_n', 'Top N', min_val=5, max_val=50, step=5)
dashboard.add_multiselect('filters', '过滤器', options=[...])
dashboard.add_button('refresh', '刷新数据', button_style='success')
```

---

## 最佳实践

### 1. Notebook 组织

推荐的 Notebook 结构：

```python
# Cell 1: 环境初始化（总是第一个）
from src.session import DataSession
# ... 导入其他库 ...

# Cell 2: 数据加载（只运行一次）
session = DataSession()
session.load(...)

# Cell 3: AI Context 生成
# 复制给 AI

# Cell 4-N: AI 生成的分析代码
# 每个 Cell 一个独立的分析

# 最后 Cell: 清理
# session.clear()
```

### 2. 命名规范

- **数据集别名：** 简短、描述性
  - ✅ `df_jan`, `df_feb`
  - ❌ `df_reinsurance_2024_01_final_v2`

- **变量名：** 清晰、一致
  - ✅ `by_product`, `top10`, `filtered`
  - ❌ `df1`, `temp`, `x`

### 3. 与 AI 协作技巧

**好的 Prompt：**
```
【背景】我有再保险业务数据
【数据】（粘贴 AI Context）
【任务】计算各产品的赔付率，找出高风险产品
【要求】赔付率 > 80% 的产品，按赔付率降序
```

**不好的 Prompt：**
```
帮我分析数据
```

### 4. 性能优化

**使用 Polars 而不是 Pandas：**
```python
# ✅ 推荐（快）
df.group_by('product').agg(...)

# ❌ 避免（慢）
df.to_pandas().groupby('product').agg(...)
```

**只在需要时转换为 Pandas：**
```python
# Polars 处理
result = df.filter(...).group_by(...).agg(...)

# 只在传给 Plotly 时转换
fig = px.bar(result.to_pandas(), ...)
```

**使用惰性加载：**
```python
# 大数据集用 lazy=True
session.load("huge.parquet", lazy=True)
```

### 5. 代码复用

如果某个分析模式经常使用，提取为函数：

```python
# src/analysis/custom.py
def calculate_growth_rate(df, metric):
    return df.with_columns(
        pl.col(metric).pct_change().alias('growth_rate')
    )

# 在 Notebook 中使用
from src.analysis.custom import calculate_growth_rate
result = calculate_growth_rate(df, 'premium')
```

---

## 故障排查

### 问题1：找不到模块

```
ModuleNotFoundError: No module named 'src'
```

**解决：**
```bash
# 确保在项目根目录
cd Jupyter_AI_DataAnalyze

# 重新安装
uv sync
```

### 问题2：数据文件找不到

```
FileNotFoundError: 找不到数据文件
```

**解决：**
```python
# 检查文件是否存在
from pathlib import Path
print(Path("data/processed").glob("*.parquet"))

# 使用完整路径
session.load("data/processed/your_file.parquet")
```

### 问题3：内存不足

```
MemoryError
```

**解决：**
```python
# 使用惰性加载
session.load("big_file.parquet", lazy=True)

# 或者分批处理
for file in files:
    df = load_data(file)
    result = process(df)
    save(result)
    del df  # 释放内存
```

### 问题4：仪表盘不更新

**解决：**
```python
# 确保更新函数有返回值
def update(controls):
    # ... 处理逻辑 ...
    return fig  # 必须返回图表对象！

# 确保绑定了更新函数
dashboard.set_update_function(update)
```

---

## 获取帮助

- **AI Context 文档：** `docs/ai_context/main.md`
- **示例代码：** `docs/examples/`
- **快速开始：** `notebooks/templates/quick_start.ipynb`

---

**祝您使用愉快！** 🎉
