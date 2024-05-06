import sys

print("Checking Python version...")

if sys.version_info > (3, 12):
    print("High Python version detected.")
    print("Please use Python 3.12 or lower.")
    print("Because PySide6 does not support Python 3.13 or higher now.")
    exit(1)

exit(0)
