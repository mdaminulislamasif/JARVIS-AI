"""
JARVIS SYSTEM ANALYZER
সিস্টেম বিশ্লেষক

This module analyzes user's system and answers questions about it.
এই module user এর system বিশ্লেষণ করে এবং প্রশ্নের উত্তর দেয়।

Features:
- Hardware information (CPU, RAM, Disk, GPU)
- Software information (OS, installed programs)
- Network information (IP, connections)
- File system information (files, folders, sizes)
- Process information (running programs)
- Performance metrics (CPU usage, memory usage)
"""

import platform
import psutil
import os
import socket
import subprocess
import json
from datetime import datetime
import re


class SystemAnalyzer:
    """Analyzes user's system and answers questions"""
    
    def __init__(self):
        self.system_info = {}
        self.cache_time = None
        self.cache_duration = 60  # Cache for 60 seconds
        
        print("✅ System Analyzer initialized!")
    
    def get_system_info(self, force_refresh=False):
        """
        Get complete system information
        সম্পূর্ণ system তথ্য পান
        
        Args:
            force_refresh: Force refresh cache
        
        Returns:
            Dictionary with all system information
        """
        # Check cache
        if not force_refresh and self.cache_time:
            elapsed = (datetime.now() - self.cache_time).seconds
            if elapsed < self.cache_duration:
                return self.system_info
        
        print("🔍 Analyzing system...")
        
        # Collect all information
        self.system_info = {
            'hardware': self._get_hardware_info(),
            'software': self._get_software_info(),
            'network': self._get_network_info(),
            'filesystem': self._get_filesystem_info(),
            'processes': self._get_process_info(),
            'performance': self._get_performance_info()
        }
        
        self.cache_time = datetime.now()
        
        return self.system_info
    
    def _get_hardware_info(self):
        """Get hardware information"""
        try:
            # CPU Information
            cpu_info = {
                'name': platform.processor(),
                'physical_cores': psutil.cpu_count(logical=False),
                'logical_cores': psutil.cpu_count(logical=True),
                'max_frequency': f"{psutil.cpu_freq().max:.2f} MHz" if psutil.cpu_freq() else "Unknown",
                'current_frequency': f"{psutil.cpu_freq().current:.2f} MHz" if psutil.cpu_freq() else "Unknown",
                'architecture': platform.machine()
            }
            
            # RAM Information
            ram = psutil.virtual_memory()
            ram_info = {
                'total': self._bytes_to_gb(ram.total),
                'available': self._bytes_to_gb(ram.available),
                'used': self._bytes_to_gb(ram.used),
                'percentage': f"{ram.percent}%"
            }
            
            # Disk Information
            disk_info = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'filesystem': partition.fstype,
                        'total': self._bytes_to_gb(usage.total),
                        'used': self._bytes_to_gb(usage.used),
                        'free': self._bytes_to_gb(usage.free),
                        'percentage': f"{usage.percent}%"
                    })
                except Exception as e:

                    print(f"⚠️ Error: {e}")
                    pass
            
            # GPU Information (Windows)
            gpu_info = self._get_gpu_info()
            
            return {
                'cpu': cpu_info,
                'ram': ram_info,
                'disk': disk_info,
                'gpu': gpu_info
            }
        
        except Exception as e:
            print(f"⚠️ Error getting hardware info: {e}")
            return {}
    
    def _get_gpu_info(self):
        """Get GPU information (Windows)"""
        try:
            if platform.system() == 'Windows':
                result = subprocess.run(
                    ['wmic', 'path', 'win32_VideoController', 'get', 'name'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    gpus = [line.strip() for line in lines[1:] if line.strip()]
                    return gpus if gpus else ['Unknown']
            
            return ['Unknown']
        
        except Exception as e:
            return ['Unknown']
    
    def _get_software_info(self):
        """Get software information"""
        try:
            return {
                'os': {
                    'system': platform.system(),
                    'release': platform.release(),
                    'version': platform.version(),
                    'architecture': platform.architecture()[0]
                },
                'python': {
                    'version': platform.python_version(),
                    'implementation': platform.python_implementation()
                },
                'hostname': socket.gethostname(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
            }
        
        except Exception as e:
            print(f"⚠️ Error getting software info: {e}")
            return {}
    
    def _get_network_info(self):
        """Get network information"""
        try:
            # Get IP addresses
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Get network interfaces
            interfaces = []
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        interfaces.append({
                            'interface': interface,
                            'ip': addr.address,
                            'netmask': addr.netmask
                        })
            
            # Get network statistics
            net_io = psutil.net_io_counters()
            
            return {
                'hostname': hostname,
                'local_ip': local_ip,
                'interfaces': interfaces,
                'bytes_sent': self._bytes_to_gb(net_io.bytes_sent),
                'bytes_received': self._bytes_to_gb(net_io.bytes_recv)
            }
        
        except Exception as e:
            print(f"⚠️ Error getting network info: {e}")
            return {}
    
    def _get_filesystem_info(self):
        """Get filesystem information"""
        try:
            # Count files and folders in common locations
            home_dir = os.path.expanduser('~')
            desktop_dir = os.path.join(home_dir, 'Desktop')
            documents_dir = os.path.join(home_dir, 'Documents')
            downloads_dir = os.path.join(home_dir, 'Downloads')
            
            locations = {
                'home': self._count_items(home_dir, max_depth=1),
                'desktop': self._count_items(desktop_dir, max_depth=2),
                'documents': self._count_items(documents_dir, max_depth=2),
                'downloads': self._count_items(downloads_dir, max_depth=2)
            }
            
            return locations
        
        except Exception as e:
            print(f"⚠️ Error getting filesystem info: {e}")
            return {}
    
    def _count_items(self, path, max_depth=1):
        """Count files and folders in a path"""
        try:
            if not os.path.exists(path):
                return {'files': 0, 'folders': 0, 'total_size': '0 GB'}
            
            files = 0
            folders = 0
            total_size = 0
            
            for root, dirs, filenames in os.walk(path):
                # Check depth
                depth = root[len(path):].count(os.sep)
                if depth >= max_depth:
                    dirs.clear()
                    continue
                
                folders += len(dirs)
                files += len(filenames)
                
                for filename in filenames:
                    try:
                        filepath = os.path.join(root, filename)
                        total_size += os.path.getsize(filepath)
                    except Exception as e:

                        print(f"⚠️ Error: {e}")
                        pass
            
            return {
                'files': files,
                'folders': folders,
                'total_size': self._bytes_to_gb(total_size)
            }
        
        except Exception as e:
            return {'files': 0, 'folders': 0, 'total_size': '0 GB'}
    
    def _get_process_info(self):
        """Get running process information"""
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu_percent': proc.info['cpu_percent'],
                        'memory_percent': proc.info['memory_percent']
                    })
                except Exception as e:

                    print(f"⚠️ Error: {e}")
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            return {
                'total_processes': len(processes),
                'top_processes': processes[:10]  # Top 10 processes
            }
        
        except Exception as e:
            print(f"⚠️ Error getting process info: {e}")
            return {}
    
    def _get_performance_info(self):
        """Get current performance metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            
            return {
                'cpu_usage': f"{cpu_percent}%",
                'ram_usage': f"{ram.percent}%",
                'ram_available': self._bytes_to_gb(ram.available),
                'disk_io': self._get_disk_io(),
                'network_io': self._get_network_io()
            }
        
        except Exception as e:
            print(f"⚠️ Error getting performance info: {e}")
            return {}
    
    def _get_disk_io(self):
        """Get disk I/O statistics"""
        try:
            disk_io = psutil.disk_io_counters()
            return {
                'read': self._bytes_to_gb(disk_io.read_bytes),
                'write': self._bytes_to_gb(disk_io.write_bytes)
            }
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return {'read': '0 GB', 'write': '0 GB'}
    
    def _get_network_io(self):
        """Get network I/O statistics"""
        try:
            net_io = psutil.net_io_counters()
            return {
                'sent': self._bytes_to_gb(net_io.bytes_sent),
                'received': self._bytes_to_gb(net_io.bytes_recv)
            }
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return {'sent': '0 GB', 'received': '0 GB'}
    
    def _bytes_to_gb(self, bytes_value):
        """Convert bytes to GB"""
        gb = bytes_value / (1024 ** 3)
        if gb < 0.01:
            mb = bytes_value / (1024 ** 2)
            return f"{mb:.2f} MB"
        return f"{gb:.2f} GB"
    
    def answer_question(self, question):
        """
        Answer questions about user's system
        User এর system সম্পর্কে প্রশ্নের উত্তর দেয়
        
        Args:
            question: User's question
        
        Returns:
            Answer dictionary with status and response
        """
        question_lower = question.lower()
        
        # Get system info
        info = self.get_system_info()
        
        # CPU Questions
        if any(word in question_lower for word in ['cpu', 'processor', 'core']):
            cpu = info['hardware']['cpu']
            
            if 'how many' in question_lower or 'কত' in question_lower or 'কতগুলো' in question_lower:
                if 'core' in question_lower:
                    return {
                        'status': 'success',
                        'response': f"""💻 CPU Cores / CPU কোর:

Physical Cores / ফিজিক্যাল কোর: {cpu['physical_cores']}
Logical Cores / লজিক্যাল কোর: {cpu['logical_cores']}

Your CPU has {cpu['physical_cores']} physical cores and {cpu['logical_cores']} logical cores (with hyper-threading).
আপনার CPU তে {cpu['physical_cores']}টি physical cores এবং {cpu['logical_cores']}টি logical cores আছে (hyper-threading সহ)।""",
                        'type': 'system_info'
                    }
            
            return {
                'status': 'success',
                'response': f"""💻 CPU Information / CPU তথ্য:

Processor / প্রসেসর: {cpu['name']}
Architecture / আর্কিটেকচার: {cpu['architecture']}
Physical Cores / ফিজিক্যাল কোর: {cpu['physical_cores']}
Logical Cores / লজিক্যাল কোর: {cpu['logical_cores']}
Max Frequency / সর্বোচ্চ ফ্রিকোয়েন্সি: {cpu['max_frequency']}
Current Frequency / বর্তমান ফ্রিকোয়েন্সি: {cpu['current_frequency']}

Current Usage / বর্তমান ব্যবহার: {info['performance']['cpu_usage']}""",
                'type': 'system_info'
            }
        
        # RAM Questions
        if any(word in question_lower for word in ['ram', 'memory', 'মেমরি']):
            ram = info['hardware']['ram']
            
            return {
                'status': 'success',
                'response': f"""💾 RAM Information / RAM তথ্য:

Total RAM / মোট RAM: {ram['total']}
Used / ব্যবহৃত: {ram['used']}
Available / উপলব্ধ: {ram['available']}
Usage / ব্যবহার: {ram['percentage']}

Current RAM Usage / বর্তমান RAM ব্যবহার: {info['performance']['ram_usage']}
Available RAM / উপলব্ধ RAM: {info['performance']['ram_available']}""",
                'type': 'system_info'
            }
        
        # Disk Questions
        if any(word in question_lower for word in ['disk', 'storage', 'space', 'drive', 'হার্ড', 'ডিস্ক']):
            disks = info['hardware']['disk']
            
            response = "💿 Disk Information / ডিস্ক তথ্য:\n\n"
            
            for i, disk in enumerate(disks, 1):
                response += f"""Drive {i} / ড্রাইভ {i}:
  Device / ডিভাইস: {disk['device']}
  Mount Point / মাউন্ট পয়েন্ট: {disk['mountpoint']}
  Filesystem / ফাইলসিস্টেম: {disk['filesystem']}
  Total / মোট: {disk['total']}
  Used / ব্যবহৃত: {disk['used']}
  Free / খালি: {disk['free']}
  Usage / ব্যবহার: {disk['percentage']}

"""
            
            return {
                'status': 'success',
                'response': response.strip(),
                'type': 'system_info'
            }
        
        # GPU Questions
        if any(word in question_lower for word in ['gpu', 'graphics', 'video card', 'গ্রাফিক্স']):
            gpus = info['hardware']['gpu']
            
            response = "🎮 GPU Information / GPU তথ্য:\n\n"
            
            for i, gpu in enumerate(gpus, 1):
                response += f"GPU {i}: {gpu}\n"
            
            return {
                'status': 'success',
                'response': response.strip(),
                'type': 'system_info'
            }
        
        # OS Questions
        if any(word in question_lower for word in ['os', 'operating system', 'windows', 'linux', 'অপারেটিং']):
            os_info = info['software']['os']
            
            return {
                'status': 'success',
                'response': f"""🖥️ Operating System / অপারেটিং সিস্টেম:

System / সিস্টেম: {os_info['system']}
Release / রিলিজ: {os_info['release']}
Version / সংস্করণ: {os_info['version']}
Architecture / আর্কিটেকচার: {os_info['architecture']}

Boot Time / বুট টাইম: {info['software']['boot_time']}
Hostname / হোস্টনাম: {info['software']['hostname']}""",
                'type': 'system_info'
            }
        
        # Network Questions
        if any(word in question_lower for word in ['ip', 'network', 'internet', 'নেটওয়ার্ক', 'ইন্টারনেট']):
            network = info['network']
            
            response = f"""🌐 Network Information / নেটওয়ার্ক তথ্য:

Hostname / হোস্টনাম: {network['hostname']}
Local IP / লোকাল IP: {network['local_ip']}

Network Interfaces / নেটওয়ার্ক ইন্টারফেস:
"""
            
            for interface in network['interfaces']:
                response += f"\n  {interface['interface']}: {interface['ip']}"
            
            response += f"""

Data Sent / ডেটা পাঠানো: {network['bytes_sent']}
Data Received / ডেটা গ্রহণ: {network['bytes_received']}"""
            
            return {
                'status': 'success',
                'response': response,
                'type': 'system_info'
            }
        
        # File Questions
        if any(word in question_lower for word in ['file', 'folder', 'ফাইল', 'ফোল্ডার']):
            filesystem = info['filesystem']
            
            if 'desktop' in question_lower:
                location = filesystem.get('desktop', {})
                location_name = 'Desktop / ডেস্কটপ'
            elif 'document' in question_lower:
                location = filesystem.get('documents', {})
                location_name = 'Documents / ডকুমেন্টস'
            elif 'download' in question_lower:
                location = filesystem.get('downloads', {})
                location_name = 'Downloads / ডাউনলোডস'
            else:
                location = filesystem.get('home', {})
                location_name = 'Home / হোম'
            
            return {
                'status': 'success',
                'response': f"""📁 {location_name} Information:

Files / ফাইল: {location.get('files', 0)}
Folders / ফোল্ডার: {location.get('folders', 0)}
Total Size / মোট সাইজ: {location.get('total_size', '0 GB')}""",
                'type': 'system_info'
            }
        
        # Process Questions
        if any(word in question_lower for word in ['process', 'program', 'running', 'প্রোগ্রাম', 'চলছে']):
            processes = info['processes']
            
            response = f"""⚙️ Running Processes / চলমান প্রোগ্রাম:

Total Processes / মোট প্রোগ্রাম: {processes['total_processes']}

Top 10 Processes by CPU Usage / CPU ব্যবহার অনুযায়ী শীর্ষ ১০:

"""
            
            for i, proc in enumerate(processes['top_processes'], 1):
                response += f"{i}. {proc['name']} - CPU: {proc['cpu_percent']}%, RAM: {proc['memory_percent']:.1f}%\n"
            
            return {
                'status': 'success',
                'response': response.strip(),
                'type': 'system_info'
            }
        
        # Performance Questions
        if any(word in question_lower for word in ['performance', 'usage', 'using', 'ব্যবহার', 'পারফরম্যান্স']):
            perf = info['performance']
            
            return {
                'status': 'success',
                'response': f"""📊 System Performance / সিস্টেম পারফরম্যান্স:

CPU Usage / CPU ব্যবহার: {perf['cpu_usage']}
RAM Usage / RAM ব্যবহার: {perf['ram_usage']}
RAM Available / RAM উপলব্ধ: {perf['ram_available']}

Disk I/O / ডিস্ক I/O:
  Read / পড়া: {perf['disk_io']['read']}
  Write / লেখা: {perf['disk_io']['write']}

Network I/O / নেটওয়ার্ক I/O:
  Sent / পাঠানো: {perf['network_io']['sent']}
  Received / গ্রহণ: {perf['network_io']['received']}""",
                'type': 'system_info'
            }
        
        # Complete System Info
        if any(word in question_lower for word in ['system', 'computer', 'pc', 'কম্পিউটার', 'সিস্টেম']):
            cpu = info['hardware']['cpu']
            ram = info['hardware']['ram']
            os_info = info['software']['os']
            
            return {
                'status': 'success',
                'response': f"""🖥️ Complete System Information / সম্পূর্ণ সিস্টেম তথ্য:

💻 CPU:
  Processor / প্রসেসর: {cpu['name']}
  Cores / কোর: {cpu['physical_cores']} physical, {cpu['logical_cores']} logical
  Usage / ব্যবহার: {info['performance']['cpu_usage']}

💾 RAM:
  Total / মোট: {ram['total']}
  Used / ব্যবহৃত: {ram['used']}
  Available / উপলব্ধ: {ram['available']}
  Usage / ব্যবহার: {ram['percentage']}

🖥️ OS:
  System / সিস্টেম: {os_info['system']} {os_info['release']}
  Architecture / আর্কিটেকচার: {os_info['architecture']}

🌐 Network:
  IP Address / IP ঠিকানা: {info['network']['local_ip']}
  Hostname / হোস্টনাম: {info['network']['hostname']}

⚙️ Processes / প্রোগ্রাম: {info['processes']['total_processes']} running

Type 'help system' for more detailed information.
আরও বিস্তারিত তথ্যের জন্য 'help system' টাইপ করুন।""",
                'type': 'system_info'
            }
        
        # If no specific question matched, return general info
        return {
            'status': 'info',
            'response': """💡 I can answer questions about your system!
💡 আমি আপনার system সম্পর্কে প্রশ্নের উত্তর দিতে পারি!

Ask me about / আমাকে জিজ্ঞাসা করুন:
- CPU: "What is my CPU?" / "আমার CPU কি?"
- RAM: "How much RAM do I have?" / "আমার কত RAM আছে?"
- Disk: "How much disk space?" / "কত disk space আছে?"
- GPU: "What is my GPU?" / "আমার GPU কি?"
- OS: "What OS am I using?" / "আমি কোন OS ব্যবহার করছি?"
- Network: "What is my IP?" / "আমার IP কি?"
- Files: "How many files on desktop?" / "desktop এ কত files আছে?"
- Processes: "What programs are running?" / "কোন programs চলছে?"
- Performance: "How is my system performing?" / "আমার system কেমন চলছে?"
- Complete: "Tell me about my computer" / "আমার computer সম্পর্কে বলো"

Just ask naturally! / স্বাভাবিকভাবে জিজ্ঞাসা করুন!""",
            'type': 'system_help'
        }


def main():
    """Test system analyzer"""
    print("\n" + "="*80)
    print("  🖥️ JARVIS SYSTEM ANALYZER TEST")
    print("  🖥️ JARVIS সিস্টেম বিশ্লেষক টেস্ট")
    print("="*80)
    
    analyzer = SystemAnalyzer()
    
    # Test questions
    test_questions = [
        "What is my CPU?",
        "How much RAM do I have?",
        "What is my disk space?",
        "What is my GPU?",
        "What OS am I using?",
        "What is my IP address?",
        "How many files on desktop?",
        "What programs are running?",
        "How is my system performing?",
        "Tell me about my computer"
    ]
    
    print("\n🧪 Testing system questions:")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*80}")
        print(f"[{i}/{len(test_questions)}] Question: {question}")
        print(f"{'='*80}")
        
        result = analyzer.answer_question(question)
        print(f"\nStatus: {result['status']}")
        print(f"Response:\n{result['response']}")
    
    print("\n" + "="*80)
    print("✅ System Analyzer test complete!")
    print("="*80)


if __name__ == "__main__":
    main()
