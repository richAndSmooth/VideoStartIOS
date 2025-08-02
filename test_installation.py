#!/usr/bin/env python3
"""
Test Installation Script
Verifies that all dependencies are properly installed and the application can start.
"""

import sys
import importlib
import subprocess
from pathlib import Path

def test_import(module_name: str, package_name: str = None) -> bool:
    """Test if a module can be imported."""
    try:
        importlib.import_module(module_name)
        print(f"✓ {package_name or module_name} - OK")
        return True
    except ImportError as e:
        print(f"✗ {package_name or module_name} - FAILED: {e}")
        return False

def test_camera_access():
    """Test if camera can be accessed."""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✓ Camera access - OK")
                return True
            else:
                print("✗ Camera access - FAILED: Cannot read frame")
                return False
        else:
            print("✗ Camera access - FAILED: Cannot open camera")
            return False
    except Exception as e:
        print(f"✗ Camera access - FAILED: {e}")
        return False

def test_qt_installation():
    """Test if PyQt6 is properly installed."""
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont
        
        # Create a minimal QApplication to test
        app = QApplication([])
        print("✓ PyQt6 installation - OK")
        return True
    except Exception as e:
        print(f"✗ PyQt6 installation - FAILED: {e}")
        return False

def test_application_modules():
    """Test if all application modules can be imported."""
    modules = [
        ("race_timer_app", "Race Timer App"),
        ("camera_thread", "Camera Thread"),
        ("countdown_widget", "Countdown Widget"),
        ("video_recorder", "Video Recorder"),
        ("timing_markers", "Timing Markers"),
        ("config_manager", "Config Manager"),
        ("webhook_server", "Webhook Server")
    ]
    
    all_ok = True
    for module_name, display_name in modules:
        if not test_import(module_name, display_name):
            all_ok = False
            
    return all_ok

def test_directory_structure():
    """Test if required directories exist or can be created."""
    directories = ["recordings"]
    
    all_ok = True
    for dir_name in directories:
        try:
            path = Path(dir_name)
            path.mkdir(exist_ok=True)
            print(f"✓ Directory '{dir_name}' - OK")
        except Exception as e:
            print(f"✗ Directory '{dir_name}' - FAILED: {e}")
            all_ok = False
            
    return all_ok

def main():
    """Run all installation tests."""
    print("Race Timer - Installation Test")
    print("=" * 40)
    print()
    
    # Test Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro} - OK")
    else:
        print(f"✗ Python {python_version.major}.{python_version.minor}.{python_version.micro} - FAILED: Requires Python 3.8+")
        return False
    
    print()
    print("Testing dependencies...")
    print("-" * 20)
    
    # Test core dependencies
    dependencies = [
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("PyQt6", "PyQt6"),
        ("requests", "Requests")
    ]
    
    all_deps_ok = True
    for module_name, display_name in dependencies:
        if not test_import(module_name, display_name):
            all_deps_ok = False
    
    print()
    print("Testing application modules...")
    print("-" * 20)
    
    # Test application modules
    modules_ok = test_application_modules()
    
    print()
    print("Testing system capabilities...")
    print("-" * 20)
    
    # Test system capabilities
    qt_ok = test_qt_installation()
    camera_ok = test_camera_access()
    dir_ok = test_directory_structure()
    
    print()
    print("Test Results Summary")
    print("=" * 40)
    
    if all_deps_ok and modules_ok and qt_ok and dir_ok:
        print("✓ All tests passed! The application should work correctly.")
        print()
        print("You can now run the application with:")
        print("  python main.py")
        print("  or")
        print("  run_race_timer.bat")
        return True
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print()
        if not all_deps_ok:
            print("To install missing dependencies, run:")
            print("  pip install -r requirements.txt")
        if not camera_ok:
            print("Camera issues may be resolved by:")
            print("  - Ensuring camera is not in use by another application")
            print("  - Checking camera drivers are up to date")
            print("  - Running as administrator if needed")
        return False

if __name__ == "__main__":
    success = main()
    print()
    input("Press Enter to exit...")
    sys.exit(0 if success else 1) 