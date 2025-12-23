# 📋 如何使用 Step 4 AI Prompt Cell

## 🎯 **目的**

Step 4 Cell 包含了**所有** AI 需要知道的信息，可以直接复制给 AI，无需让 AI 访问你的硬盘。

---

## 🚀 **使用步骤**

### **Step 1: 打开你的分析 Notebook**

例如通过以下命令创建：
```bash
python3 scripts/new_analysis.py 我的分析
```

### **Step 2: 运行 Step 1-3**

- **Step 1**: 初始化环境（包含 CSS 宽度修复）
- **Step 2**: 加载数据
- **Step 3**: 生成基本的数据概览

### **Step 3: 创建 Step 4 Cell**

在你的 Notebook 中创建一个新 cell，复制以下内容：

```python
# 从模板文件读取并执行
with open('notebooks/templates/step4_ai_prompt.py', 'r', encoding='utf-8') as f:
    exec(f.read())
```

**或者**直接复制 `notebooks/templates/step4_ai_prompt.py` 的全部内容到新 cell。

### **Step 4: 运行这个 Cell**

运行后会输出完整的 AI Prompt，包括：
- 你的数据结构（从 `session.get_ai_context()`）
- 完整的 Panel Dashboard 使用指南
- 代码模板
- 常见错误对比
- 检查清单

### **Step 5: 复制输出给 AI**

**复制 Step 4 的全部输出文本**，然后给 AI，并补充你的需求：

```
[粘贴 Step 4 的全部输出]

我的分析需求：
分析各业务险种在不同年度的保费增长趋势和赔付率变化

要求：
- 按业务险种分组
- 显示 2005 年以后的数据
- 包含保费柱状图和赔付率折线图
- 图表要占满屏幕宽度
```

### **Step 6: 获取 AI 生成的代码**

AI 会生成完整的 Panel Dashboard 代码，包括：
- CSS 宽度修复
- 正确的导入语句
- 使用 `PanelDashboardBuilder`
- `@pn.depends` 装饰器
- 动态过滤逻辑
- Plotly 图表

### **Step 7: 运行 AI 生成的代码**

在新 cell 中粘贴 AI 生成的代码并运行。

---

## ✅ **优势**

1. **无需文件访问**: AI 不需要访问你的硬盘
2. **一次性复制**: 所有必要信息都在一个输出中
3. **完整文档**: 包含所有规则、示例、常见错误
4. **即时更新**: 自动包含最新的数据结构信息

---

## 📝 **示例对话**

**你复制给 AI：**
```
========================================
📋 **复制以下所有内容给 AI**
========================================

## 📊 数据结构

字段列表：
- 业务年度 (String): 50 个唯一值
- 业务险种 (String): 15 个唯一值
- 总保费 (Float64): 数值范围 0 - 10000000
...

========================================
## 📚 Panel Dashboard 完整使用指南
========================================

# 🚨 **关键规则（必须遵守）**

## 1. 必须使用 PanelDashboardBuilder
...

[完整的文档内容]
```

**然后补充：**
```
我的需求：分析各险种的保费规模和赔付率
```

**AI 回复：**
```python
# AI 生成的完整代码
from IPython.display import HTML, display
display(HTML("""<style>...</style>"""))

import panel as pn
from src.dashboard import PanelDashboardBuilder
...
```

---

## 🎯 **文件位置**

- **模板文件**: `notebooks/templates/step4_ai_prompt.py`
- **README**: `notebooks/templates/STEP4_README.md`（本文件）

---

## 💡 **提示**

- **首次使用**：建议完整阅读输出的文档，了解所有规则
- **后续使用**：可以直接复制输出 + 需求给 AI
- **自定义**：可以修改 `step4_ai_prompt.py` 添加你的特定要求

---

**现在就试试吧！** 🚀
