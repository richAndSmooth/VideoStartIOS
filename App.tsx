import React, { useEffect } from 'react';
import {
  SafeAreaProvider,
  initialWindowMetrics,
} from 'react-native-safe-area-context';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { StatusBar, StyleSheet } from 'react-native';
import Orientation from 'react-native-orientation-locker';
import KeepAwake from 'react-native-keep-awake';

import RaceTimerApp from './src/components/RaceTimerApp';
import { ConfigProvider } from './src/context/ConfigContext';
import { CameraProvider } from './src/context/CameraContext';

const App: React.FC = () => {
  useEffect(() => {
    // Lock orientation to portrait for iPhone
    Orientation.lockToPortrait();
    
    // Keep screen awake during app usage
    KeepAwake.activate();
    
    return () => {
      KeepAwake.deactivate();
    };
  }, []);

  return (
    <GestureHandlerRootView style={styles.container}>
      <SafeAreaProvider initialMetrics={initialWindowMetrics}>
        <StatusBar
          barStyle="light-content"
          backgroundColor="#1a1a1a"
          translucent={false}
        />
        <ConfigProvider>
          <CameraProvider>
            <RaceTimerApp />
          </CameraProvider>
        </ConfigProvider>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a1a',
  },
});

export default App; 