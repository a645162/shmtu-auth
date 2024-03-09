import yaml


def read_yaml(file_path: str = 'env_list.yaml') -> dict:
    try:
        with open(file_path, 'r') as file:
            data_dict = yaml.safe_load(file)
    except:
        data_dict = {}
        print('读取文件失败，使用空字典代替')

    return data_dict


def get_dict_depth(dictionary, current_depth=1) -> int:
    """获取字典的深度"""
    if not isinstance(dictionary, dict) or not dictionary:
        return 0

    # 遍历字典中的所有值，如果值是字典，则递归计算深度
    nested_depths = [
        get_dict_depth(value, current_depth + 1)
        for value in dictionary.values()
    ]

    # 返回当前深度和所有嵌套深度中的最大值
    return max(current_depth, *nested_depths)


def generate_env_script(data_dict: dict, default_mode: bool = True) -> (str, str):
    # 获取字典深度
    dict_depth = get_dict_depth(data_dict)
    script_sh = ''
    script_pwsh = ''
    if dict_depth == 1:
        # 深度为 1 的字典，直接生成脚本
        for key, value in data_dict.items():
            value = str(value).strip()
            if default_mode:
                script_sh += f'export {key}="{value}"\n'
                script_pwsh += f'$env:{key} = "{value}"\n'
            else:
                script_sh += f'CheckAndLoadEnvVariable "{key}" "{value}"\n'
                script_pwsh += (
                    f'CheckAndLoadEnvVariable `\n'
                    f'\t-EnvVariableName "{key}" `\n'
                    f'\t-DefaultValue "{value}"\n'
                )
    else:
        # 深度大于 1 的字典，递归生成脚本
        for key, value in data_dict.items():
            str_spilt_line = "# " + "-" * 50

            script_sh += str_spilt_line + "\n"
            script_pwsh += str_spilt_line + "\n"
            script_sh += f'# {key}\n'
            script_pwsh += f'# {key}\n'

            if isinstance(value, dict):
                child_dict: dict = value

                child_script_sh, child_script_pwsh = \
                    generate_env_script(child_dict, default_mode)

                child_script_sh, child_script_pwsh = \
                    str(child_script_sh).strip(), str(child_script_pwsh).strip()

                script_sh += child_script_sh
                script_pwsh += child_script_pwsh

                script_sh += "\n"
                script_pwsh += "\n"

            script_sh += str_spilt_line
            script_pwsh += str_spilt_line

            script_sh += "\n\n"
            script_pwsh += "\n\n"

    return script_sh, script_pwsh


def save_env_script(
        dict_data: dict,
        sh_path: str = 'default_env.sh',
        pwsh_path: str = 'default_env.ps1',
        default_mode: bool = True
):
    str_public_comment = """
    # Program Environment
    """.strip() + "\n"

    str_public_comment = "# " + "=" * 50 + "\n" + str_public_comment

    sh_path = sh_path.strip()
    pwsh_path = pwsh_path.strip()

    script_sh, script_pwsh = generate_env_script(dict_data, default_mode)

    script_sh = f"{str_public_comment}{script_sh}"
    script_pwsh = f"{str_public_comment}{script_pwsh}"

    with open(sh_path, 'w') as file:
        file.write(script_sh)
    print(f"Write sh to {sh_path}")

    with open(pwsh_path, 'w') as file:
        file.write(script_pwsh)
    print(f"Write pwsh to {pwsh_path}")


if __name__ == '__main__':
    yaml_data: dict = read_yaml()

    # 打印解析后的字典
    print(yaml_data)

    # 获取字典深度
    depth = get_dict_depth(yaml_data)

    # 打印深度
    print(f"The depth of the dictionary is: {depth}")

    save_env_script(yaml_data)
    save_env_script(
        yaml_data,
        sh_path='env.sh',
        pwsh_path='env.ps1',
        default_mode=False
    )
