#!/usr/bin/env python3
"""
Test script for camera detection functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from camera_thread import CameraThread
import time

def test_camera_detection():
    """Test the camera detection functionality."""
    print("Testing Camera Detection...")
    print("=" * 50)
    
    # Create camera thread
    camera_thread = CameraThread()
    
    # Test camera detection
    print("Detecting available cameras...")
    cameras = camera_thread.get_available_cameras()
    
    if not cameras:
        print("No cameras found!")
        return
    
    print(f"Found {len(cameras)} camera(s):")
    print("-" * 30)
    
    for i, camera_name in enumerate(cameras):
        print(f"{i}: {camera_name}")
        
        # Get detailed camera information
        camera_info = camera_thread.get_camera_info(i)
        if camera_info:
            print(f"   Name: {camera_info.get('name', 'Unknown')}")
            print(f"   Index: {camera_info.get('index', 'Unknown')}")
            print(f"   Backend: {camera_info.get('backend', 'Unknown')}")
            
            capabilities = camera_info.get('capabilities', {})
            if capabilities:
                print(f"   Resolution: {capabilities.get('width', 0)}x{capabilities.get('height', 0)}")
                print(f"   FPS: {capabilities.get('fps', 0)}")
                print(f"   Supported Resolutions: {capabilities.get('supported_resolutions', [])}")
        print()
    
    # Test camera connection
    if cameras:
        print("Testing camera connection...")
        print("-" * 30)
        
        for i in range(len(cameras)):
            print(f"Testing connection to camera {i}...")
            if camera_thread.connect_camera(i):
                print(f"✓ Successfully connected to camera {i}")
                
                # Test frame reading
                frame = camera_thread.get_current_frame()
                if frame is not None:
                    print(f"✓ Successfully read frame from camera {i}")
                    print(f"  Frame shape: {frame.shape}")
                else:
                    print(f"✗ Failed to read frame from camera {i}")
                    
                # Get FPS
                fps = camera_thread.get_camera_fps()
                print(f"  Camera FPS: {fps}")
                
                # Release camera
                if camera_thread.camera:
                    camera_thread.camera.release()
            else:
                print(f"✗ Failed to connect to camera {i}")
            print()
    
    print("Camera detection test completed!")

if __name__ == "__main__":
    test_camera_detection() 