#!/bin/bash
# Force install dependencies for Streamlit Cloud
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
echo "Dependencies installed successfully!" 