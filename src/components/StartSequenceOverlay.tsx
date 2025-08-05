import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
} from 'react-native';
import { useConfig } from '../context/ConfigContext';
import { AudioManager } from '../services/AudioManager';

interface StartSequenceOverlayProps {
  onComplete: (startTime: number) => void;
  onCancel: () => void;
  audioManager: AudioManager;
}

type SequencePhase = 'countdown' | 'go_to_start' | 'in_position' | 'set' | 'start' | 'completed';

const StartSequenceOverlay: React.FC<StartSequenceOverlayProps> = ({
  onComplete,
  onCancel,
  audioManager,
}) => {
  const config = useConfig();
  const [phase, setPhase] = useState<SequencePhase>('countdown');
  const [countdown, setCountdown] = useState(3);
  const [phaseText, setPhaseText] = useState('Get Ready');
  const scaleAnim = new Animated.Value(1);

  useEffect(() => {
    startSequence();
  }, []);

  const startSequence = async () => {
    // Initial countdown (3, 2, 1)
    for (let i = 3; i >= 1; i--) {
      setCountdown(i);
      animateScale();
      await delay(1000);
    }

    // Go to start phase
    setPhase('go_to_start');
    setPhaseText('Go to the start');
    if (config.startSequenceConfig.audioEnabled) {
      await audioManager.playAudio('go_to_start');
    }
    await delay(config.startSequenceConfig.goToStartDuration * 1000);

    // In position phase
    setPhase('in_position');
    setPhaseText('In position');
    if (config.startSequenceConfig.audioEnabled) {
      await audioManager.playAudio('in_position');
    }
    const inPositionDelay = randomDelay(
      config.startSequenceConfig.inPositionMin,
      config.startSequenceConfig.inPositionMax
    );
    await delay(inPositionDelay);

    // Set phase
    setPhase('set');
    setPhaseText('Set');
    if (config.startSequenceConfig.audioEnabled) {
      await audioManager.playAudio('set');
    }
    const setDelay = randomDelay(
      config.startSequenceConfig.setMin,
      config.startSequenceConfig.setMax
    );
    await delay(setDelay);

    // START!
    setPhase('start');
    setPhaseText('GO!');
    const startTime = performance.now();
    
    if (config.startSequenceConfig.audioEnabled) {
      await audioManager.playAudio('start_beep');
    }
    
    animateScale();
    
    // Complete sequence
    setTimeout(() => {
      setPhase('completed');
      onComplete(startTime);
    }, 500);
  };

  const randomDelay = (min: number, max: number): number => {
    return (Math.random() * (max - min) + min) * 1000;
  };

  const delay = (ms: number): Promise<void> => {
    return new Promise(resolve => setTimeout(resolve, ms));
  };

  const animateScale = () => {
    scaleAnim.setValue(1.5);
    Animated.spring(scaleAnim, {
      toValue: 1,
      useNativeDriver: true,
      tension: 100,
      friction: 5,
    }).start();
  };

  const getPhaseColor = (): string => {
    switch (phase) {
      case 'countdown':
        return '#FFC107'; // Amber
      case 'go_to_start':
        return '#2196F3'; // Blue
      case 'in_position':
        return '#FF9800'; // Orange
      case 'set':
        return '#f44336'; // Red
      case 'start':
        return '#4CAF50'; // Green
      default:
        return '#FFFFFF';
    }
  };

  const getDisplayText = (): string => {
    if (phase === 'countdown') {
      return countdown.toString();
    }
    return phaseText;
  };

  return (
    <View style={styles.overlay}>
      <View style={styles.container}>
        <Animated.View 
          style={[
            styles.textContainer,
            { 
              transform: [{ scale: scaleAnim }],
              backgroundColor: getPhaseColor() + '20', // 20% opacity
              borderColor: getPhaseColor(),
            }
          ]}
        >
          <Text style={[styles.phaseText, { color: getPhaseColor() }]}>
            {getDisplayText()}
          </Text>
        </Animated.View>

        <TouchableOpacity style={styles.cancelButton} onPress={onCancel}>
          <Text style={styles.cancelButtonText}>Cancel</Text>
        </TouchableOpacity>
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
    backgroundColor: 'rgba(0, 0, 0, 0.9)',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  },
  container: {
    alignItems: 'center',
  },
  textContainer: {
    width: 200,
    height: 200,
    borderRadius: 100,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 4,
    marginBottom: 60,
  },
  phaseText: {
    fontSize: 36,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  cancelButton: {
    paddingHorizontal: 24,
    paddingVertical: 12,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.3)',
  },
  cancelButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '500',
  },
});

export default StartSequenceOverlay; 