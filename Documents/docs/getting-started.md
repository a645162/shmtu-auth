# 快速开始

## 系统要求

### 基本要求

- **Python 版本**: Python 3.8 或更高版本
- **操作系统**: Windows 7+, macOS 10.12+, Linux（任意现代发行版）
- **内存**: 至少 100MB 可用内存
- **网络**: 能够访问上海海事大学校园网

### GUI 版本额外要求

- **Python 版本**: Python 3.8+（推荐 3.13）
- **显示环境**: 支持图形界面的桌面环境
- **依赖库**: PySide6 及相关 Qt 组件

::: warning
macOS x64 (Intel) 平台下 Python 版本必须 ≤ 3.11，否则无法安装 PySide6。
:::

## 安装方式

### 1. 预编译程序（推荐）

这是最简单的安装方式，适合大多数用户。

1. 访问 [GitHub Releases](https://github.com/a645162/shmtu-auth/releases)
2. 选择最新版本
3. 根据操作系统下载对应文件：
   - **Windows**: `shmtu-auth-windows-x64.exe`
   - **macOS**: `shmtu-auth-macos-arm64`（Apple Silicon）或 `shmtu-auth-macos-x64`（Intel）
   - **Linux**: `shmtu-auth-linux-x64`

**运行**：

```bash
# macOS/Linux 需先添加执行权限
chmod +x shmtu-auth-macos-arm64
./shmtu-auth-macos-arm64

# 或使用配置文件
./shmtu-auth-macos-arm64 -t config.toml
```

::: warning
macOS 用户请确认芯片架构（Apple Silicon 或 Intel），下载对应版本。
:::

### 2. Python 包安装

```bash
# 安装最新版本
pip install shmtu-auth

# 指定版本安装
pip install shmtu-auth==2.1.0

# 升级到最新版本
pip install --upgrade shmtu-auth
```

安装后直接运行：

```bash
# 命令行使用
shmtu-auth

# 使用配置文件
shmtu-auth -t config.toml
```

### 3. 使用 UV 包管理器

推荐使用 [uv](https://docs.astral.sh/uv/) 包管理器，提供更快的依赖安装体验：

```bash
# Linux/macOS
./setup_uv.sh
uv run python start_cli.py

# Windows (PowerShell)
.\setup_uv.ps1
uv run python start_cli.py
```

### 4. Docker 部署（服务器推荐）

```bash
# 从 Docker Hub 拉取（国外）
docker pull a645162/shmtu-auth:latest

# 从阿里云 ACR 拉取（国内，推荐）
docker pull registry.cn-shanghai.aliyuncs.com/a645162/shmtu-auth:latest
```

Tag 说明：

| Tag | 说明 |
|-----|------|
| `latest` | 最新稳定版本（main 分支） |
| `vX.Y.Z` | 指定版本（稳定版） |
| `latest-beta` | beta 版本（beta 分支） |

详细 Docker 配置请参考 [Docker 部署](/docker/headless) 章节。

### 5. 源码安装

```bash
git clone https://github.com/a645162/shmtu-auth.git
cd shmtu-auth

# 使用 uv
./setup_uv.sh
uv run python start_cli.py

# 或使用 pip
pip install -r requirements.txt
python -m shmtu_auth
```

## 环境变量配置

运行前需要配置以下环境变量：

```bash
# 必选：学号列表（分号分隔）
export SHMTU_AUTH_USER_LIST="202540510004;202540510005"

# 必选：每个学号对应的密码
export SHMTU_AUTH_USER_PWD_202540510004="password1"
export SHMTU_AUTH_USER_PWD_202540510005="password2"

# 可选：检测间隔（秒，默认 60）
export SHMTU_AUTH_TIME_INTERVAL=60
```

完整配置说明请参考 [环境变量](/config/env-vars) 和 [TOML 配置](/config/toml) 章节。

## 验证安装

```bash
# 检查版本
shmtu-auth --version

# 检查帮助信息
shmtu-auth --help

# 测试配置文件加载
shmtu-auth -t /path/to/config.toml
```
