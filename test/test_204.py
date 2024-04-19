import pytest
import requests


def test_send_https_request_204():
    url_list = [
        "https://www.google.com/generate_204",
        "https://connect.rom.miui.com/generate_204",
        "https://www.v2ex.com/generate_204",
        "https://captive.v2ex.co/generate_204",
        "https://www.noisyfox.cn/generate_204",
    ]
    for url in url_list:
        make_204_get(url)


def make_204_get(url: str = "https://www.google.com/generate_204"):
    try:
        # 发送GET请求
        print("Test URL:", url)
        response = requests.get(url)
        assert response.status_code == 204
    except requests.RequestException as e:
        # 如果请求过程中发生异常，则测试失败
        pytest.fail(f"Failed to send HTTPS request: {e}")


if __name__ == "__main__":
    test_send_https_request_204()
