#!/bin/zsh

# 定义应用程序的名称和版本
APP_NAME="shmtu-auth"
APP_VERSION="2.0.0"

current_path=$(pwd)

# 定义应用程序文件夹的路径
APP_FOLDER="/path/to/your/application/folder"

# 定义目标dmg文件的名称
DMG_FILE="$APP_NAME-$APP_VERSION.dmg"

# 创建一个临时目录
TEMP_DIR="/tmp/$APP_NAME-dmg"
mkdir -p "$TEMP_DIR"

# 复制应用程序文件夹到临时目录
cp -r "$APP_FOLDER" "$TEMP_DIR"

# 切换到临时目录
cd "$TEMP_DIR" || exit

# 创建一个临时dmg文件
hdiutil create -srcfolder "$APP_NAME" -volname "$APP_NAME" -format UDZO temp.dmg

# 将临时dmg文件移动到目标位置
mv temp.dmg "$current_path/Output/macOS/$DMG_FILE"

# 清理临时目录
rm -r "$TEMP_DIR"
