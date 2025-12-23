#!/bin/bash

# 快速设置 Git 同步

echo "🚀 Jupyter_AI_DataAnalyze Git 同步设置"
echo "========================================"
echo ""

# 检查是否在项目目录
if [ ! -f "setup.py" ] && [ ! -d "src" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 1. 检查 Git
if ! command -v git &> /dev/null; then
    echo "❌ Git 未安装"
    echo "Mac: brew install git"
    echo "Windows: https://git-scm.com/download/win"
    exit 1
fi

echo "✅ Git 已安装"

# 2. 检查 GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI 未安装（推荐）"
    echo "安装: brew install gh"
    echo ""
    read -p "是否继续手动设置? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    USE_GH=false
else
    echo "✅ GitHub CLI 已安装"
    USE_GH=true
fi

# 3. 初始化 Git（如果需要）
if [ ! -d ".git" ]; then
    echo ""
    echo "📦 初始化 Git 仓库..."
    git init
    git branch -M main
    echo "✅ Git 仓库已初始化"
else
    echo "✅ Git 仓库已存在"
fi

# 4. 检查 .gitignore
if [ ! -f ".gitignore" ]; then
    echo "⚠️  .gitignore 不存在，已自动创建"
fi

# 5. 配置用户信息
echo ""
echo "🔧 配置 Git 用户信息"
read -p "输入你的名字: " git_name
read -p "输入你的邮箱: " git_email

git config user.name "$git_name"
git config user.email "$git_email"

echo "✅ 用户信息已配置"

# 6. 首次提交
echo ""
echo "📝 准备首次提交..."

# 显示将要提交的文件
echo "将提交以下文件类型:"
echo "  - Python 源代码 (src/)"
echo "  - 文档 (docs/)"
echo "  - 脚本 (scripts/)"
echo "  - 示例 (examples/)"
echo "  - 配置文件"
echo ""
echo "将排除:"
echo "  - 数据文件 (data/*.parquet)"
echo "  - 虚拟环境 (.venv/)"
echo "  - 输出文件 (*.html, *.png)"
echo ""

read -p "继续? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 1
fi

git add .
git commit -m "Initial commit: AI Data Analysis Framework"

echo "✅ 首次提交完成"

# 7. 推送到 GitHub
echo ""
echo "☁️  推送到 GitHub"

if [ "$USE_GH" = true ]; then
    # 使用 GitHub CLI
    echo "使用 GitHub CLI 创建仓库..."
    
    read -p "仓库设为私有? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        VISIBILITY="--private"
    else
        VISIBILITY="--public"
    fi
    
    gh auth status &> /dev/null || gh auth login
    
    gh repo create Jupyter_AI_DataAnalyze \
        $VISIBILITY \
        --source=. \
        --remote=origin \
        --push
    
    echo "✅ 仓库已创建并推送"
else
    # 手动设置
    echo ""
    echo "请手动完成以下步骤:"
    echo "1. 访问 https://github.com/new"
    echo "2. 创建名为 'Jupyter_AI_DataAnalyze' 的仓库"
    echo "3. 复制仓库 URL"
    echo ""
    read -p "输入仓库 URL: " repo_url
    
    git remote add origin "$repo_url"
    git push -u origin main
    
    echo "✅ 已推送到 GitHub"
fi

# 8. 完成
echo ""
echo "======================================"
echo "🎉 设置完成！"
echo ""
echo "下一步："
echo "1. 在公司电脑克隆仓库:"
echo "   git clone https://github.com/你的用户名/Jupyter_AI_DataAnalyze.git"
echo ""
echo "2. 日常使用:"
echo "   - 推送: git add . && git commit -m '描述' && git push"
echo "   - 拉取: git pull"
echo ""
echo "3. 查看详细文档:"
echo "   docs/SYNC_GUIDE.md"
echo "======================================"
