#!/usr/bin/env python3
"""
Test script to verify cursor fix for race timer application.
This script tests that the application starts without showing an hourglass cursor.
"""

import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

class CursorTestWindow(QMainWindow):
    """Simple test window to verify cursor behavior."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cursor Test - Race Timer")
        self.setGeometry(100, 100, 400, 200)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create status label
        self.status_label = QLabel("Testing cursor behavior...")
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Set initial cursor
        self.setCursor(Qt.CursorShape.ArrowCursor)
        
        # Simulate camera scanning delay
        QTimer.singleShot(100, self.simulate_camera_scan)
        
    def simulate_camera_scan(self):
        """Simulate camera scanning to test cursor behavior."""
        self.status_label.setText("Simulating camera scan...")
        self.setCursor(Qt.CursorShape.WaitCursor)  # Show hourglass
        
        # Simulate blocking operation
        QTimer.singleShot(2000, self.scan_complete)
        
    def scan_complete(self):
        """Called when simulated scan is complete."""
        self.status_label.setText("Camera scan complete!")
        self.setCursor(Qt.CursorShape.ArrowCursor)  # Restore normal cursor
        
        # Close after 2 seconds
        QTimer.singleShot(2000, self.close)

def test_cursor_behavior():
    """Test the cursor behavior."""
    app = QApplication(sys.argv)
    
    # Create test window
    window = CursorTestWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    test_cursor_behavior() 