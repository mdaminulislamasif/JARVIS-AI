"""
JARVIS CHROME DEVTOOLS AUTOMATION
Uses Chrome Developer Tools for advanced learning

Features:
- Opens Chrome with DevTools (Ctrl+Shift+I)
- Uses Chrome DevTools Protocol
- Executes JavaScript in browser
- Advanced web scraping
- Network monitoring
- Console access
- Element inspection
"""

import os
import sys
import time
import json
import subprocess
import pyautogui
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChromeDevTools:
    """Chrome DevTools automation for advanced learning"""
    
    def __init__(self):
        self.driver = None
        self.chrome_path = self._find_chrome()
        self.devtools_open = False
        
        print("🔧 JARVIS CHROME DEVTOOLS INITIALIZED!")
        print("🔧 JARVIS Chrome DevTools চালু হয়েছে!")
        
    def _find_chrome(self):
        """Find Chrome executable"""
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                print(f"✅ Found Chrome: {path}")
                return path
        
        print("⚠️ Chrome not found")
        return None
    
    def start_chrome_with_devtools(self, url="https://www.google.com"):
        """Start Chrome with DevTools enabled"""
        try:
            print(f"\n🚀 Starting Chrome with DevTools...")
            print(f"🚀 DevTools সহ Chrome শুরু করছি...")
            
            # Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Start Chrome
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.get(url)
            
            print("✅ Chrome started!")
            
            # Open DevTools with Ctrl+Shift+I
            time.sleep(2)
            self._open_devtools()
            
            return True
            
        except Exception as e:
            print(f"❌ Chrome start error: {e}")
            return False
    
    def _open_devtools(self):
        """Open DevTools using Ctrl+Shift+I"""
        try:
            print("🔧 Opening DevTools (Ctrl+Shift+I)...")
            
            # Send Ctrl+Shift+I to open DevTools
            pyautogui.hotkey('ctrl', 'shift', 'i')
            time.sleep(1)
            
            self.devtools_open = True
            print("✅ DevTools opened!")
            
        except Exception as e:
            print(f"⚠️ DevTools open error: {e}")
    
    def execute_javascript(self, script):
        """Execute JavaScript in browser console"""
        try:
            if not self.driver:
                print("❌ Chrome not started")
                return None
            
            print(f"⚡ Executing JavaScript...")
            result = self.driver.execute_script(script)
            print(f"✅ JavaScript executed!")
            return result
            
        except Exception as e:
            print(f"❌ JavaScript error: {e}")
            return None
    
    def get_page_content(self):
        """Get full page content using DevTools"""
        try:
            if not self.driver:
                print("❌ Chrome not started")
                return None
            
            print("📄 Getting page content...")
            
            # Get page HTML
            html = self.driver.page_source
            
            # Get page text
            text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Get page title
            title = self.driver.title
            
            print(f"✅ Got page content: {len(text)} characters")
            
            return {
                'title': title,
                'html': html,
                'text': text,
                'url': self.driver.current_url
            }
            
        except Exception as e:
            print(f"❌ Content error: {e}")
            return None
    
    def search_and_learn(self, topic):
        """Search Google and learn using DevTools"""
        try:
            print(f"\n🔍 SEARCHING AND LEARNING: {topic}")
            print(f"🔍 খুঁজছি এবং শিখছি: {topic}")
            
            # Start Chrome with Google
            if not self.driver:
                self.start_chrome_with_devtools("https://www.google.com")
            else:
                self.driver.get("https://www.google.com")
            
            time.sleep(2)
            
            # Find search box and search
            search_box = self.driver.find_element(By.NAME, "q")
            search_box.send_keys(topic)
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(3)
            
            # Get search results using JavaScript
            results_script = """
            let results = [];
            let searchResults = document.querySelectorAll('div.g');
            searchResults.forEach(function(result) {
                let title = result.querySelector('h3');
                let snippet = result.querySelector('.VwiC3b');
                if (title && snippet) {
                    results.push({
                        title: title.innerText,
                        snippet: snippet.innerText
                    });
                }
            });
            return results;
            """
            
            results = self.execute_javascript(results_script)
            
            if results:
                print(f"✅ Found {len(results)} search results!")
                
                # Compile learned content
                learned_content = f"Search results for '{topic}':\n\n"
                for i, result in enumerate(results[:5], 1):
                    learned_content += f"{i}. {result['title']}\n"
                    learned_content += f"   {result['snippet']}\n\n"
                
                return {
                    'status': 'success',
                    'response': f"""✅ LEARNED FROM GOOGLE USING DEVTOOLS!
✅ DevTools ব্যবহার করে Google থেকে শিখেছি!

📊 Learning Summary:
   • Topic: {topic}
   • Results Found: {len(results)}
   • DevTools: ACTIVE
   • Method: Ctrl+Shift+I + JavaScript

Content:
{learned_content[:500]}...

All knowledge extracted using Chrome DevTools!
সব জ্ঞান Chrome DevTools ব্যবহার করে extract করা হয়েছে!""",
                    'type': 'devtools_learning',
                    'results': results
                }
            else:
                return {
                    'status': 'error',
                    'response': f"❌ No results found for '{topic}'",
                    'type': 'devtools_learning'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'response': f"❌ Search error: {e}",
                'type': 'devtools_learning'
            }
    
    def inspect_element(self, selector):
        """Inspect element using DevTools"""
        try:
            if not self.driver:
                print("❌ Chrome not started")
                return None
            
            print(f"🔍 Inspecting element: {selector}")
            
            # Find element
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            
            # Get element properties using JavaScript
            script = f"""
            let element = document.querySelector('{selector}');
            return {{
                tagName: element.tagName,
                id: element.id,
                className: element.className,
                innerHTML: element.innerHTML.substring(0, 200),
                textContent: element.textContent.substring(0, 200)
            }};
            """
            
            properties = self.execute_javascript(script)
            
            print(f"✅ Element inspected!")
            return properties
            
        except Exception as e:
            print(f"❌ Inspect error: {e}")
            return None
    
    def monitor_network(self):
        """Monitor network requests using DevTools"""
        try:
            if not self.driver:
                print("❌ Chrome not started")
                return None
            
            print("📡 Monitoring network...")
            
            # Enable network monitoring
            script = """
            performance.getEntriesByType('resource').map(function(entry) {
                return {
                    name: entry.name,
                    type: entry.initiatorType,
                    duration: entry.duration
                };
            });
            """
            
            network_data = self.execute_javascript(script)
            
            print(f"✅ Network monitored: {len(network_data)} requests")
            return network_data
            
        except Exception as e:
            print(f"❌ Network monitor error: {e}")
            return None
    
    def get_console_logs(self):
        """Get console logs from DevTools"""
        try:
            if not self.driver:
                print("❌ Chrome not started")
                return None
            
            print("📋 Getting console logs...")
            
            # Get console logs
            logs = self.driver.get_log('browser')
            
            print(f"✅ Got {len(logs)} console logs")
            return logs
            
        except Exception as e:
            print(f"❌ Console logs error: {e}")
            return None
    
    def take_screenshot(self, filename="devtools_screenshot.png"):
        """Take screenshot with DevTools open"""
        try:
            if not self.driver:
                print("❌ Chrome not started")
                return False
            
            print(f"📸 Taking screenshot...")
            
            self.driver.save_screenshot(filename)
            
            print(f"✅ Screenshot saved: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            return False
    
    def learn_with_devtools(self, topic):
        """Learn about a topic using Chrome DevTools - wrapper for search_and_learn"""
        return self.search_and_learn(topic)
    
    def close(self):
        """Close Chrome and DevTools"""
        try:
            if self.driver:
                print("🔒 Closing Chrome...")
                self.driver.quit()
                self.driver = None
                self.devtools_open = False
                print("✅ Chrome closed!")
        except Exception as e:
            print(f"⚠️ Close error: {e}")


def main():
    """Main function"""
    print("\n" + "=" * 80)
    print("  🔧 JARVIS CHROME DEVTOOLS")
    print("  🔧 JARVIS Chrome DevTools")
    print("  Advanced learning with Developer Tools!")
    print("  Developer Tools দিয়ে উন্নত শেখা!")
    print("=" * 80)
    
    devtools = ChromeDevTools()
    
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        
        if command.startswith('learn '):
            topic = command.replace('learn ', '')
            result = devtools.search_and_learn(topic)
            print(f"\n{result['response']}")
            
            input("\nPress Enter to close Chrome...")
            devtools.close()
    
    else:
        print("\nCommands:")
        print("  learn <topic>  - Search and learn using DevTools")
        print("  exit           - Exit")
        
        # Start Chrome
        devtools.start_chrome_with_devtools()
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("🤖 JARVIS: Closing Chrome...")
                    devtools.close()
                    break
                
                if user_input.startswith('learn '):
                    topic = user_input.replace('learn ', '')
                    result = devtools.search_and_learn(topic)
                    print(f"\n🤖 JARVIS: {result['response']}")
                
                elif user_input == 'screenshot':
                    devtools.take_screenshot()
                    print("🤖 JARVIS: Screenshot saved!")
                
                elif user_input == 'network':
                    network = devtools.monitor_network()
                    print(f"🤖 JARVIS: {len(network)} network requests")
                
                elif user_input == 'console':
                    logs = devtools.get_console_logs()
                    print(f"🤖 JARVIS: {len(logs)} console logs")
                
                else:
                    print("\n🤖 JARVIS: Unknown command. Try 'learn <topic>', 'screenshot', 'network', or 'console'")
            
            except KeyboardInterrupt:
                print("\n\n🤖 JARVIS: Interrupted. Closing Chrome...")
                devtools.close()
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        devtools.close()


if __name__ == "__main__":
    main()
