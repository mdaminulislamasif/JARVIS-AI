"""
JARVIS 3D Face Creator (Three.js) - Python Edition
Launches the WebGL 3D face creator using a local Python HTTP server to bypass CORS issues.
"""
import os
import sys
import threading
import webbrowser
import http.server
import socketserver
import time

PORT = 8012
HTML_FILE = "CREATE_JARVIS_FACE_THREEJS.html"

# Force stdout to UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

class ThreadedHTTPServer(threading.Thread):
    def __init__(self, port=8012):
        super().__init__()
        self.port = port
        self.daemon = True
        self.server = None

    def run(self):
        handler = http.server.SimpleHTTPRequestHandler
        socketserver.TCPServer.allow_reuse_address = True
        
        # Try to bind to port
        for p in range(self.port, self.port + 50):
            try:
                self.server = socketserver.TCPServer(("", p), handler)
                self.port = p
                print(f"[SERVER] Starting local HTTP Server on port {p}...")
                self.server.serve_forever()
                break
            except OSError:
                continue

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("[SERVER] Local HTTP Server stopped.")

def main():
    print("================================================================================")
    print("  🤖 JARVIS 3D FACE CREATOR (THREE.JS) - PYTHON GUI")
    print("  🤖 JARVIS ৩ডি ফেস ক্রিয়েটর (থ্রি.জেএস)")
    print("================================================================================")
    
    # Start local HTTP server
    server = ThreadedHTTPServer(PORT)
    server.start()
    
    # Wait for server to boot
    time.sleep(1)
    
    url = f"http://localhost:{server.port}/{HTML_FILE}"
    print(f"\n[INFO] Opening WebGL 3D Creator: {url}")
    print("[INFO] Please interact with the 3D Face in the browser window.")
    print("[INFO] Press Ctrl+C in the terminal to close the application.")
    
    webbrowser.open(url)
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Stopping JARVIS 3D Face Creator...")
        server.stop()
        print("✅ Goodbye!")

if __name__ == "__main__":
    main()
