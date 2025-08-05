import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ViewStyle,
} from 'react-native';
import { TimingMarkers } from '../services/TimingMarkers';

interface StatusPanelProps {
  style?: ViewStyle;
  recordingState: 'idle' | 'recording' | 'finished';
  timingMarkers: TimingMarkers;
}

const StatusPanel: React.FC<StatusPanelProps> = ({
  style,
  recordingState,
  timingMarkers,
}) => {
  const [elapsedTime, setElapsedTime] = useState<string>('00:00.000');

  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (recordingState === 'recording' && timingMarkers.startTime) {
      interval = setInterval(() => {
        const now = performance.now();
        const elapsed = now - timingMarkers.startTime!;
        setElapsedTime(formatElapsedTime(elapsed));
      }, 10); // Update every 10ms for smooth display
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [recordingState, timingMarkers.startTime]);

  const formatElapsedTime = (ms: number): string => {
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    const milliseconds = Math.floor((ms % 1000) / 10); // Show centiseconds

    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${milliseconds.toString().padStart(2, '0')}`;
  };

  const getStatusText = (): string => {
    switch (recordingState) {
      case 'idle':
        return 'Ready';
      case 'recording':
        return 'Recording';
      case 'finished':
        return 'Recording Completed';
      default:
        return 'Unknown';
    }
  };

  const getStatusColor = (): string => {
    switch (recordingState) {
      case 'idle':
        return '#4CAF50'; // Green
      case 'recording':
        return '#f44336'; // Red
      case 'finished':
        return '#2196F3'; // Blue
      default:
        return '#757575'; // Gray
    }
  };

  return (
    <View style={[styles.container, style]}>
      <View style={styles.statusRow}>
        <View style={[styles.statusDot, { backgroundColor: getStatusColor() }]} />
        <Text style={[styles.statusText, { color: getStatusColor() }]}>
          {getStatusText()}
        </Text>
      </View>

      <View style={styles.timingContainer}>
        <View style={styles.timingRow}>
          <Text style={styles.timingLabel}>Elapsed:</Text>
          <Text style={styles.timingValue}>{elapsedTime}</Text>
        </View>

        <View style={styles.timingRow}>
          <Text style={styles.timingLabel}>Start:</Text>
          <Text style={styles.timingValue}>{timingMarkers.getFormattedStartTime()}</Text>
        </View>

        <View style={styles.timingRow}>
          <Text style={styles.timingLabel}>Finish:</Text>
          <Text style={styles.timingValue}>{timingMarkers.getFormattedFinishTime()}</Text>
        </View>

        <View style={styles.timingRow}>
          <Text style={styles.timingLabel}>Duration:</Text>
          <Text style={[styles.timingValue, styles.durationText]}>
            {timingMarkers.getFormattedDuration()}
          </Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  statusDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  statusText: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  timingContainer: {
    gap: 8,
  },
  timingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  timingLabel: {
    fontSize: 16,
    color: '#CCCCCC',
    fontWeight: '500',
  },
  timingValue: {
    fontSize: 16,
    color: '#FFFFFF',
    fontFamily: 'monospace',
    fontWeight: 'bold',
  },
  durationText: {
    color: '#FFC107', // Amber color for duration
    fontSize: 18,
  },
});

export default StatusPanel; 