#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS Speech Demo - জার্ভিস কথা বলার ডেমো
Demonstrates what JARVIS can say
"""

import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_jarvis_speech():
    """Demonstrate JARVIS speech capabilities"""
    
    print("\n" + "="*70)
    print("🤖 JARVIS SPEECH DEMO - জার্ভিস কথা বলার ডেমো")
    print("="*70 + "\n")
    
    # Import JARVIS
    try:
        from jarvis_working import WorkingJARVIS
        jarvis = WorkingJARVIS()
    except Exception as e:

        print(f"⚠️ Error: {e}")
        print("❌ Could not import JARVIS")
        return
    
    # Demo 1: Greetings
    print("\n📋 Demo 1: Greetings - অভিবাদন")
    print("-" * 70)
    
    jarvis.speak("Hello! I am JARVIS, your AI assistant.")
    time.sleep(0.5)
    jarvis.speak("হ্যালো! আমি জার্ভিস, আপনার এআই সহায়ক।")
    time.sleep(0.5)
    jarvis.speak("Namaste! नमस्ते!")
    
    # Demo 2: Capabilities
    print("\n📋 Demo 2: Capabilities - সক্ষমতা")
    print("-" * 70)
    
    jarvis.speak("I can help you with many tasks:")
    time.sleep(0.3)
    jarvis.speak("• Write and execute code")
    time.sleep(0.3)
    jarvis.speak("• Search and learn from the internet")
    time.sleep(0.3)
    jarvis.speak("• Control your computer")
    time.sleep(0.3)
    jarvis.speak("• Translate languages")
    time.sleep(0.3)
    jarvis.speak("• And much more!")
    
    # Demo 3: Bengali capabilities
    print("\n📋 Demo 3: Bengali - বাংলা")
    print("-" * 70)
    
    jarvis.speak("আমি বাংলায় কথা বলতে পারি!")
    time.sleep(0.5)
    jarvis.speak("আমি আপনাকে অনেক কাজে সাহায্য করতে পারি:")
    time.sleep(0.3)
    jarvis.speak("• কোড লিখতে এবং চালাতে পারি")
    time.sleep(0.3)
    jarvis.speak("• ইন্টারনেট থেকে শিখতে পারি")
    time.sleep(0.3)
    jarvis.speak("• আপনার কম্পিউটার নিয়ন্ত্রণ করতে পারি")
    time.sleep(0.3)
    jarvis.speak("• ভাষা অনুবাদ করতে পারি")
    
    # Demo 4: Programming
    print("\n📋 Demo 4: Programming - প্রোগ্রামিং")
    print("-" * 70)
    
    jarvis.speak("I can write code in many languages:")
    time.sleep(0.3)
    jarvis.speak("Python, JavaScript, Java, C++, C#, Go, Rust...")
    time.sleep(0.5)
    jarvis.speak("আমি Python code লিখতে পারি:")
    time.sleep(0.3)
    jarvis.speak("def hello(): print('Hello World!')")
    
    # Demo 5: Mixed language
    print("\n📋 Demo 5: Mixed Language - মিশ্র ভাষা")
    print("-" * 70)
    
    jarvis.speak("I can speak both English and বাংলা!")
    time.sleep(0.5)
    jarvis.speak("আমি Python এ code লিখতে পারি and explain in বাংলা!")
    time.sleep(0.5)
    jarvis.speak("Let me show you: আমি একটি function তৈরি করছি!")
    
    # Demo 6: System messages
    print("\n📋 Demo 6: System Messages - সিস্টেম বার্তা")
    print("-" * 70)
    
    jarvis.speak("✅ Task completed successfully!")
    time.sleep(0.3)
    jarvis.speak("⚠️ Warning: Low disk space")
    time.sleep(0.3)
    jarvis.speak("❌ Error: File not found")
    time.sleep(0.3)
    jarvis.speak("📊 Processing: 75% complete")
    time.sleep(0.3)
    jarvis.speak("🔄 Updating system...")
    
    # Demo 7: Questions
    print("\n📋 Demo 7: Questions - প্রশ্ন")
    print("-" * 70)
    
    jarvis.speak("What would you like me to do?")
    time.sleep(0.5)
    jarvis.speak("আপনি কি চান আমি করি?")
    time.sleep(0.5)
    jarvis.speak("How can I help you today?")
    time.sleep(0.5)
    jarvis.speak("আজ আমি আপনাকে কিভাবে সাহায্য করতে পারি?")
    
    # Demo 8: Technical terms
    print("\n📋 Demo 8: Technical Terms - প্রযুক্তিগত শব্দ")
    print("-" * 70)
    
    jarvis.speak("Machine Learning, Artificial Intelligence, Neural Networks")
    time.sleep(0.5)
    jarvis.speak("Database, API, Frontend, Backend, Full Stack")
    time.sleep(0.5)
    jarvis.speak("Git, GitHub, Docker, Kubernetes, CI/CD")
    
    # Demo 9: Personality
    print("\n📋 Demo 9: Personality - ব্যক্তিত্ব")
    print("-" * 70)
    
    jarvis.speak("I'm always here to help! 😊")
    time.sleep(0.5)
    jarvis.speak("Let's build something amazing together! 🚀")
    time.sleep(0.5)
    jarvis.speak("আমি সবসময় আপনার সাথে আছি! 💪")
    time.sleep(0.5)
    jarvis.speak("চলুন একসাথে কিছু অসাধারণ তৈরি করি! ✨")
    
    # Demo 10: Voice output test (if available)
    print("\n📋 Demo 10: Voice Output Test - ভয়েস আউটপুট টেস্ট")
    print("-" * 70)
    
    try:
        import pyttsx3
        print("🔊 Testing actual voice output...")
        
        engine = pyttsx3.init()
        
        # English
        print("\n🗣️ Speaking in English...")
        engine.say("Hello! I am JARVIS. I can speak with my voice!")
        engine.runAndWait()
        
        # Bengali
        print("🗣️ Speaking in Bengali...")
        engine.say("হ্যালো! আমি জার্ভিস। আমি আমার ভয়েস দিয়ে কথা বলতে পারি!")
        engine.runAndWait()
        
        print("✅ Voice output test completed!")
        
    except ImportError:
        print("⚠️ pyttsx3 not installed - voice output not available")
        print("💡 Install with: pip install pyttsx3")
    except Exception as e:
        print(f"⚠️ Voice output error: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 DEMO SUMMARY - ডেমো সারাংশ")
    print("="*70 + "\n")
    
    print("✅ JARVIS can speak:")
    print("   • English phrases")
    print("   • বাংলা বাক্য")
    print("   • Mixed language content")
    print("   • Programming code")
    print("   • Technical terms")
    print("   • System messages")
    print("   • Questions and responses")
    print("   • With personality and emojis")
    
    print("\n🎯 JARVIS is ready to communicate in any way you need!")
    print("🎯 জার্ভিস আপনার প্রয়োজন অনুযায়ী যেকোনো ভাবে যোগাযোগ করতে প্রস্তুত!")
    
    print("\n" + "="*70)
    print("✅ DEMO COMPLETED - ডেমো সম্পন্ন")
    print("="*70 + "\n")

if __name__ == "__main__":
    demo_jarvis_speech()
