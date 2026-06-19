"""
JARVIS ADVANCED VOICE CONTROL PANEL
====================================
Advanced voice control features with buttons and settings

Features:
- Voice speed control (slider)
- Voice selection (male/female)
- Volume control
- Voice test
- Bengali/English toggle
- Voice effects
- Save voice settings
"""

import customtkinter as ctk
import json
import os
from tkinter import messagebox

class VoiceControlPanel:
    """Advanced Voice Control Panel for JARVIS"""
    
    def __init__(self, parent, voice_engine, speak_callback):
        self.parent = parent
        self.voice_engine = voice_engine
        self.speak_callback = speak_callback
        self.window = None
        self.settings_file = "jarvis_voice_settings.json"
        
        # Load saved settings
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load voice settings from file"""
        default_settings = {
            'speed': 170,
            'volume': 1.0,
            'voice_type': 'auto',  # auto, male, female
            'prefer_bangla': False,
            'voice_effects': False,
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    saved = json.load(f)
                    default_settings.update(saved)
        except Exception as e:
            print(f"⚠️ Could not load voice settings: {e}")
        
        return default_settings
    
    def save_settings(self):
        """Save voice settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            print("✅ Voice settings saved!")
            return True
        except Exception as e:
            print(f"⚠️ Could not save voice settings: {e}")
            return False
    
    def apply_settings(self):
        """Apply settings to voice engine and parent GUI state"""
        try:
            if self.voice_engine:
                # Apply speed
                self.voice_engine.rate = self.settings['speed']
                print(f"✅ Voice speed set to: {self.settings['speed']}")
                
                # Apply voice type (male/female/auto)
                if hasattr(self.voice_engine, 'set_voice_type'):
                    self.voice_engine.set_voice_type(self.settings['voice_type'])
                else:
                    voice_type = self.settings['voice_type']
                    if voice_type == "male":
                        self.voice_engine.bangla_voice = "bn-BD-PradeepNeural"
                        self.voice_engine.english_voice = "en-US-GuyNeural"
                    else:
                        self.voice_engine.bangla_voice = "bn-BD-NabanitaNeural"
                        self.voice_engine.english_voice = "en-US-JennyNeural"
                    self.voice_engine.preferred_voice = None
                    print(f"✅ Voice type fallback applied: {voice_type}")
                
                # Propagate prefer_bangla to parent
                if self.parent and hasattr(self.parent, 'prefer_bangla_voice'):
                    self.parent.prefer_bangla_voice = self.settings['prefer_bangla']
                    print(f"✅ Parent prefer_bangla_voice updated: {self.settings['prefer_bangla']}")
                
                return True
        except Exception as e:
            print(f"⚠️ Could not apply settings: {e}")
            return False
    
    def open_panel(self):
        """Open the voice control panel"""
        if self.window and self.window.winfo_exists():
            self.window.focus()
            return
        
        # Create window
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("🎤 JARVIS Voice Control")
        self.window.geometry("500x700")
        self.window.resizable(False, False)
        
        # Make it stay on top
        self.window.attributes('-topmost', True)
        
        # Header
        header = ctk.CTkFrame(self.window, fg_color="#05080F", height=80)
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header,
            text="🎤 VOICE CONTROL",
            font=("Courier New", 24, "bold"),
            text_color="#00F3FF"
        ).pack(pady=20)
        
        # Main content
        content = ctk.CTkScrollableFrame(self.window, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # === VOICE SPEED SECTION ===
        speed_section = ctk.CTkFrame(content, fg_color="#05080F", border_width=1, border_color="#002233")
        speed_section.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            speed_section,
            text="🎚️ VOICE SPEED",
            font=("Courier New", 16, "bold"),
            text_color="#00FF41"
        ).pack(pady=(10, 5))
        
        self.speed_label = ctk.CTkLabel(
            speed_section,
            text=f"Current: {self.settings['speed']} (Natural: 170)",
            font=("Courier New", 12),
            text_color="#AAAAAA"
        )
        self.speed_label.pack(pady=5)
        
        self.speed_slider = ctk.CTkSlider(
            speed_section,
            from_=100,
            to=250,
            number_of_steps=150,
            command=self.on_speed_change
        )
        self.speed_slider.set(self.settings['speed'])
        self.speed_slider.pack(pady=10, padx=20, fill="x")
        
        speed_presets = ctk.CTkFrame(speed_section, fg_color="transparent")
        speed_presets.pack(pady=5)
        
        ctk.CTkButton(
            speed_presets,
            text="Slow (150)",
            width=80,
            height=30,
            fg_color="#003344",
            hover_color="#005566",
            command=lambda: self.set_speed(150)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            speed_presets,
            text="Normal (170)",
            width=80,
            height=30,
            fg_color="#004466",
            hover_color="#006688",
            command=lambda: self.set_speed(170)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            speed_presets,
            text="Fast (200)",
            width=80,
            height=30,
            fg_color="#003344",
            hover_color="#005566",
            command=lambda: self.set_speed(200)
        ).pack(side="left", padx=5)
        
        # === VOLUME SECTION ===
        volume_section = ctk.CTkFrame(content, fg_color="#05080F", border_width=1, border_color="#002233")
        volume_section.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            volume_section,
            text="🔊 VOLUME",
            font=("Courier New", 16, "bold"),
            text_color="#00FF41"
        ).pack(pady=(10, 5))
        
        self.volume_label = ctk.CTkLabel(
            volume_section,
            text=f"Current: {int(self.settings['volume'] * 100)}%",
            font=("Courier New", 12),
            text_color="#AAAAAA"
        )
        self.volume_label.pack(pady=5)
        
        self.volume_slider = ctk.CTkSlider(
            volume_section,
            from_=0.0,
            to=1.0,
            number_of_steps=100,
            command=self.on_volume_change
        )
        self.volume_slider.set(self.settings['volume'])
        self.volume_slider.pack(pady=10, padx=20, fill="x")
        
        # === VOICE TYPE SECTION ===
        voice_type_section = ctk.CTkFrame(content, fg_color="#05080F", border_width=1, border_color="#002233")
        voice_type_section.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            voice_type_section,
            text="🎭 VOICE TYPE",
            font=("Courier New", 16, "bold"),
            text_color="#00FF41"
        ).pack(pady=(10, 5))
        
        self.voice_type_var = ctk.StringVar(value=self.settings['voice_type'])
        
        voice_options = ctk.CTkFrame(voice_type_section, fg_color="transparent")
        voice_options.pack(pady=10)
        
        ctk.CTkRadioButton(
            voice_options,
            text="Auto (Best Available)",
            variable=self.voice_type_var,
            value="auto",
            command=self.on_voice_type_change
        ).pack(pady=5)
        
        ctk.CTkRadioButton(
            voice_options,
            text="Male Voice (David)",
            variable=self.voice_type_var,
            value="male",
            command=self.on_voice_type_change
        ).pack(pady=5)
        
        ctk.CTkRadioButton(
            voice_options,
            text="Female Voice (Zira)",
            variable=self.voice_type_var,
            value="female",
            command=self.on_voice_type_change
        ).pack(pady=5)
        
        # === LANGUAGE SECTION ===
        language_section = ctk.CTkFrame(content, fg_color="#05080F", border_width=1, border_color="#002233")
        language_section.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            language_section,
            text="🌐 LANGUAGE",
            font=("Courier New", 16, "bold"),
            text_color="#00FF41"
        ).pack(pady=(10, 5))
        
        self.bangla_switch = ctk.CTkSwitch(
            language_section,
            text="Prefer Bengali Voice (বাংলা)",
            command=self.on_bangla_toggle
        )
        if self.settings['prefer_bangla']:
            self.bangla_switch.select()
        self.bangla_switch.pack(pady=10)
        
        # === TEST SECTION ===
        test_section = ctk.CTkFrame(content, fg_color="#05080F", border_width=1, border_color="#002233")
        test_section.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            test_section,
            text="🎤 TEST VOICE",
            font=("Courier New", 16, "bold"),
            text_color="#00FF41"
        ).pack(pady=(10, 5))
        
        test_buttons = ctk.CTkFrame(test_section, fg_color="transparent")
        test_buttons.pack(pady=10)
        
        ctk.CTkButton(
            test_buttons,
            text="Test English",
            width=120,
            height=40,
            fg_color="#004466",
            hover_color="#006688",
            command=lambda: self.test_voice("Hello! I am JARVIS. How do I sound?")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            test_buttons,
            text="Test Bengali",
            width=120,
            height=40,
            fg_color="#004466",
            hover_color="#006688",
            command=lambda: self.test_voice("নমস্কার! আমি JARVIS। আমার voice কেমন লাগছে?")
        ).pack(side="left", padx=5)
        
        # === ACTION BUTTONS ===
        action_section = ctk.CTkFrame(content, fg_color="transparent")
        action_section.pack(fill="x", pady=20)
        
        ctk.CTkButton(
            action_section,
            text="💾 SAVE SETTINGS",
            width=200,
            height=50,
            fg_color="#006644",
            hover_color="#008866",
            font=("Courier New", 14, "bold"),
            command=self.save_and_apply
        ).pack(pady=5)
        
        ctk.CTkButton(
            action_section,
            text="🔄 RESET TO DEFAULT",
            width=200,
            height=40,
            fg_color="#664400",
            hover_color="#886600",
            command=self.reset_to_default
        ).pack(pady=5)
        
        ctk.CTkButton(
            action_section,
            text="❌ CLOSE",
            width=200,
            height=40,
            fg_color="#660000",
            hover_color="#880000",
            command=self.window.destroy
        ).pack(pady=5)
        
        # Info label
        ctk.CTkLabel(
            content,
            text="💡 Tip: Natural voice speed is 170. Lower is slower, higher is faster.",
            font=("Courier New", 10),
            text_color="#555555",
            wraplength=400
        ).pack(pady=10)
    
    def on_speed_change(self, value):
        """Handle speed slider change"""
        speed = int(value)
        self.settings['speed'] = speed
        self.speed_label.configure(text=f"Current: {speed} (Natural: 170)")
    
    def set_speed(self, speed):
        """Set speed to preset value"""
        self.settings['speed'] = speed
        self.speed_slider.set(speed)
        self.speed_label.configure(text=f"Current: {speed} (Natural: 170)")
    
    def on_volume_change(self, value):
        """Handle volume slider change"""
        self.settings['volume'] = value
        self.volume_label.configure(text=f"Current: {int(value * 100)}%")
    
    def on_voice_type_change(self):
        """Handle voice type change"""
        self.settings['voice_type'] = self.voice_type_var.get()
        print(f"✅ Voice type changed to: {self.settings['voice_type']}")
    
    def on_bangla_toggle(self):
        """Handle Bengali toggle"""
        self.settings['prefer_bangla'] = self.bangla_switch.get()
        print(f"✅ Prefer Bengali: {self.settings['prefer_bangla']}")
    
    def test_voice(self, text):
        """Test voice with current settings"""
        try:
            # Apply current settings
            self.apply_settings()
            
            # Speak test text
            if self.speak_callback:
                self.speak_callback(text)
            
            print(f"🎤 Testing voice: {text[:50]}...")
        except Exception as e:
            print(f"⚠️ Voice test error: {e}")
            messagebox.showerror("Voice Test Error", f"Could not test voice: {e}")
    
    def save_and_apply(self):
        """Save and apply settings"""
        try:
            # Apply to voice engine
            if self.apply_settings():
                # Save to file
                if self.save_settings():
                    messagebox.showinfo(
                        "Settings Saved",
                        "✅ Voice settings saved and applied successfully!"
                    )
                    print("✅ Voice settings saved and applied!")
                else:
                    messagebox.showwarning(
                        "Save Warning",
                        "⚠️ Settings applied but could not save to file."
                    )
            else:
                messagebox.showerror(
                    "Apply Error",
                    "❌ Could not apply settings to voice engine."
                )
        except Exception as e:
            print(f"⚠️ Save and apply error: {e}")
            messagebox.showerror("Error", f"Error: {e}")
    
    def reset_to_default(self):
        """Reset settings to default"""
        try:
            # Reset settings
            self.settings = {
                'speed': 170,
                'volume': 1.0,
                'voice_type': 'auto',
                'prefer_bangla': False,
                'voice_effects': False,
            }
            
            # Update UI
            self.speed_slider.set(170)
            self.speed_label.configure(text="Current: 170 (Natural: 170)")
            self.volume_slider.set(1.0)
            self.volume_label.configure(text="Current: 100%")
            self.voice_type_var.set('auto')
            if self.settings['prefer_bangla']:
                self.bangla_switch.select()
            else:
                self.bangla_switch.deselect()
            
            # Apply and save
            self.apply_settings()
            self.save_settings()
            
            messagebox.showinfo(
                "Reset Complete",
                "✅ Voice settings reset to default!"
            )
            print("✅ Voice settings reset to default!")
        except Exception as e:
            print(f"⚠️ Reset error: {e}")
            messagebox.showerror("Reset Error", f"Error: {e}")


# Helper function to open voice control panel
def open_voice_control_panel(parent, voice_engine, speak_callback):
    """Open the voice control panel"""
    try:
        panel = VoiceControlPanel(parent, voice_engine, speak_callback)
        panel.open_panel()
        return panel
    except Exception as e:
        print(f"⚠️ Could not open voice control panel: {e}")
        return None


# Test function
if __name__ == "__main__":
    print("="*60)
    print("🎤 VOICE CONTROL PANEL TEST")
    print("="*60)
    print("\n✅ Voice Control Panel module loaded successfully!")
    print("💡 Use open_voice_control_panel() to open the panel")
    print("\nFeatures:")
    print("  - Voice speed control (100-250)")
    print("  - Volume control (0-100%)")
    print("  - Voice type selection (Auto/Male/Female)")
    print("  - Bengali/English toggle")
    print("  - Voice test buttons")
    print("  - Save/Load settings")
    print("\n" + "="*60)
