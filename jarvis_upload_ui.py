#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS FILE UPLOAD UI COMPONENT
জার্ভিস ফাইল আপলোড UI কম্পোনেন্ট

UI code to add file upload button to JARVIS chat
"""

import customtkinter as ctk
from tkinter import filedialog
from jarvis_file_handler import handle_file_upload
from PIL import Image, ImageTk

def add_file_upload_button(parent_frame, entry_widget, log_function):
    """
    Add file upload button to chat interface
    
    Args:
        parent_frame: The frame containing the chat input
        entry_widget: The chat input entry widget
        log_function: Function to log messages (e.g., self.log)
    
    Returns:
        The upload button widget
    """
    
    def upload_file():
        """Handle file upload button click"""
        file_path = filedialog.askopenfilename(
            title="Select file to upload",
            filetypes=[
                ("All Files", "*.*"),
                ("Images", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("Documents", "*.pdf *.doc *.docx *.txt *.md"),
                ("Code", "*.py *.js *.html *.css *.json *.xml"),
                ("Data", "*.csv *.xlsx *.json"),
            ]
        )
        
        if file_path:
            log_function("SYSTEM", f"Uploading file: {file_path}")
            
            # Handle upload
            result = handle_file_upload(file_path)
            
            if result['success']:
                log_function("SYSTEM", 
                    f"✅ File uploaded: {result['filename']} "
                    f"({result['file_type']}, {result['file_size']} bytes)")
                
                # If it's an image, show preview
                if result['file_type'] == 'image':
                    log_function("SYSTEM", f"📷 Image preview: {result['filepath']}")
                
                # If text was extracted, show it
                if result['extracted_text'] and len(result['extracted_text']) > 0:
                    preview = result['extracted_text'][:200]
                    if len(result['extracted_text']) > 200:
                        preview += "..."
                    log_function("SYSTEM", f"📄 Content preview: {preview}")
                
                # Auto-fill entry with file analysis prompt
                entry_widget.delete(0, "end")
                entry_widget.insert(0, f"Analyze this file: {result['filename']}")
                
            else:
                log_function("ERROR", f"❌ Upload failed: {result['error']}")
    
    # Create upload button
    upload_btn = ctk.CTkButton(
        parent_frame,
        text="📁 UPLOAD",
        width=100,
        height=55,
        fg_color="#004466",
        hover_color="#006688",
        font=("Courier New", 14, "bold"),
        command=upload_file
    )
    
    return upload_btn


# Example integration code for jarvis_panel.py:
"""
# In jarvis_panel.py, around line 507-520, modify the cmd_zone section:

# Import at top of file:
from jarvis_upload_ui import add_file_upload_button

# In the __init__ method, replace the cmd_zone section with:

self.cmd_zone = ctk.CTkFrame(self.right_panel, fg_color="transparent")
self.cmd_zone.pack(fill="x", side="bottom", padx=30, pady=20)

# Add upload button FIRST
self.upload_btn = add_file_upload_button(self.cmd_zone, self.entry, self.log)
self.upload_btn.pack(side="left", padx=(0, 10))

# Then add entry
self.entry = ctk.CTkEntry(
    self.cmd_zone, 
    placeholder_text="Awaiting root command...", 
    height=55, 
    fg_color="#05080F", 
    border_color=self.neon, 
    text_color=self.neon, 
    font=("Courier New", 16)
)
self.entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
self.entry.bind("<Return>", lambda e: self.fire_cmd())

# Voice button stays the same
self.voice_btn = ctk.CTkButton(...)
"""
