#!/usr/bin/env python3
"""
Race Timing Application - Main Entry Point
A Windows 11 desktop application for complete race timing with start signal and finish line integration.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from race_timer_app import RaceTimerApp

def main():
    """Main application entry point."""
    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName("Race Timer")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("RaceTimer")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = RaceTimerApp()
    window.show()
    
    # Start the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 