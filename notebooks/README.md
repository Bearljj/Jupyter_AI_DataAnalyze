# Notebooks 目录说明

这个目录包含所有的 Jupyter Notebooks，按用途组织。

## 📁 目录结构

```
notebooks/
├── templates/          # Notebook 模板
│   ├── quick_start.ipynb                # 快速开始指南
│   ├── interactive_analysis.ipynb       # 交互式分析模板
│   ├── report_generation.ipynb          # 报告生成模板
│   └── blank_template.ipynb             # 空白模板
│
├── 01_exploration/     # 探索性分析
│   └── (你的探索性分析 notebooks)
│
├── 02_analysis/        # 专项分析
│   └── (你的专项分析 notebooks)
│
├── 03_reporting/       # 报告生成
│   └── (你的报告 notebooks)
│
└── 99_sandbox/         # 临时实验
    └── (你的临时分析 notebooks)
```

## 🎯 使用指南

### 开始新分析

1. **复制模板**
   ```bash
   cp templates/interactive_analysis.ipynb 02_analysis/my_new_analysis.ipynb
   ```

2. **打开 Notebook**
   - 在 Jupyter Lab 中打开
   - 运行初始化 Cell
   - 开始分析！

### 命名规范

建议使用以下命名格式：

```
<编号>_<主题>_<简短描述>.ipynb
```

示例：
- `01_reinsurance_monthly_analysis.ipynb`
- `02_product_performance_dashboard.ipynb`
- `03_weekly_report.ipynb`

### 模板说明

- **quick_start.ipynb** - 新用户入门，了解框架基础
- **interactive_analysis.ipynb** - 创建交互式仪表盘分析
- **report_generation.ipynb** - 生成定期报告
- **blank_template.ipynb** - 空白模板，自由发挥

## 💡 最佳实践

1. **使用模板**：从模板开始，而不是空白 notebook
2. **Cell 组织**：
   - Cell 1: 环境初始化
   - Cell 2: 数据加载
   - Cell 3: AI Context 生成
   - Cell 4+: 分析逻辑
3. **添加文档**：用 Markdown Cell 解释你的分析思路
4. **定期保存**：Jupyter Lab 会自动保存，但重要节点手动保存
5. **版本控制**：重要的 notebook 提交到 git

## 🔄 工作流建议

### 临时分析 → 固化流程

```
1. 在 99_sandbox/ 快速实验
   ↓
2. 验证成功后，移到对应目录
   ↓
3. 如果需要重复使用，提取函数到 src/
   ↓
4. 如果是定期报告，移到 03_reporting/
```

### 探索 → 分析 → 报告

```
1. 01_exploration/: 探索数据，理解结构
   ↓
2. 02_analysis/: 深入分析，验证假设
   ↓
3. 03_reporting/: 固化为报告，定期运行
```

## 🤖 与 AI 协作

每个 Notebook 都应该：

1. **生成 AI Context**
   ```python
   session.get_ai_context()
   ```

2. **复制给 AI**
   - 包括框架文档（docs/ai_context/main.md）
   - 包括当前数据概览

3. **AI 生成代码**
   - AI 知道数据结构
   - AI 知道可用工具
   - 生成的代码直接可用

## 📊 示例

查看 `templates/` 目录中的示例，了解如何：
- 加载和探索数据
- 创建交互式仪表盘
- 生成可视化报告
- 与 AI 高效协作

---

**开始你的数据分析之旅！** 🚀
