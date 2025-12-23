# 🤖 Jupyter AI DataAnalyze

**AI-Assisted Data Analysis Framework** - 专为 AI 协作设计的 Jupyter 数据分析框架

## ✨ 核心特性

- 🤖 **AI-Friendly 设计**：优化的 API 和文档，让 AI 能够快速理解并生成高质量代码
- 📊 **数据会话管理**：一次加载，全局使用，避免重复的数据加载代码
- 🎛️ **交互式仪表盘**：预制组件和模板，AI 只需关注业务逻辑
- 📚 **数据目录系统**：自动索引和管理多个数据集
- ⚡ **高性能**：基于 Polars 和 Parquet，处理大型数据集
- 📈 **可视化**：Plotly 交互式图表，专业金融级样式
- 🔄 **自动化报告**：从临时分析到定期报表的平滑过渡

## 🚀 快速开始

### 1. 安装

```bash
cd Jupyter_AI_DataAnalyze

# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -e .
```

### 2. 初始化环境

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑配置（可选）
# vim .env
```

### 3. 启动 Jupyter Lab

```bash
uv run jupyter lab
```

### 4. 启用 Polars Markdown 显示（推荐）

在 Notebook 顶部添加以下代码，让所有 DataFrame 以漂亮的表格格式显示：

```python
from src.utils import enable_polars_markdown_display
enable_polars_markdown_display()
```

详细说明见：[Polars Markdown 显示指南](docs/guides/polars_markdown_display.md)

### 5. 开始使用

打开 `notebooks/templates/quick_start.ipynb` 开始你的第一个分析！

## 📖 核心概念

### 数据会话（Data Session）

**问题：** 每次分析都要写重复的数据加载代码

**解决：** 使用数据会话，一次加载，随处使用

```python
from src.session import DataSession

# 初始化会话
session = DataSession()
session.load("2024_01", alias="df_jan")
session.load("2024_02", alias="df_feb")

# 现在可以直接使用 df_jan, df_feb
# AI 生成的代码可以直接引用这些变量
```

### 交互式仪表盘（Interactive Dashboard）

**问题：** 每次都要让 AI 生成复杂的 ipywidgets 代码

**解决：** 使用预制仪表盘构建器，AI 只需写业务逻辑

```python
from src.dashboard import DashboardBuilder

# 创建仪表盘框架
dashboard = DashboardBuilder("产品分析")
dashboard.add_dropdown('product', '选择产品', options=[...])
dashboard.add_slider('min_premium', '最小保费', min_val=0, max_val=100000)

# AI 只需要生成这个函数
def update_dashboard(controls):
    product = controls['product']
    filtered = df.filter(pl.col('product') == product)
    fig = px.bar(filtered, x='date', y='premium')
    return fig

dashboard.set_update_function(update_dashboard)
dashboard.build()
```

### 数据目录（Data Catalog）

**问题：** 多个数据集，AI 不知道有哪些数据可用

**解决：** 自动索引所有数据集，生成 AI-Readable 的数据目录

```python
from src.catalog import DataIndexer, CatalogQuery

# 一次性索引所有数据
indexer = DataIndexer()
catalog = indexer.scan_all_datasets()

# AI 可以查询和搜索
query = CatalogQuery()
datasets = query.search(keyword="保费")
ai_context = query.generate_ai_context(category="reinsurance")
```

## 📁 项目结构

```
Jupyter_AI_DataAnalyze/
├── src/                        # 核心代码库
│   ├── session.py              # 数据会话管理
│   ├── data/                   # 数据处理层
│   │   ├── loaders.py          # 数据加载器
│   │   ├── validators.py       # 数据验证
│   │   └── profiler.py         # 数据剖析
│   ├── catalog/                # 数据目录系统
│   │   ├── indexer.py          # 自动索引
│   │   ├── query.py            # 目录查询
│   │   └── transformer.py      # 数据转换
│   ├── dashboard/              # 交互式仪表盘
│   │   ├── builder.py          # 仪表盘构建器
│   │   └── templates.py        # 预制模板
│   ├── visualization/          # 可视化组件
│   ├── analysis/               # 分析工具
│   └── reporting/              # 报告生成
│
├── data/                       # 数据目录
│   ├── raw/                    # 原始数据
│   ├── processed/              # 标准化 Parquet
│   ├── catalog/                # 数据目录索引
│   └── outputs/                # 分析结果
│
├── notebooks/                  # Jupyter Notebooks
│   ├── templates/              # Notebook 模板
│   ├── 01_exploration/         # 探索性分析
│   ├── 02_analysis/            # 专项分析
│   ├── 03_reporting/           # 报告生成
│   └── 99_sandbox/             # 临时实验
│
├── docs/                       # 文档
│   ├── ai_context/             # AI Context 文档
│   │   └── main.md             # 主 AI Context
│   ├── examples/               # 示例代码库
│   └── guides/                 # 使用指南
│
└── scripts/                    # 工具脚本
    ├── setup_catalog.py        # 初始化数据目录
    └── ingest_new_data.py      # 新数据处理
```

## 🤖 与 AI 协作

### 典型工作流

```
1️⃣ 初始化数据会话
   session = DataSession()
   session.load("latest")

2️⃣ 生成 AI Context
   print(session.get_ai_context())

3️⃣ 复制 AI Context 给 AI

4️⃣ AI 生成分析代码
   （AI 知道数据结构，直接生成代码）

5️⃣ 执行并迭代
   （根据结果继续对话调整）
```

### AI Context 示例

框架会自动生成这样的 AI Context：

```markdown
# 📊 当前数据会话

已加载的数据集：

## `df_jan` (reinsurance_2024_01)
**数据量：** 1,234,567 行 × 12 列

**字段：**
- `policy_id` (String) - 保单号
- `date` (Date) - 日期
- `product` (String) - 产品类型
- `premium` (Float64) - 保费金额
...

**使用示例：**
```python
result = df_jan.group_by('product').agg(pl.col('premium').sum())
```
```

## 📚 文档

- [AI Context 文档](docs/ai_context/main.md) - AI 协作核心文档
- [使用指南](docs/guides/user_guide.md) - 完整使用手册
- [示例代码库](docs/examples/) - 常见分析模式
- [最佳实践](docs/guides/best_practices.md) - 高效使用技巧

## 🎯 使用场景

### 场景1：快速探索性分析

```python
# 只需3行代码开始分析
session.load("latest")
df = session.get("latest")
df.describe()
```

### 场景2：交互式仪表盘

```python
# 使用模板快速创建
from src.dashboard.templates import DashboardTemplates

dashboard = DashboardTemplates.time_series_analysis(df, 'date', 'premium')
dashboard.set_update_function(my_update_fn)
dashboard.build()
```

### 场景3：定期报告生成

```python
from src.reporting import ReportBuilder

report = ReportBuilder("月度报告")
report.add_section("趋势分析", data=trend_data, chart_type="line")
report.add_section("Top 20", data=top20, chart_type="bar")
report.export("outputs/reports/monthly.html")
```

## ⚙️ 配置

编辑 `.env` 文件自定义配置：

```bash
# 数据路径
RAW_DATA_PATH=data/raw
PROCESSED_DATA_PATH=data/processed

# Polars 性能
POLARS_MAX_THREADS=8

# 缓存
ENABLE_CACHE=true
CACHE_TTL=3600
```

## 🔧 高级功能

### 数据转换管道

自动将原始数据（Excel/CSV）转换为标准化 Parquet：

```bash
python scripts/ingest_new_data.py data/raw/new_data.xlsx
```

### 自动化报告

使用 papermill 自动运行 notebook 生成报告：

```bash
python scripts/run_monthly_report.py 2024-01
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [Polars](https://www.pola.rs/) - 高性能数据处理
- [Plotly](https://plotly.com/) - 交互式可视化
- [Jupyter Lab](https://jupyter.org/) - 数据分析环境

---

**开始你的 AI-Assisted 数据分析之旅！** 🚀
