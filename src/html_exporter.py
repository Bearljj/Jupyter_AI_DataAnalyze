import os
from datetime import datetime
import plotly.io as pio
from pathlib import Path

class SimpleHTMLExporter:
    """
    简化版导出器：导出为 HTML 格式（可以用浏览器打印为 PDF）
    完全不依赖 reportlab，兼容性更好
    """
    
    @staticmethod
    def export_to_html(dashboard=None, filename=None, title="数据分析报告", author="AI Data Analyst"):
        """
        将 dashboard 导出为 HTML 报告
        
        Args:
            dashboard: PanelDashboardBuilder 实例
            filename: 输出文件名
            title: 报告标题  
            author: 报告作者
        """
        # 1. 确定文件名
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.html"
        
        if not filename.endswith('.html'):
            filename += '.html'
            
        output_dir = Path("outputs/reports")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename

        print(f"🚀 开始生成 HTML 报告: {filename}...")

        # 2. 收集内容
        filters_html = ""
        if dashboard and hasattr(dashboard, 'widgets'):
            filters_html = "<h2>📋 当前分析维度与过滤条件</h2><ul>"
            for name, widget in dashboard.widgets.items():
                val = widget.value
                label = name.replace('_aggregation_dimension', '聚合维度')
                filters_html += f"<li><strong>{label}:</strong> {val}</li>"
            filters_html += "</ul>"


        # 提取图表 - 使用多种方法尝试（与 PDF 导出器相同）
        figures = []
        
        print("🔍 正在提取图表...")
        
        if dashboard:
            # 方法 1: 直接从 current_figure 属性获取
            if hasattr(dashboard, 'current_figure') and dashboard.current_figure:
                if isinstance(dashboard.current_figure, list):
                    figures = dashboard.current_figure
                    print(f"  ✅ 从 current_figure 列表获取到 {len(figures)} 个图表")
                else:
                    figures = [dashboard.current_figure]
                    print(f"  ✅ 从 current_figure 获取到 1 个图表")
            
            # 方法 2: 从 update 函数的最后一次返回值获取
            if not figures and hasattr(dashboard, '_last_figure'):
                fig = dashboard._last_figure
                if fig:
                    figures = [fig] if not isinstance(fig, list) else fig
                    print(f"  ✅ 从 _last_figure 获取到 {len(figures)} 个图表")
            
            # 方法 3: 尝试手动调用 update 函数
            if not figures and hasattr(dashboard, 'update_function'):
                try:
                    print("  🔄 尝试调用 update_function 生成图表...")
                    fig = dashboard.update_function()
                    if fig:
                        figures = [fig] if not isinstance(fig, list) else fig
                        print(f"  ✅ 通过调用 update_function 获取到 {len(figures)} 个图表")
                except Exception as e:
                    print(f"  ⚠️ 调用 update_function 失败: {e}")
        
        if not figures:
            print("  ❌ 警告: 未能提取到任何图表")
            print("  💡 提示: 请确保在运行导出前已经显示过仪表盘（执行过 dashboard.show()）")

        # 3. 生成 HTML
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        @media print {{
            body {{ margin: 0; }}
            .page-break {{ page-break-after: always; }}
        }}
        body {{
            font-family: "Microsoft YaHei", "SimSun", Arial, sans-serif;
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .cover {{
            text-align: center;
            padding: 100px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 40px;
        }}
        .cover h1 {{
            font-size: 48px;
            margin: 0;
        }}
        .cover p {{
            font-size: 18px;
            margin-top: 20px;
            opacity: 0.9;
        }}
        .content {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        h2 {{
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        ul {{
            line-height: 2;
        }}
        .chart {{
            margin: 30px 0;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="cover">
        <h1>{title}</h1>
        <p>作者: {author} | 日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>

    <div class="content">
        {filters_html}
    </div>
"""

        # 添加图表
        print(f"\n📊 开始处理 {len(figures)} 个图表...")
        
        for i, fig in enumerate(figures):
            try:
                # 获取图表标题
                chart_title = f"图表 {i+1}"
                if hasattr(fig, 'layout') and hasattr(fig.layout, 'title') and fig.layout.title:
                    chart_title = fig.layout.title.text or chart_title
                
                chart_div = f"chart_{i}"
                chart_json = fig.to_json()
                
                print(f"  ✅ 处理图表 {i+1}/{len(figures)}: {chart_title}")
                
                html_content += f"""
    <div class="content">
        <h2>📊 {chart_title}</h2>
        <div class="chart">
            <div id="{chart_div}"></div>
            <script>
                var data = {chart_json};
                Plotly.newPlot('{chart_div}', data.data, data.layout);
            </script>
        </div>
    </div>
"""
            except Exception as e:
                print(f"  ❌ 处理图表 {i+1} 失败: {e}")
                continue

        html_content += """
</body>
</html>
"""

        # 4. 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ 报告已成功导出至: {output_path}")
        print(f"💡 提示: 打开 HTML 文件后，可以使用浏览器的 '打印' 功能保存为 PDF")
        return str(output_path)
