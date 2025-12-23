# ========================================
# 移除 JupyterLab Cell 宽度限制
# ========================================
# 在任何 notebook 开头运行此 cell，让内容占满全屏

from IPython.display import HTML, display

# 移除 cell 宽度限制，让内容占满屏幕
display(HTML("""
<style>
    /* 移除 notebook cell 的最大宽度限制 */
    .jp-Notebook-cell {
        max-width: none !important;
    }
    
    /* 让输出区域也占满宽度 */
    .jp-OutputArea-output {
        max-width: none !important;
    }
    
    /* 确保容器占满宽度 */
    .jp-Cell-outputWrapper {
        max-width: none !important;
    }
</style>
"""))

print("✅ Cell 宽度限制已移除，内容将占满屏幕")
