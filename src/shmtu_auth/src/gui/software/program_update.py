from shmtu_auth.config.github.latest_version import get_branch_version
from shmtu_auth.src.config.build_info import branch, program_version
from shmtu_auth.src.gui.common.signal_bus import log_new
from shmtu_auth.src.gui.common.config import cfg
from shmtu_auth.src.utils.logs import get_logger
from shmtu_auth.src.utils.program_version import ProgramVersion

logger = get_logger()

PROGRAM_VERSION = program_version
GIT_BRANCH = branch

LATEST_VERSION = ""


def get_latest_version() -> str:
    # 从配置中获取用户选择的分支
    selected_branch = cfg.get(cfg.update_branch) if cfg else "main"

    latest_version = get_branch_version(selected_branch)

    if len(latest_version) == 0:
        return ""

    if len(latest_version) == 0:
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


if __name__ == "__main__":
    print(get_latest_version())
