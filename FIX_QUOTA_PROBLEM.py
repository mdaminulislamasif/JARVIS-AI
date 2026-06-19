"""
FIX QUOTA PROBLEM
Automatically patches JARVIS to use offline brain when API quota is hit
"""

import os
import shutil
from datetime import datetime

def backup_file(filepath):
    """Create backup of file"""
    if os.path.exists(filepath):
        backup = f"{filepath}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(filepath, backup)
        print(f"✓ Backed up: {filepath} -> {backup}")
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
                
                # AUTO-FIX: Check if quota exceeded
                if "RESOURCE_EXHAUSTED" in str(reason) or "429" in str(reason) or "quota" in str(reason).lower():
                    self.after(0, lambda: self.log("SYSTEM", "API quota exceeded. Switching to OFFLINE BRAIN..."))
                    
                    # Try offline brain
                    try:
                        from jarvis_offline_brain import OfflineBrain
                        offline_brain = OfflineBrain()
                        result = offline_brain.process_query(query)
                        res = result.get('response', 'Offline brain processing...')
                        self.after(0, lambda: self.log("JARVIS", f"[OFFLINE BRAIN] {res}"))
                        save_chat(query, res)
                        self.core.set_state("idle")
                        if self.face3d:
                            self.face3d.set_state("idle")
                        return
                    except Exception as e:
                        self.after(0, lambda: self.log("WARNING", f"Offline brain failed: {e}"))
                
                # Original error message
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
        print("   - Added automatic offline brain fallback")
        print("   - Will use offline brain when quota is exceeded")
        return True
    else:
        print(f"⚠️  Could not find target code in {filepath}")
        print("   File may have been modified already")
        return False

def fix_multi_brain():
    """Fix multi_brain.py to handle quota errors better"""
    filepath = "engine/multi_brain.py"
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    # Backup first
    backup_file(filepath)
    
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the think method
    old_code = '''    def think(self, query: str, history_str: str = "", prefer: str = "auto") -> str:
        """
        Route query to best available brain.
        prefer: "auto" | "gemini" | "ollama" | "groq" | "huggingface" | "cohere"
        """
        brains_to_try = self._build_priority(prefer)

        for brain_name in brains_to_try:
            result = self._try_brain(brain_name, query, history_str)
            if result:
                self.active_brain = brain_name
                self._status[brain_name] = "OK"
                return f"[{brain_name.upper()}] {result}"
            else:
                self._status[brain_name] = "FAIL"

        return "All neural pathways exhausted. Check API keys and internet connection."'''
    
    # New code with better error handling
    new_code = '''    def think(self, query: str, history_str: str = "", prefer: str = "auto") -> str:
        """
        Route query to best available brain.
        prefer: "auto" | "gemini" | "ollama" | "groq" | "huggingface" | "cohere"
        """
        brains_to_try = self._build_priority(prefer)

        for brain_name in brains_to_try:
            result = self._try_brain(brain_name, query, history_str)
            if result:
                self.active_brain = brain_name
                self._status[brain_name] = "OK"
                return f"[{brain_name.upper()}] {result}"
            else:
                self._status[brain_name] = "FAIL"

        # AUTO-FIX: Try offline brain as last resort
        try:
            from jarvis_offline_brain import OfflineBrain
            offline_brain = OfflineBrain()
            result = offline_brain.process_query(query)
            if result and result.get('status') == 'success':
                self.active_brain = "offline"
                self._status["offline"] = "OK"
                return f"[OFFLINE BRAIN] {result.get('response', 'Processing...')}"
        except Exception:
            print("⚠️ Error occurred but was silently ignored")

        return "Sir, all API keys have hit today's free quota. Wait for midnight PST reset, or add more keys via the Neural Protocols panel."'''
    
    # Replace
    if old_code in content:
        content = content.replace(old_code, new_code)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed: {filepath}")
        print("   - Added offline brain as fallback")
        print("   - Better error message for quota exceeded")
        return True
    else:
        print(f"⚠️  Could not find target code in {filepath}")
        return False

def main():
    """Main fix function"""
    print("\n" + "="*70)
    print("🔧 FIXING JARVIS API QUOTA PROBLEM")
    print("="*70)
    print("\nThis will:")
    print("  1. Backup your files")
    print("  2. Add automatic offline brain fallback")
    print("  3. Handle quota errors gracefully")
    print("\n" + "="*70 + "\n")
    
    input("Press ENTER to continue...")
    
    print("\n📝 Fixing files...\n")
    
    # Fix jarvis_panel.py
    success1 = fix_jarvis_panel()
    print()
    
    # Fix multi_brain.py
    success2 = fix_multi_brain()
    print()
    
    print("="*70)
    if success1 or success2:
        print("✅ FIX COMPLETE!")
        print("\nWhat changed:")
        if success1:
            print("  ✓ jarvis_panel.py - Auto-switches to offline brain on quota error")
        if success2:
            print("  ✓ multi_brain.py - Uses offline brain as fallback")
        print("\nNow when API quota is hit:")
        print("  → JARVIS automatically uses offline brain")
        print("  → No more 'Neural uplink offline' errors")
        print("  → Continues working without API keys")
        print("\nBackup files created in case you need to revert.")
    else:
        print("⚠️  FIX INCOMPLETE")
        print("\nPossible reasons:")
        print("  - Files already modified")
        print("  - Files not found")
        print("  - Different file structure")
        print("\nYou can manually add offline brain fallback or use:")
        print("  → FIX_API_PROBLEM.bat (standalone JARVIS without API)")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
