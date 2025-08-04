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
    
    def __init__(self, output_path: str, quality: Any = "Medium (720p)", camera_fps: float = 30.0):
        self.output_path = output_path
        self.quality = quality
        self.camera_fps = camera_fps
        self.writer = None
        self.is_recording = False
        self.frame_count = 0
        self.start_time = None
        self.race_start_time = None  # Time when the race actually starts (beep goes off)
        
        # Quality settings (FPS will be overridden by camera_fps)
        self.quality_settings = {
            "High (1080p)": {"width": 1920, "height": 1080},
            "Medium (720p)": {"width": 1280, "height": 720},
            "Low (480p)": {"width": 854, "height": 480}
        }
        
    def initialize_writer(self):
        """Initialize the video writer (slow operation - do this BEFORE beep)."""
        try:
            # Get quality settings - handle both string keys and dictionary objects
            if isinstance(self.quality, dict):
                # Quality is already a dictionary with width/height/fps
                settings = self.quality
            else:
                # Quality is a string key, look it up in quality_settings
                settings = self.quality_settings.get(self.quality, self.quality_settings["Medium (720p)"])
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(self.output_path)
            os.makedirs(output_dir, exist_ok=True)
            
            # Initialize video writer with fallback codecs
            codecs_to_try = ['mp4v', 'H264', 'XVID', 'MJPG']
            self.writer = None
            
            for codec in codecs_to_try:
                try:
                    fourcc = cv2.VideoWriter_fourcc(*codec)
                    self.writer = cv2.VideoWriter(
                        self.output_path,
                        fourcc,
                        self.camera_fps,  # Use camera_fps here
                        (settings["width"], settings["height"])
                    )
                    
                    if self.writer.isOpened():
                        break
                    else:
                        self.writer.release()
                        self.writer = None
                except Exception as e:
                    if self.writer:
                        self.writer.release()
                        self.writer = None
            
            if not self.writer or not self.writer.isOpened():
                raise Exception(f"Failed to initialize video writer with any codec. Tried: {codecs_to_try}")
            
            # Validate the writer was created with correct FPS
            actual_fps = self.writer.get(cv2.CAP_PROP_FPS)
            
            if abs(actual_fps - self.camera_fps) > 1.0:
                # Try to reinitialize with a different codec if there's a mismatch
                self.writer.release()
                fourcc = cv2.VideoWriter_fourcc(*'H264')
                self.writer = cv2.VideoWriter(
                    self.output_path,
                    fourcc,
                    self.camera_fps,
                    (settings["width"], settings["height"])
                )
                if not self.writer.isOpened():
                    # Fallback to original codec
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    self.writer = cv2.VideoWriter(
                        self.output_path,
                        fourcc,
                        self.camera_fps,
                        (settings["width"], settings["height"])
                    )
                    if not self.writer.isOpened():
                        raise Exception("Failed to initialize video writer with any codec")
            
            return True
            
        except Exception as e:
            raise
    
    def start_recording(self):
        """Start video recording INSTANTLY (writer must be pre-initialized)."""
        try:
            if not self.writer or not self.writer.isOpened():
                raise Exception("Video writer not initialized! Call initialize_writer() first.")
            
            # INSTANT START - no delays, just mark the recording as active
            self.is_recording = True
            self.frame_count = 0
            self.start_time = datetime.now()
            self.race_start_time = datetime.now()  # Set race start time when recording begins
            
            pass  # Recording started
            
        except Exception as e:
            raise
            
    def record_frame(self, frame: np.ndarray):
        """Record a single frame."""
        if not self.is_recording or self.writer is None:
            return
            
        try:
            # Resize frame to match quality settings - handle both string keys and dictionary objects
            if isinstance(self.quality, dict):
                # Quality is already a dictionary with width/height/fps
                settings = self.quality
            else:
                # Quality is a string key, look it up in quality_settings
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
            pass  # Handle frame recording error silently
            
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
            return frame
            
    def add_time_overlay(self, frame: np.ndarray) -> np.ndarray:
        """Add continuous time overlay to frame."""
        try:
            # Create a copy of the frame
            marked_frame = frame.copy()
            
            # Calculate elapsed time from race start
            if self.race_start_time is not None:
                # Calculate elapsed time based on frame count and FPS
                elapsed_seconds = self.frame_count / self.camera_fps
                
                # Convert to MM:SS.mmm format
                minutes = int(elapsed_seconds // 60)
                seconds = elapsed_seconds % 60
                timestamp = f"{minutes:02d}:{seconds:06.3f}"
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
            return frame
            
    def stop_recording(self):
        """Stop video recording."""
        if self.is_recording and self.writer is not None:
            try:
                self.writer.release()
                self.is_recording = False
                
                pass  # Recording stopped successfully
                
                # Create metadata file
                self.create_metadata_file()
                
            except Exception as e:
                pass  # Handle stop recording error silently
                
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
                f.write(f"Recording FPS: {self.camera_fps} fps\n")
                
                # Calculate actual recording duration and frame rate
                if self.start_time and self.frame_count > 0:
                    duration = datetime.now() - self.start_time
                    actual_fps = self.frame_count / duration.total_seconds()
                    f.write(f"Actual Recording Duration: {duration}\n")
                    f.write(f"Actual Frame Rate: {actual_fps:.2f} fps\n")
                    f.write(f"Frame Rate Accuracy: {'✓ Good' if abs(actual_fps - self.camera_fps) < 2.0 else '⚠ Mismatch'}\n")
                
                # Handle quality settings for metadata
                if isinstance(self.quality, dict):
                    f.write(f"Resolution: {self.quality['width']}x{self.quality['height']}\n")
                    f.write(f"Quality Setting FPS: {self.quality.get('fps', 'Unknown')}\n")
                else:
                    settings = self.quality_settings.get(self.quality, self.quality_settings["Medium (720p)"])
                    f.write(f"Resolution: {settings['width']}x{settings['height']}\n")
                
                # Get the actual codec used
                actual_codec = "Unknown"
                if hasattr(self, 'writer') and self.writer:
                    try:
                        # Try to get codec info from the writer
                        actual_codec = "MP4V"  # Default assumption
                    except:
                        pass
                
                f.write(f"\nVideo Codec: {actual_codec} (OpenCV)\n")
                f.write(f"Note: Video recorded at camera's actual FPS for accurate playback speed\n")
                
            pass  # Metadata saved successfully
            
        except Exception as e:
            pass  # Handle metadata creation error silently
            
    def get_recording_info(self) -> Dict[str, Any]:
        """Get information about the current recording."""
        return {
            "is_recording": self.is_recording,
            "output_path": self.output_path,
            "frame_count": self.frame_count,
            "start_time": self.start_time,
            "quality": self.quality
        } 