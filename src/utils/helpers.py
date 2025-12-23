"""工具函数模块"""

from pathlib import Path


def get_ai_context_path():
    """
    获取 AI Context 文档的正确路径
    
    无论从哪个目录运行，都能找到 AI Context 文档
    
    Returns:
        Path: AI Context 文档路径
    """
    # 尝试多个可能的路径
    possible_paths = [
        Path("docs/ai_context/main.md"),  # 从项目根目录
        Path("../../docs/ai_context/main.md"),  # 从 notebooks/templates/
        Path("../../../docs/ai_context/main.md"),  # 其他可能的位置
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    # 如果都找不到，尝试从当前文件位置计算
    src_path = Path(__file__).parent.parent
    ai_context = src_path / "docs" / "ai_context" / "main.md"
    
    if ai_context.exists():
        return ai_context
    
    raise FileNotFoundError(
        "找不到 AI Context 文档。请确保在项目根目录运行 Jupyter。"
    )


def load_ai_context():
    """
    加载 AI Context 文档内容
    
    Returns:
        str: AI Context 文档内容
    """
    context_path = get_ai_context_path()
    
    with open(context_path, "r", encoding="utf-8") as f:
        return f.read()
