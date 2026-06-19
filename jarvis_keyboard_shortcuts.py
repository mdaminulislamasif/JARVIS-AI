"""
JARVIS KEYBOARD SHORTCUTS
All Functions Accessible via Keyboard

This module provides keyboard shortcuts for all JARVIS functions.
এই module সব JARVIS functions এর জন্য keyboard shortcuts প্রদান করে।

Features:
- Global hotkeys
- Function key shortcuts (F1-F12)
- Ctrl/Alt/Shift combinations
- Custom key bindings
- Shortcut help menu
"""

import keyboard
import threading
import time
from typing import Dict, Callable, Optional


class KeyboardShortcuts:
    """Keyboard shortcuts manager for JARVIS"""
    
    def __init__(self, callback: Optional[Callable] = None):
        self.callback = callback
        self.shortcuts = {}
        self.is_active = False
        self.listener_thread = None
        
        # Initialize default shortcuts
        self._init_default_shortcuts()
    
    def _init_default_shortcuts(self):
        """Initialize default keyboard shortcuts"""
        
        # Function Keys (F1-F12)
        self.shortcuts = {
            # F1-F4: Core Functions
            'f1': {'command': 'help', 'description': 'Show Help'},
            'f2': {'command': 'screenshot', 'description': 'Take Screenshot'},
            'f3': {'command': 'search', 'description': 'Web Search'},
            'f4': {'command': 'translate', 'description': 'Translate'},
            
            # F5-F8: System Functions
            'f5': {'command': 'clean', 'description': 'System Clean'},
            'f6': {'command': 'disk', 'description': 'Disk Info'},
            'f7': {'command': 'memory', 'description': 'Memory Info'},
            'f8': {'command': 'processes', 'description': 'Show Processes'},
            
            # F9-F12: Network & Security
            'f9': {'command': 'recon', 'description': 'Network Scan'},
            'f10': {'command': 'wifi', 'description': 'WiFi Scan'},
            'f11': {'command': 'firewall', 'description': 'Firewall'},
            'f12': {'command': 'monitor', 'description': 'System Monitor'},
            
            # Ctrl + Key Combinations
            'ctrl+n': {'command': 'network scan', 'description': 'Network Scan'},
            'ctrl+w': {'command': 'wifi scan', 'description': 'WiFi Scan'},
            'ctrl+s': {'command': 'screenshot', 'description': 'Screenshot'},
            'ctrl+c': {'command': 'clean', 'description': 'System Clean'},
            'ctrl+d': {'command': 'disk', 'description': 'Disk Info'},
            'ctrl+m': {'command': 'memory', 'description': 'Memory Info'},
            'ctrl+p': {'command': 'processes', 'description': 'Processes'},
            'ctrl+l': {'command': 'lock', 'description': 'Lock Computer'},
            'ctrl+t': {'command': 'translate', 'description': 'Translate'},
            'ctrl+g': {'command': 'generate', 'description': 'AI Generate'},
            
            # Alt + Key Combinations
            'alt+n': {'command': 'notepad', 'description': 'Open Notepad'},
            'alt+b': {'command': 'browser', 'description': 'Open Browser'},
            'alt+c': {'command': 'calculator', 'description': 'Calculator'},
            'alt+e': {'command': 'explorer', 'description': 'File Explorer'},
            'alt+t': {'command': 'task manager', 'description': 'Task Manager'},
            'alt+v': {'command': 'volume', 'description': 'Volume Control'},
            'alt+s': {'command': 'settings', 'description': 'System Settings'},
            
            # Ctrl + Shift + Key Combinations
            'ctrl+shift+l': {'command': 'learn', 'description': 'Auto Learn'},
            'ctrl+shift+s': {'command': 'search learn', 'description': 'Search & Learn'},
            'ctrl+shift+a': {'command': 'article learn', 'description': 'Learn Article'},
            'ctrl+shift+t': {'command': 'translate', 'description': 'Translate'},
            'ctrl+shift+g': {'command': 'gen image', 'description': 'Generate Image'},
            'ctrl+shift+v': {'command': 'gen video', 'description': 'Generate Video'},
            'ctrl+shift+m': {'command': 'gen audio', 'description': 'Generate Audio'},
            
            # Ctrl + Alt + Key Combinations
            'ctrl+alt+k': {'command': 'kali', 'description': 'Kali Mode'},
            'ctrl+alt+f': {'command': 'flipper', 'description': 'Flipper Mode'},
            'ctrl+alt+a': {'command': 'alien', 'description': 'Alien Mode'},
            'ctrl+alt+p': {'command': 'purge', 'description': 'Virus Purge'},
            'ctrl+alt+r': {'command': 'remote', 'description': 'Remote Console'},
            'ctrl+alt+s': {'command': 'share', 'description': 'Screen Share'},
            
            # Special Combinations
            'ctrl+alt+del': {'command': 'task manager', 'description': 'Task Manager'},
            'win+l': {'command': 'lock', 'description': 'Lock Computer'},
            'win+e': {'command': 'explorer', 'description': 'File Explorer'},
            'win+r': {'command': 'run', 'description': 'Run Dialog'},
        }
    
    def add_shortcut(self, key: str, command: str, description: str = ""):
        """Add custom shortcut"""
        self.shortcuts[key.lower()] = {
            'command': command,
            'description': description or command
        }
        print(f"✅ Shortcut added: {key} → {command}")
    
    def remove_shortcut(self, key: str):
        """Remove shortcut"""
        key = key.lower()
        if key in self.shortcuts:
            del self.shortcuts[key]
            print(f"✅ Shortcut removed: {key}")
            return True
        return False
    
    def get_shortcut(self, key: str) -> Optional[Dict]:
        """Get shortcut info"""
        return self.shortcuts.get(key.lower())
    
    def get_all_shortcuts(self) -> Dict:
        """Get all shortcuts"""
        return self.shortcuts.copy()
    
    def start(self):
        """Start listening for keyboard shortcuts"""
        if self.is_active:
            print("⚠️ Shortcuts already active")
            return
        
        self.is_active = True
        
        # Register all shortcuts
        for key, info in self.shortcuts.items():
            try:
                keyboard.add_hotkey(key, self._on_shortcut, args=(key,))
            except Exception as e:
                print(f"⚠️ Could not register {key}: {e}")
        
        print("✅ Keyboard shortcuts activated")
        print("💡 Press Ctrl+H for help")
    
    def stop(self):
        """Stop listening for keyboard shortcuts"""
        if not self.is_active:
            return
        
        self.is_active = False
        
        # Unregister all shortcuts
        try:
            keyboard.unhook_all()
            print("✅ Keyboard shortcuts deactivated")
        except Exception as e:
            print(f"⚠️ Error stopping shortcuts: {e}")
    
    def _on_shortcut(self, key: str):
        """Handle shortcut press"""
        if not self.is_active:
            return
        
        shortcut = self.shortcuts.get(key)
        if shortcut:
            command = shortcut['command']
            print(f"⌨️ Shortcut pressed: {key} → {command}")
            
            # Call callback if set
            if self.callback:
                try:
                    self.callback(command)
                except Exception as e:
                    print(f"❌ Callback error: {e}")
    
    def show_help(self):
        """Show shortcuts help"""
        print("\n" + "=" * 60)
        print("⌨️ JARVIS KEYBOARD SHORTCUTS")
        print("=" * 60)
        
        # Group by category
        categories = {
            'Function Keys (F1-F12)': [],
            'Ctrl + Key': [],
            'Alt + Key': [],
            'Ctrl + Shift + Key': [],
            'Ctrl + Alt + Key': [],
            'Special': []
        }
        
        for key, info in sorted(self.shortcuts.items()):
            desc = f"{key.upper():20} → {info['description']}"
            
            if key.startswith('f') and len(key) <= 3:
                categories['Function Keys (F1-F12)'].append(desc)
            elif key.startswith('ctrl+shift+'):
                categories['Ctrl + Shift + Key'].append(desc)
            elif key.startswith('ctrl+alt+'):
                categories['Ctrl + Alt + Key'].append(desc)
            elif key.startswith('ctrl+'):
                categories['Ctrl + Key'].append(desc)
            elif key.startswith('alt+'):
                categories['Alt + Key'].append(desc)
            else:
                categories['Special'].append(desc)
        
        # Print categories
        for category, shortcuts in categories.items():
            if shortcuts:
                print(f"\n📌 {category}:")
                for shortcut in shortcuts:
                    print(f"   {shortcut}")
        
        print("\n" + "=" * 60)
        print("💡 Tip: Press Ctrl+H anytime to show this help")
        print("=" * 60 + "\n")
    
    def export_shortcuts(self, filename: str = "jarvis_shortcuts.txt"):
        """Export shortcuts to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("JARVIS KEYBOARD SHORTCUTS\n")
                f.write("=" * 60 + "\n\n")
                
                for key, info in sorted(self.shortcuts.items()):
                    f.write(f"{key.upper():20} → {info['description']}\n")
                    f.write(f"{'':20}   Command: {info['command']}\n\n")
            
            print(f"✅ Shortcuts exported to: {filename}")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def import_shortcuts(self, filename: str):
        """Import shortcuts from file"""
        try:
            import json
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for key, info in data.items():
                self.add_shortcut(key, info['command'], info.get('description', ''))
            
            print(f"✅ Shortcuts imported from: {filename}")
            return True
        except Exception as e:
            print(f"❌ Import failed: {e}")
            return False


# Integration with JARVIS Panel
def integrate_with_panel(panel):
    """Integrate keyboard shortcuts with JARVIS panel"""
    
    def on_shortcut(command):
        """Handle shortcut command"""
        panel.process(command)
    
    # Create shortcuts manager
    shortcuts = KeyboardShortcuts(callback=on_shortcut)
    
    # Add help shortcut
    shortcuts.add_shortcut('ctrl+h', 'help', 'Show Shortcuts Help')
    
    # Start listening
    shortcuts.start()
    
    return shortcuts


# Test function
def test_keyboard_shortcuts():
    """Test keyboard shortcuts"""
    print("=" * 60)
    print("JARVIS KEYBOARD SHORTCUTS TEST")
    print("=" * 60)
    
    def on_command(command):
        print(f"✅ Command executed: {command}")
    
    # Create shortcuts
    shortcuts = KeyboardShortcuts(callback=on_command)
    
    # Show help
    shortcuts.show_help()
    
    # Start listening
    print("\n🧪 Starting keyboard listener...")
    print("💡 Press any shortcut to test")
    print("💡 Press Ctrl+C to stop\n")
    
    shortcuts.start()
    
    try:
        # Keep running
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping...")
        shortcuts.stop()
    
    print("\n" + "=" * 60)
    print("✅ Test complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_keyboard_shortcuts()
