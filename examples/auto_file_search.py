# 文件自动搜索使用示例

from src.session import DataSession

session = DataSession()

# ========================================
# 方式 1: 只写文件名（最简单！）✨
# ========================================
# 系统会自动在这些目录搜索：
# - data/processed/
# - data/raw/
# - data/
# - data/external/
# - data/interim/

session.load_multiple_concat(
    ['policy_2022.parquet', 'policy_2023.parquet'],
    alias='all_policies'
)
# 输出：
# 📍 自动找到: policy_2022.parquet → data/processed/policy_2022.parquet
# 📍 自动找到: policy_2023.parquet → data/processed/policy_2023.parquet

# ========================================
# 方式 2: 写相对路径
# ========================================
session.load_multiple_concat(
    ['data/processed/file1.parquet', 'data/raw/file2.parquet'],
    alias='mixed'
)

# ========================================
# 方式 3: 使用 glob 模式（只写文件名）
# ========================================
session.load_multiple_concat(
    ['policy_*.parquet'],  # 只写文件名
    alias='all_policies_pattern'
)
# 会在 data/processed/ 中查找

# ========================================
# 方式 4: join 也支持文件名搜索
# ========================================
session.load_multiple_join(
    files={
        'policy': 'policy.parquet',  # 只写文件名
        'customer': 'customer.parquet',  # 只写文件名
        'product': 'product.parquet'  # 只写文件名
    },
    joins=[
        {'left': 'policy', 'right': 'customer', 'on': '客户ID', 'how': 'left'},
        {'left': 'policy', 'right': 'product', 'on': '产品代码', 'how': 'left'}
    ],
    result_alias='enriched'
)
# 输出：
# 📍 自动找到 policy: policy.parquet → data/processed/policy.parquet
# 📍 自动找到 customer: customer.parquet → data/processed/customer.parquet
# 📍 自动找到 product: product.parquet → data/processed/product.parquet

# ========================================
# 搜索优先级
# ========================================
# 如果同名文件在多个目录：
# 1. data/processed/  ← 优先
# 2. data/raw/
# 3. data/
# 4. data/external/
# 5. data/interim/

# ========================================
# 找不到文件的处理
# ========================================
session.load_multiple_concat(
    ['non_existent.parquet'],
    alias='test'
)
# 输出：
# ⚠️  未找到 non_existent.parquet，尝试默认路径: data/processed/non_existent.parquet
# 然后会报错：FileNotFoundError（因为确实不存在）

# ========================================
# 禁用自动搜索（如果需要）
# ========================================
session.load_multiple_concat(
    ['file.parquet'],
    alias='current_dir',
    from_project_root=False  # 从当前目录查找
)
