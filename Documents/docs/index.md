# shmtu-auth

上海海事大学校园网自动认证工具。自动检测网络认证状态，离线时自动完成登录。

## 功能特性

- ✅ **自动认证** — 检测到网络离线后自动登录校园网
- ✅ **双策略登录** — 优先 Legacy eportal 登录，失败自动切换 H3C Portal 登录
- ✅ **多账号支持** — 支持配置多个学号，逐一尝试直到登录成功
- ✅ **日志记录** — 基于 loguru 的详细日志
- ✅ **全平台运行** — Windows / macOS / Linux CLI，Docker 镜像，GUI（Windows/macOS）
- ✅ **灵活配置** — 支持环境变量、TOML 配置文件、GUI 配置三种方式

## 支持平台

| 平台 | 方式 | 说明 |
|------|------|------|
| Windows | CLI (exe / pip) | 命令行运行 |
| Windows | GUI | PySide6 桌面界面 |
| macOS | CLI (二进制 / pip) | 命令行运行 |
| macOS | GUI | PySide6 桌面界面 |
| Linux | CLI (pip) | 命令行运行 |
| 任意 | Docker | 服务器部署推荐 |

## 快速开始

```bash
# 使用 uv 安装并运行（推荐）
./setup_uv.sh          # Linux/macOS
.\setup_uv.ps1         # Windows
uv run python start_cli.py

# 或使用 pip
pip install -r requirements.txt
python -m shmtu_auth
```

前往 [快速开始](/getting-started) 了解更多安装方式。
