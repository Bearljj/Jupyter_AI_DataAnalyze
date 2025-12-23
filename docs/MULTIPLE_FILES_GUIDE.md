# 多文件加载指南

处理多个 Parquet 文件的完整指南。

---

## 📊 三种场景

### 场景 1: 同构文件合并（Concat）

**适用于**: 结构相同的多个文件
- 多年数据（2022.parquet + 2023.parquet + ...）
- 分片数据（part1.parquet + part2.parquet + ...）
- 分批次导出的数据

**特点**: 纵向堆叠，字段相同或兼容

---

### 场景 2: 异构文件关联（Join）

**适用于**: 不同表有外键关系
- 主表 + 维度表（保单 + 客户信息')
- 事实表 + 多个维度表（订单 + 客户 + 产品）
- 雪花模型/星型模型数据

**特点**: 横向拼接，通过关键字段关联

---

### 场景 3: 独立文件批量加载

**适用于**: 多个不相关的数据集
- 不同业务线数据（销售 + HR + 财务）
- 不同主题数据（用户 + 商品 + 订单）

**特点**: 分别加载，独立分析

---

## 🚀 快速开始

### 场景 1: 合并同构文件

```python
from src.session import DataSession

session = DataSession()

# 合并多个文件
session.load_multiple_concat(
    ['data/2022.parquet', 'data/2023.parquet', 'data/2024.parquet'],
    alias='all_years'
)

# 使用
all_years_df.filter(pl.col('业务年度') == '2023')
```

**使用 glob 模式**:

```python
# 匹配所有年份文件
session.load_multiple_concat(
    ['data/year_*.parquet'],
    alias='all_data'
)

# 匹配多个目录
session.load_multiple_concat(
    ['old_format/*.parquet', 'new_format/*.parquet'],
    alias='combined',
    ignore_schema_errors=True  # 容错模式
)
```

---

### 场景 2: 关联异构文件

```python
# 简单 join
session.load_multiple_join(
    files={
        'policy': 'data/保单.parquet',
        'customer': 'data/客户.parquet'
    },
    joins=[
        {
            'left': 'policy',
            'right': 'customer',
            'on': '客户ID',
            'how': 'left'
        }
    ],
    result_alias='enriched'
)

# 使用
enriched_df.select(['保单号', '客户名称', '总保费'])
```

**多表连续 join**:

```python
session.load_multiple_join(
    files={
        'policy': 'policy.parquet',
        'customer': 'customer.parquet',
        'product': 'product.parquet',
        'agent': 'agent.parquet'
    },
    joins=[
        # join 1: policy ← customer
        {'left': 'policy', 'right': 'customer', 'on': '客户ID', 'how': 'left'},
        
        # join 2: (policy+customer) ← product
        # left 会自动使用上一步的结果
        {'left': 'policy', 'right': 'product', 'on': '产品代码', 'how': 'left'},
        
        # join 3: (policy+customer+product) ← agent
        {'left': 'policy', 'right': 'agent', 'on': '代理人代码', 'how': 'left'}
    ],
    result_alias='full_data'
)
```

---

### 场景 3: 批量加载独立文件

```python
session.load_multiple_independent({
    'sales': 'data/销售.parquet',
    'hr': 'data/人力.parquet',
    'finance': 'data/财务.parquet'
})

# 分别使用
sales_df.head()
hr_df.filter(pl.col('部门') == 'IT')
finance_df.group_by('月份').agg(...)
```

---

## 📋 完整 API 文档

### `load_multiple_concat()`

纵向合并同构文件

**参数**:
- `file_patterns: list[str]` - 文件路径列表或 glob 模式
- `alias: str` - 合并后的别名
- `ignore_schema_errors: bool = False` - 是否忽略 schema 不匹配

**返回**: `pl.DataFrame`

**示例**:
```python
session.load_multiple_concat(
    ['data/*.parquet'],
    alias='all_data',
    ignore_schema_errors=True
)
```

---

### `load_multiple_join()`

关联异构文件

**参数**:
- `files: dict[str, str]` - {别名: 文件路径} 字典
- `joins: list[dict]` - join 配置列表
- `result_alias: str` - 最终结果别名

**join 配置**:
- `left: str` - 左表别名
- `right: str` - 右表别名
- `on: str | list[str]` - 连接字段
- `how: str` - 连接方式 (`left`/`inner`/`outer`/`cross`)
- `suffix: str` - 可选，右表重名列后缀（默认 `_right`）

**返回**: `pl.DataFrame`

**示例**:
```python
session.load_multiple_join(
    files={'orders': 'orders.parquet', 'items': 'items.parquet'},
    joins=[{
        'left': 'orders',
        'right': 'items',
        'on': ['订单号', '年份'],
        'how': 'inner',
        'suffix': '_item'
    }],
    result_alias='order_details'
)
```

---

### `load_multiple_independent()`

批量加载独立文件

**参数**:
- `files: dict[str, str]` - {别名: 文件路径} 字典

**返回**: `dict[str, pl.DataFrame]`

**示例**:
```python
session.load_multiple_independent({
    'sales': 'sales.parquet',
    'hr': 'hr.parquet'
})
```

---

## 💡 最佳实践

### 1. 合并文件时的注意事项

**确保文件顺序**:
```python
# 使用排序的 glob
import glob
files = sorted(glob.glob('data/year_*.parquet'))
session.load_multiple_concat(files, alias='ordered')
```

**Schema 不一致处理**:
```python
# 启用容错模式
session.load_multiple_concat(
    ['old/*.parquet', 'new/*.parquet'],
    alias='mixed',
    ignore_schema_errors=True  # 缺失字段填充 null
)

# 手动对齐 schema（更安全）
session.load_multiple_concat(
    ['old/*.parquet'],
    alias='old_data'
)
# 在 Polars 中手动添加缺失列
old_data_df = old_data_df.with_columns([
    pl.lit(None).alias('新字段')
])
```

---

### 2. Join 时的注意事项

**检查关联质量**:
```python
# 加载后检查
result = session.load_multiple_join(...)

# 检查 join 是否有数据丢失
print(f"保单数: {policy_df.height}")
print(f"Join 后: {result.height}")

# 检查 null 值
result.select([pl.col('*').is_null().sum()])
```

**处理重名列**:
```python
# 使用 suffix
session.load_multiple_join(
    files={'a': 'a.parquet', 'b': 'b.parquet'},
    joins=[{
        'left': 'a',
        'right': 'b',
        'on': 'id',
        'suffix': '_from_b'  # 重名列会变成 name_from_b
    }],
    result_alias='joined'
)
```

---

### 3. 性能优化

**大文件处理**:
```python
# 分批处理
for year in range(2020, 2025):
    session.load_multiple_concat(
        [f'data/{year}_*.parquet'],
        alias=f'year_{year}'
    )
    # 处理单年数据
    process(eval(f'year_{year}_df'))
```

**内存管理**:
```python
# 使用后清除
session.load_multiple_concat(['large_*.parquet'], alias='temp')
# ... 使用 temp_df ...
session.clear('temp_df')  # 释放内存
```

---

## 🎯 实际案例

### 案例 1: 多年保险数据分析

```python
# 1. 合并多年保单
session.load_multiple_concat(
    [f'data/policy_{y}.parquet' for y in range(2020, 2025)],
    alias='all_policies'
)

# 2. 关联维度表
session.load_multiple_join(
    files={
        'policy': 'df_all_policies',  # 可以使用已加载的
        'customer': 'data/customer.parquet',
        'product': 'data/product.parquet'
    },
    joins=[
        {'left': 'policy', 'right': 'customer', 'on': '客户ID', 'how': 'left'},
        {'left': 'policy', 'right': 'product', 'on': '产品代码', 'how': 'left'}
    ],
    result_alias='enriched'
)

# 3. 分析
enriched_df.group_by(['业务年度', '产品类型']).agg([
    pl.col('总保费').sum(),
    pl.len().alias('保单数')
])
```

---

### 案例 2: 电商订单分析

```python
# 订单主表 + 多个维度表
session.load_multiple_join(
    files={
        'orders': 'orders.parquet',
        'customers': 'customers.parquet',
        'products': 'products.parquet',
        'sellers': 'sellers.parquet'
    },
    joins=[
        {'left': 'orders', 'right': 'customers', 'on': 'customer_id', 'how': 'left'},
        {'left': 'orders', 'right': 'products', 'on': 'product_id', 'how': 'left'},
        {'left': 'orders', 'right': 'sellers', 'on': 'seller_id', 'how': 'left'}
    ],
    result_alias='full_orders'
)
```

---

## ⚠️ 常见问题

### Q1: Glob 模式匹配不到文件？

```python
# 检查路径
import glob
print(glob.glob('data/*.parquet'))

# 使用绝对路径
import os
data_dir = os.path.abspath('data')
session.load_multiple_concat(
    [f'{data_dir}/*.parquet'],
    alias='data'
)
```

### Q2: Schema 不匹配错误？

```python
# 两种解决方案：

# 方案 1: 启用容错
session.load_multiple_concat(
    ['*.parquet'],
    alias='data',
    ignore_schema_errors=True
)

# 方案 2: 手动对齐（更安全）
# 先检查每个文件的 schema
for f in glob.glob('*.parquet'):
    df = pl.read_parquet(f)
    print(f"{f}: {df.columns}")
```

### Q3: Join 后数据量不对？

```python
# 检查关联键是否唯一
customer_df.group_by('客户ID').len().filter(pl.col('len') > 1)

# 使用 inner join 看数据匹配情况
session.load_multiple_join(
    ...,
    joins=[{'..., 'how': 'inner'}],  # 只保留匹配的
    ...
)
```

---

## 📚 相关文档

- [DataSession API 文档](../docs/API.md)
- [Polars Join 文档](https://pola-rs.github.io/polars/py-polars/html/reference/dataframe/api/polars.DataFrame.join.html)
- [示例 Notebook](../notebooks/examples/multiple_files_examples.ipynb)

---

**需要帮助？** 查看示例 notebook 或提 issue！🚀
