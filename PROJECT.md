# 📋 Jupyter AI DataAnalyze - 项目档案

**项目名称：** Jupyter AI DataAnalyze  
**版本：** 1.0.0  
**创建日期：** 2024-12-21  
**目的：** AI-Assisted 数据分析框架

---

## 🎯 项目目标

创建一个专为 AI 协作优化的数据分析框架，让数据分析师能够：
1. 通过自然语言与 AI 协作完成分析
2. 避免重复的样板代码
3. 快速创建交互式仪表盘
4. 从临时分析平滑过渡到定期报表

---

## 🏗️ 核心架构

### 三大支柱

1. **DataSession（数据会话）**
   - 一次加载，全局可用
   - 自动注入 Jupyter 命名空间
   - 生成 AI-Ready 的数据概览

2. **DashboardBuilder（仪表盘构建器）**
   - 预制交互组件
   - AI 只需编写业务逻辑
   - 自动处理回调和更新

3. **AI Context（AI 上下文）**
   - 框架工具文档
   - 实时数据结构信息
   - 最佳实践示例

---

## 📂 项目结构

```
Jupyter_AI_DataAnalyze/
├── config/                 # 配置管理
├── src/                    # 核心代码
│   ├── session.py          # ⭐ 数据会话
│   ├── data/               # 数据加载
│   ├── dashboard/          # ⭐ 交互仪表盘
│   ├── catalog/            # 数据目录（未来）
│   ├── visualization/      # 可视化（未来）
│   └── reporting/          # 报告生成（未来）
├── data/                   # 数据目录
├── notebooks/              # Jupyter Notebooks
│   └── templates/          # ⭐ 模板
├── docs/                   # 文档
│   ├── ai_context/         # ⭐ AI Context
│   └── guides/             # 用户指南
└── scripts/                # 工具脚本
```

---

## 🚀 快速开始

```bash
# 1. 进入项目
cd Jupyter_AI_DataAnalyze

# 2. 启动（自动安装依赖）
./start.sh

# 3. 打开快速开始 Notebook
# notebooks/templates/quick_start.ipynb
```

---

## 📖 核心文档

### 必读文档

1. **README.md** - 项目总览
2. **docs/ai_context/main.md** - AI Context（必须！）
3. **docs/guides/user_guide.md** - 完整用户指南
4. **notebooks/README.md** - Notebooks 组织说明

### 快速参考

- 快速开始：`notebooks/templates/quick_start.ipynb`
- API 文档：`docs/ai_context/main.md`
- 示例代码：`docs/examples/`（未来）

---

## 🔑 核心概念

### 工作流程

```
1. 启动 Jupyter Lab
   ↓
2. 初始化数据会话
   session = DataSession()
   session.load("data")
   ↓
3. 生成 AI Context
   print(session.get_ai_context())
   ↓
4. 复制给 AI，开始协作
   ↓
5. AI 生成代码 → 执行 → 迭代
   ↓
6. 满意后固化为仪表盘/报告
```

### 与 AI 的协作模式

```
你的职责：
- 确定分析目标
- 准备数据
- 生成 AI Context
- 验证结果

AI 的职责：
- 根据 AI Context 理解数据
- 生成分析代码
- 创建可视化
- 迭代优化
```

---

## 🛠️ 技术栈

### 核心库

- **Polars** - 高性能数据处理（比 Pandas 快 10-100倍）
- **Plotly** - 交互式可视化
- **Jupyter Lab** - 交互式开发环境
- **ipywidgets** - Jupyter 交互组件

### 数据格式

- **Parquet** - 主要数据格式（列式存储、高压缩率）
- **CSV/Excel** - 原始数据导入
- **JSON** - 元数据和配置

### 项目管理

- **uv** - Python 包管理器（极快）
- **Git** - 版本控制
- **dotenv** - 环境变量管理

---

## 📈 未来功能（TODO）

### Phase 1（已完成）✅
- [x] 数据会话管理
- [x] 交互式仪表盘
- [x] AI Context 文档
- [x] 快速开始模板

### Phase 2（计划中）
- [ ] 数据目录系统（自动索引多数据集）
- [ ] 数据剖析工具（自动生成数据概览）
- [ ] 报告生成器（一键生成 HTML 报告）
- [ ] 仪表盘模板库（预制常见分析仪表盘）

### Phase 3（规划中）
- [ ] 数据转换管道（原始数据 → Parquet）
- [ ] 自动化调度（定时运行报告）
- [ ] 数据质量检查
- [ ] 性能监控和优化

---

## 🎓 学习路径

### 新用户（1-2小时）

1. 阅读 README.md ✅
2. 运行 `./start.sh` ✅
3. 打开并运行 `notebooks/templates/quick_start.ipynb` ✅
4. 阅读生成的 AI Context ✅
5. 尝试用自己的数据做一个简单分析 ✅

### 进阶用户（1天）

1. 阅读完整的用户指南 `docs/guides/user_guide.md`
2. 了解所有 AI Context 文档 `docs/ai_context/main.md`
3. 创建自己的第一个交互式仪表盘
4. 尝试固化一个分析为定期报告

### 高级用户（持续）

1. 浏览源代码，理解实现
2. 根据需求扩展框架功能
3. 贡献示例到 `docs/examples/`
4. 更新 AI Context 文档

---

## 📞 获取帮助

### 文档

- **AI Context：** `docs/ai_context/main.md` - 最重要！
- **用户指南：** `docs/guides/user_guide.md`
- **代码示例：** `notebooks/templates/`

### 问题排查

1. 查看用户指南的"故障排查"部分
2. 检查是否在项目根目录运行
3. 确认依赖已安装：`uv sync`

---

## 📝 维护日志

### 2024-12-21 - v1.0.0（初始版本）

**已实现：**
- ✅ 项目结构创建
- ✅ 核心组件：DataSession, DashboardBuilder
- ✅ AI Context 文档
- ✅ 快速开始 Notebook
- ✅ 用户指南文档
- ✅ 启动脚本

**下一步：**
- 添加数据目录系统
- 添加更多 Notebook 模板
- 添加示例代码库

---

## 🎉 项目特色

### 为什么选择这个框架？

1. **AI-First 设计**
   - 不是为手写代码优化，而是为 AI 生成代码优化
   - AI Context 让 AI 准确理解你的数据和工具

2. **减少重复**
   - DataSession 避免重复的加载代码
   - Dashboard 避免重复的组件代码

3. **平滑过渡**
   - 从探索 → 分析 → 报告的自然演进
   - 临时代码可以轻松固化为可复用模块

4. **高性能**
   - 基于 Polars，比 Pandas 快 10-100 倍
   - Parquet 格式，节省空间，加载快速

---

**Enjoy your AI-powered data analysis journey!** 🚀
