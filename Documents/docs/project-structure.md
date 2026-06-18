# 项目结构

```
shmtu-auth/
├── src/shmtu_auth/              # 主应用源码
│   ├── __main__.py              # python -m 入口
│   ├── main_start.py            # pip 安装后的命令行入口 (shmtu-auth)
│   ├── main_gui.py              # GUI 入口
│   ├── version.py               # 版本号
│   ├── config/                  # 构建与版本配置
│   │   ├── github/              # GitHub Release 检测
│   │   ├── generate_env_script.py
│   │   └── end_line.py
│   └── src/
│       ├── entry.py             # CLI 主入口逻辑
│       ├── parse_args.py        # 命令行参数解析
│       ├── core/                # 核心认证逻辑
│       │   ├── core.py          # ShmtuNetAuthCore - 双策略登录
│       │   ├── core_exp.py      # 网络连通性检测 + query string 提取
│       │   ├── get_query_string_requests.py  # HTTP 探测认证门户
│       │   ├── shmtu_auth.py    # ShmtuNetAuth - 多用户迭代封装
│       │   ├── shmtu_auth_const_value.py     # ServiceType 常量
│       │   ├── ismu.py          # ISMU 门户相关
│       │   └── query_string.py  # Query String 工具
│       ├── config/              # 运行时配置
│       │   ├── config_global.py # 全局配置字典
│       │   ├── config_toml.py   # TOML 配置文件解析
│       │   ├── build_info.py    # 构建信息
│       │   ├── data_directory.py
│       │   └── project_directory.py
│       ├── monitor/             # 网络状态监控
│       │   └── auth_status.py   # 后台线程监控循环
│       ├── datatype/            # 数据类型
│       │   └── shmtu/auth/      # AuthUser 等
│       ├── gui/                 # GUI 模块
│       │   ├── gui_main_application.py
│       │   ├── common/          # 通用组件与信号
│       │   ├── feature/         # 功能模块
│       │   ├── view/            # 界面与交互
│       │   ├── task/            # 后台任务
│       │   └── resource/        # Qt 资源
│       ├── system/              # 系统集成
│       │   ├── auto_start.py    # 开机自启
│       │   ├── auto_start_windows.py
│       │   ├── auto_start_macos.py
│       │   └── system_info.py
│       ├── utils/               # 工具函数
│       │   ├── env.py           # 统一环境变量读取
│       │   ├── logs.py          # loguru 日志
│       │   ├── github.py        # GitHub API
│       │   ├── my_time.py
│       │   └── file/            # 文件编码检测
│       └── webhook/             # WebHook 通知
│           └── wework.py        # 企业微信
├── docker_headless/             # Docker Headless 版本
│   ├── app/
│   │   ├── main.py             # Headless 入口
│   │   ├── auth_core.py        # Headless 认证核心
│   │   └── config.py           # 环境变量解析
│   ├── Dockerfile
│   └── docker-compose.yml
├── Docker/                      # Docker 完整版
│   ├── Dockerfile
│   └── docker-compose.yaml
├── Document/                    # 旧版 Web 文档（Vite + TS）
├── Documents/                   # VitePress 文档站点
├── Build/                       # 构建脚本
├── Tools/                       # 开发工具脚本
├── Assets/                      # 静态资源
└── pyproject.toml               # 项目元数据
```

## 两个入口点

| 入口 | 路径 | 说明 | 依赖 |
|------|------|------|------|
| CLI 主应用 | `src/shmtu_auth/src/entry.py` | 完整功能 | requests, loguru, toml, PyYAML, chardet |
| Docker Headless | `docker_headless/app/main.py` | 最小依赖 | 仅 requests |

Headless 版本剥离了 loguru、toml、PyQt 等依赖，日志输出到 stdout，适合 Docker 环境运行。
