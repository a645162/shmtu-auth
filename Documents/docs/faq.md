# 故障排除

## 认证相关问题

### "用户名或密码为空"

**可能原因**：环境变量未设置或 TOML 配置缺少用户配置。

**解决方案**：

```bash
# 检查环境变量
echo $SHMTU_AUTH_USER_LIST
echo $SHMTU_AUTH_USER_PWD_你的学号

# 正确设置
export SHMTU_AUTH_USER_LIST="你的学号"
export SHMTU_AUTH_USER_PWD_你的学号="你的密码"
```

### "Login failed" 认证失败

**可能原因**：用户名或密码错误、账号被锁定、网络连接问题、认证服务器故障。

**解决方案**：

1. 在浏览器中手动访问 `http://ismu.shmtu.edu.cn/` 验证凭据
2. 联系网络中心确认账号状态
3. 测试网络连通性：

```bash
ping ismu.shmtu.edu.cn
curl -I https://ismu.shmtu.edu.cn:8443/
```

### "Query String is Invalid!"

**可能原因**：不在校园网环境中、认证服务器响应异常。

**解决方案**：

```bash
# 检查当前网络状态
curl -I http://www.baidu.com

# 访问校园网页面查看是否跳转到认证页面
curl -L http://ismu.shmtu.edu.cn/
```

## 网络连接问题

### "Network Error!"

**可能原因**：DNS 解析问题、防火墙阻止、代理冲突、SSL 证书问题。

**解决方案**：

```bash
# DNS 检查
nslookup ismu.shmtu.edu.cn
nslookup ismu.shmtu.edu.cn 8.8.8.8

# 检查代理
echo $HTTP_PROXY
echo $HTTPS_PROXY
unset HTTP_PROXY HTTPS_PROXY
```

### 网络检测不准确（频繁误判）

**解决方案**：

```bash
# 增加检测间隔
export SHMTU_AUTH_TIME_INTERVAL=120

# 增加重试次数
export SHMTU_AUTH_NETWORK_CHECK_RETRY_TIMES=5
export SHMTU_AUTH_NETWORK_CHECK_RETRY_TIME_INTERVAL=10
```

## GUI 相关问题

### GUI 无法启动

1. 检查是否安装了 GUI 依赖：`pip install -e ".[gui]"`
2. 查看错误日志文件
3. 尝试命令行启动查看错误信息

**macOS**：首次运行需要在系统偏好设置中允许该应用。

**Linux**：确保有桌面环境，`echo $DISPLAY`。

### 系统托盘图标不显示

1. 检查系统托盘设置
2. 重启程序
3. Linux 下安装系统托盘支持：`sudo apt-get install libappindicator3-1`

## Docker 相关问题

### 容器无法启动

```bash
# 查看容器日志
docker logs shmtu-auth

# 交互式调试
docker run -it --rm \
  -e SHMTU_AUTH_USER_LIST="你的学号" \
  -e SHMTU_AUTH_USER_PWD_你的学号="你的密码" \
  registry.cn-shanghai.aliyuncs.com/a645162/shmtu-auth:latest \
  /bin/bash
```

### 容器内无法访问认证服务器

必须使用主机网络模式：

```bash
docker run -d --name shmtu-auth --network host \
  -e SHMTU_AUTH_USER_LIST="你的学号" \
  -e SHMTU_AUTH_USER_PWD_你的学号="你的密码" \
  registry.cn-shanghai.aliyuncs.com/a645162/shmtu-auth:latest
```

## 配置相关问题

### TOML 配置文件解析失败

```bash
# 验证 TOML 语法
python3 -c "import toml; print(toml.load('config.toml'))"
```

常见格式错误：

```toml
# ❌ 缺少引号
SHMTU_MACHINE_NAME = Machine Name

# ✅ 正确
SHMTU_MACHINE_NAME = "Machine Name"
```

## 性能问题

### CPU 使用率过高

```bash
# 增加检测间隔
export SHMTU_AUTH_TIME_INTERVAL=300
```

### 内存占用过大

```bash
# Docker 资源限制
docker run --memory=128m shmtu-auth
```

## 日志分析

### 常见日志信息

| 日志信息 | 含义 | 处理建议 |
|---------|------|----------|
| `Already Login!` | 网络已认证 | 正常状态 |
| `Login success.` | 认证成功 | 正常状态 |
| `Login failed` | 认证失败 | 检查用户名密码 |
| `Network Auth Status: False` | 网络未认证 | 等待程序自动认证 |
| `Query String is Invalid!` | 认证参数无效 | 检查网络环境 |
| `No user information found.` | 未找到用户配置 | 检查配置 |

### 启用详细日志

```bash
export SHMTU_AUTH_DEBUG=1
```

### 日志文件位置

| 平台 | 路径 |
|------|------|
| Linux/macOS | `~/.shmtu-auth/logs/` |
| Windows | `%USERPROFILE%\.shmtu-auth\logs\` |
| Docker | `/app/logs/` |
