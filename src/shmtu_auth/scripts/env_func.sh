# Function to check and load environment variable with a default value
function CheckAndLoadEnvVariable {
    local env_variable_name="$1"
    local default_value="$2"

    # Check if the environment variable exists
    if [[ -z "${!env_variable_name}" ]]; then
        echo "Environment variable '$env_variable_name' not found. Loading it with default value: '$default_value'"

        # Load the environment variable with the default value
        export "$env_variable_name"="$default_value"
    else
        echo "Environment variable '$env_variable_name' exists."
    fi
}
