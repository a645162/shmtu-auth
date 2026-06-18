# Docker 完整版镜像

完整版 Docker 镜像包含全部 Python 依赖，支持 loguru 日志和 TOML 配置。

## 快速部署

### Docker Compose

编辑 `Docker/docker-compose.yaml`：

```yaml
services:
  shmtu-auth:
    build:
      context: ..
      dockerfile: Docker/Dockerfile
    image: shmtu-auth:local
    container_name: shmtu-auth
    restart: unless-stopped
    network_mode: host
    tty: true
    volumes:
      - ./logs:/usr/local/shmtu/shmtu-auth/shmtu_auth/logs
    environment:
      - SHMTU_AUTH_USER_LIST=your_student_id
      - SHMTU_AUTH_USER_PWD_your_student_id=your_password
      - SHMTU_AUTH_TIME_INTERVAL=60
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

启动：

```bash
cd Docker
docker compose up --build -d
```

## 日志持久化

完整版支持将日志文件挂载到宿主机：

```yaml
volumes:
  - ./logs:/usr/local/shmtu/shmtu-auth/shmtu_auth/logs
```

## 与 Headless 版本的区别

完整版适合需要以下功能的场景：

- **loguru 文件日志** — 日志自动轮转，持久保存
- **TOML 配置** — 支持通过挂载配置文件管理设置
- **构建信息** — 显示 Docker 构建时间和版本

如果只需要基础认证功能，推荐使用更轻量的 [Headless 版本](/docker/headless)。

## 网络模式

与 Headless 版本相同，必须使用 `network_mode: host`。
