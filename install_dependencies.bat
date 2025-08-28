@echo off
echo ========================================
echo EmbyBot 依赖安装脚本
echo ========================================
echo.

echo 正在检查Python版本...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安装或不在PATH中
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

echo.
echo 正在安装依赖包...
echo.

pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✅ 依赖安装成功！
    echo.
    echo 现在可以运行: python main.py
) else (
    echo.
    echo ❌ 依赖安装失败，请检查网络连接或Python环境
)

echo.
pause
