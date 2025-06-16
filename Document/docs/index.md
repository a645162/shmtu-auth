---
layout: custom
aside: false
outline: false
lastUpdated: false
---

# 上海海事大学校园网自动认证工具

<div align="center">

![Python 3.5+](https://img.shields.io/badge/Python-3.5%2B-brightgreen)
[![License](https://img.shields.io/github/license/a645162/shmtu-auth)](https://github.com/a645162/shmtu-auth/blob/main/LICENSE)
[![Version](https://img.shields.io/github/v/release/a645162/shmtu-auth)](https://github.com/a645162/shmtu-auth/releases)

</div>

一个用于自动认证上海海事大学校园网的工具，可以帮助您自动连接校园网，并实时监控网络状态。

## ✨ 主要特性

- 🔄 **自动认证** - 自动检测网络状态并进行校园网认证
- 📱 **多平台支持** - 支持 Windows、macOS、Linux 和 Docker
- 🎛️ **图形界面** - 提供友好的 GUI 界面（基于 PySide6）
- ⚡ **命令行工具** - 支持命令行模式，适合服务器部署
- 📊 **状态监控** - 实时监控网络连接状态
- 📝 **日志记录** - 详细的日志记录功能
- ⚙️ **配置灵活** - 支持 TOML 配置文件和环境变量

## 🚀 快速开始

### 下载程序

请前往 [GitHub Releases](https://github.com/a645162/shmtu-auth/releases) 下载最新版本的预编译程序。

### Docker 部署

```bash
docker pull registry.cn-shanghai.aliyuncs.com/a645162/shmtu-auth:latest
```

### Python 包安装

```bash
pip install shmtu-auth
```

## 📖 使用指南

- [快速入门指南](./1.Guide/0.Quick%20Start/1.Quick%20Start.md)
- [Windows 平台使用](./1.Guide/1.Windows%20Platform/1.EXE%20Program.md)
- [Linux 平台使用](./1.Guide/3.Linux%20Platform/2.Install%20By%20pip.md)
- [配置说明](./1.Guide/5.Configure/1.TOML%20Config.md)

## 🏗️ 项目架构

该项目基于 Python 开发，主要模块包括：

- **核心认证模块** (`src/core/`) - 处理校园网认证逻辑
- **GUI 界面** (`src/gui/`) - 基于 PySide6 的图形界面
- **监控模块** (`src/monitor/`) - 网络状态监控
- **配置管理** (`src/config/`) - 配置文件和环境变量管理
- **工具模块** (`src/utils/`) - 通用工具函数

## 📄 许可证

本项目采用 [GPL-3.0](https://github.com/a645162/shmtu-auth/blob/main/LICENSE) 许可证开源。
