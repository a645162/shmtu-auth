# 环境变量

shmtu-auth 通过环境变量进行配置，适合 Docker 部署和 CI 场景。

## 用户认证配置（必需）

### `SHMTU_AUTH_USER_LIST`

学号列表，多个学号之间用 `;` 分隔。

```bash
# Linux/macOS
export SHMTU_AUTH_USER_LIST="202012345;202012346"

# Windows CMD
set SHMTU_AUTH_USER_LIST=202012345;202012346

# Windows PowerShell
$env:SHMTU_AUTH_USER_LIST="202012345;202012346"
```

### `SHMTU_AUTH_USER_PWD_{学号}`

每个学号对应的密码。变量名中的 `{学号}` 替换为实际学号。

```bash
# Linux/macOS
export SHMTU_AUTH_USER_PWD_202012345="your_password_1"
export SHMTU_AUTH_USER_PWD_202012346="your_password_2"

# Windows PowerShell
$env:SHMTU_AUTH_USER_PWD_202012345="your_password_1"
```

### `SHMTU_AUTH_USER_PWD_ENCRYPT_{学号}`

密码是否为密文。设为 `1` 表示密码已加密，不设置表示明文。

```bash
export SHMTU_AUTH_USER_PWD_ENCRYPT_202012345=1
```

## 网络配置

### `SHMTU_AUTH_TIME_INTERVAL`

认证状态检测间隔，单位为秒。默认 `10`（主应用）/ `60`（Headless）。

```bash
export SHMTU_AUTH_TIME_INTERVAL=60
```

### `SHMTU_AUTH_NETWORK_CHECK_RETRY_TIMES`

网络检查的重试次数。默认 `3`。

```bash
export SHMTU_AUTH_NETWORK_CHECK_RETRY_TIMES=5
```

### `SHMTU_AUTH_NETWORK_CHECK_RETRY_TIME_INTERVAL`

网络检查重试的间隔，单位为秒。默认 `30`。

```bash
export SHMTU_AUTH_NETWORK_CHECK_RETRY_TIME_INTERVAL=15
```

### `SHMTU_AUTH_USER_AGENT`

自定义 HTTP 请求的 User-Agent。

```bash
export SHMTU_AUTH_USER_AGENT="Custom-Auth-Client/1.0"
```

## 系统配置

### `SHMTU_MACHINE_NAME`

服务器名称标识，用于日志中区分不同机器。

```bash
export SHMTU_MACHINE_NAME="MyServer"
```

### `DOCKER_MODE`

指示程序运行在 Docker 环境中。Docker 镜像会自动设置此变量。

```bash
export DOCKER_MODE=1
```

## 通知配置

### `SHMTU_AUTH_WEBHOOK_WEWORK`

企业微信机器人 WebHook URL，用于发送认证状态通知。

```bash
export SHMTU_AUTH_WEBHOOK_WEWORK="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_key"
```

### `SHMTU_WEBHOOK_SLEEP_TIME_START` / `SHMTU_WEBHOOK_SLEEP_TIME_END`

WebHook 通知免打扰时间段。格式 `HH:MM`。

```bash
export SHMTU_WEBHOOK_SLEEP_TIME_START="23:00"
export SHMTU_WEBHOOK_SLEEP_TIME_END="7:00"
```

## Headless 专属变量

以下环境变量仅在 Docker Headless 版本中生效：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SHMTU_AUTH_CHECK_INTERVAL` | `60` | 检测间隔（秒），最小 5 |
| `SHMTU_AUTH_RUN_ONCE` | `false` | 仅运行一次，适合 Cron |
| `SHMTU_AUTH_PROBE_URL` | `http://1.1.1.1` | 探测 URL |
| `SHMTU_AUTH_LOGIN_URL` | `ismu.shmtu.edu.cn:8443/...` | 登录 API |
| `SHMTU_AUTH_USER_AGENT` | Chrome UA | HTTP User-Agent |

## Docker Compose 示例

```yaml
environment:
  - SHMTU_AUTH_USER_LIST=202012345;202012346
  - SHMTU_AUTH_USER_PWD_202012345=password1
  - SHMTU_AUTH_USER_PWD_202012346=password2
  - SHMTU_AUTH_TIME_INTERVAL=60
  - SHMTU_MACHINE_NAME=MyServer
```

## 安全注意事项

- 避免在脚本中明文写入密码，优先使用 TOML 配置文件并设置适当权限
- Docker 环境推荐使用 `--env-file` 或 Docker secrets 管理密钥

```bash
# 设置配置文件权限
chmod 600 config.toml

# 使用 env-file
echo "SHMTU_AUTH_USER_PWD_202012345=your_password" > .env
docker run --env-file .env shmtu-auth
```
