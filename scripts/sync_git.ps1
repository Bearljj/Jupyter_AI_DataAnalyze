# Git 同步脚本 (PowerShell)
# 用法: .\scripts\sync_git.ps1 "提交信息"

param(
    [string]$CommitMessage = "更新代码"
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "       Git 同步到 GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否在 Git 仓库中
if (-not (Test-Path ".git")) {
    Write-Host "[错误] 当前目录不是 Git 仓库" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先初始化: git init" -ForegroundColor Yellow
    exit 1
}

# 1. 查看状态
Write-Host "[1/4] 检查修改状态..." -ForegroundColor Yellow
Write-Host ""
git status --short
Write-Host ""

# 2. 添加所有修改
Write-Host "[2/4] 添加所有修改..." -ForegroundColor Yellow
git add .
Write-Host "  已添加所有修改" -ForegroundColor Green
Write-Host ""

# 3. 提交
Write-Host "[3/4] 提交更改..." -ForegroundColor Yellow
git commit -m $CommitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[提示] 没有需要提交的更改" -ForegroundColor Yellow
    exit 0
}

Write-Host ""

# 4. 推送
Write-Host "[4/4] 推送到 GitHub..." -ForegroundColor Yellow
git push

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "       同步完成！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[错误] 推送失败" -ForegroundColor Red
    Write-Host ""
    Write-Host "可能的原因:" -ForegroundColor Yellow
    Write-Host "  1. 网络问题" -ForegroundColor Yellow
    Write-Host "  2. 需要先拉取: git pull" -ForegroundColor Yellow
    Write-Host "  3. 远程仓库未设置: git remote add origin <URL>" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
