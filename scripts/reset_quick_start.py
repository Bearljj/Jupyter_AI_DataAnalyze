#!/usr/bin/env python3
"""
生成全新的 Quick Start Notebook（Panel 版本）
包含完整的 AI Prompt Cell
"""

import json

# Notebook 结构
notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.12.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# ========================================
# Cell 定义
# ========================================

cells = {
    # 标题
    "title": {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# 🚀 Quick Start - Panel Dashboard\n",
            "\n",
            "**最新版本**: Phase 2.0 - Panel Integration  \n",
            "**特性**: 可导出静态 HTML（控件 + 图表都可交互）\n",
            "\n",
            "---\n",
            "\n",
            "## 📋 本 Notebook 的步骤\n",
            "\n",
            "1. **初始化环境** - 加载框架 + CSS 宽度修复\n",
            "2. **加载数据** - 从 Parquet 文件加载\n",
            "3. **生成基本 AI Context** - 数据结构信息\n",
            "4. **生成完整 AI Prompt** - 包含所有文档（复制给 AI）\n",
            "5. **选择维度** - 选择分析维度\n",
            "6. **创建 Panel 仪表盘** - AI 生成分析逻辑\n",
            "7. **导出 HTML** - 分享给他人\n",
            "\n",
            "---\n"
        ]
    },
    
    # Step 1: 初始化
    "step1_md": {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 📦 Step 1: 初始化环境\n",
            "\n",
            "加载框架 + CSS 宽度修复（让图表占满屏幕）"
        ]
    },
    
    "step1_code": {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# ========================================\n",
            "# 移除 JupyterLab 宽度限制（关键！）\n",
            "# ========================================\n",
            "from IPython.display import HTML, display\n",
            "\n",
            "display(HTML(\"\"\"\n",
            "<style>\n",
            "    /* 核心：解除 JupyterLab 4 的宽度限制 */\n",
            "    .jp-Notebook { \n",
            "        --jp-notebook-max-width: 100% !important; \n",
            "    }\n",
            "    \n",
            "    /* 确保所有输出容器占满宽度 */\n",
            "    .jp-Notebook-cell, \n",
            "    .jp-Cell-outputWrapper, \n",
            "    .jp-OutputArea-output, \n",
            "    .jp-OutputArea-child { \n",
            "        max-width: none !important; \n",
            "        width: 100% !important; \n",
            "    }\n",
            "    \n",
            "    /* Panel 根容器强制铺满 */\n",
            "    .bk-root, .bk-root > .bk { \n",
            "        width: 100% !important; \n",
            "        max-width: none !important; \n",
            "    }\n",
            "</style>\n",
            "\"\"\"))\n",
            "\n",
            "print(\"✅ JupyterLab 宽度限制已移除\")\n",
            "\n",
            "# ========================================\n",
            "# 加载框架\n",
            "# ========================================\n",
            "import polars as pl\n",
            "import plotly.express as px\n",
            "import panel as pn\n",
            "\n",
            "from src.session import DataSession\n",
            "from src.dashboard import PanelDashboardBuilder\n",
            "from src.utils import print_markdown_table\n",
            "\n",
            "# 初始化 Panel（全局设置 stretch_width）\n",
            "pn.extension('plotly', sizing_mode='stretch_width')\n",
            "\n",
            "print(\"✅ 环境初始化完成\")\n",
            "print(\"📚 框架版本: Phase 2.0 - Panel Integration\")\n"
        ]
    },
    
    # Step 2: 加载数据
    "step2_md": {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 📂 Step 2: 加载数据\n",
            "\n",
            "从 Parquet 文件加载数据"
        ]
    },
    
    "step2_code": {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 创建数据会话\n",
            "session = DataSession()\n",
            "\n",
            "# 加载数据（替换为你的数据文件）\n",
            "session.load(\"alldata\", alias=\"df\")  # 或 session.load(\"your_data.parquet\", alias=\"df\")\n",
            "\n",
            "# 验证数据\n",
            "print(f\"✅ 数据已加载: {df_df.height:,} 行 × {df_df.width} 列\")\n",
            "print(f\"📊 数据预览:\\n\")\n",
            "print_markdown_table(df_df.head(5))\n"
        ]
    },
    
    # Step 3: 基本 AI Context
    "step3_md": {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 🤖 Step 3: 生成基本 AI Context\n",
            "\n",
            "生成数据概览"
        ]
    },
    
    "step3_code": {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 生成基本 AI Context\n",
            "print(\"📋 数据结构信息:\\n\")\n",
            "print(\"=\" * 80)\n",
            "print(session.get_ai_context())\n",
            "print(\"=\" * 80)\n",
            "\n",
            "print(\"\\n💡 提示: 下一步会生成完整的 AI Prompt\")\n"
        ]
    },
    
    # Step 4: 完整 AI Prompt
    "step4_md": {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 📋 Step 4: 生成完整 AI Prompt\n",
            "\n",
            "**运行这个 cell，然后复制全部输出给 AI**\n",
            "\n",
            "这个 cell 会输出：\n",
            "- 数据结构信息\n",
            "- 完整的 Panel Dashboard 使用指南\n",
            "- 代码模板\n",
            "- 常见错误对比\n",
            "- 检查清单\n"
        ]
    },
    
    "step4_code": {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# ========================================\n",
            "# 📋 给 AI 的完整信息（复制全部输出给 AI）\n",
            "# ========================================\n",
            "\n",
            "# 直接执行最新的 Step 4 模板\n",
            "import os\n",
            "\n",
            "# 自动找到项目根目录\n",
            "def find_project_root():\n",
            "    \"\"\"向上查找包含 src/ 和 notebooks/templates/ 的项目根目录\"\"\"\n",
            "    current = os.path.abspath('.')\n",
            "    while current != '/':\n",
            "        # 检查是否存在项目标志\n",
            "        if (os.path.exists(os.path.join(current, 'src')) and \n",
            "            os.path.exists(os.path.join(current, 'notebooks', 'templates'))):\n",
            "            return current\n",
            "        # 向上一级\n",
            "        current = os.path.dirname(current)\n",
            "    # 找不到就返回当前目录\n",
            "    return os.path.abspath('.')\n",
            "\n",
            "project_root = find_project_root()\n",
            "step4_path = os.path.join(project_root, 'notebooks', 'templates', 'step4_standalone.py')\n",
            "\n",
            "# 调试信息（可选，帮助诊断）\n",
            "# print(f\"项目根目录: {project_root}\")\n",
            "# print(f\"Step 4 路径: {step4_path}\")\n",
            "# print(f\"文件存在: {os.path.exists(step4_path)}\")\n",
            "\n",
            "if os.path.exists(step4_path):\n",
            "    exec(open(step4_path).read())\n",
            "else:\n",
            "    # 如果文件找不到，使用嵌入版本\n",
            "    print(\"=\" * 80)\n",
            "    print(\"📋 **复制以下所有内容给 AI**\")\n",
            "    print(\"=\" * 80)\n",
            "    print()\n",
            "    print(\"## 📊 数据结构\")\n",
            "    print()\n",
            "    print(session.get_ai_context())\n",
            "    print()\n",
            "    print(\"=\" * 80)\n",
            "    print(\"## 📚 Panel Dashboard 完整使用指南\")\n",
            "    print(\"=\" * 80)\n",
            "    print()\n",
            "    print(\"⚠️ 规则 0: 禁止硬编码任何维度！\")\n",
            "    print(\"必须使用: group_col = values.get('_aggregation_dimension')\")\n",
            "    print(\"必须跳过: if dim == '_aggregation_dimension': continue\")\n",
            "    print()\n",
            "    print(\"详细说明见: notebooks/templates/step4_standalone.py\")\n",
            "    print(\"=\" * 80)\n"
        ]
    },
    
    # Step 5: 选择维度
    "step5_md": {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 🎯 Step 5: 选择分析维度\n",
            "\n",
            "选择你想要分析的维度字段"
        ]
    },
    
    "step5_code": {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 👤 选择你要分析的维度\n",
            "# 修改下面的列表，添加或删除维度\n",
            "\n",
            "selected_dimensions = [\n",
            "    '业务年度',\n",
            "    '业务险种',\n",
            "    # '机构名称',  # 取消注释以启用\n",
            "    # '境内境外',  # 取消注释以启用\n",
            "]\n",
            "\n",
            "print(f\"✅ 已选择 {len(selected_dimensions)} 个维度:\")\n",
            "for dim in selected_dimensions:\n",
            "    if dim in df_df.columns:\n",
            "        n_unique = df_df[dim].n_unique()\n",
            "        print(f\"  - {dim} ({n_unique:,} 个唯一值)\")\n",
            "    else:\n",
            "        print(f\"  ⚠️  {dim} - 不存在于数据中\")\n",
            "\n",
            "print(\"\\n💡 下一步: 创建 Panel 仪表盘\")\n"
        ]
    },
    
    # Step 6: 创建仪表盘
    "step6_md": {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 📊 Step 6: 创建 Panel 仪表盘\n",
            "\n",
            "自动创建仪表盘控件，然后让 AI 生成分析逻辑"
        ]
    },
    
    "step6_code": {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 创建 Panel 仪表盘（自动生成控件）\n",
            "dashboard = PanelDashboardBuilder.from_data(\n",
            "    df_df,\n",
            "    dimensions=selected_dimensions,\n",
            "    title=\"📊 数据分析仪表盘\"\n",
            ")\n",
            "\n",
            "print(\"\\n💡 下一步: 让 AI 生成分析逻辑\")\n",
            "print(\"\\n📝 给 AI 的提示:\")\n",
            "print(\"=\"  * 80)\n",
            "print(\"请使用 Panel Dashboard 生成分析代码。\")\n",
            "print(f\"已选择维度: {selected_dimensions}\")\n",
            "print(\"需求: [描述你的分析需求，例如: 各险种保费排名 Top 10]\")\n",
            "print(\"=\"  * 80)\n"
        ]
    },
    
    # Step 7: AI 生成代码区域
    "step7_md": {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 🤖 Step 7: AI 生成分析逻辑\n",
            "\n",
            "**在这里粘贴 AI 生成的代码**\n",
            "\n",
            "AI 应该生成：\n",
            "1. `@pn.depends` 装饰的更新函数\n",
            "2. 数据过滤和聚合逻辑\n",
            "3. Plotly 图表\n",
            "4. `dashboard.show()` 和 `dashboard.save()`\n"
        ]
    },
    
    "step7_code": {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 👇 AI 生成的代码粘贴在这里\n",
            "\n",
            "# 示例模板（由 AI 替换）：\n",
            "# @pn.depends(*dashboard.widgets.values())\n",
            "# def update_dashboard(*args):\n",
            "#     values = {name: widget.value for name, widget in dashboard.widgets.items()}\n",
            "#     # ... 分析逻辑\n",
            "#     return fig\n",
            "# \n",
            "# dashboard.set_update_function(update_dashboard)\n",
            "# dashboard.show()\n",
            "# dashboard.save(\"analysis.html\")\n",
            "\n",
            "print(\"⚠️ 请粘贴 AI 生成的代码\")\n"
        ]
    },
    
    # Step 8: 导出提示
    "step8_md": {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 📤 Step 8: 导出和分享\n",
            "\n",
            "如果 AI 代码中没有包含 `dashboard.save()`，手动导出："
        ]
    },
    
    "step8_code": {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 导出为静态 HTML\n",
            "dashboard.save(\"我的分析.html\", embed=True)\n",
            "\n",
            "print(\"✅ 已导出到: 我的分析.html\")\n",
            "print(\"💡 特性:\")\n",
            "print(\"  - 所有控件可交互\")\n",
            "print(\"  - Plotly 图表可交互\")\n",
            "print(\"  - 单个文件，可离线使用\")\n",
            "print(\"  - 可邮件分享\")\n",
            "print(\"\\n🎉 分析完成！\")\n"
        ]
    },
}

# 添加所有 cells 到 notebook
cell_order = [
    "title",
    "step1_md", "step1_code",
    "step2_md", "step2_code",
    "step3_md", "step3_code",
    "step4_md", "step4_code",  # ← 新增的完整 AI Prompt
    "step5_md", "step5_code",
    "step6_md", "step6_code",
    "step7_md", "step7_code",
    "step8_md", "step8_code",
]

for cell_name in cell_order:
    notebook["cells"].append(cells[cell_name])

# 保存 Notebook
output_path = "notebooks/templates/quick_start.ipynb"

print(f"📝 生成新的 Quick Start Notebook...")
print(f"📁 输出路径: {output_path}")

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("✅ 完成！")
print(f"\n📊 Notebook 结构:")
print(f"  - 标题: Panel Dashboard Quick Start")
print(f"  - Cells: {len(notebook['cells'])}")
print(f"  - 步骤: 8 步")
print(f"\n💡 特性:")
print(f"  ✅ 使用 Panel（可导出 HTML）")
print(f"  ✅ 包含 CSS 宽度修复")
print(f"  ✅ Step 4 自动生成完整 AI Prompt")
print(f"  ✅ AI 友好的结构")
print(f"  ✅ 完整的工作流")
print(f"\n🚀 在 Jupyter Lab 中打开: {output_path}")
