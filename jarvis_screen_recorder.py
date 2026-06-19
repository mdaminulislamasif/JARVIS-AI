"""
JARVIS SCREEN RECORDER
======================
Automatically records desktop screen video and saves locally.
"""

import os
import sys
import time
import threading
import cv2
import numpy as np
import pyautogui
import PIL.ImageGrab as ImageGrab

# Force UTF-8 stdout encoding on Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

class ScreenRecorder:
    """Class to manage screen recording in the background"""
    
    def __init__(self):
        self.is_recording = False
        self.record_thread = None
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis_uploads")
        os.makedirs(self.output_dir, exist_ok=True)
        self.current_file = None
        self.fps = 10.0
        
    def start_recording(self, fps=10.0):
        """Start recording screen video"""
        if self.is_recording:
            return f"Already recording: {self.current_file}"
            
        self.is_recording = True
        self.fps = fps
        filename = f"record_{int(time.time())}.mp4"
        self.current_file = os.path.join(self.output_dir, filename)
        
        # Start recording in background thread
        self.record_thread = threading.Thread(
            target=self._record_loop,
            args=(self.current_file, self.fps),
            daemon=True
        )
        self.record_thread.start()
        
        print(f"[SCREEN RECORDER] Started recording to {filename}")
        return f"Recording started! Saving to: {filename}"
        
    def _record_loop(self, output_path, fps):
        """Internal recording loop running in thread"""
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # Grab first frame to determine native resolution
        try:
            first_img = ImageGrab.grab()
            first_frame = np.array(first_img)
            height, width = first_frame.shape[:2]
        except Exception as grab_err:
            print(f"[SCREEN RECORDER] First frame capture failed, defaulting to pyautogui size: {grab_err}")
            width, height = pyautogui.size()
            
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        delay = 1.0 / fps
        
        try:
            while self.is_recording:
                start_time = time.time()
                
                # Grab screen frame
                img = ImageGrab.grab()
                frame = np.array(img)
                
                # Verify frame shape matches the initialized size
                h, w = frame.shape[:2]
                if w != width or h != height:
                    frame = cv2.resize(frame, (width, height))
                
                # Convert RGB (PIL) to BGR (OpenCV)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Draw cursor overlay
                try:
                    px, py = pyautogui.position()
                    screen_w, screen_h = pyautogui.size()
                    rx = width / screen_w
                    ry = height / screen_h
                    cx, cy = int(px * rx), int(py * ry)
                    # Draw a nice cursor overlay: red dot center, cyan outer circle
                    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1) # Red dot center
                    cv2.circle(frame, (cx, cy), 12, (255, 243, 0), 2) # Neon cyan outer ring
                except Exception:
                    pass
                
                # Write frame to video
                out.write(frame)
                
                # Control frame rate
                elapsed = time.time() - start_time
                if elapsed < delay:
                    time.sleep(delay - elapsed)
        except Exception as e:
            print(f"[SCREEN RECORDER] Error during capture: {e}")
        finally:
            out.release()
            print(f"[SCREEN RECORDER] Released video writer for {output_path}")
            
    def stop_recording(self):
        """Stop current recording session"""
        if not self.is_recording:
            return "No recording is currently active."
            
        self.is_recording = False
        if self.record_thread:
            self.record_thread.join(timeout=3)
            
        filename = os.path.basename(self.current_file) if self.current_file else "unknown.mp4"
        print(f"[SCREEN RECORDER] Saved video recording to {filename}")
        return f"Recording stopped! Saved to: {filename}"

# Global instance
screen_recorder = ScreenRecorder()
