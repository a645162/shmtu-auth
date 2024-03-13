from src.monitor import auth_status
from src.utils.logs import get_logger

logger = get_logger()

if __name__ == '__main__':
    # SHMTU Auth
    url = "https://github.com/a645162/shmtu-auth"
    star_len = len(url) + 2

    print("=" * star_len)
    print("SHMTU Auth Monitor")
    print(url)
    print("Author: Haomin Kong")
    print("E-Mail: a645162@gmail.com")
    print("=" * star_len)

    logger.info("Program Start.")

    auth_status.start_monitor_auth()
