# 📚 文档使用指南

## 🎯 **给 AI 什么文档？**

### **答案：只需给 AI `docs/ai_context/main.md`**

**原因**：
- ✅ 已包含 Panel 和 ipywidgets 两种方案
- ✅ Panel 作为推荐方案（可导出 HTML）
- ✅ 包含所有核心要点和示例
- ✅ AI 自动知道何时用哪种方式

---

## 📋 **文档结构**

### **核心文档（必读）**
| 文档 | 用途 | 给 AI？ |
|------|------|--------|
| `docs/ai_context/main.md` | **AI Context 主文档** | ✅ **是** |

### **详细文档（参考）**
| 文档 | 用途 | 给 AI？ |
|------|------|--------|
| `docs/ai_context/PANEL_GUIDE.md` | Panel 完整教程 | 可选 |
| `docs/ai_context/CODE_TEMPLATE.md` | ipywidgets 模板 | 可选 |
| `docs/WORKFLOW_CLARIFICATION.md` | 工作流说明 | 可选 |
| `docs/PANEL_QUICKSTART.md` | 快速开始 | 用户看 |
| `PANEL_MIGRATION.md` | 迁移指南 | 用户看 |

---

## 💬 **如何给 AI 提示**

### **标准提示**

```
【使用 Jupyter AI DataAnalyze 框架】

请阅读 AI Context：
/Users/harold/working/Jupyter_AI_DataAnalyze/docs/ai_context/main.md

我想创建一个可以导出 HTML 的仪表盘，请使用 Panel Dashboard 方案。

我的需求：
[描述你的分析需求]
```

### **快速提示（AI 已熟悉框架）**

```
使用 Panel Dashboard，导出 HTML。
数据：df_df
维度：['业务年度', '业务险种']
需求：分析各险种保费，显示 Top 10
```

### **如果 AI 需要更多细节**

```
详细 Panel 教程见：
/Users/harold/working/Jupyter_AI_DataAnalyze/docs/ai_context/PANEL_GUIDE.md
```

---

## 🎯 **main.md 已包含的内容**

### ✅ **已整合 Panel 章节**（推荐方案）
- Panel 使用方法
- 完整代码示例
- 关键规则（5 条）
- @pn.depends 装饰器说明
- 与 ipywidgets 的区别

### ✅ **已整合 ipywidgets 章节**（备选方案）
- 自动创建方式
- 手动创建方式
- 适用场景

### ✅ **其他核心内容**
- 工作流澄清
- Polars API 更新（pl.len）
- 可视化规范（自适应、单位转换）
- Markdown 输出规范
- 维度识别指南
- 完整示例

---

## 🔄 **更新流程**

### **如果需要更新 AI 行为**

**只需更新 `main.md`**：
1. 编辑 `docs/ai_context/main.md`
2. 下次给 AI 时，它会读到新版本

### **如果有大量细节**

1. 在 `main.md` 中添加**精简版**（核心要点）
2. 创建**详细文档**（如 PANEL_GUIDE.md）
3. 在 `main.md` 中**引用**详细文档

---

## 📊 **文档权重**

```
main.md ⭐⭐⭐⭐⭐ (核心，AI 必读)
  ├─ Panel 章节 (推荐)
  ├─ ipywidgets 章节 (备选)
  ├─ 可视化规范
  ├─ API 参考
  └─ 完整示例

PANEL_GUIDE.md ⭐⭐⭐ (详细教程，需要时查阅)
PANEL_QUICKSTART.md ⭐⭐ (用户快速开始)
PANEL_MIGRATION.md ⭐⭐ (开发者迁移指南)
```

---

## ✅ **最佳实践**

### **给新 AI（首次交互）**

```
请阅读：
/Users/harold/working/Jupyter_AI_DataAnalyze/docs/ai_context/main.md

这是一个数据分析框架，请按照文档中的 Panel Dashboard 方式生成代码。
```

### **给熟悉的 AI（后续交互）**

```
继续使用 Panel Dashboard。
新需求：[...]
```

### **如果 AI 生成错误**

```
请查看 main.md 中的 Panel 关键规则：
1. 必须使用 @pn.depends 装饰器
2. 函数参数是 *args
3. [其他规则]
```

---

## 🎯 **总结**

| 问题 | 答案 |
|------|------|
| 给 AI 哪个文档？ | **`main.md`** |
| Panel 详细教程？ | **`PANEL_GUIDE.md`**（可选） |
| 需要同时给多个文档吗？ | ❌ **不需要** |
| main.md 够用吗？ | ✅ **够用**（已包含核心内容） |
| PANEL_GUIDE.md 的作用？ | 详细参考、深入学习 |

---

**推荐：只给 AI `main.md`，简单高效！** ✨
