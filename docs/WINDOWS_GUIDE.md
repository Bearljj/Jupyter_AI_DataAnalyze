# Windows 使用指南

Mac 和 Windows 平台差异详解及解决方案。

---

## 🖥️ **主要差异对比**

| 方面 | Mac | Windows |
|------|-----|---------|
| **Shell** | zsh/bash | PowerShell/CMD |
| **路径分隔符** | `/` | `\` |
| **配置文件** | `~/.zshrc`, `~/.bash_profile` | 环境变量设置 |
| **脚本扩展名** | `.sh` | `.bat`, `.ps1` |
| **Python 命令** | `python3` | `python` |
| **虚拟环境激活** | `source .venv/bin/activate` | `.venv\Scripts\activate` |
| **换行符** | LF (`\n`) | CRLF (`\r\n`) |

---

## 📥 **首次设置（Windows）**

### **1. 克隆项目**

```powershell
# PowerShell

# 克隆
cd C:\Users\你的用户名\Documents
git clone https://github.com/你的用户名/Jupyter_AI_DataAnalyze.git

cd Jupyter_AI_DataAnalyze
```

### **2. 安装 Python 依赖**

```powershell
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境（重要！与 Mac 不同）
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 或使用 uv（更快）
pip install uv
uv pip install -r requirements.txt
```

### **3. 启动 Jupyter Lab**

```powershell
# 在项目根目录
jupyter lab

# 或使用 uv
uv run jupyter lab
```

---

## 🔄 **日常使用差异**

### **差异 1: 虚拟环境激活**

#### **Mac:**
```bash
source .venv/bin/activate
```

#### **Windows (PowerShell):**
```powershell
.venv\Scripts\activate
```

#### **Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**💡 提示**: Windows 上可能遇到执行策略限制

---

### **差异 2: 执行策略限制（重要！）**

**问题**: Windows PowerShell 默认可能禁止运行脚本

```powershell
# 可能遇到的错误
.venv\Scripts\activate
# 错误: 无法加载文件，因为在此系统上禁止运行脚本
```

**解决方案 A**: 临时绕过（推荐）

```powershell
# 使用 PowerShell 以管理员身份运行
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然后可以正常激活
.venv\Scripts\activate
```

**解决方案 B**: 每次激活时绕过

```powershell
PowerShell -ExecutionPolicy Bypass -File .venv\Scripts\activate.ps1
```

**解决方案 C**: 使用 CMD 而不是 PowerShell

```cmd
# CMD 中没有执行策略限制
.venv\Scripts\activate.bat
```

---

### **差异 3: Python 命令**

#### **Mac:**
```bash
python3 script.py
pip3 install package
```

#### **Windows:**
```powershell
python script.py   # 注意：通常是 python，不是 python3
pip install package
```

**检查方法**:
```powershell
python --version
# Python 3.12.0

# 如果提示找不到，检查 PATH
where python
```

---

### **差异 4: Shell 脚本**

#### **Mac 上的 `.sh` 脚本**

```bash
# Mac
./scripts/setup_git_sync.sh
chmod +x scripts/setup_git_sync.sh
```

#### **Windows 需要转换或使用替代方案**

**选项 1**: 使用 Git Bash（推荐）

```bash
# 安装 Git for Windows 后，使用 Git Bash
bash scripts/setup_git_sync.sh
```

**选项 2**: 创建对应的 `.bat` 或 `.ps1` 脚本

我会在下面提供 Windows 版本的脚本。

**选项 3**: 手动执行命令

---

### **差异 5: 路径表示**

#### **Mac:**
```python
path = '/Users/harold/working/Jupyter_AI_DataAnalyze/data/file.parquet'
path = '~/working/data/file.parquet'  # 波浪号展开
```

#### **Windows:**
```python
path = 'C:\\Users\\Harold\\Documents\\Jupyter_AI_DataAnalyze\\data\\file.parquet'
path = r'C:\Users\Harold\Documents\Jupyter_AI_DataAnalyze\data\file.parquet'  # 原始字符串

# 推荐：使用 os.path 或 pathlib（跨平台）
import os
path = os.path.join('data', 'file.parquet')  # 自动使用正确分隔符

from pathlib import Path
path = Path('data') / 'file.parquet'  # 推荐
```

**好消息**: 我们的代码已经使用了 `os.path.join()`，所以是跨平台的！✅

---

### **差异 6: Git 配置**

#### **Mac:**
```bash
git config --global core.autocrlf input
```

#### **Windows:**
```powershell
# 自动转换换行符
git config --global core.autocrlf true

# 克隆时自动转换 CRLF → LF
# 提交时自动转换 LF → CRLF
```

这个已经在 Git for Windows 中默认设置好了。

---

### **差异 7: 环境变量设置**

#### **Mac (添加到 ~/.zshrc):**
```bash
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
```

#### **Windows (系统环境变量):**

**临时设置（当前会话）**:
```powershell
$env:SOME_VAR = "value"
```

**永久设置（用户级）**:
```powershell
# PowerShell (管理员)
[System.Environment]::SetEnvironmentVariable('SOME_VAR', 'value', 'User')
```

**或通过 GUI**:
1. 右键"此电脑" → 属性
2. 高级系统设置 → 环境变量
3. 新建或编辑

---

## 🛠️ **Windows 专用脚本**

### **1. 虚拟环境激活脚本（PowerShell）**

创建 `scripts/activate_venv.ps1`:

```powershell
# 激活虚拟环境的便捷脚本

Write-Host "🔧 激活虚拟环境..." -ForegroundColor Green

if (Test-Path .venv\Scripts\activate.ps1) {
    .venv\Scripts\activate
    Write-Host "✅ 虚拟环境已激活" -ForegroundColor Green
} else {
    Write-Host "❌ 虚拟环境不存在" -ForegroundColor Red
    Write-Host "创建虚拟环境: python -m venv .venv" -ForegroundColor Yellow
}
```

使用:
```powershell
.\scripts\activate_venv.ps1
```

---

### **2. Git 同步脚本（PowerShell）**

创建 `scripts/sync_git.ps1`:

```powershell
# Git 同步脚本

param(
    [string]$message = "更新代码"
)

Write-Host "🔄 Git 同步" -ForegroundColor Cyan
Write-Host ""

# 查看状态
Write-Host "📊 当前状态:" -ForegroundColor Yellow
git status

# 添加
Write-Host ""
Write-Host "➕ 添加所有修改..." -ForegroundColor Yellow
git add .

# 提交
Write-Host ""
Write-Host "💾 提交..." -ForegroundColor Yellow
git commit -m $message

# 推送
Write-Host ""
Write-Host "☁️  推送到 GitHub..." -ForegroundColor Yellow
git push

Write-Host ""
Write-Host "✅ 同步完成！" -ForegroundColor Green
```

使用:
```powershell
.\scripts\sync_git.ps1 "添加了新功能"
```

---

### **3. 启动 Jupyter 脚本（批处理）**

创建 `start_jupyter.bat`:

```batch
@echo off
echo 🚀 启动 Jupyter Lab
echo.

REM 激活虚拟环境
call .venv\Scripts\activate.bat

REM 启动 Jupyter Lab
jupyter lab

pause
```

使用: 双击 `start_jupyter.bat` 即可

---

## 📋 **完整的 Windows 工作流**

### **每天开始工作**

```powershell
# 1. 打开 PowerShell
# Win + X → Windows PowerShell

# 2. 进入项目目录
cd C:\Users\你的用户名\Documents\Jupyter_AI_DataAnalyze

# 3. 拉取最新代码
git pull

# 4. 激活虚拟环境
.venv\Scripts\activate

# 5. 启动 Jupyter Lab
jupyter lab

# 或使用批处理文件：
# 双击 start_jupyter.bat
```

### **每天结束工作**

```powershell
# 1. 保存 notebook

# 2. 提交代码
git add .
git commit -m "今日工作：xxx"
git push

# 或使用脚本：
.\scripts\sync_git.ps1 "今日工作：xxx"
```

---

## 🔧 **常见问题（Windows 特有）**

### **问题 1: PowerShell 执行策略错误**

```
无法加载文件，因为在此系统上禁止运行脚本
```

**解决**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### **问题 2: Python 找不到**

```
'python' 不是内部或外部命令
```

**解决**:
1. 确认 Python 已安装: [python.org](https://www.python.org/downloads/)
2. 安装时勾选 "Add Python to PATH"
3. 或手动添加到 PATH：
   - 找到 Python 安装路径（如 `C:\Python312\`）
   - 添加到系统环境变量 PATH

---

### **问题 3: Git 命令不可用**

**解决**: 安装 Git for Windows
- 下载: [git-scm.com](https://git-scm.com/download/win)
- 安装后包含:
  - Git Bash（类 Unix shell）
  - Git GUI
  - Git 命令行工具

---

### **问题 4: 路径太长错误**

```
文件名超出系统最大长度限制
```

**解决**:
```powershell
# 启用长路径支持（需管理员权限）
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

---

### **问题 5: 换行符问题**

Shell 脚本可能显示 `^M` 字符

**解决**:
```bash
# 使用 Git Bash
dos2unix scripts/*.sh

# 或配置 Git
git config --global core.autocrlf true
```

---

## 💡 **推荐工具（Windows）**

### **1. Windows Terminal（强烈推荐）**
- 现代化终端
- 支持多标签
- 美观且功能强大
- 免费，Microsoft Store 下载

### **2. Git Bash**
- Git for Windows 自带
- 提供 Unix-like 命令
- 可以运行 `.sh` 脚本

### **3. VS Code**
- 跨平台编辑器
- 集成终端
- Git 集成
- Jupyter 支持

---

## 🎯 **跨平台最佳实践**

### **1. 使用 `os.path` 或 `pathlib`**

```python
# ✅ 推荐（跨平台）
import os
path = os.path.join('data', 'file.parquet')

from pathlib import Path
path = Path('data') / 'file.parquet'

# ❌ 不推荐（平台特定）
path = 'data/file.parquet'  # Mac/Linux
path = 'data\\file.parquet'  # Windows
```

### **2. 使用相对路径**

```python
# ✅ 推荐
session.load('data/processed/file.parquet', alias='data')

# ❌ 不推荐
session.load('C:\\Users\\Harold\\...\\file.parquet', alias='data')
```

### **3. 配置 `.gitattributes`**

在项目根目录创建:

```
# .gitattributes
* text=auto
*.sh text eol=lf
*.py text eol=lf
*.md text eol=lf
*.bat text eol=crlf
```

---

## 📚 **快速参考卡片**

### **Mac 命令 → Windows 对应命令**

| Mac/Linux | Windows (PowerShell) | Windows (CMD) |
|-----------|---------------------|---------------|
| `ls` | `Get-ChildItem` 或 `ls` | `dir` |
| `cat file` | `Get-Content file` 或 `cat file` | `type file` |
| `rm file` | `Remove-Item file` | `del file` |
| `mv old new` | `Move-Item old new` | `move old new` |
| `cp src dst` | `Copy-Item src dst` | `copy src dst` |
| `pwd` | `Get-Location` 或 `pwd` | `cd` |
| `source .venv/bin/activate` | `.venv\Scripts\activate` | `.venv\Scripts\activate.bat` |
| `python3` | `python` | `python` |
| `./script.sh` | `.\script.ps1` 或双击 `.bat` | `script.bat` |

---

## ✅ **总结**

### **完全相同的部分**
- ✅ Python 代码（100% 兼容）
- ✅ Jupyter Notebook（100% 兼容）
- ✅ Git 操作（几乎相同）
- ✅ 数据分析逻辑（完全一样）

### **需要注意的差异**
- ⚠️ 虚拟环境激活命令
- ⚠️ Shell 脚本需要转换或用 Git Bash
- ⚠️ 路径分隔符（但我们的代码已处理）
- ⚠️ PowerShell 执行策略

### **推荐配置**
1. 安装 Git for Windows → 获得 Git Bash
2. 安装 Windows Terminal → 更好的终端体验
3. 使用 VS Code → 统一的开发环境
4. 配置好 `.gitattributes` → 自动处理换行符

---

**Windows 和 Mac 上的使用体验基本一致！** 🎉

主要注意激活虚拟环境的命令差异，其他都一样！
