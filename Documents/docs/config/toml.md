# TOML 配置文件

shmtu-auth 支持通过 TOML 文件进行详细配置，适合需要持久化配置的场景。

## 使用方式

通过 `-t` / `--toml` 参数指定配置文件路径：

```bash
shmtu-auth -t /path/to/config.toml
```

如果不指定路径，程序按以下顺序查找：

1. `./config.toml` — 当前目录
2. `./config/config.toml` — config 子目录

如果都没有找到，程序将使用环境变量和默认值。

## 完整配置示例

```toml
# shmtu-auth 配置文件

[global]
# 机器名称，用于标识当前设备（可选）
SHMTU_MACHINE_NAME = "MyLaptop"

[Network]
# 网络检查重试次数
SHMTU_AUTH_NETWORK_CHECK_RETRY_TIMES = 3
# 网络检查重试间隔（秒）
SHMTU_AUTH_NETWORK_CHECK_RETRY_TIME_INTERVAL = 30

[Auth]
# 认证状态检测间隔（秒）
SHMTU_AUTH_TIME_INTERVAL = 60

[User]
# 用户列表，多个用户用分号分隔
SHMTU_AUTH_USER_LIST = "202012345;202012346"
# 各用户的密码配置
SHMTU_AUTH_USER_PWD_202012345 = "password1"
SHMTU_AUTH_USER_PWD_202012346 = "password2"
# 密码加密标志（可选，1 表示已加密）
SHMTU_AUTH_USER_PWD_ENCRYPT_202012345 = 0
SHMTU_AUTH_USER_PWD_ENCRYPT_202012346 = 0

[Notify]
# 企业微信机器人 WebHook URL（可选）
SHMTU_AUTH_WEBHOOK_WEWORK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key"
# 通知免打扰时间段
SHMTU_WEBHOOK_SLEEP_TIME_START = "23:00"
SHMTU_WEBHOOK_SLEEP_TIME_END = "7:00"

[Advanced]
# 自定义 User-Agent（可选）
SHMTU_AUTH_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
# 调试模式（可选）
SHMTU_AUTH_DEBUG = 0
```

## 配置项说明

### `[global]` 全局配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `SHMTU_MACHINE_NAME` | string | `""` | 机器名称，用于日志标识 |

### `[Network]` 网络配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `SHMTU_AUTH_NETWORK_CHECK_RETRY_TIMES` | integer | `3` | 网络检查重试次数 |
| `SHMTU_AUTH_NETWORK_CHECK_RETRY_TIME_INTERVAL` | integer | `30` | 重试间隔（秒） |

### `[Auth]` 认证配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `SHMTU_AUTH_TIME_INTERVAL` | integer | `60` | 检测间隔（秒） |

### `[User]` 用户配置

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `SHMTU_AUTH_USER_LIST` | string | 学号列表，用分号分隔 |
| `SHMTU_AUTH_USER_PWD_{学号}` | string | 对应学号的密码 |
| `SHMTU_AUTH_USER_PWD_ENCRYPT_{学号}` | integer | 密码是否加密（1=加密，0=明文） |

### `[Notify]` 通知配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `SHMTU_AUTH_WEBHOOK_WEWORK` | string | `""` | 企业微信机器人 WebHook URL |
| `SHMTU_WEBHOOK_SLEEP_TIME_START` | string | `"23:00"` | 免打扰开始时间 |
| `SHMTU_WEBHOOK_SLEEP_TIME_END` | string | `"7:00"` | 免打扰结束时间 |

### `[Advanced]` 高级配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `SHMTU_AUTH_USER_AGENT` | string | 默认浏览器标识 | 自定义 HTTP 请求头 |
| `SHMTU_AUTH_DEBUG` | integer | `0` | 调试模式（1=开启） |

## 场景示例

### 服务器部署

```toml
[global]
SHMTU_MACHINE_NAME = "实验室服务器"

[Auth]
SHMTU_AUTH_TIME_INTERVAL = 30

[User]
SHMTU_AUTH_USER_LIST = "202012345;202012346;202012347"
SHMTU_AUTH_USER_PWD_202012345 = "password1"
SHMTU_AUTH_USER_PWD_202012346 = "password2"
SHMTU_AUTH_USER_PWD_202012347 = "password3"

[Network]
SHMTU_AUTH_NETWORK_CHECK_RETRY_TIMES = 5
SHMTU_AUTH_NETWORK_CHECK_RETRY_TIME_INTERVAL = 15

[Notify]
SHMTU_AUTH_WEBHOOK_WEWORK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=server-key"
```

### Docker 容器

```toml
[global]
SHMTU_MACHINE_NAME = "Docker容器"

[Auth]
SHMTU_AUTH_TIME_INTERVAL = 60

[Network]
SHMTU_AUTH_NETWORK_CHECK_RETRY_TIMES = 6
SHMTU_AUTH_NETWORK_CHECK_RETRY_TIME_INTERVAL = 20
```

## 编码支持

TOML 文件支持自动编码检测，如果文件不是 UTF-8 编码，程序会自动尝试推断正确的编码。

```bash
# 检查文件编码
file -i config.toml

# 转换编码
iconv -f GBK -t UTF-8 config.toml > config_utf8.toml
```

## 安全建议

```bash
# 仅所有者可读写
chmod 600 config.toml
```

详细优先级规则请参考 [配置优先级](/config/priority)。
