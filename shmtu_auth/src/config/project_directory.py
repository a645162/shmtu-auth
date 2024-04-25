import os.path

from .data_directory import get_data_path

project_name = "shmtu_auth"

py_mode = True
gui_mode = False


def get_current_py_path() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def get_pyfile_base_path() -> str:
    current_dir_path = get_current_py_path()

    for _ in range(2):
        current_dir_path = os.path.dirname(current_dir_path)

    return current_dir_path


def get_running_directory() -> str:
    return get_running_directory()


def get_directory_base_path() -> str:
    if gui_mode:
        return get_data_path(project_name)

    if py_mode:
        return get_pyfile_base_path()


def get_directory_config_path():
    base_path = get_directory_base_path()
    return os.path.join(base_path, "config")


def get_directory_log_path():
    base_path = get_directory_base_path()
    return os.path.join(base_path, "log")


if __name__ == '__main__':
    print(get_directory_base_path())
    print(get_directory_config_path())
    print(get_directory_log_path())
