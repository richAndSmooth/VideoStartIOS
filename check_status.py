#!/usr/bin/env python3
"""
Quick status check for the Race Timer application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_status():
    """Check the status of the application components."""
    print("Race Timer Application Status Check")
    print("=" * 40)
    
    # Check if required files exist
    required_files = [
        'main.py',
        'race_timer_app.py', 
        'camera_thread.py',
        'config_manager.py',
        'requirements.txt'
    ]
    
    print("Checking required files...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
    
    print("\nChecking camera detection...")
    try:
        from camera_thread import CameraThread
        camera_thread = CameraThread()
        cameras = camera_thread.get_available_cameras()
        
        if cameras:
            print(f"✓ Found {len(cameras)} camera(s)")
            for i, camera in enumerate(cameras):
                print(f"  - {camera}")
        else:
            print("✗ No cameras detected")
            
    except Exception as e:
        print(f"✗ Camera detection failed: {e}")
    
    print("\nChecking configuration...")
    try:
        from config_manager import ConfigManager
        config = ConfigManager()
        print("✓ Configuration manager working")
    except Exception as e:
        print(f"✗ Configuration failed: {e}")
    
    print("\nStatus check completed!")
    print("\nTo start the application, run: python main.py")
    print("Or use the batch file: run_race_timer.bat")

if __name__ == "__main__":
    check_status() 