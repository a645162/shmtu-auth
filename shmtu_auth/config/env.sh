# ==================================================
# Program Environment
# --------------------------------------------------
# global
CheckAndLoadEnvVariable "SHMTU_AUTH_MACHINE_NAME" ""
CheckAndLoadEnvVariable "WEBHOOK_SLEEP_TIME_START" "23:00"
CheckAndLoadEnvVariable "WEBHOOK_SLEEP_TIME_END" "7:00"
# --------------------------------------------------

# --------------------------------------------------
# AuthTool
CheckAndLoadEnvVariable "SHMTU_AUTH_RETRY" "10"
# --------------------------------------------------

# --------------------------------------------------
# Notify
CheckAndLoadEnvVariable "SHMTU_AUTH_WEBHOOK_WEWORK_DEPLOY" ""
CheckAndLoadEnvVariable "SHMTU_AUTH_WEBHOOK_WEWORK_TEST" ""
CheckAndLoadEnvVariable "SHMTU_AUTH_WEBHOOK_WEWORK" "$SHMTU_AUTH_WEBHOOK_WEWORK_DEPLOY"
CheckAndLoadEnvVariable "SHMTU_AUTH_WEBHOOK_WEWORK_WARNING" "$SHMTU_AUTH_WEBHOOK_WEWORK_TEST"
# --------------------------------------------------

# --------------------------------------------------
# Test
CheckAndLoadEnvVariable "SHMTU_AUTH_USER_LIST" "202300000000"
CheckAndLoadEnvVariable "SHMTU_AUTH_USER_PWD_202300000000" "202300000000"
# --------------------------------------------------
