#!/usr/bin/env python3
"""
Main entry point for the bot with proper logging
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# Import main
from main import main

if __name__ == '__main__':
    # Force unbuffered output for better logging
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)
    sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 1)
    
    print("🚀 Starting bot with unbuffered logging...")
    print("=" * 50)
    
    main()
