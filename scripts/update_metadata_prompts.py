import json
import os

path = '/Users/harold/working/Jupyter_AI_DataAnalyze/notebooks/templates/quick_start.ipynb'

with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    source = cell['source']
    
    # 修改 Step 6 的提示语打印
    if 'print("请严格遵守 main.md 中的 v3.0 规范。")' in "".join(source):
        new_source = []
        for line in source:
            if 'print("请严格遵守 main.md 中的 v3.0 规范。")' in line:
                new_source.append('    print("请严格遵守 main.md 中的 v3.0.1 规范。")\n')
                new_source.append('    print("1. 物理隔离：严禁遍历 .widgets，必须使用 .data_values 获取过滤值。")\n')
                new_source.append('    print("2. 自我叙述：必须在 update_dashboard 函数的 Docstring 中包含 [REPORT_METADATA] 块，总结分析背景与逻辑。")\n')
                continue
            if '核心原则' in line: continue # 移除旧的重复行
            new_source.append(line)
        cell['source'] = new_source

    # 修改 Step 7 的示例代码占位符
    if '# 示例占位符：' in "".join(source):
        new_source = []
        for line in source:
            if 'def update(*args):' in line:
                new_source.append(line)
                new_source.append('    """\n')
                new_source.append('    [REPORT_METADATA]\n')
                new_source.append('    ### 1. 分析背景\\n    [AI总结需求]\n')
                new_source.append('    [/REPORT_METADATA]\n')
                new_source.append('    """\n')
                continue
            new_source.append(line)
        cell['source'] = new_source

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print("✅ Quick Start Template updated with v3.0.1 Metadata instructions.")
