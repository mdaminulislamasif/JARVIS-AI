"""
JARVIS PROGRAMMING MASTER
Knows ALL programming languages
Teaches, writes code, explains, and helps learn any language
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import sqlite3
from datetime import datetime

class JarvisProgrammingMaster:
    def __init__(self):
        print("🤖 Initializing JARVIS Programming Master...")
        
        # Speech
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        
        # Database
        self.db = "jarvis_programming.db"
        self.init_database()
        
        # All programming languages
        self.languages = {
            # Popular Languages
            'python': {
                'name': 'Python',
                'type': 'Popular',
                'description': 'High-level, interpreted, general-purpose programming language',
                'uses': 'Web development, AI/ML, Data Science, Automation',
                'hello_world': 'print("Hello, World!")',
                'file_ext': '.py'
            },
            'javascript': {
                'name': 'JavaScript',
                'type': 'Popular',
                'description': 'High-level, interpreted scripting language for web',
                'uses': 'Web development, Frontend, Backend (Node.js)',
                'hello_world': 'console.log("Hello, World!");',
                'file_ext': '.js'
            },
            'java': {
                'name': 'Java',
                'type': 'Popular',
                'description': 'Object-oriented, class-based programming language',
                'uses': 'Enterprise applications, Android development',
                'hello_world': 'public class Main { public static void main(String[] args) { System.out.println("Hello, World!"); } }',
                'file_ext': '.java'
            },
            'csharp': {
                'name': 'C#',
                'type': 'Popular',
                'description': 'Modern, object-oriented programming language by Microsoft',
                'uses': 'Windows applications, Game development (Unity), Web',
                'hello_world': 'using System; class Program { static void Main() { Console.WriteLine("Hello, World!"); } }',
                'file_ext': '.cs'
            },
            'cpp': {
                'name': 'C++',
                'type': 'Popular',
                'description': 'General-purpose programming language with low-level memory manipulation',
                'uses': 'System software, Game engines, Performance-critical applications',
                'hello_world': '#include <iostream>\nint main() { std::cout << "Hello, World!"; return 0; }',
                'file_ext': '.cpp'
            },
            'typescript': {
                'name': 'TypeScript',
                'type': 'Popular',
                'description': 'Typed superset of JavaScript',
                'uses': 'Large-scale web applications, Frontend frameworks',
                'hello_world': 'console.log("Hello, World!");',
                'file_ext': '.ts'
            },
            'go': {
                'name': 'Go',
                'type': 'Popular',
                'description': 'Statically typed, compiled language by Google',
                'uses': 'Cloud services, Microservices, System programming',
                'hello_world': 'package main\nimport "fmt"\nfunc main() { fmt.Println("Hello, World!") }',
                'file_ext': '.go'
            },
            'rust': {
                'name': 'Rust',
                'type': 'Popular',
                'description': 'Systems programming language focused on safety and performance',
                'uses': 'System programming, WebAssembly, Embedded systems',
                'hello_world': 'fn main() { println!("Hello, World!"); }',
                'file_ext': '.rs'
            },
            'swift': {
                'name': 'Swift',
                'type': 'Popular',
                'description': 'Powerful programming language for iOS and macOS',
                'uses': 'iOS/macOS app development',
                'hello_world': 'print("Hello, World!")',
                'file_ext': '.swift'
            },
            'kotlin': {
                'name': 'Kotlin',
                'type': 'Popular',
                'description': 'Modern programming language for JVM and Android',
                'uses': 'Android development, Server-side applications',
                'hello_world': 'fun main() { println("Hello, World!") }',
                'file_ext': '.kt'
            },
            'php': {
                'name': 'PHP',
                'type': 'Popular',
                'description': 'Server-side scripting language for web development',
                'uses': 'Web development, Server-side scripting',
                'hello_world': '<?php echo "Hello, World!"; ?>',
                'file_ext': '.php'
            },
            'ruby': {
                'name': 'Ruby',
                'type': 'Popular',
                'description': 'Dynamic, object-oriented programming language',
                'uses': 'Web development (Rails), Scripting',
                'hello_world': 'puts "Hello, World!"',
                'file_ext': '.rb'
            },
            'sql': {
                'name': 'SQL',
                'type': 'Popular',
                'description': 'Domain-specific language for managing databases',
                'uses': 'Database queries, Data manipulation',
                'hello_world': 'SELECT "Hello, World!";',
                'file_ext': '.sql'
            },
            'r': {
                'name': 'R',
                'type': 'Popular',
                'description': 'Programming language for statistical computing',
                'uses': 'Data analysis, Statistical computing, Graphics',
                'hello_world': 'print("Hello, World!")',
                'file_ext': '.r'
            },
            'c': {
                'name': 'C',
                'type': 'Popular',
                'description': 'General-purpose, procedural programming language',
                'uses': 'System programming, Embedded systems, Operating systems',
                'hello_world': '#include <stdio.h>\nint main() { printf("Hello, World!"); return 0; }',
                'file_ext': '.c'
            },
            
            # Windows Specific
            'visualbasic': {
                'name': 'Visual Basic .NET',
                'type': 'Windows',
                'description': 'Object-oriented programming language for .NET',
                'uses': 'Windows applications, .NET development',
                'hello_world': 'Module Program\n    Sub Main()\n        Console.WriteLine("Hello, World!")\n    End Sub\nEnd Module',
                'file_ext': '.vb'
            },
            'powershell': {
                'name': 'PowerShell',
                'type': 'Windows',
                'description': 'Task automation and configuration management framework',
                'uses': 'Windows automation, System administration',
                'hello_world': 'Write-Host "Hello, World!"',
                'file_ext': '.ps1'
            },
            'fsharp': {
                'name': 'F#',
                'type': 'Windows',
                'description': 'Functional-first programming language for .NET',
                'uses': 'Data science, Financial computing, .NET development',
                'hello_world': 'printfn "Hello, World!"',
                'file_ext': '.fs'
            },
            'assembly': {
                'name': 'Assembly',
                'type': 'Windows',
                'description': 'Low-level programming language for x86/x64',
                'uses': 'System programming, Reverse engineering, Optimization',
                'hello_world': 'section .data\n    msg db "Hello, World!", 0\nsection .text\n    global _start\n_start:\n    mov eax, 4\n    mov ebx, 1\n    mov ecx, msg\n    mov edx, 13\n    int 0x80',
                'file_ext': '.asm'
            },
            
            # Classic & Niche
            'cobol': {
                'name': 'COBOL',
                'type': 'Classic',
                'description': 'Business-oriented programming language',
                'uses': 'Banking systems, Legacy enterprise applications',
                'hello_world': 'IDENTIFICATION DIVISION.\nPROGRAM-ID. HELLO.\nPROCEDURE DIVISION.\n    DISPLAY "Hello, World!".\n    STOP RUN.',
                'file_ext': '.cob'
            },
            'fortran': {
                'name': 'Fortran',
                'type': 'Classic',
                'description': 'General-purpose programming language for scientific computing',
                'uses': 'Scientific computing, Numerical analysis',
                'hello_world': 'program hello\n    print *, "Hello, World!"\nend program hello',
                'file_ext': '.f90'
            },
            'pascal': {
                'name': 'Pascal',
                'type': 'Classic',
                'description': 'Procedural programming language for teaching',
                'uses': 'Education, System programming',
                'hello_world': 'program Hello;\nbegin\n    writeln("Hello, World!");\nend.',
                'file_ext': '.pas'
            },
            'perl': {
                'name': 'Perl',
                'type': 'Classic',
                'description': 'High-level, general-purpose programming language',
                'uses': 'Text processing, System administration, Web development',
                'hello_world': 'print "Hello, World!\\n";',
                'file_ext': '.pl'
            },
            'lisp': {
                'name': 'Lisp',
                'type': 'Classic',
                'description': 'Family of programming languages with fully parenthesized prefix notation',
                'uses': 'AI research, Symbolic computation',
                'hello_world': '(print "Hello, World!")',
                'file_ext': '.lisp'
            },
            'haskell': {
                'name': 'Haskell',
                'type': 'Niche',
                'description': 'Purely functional programming language',
                'uses': 'Academic research, Financial systems',
                'hello_world': 'main = putStrLn "Hello, World!"',
                'file_ext': '.hs'
            },
            'ada': {
                'name': 'Ada',
                'type': 'Classic',
                'description': 'Structured, statically typed programming language',
                'uses': 'Embedded systems, Real-time systems, Aviation',
                'hello_world': 'with Ada.Text_IO; use Ada.Text_IO;\nprocedure Hello is\nbegin\n    Put_Line("Hello, World!");\nend Hello;',
                'file_ext': '.adb'
            },
            'scala': {
                'name': 'Scala',
                'type': 'Niche',
                'description': 'General-purpose programming language combining OOP and functional',
                'uses': 'Big data processing, Web applications',
                'hello_world': 'object Hello extends App { println("Hello, World!") }',
                'file_ext': '.scala'
            },
            'dart': {
                'name': 'Dart',
                'type': 'Niche',
                'description': 'Client-optimized language for mobile and web apps',
                'uses': 'Flutter development, Web applications',
                'hello_world': 'void main() { print("Hello, World!"); }',
                'file_ext': '.dart'
            },
            'objectivec': {
                'name': 'Objective-C',
                'type': 'Niche',
                'description': 'Object-oriented language for Apple platforms',
                'uses': 'iOS/macOS development (legacy)',
                'hello_world': '#import <Foundation/Foundation.h>\nint main() { NSLog(@"Hello, World!"); return 0; }',
                'file_ext': '.m'
            }
        }
        
        print("✅ JARVIS Programming Master Ready!")
        print(f"📚 Knows {len(self.languages)} programming languages!")
        
    def init_database(self):
        """Initialize database"""
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_progress (
                language TEXT PRIMARY KEY,
                level TEXT,
                last_studied TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS code_examples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language TEXT,
                code TEXT,
                description TEXT,
                created_at TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def speak(self, text):
        """Speak text"""
        print(f"\n🤖 JARVIS: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
    
    def list_all_languages(self):
        """List all programming languages"""
        print("\n" + "="*70)
        print("📚 PROGRAMMING LANGUAGES JARVIS KNOWS")
        print("="*70)
        
        # Group by type
        types = {}
        for key, lang in self.languages.items():
            lang_type = lang['type']
            if lang_type not in types:
                types[lang_type] = []
            types[lang_type].append(lang['name'])
        
        for lang_type, langs in types.items():
            print(f"\n{lang_type} Languages ({len(langs)}):")
            for lang in sorted(langs):
                print(f"  • {lang}")
        
        print(f"\n{'='*70}")
        print(f"Total: {len(self.languages)} languages")
        print("="*70 + "\n")
        
        self.speak(f"I know {len(self.languages)} programming languages across all categories!")
    
    def teach_language(self, language_key):
        """Teach a programming language"""
        if language_key not in self.languages:
            self.speak(f"I don't have information about {language_key} yet.")
            return
        
        lang = self.languages[language_key]
        
        print("\n" + "="*70)
        print(f"📖 LEARNING: {lang['name']}")
        print("="*70)
        
        self.speak(f"Let me teach you about {lang['name']}")
        
        print(f"\nType: {lang['type']}")
        print(f"Description: {lang['description']}")
        print(f"Common Uses: {lang['uses']}")
        print(f"File Extension: {lang['file_ext']}")
        
        print(f"\n💡 Hello World Example:")
        print("-" * 70)
        print(lang['hello_world'])
        print("-" * 70)
        
        self.speak(f"{lang['name']} is used for {lang['uses']}")
        
        # Save progress
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO learning_progress (language, level, last_studied)
            VALUES (?, 'beginner', ?)
        ''', (lang['name'], datetime.now()))
        conn.commit()
        conn.close()
        
        # Open documentation
        self.speak("Would you like me to open online documentation?")
        search_url = f"https://www.google.com/search?q={lang['name']}+programming+tutorial"
        webbrowser.open(search_url)
    
    def write_code(self, language_key, description):
        """Write code in specified language"""
        if language_key not in self.languages:
            self.speak(f"I don't know {language_key} yet.")
            return
        
        lang = self.languages[language_key]
        
        self.speak(f"Let me write {lang['name']} code for you")
        
        # Create code file
        filename = f"jarvis_code_{language_key}{lang['file_ext']}"
        
        code_template = f"""
# {lang['name']} Code
# Generated by JARVIS Programming Master
# Description: {description}

{lang['hello_world']}

# Add your code here
"""
        
        with open(filename, 'w') as f:
            f.write(code_template)
        
        print(f"\n✅ Created: {filename}")
        self.speak(f"I've created a {lang['name']} file for you")
        
        # Save to database
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO code_examples (language, code, description, created_at)
            VALUES (?, ?, ?, ?)
        ''', (lang['name'], code_template, description, datetime.now()))
        conn.commit()
        conn.close()
        
        # Open in notepad
        os.system(f'notepad {filename}')
    
    def compare_languages(self, lang1_key, lang2_key):
        """Compare two programming languages"""
        if lang1_key not in self.languages or lang2_key not in self.languages:
            self.speak("One or both languages not found")
            return
        
        lang1 = self.languages[lang1_key]
        lang2 = self.languages[lang2_key]
        
        print("\n" + "="*70)
        print(f"⚖️  COMPARING: {lang1['name']} vs {lang2['name']}")
        print("="*70)
        
        print(f"\n{lang1['name']}:")
        print(f"  Type: {lang1['type']}")
        print(f"  Uses: {lang1['uses']}")
        print(f"  Hello World: {lang1['hello_world'][:50]}...")
        
        print(f"\n{lang2['name']}:")
        print(f"  Type: {lang2['type']}")
        print(f"  Uses: {lang2['uses']}")
        print(f"  Hello World: {lang2['hello_world'][:50]}...")
        
        print("\n" + "="*70)
        
        self.speak(f"Comparing {lang1['name']} and {lang2['name']}")
    
    def show_learning_progress(self):
        """Show learning progress"""
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('SELECT language, level, last_studied FROM learning_progress ORDER BY last_studied DESC')
        results = cursor.fetchall()
        conn.close()
        
        if results:
            print("\n" + "="*70)
            print("📊 YOUR LEARNING PROGRESS")
            print("="*70)
            
            for lang, level, last_studied in results:
                print(f"\n{lang}:")
                print(f"  Level: {level}")
                print(f"  Last Studied: {last_studied}")
            
            print("\n" + "="*70)
            self.speak(f"You've studied {len(results)} languages so far!")
        else:
            self.speak("You haven't started learning any languages yet!")
    
    def run_interactive(self):
        """Run interactive mode"""
        print("\n" + "="*70)
        print("🤖 JARVIS PROGRAMMING MASTER")
        print("="*70)
        print("\nCommands:")
        print("  list                  - List all languages")
        print("  learn [language]      - Learn a language")
        print("  write [language]      - Write code in language")
        print("  compare [lang1] [lang2] - Compare languages")
        print("  progress              - Show learning progress")
        print("  exit                  - Exit")
        print("="*70 + "\n")
        
        self.speak("Programming Master activated! How can I help you learn programming?")
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            try:
                command = input("\n💻 Command> ").strip().lower()
                
                if not command:
                    continue
                
                if command == 'exit':
                    self.speak("Happy coding!")
                    break
                
                elif command == 'list':
                    self.list_all_languages()
                
                elif command.startswith('learn '):
                    lang = command.split('learn ')[1].strip()
                    self.teach_language(lang)
                
                elif command.startswith('write '):
                    lang = command.split('write ')[1].strip()
                    desc = input("Description: ").strip()
                    self.write_code(lang, desc)
                
                elif command.startswith('compare '):
                    parts = command.split('compare ')[1].split()
                    if len(parts) >= 2:
                        self.compare_languages(parts[0], parts[1])
                
                elif command == 'progress':
                    self.show_learning_progress()
                
                else:
                    print("❌ Unknown command. Type 'list' to see all languages.")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Main function"""
    jarvis = JarvisProgrammingMaster()
    jarvis.run_interactive()


if __name__ == "__main__":
    main()
