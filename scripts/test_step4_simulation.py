#!/usr/bin/env python3
"""
测试 Step 4 的实际输出
模拟在 Jupyter notebook 中运行
"""

import os
import sys

print("=" * 70)
print("🧪 模拟运行 Step 4")
print("=" * 70)
print()

# 模拟 notebook 环境
project_root = os.path.abspath('.')
step4_path = os.path.join(project_root, 'notebooks', 'templates', 'step4_standalone.py')

print(f"1️⃣ 当前目录: {os.getcwd()}")
print(f"2️⃣ 项目根目录: {project_root}")
print(f"3️⃣ Step 4 路径: {step4_path}")
print(f"4️⃣ 文件存在: {os.path.exists(step4_path)}")
print()

if os.path.exists(step4_path):
    print("5️⃣ 执行 step4_standalone.py:")
    print("=" * 70)
    
    # 执行（和 notebook 中一样）
    exec(open(step4_path).read())
    
    print("=" * 70)
    print()
    print("✅ 执行完成")
else:
    print("❌ 文件不存在！")
    print()
    print("会使用备用版本（简化的）")
