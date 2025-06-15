# -*- coding: utf-8 -*-

import os
import datetime

from shmtu_auth.src.config.config_global import env_from_global
from shmtu_auth.src.config.config_toml import env_from_toml


def get_env_str(key, default=None):
    if key in env_from_global:
        return str(env_from_global[key]).strip()

    if key in env_from_toml:
        return str(env_from_toml[key]).strip()

    if key in os.environ:
        return str(os.environ[key]).strip()
    return default


def get_env_int(key, default=None):
    str_int = get_env_str(key, "")
    try:
        return int(str_int)
    except Exception:
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
    except Exception:
        return default
