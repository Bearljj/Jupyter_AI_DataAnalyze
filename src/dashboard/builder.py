"""交互式仪表盘构建器

让 AI 只需要关注业务逻辑，不需要处理组件初始化和回调
"""

import ipywidgets as widgets
from IPython.display import display, clear_output
from typing import Callable, Dict, Any, List, Optional
import polars as pl


class DashboardBuilder:
    """
    交互式仪表盘构建器
    
    设计理念：
    - 组件初始化交给框架
    - AI 只需要生成业务逻辑函数
    - 自动处理回调和更新
    
    Examples:
        >>> dashboard = DashboardBuilder("产品分析")
        >>> dashboard.add_dropdown('product', '选择产品', options=['A', 'B', 'C'])
        >>> dashboard.add_slider('threshold', '阈值', min_val=0, max_val=100)
        >>> 
        >>> def update(controls):
        >>>     product = controls['product']
        >>>     threshold = controls['threshold']
        >>>     # ... 业务逻辑 ...
        >>>     return fig
        >>>     
        >>> dashboard.set_update_function(update)
        >>> dashboard.build()
    """
    
    def __init__(self, title: str = "数据分析仪表盘"):
        self.title = title
        self.controls = {}
        self.output_area = widgets.Output(layout=widgets.Layout(width='100%'))  # 设置为100%宽度
        self.layout_items = []
        self._update_function = None
    
    @classmethod
    def from_data(
        cls,
        df: pl.DataFrame,
        dimensions: List[str],
        title: str = "数据分析仪表盘",
        default_strategy: str = "latest"  # "latest", "all", "first"
    ) -> "DashboardBuilder":
        """
        从数据自动创建仪表盘
        
        从指定的维度字段中提取唯一值，自动创建相应的控件。
        控件类型基于唯一值数量智能选择。
        
        Args:
            df: Polars DataFrame
            dimensions: 维度字段列表（字段名）
            title: 仪表盘标题
            default_strategy: 默认值策略
                - "latest": 选择最新值（对年度等有序字段）
                - "all": 全选（multiselect）
                - "first": 第一个值
        
        Returns:
            配置好的 DashboardBuilder 实例（但还没有绑定 update_function）
        
        Examples:
            >>> # AI 识别维度后，用户确认
            >>> dashboard = DashboardBuilder.from_data(
            ...     df_df,
            ...     dimensions=['业务年度', '业务险种', '机构名称']
            ... )
            >>> 
            >>> # AI 生成分析逻辑
            >>> def update(controls):
            ...     year = controls['业务年度']
            ...     # ... 业务逻辑
            ...     return fig
            >>> 
            >>> dashboard.set_update_function(update)
            >>> dashboard.build()
        
        注意:
            - 这个方法只创建控件骨架，不包含分析逻辑
            - 分析逻辑由 AI 在 update_function 中生成
            - 支持的维度字段类型：String, Date, 或有限枚举的其他类型
        """
        # 创建实例
        dashboard = cls(title=title)
        
        print(f"🎨 从数据创建仪表盘: {title}")
        print(f"📊 数据维度: {df.height:,} 行 × {df.width} 列")
        print(f"🔧 配置维度字段: {', '.join(dimensions)}\n")
        
        # 为每个维度创建控件
        for dim in dimensions:
            if dim not in df.columns:
                print(f"⚠️  警告: 字段 '{dim}' 不存在于数据中，跳过")
                continue
            
            # 提取唯一值
            try:
                unique_values = df.select(pl.col(dim).unique()).to_series().sort().to_list()
                # 过滤 None/null
                unique_values = [v for v in unique_values if v is not None]
                
                if not unique_values:
                    print(f"⚠️  警告: 字段 '{dim}' 没有有效值，跳过")
                    continue
                
                n_unique = len(unique_values)
                
                # 根据唯一值数量选择控件类型
                if n_unique <= 10:
                    # 少量选项：dropdown + 全选
                    # 在选项列表开头添加"全选"
                    options_with_all = ['全选'] + unique_values
                    
                    # 确定默认值
                    if default_strategy == "latest":
                        default_val = '全选'  # 默认全选
                    elif default_strategy == "first":
                        default_val = '全选'
                    else:
                        default_val = '全选'
                    
                    dashboard.add_dropdown(
                        name=dim,
                        label=f"选择{dim}",
                        options=options_with_all,
                        default=default_val
                    )
                    print(f"  ✅ {dim}: dropdown ({n_unique} 个选项 + 全选, 默认: {default_val})")
                
                elif n_unique <= 50:
                    # 中等选项：multiselect + 全选
                    options_with_all = ['全选'] + unique_values
                    
                    if default_strategy == "all":
                        default_vals = ['全选']  # 全选
                    else:
                        # 默认选前3个
                        default_vals = unique_values[:min(3, n_unique)]
                    
                    dashboard.add_multiselect(
                        name=dim,
                        label=f"选择{dim}",
                        options=options_with_all,
                        default=default_vals
                    )
                    print(f"  ✅ {dim}: multiselect ({n_unique} 个选项 + 全选, 默认选 {len(default_vals)} 个)")
                
                else:
                    # 大量选项：multiselect + 提示 + 全选
                    options_with_all = ['全选'] + unique_values
                    
                    if default_strategy == "all":
                        default_vals = ['全选']  # 全选
                    else:
                        # 默认选前5个
                        default_vals = unique_values[:min(5, n_unique)]
                    
                    dashboard.add_multiselect(
                        name=dim,
                        label=f"选择{dim} ⚠️ 选项较多",
                        options=options_with_all,
                        default=default_vals
                    )
                    print(f"  ⚠️  {dim}: multiselect ({n_unique} 个选项 + 全选) - 选项较多，建议未来使用级联")
                
            except Exception as e:
                print(f"❌ 错误: 处理字段 '{dim}' 时出错: {e}")
                continue
        
        print(f"\n✅ 仪表盘控件创建完成")
        print(f"💡 下一步: 使用 dashboard.set_update_function(your_function) 绑定分析逻辑\n")
        
        # 显示等效的手动创建代码（便于美化）
        print("=" * 80)
        print("📄 等效代码（可复制用于自定义美化）:")
        print("=" * 80)
        print()
        print("```python")
        print("from src.dashboard import DashboardBuilder")
        print("import polars as pl")
        print()
        print(f"# 创建仪表盘")
        print(f"dashboard = DashboardBuilder(title=\"{title}\")")
        print()
        
        # 为每个维度生成控件代码
        for dim in dimensions:
            if dim not in df.columns:
                continue
            
            try:
                unique_values = df.select(pl.col(dim).unique()).to_series().sort().to_list()
                unique_values = [v for v in unique_values if v is not None]
                n_unique = len(unique_values)
                
                if n_unique <= 10:
                    # dropdown
                    print(f"# {dim} ({n_unique} 个选项)")
                    print(f"dashboard.add_dropdown(")
                    print(f"    name='{dim}',")
                    print(f"    label='选择{dim}',")
                    print(f"    options=['全选'] + {unique_values!r},")
                    print(f"    default='全选'")
                    print(f")")
                    print()
                elif n_unique <= 50:
                    # multiselect (中等)
                    print(f"# {dim} ({n_unique} 个选项)")
                    print(f"dashboard.add_multiselect(")
                    print(f"    name='{dim}',")
                    print(f"    label='选择{dim}',")
                    print(f"    options=['全选'] + {unique_values!r},")
                    print(f"    default={unique_values[:min(3, n_unique)]!r}")
                    print(f")")
                    print()
                else:
                    # multiselect (大量)
                    print(f"# {dim} ({n_unique} 个选项) - 选项较多")
                    print(f"dashboard.add_multiselect(")
                    print(f"    name='{dim}',")
                    print(f"    label='选择{dim} ⚠️ 选项较多',")
                    print(f"    options=['全选'] + [...],  # 完整列表见数据")
                    print(f"    default={unique_values[:min(5, n_unique)]!r}")
                    print(f")")
                    print()
            except:
                continue
        
        print("# 绑定更新函数（AI 生成）")
        print("# dashboard.set_update_function(update_dashboard)")
        print()
        print("# 启动仪表盘")
        print("# dashboard.build()")
        print("```")
        print()
        print("=" * 80)
        print("💡 提示: 复制上面的代码到新 cell，可以自定义控件样式、标签等")
        print("=" * 80)
        print()
        
        return dashboard

    
    def add_dropdown(
        self,
        name: str,
        label: str,
        options: List[Any],
        default: Any = None
    ):
        """
        添加下拉选择器
        
        Args:
            name: 控件名称（用于在update函数中引用）
            label: 显示标签
            options: 选项列表
            default: 默认值
        
        Returns:
            self (支持链式调用)
        """
        dropdown = widgets.Dropdown(
            options=options,
            value=default or options[0],
            description=label,
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='300px')
        )
        
        self.controls[name] = dropdown
        self.layout_items.append(dropdown)
        
        # 绑定自动更新
        dropdown.observe(self._on_change, names='value')
        
        return self
    
    def add_date_picker(
        self,
        name: str,
        label: str,
        default_value: Any = None
    ):
        """
        添加日期选择器
        
        Args:
            name: 控件名称
            label: 显示标签
            default_value: 默认日期
        
        Returns:
            self
        """
        date_picker = widgets.DatePicker(
            description=label,
            value=default_value,
            style={'description_width': 'initial'}
        )
        
        self.controls[name] = date_picker
        self.layout_items.append(date_picker)
        date_picker.observe(self._on_change, names='value')
        
        return self
    
    def add_slider(
        self,
        name: str,
        label: str,
        min_val: float,
        max_val: float,
        step: float = 1,
        default: float = None
    ):
        """
        添加滑块
        
        Args:
            name: 控件名称
            label: 显示标签
            min_val: 最小值
            max_val: 最大值
            step: 步长
            default: 默认值
        
        Returns:
            self
        """
        slider = widgets.FloatSlider(
            value=default or min_val,
            min=min_val,
            max=max_val,
            step=step,
            description=label,
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='400px')
        )
        
        self.controls[name] = slider
        self.layout_items.append(slider)
        slider.observe(self._on_change, names='value')
        
        return self
    
    def add_multiselect(
        self,
        name: str,
        label: str,
        options: List[Any],
        default: List[Any] = None
    ):
        """
        添加多选框
        
        Args:
            name: 控件名称
            label: 显示标签
            options: 选项列表
            default: 默认选中的选项
        
        Returns:
            self
        """
        multiselect = widgets.SelectMultiple(
            options=options,
            value=default or [options[0]] if options else [],
            description=label,
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='300px', height='120px')
        )
        
        self.controls[name] = multiselect
        self.layout_items.append(multiselect)
        multiselect.observe(self._on_change, names='value')
        
        return self
    
    def add_button(
        self,
        name: str,
        label: str,
        button_style: str = 'primary'
    ):
        """
        添加按钮
        
        Args:
            name: 控件名称
            label: 按钮文字
            button_style: 样式 ('primary', 'success', 'info', 'warning', 'danger')
        
        Returns:
            self
        """
        button = widgets.Button(
            description=label,
            button_style=button_style,
            layout=widgets.Layout(width='150px')
        )
        
        self.controls[name] = button
        self.layout_items.append(button)
        button.on_click(lambda _: self._on_change(None))
        
        return self
    
    def add_text_input(
        self,
        name: str,
        label: str,
        default: str = "",
        placeholder: str = ""
    ):
        """
        添加文本输入框
        
        Args:
            name: 控件名称
            label: 显示标签
            default: 默认文本
            placeholder: 占位符文本
        
        Returns:
            self
        """
        text_input = widgets.Text(
            value=default,
            placeholder=placeholder,
            description=label,
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='300px')
        )
        
        self.controls[name] = text_input
        self.layout_items.append(text_input)
        text_input.observe(self._on_change, names='value')
        
        return self
    
    def set_update_function(self, func: Callable[[Dict[str, Any]], Any]):
        """
        设置更新函数（AI 生成的核心业务逻辑）
        
        Args:
            func: 更新函数
                  - 输入：控件值字典 {name: value}
                  - 输出：图表对象、DataFrame 或任何可显示的对象
        
        Returns:
            self
        
        Examples:
            >>> def my_update(controls):
            >>>     product = controls['product']
            >>>     df_filtered = df.filter(pl.col('product') == product)
            >>>     fig = px.bar(df_filtered, x='date', y='premium')
            >>>     return fig
            >>>     
            >>> dashboard.set_update_function(my_update)
        """
        self._update_function = func
        return self
    
    def _on_change(self, change):
        """控件值变化时的回调"""
        if self._update_function:
            with self.output_area:
                clear_output(wait=True)
                
                # 获取所有控件的当前值
                values = {}
                for name, ctrl in self.controls.items():
                    if not isinstance(ctrl, widgets.Button):
                        values[name] = ctrl.value
                
                try:
                    # 调用用户定义的更新函数
                    result = self._update_function(values)
                    
                    # 显示结果
                    if result is not None:
                        display(result)
                
                except Exception as e:
                    print(f"❌ 错误: {e}")
                    import traceback
                    traceback.print_exc()
    
    def build(self):
        """构建并显示仪表盘"""
        # 标题
        title_widget = widgets.HTML(
            value=f"<h2 style='margin-bottom: 20px;'>{self.title}</h2>",
            layout=widgets.Layout(margin='0 0 20px 0')
        )
        
        # 控件区域
        controls_box = widgets.VBox(
            self.layout_items,
            layout=widgets.Layout(
                padding='20px',
                border='1px solid #ddd',
                margin='0 0 20px 0',
                border_radius='5px'
            )
        )
        
        # 输出区域（100%宽度）
        output_box = widgets.VBox(
            [self.output_area],
            layout=widgets.Layout(
                width='100%',  # 占满宽度
                padding='20px',
                border='1px solid #ddd',
                border_radius='5px'
            )
        )
        
        # 完整布局（100%宽度）
        dashboard = widgets.VBox([
            title_widget,
            controls_box,
            output_box
        ], layout=widgets.Layout(width='100%'))  # 容器也设置为100%
        
        # 显示
        display(dashboard)
        
        # 触发初始更新
        self._on_change(None)
        
        return self
    
    def get_values(self) -> Dict[str, Any]:
        """
        获取当前所有控件的值
        
        Returns:
            控件值字典
        """
        return {
            name: ctrl.value
            for name, ctrl in self.controls.items()
            if not isinstance(ctrl, widgets.Button)
        }
