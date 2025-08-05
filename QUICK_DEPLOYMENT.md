# 📱 Quick Deployment to iPhone 11 Pro Max

## Prerequisites Checklist
- [ ] **macOS computer** (required for iOS development)
- [ ] **Xcode 14+** installed from App Store
- [ ] **iPhone 11 Pro Max** with iOS 14+
- [ ] **Apple Developer Account** (free account works for testing)
- [ ] **USB Cable** to connect iPhone to Mac

## 🚀 Step-by-Step Deployment

### 1. Initial Setup (One-time)

```bash
# Install Node.js (if not already installed)
brew install node

# Install React Native CLI
npm install -g @react-native-community/cli

# Install CocoaPods
sudo gem install cocoapods
```

### 2. Project Setup

```bash
# Navigate to your project directory
cd /path/to/VideoStart

# Install dependencies
npm install

# Install iOS dependencies
cd ios && pod install && cd ..
```

### 3. iPhone Preparation

#### Enable Developer Mode:
1. Connect iPhone to Mac via USB
2. Open **Settings** > **Privacy & Security**
3. Scroll down to **Developer Mode** and enable it
4. Restart iPhone when prompted

#### Trust Computer:
1. When connecting iPhone, tap **"Trust This Computer"**
2. Enter iPhone passcode if prompted

### 4. Xcode Configuration

```bash
# Open the iOS project in Xcode
open ios/VideoStartRN.xcworkspace
```

#### In Xcode:
1. **Select your iPhone** from the device dropdown (top toolbar)
2. **Set Bundle Identifier**: 
   - Click on project name in navigator
   - Select "VideoStartRN" target
   - Change Bundle Identifier to something unique like: `com.yourname.videostart`
3. **Set Development Team**:
   - Under "Signing & Capabilities"
   - Select your Apple ID/Team
4. **Camera Permissions**: Already configured in Info.plist ✅

### 5. Deploy to iPhone

```bash
# Method 1: Using React Native CLI (Recommended)
npx react-native run-ios --device "Your iPhone Name"

# Method 2: Using Xcode
# Press the "Play" button in Xcode with your iPhone selected
```

### 6. First Run Setup

#### On iPhone:
1. **Trust Developer**: Go to Settings > General > VPN & Device Management
2. **Find your developer profile** and tap "Trust"
3. **Allow Camera Access** when prompted
4. **Allow Microphone Access** when prompted

## 🎯 Testing 240fps Recording

Once installed:
1. Open VideoStart app
2. Tap **"Start Sequence"**
3. Follow countdown prompts
4. Check recording overlay shows **"240 FPS"** target
5. Verify high frame rate recording in device settings

## 🔧 Troubleshooting

### Common Issues:

#### "Could not find iPhone"
```bash
# List available devices
xcrun xctrace list devices

# Use specific device name
npx react-native run-ios --device "iPhone 11 Pro Max"
```

#### "No development team selected"
- Open Xcode project
- Select project → Target → Signing & Capabilities
- Choose your Apple ID team

#### "Bundle identifier already exists"
- Change Bundle Identifier in Xcode to something unique
- Use format: `com.yourname.videostart.unique`

#### Metro bundler issues:
```bash
# Reset Metro cache
npx react-native start --reset-cache

# Clean and rebuild
cd ios && xcodebuild clean && cd ..
```

## 📋 Verification Checklist

After successful deployment:
- [ ] App launches on iPhone
- [ ] Camera preview shows
- [ ] Can start countdown sequence
- [ ] Audio plays during sequence
- [ ] Recording starts after "Set"
- [ ] Frame rate shows 240fps target
- [ ] Can stop recording
- [ ] Video saves to device

## 🏎️ Performance Notes

- **240fps only available** on rear cameras
- **Ensure good lighting** for optimal frame rates
- **Close other apps** to maximize performance
- **Keep iPhone cool** to prevent thermal throttling

## 🆘 Need Help?

If you encounter issues:
1. Check that iPhone 11 Pro Max is running iOS 14+
2. Verify camera permissions in iPhone Settings
3. Ensure Xcode project builds without errors
4. Try cleaning and rebuilding project 