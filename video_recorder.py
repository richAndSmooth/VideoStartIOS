"""
Video Recorder Module
Handles video capture and saving with timing markers.
"""

import cv2
import numpy as np
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from PyQt6.QtCore import QThread, pyqtSignal

class VideoRecorder:
    """Handles video recording with timing markers."""
    
    def __init__(self, output_path: str, quality: str = "Medium (720p)", camera_fps: float = 30.0):
        self.output_path = output_path
        self.quality = quality
        self.camera_fps = camera_fps
        self.writer = None
        self.is_recording = False
        self.frame_count = 0
        self.start_time = None
        
        # Quality settings (FPS will be overridden by camera_fps)
        self.quality_settings = {
            "High (1080p)": {"width": 1920, "height": 1080},
            "Medium (720p)": {"width": 1280, "height": 720},
            "Low (480p)": {"width": 854, "height": 480}
        }
        
    def start_recording(self):
        """Start video recording."""
        try:
            # Get quality settings
            settings = self.quality_settings.get(self.quality, self.quality_settings["Medium (720p)"])
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(self.output_path)
            os.makedirs(output_dir, exist_ok=True)
            
            # Initialize video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.writer = cv2.VideoWriter(
                self.output_path,
                fourcc,
                self.camera_fps,  # Use camera_fps here
                (settings["width"], settings["height"])
            )
            
            if not self.writer.isOpened():
                raise Exception("Failed to initialize video writer")
                
            self.is_recording = True
            self.frame_count = 0
            self.start_time = datetime.now()
            
            print(f"Started recording to: {self.output_path}")
            
        except Exception as e:
            print(f"Error starting recording: {str(e)}")
            raise
            
    def record_frame(self, frame: np.ndarray):
        """Record a single frame."""
        if not self.is_recording or self.writer is None:
            return
            
        try:
            # Resize frame to match quality settings
            settings = self.quality_settings.get(self.quality, self.quality_settings["Medium (720p)"])
            resized_frame = cv2.resize(frame, (settings["width"], settings["height"]))
            
            # Convert RGB to BGR for OpenCV
            bgr_frame = cv2.cvtColor(resized_frame, cv2.COLOR_RGB2BGR)
            
            # Add timing overlay if this is the start frame
            if self.frame_count == 0:
                bgr_frame = self.add_start_marker(bgr_frame)
            
            # Add continuous time overlay to every frame
            bgr_frame = self.add_time_overlay(bgr_frame)
                
            # Write frame
            self.writer.write(bgr_frame)
            self.frame_count += 1
            
        except Exception as e:
            print(f"Error recording frame: {str(e)}")
            
    def add_start_marker(self, frame: np.ndarray) -> np.ndarray:
        """Add start marker overlay to frame."""
        try:
            # Create a copy of the frame
            marked_frame = frame.copy()
            
            # Add start marker text
            text = "START"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 2.0
            thickness = 3
            color = (0, 255, 0)  # Green
            
            # Get text size
            (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
            
            # Calculate position (top-right corner)
            x = frame.shape[1] - text_width - 20
            y = text_height + 20
            
            # Add background rectangle
            cv2.rectangle(marked_frame, (x - 10, y - text_height - 10), 
                         (x + text_width + 10, y + 10), (0, 0, 0), -1)
            
            # Add text
            cv2.putText(marked_frame, text, (x, y), font, font_scale, color, thickness)
            
            # Add timestamp
            timestamp = self.start_time.strftime("%H:%M:%S.%f")[:-3]
            timestamp_text = f"Time: {timestamp}"
            timestamp_font_scale = 0.8
            timestamp_thickness = 2
            
            # Get timestamp text size
            (ts_width, ts_height), _ = cv2.getTextSize(timestamp_text, font, timestamp_font_scale, timestamp_thickness)
            
            # Calculate timestamp position (below start marker)
            ts_x = frame.shape[1] - ts_width - 20
            ts_y = y + 40
            
            # Add timestamp background
            cv2.rectangle(marked_frame, (ts_x - 10, ts_y - ts_height - 10), 
                         (ts_x + ts_width + 10, ts_y + 10), (0, 0, 0), -1)
            
            # Add timestamp text
            cv2.putText(marked_frame, timestamp_text, (ts_x, ts_y), 
                       font, timestamp_font_scale, (255, 255, 255), timestamp_thickness)
            
            return marked_frame
            
        except Exception as e:
            print(f"Error adding start marker: {str(e)}")
            return frame
            
    def add_time_overlay(self, frame: np.ndarray) -> np.ndarray:
        """Add continuous time overlay to frame."""
        try:
            # Create a copy of the frame
            marked_frame = frame.copy()
            
            # Calculate current time based on start time and frame count
            if self.start_time is not None:
                # Calculate elapsed time based on frame count and FPS
                elapsed_seconds = self.frame_count / self.camera_fps
                current_time = self.start_time + timedelta(seconds=elapsed_seconds)
                timestamp = current_time.strftime("%H:%M:%S.%f")[:-3]
            else:
                # Fallback to current system time
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            # Add time overlay text
            text = f"Time: {timestamp}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.0
            thickness = 2
            color = (255, 255, 255)  # White text
            
            # Get text size
            (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
            
            # Calculate position (top-left corner)
            x = 20
            y = text_height + 20
            
            # Add background rectangle for better visibility
            cv2.rectangle(marked_frame, (x - 10, y - text_height - 10), 
                         (x + text_width + 10, y + 10), (0, 0, 0), -1)
            
            # Add text
            cv2.putText(marked_frame, text, (x, y), font, font_scale, color, thickness)
            
            return marked_frame
            
        except Exception as e:
            print(f"Error adding time overlay: {str(e)}")
            return frame
            
    def add_finish_marker(self, frame: np.ndarray, finish_time: datetime) -> np.ndarray:
        """Add finish marker overlay to frame."""
        try:
            # Create a copy of the frame
            marked_frame = frame.copy()
            
            # Add finish marker text
            text = "FINISH"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 2.0
            thickness = 3
            color = (0, 0, 255)  # Red
            
            # Get text size
            (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
            
            # Calculate position (bottom-left corner to avoid conflict with time overlay)
            x = 20
            y = frame.shape[0] - 20
            
            # Add background rectangle
            cv2.rectangle(marked_frame, (x - 10, y - text_height - 10), 
                         (x + text_width + 10, y + 10), (0, 0, 0), -1)
            
            # Add text
            cv2.putText(marked_frame, text, (x, y), font, font_scale, color, thickness)
            
            # Add timestamp
            timestamp = finish_time.strftime("%H:%M:%S.%f")[:-3]
            timestamp_text = f"Time: {timestamp}"
            timestamp_font_scale = 0.8
            timestamp_thickness = 2
            
            # Get timestamp text size
            (ts_width, ts_height), _ = cv2.getTextSize(timestamp_text, font, timestamp_font_scale, timestamp_thickness)
            
            # Calculate timestamp position (above finish marker)
            ts_x = 20
            ts_y = y - 40
            
            # Add timestamp background
            cv2.rectangle(marked_frame, (ts_x - 10, ts_y - ts_height - 10), 
                         (ts_x + ts_width + 10, ts_y + 10), (0, 0, 0), -1)
            
            # Add timestamp text
            cv2.putText(marked_frame, timestamp_text, (ts_x, ts_y), 
                       font, timestamp_font_scale, (255, 255, 255), timestamp_thickness)
            
            return marked_frame
            
        except Exception as e:
            print(f"Error adding finish marker: {str(e)}")
            return frame
            
    def stop_recording(self):
        """Stop video recording."""
        if self.is_recording and self.writer is not None:
            try:
                self.writer.release()
                self.is_recording = False
                
                print(f"Recording stopped. Total frames: {self.frame_count}")
                print(f"Video saved to: {self.output_path}")
                
                # Create metadata file
                self.create_metadata_file()
                
            except Exception as e:
                print(f"Error stopping recording: {str(e)}")
                
    def create_metadata_file(self):
        """Create a metadata file with timing information."""
        try:
            metadata_path = self.output_path.replace('.mp4', '_metadata.txt')
            
            with open(metadata_path, 'w') as f:
                f.write("Race Timer Recording Metadata\n")
                f.write("=" * 30 + "\n\n")
                f.write(f"Video File: {os.path.basename(self.output_path)}\n")
                f.write(f"Recording Start: {self.start_time}\n")
                f.write(f"Total Frames: {self.frame_count}\n")
                f.write(f"Video Quality: {self.quality}\n")
                f.write(f"Frame Rate: {self.camera_fps} fps\n")
                f.write(f"Resolution: {self.quality_settings[self.quality]['width']}x{self.quality_settings[self.quality]['height']}\n")
                
            print(f"Metadata saved to: {metadata_path}")
            
        except Exception as e:
            print(f"Error creating metadata file: {str(e)}")
            
    def get_recording_info(self) -> Dict[str, Any]:
        """Get information about the current recording."""
        return {
            "is_recording": self.is_recording,
            "output_path": self.output_path,
            "frame_count": self.frame_count,
            "start_time": self.start_time,
            "quality": self.quality
        } 