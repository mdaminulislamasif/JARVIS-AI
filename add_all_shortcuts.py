#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add All Shortcut Keys to JARVIS
সব শর্টকাট কী জার্ভিসে যোগ করা
"""

import sqlite3
import os

DB_PATH = "jarvis_memory.db.fixed-20260504-091901"

def add_all_shortcuts():
    """Add comprehensive shortcut keys database"""
    
    print("\n" + "="*80)
    print("  ⌨️ ADDING ALL SHORTCUT KEYS TO JARVIS")
    print("  ⌨️ সব শর্টকাট কী জার্ভিসে যোগ করা হচ্ছে")
    print("="*80 + "\n")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    shortcuts = [
        # ==================== WINDOWS SHORTCUTS ====================
        ("Windows Key", "Win", "Open Start Menu | স্টার্ট মেনু খুলুন", "Windows Shortcuts"),
        ("Windows + D", "Win + D", "Show Desktop | ডেস্কটপ দেখান", "Windows Shortcuts"),
        ("Windows + E", "Win + E", "Open File Explorer | ফাইল এক্সপ্লোরার খুলুন", "Windows Shortcuts"),
        ("Windows + L", "Win + L", "Lock Computer | কম্পিউটার লক করুন", "Windows Shortcuts"),
        ("Windows + R", "Win + R", "Open Run Dialog | রান ডায়ালগ খুলুন", "Windows Shortcuts"),
        ("Windows + I", "Win + I", "Open Settings | সেটিংস খুলুন", "Windows Shortcuts"),
        ("Windows + Tab", "Win + Tab", "Task View | টাস্ক ভিউ", "Windows Shortcuts"),
        ("Windows + PrtScn", "Win + PrtScn", "Take Screenshot | স্ক্রিনশট নিন", "Windows Shortcuts"),
        ("Windows + V", "Win + V", "Clipboard History | ক্লিপবোর্ড হিস্ট্রি", "Windows Shortcuts"),
        ("Windows + X", "Win + X", "Quick Link Menu | কুইক লিংক মেনু", "Windows Shortcuts"),
        ("Alt + Tab", "Alt + Tab", "Switch Between Apps | অ্যাপ পরিবর্তন করুন", "Windows Shortcuts"),
        ("Alt + F4", "Alt + F4", "Close Active Window | উইন্ডো বন্ধ করুন", "Windows Shortcuts"),
        ("Ctrl + Shift + Esc", "Ctrl + Shift + Esc", "Open Task Manager | টাস্ক ম্যানেজার খুলুন", "Windows Shortcuts"),
        
        # ==================== COMMON SHORTCUTS ====================
        ("Copy", "Ctrl + C", "Copy selected text/file | কপি করুন", "Common Shortcuts"),
        ("Cut", "Ctrl + X", "Cut selected text/file | কাট করুন", "Common Shortcuts"),
        ("Paste", "Ctrl + V", "Paste copied content | পেস্ট করুন", "Common Shortcuts"),
        ("Undo", "Ctrl + Z", "Undo last action | আনডু করুন", "Common Shortcuts"),
        ("Redo", "Ctrl + Y", "Redo last action | রিডু করুন", "Common Shortcuts"),
        ("Select All", "Ctrl + A", "Select all content | সব সিলেক্ট করুন", "Common Shortcuts"),
        ("Save", "Ctrl + S", "Save current file | সেভ করুন", "Common Shortcuts"),
        ("Save As", "Ctrl + Shift + S", "Save file with new name | নতুন নামে সেভ করুন", "Common Shortcuts"),
        ("Open", "Ctrl + O", "Open file | ফাইল খুলুন", "Common Shortcuts"),
        ("New", "Ctrl + N", "Create new file | নতুন ফাইল তৈরি করুন", "Common Shortcuts"),
        ("Print", "Ctrl + P", "Print document | প্রিন্ট করুন", "Common Shortcuts"),
        ("Find", "Ctrl + F", "Find text | খুঁজুন", "Common Shortcuts"),
        ("Replace", "Ctrl + H", "Find and replace | খুঁজুন এবং পরিবর্তন করুন", "Common Shortcuts"),
        
        # ==================== MICROSOFT WORD SHORTCUTS ====================
        ("Bold", "Ctrl + B", "Make text bold | বোল্ড করুন", "MS Word Shortcuts"),
        ("Italic", "Ctrl + I", "Make text italic | ইটালিক করুন", "MS Word Shortcuts"),
        ("Underline", "Ctrl + U", "Underline text | আন্ডারলাইন করুন", "MS Word Shortcuts"),
        ("Left Align", "Ctrl + L", "Align text left | বাম দিকে সাজান", "MS Word Shortcuts"),
        ("Center Align", "Ctrl + E", "Center align text | মাঝখানে সাজান", "MS Word Shortcuts"),
        ("Right Align", "Ctrl + R", "Align text right | ডান দিকে সাজান", "MS Word Shortcuts"),
        ("Justify", "Ctrl + J", "Justify text | জাস্টিফাই করুন", "MS Word Shortcuts"),
        ("Increase Font Size", "Ctrl + ]", "Increase font size | ফন্ট সাইজ বাড়ান", "MS Word Shortcuts"),
        ("Decrease Font Size", "Ctrl + [", "Decrease font size | ফন্ট সাইজ কমান", "MS Word Shortcuts"),
        ("Insert Hyperlink", "Ctrl + K", "Insert hyperlink | হাইপারলিংক যোগ করুন", "MS Word Shortcuts"),
        ("Spell Check", "F7", "Check spelling | বানান চেক করুন", "MS Word Shortcuts"),
        ("Thesaurus", "Shift + F7", "Open thesaurus | থিসরাস খুলুন", "MS Word Shortcuts"),
        ("Word Count", "Ctrl + Shift + G", "Show word count | শব্দ গণনা দেখান", "MS Word Shortcuts"),
        
        # ==================== MICROSOFT EXCEL SHORTCUTS ====================
        ("New Workbook", "Ctrl + N", "Create new workbook | নতুন ওয়ার্কবুক তৈরি করুন", "MS Excel Shortcuts"),
        ("Insert Function", "Shift + F3", "Insert function | ফাংশন যোগ করুন", "MS Excel Shortcuts"),
        ("AutoSum", "Alt + =", "AutoSum selected cells | অটোসাম", "MS Excel Shortcuts"),
        ("Format Cells", "Ctrl + 1", "Open format cells dialog | ফরম্যাট সেল", "MS Excel Shortcuts"),
        ("Insert Row", "Ctrl + Shift + +", "Insert new row | নতুন রো যোগ করুন", "MS Excel Shortcuts"),
        ("Delete Row", "Ctrl + -", "Delete row | রো মুছুন", "MS Excel Shortcuts"),
        ("Go to Cell", "Ctrl + G", "Go to specific cell | নির্দিষ্ট সেলে যান", "MS Excel Shortcuts"),
        ("Fill Down", "Ctrl + D", "Fill down | নিচে ফিল করুন", "MS Excel Shortcuts"),
        ("Fill Right", "Ctrl + R", "Fill right | ডানে ফিল করুন", "MS Excel Shortcuts"),
        ("Insert Current Date", "Ctrl + ;", "Insert today's date | আজকের তারিখ যোগ করুন", "MS Excel Shortcuts"),
        ("Insert Current Time", "Ctrl + Shift + ;", "Insert current time | বর্তমান সময় যোগ করুন", "MS Excel Shortcuts"),
        ("Edit Cell", "F2", "Edit active cell | সেল এডিট করুন", "MS Excel Shortcuts"),
        ("Create Chart", "Alt + F1", "Create chart | চার্ট তৈরি করুন", "MS Excel Shortcuts"),
        ("Absolute Reference", "F4", "Toggle absolute reference | অ্যাবসলিউট রেফারেন্স", "MS Excel Shortcuts"),
        
        # ==================== MICROSOFT POWERPOINT SHORTCUTS ====================
        ("New Slide", "Ctrl + M", "Insert new slide | নতুন স্লাইড যোগ করুন", "MS PowerPoint Shortcuts"),
        ("Duplicate Slide", "Ctrl + D", "Duplicate current slide | স্লাইড ডুপ্লিকেট করুন", "MS PowerPoint Shortcuts"),
        ("Start Presentation", "F5", "Start slideshow from beginning | প্রেজেন্টেশন শুরু করুন", "MS PowerPoint Shortcuts"),
        ("Start from Current", "Shift + F5", "Start from current slide | বর্তমান স্লাইড থেকে শুরু করুন", "MS PowerPoint Shortcuts"),
        ("End Presentation", "Esc", "End slideshow | প্রেজেন্টেশন শেষ করুন", "MS PowerPoint Shortcuts"),
        ("Next Slide", "N or Space", "Go to next slide | পরবর্তী স্লাইড", "MS PowerPoint Shortcuts"),
        ("Previous Slide", "P or Backspace", "Go to previous slide | আগের স্লাইড", "MS PowerPoint Shortcuts"),
        ("Black Screen", "B", "Black screen during presentation | কালো স্ক্রিন", "MS PowerPoint Shortcuts"),
        ("White Screen", "W", "White screen during presentation | সাদা স্ক্রিন", "MS PowerPoint Shortcuts"),
        ("Group Objects", "Ctrl + G", "Group selected objects | অবজেক্ট গ্রুপ করুন", "MS PowerPoint Shortcuts"),
        ("Ungroup Objects", "Ctrl + Shift + G", "Ungroup objects | আনগ্রুপ করুন", "MS PowerPoint Shortcuts"),
        
        # ==================== BROWSER SHORTCUTS ====================
        ("New Tab", "Ctrl + T", "Open new tab | নতুন ট্যাব খুলুন", "Browser Shortcuts"),
        ("Close Tab", "Ctrl + W", "Close current tab | ট্যাব বন্ধ করুন", "Browser Shortcuts"),
        ("Reopen Tab", "Ctrl + Shift + T", "Reopen closed tab | বন্ধ ট্যাব আবার খুলুন", "Browser Shortcuts"),
        ("New Window", "Ctrl + N", "Open new window | নতুন উইন্ডো খুলুন", "Browser Shortcuts"),
        ("Incognito Mode", "Ctrl + Shift + N", "Open incognito window | ইনকগনিটো মোড", "Browser Shortcuts"),
        ("Refresh Page", "F5 or Ctrl + R", "Refresh current page | পেজ রিফ্রেশ করুন", "Browser Shortcuts"),
        ("Hard Refresh", "Ctrl + F5", "Hard refresh (clear cache) | হার্ড রিফ্রেশ", "Browser Shortcuts"),
        ("Bookmark Page", "Ctrl + D", "Bookmark current page | বুকমার্ক করুন", "Browser Shortcuts"),
        ("Show Bookmarks", "Ctrl + Shift + B", "Show bookmarks bar | বুকমার্ক বার দেখান", "Browser Shortcuts"),
        ("History", "Ctrl + H", "Open history | হিস্ট্রি খুলুন", "Browser Shortcuts"),
        ("Downloads", "Ctrl + J", "Open downloads | ডাউনলোড খুলুন", "Browser Shortcuts"),
        ("Address Bar", "Ctrl + L or F6", "Focus address bar | অ্যাড্রেস বার ফোকাস করুন", "Browser Shortcuts"),
        ("Zoom In", "Ctrl + +", "Zoom in page | জুম ইন", "Browser Shortcuts"),
        ("Zoom Out", "Ctrl + -", "Zoom out page | জুম আউট", "Browser Shortcuts"),
        ("Reset Zoom", "Ctrl + 0", "Reset zoom to 100% | জুম রিসেট করুন", "Browser Shortcuts"),
        
        # ==================== TEXT EDITOR SHORTCUTS ====================
        ("Go to Line", "Ctrl + G", "Go to specific line | নির্দিষ্ট লাইনে যান", "Text Editor Shortcuts"),
        ("Comment Line", "Ctrl + /", "Comment/uncomment line | কমেন্ট করুন", "Text Editor Shortcuts"),
        ("Duplicate Line", "Ctrl + D", "Duplicate current line | লাইন ডুপ্লিকেট করুন", "Text Editor Shortcuts"),
        ("Delete Line", "Ctrl + Shift + K", "Delete current line | লাইন মুছুন", "Text Editor Shortcuts"),
        ("Move Line Up", "Alt + Up", "Move line up | লাইন উপরে নিন", "Text Editor Shortcuts"),
        ("Move Line Down", "Alt + Down", "Move line down | লাইন নিচে নিন", "Text Editor Shortcuts"),
        ("Multi-Cursor", "Ctrl + Alt + Up/Down", "Add multiple cursors | মাল্টি-কার্সার", "Text Editor Shortcuts"),
        ("Select Word", "Ctrl + D", "Select next occurrence | পরবর্তী শব্দ সিলেক্ট করুন", "Text Editor Shortcuts"),
        ("Indent", "Tab", "Indent line | ইন্ডেন্ট করুন", "Text Editor Shortcuts"),
        ("Outdent", "Shift + Tab", "Outdent line | আউটডেন্ট করুন", "Text Editor Shortcuts"),
        ("Toggle Sidebar", "Ctrl + B", "Show/hide sidebar | সাইডবার টগল করুন", "Text Editor Shortcuts"),
        ("Command Palette", "Ctrl + Shift + P", "Open command palette | কমান্ড প্যালেট খুলুন", "Text Editor Shortcuts"),
        
        # ==================== VS CODE SHORTCUTS ====================
        ("Quick Open", "Ctrl + P", "Quick open file | দ্রুত ফাইল খুলুন", "VS Code Shortcuts"),
        ("Terminal", "Ctrl + `", "Toggle terminal | টার্মিনাল টগল করুন", "VS Code Shortcuts"),
        ("Split Editor", "Ctrl + \\", "Split editor | এডিটর স্প্লিট করুন", "VS Code Shortcuts"),
        ("Close Editor", "Ctrl + W", "Close current editor | এডিটর বন্ধ করুন", "VS Code Shortcuts"),
        ("Go to Definition", "F12", "Go to definition | ডেফিনিশনে যান", "VS Code Shortcuts"),
        ("Peek Definition", "Alt + F12", "Peek definition | ডেফিনিশন দেখুন", "VS Code Shortcuts"),
        ("Rename Symbol", "F2", "Rename symbol | সিম্বল রিনেম করুন", "VS Code Shortcuts"),
        ("Format Document", "Shift + Alt + F", "Format document | ডকুমেন্ট ফরম্যাট করুন", "VS Code Shortcuts"),
        ("Show Problems", "Ctrl + Shift + M", "Show problems panel | প্রবলেম প্যানেল দেখান", "VS Code Shortcuts"),
        ("Git", "Ctrl + Shift + G", "Open Git panel | গিট প্যানেল খুলুন", "VS Code Shortcuts"),
        
        # ==================== AUTOCAD SHORTCUTS ====================
        ("Line", "L", "Draw line | লাইন আঁকুন", "AutoCAD Shortcuts"),
        ("Circle", "C", "Draw circle | বৃত্ত আঁকুন", "AutoCAD Shortcuts"),
        ("Arc", "A", "Draw arc | আর্ক আঁকুন", "AutoCAD Shortcuts"),
        ("Rectangle", "REC", "Draw rectangle | আয়তক্ষেত্র আঁকুন", "AutoCAD Shortcuts"),
        ("Polyline", "PL", "Draw polyline | পলিলাইন আঁকুন", "AutoCAD Shortcuts"),
        ("Move", "M", "Move objects | অবজেক্ট সরান", "AutoCAD Shortcuts"),
        ("Copy", "CO", "Copy objects | কপি করুন", "AutoCAD Shortcuts"),
        ("Rotate", "RO", "Rotate objects | ঘুরান", "AutoCAD Shortcuts"),
        ("Scale", "SC", "Scale objects | স্কেল করুন", "AutoCAD Shortcuts"),
        ("Trim", "TR", "Trim objects | ট্রিম করুন", "AutoCAD Shortcuts"),
        ("Extend", "EX", "Extend objects | এক্সটেন্ড করুন", "AutoCAD Shortcuts"),
        ("Offset", "O", "Offset objects | অফসেট করুন", "AutoCAD Shortcuts"),
        ("Mirror", "MI", "Mirror objects | মিরর করুন", "AutoCAD Shortcuts"),
        ("Array", "AR", "Create array | অ্যারে তৈরি করুন", "AutoCAD Shortcuts"),
        ("Erase", "E", "Erase objects | মুছুন", "AutoCAD Shortcuts"),
        ("Undo", "U", "Undo last action | আনডু করুন", "AutoCAD Shortcuts"),
        ("Redo", "REDO", "Redo last action | রিডু করুন", "AutoCAD Shortcuts"),
        ("Zoom Extents", "Z + E", "Zoom to extents | জুম এক্সটেন্টস", "AutoCAD Shortcuts"),
        ("Zoom Window", "Z + W", "Zoom window | জুম উইন্ডো", "AutoCAD Shortcuts"),
        ("Pan", "P", "Pan view | প্যান ভিউ", "AutoCAD Shortcuts"),
        ("Layer", "LA", "Layer properties | লেয়ার প্রপার্টিজ", "AutoCAD Shortcuts"),
        ("Properties", "PR", "Object properties | অবজেক্ট প্রপার্টিজ", "AutoCAD Shortcuts"),
        ("Dimension", "DIM", "Create dimension | ডাইমেনশন তৈরি করুন", "AutoCAD Shortcuts"),
        ("Text", "T", "Create text | টেক্সট তৈরি করুন", "AutoCAD Shortcuts"),
        ("Hatch", "H", "Create hatch | হ্যাচ তৈরি করুন", "AutoCAD Shortcuts"),
        
        # ==================== FILE EXPLORER SHORTCUTS ====================
        ("New Folder", "Ctrl + Shift + N", "Create new folder | নতুন ফোল্ডার তৈরি করুন", "File Explorer Shortcuts"),
        ("Rename", "F2", "Rename file/folder | রিনেম করুন", "File Explorer Shortcuts"),
        ("Delete", "Delete", "Delete file/folder | মুছুন", "File Explorer Shortcuts"),
        ("Permanent Delete", "Shift + Delete", "Permanently delete | স্থায়ীভাবে মুছুন", "File Explorer Shortcuts"),
        ("Refresh", "F5", "Refresh view | রিফ্রেশ করুন", "File Explorer Shortcuts"),
        ("Address Bar", "Alt + D", "Focus address bar | অ্যাড্রেস বার ফোকাস করুন", "File Explorer Shortcuts"),
        ("Go Up", "Alt + Up", "Go to parent folder | উপরের ফোল্ডারে যান", "File Explorer Shortcuts"),
        ("Go Back", "Alt + Left", "Go back | পিছনে যান", "File Explorer Shortcuts"),
        ("Go Forward", "Alt + Right", "Go forward | সামনে যান", "File Explorer Shortcuts"),
        ("Properties", "Alt + Enter", "Show properties | প্রপার্টিজ দেখান", "File Explorer Shortcuts"),
        
        # ==================== SCREENSHOT SHORTCUTS ====================
        ("Full Screenshot", "PrtScn", "Capture full screen | পুরো স্ক্রিন ক্যাপচার", "Screenshot Shortcuts"),
        ("Active Window", "Alt + PrtScn", "Capture active window | অ্যাক্টিভ উইন্ডো ক্যাপচার", "Screenshot Shortcuts"),
        ("Snipping Tool", "Win + Shift + S", "Open snipping tool | স্নিপিং টুল খুলুন", "Screenshot Shortcuts"),
        
        # ==================== PHOTOSHOP SHORTCUTS ====================
        ("New File", "Ctrl + N", "Create new file | নতুন ফাইল তৈরি করুন", "Photoshop Shortcuts"),
        ("Free Transform", "Ctrl + T", "Free transform | ফ্রি ট্রান্সফর্ম", "Photoshop Shortcuts"),
        ("Merge Layers", "Ctrl + E", "Merge layers | লেয়ার মার্জ করুন", "Photoshop Shortcuts"),
        ("New Layer", "Ctrl + Shift + N", "Create new layer | নতুন লেয়ার তৈরি করুন", "Photoshop Shortcuts"),
        ("Duplicate Layer", "Ctrl + J", "Duplicate layer | লেয়ার ডুপ্লিকেট করুন", "Photoshop Shortcuts"),
        ("Invert Selection", "Ctrl + Shift + I", "Invert selection | সিলেকশন ইনভার্ট করুন", "Photoshop Shortcuts"),
        ("Deselect", "Ctrl + D", "Deselect all | ডিসিলেক্ট করুন", "Photoshop Shortcuts"),
        ("Zoom In", "Ctrl + +", "Zoom in | জুম ইন", "Photoshop Shortcuts"),
        ("Zoom Out", "Ctrl + -", "Zoom out | জুম আউট", "Photoshop Shortcuts"),
        ("Fit to Screen", "Ctrl + 0", "Fit to screen | স্ক্রিনে ফিট করুন", "Photoshop Shortcuts"),
    ]
    
    print(f"📚 Adding {len(shortcuts)} shortcut keys...\n")
    
    added = 0
    for name, keys, description, category in shortcuts:
        try:
            content = f"""
Shortcut: {keys}
Description: {description}
Category: {category}

How to use: Press {keys} to {description.split('|')[0].strip()}
কিভাবে ব্যবহার করবেন: {keys} চাপুন {description.split('|')[1].strip() if '|' in description else ''}
"""
            cursor.execute("""
                INSERT INTO knowledge_base (topic, content, source)
                VALUES (?, ?, ?)
            """, (name, content.strip(), category))
            added += 1
            print(f"  ✅ {name} ({keys})")
        except Exception as e:
            print(f"  ❌ {name} - Error: {e}")
    
    conn.commit()
    
    # Get totals
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    total_knowledge = cursor.fetchone()[0]
    
    conn.close()
    
    print("\n" + "="*80)
    print("  ✅ ALL SHORTCUT KEYS ADDED!")
    print("  ✅ সব শর্টকাট কী যোগ করা হয়েছে!")
    print("="*80)
    
    print(f"\n  📊 Results:")
    print(f"     • Successfully added: {added} shortcuts")
    print(f"     • Total knowledge: {total_knowledge} entries")
    
    print("\n" + "="*80)
    print("  📚 SHORTCUT CATEGORIES:")
    print("="*80)
    print("""
  1️⃣  Windows Shortcuts (13 shortcuts)
      • Win, Win+D, Win+E, Win+L, Win+R, etc.
      
  2️⃣  Common Shortcuts (13 shortcuts)
      • Ctrl+C, Ctrl+V, Ctrl+Z, Ctrl+S, etc.
      
  3️⃣  MS Word Shortcuts (13 shortcuts)
      • Ctrl+B, Ctrl+I, Ctrl+U, F7, etc.
      
  4️⃣  MS Excel Shortcuts (14 shortcuts)
      • Alt+=, Ctrl+1, F2, F4, etc.
      
  5️⃣  MS PowerPoint Shortcuts (11 shortcuts)
      • Ctrl+M, F5, Shift+F5, etc.
      
  6️⃣  Browser Shortcuts (15 shortcuts)
      • Ctrl+T, Ctrl+W, Ctrl+Shift+T, etc.
      
  7️⃣  Text Editor Shortcuts (12 shortcuts)
      • Ctrl+/, Ctrl+D, Alt+Up/Down, etc.
      
  8️⃣  VS Code Shortcuts (10 shortcuts)
      • Ctrl+P, Ctrl+`, F12, etc.
      
  9️⃣  AutoCAD Shortcuts (25 shortcuts)
      • L (Line), C (Circle), M (Move), etc.
      
  🔟 File Explorer Shortcuts (10 shortcuts)
      • Ctrl+Shift+N, F2, Alt+D, etc.
      
  1️⃣1️⃣ Screenshot Shortcuts (3 shortcuts)
      • PrtScn, Alt+PrtScn, Win+Shift+S
      
  1️⃣2️⃣ Photoshop Shortcuts (10 shortcuts)
      • Ctrl+T, Ctrl+J, Ctrl+E, etc.
    """)
    
    print("="*80)
    print("\n  🧪 TEST JARVIS NOW:")
    print("="*80)
    print("""
  Try these commands:
  
  python jarvis_offline_brain.py "What is Ctrl+C?"
  python jarvis_offline_brain.py "How to take screenshot?"
  python jarvis_offline_brain.py "AutoCAD line shortcut"
  python jarvis_offline_brain.py "Excel shortcuts"
  python jarvis_offline_brain.py "VS Code terminal shortcut"
    """)
    
    print("="*80)
    print("  🎉 JARVIS NOW KNOWS ALL SHORTCUT KEYS!")
    print("  🎉 জার্ভিস এখন সব শর্টকাট কী জানে!")
    print("="*80 + "\n")

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
    else:
        add_all_shortcuts()
