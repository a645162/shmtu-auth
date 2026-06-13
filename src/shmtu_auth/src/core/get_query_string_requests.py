from typing import Tuple

import re
from urllib.parse import urlparse

import requests

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()

# 全局 Session 复用连接
_session: requests.Session | None = None

# 超时配置（秒）
CONNECT_TIMEOUT = 3  # 连接超时
READ_TIMEOUT = 5     # 读取超时


def _get_session() -> requests.Session:
    """获取全局 Session，复用连接"""
    global _session
    if _session is None:
        _session = requests.Session()
    return _session


def get_text_code(url: str, timeout: float = READ_TIMEOUT) -> Tuple[str, int, str]:
    # noinspection PyBroadException
    try:
        response = _get_session().get(url, timeout=(CONNECT_TIMEOUT, timeout))
        # 自动识别编码，防止中文乱码
        response.encoding = response.apparent_encoding
        return response.text, response.status_code, response.url
    except Exception as e:
        logger.debug(f"Request Error: {e}")
        return "", 0, ""


def _is_expected_host(final_url: str, expected_hosts: tuple[str, ...]) -> bool:
    host = urlparse((final_url or "").strip()).hostname or ""
    host = host.lower()
    return any(host == expected or host.endswith(f".{expected}") for expected in expected_hosts)


def is_connect_by_sites() -> bool:
    """Use Baidu/Bilibili probe; any one success means connected."""
    logger.info("Starting connectivity probe...")
    targets = [
        ("http://www.baidu.com", ("baidu.com",)),
        ("https://www.bilibili.com/", ("bilibili.com",)),
    ]

    for url, expected_hosts in targets:
        logger.info(f"Probing: {url}")
        _, status_code, final_url = get_text_code(url)
        logger.info(f"Result: status={status_code}, final_url={final_url}")
        if status_code <= 0:
            logger.info(f"Connectivity probe failed: {url}, status={status_code}")
            continue

        if not _is_expected_host(final_url, expected_hosts):
            logger.info(f"Connectivity probe redirected: {url} -> {final_url}")
            continue

        logger.info(f"Connectivity probe success: {url}")
        return True

    logger.info("All connectivity probes failed, network offline.")
    return False


def is_connect_by_google() -> bool:
    """Compatibility wrapper: now uses site-based probe instead of Google 204."""
    return is_connect_by_sites()


def get_query_string_by_url(url: str = "http://1.1.1.1", skip_connectivity_check: bool = False) -> str:
    """获取认证URL和query string。

    Args:
        url: 探测URL，默认 http://1.1.1.1
        skip_connectivity_check: 是否跳过网络连通性检测（外部已检测过时设为True）

    Returns:
        格式: 'portal_url|query_string' 或者空字符串（已在线）
    """
    logger.debug("开始获取 query string...")

    # 只有外部没检测过才检测网络
    if not skip_connectivity_check:
        if is_connect_by_sites():
            logger.debug("网络已连接，无需认证")
            return ""

    # 尝试列表 - 优先使用传入的URL，失败后再尝试备选
    check_urls = [url]
    # 只有第一个失败才尝试备选URL
    fallback_urls = ["http://www.msftconnecttest.com/connecttest.txt", "http://www.shmtu.edu.cn"]
    
    final_url = ""
    res_string = ""

    # 先尝试主URL
    for check_url in check_urls:
        logger.debug(f"尝试访问 {check_url} 获取认证跳转")
        res_string, res_code, final_url = get_text_code(check_url)
        logger.debug(f"URL: {check_url} -> Status: {res_code} -> Final: {final_url}")

        # 如果跳转到了 hwifi 或 auth.html，说明找到了
        if "hwifi.shmtu.edu.cn" in final_url or "auth.html" in final_url or "portalpage" in final_url:
            break

    # 如果主URL没找到，再尝试备选URL
    if not final_url or ("hwifi.shmtu.edu.cn" not in final_url and "auth.html" not in final_url and "portalpage" not in final_url):
        for check_url in fallback_urls:
            logger.debug(f"尝试备选URL: {check_url}")
            res_string, res_code, final_url = get_text_code(check_url)
            logger.debug(f"URL: {check_url} -> Status: {res_code} -> Final: {final_url}")

            if "hwifi.shmtu.edu.cn" in final_url or "auth.html" in final_url or "portalpage" in final_url:
                break
    
    # Check if we got a valid response
    if not final_url:
        logger.error("所有探测URL均未返回有效跳转")
        return ""

    # 检查 Final URL 是否直接即为认证页面
    def _encode_query_string_for_form(qs: str) -> str:
        qs = (qs or "").strip()
        if not qs:
            return ""
        return qs.replace("&", "%26").replace("=", "%3D")

    def _extract_query_string_from_url(any_url: str) -> str:
        any_url = (any_url or "").strip()
        q_index = any_url.find("?")
        if q_index <= 0:
            return ""
        return any_url[q_index + 1 :].strip()

    # 如果最终URL包含了 auth.html 或者看起来像portal页面
    if "auth.html" in final_url or "portalpage" in final_url or "hwifi" in final_url:
         logger.info(f"直接定位到认证页面: {final_url}")
         qs = _extract_query_string_from_url(final_url)
         if qs: 
            qs_encoded = _encode_query_string_for_form(qs)
            return f"{final_url}|{qs_encoded}"
         else:
             # 有可能没有queryString，但是是认证页
             return f"{final_url}|"

    logger.debug(f"响应内容前500字符: {res_string[:500]}")

    def _extract_meta_refresh_url(html: str) -> str:
        html = html or ""
        # 典型格式：<meta http-equiv="refresh" content="1; URL=https://...">
        meta_match = re.search(
            r"<meta[^>]*http-equiv\s*=\s*['\"]?refresh['\"]?[^>]*>",
            html,
            flags=re.IGNORECASE,
        )
        if not meta_match:
            return ""
        meta_tag = meta_match.group(0)
        # 从 content 里提取 url=
        content_match = re.search(
            r"content\s*=\s*(['\"])(.*?)\1",
            meta_tag,
            flags=re.IGNORECASE | re.DOTALL,
        )
        content_value = content_match.group(2) if content_match else meta_tag
        url_match = re.search(r"url\s*=\s*([^\s'\"<>]+)", content_value, flags=re.IGNORECASE)
        return url_match.group(1).strip() if url_match else ""

    # 兼容：若是 302/301 之类重定向（某些网关会这样返回）
    try:
        redirect_location = ""
        # 这里不改 get_text_code 的签名，直接再探测一次 header
        r = _get_session().get(url, allow_redirects=False, timeout=(CONNECT_TIMEOUT, 3))
        if 300 <= r.status_code < 400:
            redirect_location = r.headers.get("Location", "")
        if redirect_location:
            logger.debug(f"检测到 HTTP 重定向 Location: {redirect_location}")
            qs = _extract_query_string_from_url(redirect_location)
            qs = _encode_query_string_for_form(qs)
            if qs:
                logger.info(f"成功获取 query string(redirect): {qs[:100]}...")
                return qs
    except Exception as e:
        logger.debug(f"重定向探测失败(可忽略): {e}")

    # 尝试从 META refresh 标签中提取 URL（大小写不敏感 / 支持单双引号）
    meta_url = _extract_meta_refresh_url(res_string)
    if meta_url:
        logger.debug(f"检测到 META refresh URL: {meta_url}")
        qs = _extract_query_string_from_url(meta_url)
        qs = _encode_query_string_for_form(qs)
        if qs:
            logger.info(f"成功获取认证URL(meta): {meta_url}")
            # 返回格式: 完整URL|编码后的query_string
            return f"{meta_url}|{qs}"
    
    # 尝试旧的解析方式（兼容旧格式）
    list_spilt = res_string.split("'")
    logger.debug(f"分割后的列表长度: {len(list_spilt)}")
    if len(list_spilt) > 1:
        login_page_url = list_spilt[1]
        logger.debug(f"登录页面URL: {login_page_url}")
        list_spilt_url = login_page_url.split("?")
        if len(list_spilt_url) > 1 and list_spilt_url[0].index("index.jsp") > 0:
            query_string = _encode_query_string_for_form(list_spilt_url[1])
            # github上其他学校的锐捷都是下面这样操作的，不清楚以哪个为准。
            # query_string = query_string.replace("&", "%2526").replace("=", "%253D")
            logger.info(f"成功获取 query string: {query_string}")
            return query_string
        else:
            logger.error(f"URL 格式不正确，无法解析 query string")

    logger.error("无法从响应中提取 query string")
    return ""


def get_query_string_by_baidu(url="http://www.baidu.com"):
    return get_query_string_by_url(url)


if __name__ == "__main__":
    print(get_query_string_by_url("http://www.shmtu.edu.cn"))
