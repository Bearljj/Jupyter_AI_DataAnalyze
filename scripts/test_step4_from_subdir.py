#!/usr/bin/env python3
"""
测试从 notebooks/02_analysis/ 目录运行 Step 4
模拟真实场景
"""

import os
import sys

print("=" * 70)
print("🧪 测试从子目录运行 Step 4")
print("=" * 70)
print()

# 切换到 notebooks/02_analysis 目录（模拟在那里运行 notebook）
original_dir = os.getcwd()
test_dir = os.path.join(original_dir, 'notebooks', '02_analysis')

print(f"1️⃣ 原始目录: {original_dir}")
print(f"2️⃣ 切换到: {test_dir}")
print()

os.chdir(test_dir)

print(f"3️⃣ 当前目录: {os.getcwd()}")
print()

# 执行 Step 4 的代码（和 notebook 中一样）
print("4️⃣ 执行 Step 4 代码:")
print("-" * 70)

# 这是 Step 4 cell 的实际代码
code = """
# 自动找到项目根目录
def find_project_root():
    \"\"\"向上查找包含 src/ 和 notebooks/templates/ 的项目根目录\"\"\"
    current = os.path.abspath('.')
    while current != '/':
        # 检查是否存在项目标志
        if (os.path.exists(os.path.join(current, 'src')) and 
            os.path.exists(os.path.join(current, 'notebooks', 'templates'))):
            return current
        # 向上一级
        current = os.path.dirname(current)
    # 找不到就返回当前目录
    return os.path.abspath('.')

project_root = find_project_root()
step4_path = os.path.join(project_root, 'notebooks', 'templates', 'step4_standalone.py')

# 调试信息
print(f"项目根目录: {project_root}")
print(f"Step 4 路径: {step4_path}")
print(f"文件存在: {os.path.exists(step4_path)}")
print()

if os.path.exists(step4_path):
    print("✅ 找到文件，执行完整版本:")
    print("=" * 70)
    exec(open(step4_path).read())
else:
    print("❌ 文件不存在，使用备用版本")
"""

exec(code)

print("-" * 70)
print()

# 恢复目录
os.chdir(original_dir)
print(f"5️⃣ 恢复到: {os.getcwd()}")
print()
print("✅ 测试完成")
