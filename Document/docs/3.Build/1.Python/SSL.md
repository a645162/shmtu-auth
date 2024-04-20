# SSL错误分析报告

本文撰写于`2024年4月20日的凌晨`，凌晨3点半终于解决了问题，特此记录。

如果您的Python以及所有库都使用最新版本，那么你会发现，程序在执行Login操作时会出现SSL错误。

测试URL(校内网):`https://ismu.shmtu.edu.cn:8443/`

## 复现错误

您可以通过下面的命令查看学校的SSL证书

```bash
openssl s_client -connect ismu.shmtu.edu.cn:8443
```

本文撰写于`2024年4月20日的凌晨`，我查看学校的认证服务器的证书，
发现证书的签发日期`2024年3月14日`证书还是比较新的，因此不会是SSL证书过期的问题。

但是当使用Request库执行下面的代码时，会出现SSL错误。

```python
import requests

url = "https://ismu.shmtu.edu.cn:8443/"
response = requests.get(url)
```

查询网上的解决方案均推荐使用下面的代码：

```python
import requests

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "ALL"
```

然而却提示下面的错误

```
cannot import name 'DEFAULT_CIPHERS' from 'urllib3.util.ssl_'
```

## 问题分析

并且只有在Python 3.10以及更高版本会出现，Python 3.9以及更低版本不会出现。

我创建了多个Conda虚拟环境，Python版本从3.8一直到最新的3.12，
发现只有3.10以及更高版本会出现SSL错误。

查询资料得知，Python 3.10以及更高版本的SSL库有了一些变化，
此外Request库到现在(2024年4月20日)，
最近的两次更新分别为`2.31.0 (2023-05-22)`与`2.30.0 (2023-05-03)`，
其中`2.30.0 (2023-05-03)`刚刚添加了`urllib3 2.0`的支持，
因此，可能这其中存在许多不兼容问题。

## 解决方案

### 降低Python版本(最简单)

然而，旧版本Python性能较差，而且不支持新的特性，因此不推荐。

### 降低urllib3的版本

使用`pip`安装`requests`时，可以指定`urllib3`的版本。

```bash
pip install requests "urllib3<2"
```

或者

`requirements.txt`中这样编写:

```
requests
urllib3<2
```

## Reference

https://github.com/JurajNyiri/pytapo/issues/65

https://github.com/psf/requests/issues/6443

https://github.com/psf/requests/blob/main/HISTORY.md#2300-2023-05-03
