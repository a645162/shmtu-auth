# Run other scripts to build
Write-Host "Building the executable..."
. .\Build\generate_exe_console.ps1

# Run the executable
Write-Host "Running the executable..."
. Build\shmtu_auth\shmtu_auth.exe
