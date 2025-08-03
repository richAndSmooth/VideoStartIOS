#!/usr/bin/env python3
"""
Test script to validate video recording FPS and diagnose speed issues.
This script helps identify if the video recording speed issues are resolved.
"""

import cv2
import numpy as np
import time
import os
from datetime import datetime
from video_recorder import VideoRecorder
from camera_thread import CameraThread

def test_camera_fps():
    """Test camera FPS detection."""
    print("=== Camera FPS Test ===")
    
    camera_thread = CameraThread()
    camera_thread.start()
    
    # Wait for camera to initialize
    time.sleep(2)
    
    # Test FPS detection
    fps = camera_thread.get_camera_fps()
    print(f"Detected camera FPS: {fps}")
    
    # Test frame capture timing
    print("\nTesting frame capture timing...")
    frame_count = 0
    start_time = time.time()
    
    for i in range(30):  # Test for 30 frames
        frame = camera_thread.get_current_frame()
        if frame is not None:
            frame_count += 1
        time.sleep(0.033)  # ~30fps
    
    elapsed = time.time() - start_time
    actual_fps = frame_count / elapsed
    print(f"Frame capture test: {actual_fps:.2f} fps over {elapsed:.2f} seconds")
    
    camera_thread.stop()
    return fps, actual_fps

def test_video_recording():
    """Test video recording with different FPS settings."""
    print("\n=== Video Recording Test ===")
    
    # Create test output directory
    test_dir = "test_recordings"
    os.makedirs(test_dir, exist_ok=True)
    
    # Test different FPS values
    test_fps_values = [24.0, 30.0, 60.0]
    
    for fps in test_fps_values:
        print(f"\nTesting recording at {fps} FPS...")
        
        # Create test video recorder
        output_path = os.path.join(test_dir, f"test_{fps}fps.mp4")
        quality = {"width": 640, "height": 480}
        
        recorder = VideoRecorder(output_path, quality, fps)
        
        try:
            recorder.start_recording()
            
            # Record test frames
            frame_count = 0
            start_time = time.time()
            
            for i in range(int(fps * 3)):  # Record 3 seconds worth of frames
                # Create a test frame with frame number
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(frame, f"Frame {i}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, f"FPS: {fps}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                recorder.record_frame(frame)
                frame_count += 1
                
                # Sleep to simulate real frame timing
                time.sleep(1.0 / fps)
            
            recorder.stop_recording()
            
            elapsed = time.time() - start_time
            actual_fps = frame_count / elapsed
            
            print(f"  Expected FPS: {fps}")
            print(f"  Actual FPS: {actual_fps:.2f}")
            print(f"  Frame count: {frame_count}")
            print(f"  Duration: {elapsed:.2f}s")
            print(f"  File: {output_path}")
            
            # Check if metadata file was created
            metadata_path = output_path.replace('.mp4', '_metadata.txt')
            if os.path.exists(metadata_path):
                print(f"  Metadata: {metadata_path}")
                with open(metadata_path, 'r') as f:
                    print("  Metadata contents:")
                    for line in f.readlines()[:10]:  # Show first 10 lines
                        print(f"    {line.strip()}")
            
        except Exception as e:
            print(f"  Error: {e}")

def test_playback_speed():
    """Test video playback speed by analyzing recorded files."""
    print("\n=== Playback Speed Analysis ===")
    
    test_dir = "test_recordings"
    if not os.path.exists(test_dir):
        print("No test recordings found. Run test_video_recording() first.")
        return
    
    for filename in os.listdir(test_dir):
        if filename.endswith('.mp4'):
            filepath = os.path.join(test_dir, filename)
            print(f"\nAnalyzing: {filename}")
            
            # Open video file
            cap = cv2.VideoCapture(filepath)
            
            if not cap.isOpened():
                print(f"  Error: Could not open {filename}")
                continue
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            print(f"  Video FPS: {fps}")
            print(f"  Frame count: {frame_count}")
            print(f"  Resolution: {width}x{height}")
            
            # Calculate expected duration
            expected_duration = frame_count / fps if fps > 0 else 0
            print(f"  Expected duration: {expected_duration:.2f}s")
            
            # Check metadata file
            metadata_path = filepath.replace('.mp4', '_metadata.txt')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = f.read()
                    print(f"  Metadata available: {len(metadata)} characters")
            
            cap.release()

def main():
    """Run all tests."""
    print("Video FPS and Recording Speed Test Suite")
    print("=" * 50)
    
    # Test camera FPS detection
    camera_fps, actual_fps = test_camera_fps()
    
    # Test video recording
    test_video_recording()
    
    # Test playback speed
    test_playback_speed()
    
    print("\n=== Test Summary ===")
    print(f"Camera FPS detection: {camera_fps}")
    print(f"Frame capture timing: {actual_fps:.2f} fps")
    print("Check the 'test_recordings' folder for generated test videos.")
    print("Play the videos to verify playback speed is correct.")

if __name__ == "__main__":
    main() 