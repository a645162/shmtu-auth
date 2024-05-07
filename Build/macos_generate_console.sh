#!/bin/zsh

# 初始化调试模式为关闭
DebugMode=false

# 获取当前进程ID
CurrentProcessPID=$$
echo "Current process ID: $CurrentProcessPID"

# 获取父进程
parentPID=$(ps -o ppid= -p$CurrentProcessPID)
parentProcessName=$(ps -o comm= -p"$parentPID")

echo "Parent process ID: $parentPID"
echo "Parent process name: $parentProcessName"

# 检查父进程名称中是否包含"PyCharm"，这里一般为zsh
if [[ $parentProcessName == *"PyCharm"* ]]; then
    echo "Running in PyCharm"
    DebugMode=true
fi

# 获取父进程的父进程(祖父进程)
grandparentPID=$(ps -o ppid= -p$parentPID)
grandparentProcessName=$(ps -o comm= -p$grandparentPID)

echo "Grandparent Process ID: $grandparentPID"
echo "Grandparent Process Name: $grandparentProcessName"

# 检查祖父进程名称中是否包含"PyCharm"
if [[ $grandparentProcessName == *"PyCharm"* ]]; then
    echo "Running in PyCharm"
    DebugMode=true
fi

if [[ $DebugMode == true ]]; then
    echo "Debug mode is enabled."
fi
if [[ $DebugMode == false ]]; then
    echo "Debug mode is disabled."
fi

# 获取Python命令的路径
pythonCommandPath=$(which python3)

# 检查Python命令是否存在
if [ -z "$pythonCommandPath" ]; then
    echo "Python command not found."
    exit 1
fi

# 保存路径到变量python_path
python_path=$pythonCommandPath

# 输出Python命令的路径
echo "Python path: $python_path"

# Check if requirements.txt exists
if [[ ! -f "requirements.txt" ]]; then
    # Go to parent directory
    cd ..
fi

# Check again
if [[ ! -f "requirements.txt" ]]; then
    echo "File requirements.txt not found"
    exit 1
fi

# Save current location
base_location=$(pwd)

# Install dependencies
echo "Installing requirements..."

if [[ $DebugMode == true ]]; then
    echo "Debug mode is enabled."
    Write-Host "Passing the requirements installation..."
#    pip install -r requirements.txt
#    pip install -r r-dev-requirements.txt
fi
if [[ $DebugMode == false ]]; then
    echo "Debug mode is disabled."
    pip install -r requirements.txt > /dev/null
    pip install -r r-dev-requirements.txt > /dev/null
fi

# Set project name
project_name="shmtu_auth"
profile_name="macos_console"
project_name_with_profile="${project_name}_${profile_name}"
echo "project_name_with_profile: $project_name_with_profile"

# Set source and output directories
src_location="$base_location/$project_name"
output_location="$base_location/Build/Output/macOS/$project_name_with_profile"
tmp_location="$output_location/tmp"

echo "src_location: $src_location"
echo "output_location: $output_location"
echo "tmp_location: $tmp_location"

# Set location to the source directory
cd "$src_location" || exit

# Build the project with PyInstaller
# https://pyinstaller.org/en/stable/usage.html
pyinstaller \
    --onefile \
    --noconfirm \
    --console \
    --clean \
    --icon "$base_location/Assets/Icon/macOS/Logo.icns" \
    --name "$project_name_with_profile" \
    --distpath "$output_location" \
    --workpath "$tmp_location" \
    ./main_pyinstaller.py

echo "Build Completed"

# Clean up
echo "Cleaning up..."

# Remove the PyInstaller spec file
rm -f "$src_location/$project_name_with_profile.spec"

# Remove temporary files
rm -rf "$tmp_location"

echo "Cleanup Completed"

# Restore Location
echo "Restoring Location..."
cd "$base_location" || exit

echo "Executable is located at $output_location"
echo "Build Completed!!!"
