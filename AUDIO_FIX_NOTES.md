# Audio Fix for Race Timer Executable

## Problem Identified
The executable was working perfectly except for the audio functionality during the start sequence. The issue was caused by **PyInstaller path resolution problems**.

## Root Causes
1. **Missing audio file**: `start_beep.wav` was not present in the audio directory
2. **Path resolution**: Hardcoded relative paths like `'audio/file.wav'` don't work in PyInstaller executables because:
   - PyInstaller extracts files to a temporary directory (`sys._MEIPASS`)
   - Relative paths resolve from the current working directory, not the extracted files location

## Solutions Applied

### 1. Generated Missing Audio File
- Ran `python generate_audio_files.py` to create the missing `start_beep.wav`
- Now all required audio files are present:
  - `Go to the start (trump).wav` ✅
  - `In position (trump).wav` ✅
  - `Set (trump).wav` ✅
  - `start_beep.wav` ✅ (newly generated)

### 2. Fixed Path Resolution in Code
Modified `start_sequence_widget.py` to include PyInstaller-compatible path resolution:

```python
def get_resource_path(self, relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
```

This method:
- ✅ Uses `sys._MEIPASS` when running from executable (PyInstaller sets this)
- ✅ Falls back to current directory when running from source
- ✅ Works in both development and production environments

### 3. Updated PyInstaller Configuration
Modified `race_timer.spec` to ensure audio files are properly included:
- Changed from `('audio', 'audio')` to `('audio/*.wav', 'audio')`
- This ensures all WAV files are explicitly included in the executable

## How It Works Now

### In Development (Python source):
- `base_path = os.path.abspath(".")` → Current project directory
- `file_path = ./audio/filename.wav` → Works normally

### In Executable (PyInstaller):
- `base_path = sys._MEIPASS` → Temporary extraction directory (e.g., `C:\Users\...\AppData\Local\Temp\_MEI123\`)
- `file_path = C:\Users\...\AppData\Local\Temp\_MEI123\audio\filename.wav` → Correctly resolves to extracted files

## Testing
The executable has been rebuilt with these fixes. Audio should now work properly during:
- "Go to the start" announcement
- "In position" announcement  
- "Set" announcement
- Start beep sound

## Technical Details
- **Build Method**: `python -m PyInstaller race_timer.spec`
- **File Size**: ~98 MB (includes all audio files)
- **Audio Files Included**: 4 WAV files totaling ~2.8 MB
- **Compatibility**: Windows 10/11 64-bit

## Future Maintenance
If adding new audio files:
1. Place WAV files in the `audio/` directory
2. Update the `audio_files` dictionary in `setup_audio()` method
3. Rebuild executable with `python -m PyInstaller race_timer.spec`

The path resolution will automatically handle both development and production environments.