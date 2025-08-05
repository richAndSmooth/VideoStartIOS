# VideoStart React Native

A complete rewrite of the original VideoStart desktop application as a React Native app, specifically optimized for iPhone 11 Pro Max with 1080p @ 240fps video recording capabilities.

## 🏎️ Features

### Current Functionality (Ported from Original)
- ✅ **High-Speed Camera Recording** - 1080p @ 240fps on iPhone 11 Pro Max
- ✅ **Countdown Sequence** - Configurable start sequence with audio cues
- ✅ **Frame-by-Frame Timing** - Precise timing markers for each recorded frame
- ✅ **Audio System** - Prerecorded audio for "Go to start", "In position", "Set", and start beep
- ✅ **Real-time Performance Monitoring** - Live FPS measurement and frame counting
- ✅ **Optimized UI** - iPhone 11 Pro Max specific layout optimization
- ✅ **Configuration Management** - Persistent settings with AsyncStorage

### New Mobile Features
- 📱 **Native iOS Performance** - Direct access to iPhone camera APIs
- 🎯 **Touch-Optimized Interface** - Redesigned for mobile interaction
- 🔋 **Power Management** - Keep screen awake during recording
- 📐 **Orientation Lock** - Portrait mode optimized for race timing
- 💾 **Local Storage** - Videos saved to device photo library

## 🎥 Video Recording Capabilities

| Feature | Specification |
|---------|---------------|
| **Resolution** | 1920x1080 (Full HD) |
| **Frame Rate** | 240 fps (high-speed) |
| **Format** | MP4 with H.264 encoding |
| **Audio** | Synchronized audio recording |
| **Timing Precision** | Frame-accurate timing markers |
| **Performance Monitoring** | Real-time FPS measurement |

## 📱 Device Requirements

### Required Hardware
- **iPhone 11 Pro Max** (specifically required for 240fps support)
- **iOS 15.0+** 
- **Minimum 64GB storage** (high frame rate video files are large)

### Development Requirements
- **macOS** for iOS development
- **Xcode 14+**
- **React Native 0.72+**
- **Physical device** (simulator cannot access camera)

## 🚀 Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd VideoStartRN
   npm install
   cd ios && pod install && cd ..
   ```

2. **Run on iPhone 11 Pro Max**
   ```bash
   npx react-native run-ios --device
   ```

3. **Start Recording**
   - Grant camera permissions
   - Tap "Start Sequence"
   - Follow countdown prompts
   - Recording begins automatically at "GO!"

## 🏗️ Architecture

### Key Components

```
src/
├── components/
│   ├── RaceTimerApp.tsx         # Main application component
│   ├── CameraView.tsx           # 240fps camera with frame processing
│   ├── ControlPanel.tsx         # Start/stop controls
│   ├── StatusPanel.tsx          # Timing information display
│   ├── StartSequenceOverlay.tsx # Countdown sequence UI
│   └── RecordingOverlay.tsx     # Recording status overlay
├── context/
│   ├── CameraContext.tsx        # Camera state management
│   └── ConfigContext.tsx        # Settings and configuration
└── services/
    ├── TimingMarkers.ts         # High-precision timing system
    └── AudioManager.ts          # Audio playback system
```

### Technical Implementation

- **Camera**: `react-native-vision-camera` with frame processor
- **Audio**: `react-native-sound` for sequence audio
- **Storage**: `@react-native-async-storage/async-storage` for settings
- **Timing**: `performance.now()` for microsecond precision
- **UI**: Optimized for iPhone 11 Pro Max dimensions (414×896)

## ⚙️ Configuration

### Start Sequence Settings
```typescript
{
  goToStartDuration: 5,      // seconds
  inPositionMin: 1.0,        // seconds  
  inPositionMax: 3.0,        // seconds
  setMin: 1.0,               // seconds
  setMax: 3.0,               // seconds
  audioEnabled: true         // enable/disable audio cues
}
```

### Video Quality Options
- **Target**: 1080p @ 240fps (optimal for race timing)
- **Fallback**: 1080p @ 120fps (if 240fps unavailable)
- **Alternative**: 720p @ 240fps (if 1080p unavailable)

## 📊 Performance Metrics

### Expected Performance (iPhone 11 Pro Max)
- **Frame Rate**: 240fps sustained
- **Recording Duration**: Limited by storage and thermal throttling
- **File Size**: ~2-4GB per minute at 240fps
- **Battery Life**: ~30-45 minutes continuous recording
- **Timing Precision**: <1ms accuracy

### Real-time Monitoring
- Live FPS measurement during recording
- Frame count tracking
- Elapsed time display
- Performance indicators (green/amber/red)

## 🎯 Race Timing Features

### Precise Start Marking
- Audio cue triggers exact timing marker
- Frame-accurate start time recording
- High-precision `performance.now()` timestamps

### Frame-by-Frame Analysis
- Each frame tagged with race time
- Post-recording frame analysis
- Timing data export capabilities

### Sequence Control
- Professional race start sequence
- Randomized timing for fair starts
- Audio cues with visual feedback

## 🔧 Development

### Setup Instructions
See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for complete setup guide.

### Key Development Commands
```bash
# Start development server
npm start

# Run on iOS device
npx react-native run-ios --device

# Install pods after dependency changes
cd ios && pod install && cd ..

# Clean build
npx react-native clean
```

### Testing
- **Unit tests**: `npm test`
- **Device testing**: Physical iPhone 11 Pro Max required
- **Performance testing**: Monitor FPS and frame timing accuracy

## 📝 Migration from Original

### Ported Features
- ✅ Camera integration with high frame rate support
- ✅ Start sequence with configurable timing
- ✅ Audio system for race announcements
- ✅ Timing markers and race measurement
- ✅ Configuration management
- ✅ Video recording with frame analysis

### New Mobile Enhancements
- 📱 Touch-optimized interface
- 🔐 Native iOS permissions handling
- 💾 Mobile storage management
- 🎯 Device-specific optimizations
- 📐 Orientation and layout management

### Not Yet Implemented
- ⏳ Webhook server integration (future)
- ⏳ Recent recordings management
- ⏳ Advanced settings panel
- ⏳ Video export and sharing

## 🐛 Troubleshooting

### Common Issues

1. **Camera not found**
   - Ensure iPhone 11 Pro Max is being used
   - Check camera permissions in Settings

2. **240fps not available**
   - Verify device model and iOS version
   - Check console for available camera formats

3. **Build failures**
   - Clean project: `npx react-native clean`
   - Reinstall pods: `cd ios && rm -rf Pods && pod install`

See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for detailed troubleshooting.

## 📄 License

This project maintains the same license as the original VideoStart application.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Test on iPhone 11 Pro Max
4. Submit pull request

## 📞 Support

For questions specific to the React Native version:
- Check the setup instructions
- Review troubleshooting guide
- Test on actual iPhone 11 Pro Max hardware

---

**Note**: This app requires iPhone 11 Pro Max for full 240fps functionality. Other devices may have limited capabilities. 