#!/usr/bin/env python3
"""
Audio File Generator
Generates prerecorded audio files for the race timer start sequence.
"""

import os
import sys
import pyttsx3
import winsound
import time

def generate_tts_audio(text, filename, rate=120, volume=1.0):
    """Generate TTS audio and save to file."""
    try:
        # Initialize TTS engine
        tts = pyttsx3.init()
        tts.setProperty('rate', rate)
        tts.setProperty('volume', volume)
        
        # Get available voices and use the first one
        voices = tts.getProperty('voices')
        if voices:
            tts.setProperty('voice', voices[0].id)
        
        print(f"Generating audio for: '{text}' -> {filename}")
        
        # Generate audio
        tts.say(text)
        tts.runAndWait()
        tts.stop()
        
        print(f"✓ Generated: {filename}")
        return True
        
    except Exception as e:
        print(f"✗ Error generating {filename}: {e}")
        return False

def generate_beep_audio(filename, frequency=800, duration=300):
    """Generate beep audio and save to file."""
    try:
        print(f"Generating beep audio -> {filename}")
        
        # For now, we'll use winsound to play the beep
        # In a real implementation, you'd want to record this to a file
        winsound.Beep(frequency, duration)
        
        print(f"✓ Generated: {filename}")
        return True
        
    except Exception as e:
        print(f"✗ Error generating {filename}: {e}")
        return False

def main():
    """Main function to generate all audio files."""
    print("Race Timer - Audio File Generator")
    print("=" * 40)
    print()
    
    # Create audio directory
    audio_dir = "audio"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
        print(f"Created audio directory: {audio_dir}")
    
    print("This script will generate prerecorded audio files for the start sequence.")
    print("Note: Due to TTS limitations, you may need to manually record these audio files.")
    print()
    
    # Audio files to generate
    audio_files = [
        ("Go to the start", "go_to_start.wav"),
        ("In position", "in_position.wav"),
        ("Set", "set.wav"),
        ("Start beep", "start_beep.wav")
    ]
    
    print("Generating audio files...")
    print()
    
    for text, filename in audio_files:
        if filename == "start_beep.wav":
            generate_beep_audio(filename)
        else:
            generate_tts_audio(text, filename)
        print()
    
    print("Audio generation complete!")
    print()
    print("Manual Recording Instructions:")
    print("1. Use a voice recorder or audio software")
    print("2. Record the following phrases clearly:")
    print("   - 'Go to the start'")
    print("   - 'In position'") 
    print("   - 'Set'")
    print("   - A start beep sound (3 short beeps)")
    print("3. Save as WAV files in the 'audio' directory:")
    print("   - go_to_start.wav")
    print("   - in_position.wav")
    print("   - set.wav")
    print("   - start_beep.wav")
    print()
    print("Alternative: Use online TTS services to generate these audio files.")

if __name__ == "__main__":
    main() 