#!/usr/bin/env python3
"""
Chess Game - Entry Point
A complete chess implementation with AI opponent, tutorials, and puzzles.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ui import main

if __name__ == "__main__":
    main()
