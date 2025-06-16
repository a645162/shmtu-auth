import os
import subprocess


def _get_target_directory(repo_url, target_name, base_dir):
    """获取目标目录路径"""
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    if target_name is None:
        target_name = repo_url.split("/")[-1].replace(".git", "")

    return os.path.join(base_dir, target_name), target_name


def _build_clone_command(repo_url, branch, target_dir):
    """构建 git clone 命令"""
    cmd = ["git", "clone"]
    if branch:
        cmd.extend(["-b", branch])
    cmd.extend([repo_url, target_dir])
    return cmd


def _execute_git_clone(cmd, target_name):
    """执行 git clone 命令"""
    try:
        print("正在执行克隆...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        if result.stdout:
            print(f"输出: {result.stdout.strip()}")

        if result.returncode == 0:
            print(f"克隆 {target_name} 成功")
            return True
        else:
            print(f"克隆 {target_name} 失败，返回码: {result.returncode}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"克隆 {target_name} 失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    except FileNotFoundError:
        print("错误: 未找到 git 命令。请确保已安装 Git 并添加到 PATH 环境变量中。")
        return False
    except Exception as e:
        print(f"克隆 {target_name} 时发生未知错误: {e}")
        return False


def clone_repo(repo_url, branch=None, target_name=None, base_dir=None):
    """
    克隆仓库到指定目录

    Args:
        repo_url (str): 仓库 URL
        branch (str, optional): 指定分支. Defaults to None.
        target_name (str, optional): 目标目录名. Defaults to None (使用仓库名).
        base_dir (str, optional): 基础目录. Defaults to None (使用当前脚本目录).

    Returns:
        bool: 是否成功克隆
    """
    # 获取目标目录
    target_dir, actual_target_name = _get_target_directory(repo_url, target_name, base_dir)

    # 检查目录是否已存在
    if os.path.exists(target_dir):
        print(f"目录 {actual_target_name} 已存在，跳过克隆")
        return True

    print(f"正在克隆 {repo_url} 到: {target_dir}")
    if branch:
        print(f"分支: {branch}")

    # 构建并执行克隆命令
    cmd = _build_clone_command(repo_url, branch, target_dir)
    return _execute_git_clone(cmd, actual_target_name)


def clone_repositories():
    """克隆所有需要的仓库"""
    repos = [
        {
            "url": "https://github.com/zhiyiYo/PyQt-Fluent-Widgets.git",
            "branch": "PySide6",
            "name": "PyQt-Fluent-Widgets",
        },
        # 在此处添加更多仓库
        # {
        #     "url": "https://github.com/user/repo.git",
        #     "branch": "main",
        #     "name": "custom-name"
        # },
    ]

    success_count = 0
    total_count = len(repos)

    for repo in repos:
        if clone_repo(repo["url"], repo.get("branch"), repo.get("name")):
            success_count += 1

    print(f"\n克隆完成: {success_count}/{total_count} 个仓库成功")


if __name__ == "__main__":
    clone_repositories()
