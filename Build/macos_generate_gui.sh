#!/bin/zsh

set -e

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
echo "Base location: $base_location"

echo "Build Completed!!!"
