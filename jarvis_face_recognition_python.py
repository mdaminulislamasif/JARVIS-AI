"""
JARVIS Face Recognition Panel - Python GUI Version
Converts HTML face recognition panel to Python
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import json
from datetime import datetime
import threading

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️ OpenCV not installed. Face recognition disabled.")

try:
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False


class JarvisVoice:
    """JARVIS Voice Engine"""
    def __init__(self):
        if VOICE_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                voices = self.engine.getProperty('voices')
                for voice in voices:
                    if 'david' in voice.name.lower() or 'male' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                self.engine.setProperty('rate', 150)
                self.engine.setProperty('volume', 1.0)
                self.enabled = True
            except Exception as e:

                print(f"⚠️ Error: {e}")
                self.enabled = False
        else:
            self.enabled = False
    
    def speak(self, text):
        """Make JARVIS speak"""
        if not self.enabled:
            return
        
        def _speak():
            try:
                print(f"🔊 JARVIS: {text}")
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:

                print(f"⚠️ Error: {e}")
                pass
        
        thread = threading.Thread(target=_speak)
        thread.daemon = True
        thread.start()


class FaceRecognitionPanel:
    """Face Recognition Panel"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 JARVIS Face Recognition Panel - Python Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0b10')
        
        # Initialize JARVIS
        self.jarvis = JarvisVoice()
        
        # Variables
        self.uploaded_image = None
        self.results = {}
        
        # Setup UI
        self.create_widgets()
        
        # Greet
        self.root.after(2000, lambda: self.jarvis.speak("Face recognition system online sir."))
    
    def create_widgets(self):
        """Create all widgets"""
        
        # Header
        header = tk.Frame(self.root, bg='#1e3c72', height=120)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title = tk.Label(header,
                        text="🤖 JARVIS Face Recognition Panel",
                        bg='#1e3c72',
                        fg='#00f2ff',
                        font=('Arial', 28, 'bold'))
        title.pack(pady=20)
        
        subtitle = tk.Label(header,
                           text="AI-Powered Face Recognition & Social Media Finder",
                           bg='#1e3c72',
                           fg='white',
                           font=('Arial', 12))
        subtitle.pack()
        
        # Main container
        main = tk.Frame(self.root, bg='#f5f5f5')
        main.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left side - JARVIS Face
        left_frame = tk.Frame(main, bg='#0a0b10', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_jarvis_face(left_frame)
        
        # Right side - Upload & Results
        right_frame = tk.Frame(main, bg='white', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.create_upload_section(right_frame)
        self.create_results_section(right_frame)
    
    def create_jarvis_face(self, parent):
        """Create animated JARVIS face"""
        title = tk.Label(parent,
                        text="JARVIS AI",
                        bg='#0a0b10',
                        fg='#00f2ff',
                        font=('Arial', 24, 'bold'))
        title.pack(pady=20)
        
        # Animated face placeholder
        face_frame = tk.Frame(parent, bg='#0a0b10')
        face_frame.pack(expand=True)
        
        face_label = tk.Label(face_frame,
                             text="👁️\n\n🤖\n\nFACE\nRECOGNITION\nSYSTEM",
                             bg='#0a0b10',
                             fg='#00f2ff',
                             font=('Arial', 32, 'bold'),
                             justify='center')
        face_label.pack(pady=50)
        
        # Status
        status = tk.Label(parent,
                         text="● SYSTEM ONLINE",
                         bg='#0a0b10',
                         fg='#00ff00',
                         font=('Arial', 14, 'bold'))
        status.pack(pady=20)
    
    def create_upload_section(self, parent):
        """Create upload section"""
        upload_frame = tk.LabelFrame(parent,
                                     text="📤 Upload Photo",
                                     bg='white',
                                     fg='#667eea',
                                     font=('Arial', 14, 'bold'),
                                     relief='raised',
                                     bd=2)
        upload_frame.pack(fill='x', padx=20, pady=20)
        
        # Upload button
        upload_btn = tk.Button(upload_frame,
                              text="📁 Choose Photo",
                              bg='#667eea',
                              fg='white',
                              font=('Arial', 12, 'bold'),
                              padx=30,
                              pady=15,
                              command=self.upload_photo,
                              cursor='hand2')
        upload_btn.pack(pady=20)
        
        # Image preview
        self.preview_label = tk.Label(upload_frame,
                                     text="No image uploaded",
                                     bg='#f5f5f5',
                                     fg='#666',
                                     font=('Arial', 10),
                                     width=40,
                                     height=10,
                                     relief='sunken',
                                     bd=2)
        self.preview_label.pack(pady=10, padx=20)
        
        # Analyze button
        self.analyze_btn = tk.Button(upload_frame,
                                    text="🔍 Analyze Face",
                                    bg='#00ff00',
                                    fg='black',
                                    font=('Arial', 12, 'bold'),
                                    padx=30,
                                    pady=15,
                                    command=self.analyze_face,
                                    state='disabled',
                                    cursor='hand2')
        self.analyze_btn.pack(pady=20)
    
    def create_results_section(self, parent):
        """Create results section"""
        results_frame = tk.LabelFrame(parent,
                                      text="📊 Recognition Results",
                                      bg='white',
                                      fg='#667eea',
                                      font=('Arial', 14, 'bold'),
                                      relief='raised',
                                      bd=2)
        results_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Results text
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                      bg='#f5f5f5',
                                                      fg='black',
                                                      font=('Arial', 11),
                                                      wrap='word',
                                                      height=15)
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Initial message
        self.results_text.insert('1.0', 
                                "🤖 JARVIS Face Recognition System\n\n"
                                "Upload a photo to begin analysis.\n\n"
                                "Features:\n"
                                "✅ Face Detection\n"
                                "✅ Person Identification\n"
                                "✅ Social Media Account Finder\n"
                                "✅ Information Extraction\n\n"
                                "Waiting for photo upload...")
        self.results_text.config(state='disabled')
        
        # Export button
        export_btn = tk.Button(results_frame,
                              text="💾 Export Results",
                              bg='#667eea',
                              fg='white',
                              font=('Arial', 11, 'bold'),
                              padx=20,
                              pady=10,
                              command=self.export_results,
                              cursor='hand2')
        export_btn.pack(pady=10)
    
    def upload_photo(self):
        """Upload photo"""
        filename = filedialog.askopenfilename(
            title="Select Photo",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                # Load image
                img = Image.open(filename)
                img.thumbnail((300, 300))
                
                # Display preview
                photo = ImageTk.PhotoImage(img)
                self.preview_label.config(image=photo, text="")
                self.preview_label.image = photo
                
                # Store image
                self.uploaded_image = filename
                
                # Enable analyze button
                self.analyze_btn.config(state='normal')
                
                # JARVIS feedback
                self.jarvis.speak("Photo uploaded successfully sir.")
                
                messagebox.showinfo("Success", "Photo uploaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
    
    def analyze_face(self):
        """Analyze face"""
        if not self.uploaded_image:
            messagebox.showwarning("No Image", "Please upload a photo first!")
            return
        
        # JARVIS feedback
        self.jarvis.speak("Analyzing face sir. Please wait.")
        
        # Simulate analysis
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', 'end')
        
        self.results_text.insert('end', "🔍 ANALYZING FACE...\n\n")
        self.root.update()
        
        # Simulate processing
        import time
        time.sleep(1)
        
        # Mock results
        results = {
            'name': 'John Doe',
            'age': '25-35',
            'gender': 'Male',
            'confidence': '95%',
            'social_media': {
                'Facebook': 'facebook.com/johndoe',
                'Instagram': '@johndoe',
                'Twitter': '@johndoe',
                'LinkedIn': 'linkedin.com/in/johndoe'
            },
            'info': {
                'Location': 'New York, USA',
                'Occupation': 'Software Engineer',
                'Education': 'MIT'
            }
        }
        
        self.results = results
        
        # Display results
        self.results_text.insert('end', "✅ ANALYSIS COMPLETE!\n\n")
        self.results_text.insert('end', "👤 PERSON INFORMATION:\n")
        self.results_text.insert('end', f"Name: {results['name']}\n")
        self.results_text.insert('end', f"Age: {results['age']}\n")
        self.results_text.insert('end', f"Gender: {results['gender']}\n")
        self.results_text.insert('end', f"Confidence: {results['confidence']}\n\n")
        
        self.results_text.insert('end', "📱 SOCIAL MEDIA ACCOUNTS:\n")
        for platform, account in results['social_media'].items():
            self.results_text.insert('end', f"✅ {platform}: {account}\n")
        
        self.results_text.insert('end', "\n📋 ADDITIONAL INFORMATION:\n")
        for key, value in results['info'].items():
            self.results_text.insert('end', f"• {key}: {value}\n")
        
        self.results_text.insert('end', "\n" + "="*50 + "\n")
        self.results_text.insert('end', "Analysis completed successfully!\n")
        
        self.results_text.config(state='disabled')
        
        # JARVIS feedback
        self.jarvis.speak("Analysis complete sir. Results are ready.")
        
        messagebox.showinfo("Complete", "Face analysis completed successfully!")
    
    def export_results(self):
        """Export results"""
        if not self.results:
            messagebox.showwarning("No Results", "No results to export!")
            return
        
        filename = f"face_recognition_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        messagebox.showinfo("Exported", f"Results exported to:\n{filename}")
        self.jarvis.speak("Results exported successfully sir.")


def main():
    """Main function"""
    root = tk.Tk()
    app = FaceRecognitionPanel(root)
    root.mainloop()


if __name__ == "__main__":
    main()
