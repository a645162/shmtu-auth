# TOML配置文件

## 指定配置路径

您可以通过命令行`-t`或者`--toml`参数指定TOML配置文件的路径。

```shell
shmtu-auth.exe -t config.toml
```

## 读取顺序

如果用户配置TOML路径，则**只**会读取用户指定的路径。

**否则：**

如果当前运行目录下存在`config.toml`文件，将会读取该文件作为配置文件。
如果不存在，则会读取`config/config.toml`文件作为配置文件。
