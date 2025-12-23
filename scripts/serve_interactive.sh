#!/bin/bash
# ========================================
# 启动交互式 Notebook Web 应用
# ========================================

NOTEBOOK="$1"
PORT="${2:-8866}"

if [ -z "$NOTEBOOK" ]; then
    echo "❌ 错误: 请提供 notebook 文件"
    echo "用法: $0 <notebook.ipynb> [port]"
    echo "示例: $0 notebooks/analysis.ipynb 8866"
    exit 1
fi

if [ ! -f "$NOTEBOOK" ]; then
    echo "❌ 错误: 文件不存在: $NOTEBOOK"
    exit 1
fi

echo "🚀 启动交互式 Web 应用..."
echo "📊 Notebook: $NOTEBOOK"
echo "🌐 端口: $PORT"
echo ""
echo "=" 
echo "访问链接: http://localhost:$PORT"
echo "="
echo ""
echo "💡 提示:"
echo "  - 所有仪表盘控件都可以使用"
echo "  - 图表完全可交互"
echo "  - 按 Ctrl+C 停止服务"
echo ""
echo "🔗 分享给团队:"
echo "  1. 在服务器上运行此脚本"
echo "  2. 将 localhost 替换为服务器 IP"
echo "  3. 确保端口可访问"
echo ""

# 检查 Voila 是否安装
if ! command -v voila &> /dev/null; then
    echo "⚠️  Voila 未安装"
    echo "📦 正在安装..."
    pip install voila
fi

# 启动 Voila
voila "$NOTEBOOK" \
    --port=$PORT \
    --no-browser \
    --Voila.ip=0.0.0.0 \
    --enable_nbextensions=True

# 如果失败，尝试只监听本地
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  启动失败，尝试只监听本地..."
    voila "$NOTEBOOK" --port=$PORT
fi
