#!/usr/bin/env python3
"""
Main entry point to run the Church Tech Ministry Telegram Bot
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run main
from main import main

if __name__ == '__main__':
    main()

