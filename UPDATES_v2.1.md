# 更新说明 - v2.1

**更新日期**: 2025-12-21  
**版本**: 2.1

---

## 🆕 新增功能

### 1. **Dropdown 全选功能**

所有 dropdown 控件现在自动包含"全选"选项，并默认选中。

**效果**:
```
下拉选项：
  - 全选 ← 默认
  - 2020
  - 2021  
  - 2022
  - 2023
  - 2024
```

**行为**:
- **选择"全选"**: 不应用该维度的过滤，显示所有数据
- **选择具体值**: 只显示该值的数据

**在更新函数中处理**:
```python
def update_dashboard(controls):
    filters = []
    for dim in selected_dimensions:
        value = controls[dim]
        if isinstance(value, list):  # multiselect
            if '全选' not in value:
                filters.append(pl.col(dim).is_in(value))
        else:  # dropdown
            if value != '全选':  # ← 关键：排除"全选"
                filters.append(pl.col(dim) == value)
    
    # 应用过滤
    filtered = df_df
    if filters:
        for f in filters:
            filtered = filtered.filter(f)
```

### 2. **动态维度解析（AI Context更新）**

AI 现在被要求**动态解析** `selected_dimensions`，不再硬编码字段名。

**旧方式**（硬编码）:
```python
def update_dashboard(controls):
    year = controls['业务年度']  # ❌ 硬编码
    products = controls['业务险种']
    # 如果用户选了其他维度，会报错
```

**新方式**（动态）:
```python
def update_dashboard(controls):
    # ✅ 动态获取所有维度的值
    dim_values = {dim: controls[dim] for dim in selected_dimensions}
    
    # 构建过滤条件
    filters = []
    for dim in selected_dimensions:
        value = dim_values[dim]
        if isinstance(value, list):
            if '全选' not in value:
                filters.append(pl.col(dim).is_in(value))
        else:
            if value != '全选':
                filters.append(pl.col(dim) == value)
    
    # 应用过滤
    filtered = df_df
    if filters:
        for f in filters:
            filtered = filtered.filter(f)
    
    # 使用第一个维度分组
    if len(selected_dimensions) > 0:
        group_by_dim = selected_dimensions[0]
        result = filtered.group_by(group_by_dim).agg([...])
```

---

## 💡 使用示例

### 场景 1: 用户选择单个维度

```python
selected_dimensions = ['业务年度']
```

**仪表盘控件**:
```
业务年度: [下拉框]
  全选 ← 默认
  2020
  2021
  2022
```

**用户选择"全选"** → 显示所有年度的汇总  
**用户选择"2022"** → 只显示 2022 年的数据

### 场景 2: 用户选择多个维度

```python
selected_dimensions = ['业务年度', '业务险种']
```

**仪表盘控件**:
```
业务年度: [下拉框]
  全选 ← 默认
  2020-2024

业务险种: [多选框]
  ☑ 险种A
  ☑ 险种B
  ☑ 险种C
```

**用户选择**:
- 业务年度: "全选"
- 业务险种: 选择 A和B

**结果**: 显示所有年度的险种A和B的数据

---

## 🔧 技术细节

### DashboardBuilder.from_data() 更新

```python
# 修改位置: src/dashboard/builder.py, line 113-132

# 旧代码
options=unique_values
default=unique_values[-1]

# 新代码  
options_with_all = ['全选'] + unique_values
options=options_with_all
default='全选'
```

### AI Context 更新

**文件**: `docs/ai_context/main.md`

**新增章节**:
- ⚠️ 工作流澄清 - AI 职责说明
- 动态维度解析示例
- "全选"处理逻辑

---

## ✅ 向后兼容

这些更新**完全向后兼容**：

1. **已有代码**: 不会破坏现有的 update_dashboard 函数
2. **手动控件**: 老的 add_dropdown() 方式仍然可用
3. **选项处理**: AI 需要更新逻辑以处理"全选"，但这是增强而非破坏性变更

---

## 🚀 升级指南

### 对于用户

1. **无需操作**: 新创建的仪表盘自动包含"全选"
2. **已有仪表盘**: 重新运行生成代码即可

### 对于 AI

1. **阅读更新的 AI Context**: `docs/ai_context/main.md` v2.1
2. **使用动态解析**:  遍历 `selected_dimensions`
3. **处理"全选"**: 在过滤逻辑中排除

---

## 📚 相关文档

- **AI Context v2.1**: `docs/ai_context/main.md`
- **工作流澄清**: `docs/WORKFLOW_CLARIFICATION.md`
- **Quick Start**: `notebooks/templates/quick_start.ipynb`

---

**享受更灵活的数据分析！** 🎉
