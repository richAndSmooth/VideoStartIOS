"""
Timing Markers Module
Manages start and finish timing data for race events.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import json
import os

class TimingMarkers:
    """Manages timing markers for race events."""
    
    def __init__(self):
        self.start_time: Optional[datetime] = None
        self.finish_time: Optional[datetime] = None
        self.finish_times: List[Dict[str, Any]] = []  # For multiple finish signals
        self.event_id: Optional[str] = None
        self.lane_count: int = 1
        
    def set_start_time(self, start_time: datetime):
        """Set the start time marker."""
        self.start_time = start_time
        print(f"Start time marked: {start_time.strftime('%H:%M:%S.%f')[:-3]}")
        
    def set_finish_time(self, finish_time: datetime, lane: int = 1, participant_id: Optional[str] = None):
        """Set the finish time marker."""
        self.finish_time = finish_time
        
        # Add to finish times list for multiple participants
        finish_data = {
            "time": finish_time,
            "lane": lane,
            "participant_id": participant_id,
            "duration": self.get_duration() if self.start_time else None
        }
        self.finish_times.append(finish_data)
        
        print(f"Finish time marked: {finish_time.strftime('%H:%M:%S.%f')[:-3]}")
        
    def get_duration(self) -> Optional[timedelta]:
        """Get the duration between start and finish."""
        if self.start_time and self.finish_time:
            return self.finish_time - self.start_time
        return None
        
    def get_duration_seconds(self) -> Optional[float]:
        """Get the duration in seconds."""
        duration = self.get_duration()
        if duration:
            return duration.total_seconds()
        return None
        
    def get_formatted_duration(self) -> str:
        """Get formatted duration string."""
        duration = self.get_duration()
        if duration:
            total_seconds = duration.total_seconds()
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)
            milliseconds = int((total_seconds % 1) * 1000)
            return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        return "--"
        
    def clear_markers(self):
        """Clear all timing markers."""
        self.start_time = None
        self.finish_time = None
        self.finish_times.clear()
        print("Timing markers cleared")
        
    def set_event_id(self, event_id: str):
        """Set the event identifier."""
        self.event_id = event_id
        
    def set_lane_count(self, lane_count: int):
        """Set the number of lanes/participants."""
        self.lane_count = max(1, lane_count)
        
    def get_finish_time_for_lane(self, lane: int) -> Optional[datetime]:
        """Get finish time for a specific lane."""
        for finish_data in self.finish_times:
            if finish_data["lane"] == lane:
                return finish_data["time"]
        return None
        
    def get_duration_for_lane(self, lane: int) -> Optional[timedelta]:
        """Get duration for a specific lane."""
        finish_time = self.get_finish_time_for_lane(lane)
        if self.start_time and finish_time:
            return finish_time - self.start_time
        return None
        
    def get_all_finish_times(self) -> List[Dict[str, Any]]:
        """Get all finish times with details."""
        return self.finish_times.copy()
        
    def get_timing_summary(self) -> Dict[str, Any]:
        """Get a summary of all timing data."""
        summary = {
            "event_id": self.event_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "finish_time": self.finish_time.isoformat() if self.finish_time else None,
            "duration": self.get_formatted_duration(),
            "duration_seconds": self.get_duration_seconds(),
            "lane_count": self.lane_count,
            "finish_times": []
        }
        
        for finish_data in self.finish_times:
            summary["finish_times"].append({
                "lane": finish_data["lane"],
                "participant_id": finish_data["participant_id"],
                "time": finish_data["time"].isoformat(),
                "duration": str(finish_data["duration"]) if finish_data["duration"] else None
            })
            
        return summary
        
    def save_timing_data(self, filepath: str):
        """Save timing data to a JSON file."""
        try:
            data = self.get_timing_summary()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
                
            print(f"Timing data saved to: {filepath}")
            
        except Exception as e:
            print(f"Error saving timing data: {str(e)}")
            
    def load_timing_data(self, filepath: str):
        """Load timing data from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            # Parse the data
            if data.get("start_time"):
                self.start_time = datetime.fromisoformat(data["start_time"])
            if data.get("finish_time"):
                self.finish_time = datetime.fromisoformat(data["finish_time"])
                
            self.event_id = data.get("event_id")
            self.lane_count = data.get("lane_count", 1)
            
            # Parse finish times
            self.finish_times.clear()
            for finish_data in data.get("finish_times", []):
                finish_time = datetime.fromisoformat(finish_data["time"])
                duration = None
                if finish_data.get("duration"):
                    duration = timedelta.fromisoformat(finish_data["duration"])
                    
                self.finish_times.append({
                    "time": finish_time,
                    "lane": finish_data["lane"],
                    "participant_id": finish_data.get("participant_id"),
                    "duration": duration
                })
                
            print(f"Timing data loaded from: {filepath}")
            
        except Exception as e:
            print(f"Error loading timing data: {str(e)}")
            
    def is_complete(self) -> bool:
        """Check if timing data is complete (has both start and finish)."""
        return self.start_time is not None and self.finish_time is not None
        
    def get_lane_status(self) -> Dict[int, bool]:
        """Get status of each lane (whether it has finished)."""
        status = {}
        for lane in range(1, self.lane_count + 1):
            status[lane] = self.get_finish_time_for_lane(lane) is not None
        return status
        
    def get_winner_lane(self) -> Optional[int]:
        """Get the lane number of the winner (fastest time)."""
        if not self.start_time:
            return None
            
        fastest_time = None
        winner_lane = None
        
        for finish_data in self.finish_times:
            duration = finish_data["duration"]
            if duration and (fastest_time is None or duration < fastest_time):
                fastest_time = duration
                winner_lane = finish_data["lane"]
                
        return winner_lane 