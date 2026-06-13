from shmtu_auth.src.core.get_query_string_requests import (
    get_query_string_by_url,
    is_connect_by_sites,
)
from shmtu_auth.src.core.query_string import handle_query_string
from shmtu_auth.src.core.shmtu_auth_const_value import get_default_query_string
from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()


def check_is_connected() -> bool:
    return is_connect_by_sites()


def check_is_connected_retry(
    retry_times: int = 3,
    wait_time: int = 5,
) -> bool:
    # Keep signature for compatibility, but do a single fast probe without retry/wait.
    _ = retry_times
    _ = wait_time
    return check_is_connected()


def get_query_string(skip_connectivity_check: bool = False) -> str:
    """获取认证URL和query string。

    Args:
        skip_connectivity_check: 是否跳过网络连通性检测（外部已检测过时设为True）

    Returns:
        格式: 'portal_url|query_string' 或者只返回 query_string(兼容旧逻辑)
    """
    try_str: str = get_query_string_by_url(skip_connectivity_check=skip_connectivity_check).strip()

    try_str = handle_query_string(try_str)

    if len(try_str) > 0:
        return try_str
    else:
        return get_default_query_string().strip()
