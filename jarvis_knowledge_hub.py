import os
import customtkinter as ctk
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime

class KnowledgeHub:
    def __init__(self):
        self.learning_folder = 'jarvis_learned_files'
        self.db_path = 'jarvis_memory.db'
        
        # Ensure directory exists
        if not os.path.exists(self.learning_folder):
            os.makedirs(self.learning_folder)

    def get_all_topics(self):
        """Scan learned_files directory for topics."""
        topics = []
        if not os.path.exists(self.learning_folder):
            return topics
            
        files = [f for f in os.listdir(self.learning_folder) if f.endswith('.txt')]
        for f in files:
            # Extract topic from filename (e.g., 'python_20260508_014052.txt' -> 'python')
            parts = f.split('_')
            topic = parts[0].replace('.txt', '').replace('-', ' ').title()
            
            filepath = os.path.join(self.learning_folder, f)
            stats = os.stat(filepath)
            mtime = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
            size = stats.st_size
            
            topics.append({
                'name': topic,
                'filename': f,
                'path': filepath,
                'date': mtime,
                'size': f"{size} bytes"
            })
            
        # Sort by date descending
        topics.sort(key=lambda x: x['date'], reverse=True)
        return topics

    def read_topic(self, filepath):
        """Read content of a learned topic."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

def open_knowledge_hub(master, callback_log):
    """UI for browsing JARVIS's collective knowledge."""
    hub = KnowledgeHub()
    
    popup = ctk.CTkToplevel(master)
    popup.title("🧠 JARVIS KNOWLEDGE HUB")
    popup.geometry("900x700")
    popup.attributes("-topmost", True)
    popup.configure(fg_color="#02050A")
    
    # Header
    header_frame = ctk.CTkFrame(popup, fg_color="#05080F", height=100, corner_radius=0)
    header_frame.pack(fill="x", side="top")
    
    ctk.CTkLabel(header_frame, text="🧠 COLLECTIVE KNOWLEDGE BASE", 
                 font=("Courier New", 28, "bold"), text_color="#00F3FF").pack(pady=(20, 5))
    ctk.CTkLabel(header_frame, text="Browsing all learned intelligence nodes", 
                 font=("Courier New", 12), text_color="#555555").pack(pady=(0, 10))

    # Main Split View
    split_frame = ctk.CTkFrame(popup, fg_color="transparent")
    split_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Left Side: List
    list_side = ctk.CTkFrame(split_frame, width=300, fg_color="#010306", border_width=1, border_color="#002233")
    list_side.pack(side="left", fill="both", expand=False, padx=(0, 10))
    
    ctk.CTkLabel(list_side, text="LEARNED TOPICS", font=("Courier New", 14, "bold"), text_color="#00FF41").pack(pady=10)
    
    search_entry = ctk.CTkEntry(list_side, placeholder_text="Search topics...", font=("Courier New", 12),
                               fg_color="#000000", border_color="#004466")
    search_entry.pack(fill="x", padx=10, pady=5)
    
    scroll_list = ctk.CTkScrollableFrame(list_side, fg_color="transparent")
    scroll_list.pack(expand=True, fill="both", padx=5, pady=5)
    
    # Right Side: Content
    content_side = ctk.CTkFrame(split_frame, fg_color="#010306", border_width=1, border_color="#002233")
    content_side.pack(side="right", fill="both", expand=True)
    
    content_header = ctk.CTkLabel(content_side, text="SELECT A TOPIC TO READ", font=("Courier New", 16, "bold"), text_color="#00F3FF")
    content_header.pack(pady=20)
    
    content_text = ctk.CTkTextbox(content_side, font=("Courier New", 13), fg_color="#05080F", text_color="#00FF41", 
                                 border_width=1, border_color="#002233", state="disabled")
    content_text.pack(expand=True, fill="both", padx=15, pady=15)

    def display_topic(topic_data):
        content_header.configure(text=f"📂 TOPIC: {topic_data['name'].upper()}")
        callback_log("SYSTEM", f"Accessing knowledge node: {topic_data['name']}")
        
        text = hub.read_topic(topic_data['path'])
        content_text.configure(state="normal")
        content_text.delete("1.0", "end")
        content_text.insert("end", text)
        content_text.configure(state="disabled")

    def refresh_list(query=""):
        for widget in scroll_list.winfo_children():
            widget.destroy()
            
        topics = hub.get_all_topics()
        count = 0
        for t in topics:
            if query.lower() in t['name'].lower():
                btn = ctk.CTkButton(scroll_list, text=f"{t['name']}\n{t['date']}", 
                                  anchor="w", fg_color="transparent", hover_color="#002233",
                                  font=("Courier New", 12), text_color="#888888",
                                  command=lambda data=t: display_topic(data))
                btn.pack(fill="x", pady=2)
                count += 1
        
        if count == 0:
            ctk.CTkLabel(scroll_list, text="No topics found", font=("Courier New", 10), text_color="#333333").pack()

    search_entry.bind("<KeyRelease>", lambda e: refresh_list(search_entry.get()))
    
    # Footer Actions
    footer = ctk.CTkFrame(content_side, fg_color="transparent", height=50)
    footer.pack(fill="x", side="bottom", padx=10, pady=10)
    
    ctk.CTkButton(footer, text="REFRESH DATABASE", fg_color="#004466", hover_color="#006688", 
                  command=lambda: refresh_list()).pack(side="left", padx=5)
    
    ctk.CTkButton(footer, text="CLOSE HUB", fg_color="#440000", hover_color="#660000", 
                  command=popup.destroy).pack(side="right", padx=5)

    refresh_list()
    popup.focus_force()

if __name__ == "__main__":
    # Test
    def dummy_log(tag, msg): print(f"[{tag}] {msg}")
    root = ctk.CTk()
    open_knowledge_hub(root, dummy_log)
    root.mainloop()
