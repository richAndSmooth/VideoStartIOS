import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
} from 'react-native';
import { useConfig } from '../context/ConfigContext';

interface SettingsPanelProps {
  onBack: () => void;
}

const SettingsPanel: React.FC<SettingsPanelProps> = ({ onBack }) => {
  const config = useConfig();

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={onBack} style={styles.backButton}>
          <Text style={styles.backButtonText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Settings</Text>
      </View>

      <ScrollView style={styles.content}>
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Video Quality</Text>
          <Text style={styles.settingValue}>
            {config.videoQuality.displayName}
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Start Sequence</Text>
          <Text style={styles.settingLabel}>
            Go to start: {config.startSequenceConfig.goToStartDuration}s
          </Text>
          <Text style={styles.settingLabel}>
            Audio: {config.startSequenceConfig.audioEnabled ? 'Enabled' : 'Disabled'}
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Storage</Text>
          <Text style={styles.settingLabel}>
            Auto-save: {config.autoSave ? 'Enabled' : 'Disabled'}
          </Text>
        </View>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a1a',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255, 255, 255, 0.1)',
  },
  backButton: {
    marginRight: 16,
  },
  backButtonText: {
    color: '#4CAF50',
    fontSize: 16,
    fontWeight: '500',
  },
  headerTitle: {
    color: '#FFFFFF',
    fontSize: 20,
    fontWeight: 'bold',
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
  },
  section: {
    marginVertical: 20,
    padding: 16,
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },
  sectionTitle: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 12,
  },
  settingValue: {
    color: '#4CAF50',
    fontSize: 16,
    fontWeight: '500',
  },
  settingLabel: {
    color: '#CCCCCC',
    fontSize: 16,
    marginBottom: 8,
  },
});

export default SettingsPanel; 