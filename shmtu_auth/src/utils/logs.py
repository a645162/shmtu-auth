import os
import loguru

from ..utils.env import get_env_str

logger = loguru.logger

log_directory_path = get_env_str("LOGS_PATH", "./logs")
print("Log:\n" + log_directory_path)
log_file_name = "shmtu_auth_{time}.log"
log_path = os.path.join(log_directory_path, log_file_name)
logger.add(log_path, rotation='00:00', retention='60 days')


def get_logger() -> loguru.logger:
    return logger


if __name__ == "__main__":
    logger.info("SHMTU Auth Monitor")
    logger.info("Test")