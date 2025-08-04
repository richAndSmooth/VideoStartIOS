"""
Start Sequence Widget Module
Handles the race start sequence with audio cues.
"""

import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtMultimedia import QSoundEffect
import random

class StartSequenceWidget(QWidget):
    """Widget for handling race start sequence with audio cues."""
    
    sequence_finished = pyqtSignal()
    sequence_cancelled = pyqtSignal()
    start_beep_played = pyqtSignal()  # New signal for precise timing
    
    def __init__(self, config: dict, audio_enabled: bool = True):
        super().__init__()
        self.config = config
        self.audio_enabled = audio_enabled
        self.current_step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        
        # Audio effects
        self.audio_effects = {}
        self.setup_audio()
        
        # Sequence steps
        self.sequence_steps = [
            ("go_to_start", "Go to the start", self.config.get('go_to_start_duration', 5)),
            ("in_position", "In position", random.uniform(
                self.config.get('in_position_min', 1.0),
                self.config.get('in_position_max', 3.0)
            )),
            ("set", "Set", random.uniform(
                self.config.get('set_min', 1.0),
                self.config.get('set_max', 3.0)
            )),
            ("start_beep", "GO!", 0.1)
        ]
        
        self.init_ui()
        
        # Audio loading completed
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Race Start Sequence")
        self.setFixedSize(500, 400)
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
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("RACE START SEQUENCE")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ff6b6b; margin-bottom: 20px;")
        layout.addWidget(title_label)
        
        # Current step display
        self.step_label = QLabel("")
        self.step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.step_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.step_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                background-color: #2d2d2d;
                border: 2px solid #555555;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
            }
        """)
        layout.addWidget(self.step_label)
        
        # Progress indicator
        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setFont(QFont("Arial", 14))
        self.progress_label.setStyleSheet("color: #cccccc;")
        layout.addWidget(self.progress_label)
        
        # Cancel button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel Sequence")
        self.cancel_btn.setStyleSheet("""
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
        self.cancel_btn.clicked.connect(self.cancel_sequence)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
    def get_resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller."""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def setup_audio(self):
        """Setup audio effects for the sequence."""
        if not self.audio_enabled:
            return
            
        # Use WAV files from audio directory
        audio_files = {
            'go_to_start': 'audio/Go to the start (trump).wav',
            'in_position': 'audio/In position (trump).wav',
            'set': 'audio/Set (trump).wav',
            'start_beep': 'audio/start_beep.wav'
        }
        
        for key, relative_path in audio_files.items():
            file_path = self.get_resource_path(relative_path)
            if os.path.exists(file_path):
                effect = QSoundEffect()
                effect.setSource(QUrl.fromLocalFile(file_path))
                effect.setVolume(1.0)  # Maximum volume
                self.audio_effects[key] = effect
            else:
                pass  # Audio file not found
        
    def start_sequence(self):
        """Start the race start sequence."""
        self.current_step = 0
        self.next_step()
        
    def next_step(self):
        """Move to the next step in the sequence."""
        if self.current_step >= len(self.sequence_steps):
            self.sequence_finished.emit()
            self.close()
            return
            
        step_key, step_text, duration = self.sequence_steps[self.current_step]
        
        # Update display
        self.step_label.setText(step_text)
        self.progress_label.setText(f"Step {self.current_step + 1} of {len(self.sequence_steps)}")
        
        # Special handling for start_beep step - TRULY SIMULTANEOUS audio and signal
        if step_key == "start_beep":
            # Simultaneous beep and recording start
            
            # For maximum synchronization: start audio and emit signal in rapid succession
            if self.audio_enabled and step_key in self.audio_effects:
                # Start audio first (it has its own buffering delay)
                self.audio_effects[step_key].play()
            
            # Emit signal immediately after audio starts (they're now truly synchronized)
            self.start_beep_played.emit()
            
            # Emit sequence_finished for UI updates (happens slightly after)
            self.sequence_finished.emit()
            self.close()
            return
        
        # Play audio for other steps (normal flow)
        if self.audio_enabled and step_key in self.audio_effects:
            self.audio_effects[step_key].play()
        else:
            pass  # Audio not available for this step
        
        # Schedule next step for other steps
        if duration > 0:
            self.timer.singleShot(int(duration * 1000), self.next_step)
        
        self.current_step += 1
        
    def cancel_sequence(self):
        """Cancel the start sequence."""
        self.timer.stop()
        self.sequence_cancelled.emit()
        self.close()
        
    def showEvent(self, event):
        """Override show event to start sequence automatically."""
        super().showEvent(event)
        self.start_sequence()
        
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Escape:
            self.cancel_sequence()
        else:
            super().keyPressEvent(event)