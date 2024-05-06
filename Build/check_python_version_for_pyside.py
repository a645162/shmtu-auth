import sys

print("Checking Python version...")

if sys.version_info > (3, 11):
    print("Python 3.12 or higher is not supported.")
    exit(1)

exit(0)
