# SHMTU Auth Headless

这个目录是从原项目里拆出来的无 GUI 版本，目标就是在 Docker 里稳定跑认证轮询。

## 特点

- 不依赖 GUI
- 不依赖 `loguru`、`toml`、`PyQt`
- 只保留认证核心逻辑和环境变量配置
- 日志输出到标准输出，适合 Docker 查看
- 镜像体积小 (~35MB)

## 快速开始

### Linux/macOS
```bash
./start.sh start    # 启动
./start.sh stop     # 停止
./start.sh logs     # 查看日志
./start.sh status   # 查看状态
```

### Windows (PowerShell)
```powershell
.\start.ps1 start    # 启动
.\start.ps1 stop     # 停止
.\start.ps1 logs     # 查看日志
.\start.ps1 status   # 查看状态
```

## 环境变量

编辑 `docker-compose.yml` 配置：

```yaml
environment:
  - SHMTU_AUTH_USER_LIST=your_student_id        # 学号（多个用;分隔）
  - SHMTU_AUTH_USER_PWD_your_student_id=your_password  # 密码
  - SHMTU_AUTH_CHECK_INTERVAL=60                # 检测间隔（秒）
```

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SHMTU_AUTH_USER_LIST` | 学号列表，多个用 `;` 分隔 | - |
| `SHMTU_AUTH_USER_PWD_<学号>` | 对应学号的密码 | - |
| `SHMTU_AUTH_CHECK_INTERVAL` | 轮询间隔秒数 | `60` |
| `SHMTU_AUTH_RUN_ONCE` | 只执行一次检查 | `false` |
| `SHMTU_AUTH_PROBE_URL` | 自定义探测URL | `http://1.1.1.1` |
| `SHMTU_AUTH_USER_AGENT` | 自定义UA | - |

## 本地运行（不使用 Docker）

```bash
pip install -r requirements.txt
python -m app.main
```

## Docker 手动操作

```bash
# 构建并启动
docker compose up --build -d

# 查看日志
docker compose logs -f

# 停止
docker compose down

# 重启
docker compose restart
```

## 镜像信息

- 基础镜像: `python:3.12-alpine`
- 构建方式: 多阶段构建
- 镜像大小: ~35MB
