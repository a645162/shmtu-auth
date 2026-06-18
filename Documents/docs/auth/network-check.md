# 网络检测

shmtu-auth 通过 HTTP 探针检测当前网络认证状态。

## 检测原理

程序向公共网站发送 HTTP 请求，通过检查最终跳转 URL 判断是否在线：

1. **已认证** — 请求到达目标网站，URL 为预期域名
2. **未认证** — 请求被重定向到校园网认证门户

### 探测目标

| 探测 URL | 期望域名 | 说明 |
|----------|----------|------|
| `http://www.baidu.com` | `baidu.com` | 百度 |
| `https://www.bilibili.com/` | `bilibili.com` | B 站 |

只有当 HTTP 请求的最终 URL 与期望域名匹配时，才判定为已在线。

## Query String 提取

未认证时，校园网会将 HTTP 请求重定向到认证门户。重定向 URL 中包含 `queryString` 参数，这是登录所需的特征码。

### 提取流程

1. **主探测** — GET `http://1.1.1.1`，检查重定向 URL
2. **备选探测** — 如果主探测未发现认证门户，尝试：
   - `http://www.msftconnecttest.com/connecttest.txt`
   - `http://www.shmtu.edu.cn`
3. **重定向检测** — 检查 3xx 重定向的 `Location` 头
4. **Meta Refresh 检测** — 解析 HTML 中的 `<meta http-equiv="refresh">` 标签

### URL 编码

提取的 `queryString` 在提交给 Legacy eportal 时需要特殊编码：

```
原始: param1=value1&param2=value2
编码: param1%3Dvalue1%26param2%3Dvalue2
```

即 `=` → `%3D`，`&` → `%26`。

## 超时配置

| 参数 | 值 | 说明 |
|------|-----|------|
| 连接超时 | 3 秒 | TCP 连接建立超时 |
| 读取超时 | 5 秒 | 响应数据读取超时 |

## 自定义探测

Headless 版本支持通过环境变量自定义探测行为：

```bash
# 自定义探测 URL
SHMTU_AUTH_PROBE_URL=http://1.1.1.1

# 自定义登录 API
SHMTU_AUTH_LOGIN_URL=https://ismu.shmtu.edu.cn:8443/eportal/InterFace.do?method=

# 自定义 User-Agent
SHMTU_AUTH_USER_AGENT=Mozilla/5.0...
```
