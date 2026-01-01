import os
import sys
import shutil
from datetime import datetime

def create_analysis(name):
    # 路径配置
    template_path = "src/analysis/base_template.py"
    target_dir = "src/analysis"
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{timestamp}_{name}.py"
    target_path = os.path.join(target_dir, filename)
    
    if not os.path.exists(template_path):
        print(f"❌ 错误：找不到模版文件 {template_path}")
        return

    # 复制模版
    shutil.copy(template_path, target_path)
    
    # 简单替换文件内的标题
    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('title="测试分析仪表盘"', f'title="{name}分析报告"')
    
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"✅ 已成功生成分析文件：{target_path}")
    print(f"💡 现在您可以让 AI 为该文件编写具体的业务逻辑了。")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python scripts/create_analysis.py [分析名称]")
    else:
        create_analysis(sys.argv[1])
