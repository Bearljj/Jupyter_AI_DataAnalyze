# 测试 Step 4 输出

import os
import sys

# 模拟 notebook 环境
project_root = os.path.abspath('.')
step4_path = os.path.join(project_root, 'notebooks', 'templates', 'step4_standalone.py')

print("=" * 70)
print("🧪 测试 Step 4 执行")
print("=" * 70)
print()

print(f"1️⃣ 检查文件存在:")
print(f"   路径: {step4_path}")
print(f"   存在: {os.path.exists(step4_path)}")
print()

if os.path.exists(step4_path):
    print("2️⃣ 执行文件:")
    print("-" * 70)
    
    try:
        exec(open(step4_path).read())
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        import traceback
        print(traceback.format_exc())
    
    print("-" * 70)
    print()
    print("✅ 测试完成")
else:
    print("❌ 文件不存在")
