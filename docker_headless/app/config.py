import os


def get_env_str(name: str, default: str = "") -> str:
    value = os.environ.get(name)
    if value is None:
        return default
    return str(value).strip()


def get_env_int(name: str, default: int) -> int:
    value = get_env_str(name, "")
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def get_env_bool(name: str, default: bool = False) -> bool:
    value = get_env_str(name, "")
    if not value:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def parse_user_list() -> list[tuple[str, str]]:
    raw_users = get_env_str("SHMTU_AUTH_USER_LIST", "")
    if not raw_users:
        return []

    users: list[tuple[str, str]] = []
    for user_id in raw_users.split(";"):
        user_id = user_id.strip()
        if not user_id:
            continue

        password = get_env_str(f"SHMTU_AUTH_USER_PWD_{user_id}", "")
        if password:
            users.append((user_id, password))

    return users


def mask_user(user_id: str) -> str:
    if len(user_id) == 12:
        return f"{user_id[:4]}*****{user_id[-3:]}"
    return "*" * len(user_id)
