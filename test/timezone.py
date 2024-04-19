import datetime
import pytz

now_utc = datetime.datetime.now(pytz.utc)
print("Current Time:", now_utc.strftime("%Y-%m-%d %H:%M:%S"))

beijing_timezone = pytz.timezone('Asia/Shanghai')
beijing_time = now_utc.astimezone(beijing_timezone)

print("Beijing Time:", beijing_time.strftime("%Y-%m-%d %H:%M:%S"))
