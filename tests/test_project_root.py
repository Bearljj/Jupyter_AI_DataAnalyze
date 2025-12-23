# 测试项目根目录自动解析

from src.session import DataSession
import os

session = DataSession()

# 显示当前目录
print(f"当前工作目录: {os.getcwd()}")
print()

# 测试 1: 从项目根目录加载（默认行为）
try:
    session.load_multiple_concat(
        ['data/processed/*.parquet'],  # 相对于项目根目录
        alias='test1'
    )
    print("✅ 测试 1 通过：从项目根目录加载成功")
except Exception as e:
    print(f"❌ 测试 1 失败: {e}")

print("\n" + "="*80 + "\n")

# 测试 2: 显式指定绝对路径
try:
    project_root = '/Users/harold/working/Jupyter_AI_DataAnalyze'
    session.load_multiple_concat(
        [f'{project_root}/data/processed/*.parquet'],
        alias='test2'
    )
    print("✅ 测试 2 通过：绝对路径加载成功")
except Exception as e:
    print(f"❌ 测试 2 失败: {e}")

print("\n" + "="*80 + "\n")

# 测试 3: 从当前目录加载（禁用项目根目录）
try:
    session.load_multiple_concat(
        ['../../data/processed/*.parquet'],  # 相对于当前目录
       alias='test3',
        from_project_root=False
    )
    print("✅ 测试 3 通过：从当前目录加载成功")
except Exception as e:
    print(f"❌ 测试 3 失败: {e}")

print("\n" + "="*80 + "\n")

# 测试 4: load_multiple_join 也支持项目根目录
try:
    session.load_multiple_join(
        files={
            'file1': 'data/processed/file1.parquet',
            'file2': 'data/processed/file2.parquet'
        },
        joins=[
            {'left': 'file1', 'right': 'file2', 'on': 'id', 'how': 'left'}
        ],
        result_alias='test4'
    )
    print("✅ 测试 4 通过：join 从项目根目录加载成功")
except Exception as e:
    print(f"❌ 测试 4 失败: {e}")

print("\n" + "="*80 + "\n")

# 查看所有加载的数据
session.summary()
