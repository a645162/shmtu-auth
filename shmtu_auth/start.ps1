# SHMTU Auth on Windows PowerShell

# Load Functions
. ./scripts/env_func.ps1

# Check Env Variables
. ./config/env.ps1

Write-Host "Python path:"
Get-Command python
Write-Host ""

Write-Host "Python version:"
python --version
Write-Host ""

python main.py
