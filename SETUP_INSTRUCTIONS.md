# VideoStart React Native - Setup Instructions

This document provides step-by-step instructions to set up and run the VideoStart React Native app on iPhone 11 Pro Max with 240fps video recording capabilities.

## Prerequisites

### System Requirements
- **macOS** (required for iOS development)
- **Xcode 14+** with iOS 16+ SDK
- **Node.js 16+**
- **Cocoapods** (for iOS dependencies)
- **iPhone 11 Pro Max** (physical device required for 240fps testing)

### Development Environment Setup

1. **Install Node.js and npm**
   ```bash
   # Using Homebrew
   brew install node
   
   # Or download from https://nodejs.org/
   ```

2. **Install React Native CLI**
   ```bash
   npm install -g react-native-cli
   # OR
   npm install -g @react-native-community/cli
   ```

3. **Install CocoaPods**
   ```bash
   sudo gem install cocoapods
   ```

4. **Install Xcode**
   - Download from Mac App Store
   - Install iOS Simulator and iOS 16+ SDK
   - Accept Xcode license: `sudo xcode-select --install`

## Project Setup

### 1. Initialize React Native Project

```bash
# Create new React Native project
npx react-native init VideoStartRN --version 0.72.6

# Navigate to project directory
cd VideoStartRN
```

### 2. Install Dependencies

```bash
# Install all npm dependencies
npm install

# Install iOS pods
cd ios && pod install && cd ..
```

### 3. Copy Project Files

Copy all the files from this repository into your React Native project:

- `src/` - All source code
- `package.json` - Dependencies
- `App.tsx` - Main app component
- `ios/Podfile` - iOS dependencies

### 4. iOS Configuration

#### Info.plist Configuration

Add these permissions to `ios/VideoStartRN/Info.plist`:

```xml
<dict>
  <!-- Camera Permission -->
  <key>NSCameraUsageDescription</key>
  <string>This app needs camera access to record race videos at high frame rates</string>
  
  <!-- Microphone Permission -->
  <key>NSMicrophoneUsageDescription</key>
  <string>This app needs microphone access to record audio with race videos</string>
  
  <!-- Photo Library Permission (for saving videos) -->
  <key>NSPhotoLibraryUsageDescription</key>
  <string>This app needs photo library access to save recorded race videos</string>
  
  <!-- Prevent app backgrounding during recording -->
  <key>UIBackgroundModes</key>
  <array>
    <string>background-processing</string>
  </array>
  
  <!-- Required device capabilities -->
  <key>UIRequiredDeviceCapabilities</key>
  <array>
    <string>armv7</string>
    <string>camera-flash</string>
    <string>video-camera</string>
  </array>
  
  <!-- Orientation settings -->
  <key>UISupportedInterfaceOrientations</key>
  <array>
    <string>UIInterfaceOrientationPortrait</string>
  </array>
</dict>
```

#### Enable Camera Capabilities in Xcode

1. Open `ios/VideoStartRN.xcworkspace` in Xcode
2. Select your target in the project navigator
3. Go to **Signing & Capabilities**
4. Add **Camera** capability if not present
5. Ensure **Deployment Target** is set to iOS 11.0+

### 5. Metro Configuration

Create/update `metro.config.js`:

```javascript
const {getDefaultConfig, mergeConfig} = require('@react-native/metro-config');

const config = {
  resolver: {
    assetExts: ['bin', 'txt', 'jpg', 'png', 'json', 'wav', 'mp3'],
  },
};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);
```

## Running the App

### 1. Start Metro Bundler

```bash
npm start
# or
npx react-native start
```

### 2. Run on iOS Device

**Important**: You MUST use a physical iPhone 11 Pro Max for 240fps testing. Simulator cannot access camera hardware.

```bash
# Run on connected iOS device
npx react-native run-ios --device
```

### 3. Alternative: Run via Xcode

1. Open `ios/VideoStartRN.xcworkspace` in Xcode
2. Select your iPhone 11 Pro Max as the target device
3. Click the Run button (▶)

## Device Setup

### iPhone 11 Pro Max Configuration

1. **Enable Developer Mode**
   - Go to Settings > Privacy & Security > Developer Mode
   - Enable Developer Mode
   - Restart device when prompted

2. **Trust Developer Certificate**
   - When first running the app, go to Settings > General > Device Management
   - Trust your developer certificate

3. **Camera Permissions**
   - The app will request camera and microphone permissions on first launch
   - Grant all permissions for full functionality

## Testing 240fps Functionality

### Verify High Frame Rate Support

1. Launch the app on iPhone 11 Pro Max
2. Check the status panel - it should display:
   - Target FPS: 240
   - Camera format: 1920x1080 @ 240fps
3. Start a recording and monitor the actual FPS in the recording overlay

### Expected Performance

- **Target**: 1080p @ 240fps
- **File size**: Very large (several GB per minute)
- **Battery usage**: High during recording
- **Heat generation**: Device may get warm during extended recording

## Troubleshooting

### Common Issues

1. **Camera not found**
   - Ensure using physical iPhone 11 Pro Max
   - Check camera permissions in Settings

2. **240fps not available**
   - Verify device model (iPhone 11 Pro Max required)
   - Check available camera formats in console logs

3. **Build errors**
   - Clean and rebuild: `npx react-native clean && cd ios && pod install`
   - Reset Metro cache: `npx react-native start --reset-cache`

4. **Permission denied errors**
   - Check Info.plist permissions
   - Verify app permissions in iPhone Settings

### Debug Information

Enable debug logging by adding to `App.tsx`:

```javascript
// Enable debug logging
console.log('Available camera devices:', camera.getAvailableDevices());
```

## Performance Optimization

### For iPhone 11 Pro Max

1. **Close background apps** before recording
2. **Ensure sufficient storage** (240fps creates large files)
3. **Keep device cool** - high frame rate recording generates heat
4. **Use airplane mode** if network isn't needed during recording

### Recommended Settings

- **Recording duration**: Keep under 30 seconds for testing
- **File management**: Implement automatic cleanup of old recordings
- **Memory monitoring**: Watch for memory warnings during recording

## Production Deployment

### App Store Preparation

1. **Update Info.plist** with production permission descriptions
2. **Add app icons** in appropriate sizes
3. **Configure launch screens** for different device sizes
4. **Test on multiple iOS versions** (iOS 15+)
5. **Implement crash reporting** (e.g., Crashlytics)

### Code Signing

1. Set up Apple Developer account
2. Create App ID with camera capabilities
3. Configure provisioning profiles
4. Set up automatic signing in Xcode

## Next Steps

1. **Test basic functionality** on iPhone 11 Pro Max
2. **Verify 240fps recording** works as expected
3. **Implement additional features** as needed
4. **Optimize for production** deployment

## Support

For issues specific to:
- **React Native**: Check React Native documentation
- **Camera functionality**: See react-native-vision-camera docs
- **iOS development**: Refer to Apple Developer documentation

---

**Note**: This app is specifically optimized for iPhone 11 Pro Max and may not work as expected on other devices due to the 240fps requirement. 