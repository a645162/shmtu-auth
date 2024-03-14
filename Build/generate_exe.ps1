# Save Current Loaction
$baseLocation = Get-Location

$project_name= "shmtu_auth"

$srcLocation = "$baseLocation\$project_name"
$outputLocation = "$baseLocation\Build\$project_name"
$tmpLocation = "$outputLocation\tmp"

Set-Location $srcLocation

pyinstaller `
    -F `
    -c `
    -s `
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
