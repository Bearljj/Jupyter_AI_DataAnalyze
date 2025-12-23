# 代码同步指南

在家和公司之间同步代码的完整指南。

---

## 🚀 **快速开始**

### **首次设置（在家）**

```bash
cd /Users/harold/working/Jupyter_AI_DataAnalyze

# 1. 安装 GitHub CLI
brew install gh

# 2. 登录
gh auth login

# 3. 初始化并推送
git init
git add .
git commit -m "Initial commit"
gh repo create Jupyter_AI_DataAnalyze --private --source=. --push

# 完成！
```

### **首次设置（在公司）**

```bash
# 1. 克隆
git clone https://github.com/你的用户名/Jupyter_AI_DataAnalyze.git
cd Jupyter_AI_DataAnalyze

# 2. 安装环境
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. 准备数据（见下方数据同步方案）

# 完成！
```

---

## 📅 **日常工作流**

### **在家工作后推送**

```bash
# 查看修改
git status

# 添加并提交
git add .
git commit -m "描述你的修改"

# 推送
git push

# ✅ 完成！
```

### **在公司开始工作前**

```bash
# 拉取最新代码
git pull

# 如果有冲突，解决后：
git add .
git commit -m "解决冲突"
git push

# ✅ 开始工作
```

### **在公司工作后推送**

```bash
git add .
git commit -m "在公司的修改"
git push

# ✅ 回家可以拉取
```

---

## 📊 **数据文件同步**

### **方案 1: 云存储同步（推荐）**

**优点**: 
- ✅ 简单
- ✅ 自动同步
- ✅ 不占用 GitHub 空间

**设置**:

```bash
# 在家（使用 iCloud）
mkdir -p ~/Library/Mobile\ Documents/com~apple~CloudDocs/DataFiles
ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/DataFiles data/cloud

# 在公司（使用 OneDrive）
mkdir -p ~/OneDrive/DataFiles
ln -s ~/OneDrive/DataFiles data/cloud

# 复制数据到云存储
cp data/processed/*.parquet ~/Library/.../DataFiles/

# .gitignore 中排除
echo "data/cloud/" >> .gitignore
```

**使用**:

```python
# 代码中使用云存储路径
session.load('data/cloud/insurance_data.parquet', alias='data')
```

---

### **方案 2: Git LFS（大文件支持）**

**优点**:
- ✅ 版本控制数据
- ✅ 与代码一起管理

**限制**:
- ⚠️ GitHub 免费版有配额（1GB 存储，1GB/月带宽）

**设置**:

```bash
# 安装 Git LFS
brew install git-lfs  # Mac
# Windows: 下载安装包

# 初始化
git lfs install

# 追踪大文件
git lfs track "data/processed/*.parquet"
git lfs track "*.csv"

# 提交
git add .gitattributes
git commit -m "启用 Git LFS"

# 正常添加数据文件
git add data/processed/insurance_data.parquet
git commit -m "添加数据文件"
git push
```

---

### **方案 3: 只同步样本数据**

**优点**:
- ✅ 不占用空间
- ✅ 可以测试代码

**设置**:

```python
# 创建样本数据脚本
# scripts/create_sample_data.py

import polars as pl

# 读取完整数据
df = pl.read_parquet('data/processed/insurance_data.parquet')

# 创建样本（10,000 行）
sample = df.sample(n=10000, seed=42)

# 保存
sample.write_parquet('data/processed/sample_10k.parquet')

print("✅ 样本数据已创建")
```

```bash
# 运行脚本
python scripts/create_sample_data.py

# 提交样本
git add data/processed/sample_10k.parquet
git commit -m "添加样本数据"
git push
```

**在公司使用样本**:

```python
# 使用样本数据测试
session.load('sample_10k.parquet', alias='data')
```

---

### **方案 4: 内网文件服务器**

如果公司有内网文件服务器：

```bash
# 在公司
# 将数据放在文件服务器
cp data/processed/*.parquet //server/share/DataFiles/

# 创建符号链接
ln -s //server/share/DataFiles data/server

# 使用
session.load('data/server/insurance_data.parquet', alias='data')
```

---

## 🔄 **同步冲突处理**

### **情况 1: 拉取时有冲突**

```bash
$ git pull
Auto-merging src/session.py
CONFLICT (content): Merge conflict in src/session.py

# 1. 查看冲突文件
git status

# 2. 手动编辑冲突文件
# 查找 <<<<<<< HEAD 标记
# 选择保留哪部分代码

# 3. 标记为已解决
git add src/session.py

# 4. 完成合并
git commit -m "解决冲突"
git push
```

### **情况 2: 在两地都做了修改忘记同步**

```bash
# 在公司忘记推送，回家又做了修改

# 在家尝试推送时
$ git push
! [rejected]        main -> main (fetch first)

# 解决方法：
git pull --rebase  # 拉取并变基
# 如果有冲突，解决后：
git add .
git rebase --continue
git push
```

---

## 💡 **最佳实践**

### **提交习惯**

```bash
# ✅ 好的提交信息
git commit -m "添加多文件加载功能"
git commit -m "修复数据过滤bug"
git commit -m "更新AI Context文档"

# ❌ 不好的提交信息
git commit -m "update"
git commit -m "fix"
git commit -m "aaa"
```

### **定期同步**

```bash
# 每天开始工作前
git pull

# 每天结束工作后
git add .
git commit -m "今日工作：添加xxx功能"
git push

# 每做完一个功能
git commit -m "完成：xxx功能"
git push
```

### **分支管理（可选）**

```bash
# 开发新功能时使用分支
git checkout -b feature/new-analysis

# 开发...

# 完成后合并
git checkout main
git merge feature/new-analysis
git push
```

---

## 📱 **移动办公（可选）**

### **使用 GitHub Codespaces**

在浏览器中直接编辑：

1. 访问 `https://github.com/你的用户名/Jupyter_AI_DataAnalyze`
2. 点击 `Code` → `Codespaces` → `Create codespace`
3. 在线 VS Code 环境立即可用
4. 修改后自动同步

### **使用 GitHub Mobile**

在手机上查看代码：

1. 下载 GitHub App
2. 登录查看仓库
3. 可以查看提交历史、代码改动

---

## ⚙️ **自动化同步（高级）**

### **使用 Git Hooks**

```bash
# .git/hooks/post-commit
#!/bin/bash
# 每次提交后自动推送

git push origin main

# 启用
chmod +x .git/hooks/post-commit
```

### **使用定时任务**

```bash
# 每小时自动提交和推送（Mac）
crontab -e

# 添加：
0 * * * * cd /Users/harold/working/Jupyter_AI_DataAnalyze && git add . && git commit -m "Auto commit $(date)" && git push
```

---

## 🆘 **常见问题**

### **Q: 忘记推送怎么办？**

```bash
# 检查本地是否有未推送的提交
git log origin/main..HEAD

# 如果有，推送
git push
```

### **Q: accidentally 提交了大文件**

```bash
# 从历史中删除
git rm --cached data/processed/large_file.parquet
echo "data/processed/*.parquet" >> .gitignore
git commit -m "删除大文件"
git push
```

### **Q: 想回到之前的版本**

```bash
# 查看历史
git log

# 回到某个提交
git checkout <commit-hash>

# 或创建新分支
git checkout -b old-version <commit-hash>
```

---

## 📚 **学习资源**

- [Git 官方教程](https://git-scm.com/book/zh/v2)
- [GitHub Docs](https://docs.github.com/zh)
- [Git 速查表](https://training.github.com/downloads/zh_CN/github-git-cheat-sheet/)

---

## 🎯 **推荐配置**

### **在家和公司都安装**

```bash
# Git
brew install git  # Mac
# Windows: https://git-scm.com/download/win

# GitHub CLI
brew install gh  # Mac
# Windows: https://cli.github.com/

# Git LFS (如果需要)
brew install git-lfs
```

### **配置 Git**

```bash
# 设置用户信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 设置默认编辑器
git config --global core.editor "code --wait"  # VS Code

# 设置默认分支名
git config --global init.defaultBranch main

# 启用颜色
git config --global color.ui auto
```

---

**开始同步你的代码！** 🚀
