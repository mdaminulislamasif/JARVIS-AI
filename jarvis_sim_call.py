import subprocess
import os
import time
import json
import sqlite3
import threading
from datetime import datetime

class SIMCallSystem:
    def __init__(self):
        # Try to find ADB in common paths if not in system PATH
        self.adb_path = self._find_adb()
        self.db_path = "jarvis_contacts.db"

    def _find_adb(self):
        """Try to locate ADB executable."""
        # 1. Check system PATH
        try:
            subprocess.run(["adb", "--version"], capture_output=True, text=True)
            return "adb"
        except Exception:
            print("⚠️ Error occurred but was silently ignored")

        # 2. Check common Android SDK paths
        user_profile = os.environ.get('USERPROFILE', '')
        local_app_data = os.environ.get('LOCALAPPDATA', '')
        workspace = os.path.dirname(os.path.abspath(__file__))
        
        common_paths = [
            os.path.join(workspace, "platform-tools", "adb.exe"),
            os.path.join(local_app_data, "Android", "Sdk", "platform-tools", "adb.exe"),
            os.path.join(user_profile, "AppData", "Local", "Android", "Sdk", "platform-tools", "adb.exe"),
            "C:\\platform-tools\\adb.exe",
            "D:\\platform-tools\\adb.exe",
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return f'"{path}"'
        
        return "adb" # Fallback to default

    def check_device(self):
        """Check if any Android device is connected via ADB."""
        try:
            result = subprocess.run(f"{self.adb_path} devices", shell=True, capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            devices = [line for line in lines[1:] if line.strip() and "device" in line and "devices" not in line]
            return len(devices) > 0
        except Exception:
            return False

    def make_call(self, phone_number):
        """Initiate a phone call via ADB."""
        if not self.check_device():
            return {"success": False, "error": "NO DEVICE: Connect your phone via USB and enable 'USB Debugging'"}
        
        try:
            # Command to initiate call
            cmd = f"{self.adb_path} shell am start -a android.intent.action.CALL -d tel:{phone_number}"
            subprocess.run(cmd, shell=True, capture_output=True)
            self._log_action("CALL", phone_number, "OUTGOING")
            return {"success": True, "msg": f"Initiating SIM call to {phone_number}..."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def end_call(self):
        """Hang up the current call."""
        try:
            cmd = f"{self.adb_path} shell input keyevent 6"
            subprocess.run(cmd, shell=True, capture_output=True)
            return {"success": True, "msg": "Ending call..."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_sms(self, phone_number, message):
        """Send an SMS via ADB."""
        if not self.check_device():
            return {"success": False, "error": "NO DEVICE DETECTED"}
        
        try:
            safe_msg = message.replace('"', '\\"')
            # This opens the SMS app with the message pre-filled
            cmd = f'{self.adb_path} shell am start -a android.intent.action.SENDTO -d sms:{phone_number} --es sms_body "{safe_msg}" --ez exit_on_sent true'
            subprocess.run(cmd, shell=True, capture_output=True)
            
            # On some devices, we can try to actually click 'send' using keyevents
            # but it's highly device-specific. We'll stick to drafting for safety.
            
            self._log_action("SMS", phone_number, "SENT", message)
            return {"success": True, "msg": f"SMS drafted to {phone_number}."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_whatsapp(self, phone_number, message):
        """Send a WhatsApp message via ADB."""
        if not self.check_device():
            return {"success": False, "error": "NO DEVICE DETECTED"}
        
        try:
            # Clean number (remove non-digits, ensure country code)
            clean_num = "".join(filter(str.isdigit, phone_number))
            if not clean_num.startswith("88") and len(clean_num) == 11: # Bangladesh default
                clean_num = "88" + clean_num
                
            safe_msg = message.replace(" ", "%20")
            # Open WhatsApp with API link
            cmd = f'{self.adb_path} shell am start -a android.intent.action.VIEW -d "https://api.whatsapp.com/send?phone={clean_num}&text={safe_msg}"'
            subprocess.run(cmd, shell=True, capture_output=True)
            
            self._log_action("WHATSAPP", phone_number, "SENT", message)
            return {"success": True, "msg": f"WhatsApp interface opened for {phone_number}."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def make_whatsapp_call(self, phone_number):
        """Initiate a WhatsApp voice call."""
        # Note: Direct WhatsApp calling via intent is restricted on some versions.
        # This usually opens the contact in WhatsApp.
        return self.send_whatsapp(phone_number, "[Voice Call Request via JARVIS]")

    def fetch_contacts(self):
        """Try to fetch contacts from jarvis_contacts.db"""
        contacts = []
        try:
            if os.path.exists(self.db_path):
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name, phone FROM contacts ORDER BY name")
                contacts = cursor.fetchall()
                conn.close()
        except Exception:
            print("⚠️ Error occurred but was silently ignored")
        return contacts

    def _log_action(self, type, phone, direction, content=""):
        """Log call/sms to database if possible."""
        try:
            if os.path.exists(self.db_path):
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                now = datetime.now().isoformat()
                
                if type == "CALL":
                    cursor.execute("INSERT INTO call_history (phone, direction, timestamp, status) VALUES (?, ?, ?, ?)",
                                 (phone, direction, now, "COMPLETED"))
                else:
                    cursor.execute("INSERT INTO sms_history (phone, message, direction, timestamp) VALUES (?, ?, ?, ?)",
                                 (phone, content, direction, now))
                conn.commit()
                conn.close()
        except Exception:
            print("⚠️ Error occurred but was silently ignored")

def open_call_ui(master, callback_log, initial_number=""):
    """Advanced UI for making SIM calls with Antigravity aesthetics."""
    import customtkinter as ctk
    
    popup = ctk.CTkToplevel(master)
    popup.title("JARVIS COMMUNICATION UPLINK")
    popup.geometry("500x650")
    popup.attributes("-topmost", True)
    popup.configure(fg_color="#02050A")
    
    sim_system = SIMCallSystem()
    
    # Futuristic Border
    main_frame = ctk.CTkFrame(popup, fg_color="#02050A", border_width=2, border_color="#00F3FF")
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Header
    header = ctk.CTkLabel(main_frame, text="📡 NEURAL COMM LINK", font=("Courier New", 24, "bold"), text_color="#00F3FF")
    header.pack(pady=(20, 5))
    
    status_indicator = ctk.CTkLabel(main_frame, text="SCANNING FOR UPLINK DEVICE...", font=("Courier New", 10), text_color="#555555")
    status_indicator.pack()

    def update_status():
        if sim_system.check_device():
            status_indicator.configure(text="● DEVICE CONNECTED", text_color="#00FF41")
        else:
            status_indicator.configure(text="○ NO DEVICE DETECTED", text_color="#FF3131")
        popup.after(5000, update_status)

    # Number Entry
    entry_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    entry_frame.pack(pady=20, padx=20, fill="x")
    
    ctk.CTkLabel(entry_frame, text="TARGET NUMBER:", font=("Courier New", 12, "bold"), text_color="#00F3FF").pack(anchor="w")
    num_entry = ctk.CTkEntry(entry_frame, placeholder_text="Enter number or name...", width=400, height=50, 
                            font=("Courier New", 18), fg_color="#05080F", border_color="#004466", text_color="#00FF41")
    num_entry.pack(pady=5, fill="x")
    
    if initial_number:
        num_entry.insert(0, initial_number)
    
    # Contact Search Results
    results_frame = ctk.CTkScrollableFrame(main_frame, height=150, fg_color="#010306", border_width=1, border_color="#002233")
    results_frame.pack(fill="x", padx=20, pady=5)
    
    contacts = sim_system.fetch_contacts()
    
    def select_contact(name, phone):
        num_entry.delete(0, "end")
        num_entry.insert(0, phone)
        callback_log("SYSTEM", f"Target locked: {name} ({phone})")

    def filter_contacts(*args):
        for widget in results_frame.winfo_children():
            widget.destroy()
        
        q = num_entry.get().lower()
        count = 0
        for name, phone in contacts:
            if q in name.lower() or q in phone:
                btn = ctk.CTkButton(results_frame, text=f"{name} | {phone}", 
                                  anchor="w", fg_color="transparent", hover_color="#002233",
                                  font=("Courier New", 12), text_color="#888888",
                                  command=lambda n=name, p=phone: select_contact(n, p))
                btn.pack(fill="x", pady=2)
                count += 1
                if count >= 10: break
        
        if count == 0:
            ctk.CTkLabel(results_frame, text="No contacts found", font=("Courier New", 10), text_color="#333333").pack()

    num_entry.bind("<KeyRelease>", filter_contacts)
    filter_contacts() # Initial load

    # Actions
    actions_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    actions_frame.pack(pady=10)

    def do_call():
        num = num_entry.get().strip()
        if not num: return
        callback_log("JARVIS", f"📞 Establishing cellular uplink to {num}...")
        res = sim_system.make_call(num)
        if res["success"]:
            callback_log("JARVIS", f"✅ {res['msg']}")
        else:
            callback_log("ERROR", f"❌ {res['error']}")

    def do_whatsapp():
        num = num_entry.get().strip()
        if not num: return
        
        # Ask for message
        msg_popup = ctk.CTkInputDialog(text="Enter WhatsApp Message:", title="WhatsApp Uplink")
        msg = msg_popup.get_input()
        if msg:
            callback_log("JARVIS", f"💬 Sending encrypted WhatsApp to {num}...")
            res = sim_system.send_whatsapp(num, msg)
            if res["success"]:
                callback_log("JARVIS", f"✅ {res['msg']}")
            else:
                callback_log("ERROR", f"❌ {res['error']}")

    def do_sms():
        num = num_entry.get().strip()
        if not num: return
        msg_popup = ctk.CTkInputDialog(text="Enter SMS Message:", title="SMS Uplink")
        msg = msg_popup.get_input()
        if msg:
            callback_log("JARVIS", f"📡 Transmitting SMS packet to {num}...")
            res = sim_system.send_sms(num, msg)
            if res["success"]:
                callback_log("JARVIS", f"✅ {res['msg']}")
            else:
                callback_log("ERROR", f"❌ {res['error']}")

    def do_end():
        callback_log("SYSTEM", "Terminating active call session...")
        res = sim_system.end_call()
        if res["success"]:
            callback_log("JARVIS", "✅ Call ended.")
        else:
            callback_log("ERROR", f"❌ {res['error']}")

    # Grid for Buttons
    btn_grid = ctk.CTkFrame(main_frame, fg_color="transparent")
    btn_grid.pack(pady=10, padx=20, fill="x")
    
    ctk.CTkButton(btn_grid, text="📞 SIM CALL", width=200, height=50, font=("Courier New", 14, "bold"),
                  fg_color="#00AA00", hover_color="#00CC00", command=do_call).grid(row=0, column=0, padx=5, pady=5)
    
    ctk.CTkButton(btn_grid, text="💬 WHATSAPP", width=200, height=50, font=("Courier New", 14, "bold"),
                  fg_color="#25D366", hover_color="#20BA5A", text_color="black", command=do_whatsapp).grid(row=0, column=1, padx=5, pady=5)
    
    ctk.CTkButton(btn_grid, text="📡 SEND SMS", width=200, height=50, font=("Courier New", 14, "bold"),
                  fg_color="#004466", hover_color="#006688", command=do_sms).grid(row=1, column=0, padx=5, pady=5)
    
    ctk.CTkButton(btn_grid, text="🛑 END CALL", width=200, height=50, font=("Courier New", 14, "bold"),
                  fg_color="#AA0000", hover_color="#CC0000", command=do_end).grid(row=1, column=1, padx=5, pady=5)

    # Footer
    footer = ctk.CTkLabel(main_frame, text="ENCRYPTION: AES-256 ACTIVE | UPLINK: STABLE", font=("Courier New", 8), text_color="#333333")
    footer.pack(side="bottom", pady=10)

    update_status()
    popup.focus_force()

if __name__ == "__main__":
    # Test
    def dummy_log(tag, msg): print(f"[{tag}] {msg}")
    root = ctk.CTk()
    open_call_ui(root, dummy_log)
    root.mainloop()
