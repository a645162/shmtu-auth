from loguru import logger
import datetime

current_date = datetime.datetime.today()
formatted_date = current_date.strftime("%Y%m%d")

logger.add(f"shmtu_auth_{formatted_date}.log")
