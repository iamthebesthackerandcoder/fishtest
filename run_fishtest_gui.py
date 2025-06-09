#!/usr/bin/env python3
"""
Simple launcher for Fishtest Worker GUI
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Launch the fishtest worker GUI"""
    gui_script = Path(__file__).parent / "fishtest_gui.py"
    
    if not gui_script.exists():
        print(f"Error: {gui_script} not found!")
        return 1
        
    try:
        # Launch the GUI
        subprocess.run([sys.executable, str(gui_script)])
        return 0
    except Exception as e:
        print(f"Error launching GUI: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
