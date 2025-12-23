#!/usr/bin/env python3
"""
重新设计 quick_start.ipynb - 整合维度分析到 Step 2
"""
import json
import sys

NOTEBOOK_PATH = '/Users/harold/working/Jupyter_AI_DataAnalyze/notebooks/templates/quick_start.ipynb'

# 创建新的 Notebook 结构
def create_new_notebook():
    cells = []
    
    # ===== Cell 0: 标题 =====
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# 🚀 Jupyter AI DataAnalyze - 快速开始\n",
            "\n",
            "欢迎使用 AI-Assisted 数据分析框架！\n",
            "\n",
            "本 Notebook 将带你快速了解框架的核心功能。\n"
        ]
    })
    
    # ===== Cell 1: Step 1 说明 =====
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 📦 Step 1: 初始化环境\n",
            "\n",
            "导入核心模块并启动 Markdown 显示\n"
        ]
    })
    
    # ===== Cell 2: 初始化代码 =====
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# 导入核心模块\n",
            "from src.session import DataSession\n",
            "from src.dashboard import DashboardBuilder\n",
            "from src.utils import enable_polars_markdown_display, print_markdown_table\n",
            "import polars as pl\n",
            "import plotly.express as px\n",
            "\n",
            "# 启用 Polars Markdown 显示\n",
            "enable_polars_markdown_display()\n",
            "\n",
            "print(\"✅ 环境初始化完成！\")\n",
            "print(\"💡 所有 DataFrame 将以 Markdown 表格格式显示\")\n"
        ]
    })
    
    # ===== Cell 3: Step 2 说明（整合维度分析）=====
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 📊 Step 2: 加载数据 & 分析维度\n",
            "\n",
            "创建数据会话，加载数据，并自动分析可用的维度字段\n"
        ]
    })
    
    # ===== Cell 4: 加载数据 + 维度分析 =====
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# 创建数据会话\n",
            "session = DataSession()\n",
            "\n",
            "# 加载数据（请根据实际数据修改）\n",
            "session.load(\"alldata\", alias=\"df\")\n",
            "\n",
            "# 查看会话摘要\n",
            "session.summary()\n",
            "\n",
            "print(\"\\n\" + \"=\"*80)\n",
            "print(\"🔍 分析维度字段...\")\n",
            "print(\"=\"*80 + \"\\n\")\n",
            "\n",
            "# 分析维度字段\n",
            "dimensions_info = []\n",
            "\n",
            "for col in df_df.columns:\n",
            "    dtype = str(df_df[col].dtype)\n",
            "    \n",
            "    # 字符串/日期类型 = 潜在维度\n",
            "    if dtype == 'String' or dtype.startswith('Date'):\n",
            "        n_unique = df_df[col].n_unique()\n",
            "        \n",
            "        # 确定控件类型\n",
            "        if n_unique <= 10:\n",
            "            control = \"dropdown\"\n",
            "            note = \"\"\n",
            "        elif n_unique <= 50:\n",
            "            control = \"multiselect\"\n",
            "            note = \"\"\n",
            "        elif n_unique <= 500:\n",
            "            control = \"multiselect\"\n",
            "            note = \"⚠️ 选项较多\"\n",
            "        else:\n",
            "            control = \"multiselect\"\n",
            "            note = \"⚠️ 建议 Phase 2 使用级联\"\n",
            "        \n",
            "        dimensions_info.append({\n",
            "            'field': col,\n",
            "            'unique_values': n_unique,\n",
            "            'control': control,\n",
            "            'note': note\n",
            "        })\n",
            "\n",
            "# 显示所有维度\n",
            "print(f\"📋 发现 {len(dimensions_info)} 个维度字段：\\n\")\n",
            "for i, info in enumerate(dimensions_info, 1):\n",
            "    print(f\"{i:2d}. {info['field']:<30} ({info['unique_values']:>5,} 个值) → {info['control']:<12} {info['note']}\")\n",
            "\n",
            "# 存储维度列表\n",
            "available_dimensions = [info['field'] for info in dimensions_info]\n",
            "\n",
            "print(f\"\\n✅ 数据加载完成，共 {len(available_dimensions)} 个可用维度\")\n",
            "print(\"💡 下一步：选择维度创建仪表盘\\n\")\n"
        ]
    })
    
    # ===== Cell 5: Step 3 说明 =====
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 🤖 Step 3: 生成 AI Context\n",
            "\n",
            "生成 AI-Friendly 的数据概览，复制给 AI 使用\n"
        ]
    })
    
    # ===== Cell 6: AI Context =====
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "source": [
            "print(\"🤖 复制以下内容给 AI：\")\n",
            "print(\"=\"*80)\n",
            "\n",
            "print(\"【框架】\")\n",
            "print(\"这是 Jupyter AI DataAnalyze 框架\")\n",
            "print(\"完整工具文档见项目中的 docs/ai_context/main.md\")\n",
            "print()\n",
            "\n",
            "print(\"【当前数据】\")\n",
            "print(session.get_ai_context())\n",
            "\n",
            "print(\"=\"*80)\n",
            "print()\n",
            "print(\"💡 提示：把上面的内容复制给 AI，它就能理解你的数据结构了！\")\n"
        ]
    })
    
    # ===== Cell 7: Step 4 说明（选择维度）=====
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 👤 Step 4: 选择要使用的维度\n",
            "\n",
            "从 Step 2 识别的维度中选择，取消注释即可启用\n"
        ]
    })
    
    # ===== Cell 8: 选择维度（动态生成代码）=====
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# 👤 修改下面的列表，取消注释想要使用的维度\n",
            "# 前2个已默认启用，其余已注释\n",
            "\n",
            "# 🔧 方式1：直接使用默认值（前2个）\n",
            "selected_dimensions = available_dimensions[:2]\n",
            "\n",
            "# 🔧 方式2：手动指定（复制下面生成的代码到新 cell）\n",
            "print(\"\\n💡 可用维度列表（复制到新 cell 自定义）:\\n\")\n",
            "print(\"selected_dimensions = [\")\n",
            "for i, dim in enumerate(available_dimensions):\n",
            "    info = next(d for d in dimensions_info if d['field'] == dim)\n",
            "    comment = f\"  # {info['unique_values']:,} 个值, {info['control']}\"\n",
            "    if info['note']:\n",
            "        comment += f\" {info['note']}\"\n",
            "    \n",
            "    if i < 2:  # 前2个默认启用\n",
            "        print(f\"    '{dim}',{comment}\")\n",
            "    else:  # 其余注释\n",
            "        print(f\"    # '{dim}',{comment}\")\n",
            "print(\"]\")\n",
            "print()\n",
            "\n",
            "# 验证选择\n",
            "print(f\"✅ 当前已选择 {len(selected_dimensions)} 个维度：\")\n",
            "for dim in selected_dimensions:\n",
            "    info = next(d for d in dimensions_info if d['field'] == dim)\n",
            "    print(f\"  - {dim} ({info['unique_values']:,} 个值, {info['control']})\")\n",
            "\n",
            "print(\"\\n💡 下一步：创建仪表盘\")\n"
        ]
    })
    
    # ===== Cell 9: Step 5 说明 =====
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 🎨 Step 5: 自动创建仪表盘\n",
            "\n",
            "使用 `from_data()` 自动创建仪表盘，无需手写控件代码\n"
        ]
    })
    
    # ===== Cell 10: 创建仪表盘 =====
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# 使用 from_data() 自动创建仪表盘\n",
            "dashboard = DashboardBuilder.from_data(\n",
            "    df_df,\n",
            "    dimensions=selected_dimensions,\n",
            "    title=\"保费分析仪表盘\"\n",
            ")\n",
            "\n",
            "print(\"\\n✅ 仪表盘控件创建完成！\")\n",
            "print(\"💡 下一步：定义分析逻辑\")\n"
        ]
    })
    
    # ===== Cell 11: 定义分析逻辑 =====
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# 定义分析逻辑（AI 生成）\n",
            "\n",
            "def update_dashboard(controls):\n",
            "    \"\"\"\n",
            "    仪表盘更新函数\n",
            "    \n",
            "    Args:\n",
            "        controls: 控件值字典，key 是维度字段名\n",
            "    \"\"\"\n",
            "    # 获取第一个维度的值（根据实际情况调整）\n",
            "    dim1 = selected_dimensions[0]\n",
            "    dim1_value = controls[dim1]\n",
            "    \n",
            "    # 如果有第二个维度\n",
            "    if len(selected_dimensions) > 1:\n",
            "        dim2 = selected_dimensions[1]\n",
            "        dim2_values = controls[dim2]  # multiselect 返回列表\n",
            "        \n",
            "        # 过滤数据\n",
            "        filtered = df_df.filter(\n",
            "            (pl.col(dim1) == dim1_value) &\n",
            "            (pl.col(dim2).is_in(dim2_values))\n",
            "        )\n",
            "        \n",
            "        # 聚合分析\n",
            "        result = filtered.group_by(dim2).agg([\n",
            "            pl.col('总保费').sum().alias('保费'),\n",
            "            pl.col('总保额').sum().alias('保额'),\n",
            "            pl.len().alias('保单数')\n",
            "        ]).sort('保费', descending=True)\n",
            "        \n",
            "        # Markdown 输出\n",
            "        print(f\"## {dim1}: {dim1_value}\\n\")\n",
            "        print(f\"### 筛选条件\\n\")\n",
            "        print(f\"- {dim1}: {dim1_value}\")\n",
            "        print(f\"- {dim2}: {len(dim2_values)} 个选项\")\n",
            "        print(f\"- 数据量: {filtered.height:,} 行\\n\")\n",
            "        \n",
            "        print(f\"### Top {min(10, result.height)} {dim2}\\n\")\n",
            "        print_markdown_table(result.head(10))\n",
            "        \n",
            "        # 可视化\n",
            "        fig = px.bar(\n",
            "            result.head(10).to_pandas(),\n",
            "            x=dim2,\n",
            "            y='保费',\n",
            "            title=f'{dim1_value} - Top 10 {dim2}',\n",
            "            text='保费'\n",
            "        )\n",
            "    else:\n",
            "        # 只有一个维度\n",
            "        filtered = df_df.filter(pl.col(dim1) == dim1_value)\n",
            "        \n",
            "        result = filtered.select([\n",
            "            pl.col('总保费').sum().alias('总保费'),\n",
            "            pl.col('总保额').sum().alias('总保额'),\n",
            "            pl.len().alias('保单数')\n",
            "        ])\n",
            "        \n",
            "        print(f\"## {dim1}: {dim1_value}\\n\")\n",
            "        print_markdown_table(result)\n",
            "        \n",
            "        fig = px.bar(x=[dim1_value], y=[result['总保费'][0]], title=\"保费\")\n",
            "    \n",
            "    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')\n",
            "    fig.update_layout(height=500)\n",
            "    \n",
            "    return fig\n",
            "\n",
            "# 绑定分析逻辑\n",
            "dashboard.set_update_function(update_dashboard)\n",
            "\n",
            "print(\"✅ 分析逻辑已绑定\")\n",
            "print(\"💡 运行下一个 cell 启动仪表盘\")\n"
        ]
    })
    
    # ===== Cell 12: 启动仪表盘 =====
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# 启动仪表盘\n",
            "dashboard.build()\n",
            "\n",
            "print(\"\\n🎉 仪表盘已启动！使用上方的控件进行交互分析\")\n"
        ]
    })
    
    # ===== Cell 13: 下一步 =====
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 🎓 下一步\n",
            "\n",
            "恭喜！你已经了解了框架的基本使用。\n",
            "\n",
            "**推荐阅读：**\n",
            "- [AI Context 完整文档](../../docs/ai_context/main.md)\n",
            "- [用户指南](../../docs/guides/user_guide.md)\n",
            "- [更多示例](../examples/)\n",
            "\n",
            "**下一步实践：**\n",
            "1. 使用你自己的数据\n",
            "2. 尝试不同的维度组合\n",
            "3. 让 AI 帮你生成更复杂的分析逻辑\n",
            "\n",
            "**享受 AI 辅助的数据分析！** 🚀\n"
        ]
    })
    
    return {
        "cells": cells,
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

def main():
    print("🔄 重新生成 quick_start.ipynb...")
    
    # 创建新的 notebook
    nb = create_new_notebook()
    
    # 保存
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    
    print(f"\n✅ quick_start.ipynb 已重新生成！")
    print(f"📊 总 cells: {len(nb['cells'])}")
    print(f"\n📋 结构：")
    print(f"  Step 1: 初始化环境")
    print(f"  Step 2: 加载数据 & 分析维度（🔗 整合）")
    print(f"  Step 3: 生成 AI Context")
    print(f"  Step 4: 选择维度（动态生成代码）")
    print(f"  Step 5: 创建仪表盘 + 分析逻辑 + 启动")
    print(f"\n🔄 请在 Jupyter 中重新加载 Notebook")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
