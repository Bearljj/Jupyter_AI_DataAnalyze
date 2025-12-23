"""数据会话管理

这是框架的核心组件之一，用于：
1. 避免重复的数据加载代码
2. 将数据注入到全局命名空间，AI 可以直接使用
3. 生成 AI-Friendly 的数据概览
"""

import polars as pl
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

from src.data.loaders import load_data


class DataSession:
    """
    数据会话管理器
    
    一次加载，notebook 内全局使用
    AI 生成的代码可以直接引用加载的变量
    
    Examples:
        >>> session = DataSession()
        >>> session.load("2024_01", alias="df_jan")
        >>> # 现在可以直接使用 df_jan，无需重复加载
        >>> result = df_jan.group_by('product').agg(...)
    """
    
    def __init__(self):
        self.loaded_data: Dict[str, pl.DataFrame] = {}
        self.metadata: Dict[str, dict] = {}
    
    def load(
        self,
        dataset_id: str,
        alias: str = None,
        lazy: bool = False
    ) -> pl.DataFrame:
        """
        加载数据集到会话
        
        Args:
            dataset_id: 数据集ID或文件路径
            alias: 变量别名（如 "jan", "feb"）
            lazy: 是否惰性加载
        
        Returns:
            加载的 DataFrame
        
        Examples:
            >>> session.load("2024_01", alias="df_jan")
            >>> session.load("reinsurance/2024_01.parquet", alias="jan")
        """
        # 加载数据
        try:
            df = load_data(dataset_id, lazy=lazy)
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            raise
        
        # 生成变量名
        if alias:
            var_name = alias if alias.startswith("df_") else f"df_{alias}"
        else:
            # 从路径自动生成变量名
            var_name = f"df_{Path(dataset_id).stem}"
        
        # 存储到会话
        self.loaded_data[var_name] = df
        self.metadata[var_name] = {
            'dataset_id': dataset_id,
            'loaded_at': datetime.now(),
            'lazy': lazy,
            'rows': len(df) if not lazy else "lazy",
            'cols': len(df.columns)
        }
        
        # 注入到全局命名空间（关键！）
        try:
            import __main__
            setattr(__main__, var_name, df)
            print(f"✅ 已加载: {var_name} ({dataset_id})")
        except:
            # 如果不在 Jupyter 环境，只存储在session中
            print(f"✅ 已加载到会话: {var_name}")
        
        return df
    
    def get(self, var_name: str) -> Optional[pl.DataFrame]:
        """
        获取已加载的数据
        
        Args:
            var_name: 变量名
        
        Returns:
            DataFrame 或 None
        """
        return self.loaded_data.get(var_name)
    
    def add_computed_columns(
        self,
        var_name: str,
        computed_columns: dict,
        new_alias: str = None
    ) -> pl.DataFrame:
        """
        为已加载的数据添加计算列
        
        Args:
            var_name: 已加载数据的变量名
            computed_columns: {列名: 计算表达式} 字典
            new_alias: 新变量名（None 则原地修改）
        
        Returns:
            添加计算列后的 DataFrame
        
        Examples:
            # 添加保费区间
            session.add_computed_columns(
                'df_insurance',
                {
                    '保费区间': pl.when(pl.col('总保费') >= 100000)
                                  .then(pl.lit('大额'))
                                  .otherwise(pl.lit('小额')),
                    '年份': pl.col('保险起期').str.slice(0, 4)
                }
            )
            
            # 或创建新数据集
            session.add_computed_columns(
                'df_raw',
                {'保费区间': ...},
                new_alias='enriched'
            )
        """
        # 获取原数据
        df = self.loaded_data.get(var_name)
        if df is None:
            raise ValueError(f"数据 '{var_name}' 不存在")
        
        # 添加计算列
        expressions = list(computed_columns.values())
        df_new = df.with_columns(expressions)
        
        # 确定目标变量名
        target_var = new_alias if new_alias else var_name
        if target_var != var_name and not target_var.startswith('df_'):
            target_var = f"df_{target_var}"
        
        # 更新会话
        self.loaded_data[target_var] = df_new
        self.metadata[target_var] = {
            'dataset_id': f"computed({var_name})",
            'loaded_at': datetime.now(),
            'lazy': False,
            'rows': len(df_new),
            'cols': len(df_new.columns),
            'computed_columns': list(computed_columns.keys())
        }
        
        # 注入到全局
        try:
            import __main__
            setattr(__main__, target_var, df_new)
        except:
            pass
        
        print(f"✅ 已添加 {len(computed_columns)} 个计算列: {list(computed_columns.keys())}")
        if new_alias:
            print(f"💡 新变量: {target_var}")
        else:
            print(f"💡 已更新: {target_var}")
        
        return df_new
    
    def list_loaded(self) -> list:
        """列出所有已加载的数据集"""
        return list(self.loaded_data.keys())
    
    def summary(self) -> None:
        """显示会话摘要"""
        if not self.loaded_data:
            print("⚠️  没有加载任何数据集")
            return
        
        print("✅ 数据会话已初始化\n")
        print("已加载数据集：\n")
        
        total_memory = 0
        for i, (var_name, df) in enumerate(self.loaded_data.items(), 1):
            meta = self.metadata[var_name]
            
            # 估算内存占用
            if not meta['lazy']:
                try:
                    memory_mb = df.estimated_size() / 1024 / 1024
                    total_memory += memory_mb
                    memory_str = f"{memory_mb:.1f} MB"
                except:
                    memory_str = "unknown"
            else:
                memory_str = "lazy (未加载到内存)"
            
            rows = meta['rows']
            rows_str = f"{rows:,}" if isinstance(rows, int) else rows
            
            print(f"  {i}. {var_name} ({meta['dataset_id']})")
            print(f"     - {rows_str} 行 × {meta['cols']} 列")
            print(f"     - 内存: {memory_str}")
            print()
        
        if total_memory > 0:
            print(f"总内存占用: {total_memory:.1f} MB\n")
        
        print(f"💡 AI 提示：现在可以直接使用这些变量")
        print(f"   {', '.join(self.loaded_data.keys())}\n")
    
    def get_ai_context(self) -> str:
        """
        生成当前会话的 AI Context
        
        Returns:
            包含所有已加载数据的 AI Context（可直接复制给 AI）
        
        Examples:
            >>> session.load("2024_01", alias="jan")
            >>> print(session.get_ai_context())
            >>> # 复制输出给 AI
        """
        if not self.loaded_data:
            return "⚠️  没有加载任何数据"
        
        lines = [
            "# 📊 当前数据会话",
            "",
            "已加载的数据集：",
            ""
        ]
        
        for var_name, df in self.loaded_data.items():
            meta = self.metadata[var_name]
            
            rows = meta['rows']
            rows_str = f"{rows:,}" if isinstance(rows, int) else rows
            
            lines.append(f"## `{var_name}` ({meta['dataset_id']})")
            lines.append(f"**数据量：** {rows_str} 行 × {meta['cols']} 列")
            lines.append("")
            
            # 列信息
            lines.append("**字段：**")
            for col in df.columns:
                dtype = str(df[col].dtype)
                lines.append(f"- `{col}` ({dtype})")
            
            lines.append("")
            lines.append("**使用示例：**")
            lines.append("```python")
            lines.append(f"# 直接使用变量 {var_name}")
            lines.append(f"result = {var_name}.group_by('...').agg(...)")
            lines.append(f"filtered = {var_name}.filter(pl.col('...') > 100)")
            lines.append("```")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append("💡 **重要：** 所有这些变量都已在 Jupyter 环境中可用")
        lines.append("   你生成的代码可以直接使用它们，无需再次加载")
        
        return "\n".join(lines)
    
    def load_multiple_concat(
        self,
        file_patterns: list[str],
        alias: str,
        ignore_schema_errors: bool = False,
        from_project_root: bool = True  # 新增参数
    ) -> pl.DataFrame:
        """
        场景1: 加载多个同构文件并纵向合并
        
        适用于：结构相同的多个文件（如多年数据、分片数据）
        
        Args:
            file_patterns: 文件路径列表或 glob 模式
            alias: 合并后的别名
            ignore_schema_errors: 是否忽略schema不匹配（会填充null）
            from_project_root: 是否从项目根目录开始（默认 True）
        
        Returns:
            合并后的 DataFrame
        
        Examples:
            # 从项目根目录加载（默认）
            session.load_multiple_concat(
                ['data/processed/2022.parquet', 'data/processed/2023.parquet'],
                alias='all_years'
            )
            
            # 使用 glob 模式
            session.load_multiple_concat(
                ['data/processed/year_*.parquet'],
                alias='all_years'
            )
            
            # 从当前目录加载
            session.load_multiple_concat(
                ['./local/*.parquet'],
                alias='local_data',
                from_project_root=False
            )
        """
        import glob
        import os
        
        # 自动找到项目根目录
        def find_project_root():
            """向上查找包含 src/ 目录的项目根目录"""
            current = os.getcwd()
            while current != '/':
                if os.path.exists(os.path.join(current, 'src')) and \
                   os.path.exists(os.path.join(current, 'data')):
                    return current
                current = os.path.dirname(current)
            return os.getcwd()  # 找不到就返回当前目录
        
        def search_file_in_common_locations(filename, root_dir):
            """在常见数据目录中搜索文件"""
            # 常见的数据目录（按优先级）
            common_dirs = [
                'data/processed',
                'data/raw',
                'data',
                'data/external',
                'data/interim'
            ]
            
            for dir_path in common_dirs:
                full_path = os.path.join(root_dir, dir_path, filename)
                # 支持 glob 模式
                if '*' in filename or '?' in filename:
                    matches = glob.glob(full_path)
                    if matches:
                        return matches[0]  # 返回第一个匹配
                elif os.path.exists(full_path):
                    return full_path
            
            return None  # 找不到
        
        # 解析路径
        if from_project_root:
            root_dir = find_project_root()
            resolved_patterns = []
            
            for pattern in file_patterns:
                if os.path.isabs(pattern):
                    # 已经是绝对路径，直接使用
                    resolved_patterns.append(pattern)
                elif '/' in pattern or '\\' in pattern:
                    # 包含路径分隔符，视为相对路径
                    resolved_patterns.append(os.path.join(root_dir, pattern))
                else:
                    # 只有文件名，自动搜索
                    found = search_file_in_common_locations(pattern, root_dir)
                    if found:
                        print(f"  📍 自动找到: {pattern} → {os.path.relpath(found, root_dir)}")
                        resolved_patterns.append(found)
                    else:
                        # 找不到，默认放在 data/processed
                        default_path = os.path.join(root_dir, 'data/processed', pattern)
                        resolved_patterns.append(default_path)
                        print(f"  ⚠️  未找到 {pattern}，尝试默认路径: data/processed/{pattern}")
            
            print(f"📂 从项目根目录加载: {root_dir}")
        else:
            resolved_patterns = file_patterns
        
        # 展开 glob 模式
        files = []
        for pattern in resolved_patterns:
            if '*' in pattern or '?' in pattern:
                matched = glob.glob(pattern)
                files.extend(sorted(matched))  # 排序保证顺序
            else:
                files.append(pattern)
        
        if not files:
            raise ValueError(f"未找到任何文件: {file_patterns}\n解析后的路径: {resolved_patterns}")
        
        print(f"📂 发现 {len(files)} 个文件准备合并")
        
        # 加载所有文件
        dfs = []
        total_rows = 0
        for file in files:
            try:
                df = pl.read_parquet(file)
                dfs.append(df)
                total_rows += df.height
                print(f"  ✅ {os.path.basename(file)}: {df.height:,} 行 × {df.width} 列")
            except Exception as e:
                print(f"  ❌ {os.path.basename(file)}: {e}")
                if not ignore_schema_errors:
                    raise
        
        if not dfs:
            raise ValueError("没有成功加载任何文件")
        
        # 纵向合并
        print(f"\n🔗 合并中...")
        combined = pl.concat(
            dfs,
            how='vertical_relaxed' if ignore_schema_errors else 'vertical'
        )
        
        # 生成变量名
        var_name = alias if alias.startswith("df_") else f"df_{alias}"
        
        # 存储
        self.loaded_data[var_name] = combined
        self.metadata[var_name] = {
            'dataset_id': f"concat({len(files)} files)",
            'loaded_at': datetime.now(),
            'lazy': False,
            'rows': combined.height,
            'cols': combined.width,
            'source_files': files
        }
        
        # 注入到全局
        try:
            import __main__
            setattr(__main__, var_name, combined)
        except:
            pass
        
        print(f"\n✅ 合并完成: {var_name}")
        print(f"   总计: {combined.height:,} 行 × {combined.width} 列")
        print(f"   来源: {len(files)} 个文件")
        print(f"💡 使用变量: {var_name}")
        
        return combined
    
    def load_multiple_join(
        self,
        files: dict[str, str],
        joins: list[dict],
        result_alias: str,
        from_project_root: bool = True  # 新增参数
    ) -> pl.DataFrame:
        """
        场景2: 加载多个异构文件并根据关联关系join
        
        适用于：不同表有外键关系（如订单-客户-产品）
        
        Args:
            files: {别名: 文件路径} 字典
            joins: join配置列表，每个包含：
                - left: 左表别名
                - right: 右表别名
                - on: 连接字段（字符串或列表）
                - how: 连接方式 (left/inner/outer/cross)
                - suffix: 可选，右表重名列后缀
            result_alias: 最终结果的别名
            from_project_root: 是否从项目根目录开始（默认 True）
        
        Returns:
            join后的 DataFrame
        
        Examples:
            session.load_multiple_join(
                files={
                    'policy': 'data/processed/policy.parquet',
                    'customer': 'data/processed/customer.parquet',
                    'product': 'data/processed/product.parquet'
                },
                joins=[
                    {'left': 'policy', 'right': 'customer', 'on': '客户ID', 'how': 'left'},
                    {'left': 'policy', 'right': 'product', 'on': '产品代码', 'how': 'left'}
                ],
                result_alias='enriched'
            )
        """
        import os
        import glob
        
        # 自动找到项目根目录
        def find_project_root():
            current = os.getcwd()
            while current != '/':
                if os.path.exists(os.path.join(current, 'src')) and \
                   os.path.exists(os.path.join(current, 'data')):
                    return current
                current = os.path.dirname(current)
            return os.getcwd()
        
        def search_file_in_common_locations(filename, root_dir):
            """在常见数据目录中搜索文件"""
            common_dirs = [
                'data/processed',
                'data/raw',
                'data',
                'data/external',
                'data/interim'
            ]
            
            for dir_path in common_dirs:
                full_path = os.path.join(root_dir, dir_path, filename)
                if os.path.exists(full_path):
                    return full_path
            
            return None
        
        # 解析文件路径
        if from_project_root:
            root_dir = find_project_root()
            resolved_files = {}
            
            for alias, filepath in files.items():
                if os.path.isabs(filepath):
                    # 绝对路径
                    resolved_files[alias] = filepath
                elif '/' in filepath or '\\' in filepath:
                    # 相对路径
                    resolved_files[alias] = os.path.join(root_dir, filepath)
                else:
                    # 只有文件名，自动搜索
                    found = search_file_in_common_locations(filepath, root_dir)
                    if found:
                        print(f"  📍 自动找到 {alias}: {filepath} → {os.path.relpath(found, root_dir)}")
                        resolved_files[alias] = found
                    else:
                        # 默认 data/processed
                        default_path = os.path.join(root_dir, 'data/processed', filepath)
                        resolved_files[alias] = default_path
                        print(f"  ⚠️  未找到 {alias} ({filepath})，尝试: data/processed/{filepath}")
            
            print(f"📂 从项目根目录加载: {root_dir}")
        else:
            resolved_files = files
        
        print(f"📂 加载 {len(resolved_files)} 个文件")
        
        # 1. 加载所有文件
        loaded = {}
        for alias, filepath in resolved_files.items():
            try:
                df = pl.read_parquet(filepath)
                loaded[alias] = df
                print(f"  ✅ {alias}: {df.height:,} 行 × {df.width} 列")
            except Exception as e:
                raise ValueError(f"加载失败 {alias} ({filepath}): {e}")
        
        # 2. 验证 join 配置
        for i, jc in enumerate(joins):
            if 'left' not in jc or 'right' not in jc or 'on' not in jc:
                raise ValueError(f"Join {i+1} 配置不完整: {jc}")
        
        # 3. 执行连续join
        print(f"\n🔗 执行 {len(joins)} 个Join操作")
        result = None
        
        for i, join_config in enumerate(joins, 1):
            left_alias = join_config['left']
            right_alias = join_config['right']
            on = join_config['on']
            how = join_config.get('how', 'left')
            suffix = join_config.get('suffix', '_right')
            
            # 确定左表
            if result is None:
                if left_alias not in loaded:
                    raise ValueError(f"左表 '{left_alias}' 不存在")
                left_df = loaded[left_alias]
            else:
                # 使用上一步的结果
                left_df = result
            
            # 确定右表
            if right_alias not in loaded:
                raise ValueError(f"右表 '{right_alias}' 不存在")
            right_df = loaded[right_alias]
            
            # 执行join
            result = left_df.join(right_df, on=on, how=how, suffix=suffix)
            
            print(f"  Join {i}: {left_alias} ← {right_alias}")
            print(f"    连接字段: {on}")
            print(f"    连接方式: {how}")
            print(f"    结果: {result.height:,} 行 × {result.width} 列")
        
        # 4. 存储结果
        var_name = result_alias if result_alias.startswith("df_") else f"df_{result_alias}"
        
        self.loaded_data[var_name] = result
        self.metadata[var_name] = {
            'dataset_id': f"join({', '.join(resolved_files.keys())})",
            'loaded_at': datetime.now(),
            'lazy': False,
            'rows': result.height,
            'cols': result.width,
            'source_files': list(resolved_files.values()),
            'joins': joins
        }
        
        # 注入到全局
        try:
            import __main__
            setattr(__main__, var_name, result)
        except:
            pass
        
        print(f"\n✅ Join 完成: {var_name}")
        print(f"   {result.height:,} 行 × {result.width} 列")
        print(f"💡 使用变量: {var_name}")
        
        return result
    
    def load_multiple_independent(
        self,
        files: dict[str, str]
    ) -> dict[str, pl.DataFrame]:
        """
        场景3: 批量加载多个独立文件
        
        适用于：多个不相关的数据集（如销售、HR、财务）
        
        Args:
            files: {别名: 文件路径} 字典
        
        Returns:
            {别名: DataFrame} 字典
        
        Examples:
            session.load_multiple_independent({
                'sales': 'sales.parquet',
                'hr': 'hr.parquet',
                'finance': 'finance.parquet'
            })
        """
        print(f"📂 批量加载 {len(files)} 个独立文件")
        
        loaded = {}
        for alias, filepath in files.items():
            try:
                # 使用已有的 load 方法
                df = self.load(filepath, alias=alias)
                loaded[alias] = df
            except Exception as e:
                print(f"  ❌ {alias}: {e}")
        
        print(f"\n✅ 已加载 {len(loaded)}/{len(files)} 个数据集")
        
        return loaded
    
    def clear(self, var_name: str = None) -> None:
        """
        清除加载的数据（释放内存）
        
        Args:
            var_name: 变量名，如果为None则清除所有
        """
        if var_name:
            if var_name in self.loaded_data:
                del self.loaded_data[var_name]
                del self.metadata[var_name]
                print(f"✅ 已清除: {var_name}")
            else:
                print(f"⚠️  变量不存在: {var_name}")
        else:
            count = len(self.loaded_data)
            self.loaded_data.clear()
            self.metadata.clear()
            print(f"✅ 已清除所有数据 ({count} 个)")
