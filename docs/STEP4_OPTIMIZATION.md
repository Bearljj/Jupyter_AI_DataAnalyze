# Step 4 AI Prompt 优化说明

## 📋 **更新内容**

### **优化 1: 添加工作流程指导**

在 Step 4 输出的开头，添加了明确的工作流程指导：

```
🎯 工作流程（重要！请严格遵守）

第一步：理解需求，不要急着写代码！
  1. 仔细阅读用户需求
  2. 向用户确认理解
  3. 等待用户明确指令
  4. 不要上来就写代码

第二步：处理导入语句
  - 必须自己添加必要的 import
  - 不要假设所有库都已导入
  - 检查清单：px, pl, go, datetime 等

第三步：询问确认后再优化
  1. 先给出初版代码
  2. 等用户测试
  3. 根据反馈再优化
```

---

### **优化 2: 强调 import 处理**

#### **在多个位置强调**

1. **工作流程部分**
   ```python
   ⚠️ 重要：你需要自己添加必要的 import！
   
   在生成的代码开头必须包含：
   import plotly.express as px
   import polars as pl
   ...
   ```

2. **代码模板部分**
   ```python
   # Step 7: 生成分析代码
   
   # 1️⃣ 导入必要的库（根据实际需要添加！）
   import plotly.express as px
   import polars as pl
   ```

3. **检查清单部分**
   ```
   第 0 步：检查是否有必要的导入
   □ 代码开头有 import plotly.express as px
   □ 代码开头有 import polars as pl
   □ 不要遗漏任何需要的 import！
   ```

---

## 🎯 **优化目标**

### **1. 减少上下文浪费**

**问题**：
- AI 直接写代码 → 可能理解错需求
- 多次修改 → 浪费 token

**解决**：
- 先确认需求
- 再生成代码
- 避免无效的代码生成

---

### **2. 避免 import 错误**

**问题**：
- AI 假设所有库都已导入
- 代码运行时报错：`NameError: name 'px' is not defined`

**解决**：
- 明确告诉 AI 需要自己添加 import
- 提供 import 检查清单
- 在代码模板中展示正确做法

---

## 📊 **预期效果**

### **优化前的对话**

```
用户: 分析各年度保费趋势

AI: [直接生成代码]
```python
@pn.depends(...)
def update_dashboard(...):
    result = df.group_by('业务年度')...  # ← 硬编码维度
    fig = px.bar(...)  # ← px 未定义
```

用户: 报错了，px 未定义

AI: 抱歉，加上 import...
[重新生成代码]

用户: 还是不对，维度是硬编码的

AI: 抱歉，修改...
[又重新生成]
```

**问题**：
- 3轮对话才得到正确代码
- 浪费 token
- 用户体验差

---

### **优化后的对话**

```
用户: 分析各年度保费趋势

AI: 我理解你的需求是：
    - 按年度维度查看保费变化
    - 使用柱状图展示趋势
    - 支持其他维度的过滤
    
    请确认我的理解是否正确？

用户: 是的，开始吧

AI: [生成代码]
```python
# 导入必要的库
import plotly.express as px
import polars as pl

@pn.depends(...)
def update_dashboard(...):
    group_col = values.get('_aggregation_dimension')  # ← 使用变量
    ...
    fig = px.bar(...)  # ← px 已导入
```
```

**效果**：
- 1轮确认 + 1轮生成 = 2轮对话
- 节省 token
- 代码正确率高

---

## 🔄 **更新步骤**

### **已完成**

1. ✅ 修改 `notebooks/templates/step4_standalone.py`
2. ✅ 添加工作流程指导
3. ✅ 强调 import 处理
4. ✅ 更新代码模板
5. ✅ 更新检查清单
6. ✅ 重新生成 `quick_start.ipynb`

---

### **使用新模板**

#### **方式 1: 创建新分析**

```bash
python3 scripts/new_analysis.py my_analysis
```

新创建的 notebook 会使用优化后的 Step 4。

---

#### **方式 2: 更新现有 notebook**

在现有 notebook 的 Step 4 cell 中，执行以下代码（已经有了，只需运行）：

```python
import os

def find_project_root():
    current = os.path.abspath('.')
    while current != '/':
        if (os.path.exists(os.path.join(current, 'src')) and 
            os.path.exists(os.path.join(current, 'notebooks', 'templates'))):
            return current
        current = os.path.dirname(current)
    return os.path.abspath('.')

project_root = find_project_root()
step4_path = os.path.join(project_root, 'notebooks', 'templates', 'step4_standalone.py')

if os.path.exists(step4_path):
    exec(open(step4_path).read())
```

---

## 📝 **输出示例**

运行 Step 4 后，会看到：

```
================================================================================
📋 **复制以下所有内容给 AI**
================================================================================

## 📊 数据结构
[数据信息...]

================================================================================
## 🎯 工作流程（重要！请严格遵守）
================================================================================

📌 **第一步：理解需求，不要急着写代码！**
[详细说明...]

📌 **第二步：处理导入语句**
⚠️ 重要：你需要自己添加必要的 import！
[详细说明...]

📌 **第三步：询问确认后再优化**
[详细说明...]

================================================================================
## 📚 Panel Dashboard 完整使用指南
================================================================================
[规则和示例...]

✅ 检查清单（生成代码后必须检查）

第 0 步：检查是否有必要的导入
□ 代码开头有 import plotly.express as px
□ 代码开头有 import polars as pl
...
```

---

## 🎯 **关键改进点**

### **1. 减少无效对话**

- ✅ 先确认需求再写代码
- ✅ 避免理解错误导致的重写
- ✅ 节省 token 和时间

### **2. 提高代码正确率**

- ✅ 明确 import 要求
- ✅ 提供完整的代码模板
- ✅ 详细的检查清单

### **3. 更好的用户体验**

- ✅ AI 先确认理解
- ✅ 生成的代码更可靠
- ✅ 减少调试时间

---

## 📚 **相关文件**

- **源文件**: `notebooks/templates/step4_standalone.py`
- **模板**: `notebooks/templates/quick_start.ipynb`
- **生成脚本**: `scripts/reset_quick_start.py`
- **创建脚本**: `scripts/new_analysis.py`

---

**优化已完成！现在使用新模板创建的 notebook 会有更好的 AI 交互体验。** ✅
