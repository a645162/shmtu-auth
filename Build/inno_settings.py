# Modify Inno Variables
def modify_inno_variables(src: str, variables: dict) -> str:
    spilt_list = src.split("\n")
    for i in range(len(spilt_list)):
        for key in variables.keys():
            if key in spilt_list[i]:
                spilt_list[i] = f"{key}={variables[key]}"

    return "\n".join(spilt_list)


if __name__ == '__main__':
    # Modify Inno Variables
    src = ""
