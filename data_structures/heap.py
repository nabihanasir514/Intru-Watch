# Heap/Priority Queue for Alert System

import heapq
from datetime import datetime
from typing import List, Tuple


class AlertSystem:
    """Priority Queue (Min-Heap) for security alerts
    
    Priority levels:
    - 1: High (Critical - immediate action required)
    - 2: Medium (Warning - attention needed)
    - 3: Low (Info - routine notification)
    """
    
    def __init__(self):
        self.heap: List[Tuple[int, str, str, str]] = []
        self.alert_count = 0
    
    def add_alert(self, priority: int, message: str, location: str) -> None:
        """Add an alert to the priority queue - O(log n)"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        heapq.heappush(self.heap, (priority, timestamp, message, location))
        self.alert_count += 1
    
    def get_highest_priority_alert(self) -> Tuple[int, str, str, str]:
        """Get and remove the highest priority alert - O(log n)"""
        if self.heap:
            return heapq.heappop(self.heap)
        return None
    
    def peek_highest_priority(self) -> Tuple[int, str, str, str]:
        """View highest priority alert without removing - O(1)"""
        if self.heap:
            return self.heap[0]
        return None
    
    def get_all_alerts_sorted(self) -> List[Tuple[int, str, str, str]]:
        """Get all alerts sorted by priority - O(n log n)"""
        return sorted(self.heap)
    
    def get_alerts_by_priority(self, priority: int) -> List[Tuple[int, str, str, str]]:
        """Filter alerts by priority level"""
        return [alert for alert in self.heap if alert[0] == priority]
    
    def get_alerts_by_location(self, location: str) -> List[Tuple[int, str, str, str]]:
        """Filter alerts by location"""
        return [alert for alert in self.heap if alert[3] == location]
    
    def clear_alerts(self) -> None:
        """Clear all alerts"""
        self.heap = []
    
    def count_alerts(self) -> int:
        """Get total number of active alerts"""
        return len(self.heap)
    
    def count_by_priority(self) -> dict:
        """Count alerts per priority level"""
        counts = {1: 0, 2: 0, 3: 0}
        for alert in self.heap:
            if alert[0] in counts:
                counts[alert[0]] += 1
        return counts
    
    def to_dataframe_format(self) -> List[dict]:
        """Convert alerts to list of dicts for pandas DataFrame"""
        priority_labels = {1: "High", 2: "Medium", 3: "Low"}
        return [
            {
                "Priority": f"{p} ({priority_labels.get(p, 'Unknown')})",
                "Time": t,
                "Message": m,
                "Location": l
            }
            for p, t, m, l in sorted(self.heap)
        ]
