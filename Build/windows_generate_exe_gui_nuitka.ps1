# https://nuitka.net/doc/user-manual.html
# https://doc.qt.io/qtforpython-6/deployment/deployment-pyside6-deploy.html

$DebugMode = $false

$parentProcess = (Get-WmiObject -Class Win32_Process -Filter "ProcessId =$PID").ParentProcessId
$parentProcessName = (Get-WmiObject -Class Win32_Process -Filter "ProcessId =$parentProcess").Name
# Check is include "pycharm"
if ($parentProcessName -like "pycharm*.exe")
{
    Write-Host "Running in PyCharm"
    $DebugMode = $true
}

if ($DebugMode)
{
    Write-Host "Debug mode is enabled."
}
else
{
    Write-Host "Debug mode is disabled."
}

# 获取Python命令的路径
$pythonCommandPath = (Get-Command -Name "python" -ErrorAction SilentlyContinue).Path

# python --version

if (-not $pythonCommandPath)
{
    $pythonCommandPath = "C:\Users\konghaomin\miniconda3\envs\shmtu-auth\python.exe"
}

# 检查Python命令是否存在
if (-not $pythonCommandPath)
{
    Write-Host "Python command not found."
    exit
}

# 保存路径到变量python_path
$python_path = $pythonCommandPath

# 输出Python命令的路径
Write-Host "Python path: $python_path"

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

if ($DebugMode)
{
    Write-Host "Running in Debug Mode"
    Write-Host "Passing the requirements installation..."
}
else
{
    Write-Host "Running in Release Mode"
    # $null = Read-Host "Press Enter to Continue"
    Write-Host "Installing requirements..."
    # pip install -r requirements.txt > $null
    # pip install -r r-dev-requirements.txt > $null
    # pip install -r r-gui-requirements.txt > $null
    python install.py all
    # Install Nuitka if not already installed
    pip install nuitka
}

$project_name = "shmtu_auth"
$profile_name = "windows_gui"
$project_name_with_profile = "$project_name" + "_" + "$profile_name"

$srcLocation = "$baseLocation\src\$project_name"
$outputLocation = "$baseLocation\Build\Output\Windows\$project_name_with_profile"
$tmpLocation = "$outputLocation\tmp"

Write-Host "src Location: $srcLocation"
Write-Host "output Location: $outputLocation"
Write-Host "tmp Location: $tmpLocation"

Write-Host "Building the executable..."

Set-Location $srcLocation

python -m nuitka `
    --standalone `
    --onefile `
    --windows-disable-console `
    --enable-plugin=pyside6 `
    --include-package=PySide6 `
    --include-data-dir=PySide6=PySide6 `
    --windows-icon-from-ico="$baseLocation\Assets\Icon\icons\Icon.ico" `
    --output-filename="$project_name_with_profile.exe" `
    --output-dir="$outputLocation" `
    --remove-output `
    --assume-yes-for-downloads `
    --show-progress `
    --show-memory `
    .\main_gui.py

Write-Host "Build Completed"

# Clean up
Write-Host "Cleaning up..."

# Nuitka creates .build and .dist folders, clean them up
if (Test-Path "$srcLocation\main_gui.build")
{
    Remove-Item -Recurse -Force "$srcLocation\main_gui.build"
}

if (Test-Path "$srcLocation\main_gui.dist")
{
    Remove-Item -Recurse -Force "$srcLocation\main_gui.dist"
}

# Remove any .pyi files created by Nuitka
Get-ChildItem -Path $srcLocation -Filter "*.pyi" | Remove-Item -Force

Write-Host "Cleanup Completed"

# Restore Location
Write-Host "Restored Location"
Set-Location $baseLocation

Write-Host "Executable is located at $outputLocation"
Write-Host "Build Completed!!!"
