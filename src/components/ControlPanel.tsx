import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ViewStyle,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';

interface ControlPanelProps {
  style?: ViewStyle;
  onStartSequence: () => void;
  onStopRecording: () => void;
  onOpenSettings: () => void;
  recordingState: 'idle' | 'recording' | 'finished';
  isSequenceActive: boolean;
}

const ControlPanel: React.FC<ControlPanelProps> = ({
  style,
  onStartSequence,
  onStopRecording,
  onOpenSettings,
  recordingState,
  isSequenceActive,
}) => {
  const canStart = recordingState === 'idle' && !isSequenceActive;
  const canStop = recordingState === 'recording';

  return (
    <View style={[styles.container, style]}>
      <View style={styles.buttonRow}>
        <TouchableOpacity
          style={[styles.button, styles.startButton, !canStart && styles.disabledButton]}
          onPress={onStartSequence}
          disabled={!canStart}
          activeOpacity={0.8}
        >
          <LinearGradient
            colors={canStart ? ['#4CAF50', '#45a049'] : ['#666666', '#555555']}
            style={styles.gradientButton}
          >
            <Text style={[styles.buttonText, styles.startButtonText]}>
              {isSequenceActive ? 'Starting...' : 'Start Sequence'}
            </Text>
          </LinearGradient>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.stopButton, !canStop && styles.disabledButton]}
          onPress={onStopRecording}
          disabled={!canStop}
          activeOpacity={0.8}
        >
          <LinearGradient
            colors={canStop ? ['#f44336', '#da190b'] : ['#666666', '#555555']}
            style={styles.gradientButton}
          >
            <Text style={[styles.buttonText, styles.stopButtonText]}>
              Stop Recording
            </Text>
          </LinearGradient>
        </TouchableOpacity>
      </View>

      <TouchableOpacity
        style={styles.settingsButton}
        onPress={onOpenSettings}
        activeOpacity={0.7}
      >
        <Text style={styles.settingsButtonText}>⚙️ Settings</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'transparent',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
    gap: 12,
  },
  button: {
    flex: 1,
    height: 56,
    borderRadius: 12,
    overflow: 'hidden',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
  },
  gradientButton: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  startButton: {
    // Additional start button styles
  },
  stopButton: {
    // Additional stop button styles
  },
  disabledButton: {
    opacity: 0.6,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  startButtonText: {
    color: '#FFFFFF',
  },
  stopButtonText: {
    color: '#FFFFFF',
  },
  settingsButton: {
    height: 44,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.2)',
  },
  settingsButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '500',
  },
});

export default ControlPanel; 