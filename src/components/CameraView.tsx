import React, { useEffect, useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ViewStyle,
  Dimensions,
} from 'react-native';
import {
  Camera,
  useFrameProcessor,
  VideoFile,
} from 'react-native-vision-camera';
import { runOnJS } from 'react-native-reanimated';

import { useCamera } from '../context/CameraContext';
import { useConfig } from '../context/ConfigContext';
import { TimingMarkers } from '../services/TimingMarkers';
import RecordingOverlay from './RecordingOverlay';

interface CameraViewProps {
  style?: ViewStyle;
  isRecording: boolean;
  timingMarkers: TimingMarkers;
}

const { width: screenWidth } = Dimensions.get('window');

const CameraView: React.FC<CameraViewProps> = ({
  style,
  isRecording,
  timingMarkers,
}) => {
  const camera = useCamera();
  const config = useConfig();
  const [frameCount, setFrameCount] = useState(0);
  const [actualFps, setActualFps] = useState(0);
  const frameTimestamps = useRef<number[]>([]);
  const recordingStartTime = useRef<number | null>(null);

  // Frame processor for timing analysis
  const frameProcessor = useFrameProcessor((frame) => {
    'worklet';
    
    if (isRecording && recordingStartTime.current) {
      const currentTime = performance.now();
      const elapsedMs = currentTime - recordingStartTime.current;
      
      runOnJS(() => {
        frameTimestamps.current.push(elapsedMs);
        setFrameCount(prev => prev + 1);
        
        // Calculate actual FPS every 30 frames
        if (frameTimestamps.current.length >= 30) {
          const recent30 = frameTimestamps.current.slice(-30);
          const timeDiff = recent30[29] - recent30[0];
          const measuredFps = 29000 / timeDiff; // 29 intervals over timeDiff ms
          setActualFps(measuredFps);
        }
      })();
    }
  }, [isRecording]);

  useEffect(() => {
    if (isRecording) {
      recordingStartTime.current = performance.now();
      frameTimestamps.current = [];
      setFrameCount(0);
      setActualFps(0);
      startRecording();
    } else if (recordingStartTime.current) {
      stopRecording();
      recordingStartTime.current = null;
    }
  }, [isRecording]);

  const startRecording = async () => {
    if (!camera.camera.current || !camera.device) return;
    
    try {
      await camera.camera.current.startRecording({
        onRecordingFinished: handleRecordingFinished,
        onRecordingError: handleRecordingError,
        fileType: 'mp4',
        videoCodec: 'h264',
      });
      
      camera.setIsRecording(true);
    } catch (error) {
      console.error('Failed to start recording:', error);
    }
  };

  const stopRecording = async () => {
    if (!camera.camera.current) return;
    
    try {
      await camera.camera.current.stopRecording();
      camera.setIsRecording(false);
    } catch (error) {
      console.error('Failed to stop recording:', error);
    }
  };

  const handleRecordingFinished = (video: VideoFile) => {
    console.log('Recording finished:', video.path);
    
    // Save timing data with video
    const timingData = {
      videoPath: video.path,
      startTime: timingMarkers.startTime,
      finishTime: timingMarkers.finishTime,
      duration: timingMarkers.getDuration(),
      frameTimestamps: frameTimestamps.current,
      frameCount,
      targetFps: config.videoQuality.fps,
      measuredFps: actualFps,
    };
    
    // TODO: Save timing data to file system
    console.log('Timing data:', timingData);
  };

  const handleRecordingError = (error: any) => {
    console.error('Recording error:', error);
    camera.setIsRecording(false);
  };

  if (!camera.hasPermission) {
    return (
      <View style={[styles.container, style]}>
        <Text style={styles.errorText}>Camera permission required</Text>
      </View>
    );
  }

  if (!camera.device || !camera.format) {
    return (
      <View style={[styles.container, style]}>
        <Text style={styles.errorText}>Camera not available</Text>
      </View>
    );
  }

  return (
    <View style={[styles.container, style]}>
      <Camera
        ref={camera.camera}
        style={StyleSheet.absoluteFill}
        device={camera.device}
        format={camera.format}
        fps={config.videoQuality.fps}
        isActive={camera.isActive && !isRecording} // Hide preview during recording
        video={true}
        audio={true}
        frameProcessor={frameProcessor}
        pixelFormat="yuv"
        videoStabilizationMode="standard"
        enableZoomGesture={false}
      />
      
      {isRecording && (
        <RecordingOverlay
          frameCount={frameCount}
          targetFps={config.videoQuality.fps}
          measuredFps={actualFps}
          elapsedTime={frameTimestamps.current.length > 0 ? 
            frameTimestamps.current[frameTimestamps.current.length - 1] : 0}
        />
      )}
      
      {!camera.isActive && !isRecording && (
        <View style={styles.inactiveOverlay}>
          <Text style={styles.inactiveText}>Camera Inactive</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    borderRadius: 12,
    overflow: 'hidden',
  },
  errorText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center',
    marginTop: 50,
  },
  inactiveOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  inactiveText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default CameraView; 