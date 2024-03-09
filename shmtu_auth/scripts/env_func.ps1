# Function to check and load environment variable with a default value
function CheckAndLoadEnvVariable
{
    param (
        [string]$EnvVariableName,
        [string]$DefaultValue
    )

    # Check if the environment variable exists
    if (-not(Test-Path env:\$EnvVariableName))
    {
        Write-Host "Environment variable '$EnvVariableName' not found."
        Write-Host "    Loading it with default value: '$DefaultValue'"

        # Load the environment variable with the default value
        [System.Environment]::SetEnvironmentVariable(
                $EnvVariableName,
                $DefaultValue,
                [System.EnvironmentVariableTarget]::Process
        )
    }
    else
    {
        Write-Host "Environment variable '$EnvVariableName' Found."
    }
}
