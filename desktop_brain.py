import os

class DesktopBrain:
    def __init__(self, brain_module):
        self.brain = brain_module
        self.desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')

    def find_file(self, filename):
        self.brain.speak(f"Searching Desktop for {filename}...")
        matches = []
        for root, dirs, files in os.walk(self.desktop_path):
            if any(filename.lower() in f.lower() for f in files):
                for f in files:
                    if filename.lower() in f.lower():
                        matches.append(os.path.join(root, f))
        
        if matches:
            return f"I found {len(matches)} matching files on your desktop: {matches[0]}"
        return "I couldn't find that file on your desktop."

    def list_recent_files(self):
        files = os.listdir(self.desktop_path)
        # Filter for actual files, not directories
        files = [f for f in files if os.path.isfile(os.path.join(self.desktop_path, f))]
        return f"Your desktop has {len(files)} files. Recent ones include: {', '.join(files[:5])}"
