# 核心 API

shmtu-auth 的核心认证逻辑封装在以下类中。

## ShmtuNetAuthCore

核心认证类，提供基础的网络认证功能。

**源码位置**：`src/shmtu_auth/src/core/core.py`

### 初始化

```python
from shmtu_auth.src.core.core import ShmtuNetAuthCore

auth_core = ShmtuNetAuthCore()
```

### test_net() -> bool

测试网络是否已经通过认证。

```python
is_online = auth_core.test_net()
# True: 已认证  False: 未认证
```

### login(user, pwd, password_encrypt=False, skip_network_check=False) -> tuple[bool, str]

执行校园网登录认证，采用双策略（Legacy + H3C）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `user` | str | 学号 |
| `pwd` | str | 密码 |
| `password_encrypt` | bool | 密码是否已加密，默认 `False` |
| `skip_network_check` | bool | 是否跳过登录前网络探测，默认 `False` |

**返回值**：`(是否成功, 详细信息)`

```python
success, message = auth_core.login("your_student_id", "your_password")
# success=True  → message: "Login Success (Legacy)" 或 "Login Success (H3C)"
# success=False → message: 错误描述
```

### logout() -> tuple[bool, str]

执行校园网登出操作。

### get_all_data() -> dict

获取当前认证账号的全部信息。

::: danger
此操作会获取敏感信息（包括用户名和密码），请谨慎使用。
:::

## ShmtuNetAuth

高级认证类，继承自 `ShmtuNetAuthCore`，提供多用户迭代功能。

**源码位置**：`src/shmtu_auth/src/core/shmtu_auth.py`

### login_by_list(user_list) -> bool

使用用户列表进行批量登录尝试，直到有一个成功。

```python
from shmtu_auth.src.core.shmtu_auth import ShmtuNetAuth

auth = ShmtuNetAuth()
user_list = [
    ["student_id_1", "password_1", False],
    ["student_id_2", "password_2", False]
]

if auth.login_by_list(user_list):
    print("至少一个用户登录成功")
```

### check_is_online() -> bool

检查当前网络是否在线（已认证）。

## HeadlessNetAuth

Docker Headless 版本的认证类，最小化依赖。

**源码位置**：`docker_headless/app/auth_core.py`

### login(user, password, ...) -> tuple[bool, str]

与 `ShmtuNetAuthCore.login()` 接口一致，但内部实现更轻量。

### is_connected() -> bool

检测网络是否已认证（通过 Baidu / Bilibili 探针）。

## 监控模块

### start_monitor_auth()

启动后台监控线程，周期性检测网络状态并自动登录。

```python
from shmtu_auth.src.monitor.auth_status import start_monitor_auth
start_monitor_auth()
```

## 配置读取

### get_env_str(key, default=None) -> str

统一配置读取，按优先级：全局配置 > TOML > 环境变量。

```python
from shmtu_auth.src.utils.env import get_env_str
value = get_env_str("SHMTU_AUTH_TIME_INTERVAL", "60")
```

## 完整使用示例

```python
from shmtu_auth.src.core.shmtu_auth import ShmtuNetAuth
from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()
auth = ShmtuNetAuth()

if auth.check_is_online():
    logger.info("网络已连接")
else:
    success, message = auth.login("your_student_id", "your_password")
    if success:
        logger.info(f"登录成功: {message}")
    else:
        logger.error(f"登录失败: {message}")
```
