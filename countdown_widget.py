"""
Countdown Widget Module
Displays a visual and audio countdown sequence before recording starts.
"""

import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QPainter, QPen

class CountdownWidget(QWidget):
    """Widget for displaying countdown sequence."""
    
    countdown_finished = pyqtSignal()
    countdown_cancelled = pyqtSignal()
    
    def __init__(self, duration: int = 3, audio_enabled: bool = True):
        super().__init__()
        self.duration = duration
        self.audio_enabled = audio_enabled
        self.current_count = duration
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        
        self.init_ui()
        self.setup_audio()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Countdown")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        
        # Center the window on screen
        screen = self.screen()
        screen_geometry = screen.geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
        # Set dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Countdown display
        self.countdown_label = QLabel(str(self.current_count))
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setFont(QFont("Arial", 72, QFont.Weight.Bold))
        self.countdown_label.setStyleSheet("""
            QLabel {
                color: #ff6b6b;
                background-color: transparent;
            }
        """)
        layout.addWidget(self.countdown_label)
        
        # Status label
        self.status_label = QLabel("Get Ready!")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 16))
        self.status_label.setStyleSheet("color: #ffffff;")
        layout.addWidget(self.status_label)
        
        # Cancel button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.cancel_btn.clicked.connect(self.cancel_countdown)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
    def setup_audio(self):
        """Setup audio for countdown (placeholder for future implementation)."""
        # This would integrate with a text-to-speech or audio playback system
        # For now, we'll just use visual countdown
        pass
        
    def start_countdown(self):
        """Start the countdown sequence."""
        self.current_count = self.duration
        self.update_display()
        self.timer.start(1000)  # Update every second
        
    def update_countdown(self):
        """Update the countdown display."""
        self.current_count -= 1
        
        if self.current_count > 0:
            self.update_display()
            if self.audio_enabled:
                self.play_countdown_audio(self.current_count)
        elif self.current_count == 0:
            # Show "GO!"
            self.countdown_label.setText("GO!")
            self.countdown_label.setStyleSheet("""
                QLabel {
                    color: #28a745;
                    background-color: transparent;
                }
            """)
            self.status_label.setText("Recording Started!")
            
            if self.audio_enabled:
                self.play_go_audio()
                
            # Wait a moment then finish
            QTimer.singleShot(500, self.finish_countdown)
        else:
            self.finish_countdown()
            
    def update_display(self):
        """Update the countdown display."""
        self.countdown_label.setText(str(self.current_count))
        
        # Change color based on countdown progress
        if self.current_count <= 1:
            color = "#ff6b6b"  # Red for last second
        elif self.current_count <= 2:
            color = "#ffa726"  # Orange for second to last
        else:
            color = "#42a5f5"  # Blue for others
            
        self.countdown_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                background-color: transparent;
            }}
        """)
        
    def play_countdown_audio(self, number: int):
        """Play countdown audio (placeholder)."""
        # This would integrate with a text-to-speech system
        # For now, we'll just print to console
        print(f"Countdown: {number}")
        
    def play_go_audio(self):
        """Play 'GO!' audio (placeholder)."""
        # This would play a 'GO!' sound
        print("GO!")
        
    def finish_countdown(self):
        """Finish the countdown and emit signal."""
        self.timer.stop()
        self.countdown_finished.emit()
        self.close()
        
    def cancel_countdown(self):
        """Cancel the countdown."""
        self.timer.stop()
        self.countdown_cancelled.emit()
        self.close()
        
    def showEvent(self, event):
        """Handle show event to start countdown."""
        super().showEvent(event)
        # Start countdown after a short delay
        QTimer.singleShot(500, self.start_countdown)
        
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Escape:
            self.cancel_countdown()
        else:
            super().keyPressEvent(event) 