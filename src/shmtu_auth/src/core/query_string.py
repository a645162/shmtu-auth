# -*- coding: utf-8 -*-

import os.path
from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()

save_path = "./logs/query_string.log"


def save_query_string(query_string: str) -> bool:
    dir_path = os.path.dirname(save_path)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    try:
        with open(save_path, "w") as f:
            f.write(query_string)
    except Exception as e:
        logger.error(f"Failed to save query string to {save_path}!")
        logger.error(f"Error: {e}")
        return False
    return True


def load_query_string_from_file() -> str:
    if not os.path.exists(save_path):
        return ""
    try:
        with open(save_path, "r") as f:
            query_string = f.read().strip()
    except Exception as e:
        logger.error(f"Failed to load query string from {save_path}!")
        logger.error(f"Error: {e}")
        return ""
    return query_string


def handle_query_string(query_string: str) -> str:
    query_string = query_string.strip()
    if len(query_string) > 0:
        return query_string

    query_string = load_query_string_from_file()
    return query_string
