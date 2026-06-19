import http.server
import socketserver
import socket
import threading
import os
import io
import base64
import time

PORT = 5000

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception as e:

        print(f"⚠️ Error: {e}")
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def capture_screen_jpeg():
    """Capture screen and return as JPEG bytes."""
    try:
        import pyautogui
        from PIL import Image
        img = pyautogui.screenshot()
        img = img.resize((960, 540))  # Half resolution for speed
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=60)
        return buf.getvalue()
    except Exception as e:
        print(f"[SCREEN] Capture error: {e}")
        return b''

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>JARVIS MOBILE REMOTE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: #02050A; color: #00F3FF; font-family: 'Courier New', monospace; touch-action: none; overflow: hidden; }}
        #header {{ background: #05080F; border-bottom: 1px solid #002233; padding: 10px 20px; display: flex; align-items: center; justify-content: space-between; }}
        #header h1 {{ font-size: 16px; color: #00F3FF; text-shadow: 0 0 10px #00F3FF; }}
        #status {{ font-size: 11px; color: #00FF41; }}
        #screen-container {{ width: 100vw; position: relative; }}
        #live-screen {{ width: 100%; display: block; border-bottom: 1px solid #002233; }}
        #controls {{ padding: 10px; }}
        .btn-row {{ display: flex; gap: 8px; margin-bottom: 8px; }}
        .btn {{ background: #002233; color: #00F3FF; border: 1px solid #00F3FF; padding: 12px; font-size: 14px; cursor: pointer; border-radius: 8px; flex: 1; text-align: center; font-family: 'Courier New'; transition: all 0.1s; }}
        .btn:active {{ background: #00F3FF; color: #02050A; transform: scale(0.95); }}
        .btn-red {{ border-color: #FF3131; color: #FF3131; }}
        .btn-red:active {{ background: #FF3131; color: #02050A; }}
        .btn-green {{ border-color: #00FF41; color: #00FF41; }}
        .btn-green:active {{ background: #00FF41; color: #02050A; }}
        #trackpad {{ width: 100%; height: 120px; background: #001122; border: 1px dashed #004466; border-radius: 10px; margin-bottom: 8px; display: flex; align-items: center; justify-content: center; color: #004466; font-size: 12px; cursor: crosshair; }}
        #typer-row {{ display: flex; gap: 8px; }}
        #typer {{ flex: 1; background: #000; color: #00F3FF; border: 1px solid #004466; padding: 10px; font-size: 14px; border-radius: 8px; font-family: 'Courier New'; }}
    </style>
</head>
<body>
    <div id="header">
        <h1>⚡ ANTIGRAVITY REMOTE</h1>
        <span id="status">LIVE</span>
    </div>
    <div id="screen-container">
        <img id="live-screen" src="/screen" alt="Live Screen">
    </div>
    <div id="controls">
        <div id="trackpad">TOUCH TO MOVE MOUSE</div>
        <div class="btn-row">
            <div class="btn" ontouchstart="send('click')">L-CLICK</div>
            <div class="btn" ontouchstart="send('rclick')">R-CLICK</div>
            <div class="btn" ontouchstart="send('dclick')">D-CLICK</div>
        </div>
        <div class="btn-row">
            <div class="btn" ontouchstart="send('volup')">VOL +</div>
            <div class="btn" ontouchstart="send('voldown')">VOL -</div>
            <div class="btn" ontouchstart="send('mute')">MUTE</div>
        </div>
        <div class="btn-row">
            <div class="btn" ontouchstart="send('scrollup')">SCROLL ↑</div>
            <div class="btn" ontouchstart="send('scrolldown')">SCROLL ↓</div>
            <div class="btn btn-green" ontouchstart="send('screenshot')">SNAP</div>
        </div>
        <div class="btn-row">
            <div class="btn btn-red" ontouchstart="send('lock')">LOCK PC</div>
            <div class="btn btn-red" ontouchstart="send('taskmgr')">TASK MGR</div>
        </div>
        <div id="typer-row">
            <input type="text" id="typer" placeholder="Type text to inject..." autocomplete="off">
            <div class="btn btn-green" onclick="typeText()">SEND</div>
        </div>
    </div>

    <script>
        // === LIVE SCREEN REFRESH ===
        const screen = document.getElementById('live-screen');
        function refreshScreen() {{
            screen.src = '/screen?' + Date.now();
        }}
        setInterval(refreshScreen, 800); // Refresh every 800ms

        // === TRACKPAD ===
        const trackpad = document.getElementById('trackpad');
        let lastX = 0, lastY = 0, tracking = false;
        trackpad.addEventListener('touchstart', e => {{
            lastX = e.touches[0].clientX;
            lastY = e.touches[0].clientY;
            tracking = true;
            e.preventDefault();
        }}, {{passive: false}});
        trackpad.addEventListener('touchmove', e => {{
            if (!tracking) return;
            const dx = (e.touches[0].clientX - lastX) * 3;
            const dy = (e.touches[0].clientY - lastY) * 3;
            lastX = e.touches[0].clientX;
            lastY = e.touches[0].clientY;
            fetch('/mouse/' + Math.round(dx) + '/' + Math.round(dy));
            e.preventDefault();
        }}, {{passive: false}});
        trackpad.addEventListener('touchend', () => {{ tracking = false; }});

        // === COMMANDS ===
        function send(cmd) {{ fetch('/cmd/' + cmd); }}
        function typeText() {{
            const t = document.getElementById('typer').value;
            if (t) {{
                fetch('/type/' + btoa(unescape(encodeURIComponent(t))));
                document.getElementById('typer').value = '';
            }}
        }}
    </script>
</body>
</html>
"""

class RemoteHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress access logs

    def do_GET(self):
        import pyautogui

        # Serve main page
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())

        # Live screen capture
        elif self.path.startswith('/screen'):
            jpg = capture_screen_jpeg()
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.send_header('Content-Length', str(len(jpg)))
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(jpg)

        # Mouse movement (relative)
        elif self.path.startswith('/mouse/'):
            try:
                parts = self.path.split('/')
                dx, dy = int(parts[2]), int(parts[3])
                pyautogui.moveRel(dx, dy, duration=0)
            except Exception as e:
                print(f"⚠️ Error: {e}")
            self._ok()

        # Text injection
        elif self.path.startswith('/type/'):
            try:
                encoded = self.path.split('/')[-1]
                text = base64.b64decode(encoded).decode('utf-8')
                pyautogui.write(text, interval=0.02)
            except Exception as e:
                print(f"⚠️ Error: {e}")
            self._ok()

        # Commands
        elif self.path.startswith('/cmd/'):
            cmd = self.path.split('/')[-1]
            try:
                if cmd == 'click':      pyautogui.click()
                elif cmd == 'rclick':   pyautogui.rightClick()
                elif cmd == 'dclick':   pyautogui.doubleClick()
                elif cmd == 'volup':    pyautogui.press('volumeup')
                elif cmd == 'voldown':  pyautogui.press('volumedown')
                elif cmd == 'mute':     pyautogui.press('volumemute')
                elif cmd == 'scrollup': pyautogui.scroll(3)
                elif cmd == 'scrolldown': pyautogui.scroll(-3)
                elif cmd == 'lock':     os.system('rundll32.exe user32.dll,LockWorkStation')
                elif cmd == 'taskmgr':  os.system('start taskmgr')
                elif cmd == 'screenshot':
                    path = os.path.join(os.environ['USERPROFILE'], 'Desktop', f'remote_snap_{int(time.time())}.png')
                    pyautogui.screenshot(path)
                elif cmd == 'wifi':
                    from engine.automation import scan_wifi
                    res = scan_wifi()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(res.encode())
                    return
            except Exception as e:
                print(f"[REMOTE] Command error: {e}")
            self._ok()
        else:
            self._ok()

    def _ok(self):
        self.send_response(200)
        self.end_headers()

def start_server():
    try:
        # Set allow_reuse_address before binding to avoid "Address already in use" errors
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", PORT), RemoteHandler) as httpd:
            print(f"[REMOTE] Mobile server at port {PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"[REMOTE] Server error: {e}")
