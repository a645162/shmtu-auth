# SHMTU Auth on Windows PowerShell

# Load Functions
. ./scripts/env_func.ps1

# Check Env Variables
. ./config/env.ps1

Write-Host "Python path:"
which python

Write-Host "Python version:"
python --version

python main.py
