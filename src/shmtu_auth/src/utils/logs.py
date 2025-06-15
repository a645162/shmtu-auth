# -*- coding: utf-8 -*-

import os.path
import loguru

from shmtu_auth.src.config.project_directory import get_directory_log_path

logger = loguru.logger

# log_directory_path = get_env_str("LOGS_PATH", "./logs")
log_directory_path = get_directory_log_path()

# Convert to an absolute path
# log_directory_path = os.path.abspath(log_directory_path)

print("Log:\n" + log_directory_path)
log_file_name = "shmtu_auth_{time}.log"
log_path = os.path.join(log_directory_path, log_file_name)
logger.add(log_path, rotation="00:00", retention="60 days")


def get_logger() -> loguru.logger:
    return logger


if __name__ == "__main__":
    logger.info("SHMTU Auth Monitor")
    logger.info("Test")
