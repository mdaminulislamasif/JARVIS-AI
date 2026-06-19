"""
📊 JARVIS PERFORMANCE MONITORING SYSTEM
Real-Time System Health & Analytics
"""

import time
from datetime import datetime

class PerformanceMonitor:
    """Monitor JARVIS performance in real-time"""
    
    def __init__(self):
        self.start_time = time.time()
        self.response_times = []
        self.error_count = 0
        self.query_count = 0
        
        print("✅ Performance Monitor Active!")
    
    def log_response(self, response_time_ms: float):
        """Log response time"""
        self.response_times.append(response_time_ms)
        self.query_count += 1
    
    def log_error(self):
        """Log error"""
        self.error_count += 1
    
    def get_stats(self):
        """Get performance statistics"""
        if not self.response_times:
            return {}
        
        return {
            "avg_response_time": sum(self.response_times) / len(self.response_times),
            "max_response_time": max(self.response_times),
            "min_response_time": min(self.response_times),
            "total_queries": self.query_count,
            "error_rate": (self.error_count / self.query_count * 100) if self.query_count > 0 else 0,
            "uptime_seconds": time.time() - self.start_time
        }

monitor = PerformanceMonitor()
