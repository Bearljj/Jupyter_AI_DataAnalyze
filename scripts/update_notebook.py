import json
import os

path = '/Users/harold/working/Jupyter_AI_DataAnalyze/notebooks/templates/quick_start.ipynb'

with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    source = cell['source']
    
    # Update version strings
    new_source = []
    for line in source:
        # Markdown headline
        line = line.replace('Phase 2.0 - Panel Integration', 'Phase 3.0 - Physical Isolation (v3.0)')
        line = line.replace('**特性**: 可导出静态 HTML（控件 + 图表都可交互）', '**特性**: 物理隔离 API (`data_values`) + 自动 HTML/PDF 导出')
        
        # Step 1 version print
        line = line.replace('print(\"📚 框架版本: Phase 2.0 - Panel Integration\")', 'print(\"📚 框架版本: Phase 3.0 - Physical Isolation (v3.0)\")')
        
        # Step 4 fallback
        if "print(\"⚠️ 规则 0: 禁止硬编码任何维度！\")" in line:
             line = line.replace("print(\"⚠️ 规则 0: 禁止硬编码任何维度！\")", "print(\"⚠️ 规则 0: 禁止硬编码任何维度！\")\n    print(\"物理隔离规范 (v3.0):\")\n    print(\"- 必须使用: filters = dashboard.data_values\")\n    print(\"- 必须使用: agg_dim = dashboard.widgets['_aggregation_dimension'].value\")")
        line = line.replace("print(\"必须使用: group_col = values.get('_aggregation_dimension')\")", "")
        line = line.replace("print(\"必须跳过: if dim == '_aggregation_dimension': continue\")", "")
        
        # Step 6 prompts
        if "print(\"请使用 Panel Dashboard 生成分析代码。\")" in line:
            line = line.replace("print(\"请使用 Panel Dashboard 生成分析代码。\")", 
                                'print("请严格遵守 main.md 中的 v3.0 规范。")\n        print("核心原则：严禁遍历 .widgets 进行数据过滤，必须遍历 .data_values 以实现业务列与功能列的物理隔离。")')
        
        # Step 7 example
        if 'values = {name: widget.value for name, widget in dashboard.widgets.items()}' in line:
            line = line.replace('values = {name: widget.value for name, widget in dashboard.widgets.items()}', 
                                '# ✅ 物理隔离获取业务值\\n        # filters = dashboard.data_values\\n        # ✅ 动态获取聚合轴\\n        # agg_axis = dashboard.widgets["_aggregation_dimension"].value')
            line = line.replace('# ... 分析逻辑', '# ... 分析逻辑 (遍历 filters 即可，无需 skip _aggregation_dimension)')

        new_source.append(line)
    cell['source'] = new_source

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print("Successfully updated quick_start.ipynb")
