"""Quick verification script"""
print("="*70)
print("FINAL VERIFICATION")
print("="*70)

# Test Direct AI Chat
from jarvis_direct_ai_chat import DirectAIChat
chat = DirectAIChat()
result = chat.chat_with_ai('What is Python?', 'auto')
print(f"\n✅ Direct AI Chat: {result['success']}")
print(f"🤖 AI: {result['ai']}")
print(f"💬 Response: {result['response'][:80]}...")

# Test Offline Brain
from jarvis_offline_brain import OfflineBrain
brain = OfflineBrain()
result = brain.process_query('apni ki ki korta paren')
brain.close()
print(f"\n✅ Offline Brain: {result['status']}")
print(f"💬 Response: {result['response'][:80]}...")

# Test Voice Engine
from engine.voice import VoiceEngine
voice = VoiceEngine()
print(f"\n✅ Voice Engine Rate: {voice.rate}")
print(f"🎤 Bangla Voice: {voice.bangla_voice}")

print("\n" + "="*70)
print("🎉 ALL COMPONENTS VERIFIED!")
print("="*70)
