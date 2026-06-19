import os
import time
import threading
import subprocess
import customtkinter as ctk
from datetime import datetime
import random

class AsifHackerSuite:
    def __init__(self, callback_log):
        self.callback_log = callback_log
        # Prioritize local folder; fallback to D: drive
        local_path = os.path.join(os.getcwd(), "asif_hacker_suite")
        if os.path.exists(local_path):
            self.asif_path = local_path
        else:
            self.asif_path = r"D:\AA ASIF\New folder\New folder"
            
        self.links_file = os.path.join(self.asif_path, "LINKS.txt")
        self.is_running = False

    def generate_data(self, edition, dtype, start_val, count, length=8):
        """Unified generator for all Editions (1-4)."""
        filename = f"{edition}{dtype}.TEXT"
        full_path = os.path.join(self.asif_path, filename)
        
        try:
            with open(full_path, "w", encoding='utf-8') as f:
                f.write(f"Log by JARVIS (Edition {edition}): {datetime.now()}\n")
                f.write("-" * 40 + "\n")
                
                if dtype == "PASS":
                    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%^&*"
                    for _ in range(count):
                        f.write("".join(random.choice(chars) for _ in range(length)) + "\n")
                
                elif dtype == "PHONENUMBER":
                    prefix = start_val[:-7]
                    suffix = int(start_val[-7:])
                    for i in range(count):
                        f.write(f"{prefix}{str(suffix + i + 1).zfill(7)}\n")
                
                elif dtype == "NUMBER":
                    prefix = start_val[:-8]
                    suffix = int(start_val[-8:])
                    for i in range(count):
                        f.write(f"{prefix}{str(suffix + i + 1).zfill(8)}\n")
            
            self.callback_log("SUCCESS", f"Edition {edition} {dtype} data saved to {filename}")
        except Exception as e:
            self.callback_log("ERROR", f"Failed: {e}")

    def run_bot(self, bot_num):
        bot_file = f"login_bot - {bot_num}.py" if bot_num > 0 else "login_bot.py"
        self.callback_log("SYSTEM", f"Executing {bot_file}...")
        subprocess.Popen(['start', 'cmd', '/k', 'python', bot_file], shell=True, cwd=self.asif_path)

    def get_links(self):
        links = []
        if os.path.exists(self.links_file):
            with open(self.links_file, "r") as f:
                for line in f:
                    if ">>>" in line:
                        parts = line.split(">>>")
                        name = parts[0].replace("##", "").strip()
                        url = parts[1].strip()
                        links.append((name, url))
        return links

def open_asif_suite(master, callback_log):
    suite = AsifHackerSuite(callback_log)
    
    popup = ctk.CTkToplevel(master)
    popup.title("🔥 ASIF SUPREME HACKER SUITE")
    popup.geometry("950x750")
    popup.attributes("-topmost", True)
    popup.configure(fg_color="#02050A")
    
    tabview = ctk.CTkTabview(popup, fg_color="#05080F", segment_color="#220000", 
                            segmented_button_selected_color="#AA0000")
    tabview.pack(expand=True, fill="both", padx=10, pady=10)
    
    tab_gen = tabview.add("📊 DATA GEN")
    tab_bots = tabview.add("🚀 BOT MASTER")
    tab_links = tabview.add("🔗 LINK HUB")
    tab_records = tabview.add("📝 RECORDS")

    # --- TAB: DATA GEN ---
    ctk.CTkLabel(tab_gen, text="MULTI-EDITION GENERATOR", font=("Courier New", 20, "bold"), text_color="#00F3FF").pack(pady=10)
    
    gen_frame = ctk.CTkFrame(tab_gen, fg_color="transparent")
    gen_frame.pack(pady=10)
    
    ed_var = ctk.StringVar(value="1")
    ctk.CTkLabel(gen_frame, text="Select Edition:").grid(row=0, column=0, padx=5)
    ctk.CTkOptionMenu(gen_frame, values=["1", "2", "3", "4"], variable=ed_var, fg_color="#440000").grid(row=0, column=1, padx=5)
    
    val_entry = ctk.CTkEntry(tab_gen, placeholder_text="Start Number / Prefix", width=300)
    val_entry.pack(pady=5)
    
    cnt_entry = ctk.CTkEntry(tab_gen, placeholder_text="Count (How many?)", width=300)
    cnt_entry.pack(pady=5)
    
    btn_row = ctk.CTkFrame(tab_gen, fg_color="transparent")
    btn_row.pack(pady=10)
    
    ctk.CTkButton(btn_row, text="GEN PASSWORDS", fg_color="#660000", 
                  command=lambda: suite.generate_data(ed_var.get(), "PASS", "", int(cnt_entry.get() or 0))).pack(side="left", padx=5)
    ctk.CTkButton(btn_row, text="GEN PHONES", fg_color="#660000", 
                  command=lambda: suite.generate_data(ed_var.get(), "PHONENUMBER", val_entry.get(), int(cnt_entry.get() or 0))).pack(side="left", padx=5)
    ctk.CTkButton(btn_row, text="GEN 8-DIGIT", fg_color="#660000", 
                  command=lambda: suite.generate_data(ed_var.get(), "NUMBER", val_entry.get(), int(cnt_entry.get() or 0))).pack(side="left", padx=5)

    # --- TAB: BOT MASTER ---
    ctk.CTkLabel(tab_bots, text="SELENIUM BOT CONTROLLER", font=("Courier New", 20, "bold"), text_color="#00FF41").pack(pady=10)
    for i in range(5):
        name = f"LOGIN BOT {i}" if i > 0 else "MAIN LOGIN BOT"
        ctk.CTkButton(tab_bots, text=f"RUN {name}", fg_color="#003300", hover_color="#005500", width=400,
                      command=lambda n=i: suite.run_bot(n)).pack(pady=5)
    
    ctk.CTkButton(tab_bots, text="🔥 FULL LAUNCH (CLEAN + ALL BOTS)", fg_color="#AA0000", height=60, width=400,
                  command=lambda: subprocess.Popen(['start', 'run_all_bots.bat'], shell=True, cwd=suite.asif_path)).pack(pady=20)

    # --- TAB: LINK HUB ---
    ctk.CTkLabel(tab_links, text="EXTERNAL SIGN-IN LINKS", font=("Courier New", 20, "bold"), text_color="#FFD700").pack(pady=10)
    links = suite.get_links()
    link_scroll = ctk.CTkScrollableFrame(tab_links, fg_color="transparent")
    link_scroll.pack(expand=True, fill="both")
    
    import webbrowser
    for name, url in links:
        row = ctk.CTkFrame(link_scroll, fg_color="#111111")
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text=name, width=150, anchor="w", text_color="#00F3FF").pack(side="left", padx=10)
        ctk.CTkButton(row, text="OPEN LINK", width=100, height=24, fg_color="#004466",
                      command=lambda u=url: webbrowser.open(u)).pack(side="right", padx=10)

    # --- TAB: RECORDS ---
    ctk.CTkLabel(tab_records, text="ACCOUNT RECORD MANAGER", font=("Courier New", 20, "bold"), text_color="#FFFFFF").pack(pady=10)
    rec_text = ctk.CTkTextbox(tab_records, height=300, font=("Courier New", 13), fg_color="#000000", text_color="#00FF41")
    rec_text.pack(fill="both", expand=True, padx=20, pady=10)
    
    def load_template():
        path = os.path.join(suite.asif_path, "Account Record Template.txt")
        if os.path.exists(path):
            with open(path, "r") as f: rec_text.insert("1.0", f.read())
    
    load_template()
    
    def save_record():
        name = datetime.now().strftime("Record_%Y%m%d_%H%M%S.txt")
        path = os.path.join(suite.asif_path, name)
        with open(path, "w") as f: f.write(rec_text.get("1.0", "end"))
        suite.callback_log("SUCCESS", f"Record saved as {name}")

    ctk.CTkButton(tab_records, text="SAVE RECORD TO DIR", fg_color="#004400", command=save_record).pack(pady=10)

    # Footer
    footer = ctk.CTkFrame(popup, fg_color="transparent", height=40)
    footer.pack(fill="x", side="bottom")
    ctk.CTkLabel(footer, text=f"Work Directory: {suite.asif_path}", font=("Courier New", 10), text_color="#555555").pack()

if __name__ == "__main__":
    def dummy_log(t, m): print(f"[{t}] {m}")
    root = ctk.CTk()
    open_asif_suite(root, dummy_log)
    root.mainloop()
