# 使用计算列作为分析维度 - 完整示例

import polars as pl
from src.session import DataSession
from src.dashboard import PanelDashboardBuilder

session = DataSession()

# ========================================
# 方法 1: 使用 add_computed_columns（最优雅）
# ========================================

# 1. 加载数据
session.load('insurance_data.parquet', alias='insurance')

# 2. 添加计算列
session.add_computed_columns(
    'df_insurance',
    {
        # 保费区间
        '保费区间': pl.when(pl.col('总保费') >= 1_000_000)
                      .then(pl.lit('超大额'))
                      .when(pl.col('总保费') >= 100_000)
                      .then(pl.lit('大额'))
                      .when(pl.col('总保费') >= 10_000)
                      .then(pl.lit('中等'))
                      .otherwise(pl.lit('小额')),
        
        # 时间维度
        '年份': pl.col('保险起期').str.slice(0, 4),
        '月份': pl.col('保险起期').str.slice(5, 2),
        
        # 赔付率
        '赔付率': ((pl.col('总已决赔款') + pl.col('总未决赔款')) / pl.col('总保费') * 100)
                  .fill_nan(0)
                  .round(2),
        
        # 业务规模（自留比例）
        '自留比例': (pl.col('自留保费') / pl.col('总保费') * 100)
                    .fill_nan(0)
                    .round(2)
    }
)

# 3. 可以继续添加基于前面计算列的新列
session.add_computed_columns(
    'df_insurance',
    {
        # 基于赔付率的风险等级
        '风险等级': pl.when(pl.col('赔付率') >= 80)
                      .then(pl.lit('高风险'))
                      .when(pl.col('赔付率') >= 50)
                      .then(pl.lit('中风险'))
                      .otherwise(pl.lit('低风险')),
        
        # 季度
        '季度': (pl.col('月份').cast(pl.Int32) - 1) // 3 + 1,
    }
)

# 4. 创建仪表盘，使用计算列作为维度
dashboard = PanelDashboardBuilder.from_data(
    df_insurance,
    dimensions=[
        '年份',        # 计算列
        '季度',        # 计算列
        '保费区间',    # 计算列
        '风险等级',    # 计算列
        '业务险种'     # 原始列
    ],
    title="📊 多维度保险分析"
)

# ========================================
# 方法 2: 直接在 Polars 中操作（传统方式）
# ========================================

# 加载并直接添加列
df = pl.read_parquet('insurance_data.parquet')

df_enriched = df.with_columns([
    # 多个计算列
    pl.when(pl.col('总保费') >= 100_000)
      .then(pl.lit('大客户'))
      .otherwise(pl.lit('小客户'))
      .alias('客户分类'),
    
    pl.col('保险起期').str.slice(0, 4).alias('年份'),
    
    ((pl.col('总已决赔款') + pl.col('总未决赔款')) / pl.col('总保费') * 100)
      .alias('赔付率')
])

# 直接用于仪表盘
dashboard = PanelDashboardBuilder.from_data(
    df_enriched,
    dimensions=['年份', '客户分类', '业务险种'],
    title="分析"
)

# ========================================
# 方法 3: 创建辅助函数库（推荐用于复杂场景）
# ========================================

def create_premium_tiers(col_name='总保费'):
    """创建保费分层表达式"""
    return (
        pl.when(pl.col(col_name) >= 1_000_000)
          .then(pl.lit('超大额(>100万)'))
          .when(pl.col(col_name) >= 100_000)
          .then(pl.lit('大额(10-100万)'))
          .when(pl.col(col_name) >= 10_000)
          .then(pl.lit('中等(1-10万)'))
          .otherwise(pl.lit('小额(<1万)'))
    )

def create_loss_ratio_tiers():
    """创建赔付率分层"""
    return (
        pl.when(pl.col('赔付率') >= 100)
          .then(pl.lit('亏损(>100%)'))
          .when(pl.col('赔付率') >= 80)
          .then(pl.lit('高赔付(80-100%)'))
          .when(pl.col('赔付率') >= 50)
          .then(pl.lit('中赔付(50-80%)'))
          .otherwise(pl.lit('低赔付(<50%)'))
    )

def extract_time_dimensions(date_col='保险起期'):
    """提取时间维度"""
    return {
        '年份': pl.col(date_col).str.slice(0, 4),
        '月份': pl.col(date_col).str.slice(5, 2),
        '季度': ((pl.col(date_col).str.slice(5, 2).cast(pl.Int32) - 1) // 3 + 1)
                .cast(pl.Utf8),
        '年月': pl.col(date_col).str.slice(0, 7)  # 'YYYY-MM'
    }

# 使用辅助函数
df = pl.read_parquet('insurance_data.parquet')

df_enriched = df.with_columns([
    # 使用辅助函数
    create_premium_tiers().alias('保费区间'),
    
    # 先计算赔付率
    ((pl.col('总已决赔款') + pl.col('总未决赔款')) / pl.col('总保费') * 100)
      .fill_nan(0)
      .alias('赔付率')
]).with_columns([
    # 基于赔付率的分层
    create_loss_ratio_tiers().alias('赔付率区间')
]).with_columns(
    # 时间维度
    list(extract_time_dimensions('保险起期').values())
)

dashboard = PanelDashboardBuilder.from_data(
    df_enriched,
    dimensions=['年份', '季度', '保费区间', '赔付率区间', '业务险种'],
    title="📊 综合分析"
)

# ========================================
# 方法 4: 使用 DataSession 的链式调用
# ========================================

(session
 .load('insurance_data.parquet', alias='raw')
 .pipe(lambda s: s.add_computed_columns(
     'df_raw',
     {
         '保费区间': create_premium_tiers(),
         '年份': pl.col('保险起期').str.slice(0, 4),
         '赔付率': ((pl.col('总已决赔款') + pl.col('总未决赔款')) / 
                    pl.col('总保费') * 100).fill_nan(0)
     }
 ))
 .pipe(lambda s: s.add_computed_columns(
     'df_raw',
     {'风险等级': create_loss_ratio_tiers()}
 )))

# ========================================
# 实际案例：保险业务分析
# ========================================

# 加载数据
session.load('insurance_data_cleaned.parquet', alias='policy')

# 添加业务分析维度
session.add_computed_columns(
    'df_policy',
    {
        # 1. 保费规模分层
        '保费规模': pl.when(pl.col('总保费') >= 1_000_000)
                      .then(pl.lit('超大额'))
                      .when(pl.col('总保费') >= 100_000)
                      .then(pl.lit('大额'))
                      .otherwise(pl.lit('中小额')),
        
        # 2. 时间维度
        '年份': pl.col('保险起期').str.slice(0, 4),
        '年月': pl.col('保险起期').str.slice(0, 7),
        
        # 3. 赔付相关
        '总赔款': pl.col('总已决赔款') + pl.col('总未决赔款'),
        '自留赔款': pl.col('自留已决') + pl.col('自留未决'),
        
        # 4. 业务结构
        '分出比例': ((pl.col('总保费') - pl.col('自留保费')) / pl.col('总保费') * 100)
                    .fill_nan(0)
                    .round(2),
    }
)

# 基于第一步的计算列，添加更多维度
session.add_computed_columns(
    'df_policy',
    {
        # 赔付率
        '赔付率': (pl.col('总赔款') / pl.col('总保费') * 100)
                  .fill_nan(0)
                  .round(2),
        
        # 分出程度分类
        '分出程度': pl.when(pl.col('分出比例') >= 50)
                      .then(pl.lit('高分出'))
                      .when(pl.col('分出比例') >= 20)
                      .then(pl.lit('中分出'))
                      .otherwise(pl.lit('低分出')),
    }
)

# 最后添加风险等级
session.add_computed_columns(
    'df_policy',
    {
        '风险评级': pl.when(pl.col('赔付率') >= 100)
                      .then(pl.lit('A级-亏损'))
                      .when(pl.col('赔付率') >= 80)
                      .then(pl.lit('B级-警戒'))
                      .when(pl.col('赔付率') >= 60)
                      .then(pl.lit('C级-正常'))
                      .otherwise(pl.lit('D级-优秀'))
    }
)

# 创建分析仪表盘
dashboard = PanelDashboardBuilder.from_data(
    df_policy,
    dimensions=[
        '年份',        # 计算列
        '年月',        # 计算列
        '保费规模',    # 计算列
        '风险评级',    # 计算列
        '分出程度',    # 计算列
        '业务险种',    # 原始列
        '机构名称'     # 原始列
    ],
    title="📊 保险业务多维分析"
)

# 查看所有数据（包括计算列）
session.summary()

print("\n✅ 计算列已添加，可以开始分析！")
print(f"💡 总列数: {df_policy.width}")
print(f"💡 原始列 + 计算列: {df_policy.columns}")
