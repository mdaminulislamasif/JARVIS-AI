"""
JARVIS Windows 10 Intelligence & Control Engine
================================================
Handles:
1. Windows 10 knowledge & commands (in Bangla/Banglish)
2. App control (open, close, focus, type, etc.)
3. Mouse control (move, click, drag, scroll)
4. Keyboard control (press, hotkey, type text)
5. Screen/window management
"""

import os
import sys
import time
import subprocess
import threading
import pyautogui
import pyperclip
import psutil

# Safety: disable pyautogui failsafe for controlled operation
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05  # Fast but safe

# ══════════════════════════════════════════════════════════════
# WINDOWS 10 KNOWLEDGE BASE (Bangla + English)
# ══════════════════════════════════════════════════════════════

WIN10_KNOWLEDGE = {
    # Settings
    "settings": "ms-settings:",
    "time setting": "ms-settings:dateandtime",
    "display setting": "ms-settings:display",
    "sound setting": "ms-settings:sound",
    "wifi setting": "ms-settings:network-wifi",
    "bluetooth setting": "ms-settings:bluetooth",
    "update setting": "ms-settings:windowsupdate",
    "privacy setting": "ms-settings:privacy",
    "power setting": "ms-settings:powersleep",
    "storage setting": "ms-settings:storagesense",
    "apps setting": "ms-settings:appsfeatures",
    "startup setting": "ms-settings:startupapps",
    "notification setting": "ms-settings:notifications",
    "language setting": "ms-settings:regionlanguage",
    "account setting": "ms-settings:yourinfo",
    "taskbar setting": "ms-settings:taskbar",
    "mouse setting": "ms-settings:mousetouchpad",
    "keyboard setting": "ms-settings:typing",
    "firewall setting": "ms-settings:windowsdefender",
    "theme setting": "ms-settings:themes",
    "color setting": "ms-settings:colors",
    "night light": "ms-settings:nightlight",
}

WIN10_FOLDERS = {
    "desktop": os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\Default"), "Desktop"),
    "downloads": os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\Default"), "Downloads"),
    "documents": os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\Default"), "Documents"),
    "pictures": os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\Default"), "Pictures"),
    "music": os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\Default"), "Music"),
    "videos": os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\Default"), "Videos"),
    "appdata_local": os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\Default"), "AppData", "Local"),
    "appdata_roaming": os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\Default"), "AppData", "Roaming"),
    "temp": os.environ.get("TEMP", "C:\\Windows\\Temp"),
    "program_files": "C:\\Program Files",
    "program_files_x86": "C:\\Program Files (x86)",
    "system32": "C:\\Windows\\System32",
    "recycle_bin": "Recycle Bin",
}

WIN10_SHORTCUTS = {
    # Windows 10 built-in shortcuts
    "show desktop": ["win", "d"],
    "task view": ["win", "tab"],
    "action center": ["win", "a"],
    "settings": ["win", "i"],
    "search": ["win", "s"],
    "run dialog": ["win", "r"],
    "lock screen": ["win", "l"],
    "file explorer": ["win", "e"],
    "clipboard": ["win", "v"],
    "screenshot": ["win", "shift", "s"],
    "game bar": ["win", "g"],
    "minimize all": ["win", "m"],
    "restore all": ["win", "shift", "m"],
    "virtual desktop left": ["win", "ctrl", "left"],
    "virtual desktop right": ["win", "ctrl", "right"],
    "new virtual desktop": ["win", "ctrl", "d"],
    "close virtual desktop": ["win", "ctrl", "f4"],
    "split left": ["win", "left"],
    "split right": ["win", "right"],
    "maximize": ["win", "up"],
    "minimize": ["win", "down"],
    "task manager": ["ctrl", "shift", "esc"],
    "copy": ["ctrl", "c"],
    "paste": ["ctrl", "v"],
    "cut": ["ctrl", "x"],
    "undo": ["ctrl", "z"],
    "redo": ["ctrl", "y"],
    "select all": ["ctrl", "a"],
    "save": ["ctrl", "s"],
    "find": ["ctrl", "f"],
    "new tab": ["ctrl", "t"],
    "close tab": ["ctrl", "w"],
    "refresh": ["f5"],
    "fullscreen": ["f11"],
    "address bar": ["ctrl", "l"],
    "zoom in": ["ctrl", "="],
    "zoom out": ["ctrl", "-"],
    "zoom reset": ["ctrl", "0"],
    "new window": ["ctrl", "n"],
    "print": ["ctrl", "p"],
    "close window": ["alt", "f4"],
    "switch window": ["alt", "tab"],
    "next window": ["alt", "tab"],
    "force quit": ["ctrl", "shift", "esc"],
}

BANGLA_WIN10_COMMANDS = {
    # Bangla/Banglish to Windows 10 commands
    "ডেস্কটপ দেখাও": "show desktop",
    "ডেস্কটপ": "show desktop",
    "সেটিংস": "settings",
    "সার্চ": "search",
    "রান": "run dialog",
    "লক করো": "lock screen",
    "ফাইল এক্সপ্লোরার": "file explorer",
    "ক্লিপবোর্ড": "clipboard",
    "স্ক্রিনশট": "screenshot",
    "টাস্ক ম্যানেজার": "task manager",
    "মিনিমাইজ করো": "minimize",
    "ম্যাক্সিমাইজ করো": "maximize",
    "বাম স্প্লিট": "split left",
    "ডান স্প্লিট": "split right",
    "কপি করো": "copy",
    "পেস্ট করো": "paste",
    "কাটো": "cut",
    "আনডু করো": "undo",
    "রিডু করো": "redo",
    "সব সিলেক্ট": "select all",
    "সেভ করো": "save",
    "খোঁজো": "find",
    "নতুন ট্যাব": "new tab",
    "ট্যাব বন্ধ": "close tab",
    "রিফ্রেশ করো": "refresh",
    "ফুলস্ক্রিন": "fullscreen",
    "বন্ধ করো": "close window",
    "প্রিন্ট করো": "print",
    "জুম ইন": "zoom in",
    "জুম আউট": "zoom out",
    # Banglish
    "desktop dekhao": "show desktop",
    "settings kholo": "settings",
    "lock koro": "lock screen",
    "minimize koro": "minimize",
    "maximize koro": "maximize",
    "copy koro": "copy",
    "paste koro": "paste",
    "undo koro": "undo",
    "save koro": "save",
    "screenshot nao": "screenshot",
    "taskmanager kholo": "task manager",
    "file explorer kholo": "file explorer",
    "refresh koro": "refresh",
}

# ══════════════════════════════════════════════════════════════
# MOUSE CONTROL (Full precision)
# ══════════════════════════════════════════════════════════════

def mouse_move(x, y, duration=0.2):
    """Move mouse to specific coordinates"""
    try:
        screen_w, screen_h = pyautogui.size()
        x = max(0, min(int(x), screen_w - 1))
        y = max(0, min(int(y), screen_h - 1))
        pyautogui.moveTo(x, y, duration=duration)
        return f"🖱️ Mouse moved to ({x}, {y})"
    except Exception as e:
        return f"Mouse move failed: {e}"

def mouse_click(x=None, y=None, button="left", clicks=1, interval=0.1):
    """Click mouse at position"""
    try:
        if x is not None and y is not None:
            pyautogui.click(int(x), int(y), button=button, clicks=clicks, interval=interval)
            return f"🖱️ {button.upper()} clicked at ({x}, {y})"
        else:
            pyautogui.click(button=button, clicks=clicks, interval=interval)
            pos = pyautogui.position()
            return f"🖱️ {button.upper()} clicked at current position ({pos.x}, {pos.y})"
    except Exception as e:
        return f"Mouse click failed: {e}"

def mouse_double_click(x=None, y=None):
    """Double click"""
    try:
        if x is not None and y is not None:
            pyautogui.doubleClick(int(x), int(y))
            return f"🖱️ Double-clicked at ({x}, {y})"
        else:
            pyautogui.doubleClick()
            return "🖱️ Double-clicked at current position"
    except Exception as e:
        return f"Double click failed: {e}"

def mouse_right_click(x=None, y=None):
    """Right click"""
    return mouse_click(x, y, button="right")

def mouse_drag(x1, y1, x2, y2, duration=0.4):
    """Drag from one position to another"""
    try:
        pyautogui.moveTo(int(x1), int(y1), duration=0.1)
        pyautogui.dragTo(int(x2), int(y2), duration=duration, button="left")
        return f"🖱️ Dragged from ({x1},{y1}) to ({x2},{y2})"
    except Exception as e:
        return f"Drag failed: {e}"

def mouse_scroll(amount, x=None, y=None):
    """Scroll up (positive) or down (negative)"""
    try:
        if x is not None and y is not None:
            pyautogui.scroll(int(amount), x=int(x), y=int(y))
        else:
            pyautogui.scroll(int(amount))
        direction = "up" if int(amount) > 0 else "down"
        return f"🖱️ Scrolled {direction} by {abs(int(amount))} units"
    except Exception as e:
        return f"Scroll failed: {e}"

def mouse_position():
    """Get current mouse position"""
    try:
        pos = pyautogui.position()
        screen_w, screen_h = pyautogui.size()
        return f"🖱️ Mouse position: ({pos.x}, {pos.y}) | Screen: {screen_w}x{screen_h}"
    except Exception as e:
        return f"Position check failed: {e}"

def mouse_hold_click(x, y, duration=1.0, button="left"):
    """Hold click for specified duration"""
    try:
        pyautogui.mouseDown(int(x), int(y), button=button)
        time.sleep(duration)
        pyautogui.mouseUp(button=button)
        return f"🖱️ Held {button} click at ({x},{y}) for {duration}s"
    except Exception as e:
        return f"Hold click failed: {e}"

# ══════════════════════════════════════════════════════════════
# KEYBOARD CONTROL (Full control)
# ══════════════════════════════════════════════════════════════

def keyboard_type(text, interval=0.02):
    """Type text using keyboard"""
    try:
        pyperclip.copy(str(text))
        pyautogui.hotkey("ctrl", "v")
        return f"⌨️ Typed: {str(text)[:50]}{'...' if len(str(text)) > 50 else ''}"
    except Exception as e:
        return f"Type failed: {e}"

def keyboard_press(key):
    """Press a single key"""
    try:
        key = str(key).lower().strip()
        # Key name mappings for Bangla users
        key_map = {
            "enter": "enter",
            "এন্টার": "enter",
            "space": "space",
            "স্পেস": "space",
            "backspace": "backspace",
            "ব্যাকস্পেস": "backspace",
            "delete": "delete",
            "ডিলিট": "delete",
            "escape": "escape",
            "esc": "escape",
            "tab": "tab",
            "উপরে": "up",
            "নিচে": "down",
            "বামে": "left",
            "ডানে": "right",
            "home": "home",
            "end": "end",
            "pageup": "pageup",
            "pagedown": "pagedown",
            "f1": "f1", "f2": "f2", "f3": "f3", "f4": "f4",
            "f5": "f5", "f6": "f6", "f7": "f7", "f8": "f8",
            "f9": "f9", "f10": "f10", "f11": "f11", "f12": "f12",
        }
        actual_key = key_map.get(key, key)
        pyautogui.press(actual_key)
        return f"⌨️ Pressed: {actual_key}"
    except Exception as e:
        return f"Key press failed: {e}"

def keyboard_hotkey(*keys):
    """Press key combination (hotkey)"""
    try:
        # Parse and clean keys
        cleaned = []
        for k in keys:
            k = str(k).lower().strip().replace("windows", "win").replace("ctrl", "ctrl").replace("alt", "alt").replace("shift", "shift")
            cleaned.append(k)
        pyautogui.hotkey(*cleaned)
        return f"⌨️ Hotkey: {' + '.join(cleaned)}"
    except Exception as e:
        return f"Hotkey failed: {e}"

def keyboard_hold(key, duration=1.0):
    """Hold a key for duration"""
    try:
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)
        return f"⌨️ Held '{key}' for {duration}s"
    except Exception as e:
        return f"Key hold failed: {e}"

# ══════════════════════════════════════════════════════════════
# WINDOWS 10 SPECIFIC CONTROLS
# ══════════════════════════════════════════════════════════════

def win10_open_settings(page=""):
    """Open Windows 10 Settings (native app, not browser)"""
    try:
        uri = WIN10_KNOWLEDGE.get(page.lower(), "ms-settings:")
        if not uri.startswith("ms-settings"):
            uri = "ms-settings:"
        subprocess.Popen(f'start "" "{uri}"', shell=True)
        return f"⚙️ Windows Settings opened: {page or 'Home'}"
    except Exception as e:
        return f"Settings open failed: {e}"

def win10_shortcut(action):
    """Execute Windows 10 shortcut"""
    try:
        action_lower = action.lower().strip()
        
        # Check Bangla mapping first
        if action_lower in BANGLA_WIN10_COMMANDS:
            action_lower = BANGLA_WIN10_COMMANDS[action_lower]
        
        # Get shortcut keys
        keys = WIN10_SHORTCUTS.get(action_lower)
        if keys:
            pyautogui.hotkey(*keys)
            return f"⌨️ Windows 10 shortcut: {action} → {' + '.join(keys)}"
        
        return f"Unknown shortcut: {action}. Try: {', '.join(list(WIN10_SHORTCUTS.keys())[:10])}"
    except Exception as e:
        return f"Shortcut failed: {e}"

def win10_run_command(command):
    """Open Run dialog and execute command"""
    try:
        pyautogui.hotkey("win", "r")
        time.sleep(0.5)
        pyperclip.copy(command)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.2)
        pyautogui.press("enter")
        return f"⚡ Run command executed: {command}"
    except Exception as e:
        return f"Run command failed: {e}"

def win10_system_info():
    """Get comprehensive Windows 10 system information"""
    try:
        import platform
        info = []
        info.append("=== WINDOWS 10 SYSTEM INTELLIGENCE ===")
        
        # OS Info
        info.append(f"OS: {platform.system()} {platform.release()} ({platform.version()})")
        info.append(f"Machine: {platform.machine()} | Processor: {platform.processor()}")
        info.append(f"Computer Name: {os.environ.get('COMPUTERNAME', 'Unknown')}")
        info.append(f"User: {os.environ.get('USERNAME', 'Unknown')}")
        
        # Hardware
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('C:\\')
        
        info.append(f"\nCPU: {cpu_count} cores | Usage: {cpu_percent}%")
        info.append(f"RAM: {mem.total // (1024**3)}GB total | {mem.percent}% used | {mem.available // (1024**2)}MB free")
        info.append(f"C: Drive: {disk.total // (1024**3)}GB total | {disk.percent}% used | {disk.free // (1024**3)}GB free")
        
        # Network
        try:
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            info.append(f"\nHostname: {hostname} | Local IP: {local_ip}")
        except Exception:
            pass
        
        # Battery
        battery = psutil.sensors_battery()
        if battery:
            info.append(f"Battery: {battery.percent:.0f}% | {'Charging' if battery.power_plugged else 'On Battery'}")
        
        # Uptime
        import datetime
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        info.append(f"System Uptime: {str(uptime).split('.')[0]}")
        
        info.append("=== END SYSTEM REPORT ===")
        return "\n".join(info)
    except Exception as e:
        return f"System info failed: {e}"

def win10_manage_process(name, action="info"):
    """Manage Windows processes"""
    try:
        results = []
        name_lower = name.lower()
        
        if action == "kill":
            killed = 0
            for proc in psutil.process_iter(['name', 'pid']):
                if name_lower in proc.info['name'].lower():
                    try:
                        proc.kill()
                        killed += 1
                    except Exception:
                        pass
            return f"⚡ Killed {killed} process(es) matching '{name}'"
        
        elif action == "info":
            for proc in psutil.process_iter(['name', 'pid', 'cpu_percent', 'memory_percent', 'status']):
                if name_lower in proc.info['name'].lower():
                    results.append(f"PID {proc.info['pid']}: {proc.info['name']} | CPU: {proc.info['cpu_percent']}% | RAM: {proc.info['memory_percent']:.1f}% | {proc.info['status']}")
            if results:
                return f"Process info for '{name}':\n" + "\n".join(results[:10])
            return f"No process found matching '{name}'"
        
        elif action == "list":
            procs = []
            for proc in psutil.process_iter(['name', 'cpu_percent']):
                try:
                    procs.append(proc.info)
                except Exception:
                    pass
            top = sorted(procs, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:10]
            return "Top 10 Processes:\n" + "\n".join([f"  {p['name']} - {p['cpu_percent']}% CPU" for p in top])
        
        return f"Unknown action: {action}"
    except Exception as e:
        return f"Process management failed: {e}"

def win10_open_app(app_name):
    """Smart app opener with Windows 10 knowledge"""
    app_name = app_name.strip().lower()
    
    # Extended app database
    APP_DATABASE = {
        # Core Windows Apps
        "notepad": "notepad.exe",
        "নোটপ্যাড": "notepad.exe",
        "calculator": "calc.exe",
        "ক্যালকুলেটর": "calc.exe",
        "calc": "calc.exe",
        "paint": "mspaint.exe",
        "পেইন্ট": "mspaint.exe",
        "wordpad": "wordpad.exe",
        "explorer": "explorer.exe",
        "ফাইল এক্সপ্লোরার": "explorer.exe",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "powershell": "powershell.exe",
        "terminal": "wt.exe",
        "task manager": "taskmgr.exe",
        "taskmgr": "taskmgr.exe",
        "টাস্ক ম্যানেজার": "taskmgr.exe",
        "regedit": "regedit.exe",
        "control panel": "control.exe",
        "কন্ট্রোল প্যানেল": "control.exe",
        "device manager": "devmgmt.msc",
        "disk management": "diskmgmt.msc",
        "services": "services.msc",
        "event viewer": "eventvwr.msc",
        "system properties": "sysdm.cpl",
        "snipping tool": "snippingtool.exe",
        "magnifier": "magnify.exe",
        "narrator": "narrator.exe",
        "osk": "osk.exe",
        "on screen keyboard": "osk.exe",
        "sticky notes": "stikynot.exe",
        
        # Microsoft Office
        "word": "winword.exe",
        "ওয়ার্ড": "winword.exe",
        "excel": "excel.exe",
        "এক্সেল": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "পাওয়ারপয়েন্ট": "powerpnt.exe",
        "outlook": "outlook.exe",
        "access": "msaccess.exe",
        
        # Browsers
        "chrome": "chrome.exe",
        "ক্রোম": "chrome.exe",
        "edge": "msedge.exe",
        "firefox": "firefox.exe",
        "brave": "brave.exe",
        "opera": "opera.exe",
        
        # Dev Tools
        "vscode": "code.exe",
        "vs code": "code.exe",
        "visual studio code": "code.exe",
        "sublime": "sublime_text.exe",
        "notepad++": "notepad++.exe",
        "git bash": "git-bash.exe",
        
        # Media
        "vlc": "vlc.exe",
        "spotify": "spotify.exe",
        "windows media player": "wmplayer.exe",
        "photos": "ms-photos:",
        "camera": "microsoft.windows.camera:",
        
        # Communication
        "whatsapp": "https://web.whatsapp.com",
        "telegram": "https://web.telegram.org",
        "discord": "discord.exe",
        "zoom": "zoom.exe",
        "teams": "teams.exe",
        "skype": "skype.exe",
        
        # Utilities
        "7zip": "7zfm.exe",
        "winrar": "winrar.exe",
        "ccleaner": "ccleaner.exe",
        "putty": "putty.exe",
        "wireshark": "wireshark.exe",
        "obs": "obs64.exe",
        
        # Games
        "steam": "steam.exe",
        
        # Settings shortcuts  
        "settings": "ms-settings:",
        "সেটিংস": "ms-settings:",
        "time settings": "ms-settings:dateandtime",
        "টাইম সেটিংস": "ms-settings:dateandtime",
        "display settings": "ms-settings:display",
    }
    
    # Check database
    target = APP_DATABASE.get(app_name, app_name)
    
    try:
        if target.startswith("http://") or target.startswith("https://"):
            import webbrowser
            webbrowser.open(target)
            return f"🌐 Opened {app_name} in browser"
        elif target.startswith("ms-"):
            subprocess.Popen(f'start "" "{target}"', shell=True)
            return f"⚙️ Opened Windows app: {app_name}"
        elif target.endswith(".msc") or target.endswith(".cpl"):
            subprocess.Popen(["control", target], shell=True)
            return f"⚙️ Opened control: {app_name}"
        else:
            from engine.automation import resolve_app_path
            path = resolve_app_path(target)
            if path:
                try:
                    os.startfile(path)
                    return f"✅ Opened: {app_name} (Resolved to: {path})"
                except Exception as e:
                    return f"❌ Failed to launch resolved path: {path}. Error: {e}"
            else:
                try:
                    os.startfile(target)
                    return f"✅ Opened: {app_name}"
                except Exception:
                    try:
                        subprocess.Popen(f'start "" "{target}"', shell=True)
                        return f"✅ Sent open command for: {app_name}"
                    except Exception as e:
                        return f"❌ Failed to open {app_name}: {e}"

    except Exception as e:
        return f"❌ Failed to open {app_name}: {e}"

def win10_close_app(app_name):
    """Close an application"""
    try:
        app_name = app_name.strip().lower()
        if not app_name.endswith(".exe"):
            # Try to find and kill by name
            killed = 0
            for proc in psutil.process_iter(['name']):
                if app_name in proc.info['name'].lower():
                    try:
                        proc.kill()
                        killed += 1
                    except Exception:
                        pass
            if killed:
                return f"❌ Closed {killed} instance(s) of {app_name}"
            return f"No running process found for {app_name}"
        else:
            os.system(f"taskkill /f /im {app_name}")
            return f"❌ Force closed: {app_name}"
    except Exception as e:
        return f"Close app failed: {e}"

def win10_focus_window(window_title):
    """Bring a window to focus"""
    try:
        cmd = (
            "$wshell = New-Object -ComObject WScript.Shell; "
            f"$result = $wshell.AppActivate('{window_title}'); "
            "Write-Output $result"
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            capture_output=True, text=True, timeout=5
        )
        if "True" in result.stdout or result.returncode == 0:
            return f"✅ Focused window: {window_title}"
        return f"⚠️ Window not found: {window_title}"
    except Exception as e:
        return f"Focus failed: {e}"

def win10_list_windows():
    """List all open windows"""
    try:
        cmd = (
            "Get-Process | Where-Object {$_.MainWindowTitle -ne ''} | "
            "Select-Object ProcessName, Id, MainWindowTitle | "
            "Format-Table -AutoSize | Out-String -Width 200"
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            capture_output=True, text=True, timeout=10
        )
        return "=== OPEN WINDOWS ===\n" + (result.stdout.strip() or "No windows found")
    except Exception as e:
        return f"Window list failed: {e}"

def win10_volume_control(action, level=None):
    """Control Windows 10 volume"""
    try:
        if action == "up":
            for _ in range(5):
                pyautogui.press("volumeup")
            return "🔊 Volume increased"
        elif action == "down":
            for _ in range(5):
                pyautogui.press("volumedown")
            return "🔉 Volume decreased"
        elif action == "mute":
            pyautogui.press("volumemute")
            return "🔇 Volume muted/unmuted"
        elif action == "set" and level is not None:
            # Use PowerShell for precise volume control
            script = f"""
$vol = {int(level)} / 100.0;
$code = '[DllImport("user32.dll")] public static extern int SendMessage(IntPtr hWnd, int Msg, int wParam, int lParam);';
$wmType = Add-Type -MemberDefinition $code -Name WinUser -Namespace Win32 -PassThru;
for($i=0; $i -lt 100; $i++) {{ [void]$wmType::SendMessage(65535, 0x0319, 0, 589824); }}
for($i=0; $i -lt [Math]::Round({int(level)}/2); $i++) {{ [void]$wmType::SendMessage(65535, 0x0319, 0, 655360); }}
"""
            # Simpler approach: use nircmd if available, else use keystrokes
            steps = int(level) // 2
            pyautogui.press("volumemute")  # mute
            time.sleep(0.1)
            pyautogui.press("volumemute")  # unmute (reset)
            for _ in range(50):  # go to 0 first
                pyautogui.press("volumedown")
            for _ in range(steps):  # set to level
                pyautogui.press("volumeup")
            return f"🔊 Volume set to ~{level}%"
        return "Unknown volume action"
    except Exception as e:
        return f"Volume control failed: {e}"

def win10_brightness_control(level):
    """Control screen brightness (Windows 10)"""
    try:
        level = max(0, min(100, int(level)))
        cmd = f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})"
        subprocess.run(["powershell", "-Command", cmd], capture_output=True, timeout=5)
        return f"☀️ Brightness set to {level}%"
    except Exception as e:
        return f"Brightness control failed: {e}"

def win10_screen_info():
    """Get screen/display information"""
    try:
        screen_w, screen_h = pyautogui.size()
        
        cmd = "Get-WmiObject -Class Win32_VideoController | Select-Object Name, CurrentHorizontalResolution, CurrentVerticalResolution, CurrentRefreshRate | Format-List | Out-String"
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=5)
        
        return f"🖥️ Screen: {screen_w}x{screen_h}\n" + result.stdout.strip()
    except Exception as e:
        return f"Screen info failed: {e}"

# ══════════════════════════════════════════════════════════════
# MASTER COMMAND PARSER — Windows 10 + Mouse + Keyboard
# ══════════════════════════════════════════════════════════════

def windows_control(command_line=""):
    """
    Master controller for all Windows 10, Mouse, and Keyboard commands.
    
    Usage examples:
        windows mouse move 500 300
        windows mouse click
        windows mouse click 500 300
        windows mouse right 200 200
        windows mouse double 400 400
        windows mouse scroll -5
        windows mouse scroll 5 400 300
        windows mouse drag 100 100 500 500
        windows mouse position
        
        windows keyboard type Hello World
        windows keyboard press enter
        windows keyboard hotkey ctrl+c
        windows keyboard hotkey win+d
        windows keyboard hold ctrl 2
        
        windows app open chrome
        windows app close notepad
        windows app focus Calculator
        windows app list
        
        windows shortcut show desktop
        windows shortcut screenshot
        windows shortcut task manager
        windows shortcut minimize
        
        windows settings time
        windows settings display
        windows settings wifi
        
        windows system info
        windows system volume up
        windows system volume down
        windows system volume mute
        windows system brightness 70
        windows system screen
        windows system processes
        
        windows run notepad
        windows run calc
    """
    try:
        parts = (command_line or "").strip().split(None, 2)
        if not parts:
            return _windows_help()
        
        category = parts[0].lower()
        sub = parts[1].lower() if len(parts) > 1 else ""
        args = parts[2] if len(parts) > 2 else ""
        
        # ── MOUSE ──────────────────────────────────────────
        if category == "mouse":
            arg_parts = args.split()
            
            if sub == "move":
                if len(arg_parts) >= 2:
                    return mouse_move(arg_parts[0], arg_parts[1])
                return "Usage: windows mouse move X Y"
            
            elif sub in ["click", "left"]:
                if len(arg_parts) >= 2:
                    return mouse_click(arg_parts[0], arg_parts[1])
                return mouse_click()
            
            elif sub == "right":
                if len(arg_parts) >= 2:
                    return mouse_right_click(arg_parts[0], arg_parts[1])
                return mouse_right_click()
            
            elif sub == "double":
                if len(arg_parts) >= 2:
                    return mouse_double_click(arg_parts[0], arg_parts[1])
                return mouse_double_click()
            
            elif sub == "scroll":
                amount = int(arg_parts[0]) if arg_parts else -3
                x = arg_parts[1] if len(arg_parts) > 1 else None
                y = arg_parts[2] if len(arg_parts) > 2 else None
                return mouse_scroll(amount, x, y)
            
            elif sub == "drag":
                if len(arg_parts) >= 4:
                    return mouse_drag(arg_parts[0], arg_parts[1], arg_parts[2], arg_parts[3])
                return "Usage: windows mouse drag X1 Y1 X2 Y2"
            
            elif sub == "position":
                return mouse_position()
            
            elif sub == "hold":
                if len(arg_parts) >= 3:
                    return mouse_hold_click(arg_parts[0], arg_parts[1], float(arg_parts[2]))
                elif len(arg_parts) >= 2:
                    return mouse_hold_click(arg_parts[0], arg_parts[1])
                return "Usage: windows mouse hold X Y [duration]"
            
            return f"Unknown mouse command: {sub}. Options: move, click, right, double, scroll, drag, position, hold"
        
        # ── KEYBOARD ───────────────────────────────────────
        elif category == "keyboard":
            
            if sub == "type":
                if args:
                    return keyboard_type(args)
                return "Usage: windows keyboard type [text]"
            
            elif sub == "press":
                if args:
                    return keyboard_press(args.strip())
                elif sub:
                    return keyboard_press(sub)
                return "Usage: windows keyboard press [key]"
            
            elif sub == "hotkey":
                if args:
                    keys = [k.strip() for k in args.replace("+", " ").split()]
                    return keyboard_hotkey(*keys)
                return "Usage: windows keyboard hotkey ctrl+c"
            
            elif sub == "hold":
                key_args = args.split()
                if key_args:
                    dur = float(key_args[1]) if len(key_args) > 1 else 1.0
                    return keyboard_hold(key_args[0], dur)
                return "Usage: windows keyboard hold [key] [duration]"
            
            return f"Unknown keyboard command: {sub}. Options: type, press, hotkey, hold"
        
        # ── APP ────────────────────────────────────────────
        elif category == "app":
            
            if sub == "open":
                if args:
                    return win10_open_app(args)
                return "Usage: windows app open [app name]"
            
            elif sub == "close":
                if args:
                    return win10_close_app(args)
                return "Usage: windows app close [app name]"
            
            elif sub == "focus":
                if args:
                    return win10_focus_window(args)
                return "Usage: windows app focus [window title]"
            
            elif sub == "list":
                return win10_list_windows()
            
            elif sub == "kill":
                target = args or sub
                return win10_manage_process(target, "kill")
            
            elif sub == "info":
                if args:
                    return win10_manage_process(args, "info")
                return win10_manage_process("", "list")
            
            return f"Unknown app command: {sub}. Options: open, close, focus, list, kill, info"
        
        # ── SHORTCUT ───────────────────────────────────────
        elif category == "shortcut":
            action = (sub + " " + args).strip()
            return win10_shortcut(action)
        
        # ── SETTINGS ───────────────────────────────────────
        elif category == "settings":
            page = (sub + " " + args).strip()
            setting_key = page + " setting" if not page.endswith("setting") else page
            return win10_open_settings(setting_key)
        
        # ── SYSTEM ─────────────────────────────────────────
        elif category == "system":
            
            if sub == "info":
                return win10_system_info()
            
            elif sub == "volume":
                action = args.strip() if args else sub
                if not action:
                    action = "up"
                if action.isdigit():
                    return win10_volume_control("set", int(action))
                return win10_volume_control(action)
            
            elif sub == "brightness":
                level = int(args.strip()) if args.strip().isdigit() else 70
                return win10_brightness_control(level)
            
            elif sub == "screen":
                return win10_screen_info()
            
            elif sub == "processes":
                return win10_manage_process("", "list")
            
            elif sub in ["folders", "folder"]:
                requested_folder = args.strip().lower()
                if requested_folder in WIN10_FOLDERS:
                    return f"📁 Path of '{requested_folder}': {WIN10_FOLDERS[requested_folder]}"
                else:
                    lines = ["📁 WINDOWS 10 STANDARD DIRECTORIES:"]
                    for k, v in WIN10_FOLDERS.items():
                        lines.append(f"  • {k:18} : {v}")
                    return "\n".join(lines)
            
            elif sub == "sleep":
                subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
                return "💤 System going to sleep..."
            
            elif sub == "hibernate":
                subprocess.Popen("shutdown /h", shell=True)
                return "💤 Hibernating..."
            
            return f"Unknown system command: {sub}. Options: info, volume, brightness, screen, processes, sleep"
        
        # ── RUN ────────────────────────────────────────────
        elif category == "run":
            cmd = (sub + " " + args).strip()
            return win10_run_command(cmd)
        
        # ── HELP ───────────────────────────────────────────
        elif category in ["help", ""]:
            return _windows_help()
        
        # ── DIRECT SHORTCUT (e.g., "windows win+d") ────────
        else:
            if "+" in category:
                keys = [k.strip() for k in category.split("+")]
                return keyboard_hotkey(*keys)
            return _windows_help()
    
    except Exception as e:
        return f"Windows Control Error: {e}"

def _windows_help():
    return """═══ JARVIS WINDOWS 10 CONTROL ═══
🖱️ MOUSE:
  windows mouse move 500 300      → Move to (500,300)
  windows mouse click             → Left click here
  windows mouse click 500 300     → Click at (500,300)
  windows mouse right 200 200     → Right click
  windows mouse double 400 400    → Double click
  windows mouse scroll -5         → Scroll down 5
  windows mouse drag 100 100 500 500 → Drag
  windows mouse position          → Where is mouse?

⌨️ KEYBOARD:
  windows keyboard type Hello!    → Type text
  windows keyboard press enter    → Press Enter
  windows keyboard hotkey ctrl+c  → Copy
  windows keyboard hotkey win+d   → Show desktop
  windows keyboard hold ctrl 2    → Hold Ctrl 2s

📱 APPS:
  windows app open chrome         → Open Chrome
  windows app close notepad       → Close Notepad
  windows app focus Calculator    → Focus window
  windows app list                → List all windows

⚡ SHORTCUTS:
  windows shortcut show desktop
  windows shortcut screenshot
  windows shortcut task manager
  windows shortcut minimize / maximize

⚙️ SETTINGS:
  windows settings time           → Date & Time
  windows settings display        → Display
  windows settings wifi           → Network/WiFi

🖥️ SYSTEM:
  windows system info             → Full system report
  windows system volume up/down
  windows system brightness 70
  windows system processes

▶️ RUN:
  windows run calc                → Run Calculator
  windows run notepad             → Run Notepad
══════════════════════════════════"""


# Bangla/Banglish wrapper - maps common phrases to windows_control
def bangla_windows_command(text):
    """Parse Bangla/Banglish text and route to windows_control"""
    t = text.strip().lower()
    
    # Mouse patterns
    if "মাউস" in t or "mouse" in t:
        if "ক্লিক" in t or "click" in t:
            parts = t.split()
            nums = [p for p in parts if p.isdigit()]
            if len(nums) >= 2:
                return windows_control(f"mouse click {nums[0]} {nums[1]}")
            return windows_control("mouse click")
        if "স্ক্রোল" in t or "scroll" in t:
            if "উপরে" in t or "up" in t:
                return windows_control("mouse scroll 5")
            return windows_control("mouse scroll -5")
        if "ডানে" in t or "right" in t:
            return windows_control("mouse right")
        if "সরাও" in t or "move" in t:
            parts = t.split()
            nums = [p for p in parts if p.isdigit()]
            if len(nums) >= 2:
                return windows_control(f"mouse move {nums[0]} {nums[1]}")
        return mouse_position()
    
    # Keyboard patterns
    if "কীবোর্ড" in t or "keyboard" in t or "টাইপ" in t or "type" in t:
        if "টাইপ" in t or "type" in t:
            # Extract text to type
            for prefix in ["টাইপ করো", "type koro", "type"]:
                if prefix in t:
                    text_to_type = t.split(prefix, 1)[-1].strip()
                    if text_to_type:
                        return keyboard_type(text_to_type)
        if "এন্টার" in t or "enter" in t:
            return keyboard_press("enter")
        if "ব্যাকস্পেস" in t or "backspace" in t:
            return keyboard_press("backspace")
        if "ডিলিট" in t or "delete" in t:
            return keyboard_press("delete")
        if "স্পেস" in t or "space" in t:
            return keyboard_press("space")
    
    # Volume patterns
    if "ভলিউম" in t or "volume" in t or "শব্দ" in t or "sound" in t:
        if "বাড়াও" in t or "up" in t or "বেশি" in t:
            return win10_volume_control("up")
        if "কমাও" in t or "down" in t or "কম" in t:
            return win10_volume_control("down")
        if "বন্ধ" in t or "mute" in t or "নিরব" in t:
            return win10_volume_control("mute")
    
    # Brightness patterns
    if "ব্রাইটনেস" in t or "brightness" in t or "আলো" in t:
        import re
        nums = re.findall(r'\d+', t)
        if nums:
            return win10_brightness_control(int(nums[0]))
        if "বাড়াও" in t or "up" in t:
            return win10_brightness_control(80)
        if "কমাও" in t or "down" in t:
            return win10_brightness_control(40)
    
    # System info
    if "সিস্টেম ইনফো" in t or "system info" in t or "পিসি ইনফো" in t:
        return win10_system_info()
    
    # App open patterns
    if "খোলো" in t or "চালু করো" in t or "open" in t:
        for app in ["chrome", "notepad", "calculator", "word", "excel", "explorer", 
                    "ক্রোম", "নোটপ্যাড", "ক্যালকুলেটর"]:
            if app in t:
                return win10_open_app(app)
    
    # Shortcut detection
    for bangla_cmd, shortcut in BANGLA_WIN10_COMMANDS.items():
        if bangla_cmd in t:
            return win10_shortcut(shortcut)
    
    return None  # Not handled
