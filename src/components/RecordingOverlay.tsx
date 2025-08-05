import React from 'react';
import {
  View,
  Text,
  StyleSheet,
} from 'react-native';

interface RecordingOverlayProps {
  frameCount: number;
  targetFps: number;
  measuredFps: number;
  elapsedTime: number;
}

const RecordingOverlay: React.FC<RecordingOverlayProps> = ({
  frameCount,
  targetFps,
  measuredFps,
  elapsedTime,
}) => {
  const formatElapsedTime = (ms: number): string => {
    const seconds = Math.floor(ms / 1000);
    const milliseconds = Math.floor((ms % 1000) / 10);
    return `${seconds.toString().padStart(2, '0')}.${milliseconds.toString().padStart(2, '0')}s`;
  };

  const getFpsColor = (): string => {
    const fpsRatio = measuredFps / targetFps;
    if (fpsRatio >= 0.9) return '#4CAF50'; // Green - good
    if (fpsRatio >= 0.7) return '#FFC107'; // Amber - warning
    return '#f44336'; // Red - poor
  };

  return (
    <View style={styles.overlay}>
      <View style={styles.recordingIndicator}>
        <View style={styles.recordingDot} />
        <Text style={styles.recordingText}>RECORDING</Text>
      </View>

      <View style={styles.statsContainer}>
        <Text style={styles.timeText}>{formatElapsedTime(elapsedTime)}</Text>
        
        <View style={styles.fpsContainer}>
          <Text style={styles.fpsLabel}>FPS:</Text>
          <Text style={[styles.fpsValue, { color: getFpsColor() }]}>
            {measuredFps.toFixed(1)}/{targetFps}
          </Text>
        </View>

        <Text style={styles.frameText}>Frames: {frameCount}</Text>
      </View>

      <View style={styles.warningContainer}>
        <Text style={styles.warningText}>
          🔴 Recording in progress
        </Text>
        <Text style={styles.warningSubtext}>
          Do not move or close the app
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 40,
    paddingHorizontal: 20,
  },
  recordingIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(244, 67, 54, 0.9)',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  recordingDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: '#FFFFFF',
    marginRight: 8,
  },
  recordingText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  statsContainer: {
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    paddingVertical: 20,
    paddingHorizontal: 24,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.2)',
  },
  timeText: {
    color: '#FFFFFF',
    fontSize: 32,
    fontWeight: 'bold',
    fontFamily: 'monospace',
    marginBottom: 12,
  },
  fpsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  fpsLabel: {
    color: '#CCCCCC',
    fontSize: 16,
    marginRight: 8,
  },
  fpsValue: {
    fontSize: 18,
    fontWeight: 'bold',
    fontFamily: 'monospace',
  },
  frameText: {
    color: '#CCCCCC',
    fontSize: 14,
    fontFamily: 'monospace',
  },
  warningContainer: {
    alignItems: 'center',
  },
  warningText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 4,
  },
  warningSubtext: {
    color: '#CCCCCC',
    fontSize: 14,
    textAlign: 'center',
  },
});

export default RecordingOverlay; 