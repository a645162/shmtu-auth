#!/usr/bin/env bash
# 快速设置 uv 环境的脚本

echo "正在安装 uv..."

# 检查是否已安装 uv
if ! command -v uv &>/dev/null; then
	echo "uv 未安装，正在安装..."
	# 在 Linux/macOS 上安装 uv
	curl -LsSf https://astral.sh/uv/install.sh | sh
	# 添加到 PATH
	export PATH="$HOME/.cargo/bin:$PATH"
	echo "uv 安装完成！"
else
	echo "uv 已安装"
fi

echo "正在初始化项目..."

# 同步依赖
uv sync

echo "设置完成！"
echo ""
echo "使用方法："
echo "  uv run python start_cli.py         # 运行 CLI 版本"
echo "  uv run python -m shmtu_auth        # 运行模块"
echo "  uv add <package>                   # 添加新依赖"
echo "  uv remove <package>                # 移除依赖"
echo "  uv sync                            # 同步依赖"
echo "  uv run pytest                      # 运行测试"
