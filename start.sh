#!/bin/bash

# Jupyter AI DataAnalyze - 快速启动脚本

echo "🚀 Jupyter AI DataAnalyze"
echo

# 检查是否在项目目录
if [ ! -f "pyproject.toml" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

# 检查 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo "📦 uv 未安装，正在安装..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# 同步依赖
echo "📦 安装依赖..."
uv sync

# 确保环境变量文件存在
if [ ! -f ".env" ]; then
    echo "📝 创建环境变量文件..."
    cp .env.example .env
fi

# 启动 Jupyter Lab
echo
echo "✅ 环境就绪！"
echo
echo "🚀 启动 Jupyter Lab..."
echo
uv run jupyter lab
