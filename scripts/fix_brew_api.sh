#!/bin/bash

# 快速修复 Homebrew 镜像配置

echo "🔧 快速修复 Homebrew 配置"
echo ""

# 检测 shell 配置文件
if [ -f ~/.zshrc ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -f ~/.bash_profile ]; then
    SHELL_CONFIG="$HOME/.bash_profile"
else
    SHELL_CONFIG="$HOME/.zshrc"
fi

echo "配置文件: $SHELL_CONFIG"
echo ""

# 添加缺失的配置
if ! grep -q "HOMEBREW_API_DOMAIN" "$SHELL_CONFIG"; then
    echo "添加 API 域名配置..."
    
    cat >> "$SHELL_CONFIG" << 'EOF'

# Homebrew API 镜像（修复）
export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
export HOMEBREW_NO_INSTALL_FROM_API=1
EOF
    
    echo "✅ 已添加 API 配置"
else
    echo "✅ API 配置已存在"
fi

# 立即生效
echo ""
echo "🔄 使配置生效..."
export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
export HOMEBREW_NO_INSTALL_FROM_API=1

# 显示当前配置
echo ""
echo "📊 当前配置："
echo "HOMEBREW_BOTTLE_DOMAIN: ${HOMEBREW_BOTTLE_DOMAIN:-未设置}"
echo "HOMEBREW_API_DOMAIN: ${HOMEBREW_API_DOMAIN}"
echo "HOMEBREW_NO_INSTALL_FROM_API: ${HOMEBREW_NO_INSTALL_FROM_API}"

echo ""
echo "✅ 修复完成！"
echo ""
echo "💡 下一步："
echo "1. 运行: source $SHELL_CONFIG"
echo "2. 重新尝试: brew update"
echo "3. 或直接关闭终端重新打开"
