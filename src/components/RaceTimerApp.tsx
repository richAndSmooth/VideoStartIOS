import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  Dimensions,
  Alert,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import CameraView from './CameraView';
import ControlPanel from './ControlPanel';
import StatusPanel from './StatusPanel';
import SettingsPanel from './SettingsPanel';
import StartSequenceOverlay from './StartSequenceOverlay';
import { useCamera } from '../context/CameraContext';
import { useConfig } from '../context/ConfigContext';
import { TimingMarkers } from '../services/TimingMarkers';
import { AudioManager } from '../services/AudioManager';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

// iPhone 11 Pro Max specific dimensions
const IPHONE_11_PRO_MAX_WIDTH = 414;
const IPHONE_11_PRO_MAX_HEIGHT = 896;

const RaceTimerApp: React.FC = () => {
  const insets = useSafeAreaInsets();
  const camera = useCamera();
  const config = useConfig();
  
  const [currentView, setCurrentView] = useState<'camera' | 'settings'>('camera');
  const [isSequenceActive, setIsSequenceActive] = useState(false);
  const [recordingState, setRecordingState] = useState<'idle' | 'recording' | 'finished'>('idle');
  const [timingMarkers] = useState(() => new TimingMarkers());
  const [audioManager] = useState(() => new AudioManager());

  useEffect(() => {
    initializeApp();
    return () => {
      cleanup();
    };
  }, []);

  const initializeApp = async () => {
    try {
      // Request camera permissions
      const hasPermissions = await camera.requestPermissions();
      if (!hasPermissions) {
        Alert.alert(
          'Permissions Required',
          'Camera and microphone permissions are required for this app to function.',
          [{ text: 'OK' }]
        );
        return;
      }

      // Initialize camera
      const devices = camera.getAvailableDevices();
      const backCamera = devices.find(device => device.position === 'back');
      
      if (backCamera) {
        camera.setDevice(backCamera);
        const bestFormat = camera.findBestFormat(backCamera, config.videoQuality.fps);
        if (bestFormat) {
          camera.setFormat(bestFormat);
        }
        camera.setIsActive(true);
      }

      // Initialize audio
      await audioManager.initialize();
      
    } catch (error) {
      console.error('Failed to initialize app:', error);
      Alert.alert('Initialization Error', 'Failed to initialize the app. Please try again.');
    }
  };

  const cleanup = () => {
    camera.setIsActive(false);
    audioManager.cleanup();
  };

  const handleStartSequence = async () => {
    if (isSequenceActive || recordingState === 'recording') return;

    try {
      setIsSequenceActive(true);
      setRecordingState('recording');
      
      // This will trigger the StartSequenceOverlay
    } catch (error) {
      console.error('Failed to start sequence:', error);
      setIsSequenceActive(false);
      setRecordingState('idle');
    }
  };

  const handleStopRecording = () => {
    if (recordingState !== 'recording') return;
    
    setRecordingState('finished');
    setIsSequenceActive(false);
    
    // Mark finish time
    const finishTime = performance.now();
    timingMarkers.setFinishTime(finishTime);
  };

  const handleSequenceComplete = (startTime: number) => {
    timingMarkers.setStartTime(startTime);
    // Recording continues after sequence completion
  };

  const handleSequenceCancelled = () => {
    setIsSequenceActive(false);
    setRecordingState('idle');
  };

  // Optimize layout for iPhone 11 Pro Max
  const isOptimalSize = screenWidth === IPHONE_11_PRO_MAX_WIDTH && 
                       screenHeight === IPHONE_11_PRO_MAX_HEIGHT;

  const styles = createStyles(insets, isOptimalSize);

  return (
    <View style={styles.container}>
      {currentView === 'camera' ? (
        <>
          <CameraView 
            style={styles.cameraContainer}
            isRecording={recordingState === 'recording'}
            timingMarkers={timingMarkers}
          />
          
          <ControlPanel
            style={styles.controlPanel}
            onStartSequence={handleStartSequence}
            onStopRecording={handleStopRecording}
            onOpenSettings={() => setCurrentView('settings')}
            recordingState={recordingState}
            isSequenceActive={isSequenceActive}
          />
          
          <StatusPanel
            style={styles.statusPanel}
            recordingState={recordingState}
            timingMarkers={timingMarkers}
          />
        </>
      ) : (
        <SettingsPanel
          onBack={() => setCurrentView('camera')}
        />
      )}
      
      {isSequenceActive && (
        <StartSequenceOverlay
          onComplete={handleSequenceComplete}
          onCancel={handleSequenceCancelled}
          audioManager={audioManager}
        />
      )}
    </View>
  );
};

const createStyles = (insets: any, isOptimalSize: boolean) => 
  StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#1a1a1a',
      paddingTop: insets.top,
      paddingBottom: insets.bottom,
    },
    cameraContainer: {
      flex: 1,
      marginHorizontal: isOptimalSize ? 16 : 12,
      marginTop: 16,
      borderRadius: 12,
      overflow: 'hidden',
      backgroundColor: '#000',
    },
    controlPanel: {
      paddingHorizontal: isOptimalSize ? 20 : 16,
      paddingVertical: 16,
    },
    statusPanel: {
      paddingHorizontal: isOptimalSize ? 20 : 16,
      paddingBottom: 8,
    },
  });

export default RaceTimerApp; 