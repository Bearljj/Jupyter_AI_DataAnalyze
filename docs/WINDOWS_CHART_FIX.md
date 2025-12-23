# Windows 图表显示问题完整解决方案

---

## 🔍 **常见原因和解决方案**

### **问题 1: Panel 扩展未加载**

#### **症状**
- Panel dashboard 不显示
- 只看到空白或加载中

#### **解决方案**

在 notebook 的**第一个 cell**（Step 1）确保包含：

```python
import panel as pn

# ✅ 必须！加载 Plotly 扩展
pn.extension('plotly', sizing_mode='stretch_width')
```

**检查**: 运行诊断脚本

```python
# 在 notebook 新 cell 中运行
%run scripts/diagnose_windows_charts.py
```

---

### **问题 2: Plotly 渲染器设置错误**

#### **症状**
- Plotly 图表不显示
- 控制台报错 "Plotly renderer not set"

#### **解决方案**

```python
# 方法 1: 设置默认渲染器
import plotly.io as pio
pio.renderers.default = 'notebook'

# 方法 2: 或使用 jupyterlab 渲染器
pio.renderers.default = 'jupyterlab'

# 方法 3: 显式指定渲染器
fig.show(renderer='notebook')
```

**完整示例**:

```python
import plotly.express as px
import plotly.io as pio

# 设置渲染器
pio.renderers.default = 'jupyterlab'

# 创建图表
fig = px.bar(df, x='x', y='y')

# 显示
fig.show()
```

---

### **问题 3: Jupyter Lab 扩展未安装**

#### **症状**
- 图表区域显示 "Loading..."
- 或显示原始 JSON

#### **解决方案**

```powershell
# 在虚拟环境中运行

# 1. 更新 JupyterLab
pip install --upgrade jupyterlab

# 2. 安装/重建扩展
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyterlab-plotly

# 3. 重建
jupyter lab build

# 4. 清除缓存
jupyter lab clean

# 5. 重启 Jupyter Lab
```

---

### **问题 4: CDN 资源加载失败**

#### **症状**
- 离线环境或网络受限
- 控制台显示 "Failed to load resource from CDN"

#### **解决方案**

使用本地资源而不是 CDN：

```python
import plotly.io as pio

# 配置为使用本地 Plotly.js
pio.renderers.default = 'iframe'

# 或强制内联模式
fig.show(config={'displayModeBar': False}, 
         include_plotlyjs='cdn')  # 改为 'inline'
```

**Panel 配置**:

```python
import panel as pn

# 使用内联资源
pn.extension('plotly', 
             sizing_mode='stretch_width',
             inline=True)  # ← 强制内联
```

---

### **问题 5: 浏览器兼容性**

#### **症状**
- 在某些浏览器中不显示
- 控制台有 JavaScript 错误

#### **解决方案**

**推荐浏览器**:
1. ✅ Chrome (最推荐)
2. ✅ Microsoft Edge (Chromium 版本)
3. ✅ Firefox

**避免**:
- ❌ IE 浏览器
- ❌ 旧版 Edge (非 Chromium)

**测试**:
```powershell
# 在不同浏览器中打开
# Chrome
start chrome http://localhost:8888

# Edge
start msedge http://localhost:8888
```

---

### **问题 6: 中文字体问题**

#### **症状**
- 中文显示为方框 □□□
- 或显示乱码

#### **解决方案**

```python
import plotly.express as px
import plotly.graph_objects as go

# 配置中文字体
fig.update_layout(
    font=dict(
        family="Microsoft YaHei, SimHei, Arial",  # Windows 字体
        size=12
    )
)
```

**全局配置**:

```python
import plotly.io as pio

# 设置默认字体
pio.templates["custom"] = pio.templates["plotly"]
pio.templates["custom"].layout.font.family = "Microsoft YaHei"
pio.templates.default = "custom"
```

---

### **问题 7: 防火墙/代理阻止**

#### **症状**
- 网络环境严格
- CDN 资源被阻止

#### **解决方案**

**方法 1**: 配置代理

```python
import os

# 设置代理
os.environ['HTTP_PROXY'] = 'http://proxy.company.com:8080'
os.environ['HTTPS_PROXY'] = 'http://proxy.company.com:8080'
```

**方法 2**: 完全离线模式

```python
import plotly.io as pio

# 使用完全内联模式
pio.renderers.default = 'iframe'

# 创建图表
fig = px.bar(...)

# 显示（包含所有资源）
fig.show(include_plotlyjs='inline')
```

---

### **问题 8: 内存不足**

#### **症状**
- 大数据量时图表不显示
- Jupyter 卡死

#### **解决方案**

```python
# 限制显示数据量
result = df.group_by('category').agg([...])

# ✅ 只显示 Top 20
result_display = result.head(20)

# 创建图表
fig = px.bar(result_display.to_pandas(), ...)
```

---

## 🔧 **完整的修复流程**

### **步骤 1: 诊断问题**

在 Jupyter notebook 新 cell 中运行：

```python
%run scripts/diagnose_windows_charts.py
```

查看输出，找出具体问题。

---

### **步骤 2: 应用对应修复**

根据诊断结果，应用上面的解决方案。

---

### **步骤 3: 标准化 Step 1**

确保 notebook 的 Step 1 包含：

```python
# Step 1: 初始化（必须在最开始运行）

from IPython.display import HTML, display
import panel as pn
import polars as pl
import plotly.io as pio

# CSS 修复（JupyterLab 宽度）
display(HTML('''
<style>
    .jp-Notebook { --jp-notebook-max-width: 100% !important; }
    .jp-Notebook-cell, .jp-Cell-outputWrapper, 
    .jp-OutputArea-output, .jp-OutputArea-child { 
        max-width: none !important; 
        width: 100% !important; 
    }
    .bk-root, .bk-root > .bk { 
        width: 100% !important; 
        max-width: none !important; 
    }
</style>
'''))

# Panel 扩展（关键！）
pn.extension('plotly', 
             sizing_mode='stretch_width',
             inline=True)  # Windows 推荐

# Plotly 渲染器
pio.renderers.default = 'jupyterlab'

# 中文字体配置
pio.templates["custom"] = pio.templates["plotly"]
pio.templates["custom"].layout.font.family = "Microsoft YaHei, SimHei, Arial"
pio.templates.default = "custom"

print("✅ 环境初始化完成")
print(f"Panel 版本: {pn.__version__}")
print(f"Plotly 渲染器: {pio.renderers.default}")
```

---

### **步骤 4: 创建图表的标准模板**

```python
import plotly.express as px

# 创建图表
fig = px.bar(df, x='x', y='y', title='标题')

# 配置（确保兼容性）
fig.update_layout(
    autosize=True,
    width=None,  # 不固定宽度
    height=600,
    font=dict(family="Microsoft YaHei, SimHei, Arial")
)

# 显示（指定渲染器）
fig.show()
```

---

### **步骤 5: 重启 Jupyter Lab**

```powershell
# 关闭当前 Jupyter Lab (Ctrl+C)

# 清除缓存
jupyter lab clean

# 重启
jupyter lab
```

---

## 🧪 **测试用例**

### **测试 1: 简单 Plotly 图表**

```python
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 5, 3, 7, 4]
})

fig = px.line(df, x='x', y='y', title='测试图表')
fig.show()

# 应该显示折线图
```

### **测试 2: Panel Dashboard**

```python
import panel as pn
pn.extension('plotly')

widget = pn.widgets.IntSlider(name='值', start=0, end=10, value=5)

@pn.depends(widget.param.value)
def update(value):
    return f"当前值: {value}"

dashboard = pn.Column(widget, update)
dashboard

# 应该显示交互式 slider
```

### **测试 3: 中文显示**

```python
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    '年份': ['2022', '2023', '2024'],
    '保费': [100, 150, 200]
})

fig = px.bar(df, x='年份', y='保费', title='保费趋势')
fig.show()

# 应该正确显示中文
```

---

## 📋 **快速检查清单**

运行每个测试，打勾通过的：

- [ ] Step 1 包含 `pn.extension('plotly')`
- [ ] 简单 Plotly 图表能显示
- [ ] Panel dashboard 能显示
- [ ] 中文字体正常
- [ ] 浏览器控制台（F12）无错误
- [ ] 使用推荐浏览器（Chrome/Edge）
- [ ] Jupyter Lab 版本 >= 3.0
- [ ] 网络正常（或使用 inline 模式）

---

## 🆘 **还是不行？**

### **终极解决方案：重新安装环境**

```powershell
# 1. 备份当前 notebooks
# 复制 notebooks/ 文件夹到安全位置

# 2. 删除虚拟环境
rmdir /s .venv

# 3. 重新创建
python -m venv .venv
.venv\Scripts\activate

# 4. 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 5. 安装 Jupyter Lab 扩展
pip install --upgrade jupyterlab
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyterlab-plotly

# 6. 重建
jupyter lab build

# 7. 启动
jupyter lab
```

---

## 💡 **预防措施**

### **标准化 requirements.txt**

确保包含最新版本：

```txt
panel>=1.3.0
plotly>=5.17.0
polars>=0.19.0
jupyterlab>=4.0.0
jupyter-bokeh>=4.0.0
```

### **使用项目模板**

始终从 `quick_start.ipynb` 创建新 notebook，确保 Step 1 配置正确。

---

**按照这个指南，99% 的图表显示问题都能解决！** ✅
