#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS FOLDER UPLOAD SYSTEM
============================
পুরো folder upload করুন — JARVIS সব ফাইল পড়বে, শিখবে এবং AI দিয়ে analyze করবে
"""

import os
import sys
import threading
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
import mimetypes

_BASE = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(_BASE, "jarvis_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# File types JARVIS can read
READABLE_EXTENSIONS = {
    # Text/Code
    ".txt", ".py", ".js", ".html", ".css", ".json", ".xml", ".csv",
    ".md", ".yaml", ".yml", ".ini", ".cfg", ".bat", ".sh",
    ".java", ".c", ".cpp", ".h", ".cs", ".php", ".rb", ".go",
    ".ts", ".jsx", ".tsx", ".vue", ".sql", ".r", ".m",
    # Documents
    ".pdf", ".docx", ".xlsx", ".pptx",
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mkv", ".mov", ".wmv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}


class FolderUploader(ctk.CTkToplevel):
    def __init__(self, master=None, brain=None, on_complete=None):
        super().__init__(master)
        self.brain = brain
        self.on_complete = on_complete
        self.uploaded_files = []
        self.is_uploading = False

        self.title("JARVIS FOLDER UPLOAD")
        self.geometry("800x600")
        self.configure(fg_color="#02050A")
        ctk.set_appearance_mode("dark")
        self.attributes("-topmost", True)

        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="#05080F",
                              border_width=1, border_color="#003344")
        header.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(header, text="📁 JARVIS FOLDER UPLOAD",
                     font=("Courier New", 20, "bold"),
                     text_color="#00F3FF").pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(header,
                     text="Folder এর সব ফাইল JARVIS এ upload করুন",
                     font=("Courier New", 11),
                     text_color="#555555").pack(side="left", padx=10)

        # Buttons row
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(btn_frame,
                      text="📁 SELECT FOLDER",
                      fg_color="#003355",
                      hover_color="#005577",
                      font=("Courier New", 13, "bold"),
                      height=45, width=200,
                      command=self._select_folder).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame,
                      text="📄 SELECT FILES",
                      fg_color="#003333",
                      hover_color="#005555",
                      font=("Courier New", 13, "bold"),
                      height=45, width=200,
                      command=self._select_files).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame,
                      text="🤖 AI ANALYZE ALL",
                      fg_color="#440066",
                      hover_color="#660088",
                      font=("Courier New", 13, "bold"),
                      height=45, width=200,
                      command=self._ai_analyze_all).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame,
                      text="🗑 CLEAR",
                      fg_color="#440000",
                      hover_color="#660000",
                      font=("Courier New", 13, "bold"),
                      height=45, width=100,
                      command=self._clear).pack(side="left", padx=5)

        # Stats bar
        self.stats_label = ctk.CTkLabel(self,
                                        text="0 files selected | 0 MB",
                                        font=("Courier New", 11),
                                        text_color="#555555")
        self.stats_label.pack(anchor="w", padx=20, pady=2)

        # Progress bar
        self.progress = ctk.CTkProgressBar(self, height=8,
                                           fg_color="#001122",
                                           progress_color="#00F3FF")
        self.progress.pack(fill="x", padx=15, pady=2)
        self.progress.set(0)

        # File list
        list_frame = ctk.CTkFrame(self, fg_color="#030810",
                                  border_width=1, border_color="#002233")
        list_frame.pack(fill="both", expand=True, padx=15, pady=5)

        ctk.CTkLabel(list_frame, text="[ UPLOADED FILES ]",
                     font=("Courier New", 10, "bold"),
                     text_color="#00FF41").pack(anchor="w", padx=10, pady=3)

        self.file_list = ctk.CTkTextbox(list_frame,
                                        font=("Consolas", 11),
                                        fg_color="#030810",
                                        text_color="#00FF41",
                                        border_width=0)
        self.file_list.pack(fill="both", expand=True, padx=5, pady=5)

        # AI Output
        ai_frame = ctk.CTkFrame(self, fg_color="#030610",
                                border_width=1, border_color="#002233")
        ai_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(ai_frame, text="[ AI ANALYSIS ]",
                     font=("Courier New", 10, "bold"),
                     text_color="#00F3FF").pack(anchor="w", padx=10, pady=3)

        self.ai_output = ctk.CTkTextbox(ai_frame, height=120,
                                        font=("Consolas", 11),
                                        fg_color="#030610",
                                        text_color="#00F3FF",
                                        border_width=0)
        self.ai_output.pack(fill="x", padx=5, pady=(0, 5))

        # Question input
        q_frame = ctk.CTkFrame(self, fg_color="transparent")
        q_frame.pack(fill="x", padx=15, pady=(0, 15))

        self.question_entry = ctk.CTkEntry(q_frame,
                                           placeholder_text="Uploaded files সম্পর্কে প্রশ্ন করুন...",
                                           height=38,
                                           fg_color="#000000",
                                           border_color="#003344",
                                           font=("Consolas", 12))
        self.question_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.question_entry.bind("<Return>", lambda e: self._ask_about_files())

        ctk.CTkButton(q_frame, text="ASK AI",
                      width=80, height=38,
                      fg_color="#004466",
                      command=self._ask_about_files).pack(side="left")

    def _select_folder(self):
        folder = filedialog.askdirectory(title="Select Folder to Upload")
        if not folder:
            return
        self._log(f"📁 Scanning folder: {folder}\n")
        threading.Thread(target=self._scan_and_upload_folder,
                         args=(folder,), daemon=True).start()

    def _select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=[("All files", "*.*")]
        )
        if files:
            threading.Thread(target=self._upload_files,
                             args=(list(files),), daemon=True).start()

    def _scan_and_upload_folder(self, folder_path):
        all_files = []
        for root, dirs, files in os.walk(folder_path):
            # Skip hidden and cache folders
            dirs[:] = [d for d in dirs
                       if not d.startswith('.') and d not in
                       ('__pycache__', 'node_modules', '.git', 'venv', 'env')]
            for f in files:
                if not f.startswith('.'):
                    all_files.append(os.path.join(root, f))

        self.after(0, lambda n=len(all_files):
                   self._log(f"Found {n} files. Uploading...\n"))
        self._upload_files(all_files)

    def _upload_files(self, file_paths):
        self.is_uploading = True
        total = len(file_paths)
        total_size = 0

        for i, src_path in enumerate(file_paths):
            try:
                if not os.path.exists(src_path):
                    continue

                size = os.path.getsize(src_path)
                total_size += size
                name = os.path.basename(src_path)
                ext = Path(src_path).suffix.lower()

                # Copy to uploads dir
                import shutil
                dest = os.path.join(UPLOAD_DIR, name)
                # Avoid name collision
                if os.path.exists(dest):
                    base = Path(name).stem
                    suffix = Path(name).suffix
                    dest = os.path.join(UPLOAD_DIR, f"{base}_{i}{suffix}")

                shutil.copy2(src_path, dest)
                self.uploaded_files.append({
                    "path": dest,
                    "original": src_path,
                    "name": name,
                    "size": size,
                    "ext": ext,
                })

                # Update UI
                progress = (i + 1) / max(total, 1)
                icon = self._get_icon(ext)
                size_str = self._fmt_size(size)
                self.after(0, lambda p=progress: self.progress.set(p))
                self.after(0, lambda n=name, s=size_str, ic=icon:
                           self._log(f"{ic} {n}  ({s})\n"))

            except Exception as e:
                self.after(0, lambda n=src_path, err=str(e):
                           self._log(f"❌ Error: {n} — {err}\n"))

        self.is_uploading = False
        summary = (f"\n✅ Upload complete!\n"
                   f"   Files: {len(self.uploaded_files)}\n"
                   f"   Total size: {self._fmt_size(total_size)}\n"
                   f"   Saved to: {UPLOAD_DIR}\n")
        self.after(0, lambda: self._log(summary))
        self.after(0, lambda: self.stats_label.configure(
            text=f"{len(self.uploaded_files)} files | {self._fmt_size(total_size)}"))
        self.after(0, lambda: self.progress.set(1))

        if self.on_complete:
            self.after(0, lambda: self.on_complete(self.uploaded_files))

    def _ai_analyze_all(self):
        if not self.uploaded_files:
            self._ai_log("❌ কোনো file upload হয়নি এখনো।\n")
            return
        if not self.brain:
            self._ai_log("❌ Brain offline। API key add করুন।\n")
            return

        def _run():
            # Build summary of files
            readable = []
            for f in self.uploaded_files:
                if f["ext"] in READABLE_EXTENSIONS:
                    try:
                        with open(f["path"], "r", encoding="utf-8", errors="ignore") as fh:
                            content = fh.read(3000)
                        readable.append(f"=== {f['name']} ===\n{content}\n")
                    except Exception:
                        pass

            if not readable:
                self.after(0, lambda: self._ai_log(
                    "📊 Files uploaded but content not readable by AI (binary files).\n"
                    f"Total files: {len(self.uploaded_files)}\n"))
                return

            combined = "\n".join(readable[:5])  # First 5 readable files
            prompt = (f"Analyze these {len(readable)} uploaded files and give a summary in Bengali/Banglish:\n\n"
                      f"{combined[:6000]}\n\n"
                      f"Tell: 1) কী কী ফাইল আছে, 2) কোড হলে কী করে, 3) কোনো সমস্যা আছে কিনা")

            self.after(0, lambda: self._ai_log("🤖 AI analyzing files...\n"))
            try:
                response = self.brain.think(prompt)
                self.after(0, lambda r=response: self._ai_log(f"\n{r}\n"))
            except Exception as e:
                self.after(0, lambda err=str(e): self._ai_log(f"❌ AI Error: {err}\n"))

        threading.Thread(target=_run, daemon=True).start()

    def _ask_about_files(self):
        question = self.question_entry.get().strip()
        if not question:
            return
        self.question_entry.delete(0, "end")
        if not self.uploaded_files:
            self._ai_log("❌ কোনো file নেই।\n")
            return

        def _run():
            # Get file names and some content
            file_info = []
            for f in self.uploaded_files[:10]:
                content = ""
                if f["ext"] in READABLE_EXTENSIONS:
                    try:
                        with open(f["path"], "r", encoding="utf-8", errors="ignore") as fh:
                            content = fh.read(1000)
                    except Exception:
                        pass
                file_info.append(f"File: {f['name']}\n{content[:500]}")

            context = "\n\n".join(file_info[:5])
            prompt = (f"Uploaded files:\n{context}\n\n"
                      f"Question: {question}\n\n"
                      f"Answer in Bengali/Banglish:")

            self.after(0, lambda: self._ai_log(f"\n❓ {question}\n"))
            try:
                response = self.brain.think(prompt)
                self.after(0, lambda r=response: self._ai_log(f"🤖 {r}\n\n"))
            except Exception as e:
                self.after(0, lambda err=str(e): self._ai_log(f"❌ {err}\n"))

        threading.Thread(target=_run, daemon=True).start()

    def _clear(self):
        self.uploaded_files = []
        self.file_list.delete("1.0", "end")
        self.ai_output.delete("1.0", "end")
        self.progress.set(0)
        self.stats_label.configure(text="0 files selected | 0 MB")

    def _log(self, msg):
        self.file_list.insert("end", msg)
        self.file_list.see("end")

    def _ai_log(self, msg):
        self.ai_output.insert("end", msg)
        self.ai_output.see("end")

    def _get_icon(self, ext):
        if ext in IMAGE_EXTENSIONS: return "🖼"
        if ext in VIDEO_EXTENSIONS: return "🎬"
        if ext in AUDIO_EXTENSIONS: return "🎵"
        if ext in {".py", ".js", ".html", ".css", ".java", ".c", ".cpp"}: return "💻"
        if ext in {".pdf", ".docx", ".xlsx"}: return "📄"
        if ext in {".zip", ".rar", ".7z"}: return "📦"
        if ext in {".txt", ".md"}: return "📝"
        return "📁"

    def _fmt_size(self, size_bytes):
        if size_bytes < 1024: return f"{size_bytes} B"
        if size_bytes < 1024**2: return f"{size_bytes/1024:.1f} KB"
        if size_bytes < 1024**3: return f"{size_bytes/1024**2:.1f} MB"
        return f"{size_bytes/1024**3:.1f} GB"


def open_folder_upload(master=None, brain=None, on_complete=None):
    """Open Folder Upload window"""
    win = FolderUploader(master, brain, on_complete)
    win.lift()
    win.focus_force()
    return win


if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    win = FolderUploader(root)
    root.mainloop()
