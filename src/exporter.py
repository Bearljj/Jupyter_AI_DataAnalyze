import os
from datetime import datetime
import plotly.io as pio
import polars as pl
from pathlib import Path

class ReportExporter:
    """
    通用 PDF 报告导出器
    与具体分析逻辑解耦，只依赖于 dashboard 对象或 Plotly 图表列表
    """
    
    @staticmethod
    def export_to_pdf(dashboard=None, filename=None, title="数据分析报告", author="AI Data Analyst"):
        """
        将 dashboard 导出为 PDF 报告
        
        Args:
            dashboard: PanelDashboardBuilder 实例
            filename: 输出文件名
            title: 报告标题
            author: 报告作者
        """
        try:
            import kaleido  # 必须安装: pip install kaleido
        except ImportError:
            print("❌ 错误: 请先安装 kaleido 以便导出静态图表: pip install kaleido")
            return

        # 1. 确定文件名
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.pdf"
        
        if not filename.endswith('.pdf'):
            filename += '.pdf'
            
        output_dir = Path("outputs/reports")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename

        print(f"🚀 开始生成 PDF 报告: {filename}...")

        # 2. 收集内容
        content = []
        
        # 提取当前过滤配置 (来自 dashboard 控件)
        filters_str = ""
        if dashboard and hasattr(dashboard, 'widgets'):
            filters_str = "📋 **当前分析维度与过滤条件:**\n"
            for name, widget in dashboard.widgets.items():
                val = widget.value
                label = name.replace('_aggregation_dimension', '聚合维度')
                filters_str += f"- {label}: {val}\n"
        
        # 提取图表 - 使用多种方法尝试
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

        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.pdfbase import pdfmetrics  # 正确的导入！
        from reportlab.pdfbase.ttfonts import TTFont

        # 尝试加载中文字体
        font_name = 'Helvetica'  # 默认降级
        
        try:
            # 使用系统中实际存在的中文字体
            fonts_to_try = [
                ("/System/Library/Fonts/Hiragino Sans GB.ttc", 0),  # Mac - 冬青黑体
                ("/System/Library/Fonts/STHeiti Medium.ttc", 0),    # Mac - 华文黑体
                ("C:\\Windows\\Fonts\\msyh.ttc", 0),                # Windows - 微软雅黑
                ("C:\\Windows\\Fonts\\simhei.ttf", None),           # Windows - 黑体
            ]
            
            for font_path, subfont_index in fonts_to_try:
                if os.path.exists(font_path):
                    try:
                        if subfont_index is not None:
                            # .ttc 文件需要指定 subfontIndex
                            pdfmetrics.registerFont(TTFont('ChineseFont', font_path, subfontIndex=subfont_index))
                        else:
                            # .ttf 文件直接加载
                            pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                        
                        font_name = 'ChineseFont'
                        print(f"✅ 成功加载中文字体: {font_path}")
                        break
                    except Exception as e:
                        print(f"⚠️ 尝试加载 {font_path} 失败: {e}")
                        continue
            
            if font_name == 'Helvetica':
                print("⚠️ 警告: 未找到支持的中文字体")
                print("💡 建议: 使用 SimpleHTMLExporter.export_to_html() 导出 HTML 格式")
                
        except Exception as e:
            print(f"❌ 字体加载过程出错: {e}")
            print("💡 建议: 使用 HTML 导出以避免字体问题")
            font_name = 'Helvetica'

        doc = SimpleDocTemplate(str(output_path), pagesize=A4)
        styles = getSampleStyleSheet()
        
        # 自定义样式 - 使用 Normal 作为父样式以避免字体覆盖
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Normal'],  # 改用 Normal 避免字体被覆盖
            fontName=font_name,
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # 居中对齐
            textColor='#1A237E'
        )
        
        heading2_style = ParagraphStyle(
            'Heading2Custom',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=16,
            spaceAfter=12,
            textColor='#333333'
        )
        
        heading3_style = ParagraphStyle(
            'Heading3Custom',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=14,
            spaceAfter=10,
            textColor='#555555'
        )
        
        body_style = ParagraphStyle(
            'BodyText',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=10,
            leading=14,
            spaceBefore=6
        )

        elements = []

        # -- 封面 --
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(f"作者: {author}", body_style))
        elements.append(Paragraph(f"日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}", body_style))
        elements.append(PageBreak())

        # -- 配置页面 --
        if filters_str:
            elements.append(Paragraph("🔍 分析配置汇总", heading2_style))
            elements.append(Spacer(1, 10))
            for line in filters_str.split('\n'):
                if line.strip():
                    elements.append(Paragraph(line, body_style))
            elements.append(Spacer(1, 20))

        # -- 图表页面 --
        temp_images = []
        print(f"\n📊 开始处理 {len(figures)} 个图表...")
        
        for i, fig in enumerate(figures):
            img_path = None
            chart_title = f"图表 {i+1}"
            
            try:
                # 尝试获取图表标题
                if hasattr(fig, 'layout') and hasattr(fig.layout, 'title') and fig.layout.title:
                    chart_title = fig.layout.title.text or chart_title
            except Exception as e:
                print(f"  ⚠️ 无法获取图表 {i+1} 的标题: {e}")
            
            # 添加标题到 PDF
            try:
                elements.append(Paragraph(f"📊 图表 {i+1}: {chart_title}", heading3_style))
                elements.append(Spacer(1, 10))
            except Exception as e:
                print(f"  ⚠️ 添加图表标题失败: {e}")
            
            # 转换并添加图表图片
            try:
                img_path = f"temp_fig_{i}.png"
                print(f"  🖼️ 正在导出图表 {i+1}/{len(figures)}: {chart_title}...")
                
                # 将 Plotly 转为静态图
                fig.write_image(img_path, format="png", width=1200, height=800, scale=2)
                temp_images.append(img_path)
                
                if os.path.exists(img_path):
                    file_size = os.path.getsize(img_path) / 1024
                    print(f"    ✅ 成功生成图片 ({file_size:.1f} KB)")
                    
                    # 插入 PDF
                    img = Image(img_path, width=6.5*inch, height=4*inch)
                    elements.append(img)
                    elements.append(Spacer(1, 20))
                else:
                    print(f"    ❌ 图片文件未生成")
                    
            except Exception as e:
                print(f"  ❌ 导出图表 {i+1} 失败: {e}")
                import traceback
                traceback.print_exc()
            
            # 分页
            if (i + 1) % 2 == 0:
                elements.append(PageBreak())

        # 4. 生成 PDF
        doc.build(elements)

        # 5. 清理临时文件
        for img in temp_images:
            if os.path.exists(img):
                os.remove(img)

        print(f"✅ 报告已成功导出至: {output_path}")
        return str(output_path)
