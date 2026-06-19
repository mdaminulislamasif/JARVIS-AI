"""
Debug script to show when World AI Chat activates
এই script দেখাবে World AI Chat কখন activate হয়
"""

print("="*80)
print("🔍 WORLD AI CHAT ACTIVATION DEBUG")
print("="*80)

print("\n📋 World AI Chat activates in these scenarios:")
print("\n1️⃣ SCENARIO 1: No API Key")
print("   - User has no API key configured")
print("   - Brain is not connected")
print("   - Offline brain tries first")
print("   - If offline brain fails → World AI Chat activates")

print("\n2️⃣ SCENARIO 2: API Quota Exceeded")
print("   - User has API key but quota is exhausted")
print("   - Brain returns quota/limit error")
print("   - Offline brain tries first")
print("   - If offline brain fails → World AI Chat activates")

print("\n3️⃣ SCENARIO 3: Offline Brain Error")
print("   - Brain not connected")
print("   - Offline brain has an error")
print("   - World AI Chat activates as final fallback")

print("\n" + "="*80)
print("🧪 TESTING ACTIVATION CONDITIONS")
print("="*80)

# Check if jarvis_panel.py has the activation code
print("\n📂 Checking jarvis_panel.py for activation code...")

try:
    with open('jarvis_panel.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for activation points
    activation_points = {
        'Import Statement': 'from jarvis_world_ai_chat import WorldAIChat',
        'Initialization': 'self.world_ai_chat = WorldAIChat()',
        'Fallback Check': 'if self.world_ai_chat:',
        'AI Selector': 'show_ai_selector_dialog',
        'Chat Method': 'chat_with_ai',
        'Learning': 'learn_from_response',
        'No API Key Fallback': 'Brain NOT connected',
        'Quota Exceeded Fallback': 'QUOTA.*LIMIT',
    }
    
    print("\n✅ Activation Points Found:")
    for point, search_text in activation_points.items():
        if search_text in content:
            print(f"   ✅ {point}")
        else:
            print(f"   ⚠️ {point} - NOT FOUND")
    
    # Count how many times World AI Chat is referenced
    world_ai_count = content.count('world_ai_chat')
    print(f"\n📊 'world_ai_chat' mentioned {world_ai_count} times in jarvis_panel.py")
    
    # Check for the actual fallback code
    print("\n🔍 Checking fallback implementation...")
    
    fallback_checks = {
        'Offline Brain Try-Catch': 'except Exception as e:' in content and 'offline brain' in content.lower(),
        'World AI Chat Condition': 'if self.world_ai_chat:' in content,
        'AI Selection': 'selected_ai = self.world_ai_chat.show_ai_selector_dialog' in content,
        'Chat Execution': 'result = self.world_ai_chat.chat_with_ai' in content,
        'Learning Integration': 'learn_result = self.world_ai_chat.learn_from_response' in content,
    }
    
    all_present = True
    for check, result in fallback_checks.items():
        if result:
            print(f"   ✅ {check}")
        else:
            print(f"   ❌ {check} - MISSING!")
            all_present = False
    
    if all_present:
        print("\n✅ All fallback mechanisms are properly implemented!")
    else:
        print("\n⚠️ Some fallback mechanisms are missing!")
        print("\n🔧 Recommendation: Re-check jarvis_panel.py integration")
    
except Exception as e:
    print(f"❌ Error reading jarvis_panel.py: {e}")

print("\n" + "="*80)
print("📝 HOW TO TEST MANUALLY")
print("="*80)

print("""
1. Remove or rename jarvis_config.txt (to simulate no API key)
   
2. Start JARVIS:
   python jarvis_panel.py
   
3. Ask any question:
   "What is Python?"
   
4. Expected behavior:
   - JARVIS tries to use API → Fails (no key)
   - JARVIS tries Offline Brain → May fail
   - World AI Chat dialog appears
   - You select an AI (Gemini, ChatGPT, etc.)
   - Browser opens with AI website
   - Your question is in clipboard
   - You paste in AI, get response
   - You copy response back to JARVIS
   - JARVIS learns and shows output

5. If World AI Chat doesn't appear:
   - Check terminal for error messages
   - Run: python TEST_WORLD_AI_INTEGRATION.py
   - Check if all dependencies are installed
""")

print("\n" + "="*80)
print("🐛 COMMON ISSUES & SOLUTIONS")
print("="*80)

print("""
❌ Issue 1: Dialog doesn't appear
✅ Solution: Check if customtkinter is installed
   pip install customtkinter

❌ Issue 2: Browser doesn't open
✅ Solution: Check internet connection and default browser

❌ Issue 3: Clipboard doesn't work
✅ Solution: Install pyperclip
   pip install pyperclip

❌ Issue 4: Learning doesn't work
✅ Solution: Check if learning systems are available
   - Auto Background Learner
   - Offline Brain
   - Tree Learner

❌ Issue 5: "world_ai_chat not found" error
✅ Solution: Check if jarvis_world_ai_chat.py exists
   and is in the same directory as jarvis_panel.py
""")

print("\n" + "="*80)
print("✅ DEBUG COMPLETE")
print("="*80)

print("\n💡 Next Steps:")
print("1. Run: python TEST_WORLD_AI_INTEGRATION.py")
print("2. If all tests pass, try manual testing")
print("3. Check terminal logs for any errors")
print("4. If issues persist, check the error messages")

print("\n🚀 World AI Chat is ready to help when API keys fail!")
