# 上海海事大学-校园网-自动认证

## Features

- [x] 自动登录
- [x] IP变动后企业微信通知

## Usage

### Windows

```powershell
.\start.ps1
```

### Linux

```bash
chmod +x start.sh
./start.sh
```

## Environment Variables

学号列表中，学号之间用`;`分隔

- `SHMTU_AUTH_NOTIFY_WEWORK`: 企业微信机器人WebHook
- `SHMTU_AUTH_HOST_NAME`: 服务器名称
- `SHMTU_AUTH_USER_LIST` : {学号1};{学号2}
- `SHMTU_AUTH_USER_PWD_{学号1}` : {学号1的密码}
- `SHMTU_AUTH_USER_PWD_{学号2}` : {学号2的密码}
- `SHMTU_AUTH_USER_PWD_ENCRYPT_{学号1}` : {学号1的密码的是否为密文，密文为1，否则不用填}