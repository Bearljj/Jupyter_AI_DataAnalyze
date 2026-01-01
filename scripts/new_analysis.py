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
    print(f"   2. 依次运行所有 Cell (Step 1-7)")
    print(f"   3. **重要**: 在 Step 4 获取针对 AI 的物理隔离 (v3.0) 开发指令")
    print(f"   4. 在 Step 7 粘贴并运行 AI 生成的业务逻辑")
    print(f"   5. 导出 HTML 或使用 Step 8 导出 PDF 报告")
    print(f"\n💡 提示:")
    print(f"   - 模板已升级至 v3.0 物理隔离规范")
    print(f"   - 严禁遍历 .widgets，请使用 .data_values")
    print(f"   - 每个分析独立保存，可随时创建新副本")
    
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
