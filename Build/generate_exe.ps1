# Save Current Loaction
$oldLocation = Get-Location

Set-Location .\shmtu_auth\
pyinstaller `
    -F `
    -c `
    -n shmtu_auth `
    .\main_pyinstaller.py

# Restore Location
Set-Location $oldLocation
