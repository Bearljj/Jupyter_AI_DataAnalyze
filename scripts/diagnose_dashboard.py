"""
诊断 dashboard 对象的图表状态
"""

# 检查 dashboard 对象
if 'dashboard' in globals():
    dashboard = globals()['dashboard']
    
    print("=" * 70)
    print("🔍 Dashboard 对象诊断")
    print("=" * 70)
    print()
    
    # 1. 检查对象类型
    print(f"1️⃣ 对象类型: {type(dashboard)}")
    print()
    
    # 2. 检查所有属性
    print("2️⃣ 可用属性:")
    attrs = [attr for attr in dir(dashboard) if not attr.startswith('_')]
    for attr in attrs[:20]:  # 只显示前20个
        print(f"   - {attr}")
    print()
    
    # 3. 检查 current_figure
    print("3️⃣ current_figure 属性:")
    if hasattr(dashboard, 'current_figure'):
        fig = dashboard.current_figure
        print(f"   类型: {type(fig)}")
        print(f"   值: {fig is not None}")
        if isinstance(fig, list):
            print(f"   列表长度: {len(fig)}")
        print()
    else:
        print("   ❌ 没有 current_figure 属性")
        print()
    
    # 4. 检查 _last_figure
    print("4️⃣ _last_figure 属性:")
    if hasattr(dashboard, '_last_figure'):
        fig = dashboard._last_figure
        print(f"   类型: {type(fig)}")
        print(f"   值: {fig is not None}")
        print()
    else:
        print("   ❌ 没有 _last_figure 属性")
        print()
    
    # 5. 检查 update_function
    print("5️⃣ update_function 属性:")
    if hasattr(dashboard, 'update_function'):
        print(f"   类型: {type(dashboard.update_function)}")
        print(f"   可调用: {callable(dashboard.update_function)}")
        
        # 尝试调用
        print("\n   🔄 尝试调用 update_function:")
        try:
            result = dashboard.update_function()
            print(f"   ✅ 调用成功")
            print(f"   返回类型: {type(result)}")
            print(f"   返回值非空: {result is not None}")
            
            # 检查是否是 Plotly Figure
            if result:
                import plotly.graph_objects as go
                is_plotly = isinstance(result, go.Figure)
                print(f"   是 Plotly Figure: {is_plotly}")
                
                if is_plotly:
                    print(f"\n   📊 图表信息:")
                    if hasattr(result, 'layout') and hasattr(result.layout, 'title'):
                        print(f"   标题: {result.layout.title.text}")
                    print(f"   数据轨迹数: {len(result.data)}")
        except Exception as e:
            print(f"   ❌ 调用失败: {e}")
            import traceback
            traceback.print_exc()
        print()
    else:
        print("   ❌ 没有 update_function 属性")
        print()
    
    # 6. 列出所有以 'figure' 或 'fig' 开头的属性
    print("6️⃣ 所有图表相关属性:")
    fig_attrs = [attr for attr in dir(dashboard) if 'fig' in attr.lower()]
    for attr in fig_attrs:
        print(f"   - {attr}")
    
    print()
    print("=" * 70)
    
else:
    print("❌ 没有找到 dashboard 对象")
    print("请先运行 Step 6 和 Step 7 创建并显示仪表盘")
