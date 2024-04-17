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

pip install -r requirements.txt
pip install -r dev-requirements.txt

$project_name = "shmtu_auth"

$srcLocation = "$baseLocation\$project_name"
$outputLocation = "$baseLocation\Build\$project_name"
$tmpLocation = "$outputLocation\tmp"

Set-Location $srcLocation

pyinstaller `
    -F `
    -c `
    -s `
    -i ..\Assets\Icon\logopng.fw.ico `
    -n $project_name `
    --distpath $outputLocation `
    --workpath $tmpLocation `
    .\main_pyinstaller.py

# Remove File "shmtu_auth.spec"
Remove-Item -Recurse -Force "$srcLocation\$project_name.spec"

# Remove Temp Files
Remove-Item -Recurse -Force $tmpLocation

# Restore Location
Set-Location $baseLocation
