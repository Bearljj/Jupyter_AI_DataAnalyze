# Homebrew 国内镜像源配置指南

加速 Homebrew 在中国的下载速度。

---

## 🚀 快速配置

### **运行自动化脚本**

```bash
cd /Users/harold/working/Jupyter_AI_DataAnalyze

./scripts/setup_brew_china_mirror.sh

# 按提示选择：
# 1) 清华大学镜像（推荐）
# 2) 阿里云镜像
# 3) 中科大镜像
# 4) 恢复官方源
```

---

## 📋 手动配置（备选）

### **方案 1: 清华大学镜像（推荐）**

```bash
# 1. 替换 brew.git
cd "$(brew --repo)"
git remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git

# 2. 替换 homebrew-core.git
cd "$(brew --repo homebrew/core)"
git remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git

# 3. 配置环境变量（zsh）
echo 'export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"' >> ~/.zshrc
echo 'export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"' >> ~/.zshrc
echo 'export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"' >> ~/.zshrc

# 4. 生效
source ~/.zshrc

# 5. 更新
brew update
```

---

### **方案 2: 阿里云镜像**

```bash
# 1. 替换源
cd "$(brew --repo)"
git remote set-url origin https://mirrors.aliyun.com/homebrew/brew.git

cd "$(brew --repo homebrew/core)"
git remote set-url origin https://mirrors.aliyun.com/homebrew/homebrew-core.git

# 2. 环境变量
echo 'export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.aliyun.com/homebrew/brew.git"' >> ~/.zshrc
echo 'export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.aliyun.com/homebrew/homebrew-core.git"' >> ~/.zshrc
echo 'export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.aliyun.com/homebrew/homebrew-bottles"' >> ~/.zshrc

source ~/.zshrc
brew update
```

---

### **方案 3: 中科大镜像**

```bash
cd "$(brew --repo)"
git remote set-url origin https://mirrors.ustc.edu.cn/brew.git

cd "$(brew --repo homebrew/core)"
git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git

echo 'export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.ustc.edu.cn/brew.git"' >> ~/.zshrc
echo 'export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.ustc.edu.cn/homebrew-core.git"' >> ~/.zshrc
echo 'export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.ustc.edu.cn/homebrew-bottles"' >> ~/.zshrc

source ~/.zshrc
brew update
```

---

## 🔄 恢复官方源

```bash
# 1. 恢复 git 源
cd "$(brew --repo)"
git remote set-url origin https://github.com/Homebrew/brew

cd "$(brew --repo homebrew/core)"
git remote set-url origin https://github.com/Homebrew/homebrew-core

# 2. 删除环境变量
# 编辑 ~/.zshrc，删除以下行：
# export HOMEBREW_BREW_GIT_REMOTE="..."
# export HOMEBREW_CORE_GIT_REMOTE="..."
# export HOMEBREW_BOTTLE_DOMAIN="..."

# 3. 生效
source ~/.zshrc

# 4. 更新
brew update
```

---

## ✅ 验证配置

### **检查当前源**

```bash
# 查看 brew 源
cd "$(brew --repo)" && git remote -v

# 查看 core 源
cd "$(brew --repo homebrew/core)" && git remote -v

# 查看环境变量
echo $HOMEBREW_BREW_GIT_REMOTE
echo $HOMEBREW_CORE_GIT_REMOTE
echo $HOMEBREW_BOTTLE_DOMAIN
```

### **测试速度**

```bash
# 安装一个小软件测试
brew install wget

# 应该能看到从国内镜像下载，速度快很多
```

---

## 🎯 推荐镜像源

| 镜像源 | 速度 | 稳定性 | 推荐 |
|--------|------|--------|------|
| 清华大学 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ 首选 |
| 阿里云 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ 备选 |
| 中科大 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ 备选 |

**建议**：优先使用清华源，如果遇到问题再换其他源。

---

## 💡 其他优化

### **禁用自动更新（可选）**

```bash
# Homebrew 每次 install 前都会自动更新，比较慢
# 可以禁用（但要定期手动更新）

echo 'export HOMEBREW_NO_AUTO_UPDATE=1' >> ~/.zshrc
source ~/.zshrc

# 需要更新时手动运行
brew update
```

### **使用代理（备选）**

```bash
# 如果有代理
echo 'export ALL_PROXY=http://127.0.0.1:7890' >> ~/.zshrc
source ~/.zshrc
```

---

## 🆘 常见问题

### **Q: 配置后还是很慢？**

A: 可能是 Bottles（预编译包）的问题：

```bash
# 检查 Bottles 域名
echo $HOMEBREW_BOTTLE_DOMAIN

# 应该显示国内镜像
# 如果不是，重新配置环境变量
```

### **Q: 更新时报错？**

A: 尝试：

```bash
# 清理缓存
brew cleanup

# 强制更新
brew update --force

# 如果还是不行，恢复官方源后再配置国内源
```

### **Q: 某些包下载还是慢？**

A: 部分包可能没有国内镜像：

```bash
# 临时使用官方源
HOMEBREW_BOTTLE_DOMAIN="" brew install <package>
```

---

## 📚 参考链接

- [清华大学开源镜像站](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/)
- [阿里云镜像站](https://developer.aliyun.com/mirror/homebrew)
- [中科大镜像站](https://mirrors.ustc.edu.cn/help/brew.git.html)

---

**配置完成后，Homebrew 下载速度会显著提升！** 🚀
