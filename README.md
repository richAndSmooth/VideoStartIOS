# Race Timer - Complete Timing System

A Windows 11 desktop application for complete race timing with start signal and finish line integration. This application provides real-time webcam recording with automatic start signal marking and configurable countdown sequences.

## Features

### Current Phase (Phase 1)
- **Desktop Application**: Native Windows 11 desktop app built with PyQt6
- **Camera Integration**: Real-time webcam preview and recording
- **Prerecorded Audio**: High-quality prerecorded audio for start sequence
- **Countdown Sequence**: Configurable 3-2-1-GO countdown with visual and audio cues
- **Automatic Start Marking**: Precise frame marking at start signal
- **Video Recording**: MP4 output with embedded timing markers
- **Offline Functionality**: Fully offline operation (except future webhook feature)

### Future Phase (Phase 2)
- **Webhook Integration**: HTTP server to receive finish line signals
- **Multiple Finish Signals**: Support for different lanes/participants
- **Configurable Endpoints**: Customizable webhook endpoints and authentication

## Installation

### Prerequisites
- Windows 11 (or Windows 10)
- Python 3.8 or higher
- Webcam/camera device

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd VideoStart
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create audio files (optional but recommended)**
   ```bash
   python create_audio_files.py
   ```
   This creates basic audio files. For better quality, record your own voice or use online TTS services.

4. **Run the application**
   ```bash
   python main.py
   ```

#### Quick Start (Windows)
- Double-click `run_race_timer.bat` to automatically install dependencies and start the application

## Audio Setup

The application uses prerecorded audio files for the start sequence. These files should be placed in the `audio/` directory:

### Required Audio Files
- `go_to_start.wav` - "Go to the start" announcement
- `in_position.wav` - "In position" announcement  
- `set.wav` - "Set" announcement
- `start_beep.wav` - Start signal beep

### Creating Audio Files

#### Option 1: Automatic Generation
```bash
python create_audio_files.py
```
This creates basic tone-based audio files.

#### Option 2: Manual Recording
1. Use a voice recorder or audio software
2. Record the phrases clearly and consistently
3. Save as WAV files in the `audio/` directory
4. Ensure consistent volume levels

#### Option 3: Online TTS Services
Use online text-to-speech services to generate professional-quality audio files.

## Usage Guide

### Basic Operation

1. **Launch the Application**
   - Run `python main.py`
   - The application will automatically detect available cameras

2. **Camera Setup**
   - Select your camera from the dropdown menu
   - Click "Refresh" if your camera isn't detected
   - Position your camera to capture the race start line

3. **Configure Settings**
   - Set countdown duration (3-10 seconds)
   - Choose video quality (High/Medium/Low)
   - Enable/disable countdown audio
   - Configure auto-save settings

4. **Start Recording**
   - Click "Start Recording" to begin the countdown sequence
   - The countdown will display: "3... 2... 1... GO!"
   - At "GO!", recording automatically starts and marks the start frame
   - The start time is precisely captured and displayed

5. **Stop Recording**
   - Click "Stop Recording" when the race is finished
   - The finish time is marked and duration is calculated
   - Video is automatically saved with timing markers

### Advanced Features

#### Timing Markers
- **Start Marker**: Automatically added to the first frame with timestamp
- **Finish Marker**: Added when recording stops
- **Duration Calculation**: Precise timing between start and finish
- **Metadata File**: JSON file with complete timing information

#### Video Output
- **Format**: MP4 with H.264 encoding
- **Quality Options**: 
  - High: 1920x1080 @ 30fps
  - Medium: 1280x720 @ 30fps
  - Low: 854x480 @ 30fps
- **File Location**: `~/Pictures/RaceTimer/` directory with timestamped filenames

#### Recent Recordings
- View list of recent recordings with timing information
- Access to start time, finish time, and duration for each recording

## File Structure

```
VideoStart/
├── main.py                    # PyQt6 application entry point
├── race_timer_app.py          # PyQt6 main application window
├── camera_thread.py           # Camera capture thread
├── countdown_widget.py        # PyQt6 countdown display widget
├── video_recorder.py          # Video recording and markers
├── timing_markers.py          # Timing data management
├── config_manager.py          # Configuration management
├── webhook_server.py          # Webhook server for future features
├── requirements.txt           # PyQt6 dependencies
├── run_race_timer.bat         # Windows batch launcher
├── test_installation.py       # Installation test script
├── create_audio_files.py      # Audio file creation script
├── README.md                  # This file
├── audio/                     # Prerecorded audio files
│   ├── go_to_start.wav
│   ├── in_position.wav
│   ├── set.wav
│   └── start_beep.wav
└── config.json                # Application configuration
```

**Note**: Video recordings are automatically saved to `~/Pictures/RaceTimer/` directory.

## Configuration

The application automatically creates a `config.json` file with default settings. You can modify these settings:

### Camera Settings
- Default camera selection
- Resolution and frame rate
- Auto-connect behavior

### Recording Settings
- Default video quality
- Countdown duration
- Audio preferences
- Output directory (defaults to ~/Pictures/RaceTimer/)

### Webhook Settings (Future)
- Server port and endpoint
- Authentication configuration
- Enable/disable webhook server

## Troubleshooting

### Camera Issues
- **No cameras detected**: Ensure your webcam is connected and not in use by another application
- **Poor video quality**: Try different quality settings or check camera drivers
- **Camera not responding**: Click "Refresh" or restart the application

### Audio Issues
- **No audio during countdown**: Check that audio files exist in the `audio/` directory
- **Audio files missing**: Run `python create_audio_files.py` to generate basic audio files
- **Poor audio quality**: Replace generated audio files with higher quality recordings

### Recording Issues
- **Video not saving**: Check available disk space and write permissions
- **Poor performance**: Lower video quality or close other applications

### General Issues
- **Application crashes**: Check Python version compatibility
- **Missing dependencies**: Run `pip install -r requirements.txt`
- **Permission errors**: Run as administrator if needed

## Development

### Architecture Overview
- **Modular Design**: Each component is separate for easy maintenance
- **Thread-Safe**: Camera operations run in separate thread
- **Extensible**: Easy to add webhook functionality in future
- **Configurable**: All settings stored in JSON configuration

### Adding Features
1. **Webhook Integration**: Extend `config_manager.py` and add webhook server
2. **Audio Support**: Integrate text-to-speech in `countdown_widget.py`
3. **Multiple Cameras**: Enhance `camera_thread.py` for multi-camera support
4. **Advanced Timing**: Extend `timing_markers.py` for complex race formats

### Building Distribution
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed main.py
```

## License

This project is provided as-is for educational and personal use.

## Support

For issues and feature requests, please check the troubleshooting section above or create an issue in the project repository.

## Future Enhancements

- **Webhook Server**: HTTP endpoint for finish line integration
- **Audio Integration**: Text-to-speech countdown and sound effects
- **Multi-Camera Support**: Simultaneous recording from multiple cameras
- **Advanced Timing**: Support for complex race formats and multiple participants
- **Cloud Integration**: Upload recordings and timing data to cloud services
- **Mobile App**: Companion app for remote control and monitoring 