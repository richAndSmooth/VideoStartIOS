"""
Race Timer Application - Main Application Class
Handles camera integration, countdown sequences, and video recording with timing markers.
"""

import sys
import os
import cv2
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QComboBox, QSpinBox, QGroupBox, QTextEdit, QFileDialog,
    QMessageBox, QProgressBar, QSlider, QCheckBox, QFrame
)
from PyQt6.QtCore import (
    QTimer, QThread, pyqtSignal, QTime, QDate, Qt, QSize
)
from PyQt6.QtGui import (
    QPixmap, QImage, QFont, QPalette, QColor, QPainter, QPen
)
from camera_thread import CameraThread
from start_sequence_widget import StartSequenceWidget
from video_recorder import VideoRecorder
from timing_markers import TimingMarkers
from config_manager import ConfigManager

class RaceTimerApp(QMainWindow):
    """Main application window for race timing."""
    
    def __init__(self):
        super().__init__()
        self.config = ConfigManager()
        self.camera_thread = None
        self.video_recorder = None
        self.timing_markers = TimingMarkers()
        self.start_sequence_widget = None
        self.is_recording = False
        self.is_sequence_active = False
        
        # Initialize start sequence configuration
        self.init_start_sequence_config()
        
        self.init_ui()
        self.setup_camera()
        self.connect_camera_signals()
        
    def init_start_sequence_config(self):
        """Initialize start sequence configuration with defaults."""
        # Get existing config or set defaults
        self.start_sequence_config = {
            'go_to_start_duration': self.config.get('go_to_start_duration', 5),
            'in_position_min': self.config.get('in_position_min', 1.0),
            'in_position_max': self.config.get('in_position_max', 3.0),
            'set_min': self.config.get('set_min', 1.0),
            'set_max': self.config.get('set_max', 3.0),
            'audio_enabled': self.config.get('audio_enabled', True)
        }
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Race Timer - Complete Timing System")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)
        
        # Set window icon and style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #4a90e2;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2d5aa0;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }
            QLabel {
                color: #ffffff;
            }
            QComboBox, QSpinBox {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                color: #ffffff;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel - Camera and controls
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 2)
        
        # Right panel - Settings and status
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)
        
    def create_left_panel(self):
        """Create the left panel with camera view and main controls."""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(panel)
        
        # Camera view
        camera_group = QGroupBox("Camera View")
        camera_layout = QVBoxLayout(camera_group)
        
        self.camera_label = QLabel("Camera not connected")
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
        camera_layout.addWidget(self.camera_label)
        
        # Camera controls
        camera_controls = QHBoxLayout()
        
        self.camera_combo = QComboBox()
        self.camera_combo.addItem("Loading cameras...")
        self.refresh_cameras()
        camera_controls.addWidget(QLabel("Camera:"))
        camera_controls.addWidget(self.camera_combo)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_cameras)
        camera_controls.addWidget(self.refresh_btn)
        
        camera_layout.addLayout(camera_controls)
        layout.addWidget(camera_group)
        
        # Start Sequence Controls
        recording_group = QGroupBox("Start Sequence Controls")
        recording_layout = QVBoxLayout(recording_group)
        
        # Phase 1: Go to start duration
        phase1_layout = QHBoxLayout()
        phase1_layout.addWidget(QLabel("Go to start:"))
        
        self.go_to_start_spin = QSpinBox()
        self.go_to_start_spin.setRange(3, 15)
        self.go_to_start_spin.setValue(self.start_sequence_config['go_to_start_duration'])
        self.go_to_start_spin.valueChanged.connect(self.update_start_sequence_config)
        phase1_layout.addWidget(self.go_to_start_spin)
        phase1_layout.addWidget(QLabel("seconds"))
        phase1_layout.addStretch()
        
        recording_layout.addLayout(phase1_layout)
        
        # Phase 2: In position timing
        phase2_layout = QHBoxLayout()
        phase2_layout.addWidget(QLabel("In position:"))
        
        self.in_position_min_spin = QSpinBox()
        self.in_position_min_spin.setRange(1, 50)
        self.in_position_min_spin.setValue(int(self.start_sequence_config['in_position_min'] * 10))
        self.in_position_min_spin.setSuffix(" (×0.1s)")
        self.in_position_min_spin.valueChanged.connect(self.update_start_sequence_config)
        phase2_layout.addWidget(QLabel("min"))
        phase2_layout.addWidget(self.in_position_min_spin)
        
        self.in_position_max_spin = QSpinBox()
        self.in_position_max_spin.setRange(1, 50)
        self.in_position_max_spin.setValue(int(self.start_sequence_config['in_position_max'] * 10))
        self.in_position_max_spin.setSuffix(" (×0.1s)")
        self.in_position_max_spin.valueChanged.connect(self.update_start_sequence_config)
        phase2_layout.addWidget(QLabel("max"))
        phase2_layout.addWidget(self.in_position_max_spin)
        phase2_layout.addStretch()
        
        recording_layout.addLayout(phase2_layout)
        
        # Phase 3: Set timing
        phase3_layout = QHBoxLayout()
        phase3_layout.addWidget(QLabel("Set:"))
        
        self.set_min_spin = QSpinBox()
        self.set_min_spin.setRange(1, 50)
        self.set_min_spin.setValue(int(self.start_sequence_config['set_min'] * 10))
        self.set_min_spin.setSuffix(" (×0.1s)")
        self.set_min_spin.valueChanged.connect(self.update_start_sequence_config)
        phase3_layout.addWidget(QLabel("min"))
        phase3_layout.addWidget(self.set_min_spin)
        
        self.set_max_spin = QSpinBox()
        self.set_max_spin.setRange(1, 50)
        self.set_max_spin.setValue(int(self.start_sequence_config['set_max'] * 10))
        self.set_max_spin.setSuffix(" (×0.1s)")
        self.set_max_spin.valueChanged.connect(self.update_start_sequence_config)
        phase3_layout.addWidget(QLabel("max"))
        phase3_layout.addWidget(self.set_max_spin)
        phase3_layout.addStretch()
        
        recording_layout.addLayout(phase3_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Sequence")
        self.start_btn.clicked.connect(self.start_recording)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                font-size: 14px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop Recording")
        self.stop_btn.clicked.connect(self.stop_recording)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                font-size: 14px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        button_layout.addWidget(self.stop_btn)
        
        recording_layout.addLayout(button_layout)
        layout.addWidget(recording_group)
        
        # Status display
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #28a745;")
        status_layout.addWidget(self.status_label)
        
        self.recording_time_label = QLabel("Recording time: 00:00:00")
        self.recording_time_label.setStyleSheet("font-size: 12px; color: #888888;")
        status_layout.addWidget(self.recording_time_label)
        
        layout.addWidget(status_group)
        layout.addStretch()
        
        return panel
        
    def create_right_panel(self):
        """Create the right panel with settings and timing information."""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(panel)
        
        # Timing markers
        markers_group = QGroupBox("Timing Markers")
        markers_layout = QVBoxLayout(markers_group)
        
        self.start_time_label = QLabel("Start: Not marked")
        self.start_time_label.setStyleSheet("color: #28a745; font-weight: bold;")
        markers_layout.addWidget(self.start_time_label)
        
        self.finish_time_label = QLabel("Finish: Not marked")
        self.finish_time_label.setStyleSheet("color: #dc3545; font-weight: bold;")
        markers_layout.addWidget(self.finish_time_label)
        
        self.duration_label = QLabel("Duration: --")
        self.duration_label.setStyleSheet("color: #ffc107; font-weight: bold;")
        markers_layout.addWidget(self.duration_label)
        
        layout.addWidget(markers_group)
        
        # Settings
        settings_group = QGroupBox("Settings")
        settings_layout = QVBoxLayout(settings_group)
        
        # Video quality
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Video Quality:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["High (1080p)", "Medium (720p)", "Low (480p)"])
        self.quality_combo.setCurrentText("Medium (720p)")
        quality_layout.addWidget(self.quality_combo)
        settings_layout.addLayout(quality_layout)
        
        # Audio settings
        self.audio_checkbox = QCheckBox("Enable start sequence audio")
        self.audio_checkbox.setChecked(self.start_sequence_config['audio_enabled'])
        self.audio_checkbox.stateChanged.connect(self.update_audio_setting)
        settings_layout.addWidget(self.audio_checkbox)
        
        # Auto-save
        self.auto_save_checkbox = QCheckBox("Auto-save recordings")
        self.auto_save_checkbox.setChecked(True)
        settings_layout.addWidget(self.auto_save_checkbox)
        
        layout.addWidget(settings_group)
        
        # Recent recordings
        recent_group = QGroupBox("Recent Recordings")
        recent_layout = QVBoxLayout(recent_group)
        
        self.recent_list = QTextEdit()
        self.recent_list.setMaximumHeight(150)
        self.recent_list.setReadOnly(True)
        self.recent_list.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                border: 1px solid #555555;
                color: #ffffff;
            }
        """)
        recent_layout.addWidget(self.recent_list)
        
        layout.addWidget(recent_group)
        
        # Webhook status (future feature)
        webhook_group = QGroupBox("Webhook Status (Future)")
        webhook_layout = QVBoxLayout(webhook_group)
        
        self.webhook_status = QLabel("Webhook server: Disabled")
        self.webhook_status.setStyleSheet("color: #888888;")
        webhook_layout.addWidget(self.webhook_status)
        
        layout.addWidget(webhook_group)
        
        layout.addStretch()
        
        return panel
        
    def setup_camera(self):
        """Initialize camera thread and connections."""
        self.camera_thread = CameraThread()
        self.camera_thread.frame_ready.connect(self.update_camera_view)
        self.camera_thread.error_occurred.connect(self.handle_camera_error)
        self.camera_thread.frame_ready_signal.connect(self.trigger_frame_recording)
        
        # Start camera thread
        self.camera_thread.start()
        
    def connect_camera_signals(self):
        """Connect camera-related UI signals after UI is initialized."""
        if hasattr(self, 'camera_combo'):
            self.camera_combo.currentIndexChanged.connect(self.change_camera)
        
    def refresh_cameras(self):
        """Refresh the list of available cameras."""
        self.camera_combo.clear()
        
        if self.camera_thread is None:
            self.camera_combo.addItem("Camera not initialized")
            return
            
        cameras = self.camera_thread.get_available_cameras()
        
    def update_start_sequence_config(self):
        """Update start sequence configuration when UI controls change."""
        self.start_sequence_config['go_to_start_duration'] = self.go_to_start_spin.value()
        self.start_sequence_config['in_position_min'] = self.in_position_min_spin.value() / 10.0
        self.start_sequence_config['in_position_max'] = self.in_position_max_spin.value() / 10.0
        self.start_sequence_config['set_min'] = self.set_min_spin.value() / 10.0
        self.start_sequence_config['set_max'] = self.set_max_spin.value() / 10.0
        
        # Save to config
        self.config.set('go_to_start_duration', self.start_sequence_config['go_to_start_duration'])
        self.config.set('in_position_min', self.start_sequence_config['in_position_min'])
        self.config.set('in_position_max', self.start_sequence_config['in_position_max'])
        self.config.set('set_min', self.start_sequence_config['set_min'])
        self.config.set('set_max', self.start_sequence_config['set_max'])
        
    def update_audio_setting(self):
        """Update audio enabled setting."""
        self.start_sequence_config['audio_enabled'] = self.audio_checkbox.isChecked()
        self.config.set('audio_enabled', self.start_sequence_config['audio_enabled'])
        
        if not cameras:
            self.camera_combo.addItem("No cameras found")
        else:
            for i, camera_info in enumerate(cameras):
                self.camera_combo.addItem(f"Camera {i}: {camera_info}")
                
        if cameras:
            self.camera_combo.setCurrentIndex(0)
            
    def change_camera(self):
        """Change the active camera."""
        if self.camera_thread and self.camera_combo.currentIndex() >= 0:
            camera_index = self.camera_combo.currentIndex()
            self.camera_thread.change_camera(camera_index)
            
    def update_camera_view(self, frame):
        """Update the camera view with a new frame."""
        if frame is not None:
            # Convert OpenCV frame to QPixmap
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            
            # Scale to fit the label while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                self.camera_label.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            
            self.camera_label.setPixmap(scaled_pixmap)
            
    def handle_camera_error(self, error_message):
        """Handle camera errors."""
        self.status_label.setText(f"Camera Error: {error_message}")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #dc3545;")
        
    def start_recording(self):
        """Start the recording process with start sequence."""
        if self.is_recording or self.is_sequence_active:
            return
            
        # Create start sequence widget
        self.start_sequence_widget = StartSequenceWidget(
            self.start_sequence_config, 
            self.audio_checkbox.isChecked()
        )
        self.start_sequence_widget.sequence_finished.connect(self.on_sequence_finished)
        self.start_sequence_widget.sequence_cancelled.connect(self.on_sequence_cancelled)
        
        # Show start sequence
        self.start_sequence_widget.show()
        self.is_sequence_active = True
        self.start_btn.setEnabled(False)
        self.status_label.setText("Start sequence in progress...")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffc107;")
        
    def on_sequence_finished(self):
        """Handle start sequence completion and start recording."""
        self.is_sequence_active = False
        
        # Initialize video recorder with camera's actual FPS
        output_path = self.get_output_path()
        quality = self.quality_combo.currentText()
        
        # Wait for camera to be fully ready and get camera's actual FPS
        import time
        print("Waiting for camera to be ready...")
        time.sleep(1)  # Give camera a moment to stabilize
        
        camera_fps = self.camera_thread.get_camera_fps()
        print(f"Using camera FPS: {camera_fps}")
        
        self.video_recorder = VideoRecorder(output_path, quality, camera_fps)
        self.video_recorder.start_recording()
        
        # Mark start time
        start_time = datetime.now()
        self.timing_markers.set_start_time(start_time)
        self.start_time_label.setText(f"Start: {start_time.strftime('%H:%M:%S.%f')[:-3]}")
        
        # Update UI
        self.is_recording = True
        self.stop_btn.setEnabled(True)
        self.status_label.setText("Recording...")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #dc3545;")
        
        # Start recording timer
        self.recording_timer = QTimer()
        self.recording_timer.timeout.connect(self.update_recording_time)
        self.recording_start_time = datetime.now()
        self.recording_timer.start(100)  # Update every 100ms
        
        # Start frame recording using camera's natural rate
        # Instead of a timer, we'll record frames when they're available
        self.frame_recording_active = True
        
    def on_sequence_cancelled(self):
        """Handle start sequence cancellation."""
        self.is_sequence_active = False
        self.start_btn.setEnabled(True)
        self.status_label.setText("Ready")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #28a745;")
        
    def stop_recording(self):
        """Stop the recording."""
        if not self.is_recording:
            return
            
        # Stop recording timers
        if hasattr(self, 'recording_timer'):
            self.recording_timer.stop()
        
        # Stop frame recording
        self.frame_recording_active = False
            
        # Stop video recorder
        if self.video_recorder:
            self.video_recorder.stop_recording()
            
        # Mark finish time
        finish_time = datetime.now()
        self.timing_markers.set_finish_time(finish_time)
        self.finish_time_label.setText(f"Finish: {finish_time.strftime('%H:%M:%S.%f')[:-3]}")
        
        # Calculate duration
        if self.timing_markers.start_time and self.timing_markers.finish_time:
            duration = self.timing_markers.finish_time - self.timing_markers.start_time
            self.duration_label.setText(f"Duration: {duration}")
            
        # Update UI
        self.is_recording = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Recording saved")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #28a745;")
        
        # Add to recent recordings
        self.add_recent_recording()
        
    def update_recording_time(self):
        """Update the recording time display."""
        if hasattr(self, 'recording_start_time'):
            elapsed = datetime.now() - self.recording_start_time
            self.recording_time_label.setText(f"Recording time: {str(elapsed).split('.')[0]}")
            
    def record_current_frame(self):
        """Record the current camera frame."""
        if self.is_recording and self.video_recorder and self.camera_thread and hasattr(self, 'frame_recording_active'):
            frame = self.camera_thread.get_current_frame()
            if frame is not None:
                self.video_recorder.record_frame(frame)
                
    def trigger_frame_recording(self):
        """Trigger frame recording when a new frame is available."""
        if hasattr(self, 'frame_recording_active') and self.frame_recording_active:
            self.record_current_frame()
            
    def get_output_path(self):
        """Get the output path for the video file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"race_recording_{timestamp}.mp4"
        
        # Create recordings directory if it doesn't exist
        recordings_dir = os.path.join(os.getcwd(), "recordings")
        os.makedirs(recordings_dir, exist_ok=True)
        
        return os.path.join(recordings_dir, filename)
        
    def add_recent_recording(self):
        """Add the current recording to the recent recordings list."""
        if self.video_recorder and self.video_recorder.output_path:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filename = os.path.basename(self.video_recorder.output_path)
            
            recent_text = f"[{timestamp}] {filename}\n"
            if self.timing_markers.start_time:
                start_str = self.timing_markers.start_time.strftime("%H:%M:%S.%f")[:-3]
                recent_text += f"  Start: {start_str}\n"
            if self.timing_markers.finish_time:
                finish_str = self.timing_markers.finish_time.strftime("%H:%M:%S.%f")[:-3]
                recent_text += f"  Finish: {finish_str}\n"
            if self.timing_markers.start_time and self.timing_markers.finish_time:
                duration = self.timing_markers.finish_time - self.timing_markers.start_time
                recent_text += f"  Duration: {duration}\n"
            recent_text += "\n"
            
            current_text = self.recent_list.toPlainText()
            self.recent_list.setPlainText(recent_text + current_text)
            
    def closeEvent(self, event):
        """Handle application close event."""
        if self.is_recording:
            reply = QMessageBox.question(
                self, 'Stop Recording?', 
                'Recording is in progress. Do you want to stop and save?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.stop_recording()
            else:
                event.ignore()
                return
                
        if self.camera_thread:
            self.camera_thread.stop()
            
        event.accept() 