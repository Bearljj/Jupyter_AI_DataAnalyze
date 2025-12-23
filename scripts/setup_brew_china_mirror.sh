#!/bin/bash

# Homebrew 国内镜像源配置脚本
# 支持清华源和阿里源

echo "🍺 Homebrew 国内镜像源配置"
echo "================================"
echo ""

# 检查是否安装了 Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew 未安装"
    echo "请先安装 Homebrew: https://brew.sh"
    exit 1
fi

echo "✅ Homebrew 已安装"
echo ""

# 显示当前配置
echo "📊 当前配置："
echo "HOMEBREW_BREW_GIT_REMOTE: ${HOMEBREW_BREW_GIT_REMOTE:-未设置}"
echo "HOMEBREW_CORE_GIT_REMOTE: ${HOMEBREW_CORE_GIT_REMOTE:-未设置}"
echo ""

# 选择镜像源
echo "请选择镜像源："
echo "1) 清华大学镜像（推荐）"
echo "2) 阿里云镜像"
echo "3) 中科大镜像"
echo "4) 恢复官方源"
echo ""
read -p "输入选项 (1-4): " choice

case $choice in
    1)
        MIRROR_NAME="清华大学"
        BREW_GIT="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
        CORE_GIT="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"
        BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
        ;;
    2)
        MIRROR_NAME="阿里云"
        BREW_GIT="https://mirrors.aliyun.com/homebrew/brew.git"
        CORE_GIT="https://mirrors.aliyun.com/homebrew/homebrew-core.git"
        BOTTLE_DOMAIN="https://mirrors.aliyun.com/homebrew/homebrew-bottles"
        ;;
    3)
        MIRROR_NAME="中科大"
        BREW_GIT="https://mirrors.ustc.edu.cn/brew.git"
        CORE_GIT="https://mirrors.ustc.edu.cn/homebrew-core.git"
        BOTTLE_DOMAIN="https://mirrors.ustc.edu.cn/homebrew-bottles"
        ;;
    4)
        echo "🔄 恢复官方源..."
        
        # 恢复 brew 源
        cd "$(brew --repo)"
        git remote set-url origin https://github.com/Homebrew/brew
        
        # 恢复 core 源
        cd "$(brew --repo homebrew/core)"
        git remote set-url origin https://github.com/Homebrew/homebrew-core
        
        # 删除环境变量
        if [ -f ~/.zshrc ]; then
            sed -i.bak '/HOMEBREW_BREW_GIT_REMOTE/d' ~/.zshrc
            sed -i.bak '/HOMEBREW_CORE_GIT_REMOTE/d' ~/.zshrc
            sed -i.bak '/HOMEBREW_BOTTLE_DOMAIN/d' ~/.zshrc
        fi
        
        if [ -f ~/.bash_profile ]; then
            sed -i.bak '/HOMEBREW_BREW_GIT_REMOTE/d' ~/.bash_profile
            sed -i.bak '/HOMEBREW_CORE_GIT_REMOTE/d' ~/.bash_profile
            sed -i.bak '/HOMEBREW_BOTTLE_DOMAIN/d' ~/.bash_profile
        fi
        
        echo "✅ 已恢复官方源"
        echo "💡 请运行: source ~/.zshrc"
        exit 0
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "🔄 正在配置 $MIRROR_NAME 镜像源..."
echo ""

# 1. 替换 brew.git
echo "📦 配置 Homebrew 核心..."
cd "$(brew --repo)"
git remote set-url origin "$BREW_GIT"
echo "✅ Homebrew 核心源已更新"

# 2. 替换 homebrew-core.git
echo ""
echo "📦 配置 Homebrew Core..."

CORE_PATH="$(brew --repo homebrew/core)"
if [ -d "$CORE_PATH" ]; then
    cd "$CORE_PATH"
    git remote set-url origin "$CORE_GIT"
    echo "✅ Homebrew Core 源已更新"
else
    echo "⚠️  homebrew-core 不存在，正在安装..."
    brew tap homebrew/core
    if [ -d "$CORE_PATH" ]; then
        cd "$CORE_PATH"
        git remote set-url origin "$CORE_GIT"
        echo "✅ Homebrew Core 源已更新"
    else
        echo "⚠️  跳过 Core 配置（新版 Homebrew 可能不需要）"
    fi
fi

# 3. 配置环境变量
echo ""
echo "🔧 配置环境变量..."

# 检测 shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bash_profile"
else
    SHELL_CONFIG="$HOME/.zshrc"
fi

# 删除旧配置
if [ -f "$SHELL_CONFIG" ]; then
    sed -i.bak '/HOMEBREW_BREW_GIT_REMOTE/d' "$SHELL_CONFIG"
    sed -i.bak '/HOMEBREW_CORE_GIT_REMOTE/d' "$SHELL_CONFIG"
    sed -i.bak '/HOMEBREW_BOTTLE_DOMAIN/d' "$SHELL_CONFIG"
fi

# 添加新配置
cat >> "$SHELL_CONFIG" << EOF

# Homebrew 国内镜像源 ($MIRROR_NAME)
export HOMEBREW_BREW_GIT_REMOTE="$BREW_GIT"
export HOMEBREW_CORE_GIT_REMOTE="$CORE_GIT"
export HOMEBREW_BOTTLE_DOMAIN="$BOTTLE_DOMAIN"
export HOMEBREW_API_DOMAIN="$BOTTLE_DOMAIN/api"
export HOMEBREW_NO_INSTALL_FROM_API=1
EOF

echo "✅ 环境变量已配置到 $SHELL_CONFIG"

# 4. 更新
echo ""
echo "🔄 更新 Homebrew..."
brew update

# 5. 完成
echo ""
echo "================================"
echo "🎉 配置完成！"
echo ""
echo "已配置 $MIRROR_NAME 镜像源："
echo "  Homebrew: $BREW_GIT"
echo "  Core: $CORE_GIT"
echo "  Bottles: $BOTTLE_DOMAIN"
echo ""
echo "💡 下一步："
echo "1. 运行: source $SHELL_CONFIG"
echo "2. 测试: brew install wget"
echo ""
echo "如需恢复官方源，重新运行此脚本并选择选项 4"
echo "================================"
