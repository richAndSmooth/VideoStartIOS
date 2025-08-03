#!/usr/bin/env python3
"""
Simple test script to verify the application starts without crashing.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

def test_startup():
    """Test that the application can start without crashing."""
    print("Testing application startup...")
    
    try:
        # Create the application
        app = QApplication(sys.argv)
        app.setApplicationName("Race Timer Test")
        
        # Import and create the main window
        from race_timer_app import RaceTimerApp
        
        print("Creating main window...")
        window = RaceTimerApp()
        
        print("Showing main window...")
        window.show()
        
        # Set up a timer to close the app after 5 seconds
        def close_app():
            print("Test completed successfully - closing application")
            app.quit()
        
        QTimer.singleShot(5000, close_app)
        
        print("Starting application event loop...")
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_startup()
    if success:
        print("✅ Startup test passed!")
    else:
        print("❌ Startup test failed!")
        sys.exit(1) 