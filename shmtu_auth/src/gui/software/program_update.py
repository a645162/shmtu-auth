from ...config.build_info import (
    program_version,
    branch
)
from ....config.github.latest_version import get_branch_version
from ..common.signal_bus import log_new

from ...utils.logs import get_logger

logger = get_logger()

PROGRAM_VERSION = program_version
GIT_BRANCH = branch

LATEST_VERSION = ""


def get_latest_version() -> str:
    latest_version = get_branch_version(GIT_BRANCH)

    if len(latest_version) == 0:
        log_new("Update", "Get Github Version Failed.")
        logger.info("Get Github Version Failed.")
        return ""

    log_new("Update", f"Branch:{GIT_BRANCH} Latest Version:{latest_version}")
    logger.info(f"Branch:{GIT_BRANCH} Latest Version:{latest_version}")

    global LATEST_VERSION
    LATEST_VERSION = latest_version

    return latest_version


def is_have_new_version() -> bool:
    if LATEST_VERSION == "":
        get_latest_version()
    if LATEST_VERSION == "" or PROGRAM_VERSION == "":
        return False

    have_new_version = \
        PROGRAM_VERSION != LATEST_VERSION

    if have_new_version:
        log_text = (
            f"Found new version {LATEST_VERSION}"
            f"(Current:{PROGRAM_VERSION})"
        )
        log_new("Update", log_text)
        logger.info(log_text)

    return have_new_version


if __name__ == "__main__":
    print(get_latest_version())
