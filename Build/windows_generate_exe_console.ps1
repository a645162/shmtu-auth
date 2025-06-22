# https://pyinstaller.org/en/stable/usage.html

$DebugMode = $false

$parentProcess = (Get-WmiObject -Class Win32_Process -Filter "ProcessId =$PID").ParentProcessId
$parentProcessName = (Get-WmiObject -Class Win32_Process -Filter "ProcessId =$parentProcess").Name
# Check is include "pycharm"
if ($parentProcessName -like "pycharm*.exe") {
    Write-Host "Running in PyCharm"
    $DebugMode = $true
}

if ($DebugMode) {
    Write-Host "Debug mode is enabled."
}
else {
    Write-Host "Debug mode is disabled."
}

# 获取Python命令的路径
$pythonCommandPath = (Get-Command -Name "python" -ErrorAction SilentlyContinue).Path

if (-not $pythonCommandPath) {
    $pythonCommandPath = "C:\Users\konghaomin\miniconda3\envs\shmtu-auth\python.exe"
}

# 检查Python命令是否存在
if (-not $pythonCommandPath) {
    Write-Host "Python command not found."
    exit
}

# 保存路径到变量python_path
$python_path = $pythonCommandPath

# 输出Python命令的路径
Write-Host "Python path: $python_path"

# Check requirements.txt is exist
if (-not (Test-Path "requirements.txt")) {
    # Go to parent directory
    Set-Location ..
}

# Check again
if (-not (Test-Path "requirements.txt")) {
    Write-Host "File requirements.txt not found"
    exit
}

# Save Current Loaction
$baseLocation = Get-Location

Write-Host "Installing requirements..."

if ($DebugMode) {
    Write-Host "Debug mode is enabled."
    Write-Host "Passing the requirements installation..."
}
else {
    Write-Host "Debug mode is disabled."
    # $null = Read-Host "Press Enter to Continue"
    # pip install -r requirements.txt > $null
    # pip install -r r-dev-requirements.txt > $null
    python install.py all
}

$project_name = "shmtu_auth"
$profile_name = "windows_console"
$project_name_with_profile = "$project_name" + "_" + "$profile_name"

$srcLocation = "$baseLocation\src\$project_name"
$pkgLocation = "$srcLocation"
$outputLocation = "$baseLocation\Build\Output\Windows\$project_name_with_profile"
$tmpLocation = "$outputLocation\tmp"

Write-Host "src Location: $srcLocation"
Write-Host "output Location: $outputLocation"
Write-Host "tmp Location: $tmpLocation"

Write-Host "Building the executable..."

Set-Location $baseLocation

pyinstaller `
    --onefile `
    --console `
    --strip `
    --noupx `
    --noconfirm `
    --clean `
    --icon "$baseLocation\Assets\Icon\icons\Icon.ico" `
    --name "$project_name_with_profile" `
    --distpath "$outputLocation" `
    --workpath "$tmpLocation" `
    $pkgLocation\main_pyinstaller.py

Write-Host "Build Completed"

# Clean up
Write-Host "Cleaning up..."

# Remove the PyInstaller spec file
Remove-Item -Recurse -Force "$srcLocation\$project_name_with_profile.spec"

# Remove temporary files
Remove-Item -Recurse -Force $tmpLocation

Write-Host "Cleanup Completed"

# Restore Location
Write-Host "Restoring Location..."
Set-Location $baseLocation

Write-Host "Executable is located at $outputLocation"
Write-Host "Build Completed!!!"
