#!/usr/bin/env python3
"""
更新 quick_start.ipynb 以整合 Phase 1 新功能
"""
import json
import sys

NOTEBOOK_PATH = '/Users/harold/working/Jupyter_AI_DataAnalyze/notebooks/templates/quick_start.ipynb'

# 新的 cells
NEW_CELLS = {
    # Cell 1: 初始化（添加 Markdown 显示）
    "init": {
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
            "# 🆕 启用 Polars Markdown 显示\n",
            "enable_polars_markdown_display()\n",
            "\n",
            "print(\"✅ 环境初始化完成！\")\n",
            "print(\"💡 所有 DataFrame 将以 Markdown 表格格式显示\")\n"
        ]
    },
    
    # 新增：维度识别 cell
    "dimension_analysis": {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 🔍 Step 4: 分析维度字段（🆕 新功能）\n",
            "\n",
            "识别哪些字段适合作为仪表盘的维度（用于筛选/分组）\n"
        ]
    },
    
    "dimension_code": {
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# 🤖 AI 分析维度字段\n",
            "print(\"🔍 分析数据结构，识别维度字段...\\n\")\n",
            "\n",
            "dimensions_info = []\n",
            "\n",
            "for col in df_df.columns:\n",
            "    dtype = str(df_df[col].dtype)\n",
            "    \n",
            "    # 字符串类型 = 潜在维度\n",
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
            "# 🆕 显示所有维度\n",
            "print(f\"### 发现 {len(dimensions_info)} 个维度字段：\\n\")\n",
            "for i, info in enumerate(dimensions_info, 1):\n",
            "    print(f\"{i:2d}. **{info['field']}** ({info['unique_values']:,} 个值) → {info['control']} {info['note']}\")\n",
            "\n",
            "# 存储建议的维度列表（供下一步使用）\n",
            "available_dimensions = [info['field'] for info in dimensions_info]\n",
            "\n",
            "print(f\"\\n✅ 维度分析完成，共 {len(available_dimensions)} 个可用维度\")\n",
            "print(\"💡 下一步：选择要使用的维度创建仪表盘\")\n"
        ]
    },
    
    # 新增：维度选择 cell
    "dimension_select": {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 👤 选择要使用的维度\n",
            "\n",
            "从上面的列表中选择几个维度，修改下面的 `selected_dimensions` 列表\n"
        ]
    },
    
    "dimension_select_code": {
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# 👤 选择你要使用的维度字段\n",
            "# 默认已列出所有可用维度，取消注释即可启用\n",
            "\n",
            "# 🆕 动态生成维度列表（前2个默认启用，其余注释）\n",
            "print(\"生成维度选择代码...\\n\")\n",
            "print(\"selected_dimensions = [\")\n",
            "\n",
            "for i, dim in enumerate(available_dimensions):\n",
            "    # 获取维度信息\n",
            "    info = next(d for d in dimensions_info if d['field'] == dim)\n",
            "    comment = f\"  # {info['unique_values']:,} 个值, {info['control']}\"\n",
            "    if info['note']:\n",
            "        comment += f\" {info['note']}\"\n",
            "    \n",
            "    if i < 2:  # 前2个默认启用\n",
            "        print(f\"    '{dim}',{comment}\")\n",
            "    else:  # 其余注释掉\n",
            "        print(f\"    # '{dim}',{comment}\")\n",
            "\n",
            "print(\"]\")\n",
            "print(\"\\n💡 将上面的代码复制到下一个 cell 中\")\n",
            "print(\"💡 或者直接修改下面的 selected_dimensions 列表\\n\")\n",
            "\n",
            "# 默认选择（用户可以修改）\n",
            "selected_dimensions = available_dimensions[:2]  # 默认前2个\n",
            "\n",
            "# 验证选择\n",
            "print(f\"✅ 当前已选择 {len(selected_dimensions)} 个维度：\")\n",
            "for dim in selected_dimensions:\n",
            "    info = next(d for d in dimensions_info if d['field'] == dim)\n",
            "    print(f\"  - {dim} ({info['unique_values']:,} 个值, {info['control']})\")\n",
            "\n",
            "print(\"\\n💡 下一步：创建仪表盘\")\n"
        ]
    },
    
    # 更新的仪表盘 cell
    "dashboard_new": {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 🎨 Step 5: 自动创建仪表盘（🆕 新方式）\n",
            "\n",
            "使用 `from_data()` 自动创建仪表盘，无需手写控件代码\n"
        ]
    },
    
    "dashboard_create": {
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# 🎨 使用 from_data() 自动创建仪表盘\n",
            "#\n",
            "# 框架会自动：\n",
            "# 1. 从数据中提取唯一值\n",
            "# 2. 根据唯一值数量选择控件类型（dropdown/multiselect）\n",
            "# 3. 填充真实数据到控件选项\n",
            "\n",
            "dashboard = DashboardBuilder.from_data(\n",
            "    df_df,\n",
            "    dimensions=selected_dimensions,  # 使用上一步选择的维度\n",
            "    title=\"保费分析仪表盘\"\n",
            ")\n",
            "\n",
            "print(\"\\n✅ 仪表盘控件创建完成！\")\n",
            "print(\"💡 下一步：定义分析逻辑\")\n"
        ]
    },
    
    "dashboard_logic": {
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# 📊 定义分析逻辑（AI 生成）\n",
            "\n",
            "def update_dashboard(controls):\n",
            "    \"\"\"\n",
            "    仪表盘更新函数\n",
            "    \n",
            "    Args:\n",
            "        controls: 控件值字典\n",
            "            - '业务年度': 单个年度值（dropdown）\n",
            "            - '业务险种': 险种列表（multiselect）\n",
            "    \"\"\"\n",
            "    # 获取控件值\n",
            "    year = controls['业务年度']\n",
            "    products = controls['业务险种']\n",
            "    \n",
            "    # 过滤数据\n",
            "    filtered = df_df.filter(\n",
            "        (pl.col('业务年度') == year) &\n",
            "        (pl.col('业务险种').is_in(products))\n",
            "    )\n",
            "    \n",
            "    # 聚合分析\n",
            "    result = filtered.group_by('业务险种').agg([\n",
            "        pl.col('总保费').sum().alias('保费'),\n",
            "        pl.col('总保额').sum().alias('保额'),\n",
            "        pl.len().alias('保单数')\n",
            "    ]).sort('保费', descending=True)\n",
            "    \n",
            "    # 🆕 使用 Markdown 格式输出\n",
            "    print(f\"## {year}年 险种分析报告\\n\")\n",
            "    print(f\"### 筛选条件\\n\")\n",
            "    print(f\"- 年度: {year}\")\n",
            "    print(f\"- 险种数量: {len(products)} 个\")\n",
            "    print(f\"- 数据量: {filtered.height:,} 行\\n\")\n",
            "    \n",
            "    print(f\"### Top {min(10, result.height)} 险种保费排名\\n\")\n",
            "    print_markdown_table(result.head(10))\n",
            "    \n",
            "    # 创建可视化\n",
            "    fig = px.bar(\n",
            "        result.head(10).to_pandas(),\n",
            "        x='业务险种',\n",
            "        y='保费',\n",
            "        title=f'{year}年 Top 10 险种保费',\n",
            "        text='保费'\n",
            "    )\n",
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
    },
    
    "dashboard_build": {
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# 🚀 启动仪表盘\n",
            "dashboard.build()\n",
            "\n",
            "print(\"\\n🎉 仪表盘已启动！使用上方的控件进行交互分析\")\n"
        ]
    }
}

def main():
    # 读取 notebook
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    print(f"原始 cells: {len(nb['cells'])}")
    
    # 创建新的 cells 列表
    new_cells = []
    
    # Cell 0: Title (保留)
    new_cells.append(nb['cells'][0])
    
    # Cell 1: Step 1 intro (保留)
    new_cells.append(nb['cells'][1])
    
    # Cell 2: 初始化（替换为新版本）
    new_cells.append(NEW_CELLS['init'])
    
    # Cell 3: Step 2 intro (保留)
    new_cells.append(nb['cells'][3])
    
    # Cell 4: 加载数据（保留）
    new_cells.append(nb['cells'][4])
    
    # Cell 5: Step 3 intro (保留)
    new_cells.append(nb['cells'][5])
    
    # Cell 6: AI Context（保留）
    new_cells.append(nb['cells'][6])
    
    # 新增：Step 4 - 维度分析
    new_cells.append(NEW_CELLS['dimension_analysis'])
    new_cells.append(NEW_CELLS['dimension_code'])
    
    # 新增：维度选择
    new_cells.append(NEW_CELLS['dimension_select'])
    new_cells.append(NEW_CELLS['dimension_select_code'])
    
    # 新增：Step 5 - 自动仪表盘
    new_cells.append(NEW_CELLS['dashboard_new'])
    new_cells.append(NEW_CELLS['dashboard_create'])
    new_cells.append(NEW_CELLS['dashboard_logic'])
    new_cells.append(NEW_CELLS['dashboard_build'])
    
    # 最后：下一步（保留原有的）
    new_cells.append(nb['cells'][-2])  # "下一步" markdown
    
    # 更新 notebook
    nb['cells'] = new_cells
    
    # 保存
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    
    print(f"\n✅ quick_start.ipynb 已更新！")
    print(f"新 cells: {len(new_cells)}")
    print(f"\n主要更新：")
    print(f"  1. ✅ 启用 Markdown 显示")
    print(f"  2. ✅ 新增维度识别步骤（Step 4）")
    print(f"  3. ✅ 使用 from_data() 创建仪表盘（Step 5）")
    print(f"  4. ✅ 分析逻辑使用 Markdown 输出")
    print(f"  5. ✅ 移除了旧的示例数据代码")
    print(f"\n🔄 建议在 Jupyter 中重新加载 Notebook")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
