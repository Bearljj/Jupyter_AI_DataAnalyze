#!/usr/bin/env python3
"""
批量替换 pl.count() 为 pl.len()
"""
import os
import re

# 要处理的文件列表
files_to_update = [
    '/Users/harold/working/Jupyter_AI_DataAnalyze/notebooks/templates/real_data_dashboard_cell.py',
    '/Users/harold/working/Jupyter_AI_DataAnalyze/notebooks/examples/auto_dashboard_example.py',
    '/Users/harold/working/Jupyter_AI_DataAnalyze/notebooks/analysis_premium_loss_ratio_5years.py',
    '/Users/harold/working/Jupyter_AI_DataAnalyze/scripts/regenerate_quick_start.py',
    '/Users/harold/working/Jupyter_AI_DataAnalyze/scripts/fix_quick_start_dashboard.py',
    '/Users/harold/working/Jupyter_AI_DataAnalyze/scripts/update_quick_start.py',
    '/Users/harold/working/Jupyter_AI_DataAnalyze/docs/WORKFLOW_CLARIFICATION.md',
    '/Users/harold/working/Jupyter_AI_DataAnalyze/docs/ai_context/CODE_TEMPLATE.md',
    '/Users/harold/working/Jupyter_AI_DataAnalyze/docs/ai_context/main.md',
    '/Users/harold/working/Jupyter_AI_DataAnalyze/docs/guides/fix_dashboard_sample_data.md',
]

def replace_count_with_len(file_path):
    """替换文件中的 pl.count() 为 pl.len()"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 计算替换次数
        count_before = content.count('pl.count()')
        
        # 替换
        new_content = content.replace('pl.count()', 'pl.len()')
        
        # 保存
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        if count_before > 0:
            print(f"✅ {file_path}")
            print(f"   替换了 {count_before} 处 pl.count() → pl.len()")
        
        return count_before
    except Exception as e:
        print(f"❌ {file_path}: {e}")
        return 0

def main():
    print("🔄 批量替换 pl.count() → pl.len()")
    print("=" * 80)
    
    total_replaced = 0
    files_updated = 0
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            count = replace_count_with_len(file_path)
            if count > 0:
                total_replaced += count
                files_updated += 1
        else:
            print(f"⚠️  文件不存在: {file_path}")
    
    print("\n" + "=" * 80)
    print(f"✅ 完成！")
    print(f"   更新了 {files_updated} 个文件")
    print(f"   替换了 {total_replaced} 处")
    print("\n💡 建议：重启 Jupyter Kernel 以加载更新")

if __name__ == '__main__':
    main()
