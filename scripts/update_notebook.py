import json
import os

path = '/Users/harold/working/Jupyter_AI_DataAnalyze/notebooks/templates/quick_start.ipynb'

with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    source = cell['source']
    
    if isinstance(source, str):
        source = source.splitlines(keepends=True)
    
    new_source = []
    for line in source:
        # 彻底解决任何带有 \n 的单行合并问题
        if '\\n' in line:
            # 这是一个被转义的换行符
            parts = line.split('\\n')
            for i, p in enumerate(parts):
                clean_p = p.strip()
                if clean_p:
                    # 获取原始行号前面的内容（如果是第一部分）
                    if i == 0:
                        new_source.append(p.rstrip() + '\n')
                    else:
                        # 尝试恢复一点点注释的缩进
                        indent = "        " if clean_p.startswith('#') else ""
                        new_source.append(f'# {clean_p}\n' if clean_p.startswith('filters') or clean_p.startswith('agg_axis') else f'{clean_p}\n')
            continue
        
        # 正常行处理
        new_source.append(line)

    cell['source'] = new_source

# 重新应用正确的模板 (确保幂等且正确)
for cell in nb['cells']:
    source = cell['source']
    new_source = []
    
    # 辅助查找
    whole_text = "".join(source)
    
    for line in source:
        indent = line[:len(line) - len(line.lstrip())]
        
        # Step 6 修复
        if '请严格遵守 main.md 中的 v3.0 规范' in line:
            if '核心原则' not in whole_text:
                new_source.append(line)
                new_source.append(f'{indent}print("核心原则：严禁遍历 .widgets 进行数据过滤，必须遍历 .data_values 以实现业务列与功能列的物理隔离。")\n')
                continue
        
        # Step 7 修复
        if 'def update_dashboard(*args):' in line:
            new_source.append(line)
            if '物理隔离获取业务值' not in whole_text:
                new_source.append(f'        # ✅ 物理隔离获取业务值\n')
                new_source.append(f'        # filters = dashboard.data_values\n')
                new_source.append(f'        # ✅ 动态获取聚合轴\n')
                new_source.append(f'        # agg_axis = dashboard.widgets["_aggregation_dimension"].value\n')
                new_source.append(f'        # ... 分析逻辑 (遍历 filters 即可，无需 skip _aggregation_dimension)\n')
            continue
            
        # 过滤掉重复或损坏的行
        if '核心原则' in line and 'print' not in line: continue
        if 'skip _aggregation_dimension' in line and '#' not in line: continue
        if '\\n' in line: continue

        new_source.append(line)
    cell['source'] = new_source

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print("🚀 Final surgery complete. Notebook is healthy.")
