import os


def set_py_variable(
        src_text: str,
        var_name: str, var_value: str
) -> str:
    """
    设置py文件中的变量
    :param src_text:
    :param var_name:
    :param var_value:
    :return:
    """

    src_spilt_list = src_text.split("\n")
    target_text = f"{var_name} = "

    found = False

    for i in range(len(src_spilt_list)):
        if target_text in src_spilt_list[i]:
            index = src_spilt_list[i].find(target_text) + len(target_text)
            src_spilt_list[i] = src_spilt_list[i][:index] + var_value
            found = True
            break

    if not found:
        raise Exception("Variable is not found")

    result_text = "\n".join(src_spilt_list)

    return result_text
