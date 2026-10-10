#!/usr/bin/env python3
"""
Demo script for Server Health Monitor.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from health_monitor import main

if __name__ == "__main__":
    print("Running Server Health Monitor Demo...")
    report = main()
    print("\nDemo completed successfully!")