import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface StartSequenceConfig {
  goToStartDuration: number;
  inPositionMin: number;
  inPositionMax: number;
  setMin: number;
  setMax: number;
  audioEnabled: boolean;
}

interface VideoQuality {
  width: number;
  height: number;
  fps: number;
  displayName: string;
}

interface ConfigContextType {
  startSequenceConfig: StartSequenceConfig;
  videoQuality: VideoQuality;
  autoSave: boolean;
  updateStartSequenceConfig: (config: Partial<StartSequenceConfig>) => void;
  updateVideoQuality: (quality: VideoQuality) => void;
  setAutoSave: (enabled: boolean) => void;
  loadConfig: () => Promise<void>;
  saveConfig: () => Promise<void>;
}

const defaultStartSequenceConfig: StartSequenceConfig = {
  goToStartDuration: 5,
  inPositionMin: 1.0,
  inPositionMax: 3.0,
  setMin: 1.0,
  setMax: 3.0,
  audioEnabled: true,
};

const defaultVideoQuality: VideoQuality = {
  width: 1920,
  height: 1080,
  fps: 240,
  displayName: '1080p @ 240fps',
};

const ConfigContext = createContext<ConfigContextType | undefined>(undefined);

interface ConfigProviderProps {
  children: ReactNode;
}

export const ConfigProvider: React.FC<ConfigProviderProps> = ({ children }) => {
  const [startSequenceConfig, setStartSequenceConfig] = useState<StartSequenceConfig>(defaultStartSequenceConfig);
  const [videoQuality, setVideoQuality] = useState<VideoQuality>(defaultVideoQuality);
  const [autoSave, setAutoSaveState] = useState<boolean>(true);

  const updateStartSequenceConfig = (config: Partial<StartSequenceConfig>) => {
    setStartSequenceConfig(prev => ({ ...prev, ...config }));
  };

  const updateVideoQuality = (quality: VideoQuality) => {
    setVideoQuality(quality);
  };

  const setAutoSave = (enabled: boolean) => {
    setAutoSaveState(enabled);
  };

  const loadConfig = async () => {
    try {
      const storedConfig = await AsyncStorage.getItem('videostart_config');
      if (storedConfig) {
        const parsed = JSON.parse(storedConfig);
        setStartSequenceConfig(prev => ({ ...prev, ...parsed.startSequenceConfig }));
        setVideoQuality(prev => ({ ...prev, ...parsed.videoQuality }));
        setAutoSaveState(parsed.autoSave ?? true);
      }
    } catch (error) {
      console.error('Failed to load config:', error);
    }
  };

  const saveConfig = async () => {
    try {
      const config = {
        startSequenceConfig,
        videoQuality,
        autoSave,
      };
      await AsyncStorage.setItem('videostart_config', JSON.stringify(config));
    } catch (error) {
      console.error('Failed to save config:', error);
    }
  };

  useEffect(() => {
    loadConfig();
  }, []);

  useEffect(() => {
    saveConfig();
  }, [startSequenceConfig, videoQuality, autoSave]);

  const value: ConfigContextType = {
    startSequenceConfig,
    videoQuality,
    autoSave,
    updateStartSequenceConfig,
    updateVideoQuality,
    setAutoSave,
    loadConfig,
    saveConfig,
  };

  return (
    <ConfigContext.Provider value={value}>
      {children}
    </ConfigContext.Provider>
  );
};

export const useConfig = (): ConfigContextType => {
  const context = useContext(ConfigContext);
  if (!context) {
    throw new Error('useConfig must be used within a ConfigProvider');
  }
  return context;
}; 