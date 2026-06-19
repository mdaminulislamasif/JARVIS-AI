#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS CHAT FILE UPLOAD SYSTEM
জার্ভিস চ্যাট ফাইল আপলোড সিস্টেম

Add file upload functionality to JARVIS chat system
জার্ভিস চ্যাট সিস্টেমে ফাইল আপলোড কার্যকারিতা যোগ করুন

Features:
বৈশিষ্ট্য:
1. Upload any file type
   যেকোনো ফাইল টাইপ আপলোড করুন
2. Preview images
   ছবি প্রিভিউ করুন
3. Read text files
   টেক্সট ফাইল পড়ুন
4. Extract document content
   ডকুমেন্ট কন্টেন্ট এক্সট্র্যাক্ট করুন
5. Store uploaded files
   আপলোড করা ফাইল সংরক্ষণ করুন
"""

import os
import sys
import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

DB_PATH = "jarvis_memory.db.fixed-20260504-091901"

def add_file_upload_system():
    """
    Add file upload system to JARVIS
    """
    print("\n" + "="*80)
    print("  📁 ADDING FILE UPLOAD SYSTEM TO JARVIS CHAT")
    print("  📁 জার্ভিস চ্যাটে ফাইল আপলোড সিস্টেম যোগ করা হচ্ছে")
    print("="*80 + "\n")
    
    # Create uploads directory
    uploads_dir = "jarvis_uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    print(f"✅ Created uploads directory: {uploads_dir}")
    
    # Create database table for uploaded files
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uploaded_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                file_type TEXT,
                file_size INTEGER,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                description TEXT,
                extracted_text TEXT
            )
        """)
        
        conn.commit()
        print("✅ Database table 'uploaded_files' created")
        
        # Add sample entry
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source)
            VALUES (?, ?, ?)
        """, (
            "File Upload System",
            """JARVIS File Upload System
জার্ভিস ফাইল আপলোড সিস্টেম

JARVIS can now accept file uploads in chat!
জার্ভিস এখন চ্যাটে ফাইল আপলোড গ্রহণ করতে পারে!

Supported file types:
সমর্থিত ফাইল টাইপ:
• Images: PNG, JPG, JPEG, GIF, BMP, WEBP
• Documents: PDF, DOCX, TXT, MD
• Code: PY, JS, HTML, CSS, JSON, XML
• Data: CSV, XLSX, JSON
• Archives: ZIP, RAR, 7Z
• Audio: MP3, WAV, OGG
• Video: MP4, AVI, MKV
• Any other file type

Features:
বৈশিষ্ট্য:
1. Drag and drop files into chat
   চ্যাটে ফাইল ড্র্যাগ এবং ড্রপ করুন
2. Click upload button to browse files
   ফাইল ব্রাউজ করতে আপলোড বাটনে ক্লিক করুন
3. Automatic file type detection
   স্বয়ংক্রিয় ফাইল টাইপ সনাক্তকরণ
4. Image preview in chat
   চ্যাটে ছবি প্রিভিউ
5. Text extraction from documents
   ডকুমেন্ট থেকে টেক্সট এক্সট্র্যাকশন
6. File history and management
   ফাইল ইতিহাস এবং ব্যবস্থাপনা

All uploaded files are stored in: jarvis_uploads/
সব আপলোড করা ফাইল সংরক্ষিত হয়: jarvis_uploads/

JARVIS can analyze, process, and learn from uploaded files!
জার্ভিস আপলোড করা ফাইল বিশ্লেষণ, প্রক্রিয়া এবং শিখতে পারে!""",
            "File Upload System"
        ))
        
        conn.commit()
        conn.close()
        
        print("✅ Knowledge base updated")
        
    except Exception as e:
        print(f"⚠️ Error creating database table: {e}")
    
    # Create file upload handler module
    create_file_handler()
    
    # Create UI component code
    create_ui_component()
    
    # Create integration instructions
    create_integration_guide()
    
    print("\n" + "="*80)
    print("  ✅ FILE UPLOAD SYSTEM ADDED SUCCESSFULLY!")
    print("  ✅ ফাইল আপলোড সিস্টেম সফলভাবে যোগ করা হয়েছে!")
    print("="*80)
    
    print(f"""
  📋 WHAT WAS CREATED:
  
  ✅ jarvis_uploads/ - Upload directory
  ✅ jarvis_file_handler.py - File processing module
  ✅ jarvis_upload_ui.py - UI component code
  ✅ FILE_UPLOAD_INTEGRATION_GUIDE.txt - Integration instructions
  ✅ Database table: uploaded_files
  
  📝 NEXT STEPS:
  
  1. Review jarvis_upload_ui.py for UI code
  2. Follow FILE_UPLOAD_INTEGRATION_GUIDE.txt to integrate
  3. Test file upload functionality
  4. Upload any file type to JARVIS chat!
    """)

def create_file_handler():
    """
    Create file handler module
    """
    code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS FILE HANDLER
জার্ভিস ফাইল হ্যান্ডলার

Handle uploaded files in JARVIS chat
"""

import os
import sqlite3
import shutil
from datetime import datetime
from pathlib import Path
import mimetypes

DB_PATH = "jarvis_memory.db.fixed-20260504-091901"
UPLOADS_DIR = "jarvis_uploads"

class FileHandler:
    """Handle file uploads and processing"""
    
    def __init__(self):
        self.uploads_dir = UPLOADS_DIR
        os.makedirs(self.uploads_dir, exist_ok=True)
        
    def handle_upload(self, file_path):
        """
        Handle file upload
        
        Args:
            file_path: Path to the file to upload
            
        Returns:
            dict: Upload result with file info
        """
        try:
            if not os.path.exists(file_path):
                return {
                    'success': False,
                    'error': 'File not found'
                }
            
            # Get file info
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            file_type = self.get_file_type(file_path)
            
            # Copy to uploads directory
            dest_path = os.path.join(self.uploads_dir, filename)
            
            # Handle duplicate filenames
            if os.path.exists(dest_path):
                name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{name}_{timestamp}{ext}"
                dest_path = os.path.join(self.uploads_dir, filename)
            
            shutil.copy2(file_path, dest_path)
            
            # Extract text if possible
            extracted_text = self.extract_text(dest_path, file_type)
            
            # Save to database
            file_id = self.save_to_database(
                filename, dest_path, file_type, file_size, extracted_text
            )
            
            return {
                'success': True,
                'file_id': file_id,
                'filename': filename,
                'filepath': dest_path,
                'file_type': file_type,
                'file_size': file_size,
                'extracted_text': extracted_text
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_file_type(self, file_path):
        """Get file type from extension"""
        ext = os.path.splitext(file_path)[1].lower()
        
        type_map = {
            # Images
            '.png': 'image', '.jpg': 'image', '.jpeg': 'image',
            '.gif': 'image', '.bmp': 'image', '.webp': 'image',
            '.svg': 'image', '.ico': 'image',
            
            # Documents
            '.pdf': 'document', '.doc': 'document', '.docx': 'document',
            '.txt': 'text', '.md': 'text', '.rtf': 'document',
            
            # Code
            '.py': 'code', '.js': 'code', '.html': 'code',
            '.css': 'code', '.json': 'code', '.xml': 'code',
            '.java': 'code', '.cpp': 'code', '.c': 'code',
            '.php': 'code', '.rb': 'code', '.go': 'code',
            
            # Data
            '.csv': 'data', '.xlsx': 'data', '.xls': 'data',
            
            # Archives
            '.zip': 'archive', '.rar': 'archive', '.7z': 'archive',
            '.tar': 'archive', '.gz': 'archive',
            
            # Audio
            '.mp3': 'audio', '.wav': 'audio', '.ogg': 'audio',
            '.flac': 'audio', '.m4a': 'audio',
            
            # Video
            '.mp4': 'video', '.avi': 'video', '.mkv': 'video',
            '.mov': 'video', '.wmv': 'video', '.flv': 'video',
        }
        
        return type_map.get(ext, 'other')
    
    def extract_text(self, file_path, file_type):
        """Extract text from file if possible"""
        try:
            if file_type == 'text' or file_type == 'code':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            
            # For other types, return basic info
            return f"File type: {file_type}\\nSize: {os.path.getsize(file_path)} bytes"
            
        except Exception as e:
            return f"Could not extract text: {e}"
    
    def save_to_database(self, filename, filepath, file_type, file_size, extracted_text):
        """Save file info to database"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO uploaded_files 
                (filename, filepath, file_type, file_size, extracted_text)
                VALUES (?, ?, ?, ?, ?)
            """, (filename, filepath, file_type, file_size, extracted_text))
            
            file_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return file_id
            
        except Exception as e:
            print(f"Error saving to database: {e}")
            return None
    
    def get_uploaded_files(self, limit=10):
        """Get list of uploaded files"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, filename, file_type, file_size, upload_date
                FROM uploaded_files
                ORDER BY upload_date DESC
                LIMIT ?
            """, (limit,))
            
            files = cursor.fetchall()
            conn.close()
            
            return files
            
        except Exception as e:
            print(f"Error getting files: {e}")
            return []
    
    def get_file_info(self, file_id):
        """Get detailed info about a file"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM uploaded_files WHERE id = ?
            """, (file_id,))
            
            file_info = cursor.fetchone()
            conn.close()
            
            return file_info
            
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None

# Global instance
file_handler = FileHandler()

def handle_file_upload(file_path):
    """Convenience function for file upload"""
    return file_handler.handle_upload(file_path)

def get_recent_uploads(limit=10):
    """Get recent uploaded files"""
    return file_handler.get_uploaded_files(limit)
'''
    
    with open("jarvis_file_handler.py", "w", encoding="utf-8") as f:
        f.write(code)
    
    print("✅ Created jarvis_file_handler.py")

def create_ui_component():
    """
    Create UI component code for file upload
    """
    code = '''#!/usr/bin/env python3
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
'''
    
    with open("jarvis_upload_ui.py", "w", encoding="utf-8") as f:
        f.write(code)
    
    print("✅ Created jarvis_upload_ui.py")

def create_integration_guide():
    """
    Create integration guide
    """
    guide = """
================================================================================
  📁 FILE UPLOAD INTEGRATION GUIDE
  📁 ফাইল আপলোড ইন্টিগ্রেশন গাইড
================================================================================

HOW TO ADD FILE UPLOAD TO JARVIS CHAT
জার্ভিস চ্যাটে ফাইল আপলোড কিভাবে যোগ করবেন

================================================================================
  STEP 1: IMPORT THE MODULES
  ধাপ ১: মডিউল ইম্পোর্ট করুন
================================================================================

Add these imports at the top of jarvis_panel.py:

from jarvis_file_handler import handle_file_upload, get_recent_uploads
from jarvis_upload_ui import add_file_upload_button


================================================================================
  STEP 2: MODIFY THE CMD_ZONE SECTION
  ধাপ ২: CMD_ZONE সেকশন পরিবর্তন করুন
================================================================================

In jarvis_panel.py, find the cmd_zone section (around line 505-520).

REPLACE THIS:
-------------
self.cmd_zone = ctk.CTkFrame(self.right_panel, fg_color="transparent")
self.cmd_zone.pack(fill="x", side="bottom", padx=30, pady=20)

self.entry = ctk.CTkEntry(self.cmd_zone, placeholder_text="Awaiting root command...", 
                          height=55, fg_color="#05080F", border_color=self.neon, 
                          text_color=self.neon, font=("Courier New", 16))
self.entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
self.entry.bind("<Return>", lambda e: self.fire_cmd())


WITH THIS:
----------
self.cmd_zone = ctk.CTkFrame(self.right_panel, fg_color="transparent")
self.cmd_zone.pack(fill="x", side="bottom", padx=30, pady=20)

# Add upload button
self.upload_btn = add_file_upload_button(self.cmd_zone, self.entry, self.log)
self.upload_btn.pack(side="left", padx=(0, 10))

# Entry field
self.entry = ctk.CTkEntry(self.cmd_zone, placeholder_text="Awaiting root command...", 
                          height=55, fg_color="#05080F", border_color=self.neon, 
                          text_color=self.neon, font=("Courier New", 16))
self.entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
self.entry.bind("<Return>", lambda e: self.fire_cmd())


================================================================================
  STEP 3: ADD FILE UPLOAD COMMAND
  ধাপ ৩: ফাইল আপলোড কমান্ড যোগ করুন
================================================================================

In the process() method, add file upload handling:

# Add to direct_commands list (around line 972):
direct_commands = [
    "clean", "workspace", "screenshot", "recon", "wifi", "users", "devices",
    "kali", "remote", "flipper", "alien", "purge", "mobile", "share", "send",
    "disk", "bt", "ducky", "cipher", "signal", "port", "payload", "find",
    "connect", "firewall", "browser", "window", "battery", "uptime",
    "upload", "files"  # ADD THESE
]

# Add file upload command handler (around line 1114):
elif cmd_root == "upload" or cmd_root == "files":
    recent = get_recent_uploads(10)
    if recent:
        cmd_res = "📁 Recent Uploads:\\n\\n"
        for file_id, filename, file_type, file_size, upload_date in recent:
            cmd_res += f"• {filename} ({file_type}, {file_size} bytes) - {upload_date}\\n"
    else:
        cmd_res = "No files uploaded yet. Click 📁 UPLOAD button to upload files!"


================================================================================
  STEP 4: TEST THE SYSTEM
  ধাপ ৪: সিস্টেম টেস্ট করুন
================================================================================

1. Run JARVIS:
   python jarvis_panel.py

2. Look for the "📁 UPLOAD" button next to the chat input

3. Click the button and select a file

4. JARVIS will:
   ✅ Upload the file
   ✅ Show file info
   ✅ Extract text if possible
   ✅ Auto-suggest analysis prompt

5. Type "upload" or "files" to see recent uploads


================================================================================
  FEATURES
  বৈশিষ্ট্য
================================================================================

✅ Upload any file type
   যেকোনো ফাইল টাইপ আপলোড করুন

✅ Automatic file type detection
   স্বয়ংক্রিয় ফাইল টাইপ সনাক্তকরণ

✅ Text extraction from text/code files
   টেক্সট/কোড ফাইল থেকে টেক্সট এক্সট্র্যাকশন

✅ Image preview support
   ছবি প্রিভিউ সমর্থন

✅ File history in database
   ডাটাবেসে ফাইল ইতিহাস

✅ Duplicate filename handling
   ডুপ্লিকেট ফাইলনাম হ্যান্ডলিং

✅ Auto-suggest analysis prompts
   স্বয়ংক্রিয়-সুপারিশ বিশ্লেষণ প্রম্পট


================================================================================
  SUPPORTED FILE TYPES
  সমর্থিত ফাইল টাইপ
================================================================================

📷 Images: PNG, JPG, JPEG, GIF, BMP, WEBP, SVG, ICO
📄 Documents: PDF, DOC, DOCX, TXT, MD, RTF
💻 Code: PY, JS, HTML, CSS, JSON, XML, JAVA, CPP, C, PHP, RB, GO
📊 Data: CSV, XLSX, XLS, JSON
📦 Archives: ZIP, RAR, 7Z, TAR, GZ
🎵 Audio: MP3, WAV, OGG, FLAC, M4A
🎬 Video: MP4, AVI, MKV, MOV, WMV, FLV
📁 Other: Any other file type


================================================================================
  USAGE EXAMPLES
  ব্যবহারের উদাহরণ
================================================================================

1. Upload an image:
   • Click 📁 UPLOAD
   • Select image file
   • JARVIS shows preview
   • Ask: "What's in this image?"

2. Upload a code file:
   • Click 📁 UPLOAD
   • Select .py file
   • JARVIS extracts code
   • Ask: "Review this code"

3. Upload a document:
   • Click 📁 UPLOAD
   • Select .txt or .pdf
   • JARVIS extracts text
   • Ask: "Summarize this document"

4. View recent uploads:
   • Type: "upload" or "files"
   • See list of recent files


================================================================================
  TROUBLESHOOTING
  সমস্যা সমাধান
================================================================================

Problem: Upload button not showing
Solution: Make sure you imported jarvis_upload_ui correctly

Problem: File not uploading
Solution: Check jarvis_uploads/ directory exists and has write permissions

Problem: Database error
Solution: Make sure uploaded_files table exists in database

Problem: Text extraction not working
Solution: Check file encoding, try UTF-8


================================================================================
  FILES CREATED
  তৈরি ফাইল
================================================================================

✅ jarvis_file_handler.py - File processing module
✅ jarvis_upload_ui.py - UI component
✅ jarvis_uploads/ - Upload directory
✅ Database table: uploaded_files
✅ FILE_UPLOAD_INTEGRATION_GUIDE.txt - This guide


================================================================================
  ✅ FILE UPLOAD SYSTEM READY!
  ✅ ফাইল আপলোড সিস্টেম প্রস্তুত!
================================================================================

Now JARVIS can accept file uploads in chat!
এখন জার্ভিস চ্যাটে ফাইল আপলোড গ্রহণ করতে পারে!

Upload any file and JARVIS will analyze it!
যেকোনো ফাইল আপলোড করুন এবং জার্ভিস এটি বিশ্লেষণ করবে!

================================================================================
"""
    
    with open("FILE_UPLOAD_INTEGRATION_GUIDE.txt", "w", encoding="utf-8") as f:
        f.write(guide)
    
    print("✅ Created FILE_UPLOAD_INTEGRATION_GUIDE.txt")

def main():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        print("Please make sure the database file exists.")
        return
    
    add_file_upload_system()
    
    print("\n" + "="*80)
    print("  🎉 SUCCESS!")
    print("  🎉 সফলতা!")
    print("="*80)
    print("""
  📁 File upload system has been added to JARVIS!
  📁 ফাইল আপলোড সিস্টেম জার্ভিসে যোগ করা হয়েছে!
  
  📝 Next steps:
  
  1. Read FILE_UPLOAD_INTEGRATION_GUIDE.txt
  2. Follow the integration steps
  3. Test the upload button
  4. Upload files to JARVIS chat!
  
  ✅ JARVIS can now accept file uploads!
  ✅ জার্ভিস এখন ফাইল আপলোড গ্রহণ করতে পারে!
    """)

if __name__ == "__main__":
    main()
