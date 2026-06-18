# 双策略登录

shmtu-auth 采用双策略登录机制，确保在不同校园网门户系统下都能成功认证。

## 登录流程

```
开始登录
  │
  ├─ 1. Legacy eportal 登录
  │     POST https://ismu.shmtu.edu.cn:8443/eportal/InterFace.do?method=login
  │     ├─ 成功 → 返回 "Login Success (Legacy)"
  │     └─ 失败 → 继续下一步
  │
  ├─ 2. H3C Portal 登录（Fallback）
  │     GET  http://1.1.1.1 → 获取认证页面
  │     POST https://hwifi.shmtu.edu.cn/portalauth/login
  │     ├─ 成功 → 返回 "Login Success (H3C)"
  │     └─ 失败 → 返回错误信息
  │
  └─ 结束
```

## Legacy eportal 登录

传统 ISMU 认证门户，适用于 `ismu.shmtu.edu.cn` 环境。

**请求格式**：

```
POST https://ismu.shmtu.edu.cn:8443/eportal/InterFace.do?method=login
Content-Type: application/x-www-form-urlencoded

userId={学号}&password={密码}&service=%E6%A0%A1%E5%9B%AD%E7%BD%91&passwordEncrypt=false&queryString={query_string}
```

**关键参数**：

| 参数 | 说明 |
|------|------|
| `userId` | 学号 |
| `password` | 密码（明文或密文） |
| `service` | 服务类型，固定为 `校园网`（URL 编码） |
| `passwordEncrypt` | 密码是否已加密，`true` 或 `false` |
| `queryString` | 认证探针获取的特征码 |

**响应**：

```json
{ "result": "success", "userIndex": "...", "message": "..." }
```

## H3C Portal 登录

H3C Portal 认证，适用于 `hwifi.shmtu.edu.cn` 环境。当 Legacy 登录失败时自动切换。

### 流程

1. **访问认证入口** — GET `http://1.1.1.1`，获取重定向到 `auth.html` 页面
2. **提取参数** — 从重定向 URL 解析 `pushPageId`、`apmac`、`authType`、`ssid`、`uaddress`、`umac`
3. **获取 XSRF Token** — 从 Cookie 中读取 `XSRF-TOKEN`，设置 `X-XSRF-TOKEN` 请求头
4. **提交登录** — POST `{base_url}/portalauth/login`

**请求格式**：

```
POST https://hwifi.shmtu.edu.cn/portalauth/login
Content-Type: application/x-www-form-urlencoded
X-XSRF-TOKEN: {token}

userName={学号}&userPass={密码}&pushPageId=...&apmac=...&authType=1&ssid=...&agreed=1
```

**响应**：

```json
{ "success": true }  // 或 { "result": "success" }
```

### 特殊处理

- **重定向成功**：如果响应状态码为 3xx，视为登录成功（H3C Redirect）
- **已认证页面**：如果 GET 请求到达 `authSuccess` 页面，说明已经在线

## 连通性二次确认

当登录请求的响应结果不明确时（如网络波动），程序会执行连通性二次确认：

1. 向 Baidu / Bilibili 发送 HTTP 请求
2. 检查最终 URL 是否指向预期域名
3. 如果可达，则判定登录成功

这避免了因门户响应异常但实际已认证导致的误判。
