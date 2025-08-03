#!/usr/bin/env python3
"""
Test script to verify recording display functionality
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

class TestRecordingDisplay(QMainWindow):
    """Simple test window to verify recording display functionality."""
    
    def __init__(self):
        super().__init__()
        self.is_recording = False
        self.recording_time = 0
        self.init_ui()
        
    def init_ui(self):
        """Initialize the test UI."""
        self.setWindowTitle("Recording Display Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Camera view label (simulated)
        self.camera_label = QLabel("Camera Feed (Simulated)")
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setStyleSheet("""
            QLabel {
                background-color: #1a1a1a;
                border: 2px solid #555555;
                border-radius: 5px;
                color: #888888;
                font-size: 16px;
            }
        """)
        layout.addWidget(self.camera_label)
        
        # Control buttons
        self.start_btn = QPushButton("Start Recording")
        self.start_btn.clicked.connect(self.start_recording)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                border: none;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop Recording")
        self.stop_btn.clicked.connect(self.stop_recording)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                border: none;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        layout.addWidget(self.stop_btn)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #28a745;")
        layout.addWidget(self.status_label)
        
        # Recording timer
        self.recording_timer = QTimer()
        self.recording_timer.timeout.connect(self.update_recording_time)
        
    def start_recording(self):
        """Start recording simulation."""
        self.is_recording = True
        self.recording_time = 0
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("Recording...")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #dc3545;")
        
        # Show recording message
        self.show_recording_message("Recording in progress...")
        
        # Start timer
        self.recording_timer.start(1000)  # Update every second
        
    def stop_recording(self):
        """Stop recording simulation."""
        self.is_recording = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Recording stopped")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #28a745;")
        
        # Restore camera view
        self.restore_camera_view()
        
        # Stop timer
        self.recording_timer.stop()
        
    def update_recording_time(self):
        """Update recording time."""
        self.recording_time += 1
        elapsed_str = f"{self.recording_time//60:02d}:{self.recording_time%60:02d}"
        self.show_recording_message(f"Recording in progress...\n\n{elapsed_str}")
        
    def show_recording_message(self, message: str):
        """Show a recording message instead of the camera feed."""
        self.camera_label.clear()
        self.camera_label.setText(message)
        self.camera_label.setStyleSheet("""
            QLabel {
                background-color: #1a1a1a;
                border: 3px solid #dc3545;
                border-radius: 10px;
                color: #dc3545;
                font-size: 24px;
                font-weight: bold;
                padding: 40px;
                text-align: center;
            }
        """)
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    def restore_camera_view(self):
        """Restore the camera view display."""
        self.camera_label.setText("Camera Feed (Simulated)")
        self.camera_label.setStyleSheet("""
            QLabel {
                background-color: #1a1a1a;
                border: 2px solid #555555;
                border-radius: 5px;
                color: #888888;
                font-size: 16px;
            }
        """)
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

def main():
    """Main function."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = TestRecordingDisplay()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 