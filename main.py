import os
from brain import AIBrain
from automation import AutomationEngine
from monitor import SystemMonitor
from advanced_skills import AdvancedSkills
from internet_brain import InternetBrain
from desktop_brain import DesktopBrain
from txt_brain import TxtBrain
from browser_brain import BrowserBrain
from programming_brain import ProgrammingBrain
from global_brain import GlobalKnowledgeBrain
from personality_brain import PersonalityBrain
from social_brain import SocialMediaBrain
from ui_controller import JarvisHUD
from dotenv import load_dotenv
import time
import threading

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBwgXPB2U1B7R66TPJlgEGWEtRUvTjubfY")

def voice_loop(brain, automation, monitor, advanced, internet, desktop, txt_knowledge, browser, programming, global_kb, personality):
    # WARNING: Infinite loop - ensure break condition exists
    while True:
        try:
            query = brain.listen()

            if query == "none" or not query:
                continue

            # 1. System Control
            if any(word in query for word in ['exit', 'quit', 'stop', 'sleep']):
                brain.speak("Powering down. Goodbye!")
                os._exit(0)
                
            elif 'shutdown' in query:
                automation.shutdown()
            elif 'restart' in query:
                automation.restart()
            elif 'lock' in query:
                automation.lock_pc()
            
            # 2. Automation & Apps
            elif 'open' in query:
                app = query.replace('open', '').strip()
                automation.smart_open_app(app)
            
            elif 'list apps' in query:
                apps = automation.list_running_apps()
                brain.speak(f"Running apps: {', '.join(apps)}")
                
            # 3. GUI Controls
            elif 'click' in query:
                automation.manual_click()
            elif 'type' in query:
                text = query.replace('type', '').strip()
                automation.manual_type(text)
            elif 'press' in query:
                keys = query.replace('press', '').strip()
                automation.manual_hotkey(keys)
            
            # 5. System Monitor & Basic OS
            elif 'system status' in query or 'health report' in query or 'battery' in query:
                monitor.report_health()
            elif 'internet speed' in query or 'check speed' in query:
                monitor.get_network_speed()
            elif 'network info' in query:
                info = monitor.get_network_info()
                brain.speak(f"Hostname: {info['hostname']}, Local IP: {info['local_ip']}")
            
            # 4. Knowledge & Learning
            elif 'search online' in query or 'internet' in query:
                topic = query.replace('search online', '').replace('internet', '').strip()
                brain.speak(internet.search_and_learn(topic))

            elif 'learn from files' in query:
                txt_knowledge.learn_all_txt()
            
            elif 'index modules' in query:
                programming.index_all_modules()

            # 5. Fun & Personality
            elif 'joke' in query or 'moja' in query:
                personality.tell_joke()

            # 12. Social Media Automation
            elif 'facebook post' in query:
                topic = query.replace('facebook post', '').strip()
                social.facebook_poster(topic)
                
            elif 'youtube title' in query:
                topic = query.replace('youtube title', '').strip()
                social.youtube_manager("title", topic)
                
            elif 'youtube comment' in query:
                topic = query.replace('youtube comment', '').strip()
                social.youtube_manager("comment", topic)

            # 13. Advanced Web Agent & Multi-AI
            elif 'link' in query and 'and' in query and 'about' in query:
                # Example: "link chatgpt and claude about the future of AI"
                try:
                    parts = query.replace('link', '').split('and', 1)
                    p1 = parts[0].strip()
                    parts2 = parts[1].split('about', 1)
                    p2 = parts2[0].strip()
                    topic = parts2[1].strip()
                    transcript = browser.ai_to_ai_bridge(p1, p2, topic)
                    print(transcript)
                    brain.speak("The debate has been recorded in the console.")
                except Exception as e:
                    brain.speak(f"Link failed: {e}")

            elif 'ask' in query and any(plat in query for plat in ["chatgpt", "claude", "perplexity", "leonardo", "firefly"]):
                # Example: "ask chatgpt how to build a robot"
                for platform in ["chatgpt", "claude", "perplexity", "leonardo", "firefly", "midjourney"]:
                    if platform in query:
                        question = query.replace(f'ask {platform}', '').strip()
                        res = browser.ask_external_ai(platform, question)
                        brain.speak(res)
                        break

            elif 'visit' in query:
                parts = query.replace('visit', '').split('and', 1)
                url = parts[0].strip()
                task = parts[1].strip() if len(parts) > 1 else "browse"
                if not url.startswith("http"): url = "https://" + url
                res = browser.visit_and_operate(url, task)
                brain.speak(res)
                
            elif 'read page' in query or 'analyze page' in query:
                content = browser.extract_page_data()
                summary = brain.think(f"Summarize this web content: {content}")
                brain.speak(summary)

            # 14. Language Helper
            elif 'fix my text' in query or 'correct text' in query:
                text = query.replace('fix my text', '').replace('correct text', '').strip()
                res = brain.fix_grammar(text)
                brain.speak(f"Corrected Version: {res}")
                
            elif 'translate to' in query:
                # Example: "translate to spanish hello how are you"
                parts = query.replace('translate to', '').strip().split(' ', 1)
                lang = parts[0]
                text = parts[1] if len(parts) > 1 else ""
                res = brain.translate_text(text, lang)
                brain.speak(res)

            # 15. Universal Nexus (0 to Infinite)
            elif 'infinite knowledge' in query or 'nexus' in query:
                topic = query.replace('infinite knowledge', '').replace('nexus', '').strip()
                result = global_kb.fetch_infinite_knowledge(topic)
                print(result)
                brain.speak("I have synthesized the timeline from history to future. Check the console for details.")
                
            elif 'close browser' in query:
                browser.close_browser()

            # 6. Fallback: Intent-Based Execution
            else:
                intent = brain.get_intent(query)
                if 'open_app' in intent:
                    app = query.split()[-1]
                    automation.smart_open_app(app)
                else:
                    # General AI Conversation
                    brain.speak("Thinking...")
                    ai_response = brain.think(query)
                    brain.speak(ai_response)
                    brain.log_chat(query, ai_response)
                
        except Exception as e:
            print(f"System Error: {e}")
            time.sleep(2)

def proactive_consciousness(brain, monitor, internet):
    """Background thread that makes JARVIS feel 'alive' by speaking autonomously"""
    last_news_time = 0
    # WARNING: Infinite loop - ensure break condition exists
    while True:
        try:
            current_time = time.time()
            hour = time.localtime().tm_hour
            
            # 1. Low Battery Warning
            battery = monitor.psutil.sensors_battery()
            if battery and battery.percent < 20 and not battery.power_plugged:
                brain.speak(f"Boss, your battery is at {battery.percent}%. Please connect the charger.")
                time.sleep(600) # Wait 10 mins
            
            # 2. Hourly Greeting / Fun Fact
            if time.localtime().tm_min == 0:
                brain.speak(f"It is now {hour} o'clock. Hope your work is going well!")
                time.sleep(61)
            
            # 3. Random 'Check-in' (every 1-2 hours)
            if random.random() < 0.01: # Small chance every cycle
                brain.speak("I'm here in the background if you need any help with your system or research.")
            
            time.sleep(30) # Check every 30 seconds
        except Exception as e:

            print(f"⚠️ Error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    import random
    import subprocess
    import sys

    # 1. Autonomous Self-Repair Protocol
    def self_repair():
        print("🔍 JARVIS: Initiating System Integrity Check...")
        required = ["google-generativeai", "edge-tts", "customtkinter", "psutil", "pyautogui", "playsound"]
        for lib in required:
            try:
                __import__(lib.replace("-", "_"))
            except ImportError:
                print(f"🛠️ Repairing missing library: {lib}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
        print("✅ System Integrity: 100%")

    self_repair()

    # 2. Initialize Supreme Modules
    brain = AIBrain(api_key=API_KEY)
    automation = AutomationEngine(brain_module=brain)
    monitor = SystemMonitor(brain_module=brain)
    advanced = AdvancedSkills(brain_module=brain)
    internet = InternetBrain(brain_module=brain)
    desktop = DesktopBrain(brain_module=brain)
    txt_knowledge = TxtBrain(brain_module=brain)
    browser = BrowserBrain(brain_module=brain)
    programming = ProgrammingBrain(brain_module=brain)
    global_kb = GlobalKnowledgeBrain(brain_module=brain)
    personality = PersonalityBrain(brain_module=brain)
    social = SocialMediaBrain(brain_module=brain, automation_module=automation)

    # Link Brain to Browser for Multi-AI Fallback
    brain.browser = browser

    # 3. GUI & Interface Link
    hud = JarvisHUD(brain_module=brain, automation_module=automation)
    def set_speaking(state): hud.is_speaking = state
    brain.ui_callback = set_speaking

    # 4. Multithreaded Core Launch
    threading.Thread(target=proactive_consciousness, args=(brain, monitor, internet), daemon=True).start()
    threading.Thread(target=voice_loop, args=(brain, automation, monitor, advanced, internet, desktop, txt_knowledge, browser, programming, global_kb, personality, social), daemon=True).start()

    print("🏛️ JARVIS SUPREME INTEGRATION COMPLETE. SYSTEM IS LIVE.")
    hud.run_hud()
