# 多文件加载功能

## ✨ 新增功能

DataSession 现在支持三种多文件加载场景：

### 1️⃣ 同构文件合并（Concat）
合并结构相同的多个文件

```python
session.load_multiple_concat(
    ['data/2022.parquet', 'data/2023.parquet'],
    alias='all_years'
)
```

### 2️⃣ 异构文件关联（Join）
关联不同表通过外键

```python
session.load_multiple_join(
    files={'policy': 'policy.parquet', 'customer': 'customer.parquet'},
    joins=[{'left': 'policy', 'right': 'customer', 'on': '客户ID', 'how': 'left'}],
    result_alias='enriched'
)
```

### 3️⃣ 独立文件批量加载
批量加载多个不相关的数据集

```python
session.load_multiple_independent({
    'sales': 'sales.parquet',
    'hr': 'hr.parquet'
})
```

---

## 📚 文档

- **详细指南**: [docs/MULTIPLE_FILES_GUIDE.md](../docs/MULTIPLE_FILES_GUIDE.md)
- **示例 Notebook**: [notebooks/examples/multiple_files_examples.ipynb](../notebooks/examples/multiple_files_examples.ipynb)
- **AI Context**: [docs/ai_context/main.md](../docs/ai_context/main.md)

---

## 🚀 快速开始

1. 查看示例：
```bash
jupyter lab notebooks/examples/multiple_files_examples.ipynb
```

2. 阅读文档：
```bash
cat docs/MULTIPLE_FILES_GUIDE.md
```

3. 在你的 notebook 中使用：
```python
from src.session import DataSession
session = DataSession()

# 选择合适的方法加载
session.load_multiple_concat([...], alias='data')
# 或
session.load_multiple_join(files={...}, joins=[...], result_alias='data')
# 或
session.load_multiple_independent({...})
```

---

**版本**: v1.0  
**更新时间**: 2025-12-22
