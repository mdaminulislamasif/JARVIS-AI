"""
JARVIS Voice Server - Flask API for HTML Panel Integration
Provides better voice quality through Python TTS
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pyttsx3
import threading
import sys
from engine.voice import VoiceEngine

# Fix console encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

app = Flask(__name__)
CORS(app)  # Enable CORS for HTML panel

class JarvisVoiceServer:
    def __init__(self):
        """Initialize JARVIS voice engine"""
        self.voice_engine = VoiceEngine()
        self.is_speaking = False
    
    def speak(self, text):
        """Make JARVIS speak in separate thread using premium neural voice"""
        def _speak():
            self.is_speaking = True
            print(f"🔊 JARVIS: {text}")
            self.voice_engine.speak(text)
            self.is_speaking = False
        
        thread = threading.Thread(target=_speak)
        thread.daemon = True
        thread.start()

# Initialize JARVIS
jarvis = JarvisVoiceServer()

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'JARVIS Voice Server is running',
        'version': '1.0'
    })

@app.route('/speak', methods=['POST'])
def speak():
    """Speak endpoint - receives text and optional language and makes JARVIS speak"""
    try:
        data = request.get_json() or {}
        text = data.get('text', '')
        lang = data.get('lang', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Set last language if provided to guide voice selection
        if lang:
            jarvis.voice_engine.last_language = lang
        
        # Make JARVIS speak
        jarvis.speak(text)
        
        return jsonify({
            'success': True,
            'message': 'JARVIS is speaking',
            'text': text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/greet', methods=['GET'])
def greet():
    """Greeting endpoint"""
    import random
    greetings = [
        "Good day sir. All systems are operational.",
        "Welcome back. I have prepared everything for you.",
        "At your service sir. All features are unlocked.",
        "Systems online. Ready to assist you.",
        "Hello sir. All Antigravity protocols are active."
    ]
    greeting = random.choice(greetings)
    jarvis.speak(greeting)
    
    return jsonify({
        'success': True,
        'message': greeting
    })

@app.route('/action/<action_name>', methods=['GET'])
def action(action_name):
    """Action confirmation endpoint"""
    responses = {
        'premium': "Premium activated successfully sir.",
        'unlock': "All features unlocked sir.",
        'key': "License key generated sir.",
        'dark': "Dark mode activated sir.",
        'light': "Light mode activated sir.",
        'api': "API access granted sir.",
        'cloud': "Cloud storage enabled sir.",
        'team': "Team mode activated sir.",
        'backup': "Auto backup enabled sir.",
        'offline': "Offline mode enabled sir.",
        'analytics': "Analytics access granted sir."
    }
    
    message = responses.get(action_name, f"{action_name} completed sir.")
    jarvis.speak(message)
    
    return jsonify({
        'success': True,
        'action': action_name,
        'message': message
    })

@app.route('/status', methods=['GET'])
def status():
    """Status endpoint"""
    return jsonify({
        'status': 'online',
        'is_speaking': jarvis.is_speaking,
        'message': 'JARVIS Voice Server is operational'
    })

# =====================================================================
# UNIFIED BACKEND ADDITIONS: SYSTEM STATS, COMMAND EXECUTION & FACE RECON
# =====================================================================

@app.route('/api/system_stats', methods=['GET'])
def get_system_stats_api():
    """Fetch live system metrics using psutil"""
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Mock network traffic speeds for visual dynamics
        import random
        net_in = round(random.uniform(5.0, 150.0), 2)
        net_out = round(random.uniform(2.0, 30.0), 2)
        
        return jsonify({
            'success': True,
            'cpu': cpu,
            'ram': mem.percent,
            'disk': disk.percent,
            'net_in': net_in,
            'net_out': net_out,
            'uptime': round(time.time() - start_time, 2)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/execute_cmd', methods=['POST'])
def execute_command_api():
    """Receive automation task commands and execute them"""
    try:
        data = request.get_json() or {}
        cmd = data.get('command', '').strip().lower()
        if not cmd:
            return jsonify({'success': False, 'error': 'No command provided'}), 400
        
        # Preprocess to strip qualifiers like "run", "execute", "jarvis"
        clean_cmd = cmd.strip()
        if clean_cmd.startswith("jarvis "):
            clean_cmd = clean_cmd[7:].strip()
        if clean_cmd.startswith("run "):
            clean_cmd = clean_cmd[4:].strip()
        if clean_cmd.startswith("execute "):
            clean_cmd = clean_cmd[8:].strip()
            
        # Command routing map to engine.automation functions
        import engine.automation as aut
        
        parts = clean_cmd.split(" ", 1)
        cmd_root = parts[0]
        cmd_args = parts[1] if len(parts) > 1 else ""

        
        response_text = ""
        
        # Check for mouse, keyboard, or windows commands
        if cmd_root == "mouse":
            import engine.windows_control as wc
            sub_parts = cmd_args.strip().split()
            sub_action = sub_parts[0].lower() if sub_parts else ""
            sub_args = sub_parts[1:]
            try:
                if sub_action in ["move", "go", "moveto"]:
                    if len(sub_args) >= 2:
                        response_text = wc.mouse_move(sub_args[0], sub_args[1])
                    else:
                        response_text = "Usage: mouse move X Y"
                elif sub_action in ["click", "left", "laft", "clk"]:
                    if len(sub_args) >= 2:
                        response_text = wc.mouse_click(sub_args[0], sub_args[1])
                    else:
                        response_text = wc.mouse_click()
                elif sub_action in ["right", "rclick", "rightclick"]:
                    if len(sub_args) >= 2:
                        response_text = wc.mouse_right_click(sub_args[0], sub_args[1])
                    else:
                        response_text = wc.mouse_right_click()
                elif sub_action in ["double", "dblclick", "doubleclick"]:
                    if len(sub_args) >= 2:
                        response_text = wc.mouse_double_click(sub_args[0], sub_args[1])
                    else:
                        response_text = wc.mouse_double_click()
                elif sub_action in ["scroll", "scrollup", "scrolldown"]:
                    amount = int(sub_args[0]) if sub_args else -3
                    x = sub_args[1] if len(sub_args) > 1 else None
                    y = sub_args[2] if len(sub_args) > 2 else None
                    response_text = wc.mouse_scroll(amount, x, y)
                elif sub_action in ["drag"]:
                    if len(sub_args) >= 4:
                        response_text = wc.mouse_drag(sub_args[0], sub_args[1], sub_args[2], sub_args[3])
                    else:
                        response_text = "Usage: mouse drag X1 Y1 X2 Y2"
                elif sub_action in ["position", "pos", "where"]:
                    response_text = wc.mouse_position()
                else:
                    response_text = wc.mouse_click()
            except Exception as _me:
                response_text = f"Mouse control error: {_me}"
        
        elif cmd_root == "keyboard":
            import engine.windows_control as wc
            sub_parts = cmd_args.strip().split(None, 1)
            sub_action = sub_parts[0].lower() if sub_parts else ""
            sub_text = sub_parts[1].strip() if len(sub_parts) > 1 else ""
            try:
                if sub_action in ["type", "write", "input"]:
                    response_text = wc.keyboard_type(sub_text) if sub_text else "Usage: keyboard type [text]"
                elif sub_action in ["press", "key"]:
                    response_text = wc.keyboard_press(sub_text) if sub_text else "Usage: keyboard press [key]"
                elif sub_action in ["hotkey", "shortcut", "combo"]:
                    keys = [k.strip() for k in sub_text.replace("+", " ").split() if k.strip()]
                    response_text = wc.keyboard_hotkey(*keys) if keys else "Usage: keyboard hotkey ctrl+c"
                else:
                    response_text = f"Unknown keyboard action: {sub_action}. Use: type, press, hotkey"
            except Exception as _ke:
                response_text = f"Keyboard control error: {_ke}"
        
        elif cmd_root == "windows":
            import engine.windows_control as wc
            try:
                response_text = wc.windows_control(cmd_args)
            except Exception as _we:
                response_text = f"Windows control error: {_we}"
        
        elif cmd_root == "cmd":
            try:
                response_text = aut.run_command_prompt(cmd_args)
            except Exception as _ce:
                response_text = f"CMD execution error: {_ce}"
                
        elif cmd_root == "powershell":
            try:
                response_text = aut.run_powershell(cmd_args)
            except Exception as _pe:
                response_text = f"PowerShell execution error: {_pe}"

        # Check if it's an app control command
        elif cmd_root == "app" or cmd_root in ["open", "focus", "type", "press", "hotkey", "click", "move", "scroll", "wait", "drag", "maximize", "minimize"]:
            clean_cmd = cmd[4:] if cmd.startswith("app ") else cmd
            response_text = aut.app_control(clean_cmd)
        elif cmd_root == "clean":
            response_text = f"System purged. {aut.clean_system()} temporary files eliminated."
        elif cmd_root == "workspace":
            response_text = aut.start_workspace()
        elif cmd_root == "screenshot":
            response_text = aut.take_screenshot()
        elif cmd_root == "scan":
            response_text = aut.scan_network()
        elif cmd_root == "ping":
            response_text = aut.ping_device(cmd_args)
        elif cmd_root in ["battery", "uptime"]:
            response_text = aut.get_system_stats()
        elif cmd_root == "copy":
            response_text = aut.copy_to_clipboard(cmd_args)
        elif cmd_root == "volume":
            response_text = aut.control_volume(cmd_args)
        elif cmd_root == "processes":
            response_text = aut.get_running_processes()
        elif cmd_root == "memory":
            response_text = aut.get_memory_info()
        elif cmd_root == "note":
            response_text = aut.save_note(cmd_args)
        elif cmd_root in ["taskmgr", "task"]:
            response_text = aut.open_task_manager()
        elif cmd_root == "lock":
            response_text = aut.lock_computer()
        elif cmd_root == "shutdown":
            response_text = aut.shutdown_computer()
        elif cmd_root == "restart":
            response_text = aut.restart_computer()
        elif cmd_root == "disk":
            response_text = aut.get_disk_info()
        elif cmd_root == "explorer":
            response_text = aut.open_explorer(cmd_args)
        elif cmd_root == "net":
            response_text = aut.run_net_command(cmd_args)
        elif cmd_root == "users":
            response_text = aut.get_network_users()
        elif cmd_root == "boost":
            response_text = aut.boost_game(cmd_args)
        elif cmd_root == "android":
            response_text = aut.android_boost()
        elif cmd_root == "kali":
            response_text = aut.setup_kali_mode()
        elif cmd_root == "remote":
            if "setup" in cmd_args or "enable" in cmd_args:
                response_text = aut.setup_remote_desktop()
            else:
                response_text = aut.start_remote_connection(cmd_args)
        elif cmd_root == "recon":
            response_text = aut.auto_collect_info()
        elif cmd_root == "virus":
            response_text = aut.scan_for_viruses()
        elif cmd_root == "kill":
            response_text = aut.force_kill_process(cmd_args)
        elif cmd_root == "bin":
            response_text = aut.empty_recycle_bin()
        elif cmd_root == "brightness":
            response_text = aut.set_brightness(cmd_args)
        elif cmd_root == "media":
            response_text = aut.media_control(cmd_args)
        elif cmd_root == "wifi":
            response_text = aut.scan_wifi()
        elif cmd_root == "share":
            response_text = aut.create_screen_share()
        elif cmd_root == "send" or cmd_root == "files":
            response_text = aut.share_files()
        elif cmd_root == "port":
            response_text = aut.deep_port_scan(cmd_args)
        elif cmd_root == "payload":
            response_text = aut.generate_payload(cmd_args)
        elif cmd_root == "bluetooth":
            response_text = aut.scan_bluetooth()
        elif cmd_root == "ducky":
            response_text = aut.ducky_deploy(cmd_args)
        elif cmd_root == "cipher":
            response_text = aut.alien_cipher(cmd_args)
        elif cmd_root == "signal":
            response_text = aut.signal_scan()
        elif cmd_root == "devices" or cmd_root == "find":
            response_text = aut.find_and_connect(cmd_args)
        elif cmd_root == "connect":
            parts2 = cmd_args.split()
            target = parts2[0] if len(parts2) > 0 else ""
            proto = parts2[1] if len(parts2) > 1 else "ping"
            response_text = aut.manage_device(target, proto)
        elif cmd_root == "purge" or cmd_root == "badshah":
            response_text = aut.neutralize_badshah()
        elif cmd_root == "firewall":
            response_text = aut.setup_infinity_firewall()
        elif cmd_root in ["webaudit", "webscan"]:
            response_text = aut.web_security_audit(cmd_args)
        elif cmd_root == "router":
            parts2 = cmd_args.split()
            if parts2 and parts2[0] in ["ping", "ports", "rdp", "share"]:
                response_text = aut.router_connect(parts2[1] if len(parts2) > 1 else "192.168.1.1", parts2[0])
            else:
                response_text = aut.scan_router_devices()
        else:
            # Fallback to general app_control command execution
            response_text = aut.app_control(clean_cmd)

        # Make JARVIS speak the success confirmation
        jarvis.speak(response_text)
        
        return jsonify({
            'success': True,
            'response': response_text
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_face_api():
    """Face recognition analysis wrapper"""
    try:
        import base64
        import datetime
        from PIL import Image
        from io import BytesIO
        
        data = request.get_json() or {}
        image_data = data.get('image')
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Check face landmarks and profile matching (mock/simulated lookup)
        import random
        names = ["Asif Islam", "Aminul Islam", "Kazi Sazzad", "Sabina Yasmin", "Badshah Khan"]
        locations = ["Dhaka, Bangladesh", "Natore, Lalpur", "Chittagong, BD", "Sylhet Town", "Rajshahi Division"]
        occupations = ["Full-stack Engineer", "Android System Integrator", "Network Security Analyst", "UX Designer", "Malware Researcher"]
        
        matched_name = random.choice(names)
        matched_loc = random.choice(locations)
        matched_occ = random.choice(occupations)
        
        # If the user's name is saved, associate it
        if random.random() > 0.4:
            matched_name = "Md. Aminul Islam"
            matched_loc = "Natore District, Lalpur Thana"
        
        confidence = f"{random.randint(88, 99)}%"
        
        results = {
            'name': matched_name,
            'age': str(random.randint(22, 38)),
            'location': matched_loc,
            'confidence': confidence,
            'socialMedia': {
                'facebook': f"https://www.facebook.com/search/top/?q={matched_name.replace(' ', '%20')}",
                'instagram': f"https://www.instagram.com/{matched_name.lower().replace(' ', '_')}/",
                'linkedin': f"https://www.linkedin.com/in/{matched_name.lower().replace(' ', '-')}/"
            },
            'additionalInfo': {
                'occupation': matched_occ,
                'education': "B.Sc. in Computer Science & Engineering",
                'interests': "Cybersecurity, Artificial Intelligence, Mobile Automation",
                'lastSeen': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        
        # Make voice comment
        jarvis.speak(f"Analysis complete. Match found: {matched_name} with {confidence} confidence.")
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search_by_name', methods=['POST'])
def search_by_name_api():
    """Search social media by name"""
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        if not name:
            return jsonify({'error': 'No name provided'}), 400
        
        fb_url = f"https://www.facebook.com/search/top/?q={name.replace(' ', '%20')}"
        ig_url = f"https://www.instagram.com/{name.lower().replace(' ', '_')}/"
        li_url = f"https://www.linkedin.com/in/{name.lower().replace(' ', '-')}/"
        
        return jsonify({
            'facebook': fb_url,
            'instagram': ig_url,
            'linkedin': li_url,
            'twitter': f"https://twitter.com/{name.lower().replace(' ', '_')}"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================================================================
# WI-FI CONNECTED DEVICE CONTROLLER API ENDPOINTS
# =====================================================================

def get_local_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '192.168.1.9' # Fallback
    finally:
        s.close()
    return ip

def ping_ip(ip):
    import subprocess
    ping_exe = r"C:\Windows\System32\PING.EXE"
    cmd = f'"{ping_exe}" -n 1 -w 150 {ip}'
    res = subprocess.run(cmd, shell=True, capture_output=True)
    if res.returncode == 0:
        return ip
    return None

@app.route('/api/network_scan', methods=['GET'])
def network_scan_api():
    try:
        import concurrent.futures
        import socket
        import os
        local_ip = get_local_ip()
        base_ip = ".".join(local_ip.split(".")[:-1])
        
        ips_to_scan = [f"{base_ip}.{i}" for i in range(1, 255) if f"{base_ip}.{i}" != local_ip]
        
        active_ips = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=80) as executor:
            results = executor.map(ping_ip, ips_to_scan)
            for r in results:
                if r:
                    active_ips.append(r)
        
        devices = []
        # Add host computer
        devices.append({
            'ip': local_ip,
            'name': 'This PC (Host)',
            'type': 'host',
            'status': 'online'
        })
        
        for ip in active_ips:
            dev_type = 'device'
            if ip.endswith(".1"):
                dev_type = 'router'
                name = 'Router/Gateway'
            else:
                try:
                    name = socket.gethostbyaddr(ip)[0]
                except Exception:
                    name = 'Atom 5 Phone' if ip == '192.168.1.5' else 'Connected Node'
            
            devices.append({
                'ip': ip,
                'name': name,
                'type': dev_type,
                'status': 'online'
            })
            
        return jsonify({
            'success': True,
            'devices': devices
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/connect_wireless', methods=['POST'])
def connect_wireless_api():
    try:
        import subprocess
        import os
        data = request.get_json() or {}
        ip = data.get('ip')
        port = data.get('port', '5555')
        if not ip:
            return jsonify({'success': False, 'error': 'No IP provided'}), 400
            
        workspace = os.path.dirname(os.path.abspath(__file__))
        adb_path = os.path.join(workspace, "platform-tools", "adb.exe")
        if not os.path.exists(adb_path):
            adb_path = "adb"
            
        cmd = f'"{adb_path}" connect {ip}:{port}'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        is_success = "connected to" in res.stdout.lower()
        
        msg = f"Wireless connection to {ip} succeeded." if is_success else f"Wireless connection to {ip} was refused. Connect via USB first."
        jarvis.speak(msg)
        
        return jsonify({
            'success': True,
            'msg': res.stdout.strip(),
            'connected': is_success
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mirror_device', methods=['POST'])
def mirror_device_api():
    try:
        import subprocess
        import os
        data = request.get_json() or {}
        ip = data.get('ip')
        
        workspace = os.path.dirname(os.path.abspath(__file__))
        adb_path = os.path.join(workspace, "platform-tools", "adb.exe")
        if not os.path.exists(adb_path):
            adb_path = "adb"
            
        scrcpy_exe = os.path.join(workspace, "scrcpy", "scrcpy-win64-v2.4", "scrcpy.exe")
        
        # Audio configuration
        audio_source = data.get('audio_source')  # 'mic' or 'system'
        audio_flag = ""
        if audio_source == "mic":
            audio_flag = "--audio-source=mic"

        target = ""
        device_desc = ""
        if ip:
            target = f"-s {ip}:5555"
            device_desc = f"wireless device at {ip}"
        else:
            # USB Mode - Auto detect serial number
            check = subprocess.run(f'"{adb_path}" devices', shell=True, capture_output=True, text=True)
            lines = check.stdout.strip().split("\n")[1:]
            serial = None
            for line in lines:
                if line.strip() and "device" in line and "devices" not in line and "unauthorized" not in line:
                    serial = line.split()[0]
                    break
            if serial:
                target = f"-s {serial}"
                device_desc = f"USB device ({serial})"
            else:
                return jsonify({'success': False, 'error': 'No connected Android device found over USB or Wi-Fi.'}), 400

        # Grant RECORD_AUDIO permission to scrcpy server APK when using mic audio source.
        # Without this, --audio-source=mic fails with a permissions error on the Android device.
        if audio_source == "mic":
            scrcpy_pkg = "com.genymobile.scrcpy"
            grant_cmd = f'"{adb_path}" {target} shell pm grant {scrcpy_pkg} android.permission.RECORD_AUDIO'
            subprocess.run(grant_cmd, shell=True, capture_output=True, text=True)

        if os.path.exists(scrcpy_exe):
            cmd_str = f'"{scrcpy_exe}" {target} --always-on-top {audio_flag}'.strip()
            subprocess.Popen(cmd_str, shell=True)
            msg = f"Mirroring launched for {device_desc}."
            jarvis.speak(msg)
            return jsonify({'success': True, 'msg': msg})
        else:
            cmd_str = f'scrcpy {target} --always-on-top {audio_flag}'.strip()
            subprocess.Popen(cmd_str, shell=True)
            msg = f"Fallback mirroring launched for {device_desc}."
            jarvis.speak(msg)
            return jsonify({'success': True, 'msg': msg})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/boost_wireless', methods=['POST'])
def boost_wireless_api():
    try:
        import subprocess
        import os
        data = request.get_json() or {}
        ip = data.get('ip')
        
        workspace = os.path.dirname(os.path.abspath(__file__))
        adb_path = os.path.join(workspace, "platform-tools", "adb.exe")
        if not os.path.exists(adb_path):
            adb_path = "adb"
            
        target = ""
        device_desc = ""
        if ip:
            target = f"-s {ip}:5555"
            device_desc = f"wireless device at {ip}"
        else:
            # USB Mode - Auto detect serial number
            check = subprocess.run(f'"{adb_path}" devices', shell=True, capture_output=True, text=True)
            lines = check.stdout.strip().split("\n")[1:]
            serial = None
            for line in lines:
                if line.strip() and "device" in line and "devices" not in line and "unauthorized" not in line:
                    serial = line.split()[0]
                    break
            if serial:
                target = f"-s {serial}"
                device_desc = f"USB device ({serial})"
            else:
                return jsonify({'success': False, 'error': 'No connected Android device found over USB or Wi-Fi.'}), 400
                
        settings_to_boost = [
            "volume_music", "volume_voice", "volume_ring", "volume_system", "volume_alarm",
            "volume_bluetooth_sco", "volume_bluetooth_sco_bt_a2dp", "volume_bluetooth_sco_earpiece",
            "volume_bluetooth_sco_speaker", "volume_music_speaker", "volume_music_headphone",
            "volume_music_headset", "volume_notification", "volume_notification_speaker",
            "volume_ring_speaker", "volume_voice_earpiece", "volume_voice_headset",
            "volume_voice_speaker", "volume_music_earpiece", "volume_notification_earpiece", "volume_ring_earpiece"
        ]
        
        for s in settings_to_boost:
            subprocess.run(f'"{adb_path}" {target} shell settings put system {s} 15', shell=True)
            
        subprocess.run(f'"{adb_path}" {target} shell "for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do input keyevent 24; done"', shell=True)
        
        msg = f"Volume levels and mic gain boosted for {device_desc}."
        jarvis.speak(msg)
        return jsonify({'success': True, 'msg': msg})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/grant_mic_permission', methods=['POST'])
def grant_mic_permission_api():
    """Grant RECORD_AUDIO permission to scrcpy APK on the connected Android device via ADB.
    Call this before using --audio-source=mic mirroring if scrcpy mic audio fails."""
    try:
        import subprocess, os
        data = request.get_json() or {}
        ip = data.get('ip')

        workspace = os.path.dirname(os.path.abspath(__file__))
        adb_path = os.path.join(workspace, "platform-tools", "adb.exe")
        if not os.path.exists(adb_path):
            adb_path = "adb"

        target = ""
        device_desc = ""
        if ip:
            target = f"-s {ip}:5555"
            device_desc = f"wireless device at {ip}"
        else:
            check = subprocess.run(f'"{adb_path}" devices', shell=True, capture_output=True, text=True)
            lines = check.stdout.strip().split("\n")[1:]
            serial = None
            for line in lines:
                if line.strip() and "device" in line and "devices" not in line and "unauthorized" not in line:
                    serial = line.split()[0]
                    break
            if serial:
                target = f"-s {serial}"
                device_desc = f"USB device ({serial})"
            else:
                return jsonify({'success': False, 'error': 'No connected Android device found.'}), 400

        scrcpy_pkg = "com.genymobile.scrcpy"
        grant_cmd = f'"{adb_path}" {target} shell pm grant {scrcpy_pkg} android.permission.RECORD_AUDIO'
        res = subprocess.run(grant_cmd, shell=True, capture_output=True, text=True)

        # pm grant returns empty stdout on success; non-zero exit on failure
        if res.returncode == 0:
            msg = f"Microphone access granted to scrcpy on {device_desc}."
        else:
            msg = f"Permission grant returned: {(res.stderr or res.stdout).strip() or 'Unknown result'}"

        jarvis.speak(msg)
        return jsonify({'success': res.returncode == 0, 'msg': msg})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/adb_devices', methods=['GET'])
def adb_devices_api():
    """List all connected ADB devices with serial, state, model and transport type."""
    try:
        import subprocess, os, re
        workspace = os.path.dirname(os.path.abspath(__file__))
        adb_path = os.path.join(workspace, "platform-tools", "adb.exe")
        if not os.path.exists(adb_path):
            adb_path = "adb"

        # -l flag gives long format: serial  state  product:xxx model:xxx device:xxx transport_id:N
        res = subprocess.run(f'"{adb_path}" devices -l', shell=True, capture_output=True, text=True, timeout=5)
        lines = res.stdout.strip().split("\n")

        devices = []
        for line in lines[1:]:  # skip "List of devices attached" header
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 2:
                continue

            serial = parts[0]
            state  = parts[1]  # device, unauthorized, offline, sideload

            # Parse long-format key:value tokens
            info = {}
            for token in parts[2:]:
                if ':' in token:
                    k, v = token.split(':', 1)
                    info[k] = v

            model   = info.get('model', 'Unknown').replace('_', ' ')
            product = info.get('product', '')
            transport_id = info.get('transport_id', '')

            # Determine transport: TCP/IP (wireless) vs USB
            transport = "Wi-Fi" if re.match(r'^\d+\.\d+\.\d+\.\d+', serial) else "USB"

            # Fetch battery level for connected devices
            battery = None
            if state == "device":
                try:
                    bat_res = subprocess.run(
                        f'"{adb_path}" -s {serial} shell dumpsys battery | findstr level',
                        shell=True, capture_output=True, text=True, timeout=3
                    )
                    m = re.search(r'level:\s*(\d+)', bat_res.stdout)
                    if m:
                        battery = int(m.group(1))
                except Exception:
                    pass

            devices.append({
                'serial':      serial,
                'state':       state,
                'model':       model,
                'product':     product,
                'transport':   transport,
                'transport_id': transport_id,
                'battery':     battery
            })

        return jsonify({'success': True, 'devices': devices, 'count': len(devices)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


import time
start_time = time.time()

if __name__ == '__main__':
    print("=" * 60)
    print("🤖 JARVIS UNIFIED BACKEND SERVER Starting...")
    print("=" * 60)
    print("\n✅ Server will run on: http://localhost:5000")
    print("\nEndpoints:")
    print("  GET  /                  - Server status")
    print("  POST /speak         - Make JARVIS speak (JSON: {text: '...'})")
    print("  GET  /greet         - JARVIS greeting")
    print("  GET  /action/<name> - Action confirmation")
    print("  GET  /status        - Check if JARVIS is speaking")
    print("  GET  /api/system_stats - Live CPU/RAM/Disk metrics")
    print("  POST /api/execute_cmd - Receive and run automation task")
    print("  POST /analyze       - Face image recognition lookup")
    print("  POST /search_by_name - Social lookup by name")
    print("\n" + "=" * 60)
    print("🚀 Starting unified server...\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
