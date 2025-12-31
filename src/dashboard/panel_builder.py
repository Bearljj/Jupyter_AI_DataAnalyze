"""
Panel-based Dashboard Builder

支持静态 HTML 导出的交互式仪表盘构建器。
"""

import panel as pn
import polars as pl
from typing import List, Dict, Any, Callable, Optional
import plotly.graph_objects as go


class PanelDashboardBuilder:
    """
    基于 Panel 的仪表盘构建器
    
    特性:
    - ✅ 支持导出静态 HTML（包含交互控件）
    - ✅ 自动从数据创建控件
    - ✅ 图表自适应占满宽度
    - ✅ 支持 Jupyter Notebook 和独立部署
    """
    
    def __init__(self, title: str = "数据分析仪表盘"):
        self.title = title
        self.widgets = {}
        self.update_function = None
        self.layout = None
        
        # 初始化 Panel 扩展
        pn.extension('plotly')
    
    @classmethod
    def from_data(
        cls,
        df: pl.DataFrame,
        dimensions: List[str],
        title: str = "数据分析仪表盘",
        default_strategy: str = "all"
    ) -> "PanelDashboardBuilder":
        """
        从数据自动创建仪表盘
        
        Args:
            df: Polars DataFrame
            dimensions: 维度字段列表
            title: 仪表盘标题
            default_strategy: 默认值策略 ("all", "latest", "first")
        
        Returns:
            配置好的 PanelDashboardBuilder 实例
        
        Examples:
            >>> dashboard = PanelDashboardBuilder.from_data(
            ...     df_df,
            ...     dimensions=['业务年度', '业务险种'],
            ...     title="保费分析仪表盘"
            ... )
            >>> 
            >>> # AI 生成分析逻辑
            >>> @pn.depends(*dashboard.widgets.values())
            >>> def update(*args):
            ...     # 分析逻辑
            ...     return fig
            >>> 
            >>> dashboard.set_update_function(update)
            >>> dashboard.show()  # Jupyter 中显示
            >>> dashboard.save("dashboard.html")  # 导出 HTML
        """
        print(f"🎨 从数据创建仪表盘: {title}")
        print(f"📊 数据维度: {df.height:,} 行 × {df.width} 列")
        print(f"🔧 配置维度字段: {', '.join(dimensions)}\n")
        
        dashboard = cls(title=title)
        
        # 为每个维度创建控件
        for dim in dimensions:
            if dim not in df.columns:
                print(f"⚠️  警告: 字段 '{dim}' 不存在于数据中，跳过")
                continue
            
            try:
                # 提取唯一值
                unique_values = df.select(pl.col(dim).unique()).to_series().sort().to_list()
                unique_values = [v for v in unique_values if v is not None]
                n_unique = len(unique_values)
                
                # 根据唯一值数量选择控件类型
                if n_unique <= 10:
                    # 少量选项：Select（单选）+ 全选
                    options_with_all = ['全选'] + unique_values
                    
                    widget = pn.widgets.Select(
                        name=f"📊 {dim}",
                        options=options_with_all,
                        value='全选'
                    )
                    print(f"  ✅ {dim}: Select ({n_unique} 个选项 + 全选, 默认: 全选)")
                
                elif n_unique <= 50:
                    # 中等选项：MultiChoice（多选）
                    options_with_all = ['全选'] + unique_values
                    
                    if default_strategy == "all":
                        default_vals = ['全选']
                    else:
                        default_vals = unique_values[:min(3, n_unique)]
                    
                    widget = pn.widgets.MultiChoice(
                        name=f"📊 {dim}",
                        options=options_with_all,
                        value=default_vals,
                        sizing_mode='stretch_width'
                    )
                    print(f"  ✅ {dim}: MultiChoice ({n_unique} 个选项 + 全选, 默认选 {len(default_vals)} 个)")
                
                else:
                    # 大量选项：MultiChoice + 提示
                    options_with_all = ['全选'] + unique_values
                    
                    if default_strategy == "all":
                        default_vals = ['全选']
                    else:
                        default_vals = unique_values[:min(5, n_unique)]
                    
                    widget = pn.widgets.MultiChoice(
                        name=f"⚠️ {dim} (选项较多)",
                        options=options_with_all,
                        value=default_vals,
                        sizing_mode='stretch_width'
                    )
                    print(f"  ⚠️  {dim}: MultiChoice ({n_unique} 个选项 + 全选) - 建议 Phase 2 使用级联")
                
                dashboard.widgets[dim] = widget
                
            except Exception as e:
                print(f"❌ 错误: 处理字段 '{dim}' 时出错: {e}")
                continue
        
        # 添加"聚合维度"选择器（从已选维度中选择）
        if len(dimensions) > 0:
            agg_widget = pn.widgets.Select(
                name="⚡️ 聚合维度（分组字段）",
                options=dimensions,
                value=dimensions[0]  # 默认选第一个
            )
            dashboard.widgets['_aggregation_dimension'] = agg_widget
            print(f"\n  ✅ 聚合维度选择器: Select ({len(dimensions)} 个维度可选, 默认: {dimensions[0]})")
        
        print(f"\n✅ 仪表盘控件创建完成 ({len(dashboard.widgets)} 个控件)")
        print(f"💡 下一步: 使用 dashboard.set_update_function(your_function)\n")
        
        # 显示等效代码
        dashboard._print_code_example(dimensions, unique_values if dimensions else [])
        
        return dashboard
    
    def _print_code_example(self, dimensions: List[str], sample_values: List):
        """显示等效的手动创建代码"""
        print("=" * 80)
        print("📄 等效代码（可复制用于自定义）:")
        print("=" * 80)
        print()
        print("```python")
        print("import panel as pn")
        print("import polars as pl")
        print()
        print(f"dashboard = PanelDashboardBuilder(title=\"{self.title}\")")
        print()
        
        for dim in dimensions[:2]:  # 只显示前2个示例
            print(f"# 示例: {dim}")
            print(f"widget = pn.widgets.Select(name='{dim}', options=[...])")
            print(f"dashboard.widgets['{dim}'] = widget")
            print()
        
        print("# 定义更新函数")
        print("@pn.depends(*dashboard.widgets.values())")
        print("def update(*args):")
        print("    # 你的分析逻辑")
        print("    return fig")
        print()
        print("dashboard.set_update_function(update)")
        print("dashboard.show()  # Jupyter 显示")
        print("dashboard.save('output.html')  # 导出 HTML")
        print("```")
        print()
        print("=" * 80)
        print()
    
    @property
    def data_controls(self) -> Dict[str, Any]:
        """
        ✅ 仅获取对应数据维度的控件
        自动排除以 '_' 开头的系统功能控件（如 _aggregation_dimension）。
        AI 开发提示：在进行数据过滤逻辑开发时，请务必遍历此属性而非 .widgets。
        """
        return {k: v for k, v in self.widgets.items() if not k.startswith('_')}

    @property
    def data_values(self) -> Dict[str, Any]:
        """
        ✅ 获取数据维度控件的当前值字典 {字段名: 选中值}
        AI 开发提示：这是最推荐的获取过滤值的方式，可直接用于多维过滤循环。
        """
        return {k: v.value for k, v in self.data_controls.items()}

    def set_update_function(self, func: Callable):
        """
        设置更新函数
        
        Args:
            func: 更新函数，应该用 @pn.depends 装饰
        
        Examples:
            >>> @pn.depends(*dashboard.widgets.values())
            >>> def update(*args):
            ...     # ✅ 推荐方式：获取数据过滤值
            ...     values = dashboard.data_values
            ...     # 业务逻辑
            ...     return fig
            >>> 
            >>> dashboard.set_update_function(update)
        """
        self.update_function = func
        return self
    
    def build_layout(self):
        """构建仪表盘布局"""
        if self.update_function is None:
            raise ValueError("请先使用 set_update_function() 设置更新函数")
        
        # 标题
        title_pane = pn.pane.Markdown(f"# {self.title}", sizing_mode='stretch_width')
        
        # 控件区域（水平排列，自动换行）
        controls = pn.FlexBox(
            *self.widgets.values(),
            sizing_mode='stretch_width'
        )
        
        # 输出区域
        output = pn.panel(self.update_function, sizing_mode='stretch_width')
        
        # 完整布局
        self.layout = pn.Column(
            title_pane,
            controls,
            output,
            sizing_mode='stretch_width'
        )
        
        return self.layout
    
    def show(self):
        """在 Jupyter Notebook 中显示仪表盘"""
        if self.layout is None:
            self.build_layout()
        return self.layout
    
    def save(self, filename: str = "dashboard.html", embed: bool = True, **kwargs):
        """
        导出为静态 HTML
        
        Args:
            filename: 输出文件名
            embed: 是否嵌入所有资源（True = 单文件）
            **kwargs: 传递给 Panel save() 的其他参数
        
        Examples:
            >>> dashboard.save("analysis.html")
            >>> dashboard.save("analysis.html", embed=True, title="分析报告")
        """
        if self.layout is None:
            self.build_layout()
        
        print(f"📤 导出仪表盘到: {filename}")
        print(f"   - 控件: {len(self.widgets)} 个")
        print(f"   - 嵌入资源: {'是' if embed else '否'}")
        
        self.layout.save(filename, embed=embed, **kwargs)
        
        print(f"✅ 导出完成！")
        print(f"💡 用浏览器打开 {filename} 查看")
        print(f"   - 所有控件可交互")
        print(f"   - Plotly 图表可交互")
        print(f"   - 可离线使用")
        
        return filename
    
    def serve(self, port: int = 5006, **kwargs):
        """
        启动本地服务器
        
        Args:
            port: 端口号
            **kwargs: 传递给 Panel serve() 的其他参数
        """
        if self.layout is None:
            self.build_layout()
        
        print(f"🚀 启动仪表盘服务...")
        print(f"🌐 访问: http://localhost:{port}")
        
        self.layout.show(port=port, **kwargs)
