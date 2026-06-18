# 安装指南

本文档提供各平台的详细安装说明。

## Windows 平台

### EXE 程序

请前往 [GitHub Release](https://github.com/a645162/shmtu-auth/releases) 下载最新版本的 exe 程序。

### pip 安装

```powershell
pip install shmtu-auth
shmtu-auth
```

### GUI 版本

1. 下载 `shmtu-auth-gui-windows-x64.exe`
2. 双击运行即可，程序会自动启动到系统托盘

**注意**：Windows AMD 显卡用户，程序已全局关闭 Mica 云母特效以避免显示问题。

## macOS 平台

### 二进制程序

请前往 [GitHub Release](https://github.com/a645162/shmtu-auth/releases) 下载。

::: warning
请确认芯片架构（Apple Silicon 或 Intel），下载对应版本！PyInstaller 打包的二进制程序仅支持特定架构。
:::

**macOS x64 (Intel) 限制**：Python 版本必须 ≤ 3.11，否则无法安装 PySide6。

### GUI 版本

1. 下载 `shmtu-auth-gui-macos.dmg`
2. 挂载 DMG 文件并将应用拖拽到 Applications 文件夹
3. 首次运行需要在系统偏好设置中允许该应用

## Linux 平台

### Docker 镜像（推荐）

```bash
docker pull registry.cn-shanghai.aliyuncs.com/a645162/shmtu-auth:latest
```

详见 [Docker 部署](/docker/headless)。

### pip 安装

```bash
pip install shmtu-auth
```

### systemd 服务

适合将 shmtu-auth 作为系统服务在后台运行。

1. 创建服务文件：

```bash
sudo nano /etc/systemd/system/shmtu-auth.service
```

2. 写入以下内容：

```ini
[Unit]
Description=SHMTU Campus Network Auto Auth
After=network.target

[Service]
Type=simple
User=your_user
Environment=SHMTU_AUTH_USER_LIST=your_student_id
Environment=SHMTU_AUTH_USER_PWD_your_student_id=your_password
Environment=SHMTU_AUTH_TIME_INTERVAL=60
ExecStart=/usr/local/bin/shmtu-auth
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. 启用并启动：

```bash
sudo systemctl daemon-reload
sudo systemctl enable shmtu-auth
sudo systemctl start shmtu-auth

# 查看状态
sudo systemctl status shmtu-auth

# 查看日志
sudo journalctl -u shmtu-auth -f
```

### 源码安装

```bash
# 安装依赖（Ubuntu/Debian）
sudo apt-get update
sudo apt-get install python3-pip python3-venv

git clone https://github.com/a645162/shmtu-auth.git
cd shmtu-auth
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m shmtu_auth
```
