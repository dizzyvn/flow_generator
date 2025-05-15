#!/bin/bash

# Check if Python virtual environment exists, if not create it
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install requirements if not already installed
if [ ! -f ".venv/requirements_installed" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
    touch .venv/requirements_installed
fi

# Check if requirement is provided
if [ -z "$1" ]; then
    echo "Please provide a requirement as an argument"
    echo "Usage: ./run.sh \"your requirement here\""
    exit 1
fi

# Generate the flow code
echo "Generating flow code for requirement: $1"
python main.py --requirement "$1"

# Visualize the flow
echo "Generating flow visualization..."
python execution_sandbox/visualize.py

# Build and run the Docker container
echo "Building and running the flow..."
docker build -t execution .
docker run -it --env-file .env execution

# Deactivate virtual environment
deactivate
