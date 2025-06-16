#!/bin/bash

set -e

# 定义应用程序的名称和版本
APP_NAME="shmtu-auth"
APP_VERSION="2.0.0"

app_name="shmtu_auth"
profile_name="macos"
app_name_with_profile="${app_name}_${profile_name}"

current_path="$(pwd)"

# 定义应用程序文件夹的路径
APP_BUNDLE_FOLDER="${current_path}/Output/macOS/${app_name_with_profile}/${app_name_with_profile}.app"

if [ ! -d "${APP_BUNDLE_FOLDER}" ]; then
  echo "Error: Application bundle not found at ${APP_BUNDLE_FOLDER}"
  exit 1
fi

# 定义目标dmg文件的名称
OutputDirectory="${current_path}/Output/macOS"
DMG_FILE="${APP_NAME}-${APP_VERSION}.dmg"
DMG_Path="${OutputDirectory}/${DMG_FILE}"

# 创建一个临时目录
SYSTEM_TEMP_DIR="/tmp"
WORK_DIR="${SYSTEM_TEMP_DIR}/shmtu-auth-temp"
mkdir -p "${WORK_DIR}"

ALL_FILE_DIR="${WORK_DIR}/${APP_NAME}-dmg"
mkdir -p "$ALL_FILE_DIR"

# 复制应用程序文件夹到临时目录
cp -r "${APP_BUNDLE_FOLDER}" "${ALL_FILE_DIR}"
ln -s "/Applications" "${ALL_FILE_DIR}/Applications"

# Rename
mv "${ALL_FILE_DIR}/${app_name_with_profile}.app" "${ALL_FILE_DIR}/${APP_NAME}.app"

# 切换到临时目录
cd "${WORK_DIR}" || exit

# 删除旧的dmg文件
if [ -f "shmtu-auth-temp.dmg" ]; then
  rm -f "shmtu-auth-temp.dmg"
fi

# 创建一个临时dmg文件
hdiutil create \
  -srcdir "${ALL_FILE_DIR}" \
  -volname "$APP_NAME" \
  -format UDZO \
  shmtu-auth-temp.dmg

# 将临时dmg文件移动到目标位置
mv shmtu-auth-temp.dmg "${DMG_Path}"

# Clean up
rm -r "${WORK_DIR}"

# Restore Directory
cd - || exit

echo "DMG file created at: ${DMG_Path}"
