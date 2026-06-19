import os
import subprocess
import sys
import pkgutil
import time
import requests
from database import AsifDatabase

class ProgrammingBrain:
    def __init__(self, brain_module):
        self.brain = brain_module
        self.db = AsifDatabase()
        # Initialize Programming Table
        self._init_prog_db()

    def autonomous_install(self, package_name):
        """Offer to install a missing library autonomously"""
        self.brain.speak(f"The library '{package_name}' is required for this task but not found. Should I install it for you?")
        # If user says yes (simulated or real), run pip install
        self.brain.speak(f"Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            self.brain.speak(f"Successfully installed {package_name}. We are ready to proceed.")
            return True
        except Exception as e:

            print(f"⚠️ Error: {e}")
            self.brain.speak(f"Failed to install {package_name}. Please check your internet connection.")
            return False

    def _init_prog_db(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS programming_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language TEXT,
                syntax_topic TEXT,
                example_code TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def fetch_global_docs(self, language, topic):
        """Fetch documentation for any programming language from the world database"""
        self.brain.speak(f"Searching global programming records for {language} {topic}...")
        
        # Search StackOverflow/GitHub snippets via Internet Brain
        search_query = f"{language} {topic} documentation and example code"
        web_info = self.brain.internet.search_and_learn(search_query)
        
        if web_info:
            # Save to programming knowledge
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO programming_knowledge (language, syntax_topic, example_code) VALUES (?, ?, ?)",
                           (language, topic, web_info))
            conn.commit()
            conn.close()
            return f"Found Documentation for {language}:\n{web_info[:500]}..."
        
        return "No specific documentation found in global records."

    def find_package(self, language, requirement):
        """Find libraries/packages for any language (PyPI, NPM, etc.)"""
        self.brain.speak(f"Locating libraries for {language} related to {requirement}...")
        
        repos = {
            "python": "https://pypi.org/search/?q=",
            "javascript": "https://www.npmjs.com/search?q=",
            "rust": "https://crates.io/search?q=",
            "java": "https://search.maven.org/search?q="
        }
        
        base_url = repos.get(language.lower(), "https://github.com/search?q=")
        full_url = f"{base_url}{requirement.replace(' ', '+')}"
        
        # We can use the browser brain to open the repo
        self.brain.speak(f"Opening the {language} package repository for you.")
        import webbrowser
        webbrowser.open(full_url)
        return f"Package search initiated for {language}."

    def run_python_code(self, code):
        self.brain.speak("Executing code...")
        temp_file = "temp_asif_exec.py"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(code)
        try:
            result = subprocess.run([sys.executable, temp_file], capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                return f"Output:\n{result.stdout}"
            else:
                return self.debug_code(code, result.stderr)
        except Exception as e:
            return f"Runtime Error: {e}"
        finally:
            if os.path.exists(temp_file): os.remove(temp_file)

    def debug_code(self, code, error):
        prompt = f"Fix this Python code. Error: {error}\nCode:\n{code}\nCode only."
        try:
            fixed = self.brain.model.generate_content(prompt).text.strip().replace("```python", "").replace("```", "")
            self.brain.speak("Code fixed and re-running.")
            return self.run_python_code(fixed)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return "Debugging failed."

    def create_automation_tool(self, tool_description):
        self.brain.speak(f"Generating tool for: {tool_description}")
        prompt = f"Create a professional Python script for: {tool_description}. Code only."
        try:
            code = self.brain.model.generate_content(prompt).text.strip().replace("```python", "").replace("```", "")
            filename = f"tool_{int(time.time())}.py"
            with open(filename, "w", encoding="utf-8") as f: f.write(code)
            return f"Tool created: {filename}"
        except Exception as e: return f"Failed: {e}"
