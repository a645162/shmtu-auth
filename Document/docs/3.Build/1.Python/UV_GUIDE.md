# UV 包管理器使用指南

本项目现在支持使用 [uv](https://docs.astral.sh/uv/) 作为 Python 包管理器，它比传统的 pip 更快、更可靠。

## 安装 UV

### Windows (PowerShell)

```powershell
# 运行自动安装脚本
.\setup_uv.ps1

# 或手动安装
Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
```

### Linux/macOS (Bash)

```bash
# 运行自动安装脚本
./setup_uv.sh

# 或手动安装
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 使用 pip 安装

```bash
pip install uv
```

## 项目设置

### 1. 初始化项目环境

```bash
# 同步所有依赖（包括开发依赖）
uv sync

# 仅安装生产依赖
uv sync --no-dev
```

### 2. 运行项目

```bash
# 运行 CLI 版本
uv run python start_cli.py

# 运行作为模块
uv run python -m shmtu_auth

# 运行测试
uv run pytest
```

## 包管理

### 添加依赖

```bash
# 添加生产依赖
uv add requests

# 添加开发依赖
uv add --dev pytest

# 添加可选依赖
uv add --optional gui PySide6
```

### 移除依赖

```bash
# 移除包
uv remove requests

# 移除开发依赖
uv remove --dev pytest
```

### 更新依赖

```bash
# 更新所有依赖
uv sync --upgrade

# 更新特定包
uv add requests --upgrade
```

## Python 版本管理

### 安装 Python 版本

```bash
# 安装特定 Python 版本
uv python install 3.8

# 使用特定 Python 版本
uv python use 3.8
```

### 查看可用版本

```bash
# 查看已安装的 Python 版本
uv python list

# 查看可安装的 Python 版本
uv python list --all
```

## 构建和发布

### 构建包

```bash
# 构建 wheel 和 source distribution
uv build

# 仅构建 wheel
uv build --wheel

# 仅构建 source distribution
uv build --sdist
```

### 发布到 PyPI

```bash
# 发布到 PyPI
uv publish

# 发布到测试 PyPI
uv publish --repository testpypi
```

## 环境管理

### 创建虚拟环境

```bash
# 创建新的虚拟环境
uv venv

# 使用特定 Python 版本创建环境
uv venv --python 3.8

# 激活虚拟环境 (Windows)
.venv\Scripts\activate

# 激活虚拟环境 (Linux/macOS)
source .venv/bin/activate
```

### 查看环境信息

```bash
# 显示项目信息
uv show

# 显示依赖树
uv tree
```

## 配置

### 项目配置文件

项目的 uv 配置在 `pyproject.toml` 中：

```toml
[tool.uv]
dev-dependencies = [
    "pytest>=6.0",
    "flake8",
    "black",
    "isort",
]
```

### 全局配置

```bash
# 设置全局配置
uv config set global.index-url https://pypi.org/simple/

# 查看配置
uv config list
```

## 优势

相比传统的 pip + virtualenv 工作流，uv 提供了：

* **速度**：比 pip 快 10-100 倍
* **可靠性**：内置依赖解析器，避免冲突
* **简单性**：单一工具管理 Python 版本、包和环境
* **兼容性**：完全兼容 pip 和 PyPI
* **锁定文件**：自动生成 `uv.lock` 确保可重现构建

## 迁移指南

如果您之前使用 pip：

| pip 命令 | uv 命令 |
|----------|---------|
| `pip install package` | `uv add package` |
| `pip install -r requirements.txt` | `uv sync` |
| `pip uninstall package` | `uv remove package` |
| `pip list` | `uv show` |
| `python -m venv .venv` | `uv venv` |
| `pip install -e .` | `uv sync` |

## 故障排除

### 常见问题

1. **uv 命令未找到**
   * 确保 uv 已正确安装并在 PATH 中
   * Windows: 重启终端或重新加载环境变量
   * Linux/macOS: `source ~/.bashrc` 或 `source ~/.zshrc`

2. **依赖冲突**

```bash
   # 重新解析依赖
   uv sync --refresh
   ```

3. **Python 版本问题**

```bash
   # 检查当前 Python 版本
   uv python list
   
   # 安装需要的版本
   uv python install 3.8
   ```

4. **网络问题**

```bash
   # 使用不同的索引
   uv sync --index-url https://mirrors.aliyun.com/pypi/simple/
   ```

更多信息请参考 [uv 官方文档](https://docs.astral.sh/uv/)。
