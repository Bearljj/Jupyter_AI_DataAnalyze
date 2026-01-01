# Jupyter AI DataAnalyze - AI Context (Updated 2026-01-01)

**版本：** 3.1.0 (LTS)
**最后更新：** 2026-01-01
**核心变更：** **最高交互协议 (Prime Directive)** | **Level 3 物理隔离** | **分析自我叙述规范**

---

# 🛑 核心交互协议 (CRITICAL PROTOCOL)

**⚠️ 严禁直接生成代码 (ZERO CODE POLICY)**

在用户提出新的分析需求后的**第一轮回复中**，你**绝对禁止**编写任何具体的 `update_dashboard` 函数。
你必须严格遵守以下 **"咨询-确认-执行"** 流程：

### 1. 阶段一：复述与设计 (Consultation)
你必须以自然语言回复，并包含以下内容：
*   **业务理解**：总结分析目的及业务价值（为什么要分析）。
*   **计算口径**：详细解释具体的分析逻辑，列出核心指标的数学公式。
*   **技术自检**：列出逻辑依赖的关键列名，并说明将使用哪种可视化类型。
*   **明确询问**："请确认以上逻辑是否符合您的预期？确认后我将为您生成代码。"

### 2. 阶段二：等待指令 (Wait)
*   **停止输出**。等待用户回复 "OK"、"确认" 或修改意见。

### 3. 阶段三：执行代码 (Execution)
*   只有在收到明确确认后，才允许生成代码。
*   生成的代码必须通过 **STATE: FINAL_VALIDATION** 自检（详见后文）。

---

## 🚦 分析状态机 (Analysis State Machine)

你必须根据以下状态维护你的交互链路：

*   **STATE: PENDING_CONFIRMATION** (初始状态)
    *   用户提出了分析需求。
    *   **动作**：解释设计逻辑，列出公式，询问确认。❌ **禁止生成代码**。
    
*   **STATE: APPROVED** (仅当收到确认指令)
    *   **动作**：生成符合 v3.1 规范的代码。
    
*   **STATE: FINAL_VALIDATION** (输出前的自动化质量网关)
    *   **自检清单**：
        1. 物理隔离：是否使用 `dashboard.data_values`？是否避免了遍历 `.widgets`？
        2. 自我叙述：是否包含 `[REPORT_METADATA]` 块？内容是否详尽？
        3. 金额规范：保费类大额字段是否包含 `>100万转万元` 逻辑？坐标轴单位是否同步？
        4. API 规范：是否使用 `pl.len()`？是否使用 `print_markdown_table()`？
        5. 启动启动：是否在结尾调用 `dashboard.show()`？

---

## 📊 v3.1 标准分析范式 (The Golden Sample)

```python
import plotly.express as px
import polars as pl
import panel as pn
from src.utils import print_markdown_table

@pn.depends(*dashboard.widgets.values())
def update_dashboard(*args):
    """
    [REPORT_METADATA]
    ### 1. 业务背景
    [在此处填入已确认的分析目的。例如：分析 2025 年度分保业务的损益情况，评估再保合同的有效性。]
    
    ### 2. 分析逻辑
    [在此处填入已确认的详细计算公式。例如：损益 = 摊回费用 + 赔款 - 保费。金额超过 100 万时自动转换为万元。]
    [/REPORT_METADATA]
    """
    # 1. 物理隔离：直接获取业务数据控件的值
    filters = dashboard.data_values
    # 2. 动态维度：从系统控件获取当前的聚合轴
    agg_dim = dashboard.widgets['_aggregation_dimension'].value
    
    # 3. 极简动态过滤
    filtered = df_df
    for dim, val in filters.items():
        if isinstance(val, list):
            if '全选' not in val:
                filtered = filtered.filter(pl.col(dim).is_in(val))
        elif val != '全选':
            filtered = filtered.filter(pl.col(dim) == val)
    
    # 4. 执行聚合
    result = filtered.group_by(agg_dim).agg([
        pl.col('总保费').sum().alias('保费'),
        pl.len().alias('保单数')
    ]).sort('保费', descending=True)
    
    # 5. 金额单位自动化 (Amt Normalization)
    max_premium = result['保费'].max()
    if max_premium and max_premium > 1_000_000:
        result = result.with_columns([(pl.col('保费')/10000).alias('保费(万元)')])
        y_col = '保费(万元)'
    else:
        y_col = '保费'
    
    # 6. 输出 (必须使用 print_markdown_table 以支持 PDF 导出)
    print(f"## 按 {agg_dim} 分析结果\n")
    print_markdown_table(result.head(10))
    
    # 7. 可视化 (自适应宽度)
    fig = px.bar(result.to_pandas(), x=agg_dim, y=y_col, title=f"各{agg_dim}保费分布")
    fig.update_layout(autosize=True, height=600)
    
    return fig

# 绑定并显示
dashboard.set_update_function(update_dashboard)
dashboard.show()
```

---

## ⚠️ **重要：工作流澄清**

如果用户正在使用 `quick_start.ipynb`，**环境已由框架准备就绪**：

1.  **物理隔离 (Level 3)**：✅ 必须使用 `dashboard.data_values` 获取过滤条件。
2.  **动态轴**：✅ 必须使用 `dashboard.widgets['_aggregation_dimension'].value` 获取聚合轴。
3.  **自我叙述**：✅ 必须在 Docstring 中包含 `[REPORT_METADATA]` 块。
4.  **启动命令**：✅ 必须调用 `dashboard.show()`。

---

## 🆕 框架核心规范 (Updated 2025-12-31)

### 1. 仪表盘创建已简化
- ✅ 本地 Notebook 自动分析维度
- ✅ AI 只负责生成分析逻辑
- ✅ 不再需要手动写控件代码

### 2. 输出必须使用 Markdown 格式
- ✅ 所有 DataFrame 输出使用 `print_markdown_table()`
- ✅ 分析摘要使用 Markdown 标题和列表
- ✅ 让输出在 Jupyter 中渲染为漂亮的表格

### 3. ⚠️ Polars API 更新
- ✅ **使用 `pl.len()` 而不是 `pl.count()`**
- ❌ `pl.count()` 已在 Polars 0.20.5 中弃用
- ✅ 正确写法：`pl.len().alias('数量')`

### 4. 📊 可视化审美规范

#### A. 图表尺寸与布局
- ✅ **自适应占满显示空间**：设置 `autosize=True`。
- ✅ **移除 JupyterLab Cell 宽度限制**：在 notebook 开头运行 CSS 注入代码（见下文）。
- ✅ **精细化边距**：`margin=dict(l=50, r=50, t=80, b=50)`。

#### B. 金额字段处理
- ✅ **金额超过 100 万时，自动转换为"万元"**。
- ✅ 坐标轴标题与图表标题中的单位必须与转换结果保持一致。

---

## 📊 维度字段识别指南（核心干货）

### 识别标准

**维度字段**（用于分组/筛选）：
- ✅ 字符串类型（String）或日期类型（Date）
- ✅ 描述业务对象的属性（"是什么"、"在哪里"、"什么时候"）
- ✅ 有固定的取值范围（即使很大，如机构名称可能有500+个）
- ✅ 用于 `group_by()`, `filter()`, 控件筛选

**度量字段**（用于聚合计算）：
- ✅ 数值类型（Float64, Int64）
- ✅ 描述数量、金额、比率
- ✅ 用于 `sum()`, `mean()`, `count()`等

### 控件类型映射

| 唯一值数量 | 控件类型 | 默认选择策略 |
|-----------|----------|-------------|
| ≤ 10      | dropdown（单选） | 全部或最新值 |
| 11-50     | multiselect（多选） | 前3个 |
| 51-500    | multiselect | 前5个 + 提示"选项较多" |
| 500+      | multiselect | 前5个 + 建议级联 |

---

## 📦 框架 API 快速参考

### 1. 数据会话 (DataSession)
```python
session = DataSession()
session.load("alldata", alias="df") # 创建 df_df
print(session.get_ai_context())     # 获取元数据上下文
```

### 2. 移除宽度限制 (Notebook CSS)
```python
from IPython.display import HTML, display
display(HTML("<style>.jp-Notebook { --jp-notebook-max-width: 100% !important; }</style>"))
```

### 3. Markdown 输出
```python
from src.utils import print_markdown_table, enable_polars_markdown_display
# 强烈建议手动调用 print_markdown_table 以支持 PDF 拦截抓取
print_markdown_table(df.head(10)) 
```

---

## 💡 常见分析模式库

### 模式 1: 复杂聚合与分面
当分析“按[维度A]下的[维度B]保费构成”时，建议使用 `px.bar` 的 `facet_col` 或 `color` 参数进行对比分析。

### 模式 2: 长表逆透视 (Unpivot)
针对多保费项（自留、协议、临分）对比时，先 `unpivot` 再绘图是展示堆叠柱状图的最佳实践。

### 模式 3: 异常探测
利用 `pl.when().then().otherwise()` 标记离群值或特定的分保阈值（如法分线 4.5 亿）。
