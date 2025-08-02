#!/usr/bin/env python3
"""
Simple audio test script to verify WAV files can be played.
"""

import os
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl

def test_audio_files():
    """Test if audio files can be loaded and played."""
    app = QApplication(sys.argv)
    
    audio_files = {
        'go_to_start': 'audio/go_to_start.wav',
        'in_position': 'audio/in_position.wav',
        'set': 'audio/set.wav',
        'start_beep': 'audio/start_beep.wav'
    }
    
    effects = {}
    
    print("Testing audio files...")
    print("=" * 50)
    
    for key, file_path in audio_files.items():
        if os.path.exists(file_path):
            effect = QSoundEffect()
            effect.setSource(QUrl.fromLocalFile(file_path))
            effect.setVolume(1.0)
            effects[key] = effect
            print(f"✅ Loaded: {key} -> {file_path}")
        else:
            print(f"❌ Missing: {key} -> {file_path}")
    
    print("\n" + "=" * 50)
    print("Playing each audio file (3 second delay between each)...")
    print("You should hear each sound clearly.")
    print("=" * 50)
    
    import time
    
    for key, effect in effects.items():
        print(f"Playing: {key}")
        effect.play()
        time.sleep(3)  # Wait 3 seconds between each sound
    
    print("Audio test complete!")
    print("If you didn't hear anything, check:")
    print("1. System volume is turned up")
    print("2. Correct audio device is selected")
    print("3. Speakers/headphones are connected and working")

if __name__ == "__main__":
    test_audio_files() 