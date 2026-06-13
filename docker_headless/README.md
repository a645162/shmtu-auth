# SHMTU Auth Headless

这个目录是从原项目里拆出来的无 GUI 版本，目标就是在 Docker 里稳定跑认证轮询。

## 特点

- 不依赖 GUI
- 不依赖 `loguru`、`toml`、`PyQt`
- 只保留认证核心逻辑和环境变量配置
- 日志输出到标准输出，适合 Docker 查看

## 环境变量

- `SHMTU_AUTH_USER_LIST`
  - 多个学号用 `;` 分隔
- `SHMTU_AUTH_USER_PWD_<学号>`
  - 对应学号的密码
- `SHMTU_AUTH_CHECK_INTERVAL`
  - 轮询间隔秒数，默认 `60`
- `SHMTU_AUTH_RUN_ONCE`
  - 设为 `1/true/yes/on` 时只执行一次检查
- `SHMTU_AUTH_USER_AGENT`
  - 可选，自定义请求头 UA
- `SHMTU_AUTH_LOGIN_URL`
  - 可选，旧版 eportal 登录接口地址
- `SHMTU_AUTH_PROBE_URL`
  - 可选，默认 `http://1.1.1.1`

## 本地运行

```bash
pip install -r requirements.txt
python -m app.main
```

## Docker

```bash
docker compose up --build -d
docker compose logs -f
```
