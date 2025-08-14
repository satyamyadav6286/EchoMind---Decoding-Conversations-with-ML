#!/bin/bash

# Install system dependencies
apt-get update
apt-get install -y \
    python3-pip \
    python3-dev \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    python3-tk \
    tcl-dev \
    tk-dev \
    python-tk \
    python3-tk \
    libffi-dev \
    libssl-dev

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Make sure the script is executable
chmod +x setup.sh

mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml