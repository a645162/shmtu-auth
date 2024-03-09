import os
import datetime


def get_env_str(key, default=None):
    if key in os.environ:
        return str(os.environ[key]).strip()
    return default


def get_env_int(key, default=None):
    str_int = get_env_str(key, "")
    try:
        return int(str_int)
    except:
        return default


def get_env_time(key, default=None):
    time_str = get_env_str(key, "")
    index = time_str.find(":")
    if index == -1:
        return default

    time_str_1 = time_str[:index].strip()
    time_str_2 = time_str[index + 1 :].strip()

    try:
        int_1 = int(time_str_1)
        int_2 = int(time_str_2)

        return datetime.time(int_1, int_2)
    except:
        return default
