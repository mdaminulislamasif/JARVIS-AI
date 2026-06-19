"""
AUTO FIX - Runs immediately without waiting
Patches JARVIS to work WITHOUT API keys
"""

import os
import shutil
from datetime import datetime

def backup_file(filepath):
    """Create backup of file"""
    if os.path.exists(filepath):
        backup = f"{filepath}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(filepath, backup)
        print(f"✓ Backed up: {os.path.basename(filepath)}")
        return True
    return False

def fix_jarvis_panel():
    """Fix jarvis_panel.py to use offline brain when quota is hit"""
    filepath = "jarvis_panel.py"
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    # Backup first
    backup_file(filepath)
    
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already fixed
    if "AUTO-FIX: Check if quota exceeded" in content:
        print(f"✓ {filepath} already fixed!")
        return True
    
    # Find the section that shows "Neural uplink is offline"
    old_code = '''        else:
            if not self.brain or not self.brain.is_connected:
                reason = getattr(self.brain, "last_error", "No API key configured") if self.brain else "No API key configured"
                if self.prefer_bangla_voice:
                    res = f"নিউরাল আপলিংক অফলাইন আছে: {reason}. Neural Protocols থেকে valid API key add বা activate করুন।"
                else:
                    res = f"Neural uplink is offline: {reason}. Add or activate a valid API key from Neural Protocols."
                self.after(0, lambda: self.log("JARVIS", res))
                save_chat(query, res)
                self.core.set_state("idle")
                if self.face3d:
                    self.face3d.set_state("idle")
                return'''
    
    # New code that uses offline brain as fallback
    new_code = '''        else:
            if not self.brain or not self.brain.is_connected:
                reason = getattr(self.brain, "last_error", "No API key configured") if self.brain else "No API key configured"
                
                # AUTO-FIX: Check if quota exceeded or no API key
                if "RESOURCE_EXHAUSTED" in str(reason) or "429" in str(reason) or "quota" in str(reason).lower() or "No API key" in str(reason):
                    self.after(0, lambda: self.log("SYSTEM", "Switching to OFFLINE BRAIN (No API key needed)..."))
                    
                    # Try offline brain
                    try:
                        from jarvis_offline_brain import OfflineBrain
                        offline_brain = OfflineBrain()
                        result = offline_brain.process_query(query)
                        res = result.get('response', 'Processing...')
                        self.after(0, lambda: self.log("JARVIS", f"[OFFLINE] {res}"))
                        save_chat(query, res)
                        self.core.set_state("idle")
                        if self.face3d:
                            self.face3d.set_state("idle")
                        return
                    except Exception as e:
                        self.after(0, lambda: self.log("WARNING", f"Offline brain error: {e}"))
                
                # Original error message (only if offline brain fails)
                if self.prefer_bangla_voice:
                    res = f"নিউরাল আপলিংক অফলাইন আছে: {reason}. Neural Protocols থেকে valid API key add বা activate করুন।"
                else:
                    res = f"Neural uplink is offline: {reason}. Add or activate a valid API key from Neural Protocols."
                self.after(0, lambda: self.log("JARVIS", res))
                save_chat(query, res)
                self.core.set_state("idle")
                if self.face3d:
                    self.face3d.set_state("idle")
                return'''
    
    # Replace
    if old_code in content:
        content = content.replace(old_code, new_code)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed: {filepath}")
        return True
    else:
        print(f"⚠️  Pattern not found in {filepath}")
        return False

def main():
    """Main fix function"""
    print("\n" + "="*70)
    print("🔧 AUTO-FIXING JARVIS - NO API KEY NEEDED")
    print("="*70)
    print("\nPatching JARVIS to work WITHOUT any API keys...")
    print()
    
    # Fix jarvis_panel.py
    success = fix_jarvis_panel()
    print()
    
    print("="*70)
    if success:
        print("✅ FIX COMPLETE!")
        print("\nWhat changed:")
        print("  ✓ JARVIS now uses offline brain automatically")
        print("  ✓ Works WITHOUT any API keys")
        print("  ✓ No quota errors")
        print("  ✓ No waiting for midnight reset")
        print("\nNow:")
        print("  1. Restart your JARVIS application")
        print("  2. Say 'HELLO' - it will work WITHOUT API key!")
        print("  3. JARVIS uses offline brain automatically")
        print("\nBackup created: jarvis_panel.py.backup_*")
    else:
        print("⚠️  FIX INCOMPLETE")
        print("\nAlternative: Use standalone JARVIS")
        print("  Run: FIX_API_PROBLEM.bat")
        print("  Or: JARVIS.bat")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
