# ==================================================
# Program Environment
# --------------------------------------------------
# global
CheckAndLoadEnvVariable "SHMTU_MACHINE_NAME" ""
CheckAndLoadEnvVariable "SHMTU_WEBHOOK_SLEEP_TIME_START" "23:00"
CheckAndLoadEnvVariable "SHMTU_WEBHOOK_SLEEP_TIME_END" "7:00"
# --------------------------------------------------

# --------------------------------------------------
# Auth
CheckAndLoadEnvVariable "SHMTU_AUTH_TIME_INTERVAL" "10"
# --------------------------------------------------

# --------------------------------------------------
# Notify
CheckAndLoadEnvVariable "SHMTU_AUTH_WEBHOOK_WEWORK" ""
# --------------------------------------------------

# --------------------------------------------------
# Test
CheckAndLoadEnvVariable "SHMTU_AUTH_USER_LIST" "202300000000"
CheckAndLoadEnvVariable "SHMTU_AUTH_USER_PWD_202300000000" "202300000000"
# --------------------------------------------------
