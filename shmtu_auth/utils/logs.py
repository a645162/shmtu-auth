from loguru import logger
import datetime, os

current_date = datetime.datetime.today()
formatted_date = current_date.strftime("%Y%m%d")

log_directory_path = ""
log_file_name = f"shmtu_auth_{formatted_date}.log"
log_path = os.path.join(log_directory_path, log_file_name)
logger.add(log_path)
print("Try to log to " + log_path)
