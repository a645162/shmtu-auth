import warnings

import requests


def test_ssl():
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # 创建一个日志记录器，用于捕获警告
    with warnings.catch_warnings(record=True) as w:
        # 发起一个未经验证的 HTTPS 请求
        response = requests.get("https://expired.badssl.com/", verify=False)

    assert not w
    assert response.status_code == 200
