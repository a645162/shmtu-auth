# ==================================================
# Program Environment
# --------------------------------------------------
# global
$env:SHMTU_AUTH_MACHINE_NAME = ""
$env:WEBHOOK_SLEEP_TIME_START = "23:00"
$env:WEBHOOK_SLEEP_TIME_END = "7:00"
# --------------------------------------------------

# --------------------------------------------------
# AuthTool
$env:SHMTU_AUTH_RETRY = "10"
# --------------------------------------------------

# --------------------------------------------------
# Notify
$env:SHMTU_AUTH_WEBHOOK_WEWORK_DEPLOY = ""
$env:SHMTU_AUTH_WEBHOOK_WEWORK_TEST = ""
$env:SHMTU_AUTH_WEBHOOK_WEWORK = "$SHMTU_AUTH_WEBHOOK_WEWORK_DEPLOY"
$env:SHMTU_AUTH_WEBHOOK_WEWORK_WARNING = "$SHMTU_AUTH_WEBHOOK_WEWORK_TEST"
# --------------------------------------------------

