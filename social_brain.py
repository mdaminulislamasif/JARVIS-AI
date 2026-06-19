import time
import pyautogui

class SocialMediaBrain:
    def __init__(self, brain_module, automation_module):
        self.brain = brain_module
        self.automation = automation_module

    def generate_content(self, platform, topic):
        self.brain.speak(f"Generating optimized content for {platform} about {topic}...")
        prompt = f"Write a highly engaging {platform} post/title about: {topic}. Include relevant hashtags and a call to action. Content only."
        try:
            content = self.brain.model.generate_content(prompt).text.strip()
            return content
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return f"Thinking about {topic} for {platform}..."

    def facebook_poster(self, topic):
        content = self.generate_content("Facebook", topic)
        self.brain.speak("Opening Facebook and preparing to post...")
        
        # Logic: Open browser, go to FB, click post box
        import webbrowser
        webbrowser.open("https://www.facebook.com")
        time.sleep(7) # Wait for load
        
        # This is a simplified GUI automation. Real world would need precise coords or OCR.
        # For now, we use the 'type' and 'press' logic.
        self.brain.speak("Navigating to the post section...")
        pyautogui.press('p') # Shortcut for some FB versions or just search
        time.sleep(2)
        pyautogui.write(content)
        self.brain.speak(f"Content typed: {content[:30]}...")
        self.brain.speak("Post is ready. Would you like me to click 'Post' now?")

    def youtube_manager(self, action, topic):
        if "title" in action:
            self.brain.speak("Generating viral YouTube titles...")
            prompt = f"Create 5 viral, clickbait YouTube titles for a video about: {topic}."
            titles = self.brain.model.generate_content(prompt).text.strip()
            self.brain.speak(f"Here are some ideas: {titles}")
            return titles
        elif "comment" in action:
            self.brain.speak("Writing a professional comment for YouTube...")
            prompt = f"Write a friendly and engaging YouTube comment for a video about: {topic}."
            comment = self.brain.model.generate_content(prompt).text.strip()
            self.brain.speak(f"Comment generated: {comment}")
            # Use GUI to paste
            pyautogui.write(comment)
            return comment
