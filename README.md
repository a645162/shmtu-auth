# 上海海事大学-校园网-自动认证

## Features

- [x] 自动登录
- [x] 程序记录日志

## Usage

### Docker(Recommended)

[https://hub.docker.com/r/a645162/shmtu-auth](https://hub.docker.com/r/a645162/shmtu-auth)

```bash
docker pull registry.cn-shanghai.aliyuncs.com/a645162/shmtu-auth:latest
```

### Directly Run

#### Windows

```powershell
.\start.ps1
```

#### Linux

```bash
chmod +x start.sh
./start.sh
```

## Environment Variables

学号列表中，学号之间用`;`分隔

- `SHMTU_AUTH_USER_LIST` : {学号1};{学号2}
- `SHMTU_AUTH_USER_PWD_{学号1}` : {学号1的密码}
- `SHMTU_AUTH_USER_PWD_{学号2}` : {学号2的密码}
- `SHMTU_AUTH_USER_PWD_ENCRYPT_{学号1}` : {学号1的密码的是否为密文，密文为1，否则不用填}
- `SHMTU_MACHINE_NAME`: 服务器名称
- `SHMTU_AUTH_TIME_INTERVAL`: 认证状态检测时间间隔
- `SHMTU_AUTH_WEBHOOK_WEWORK`: 企业微信机器人WebHook
- `SHMTU_WEBHOOK_SLEEP_TIME_START`: WebHook免打扰-开始时间
- `SHMTU_WEBHOOK_SLEEP_TIME_END`: WebHook免打扰-结束时间
