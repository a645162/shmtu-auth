#!/bin/zsh

# https://blog.csdn.net/yc__coder/article/details/107425940
iconset_dir_path="logo.iconset"

rm -rf "$iconset_dir_path"
mkdir "$iconset_dir_path"

sips -z 16 16 logo.png --out $iconset_dir_path/icon_16.png
sips -z 16 16 logo.png --out $iconset_dir_path/icon_16@2x.png

sips -z 32 32 logo.png --out $iconset_dir_path/icon_32.png
sips -z 32 32 logo.png --out $iconset_dir_path/icon_32@2x.png

sips -z 64 64 logo.png --out $iconset_dir_path/icon_64.png
sips -z 64 64 logo.png --out $iconset_dir_path/icon_64@2x.png

sips -z 128 128 logo.png --out $iconset_dir_path/icon_128.png
sips -z 128 128 logo.png --out $iconset_dir_path/icon_128@2x.png

sips -z 256 256 logo.png --out $iconset_dir_path/icon_256.png
sips -z 256 256 logo.png --out $iconset_dir_path/icon_256@2x.png

sips -z 512 512 logo.png --out $iconset_dir_path/icon_512.png
sips -z 512 512 logo.png --out $iconset_dir_path/icon_512@2x.png

iconutil -c icns logo.iconset
