# 🔧 Panel Dashboard 宽度问题技术说明

**问题**: Panel Dashboard 图表挤在左边，无法占满屏幕宽度  
**解决日期**: 2025-12-21  
**状态**: ✅ 已解决

---

## 📋 **问题表现**

- 图表只占据屏幕左侧约 60% 的宽度
- 即使设置了 `autosize=True` 和 `sizing_mode='stretch_width'` 也无效
- Jupyter Notebook 内和导出的 HTML 中都有此问题

---

## 🔍 **根本原因分析**

### **三层限制导致问题**

#### **1. JupyterLab 4 的 CSS 变量限制（最根本）**

```css
/* JupyterLab 4 默认样式 */
.jp-Notebook {
    --jp-notebook-max-width: 1140px;  /* ← 根本限制！*/
}
```

**影响**：
- 整个 notebook 的最大宽度被限制为 1140px
- 所有 cell 的输出都受此限制
- 即使子元素设置 `width: 100%` 也只能占满 1140px

#### **2. Panel/Bokeh 容器的默认行为**

```python
# Panel 默认不是 stretch_width
pn.Column(...)  # 默认 sizing_mode='fixed' 或 'scale_width'
```

**影响**：
- Panel 容器如果没有明确设置 `sizing_mode='stretch_width'`，会使用固定或比例宽度
- 即使外层容器很宽，内部容器也不会自动扩展

#### **3. Plotly 的 autosize 依赖**

```python
# Plotly 的 autosize 依赖父容器宽度
fig.update_layout(autosize=True)
```

**影响**：
- `autosize=True` 依赖父容器有明确的宽度信息
- 如果父容器宽度不明确，Plotly 回退到默认宽度（700px）
- 需要同时设置 `width=None` 告诉 Plotly 不使用固定宽度

---

## ✅ **完整解决方案**

### **层级 1: 移除 JupyterLab CSS 限制**

```python
from IPython.display import HTML, display

display(HTML("""
<style>
    /* 核心：覆盖 CSS 变量 */
    .jp-Notebook { 
        --jp-notebook-max-width: 100% !important; 
    }
    
    /* 确保所有输出容器不受限 */
    .jp-Notebook-cell, 
    .jp-Cell-outputWrapper, 
    .jp-OutputArea-output, 
    .jp-OutputArea-child { 
        max-width: none !important; 
        width: 100% !important; 
    }
    
    /* Panel 根容器强制铺满 */
    .bk-root, .bk-root > .bk { 
        width: 100% !important; 
        max-width: none !important; 
    }
</style>
"""))
```

**关键点**：
- `--jp-notebook-max-width: 100%` ← 最关键，解除根限制
- `!important` 确保覆盖默认样式
- 同时处理所有可能的容器层级

### **层级 2: Panel 全局和局部设置**

```python
# 全局设置
pn.extension('plotly', sizing_mode='stretch_width')

# 局部强化（在更新函数中）
return pn.Column(
    ...,
    sizing_mode='stretch_width',  # Column 本身
    width_policy='max'             # 额外保证占满最大宽度
)
```

**关键点**：
- 全局 `sizing_mode` 设置所有 Panel 对象的默认行为
- 局部 `sizing_mode` 确保特定容器的行为
- `width_policy='max'` 额外强制占满可用宽度

### **层级 3: Plotly 图表配置**

```python
fig.update_layout(
    height=600,
    width=None,       # ← 不使用固定宽度
    autosize=True,    # ← 自适应
    # 不要添加 responsive=True，Plotly 没有这个属性
)
```

**关键点**：
- `width=None` 明确告诉 Plotly 不要固定宽度
- `autosize=True` 启用自适应
- 不使用固定 `width=1000` 等值

### **层级 4: 导出 HTML 兼容（可选）**

如果需要导出的 HTML 也占满宽度，可以在 Panel 对象中嵌入 CSS：

```python
# 创建隐藏的 CSS pane
css_pane = pn.pane.HTML("""
<style>
    .bk-root { width: 100% !important; }
    .js-plotly-plot { width: 100% !important; }
</style>
""", width=0, height=0, margin=0)

return pn.Column(
    css_pane,  # ← 嵌入到 Panel 对象中
    pn.pane.Markdown(...),
    pn.pane.Plotly(fig),
    sizing_mode='stretch_width'
)
```

**关键点**：
- CSS 嵌入到 Panel 对象内部
- 导出 HTML 时会自动包含这些样式
- `width=0, height=0` 使其不可见但生效

---

## 🎯 **实施步骤**

### **对于新 Notebook**
1. 使用最新的 quick_start 模板（已包含所有修复）
2. Step 1 会自动运行 CSS 修复
3. AI 生成的代码会自动应用正确配置

### **对于现有 Notebook**
1. 在 notebook **开头**添加 CSS 修复 cell
2. 修改 `pn.extension()` 添加 `sizing_mode='stretch_width'`
3. 确保更新函数返回的 Column 设置了 `sizing_mode='stretch_width'`
4. 图表 `update_layout` 设置 `width=None, autosize=True`

---

## 📊 **效果对比**

### **修复前**
```
|<--- 1140px 限制 --->|
[图表挤在左边........]           空白区域
```

### **修复后**
```
|<----------- 100% 宽度 ----------->|
[图表占满整个屏幕宽度..............]
```

---

## ⚠️ **注意事项**

### **1. CSS 必须在 Notebook 开头**
如果后面才运行 CSS，之前的 cell 输出不会自动调整，需要重新运行。

### **2. 每个 Notebook 都需要**
CSS 只影响当前 notebook，打开新 notebook 需要重新运行。

### **3. 不要使用 responsive: True**
Plotly layout 没有 `responsive` 属性，会报错。

### **4. Panel pane 也要设置 sizing_mode**
```python
pn.pane.Plotly(fig, sizing_mode='stretch_width')  # ← 别忘了
```

---

## 🧪 **验证方法**

### **Jupyter 中验证**
1. 运行包含修复的 cell
2. 图表应该占满整个浏览器宽度
3. 调整浏览器窗口，图表应该随之调整

### **导出 HTML 验证**
1. `dashboard.save("test.html")`
2. 用浏览器打开 `test.html`
3. 图表应该占满浏览器宽度
4. 调整窗口，图表应该随之调整

---

## 🔗 **相关文件更新**

已更新以下文件包含完整修复：

- ✅ `scripts/reset_quick_start.py` - 模板生成脚本
- ✅ `docs/ai_context/main.md` - AI Context 主文档
- ✅ `docs/ai_context/PANEL_GUIDE.md` - Panel 完整指南
- ✅ `notebooks/templates/quick_start.ipynb` - Quick Start 模板

---

## 💡 **总结**

**核心原理**：
- JupyterLab 通过 CSS 变量限制了 notebook 宽度
- 需要通过 CSS 覆盖这个变量
- 同时确保 Panel 和 Plotly 都设置了正确的宽度行为

**最小修复代码**：
```python
# 1. CSS 修复（必须）
display(HTML("""<style>
.jp-Notebook { --jp-notebook-max-width: 100% !important; }
</style>"""))

# 2. Panel 设置（推荐）
pn.extension('plotly', sizing_mode='stretch_width')

# 3. 图表配置（推荐）
fig.update_layout(width=None, autosize=True)
```

**三行代码解决问题！** ✨

---

**问题已彻底解决，所有新项目都将自动应用此修复。** 🎉
