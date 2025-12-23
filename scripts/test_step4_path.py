# 测试 Step 4 路径解析

import os
import sys

print("🔍 检查 Step 4 路径配置")
print("=" * 60)
print()

# 1. 当前工作目录
cwd = os.getcwd()
print(f"当前工作目录: {cwd}")
print()

# 2. 项目根目录（模拟 notebook 中的逻辑）
project_root = os.path.abspath('.')
print(f"项目根目录: {project_root}")
print()

# 3. Step 4 文件路径
step4_path = os.path.join(project_root, 'notebooks', 'templates', 'step4_standalone.py')
print(f"Step 4 路径: {step4_path}")
print()

# 4. 检查文件是否存在
exists = os.path.exists(step4_path)
print(f"文件存在: {'✅ 是' if exists else '❌ 否'}")
print()

# 5. 如果存在，显示文件信息
if exists:
    file_size = os.path.getsize(step4_path)
    print(f"文件大小: {file_size:,} 字节 ({file_size/1024:.1f} KB)")
    
    # 读取前几行
    print()
    print("文件前 10 行:")
    print("-" * 60)
    with open(step4_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if i > 10:
                break
            print(f"{i:2d}: {line.rstrip()}")
    print("-" * 60)
else:
    print("❌ 文件不存在！")
    print()
    print("可能的原因:")
    print("1. 路径配置错误")
    print("2. 文件被移动或删除")
    print("3. 工作目录不对")

print()
print("=" * 60)
print("检查完成！")
