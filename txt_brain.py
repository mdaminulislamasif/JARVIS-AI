import os

class TxtBrain:
    def __init__(self, brain_module):
        self.brain = brain_module
        self.knowledge_base = {}
        self.target_dirs = [
            os.path.join(os.environ['USERPROFILE'], 'Desktop'),
            os.path.join(os.environ['USERPROFILE'], 'Documents')
        ]

    def learn_all_txt(self):
        self.brain.speak("Learning from all text files in your system...")
        count = 0
        for directory in self.target_dirs:
            if not os.path.exists(directory): continue
            for root, dirs, files in os.walk(directory):
                # Limit depth to avoid massive systems
                if root.count(os.sep) - directory.count(os.sep) > 2: continue
                
                for file in files:
                    if file.endswith(".txt"):
                        path = os.path.join(root, file)
                        try:
                            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                self.knowledge_base[file] = content[:1000] # Store snippet
                                self.brain.db.save_memory(file, content[:1000], "Local File")
                                count += 1
                        except Exception as e:

                            print(f"⚠️ Error: {e}")
                            pass
        self.brain.speak(f"Learning complete. I have ingested knowledge from {count} text files.")

    def search_knowledge(self, query):
        results = []
        for file, content in self.knowledge_base.items():
            if query.lower() in content.lower() or query.lower() in file.lower():
                results.append(f"From {file}: {content[:200]}...")
        
        if results:
            return "\n".join(results[:2])
        return "No local text knowledge found for that query."
