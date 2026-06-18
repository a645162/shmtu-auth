# 配置优先级

shmtu-auth 的配置值按以下优先级从高到低解析：

```
全局配置 (config_global.py)  >  TOML 配置文件  >  环境变量
         高 ──────────────────────────────────────── 低
```

## 三层配置源

### 1. 全局配置（最高优先级）

- **来源**：`src/shmtu_auth/src/config/config_global.py`
- **类型**：Python 字典 `env_from_global`
- **用途**：GUI 模式下用户在界面中修改的配置会写入此字典
- **特点**：运行时动态修改，优先级最高

### 2. TOML 配置文件

- **来源**：`config.toml` 或 `config/config.toml`
- **解析器**：`src/shmtu_auth/src/config/config_toml.py`
- **存储**：`env_from_toml` 字典
- **特点**：文件持久化，适合 CLI 模式

### 3. 环境变量（最低优先级）

- **来源**：`os.environ`
- **特点**：Docker 部署的主要配置方式

## 读取逻辑

```python
def get_env_str(key, default=None):
    if key in env_from_global:      # 1. 先查全局配置
        return str(env_from_global[key]).strip()
    if key in env_from_toml:        # 2. 再查 TOML 配置
        return str(env_from_toml[key]).strip()
    if key in os.environ:           # 3. 最后查环境变量
        return str(os.environ[key]).strip()
    return default
```

## 典型场景

| 场景 | 推荐方式 | 原因 |
|------|---------|------|
| Docker 部署 | 环境变量 | 容器无文件系统持久化 |
| CLI 长期运行 | TOML 文件 | 配置持久化，修改后重启生效 |
| GUI 交互使用 | 全局配置 | 界面修改即时生效 |
| CI/CD 流水线 | 环境变量 | 标准化注入方式 |
