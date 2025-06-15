import os
import re


def read_version_from_init():
    """从 src/shmtu_auth/__init__.py 中读取 __version__ 变量"""
    # 获取当前文件所在目录作为base_dir
    base_dir = os.path.dirname(os.path.abspath(__file__))
    init_file_path = os.path.join(base_dir, "src", "shmtu_auth", "__init__.py")

    try:
        with open(init_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 使用正则表达式匹配 __version__ 变量
        version_pattern = r'__version__\s*=\s*["\']([^"\']+)["\']'
        match = re.search(version_pattern, content)

        if match:
            version = match.group(1)
            return version
        else:
            return None

    except FileNotFoundError:
        return None
    except Exception as e:
        return None


if __name__ == "__main__":
    version = read_version_from_init()
    if version:
        print(version)
    else:
        exit(1)
