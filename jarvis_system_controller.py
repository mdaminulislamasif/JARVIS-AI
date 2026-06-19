"""
JARVIS ULTIMATE SYSTEM CONTROLLER
সব কিছু manage করবে - Complete System Control

This module provides complete system control for JARVIS.
এই module JARVIS এর জন্য complete system control প্রদান করে।

Features:
- File/Folder management
- Program control
- System settings
- Task automation
- Process monitoring
- Service management
- Registry control (Windows)
- Startup management
- Network control
- User management
"""

import os
import sys
import subprocess
import psutil
import shutil
import winreg
import ctypes
import threading
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json


class SystemController:
    """Ultimate system controller for JARVIS"""
    
    def __init__(self):
        self.is_admin = self._check_admin()
        self.system_info = self._get_system_info()
        
    def _check_admin(self) -> bool:
        """Check if running with admin privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return False
    
    def _get_system_info(self) -> Dict:
        """Get system information"""
        return {
            "os": sys.platform,
            "python_version": sys.version,
            "is_admin": self.is_admin,
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "disk_partitions": [p.device for p in psutil.disk_partitions()],
        }
    
    # =========================================================================
    # FILE & FOLDER MANAGEMENT
    # =========================================================================
    
    def create_folder(self, path: str) -> bool:
        """Create folder"""
        try:
            os.makedirs(path, exist_ok=True)
            print(f"✅ Folder created: {path}")
            return True
        except Exception as e:
            print(f"❌ Failed to create folder: {e}")
            return False
    
    def delete_folder(self, path: str, force: bool = False) -> bool:
        """Delete folder"""
        try:
            if force:
                shutil.rmtree(path)
            else:
                os.rmdir(path)
            print(f"✅ Folder deleted: {path}")
            return True
        except Exception as e:
            print(f"❌ Failed to delete folder: {e}")
            return False
    
    def copy_folder(self, src: str, dst: str) -> bool:
        """Copy folder"""
        try:
            shutil.copytree(src, dst)
            print(f"✅ Folder copied: {src} → {dst}")
            return True
        except Exception as e:
            print(f"❌ Failed to copy folder: {e}")
            return False
    
    def move_folder(self, src: str, dst: str) -> bool:
        """Move folder"""
        try:
            shutil.move(src, dst)
            print(f"✅ Folder moved: {src} → {dst}")
            return True
        except Exception as e:
            print(f"❌ Failed to move folder: {e}")
            return False
    
    def list_files(self, path: str, pattern: str = "*") -> List[str]:
        """List files in folder"""
        try:
            p = Path(path)
            files = [str(f) for f in p.glob(pattern)]
            print(f"✅ Found {len(files)} files")
            return files
        except Exception as e:
            print(f"❌ Failed to list files: {e}")
            return []
    
    def create_file(self, path: str, content: str = "") -> bool:
        """Create file"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ File created: {path}")
            return True
        except Exception as e:
            print(f"❌ Failed to create file: {e}")
            return False
    
    def delete_file(self, path: str) -> bool:
        """Delete file"""
        try:
            os.remove(path)
            print(f"✅ File deleted: {path}")
            return True
        except Exception as e:
            print(f"❌ Failed to delete file: {e}")
            return False
    
    def copy_file(self, src: str, dst: str) -> bool:
        """Copy file"""
        try:
            shutil.copy2(src, dst)
            print(f"✅ File copied: {src} → {dst}")
            return True
        except Exception as e:
            print(f"❌ Failed to copy file: {e}")
            return False
    
    def move_file(self, src: str, dst: str) -> bool:
        """Move file"""
        try:
            shutil.move(src, dst)
            print(f"✅ File moved: {src} → {dst}")
            return True
        except Exception as e:
            print(f"❌ Failed to move file: {e}")
            return False
    
    def read_file(self, path: str) -> Optional[str]:
        """Read file content"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✅ File read: {path}")
            return content
        except Exception as e:
            print(f"❌ Failed to read file: {e}")
            return None
    
    def write_file(self, path: str, content: str) -> bool:
        """Write file content"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ File written: {path}")
            return True
        except Exception as e:
            print(f"❌ Failed to write file: {e}")
            return False
    
    # =========================================================================
    # PROGRAM CONTROL
    # =========================================================================
    
    def start_program(self, program: str, args: List[str] = None) -> bool:
        """Start program"""
        try:
            if args:
                subprocess.Popen([program] + args)
            else:
                subprocess.Popen(program)
            print(f"✅ Program started: {program}")
            return True
        except Exception as e:
            print(f"❌ Failed to start program: {e}")
            return False
    
    def stop_program(self, program_name: str) -> bool:
        """Stop program by name"""
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == program_name.lower():
                    proc.kill()
                    print(f"✅ Program stopped: {program_name}")
                    return True
            print(f"⚠️ Program not found: {program_name}")
            return False
        except Exception as e:
            print(f"❌ Failed to stop program: {e}")
            return False
    
    def is_program_running(self, program_name: str) -> bool:
        """Check if program is running"""
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == program_name.lower():
                    return True
            return False
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return False
    
    def get_running_programs(self) -> List[Dict]:
        """Get list of running programs"""
        try:
            programs = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                programs.append(proc.info)
            print(f"✅ Found {len(programs)} running programs")
            return programs
        except Exception as e:
            print(f"❌ Failed to get programs: {e}")
            return []
    
    # =========================================================================
    # PROCESS MANAGEMENT
    # =========================================================================
    
    def kill_process(self, pid: int) -> bool:
        """Kill process by PID"""
        try:
            proc = psutil.Process(pid)
            proc.kill()
            print(f"✅ Process killed: {pid}")
            return True
        except Exception as e:
            print(f"❌ Failed to kill process: {e}")
            return False
    
    def get_process_info(self, pid: int) -> Optional[Dict]:
        """Get process information"""
        try:
            proc = psutil.Process(pid)
            info = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent', 'status'])
            return info
        except Exception as e:
            print(f"❌ Failed to get process info: {e}")
            return None
    
    def get_all_processes(self) -> List[Dict]:
        """Get all processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                processes.append(proc.info)
            return processes
        except Exception as e:
            print(f"❌ Failed to get processes: {e}")
            return []
    
    # =========================================================================
    # SYSTEM SETTINGS
    # =========================================================================
    
    def set_volume(self, level: int) -> bool:
        """Set system volume (0-100)"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            print(f"✅ Volume set to: {level}%")
            return True
        except Exception as e:
            print(f"❌ Failed to set volume: {e}")
            return False
    
    def get_volume(self) -> Optional[int]:
        """Get system volume"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            level = int(volume.GetMasterVolumeLevelScalar() * 100)
            return level
        except Exception as e:
            print(f"❌ Failed to get volume: {e}")
            return None
    
    def set_brightness(self, level: int) -> bool:
        """Set screen brightness (0-100)"""
        try:
            import screen_brightness_control as sbc
            sbc.set_brightness(level)
            print(f"✅ Brightness set to: {level}%")
            return True
        except Exception as e:
            print(f"❌ Failed to set brightness: {e}")
            return False
    
    def get_brightness(self) -> Optional[int]:
        """Get screen brightness"""
        try:
            import screen_brightness_control as sbc
            level = sbc.get_brightness()[0]
            return level
        except Exception as e:
            print(f"❌ Failed to get brightness: {e}")
            return None
    
    # =========================================================================
    # STARTUP MANAGEMENT
    # =========================================================================
    
    def add_to_startup(self, name: str, path: str) -> bool:
        """Add program to startup"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, path)
            winreg.CloseKey(key)
            print(f"✅ Added to startup: {name}")
            return True
        except Exception as e:
            print(f"❌ Failed to add to startup: {e}")
            return False
    
    def remove_from_startup(self, name: str) -> bool:
        """Remove program from startup"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)
            print(f"✅ Removed from startup: {name}")
            return True
        except Exception as e:
            print(f"❌ Failed to remove from startup: {e}")
            return False
    
    def get_startup_programs(self) -> List[Tuple[str, str]]:
        """Get startup programs"""
        try:
            programs = []
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ
            )
            i = 0
            # WARNING: Infinite loop - ensure break condition exists
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    programs.append((name, value))
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
            print(f"✅ Found {len(programs)} startup programs")
            return programs
        except Exception as e:
            print(f"❌ Failed to get startup programs: {e}")
            return []
    
    # =========================================================================
    # SYSTEM MONITORING
    # =========================================================================
    
    def get_cpu_usage(self) -> float:
        """Get CPU usage percentage"""
        return psutil.cpu_percent(interval=1)
    
    def get_memory_usage(self) -> Dict:
        """Get memory usage"""
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "percent": mem.percent
        }
    
    def get_disk_usage(self, path: str = "C:\\") -> Dict:
        """Get disk usage"""
        disk = psutil.disk_usage(path)
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }
    
    def get_network_stats(self) -> Dict:
        """Get network statistics"""
        net = psutil.net_io_counters()
        return {
            "bytes_sent": net.bytes_sent,
            "bytes_recv": net.bytes_recv,
            "packets_sent": net.packets_sent,
            "packets_recv": net.packets_recv
        }
    
    def get_battery_status(self) -> Optional[Dict]:
        """Get battery status"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": battery.percent,
                    "plugged": battery.power_plugged,
                    "time_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
                }
            return None
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return None
    
    # =========================================================================
    # SYSTEM CONTROL
    # =========================================================================
    
    def shutdown(self, delay: int = 0) -> bool:
        """Shutdown system"""
        try:
            os.system(f"shutdown /s /t {delay}")
            print(f"✅ Shutdown scheduled in {delay} seconds")
            return True
        except Exception as e:
            print(f"❌ Failed to shutdown: {e}")
            return False
    
    def restart(self, delay: int = 0) -> bool:
        """Restart system"""
        try:
            os.system(f"shutdown /r /t {delay}")
            print(f"✅ Restart scheduled in {delay} seconds")
            return True
        except Exception as e:
            print(f"❌ Failed to restart: {e}")
            return False
    
    def lock(self) -> bool:
        """Lock system"""
        try:
            ctypes.windll.user32.LockWorkStation()
            print("✅ System locked")
            return True
        except Exception as e:
            print(f"❌ Failed to lock: {e}")
            return False
    
    def sleep(self) -> bool:
        """Put system to sleep"""
        try:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            print("✅ System sleeping")
            return True
        except Exception as e:
            print(f"❌ Failed to sleep: {e}")
            return False
    
    def hibernate(self) -> bool:
        """Hibernate system"""
        try:
            os.system("shutdown /h")
            print("✅ System hibernating")
            return True
        except Exception as e:
            print(f"❌ Failed to hibernate: {e}")
            return False
    
    # =========================================================================
    # TASK AUTOMATION
    # =========================================================================
    
    def schedule_task(self, name: str, command: str, time_str: str) -> bool:
        """Schedule task using Windows Task Scheduler"""
        try:
            cmd = f'schtasks /create /tn "{name}" /tr "{command}" /sc once /st {time_str}'
            subprocess.run(cmd, shell=True, check=True)
            print(f"✅ Task scheduled: {name}")
            return True
        except Exception as e:
            print(f"❌ Failed to schedule task: {e}")
            return False
    
    def delete_task(self, name: str) -> bool:
        """Delete scheduled task"""
        try:
            cmd = f'schtasks /delete /tn "{name}" /f'
            subprocess.run(cmd, shell=True, check=True)
            print(f"✅ Task deleted: {name}")
            return True
        except Exception as e:
            print(f"❌ Failed to delete task: {e}")
            return False
    
    def list_tasks(self) -> List[str]:
        """List scheduled tasks"""
        try:
            result = subprocess.run('schtasks /query /fo list', shell=True, capture_output=True, text=True)
            tasks = [line.split(":")[1].strip() for line in result.stdout.split("\n") if "TaskName" in line]
            print(f"✅ Found {len(tasks)} tasks")
            return tasks
        except Exception as e:
            print(f"❌ Failed to list tasks: {e}")
            return []
    
    # =========================================================================
    # SYSTEM INFO
    # =========================================================================
    
    def get_system_info_detailed(self) -> Dict:
        """Get detailed system information"""
        return {
            "platform": sys.platform,
            "python_version": sys.version,
            "is_admin": self.is_admin,
            "cpu": {
                "count": psutil.cpu_count(),
                "percent": psutil.cpu_percent(interval=1),
                "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            "memory": self.get_memory_usage(),
            "disk": {part.device: self.get_disk_usage(part.device) for part in psutil.disk_partitions()},
            "network": self.get_network_stats(),
            "battery": self.get_battery_status(),
            "boot_time": psutil.boot_time()
        }


# Test function
def test_system_controller():
    """Test system controller"""
    print("=" * 60)
    print("JARVIS SYSTEM CONTROLLER TEST")
    print("=" * 60)
    
    controller = SystemController()
    
    # Test 1: System Info
    print("\n🧪 Test 1: System Info")
    info = controller.get_system_info_detailed()
    print(f"Platform: {info['platform']}")
    print(f"Admin: {info['is_admin']}")
    print(f"CPU: {info['cpu']['count']} cores, {info['cpu']['percent']}%")
    print(f"Memory: {info['memory']['percent']}%")
    
    # Test 2: File Operations
    print("\n🧪 Test 2: File Operations")
    test_file = "test_jarvis.txt"
    controller.create_file(test_file, "Hello JARVIS!")
    content = controller.read_file(test_file)
    print(f"File content: {content}")
    controller.delete_file(test_file)
    
    # Test 3: Process Info
    print("\n🧪 Test 3: Process Info")
    programs = controller.get_running_programs()
    print(f"Running programs: {len(programs)}")
    
    # Test 4: System Monitoring
    print("\n🧪 Test 4: System Monitoring")
    cpu = controller.get_cpu_usage()
    mem = controller.get_memory_usage()
    print(f"CPU: {cpu}%")
    print(f"Memory: {mem['percent']}%")
    
    print("\n" + "=" * 60)
    print("✅ All tests complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_system_controller()
