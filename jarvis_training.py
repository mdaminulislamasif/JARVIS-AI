#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS Training System - জার্ভিস ট্রেনিং সিস্টেম
Train JARVIS with new knowledge interactively
"""

import sqlite3
import os
from datetime import datetime

# Database path
DB_PATH = "jarvis_memory.db.fixed-20260504-091901"

class JarvisTrainer:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        
    def show_banner(self):
        print("\n" + "="*80)
        print("  🎓 JARVIS TRAINING SYSTEM - জার্ভিস ট্রেনিং সিস্টেম")
        print("  🧠 Teach JARVIS new knowledge - জার্ভিসকে নতুন জ্ঞান শেখান")
        print("="*80 + "\n")
        
    def show_menu(self):
        print("\n📚 TRAINING OPTIONS (ট্রেনিং অপশন):\n")
        print("  1️⃣  Add New Knowledge (নতুন জ্ঞান যোগ করুন)")
        print("  2️⃣  View All Knowledge (সব জ্ঞান দেখুন)")
        print("  3️⃣  Search Knowledge (জ্ঞান খুঁজুন)")
        print("  4️⃣  Update Knowledge (জ্ঞান আপডেট করুন)")
        print("  5️⃣  Delete Knowledge (জ্ঞান মুছুন)")
        print("  6️⃣  Show Statistics (পরিসংখ্যান দেখুন)")
        print("  7️⃣  Test JARVIS (জার্ভিস টেস্ট করুন)")
        print("  8️⃣  Batch Training (একসাথে অনেক শেখান)")
        print("  9️⃣  Export Knowledge (জ্ঞান এক্সপোর্ট করুন)")
        print("  0️⃣  Exit (বের হন)")
        print()
        
    def add_knowledge(self):
        """Add new knowledge to JARVIS"""
        print("\n" + "="*80)
        print("  ➕ ADD NEW KNOWLEDGE - নতুন জ্ঞান যোগ করুন")
        print("="*80 + "\n")
        
        topic = input("📌 Topic (বিষয়): ").strip()
        if not topic:
            print("❌ Topic cannot be empty!")
            return
            
        content = input("📝 Content (বিষয়বস্তু): ").strip()
        if not content:
            print("❌ Content cannot be empty!")
            return
            
        source = input("🔗 Source (উৎস) [Optional]: ").strip()
        if not source:
            source = "User Training"
            
        try:
            self.cursor.execute("""
                INSERT INTO knowledge_base (topic, content, source)
                VALUES (?, ?, ?)
            """, (topic, content, source))
            self.conn.commit()
            
            print("\n✅ Knowledge added successfully!")
            print(f"   Topic: {topic}")
            print(f"   Content: {content[:50]}...")
            print(f"   Source: {source}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def view_all_knowledge(self):
        """View all knowledge in database"""
        print("\n" + "="*80)
        print("  📚 ALL KNOWLEDGE - সব জ্ঞান")
        print("="*80 + "\n")
        
        limit = input("How many entries to show? (Press Enter for 20): ").strip()
        limit = int(limit) if limit.isdigit() else 20
        
        self.cursor.execute("""
            SELECT id, topic, content, source, created_at 
            FROM knowledge_base 
            ORDER BY id DESC 
            LIMIT ?
        """, (limit,))
        
        results = self.cursor.fetchall()
        
        if not results:
            print("❌ No knowledge found!")
            return
            
        for row in results:
            id, topic, content, source, created_at = row
            print(f"\n🆔 ID: {id}")
            print(f"📌 Topic: {topic}")
            print(f"📝 Content: {content[:100]}...")
            print(f"🔗 Source: {source}")
            print(f"📅 Created: {created_at}")
            print("-" * 80)
            
    def search_knowledge(self):
        """Search for knowledge"""
        print("\n" + "="*80)
        print("  🔍 SEARCH KNOWLEDGE - জ্ঞান খুঁজুন")
        print("="*80 + "\n")
        
        query = input("🔎 Search query: ").strip()
        if not query:
            print("❌ Query cannot be empty!")
            return
            
        self.cursor.execute("""
            SELECT id, topic, content, source 
            FROM knowledge_base 
            WHERE topic LIKE ? OR content LIKE ?
            ORDER BY id DESC
        """, (f"%{query}%", f"%{query}%"))
        
        results = self.cursor.fetchall()
        
        if not results:
            print(f"❌ No results found for: {query}")
            return
            
        print(f"\n✅ Found {len(results)} results:\n")
        
        for row in results:
            id, topic, content, source = row
            print(f"\n🆔 ID: {id}")
            print(f"📌 Topic: {topic}")
            print(f"📝 Content: {content[:100]}...")
            print(f"🔗 Source: {source}")
            print("-" * 80)
            
    def update_knowledge(self):
        """Update existing knowledge"""
        print("\n" + "="*80)
        print("  ✏️ UPDATE KNOWLEDGE - জ্ঞান আপডেট করুন")
        print("="*80 + "\n")
        
        id = input("🆔 Enter ID to update: ").strip()
        if not id.isdigit():
            print("❌ Invalid ID!")
            return
            
        # Check if exists
        self.cursor.execute("SELECT topic, content FROM knowledge_base WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        
        if not result:
            print(f"❌ No knowledge found with ID: {id}")
            return
            
        old_topic, old_content = result
        print(f"\n📌 Current Topic: {old_topic}")
        print(f"📝 Current Content: {old_content[:100]}...\n")
        
        new_topic = input(f"📌 New Topic (press Enter to keep '{old_topic}'): ").strip()
        new_content = input(f"📝 New Content (press Enter to keep current): ").strip()
        
        if not new_topic:
            new_topic = old_topic
        if not new_content:
            new_content = old_content
            
        try:
            self.cursor.execute("""
                UPDATE knowledge_base 
                SET topic = ?, content = ?
                WHERE id = ?
            """, (new_topic, new_content, id))
            self.conn.commit()
            
            print("\n✅ Knowledge updated successfully!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def delete_knowledge(self):
        """Delete knowledge"""
        print("\n" + "="*80)
        print("  🗑️ DELETE KNOWLEDGE - জ্ঞান মুছুন")
        print("="*80 + "\n")
        
        id = input("🆔 Enter ID to delete: ").strip()
        if not id.isdigit():
            print("❌ Invalid ID!")
            return
            
        # Check if exists
        self.cursor.execute("SELECT topic FROM knowledge_base WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        
        if not result:
            print(f"❌ No knowledge found with ID: {id}")
            return
            
        topic = result[0]
        confirm = input(f"⚠️ Delete '{topic}'? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            self.cursor.execute("DELETE FROM knowledge_base WHERE id = ?", (id,))
            self.conn.commit()
            print("✅ Knowledge deleted successfully!")
        else:
            print("❌ Deletion cancelled.")
            
    def show_statistics(self):
        """Show database statistics"""
        print("\n" + "="*80)
        print("  📊 JARVIS STATISTICS - পরিসংখ্যান")
        print("="*80 + "\n")
        
        # Total knowledge
        self.cursor.execute("SELECT COUNT(*) FROM knowledge_base")
        total_knowledge = self.cursor.fetchone()[0]
        
        # Total system info
        self.cursor.execute("SELECT COUNT(*) FROM system_info")
        total_system = self.cursor.fetchone()[0]
        
        # Recent additions
        self.cursor.execute("""
            SELECT COUNT(*) FROM knowledge_base 
            WHERE created_at >= datetime('now', '-7 days')
        """)
        recent = self.cursor.fetchone()[0]
        
        # Top sources
        self.cursor.execute("""
            SELECT source, COUNT(*) as count 
            FROM knowledge_base 
            GROUP BY source 
            ORDER BY count DESC 
            LIMIT 5
        """)
        top_sources = self.cursor.fetchall()
        
        print(f"📚 Total Knowledge Entries: {total_knowledge}")
        print(f"⚙️ Total System Info: {total_system}")
        print(f"🆕 Added in Last 7 Days: {recent}")
        print(f"\n🔝 Top 5 Knowledge Sources:\n")
        
        for source, count in top_sources:
            print(f"   • {source}: {count} entries")
            
        print()
        
    def test_jarvis(self):
        """Test JARVIS with a query"""
        print("\n" + "="*80)
        print("  🧪 TEST JARVIS - জার্ভিস টেস্ট করুন")
        print("="*80 + "\n")
        
        query = input("❓ Ask JARVIS: ").strip()
        if not query:
            print("❌ Query cannot be empty!")
            return
            
        # Search for relevant knowledge
        self.cursor.execute("""
            SELECT topic, content 
            FROM knowledge_base 
            WHERE topic LIKE ? OR content LIKE ?
            LIMIT 3
        """, (f"%{query}%", f"%{query}%"))
        
        results = self.cursor.fetchall()
        
        if not results:
            print(f"\n🤖 JARVIS: I don't have information about '{query}' yet.")
            print("   আমার কাছে এই বিষয়ে তথ্য নেই।")
            print("\n💡 Tip: Use option 1 to teach me!")
            return
            
        print(f"\n🤖 JARVIS: Here's what I know about '{query}':\n")
        
        for topic, content in results:
            print(f"📌 {topic}")
            print(f"   {content[:200]}...")
            print()
            
    def batch_training(self):
        """Add multiple knowledge entries at once"""
        print("\n" + "="*80)
        print("  📦 BATCH TRAINING - একসাথে অনেক শেখান")
        print("="*80 + "\n")
        
        print("Enter knowledge entries (format: topic | content)")
        print("Type 'done' when finished\n")
        
        entries = []
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            line = input("➡️ ").strip()
            if line.lower() == 'done':
                break
            if '|' not in line:
                print("❌ Invalid format! Use: topic | content")
                continue
            entries.append(line)
            
        if not entries:
            print("❌ No entries to add!")
            return
            
        added = 0
        for entry in entries:
            parts = entry.split('|', 1)
            if len(parts) == 2:
                topic, content = parts[0].strip(), parts[1].strip()
                try:
                    self.cursor.execute("""
                        INSERT INTO knowledge_base (topic, content, source)
                        VALUES (?, ?, ?)
                    """, (topic, content, "Batch Training"))
                    added += 1
                except Exception as e:
                    print(f"❌ Error adding '{topic}': {e}")
                    
        self.conn.commit()
        print(f"\n✅ Added {added} knowledge entries!")
        
    def export_knowledge(self):
        """Export knowledge to a text file"""
        print("\n" + "="*80)
        print("  💾 EXPORT KNOWLEDGE - জ্ঞান এক্সপোর্ট করুন")
        print("="*80 + "\n")
        
        filename = f"jarvis_knowledge_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        self.cursor.execute("SELECT topic, content, source FROM knowledge_base ORDER BY id")
        results = self.cursor.fetchall()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("JARVIS KNOWLEDGE EXPORT\n")
            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Entries: {len(results)}\n")
            f.write("="*80 + "\n\n")
            
            for topic, content, source in results:
                f.write(f"TOPIC: {topic}\n")
                f.write(f"SOURCE: {source}\n")
                f.write(f"CONTENT:\n{content}\n")
                f.write("-"*80 + "\n\n")
                
        print(f"✅ Knowledge exported to: {filename}")
        print(f"📊 Total entries: {len(results)}")
        
    def run(self):
        """Main training loop"""
        self.show_banner()
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            self.show_menu()
            choice = input("👉 Select option (অপশন নির্বাচন করুন): ").strip()
            
            if choice == '1':
                self.add_knowledge()
            elif choice == '2':
                self.view_all_knowledge()
            elif choice == '3':
                self.search_knowledge()
            elif choice == '4':
                self.update_knowledge()
            elif choice == '5':
                self.delete_knowledge()
            elif choice == '6':
                self.show_statistics()
            elif choice == '7':
                self.test_jarvis()
            elif choice == '8':
                self.batch_training()
            elif choice == '9':
                self.export_knowledge()
            elif choice == '0':
                print("\n👋 Goodbye! JARVIS training session ended.")
                print("   বিদায়! জার্ভিস ট্রেনিং শেষ।\n")
                break
            else:
                print("❌ Invalid option! Please try again.")
                
        self.conn.close()

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        print("   Please run the database setup first!")
    else:
        trainer = JarvisTrainer()
        trainer.run()
