from shmtu_auth.config.github.latest_version import get_branch_version
from shmtu_auth.src.config.build_info import branch, program_version
from shmtu_auth.src.gui.common.config import cfg
from shmtu_auth.src.gui.common.signal_bus import log_new
from shmtu_auth.src.utils.logs import get_logger
from shmtu_auth.src.utils.program_version import ProgramVersion

logger = get_logger()

PROGRAM_VERSION = program_version
GIT_BRANCH = branch

LATEST_VERSION = ""


def get_latest_version() -> str:
    # 从配置中获取用户选择的分支
    selected_branch = cfg.get(cfg.update_branch) if cfg else "main"
    logger.info(f"开始获取版本信息，分支: {selected_branch}")

    try:
        latest_version = get_branch_version(selected_branch)
        logger.info(f"GitHub API返回的版本: '{latest_version}'")
    except Exception as e:
        logger.error(f"调用get_branch_version时发生异常: {e}")
        return ""

    if len(latest_version) == 0:
        logger.warning("获取到的版本字符串为空")
        log_new("Update", "Get Github Version Failed.")
        logger.info("Get Github Version Failed.")
        return ""

    log_new("Update", f"Branch:{selected_branch} Latest Version:{latest_version}")
    logger.info(f"Branch:{selected_branch} Latest Version:{latest_version}")

    global LATEST_VERSION
    LATEST_VERSION = latest_version

    return latest_version


def is_have_new_version() -> bool:
    if LATEST_VERSION == "" or PROGRAM_VERSION == "":
        return False

    latest_version_obj = ProgramVersion.from_str(LATEST_VERSION)
    program_version_obj = ProgramVersion.from_str(PROGRAM_VERSION)

    have_new_version = program_version_obj < latest_version_obj

    if have_new_version:
        log_text = f"Found new version {LATEST_VERSION}(Current:{PROGRAM_VERSION})"
        log_new("Update", log_text)
        logger.info(log_text)

    return have_new_version


def check_update_manually(selected_branch=None) -> dict:
    """
    手动检查更新
    返回更新检查结果的字典
    """
    logger.info("=== 开始手动检查更新 ===")

    result = {
        "success": False,
        "has_update": False,
        "is_ahead": False,
        "current_version": PROGRAM_VERSION,
        "latest_version": "",
        "selected_branch": "",
        "error_message": "",
    }

    logger.info(f"当前版本: {PROGRAM_VERSION}")

    try:
        # 获取当前选择的分支
        logger.info("正在获取配置中的分支设置...")
        if selected_branch is None:
            selected_branch = cfg.get(cfg.update_branch) if cfg else "main"
        result["selected_branch"] = selected_branch
        logger.info(f"选择的分支: {selected_branch}")

        # 直接调用get_branch_version，而不是get_latest_version
        logger.info("正在从GitHub获取最新版本...")
        latest_version = get_branch_version(selected_branch)
        logger.info(f"GitHub API返回的版本: '{latest_version}'")

        if not latest_version:
            error_msg = "无法获取最新版本信息，请检查网络连接"
            result["error_message"] = error_msg
            logger.error(error_msg)
            log_new("Update", f"Manual check failed: {error_msg}")
            return result

        result["latest_version"] = latest_version
        result["success"] = True
        logger.info("成功获取最新版本信息")

        # 检查是否有新版本
        if PROGRAM_VERSION and latest_version:
            logger.info("正在比较版本...")
            try:
                latest_version_obj = ProgramVersion.from_str(latest_version)
                program_version_obj = ProgramVersion.from_str(PROGRAM_VERSION)
                result["has_update"] = program_version_obj < latest_version_obj

                # 检查当前版本是否超前于远端版本
                result["is_ahead"] = program_version_obj > latest_version_obj

                logger.info(
                    f"版本比较结果: 当前版本 {PROGRAM_VERSION} {'<' if result['has_update'] else ('>' if result['is_ahead'] else '=')} 最新版本 {latest_version}"
                )

                if result["has_update"]:
                    log_msg = f"发现新版本: {latest_version} (当前: {PROGRAM_VERSION})"
                    logger.info(log_msg)
                    log_new("Update", log_msg)
                elif result["is_ahead"]:
                    log_msg = f"当前版本超前: {PROGRAM_VERSION} > 远端版本: {latest_version}"
                    logger.info(log_msg)
                    log_new("Update", log_msg)
                else:
                    log_msg = f"已是最新版本: {PROGRAM_VERSION}"
                    logger.info(log_msg)
                    log_new("Update", log_msg)

            except Exception as version_e:
                logger.error(f"版本比较时发生错误: {version_e}")
                result["error_message"] = f"版本比较失败: {str(version_e)}"
                return result
        else:
            logger.warning(f"版本信息不完整 - 当前版本: {PROGRAM_VERSION}, 最新版本: {latest_version}")

        logger.info("=== 手动检查更新完成 ===")
        return result

    except Exception as e:
        error_msg = f"检查更新时发生错误: {str(e)}"
        result["error_message"] = error_msg
        logger.error(f"Manual update check failed: {e}")
        log_new("Update", f"Manual check error: {error_msg}")
        return result


if __name__ == "__main__":
    print(get_latest_version())
    print("Manual check result:", check_update_manually())
