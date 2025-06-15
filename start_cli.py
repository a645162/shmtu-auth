# -*- coding: utf-8 -*-

import os
import sys

# Add ./src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from shmtu_auth.main_start import main

if __name__ == "__main__":
    main()
