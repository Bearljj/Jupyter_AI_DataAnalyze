# 🚀 Quick Start 使用指南（更新版）

## ✅ **更新内容**

**新增了 Step 4**：自动生成包含所有文档的完整 AI Prompt！

现在的流程：
1. Step 1: 初始化环境 + CSS 宽度修复 ✅
2. Step 2: 加载数据 ✅
3. Step 3: 生成基本数据结构信息
4. **Step 4: 生成完整 AI Prompt** ⭐ **（新增）**
5. Step 5: 选择分析维度
6. Step 6: 创建 Panel 仪表盘
7. Step 7: AI 生成分析逻辑（粘贴 AI 的代码）
8. Step 8: 导出 HTML

---

## 🎯 **Step 4 的作用**

**Step 4 会自动输出完整的 AI Prompt，包括**：

1. **数据结构信息**（从 `session.get_ai_context()`）
2. **完整的 Panel Dashboard 使用指南**（嵌入在输出中）
3. **代码模板**
4. **关键规则清单**
5. **常见错误对比**
6. **检查清单**

**你只需要复制 Step 4 的全部输出给 AI，无需手动打开文档！**

---

## 📋 **完整使用流程**

### **1. 创建新分析**

```bash
python3 scripts/new_analysis.py 我的分析名称
```

这会从 `notebooks/templates/quick_start.ipynb` 复制一个新的 notebook。

### **2. 在 Jupyter Lab 中打开**

打开新创建的 notebook，例如：
```
notebooks/02_analysis/我的分析名称.ipynb
```

### **3. 按顺序运行 Step 1-4**

#### **Step 1: 初始化环境**
- 运行后会输出：`✅ JupyterLab 宽度限制已移除`
- 这很关键，让图表占满屏幕

#### **Step 2: 加载数据**
- 修改数据文件路径（如果需要）
- 运行后显示数据预览

#### **Step 3: 生成基本 AI Context**
- 显示数据结构信息

#### **Step 4: 生成完整 AI Prompt** ⭐
- 运行这个 cell
- **复制全部输出**

### **4. 给 AI 的提示**

**复制 Step 4 的全部输出**，然后补充你的需求：

```
[粘贴 Step 4 的全部输出]

========================================
我的分析需求：
========================================

分析各业务险种在不同年度的保费增长趋势和赔付率变化

要求：
- 按业务险种分组
- 显示 2005 年以后的数据
- 包含保费柱状图和赔付率折线图
- 图表要占满屏幕宽度
- 可以在 Jupyter 中交互
- 可以导出为 HTML 文件
```

### **5. 获取 AI 生成的代码**

AI 会生成完整的代码，包括：
- CSS 宽度修复（已在 Step 1 完成，但 AI 可能会再生成一次）
- 正确的导入语句
- 使用 `PanelDashboardBuilder`
- `@pn.depends` 装饰器
- 动态过滤逻辑
- Plotly 图表

### **6. 运行 Step 5-6**

#### **Step 5: 选择维度**
- 根据需要修改维度列表
- 运行后显示已选择的维度

#### **Step 6: 创建仪表盘**
- 自动创建 Panel Dashboard 控件

### **7. 粘贴 AI 代码到 Step 7**

在 Step 7 的 cell 中：
1. 删除示例代码
2. 粘贴 AI 生成的代码
3. 运行

如果一切正常，你会看到：
- 交互式控件（下拉框、多选框等）
- 动态更新的图表
- 图表占满整个屏幕宽度 ✅

### **8. 导出 HTML（Step 8）**

如果 AI 的代码没有包含 `dashboard.save()`，运行 Step 8 手动导出。

---

## 🎉 **优势**

### **之前的流程**
```
1. 运行 notebook
2. 告诉 AI: "请阅读 docs/ai_context/main.md"
3. AI: "我无法访问你的文件系统"
4. 你手动打开文档
5. 复制文档内容给 AI
6. ...重复多次...
```

### **现在的流程**
```
1. 运行 Step 1-4
2. 复制 Step 4 的输出给 AI
3. AI 生成代码
4. 粘贴运行
5. 完成！✨
```

---

## 📊 **Step 4 输出示例**

```
================================================================================
📋 **复制以下所有内容给 AI**
================================================================================

## 📊 数据结构

数据集: alldata
总行数: 150,000
总列数: 45

字段列表:
- 业务年度 (String): 50 个唯一值
- 业务险种 (String): 15 个唯一值
- 总保费 (Float64): 数值范围 0 - 10000000
...

================================================================================
## 📚 Panel Dashboard 完整使用指南
================================================================================

# 🚨 **关键规则（必须遵守）**

## 1. 必须使用 PanelDashboardBuilder

```python
# ✅ 正确
from src.dashboard import PanelDashboardBuilder
...
```

[完整的使用指南、代码模板、常见错误对比等]

================================================================================
💡 **使用方法**
================================================================================

1. 复制上面的所有内容给 AI
2. 告诉 AI 你的具体分析需求
3. AI 会生成符合规范的 Panel Dashboard 代码
4. 粘贴代码到新 cell 并运行

================================================================================
```

---

## ⚠️ **注意事项**

1. **Step 4 需要 Step 3 先运行**
   - 因为 Step 4 使用 `session.get_ai_context()`
   
2. **Step 4 依赖模板文件**
   - 文件位置: `notebooks/templates/step4_ai_prompt.py`
   - 如果文件不存在，会使用简化版本

3. **重新生成模板**
   - 如果修改了文档，运行：
     ```bash
     python3 scripts/reset_quick_start.py
     ```

---

## 🔧 **自定义 Step 4**

如果你想自定义 Step 4 的输出，编辑：
```
notebooks/templates/step4_ai_prompt.py
```

然后重新生成 quick_start.ipynb：
```bash
python3 scripts/reset_quick_start.py
```

---

## 📚 **相关文件**

- `scripts/reset_quick_start.py` - 模板生成脚本
- `scripts/new_analysis.py` - 创建新分析
- `notebooks/templates/quick_start.ipynb` - Quick Start 模板
- `notebooks/templates/step4_ai_prompt.py` - Step 4 内容
- `notebooks/templates/STEP4_README.md` - Step 4 说明
- `docs/ai_context/AI_QUICK_REFERENCE.md` - AI 快速参考
- `docs/ai_context/PANEL_GUIDE.md` - Panel 完整指南
- `docs/ai_context/main.md` - 主要文档

---

**现在开始创建你的第一个分析吧！** 🚀

```bash
python3 scripts/new_analysis.py 我的第一个分析
```
