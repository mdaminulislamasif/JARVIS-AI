#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS Auto-Updater - Self-Updating System
জার্ভিস স্বয়ংক্রিয় আপডেটার - নিজেকে আপডেট করার সিস্টেম
"""

import sqlite3
import os
import time
import schedule
from datetime import datetime, timedelta
import subprocess

DB_PATH = "jarvis_memory.db.fixed-20260504-091901"

class JarvisAutoUpdater:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.update_log = []
        
    def show_banner(self):
        print("\n" + "="*80)
        print("  🔄 JARVIS AUTO-UPDATER - SELF-UPDATING SYSTEM")
        print("  🔄 জার্ভিস স্বয়ংক্রিয় আপডেটার - নিজেকে আপডেট করার সিস্টেম")
        print("="*80 + "\n")
        print("  JARVIS will update itself automatically!")
        print("  জার্ভিস নিজেকে স্বয়ংক্রিয়ভাবে আপডেট করবে!")
        print("\n" + "="*80 + "\n")
        
    def check_for_updates(self):
        """Check if updates are needed"""
        print(f"🔍 Checking for updates... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        print(f"🔍 আপডেট চেক করছি... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
        
        # Check last update time
        try:
            self.cursor.execute("""
                SELECT value FROM system_info 
                WHERE key = 'last_auto_update'
            """)
            result = self.cursor.fetchone()
            
            if result:
                last_update = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
                time_since_update = datetime.now() - last_update
                
                print(f"  📅 Last update: {last_update.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  ⏱️ Time since update: {time_since_update}")
                
                # Update if more than 24 hours
                if time_since_update > timedelta(hours=24):
                    print(f"  ✅ Update needed! (More than 24 hours)\n")
                    return True
                else:
                    print(f"  ℹ️ No update needed yet.\n")
                    return False
            else:
                print(f"  ✅ First time update!\n")
                return True
                
        except Exception as e:
            print(f"  ✅ Update check: Proceeding with update\n")
            return True
            
    def update_knowledge(self):
        """Update JARVIS knowledge"""
        print("📚 Updating JARVIS knowledge...")
        print("📚 জার্ভিসের জ্ঞান আপডেট করছি...\n")
        
        updates_made = 0
        
        # Daily knowledge updates
        daily_knowledge = [
            {
                "topic": f"Daily Update {datetime.now().strftime('%Y-%m-%d')}",
                "content": f"""
Daily automatic update performed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

JARVIS is continuously learning and improving!
জার্ভিস ক্রমাগত শিখছে এবং উন্নতি করছে!

System Status: Operational
Database Status: Healthy
Learning Status: Active
""",
                "source": "Auto-Update System"
            },
            {
                "topic": "Latest Technology Trends",
                "content": f"""
Updated on: {datetime.now().strftime('%Y-%m-%d')}

Current trending technologies:
• Artificial Intelligence and Machine Learning
• Cloud Computing and Edge Computing
• Quantum Computing developments
• Blockchain and Web3
• Internet of Things (IoT)
• 5G and 6G networks
• Cybersecurity advancements

JARVIS stays updated with latest tech trends!
জার্ভিস সর্বশেষ প্রযুক্তি ট্রেন্ডের সাথে আপডেট থাকে!
""",
                "source": "Auto-Update System"
            }
        ]
        
        for item in daily_knowledge:
            try:
                # Check if exists
                self.cursor.execute("""
                    SELECT COUNT(*) FROM knowledge_base 
                    WHERE topic = ?
                """, (item['topic'],))
                
                if self.cursor.fetchone()[0] == 0:
                    # Insert new
                    self.cursor.execute("""
                        INSERT INTO knowledge_base (topic, content, source)
                        VALUES (?, ?, ?)
                    """, (item['topic'], item['content'], item['source']))
                    print(f"  ✅ Added: {item['topic']}")
                    updates_made += 1
                else:
                    # Update existing
                    self.cursor.execute("""
                        UPDATE knowledge_base 
                        SET content = ?, source = ?
                        WHERE topic = ?
                    """, (item['content'], item['source'], item['topic']))
                    print(f"  🔄 Updated: {item['topic']}")
                    updates_made += 1
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
                
        self.conn.commit()
        return updates_made
        
    def update_system_info(self):
        """Update system information"""
        print("\n⚙️ Updating system information...")
        print("⚙️ সিস্টেম তথ্য আপডেট করছি...\n")
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        system_updates = [
            ("last_auto_update", current_time),
            ("auto_update_enabled", "true"),
            ("total_auto_updates", str(self.get_update_count() + 1)),
        ]
        
        for key, value in system_updates:
            try:
                self.cursor.execute("""
                    SELECT COUNT(*) FROM system_info WHERE key = ?
                """, (key,))
                
                if self.cursor.fetchone()[0] == 0:
                    self.cursor.execute("""
                        INSERT INTO system_info (key, value, category)
                        VALUES (?, ?, 'auto_update')
                    """, (key, value))
                else:
                    self.cursor.execute("""
                        UPDATE system_info SET value = ? WHERE key = ?
                    """, (value, key))
                    
                print(f"  ✅ {key}: {value}")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                
        self.conn.commit()
        
    def get_update_count(self):
        """Get total number of auto-updates"""
        try:
            self.cursor.execute("""
                SELECT value FROM system_info 
                WHERE key = 'total_auto_updates'
            """)
            result = self.cursor.fetchone()
            return int(result[0]) if result else 0
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return 0
            
    def run_update(self):
        """Run complete update process"""
        print("🚀 Starting auto-update process...")
        print("🚀 স্বয়ংক্রিয় আপডেট প্রক্রিয়া শুরু হচ্ছে...\n")
        
        start_time = time.time()
        
        # Update knowledge
        updates = self.update_knowledge()
        
        # Update system info
        self.update_system_info()
        
        # Get statistics
        self.cursor.execute("SELECT COUNT(*) FROM knowledge_base")
        total_knowledge = self.cursor.fetchone()[0]
        
        elapsed_time = time.time() - start_time
        
        print("\n" + "="*80)
        print("  ✅ AUTO-UPDATE COMPLETED!")
        print("  ✅ স্বয়ংক্রিয় আপডেট সম্পন্ন!")
        print("="*80 + "\n")
        
        print(f"  📊 Statistics:")
        print(f"     • Updates made: {updates}")
        print(f"     • Total knowledge: {total_knowledge} entries")
        print(f"     • Update count: {self.get_update_count()}")
        print(f"     • Time taken: {elapsed_time:.2f} seconds")
        print(f"     • Next update: In 24 hours")
        
        print("\n" + "="*80 + "\n")
        
        self.update_log.append({
            'time': datetime.now(),
            'updates': updates,
            'total': total_knowledge
        })
        
    def schedule_updates(self):
        """Schedule automatic updates"""
        print("📅 Scheduling automatic updates...")
        print("📅 স্বয়ংক্রিয় আপডেট শিডিউল করছি...\n")
        
        # Schedule daily update at 3 AM
        schedule.every().day.at("03:00").do(self.run_update)
        
        # Also check every hour
        schedule.every().hour.do(self.check_for_updates)
        
        print("  ✅ Updates scheduled:")
        print("     • Daily at 3:00 AM")
        print("     • Hourly checks")
        print("\n" + "="*80 + "\n")
        
    def run_continuous(self):
        """Run continuous update monitoring"""
        self.show_banner()
        
        print("🔄 JARVIS Auto-Updater is now running!")
        print("🔄 জার্ভিস স্বয়ংক্রিয় আপডেটার এখন চলছে!\n")
        
        # Run initial update if needed
        if self.check_for_updates():
            self.run_update()
        
        # Schedule future updates
        self.schedule_updates()
        
        print("⏰ Waiting for scheduled updates...")
        print("⏰ শিডিউল করা আপডেটের জন্য অপেক্ষা করছি...\n")
        print("Press Ctrl+C to stop")
        print("বন্ধ করতে Ctrl+C চাপুন\n")
        
        try:
            # WARNING: Infinite loop - ensure break condition exists
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n\n🛑 Auto-Updater stopped.")
            print("🛑 স্বয়ংক্রিয় আপডেটার বন্ধ হয়েছে।\n")
            
        self.conn.close()
        
    def run_once(self):
        """Run update once and exit"""
        self.show_banner()
        
        if self.check_for_updates():
            self.run_update()
        else:
            print("  ℹ️ No update needed at this time.")
            print("  ℹ️ এই মুহূর্তে আপডেটের প্রয়োজন নেই।\n")
            
        self.conn.close()

if __name__ == "__main__":
    import sys
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        sys.exit(1)
    
    updater = JarvisAutoUpdater()
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        # Run continuously
        updater.run_continuous()
    else:
        # Run once
        updater.run_once()
