# -*- coding: utf-8 -*-

import os
import sys

# Ensure the src directory is in the Python path
current_py_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_py_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from shmtu_auth.src.entry import entry


def main():
    entry()


if __name__ == "__main__":
    main()
