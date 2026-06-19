import customtkinter as ctk
import threading
import time
import psutil
import math
import random

class JarvisHUD(ctk.CTk):
    def __init__(self, brain_module, automation_module):
        super().__init__()
        self.brain = brain_module
        self.automation = automation_module
        
        # Window Setup
        self.title("JARVIS ADVANCED HUD")
        self.geometry("1000x700")
        ctk.set_appearance_mode("dark")
        
        # UI Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar for Controls
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#0a0a0a")
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="JARVIS", font=ctk.CTkFont(size=24, weight="bold", family="Orbitron"), text_color="#ff0000")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.load_dynamic_buttons()

        # Main HUD Area
        self.hud_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#121212")
        self.hud_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # --- 3D CODE SYSTEM FACE (NEURAL MATRIX) ---
        self.face_canvas = ctk.CTkCanvas(self.hud_frame, width=400, height=400, bg="#121212", highlightthickness=0)
        self.face_canvas.pack(pady=10)
        
        self.is_speaking = False
        self.matrix_lines = []
        for _ in range(12):
            line = self.face_canvas.create_line(200, 200, 200, 200, fill="#ff0000", width=2)
            self.matrix_lines.append(line)
        
        self.status_label = ctk.CTkLabel(self.hud_frame, text="NEURAL LINK: STABLE", font=ctk.CTkFont(size=18), text_color="#00ff00")
        self.status_label.pack(pady=10)
        
        self.stats_box = ctk.CTkTextbox(self.hud_frame, width=600, height=150, fg_color="#000000", text_color="#00ff00", font=("Consolas", 12))
        self.stats_box.pack(padx=20, pady=10)
        
        # Start Threads
        threading.Thread(target=self.update_telemetry, daemon=True).start()
        threading.Thread(target=self.animate_3d_face, daemon=True).start()

    def animate_3d_face(self):
        """Animates a 3D-like Neural Matrix face that reacts to speech"""
        angle = 0
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            angle += 0.05
            for i, line in enumerate(self.matrix_lines):
                # Calculate 3D rotation simulation
                # speaking increases speed and spread
                mod = 2.5 if self.is_speaking else 1.0
                
                offset = (i * (360/len(self.matrix_lines))) * (math.pi / 180)
                length = (80 + math.sin(angle * mod + i) * 30) * mod
                
                x1 = 200 + math.cos(angle + offset) * (length * 0.5)
                y1 = 200 + math.sin(angle + offset) * (length * 0.5)
                x2 = 200 + math.cos(angle + offset) * length
                y2 = 200 + math.sin(angle + offset) * length
                
                color = random.choice(["#ff0000", "#ff5555", "#aa0000"]) if self.is_speaking else "#550000"
                self.face_canvas.coords(line, x1, y1, x2, y2)
                self.face_canvas.itemconfig(line, fill=color)
            
            time.sleep(0.03)

    def execute_ui_command(self, command_str):
        # Direct Offline Commands (Work without API Key)
        if "clean" in command_str.lower():
            self.automation.clean_temp_files()
        elif "lock" in command_str.lower():
            self.automation.lock_pc()
        elif "apps" in command_str.lower():
            self.brain.speak("Opening app launcher...")
            self.automation.manual_hotkey("win")
        else:
            self.brain.speak(f"Executing {command_str}")

    def load_dynamic_buttons(self):
        try:
            conn = self.brain.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT label, action_command FROM ui_config WHERE is_active=1")
            rows = cursor.fetchall()
            if not rows:
                default_btns = [("CLEAN SYSTEM", self.automation.clean_temp_files), ("LOCK PC", self.automation.lock_pc)]
                for i, (label, cmd) in enumerate(default_btns):
                    btn = ctk.CTkButton(self.sidebar, text=label, command=cmd, fg_color="#2b2b2b", hover_color="#ff0000")
                    btn.grid(row=i+1, column=0, padx=20, pady=10)
            conn.close()
        except Exception as e:
            print(f"⚠️ Error: {e}")

    def update_telemetry(self):
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            text = f">>> SYSTEM STATUS <<<\n[CPU]: {cpu}%\n[RAM]: {ram}%\n[CORE]: ONLINE\n[VOICE]: {'SPEAKING' if self.is_speaking else 'IDLE'}"
            self.stats_box.delete("1.0", "end")
            self.stats_box.insert("1.0", text)
            time.sleep(1)

    def run_hud(self):
        self.mainloop()
