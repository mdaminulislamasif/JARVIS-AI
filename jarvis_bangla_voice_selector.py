"""
JARVIS BANGLA VOICE SELECTOR
============================
Select and test the best Bengali voice for JARVIS

বাংলা ভয়েস select এবং test করুন
"""

import customtkinter as ctk
from tkinter import messagebox
import asyncio
import os
import tempfile
import subprocess

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except Exception as e:

    print(f"⚠️ Error: {e}")
    EDGE_TTS_AVAILABLE = False
    print("⚠️ edge-tts not installed. Install with: pip install edge-tts")


class BanglaVoiceSelector(ctk.CTkToplevel):
    """Bengali voice selector and tester"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("JARVIS - Bengali Voice Selector")
        self.geometry("700x800")
        self.configure(fg_color="#02050A")
        
        # Make it visible
        self.attributes("-topmost", True)
        self.lift()
        self.focus_force()
        
        # Center window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Available Bengali voices
        self.bangla_voices = {
            'bn-BD-NabanitaNeural': {
                'name': 'Nabanita (Female)',
                'country': 'Bangladesh',
                'quality': '⭐⭐⭐⭐⭐',
                'description': 'Clear, natural, best for general use',
                'icon': '👩'
            },
            'bn-BD-PradeepNeural': {
                'name': 'Pradeep (Male)',
                'country': 'Bangladesh',
                'quality': '⭐⭐⭐⭐⭐',
                'description': 'Natural, professional, good clarity',
                'icon': '👨'
            },
            'bn-IN-BashkarNeural': {
                'name': 'Bashkar (Male)',
                'country': 'India',
                'quality': '⭐⭐⭐⭐',
                'description': 'Indian accent, clear pronunciation',
                'icon': '👨'
            },
            'bn-IN-TanishaaNeural': {
                'name': 'Tanishaa (Female)',
                'country': 'India',
                'quality': '⭐⭐⭐⭐',
                'description': 'Indian accent, soft voice',
                'icon': '👩'
            },
        }
        
        self.selected_voice = 'bn-BD-NabanitaNeural'  # Default
        
        self._create_ui()
    
    def _create_ui(self):
        """Create UI"""
        
        # Header
        header = ctk.CTkFrame(self, fg_color="#FF3131", height=100)
        header.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(
            header,
            text="🎤 BENGALI VOICE SELECTOR",
            font=("Courier New", 28, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            header,
            text="বাংলা ভয়েস বেছে নিন এবং test করুন",
            font=("Courier New", 14),
            text_color="#FFFF00"
        ).pack(pady=(0, 15))
        
        # Check if edge-tts is available
        if not EDGE_TTS_AVAILABLE:
            error_frame = ctk.CTkFrame(self, fg_color="#660000", border_width=2, border_color="#FF0000")
            error_frame.pack(fill="x", padx=20, pady=20)
            
            ctk.CTkLabel(
                error_frame,
                text="❌ edge-tts not installed!",
                font=("Courier New", 16, "bold"),
                text_color="#FF0000"
            ).pack(pady=10)
            
            ctk.CTkLabel(
                error_frame,
                text="Install with: pip install edge-tts",
                font=("Courier New", 12),
                text_color="#FFFF00"
            ).pack(pady=5)
            
            return
        
        # Scrollable frame for voices
        voices_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            height=400
        )
        voices_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Voice buttons
        for voice_id, voice_info in self.bangla_voices.items():
            self._create_voice_button(voices_frame, voice_id, voice_info)
        
        # Test text input
        test_frame = ctk.CTkFrame(self, fg_color="#05080F", border_width=2, border_color="#00FF41")
        test_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(
            test_frame,
            text="📝 Test Text (বাংলায় লিখুন):",
            font=("Courier New", 13, "bold"),
            text_color="#00FF41"
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.test_text = ctk.CTkTextbox(
            test_frame,
            height=80,
            font=("Courier New", 12),
            fg_color="#001100",
            text_color="#00FF41",
            border_width=2,
            border_color="#00FF41"
        )
        self.test_text.pack(fill="x", padx=20, pady=(0, 15))
        
        # Default test text
        self.test_text.insert("1.0", "হ্যালো! আমি জার্ভিস। আমি কিভাবে সাহায্য করতে পারি?")
        
        # Test button
        test_btn = ctk.CTkButton(
            self,
            text="🔊 TEST SELECTED VOICE",
            command=self.test_voice,
            fg_color="#00AA00",
            hover_color="#00FF00",
            font=("Courier New", 16, "bold"),
            height=50,
            border_width=2,
            border_color="#00FF00"
        )
        test_btn.pack(fill="x", padx=20, pady=(0, 10))
        
        # Save button
        save_btn = ctk.CTkButton(
            self,
            text="✅ SAVE & APPLY",
            command=self.save_voice,
            fg_color="#0055AA",
            hover_color="#0077FF",
            font=("Courier New", 16, "bold"),
            height=50,
            border_width=2,
            border_color="#0077FF"
        )
        save_btn.pack(fill="x", padx=20, pady=(0, 20))
    
    def _create_voice_button(self, parent, voice_id, voice_info):
        """Create voice selection button"""
        
        # Voice frame
        voice_frame = ctk.CTkFrame(parent, fg_color="#05080F", border_width=2, border_color="#003355")
        voice_frame.pack(fill="x", pady=10)
        
        # Radio button
        radio = ctk.CTkRadioButton(
            voice_frame,
            text="",
            variable=None,
            value=voice_id,
            command=lambda: self.select_voice(voice_id),
            fg_color="#00AA00",
            hover_color="#00FF00"
        )
        radio.pack(side="left", padx=20, pady=20)
        
        # Check if this is selected
        if voice_id == self.selected_voice:
            radio.select()
        
        # Voice info
        info_frame = ctk.CTkFrame(voice_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=10)
        
        # Name
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"{voice_info['icon']} {voice_info['name']}",
            font=("Courier New", 16, "bold"),
            text_color="#00F3FF"
        )
        name_label.pack(anchor="w")
        
        # Country
        country_label = ctk.CTkLabel(
            info_frame,
            text=f"🌍 {voice_info['country']}",
            font=("Courier New", 12),
            text_color="#888888"
        )
        country_label.pack(anchor="w")
        
        # Quality
        quality_label = ctk.CTkLabel(
            info_frame,
            text=f"Quality: {voice_info['quality']}",
            font=("Courier New", 12),
            text_color="#FFD700"
        )
        quality_label.pack(anchor="w")
        
        # Description
        desc_label = ctk.CTkLabel(
            info_frame,
            text=voice_info['description'],
            font=("Courier New", 11),
            text_color="#00FF41"
        )
        desc_label.pack(anchor="w")
    
    def select_voice(self, voice_id):
        """Select a voice"""
        self.selected_voice = voice_id
        print(f"✅ Selected voice: {self.bangla_voices[voice_id]['name']}")
    
    def test_voice(self):
        """Test the selected voice"""
        if not EDGE_TTS_AVAILABLE:
            messagebox.showerror("Error", "edge-tts not installed!")
            return
        
        text = self.test_text.get("1.0", "end-1c").strip()
        
        if not text:
            messagebox.showwarning("Empty Text", "Please enter some Bengali text to test!")
            return
        
        try:
            # Show testing message
            self.bell()
            print(f"🔊 Testing voice: {self.bangla_voices[self.selected_voice]['name']}")
            print(f"📝 Text: {text}")
            
            # Create temp file
            fd, audio_path = tempfile.mkstemp(prefix="jarvis_test_", suffix=".mp3")
            os.close(fd)
            
            # Generate audio
            asyncio.run(self._generate_audio(text, audio_path))
            
            # Play audio
            self._play_audio(audio_path)
            
            # Clean up
            try:
                os.remove(audio_path)
            except Exception as e:

                print(f"⚠️ Error: {e}")
                pass
            
            print("✅ Test complete!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Test failed: {e}")
            print(f"❌ Test error: {e}")
    
    async def _generate_audio(self, text, audio_path):
        """Generate audio file"""
        communicate = edge_tts.Communicate(
            text,
            voice=self.selected_voice,
            rate="-10%",  # Slightly slower
            volume="+10%",  # Louder
            pitch="+0Hz"  # Natural
        )
        await communicate.save(audio_path)
    
    def _play_audio(self, audio_path):
        """Play audio file"""
        ps_script = (
            "Add-Type -AssemblyName PresentationCore; "
            "$player = New-Object System.Windows.Media.MediaPlayer; "
            f"$player.Open([Uri]::new('{audio_path.replace(chr(39), chr(39) + chr(39))}')); "
            "$player.Play(); "
            "while ($player.NaturalDuration.HasTimeSpan -eq $false) { Start-Sleep -Milliseconds 50 }; "
            "Start-Sleep -Milliseconds ([int]$player.NaturalDuration.TimeSpan.TotalMilliseconds + 200); "
            "$player.Close();"
        )
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    
    def save_voice(self):
        """Save selected voice"""
        try:
            # Update voice.py
            voice_file = 'engine/voice.py'
            
            with open(voice_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update default voice
            old_line = 'self.bangla_voice = self.bangla_voices[0]  # Default to first (best)'
            new_line = f'self.bangla_voice = "{self.selected_voice}"  # Selected by user'
            
            if old_line in content:
                content = content.replace(old_line, new_line)
            else:
                # Try alternative pattern
                import re
                content = re.sub(
                    r'self\.bangla_voice = "[^"]*".*',
                    new_line,
                    content
                )
            
            with open(voice_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            voice_name = self.bangla_voices[self.selected_voice]['name']
            
            messagebox.showinfo(
                "Success",
                f"✅ Voice saved!\n\n"
                f"Selected: {voice_name}\n\n"
                f"Restart JARVIS to apply changes."
            )
            
            print(f"✅ Voice saved: {voice_name}")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")
            print(f"❌ Save error: {e}")


def open_bangla_voice_selector(parent=None):
    """Open Bengali voice selector"""
    if parent is None:
        app = ctk.CTk()
        app.withdraw()
        selector = BanglaVoiceSelector(app)
        app.mainloop()
    else:
        selector = BanglaVoiceSelector(parent)
        return selector


# Test
if __name__ == "__main__":
    open_bangla_voice_selector()
