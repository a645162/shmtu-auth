# ==================================================
# Program Environment
# --------------------------------------------------
# global
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_AUTH_MACHINE_NAME" `
	-DefaultValue ""
CheckAndLoadEnvVariable `
	-EnvVariableName "WEBHOOK_SLEEP_TIME_START" `
	-DefaultValue "23:00"
CheckAndLoadEnvVariable `
	-EnvVariableName "WEBHOOK_SLEEP_TIME_END" `
	-DefaultValue "7:00"
# --------------------------------------------------

# --------------------------------------------------
# AuthTool
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_AUTH_RETRY" `
	-DefaultValue "10"
# --------------------------------------------------

# --------------------------------------------------
# Notify
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_AUTH_WEBHOOK_WEWORK_DEPLOY" `
	-DefaultValue ""
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_AUTH_WEBHOOK_WEWORK_TEST" `
	-DefaultValue ""
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_AUTH_WEBHOOK_WEWORK" `
	-DefaultValue "$SHMTU_AUTH_WEBHOOK_WEWORK_DEPLOY"
CheckAndLoadEnvVariable `
	-EnvVariableName "SHMTU_AUTH_WEBHOOK_WEWORK_WARNING" `
	-DefaultValue "$SHMTU_AUTH_WEBHOOK_WEWORK_TEST"
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

