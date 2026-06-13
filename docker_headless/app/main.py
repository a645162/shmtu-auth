import logging
import time

from app.auth_core import HeadlessNetAuth
from app.config import get_env_bool, get_env_int, mask_user, parse_user_list


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def run_once(auth: HeadlessNetAuth, users: list[tuple[str, str]]) -> bool:
    # 先检测网络状态
    if auth.is_connected():
        logging.info("Network is already online")
        return True

    # 网络离线，尝试登录（跳过内部网络检测，因为已经检测过了）
    for user_id, password in users:
        logging.info("Trying login for user %s", mask_user(user_id))
        ok, message = auth.login(user_id, password, skip_network_check=True)
        if ok:
            logging.info("Login succeeded for user %s: %s", mask_user(user_id), message)
            return True
        logging.warning("Login failed for user %s: %s", mask_user(user_id), message)

    return False


def main() -> int:
    setup_logging()

    users = parse_user_list()
    if not users:
        logging.error("No valid users found in environment variables")
        return 1

    interval = get_env_int("SHMTU_AUTH_CHECK_INTERVAL", 60)
    run_once_only = get_env_bool("SHMTU_AUTH_RUN_ONCE", False)

    logging.info("Loaded %s user(s)", len(users))
    for user_id, _ in users:
        logging.info("Configured user: %s", mask_user(user_id))

    auth = HeadlessNetAuth()

    while True:
        success = run_once(auth, users)
        if run_once_only:
            return 0 if success else 1
        time.sleep(max(interval, 5))


if __name__ == "__main__":
    raise SystemExit(main())
