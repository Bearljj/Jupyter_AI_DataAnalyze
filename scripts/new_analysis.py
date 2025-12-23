#!/usr/bin/env python3
"""
从模板创建新的分析 Notebook
"""
import shutil
import os
from datetime import datetime
import sys

def create_from_template(analysis_name=None):
    """从模板创建新的分析 notebook"""
    
    # 模板路径
    template_path = "notebooks/templates/quick_start.ipynb"
    
    # 生成文件名
    if analysis_name is None:
        # 使用时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_name = f"analysis_{timestamp}"
    
    # 清理文件名（移除非法字符）
    analysis_name = "".join(c for c in analysis_name if c.isalnum() or c in ('_', '-'))
    
    # 输出路径
    output_dir = "notebooks/02_analysis"
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/{analysis_name}.ipynb"
    
    # 检查是否已存在
    if os.path.exists(output_path):
        response = input(f"⚠️  文件已存在: {output_path}\n是否覆盖？(y/n): ")
        if response.lower() != 'y':
            print("❌ 取消创建")
            return None
    
    # 复制模板
    print(f"📋 从模板创建新分析...")
    print(f"📂 模板: {template_path}")
    print(f"📁 输出: {output_path}")
    
    shutil.copy2(template_path, output_path)
    
    print(f"\n✅ 创建成功！")
    print(f"\n📊 新分析文件:")
    print(f"   {output_path}")
    print(f"\n🚀 下一步:")
    print(f"   1. 在 Jupyter Lab 中打开: {output_path}")
    print(f"   2. 按步骤运行 (Step 1-7)")
    print(f"   3. 让 AI 生成分析代码（Step 6）")
    print(f"   4. 导出 HTML (Step 7)")
    print(f"\n💡 提示:")
    print(f"   - 模板保持干净，可反复使用")
    print(f"   - 每个分析独立保存")
    print(f"   - 可随时创建新分析")
    
    return output_path


if __name__ == "__main__":
    # 获取分析名称
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        print("🎯 创建新的数据分析")
        print()
        name = input("📝 输入分析名称（回车使用时间戳）: ").strip()
        if not name:
            name = None
    
    # 创建
    create_from_template(name)
