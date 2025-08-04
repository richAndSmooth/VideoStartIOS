# Race Timer - Distribution Package

## Executable Information

**File:** `dist/RaceTimer.exe` (98 MB)  
**Type:** Standalone Windows executable  
**Dependencies:** All included (no Python installation required)  

## What's Included

The executable contains:
- Complete Race Timer application
- PyQt6 GUI framework
- OpenCV for camera handling
- NumPy for numerical operations
- All Python runtime dependencies
- Configuration files (`config.json`)
- Audio directory structure
- Documentation files

## How to Distribute

### Option 1: Simple Distribution
Just copy the `dist/RaceTimer.exe` file to the target computer and run it.

### Option 2: Complete Package Distribution
Create a distribution folder with:
```
RaceTimer_Distribution/
├── RaceTimer.exe                 # Main executable
├── RaceTimer_Portable.bat        # Launch helper
├── README.md                     # User documentation
├── INSTALLATION_GUIDE.md         # Setup instructions
├── audio/                        # Audio files directory
└── recordings/                   # Output recordings directory
```

### Option 3: Installer Creation
For professional distribution, consider creating an installer using:
- NSIS (Nullsoft Scriptable Install System)
- Inno Setup
- WiX Toolset
- Advanced Installer

## System Requirements

**Operating System:** Windows 10/11 (64-bit)  
**Memory:** 4 GB RAM minimum, 8 GB recommended  
**Storage:** 200 MB free space  
**Camera:** USB webcam or built-in camera  
**Additional:** Visual C++ Redistributable (usually pre-installed)  

## Running the Application

### Method 1: Direct Execution
Double-click `RaceTimer.exe` to run directly.

### Method 2: Using the Batch Launcher
Double-click `RaceTimer_Portable.bat` for guided startup with error checking.

### Method 3: Command Line
```cmd
cd dist
RaceTimer.exe
```

## Troubleshooting

### Application Won't Start
1. **Antivirus Software:** Some antivirus programs may flag the executable. Add it to exclusions.
2. **Windows Defender:** Right-click → "Run anyway" if SmartScreen appears.
3. **Missing DLLs:** Install Visual C++ Redistributable for Visual Studio 2015-2022.
4. **Permissions:** Run as Administrator if needed.

### Audio Issues (FIXED!)
1. **Audio not playing**: This has been fixed in the latest build with proper PyInstaller path resolution
2. **Audio quality**: The executable includes high-quality prerecorded WAV files  
3. **Audio timing**: Start sequence audio is perfectly synchronized with visual cues

### Camera Issues
1. Ensure camera is connected and not used by other applications
2. Check Windows camera privacy settings
3. Try different USB ports for external cameras

### Performance Issues
1. Close other camera applications
2. Ensure adequate RAM available
3. Use SSD storage for recordings if possible

## File Locations

When running the portable executable:
- **Recordings:** Saved to `~/Pictures/RaceTimer/` by default
- **Configuration:** Embedded in executable, changes are temporary
- **Audio Files:** Embedded in executable
- **Logs:** No log files created (production build)

## Security Notes

- The executable is self-contained and doesn't modify system files
- No network connections made (except webhook feature if enabled)
- Camera access only when explicitly started by user
- All recordings stay local to the user's machine

## Version Information

**Build Date:** $(Get-Date -Format "yyyy-MM-dd")  
**Python Version:** 3.12.x  
**PyQt Version:** 6.4.0+  
**OpenCV Version:** 4.8.0+  

## Support

For technical support or issues:
1. Check the main README.md for application usage
2. Verify system requirements are met
3. Try running from command line to see error messages
4. Check Windows Event Viewer for application errors

---

**Note:** This is a standalone executable build. Source code modifications require rebuilding the executable using PyInstaller.