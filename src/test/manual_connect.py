# https://ismu.shmtu.edu.cn:8443/eportal/index.jsp
# https://user.ismu.shmtu.edu.cn:8443/selfservice/

from shmtu_auth.src.core.shmtu_auth import ShmtuNetAuthCore


def main():
    net_auth = ShmtuNetAuthCore()
    # print(net_auth.test_net())
    print(net_auth.login("", ""))


if __name__ == "__main__":
    main()
