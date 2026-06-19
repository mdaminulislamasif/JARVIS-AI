#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS COMPLETE SYSTEM CONTROL
================================
সব ধরনের system access একটা module এ
"""

import os, sys, subprocess, platform, ctypes
import threading, time, datetime, json
import webbrowser, shutil, winreg
import psutil, pyautogui, pyperclip

_BASE = os.path.dirname(os.path.abspath(__file__))

# ─── ADMIN CHECK ─────────────────────────────────────────────────────────────
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(cmd):
    """Run command as administrator"""
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/c {cmd}", None, 1)
        return True
    except:
        return False

# ─── 1-5: FILE & PROCESS CONTROL ─────────────────────────────────────────────
def file_read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"

def file_write(path, content):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Written: {path}"
    except Exception as e:
        return f"Error: {e}"

def file_delete(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        return f"Deleted: {path}"
    except Exception as e:
        return f"Error: {e}"

def process_list():
    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            procs.append(f"[{p.pid}] {p.name()} CPU:{p.cpu_percent():.1f}% MEM:{p.memory_percent():.1f}%")
        except:
            pass
    return "\n".join(procs[:30])

def process_kill(name_or_pid):
    killed = []
    for p in psutil.process_iter(["pid", "name"]):
        try:
            if str(name_or_pid).isdigit():
                if p.pid == int(name_or_pid):
                    p.terminate()
                    killed.append(f"Killed PID {p.pid}")
            else:
                if name_or_pid.lower() in p.name().lower():
                    p.terminate()
                    killed.append(f"Killed {p.name()} [{p.pid}]")
        except:
            pass
    return "\n".join(killed) if killed else "Process not found"

def run_command(cmd, shell=True, timeout=15):
    """Execute any shell command"""
    try:
        result = subprocess.run(
            cmd, shell=shell, capture_output=True,
            text=True, encoding='utf-8', errors='replace', timeout=timeout
        )
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        return (stdout + stderr).strip()
    except subprocess.TimeoutExpired:
        return "Command timed out"
    except Exception as e:
        return f"Error: {e}"

# ─── 6: MOUSE & KEYBOARD ─────────────────────────────────────────────────────
def mouse_move(x, y):
    pyautogui.moveTo(x, y, duration=0.3)
    return f"Mouse moved to ({x}, {y})"

def mouse_click(x=None, y=None, button="left", clicks=1):
    if x and y:
        pyautogui.click(x, y, clicks=clicks, button=button)
    else:
        pyautogui.click(clicks=clicks, button=button)
    return f"Clicked {button} x{clicks}"

def keyboard_type(text):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    return f"Typed: {text[:50]}"

def keyboard_press(keys):
    """Press key combination like ctrl+c, alt+f4"""
    parts = [k.strip() for k in keys.replace("+", " ").split()]
    pyautogui.hotkey(*parts)
    return f"Pressed: {keys}"

def keyboard_hotkey(combo):
    parts = combo.lower().replace("+", " ").split()
    pyautogui.hotkey(*parts)
    return f"Hotkey: {combo}"

# ─── 7-10: HARDWARE & SYSTEM INFO ────────────────────────────────────────────
def get_disk_info():
    info = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            info.append(f"{part.device} ({part.mountpoint}): "
                        f"Total={usage.total//1024**3}GB "
                        f"Used={usage.used//1024**3}GB "
                        f"Free={usage.free//1024**3}GB")
        except:
            pass
    return "\n".join(info)

def get_cpu_info():
    return (f"CPU: {platform.processor()}\n"
            f"Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count()} logical\n"
            f"Usage: {psutil.cpu_percent(interval=1)}%\n"
            f"Freq: {psutil.cpu_freq().current:.0f}MHz")

def get_memory_info():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return (f"RAM Total: {mem.total//1024**3}GB\n"
            f"RAM Used: {mem.used//1024**3}GB ({mem.percent}%)\n"
            f"RAM Free: {mem.available//1024**3}GB\n"
            f"Swap: {swap.total//1024**3}GB used {swap.percent}%")

def get_hardware_info():
    info = []
    info.append(f"OS: {platform.system()} {platform.release()} {platform.version()}")
    info.append(f"PC Name: {platform.node()}")
    info.append(f"Architecture: {platform.machine()}")
    info.append(get_cpu_info())
    info.append(get_memory_info())
    info.append(get_disk_info())
    return "\n".join(info)

def get_temperature():
    """Get CPU temperature"""
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                for entry in entries:
                    return f"{name}: {entry.current}°C"
        return "Temperature sensors not available (Windows)"
    except:
        # Try WMI on Windows
        try:
            result = run_command("wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature")
            return f"Thermal: {result}"
        except:
            return "Temperature: N/A"

# ─── 11: CAMERA ACCESS ───────────────────────────────────────────────────────
def take_photo(save_path=None):
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            if not save_path:
                save_path = os.path.join(_BASE, "jarvis_uploads",
                                         f"photo_{int(time.time())}.jpg")
            cv2.imwrite(save_path, frame)
            return f"Photo saved: {save_path}"
        return "Camera capture failed"
    except ImportError:
        return "opencv-python needed: pip install opencv-python"
    except Exception as e:
        return f"Camera error: {e}"

# ─── 12: SCREEN CAPTURE ──────────────────────────────────────────────────────
def screenshot(save_path=None):
    if not save_path:
        save_path = os.path.join(_BASE, "jarvis_uploads",
                                 f"screen_{int(time.time())}.png")
    pyautogui.screenshot(save_path)
    return f"Screenshot: {save_path}"

def get_screen_size():
    s = pyautogui.size()
    return f"Screen: {s.width}x{s.height}"

# ─── SCREEN RECORDING ────────────────────────────────────────────────────────
def start_screen_record():
    try:
        from jarvis_screen_recorder import screen_recorder
        return screen_recorder.start_recording()
    except Exception as e:
        return f"Error starting screen record: {e}"

def stop_screen_record():
    try:
        from jarvis_screen_recorder import screen_recorder
        return screen_recorder.stop_recording()
    except Exception as e:
        return f"Error stopping screen record: {e}"


# ─── 13: NETWORK ─────────────────────────────────────────────────────────────
def get_network_info():
    info = []
    import socket
    info.append(f"Hostname: {socket.gethostname()}")
    try:
        info.append(f"Local IP: {socket.gethostbyname(socket.gethostname())}")
    except:
        pass
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                info.append(f"{iface}: {addr.address}")
    return "\n".join(info)

def ping(host="8.8.8.8"):
    result = run_command(f"ping -n 1 {host}", timeout=5)
    return result

def get_wifi_password(ssid=None):
    if ssid:
        result = run_command(f'netsh wlan show profile name="{ssid}" key=clear')
    else:
        result = run_command("netsh wlan show profiles")
    return result

# ─── 14: LOCATION ────────────────────────────────────────────────────────────
def get_location():
    try:
        import urllib.request, json
        with urllib.request.urlopen("https://ipinfo.io/json", timeout=5) as r:
            data = json.loads(r.read())
            return (f"IP: {data.get('ip')}\n"
                    f"City: {data.get('city')}\n"
                    f"Region: {data.get('region')}\n"
                    f"Country: {data.get('country')}\n"
                    f"Coords: {data.get('loc')}")
    except Exception as e:
        return f"Location error: {e}"

# ─── 16: TASK SCHEDULER ──────────────────────────────────────────────────────
def schedule_task(name, command, time_str):
    """Schedule a Windows task"""
    result = run_command(
        f'schtasks /create /tn "{name}" /tr "{command}" /sc once /st {time_str} /f'
    )
    return result

def list_scheduled_tasks():
    return run_command("schtasks /query /fo list /v | findstr /i \"task name status\"")

# ─── 17: ENVIRONMENT VARIABLES ───────────────────────────────────────────────
def get_env(key=None):
    if key:
        return os.environ.get(key, f"{key} not found")
    return "\n".join([f"{k}={v}" for k, v in list(os.environ.items())[:20]])

def set_env_permanent(key, value):
    """Set permanent environment variable"""
    result = run_command(f'setx {key} "{value}"')
    os.environ[key] = value
    return result

# ─── 18: PYTHON PACKAGES ─────────────────────────────────────────────────────
def install_package(package):
    result = run_command(f"{sys.executable} -m pip install {package} -q", timeout=60)
    return result

def list_packages():
    result = run_command(f"{sys.executable} -m pip list --format=columns")
    return result

def install_all_jarvis_packages():
    """Install all packages JARVIS needs"""
    packages = [
        # Core
        "customtkinter", "Pillow", "psutil", "pyautogui", "pyperclip",
        # Voice
        "SpeechRecognition", "pyaudio", "edge-tts", "pyttsx3",
        # AI
        "google-genai", "requests",
        # Vision
        "opencv-python",
        # Crypto
        "cryptography",
        # Web
        "selenium", "beautifulsoup4", "lxml",
        # Data
        "pandas", "numpy",
        # Android
        "pure-python-adb",
        # Hacking/Security (ethical)
        "scapy", "python-nmap",
        # Automation
        "pywin32", "schedule",
    ]
    results = []
    for pkg in packages:
        print(f"Installing {pkg}...")
        r = install_package(pkg)
        results.append(f"{'OK' if 'error' not in r.lower() else 'FAIL'}: {pkg}")
    return "\n".join(results)

# ─── 19: HARDWARE DETECTION ──────────────────────────────────────────────────
def detect_hardware():
    info = []
    # USB devices
    usb = run_command("wmic path Win32_USBHub get Description,DeviceID")
    info.append(f"USB:\n{usb[:500]}")
    # Printers
    printers = run_command("wmic printer get name,status")
    info.append(f"Printers:\n{printers[:300]}")
    # Audio devices
    audio = run_command("wmic sounddev get name,status")
    info.append(f"Audio:\n{audio[:300]}")
    return "\n\n".join(info)

# ─── 20: SERVICE MANAGEMENT ──────────────────────────────────────────────────
def list_services(filter_str="running"):
    return run_command(f'sc query state= {filter_str} | findstr "SERVICE_NAME RUNNING"')

def service_start(name):
    return run_command(f"net start {name}")

def service_stop(name):
    return run_command(f"net stop {name}")

# ─── 24: STARTUP PROGRAMS ────────────────────────────────────────────────────
def get_startup_programs():
    result = run_command(
        'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"'
    )
    result += run_command(
        'reg query "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"'
    )
    return result

def add_startup(name, path):
    return run_command(
        f'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" '
        f'/v "{name}" /t REG_SZ /d "{path}" /f'
    )

# ─── 25: SYSTEM LOGS ─────────────────────────────────────────────────────────
def get_system_logs(count=20):
    return run_command(
        f"wevtutil qe System /c:{count} /f:text /rd:true"
    )

def get_app_logs(count=10):
    return run_command(
        f"wevtutil qe Application /c:{count} /f:text /rd:true"
    )

# ─── 27: USER MANAGEMENT ─────────────────────────────────────────────────────
def list_users():
    return run_command("net user")

def create_user(username, password):
    r1 = run_command(f'net user "{username}" "{password}" /add')
    return r1

def delete_user(username):
    return run_command(f'net user "{username}" /delete')

# ─── 28: SYSTEM TIME ─────────────────────────────────────────────────────────
def get_system_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def set_system_time(datetime_str):
    """Set system date/time (requires admin)"""
    return run_command(f'date {datetime_str}')

# ─── 30: FIREWALL ────────────────────────────────────────────────────────────
def firewall_status():
    return run_command("netsh advfirewall show allprofiles state")

def firewall_block(ip):
    return run_command(
        f'netsh advfirewall firewall add rule name="JARVIS Block {ip}" '
        f'dir=out action=block remoteip={ip}'
    )

def firewall_allow_port(port, protocol="TCP"):
    return run_command(
        f'netsh advfirewall firewall add rule name="JARVIS Allow {port}" '
        f'dir=in action=allow protocol={protocol} localport={port}'
    )

# ─── 33: USER PERMISSIONS ────────────────────────────────────────────────────
def change_file_permission(path, permission="F"):
    """F=Full, R=Read, W=Write"""
    user = os.environ.get("USERNAME", "Users")
    return run_command(f'icacls "{path}" /grant {user}:{permission}')

# ─── 35: REMOTE DESKTOP ──────────────────────────────────────────────────────
def enable_remote_desktop():
    cmds = [
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f',
        "netsh advfirewall firewall set rule group=\"remote desktop\" new enable=yes"
    ]
    return "\n".join(run_command(c) for c in cmds)

def get_rdp_info():
    return run_command('reg query "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server"')

# ─── 37: SHUTDOWN/REBOOT ─────────────────────────────────────────────────────
def shutdown(delay=0):
    return run_command(f"shutdown /s /t {delay}")

def restart(delay=0):
    return run_command(f"shutdown /r /t {delay}")

def cancel_shutdown():
    return run_command("shutdown /a")

# ─── 45: HARDWARE SENSORS ────────────────────────────────────────────────────
def get_sensors():
    info = []
    battery = psutil.sensors_battery()
    if battery:
        info.append(f"Battery: {battery.percent}% {'Charging' if battery.power_plugged else 'Discharging'}")
    info.append(f"CPU Usage: {psutil.cpu_percent(interval=0.5)}%")
    info.append(f"RAM Usage: {psutil.virtual_memory().percent}%")
    info.append(get_temperature())
    # Fan speed (Windows only via WMI)
    fan = run_command("wmic path Win32_Fan get ActiveCooling,DesiredSpeed 2>nul")
    if fan and "no instance" not in fan.lower():
        info.append(f"Fan: {fan[:100]}")
    return "\n".join(info)

# ─── 47: CLOUD STORAGE ───────────────────────────────────────────────────────
def open_onedrive():
    onedrive = os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive")
    if os.path.exists(onedrive):
        os.startfile(onedrive)
        return f"Opened OneDrive: {onedrive}"
    return "OneDrive not found"

# ─── 53: VISUAL PROCESSING ───────────────────────────────────────────────────
def analyze_screen_region(x=0, y=0, w=None, h=None):
    """Capture and describe screen region"""
    try:
        import PIL.ImageGrab as ImageGrab
        if w and h:
            img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
        else:
            img = ImageGrab.grab()
        path = os.path.join(_BASE, "jarvis_uploads", f"region_{int(time.time())}.png")
        img.save(path)
        return f"Screen region saved: {path}"
    except Exception as e:
        return f"Error: {e}"

# ─── 81: PERFORMANCE OPTIMIZATION ───────────────────────────────────────────
def optimize_performance():
    results = []
    # Kill memory-heavy processes (non-system)
    system_procs = {"system", "svchost.exe", "lsass.exe", "csrss.exe", "winlogon.exe"}
    for p in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            if p.memory_percent() > 5 and p.name().lower() not in system_procs:
                results.append(f"High memory: {p.name()} ({p.memory_percent():.1f}%)")
        except:
            pass
    # Empty recycle bin
    try:
        import winshell
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
        results.append("Recycle bin emptied")
    except:
        run_command("rd /s /q %systemdrive%\\$Recycle.bin")
        results.append("Recycle bin cleared")
    return "\n".join(results) if results else "System already optimized"

# ─── 82: PORT TROUBLESHOOTING ────────────────────────────────────────────────
def troubleshoot_port_conflict(port):
    """Find and kill processes listening on the specified port"""
    import psutil
    try:
        port = int(port)
    except ValueError:
        return f"Invalid port: {port}"
        
    killed_procs = []
    
    # Try netstat first (fast and reliable on Windows)
    try:
        output = run_command(f"netstat -ano | findstr :{port}")
        if output:
            lines = output.strip().split("\n")
            pids_to_kill = set()
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 5:
                    local_addr = parts[1]
                    if f":{port}" in local_addr:
                        pid = parts[-1]
                        if pid.isdigit() and int(pid) > 0:
                            pids_to_kill.add(int(pid))
            
            for pid in pids_to_kill:
                try:
                    p = psutil.Process(pid)
                    p_name = p.name()
                    p.terminate()
                    killed_procs.append(f"Killed process '{p_name}' (PID: {pid}) listening on port {port} via netstat")
                except Exception as pe:
                    try:
                        r = run_command(f"taskkill /F /PID {pid}")
                        killed_procs.append(f"Killed PID {pid} on port {port} via taskkill: {r}")
                    except Exception as te:
                        killed_procs.append(f"Failed to kill PID {pid}: {pe}, {te}")
    except Exception as e:
        pass

    # Fallback to psutil.net_connections only if netstat didn't find/kill anything
    if not killed_procs:
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr and conn.laddr.port == port:
                    pid = conn.pid
                    if pid:
                        try:
                            p = psutil.Process(pid)
                            p_name = p.name()
                            p.terminate()
                            killed_procs.append(f"Killed process '{p_name}' (PID: {pid}) listening on port {port} via net_connections")
                        except Exception as pe:
                            killed_procs.append(f"Failed to kill PID {pid}: {pe}")
        except Exception as e:
            pass

    return "\n".join(killed_procs) if killed_procs else f"No active process found listening on port {port}."

# ─── 83: REGISTRY MANAGEMENT ─────────────────────────────────────────────────
def registry_read(key_path, value_name):
    """Read a value from the Windows Registry"""
    try:
        parts = key_path.strip().split("\\", 1)
        root_name = parts[0].upper()
        subkey = parts[1] if len(parts) > 1 else ""
        
        root_map = {
            "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
            "HKCR": winreg.HKEY_CLASSES_ROOT,
            "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
            "HKCU": winreg.HKEY_CURRENT_USER,
            "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
            "HKLM": winreg.HKEY_LOCAL_MACHINE,
            "HKEY_USERS": winreg.HKEY_USERS,
            "HKU": winreg.HKEY_USERS,
            "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
            "HKCC": winreg.HKEY_CURRENT_CONFIG
        }
        
        root_key = root_map.get(root_name)
        if root_key is None:
            return f"Invalid root key: {root_name}. Use HKLM, HKCU, etc."
            
        with winreg.OpenKey(root_key, subkey, 0, winreg.KEY_READ) as key:
            val, val_type = winreg.QueryValueEx(key, value_name)
            type_names = {
                winreg.REG_SZ: "REG_SZ",
                winreg.REG_DWORD: "REG_DWORD",
                winreg.REG_BINARY: "REG_BINARY",
                winreg.REG_MULTI_SZ: "REG_MULTI_SZ",
                winreg.REG_EXPAND_SZ: "REG_EXPAND_SZ"
            }
            type_str = type_names.get(val_type, f"Type:{val_type}")
            return f"Path: {key_path}\nValue Name: {value_name}\nData: {val}\nType: {type_str}"
    except FileNotFoundError:
        return f"Registry key or value not found: {key_path} -> {value_name}"
    except Exception as e:
        return f"Error reading registry: {e}"

def registry_write(key_path, value_name, value, val_type_str="REG_SZ"):
    """Write or update a registry value"""
    try:
        parts = key_path.strip().split("\\", 1)
        root_name = parts[0].upper()
        subkey = parts[1] if len(parts) > 1 else ""
        
        root_map = {
            "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
            "HKCR": winreg.HKEY_CLASSES_ROOT,
            "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
            "HKCU": winreg.HKEY_CURRENT_USER,
            "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
            "HKLM": winreg.HKEY_LOCAL_MACHINE,
            "HKEY_USERS": winreg.HKEY_USERS,
            "HKU": winreg.HKEY_USERS,
            "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
            "HKCC": winreg.HKEY_CURRENT_CONFIG
        }
        
        root_key = root_map.get(root_name)
        if root_key is None:
            return f"Invalid root key: {root_name}."
            
        type_map = {
            "REG_SZ": winreg.REG_SZ,
            "REG_DWORD": winreg.REG_DWORD,
            "REG_BINARY": winreg.REG_BINARY,
            "REG_MULTI_SZ": winreg.REG_MULTI_SZ,
            "REG_EXPAND_SZ": winreg.REG_EXPAND_SZ
        }
        val_type = type_map.get(val_type_str.upper(), winreg.REG_SZ)
        
        if val_type == winreg.REG_DWORD:
            value = int(value)
        elif val_type == winreg.REG_BINARY:
            if isinstance(value, str):
                if value.startswith("0x") or value.startswith("0X"):
                    value = bytes.fromhex(value[2:])
                else:
                    value = value.encode('utf-8')
                    
        with winreg.CreateKeyEx(root_key, subkey, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, value_name, 0, val_type, value)
            return f"Successfully wrote value '{value_name}' to registry key '{key_path}'"
    except Exception as e:
        return f"Error writing registry: {e}"

def registry_delete(key_path, value_name=None):
    """Delete a registry key or value"""
    try:
        parts = key_path.strip().split("\\", 1)
        root_name = parts[0].upper()
        subkey = parts[1] if len(parts) > 1 else ""
        
        root_map = {
            "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
            "HKCR": winreg.HKEY_CLASSES_ROOT,
            "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
            "HKCU": winreg.HKEY_CURRENT_USER,
            "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
            "HKLM": winreg.HKEY_LOCAL_MACHINE,
            "HKEY_USERS": winreg.HKEY_USERS,
            "HKU": winreg.HKEY_USERS,
            "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
            "HKCC": winreg.HKEY_CURRENT_CONFIG
        }
        
        root_key = root_map.get(root_name)
        if root_key is None:
            return f"Invalid root key: {root_name}."
            
        if value_name:
            with winreg.OpenKey(root_key, subkey, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, value_name)
                return f"Successfully deleted registry value '{value_name}' from '{key_path}'"
        else:
            winreg.DeleteKey(root_key, subkey)
            return f"Successfully deleted registry key '{key_path}'"
    except FileNotFoundError:
        return f"Registry key or value not found: {key_path}"
    except Exception as e:
        return f"Error deleting registry: {e}"

# ─── 84: RESOURCE MANAGEMENT ─────────────────────────────────────────────────
def set_process_priority(pid_or_name, priority_class):
    """Set process priority class (CPU scheduling resource allocation)"""
    import psutil
    priority_map = {
        "idle": psutil.IDLE_PRIORITY_CLASS,
        "below_normal": psutil.BELOW_NORMAL_PRIORITY_CLASS,
        "normal": psutil.NORMAL_PRIORITY_CLASS,
        "above_normal": psutil.ABOVE_NORMAL_PRIORITY_CLASS,
        "high": psutil.HIGH_PRIORITY_CLASS,
        "realtime": psutil.REALTIME_PRIORITY_CLASS
    }
    pc = priority_map.get(priority_class.lower())
    if pc is None:
        return f"Invalid priority class: {priority_class}. Use: idle, below_normal, normal, above_normal, high, realtime"
        
    adjusted = []
    for p in psutil.process_iter(["pid", "name"]):
        try:
            match = False
            if str(pid_or_name).isdigit():
                if p.pid == int(pid_or_name):
                    match = True
            else:
                if pid_or_name.lower() in p.name().lower():
                    match = True
            if match:
                p.nice(pc)
                adjusted.append(f"Set PID {p.pid} ({p.name()}) priority to {priority_class}")
        except Exception as e:
            adjusted.append(f"Failed to set PID {p.pid} priority: {e}")
            
    return "\n".join(adjusted) if adjusted else f"No process found matching: {pid_or_name}"

# ─── 85: INTEGRATED DIAGNOSTICS & HEALING ────────────────────────────────────
def run_self_healing():
    """Run diagnostics and auto-healing checks in an isolated subprocess"""
    try:
        # Run using inline python code to avoid main() input prompt hanging the process
        cmd = f'{sys.executable} -X utf8 -c "from jarvis_self_healing import SelfHealingSystem; h = SelfHealingSystem(); h.run_self_diagnosis(); h.auto_fix_issues()"'
        result = run_command(cmd, timeout=120)
        return f"Self-healing complete. Execution details:\n{result[:1000]}"
    except Exception as e:
        return f"Self-healing run error: {e}"

# ─── MASTER CONTROL FUNCTION ─────────────────────────────────────────────────
def jarvis_execute(command: str, brain=None) -> str:
    """
    Master function — JARVIS দিয়ে যেকোনো system command execute করুন
    """
    cmd = command.lower().strip()

    # Port troubleshooting routing
    if cmd.startswith("port conflict "):
        return troubleshoot_port_conflict(command[14:].strip())
        
    # Registry management routing
    if cmd.startswith("reg read "):
        parts = command[9:].split(None, 1)
        if len(parts) >= 2:
            return registry_read(parts[0], parts[1])
        return "Usage: reg read [key_path] [value_name]"
        
    if cmd.startswith("reg write "):
        parts = command[10:].split(None, 3)
        if len(parts) >= 3:
            key_path = parts[0]
            val_name = parts[1]
            val_data = parts[2]
            val_type = parts[3] if len(parts) > 3 else "REG_SZ"
            return registry_write(key_path, val_name, val_data, val_type)
        return "Usage: reg write [key_path] [value_name] [value] [type]"
        
    if cmd.startswith("reg delete "):
        parts = command[11:].split(None, 1)
        if len(parts) >= 1:
            key_path = parts[0]
            val_name = parts[1] if len(parts) > 1 else None
            return registry_delete(key_path, val_name)
        return "Usage: reg delete [key_path] [value_name]"
        
    # Resource management routing
    if cmd.startswith("set priority "):
        parts = command[13:].split()
        if len(parts) >= 2:
            return set_process_priority(parts[0], parts[1])
        return "Usage: set priority [pid_or_name] [priority_class]"
        
    # Self-healing routing
    if "self heal" in cmd or "run self healing" in cmd or "heal system" in cmd:
        return run_self_healing()

    # Screen Recording routing
    if "start record" in cmd or "start screen record" in cmd:
        return start_screen_record()
    if "stop record" in cmd or "stop screen record" in cmd:
        return stop_screen_record()


    # File operations
    if cmd.startswith("read "):
        return file_read(command[5:].strip())
    if cmd.startswith("write "):
        parts = command[6:].split(" ", 1)
        return file_write(parts[0], parts[1] if len(parts) > 1 else "")
    if cmd.startswith("delete "):
        return file_delete(command[7:].strip())

    # Process
    if "process list" in cmd or "running apps" in cmd:
        return process_list()
    if cmd.startswith("kill "):
        return process_kill(command[5:].strip())
    if cmd.startswith("run "):
        return run_command(command[4:].strip())

    # Mouse/Keyboard
    if cmd.startswith("type "):
        return keyboard_type(command[5:].strip())
    if cmd.startswith("press "):
        return keyboard_press(command[6:].strip())
    if cmd.startswith("hotkey "):
        return keyboard_hotkey(command[7:].strip())
    if "mouse click" in cmd:
        return mouse_click()
    if cmd.startswith("move mouse "):
        parts = command[11:].split()
        if len(parts) >= 2:
            return mouse_move(int(parts[0]), int(parts[1]))

    # System info
    if "hardware info" in cmd or "system info" in cmd:
        return get_hardware_info()
    if "disk info" in cmd or "storage" in cmd:
        return get_disk_info()
    if "cpu" in cmd:
        return get_cpu_info()
    if "memory" in cmd or "ram" in cmd:
        return get_memory_info()
    if "temperature" in cmd or "temp" in cmd:
        return get_temperature()
    if "sensors" in cmd:
        return get_sensors()
    if "detect hardware" in cmd or "devices" in cmd:
        return detect_hardware()

    # Network
    if "network info" in cmd or "ip address" in cmd:
        return get_network_info()
    if cmd.startswith("ping "):
        return ping(command[5:].strip())
    if "wifi password" in cmd:
        return get_wifi_password()
    if "location" in cmd:
        return get_location()
    if "firewall status" in cmd:
        return firewall_status()

    # Screenshot/Camera
    if "screenshot" in cmd:
        return screenshot()
    if "photo" in cmd or "camera" in cmd:
        return take_photo()
    if "screen size" in cmd:
        return get_screen_size()

    # Services
    if "list services" in cmd:
        return list_services()
    if cmd.startswith("start service "):
        return service_start(command[14:].strip())
    if cmd.startswith("stop service "):
        return service_stop(command[13:].strip())

    # Users
    if "list users" in cmd:
        return list_users()
    if cmd.startswith("create user "):
        parts = command[12:].split()
        return create_user(parts[0], parts[1] if len(parts) > 1 else "Pass@123")

    # System
    if "system time" in cmd:
        return get_system_time()
    if "startup programs" in cmd:
        return get_startup_programs()
    if "system logs" in cmd:
        return get_system_logs()
    if "env var" in cmd or "environment" in cmd:
        return get_env()
    if "optimize" in cmd or "performance" in cmd:
        return optimize_performance()

    # Packages
    if cmd.startswith("install "):
        return install_package(command[8:].strip())
    if "install all" in cmd or "install packages" in cmd:
        return "Installing all packages... This takes a few minutes."
    if "list packages" in cmd:
        return list_packages()

    # Power
    if "shutdown" in cmd:
        return shutdown(30)
    if "restart" in cmd or "reboot" in cmd:
        return restart(30)
    if "cancel shutdown" in cmd:
        return cancel_shutdown()

    # Remote desktop
    if "enable remote" in cmd or "rdp" in cmd:
        return enable_remote_desktop()

    # Admin
    if "is admin" in cmd:
        return f"Admin: {'YES' if is_admin() else 'NO'}"

    return f"Command not recognized: {command}"


if __name__ == "__main__":
    print("JARVIS System Control Test")
    print(get_hardware_info())
    print("\n" + get_sensors())
    print("\n" + get_network_info())
