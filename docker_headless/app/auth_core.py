import json
import logging
from urllib.parse import parse_qs, urlparse

import requests
import urllib3

from app.config import get_env_str

LOGGER = logging.getLogger("shmtu_auth_headless")

# 超时配置（秒）
CONNECT_TIMEOUT = 3  # 连接超时
READ_TIMEOUT = 5     # 读取超时


class ServiceType:
    EDU = "%E6%A0%A1%E5%9B%AD%E7%BD%91"


class HeadlessNetAuth:
    def __init__(self) -> None:
        self.login_api = get_env_str(
            "SHMTU_AUTH_LOGIN_URL",
            "https://ismu.shmtu.edu.cn:8443/eportal/InterFace.do?method=",
        )
        self.probe_url = get_env_str("SHMTU_AUTH_PROBE_URL", "http://1.1.1.1")
        self.info = ""
        self.user_index = ""
        self.is_login = False
        self.data: dict[str, str] = {}
        self.session = requests.Session()  # 复用连接
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": get_env_str(
                "SHMTU_AUTH_USER_AGENT",
                (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/145.0.0.0 Safari/537.36"
                ),
            ),
            "Accept-Encoding": "identify",
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @staticmethod
    def _is_expected_host(final_url: str, expected_hosts: tuple[str, ...]) -> bool:
        host = urlparse((final_url or "").strip()).hostname or ""
        host = host.lower()
        return any(host == expected or host.endswith(f".{expected}") for expected in expected_hosts)

    def _get_text_code(self, url: str) -> tuple[str, int, str]:
        try:
            response = self.session.get(url, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT), verify=False)
            response.encoding = response.apparent_encoding
            return response.text, response.status_code, response.url
        except Exception as exc:
            LOGGER.debug("Probe request failed for %s: %s", url, exc)
            return "", 0, ""

    def is_connected(self) -> bool:
        targets = [
            ("http://www.baidu.com", ("baidu.com",)),
            ("https://www.bilibili.com/", ("bilibili.com",)),
        ]
        for url, expected_hosts in targets:
            _, status_code, final_url = self._get_text_code(url)
            if status_code <= 0:
                continue
            if not self._is_expected_host(final_url, expected_hosts):
                continue
            return True
        return False

    def _extract_query_string_from_url(self, any_url: str) -> str:
        any_url = (any_url or "").strip()
        q_index = any_url.find("?")
        if q_index <= 0:
            return ""
        return any_url[q_index + 1 :].strip()

    def _encode_query_string_for_form(self, query_string: str) -> str:
        query_string = (query_string or "").strip()
        if not query_string:
            return ""
        return query_string.replace("&", "%26").replace("=", "%3D")

    def _extract_meta_refresh_url(self, html: str) -> str:
        import re

        meta_match = re.search(
            r"<meta[^>]*http-equiv\s*=\s*['\"]?refresh['\"]?[^>]*>",
            html or "",
            flags=re.IGNORECASE,
        )
        if not meta_match:
            return ""

        meta_tag = meta_match.group(0)
        content_match = re.search(
            r"content\s*=\s*(['\"])(.*?)\1",
            meta_tag,
            flags=re.IGNORECASE | re.DOTALL,
        )
        content_value = content_match.group(2) if content_match else meta_tag
        url_match = re.search(r"url\s*=\s*([^\s'\"<>]+)", content_value, flags=re.IGNORECASE)
        return url_match.group(1).strip() if url_match else ""

    def get_auth_result(self, skip_connectivity_check: bool = False) -> str:
        """获取认证URL和query string。

        Args:
            skip_connectivity_check: 是否跳过网络连通性检测（外部已检测过时设为True）

        Returns:
            格式: 'portal_url|query_string' 或者空字符串（已在线）
        """
        if not skip_connectivity_check:
            if self.is_connected():
                return ""

        # 优先使用配置的探测URL，失败后再尝试备选
        primary_url = self.probe_url
        fallback_urls = [
            "http://www.msftconnecttest.com/connecttest.txt",
            "http://www.shmtu.edu.cn",
        ]

        final_url = ""
        response_text = ""

        # 先尝试主URL
        response_text, _, final_url = self._get_text_code(primary_url)
        if "hwifi.shmtu.edu.cn" not in final_url and "auth.html" not in final_url and "portalpage" not in final_url:
            # 主URL没找到，尝试备选URL
            for check_url in fallback_urls:
                response_text, _, final_url = self._get_text_code(check_url)
                if "hwifi.shmtu.edu.cn" in final_url or "auth.html" in final_url or "portalpage" in final_url:
                    break

        if not final_url:
            return ""

        if "auth.html" in final_url or "portalpage" in final_url or "hwifi" in final_url:
            query_string = self._extract_query_string_from_url(final_url)
            encoded = self._encode_query_string_for_form(query_string)
            return f"{final_url}|{encoded}"

        try:
            res = self.session.get(self.probe_url, allow_redirects=False, timeout=(CONNECT_TIMEOUT, 3), verify=False)
            if 300 <= res.status_code < 400:
                redirect_location = res.headers.get("Location", "")
                query_string = self._extract_query_string_from_url(redirect_location)
                encoded = self._encode_query_string_for_form(query_string)
                if encoded:
                    return f"{redirect_location}|{encoded}"
        except Exception as exc:
            LOGGER.debug("Redirect probe failed: %s", exc)

        meta_url = self._extract_meta_refresh_url(response_text)
        if meta_url:
            query_string = self._extract_query_string_from_url(meta_url)
            encoded = self._encode_query_string_for_form(query_string)
            if encoded:
                return f"{meta_url}|{encoded}"

        return ""

    @staticmethod
    def _split_auth_result(auth_result: str) -> tuple[str, str]:
        auth_result = (auth_result or "").strip()
        if not auth_result:
            return "", ""

        if "|" in auth_result:
            portal_url, query_string = auth_result.split("|", 1)
            return portal_url.strip(), query_string.strip()

        if "hwifi" in auth_result and "?" in auth_result:
            parsed = urlparse(auth_result)
            encoded_query = parsed.query.replace("&", "%26").replace("=", "%3D")
            return auth_result, encoded_query

        return "", auth_result

    def _confirm_login_success(self, stage: str) -> tuple[bool, str] | None:
        if self.is_connected():
            LOGGER.warning("%s response looked failed, but network is online now", stage)
            self.is_login = True
            return True, f"Login Success ({stage} Confirmed)"
        return None

    def _login_legacy(self, query_string: str) -> tuple[bool, str]:
        query_string = (query_string or "").strip()
        if not query_string:
            return False, "Query string is invalid"

        payload = self.data.copy()
        payload["queryString"] = query_string

        try:
            response = self.session.post(
                self.login_api + "login",
                headers=self.headers,
                data=payload,
                verify=False,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            result = json.loads(response.text)
            self.user_index = result.get("userIndex", "")
            self.info = result.get("message", "")

            if result.get("result") == "success":
                self.is_login = True
                return True, "Login Success (Legacy)"

            confirmed = self._confirm_login_success("Legacy")
            if confirmed is not None:
                return confirmed
            return False, self.info or "Legacy login failed"
        except Exception as exc:
            LOGGER.warning("Legacy login request failed: %s", exc)
            confirmed = self._confirm_login_success("Legacy")
            if confirmed is not None:
                return confirmed
            return False, f"Legacy network error: {exc}"

    def _login_h3c(self, user: str, password: str, portal_url: str = "") -> tuple[bool, str]:
        try:
            entry_url = portal_url.strip() or self.probe_url
            session = requests.Session()

            browser_headers = {
                "User-Agent": self.headers["User-Agent"],
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }
            response = session.get(
                entry_url,
                headers=browser_headers,
                verify=False,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
                allow_redirects=True,
            )

            if "authSuccess" in response.url or "success" in response.url.lower():
                self.is_login = True
                return True, "Login Success (H3C)"

            if "auth.html" not in response.url and "hwifi.shmtu.edu.cn" not in response.url:
                return False, f"Unknown H3C flow: {response.url}"

            parsed = urlparse(response.url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            query = parse_qs(parsed.query)

            post_headers = {
                **browser_headers,
                "X-Requested-With": "XMLHttpRequest",
                "Referer": response.url,
                "Origin": base_url,
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Accept": "application/json, text/javascript, */*; q=0.01",
            }

            xsrf_token = session.cookies.get("XSRF-TOKEN")
            if xsrf_token:
                post_headers["X-XSRF-TOKEN"] = xsrf_token

            payload = {
                "userName": user,
                "userPass": password,
                "pushPageId": query.get("pushPageId", [""])[0],
                "esn": "",
                "apmac": query.get("apmac", [""])[0],
                "armac": "",
                "authType": query.get("authType", ["1"])[0],
                "ssid": query.get("ssid", [""])[0],
                "uaddress": query.get("uaddress", [""])[0],
                "umac": query.get("umac", [""])[0],
                "accessMac": "",
                "businessType": "",
                "acip": "",
                "agreed": "1",
                "registerCode": "",
                "questions": "",
                "dynamicValidCode": "",
                "dynamicRSAToken": "",
                "validCode": "",
            }

            result_response = session.post(
                f"{base_url}/portalauth/login",
                data=payload,
                headers=post_headers,
                verify=False,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
                allow_redirects=False,
            )

            if result_response.status_code == 200:
                try:
                    result = result_response.json()
                    if result.get("success") or result.get("result") == "success":
                        self.is_login = True
                        return True, "Login Success (H3C)"
                    confirmed = self._confirm_login_success("H3C")
                    if confirmed is not None:
                        return confirmed
                    return False, result.get("msg") or result.get("message") or "Unknown H3C error"
                except Exception:
                    confirmed = self._confirm_login_success("H3C")
                    if confirmed is not None:
                        return confirmed
                    return False, "H3C response parse failed"

            if 300 <= result_response.status_code < 400:
                self.is_login = True
                return True, "Login Success (H3C Redirect)"

            confirmed = self._confirm_login_success("H3C")
            if confirmed is not None:
                return confirmed
            return False, f"H3C login failed status={result_response.status_code}"
        except Exception as exc:
            LOGGER.exception("H3C login flow failed: %s", exc)
            confirmed = self._confirm_login_success("H3C")
            if confirmed is not None:
                return confirmed
            return False, "H3C network error"

    def login(self, user: str, password: str, password_encrypt: bool = False, skip_network_check: bool = False) -> tuple[bool, str]:
        """登录校园网。

        Args:
            user: 用户名
            password: 密码
            password_encrypt: 密码是否已加密
            skip_network_check: 是否跳过网络检测（外部已检测过时设为True）

        Returns:
            (是否成功, 消息)
        """
        if not skip_network_check:
            if self.is_connected():
                self.is_login = True
                return True, "Already online"

        if not user or not password:
            return False, "Username or password is empty"

        self.data = {
            "userId": user,
            "password": password,
            "service": ServiceType.EDU,
            "operatorPwd": "",
            "operatorUserId": "",
            "validcode": "",
            "passwordEncrypt": str(password_encrypt),
        }

        auth_result = self.get_auth_result(skip_connectivity_check=skip_network_check).strip()
        portal_url, query_string = self._split_auth_result(auth_result)

        legacy_ok, legacy_msg = self._login_legacy(query_string)
        if legacy_ok:
            return True, legacy_msg

        LOGGER.warning("Legacy login failed, switching to H3C fallback: %s", legacy_msg)

        h3c_ok, h3c_msg = self._login_h3c(user, password, portal_url)
        if h3c_ok:
            return True, h3c_msg

        return False, f"Legacy failed: {legacy_msg}; H3C failed: {h3c_msg}"
