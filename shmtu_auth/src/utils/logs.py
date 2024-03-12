from loguru import logger
import datetime, os
from ..utils.env import get_env_str

current_date = datetime.datetime.today()
formatted_date = current_date.strftime("%Y%m%d_%H%M%S")

log_directory_path = get_env_str("LOGS_PATH", "./logs")
log_file_name = f"shmtu_auth_{formatted_date}.log"
log_path = os.path.join(log_directory_path, log_file_name)
logger.add(log_path)
print("Log:\n" + log_path)


def get_current_date_time_str() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


if __name__ == "__main__":
    logger.info("SHMTU Auth Monitor")
    logger.info("Test")
