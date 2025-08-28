#!/bin/bash

echo "========================================"
echo "EmbyBot 依赖安装脚本"
echo "========================================"
echo

echo "正在检查Python版本..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3未安装或不在PATH中"
    echo "请先安装Python 3.8+"
    exit 1
fi

echo
echo "正在安装依赖包..."
echo

pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo
    echo "✅ 依赖安装成功！"
    echo
    echo "现在可以运行: python3 main.py"
else
    echo
    echo "❌ 依赖安装失败，请检查网络连接或Python环境"
fi

echo
