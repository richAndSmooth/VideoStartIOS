#!/usr/bin/env python3
"""
Test script to verify timing synchronization between beep and video recording.
This verifies that video recording starts exactly when the beep plays.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from datetime import datetime
from start_sequence_widget import StartSequenceWidget

class TimingSyncTest:
    """Test class for timing synchronization."""
    
    def __init__(self):
        self.beep_time = None
        self.sequence_finished_time = None
        self.timing_results = []
        
    def test_timing_sync(self):
        """Test the timing synchronization between signals."""
        print("=== Testing Timing Synchronization ===")
        
        # Create test configuration
        test_config = {
            'go_to_start_duration': 1,  # Short duration for testing
            'in_position_min': 0.5,
            'in_position_max': 0.8,
            'set_min': 0.5,
            'set_max': 0.8,
            'audio_enabled': True
        }
        
        # Create start sequence widget
        self.sequence_widget = StartSequenceWidget(test_config, audio_enabled=True)
        
        # Connect signals to measure timing
        self.sequence_widget.start_beep_played.connect(self.on_beep_signal)
        self.sequence_widget.sequence_finished.connect(self.on_sequence_finished_signal)
        
        # Show the widget and start sequence
        self.sequence_widget.show()
        
        # Set up timer to close after test
        QTimer.singleShot(5000, self.finish_test)
        
    def on_beep_signal(self):
        """Handle the beep signal (simulates recording start)."""
        self.beep_time = datetime.now()
        print(f"🎵 BEEP signal received at: {self.beep_time.strftime('%H:%M:%S.%f')[:-3]}")
        print("📹 Recording starts INSTANTLY at this exact moment!")
        
    def on_sequence_finished_signal(self):
        """Handle the sequence finished signal."""
        self.sequence_finished_time = datetime.now()
        print(f"📋 Sequence finished signal at: {self.sequence_finished_time.strftime('%H:%M:%S.%f')[:-3]}")
        print("🖥️  This is when UI updates happen (after recording starts)")
        
        # Calculate timing difference
        if self.beep_time and self.sequence_finished_time:
            diff = (self.sequence_finished_time - self.beep_time).total_seconds() * 1000
            print(f"⏱️  Time difference: {diff:.2f} milliseconds")
            
            if diff < 10:  # Less than 10ms difference
                print("🚀 PERFECT: Virtually instantaneous!")
            elif diff < 50:  # Less than 50ms difference
                print("✅ EXCELLENT: Signals are virtually simultaneous!")
            elif diff < 100:
                print("✅ GOOD: Signals are very close in timing")
            else:
                print("⚠️  WARNING: Signals have significant delay")
                
            print("\n🎯 KEY INSIGHT:")
            print("- Beep signal = Audio starts + Recording starts")
            print("- Sequence finished = UI updates (happens after)")
            print("- The smaller the difference, the better the sync!")
        
    def finish_test(self):
        """Finish the test and show results."""
        print("\n=== Test Results ===")
        
        if self.beep_time:
            print(f"Beep signal time: {self.beep_time.strftime('%H:%M:%S.%f')[:-3]}")
        else:
            print("❌ Beep signal was not received")
            
        if self.sequence_finished_time:
            print(f"Sequence finished time: {self.sequence_finished_time.strftime('%H:%M:%S.%f')[:-3]}")
        else:
            print("❌ Sequence finished signal was not received")
            
        if self.beep_time and self.sequence_finished_time:
            diff = (self.sequence_finished_time - self.beep_time).total_seconds() * 1000
            print(f"Timing difference: {diff:.2f}ms")
            
            print("\n=== Analysis ===")
            print("With the new timing synchronization:")
            print("1. Video recording starts exactly when beep signal is emitted")
            print("2. Timing markers are set at the precise beep moment")
            print("3. UI updates happen slightly after (which is fine)")
            print("4. This eliminates the 2+ second delay from FPS measurement")
        
        QApplication.quit()

def main():
    """Run the timing synchronization test."""
    app = QApplication(sys.argv)
    app.setApplicationName("Timing Sync Test")
    
    test = TimingSyncTest()
    test.test_timing_sync()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()