import os
from datetime import datetime
import plotly.io as pio
import polars as pl
from pathlib import Path
import re

# ReportLab 核心导入
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class ReportExporter:
    """
    通用 PDF 报告导出器
    与具体分析逻辑解耦，只依赖于 dashboard 对象或 Plotly 图表列表
    """
    
    @staticmethod
    def _extract_metadata(func):
        """从函数 docstring 中提取 [REPORT_METADATA] 块"""
        if not func or not func.__doc__:
            return None
        
        doc = func.__doc__
        # 兼容 [REPORT_METADATA] 或 [METADATA] 标签
        match = re.search(r"\[REPORT_METADATA\](.*?)\[/REPORT_METADATA\]", doc, re.DOTALL)
        if not match:
            match = re.search(r"\[METADATA\](.*?)\[/METADATA\]", doc, re.DOTALL)
            
        if match:
            return match.group(1).strip()
        return None

    @staticmethod
    def _extract_content(dashboard):
        """
        从仪表盘中提取图表和表格内容
        返回: (figures_list, tables_data_list)
        """
        figures = []
        captured_tables = []
        
        if not dashboard or not hasattr(dashboard, 'update_function') or not dashboard.update_function:
            return figures, captured_tables

        # Mock 机制：深度物理拦截（拦截漏斗底端的 df_to_markdown）
        import src.utils.polars_display as pd_util
        
        # 记录原始函数用于后续恢复
        original_df_to_md = pd_util.df_to_markdown
        
        def mock_df_to_markdown(df, **kwargs):
            if df is not None:
                # 抓取数据
                captured_tables.append(df)
                print(f"    ✨ 成功拦截底层表格数据: {df.height} 行")
            # 调用原函数以生成输出对象（虽然在 PDF 导出中我们不显式 display 它）
            return original_df_to_md(df, **kwargs)
        
        # 物理替换模块底层的函数入口
        pd_util.df_to_markdown = mock_df_to_markdown
        
        try:
            print("  🔄 正在执行分析逻辑并捕获多维内容...")
            # 当此函数执行时，其内部调用的 print_markdown_table 
            # 将会由于 Python 的 Module Globals 查找机制寻找到我们 mock 的 df_to_markdown
            fig = dashboard.update_function()
            if fig:
                figures = fig if isinstance(fig, list) else [fig]
        except Exception as e:
            print(f"  ⚠️ 内容提取失败: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # 恢复现场
            pd_util.df_to_markdown = original_df_to_md
            
        print(f"  ✅ 提取结果: {len(figures)} 个图表, {len(captured_tables)} 个表格")
        return figures, captured_tables

    @staticmethod
    def _create_pdf_table(df, font_name, body_style):
        """将 DataFrame 转换为 ReportLab Table 对象"""
        if df is None or df.is_empty():
            return None
            
        # 转换为列表 [header, row1, row2, ...]
        headers = df.columns
        data = [headers]
        
        # 智能截取逻辑：默认显示前 100 行
        MAX_SHOW = 100
        if df.height > MAX_SHOW:
            rows = df.head(MAX_SHOW-1).to_numpy().tolist()
            # 探测最后一行是否是合计行
            last_row = df.tail(1)
            first_val = str(last_row[0, 0]) if last_row.width > 0 else ""
            if "合计" in first_val or "Total" in first_val or "SUM" in first_val.upper():
                rows.append(last_row.to_numpy().tolist()[0])
            else:
                rows.append(["..." for _ in headers])
        else:
            rows = df.to_numpy().tolist()
            
        data.extend(rows)
        
        # 处理数值格式与合计行标记
        total_row_index = -1
        for r in range(1, len(data)):
            # 探测这一行是不是合计行
            first_cell = str(data[r][0])
            if "合计" in first_cell or "Total" in first_cell:
                total_row_index = r
                
            for c in range(len(data[r])):
                val = data[r][c]
                if isinstance(val, (float, int)) and not isinstance(val, bool):
                    if isinstance(val, float): 
                        data[r][c] = f"{val:,.2f}"
                    else:
                        data[r][c] = f"{val:,}"
                elif val is None:
                    data[r][c] = "-"

        # 创建 ReportLab 表格
        table = Table(data, hAlign='LEFT')
        
        # 基础样式
        table_style_list = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A237E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
        ]
        
        # 如果有合计行，高亮显示
        if total_row_index != -1:
            table_style_list.append(('BACKGROUND', (0, total_row_index), (-1, total_row_index), colors.HexColor('#E8EAF6')))
            table_style_list.append(('FONTNAME', (0, total_row_index), (-1, total_row_index), font_name))
            table_style_list.append(('TEXTCOLOR', (0, total_row_index), (-1, total_row_index), colors.black))
            table_style_list.append(('LINEABOVE', (0, total_row_index), (-1, total_row_index), 2, colors.HexColor('#1A237E')))

        table.setStyle(TableStyle(table_style_list))
        return table

    @staticmethod
    def export_to_pdf(dashboard=None, filename=None, title="数据分析报告", author="AI Data Analyst"):
        """
        将 dashboard (单个或列表) 导出为 PDF 报告
        """
        try:
            import kaleido  # 必须安装: pip install kaleido
        except ImportError:
            print("❌ 错误: 请先安装 kaleido 以便导出静态图表: pip install kaleido")
            return

        # 支持多仪表盘传入
        dashboards = []
        if isinstance(dashboard, list):
            dashboards = dashboard
        elif dashboard:
            dashboards = [dashboard]

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

        # 尝试加载中文字体
        font_name = 'Helvetica'  # 默认降级
        
        try:
            # 使用系统中实际存在的中文字体
            fonts_to_try = [
                ("/System/Library/Fonts/Hiragino Sans GB.ttc", 0),  # Mac - 东青黑体
                ("/System/Library/Fonts/STHeiti Medium.ttc", 0),    # Mac - 华文黑体
                ("C:\\Windows\\Fonts\\msyh.ttc", 0),                # Windows - 微软雅黑
                ("C:\\Windows\\Fonts\\simhei.ttf", None),           # Windows - 黑体
            ]
            
            for font_path, subfont_index in fonts_to_try:
                if os.path.exists(font_path):
                    try:
                        if subfont_index is not None:
                            pdfmetrics.registerFont(TTFont('ChineseFont', font_path, subfontIndex=subfont_index))
                        else:
                            pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                        
                        font_name = 'ChineseFont'
                        print(f"✅ 成功加载中文字体: {font_path}")
                        break
                    except Exception as e:
                        print(f"⚠️ 尝试加载 {font_path} 失败: {e}")
                        continue
            
            if font_name == 'Helvetica':
                print("⚠️ 警告: 未找到支持的中文字体")
                
        except Exception as e:
            print(f"❌ 字体加载过程出错: {e}")

        doc = SimpleDocTemplate(str(output_path), pagesize=A4)
        styles = getSampleStyleSheet()
        
        # 自定义样式
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=24,
            spaceAfter=30,
            alignment=1,
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

        # 列表样式
        list_item_style = ParagraphStyle(
            'ListItem',
            parent=body_style,
            leftIndent=20,
            firstLineIndent=-10,
            spaceBefore=2
        )

        elements = []

        # 封面
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(f"作者: {author}", body_style))
        elements.append(Paragraph(f"日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}", body_style))
        elements.append(PageBreak())

        # -- 各仪表盘详情页面 --
        temp_images = []
        for db_idx, db in enumerate(dashboards):
            print(f"\n📑 处理仪表盘 {db_idx+1} ({db.title if hasattr(db, 'title') else '未命名'}):")
            
            # 1. 提取元数据
            notes = ReportExporter._extract_metadata(db.update_function) if hasattr(db, 'update_function') else None
            
            # 2. 详情页页眉
            elements.append(Paragraph(f"第 {db_idx+1} 部分: {db.title if hasattr(db, 'title') else '数据分析'}", heading2_style))
            elements.append(Spacer(1, 10))

            # 3. 业务逻辑说明 (解析极简 Markdown)
            if notes:
                elements.append(Paragraph("📖 业务逻辑说明", heading3_style))
                for line in notes.split('\n'):
                    line = line.strip()
                    if not line: continue
                    
                    # A. 替换加粗 **text** -> <b>text</b>
                    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                    
                    # B. 匹配标题 ###
                    if line.startswith('###'):
                        elements.append(Paragraph(line.replace('###', '').strip(), heading3_style))
                    # C. 匹配标题 ##
                    elif line.startswith('##'):
                        elements.append(Paragraph(line.replace('##', '').strip(), heading2_style))
                    # D. 匹配列表 - 或 *
                    elif line.startswith('- ') or line.startswith('* '):
                        clean_text = line[2:].strip()
                        elements.append(Paragraph(f"• {clean_text}", list_item_style))
                    # E. 普通文本
                    else:
                        elements.append(Paragraph(line, body_style))
                        
                elements.append(Spacer(1, 15))

            # 4. 提取内容 (图表 + 表格)
            db_figures, db_tables = ReportExporter._extract_content(db)
            
            if not db_figures and not db_tables:
                print(f"  ⚠️ 警告: 仪表盘 {db_idx+1} 未能提取到任何内容")
                continue

            # 5. 分析配置
            if hasattr(db, 'widgets'):
                elements.append(Paragraph("📋 分析配置 (Filters & Aggregation)", heading3_style))
                for name, widget in db.widgets.items():
                    if name.startswith('_') and name != '_aggregation_dimension':
                        continue
                    val = widget.value
                    label = "当前聚合维度" if name == '_aggregation_dimension' else name
                    val_str = ", ".join([str(v) for v in val]) if isinstance(val, list) else str(val)
                    elements.append(Paragraph(f"• <b>{label}:</b> {val_str}", body_style))
                elements.append(Spacer(1, 15))

            # 6. 汇总数据表
            if db_tables:
                elements.append(Paragraph("📊 汇总数据表", heading3_style))
                elements.append(Spacer(1, 10))
                for df in db_tables:
                    pdf_table = ReportExporter._create_pdf_table(df, font_name, body_style)
                    if pdf_table:
                        elements.append(pdf_table)
                        elements.append(Spacer(1, 20))

            # 7. 渲染图表
            for fig_idx, fig in enumerate(db_figures):
                chart_title = f"图表 {fig_idx+1}"
                if hasattr(fig, 'layout') and hasattr(fig.layout, 'title') and fig.layout.title:
                    chart_title = fig.layout.title.text or chart_title

                elements.append(Paragraph(f"📊 {chart_title}", heading3_style))
                elements.append(Spacer(1, 5))

                img_path = f"temp_db{db_idx}_fig{fig_idx}.png"
                try:
                    fig.write_image(img_path, format="png", width=1200, height=800, scale=2)
                    temp_images.append(img_path)
                    img = Image(img_path, width=6.5*inch, height=4*inch)
                    elements.append(img)
                    elements.append(Spacer(1, 20))
                except Exception as e:
                    print(f"  ❌ 图表导出失败: {e}")
                
                if (fig_idx + 1) % 2 == 0:
                    elements.append(PageBreak())

            if db_idx < len(dashboards) - 1:
                elements.append(PageBreak())

        # 生成 PDF
        doc.build(elements)

        # 清理临时文件
        for img in temp_images:
            if os.path.exists(img):
                os.remove(img)

        print(f"✅ 报告已成功导出至: {output_path}")
        return str(output_path)
