# ⚠️ 重要：交互式图表说明

## 🎯 **交互式 vs 静态分享**

### **问题：为什么 HTML 中交互失效？**

**两种交互类型**：

1. **📊 Plotly 图表交互**（缩放、悬停、选择）
   - ✅ 在静态 HTML 中**应该工作**
   - 需要正确的导出设置

2. **🎛️ 仪表盘控件交互**（ipywidgets：dropdown、slider）
   - ❌ 在静态 HTML 中**不会工作**
   - 需要 Python kernel 运行

---

## ✅ **解决方案矩阵**

| 需求 | 推荐方案 | 命令 | 交互程度 |
|-----|---------|------|---------|
| 快速查看结果 | Static HTML | `jupyter nbconvert` | ⭐ 仅 Plotly |
| 团队协作使用 | Voila | `./scripts/serve_interactive.sh` | ⭐⭐⭐ 完全交互 |
| 正式汇报 | PDF | `nbconvert --to pdf` | 无交互 |
| 公开展示 | GitHub Pages + Voila | 部署服务 | ⭐⭐⭐ 完全交互 |

---

## 🚀 **完全交互式分享（Voila）**

### **本地使用**

```bash
# 安装 Voila
pip install voila

# 启动交互式应用
voila notebooks/your_analysis.ipynb

# 或使用脚本
./scripts/serve_interactive.sh notebooks/your_analysis.ipynb
```

**访问**: `http://localhost:8866`

**效果**:
- ✅ 所有仪表盘控件可用
- ✅ Plotly 图表可交互
- ✅ 实时计算
- ✅ 像 Web 应用一样

### **分享给团队（内网）**

**在服务器上部署**：
```bash
# SSH 到服务器
ssh user@server

# 克隆/上传项目
cd /path/to/project

# 启动 Voila（后台运行）
nohup voila notebooks/your_analysis.ipynb \
    --port=8866 \
    --no-browser \
    --Voila.ip=0.0.0.0 \
    > voila.log 2>&1 &

# 查看日志
tail -f voila.log
```

**团队访问**: `http://server-ip:8866`

### **云部署（外网访问）**

**使用 ngrok（快速测试）**：
```bash
# 安装 ngrok
brew install ngrok

# 启动 Voila
voila notebooks/your_analysis.ipynb --port=8866 &

# 创建公网隧道
ngrok http 8866
```

会得到一个公网 URL：`https://xxxxx.ngrok.io`

**使用云服务**：
- **Heroku**: 免费，需要 Dockerfile
- **Binder**: 免费，GitHub 集成
- **Streamlit Cloud**: 需要转换为 Streamlit
- **AWS/Azure**: 完全控制，需要付费

---

## 📊 **Plotly 图表交互（静态 HTML）**

如果只需要 Plotly 图表交互，不需要仪表盘：

### **方法 1：直接导出 Plotly 图表**

```python
# 在 Notebook 中
import plotly.graph_objects as go

fig = go.Figure(...)

# 导出为独立 HTML
fig.write_html("reports/chart.html", 
               include_plotlyjs='cdn',  # 使用 CDN
               config={'displayModeBar': True})  # 显示工具栏
```

### **方法 2：确保 nbconvert 正确导出**

```bash
# 使用正确的配置
jupyter nbconvert --to html \
    --template lab \
    --no-input \
    notebooks/your_analysis.ipynb
```

**检查 HTML 中的 Plotly**：
打开生成的 HTML，按 F12 查看控制台，确保没有 JavaScript 错误。

---

## 🎨 **混合方案（推荐）**

**场景**：既要静态报告，又要交互探索

### **创建两个版本**

**1. 静态报告版**（给领导）：
```bash
# 只显示最终结果，隐藏代码
jupyter nbconvert --to html --no-input \
    notebooks/analysis.ipynb \
    -o reports/analysis_report.html
```

**2. 交互探索版**（给团队）：
```bash
# 完整交互式应用
./scripts/serve_interactive.sh notebooks/analysis.ipynb
```

### **在 Notebook 中分离**

```python
# ========================================
# 📊 静态报告部分
# ========================================
# 这部分会出现在静态 HTML 中

# 关键发现
print("## 主要发现")
print("1. 总保费增长 15%")
print("2. 综合成本率下降 2%")

# 核心图表（Plotly，可交互）
fig = px.bar(summary_data, ...)
fig.show()

# ========================================
# 🎛️ 交互探索部分（需要 Voila）
# ========================================
# 仪表盘控件
dashboard = DashboardBuilder(...)
dashboard.build()
```

---

## 🔧 **故障排除**

### **问题 1: Plotly 图表在 HTML 中不显示**

**检查**：
```python
# 在 Notebook 中运行
import plotly.io as pio
print(pio.renderers.default)  # 应该是 'notebook'
```

**修复**：
```python
import plotly.io as pio
pio.renderers.default = "notebook"

# 然后重新运行 nbconvert
```

### **问题 2: HTML 文件很大**

**原因**: Plotly 图表包含大量数据

**优化**：
```python
# 1. 减少数据点
result_top = result.head(50)  # 只显示前 50 条

# 2. 使用外部 Plotly.js
fig.write_html("chart.html", include_plotlyjs='cdn')
```

### **问题 3: Voila 启动失败**

**检查依赖**：
```bash
pip install voila ipywidgets plotly polars
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

**查看日志**：
```bash
voila notebook.ipynb --debug
```

---

## 📚 **快速参考**

### **静态 HTML（Plotly 可交互）**
```bash
jupyter nbconvert --to html --no-input notebook.ipynb
```

### **完全交互（Voila）**
```bash
voila notebook.ipynb
# 或
./scripts/serve_interactive.sh notebook.ipynb
```

### **导出单个 Plotly 图表**
```python
fig.write_html("chart.html")
```

### **云部署（ngrok）**
```bash
voila notebook.ipynb --port=8866 &
ngrok http 8866
```

---

## 💡 **最佳实践**

1. **分离静态和交互内容**
   - 静态：用 `nbconvert`
   - 交互：用 `voila`

2. **优化 Plotly 图表**
   - 限制数据量
   - 使用 CDN（`include_plotlyjs='cdn'`）

3. **测试 HTML**
   - 离线打开测试
   - 检查 JavaScript 控制台

4. **文档说明**
   - 告知用户哪些可交互
   - 提供 Voila 链接（如果需要完整交互）

---

**选择合适的方案，享受交互式数据分析！** 🎉
