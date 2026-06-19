import os
import time
import threading
import json
import sqlite3
import pyautogui
import customtkinter as ctk
from cryptography.fernet import Fernet

# --- Encryption Setup ---
# In a real app, this key should be stored more securely
KEY_FILE = "login_bot.key"
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
else:
    with open(KEY_FILE, "rb") as f:
        key = f.read()

cipher_suite = Fernet(key)

class LoginBot:
    def __init__(self):
        self.db_path = "jarvis_logins.db"
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                url TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add_login(self, service, username, password, url=""):
        encrypted_pw = cipher_suite.encrypt(password.encode()).decode()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logins (service, username, password, url) VALUES (?, ?, ?, ?)",
                     (service, username, encrypted_pw, url))
        conn.commit()
        conn.close()

    def get_logins(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, service, username, password, url FROM logins")
        rows = cursor.fetchall()
        conn.close()
        
        logins = []
        for r in rows:
            try:
                decrypted_pw = cipher_suite.decrypt(r[3].encode()).decode()
            except Exception as e:

                print(f"⚠️ Error: {e}")
                decrypted_pw = "********"
            logins.append({
                'id': r[0],
                'service': r[1],
                'username': r[2],
                'password': decrypted_pw,
                'url': r[4]
            })
        return logins

    def delete_login(self, login_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM logins WHERE id = ?", (login_id,))
        conn.commit()
        conn.close()

    def perform_login(self, username, password, delay=3):
        """Automate typing credentials."""
        # Countdown
        time.sleep(delay)
        
        # Type Username
        pyautogui.write(username, interval=0.1)
        pyautogui.press('tab')
        time.sleep(0.5)
        
        # Type Password
        pyautogui.write(password, interval=0.1)
        pyautogui.press('enter')

def open_login_bot_ui(master, callback_log):
    """UI for managing and executing automated logins."""
    bot = LoginBot()
    
    popup = ctk.CTkToplevel(master)
    popup.title("🔐 JARVIS LOGIN BOT")
    popup.geometry("600x550")
    popup.attributes("-topmost", True)
    popup.configure(fg_color="#02050A")
    
    # Header
    header = ctk.CTkLabel(popup, text="🔐 SECURE LOGIN BOT", font=("Courier New", 22, "bold"), text_color="#00F3FF")
    header.pack(pady=15)
    
    # Form Frame
    form_frame = ctk.CTkFrame(popup, fg_color="#05080F", border_width=1, border_color="#002233")
    form_frame.pack(fill="x", padx=20, pady=5)
    
    ctk.CTkLabel(form_frame, text="ADD NEW CREDENTIAL", font=("Courier New", 12, "bold"), text_color="#555555").pack(pady=5)
    
    inputs_row = ctk.CTkFrame(form_frame, fg_color="transparent")
    inputs_row.pack(fill="x", padx=10, pady=5)
    
    service_entry = ctk.CTkEntry(inputs_row, placeholder_text="Service (e.g. FB)", width=120)
    service_entry.pack(side="left", padx=5)
    
    user_entry = ctk.CTkEntry(inputs_row, placeholder_text="Username", width=150)
    user_entry.pack(side="left", padx=5)
    
    pass_entry = ctk.CTkEntry(inputs_row, placeholder_text="Password", show="*", width=150)
    pass_entry.pack(side="left", padx=5)
    
    def save_cred():
        s, u, p = service_entry.get(), user_entry.get(), pass_entry.get()
        if s and u and p:
            bot.add_login(s, u, p)
            service_entry.delete(0, "end")
            user_entry.delete(0, "end")
            pass_entry.delete(0, "end")
            callback_log("SYSTEM", f"Encrypted node added for: {s}")
            refresh_list()
        else:
            callback_log("ERROR", "All fields required for encryption node.")

    ctk.CTkButton(inputs_row, text="SAVE", width=60, fg_color="#004400", command=save_cred).pack(side="left", padx=5)

    # List Frame
    list_frame = ctk.CTkScrollableFrame(popup, fg_color="#010306", border_width=1, border_color="#002233")
    list_frame.pack(expand=True, fill="both", padx=20, pady=10)

    def run_bot(u, p):
        callback_log("SYSTEM", "BOT ACTIVATED. Switch to login window NOW (3s delay)...")
        threading.Thread(target=bot.perform_login, args=(u, p), daemon=True).start()

    def refresh_list():
        for widget in list_frame.winfo_children():
            widget.destroy()
            
        logins = bot.get_logins()
        for l in logins:
            row = ctk.CTkFrame(list_frame, fg_color="#05080F", border_width=1, border_color="#001122")
            row.pack(fill="x", pady=2, padx=2)
            
            ctk.CTkLabel(row, text=f"{l['service']}: {l['username']}", font=("Courier New", 12), text_color="#00FF41", width=250, anchor="w").pack(side="left", padx=10)
            
            ctk.CTkButton(row, text="LOGIN NOW", width=100, height=24, fg_color="#004466", 
                         command=lambda u=l['username'], p=l['password']: run_bot(u, p)).pack(side="right", padx=5)
            
            ctk.CTkButton(row, text="DEL", width=40, height=24, fg_color="#440000", 
                         command=lambda i=l['id']: (bot.delete_login(i), refresh_list())).pack(side="right", padx=5)

    refresh_list()
    
    ctk.CTkLabel(popup, text="WARNING: This bot types keys using virtual driver.\nEnsure correct field is focused after clicking 'LOGIN NOW'.", 
                 font=("Courier New", 9), text_color="#444444").pack(pady=10)

if __name__ == "__main__":
    def dummy_log(t, m): print(f"[{t}] {m}")
    root = ctk.CTk()
    open_login_bot_ui(root, dummy_log)
    root.mainloop()
