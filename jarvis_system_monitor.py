"""
JARVIS SYSTEM MONITOR
Shows what JARVIS is doing in real-time
JARVIS কি করছে তা real-time এ দেখায়
"""

import psutil
import time
import os
import sys
from datetime import datetime

class JarvisSystemMonitor:
    """Monitor JARVIS system activities"""
    
    def __init__(self):
        self.start_time = time.time()
        self.activities = []
        
    def log_activity(self, activity_type, description):
        """Log an activity"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activities.append({
            'time': timestamp,
            'type': activity_type,
            'description': description
        })
        
    def get_system_status(self):
        """Get current system status"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            status = f"""
╔══════════════════════════════════════════════════════════════════╗
║              JARVIS SYSTEM MONITOR                               ║
║              JARVIS সিস্টেম মনিটর                                ║
╚══════════════════════════════════════════════════════════════════╝

⏰ Current Time / বর্তমান সময়: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
⏱️  Uptime / চলার সময়: {self._format_uptime()}

╔══════════════════════════════════════════════════════════════════╗
║  SYSTEM RESOURCES / সিস্টেম রিসোর্স                              ║
╚══════════════════════════════════════════════════════════════════╝

🖥️  CPU Usage / CPU ব্যবহার:
    {self._create_bar(cpu, 100)} {cpu:.1f}%

💾 Memory / মেমরি:
    Used / ব্যবহৃত: {memory.used / (1024**3):.1f} GB / {memory.total / (1024**3):.1f} GB
    {self._create_bar(memory.percent, 100)} {memory.percent:.1f}%

💿 Disk / ডিস্ক:
    Used / ব্যবহৃত: {disk.used / (1024**3):.1f} GB / {disk.total / (1024**3):.1f} GB
    {self._create_bar(disk.percent, 100)} {disk.percent:.1f}%

╔══════════════════════════════════════════════════════════════════╗
║  JARVIS STATUS / JARVIS অবস্থা                                  ║
╚══════════════════════════════════════════════════════════════════╝

🧠 Brain Status / ব্রেইন অবস্থা: {self._check_brain_status()}
🎤 Voice Engine / ভয়েস ইঞ্জিন: {self._check_voice_status()}
🌐 Network / নেটওয়ার্ক: {self._check_network_status()}
📁 Files / ফাইল: {self._check_files_status()}

╔══════════════════════════════════════════════════════════════════╗
║  RECENT ACTIVITIES / সাম্প্রতিক কার্যক্রম                        ║
╚══════════════════════════════════════════════════════════════════╝

{self._format_activities()}

╔══════════════════════════════════════════════════════════════════╗
║  RUNNING PROCESSES / চলমান প্রসেস                               ║
╚══════════════════════════════════════════════════════════════════╝

{self._get_jarvis_processes()}
"""
            return status
        except Exception as e:
            return f"Error getting system status: {e}"
    
    def _format_uptime(self):
        """Format uptime"""
        uptime_seconds = int(time.time() - self.start_time)
        hours = uptime_seconds // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def _create_bar(self, value, max_value, length=30):
        """Create a progress bar"""
        filled = int((value / max_value) * length)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}]"
    
    def _check_brain_status(self):
        """Check if brain is working"""
        try:
            if os.path.exists('jarvis_offline_brain.py'):
                return "✅ ONLINE (Offline Brain Ready)"
            else:
                return "⚠️ Offline Brain Not Found"
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return "❌ ERROR"
    
    def _check_voice_status(self):
        """Check voice engine status"""
        try:
            import speech_recognition
            return "✅ READY"
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return "⚠️ NOT INSTALLED"
    
    def _check_network_status(self):
        """Check network status"""
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return "✅ CONNECTED"
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return "❌ OFFLINE"
    
    def _check_files_status(self):
        """Check important files"""
        important_files = [
            'jarvis_panel.py',
            'core/brain.py',
            'engine/multi_brain.py',
            'jarvis_offline_brain.py'
        ]
        
        existing = sum(1 for f in important_files if os.path.exists(f))
        total = len(important_files)
        
        if existing == total:
            return f"✅ ALL OK ({existing}/{total})"
        else:
            return f"⚠️ MISSING ({existing}/{total})"
    
    def _format_activities(self):
        """Format recent activities"""
        if not self.activities:
            return "    No recent activities / কোনো সাম্প্রতিক কার্যক্রম নেই"
        
        # Show last 5 activities
        recent = self.activities[-5:]
        lines = []
        for act in recent:
            lines.append(f"    [{act['time']}] {act['type']}: {act['description']}")
        
        return "\n".join(lines)
    
    def _get_jarvis_processes(self):
        """Get JARVIS related processes"""
        try:
            jarvis_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    name = proc.info['name'].lower()
                    if 'python' in name or 'jarvis' in name:
                        jarvis_processes.append(proc.info)
                except Exception as e:

                    print(f"⚠️ Error: {e}")
                    pass
            
            if not jarvis_processes:
                return "    No JARVIS processes found / কোনো JARVIS প্রসেস পাওয়া যায়নি"
            
            lines = []
            for proc in jarvis_processes[:5]:  # Show top 5
                lines.append(
                    f"    PID: {proc['pid']:6d} | "
                    f"CPU: {proc['cpu_percent']:5.1f}% | "
                    f"MEM: {proc['memory_percent']:5.1f}% | "
                    f"{proc['name']}"
                )
            
            return "\n".join(lines)
        except Exception as e:
            return f"    Error: {e}"
    
    def show_live_monitor(self, refresh_interval=2):
        """Show live monitoring (updates every N seconds)"""
        print("\n" + "="*70)
        print("  JARVIS LIVE SYSTEM MONITOR")
        print("  Press Ctrl+C to stop")
        print("="*70)
        
        try:
            # WARNING: Infinite loop - ensure break condition exists
            while True:
                # Clear screen
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # Show status
                print(self.get_system_status())
                
                # Wait
                time.sleep(refresh_interval)
        except KeyboardInterrupt:
            print("\n\n✅ Monitor stopped / মনিটর বন্ধ হয়েছে")


def main():
    """Main function"""
    print("\n" + "="*70)
    print("  🔍 JARVIS SYSTEM MONITOR")
    print("  🔍 JARVIS সিস্টেম মনিটর")
    print("="*70)
    
    monitor = JarvisSystemMonitor()
    
    # Log some sample activities
    monitor.log_activity("STARTUP", "System monitor started")
    monitor.log_activity("CHECK", "Checking system resources")
    monitor.log_activity("SCAN", "Scanning for JARVIS processes")
    
    if len(sys.argv) > 1 and sys.argv[1] == 'live':
        # Live monitoring mode
        monitor.show_live_monitor()
    else:
        # Single snapshot mode
        print(monitor.get_system_status())
        print("\n💡 TIP: Run 'python jarvis_system_monitor.py live' for live monitoring")
        print("💡 টিপ: Live monitoring এর জন্য 'python jarvis_system_monitor.py live' চালান")


if __name__ == "__main__":
    main()
