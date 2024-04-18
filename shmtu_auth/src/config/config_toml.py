import os
import toml

from ..utils.file.infer_encoding import read_file_with_auto_encoding

toml_config: dict = {}


def read_config_toml(toml_path: str = 'config.toml'):
    global toml_config

    if not os.path.exists(toml_path):
        print("TOML Config is not found.")
        return

    try:
        file_content = read_file_with_auto_encoding(toml_path)
        toml_config = toml.load(file_content)
    except Exception as e:
        print(f"An error occurred while reading the TOML file: {e}")


if __name__ == '__main__':
    read_config_toml()
    print()
