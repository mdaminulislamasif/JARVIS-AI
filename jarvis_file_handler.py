#!/usr/bin/env python3
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

DB_PATH = "jarvis_memory.db"
UPLOADS_DIR = "jarvis_uploads"

class FileHandler:
    """Handle file uploads and processing"""
    
    def __init__(self):
        self.uploads_dir = UPLOADS_DIR
        os.makedirs(self.uploads_dir, exist_ok=True)
        self.init_db()

    def init_db(self):
        """Initialize database tables if they do not exist"""
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
            conn.close()
        except Exception as e:
            print(f"Error initializing uploaded_files table: {e}")
        
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
            return f"File type: {file_type}\nSize: {os.path.getsize(file_path)} bytes"
            
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
