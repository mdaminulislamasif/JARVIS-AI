#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS Background Learner - ব্যাকগ্রাউন্ড লার্নিং সিস্টেম
Runs in background, monitors activities, and learns automatically
"""

import sqlite3
import os
import time
import psutil
import win32gui
import win32process
from datetime import datetime
from collections import defaultdict
import threading
import keyboard
import pyperclip

# Database path
DB_PATH = "jarvis_memory.db.fixed-20260504-091901"

class JarvisBackgroundLearner:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.running = True
        self.app_usage = defaultdict(int)
        self.learned_activities = []
        self.last_window = None
        self.clipboard_history = []
        
    def show_banner(self):
        print("\n" + "="*80)
        print("  🤖 JARVIS BACKGROUND LEARNER - ব্যাকগ্রাউন্ড লার্নার")
        print("  👁️ Monitoring your activities and learning...")
        print("  👁️ আপনার কাজ মনিটর করছি এবং শিখছি...")
        print("="*80 + "\n")
        print("  🔹 Press Ctrl+Q to stop")
        print("  🔹 Press Ctrl+S to see statistics")
        print("  🔹 Press Ctrl+L to see what I learned")
        print("\n" + "="*80 + "\n")
        
    def get_active_window(self):
        """Get currently active window title and process"""
        try:
            window = win32gui.GetForegroundWindow()
            pid = win32process.GetWindowThreadProcessId(window)[1]
            process = psutil.Process(pid)
            window_title = win32gui.GetWindowText(window)
            return {
                'title': window_title,
                'process': process.name(),
                'exe': process.exe() if hasattr(process, 'exe') else 'Unknown'
            }
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return None
            
    def monitor_activities(self):
        """Monitor user activities in background"""
        print("🔍 Monitoring started... (ব্যাকগ্রাউন্ডে চলছে)")
        
        while self.running:
            try:
                # Get active window
                window_info = self.get_active_window()
                
                if window_info and window_info['title']:
                    # Track app usage
                    app_name = window_info['process']
                    self.app_usage[app_name] += 1
                    
                    # Learn from window title
                    if window_info['title'] != self.last_window:
                        self.learn_from_activity(window_info)
                        self.last_window = window_info['title']
                
                # Check clipboard for learning
                try:
                    clipboard_content = pyperclip.paste()
                    if clipboard_content and clipboard_content not in self.clipboard_history:
                        if len(clipboard_content) < 500:  # Only short texts
                            self.clipboard_history.append(clipboard_content)
                            self.learn_from_clipboard(clipboard_content)
                except Exception as e:

                    print(f"⚠️ Error: {e}")
                    pass
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                time.sleep(5)
                
    def learn_from_activity(self, window_info):
        """Learn from user activity"""
        try:
            title = window_info['title']
            process = window_info['process']
            
            # Detect programming activity
            if any(ext in title.lower() for ext in ['.py', '.js', '.java', '.cpp', '.html', '.css']):
                file_ext = None
                for ext in ['.py', '.js', '.java', '.cpp', '.html', '.css', '.json', '.xml']:
                    if ext in title.lower():
                        file_ext = ext
                        break
                
                if file_ext:
                    activity = f"User is coding in {file_ext} file"
                    self.save_learned_activity(activity, "Programming Activity")
                    
            # Detect browser activity
            if 'chrome' in process.lower() or 'firefox' in process.lower() or 'edge' in process.lower():
                if any(keyword in title.lower() for keyword in ['youtube', 'github', 'stackoverflow', 'google']):
                    activity = f"User is browsing: {title[:50]}"
                    self.save_learned_activity(activity, "Web Browsing")
                    
            # Detect document editing
            if 'word' in process.lower() or 'excel' in process.lower() or 'notepad' in process.lower():
                activity = f"User is editing document: {title[:50]}"
                self.save_learned_activity(activity, "Document Editing")
                
            # Detect terminal/command line
            if 'cmd' in process.lower() or 'powershell' in process.lower() or 'terminal' in process.lower():
                activity = "User is using command line"
                self.save_learned_activity(activity, "Command Line Usage")
                
        except Exception as e:
            print(f"⚠️ Error: {e}")
            
    def learn_from_clipboard(self, content):
        """Learn from clipboard content"""
        try:
            # Detect code snippets
            if any(keyword in content for keyword in ['def ', 'function ', 'class ', 'import ', 'const ', 'var ']):
                self.save_learned_activity(f"User copied code snippet: {content[:100]}", "Code Learning")
                
            # Detect commands
            if content.startswith(('python ', 'npm ', 'git ', 'cd ', 'mkdir ', 'pip ')):
                self.save_learned_activity(f"User used command: {content}", "Command Learning")
                
            # Detect URLs
            if content.startswith(('http://', 'https://', 'www.')):
                self.save_learned_activity(f"User visited: {content}", "Web Activity")
                
        except Exception as e:
            print(f"⚠️ Error: {e}")
            
    def save_learned_activity(self, activity, category):
        """Save learned activity to database"""
        try:
            # Check if already exists
            self.cursor.execute("""
                SELECT COUNT(*) FROM knowledge_base 
                WHERE topic = ? AND content = ?
            """, (category, activity))
            
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("""
                    INSERT INTO knowledge_base (topic, content, source)
                    VALUES (?, ?, ?)
                """, (category, activity, "Background Learning"))
                self.conn.commit()
                
                self.learned_activities.append({
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'category': category,
                    'activity': activity
                })
                
                print(f"  📚 Learned: {category} - {activity[:50]}...")
                
        except Exception as e:
            print(f"⚠️ Error: {e}")
            
    def show_statistics(self):
        """Show learning statistics"""
        print("\n" + "="*80)
        print("  📊 JARVIS LEARNING STATISTICS - শেখার পরিসংখ্যান")
        print("="*80 + "\n")
        
        # App usage
        print("  🖥️ Most Used Applications:")
        sorted_apps = sorted(self.app_usage.items(), key=lambda x: x[1], reverse=True)[:10]
        for app, count in sorted_apps:
            print(f"     • {app}: {count} times")
            
        # Learned activities
        print(f"\n  📚 Total Activities Learned: {len(self.learned_activities)}")
        
        # Recent learning
        print("\n  🆕 Recent Learning (Last 10):")
        for item in self.learned_activities[-10:]:
            print(f"     [{item['time']}] {item['category']}: {item['activity'][:50]}...")
            
        # Database stats
        self.cursor.execute("SELECT COUNT(*) FROM knowledge_base WHERE source = 'Background Learning'")
        bg_learned = self.cursor.fetchone()[0]
        print(f"\n  💾 Saved to Database: {bg_learned} entries")
        
        print("\n" + "="*80 + "\n")
        
    def show_learned_activities(self):
        """Show what JARVIS learned"""
        print("\n" + "="*80)
        print("  🧠 WHAT JARVIS LEARNED - জার্ভিস কি শিখেছে")
        print("="*80 + "\n")
        
        if not self.learned_activities:
            print("  ℹ️ No activities learned yet. Keep working!")
            print("  ℹ️ এখনও কিছু শেখেনি। কাজ চালিয়ে যান!")
        else:
            for idx, item in enumerate(self.learned_activities, 1):
                print(f"  {idx}. [{item['time']}] {item['category']}")
                print(f"     {item['activity']}")
                print()
                
        print("="*80 + "\n")
        
    def setup_hotkeys(self):
        """Setup keyboard shortcuts"""
        keyboard.add_hotkey('ctrl+q', self.stop)
        keyboard.add_hotkey('ctrl+s', self.show_statistics)
        keyboard.add_hotkey('ctrl+l', self.show_learned_activities)
        
    def stop(self):
        """Stop the background learner"""
        print("\n" + "="*80)
        print("  🛑 Stopping JARVIS Background Learner...")
        print("  🛑 জার্ভিস ব্যাকগ্রাউন্ড লার্নার বন্ধ হচ্ছে...")
        print("="*80 + "\n")
        
        self.show_statistics()
        
        self.running = False
        self.conn.close()
        
        print("  ✅ JARVIS stopped. Goodbye!")
        print("  ✅ জার্ভিস বন্ধ হয়েছে। বিদায়!")
        print("\n" + "="*80 + "\n")
        
        os._exit(0)
        
    def run(self):
        """Main run loop"""
        self.show_banner()
        
        # Setup hotkeys
        self.setup_hotkeys()
        
        # Start monitoring in background thread
        monitor_thread = threading.Thread(target=self.monitor_activities, daemon=True)
        monitor_thread.start()
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

if __name__ == "__main__":
    print("\n" + "="*80)
    print("  🚀 Starting JARVIS Background Learner...")
    print("  🚀 জার্ভিস ব্যাকগ্রাউন্ড লার্নার শুরু হচ্ছে...")
    print("="*80 + "\n")
    
    # Check dependencies
    try:
        import win32gui
        import win32process
        import psutil
        import keyboard
        import pyperclip
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\n📦 Installing required packages...")
        print("   Run: pip install pywin32 psutil keyboard pyperclip")
        print("\n   Or run: pip install -r requirements_background.txt")
        input("\nPress Enter to exit...")
        exit(1)
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        print("   Please run the database setup first!")
        input("\nPress Enter to exit...")
        exit(1)
    
    learner = JarvisBackgroundLearner()
    learner.run()
