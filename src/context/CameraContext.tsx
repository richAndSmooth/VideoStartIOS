import React, { createContext, useContext, useState, useRef, ReactNode } from 'react';
import { Camera, CameraDevice, CameraFormat } from 'react-native-vision-camera';

interface CameraContextType {
  camera: React.RefObject<Camera>;
  device: CameraDevice | undefined;
  format: CameraFormat | undefined;
  isActive: boolean;
  isRecording: boolean;
  hasPermission: boolean;
  setDevice: (device: CameraDevice | undefined) => void;
  setFormat: (format: CameraFormat | undefined) => void;
  setIsActive: (active: boolean) => void;
  setIsRecording: (recording: boolean) => void;
  setHasPermission: (permission: boolean) => void;
  requestPermissions: () => Promise<boolean>;
  getAvailableDevices: () => CameraDevice[];
  findBestFormat: (device: CameraDevice, targetFps: number) => CameraFormat | undefined;
}

const CameraContext = createContext<CameraContextType | undefined>(undefined);

interface CameraProviderProps {
  children: ReactNode;
}

export const CameraProvider: React.FC<CameraProviderProps> = ({ children }) => {
  const camera = useRef<Camera>(null);
  const [device, setDevice] = useState<CameraDevice | undefined>(undefined);
  const [format, setFormat] = useState<CameraFormat | undefined>(undefined);
  const [isActive, setIsActive] = useState<boolean>(false);
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [hasPermission, setHasPermission] = useState<boolean>(false);

  const requestPermissions = async (): Promise<boolean> => {
    try {
      const cameraPermission = await Camera.requestCameraPermission();
      const microphonePermission = await Camera.requestMicrophonePermission();
      
      const granted = cameraPermission === 'authorized' && microphonePermission === 'authorized';
      setHasPermission(granted);
      return granted;
    } catch (error) {
      console.error('Permission request failed:', error);
      setHasPermission(false);
      return false;
    }
  };

  const getAvailableDevices = (): CameraDevice[] => {
    try {
      return Camera.getAvailableCameraDevices();
    } catch (error) {
      console.error('Failed to get camera devices:', error);
      return [];
    }
  };

  const findBestFormat = (device: CameraDevice, targetFps: number): CameraFormat | undefined => {
    if (!device.formats) return undefined;

    // Sort formats by preference: 1080p 240fps -> 1080p 120fps -> 720p 240fps -> etc.
    const sortedFormats = device.formats
      .filter(format => 
        format.videoWidth && 
        format.videoHeight && 
        format.maxFps >= targetFps
      )
      .sort((a, b) => {
        // Prefer higher resolution
        const aPixels = (a.videoWidth || 0) * (a.videoHeight || 0);
        const bPixels = (b.videoWidth || 0) * (b.videoHeight || 0);
        
        if (aPixels !== bPixels) {
          return bPixels - aPixels;
        }
        
        // Then prefer higher fps
        return (b.maxFps || 0) - (a.maxFps || 0);
      });

    // Try to find 1080p 240fps first
    const ideal1080p240 = sortedFormats.find(f => 
      f.videoWidth === 1920 && 
      f.videoHeight === 1080 && 
      (f.maxFps || 0) >= 240
    );
    
    if (ideal1080p240) return ideal1080p240;

    // Fallback to best available format
    return sortedFormats[0];
  };

  const value: CameraContextType = {
    camera,
    device,
    format,
    isActive,
    isRecording,
    hasPermission,
    setDevice,
    setFormat,
    setIsActive,
    setIsRecording,
    setHasPermission,
    requestPermissions,
    getAvailableDevices,
    findBestFormat,
  };

  return (
    <CameraContext.Provider value={value}>
      {children}
    </CameraContext.Provider>
  );
};

export const useCamera = (): CameraContextType => {
  const context = useContext(CameraContext);
  if (!context) {
    throw new Error('useCamera must be used within a CameraProvider');
  }
  return context;
}; 