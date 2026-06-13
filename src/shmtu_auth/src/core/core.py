import json
from urllib.parse import parse_qs, urlparse

import requests
from urllib3 import __version__ as urllib3_version

from shmtu_auth.src.core.core_exp import check_is_connected_retry, get_query_string
from shmtu_auth.src.core.shmtu_auth_const_value import ServiceType
from shmtu_auth.src.utils.env import get_env_str
from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()

if urllib3_version.startswith("2."):
    logger.warning(
        "You are using urllib3 version 2.x, which is not fully compatible with this module. "
        "Please use urllib3 version 1.x for better compatibility.",
        stacklevel=2,
    )
    logger.warning(
        'Please run: pip install "urllib3<2"',
        stacklevel=2,
    )

# 超时配置（秒）
CONNECT_TIMEOUT = 3  # 连接超时
READ_TIMEOUT = 5     # 读取超时


class ShmtuNetAuthCore:
    userIndex: str
    info: str
    data: dict
    url: str
    header: dict
    isLogin: bool
    allData: dict
    session: requests.Session

    def __init__(self):
        self.userIndex = ""
        self.info = ""
        self.data = {}
        self.url: str = "https://ismu.shmtu.edu.cn:8443/eportal/InterFace.do?method="
        self.header: dict = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.2.1 Safari/605.1.15",
            "Accept-Encoding": "identify",
        }
        self.isLogin: bool = False
        self.allData: dict = {}
        self.session = requests.Session()  # 复用连接

        env_ua = get_env_str("SHMTU_AUTH_USER_AGENT", "")
        if env_ua != "":
            self.header["User-Agent"] = env_ua
        logger.info("ShmtuNetAuthCore initialization complete!")

    def test_net(self) -> bool:
        """
        测试网络是否认证
        :return: 是否已经认证
        """
        self.isLogin = check_is_connected_retry(retry_times=3, wait_time=5)
        if not self.isLogin:
            logger.info(f"Network Auth Status: {self.isLogin}")
        return self.isLogin

    def test_net_by_ismu(self) -> bool:
        """
        测试网络是否认证(通过ismu的认证界面)
        会有一个问题，就是他系统有bug，可能不跳转！
        :return: 是否已经认证
        """
        import urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # noinspection PyBroadException
        try:
            res = requests.get("http://ismu.shmtu.edu.cn/", headers=self.header, verify=False)
            # print(res.geturl())
            if res.url.find("success.jsp") > 0:
                self.isLogin = True
            else:
                self.isLogin = False
        except Exception:
            self.isLogin = False
        return self.isLogin

    @staticmethod
    def _split_auth_result(auth_result: str) -> tuple[str, str]:
        """Split auth probe result into portal_url and query_string."""
        auth_result = (auth_result or "").strip()
        if not auth_result:
            return "", ""

        if "|" in auth_result:
            portal_url, query_string = auth_result.split("|", 1)
            return portal_url.strip(), query_string.strip()

        # Fallback for full URL returned without "|" separator.
        if "hwifi" in auth_result and "?" in auth_result:
            parsed = urlparse(auth_result)
            encoded_query = parsed.query.replace("&", "%26").replace("=", "%3D")
            return auth_result, encoded_query

        # Legacy format (query string only).
        return "", auth_result

    def _confirm_login_success(self, stage: str) -> tuple[bool, str] | None:
        """Double check actual connectivity when portal responses are ambiguous."""
        try:
            if check_is_connected_retry(retry_times=1, wait_time=0):
                logger.warning(
                    f"{stage} response looked failed, but connectivity is online now; treat as success."
                )
                self.isLogin = True
                return True, f"Login Success ({stage} Confirmed)"
        except Exception as e:
            logger.debug(f"{stage} connectivity confirmation skipped: {e}")
        return None

    def _login_legacy(self, query_string: str) -> tuple[bool, str]:
        """Legacy ISMU/eportal login flow."""
        query_string = (query_string or "").strip()
        if len(query_string) == 0:
            return False, "Query String is Invalid!"

        payload = self.data.copy()
        payload["queryString"] = query_string
        logger.debug("Legacy Query String: " + query_string)

        try:
            res = self.session.post(
                self.url + "login",
                headers=self.header,
                data=payload,
                verify=False,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            login_json = json.loads(res.text)
            self.userIndex = login_json.get("userIndex", "")
            self.info = login_json.get("message", "")
            logger.info(f"Legacy Login: {login_json}")

            if login_json.get("result") == "success":
                return True, "Login Success (Legacy)"
            confirmed = self._confirm_login_success("Legacy")
            if confirmed is not None:
                return confirmed
            return False, self.info or "Legacy login failed"
        except Exception as e:
            logger.warning(f"Legacy Login failed: {e}")
            confirmed = self._confirm_login_success("Legacy")
            if confirmed is not None:
                return confirmed
            return False, f"Legacy Network Error: {e}"

    def _login_h3c(self, user: str, pwd: str, portal_url: str = "") -> tuple[bool, str]:
        """New H3C portal login flow."""
        try:
            entry_url = portal_url.strip()
            if not entry_url:
                entry_url = "http://1.1.1.1"

            logger.info(f"Start H3C fallback login flow, entry: {entry_url}")

            session = requests.Session()
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
                ),
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            }
            res = session.get(
                entry_url,
                headers=headers,
                verify=False,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
                allow_redirects=True,
            )

            if "authSuccess" in res.url or "success" in res.url.lower():
                logger.info(f"Already authenticated in H3C flow: {res.url}")
                return True, "Login Success (H3C)"

            if "auth.html" not in res.url and "hwifi.shmtu.edu.cn" not in res.url:
                logger.error(f"Unknown H3C auth flow URL: {res.url}")
                return False, f"Unknown H3C flow: {res.url}"

            parsed = urlparse(res.url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            qs_params = parse_qs(parsed.query)

            post_headers = headers.copy()
            post_headers.update(
                {
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": res.url,
                    "Origin": base_url,
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                }
            )

            xsrf_token = session.cookies.get("XSRF-TOKEN")
            if xsrf_token:
                post_headers["X-XSRF-TOKEN"] = xsrf_token

            final_auth_data = {
                "userName": user,
                "userPass": pwd,
                "pushPageId": qs_params.get("pushPageId", [""])[0],
                "esn": "",
                "apmac": qs_params.get("apmac", [""])[0],
                "armac": "",
                "authType": qs_params.get("authType", ["1"])[0],
                "ssid": qs_params.get("ssid", [""])[0],
                "uaddress": qs_params.get("uaddress", [""])[0],
                "umac": qs_params.get("umac", [""])[0],
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

            submit_url = f"{base_url}/portalauth/login"
            res2 = session.post(
                submit_url,
                data=final_auth_data,
                headers=post_headers,
                verify=False,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
                allow_redirects=False,
            )

            if res2.status_code == 200:
                try:
                    result = res2.json()
                    logger.info(f"H3C Login Response: {result}")
                    if result.get("success") or result.get("result") == "success":
                        return True, "Login Success (H3C)"
                    confirmed = self._confirm_login_success("H3C")
                    if confirmed is not None:
                        return confirmed
                    error_msg = result.get("msg") or result.get("message") or "Unknown H3C error"
                    return False, error_msg
                except Exception as e:
                    logger.error(f"Failed to parse H3C response: {e}. Body: {res2.text[:200]}")
                    confirmed = self._confirm_login_success("H3C")
                    if confirmed is not None:
                        return confirmed
                    return False, "H3C response parse failed"

            if 300 <= res2.status_code < 400:
                return True, "Login Success (H3C Redirect)"

            confirmed = self._confirm_login_success("H3C")
            if confirmed is not None:
                return confirmed
            return False, f"H3C login failed status={res2.status_code}"
        except Exception as e:
            logger.exception(f"H3C Login Network Error: {e}")
            confirmed = self._confirm_login_success("H3C")
            if confirmed is not None:
                return confirmed
            return False, "H3C Network Error!"

    def login(self, user, pwd, password_encrypt=False, skip_network_check=False) -> (bool, str):
        """
        输入参数登入校园网，自动检测当前网络是否认证。
        :param user:登入id
        :param pwd:登入密码
        :param password_encrypt: 密码是否为密文
        :param skip_network_check: 是否跳过登录前联网探测
        :return:元组第一项：是否认证状态；第二项：详细信息
        """
        import urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if not skip_network_check:
            # 执行登录前再进行一次状态检测
            self.test_net()
            if self.isLogin:
                logger.info("Already Login!")
                return True, "Already Login"

        if user == "" or pwd == "":
            return False, "用户名或密码为空"

        self.data = {
            "userId": user,
            "password": pwd,
            "service": ServiceType.EDU,
            "operatorPwd": "",
            "operatorUserId": "",
            "validcode": "",
            "passwordEncrypt": str(password_encrypt),
        }
        # 如果外部已检测过网络状态，则跳过 get_query_string 内部的网络检测
        auth_result = get_query_string(skip_connectivity_check=skip_network_check).strip()
        portal_url, current_query_string = self._split_auth_result(auth_result)

        # 1) Always try historical logic first.
        legacy_ok, legacy_msg = self._login_legacy(current_query_string)
        if legacy_ok:
            return True, legacy_msg

        logger.warning(f"Legacy login failed, switch to H3C fallback: {legacy_msg}")

        # 2) Fallback to modified logic.
        h3c_ok, h3c_msg = self._login_h3c(user, pwd, portal_url)
        if h3c_ok:
            return True, h3c_msg

        return False, f"Legacy failed: {legacy_msg}; H3C failed: {h3c_msg}"

    def get_all_data(self) -> dict:
        """
        获取当前认证账号全部信息
        #！！！注意！！！#此操作会获得账号alldata['userId']姓名alldata['userName']以及密码alldata['password']
        :return:全部数据的字典格式
        """
        import urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        res = requests.get(self.url + "getOnlineUserInfo", headers=self.header, verify=False)
        try:
            self.allData = json.loads(res.text)
            logger.info(f"Get All Data: {self.allData}")
        except json.decoder.JSONDecodeError as e:
            print("数据解析失败，请稍后重试。")
            logger.exception(f"Data Parse Error: {e}")
            print(e)
        print(self.allData)
        return self.allData

    def logout(self) -> (bool, str):
        """
        登出，操作内会自动获取特征码，海事这个操作没啥用，会自动重连
        :return:元组第一项：是否操作成功；第二项：详细信息
        """
        # if self.alldata == None:
        #     self.get_alldata()

        import urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        res = requests.get(self.url + "logout", headers=self.header, verify=False)
        logout_json = json.loads(res.text)
        self.info = logout_json["message"]
        logger.info(f"Logout: {logout_json}")
        if logout_json["result"] == "success":
            return True, "下线成功"
        else:
            return False, self.info


if __name__ == "__main__":
    net_auth = ShmtuNetAuthCore()
    # print(net_auth.test_net())
    print(net_auth.login("", ""))
