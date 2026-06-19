from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class BrowserBrain:
    def __init__(self, brain_module):
        self.brain = brain_module
        self.driver = None
        self.ai_platforms = {
            "chatgpt": "https://chatgpt.com",
            "gemini_studio": "https://aistudio.google.com",
            "claude": "https://claude.ai",
            "perplexity": "https://perplexity.ai",
            "midjourney": "https://www.midjourney.com",
            "dalle": "https://openai.com/dall-e-3",
            "elevenlabs": "https://elevenlabs.io",
            "leonardo": "https://leonardo.ai",
            "firefly": "https://firefly.adobe.com",
            "heygen": "https://heygen.com",
            "runway": "https://runwayml.com"
        }

    def _init_driver(self):
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def ask_external_ai(self, platform, query, stay_open=False):
        """Autonomously interact with external AI platforms with robust selectors"""
        if platform not in self.ai_platforms:
            return f"Platform {platform} is not in my database."
            
        url = self.ai_platforms[platform]
        self.brain.speak(f"Navigating to {platform} to communicate with their intelligence...")
        self._init_driver()
        
        try:
            self.driver.get(url)
            time.sleep(5)
            
            # Universal Chat Input Search
            chat_input = None
            input_selectors = [
                "textarea", "div[contenteditable='true']", "input[type='text']",
                "#prompt-textarea", ".ProseMirror", "[placeholder*='message']",
                "[placeholder*='Ask']", "textarea[id*='input']"
            ]
            
            for selector in input_selectors:
                try:
                    chat_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if chat_input: break
                except Exception as e:
                    print(f"⚠️ Error: {e}")
                    continue
                
            if chat_input:
                chat_input.send_keys(query)
                chat_input.send_keys(Keys.ENTER)
                self.brain.speak(f"Message delivered to {platform}. Waiting for neural feedback...")
                
                # Smart Wait for Response
                time.sleep(15) 
                
                # Response Capture Selectors
                response_selectors = [
                    ".markdown", ".prose", "div[data-message-author-role='assistant']",
                    ".message-content", ".ai-response", ".reply-content",
                    "div.text-base", ".ant-typography"
                ]
                
                for res_sel in response_selectors:
                    try:
                        responses = self.driver.find_elements(By.CSS_SELECTOR, res_sel)
                        if responses:
                            last_response = responses[-1].text
                            if len(last_response) > 10:
                                return last_response
                    except Exception as e:
                        print(f"⚠️ Error: {e}")
                        continue
                return "Neural input accepted, but response format is unrecognized."
            return f"Opened {platform}, but input terminal was blocked or missing."
        except Exception as e:
            return f"Neural bridge failed: {e}"

    def ai_to_ai_bridge(self, p1, p2, topic, turns=2):
        """Bridge two AIs to talk to each other"""
        self.brain.speak(f"Initializing Neural Bridge between {p1} and {p2} regarding {topic}.")
        
        current_thought = f"Hey {p1}, what are your thoughts on {topic}?"
        conversation_log = []

        for i in range(turns):
            # Turn for AI 1
            self.brain.speak(f"Consulting {p1}...")
            response1 = self.ask_external_ai(p1, current_thought)
            conversation_log.append(f"{p1.upper()}: {response1}")
            
            # Turn for AI 2
            self.brain.speak(f"Feeding {p1}'s response to {p2}...")
            bridge_prompt = f"{p1} said this about {topic}: '{response1}'. How do you respond or counter this?"
            response2 = self.ask_external_ai(p2, bridge_prompt)
            conversation_log.append(f"{p2.upper()}: {response2}")
            
            current_thought = f"{p2} argued: '{response2}'. Continue the debate."

        full_log = "\n\n".join(conversation_log)
        self.brain.speak("Neural Bridge conversation complete. I have saved the transcript for you.")
        return full_log

    def visit_and_operate(self, url, task_description):
        self.brain.speak(f"Navigating to {url} to perform: {task_description}")
        self._init_driver()
        try:
            self.driver.get(url)
            time.sleep(3) # Wait for initial load
            
            # AI reasoning to find what to do
            # For now, we search for common elements based on task
            if "login" in task_description.lower():
                self.brain.speak("I have identified a login form. Please provide credentials or let me handle the layout.")
            
            if "search" in task_description.lower():
                search_box = self.driver.find_element(By.NAME, "q") # Common for Google/GitHub
                search_box.send_keys(task_description)
                search_box.send_keys(Keys.ENTER)
                self.brain.speak("Search initiated on the page.")
                
            return "Web operation initiated. I am now monitoring the page."
        except Exception as e:
            return f"Web Error: {e}"

    def extract_page_data(self):
        if not self.driver: return "No active browser session."
        text = self.driver.find_element(By.TAG_NAME, "body").text
        self.brain.speak("I have extracted the page content for analysis.")
        return text[:1000] # Return first 1000 chars for AI to process

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.brain.speak("Browser session closed.")
