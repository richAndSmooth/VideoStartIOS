#!/usr/bin/env python3
"""
Test script to verify the FPS fix for 2x speed playback issue.
This script tests that videos are recorded at the correct frame rate.
"""

import cv2
import numpy as np
import time
import os
from datetime import datetime
from camera_thread import CameraThread

def test_fps_measurement():
    """Test the new FPS measurement functionality."""
    print("=== Testing FPS Measurement Fix ===")
    
    camera_thread = CameraThread()
    camera_thread.start()
    
    # Wait for camera to initialize
    time.sleep(2)
    
    try:
        # Test the old method (for comparison)
        print("\n1. Testing camera reported FPS...")
        reported_fps = 30.0  # Default value
        if camera_thread.camera and camera_thread.camera.isOpened():
            reported_fps = camera_thread.camera.get(cv2.CAP_PROP_FPS)
            print(f"Camera reported FPS: {reported_fps}")
        else:
            print("Camera not available for reported FPS test")
        
        # Test the new measurement method
        print("\n2. Testing new FPS measurement...")
        measured_fps = camera_thread.get_camera_fps()
        print(f"New measured FPS: {measured_fps:.2f}")
        
        # Test real-time measurement
        print("\n3. Testing real-time FPS measurement...")
        realtime_fps = camera_thread.measure_real_time_fps(3.0)
        print(f"Real-time measured FPS: {realtime_fps:.2f}")
        
        # Compare results
        print("\n=== Comparison ===")
        print(f"Reported FPS:    {reported_fps:.2f}")
        print(f"Measured FPS:    {measured_fps:.2f}")
        print(f"Real-time FPS:   {realtime_fps:.2f}")
        
        if reported_fps > 0:
            ratio = measured_fps / reported_fps
            print(f"Measurement/Reported ratio: {ratio:.2f}")
            if ratio < 0.8:
                print("⚠️  Camera is lying about FPS! This was causing the 2x speed issue.")
                print("✅ FIX: Now using measured FPS instead of reported FPS")
            else:
                print("✅ Camera FPS reporting seems accurate.")
    
    finally:
        camera_thread.stop()
    
    return measured_fps, realtime_fps

def create_test_video_with_measured_fps():
    """Create a test video using the measured FPS to verify playback speed."""
    print("\n=== Creating Test Video with Measured FPS ===")
    
    camera_thread = CameraThread()
    camera_thread.start()
    time.sleep(2)
    
    try:
        # Measure FPS
        actual_fps = camera_thread.measure_real_time_fps(2.0)
        print(f"Using measured FPS: {actual_fps:.2f}")
        
        # Create test video
        output_path = f"test_fps_fix_{actual_fps:.1f}fps.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # Use the MEASURED FPS for video encoding
        writer = cv2.VideoWriter(output_path, fourcc, actual_fps, (640, 480))
        
        if not writer.isOpened():
            print("Failed to create video writer")
            return None
        
        print(f"Recording test video for 5 seconds at {actual_fps:.2f} FPS...")
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < 5.0:  # Record for 5 seconds
            frame = camera_thread.get_current_frame()
            if frame is not None:
                # Resize and convert frame
                frame_resized = cv2.resize(frame, (640, 480))
                frame_bgr = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2BGR)
                
                # Add frame counter and timestamp
                current_time = time.time() - start_time
                cv2.putText(frame_bgr, f"Frame: {frame_count}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame_bgr, f"Time: {current_time:.2f}s", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame_bgr, f"FPS: {actual_fps:.2f}", (10, 110), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                writer.write(frame_bgr)
                frame_count += 1
            
            # Sleep to match the measured frame rate
            time.sleep(1.0 / actual_fps)
        
        writer.release()
        
        # Analyze the created video
        print(f"\nAnalyzing created video: {output_path}")
        cap = cv2.VideoCapture(output_path)
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        video_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = video_frame_count / video_fps if video_fps > 0 else 0
        
        print(f"Video FPS: {video_fps}")
        print(f"Video frame count: {video_frame_count}")
        print(f"Video duration: {video_duration:.2f}s")
        print(f"Expected duration: ~5.0s")
        
        if abs(video_duration - 5.0) < 0.5:
            print("✅ Video duration is correct - FPS fix working!")
        else:
            print("❌ Video duration mismatch - may still have issues")
        
        cap.release()
        return output_path
        
    except Exception as e:
        print(f"Error creating test video: {e}")
        return None
    finally:
        camera_thread.stop()

def main():
    """Run the FPS fix test."""
    print("Testing FPS Fix for 2x Speed Playback Issue")
    print("=" * 50)
    
    # Test FPS measurement
    measured_fps, realtime_fps = test_fps_measurement()
    
    # Create test video
    test_video = create_test_video_with_measured_fps()
    
    print("\n=== Test Results ===")
    print(f"Measured FPS: {measured_fps:.2f}")
    print(f"Real-time FPS: {realtime_fps:.2f}")
    if test_video:
        print(f"Test video created: {test_video}")
        print("Play this video to verify it plays at normal speed (not 2x)")
    
    print("\n=== Next Steps ===")
    print("1. Test the main application with a real recording")
    print("2. Check that videos now play at normal speed")
    print("3. Verify metadata shows accurate FPS measurements")

if __name__ == "__main__":
    main()