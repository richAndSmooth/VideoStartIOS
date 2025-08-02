"""
Camera Thread Module
Handles webcam capture in a separate thread to prevent UI blocking.
"""

import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from typing import List, Optional

class CameraThread(QThread):
    """Thread for handling camera capture."""
    
    frame_ready = pyqtSignal(np.ndarray)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.camera = None
        self.is_running = False
        self.current_camera_index = 0
        self.available_cameras = []
        
    def run(self):
        """Main thread loop for camera capture."""
        self.is_running = True
        
        while self.is_running:
            try:
                if self.camera is not None and self.camera.isOpened():
                    ret, frame = self.camera.read()
                    
                    if ret and frame is not None:
                        # Convert BGR to RGB for Qt
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        self.frame_ready.emit(frame_rgb)
                    else:
                        # Frame read failed, try to reconnect
                        print("Frame read failed, attempting to reconnect...")
                        self.connect_camera(self.current_camera_index)
                        self.msleep(500)  # Wait 500ms before retry
                else:
                    # Camera not connected, try to connect
                    if not self.connect_camera(self.current_camera_index):
                        self.msleep(1000)  # Wait 1 second before retry
            except Exception as e:
                print(f"Camera thread error: {e}")
                self.msleep(1000)
                
        # Clean up
        if self.camera is not None:
            self.camera.release()
            
    def connect_camera(self, camera_index: int) -> bool:
        """Connect to a specific camera."""
        try:
            if self.camera is not None:
                self.camera.release()
                
            # Try different camera backends
            backends = [
                cv2.CAP_DSHOW,  # DirectShow (Windows)
                cv2.CAP_MSMF,   # Microsoft Media Foundation
                cv2.CAP_ANY     # Auto-detect
            ]
            
            camera = None
            for backend in backends:
                try:
                    camera = cv2.VideoCapture(camera_index, backend)
                    if camera.isOpened():
                        # Test if we can actually read a frame
                        ret, test_frame = camera.read()
                        if ret and test_frame is not None:
                            self.camera = camera
                            break
                        else:
                            camera.release()
                except Exception as e:
                    print(f"Backend {backend} failed: {e}")
                    if camera:
                        camera.release()
            
            if self.camera is None or not self.camera.isOpened():
                print(f"Failed to connect to camera {camera_index} with any backend")
                self.error_occurred.emit(f"Failed to connect to camera {camera_index}")
                return False
                
            # Set camera properties for better performance
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            self.current_camera_index = camera_index
            print(f"Successfully connected to camera {camera_index}")
            return True
            
        except Exception as e:
            print(f"Error connecting to camera: {str(e)}")
            self.error_occurred.emit(f"Error connecting to camera: {str(e)}")
            return False
            
    def change_camera(self, camera_index: int):
        """Change to a different camera."""
        if camera_index != self.current_camera_index:
            self.connect_camera(camera_index)
            
    def get_available_cameras(self) -> List[str]:
        """Get list of available cameras."""
        cameras = []
        
        # Try to find cameras by testing indices 0-9
        for i in range(10):
            try:
                cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Try DirectShow first
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        # Get camera name/info
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        fps = int(cap.get(cv2.CAP_PROP_FPS))
                        
                        camera_info = f"Camera {i} ({width}x{height} @ {fps}fps)"
                        cameras.append(camera_info)
                    cap.release()
            except Exception as e:
                print(f"Error testing camera {i}: {e}")
                
        # If no cameras found with DirectShow, try MSMF
        if not cameras:
            for i in range(10):
                try:
                    cap = cv2.VideoCapture(i, cv2.CAP_MSMF)
                    if cap.isOpened():
                        ret, frame = cap.read()
                        if ret and frame is not None:
                            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            fps = int(cap.get(cv2.CAP_PROP_FPS))
                            
                            camera_info = f"Camera {i} ({width}x{height} @ {fps}fps)"
                            cameras.append(camera_info)
                        cap.release()
                except Exception as e:
                    print(f"Error testing camera {i} with MSMF: {e}")
                
        self.available_cameras = cameras
        return cameras
        
    def stop(self):
        """Stop the camera thread."""
        self.is_running = False
        self.wait()  # Wait for thread to finish
        
    def get_current_frame(self) -> Optional[np.ndarray]:
        """Get the current frame from camera (for recording)."""
        if self.camera is not None and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None 