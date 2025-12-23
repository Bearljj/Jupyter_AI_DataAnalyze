@echo off
REM Jupyter Lab 启动脚本 (Windows)

echo ========================================
echo    启动 Jupyter AI Data Analysis
echo ========================================
echo.

REM 检查虚拟环境
if not exist ".venv\Scripts\activate.bat" (
    echo [错误] 虚拟环境不存在
    echo.
    echo 请先创建虚拟环境:
    echo   python -m venv .venv
    echo   .venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM 激活虚拟环境
echo [1/2] 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 启动 Jupyter Lab
echo [2/2] 启动 Jupyter Lab...
echo.
echo ========================================
echo  在浏览器中打开: http://localhost:8888
echo  按 Ctrl+C 停止服务器
echo ========================================
echo.

jupyter lab

pause
