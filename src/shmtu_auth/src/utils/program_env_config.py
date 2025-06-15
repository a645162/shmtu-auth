# -*- coding: utf-8 -*-

from shmtu_auth.src.utils.env import get_env_str


def get_user_num_list():
    user_list = get_env_str("SHMTU_AUTH_USER_LIST", "")
    if user_list == "":
        return []
    else:
        list_ori = user_list.split(";")
        new_list = []
        for item in list_ori:
            item = str(item).strip()
            if len(item) > 0:
                new_list.append(item)
        return new_list


def get_user_pwd(user_num):
    user_pwd = get_env_str("SHMTU_AUTH_USER_PWD_" + user_num, "")
    return user_pwd


def get_user_list():
    user_list = get_user_num_list()
    return_list = []
    for user_num in user_list:
        truly_user_num = user_num.strip()
        pwd = get_user_pwd(truly_user_num)
        if pwd != "":
            is_encrypt = (
                len(get_env_str("SHMTU_AUTH_USER_PWD_ENCRYPT_" + user_num, "")) > 0
            )
            return_list.append((truly_user_num, pwd, is_encrypt))

    return return_list


def convert_number_to_star(number: str) -> str:
    length = len(number)
    if length == 12:
        new_str = number[0:4] + "*****" + number[9:12]
        return new_str
    return "*" * length


def convert_password_to_star(password: str) -> str:
    return "*" * len(password)


if __name__ == "__main__":
    my_variable_value = get_env_str("SHMTU_AUTH_USER_LIST", "")
    print(my_variable_value)
    print(len(my_variable_value))
