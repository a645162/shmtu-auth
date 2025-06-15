# ==================================================
# Program Environment
# --------------------------------------------------
# global
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_MACHINE_NAME" `
	-DefaultValue ""
# --------------------------------------------------

# --------------------------------------------------
# Network
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_AUTH_NETWORK_CHECK_RETRY_TIMES" `
	-DefaultValue "3"
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_AUTH_NETWORK_CHECK_RETRY_TIME_INTERVAL" `
	-DefaultValue "30"
# --------------------------------------------------

# --------------------------------------------------
# Auth
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_AUTH_TIME_INTERVAL" `
	-DefaultValue "10"
# --------------------------------------------------

# --------------------------------------------------
# Notify
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_AUTH_WEBHOOK_WEWORK" `
	-DefaultValue ""
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_WEBHOOK_SLEEP_TIME_START" `
	-DefaultValue "23:00"
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_WEBHOOK_SLEEP_TIME_END" `
	-DefaultValue "7:00"
# --------------------------------------------------

# --------------------------------------------------
# Test
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_AUTH_USER_LIST" `
	-DefaultValue "202300000000"
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_AUTH_USER_PWD_202300000000" `
	-DefaultValue "202300000000"
# --------------------------------------------------
