# 开发环境搭建

## 前置要求

- Python ≥ 3.8（macOS x64 需要 ≤ 3.11）
- 推荐使用 [uv](https://docs.astral.sh/uv/) 包管理器
- 推荐使用 JetBrains PyCharm Professional（学生认证免费）

## 使用 UV 初始化

```bash
# Linux/macOS
./setup_uv.sh

# Windows
.\setup_uv.ps1
```

## 使用 Conda

```bash
# 创建虚拟环境
conda create -n shmtu-auth python=3.11
conda activate shmtu-auth

# 安装依赖
pip install -r requirements.txt
```

## 安装开发依赖

```bash
# 使用 pip
pip install -e ".[dev]"

# 或使用 uv
uv pip install -e ".[dev]"
```

开发依赖包含：pytest, pylint, flake8, ruff, pyinstaller, setuptools, wheel, twine, pillow, pytz

## 代码检查

```bash
# Ruff（推荐）
ruff check .

# Flake8
flake8 .

# Pylint
pylint src/shmtu_auth/
```

## 运行测试

```bash
# 运行全部测试
python -m pytest PyTest/ -v

# SSL 相关测试
python -m pytest PyTest/SSL/ -v
```

## PyCharm 配置

项目包含 `.run/` 目录下的运行配置，导入后可直接使用：

| 配置 | 功能 |
|------|------|
| `dev.run.xml` | 开发运行 |
| `build.run.xml` | 构建 |
| `test.run.xml` | 测试 |
| `install.run.xml` | 安装 |
| `flake8.run.xml` | 代码检查 |
