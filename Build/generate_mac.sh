#!/bin/zsh

# https://pyinstaller.org/en/stable/usage.html

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
current_location=$(pwd)

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null
pip install -r dev-requirements.txt > /dev/null

# Set project name
project_name="shmtu_auth"

# Set source and output directories
src_location="$current_location/$project_name"
output_location="$current_location/Build/$project_name"
tmp_location="$output_location/tmp"

echo "src_location: $src_location"
echo "output_location: $output_location"
echo "tmp_location: $tmp_location"

# Set location to the source directory
cd "$src_location" || exit

# Build the project with PyInstaller
pyinstaller \
    -F \
    -c \
    -y \
    --console \
    --clean \
    -i "$current_location/Assets/Icon/macOS/Logo.icns" \
    -n "$project_name" \
    --distpath "$output_location" \
    --workpath "$tmp_location" \
    main_pyinstaller.py

## Remove the PyInstaller spec file
rm -rf "$src_location/$project_name.spec"

## Remove temporary files
rm -rf "$tmp_location"

## Restore the original location
#cd "$current_location" || exit
