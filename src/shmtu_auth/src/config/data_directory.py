# -*- coding: utf-8 -*-

import os


def get_windows_data_path(project_name=""):
    data_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming")

    project_path = project_name.strip()
    if len(project_path):
        data_path = os.path.join(data_path, project_path)

    os.makedirs(data_path, exist_ok=True)

    return data_path


def get_mac_data_path(project_name=""):
    data_path = os.path.join(os.environ["HOME"], "Library", "Application Support")

    project_path = project_name.strip()
    if len(project_path):
        data_path = os.path.join(data_path, project_path)

    return data_path


def get_linux_data_path(project_name=""):
    data_path = os.path.join(os.environ["HOME"], ".config")

    project_path = project_name.strip()
    if len(project_path):
        data_path = os.path.join(data_path, project_path)

    return data_path


def get_data_path(project_name=""):
    if os.name == "nt":
        return get_windows_data_path(project_name)
    elif os.name == "mac":
        return get_mac_data_path(project_name)
    elif os.name == "posix":
        return get_linux_data_path(project_name)
    else:
        raise Exception("Unsupported OS")


if __name__ == "__main__":
    print(os.name)
    print(get_windows_data_path("shmtu_auth"))
    print(get_mac_data_path("shmtu_auth"))
    print(get_linux_data_path("shmtu_auth"))
