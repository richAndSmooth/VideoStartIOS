# Race Timer - Installation Guide

This guide provides step-by-step instructions for installing and running the Race Timer application on Windows 11/10.

## Quick Start

### For Most Users
1. **Download the project files**
2. **Double-click `run_race_timer.bat`**
3. **The script will automatically:**
   - Check Python installation
   - Install required dependencies
   - Start the application

### Manual Installation

#### Prerequisites
- **Python 3.8 or higher** - Download from [python.org](https://python.org)
- **Webcam/camera** - Built-in or USB camera
- **Windows 11 or 10** - Tested on Windows 11

#### Step 1: Install Python Dependencies

**Option A: PyQt6 Version (Recommended)**
```bash
pip install -r requirements.txt
```

**Option B: Tkinter Version (Better compatibility)**
```bash
pip install -r requirements_simple.txt
```

#### Step 2: Run the Application

**PyQt6 Version:**
```bash
python main.py
```

**Tkinter Version:**
```bash
python run_tkinter_version.py
```

## Troubleshooting

### Common Issues

#### 1. "Python is not recognized"
**Solution:** Install Python and add it to PATH
- Download Python from [python.org](https://python.org)
- During installation, check "Add Python to PATH"
- Restart your command prompt

#### 2. PyQt6 Installation Fails
**Error:** `OSError: [Errno 2] No such file or directory`
**Solution:** Use the tkinter version instead
```bash
pip install -r requirements_simple.txt
python run_tkinter_version.py
```

#### 3. Camera Not Detected
**Solutions:**
- Ensure camera is not in use by another application
- Check camera drivers are up to date
- Try different camera index (0, 1, 2) in the application
- Run as administrator if needed

#### 4. "Module not found" Errors
**Solution:** Install missing dependencies
```bash
pip install opencv-python numpy requests python-dotenv Pillow
```

#### 5. Video Recording Issues
**Solutions:**
- Check available disk space
- Ensure write permissions to the recordings folder
- Try lower video quality settings
- Close other applications using the camera

### System Requirements

#### Minimum Requirements
- **OS:** Windows 10 (version 1903 or later)
- **Python:** 3.8 or higher
- **RAM:** 4 GB
- **Storage:** 1 GB free space
- **Camera:** Any webcam or USB camera

#### Recommended Requirements
- **OS:** Windows 11
- **Python:** 3.9 or higher
- **RAM:** 8 GB
- **Storage:** 5 GB free space
- **Camera:** HD webcam (720p or higher)

### Performance Tips

1. **Close unnecessary applications** before running the race timer
2. **Use lower video quality** for longer recordings
3. **Ensure good lighting** for better video quality
4. **Position camera properly** to capture the entire race area
5. **Use SSD storage** for better recording performance

### Testing Your Installation

Run the test script to verify everything works:
```bash
python test_installation.py
```

This will check:
- Python version
- Required modules
- Camera access
- Application modules
- Directory permissions

### Getting Help

If you encounter issues:

1. **Check the troubleshooting section above**
2. **Run the test script:** `python test_installation.py`
3. **Check the logs** in the console output
4. **Try the tkinter version** if PyQt6 doesn't work
5. **Ensure your system meets the requirements**

### Advanced Configuration

#### Custom Settings
Edit `config.json` to customize:
- Default camera settings
- Recording quality
- Countdown duration
- Output directory

#### Webhook Setup (Future Feature)
The application includes webhook server functionality for future finish line integration:
- Port: 8080 (configurable)
- Endpoint: `/finish`
- Authentication: API key (optional)

## File Structure

```
VideoStart/
├── main.py                    # PyQt6 application
├── race_timer_tkinter.py      # Tkinter application
├── run_tkinter_version.py     # Tkinter launcher
├── run_race_timer.bat         # Windows launcher
├── test_installation.py       # Installation test
├── requirements.txt           # PyQt6 dependencies
├── requirements_simple.txt    # Tkinter dependencies
├── recordings/                # Video output folder
└── config.json               # Configuration file
```

## Support

For additional support:
- Check the main README.md file
- Review the troubleshooting section
- Test with the installation script
- Try both PyQt6 and tkinter versions

The application is designed to work offline and doesn't require internet connection for basic functionality. 