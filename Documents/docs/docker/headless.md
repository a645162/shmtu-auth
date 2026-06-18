# Docker Headless 版本

Headless 版本是专为服务器环境设计的轻量级 Docker 镜像，仅依赖 `requests` 库。

## 与完整版的区别

| 特性 | Headless | 完整版 |
|------|----------|--------|
| Python 依赖 | 仅 requests | requests + loguru + toml + PyYAML |
| 日志 | stdout（标准输出） | loguru 文件日志 |
| 配置方式 | 仅环境变量 | 环境变量 + TOML + GUI |
| 镜像大小 | 更小 | 较大 |
| 适用场景 | 服务器 / Docker | 桌面 / 开发 |

## 快速部署

### Docker Compose（推荐）

编辑 `docker_headless/docker-compose.yml`：

```yaml
services:
  shmtu-auth-headless:
    build:
      context: ..
      dockerfile: docker_headless/Dockerfile
    image: shmtu-auth-headless:local
    container_name: shmtu-auth-headless
    restart: unless-stopped
    network_mode: host
    environment:
      - SHMTU_AUTH_USER_LIST=your_student_id
      - SHMTU_AUTH_USER_PWD_your_student_id=your_password
      - SHMTU_AUTH_CHECK_INTERVAL=60
    deploy:
      resources:
        limits:
          memory: 128M
        reservations:
          memory: 32M
```

启动：

```bash
cd docker_headless
docker compose up --build -d
```

### Docker Hub 镜像

```bash
docker pull a645162/shmtu-auth:latest

# 阿里云 ACR（国内加速）
docker pull registry.cn-shanghai.aliyuncs.com/a645162/shmtu-auth:latest
```

Tag 说明：

| Tag | 说明 |
|-----|------|
| `latest` | 最新稳定版本（main 分支） |
| `vX.Y.Z` | 指定版本（稳定版） |
| `latest-beta` | beta 版本（beta 分支） |

### 单次运行

设置 `SHMTU_AUTH_RUN_ONCE=true`，程序检测一次后退出，适合配合 Cron 使用：

```yaml
environment:
  - SHMTU_AUTH_RUN_ONCE=true
```

## Headless 专属环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SHMTU_AUTH_CHECK_INTERVAL` | `60` | 检测间隔（秒），最小 5 |
| `SHMTU_AUTH_RUN_ONCE` | `false` | 仅运行一次 |
| `SHMTU_AUTH_PROBE_URL` | `http://1.1.1.1` | 探测 URL |
| `SHMTU_AUTH_LOGIN_URL` | `ismu.shmtu.edu.cn:8443/...` | 登录 API |
| `SHMTU_AUTH_USER_AGENT` | Chrome UA | HTTP User-Agent |

完整环境变量列表请参考 [环境变量](/config/env-vars) 章节。

## 资源与日志配置

```yaml
deploy:
  resources:
    limits:
      memory: 128M
    reservations:
      memory: 32M

logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## 网络模式

必须使用 `network_mode: host`，校园网认证需要直接访问本地网络：

```yaml
network_mode: host
```

::: warning
如果使用桥接网络模式，容器内可能无法检测到校园网认证门户的重定向。
:::
