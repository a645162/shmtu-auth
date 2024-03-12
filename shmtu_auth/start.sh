#!/bin/bash

# Load Functions
source ./scripts/env_func.sh

# Check Env Variables
source ./config/env.sh

echo "Python path:"
which python
echo ""

echo "Python version:"
python --version
echo ""

python main.py
