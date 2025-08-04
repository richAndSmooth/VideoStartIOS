"""
Configuration Manager Module
Handles application settings and preferences.
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime

class ConfigManager:
    """Manages application configuration and settings."""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_default_config()
        self.load_config()
        
    def load_default_config(self) -> Dict[str, Any]:
        """Load default configuration values."""
        return {
            "camera": {
                "default_camera": 0,
                "resolution": "1280x720",
                "fps": 30,
                "auto_connect": True
            },
            "recording": {
                "default_quality": "Medium (720p)",
                "countdown_duration": 3,
                "audio_enabled": True,
                "auto_save": True,
                "output_directory": "~/Pictures/RaceTimer"
            },
            "timing": {
                "precision": "milliseconds",
                "time_format": "24h",
                "auto_clear": False
            },
            "webhook": {
                "enabled": False,
                "port": 8080,
                "endpoint": "/finish",
                "authentication": {
                    "enabled": False,
                    "api_key": ""
                }
            },
            "ui": {
                "theme": "dark",
                "window_size": [1200, 800],
                "window_position": [100, 100],
                "show_tooltips": True
            },
            "advanced": {
                "debug_mode": False,
                "log_level": "INFO",
                "backup_recordings": True,
                "max_recordings": 100
            }
        }
        
    def load_config(self):
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    
                # Merge with default config (preserve defaults for new settings)
                self.merge_config(self.config, loaded_config)
            else:
                # No configuration file found, using defaults
                self.save_config()
                
        except Exception as e:
            pass  # Using default configuration
            
    def save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            pass  # Configuration saved successfully
            
        except Exception as e:
            pass  # Error saving configuration
            
    def merge_config(self, default: Dict[str, Any], loaded: Dict[str, Any]):
        """Recursively merge loaded configuration with defaults."""
        for key, value in loaded.items():
            if key in default:
                if isinstance(value, dict) and isinstance(default[key], dict):
                    self.merge_config(default[key], value)
                else:
                    default[key] = value
            else:
                default[key] = value
                
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation."""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
            
    def set(self, key_path: str, value: Any):
        """Set a configuration value using dot notation."""
        keys = key_path.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
            
        # Set the value
        config[keys[-1]] = value
        
    def get_camera_config(self) -> Dict[str, Any]:
        """Get camera configuration."""
        return self.config["camera"]
        
    def get_recording_config(self) -> Dict[str, Any]:
        """Get recording configuration."""
        return self.config["recording"]
        
    def get_timing_config(self) -> Dict[str, Any]:
        """Get timing configuration."""
        return self.config["timing"]
        
    def get_webhook_config(self) -> Dict[str, Any]:
        """Get webhook configuration."""
        return self.config["webhook"]
        
    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI configuration."""
        return self.config["ui"]
        
    def get_advanced_config(self) -> Dict[str, Any]:
        """Get advanced configuration."""
        return self.config["advanced"]
        
    def update_camera_settings(self, camera_index: int, resolution: str, fps: int):
        """Update camera settings."""
        self.config["camera"]["default_camera"] = camera_index
        self.config["camera"]["resolution"] = resolution
        self.config["camera"]["fps"] = fps
        self.save_config()
        
    def update_recording_settings(self, quality: str, countdown: int, audio: bool, auto_save: bool):
        """Update recording settings."""
        self.config["recording"]["default_quality"] = quality
        self.config["recording"]["countdown_duration"] = countdown
        self.config["recording"]["audio_enabled"] = audio
        self.config["recording"]["auto_save"] = auto_save
        self.save_config()
        
    def update_webhook_settings(self, enabled: bool, port: int, endpoint: str, api_key: str = ""):
        """Update webhook settings."""
        self.config["webhook"]["enabled"] = enabled
        self.config["webhook"]["port"] = port
        self.config["webhook"]["endpoint"] = endpoint
        self.config["webhook"]["authentication"]["enabled"] = bool(api_key)
        self.config["webhook"]["authentication"]["api_key"] = api_key
        self.save_config()
        
    def update_ui_settings(self, theme: str, window_size: list, window_position: list):
        """Update UI settings."""
        self.config["ui"]["theme"] = theme
        self.config["ui"]["window_size"] = window_size
        self.config["ui"]["window_position"] = window_position
        self.save_config()
        
    def reset_to_defaults(self):
        """Reset configuration to default values."""
        self.config = self.load_default_config()
        self.save_config()
        
    def export_config(self, filepath: str):
        """Export configuration to a file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.config, f, indent=2)
            pass  # Configuration exported successfully
            
        except Exception as e:
            pass  # Error exporting configuration
            
    def import_config(self, filepath: str):
        """Import configuration from a file."""
        try:
            with open(filepath, 'r') as f:
                imported_config = json.load(f)
                
            self.merge_config(self.config, imported_config)
            self.save_config()
            pass  # Configuration imported successfully
            
        except Exception as e:
            pass  # Error importing configuration
            
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration."""
        return {
            "camera": {
                "default_camera": self.config["camera"]["default_camera"],
                "resolution": self.config["camera"]["resolution"],
                "fps": self.config["camera"]["fps"]
            },
            "recording": {
                "quality": self.config["recording"]["default_quality"],
                "countdown": self.config["recording"]["countdown_duration"],
                "audio": self.config["recording"]["audio_enabled"]
            },
            "webhook": {
                "enabled": self.config["webhook"]["enabled"],
                "port": self.config["webhook"]["port"]
            },
            "ui": {
                "theme": self.config["ui"]["theme"]
            }
        } 