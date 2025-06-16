# Makefile for shmtu-auth project with UV support
.PHONY: help install dev-install run test build clean lint format check

# 默认目标
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  dev-install  - Install all dependencies (including dev)"
	@echo "  run          - Run the CLI application"
	@echo "  test         - Run tests"
	@echo "  build        - Build the package"
	@echo "  clean        - Clean build artifacts"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  check        - Run all checks (lint + test)"

# 安装生产依赖
install:
	uv sync --no-dev

# 安装所有依赖（包括开发依赖）
dev-install:
	uv sync

# 运行应用程序
run:
	uv run python start_cli.py

# 运行测试
test:
	uv run pytest PyTest/ -v

# 构建包
build:
	uv build

# 清理构建文件
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# 代码检查
lint:
	uv run flake8 src/

# 代码格式化
format:
	uv run black src/
	uv run isort src/

# 运行所有检查
check: lint test

# 更新依赖
upgrade:
	uv sync --upgrade

# 显示依赖树
tree:
	uv tree

# 显示项目信息
info:
	uv show
