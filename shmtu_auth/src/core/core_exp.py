from .get_query_string_requests import is_connect_by_google, get_query_string_by_url
from .shmtu_auth_const_value import get_default_query_string


def check_is_connected() -> bool:
    return is_connect_by_google()


def get_query_string() -> str:
    try_str: str = get_query_string_by_url().strip()
    if len(try_str) > 0:
        return try_str
    else:
        return get_default_query_string().strip()
