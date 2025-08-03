"""
Camera Thread Module
Handles webcam capture in a separate thread to prevent UI blocking.
"""

import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from typing import List, Optional, Dict, Tuple
import subprocess
import re
import os

# Suppress OpenCV warnings to reduce console noise
os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'

class CameraThread(QThread):
    """Thread for handling camera capture."""
    
    frame_ready = pyqtSignal(np.ndarray)
    frame_ready_signal = pyqtSignal()  # Signal for frame recording
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.camera = None
        self.is_running = False
        self.current_camera_index = 0
        self.available_cameras = []
        self.camera_details = {}  # Store detailed camera information
        self.is_switching = False  # Flag to prevent frame reading during camera switch
        
    def run(self):
        """Main thread loop for camera capture."""
        self.is_running = True
        
        while self.is_running:
            try:
                # Skip frame reading if we're switching cameras
                if self.is_switching:
                    self.msleep(100)  # Short sleep during switching
                    continue
                    
                if self.camera is not None and self.camera.isOpened():
                    try:
                        ret, frame = self.camera.read()
                        
                        if ret and frame is not None:
                            # Convert BGR to RGB for Qt
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            self.frame_ready.emit(frame_rgb)
                            
                            # Signal that a new frame is available for recording
                            self.frame_ready_signal.emit()
                        else:
                            # Frame read failed, try to reconnect
                            self.camera = None  # Force reconnection
                            self.msleep(500)  # Wait 500ms before retry
                    except Exception as e:
                        print(f"Frame read error: {e}")
                        # Try to reconnect on frame read errors
                        self.camera = None  # Force reconnection
                        self.msleep(500)
                else:
                    # Camera not connected, try to connect
                    if not self.connect_camera(self.current_camera_index):
                        self.msleep(1000)  # Wait 1 second before retry
            except Exception as e:
                print(f"Camera thread error: {e}")
                import traceback
                traceback.print_exc()
                self.msleep(1000)
                
        # Clean up
        if self.camera is not None:
            try:
                self.camera.release()
            except Exception as e:
                print(f"Error releasing camera during cleanup: {e}")
            
    def get_windows_camera_names(self) -> Dict[int, str]:
        """Get camera names from Windows using PowerShell."""
        camera_names = {}
        try:
            # Try a simpler PowerShell command that's less likely to timeout
            cmd = ["powershell", "-Command", "Get-WmiObject -Class Win32_PnPEntity | Where-Object {$_.Name -like '*Camera*'} | Select-Object -First 5 Name"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1)
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                camera_index = 0
                for line in lines:
                    if line.strip() and not line.startswith('----') and 'Name' not in line:
                        # Clean up the line and extract camera name
                        line = line.strip()
                        if any(keyword in line.lower() for keyword in ['camera', 'webcam', 'usb video']):
                            # Remove any special characters and clean up
                            camera_name = line
                            # Remove common prefixes/suffixes
                            for prefix in ['USB\\', '\\', 'SWD\\', 'Device\\']:
                                if camera_name.startswith(prefix):
                                    camera_name = camera_name[len(prefix):]
                            
                            # Clean up the name
                            camera_name = camera_name.strip()
                            if camera_name and len(camera_name) > 3 and camera_name not in camera_names.values():
                                camera_names[camera_index] = camera_name
                                camera_index += 1
                                
        except Exception as e:
            # Silently fail - this is not critical functionality
            pass
            
        return camera_names
            
    def connect_camera(self, camera_index: int) -> bool:
        """Connect to a specific camera."""
        try:
            if self.camera is not None:
                try:
                    self.camera.release()
                except Exception as e:
                    print(f"Error releasing previous camera: {e}")
            
            # Check if we have stored camera info for this index
            camera_info = self.camera_details.get(camera_index)
            if camera_info and 'backend' in camera_info:
                # Use the backend that was successful during initial detection
                stored_backend = camera_info['backend']
                backends = [stored_backend]
            else:
                # Fallback to trying different backends
                backends = [
                    cv2.CAP_DSHOW,  # DirectShow (Windows)
                    cv2.CAP_MSMF,   # Microsoft Media Foundation
                    cv2.CAP_ANY     # Auto-detect
                ]
            
            camera = None
            for backend in backends:
                try:
                    print(f"Trying to connect to camera {camera_index} with backend {backend}...")
                    camera = cv2.VideoCapture(camera_index, backend)
                    
                    # Wait for camera to initialize (up to 5 seconds)
                    import time
                    start_time = time.time()
                    while not camera.isOpened() and time.time() - start_time < 5:
                        time.sleep(0.1)
                    
                    if camera.isOpened():
                        print(f"Camera opened with backend {backend}, testing frame read...")
                        # Test if we can actually read a frame
                        try:
                            ret, test_frame = camera.read()
                            if ret and test_frame is not None:
                                self.camera = camera
                                print(f"Camera {camera_index} connected successfully with backend {backend}")
                                break
                            else:
                                print(f"Camera opened but frame read failed with backend {backend}")
                                camera.release()
                        except Exception as e:
                            print(f"Frame read test failed with backend {backend}: {e}")
                            camera.release()
                    else:
                        print(f"Failed to open camera with backend {backend}")
                        if camera:
                            camera.release()
                except Exception as e:
                    print(f"Backend {backend} failed: {e}")
                    if camera:
                        try:
                            camera.release()
                        except:
                            pass
            
            if self.camera is None or not self.camera.isOpened():
                print(f"Failed to connect to camera {camera_index} with any backend")
                self.error_occurred.emit(f"Failed to connect to camera {camera_index}")
                return False
                
            # Set camera properties for better performance (with error handling)
            try:
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                self.camera.set(cv2.CAP_PROP_FPS, 30)
                self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            except Exception as e:
                print(f"Warning: Could not set camera properties: {e}")
            
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
            try:
                # Set switching flag to prevent frame reading
                self.is_switching = True
                
                # Force release the current camera
                if self.camera is not None:
                    try:
                        self.camera.release()
                        self.camera = None
                    except Exception as e:
                        print(f"Error releasing camera during switch: {e}")
                
                # Update the current camera index
                self.current_camera_index = camera_index
                
                # Connect to the new camera immediately
                success = self.connect_camera(camera_index)
                if not success:
                    print(f"Failed to connect to camera {camera_index}")
                else:
                    # Add a small delay to let the camera stabilize
                    import time
                    time.sleep(0.5)
                
                # Clear switching flag
                self.is_switching = False
                    
            except Exception as e:
                print(f"Error during camera switch: {e}")
                import traceback
                traceback.print_exc()
                # Reset to a safe state
                self.current_camera_index = 0
                if self.camera is not None:
                    try:
                        self.camera.release()
                        self.camera = None
                    except:
                        pass
            
    def get_camera_capabilities(self, camera_index: int, backend) -> Dict[str, any]:
        """Get detailed camera capabilities including framerates."""
        capabilities = {}
        cap = None
        try:
            cap = cv2.VideoCapture(camera_index, backend)
            
            # Add timeout for camera opening
            import time
            start_time = time.time()
            while not cap.isOpened() and time.time() - start_time < 3:  # 3 second timeout
                time.sleep(0.1)
            
            if cap.isOpened():
                # Get basic properties
                try:
                    capabilities['width'] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    capabilities['height'] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    capabilities['fps'] = int(cap.get(cv2.CAP_PROP_FPS))
                    capabilities['backend'] = backend
                except Exception as e:
                    print(f"Error getting basic camera properties: {e}")
                    capabilities['width'] = 0
                    capabilities['height'] = 0
                    capabilities['fps'] = 0
                    capabilities['backend'] = backend
                
                # Test different resolution and framerate combinations
                try:
                    # Reduced test combinations for faster detection
                    test_combinations = [
                        (1920, 1080, 30),  # 1080p @ 30fps
                        (1280, 720, 30),   # 720p @ 30fps
                        (640, 480, 30)     # 480p @ 30fps
                    ]
                    
                    supported_combinations = []
                    
                    for width, height, fps in test_combinations:
                        try:
                            # Set resolution and framerate
                            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                            cap.set(cv2.CAP_PROP_FPS, fps)
                            
                            # Get actual values
                            actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            actual_fps = int(cap.get(cv2.CAP_PROP_FPS))
                            
                            # More lenient validation for faster detection
                            width_match = abs(actual_width - width) <= 50  # Allow larger tolerance
                            height_match = abs(actual_height - height) <= 50  # Allow larger tolerance
                            fps_match = abs(actual_fps - fps) <= 10  # Allow larger tolerance for FPS
                            
                            # Only add if the camera actually supports this combination
                            if width_match and height_match and fps_match:
                                combination = {
                                    'width': actual_width,
                                    'height': actual_height,
                                    'fps': actual_fps,
                                    'display_name': f"{actual_width}x{actual_height} @ {actual_fps}fps"
                                }
                                supported_combinations.append(combination)
                                
                        except Exception as e:
                            print(f"Error testing {width}x{height} @ {fps}fps: {e}")
                            continue
                    
                    # Use the supported combinations directly without frame reading verification
                    # This is more stable and prevents crashes during camera switching
                    capabilities['supported_combinations'] = supported_combinations
                    
                    # Also keep the old format for backward compatibility
                    resolutions = list(set([f"{c['width']}x{c['height']}" for c in supported_combinations]))
                    capabilities['supported_resolutions'] = resolutions
                    
                except Exception as e:
                    print(f"Error testing resolution/framerate combinations: {e}")
                    capabilities['supported_combinations'] = []
                    capabilities['supported_resolutions'] = []
                    
        except Exception as e:
            print(f"Error getting camera capabilities: {e}")
        finally:
            if cap is not None:
                try:
                    cap.release()
                except Exception as e:
                    print(f"Error releasing camera: {e}")
            
        return capabilities
            
    def get_available_cameras(self) -> List[str]:
        """Get list of available cameras with detailed information."""
        cameras = []
        self.camera_details = {}
        
        try:
            # Get Windows camera names
            windows_camera_names = self.get_windows_camera_names()
            
            # Try to find cameras by testing indices 0-2 (most systems have 1-2 cameras)
            for i in range(3):
                try:
                    # Try DirectShow first (most common on Windows)
                    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
                    if cap.isOpened():
                        ret, frame = cap.read()
                        if ret and frame is not None:
                            # Get camera capabilities
                            capabilities = self.get_camera_capabilities(i, cv2.CAP_DSHOW)
                            
                            # Get camera name from Windows or use default
                            camera_name = windows_camera_names.get(i, f"Camera {i}")
                            
                            # Create detailed camera info
                            width = capabilities.get('width', 0)
                            height = capabilities.get('height', 0)
                            fps = capabilities.get('fps', 0)
                            resolutions = capabilities.get('supported_resolutions', [])
                            
                            # Format camera display name
                            if width > 0 and height > 0:
                                if fps > 0:
                                    display_name = f"{camera_name} ({width}x{height} @ {fps}fps)"
                                else:
                                    display_name = f"{camera_name} ({width}x{height})"
                            else:
                                display_name = f"{camera_name} (Camera {i})"
                                
                            cameras.append(display_name)
                            
                            # Store detailed information
                            self.camera_details[i] = {
                                'name': camera_name,
                                'index': i,
                                'backend': cv2.CAP_DSHOW,
                                'capabilities': capabilities,
                                'display_name': display_name
                            }
                            
                        cap.release()
                        
                except Exception as e:
                    print(f"Error testing camera {i} with DirectShow: {e}")
                    
            # If no cameras found with DirectShow, try MSMF
            if not cameras:
                for i in range(3):
                    try:
                        cap = cv2.VideoCapture(i, cv2.CAP_MSMF)
                        if cap.isOpened():
                            ret, frame = cap.read()
                            if ret and frame is not None:
                                capabilities = self.get_camera_capabilities(i, cv2.CAP_MSMF)
                                
                                camera_name = windows_camera_names.get(i, f"Camera {i}")
                                
                                width = capabilities.get('width', 0)
                                height = capabilities.get('height', 0)
                                fps = capabilities.get('fps', 0)
                                
                                if width > 0 and height > 0:
                                    if fps > 0:
                                        display_name = f"{camera_name} ({width}x{height} @ {fps}fps) [MSMF]"
                                    else:
                                        display_name = f"{camera_name} ({width}x{height}) [MSMF]"
                                else:
                                    display_name = f"{camera_name} (Camera {i}) [MSMF]"
                                    
                                cameras.append(display_name)
                                
                                self.camera_details[i] = {
                                    'name': camera_name,
                                    'index': i,
                                    'backend': cv2.CAP_MSMF,
                                    'capabilities': capabilities,
                                    'display_name': display_name
                                }
                                
                            cap.release()
                    except Exception as e:
                        print(f"Error testing camera {i} with MSMF: {e}")
                        
        except Exception as e:
            print(f"Error in get_available_cameras: {e}")
                
        self.available_cameras = cameras
        
        # Fallback: if no cameras found with detailed detection, try simple detection
        if not cameras:
            print("No cameras found with detailed detection, trying simple fallback...")
            for i in range(3):  # Try fewer cameras for fallback
                try:
                    cap = cv2.VideoCapture(i)
                    if cap.isOpened():
                        ret, frame = cap.read()
                        if ret and frame is not None:
                            display_name = f"Camera {i} (Basic Detection)"
                            cameras.append(display_name)
                            
                            self.camera_details[i] = {
                                'name': f"Camera {i}",
                                'index': i,
                                'backend': cv2.CAP_ANY,
                                'capabilities': {
                                    'width': frame.shape[1],
                                    'height': frame.shape[0],
                                    'fps': 30,
                                    'supported_resolutions': []
                                },
                                'display_name': display_name
                            }
                        cap.release()
                except Exception as e:
                    print(f"Fallback camera detection failed for camera {i}: {e}")
                    
        return cameras
        
    def get_camera_info(self, camera_index: int) -> Optional[Dict]:
        """Get detailed information about a specific camera."""
        return self.camera_details.get(camera_index)
        
    def stop(self):
        """Stop the camera thread."""
        self.is_running = False
        self.wait()  # Wait for thread to finish
        
    def get_current_frame(self) -> Optional[np.ndarray]:
        """Get the current frame from camera (for recording)."""
        if self.camera is not None and self.camera.isOpened():
            try:
                ret, frame = self.camera.read()
                if ret and frame is not None:
                    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except Exception as e:
                print(f"Error reading frame: {e}")
        return None
        
    def get_camera_fps(self) -> float:
        """Get the actual FPS of the connected camera."""
        if self.camera is not None and self.camera.isOpened():
            try:
                # First, try to get the reported FPS
                fps = self.camera.get(cv2.CAP_PROP_FPS)
                print(f"Camera reported FPS: {fps}")
                
                # If FPS is 0 or invalid, use a reasonable default based on camera capabilities
                if fps <= 0 or fps > 120:  # Also check for unreasonably high values
                    # Instead of measuring (which interferes with the main thread),
                    # use a reasonable default based on typical camera capabilities
                    width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
                    height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    
                    # Estimate FPS based on resolution
                    if width >= 1920 or height >= 1080:
                        fps = 30.0  # 1080p typically 30fps
                    elif width >= 1280 or height >= 720:
                        fps = 30.0  # 720p typically 30fps
                    else:
                        fps = 30.0  # Default to 30fps
                    
                    print(f"Using estimated FPS based on resolution: {fps}")
                else:
                    print(f"Using camera reported FPS: {fps}")
                
                # Ensure FPS is within reasonable bounds
                fps = max(15.0, min(60.0, fps))  # Clamp between 15-60 FPS
                return fps
                
            except Exception as e:
                print(f"Error detecting FPS: {e}, using default")
                return 30.0
        return 30.0  # Default fallback
        
    def get_current_camera_index(self) -> int:
        """Get the current camera index."""
        return self.current_camera_index 