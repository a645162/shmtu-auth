# https://pyinstaller.org/en/stable/usage.html

# Check requirements.txt is exist
if (-not (Test-Path "requirements.txt"))
{
    # Go to parent directory
    Set-Location ..
}

# Check again
if (-not (Test-Path "requirements.txt"))
{
    Write-Host "File requirements.txt not found"
    exit
}

# Save Current Loaction
$baseLocation = Get-Location

Write-Host "Installing requirements..."

pip install -r requirements.txt > $null
pip install -r r-dev-requirements.txt > $null

$project_name = "shmtu_auth"
$profile_name = "windows_console"
$project_name_with_profile = "$project_name" + "_" + "$profile_name"

$srcLocation = "$baseLocation\$project_name"
$outputLocation = "$baseLocation\Build\$project_name_with_profile"
$tmpLocation = "$outputLocation\tmp"

Write-Host "src Location: $srcLocation"
Write-Host "output Location: $outputLocation"
Write-Host "tmp Location: $tmpLocation"

Write-Host "Building the executable..."

Set-Location $srcLocation

pyinstaller `
    -F `
    -c `
    -s `
    --noupx `
    -i ..\Assets\Icon\icons\Icon.ico `
    -n $project_name_with_profile `
    --distpath $outputLocation `
    --workpath $tmpLocation `
    .\main_pyinstaller.py

# Remove File "shmtu_auth.spec"
Remove-Item -Recurse -Force "$srcLocation\$project_name.spec"

# Remove Temp Files
Remove-Item -Recurse -Force $tmpLocation

# Restore Location
Set-Location $baseLocation
