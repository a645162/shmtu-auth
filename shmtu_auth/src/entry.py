from .monitor import auth_status
from .parse_args import parse_run_args

from .utils.logs import get_logger

logger = get_logger()


def print_info():
    # SHMTU Auth
    url = "https://github.com/a645162/shmtu-auth"
    star_len = len(url) + 3

    print("=" * star_len)
    print("SHMTU Auth Monitor")
    print(url)
    print("Author: Haomin Kong")
    print("E-Mail: a645162@gmail.com")
    print("=" * star_len)


def entry():
    print_info()

    logger.info("Parse args...")

    parse_run_args()

    logger.info("Program Start.")

    auth_status.start_monitor_auth()


if __name__ == "__main__":
    entry()
