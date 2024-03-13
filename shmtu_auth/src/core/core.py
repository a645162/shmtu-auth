import json

import requests as req

from ..core.core_exp import check_is_connected, get_query_string
from ..core.shmtu_auth_const_value import ServiceType
from ..utils.env import get_env_str

from ..utils.logs import get_logger

logger = get_logger()


class ShmtuNetAuthCore:
    def __init__(self):
        self.data = None
        self.url: str = \
            "https://ismu.shmtu.edu.cn:8443/eportal/InterFace.do?method="
        self.header: dict = {
            "Content-Type":
                "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Version/17.2.1 Safari/605.1.15",
            "Accept-Encoding":
                "identify",
        }
        self.isLogin: bool = False
        self.allData: dict = {}

        env_ua = get_env_str("SHMTU_AUTH_USER_AGENT", "")
        if env_ua != "":
            self.header["User-Agent"] = env_ua
        logger.info("ShmtuNetAuthCore initialization complete!")

    def test_net(self) -> bool:
        """
        测试网络是否认证
        :return: 是否已经认证
        """
        self.isLogin = check_is_connected()
        if not self.isLogin:
            logger.info(f"Network Auth Status: {self.isLogin}")
        return self.isLogin

    def test_net_by_ismu(self) -> bool:
        """
        测试网络是否认证(通过ismu的认证界面)
        会有一个问题，就是他系统有bug，可能不跳转！
        :return: 是否已经认证
        """
        try:
            res = req.get("http://ismu.shmtu.edu.cn/", headers=self.header)
            # print(res.geturl())
            if res.url.find("success.jsp") > 0:
                self.isLogin = True
            else:
                self.isLogin = False
        except Exception:
            self.isLogin = False
        return self.isLogin

    def login(self, user, pwd, password_encrypt=False) -> (bool, str):
        """
        输入参数登入校园网，自动检测当前网络是否认证。
        :param user:登入id
        :param pwd:登入密码
        :param password_encrypt: 密码是否为密文
        :return:元组第一项：是否认证状态；第二项：详细信息
        """
        # if self.isLogin is True:
        self.test_net()
        # self.isLogin = False
        if not self.isLogin:
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
            current_query_string: str = get_query_string().strip()

            try:
                if len(current_query_string) == 0:
                    print("Query String Error!")
                    logger.exception("Query String Error!")
                    return False, "Query String Error!"

                self.data["queryString"] = current_query_string

                res = req.post(
                    self.url + "login",
                    headers=self.header,
                    data=self.data
                )

                # login_json = json.loads(res.read().decode('utf-8'))
                login_json = json.loads(res.text)
                self.userindex = login_json["userIndex"]
                self.info = login_json["message"]
                logger.info(f"Login: {login_json}")
                if login_json["result"] == "success":
                    return True, "认证成功"
                else:
                    return False, self.info
            except Exception as e:
                print(e)
                logger.exception(f"Network Error: {e}")
                return False, "Network Error!"
        return True, "已经在线"

    def get_all_data(self) -> dict:
        """
        获取当前认证账号全部信息
        #！！！注意！！！#此操作会获得账号alldata['userId']姓名alldata['userName']以及密码alldata['password']
        :return:全部数据的字典格式
        """
        res = req.get(
            self.url + "getOnlineUserInfo",
            headers=self.header
        )
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

        res = req.get(self.url + "logout", headers=self.header)
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
