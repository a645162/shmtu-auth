import os
import sys

# Add ./src directory to the Python path
sys.path.append(os.path.dirname(__file__))

from shmtu_auth.main_start import main

if __name__ == "__main__":
    main()
